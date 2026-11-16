# Phase 7 results on half A (development numbers, not final results)

## sheet_metal

| Configuration | Seeds | AU-PRO 5% | AU-PRO 30% | Pixel F1 | Image F1 [95% interval] | Flag-everything F1 | Image AU-ROC [95% interval] | Seconds per photo | Peak GPU GB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 PaDiM, ResNet-18 | 1 | 0.043 | 0.241 | 0.106 | 0.884 [0.875 to 0.894] | 0.875 | 0.75 [0.631 to 0.889] | 0.006 | 0.326 |
| C2 PaDiM, Wide ResNet-50 | 1 | 0.066 | 0.241 | 0.413 | 0.526 [0.133 to 0.833] | 0.875 | 0.742 [0.381 to 0.984] | 0.021 | 5.613 |
| C3 PaDiM, EfficientNet-B0 | 1 | 0.0 | 0.125 | 0.085 | 0.875 [0.875 to 0.875] | 0.875 | 0.595 [0.583 to 0.619] | 0.007 | 0.306 |
| C4 PatchCore, ResNet-18 | 3 | 0.078 (0.003) | 0.288 (0.008) | 0.244 (0.004) | 0.811 (0.038) [0.715 to 0.885] | 0.875 | 0.649 (0.029) [0.466 to 0.842] | 0.012 (0.001) | 0.16 (0.0) |
| C5 PatchCore, Wide ResNet-50 | 3 | 0.053 (0.001) | 0.216 (0.011) | 0.197 (0.003) | 0.858 (0.012) [0.776 to 0.921] | 0.875 | 0.796 (0.027) [0.695 to 0.911] | 0.026 (0.004) | 0.434 (0.0) |
| C6 PatchCore, EfficientNet-B0 | 3 | 0.072 (0.005) | 0.278 (0.008) | 0.199 (0.004) | 0.875 (0.011) [0.783 to 0.929] | 0.875 | 0.774 (0.009) [0.656 to 0.893] | 0.011 (0.0) | 0.15 (0.001) |
| C7 WinCLIP, CLIP | 1 | 0.066 | 0.224 | 0.004 | 0.174 [0.0 to 0.385] | 0.875 | 0.754 [0.421 to 0.992] | 0.223 | 1.453 |
| C8 Reverse Distillation, Wide ResNet-50 | 1 | 0.078 | 0.268 | 0.495 | 0.635 [0.28 to 0.911] | 0.875 | 0.851 [0.587 to 1.0] | 0.028 | 1.371 |

Intervals come from drawing 2 good and 7 defective parts, 2,000 times. With so few good parts, they are wide and rough.

## vial

| Configuration | Seeds | AU-PRO 5% | AU-PRO 30% | Pixel F1 | Image F1 [95% interval] | Flag-everything F1 | Image AU-ROC [95% interval] | Seconds per photo | Peak GPU GB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 PaDiM, ResNet-18 | 1 | 0.003 | 0.462 | 0.117 | 0.831 [0.824 to 0.845] | 0.824 | 0.741 [0.672 to 0.799] | 0.006 | 0.326 |
| C2 PaDiM, Wide ResNet-50 | 1 | 0.038 | 0.652 | 0.122 | 0.824 [0.824 to 0.824] | 0.824 | 0.685 [0.52 to 0.764] | 0.018 | 5.612 |
| C3 PaDiM, EfficientNet-B0 | 1 | 0.0 | 0.205 | 0.026 | 0.796 [0.739 to 0.847] | 0.824 | 0.534 [0.446 to 0.621] | 0.007 | 0.306 |
| C4 PatchCore, ResNet-18 | 3 | 0.422 (0.002) | 0.826 (0.001) | 0.278 (0.003) | 0.861 (0.01) [0.817 to 0.958] | 0.824 | 0.846 (0.015) [0.635 to 0.976] | 0.017 (0.002) | 0.216 (0.0) |
| C5 PatchCore, Wide ResNet-50 | 3 | 0.385 (0.003) | 0.782 (0.003) | 0.261 (0.002) | 0.865 (0.004) [0.824 to 0.961] | 0.824 | 0.818 (0.008) [0.543 to 0.981] | 0.039 (0.0) | 0.562 (0.0) |
| C6 PatchCore, EfficientNet-B0 | 3 | 0.56 (0.004) | 0.87 (0.001) | 0.414 (0.002) | 0.835 (0.011) [0.824 to 0.846] | 0.824 | 0.871 (0.009) [0.68 to 0.969] | 0.013 (0.002) | 0.18 (0.0) |
| C7 WinCLIP, CLIP | 1 | 0.37 | 0.659 | 0.016 | 0.824 [0.824 to 0.824] | 0.824 | 0.902 [0.686 to 1.0] | 0.237 | 1.451 |
| C8 Reverse Distillation, Wide ResNet-50 | 1 | 0.48 | 0.815 | 0.203 | 0.824 [0.824 to 0.824] | 0.824 | 0.508 [0.258 to 0.76] | 0.026 | 1.408 |

Intervals come from drawing 3 good and 7 defective parts, 2,000 times. With so few good parts, they are wide and rough.

Pixel metrics are uncertain, because masks were drawn by people and their agreement cannot be measured here.
