"""The business side: what each pass-or-fail line costs.

CRISP-DM stage: evaluation.

A false reject (a good part thrown away) counts as 1. A missed defect (a
defective part shipped) counts as the cost ratio, 10 by the project's
business assumption. The defect rate says how often defects happen on the
production line, which is far lower than in the test photos.
"""

# A false reject is the unit of cost, so it counts as 1
FALSE_REJECT_COST = 1.0
# The project's business assumptions, tested over these ranges
COST_RATIOS = [2, 5, 10, 20, 50, 100]
DEFECT_RATES = [0.001, 0.01, 0.10]
MAIN_COST_RATIO = 10
MAIN_DEFECT_RATE = 0.01


def rates_at(scores, labels, threshold):
    """Return the miss rate and false-reject rate when photos above the line are rejected.

    Miss rate: the share of defective photos that pass.
    False-reject rate: the share of good photos that are rejected.
    """
    rejected = scores > threshold
    defective_count = int(labels.sum())
    good_count = int((~labels).sum())
    misses = int((~rejected & labels).sum())
    false_rejects = int((rejected & ~labels).sum())
    return misses / defective_count, false_rejects / good_count


def expected_cost(miss_rate, false_reject_rate, defect_rate, cost_ratio):
    """Return the expected cost per part on the production line.

    cost = defect rate x miss rate x cost ratio + (1 - defect rate) x false-reject rate x 1
    """
    missed_cost = defect_rate * miss_rate * cost_ratio
    rejected_cost = (1 - defect_rate) * false_reject_rate * FALSE_REJECT_COST
    return missed_cost + rejected_cost


def candidate_thresholds(scores):
    """Return every useful line position, from rejecting everything to passing everything.

    Lines sit halfway between neighbouring scores, so a line chosen on one set
    of photos does not sit exactly on a score. One line sits below every score
    (reject everything) and one above every score (pass everything).
    """
    distinct = sorted(set(scores.tolist()))
    lines = [distinct[0] - 1.0]
    for position in range(len(distinct) - 1):
        lines.append((distinct[position] + distinct[position + 1]) / 2)
    lines.append(distinct[-1] + 1.0)
    return lines


def cheapest_threshold(scores, labels, defect_rate, cost_ratio):
    """Return the line with the lowest expected cost, its cost and its two error rates.

    Lines are tried from the highest down, and a lower line replaces the best
    so far only if it is strictly cheaper. So when two lines cost the same, the
    one rejecting fewer parts is kept.
    """
    lines = candidate_thresholds(scores)
    lines.reverse()
    best = None
    for line in lines:
        miss_rate, false_reject_rate = rates_at(scores, labels, line)
        cost = expected_cost(miss_rate, false_reject_rate, defect_rate, cost_ratio)
        if best is None or cost < best["cost"]:
            best = {"threshold": line, "cost": cost, "miss_rate": miss_rate, "false_reject_rate": false_reject_rate}
    return best


def cost_at(scores, labels, threshold, defect_rate, cost_ratio):
    """Return the expected cost and error rates of a given line."""
    miss_rate, false_reject_rate = rates_at(scores, labels, threshold)
    cost = expected_cost(miss_rate, false_reject_rate, defect_rate, cost_ratio)
    return {"threshold": threshold, "cost": cost, "miss_rate": miss_rate, "false_reject_rate": false_reject_rate}


def confusion_counts(scores, labels, threshold):
    """Return correct passes, correct rejects, false rejects and missed defects."""
    rejected = scores > threshold
    return {
        "correct_passes": int((~rejected & ~labels).sum()),
        "correct_rejects": int((rejected & labels).sum()),
        "false_rejects": int((rejected & ~labels).sum()),
        "missed_defects": int((~rejected & labels).sum()),
    }
