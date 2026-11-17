"""Shared code for the Final test: scoring half B once, after the Lock.

Every Final test notebook first fits its model and scores half A exactly as in
its earlier phase, so the half A numbers can be checked against the locked
ones. It then calls the functions here to score half B with the same model and
the same benchmark line. Nothing here chooses anything: lines and settings were
fixed in the Lock (DECISIONS.md, 17 Nov 2026).

CRISP-DM stage: evaluation.
"""

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import torch

from src import evaluate

# Half B parts, copied from outputs/results/02_exploration/half_b_files.csv.
# Every lighting version of each part is used, as for half A
HALF_B_PARTS = {
    "sheet_metal": {"good": ["000", "003"], "bad": ["001", "002", "003", "006", "008", "010", "011", "014"]},
    "vial": {"good": ["001", "004"], "bad": ["000", "002", "003", "004", "005", "006", "007", "009"]},
}
# Photo counts in half_b_files.csv, so a wrong selection stops the run
EXPECTED_HALF_B_PHOTOS = {"sheet_metal": 60, "vial": 70}


def half_b_positions(test_paths, product_name, half_a_positions, expected_count):
    """Return the positions of half B photos in the public test set.

    Stops the run if the count is wrong, or if any photo is also in half A.
    """
    positions = []
    for position in range(len(test_paths)):
        path = Path(test_paths[position])
        if path.stem.split("_")[0] in HALF_B_PARTS[product_name][path.parent.name]:
            positions.append(position)
    if len(positions) != expected_count:
        raise ValueError("Wrong number of half B photos for " + product_name + ": " + str(len(positions)))
    for position in positions:
        if position in half_a_positions:
            raise ValueError("A photo is in both halves: " + str(test_paths[position]))
    return positions


def labels_from_paths(paths):
    """Return True for each photo in a 'bad' folder, as a tensor."""
    labels = []
    for path in paths:
        labels.append(Path(path).parent.name == "bad")
    return torch.tensor(labels)


def save_half_b(results_folder, run_name, validation_maps, validation_scores, maps, scores, masks, paths,
                model_seconds, peak_gb):
    """Measure half B with the shared metrics, save the numbers, and return them.

    The benchmark line comes from the same good validation photos as for half A,
    so it is the locked line. The cost-based line is applied later, on the laptop,
    from the saved photo scores.
    """
    labels = labels_from_paths(paths)
    results = evaluate.evaluate(validation_maps, maps, scores, masks, labels, model_seconds, peak_gb)
    threshold = results["threshold"]
    results["run"] = run_name
    results["half"] = "B"
    results["half_b_photos"] = len(paths)
    results["defective_photos"] = int(labels.sum())
    results["good_validation_photos_flagged"] = int((validation_scores > threshold).sum())
    results["good_validation_photos"] = len(validation_scores)
    results["good_half_b_photos_flagged"] = int(((scores > threshold) & ~labels).sum())
    results["defective_half_b_photos_flagged"] = int(((scores > threshold) & labels).sum())
    # Secondary metrics for the appendix
    results["image_auprc"] = evaluate.image_auprc(scores, labels)
    results["pixel_average_precision"] = evaluate.pixel_average_precision(maps, masks)

    # A separate folder, so half B files can never be mistaken for half A ones
    folder = Path(results_folder) / "half_b"
    folder.mkdir(parents=True, exist_ok=True)
    # Numbers only, with no image content, so these files can be committed
    with open(folder / (run_name + "_halfB_metrics.json"), "w") as file:
        json.dump(results, file, indent=1)
    with open(folder / (run_name + "_halfB_photo_scores.csv"), "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["file_name", "label", "score", "above_threshold"])
        for position in range(len(paths)):
            writer.writerow([Path(paths[position]).name, Path(paths[position]).parent.name,
                             round(float(scores[position]), 6), bool(scores[position] > threshold)])
    print("Half B,", run_name)
    for key in results:
        print(" ", key, results[key])
    return results


def failure_gallery(file_name, title, dataset, positions, recipe, maps, scores, masks, paths):
    """Draw the 2 highest-scoring defective photos, the 4 lowest-scoring defective and the 4 highest-scoring good.

    The same picking rule as in Phases 6 to 8. It only describes the locked
    results and leads to no change. Returns the picks as rows for a csv file.
    """
    labels = labels_from_paths(paths)
    defective = []
    good = []
    for position in range(len(paths)):
        if labels[position]:
            defective.append(position)
        else:
            good.append(position)

    def score_of(position):
        return float(scores[position])

    defective.sort(key=score_of)
    good.sort(key=score_of)
    picked = []
    for position in defective[-2:]:
        picked.append(("hit", position))
    for position in defective[:4]:
        picked.append(("hardest defective", position))
    for position in good[-4:]:
        picked.append(("hardest good", position))

    # Undo the normalisation, so the photo looks as it did before preparation
    normalize_step = recipe.transforms[1]
    means = torch.tensor(normalize_step.mean).view(3, 1, 1)
    stds = torch.tensor(normalize_step.std).view(3, 1, 1)
    top = float(maps.max())
    bottom = float(maps.min())
    rows = []
    figure, axes = plt.subplots(len(picked), 2, figsize=(8, 3.6 * len(picked)), squeeze=False)
    for row_number in range(len(picked)):
        kind, position = picked[row_number]
        path = Path(paths[position])
        photo = recipe(dataset[positions[position]].image)
        photo = (photo * stds + means).clamp(0, 1)
        mask = masks[position].float()
        axes[row_number][0].imshow(photo[0], cmap="gray", vmin=0, vmax=1)
        axes[row_number][1].imshow(maps[position], cmap="Blues", vmin=bottom, vmax=top)
        if bool(mask.any()):
            axes[row_number][0].contour(mask, levels=[0.5], colors="red", linewidths=0.8)
            axes[row_number][1].contour(mask, levels=[0.5], colors="red", linewidths=0.8)
        axes[row_number][0].set_title(kind + ": " + path.parent.name + " " + path.name, fontsize=9)
        axes[row_number][1].set_title("score " + str(round(float(scores[position]), 3)), fontsize=9)
        axes[row_number][0].axis("off")
        axes[row_number][1].axis("off")
        rows.append([kind, path.parent.name, path.name, round(float(scores[position]), 6)])
    figure.suptitle(title, y=1.0)
    figure.tight_layout()
    figure.savefig(file_name, dpi=120, bbox_inches="tight")
    # Closing without showing keeps dataset images out of the notebook's log
    plt.close(figure)
    return rows


def save_failure_picks(results_folder, file_stem, rows):
    """Save the gallery picks as numbers and names only, so they can be committed."""
    folder = Path(results_folder) / "half_b"
    folder.mkdir(parents=True, exist_ok=True)
    with open(folder / (file_stem + "_halfB_failure_picks.csv"), "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["run", "kind", "label", "file_name", "score"])
        for row in rows:
            writer.writerow([file_stem] + row)
