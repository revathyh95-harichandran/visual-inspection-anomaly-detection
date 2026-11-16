# Phase 7 failure analysis on half A: likely causes for C3, C6, C7 and C8

**CRISP-DM stage:** Evaluation

This continues `outputs/results/06_evaluation/failure_causes.md`, which covers C1, C2, C4 and C5. The method is the same. Each Phase 7 run saved a failure gallery, `outputs/figures/gallery_failures_{config}_{product}.png` (kept out of git because it shows dataset photos). Each gallery has 2 hits, 4 hardest defective photos and 4 hardest good photos, chosen by score, for PatchCore with seed 42 only. The picks are listed in `outputs/results/07_core/{config}/..._failure_picks.csv`.

The causes are **likely**, not proven. They come from looking at the heat maps and the scores. Only a few photos were chosen per run, and half A has only 2 or 3 good parts per product.

## Grouped causes

| # | Likely cause | Product | Configurations | Photos | What the map and scores show |
|---|---|---|---|---|---|
| 1 | **The score measures the lighting, not the part** (new, the strongest case so far) | Sheet Metal, Vial | C3 (PaDiM, EfficientNet-B0) | Sheet Metal: every photo under shift_1, shift_2 or shift_3. Vial: every photo under underexposed | On Sheet Metal, every photo under regular, overexposed or underexposed light scores about 30 to 71. Every photo under shift_1 to shift_3 scores about 123 to 144, good or defective. On Vial, underexposed photos score about 400 and most others about 20 to 220. The map lights up the same background area on the right of every underexposed vial, not the vial. This is why C3's AU-ROC is the lowest (0.60 and 0.53). Its "hits" are hits for the wrong reason: the lighting pushed them up |
| 2 | **Lighting change makes good parts look unusual** (same as Phase 6 cause 1 and 3) | Sheet Metal, Vial | C6, C7 | C6 Sheet Metal: good 001 and 002 under shift_1 and shift_2. C6 Vial: good 000, 002, 003 underexposed, 003 shift_4. C7 Vial: good 000 and 003 under shift_1, shift_2, shift_4 | The hardest good photos are almost all changed-light photos, as in Phase 6 |
| 3 | **Bubbles and the printed code on good vials look like defects** (new) | Vial | C8 (Reverse Distillation) | Good 000 and 002 under shift_1 and shift_4 | The student fails to copy the teacher around the many air bubbles and the dense printed code. Those are normal on a good vial, but they vary from part to part. Every hardest good photo scores 0.60, above most defective photos. This is the main reason C8's Vial AU-ROC is only 0.51 |
| 4 | **Normal variation of the good part's printed code and bubbles** | Vial | C7 (WinCLIP) | Good 003 and 000 | WinCLIP's map is coarse and roughly the shape of the whole vial. It does not point to one spot, so it cannot separate a defect from normal busy areas |
| 5 | **Large, faint area in the label region** (same as Phase 6 cause 8) | Vial | C3, C7, C8 | Bad 008 (all three), 012 (C8), 010 regular and shift_3 (C3) | The mask covers a large part of the tube, but the map is pale there. A large faint change is hard for every method |
| 6 | **Tiny defect at the vial's tip** (same as Phase 6 cause 7) | Vial | C6 | Bad 011, four lightings | Same as Phase 6 |
| 7 | **Long, thin defect along the sheet's edge** (same as Phase 6 cause 5) | Sheet Metal | C8 | Bad 007, regular, overexposed, underexposed | The defect runs down the left edge. The map is pale there. Reverse Distillation also misses it |
| 8 | **Thin scratches or tiny marks** (same as Phase 6 cause 6) | Sheet Metal | C3, C6, C7, C8 | Bad 012 (one tiny mark), 005 (thin lines, C7), 000, 004 | The mark is a few pixels wide after shrinking to 256 (240 for WinCLIP). The map shows nothing there |
| 9 | **Normal texture variation between good parts** (same as Phase 6 cause 4) | Sheet Metal | C7, C8 | C7: good 002 in four lightings. C8: good 001 in four lightings | The map is spread across the whole sheet, with no single hot spot |

## Hits for the right reason

- **Sheet Metal, bad 013** is caught by C6, C7 and C8, and the map's hottest area sits on the defect in each case. For C8, both the small mark in the middle and the line at the right edge light up.
- **Vial, bad 010** is caught by C7 and C8, with the heat on the marked defect.
- **Vial, bad 001** is C6's top hit, under overexposed and underexposed light. The darkest spot of the map sits on the marked defect near the tip.

## Hits for the wrong reason

- **C3, all its hits** (Sheet Metal 007 and 012 under shift_2; Vial 010 and 008 underexposed). The map lights up the background, not the defect. The score is high because of the light (cause 1).

## What this tells us

- **Lighting is still the biggest cause of false alarms,** now for 7 of the 8 configurations. C3 shows the extreme case: its score is mostly a lighting measure.
- **Reverse Distillation (C8) behaves differently on the two products.** On Sheet Metal its map points at real defects and it is the least thrown by light changes (see `outputs/results/07_lighting/lighting_by_config.csv`). On Vial it reacts to normal bubbles and print, so it barely ranks at all.
- **Small, thin or faint defects are missed by every method,** which points to the image size (256 pixels) as one likely cause. This is what the Phase 8 resolution test checks.
