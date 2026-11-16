# Phase 6 failure analysis on half A: likely causes

**CRISP-DM stage:** Evaluation.

**Source:** `notebooks/06_failure_maps_cpu.ipynb` (run R027 on Kaggle, processor only, seed 42, half A only). The galleries are in `outputs/figures/gallery_failures_*.png`. They are kept out of git because they show dataset photos. The photo names and scores are in `failure_picks.csv`.

**How the photos were picked:** for each configuration and product, the 2 defective photos with the highest scores (hits), the 4 defective photos with the lowest scores (hardest defective), and the 4 good photos with the highest scores (hardest good). They are picked by score, not by where a line sits.

**Check that these are the measured runs:** PaDiM scores match Phase 5 seed 42 within 1%. PatchCore scores differ by up to 6%, because the processor draws different random numbers from the GPU when choosing the memory sample, even with the same seed. The same parts come out as hardest in almost every case (3 or 4 of 4 for every seed, except C4 Vial with 2 of 4, where the swaps are the same parts under another lighting).

**Caution:** a heat map shows where the model looked, not whether it was right to. The causes below are judged by eye from the photos and maps. They are likely causes, not proven ones, and are for you to review.

## Grouped causes

| # | Likely cause | Product | Configurations | Photos | What the map shows |
|---|---|---|---|---|---|
| 1 | **Lighting change makes good parts look unusual** | Vial | C1, C2, C4, C5 | Good 000, 002, 003 underexposed; 003 and 000 overexposed; 003 shift_3 | These are the top false alarms for every configuration. PaDiM lights up the bright background to the right of the tube. PatchCore lights up the whole tube and background. Nothing in the part is wrong. |
| 2 | **Right answer for the wrong reason** | Vial | C1, C2 (PaDiM) | Hits: bad 008 underexposed, 013 underexposed | PaDiM's two highest-scored defective photos are high because of the same background glow as in cause 1, not because of the defect. The red mask area itself is pale. So PaDiM's Vial hits are partly a "dark photo" detector. |
| 3 | **Lighting change on Sheet Metal** | Sheet Metal | C1, C4, C5 | Good 001 and 002, shift_1, shift_2, shift_3 | The hardest good photos are the shifted-lighting versions. The map is raised over the whole sheet, or at the borders and corners, with no single spot. |
| 4 | **Normal texture variation between good parts** | Sheet Metal | C2 (and partly all) | Good 001 regular, overexposed, shift_1, shift_2 | The heat is spread as many small spots across the whole sheet. The sheet's random texture differs from part to part, so a good part can look as unusual as a defective one. |
| 5 | **Long, thin defect along the sheet's edge** | Sheet Metal | C1, C2, C5 | Bad 007, all lightings | The defect runs down the left edge, where the sheet meets the background strip. The map stays pale there. It is very thin after shrinking to 256, and it sits on a strong edge the model already sees on every good part. |
| 6 | **Thin scratches or tiny marks** | Sheet Metal | C1, C4, C5 | Bad 005 (several thin lines), 012 (one tiny mark), 009 (thin cluster) | The maps show nothing at the marks. At 256 pixels these are only one or two pixels wide. This matches the Phase 2 finding that many Sheet Metal defects are very small. |
| 7 | **Tiny defect at the vial's tip** | Vial | C2, C4, C5 | Bad 011, all lightings | The defect is a small spot at the tip. The model lights up the tube body full of bubbles more than the tip. The defect is small, and the bubbles and clear plastic already vary a lot on good parts. |
| 8 | **Large, faint area in the label region** | Vial | C1, C2 | Bad 008 (regular, shift_2), 012, 013 shift_3 | The mask covers a large area of the tube, but the photo shows no clear mark to the eye, and the map is pale. **Unclear:** I can't tell from the photo what the defect looks like, so I'm not guessing a cause. |
| 9 | **Defect near the cap at the top edge** | Vial | C4 | Bad 014 shift_3 | Part of the mask is on the cap at the top of the photo. The map lights up the tube body instead. Possibly the same as cause 1 (lighting) plus the defect being at the photo edge. Unclear. |

## Hits for the right reason

- **Sheet Metal 013** (all four configurations): the bright, raised mark near the top is clearly lit up. The long diagonal mask on the right is only partly lit.
- **Vial 001** (C4, C5, PatchCore): the dark spot at the bottom of the tube is the darkest place on the map.

## What this tells us

- **Lighting is the biggest single cause of false alarms on both products, for every configuration.** On Vial it also inflates PaDiM's "hits". The Phase 7 lighting test was planned for this question, and the rule there is to report lighting results as a finding, not to tune them away on test data.
- **Small and thin defects are the main cause of misses** on Sheet Metal (causes 5 and 6) and on Vial (cause 7). This points to image size, which the Phase 8 resolution test at 512 was planned to check, with Sheet Metal first.
- **PatchCore's hits are more often for the right reason than PaDiM's** on Vial. This fits C4 and C5 being ranked higher on Vial in Phase 5, but it is a judgement from a few photos, not a measurement.
- **Limits:** one seed, 10 photos per configuration and product, half A only, and the grouping is by eye.
