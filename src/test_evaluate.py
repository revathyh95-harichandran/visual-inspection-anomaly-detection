"""Known-answer tests for src/evaluate.py.

Each test uses small made-up numbers whose answers are worked out by hand. The
last test recomputes C1's image F1 and image AU-ROC from its saved photo
scores, to check this file matches the C1 notebook.

Run from the project folder: python -m src.test_evaluate
"""

import csv
from pathlib import Path

import torch

from src import evaluate


def check(name, actual, wanted):
    """Stop with a clear message if a result is not the answer worked out by hand."""
    if isinstance(wanted, float):
        matches = abs(actual - wanted) < 0.0001
    else:
        matches = actual == wanted
    if not matches:
        raise ValueError(name + ": got " + str(actual) + ", wanted " + str(wanted))
    print("passed:", name)


# Threshold: values 1, 2, 3 have mean 2 and standard deviation 1, so 2 + 3 x 1 = 5
check("threshold", evaluate.benchmark_threshold(torch.tensor([[[1.0, 2.0, 3.0]]])), 5.0)

# F1: 1 right alarm, 1 false alarm, 1 miss gives 2 / (2 + 1 + 1) = 0.5
flagged = torch.tensor([True, True, False, False])
actual = torch.tensor([True, False, True, False])
check("F1", evaluate.f1_from_flags(flagged, actual), 0.5)

# F1 with nothing flagged and nothing to find is 0
check("F1 with nothing", evaluate.f1_from_flags(torch.tensor([False]), torch.tensor([False])), 0.0)

# AU-ROC on scores above 1, perfectly ordered, must be 1.0, not 0.5
scores = torch.tensor([20.0, 30.0, 40.0, 50.0])
labels = torch.tensor([False, False, True, True])
check("AU-ROC above 1", evaluate.image_auroc(scores, labels), 1.0)

# AU-ROC with only defective photos cannot be calculated
check("AU-ROC one kind", evaluate.image_auroc(scores, torch.tensor([True, True, True, True])), "not defined")

# A shape mismatch must stop the run, like the column-of-scores bug in Phase 4
try:
    evaluate.f1_from_flags(torch.ones(4, 1, dtype=torch.bool), torch.ones(4, dtype=torch.bool))
    raise RuntimeError("A shape mismatch was not caught")
except ValueError:
    print("passed: shape mismatch is caught")

# A good photo with a mask must stop the run
maps = torch.zeros(2, 4, 4)
masks = torch.zeros(2, 4, 4, dtype=torch.bool)
masks[0, 1, 1] = True
try:
    evaluate.check_inputs(maps, torch.tensor([1.0, 2.0]), masks, torch.tensor([False, False]))
    raise RuntimeError("A mask on a good photo was not caught")
except ValueError:
    print("passed: mask on a good photo is caught")

# A full made-up evaluation: perfect maps must give perfect pixel and image F1
validation = torch.zeros(3, 4, 4)
test_masks = torch.zeros(2, 4, 4, dtype=torch.bool)
test_masks[0, 0:2, 0:2] = True
test_maps = test_masks.float() * 10
test_scores = torch.tensor([10.0, 0.0])
test_labels = torch.tensor([True, False])
results = evaluate.evaluate(validation, test_maps, test_scores, test_masks, test_labels, 0.2, "no gpu")
check("threshold of all zeros", results["threshold"], 0.0)
check("perfect pixel F1", results["pixel_f1"], 1.0)
check("perfect image F1", results["image_f1"], 1.0)
check("perfect AU-ROC", results["image_au_roc"], 1.0)
check("seconds per photo", results["seconds_per_photo"], 0.1)

# C1's saved photo scores must give the same image metrics as the C1 notebook
scores_file = Path("outputs/results/04_padim_baseline/c1_sheet_metal_photo_scores.csv")
c1_scores = []
c1_labels = []
with open(scores_file, newline="") as file:
    for row in csv.DictReader(file):
        c1_scores.append(float(row["score"]))
        c1_labels.append(row["label"] == "bad")
c1_scores = torch.tensor(c1_scores)
c1_labels = torch.tensor(c1_labels)
c1_threshold = 19.6001
check("C1 image F1", round(evaluate.f1_from_flags(c1_scores > c1_threshold, c1_labels), 4), 0.8842)
check("C1 image AU-ROC", round(evaluate.image_auroc(c1_scores, c1_labels), 4), 0.75)

# Bootstrap: drawn parts keep the same numbers of good and defective parts
import random
drawn = evaluate.draw_parts(["good_1", "good_2"], ["defective_1", "defective_2", "defective_3"], random.Random(1))
good_drawn = [part for part in drawn if part.startswith("good")]
check("parts drawn", len(drawn), 5)
check("good parts drawn", len(good_drawn), 2)

# Bootstrap: perfectly separated scores give the same answer in every draw, so the interval has no width
names = ["001_regular.png", "001_shift_1.png", "002_regular.png", "003_regular.png", "004_regular.png"]
perfect_labels = torch.tensor([False, False, False, True, True])
perfect_scores = torch.tensor([1.0, 1.0, 2.0, 10.0, 20.0])
intervals = evaluate.bootstrap_image_metrics([perfect_scores, perfect_scores], [5.0, 5.0], perfect_labels, names)
check("interval F1 low", intervals["image_f1_low"], 1.0)
check("interval F1 high", intervals["image_f1_high"], 1.0)
check("interval AU-ROC low", intervals["image_au_roc_low"], 1.0)
check("good parts counted", intervals["good_parts"], 2)
check("defective parts counted", intervals["defective_parts"], 2)

# Paired difference: a configuration compared with itself has a gap of 0 in every draw
same = ([perfect_scores], [5.0])
gap = evaluate.paired_bootstrap_difference(same, same, perfect_labels, names)
check("paired gap", gap["image_au_roc_difference"], 0.0)
check("paired gap low", gap["image_au_roc_difference_low"], 0.0)
check("paired gap high", gap["image_f1_difference_high"], 0.0)

# Paired difference: perfect scores against reversed scores gives an AU-ROC gap of 1 - 0 = 1
reversed_scores = torch.tensor([20.0, 20.0, 10.0, 2.0, 1.0])
gap = evaluate.paired_bootstrap_difference(same, ([reversed_scores], [5.0]), perfect_labels, names)
check("paired AU-ROC gap", gap["image_au_roc_difference"], 1.0)

# Image AUPRC: sorted from most suspicious, 0.8 is defective (precision 1/1), 0.4 is good,
# 0.35 is defective (precision 2/3). The average of 1 and 2/3 is 0.8333
check("image AUPRC", evaluate.image_auprc(torch.tensor([0.1, 0.4, 0.35, 0.8]),
                                          torch.tensor([False, False, True, True])), 0.8333)
check("image AUPRC one kind", evaluate.image_auprc(scores, torch.tensor([True, True, True, True])), "not defined")

# Precision and recall: the line 1.5 rejects scores 2, 3 and 4. Two of these are defective,
# so precision is 2/3, and both defective photos are rejected, so recall is 1
counts = evaluate.precision_recall_at(torch.tensor([1.0, 2.0, 3.0, 4.0]),
                                      torch.tensor([False, True, False, True]), 1.5)
check("precision", counts["precision"], 0.6667)
check("recall", counts["recall"], 1.0)
# A line above every score rejects nothing, so precision has no bottom number
counts = evaluate.precision_recall_at(torch.tensor([1.0, 2.0]), torch.tensor([False, True]), 10.0)
check("precision with nothing rejected", counts["precision"], "not defined")
check("recall with nothing rejected", counts["recall"], 0.0)

# Pixel average precision: both defect pixels score above both clean pixels, so it is 1.0
pixel_maps = torch.tensor([[[0.9, 0.1], [0.8, 0.2]]])
pixel_masks = torch.tensor([[[True, False], [True, False]]])
check("pixel average precision", evaluate.pixel_average_precision(pixel_maps, pixel_masks), 1.0)

print("All tests passed")
