# C1: repeat run and a loose comparison with the paper

**CRISP-DM stage:** Modelling. This is C1, PaDiM with ResNet-18, on Sheet Metal, half A only.

## Does the same seed give the same numbers?

Yes, for every result. The same notebook ran twice with seed 42. Every metric, the threshold and all 54 photo scores matched, and the score files are byte-identical. Scores are saved to 4 decimal places, so differences smaller than that would not show. Only two timings changed: features took 41.09 s and then 40.94 s, and the fit took 4.54 s and then 4.75 s.

**Why they match:** the pretrained network is fixed, the photos are read in a fixed order, the seed fixes PaDiM's random choice of features, and the rest is ordinary calculation.

**Why timings differ:** they depend on what the machine is doing at that moment.

**Limits:** PyTorch's strict repeatable mode is not switched on, and GPU calculations are not guaranteed to repeat exactly. This shows the run repeated here, not that it always will. Matching numbers show the run is repeatable, not that its result is right.

## Loose comparison

**The paper did not evaluate PaDiM,** so there is no direct number to compare with. The table shows only whether these numbers sit in a sensible range. It does not rank PaDiM against any method.

**The paper's numbers are unverified.** They came from an automatic summary of its result tables, not from reading the tables directly. Check them against the paper before citing them.

| Sheet Metal, in percent | C1 on half A | Range of the paper's 7 methods, private set | Range, private mixed-lighting set |
| --- | --- | --- | --- |
| AU-PRO at 5 percent | 4.27 | 9.3 to 18.0 | 5.3 to 16.1 |
| AU-PRO at 30 percent | 24.13 | 26.6 to 46.9 | 22.9 to 45.2 |
| Pixel F1 | 10.63 | 1.8 to 41.3 | 1.1 to 39.2 |
| Image F1 | 88.42 | 1.9 to 86.4 | 1.9 to 85.5 |

**Reading this loosely:** C1's AU-PRO is at or below the low end of the range, and its pixel F1 is inside the range. Its image F1 looks highest, but this does not mean it is better: half A is about 78 percent defective, and flagging everything there already scores 87.5.

## Differences in setup

| | The paper | This run |
| --- | --- | --- |
| Method | EfficientAD, Reverse Distillation, RD++, PatchCore, MSFlow, SimpleNet, DSR | PaDiM |
| Network | Each method's own default | ResNet-18 |
| Test photos | Private sets, 142 photos each for Sheet Metal | Half A of the public set, 54 photos |
| Lighting | Training lighting, and mixed seen and unseen lighting | Six public lighting conditions |
| Answers | Masks held on the evaluation server | Public masks |
| Share of defective photos | Not known | 42 of 54 |
| Image size | 256 x 256 for some tables, and not clear for others | 256 x 256, squashed |
| Scoring size | Not clearly stated | 256 x 256 |
| Tuning | Default settings, with no tuning per scenario | Default settings |
| Seeds | Not known | One seed |
| Threshold | Mean plus 3 standard deviations of good validation values, with pooling not clearly stated | The same rule, with all pixels pooled |
| Where statistics run | Each method's own | PaDiM's statistics on the processor, because the GPU's inverse step crashed |
| Evaluated by | The paper's authors | Run with anomalib 2.7.0 and a separate metric calculation |
