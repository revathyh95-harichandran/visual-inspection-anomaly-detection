# Final test findings: half B

**CRISP-DM stage:** Evaluation. **Data:** half B of the public test set, opened once, after the Lock (17 Nov 2026). These are the reported results. Nothing was changed after half B was seen.

The full numbers are in [final_results_table.md](final_results_table.md), [final_cost_main_setting.csv](final_cost_main_setting.csv), [final_cost_sensitivity.csv](final_cost_sensitivity.csv), [final_paired_differences.csv](final_paired_differences.csv), [final_secondary_metrics.csv](final_secondary_metrics.csv) and [lighting/lighting_by_config.csv](lighting/lighting_by_config.csv).

## 1. The runs repeated exactly

**34 of 34 runs repeat their locked half A numbers exactly**: the threshold, AU-PRO, pixel F1, image F1, AU-ROC and every flagged count. This covers every refitted model and the reused C8 students, as listed in [half_a_repeat_check.csv](half_a_repeat_check.csv). So any difference below comes from the photos, not from the models.

## 2. Half A did not predict half B well

| Image AU-ROC | Sheet Metal, half A → half B [95% interval] | Vial, half A → half B [95% interval] |
| --- | --- | --- |
| C1 PaDiM, ResNet-18 | 0.75 → 0.63 [0.52 to 0.73] | 0.74 → 0.61 [0.45 to 0.70] |
| C2 PaDiM, Wide ResNet-50 | 0.74 → **0.93** [0.77 to 1.0] | 0.69 → 0.67 [0.58 to 0.73] |
| C3 PaDiM, EfficientNet-B0 | 0.60 → 0.66 [0.61 to 0.71] | 0.53 → 0.56 [0.53 to 0.58] |
| C4 PatchCore, ResNet-18 | 0.65 → 0.59 [0.42 to 0.76] | 0.85 → 0.90 [0.76 to 0.99] |
| C5 PatchCore, Wide ResNet-50 | 0.80 → 0.65 [0.49 to 0.79] | 0.82 → 0.92 [0.86 to 0.98] |
| C6 PatchCore, EfficientNet-B0 | 0.77 → **0.52** [0.40 to 0.64] | 0.87 → 0.90 [0.78 to 0.98] |
| C7 WinCLIP | 0.75 → **0.17** [0.01 to 0.37] | 0.90 → **0.66** [0.37 to 0.91] |
| C8 Reverse Distillation | 0.85 → 0.88 [0.75 to 0.99] | 0.51 → **0.93** [0.82 to 1.0] |
| C6 at 512 | 0.75 → 0.63 [0.40 to 0.82] | 0.81 → 0.92 [0.79 to 0.99] |

- **Vial:** the PatchCore runs (C4, C5, C6 and C6 at 512) and C8 all land between 0.90 and 0.93. **C8 jumps from 0.51 to 0.93.** C7, the best on half A, falls to 0.66.
- **Sheet Metal:** most methods fall. C7 now ranks photos worse than chance (0.17), so its scores point the wrong way on these parts. Only C2 (0.93) and C8 (0.88) rank well.

## 3. The recommended combinations did not hold up

The cost is per part, at 1 percent defects with a miss costing 10 false rejects. Passing everything costs 0.10.

| Product | Locked recommendation | Half A cost | Half B cost | What happened on half B |
| --- | --- | --- | --- | --- |
| Sheet Metal | C6, cost-based line | 0.041 | **0.373** | 31 percent of good photos rejected and 71 percent of defects missed. Worse than passing everything |
| Vial | C7, cost-based line | 0.018 | **0.805** | 79 percent of good photos rejected. Worse than passing everything |

Following the Lock, **the recommendation is not changed**. It is reported as a recommendation that failed on new parts.

- **Cheapest at the locked lines on half B:**
  - **Sheet Metal:** C8 at 0.069, C6 at 512 at 0.065, and C2 at 0.029. C2 is the cheapest at 15 of the 18 business settings.
  - **Vial:** C6 and C6 at 512 at 0.046, and C4 at 0.050. C6 is the cheapest at 11 of the 18 business settings.
- **These are observations, not a new choice.** A choice made from half B could not be tested on any unseen photos.

## 4. Paired differences on half B (real only if the interval leaves out 0)

- **Real:**
  - Sheet Metal:
    - C2 above C1 on AU-ROC (+0.30).
    - C8 above C5 on AU-ROC (+0.23). For image F1 at the benchmark line, C8 is below C5 (−0.40).
    - C5 below C2 on AU-ROC (−0.27).
    - C7 below C5 on both AU-ROC and image F1.
  - Vial:
    - PatchCore above PaDiM, for both networks: C4 against C1 (+0.30) and C5 against C2 (+0.26).
    - C7 below C5 on AU-ROC (−0.27).
- **Not real:**
  - The network differences within PatchCore, for example C6 against C5: −0.13 on Sheet Metal and −0.02 on Vial.
  - **C6 at 512 against 256** on AU-ROC: +0.11 on Sheet Metal and +0.02 on Vial. On Vial, image F1 at the benchmark line is lower at 512 (−0.06, real).

## 5. Likely causes, judged by eye from the half B galleries and the lighting breakdown

These causes are my judgement from looking at the galleries, not something that was measured.

- **Too few good parts to set a line.** Each half has only 2 or 3 good parts. The cost-based lines were set just above half A's few good parts. Half B's good parts look different: on Sheet Metal they are darker, especially under shifted light, and on Vial, part 004 has a smaller printed code and less liquid. So the locked lines rejected many of them. With so few good parts, half A could not show this.
- **Lighting drift again.** On half B, a line set just above the good photos under regular light throws away, on average under the changed lightings:
  - **Sheet Metal:** between 40 percent (C2 and C8) and 90 percent (C3) of good photos.
  - **Vial:** between 39 percent (C4) and 92 percent (C2 and C3).

  This repeats the Phase 7 finding. The lighting groups have only 10 photos each, so these shares are rough.
- **WinCLIP scores the whole look of the object.** Good vials and sheets that look unusual score as high as defects, and its scores on Sheet Metal point the wrong way on these parts.
- **Reverse Distillation on Vial:** half A's good vials had many bubbles, which it flagged, and half B's good vials have fewer. This fits the bubble cause found in Phase 7.

## 6. What this means

- **The main lesson.** With 2 or 3 good test parts per half, half A results and thresholds were not stable enough to pick a winner. The half A intervals already warned about this: they were wide. The honest conclusion is that **no configuration is shown to be best on both products**.
- **What is consistent across both halves:**
  - PatchCore beats PaDiM on Vial.
  - C8 ranks Sheet Metal well.
  - Thresholds are the weak point.
  - Lighting changes hurt every method.
- **For a real line:**
  - Thresholds need many more good parts.
  - They need to be checked again after any change in lighting or product look.
  - This is part of the monitoring plan in the model card.
- **Pixel metrics:** these stay uncertain, because the masks were drawn by people.
