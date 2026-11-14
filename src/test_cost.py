"""Known-answer tests for src/cost.py.

Run from the project folder: python -m src.test_cost
"""

import torch

from src import cost


def check(name, actual, wanted):
    """Stop with a clear message if a result is not the answer worked out by hand."""
    if isinstance(wanted, float):
        matches = abs(actual - wanted) < 0.000001
    else:
        matches = actual == wanted
    if not matches:
        raise ValueError(name + ": got " + str(actual) + ", wanted " + str(wanted))
    print("passed:", name)


scores = torch.tensor([1.0, 2.0, 3.0, 4.0])
labels = torch.tensor([False, False, True, True])

# A line at 2.5 rejects 3 and 4: no misses and no false rejects
miss_rate, false_reject_rate = cost.rates_at(scores, labels, 2.5)
check("miss rate at 2.5", miss_rate, 0.0)
check("false-reject rate at 2.5", false_reject_rate, 0.0)

# A line at 3.5 passes the defective 3: 1 of 2 defective missed
miss_rate, false_reject_rate = cost.rates_at(scores, labels, 3.5)
check("miss rate at 3.5", miss_rate, 0.5)

# Cost: 1 percent defects, all missed, ratio 10, no false rejects: 0.01 x 1 x 10 = 0.1
check("cost of passing everything", cost.expected_cost(1.0, 0.0, 0.01, 10), 0.1)
# Cost: rejecting everything throws away the 99 percent good parts: 0.99
check("cost of rejecting everything", cost.expected_cost(0.0, 1.0, 0.01, 10), 0.99)

# Line positions: below every score, halfway points, and above every score
check("lines", cost.candidate_thresholds(scores), [0.0, 1.5, 2.5, 3.5, 5.0])

# Perfectly separated scores: the cheapest line is 2.5, with no cost at all
best = cost.cheapest_threshold(scores, labels, 0.01, 10)
check("cheapest line", best["threshold"], 2.5)
check("cheapest cost", best["cost"], 0.0)

# Reversed scores and rare defects: passing everything (0.1) is cheaper than any line that rejects
reversed_scores = torch.tensor([4.0, 3.0, 2.0, 1.0])
best = cost.cheapest_threshold(reversed_scores, labels, 0.01, 10)
check("pass everything when ranking is wrong", best["threshold"], 5.0)
check("its cost", best["cost"], 0.1)

# Confusion counts at 3.5: passes 1, 2 and 3, rejects 4
counts = cost.confusion_counts(scores, labels, 3.5)
check("correct passes", counts["correct_passes"], 2)
check("missed defects", counts["missed_defects"], 1)
check("correct rejects", counts["correct_rejects"], 1)
check("false rejects", counts["false_rejects"], 0)

print("All tests passed")
