# Resolution test: C6 at 512 against 256 pixels

**CRISP-DM stage:** Evaluation. **Data:** half A of the public test set only, so these are development numbers, not final results. Half B was not read.

**Setup:** C6 is PatchCore with EfficientNet-B0. It ran with seeds 42, 43 and 44 at both sizes, and every setting except the image size stayed the same. The 256 numbers are reused from Phase 7. Each value is the mean over 3 seeds, with the spread in brackets. The full tables are in [resolution_table.csv](resolution_table.csv) and [resolution_paired_differences.csv](resolution_paired_differences.csv).

| Product | Size | AU-PRO 5% | AU-PRO 30% | Pixel F1 | Image F1 | Image AU-ROC | Seconds per photo | Fitting time | Peak GPU while fitting |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sheet Metal | 256 | 0.072 (0.009) | 0.278 (0.016) | 0.199 (0.009) | 0.876 (0.023) | 0.774 (0.018) | 0.011 | 55 s | 0.45 GB |
| Sheet Metal | 512 | 0.036 (0.002) | 0.200 (0.012) | 0.432 (0.020) | 0.879 (0.015) | 0.748 (0.087) | 0.077 | 555 s | 1.86 GB |
| Vial | 256 | 0.561 (0.008) | 0.870 (0.002) | 0.414 (0.004) | 0.835 (0.021) | 0.871 (0.016) | 0.013 | 168 s | 0.97 GB |
| Vial | 512 | 0.599 (0.005) | 0.885 (0.002) | 0.246 (0.063) | 0.824 (0.000) | 0.808 (0.014) | 0.142 | 2462 s | 4.11 GB |

## What the numbers say

1. **Ranking photos does not get better at 512.**
   - The paired bootstrap, which draws parts, gives these AU-ROC changes from 256 to 512:
     - Sheet Metal: -0.026, interval -0.29 to 0.23.
     - Vial: -0.063, interval -0.29 to 0.11.
   - The image F1 changes are +0.003 for Sheet Metal and -0.012 for Vial.
   - Every interval includes 0, so **half A shows no real difference** either way.
2. **The time per photo grows 7 times for Sheet Metal and 11 times for Vial.** Fitting grows 10 to 15 times, because the memory bank holds 4 times as many patches and the coreset step has to search all of them.
3. **The benchmark line stops working at 512.**
   - The line is the mean plus 3 standard deviations of good validation pixels. At 512 it flags:
     - On Sheet Metal, 17 or 18 of 19 good validation photos. At 256 it flagged 12.
     - On Vial, 39 or 40 of 41. At 256 it flagged 29 to 33.
   - So at 512, image F1 at this line is close to the F1 of simply rejecting every photo: 0.875 for Sheet Metal and 0.824 for Vial.
4. **Pixel results move in opposite directions on the two products.**
   - **Sheet Metal:** pixel F1 doubles (0.20 to 0.43), but AU-PRO falls. Pixel F1 counts pixels, so the large defects dominate it. AU-PRO gives every defect region equal weight, so it is pulled down by the small and faint regions, which are still missed.
   - **Vial:** AU-PRO rises a little (0.87 to 0.89), but pixel F1 falls (0.41 to 0.25), because the line now sits inside the scores of good glass.
5. **Part by part, the change is mixed.** For each defective part, I looked at the share of its photos that score above every good photo with the same lighting (in [resolution_by_part.csv](resolution_by_part.csv)):
   - **Sheet Metal:**
     - Part 000 rises from 0.72 to 1.0.
     - Part 012, one of the small defects, rises from 0.50 to 0.83.
     - Parts 007 and 009 fall from 1.0 to about 0. These are a defect at the very edge of the sheet and a group of faint, thin cracks.
     - Part 005 falls from 0.94 to 0.39.
   - **Vial:**
     - Parts 011 and 014 rise.
     - Parts 008, 012 and 013 fall. Part 013 falls from 0.90 to 0.

## Likely causes, judged by eye from the failure galleries

These causes are my judgement from looking at the galleries, not something that was measured.

- **Sheet Metal:** at 512, the textured surface itself, and the dark band at both sides of the sheet, get more suspicious on good photos. A defect at the edge (007) or one that is faint (009) is then lost in that background.
- **Vial:** at 512, the printed code and the bubbles on good vials score as high as many defects. Vial 013 has a defect inside the bubbly region, and it is no longer separated. The same cause was seen for Reverse Distillation in Phase 7.

## Answer to the question

A sharper photo **helps a few small Sheet Metal defects** (000 and 012) and makes the matched defect pixels more precise. On half A, it **does not find more defective parts overall** and **costs 7 to 11 times the time per photo**. The main settings stay at 256. Half B will be scored at 256 for every configuration. Whether C6 at 512 is also scored on half B is part of the Lock decision.
