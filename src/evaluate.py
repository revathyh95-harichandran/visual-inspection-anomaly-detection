"""One shared way to measure every configuration.

CRISP-DM stage: modelling, with the measurements reused in evaluation.

Every configuration is measured with these functions, so results can be
compared fairly. Where anomalib already does the job safely, its code is used.
Our own code covers only what anomalib does not provide, or does not handle
safely on raw scores: the benchmark threshold, F1, timing and memory.
"""

import random
import time

import numpy
import torch
from anomalib.metrics.aupro import _AUPRO
from sklearn.metrics import roc_auc_score

# The benchmark's rule: mean plus 3 standard deviations of good validation pixels
STD_MULTIPLIER = 3
# The benchmark reports AU-PRO at these two false-alarm limits
FALSE_POSITIVE_LIMITS = [0.05, 0.30]


def benchmark_threshold(validation_maps):
    """Return the mean plus 3 standard deviations of every good validation pixel.

    The MVTec AD 2 paper sets its threshold this way, from per-pixel values of
    good validation photos. It does not clearly say whether pixels are pooled,
    so all pixels are pooled here, which is the simpler reading.
    """
    values = validation_maps.flatten().double()
    return float(values.mean() + STD_MULTIPLIER * values.std())


def f1_from_flags(flagged, actual):
    """Return F1 from true or false flags and true or false answers.

    F1 balances catching defects against false alarms:
    2 x right alarms / (2 x right alarms + false alarms + misses).
    It returns 0 if nothing was flagged and nothing was there to find.
    """
    if flagged.shape != actual.shape:
        raise ValueError("Flags and answers differ in shape: " + str(list(flagged.shape)) + ", " + str(list(actual.shape)))
    right_alarms = int((flagged & actual).sum())
    false_alarms = int((flagged & ~actual).sum())
    misses = int((~flagged & actual).sum())
    bottom = 2 * right_alarms + false_alarms + misses
    if bottom == 0:
        return 0.0
    return 2 * right_alarms / bottom


def aupro(maps, masks, limit):
    """Return AU-PRO up to one false-alarm limit, using anomalib's calculation.

    `_AUPRO` is the calculation inside anomalib's metric. It is used directly
    because this project works with plain numbers, not anomalib's batch objects.
    It was checked to give the same answer whatever the size of the scores.
    """
    metric = _AUPRO(fpr_limit=limit)
    metric.update(maps, masks.long())
    return float(metric.compute())


def image_auroc(scores, labels):
    """Return image AU-ROC, or "not defined" if only one kind of photo is present.

    scikit-learn's `roc_auc_score` uses only the order of scores. Both
    torchmetrics' and anomalib's AU-ROC squash scores outside 0 to 1 with a
    sigmoid, so raw scores all become ties and give 0.5.
    """
    if labels.all() or not labels.any():
        return "not defined"
    return float(roc_auc_score(labels.int().tolist(), scores.tolist()))


def wait_for_gpu():
    """Wait for the GPU to finish, if there is one."""
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def start_timer():
    """Note the time, after earlier GPU work has finished."""
    wait_for_gpu()
    return time.perf_counter()


def stop_timer(started):
    """Return the seconds since `start_timer`, after the GPU has finished."""
    wait_for_gpu()
    return time.perf_counter() - started


def reset_peak_memory():
    """Start a new peak GPU memory measurement."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()


def peak_memory_gb():
    """Return the most GPU memory used since the last reset, or "no gpu"."""
    if torch.cuda.is_available():
        return round(torch.cuda.max_memory_allocated() / 1e9, 3)
    return "no gpu"


def check_inputs(maps, scores, masks, labels):
    """Stop with a clear error if the inputs do not line up.

    A shape mismatch can give believable but wrong results with no error, as
    found in Phase 4, so these checks come before any metric.
    """
    if maps.ndim != 3:
        raise ValueError("Maps must be shaped [photos, height, width], got " + str(list(maps.shape)))
    if maps.shape != masks.shape:
        raise ValueError("Maps and masks differ in shape: " + str(list(maps.shape)) + ", " + str(list(masks.shape)))
    if scores.shape != labels.shape or scores.shape[0] != maps.shape[0]:
        raise ValueError("Scores, labels and maps do not line up: " + str(list(scores.shape)) + ", "
                         + str(list(labels.shape)) + ", " + str(list(maps.shape)))
    for position in range(len(labels)):
        has_defect_pixels = bool(masks[position].any())
        if has_defect_pixels != bool(labels[position]):
            raise ValueError("Photo " + str(position) + " has a mask that does not fit its label")


def evaluate(validation_maps, maps, scores, masks, labels, model_seconds, peak_gb):
    """Measure one configuration on one set of test photos.

    validation_maps: anomaly maps of good validation photos, for the threshold.
    maps, scores, masks, labels: anomaly maps, photo scores, true or false
    masks, and true for defective photos, all for the same test photos.
    model_seconds: time the model spent on these photos.
    peak_gb: peak GPU memory while scoring them.
    """
    check_inputs(maps, scores, masks, labels)
    threshold = benchmark_threshold(validation_maps)

    results = {"threshold": threshold}
    for limit in FALSE_POSITIVE_LIMITS:
        results["au_pro_" + str(round(limit * 100)) + "_percent"] = aupro(maps, masks, limit)
    results["pixel_f1"] = f1_from_flags(maps > threshold, masks)
    # The paper rejects a photo if any pixel is above the line, which is its score being above the line
    results["image_f1"] = f1_from_flags(scores > threshold, labels)
    results["flag_everything_image_f1"] = f1_from_flags(torch.ones_like(labels), labels)
    results["image_au_roc"] = image_auroc(scores, labels)
    results["seconds_per_photo"] = model_seconds / len(scores)
    results["peak_gpu_gb"] = peak_gb
    return results


# Enough draws for a steady 95 percent interval. More would barely change it
BOOTSTRAP_DRAWS = 2000
BOOTSTRAP_SEED = 42
# The middle 95 percent of the draws
INTERVAL_LOW = 2.5
INTERVAL_HIGH = 97.5


def part_number(file_name):
    """Return the part number from a name such as 004_shift_1.png."""
    return file_name.split("_")[0]


def draw_parts(good_parts, defective_parts, generator):
    """Draw good and defective parts separately, with repeats, keeping their numbers.

    Drawing the two groups separately means every draw has both good and
    defective parts, so AU-ROC can always be calculated.
    """
    drawn = []
    for parts in [good_parts, defective_parts]:
        for count in range(len(parts)):
            drawn.append(generator.choice(parts))
    return drawn


def bootstrap_image_metrics(score_lists, thresholds, labels, file_names):
    """Return 95 percent bootstrap intervals for image F1 and image AU-ROC.

    score_lists and thresholds hold one entry per seed, all for the same photos.
    Parts are drawn, not photos, because the photos of one part under different
    lights are not independent. In each draw, each metric is worked out for every
    seed on the same parts, then averaged over seeds.
    """
    # Good and defective parts can share a number, so the label is part of the name
    photos_of_part = {}
    good_parts = []
    defective_parts = []
    for position in range(len(file_names)):
        label = "defective" if bool(labels[position]) else "good"
        part = label + "_" + part_number(file_names[position])
        if part not in photos_of_part:
            photos_of_part[part] = []
            if label == "good":
                good_parts.append(part)
            else:
                defective_parts.append(part)
        photos_of_part[part].append(position)

    generator = random.Random(BOOTSTRAP_SEED)
    f1_values = []
    auroc_values = []
    for draw_number in range(BOOTSTRAP_DRAWS):
        positions = []
        for part in draw_parts(good_parts, defective_parts, generator):
            positions.extend(photos_of_part[part])
        chosen = torch.tensor(positions)

        f1_total = 0.0
        auroc_total = 0.0
        for seed_number in range(len(score_lists)):
            scores = score_lists[seed_number][chosen]
            drawn_labels = labels[chosen]
            f1_total = f1_total + f1_from_flags(scores > thresholds[seed_number], drawn_labels)
            auroc_total = auroc_total + image_auroc(scores, drawn_labels)
        f1_values.append(f1_total / len(score_lists))
        auroc_values.append(auroc_total / len(score_lists))

    return {
        "image_f1_low": float(numpy.percentile(f1_values, INTERVAL_LOW)),
        "image_f1_high": float(numpy.percentile(f1_values, INTERVAL_HIGH)),
        "image_au_roc_low": float(numpy.percentile(auroc_values, INTERVAL_LOW)),
        "image_au_roc_high": float(numpy.percentile(auroc_values, INTERVAL_HIGH)),
        "good_parts": len(good_parts),
        "defective_parts": len(defective_parts),
    }
