# Model card: C6, PatchCore with EfficientNet-B0

**CRISP-DM stage:** Deployment. This card describes the configuration used in the [demo](../app/README.md). C6 is also the locked recommendation for Sheet Metal, and the card closes with a short note on C7 (WinCLIP), the locked recommendation for Vial. Both recommendations failed at their locked lines on the final test, and this card says so plainly.

## What it does

C6 learns what good parts look like, then scores how unusual each new photo is and shows where.

1. **It describes good parts as patches.** A pretrained EfficientNet-B0 describes each good training photo as a grid of small patches. It uses the layers `blocks.2` and `blocks.4`, which shrink the photo by 8 and 16.
2. **It keeps a memory bank.** It keeps the most varied 10 percent of those patches (a coreset).
3. **It scores a new photo.** Each patch of the new photo is compared with its nearest patch in the memory bank. The distances make a heat map, and the photo's score comes from its most unusual patch, using anomalib's default of 9 neighbours.
4. **It gives a verdict.** A photo is rejected if its score is above a line. Two lines are kept:
   - **The cost-based line,** which is used for the verdict. It was the cheapest line on half A, for 1 percent defects with a missed defect costing 10 times a false reject.
   - **The benchmark line,** for comparison with the paper: the mean plus 3 standard deviations of good validation pixels.

**Settings:**
- 256 x 256 pixels, squashed with no crop. Masks are resized with nearest-neighbour interpolation.
- ImageNet normalisation, and fitted on good training photos only.
- Seeds 42, 43 and 44. The demo uses seed 42.
- All settings and their reasons are in [C6_patchcore_efficientnet.yaml](../configs/C6_patchcore_efficientnet.yaml).

**Software:** anomalib 2.7.0, through its PyTorch model classes.

## Results

Means over 3 seeds. Development results come from half A of the public test set; the reported results come from half B, which was opened once after the Lock.

| | Sheet Metal, half A | Sheet Metal, half B | Vial, half A | Vial, half B |
| --- | --- | --- | --- | --- |
| Image AU-ROC [95% interval] | 0.77 | **0.52** [0.40 to 0.64] | 0.87 | **0.90** [0.78 to 0.98] |
| AU-PRO at 30% | 0.28 | 0.16 | 0.87 | 0.92 |
| Pixel F1 at the benchmark line | 0.20 | 0.004 | 0.41 | 0.37 |
| Cost per part at the cost-based line (passing everything: 0.10) | 0.041 | **0.373** | 0.071 | **0.046** |
| Defects missed at the cost-based line | 41% | 71% | 71% | 46% |
| Good parts rejected at the cost-based line | 0% | 31% | 0% | 0% |

**Speed and memory** (Kaggle Tesla T4 GPU):
- **Time per photo:** about 0.011 seconds.
- **Peak GPU memory when scoring:** 0.15 to 0.18 GB.
- **Fitting:** about 1 minute (Sheet Metal) and 3 minutes (Vial).

**At 512 pixels:** the image AU-ROC was not really different, and each photo took 7 to 12 times longer ([resolution findings](../outputs/results/08_resolution/resolution_findings.md)).

The full comparison of all eight configurations is in the [Final test findings](../outputs/results/final_test/final_findings.md).

## Known failure cases (from the failure galleries, judged by eye)

- **Good parts that look different from the training parts** score as high as defects. This was the main failure on Sheet Metal half B: the darker sheets of good parts 000 and 003, under shifted light.
- **Changed lighting:**
  - **What happens:** a line set under regular light rejects most good photos under over-exposure, under-exposure or a shifted light.
  - **How much:** 73 percent on Sheet Metal and 89 percent on Vial, on half B.
- **Small, thin or faint defects** are missed, for example thin scratches and faint cracks on Sheet Metal. The heat map is too coarse at 256 pixels to separate them from the surface texture.
- **Defects at the very edge** of the sheet are missed more often at 512 pixels than at 256.
- **Vial:** printed codes and bubbles on good vials can raise the score.

## Intended use

- **Teaching and research:** a demonstration of learning-from-good-parts anomaly detection, and of how to evaluate it honestly.
- **As an assistant to a human inspector:** it can show a heat map of where to look. A person makes the decision.

## Not suitable for

- **Commercial use of any kind.** The model is fitted on MVTec AD 2, whose licence (CC BY-NC-SA 4.0) allows non-commercial use only.
- **Automatic pass or reject decisions without a human.** On half B, its locked line cost more than passing every part on Sheet Metal.
- **Other products, cameras or lighting** without fitting it again and checking it on many good parts.
- **Defect types it was never checked on.** The test files do not label defect types, so it is unknown which types it handles.

## Monitoring plan (what a factory would have to watch after go-live)

Half B showed that a line set on a few good parts does not carry over to new good parts. A factory would need to check the following continuously.

1. **Drift in the scores of good parts.**
   - **What to track:** the score distribution of parts that a person confirmed as good, every shift.
   - **Warning signal:** the median or the 95th percentile moving by more than the spread seen at go-live.
   - **Why:** this is the first warning that the parts, the camera or the light have changed.
2. **Lighting.**
   - **What to log:** the average brightness of each photo, beside its score.
   - **Trigger for a recheck:** any change of lamp, camera setting or line position, before the line is trusted again. Lighting was the biggest cause of false rejects in this project.
3. **The false-reject rate.** Track the share of rejected parts that a person finds to be good. If it rises above the rate assumed when the line was set, the line or the model needs a recheck.
4. **Missed defects.**
   - **What to track:** returns and spot checks of passed parts.
   - **Trigger for a recheck:** a rise in either.
5. **New defect types.**
   - **What to do:** keep every confirmed defect with its heat map, so new kinds can be seen.
   - **Why:** the method has no list of defect types. It only knows "different from good".
6. **When to fit again:**
   - **Triggers:** a change in product, camera, lighting or supplier, or a lasting score drift.
   - **How:** fit on fresh good photos, then set the line again on a new set with many good parts, never on the photos it is judged on.
7. **Human review:** every rejected part stays under human review, and a sample of passed parts is checked as well.

## Note on C7 (WinCLIP), the locked recommendation for Vial

**What it is:** WinCLIP compares windows of the photo with text descriptions of normal and damaged objects. It needs no training photos ("zero-shot").

**Results for Vial:**

| | Half A | Half B |
| --- | --- | --- |
| Image AU-ROC | 0.90 | 0.66 [0.37 to 0.91] |
| Cost per part at its cost-based line | 0.018 | 0.80 |
| Good photos rejected | | 79% |

**Speed:** about 0.24 seconds per photo, and it needs an 800 MB model. That is why it is not in the live demo.

**Same limits as C6:** the same "not suitable" list and the same monitoring plan apply.

## Citations and licences

- **Data:** MVTec AD 2 (CC BY-NC-SA 4.0).
- **Method and network:**
  - PatchCore (Roth and colleagues, 2022).
  - EfficientNet (Tan and Le, 2019), pretrained on ImageNet and loaded through timm (Apache-2.0).
- **Software:** anomalib 2.7.0 (Apache-2.0).
- **Full references:** in the [README](../README.md).
