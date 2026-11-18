# Final test results on half B

Settings and lines were locked on half A before half B was opened (DECISIONS.md, 17 Nov 2026). Each value is the mean over seeds, with the spread in brackets for 3 seeds. Intervals are 95 percent part bootstraps.

## sheet_metal

| Configuration | Seeds | AU-PRO 5% | AU-PRO 30% | Pixel F1 | Image F1, benchmark line [interval] | Image F1, cost-based line [interval] | Flag-everything F1 | Image AU-ROC [interval] | Half A AU-ROC | Seconds per photo | Peak GPU GB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 PaDiM, ResNet-18 | 1 | 0.013 | 0.152 | 0.003 | 0.889 [0.889 to 0.889] | 0.218 [0.113 to 0.339] | 0.8889 | 0.628 [0.517 to 0.729] | 0.75 | 0.006 | 0.326 |
| C2 PaDiM, Wide ResNet-50 | 1 | 0.037 | 0.168 | 0.04 | 0.769 [0.499 to 0.945] | 0.829 [0.588 to 1.0] | 0.8889 | 0.925 [0.771 to 1.0] | 0.742 | 0.021 | 5.613 |
| C3 PaDiM, EfficientNet-B0 | 1 | 0.0 | 0.097 | 0.003 | 0.889 [0.889 to 0.889] | 0.041 [0.0 to 0.118] | 0.8889 | 0.661 [0.608 to 0.708] | 0.595 | 0.007 | 0.306 |
| C4 PatchCore, ResNet-18 | 3 | 0.035 (0.001) | 0.165 (0.002) | 0.007 (0.0) | 0.804 (0.008) [0.698 to 0.891] | 0.24 [0.027 to 0.492] | 0.8889 | 0.588 (0.011) [0.422 to 0.762] | 0.649 | 0.012 (0.001) | 0.16 (0.0) |
| C5 PatchCore, Wide ResNet-50 | 3 | 0.042 (0.002) | 0.22 (0.006) | 0.009 (0.001) | 0.873 (0.012) [0.8 to 0.922] | 0.494 [0.282 to 0.642] | 0.8889 | 0.65 (0.04) [0.486 to 0.787] | 0.796 | 0.027 (0.003) | 0.434 (0.0) |
| C6 PatchCore, EfficientNet-B0 | 3 | 0.022 (0.001) | 0.156 (0.011) | 0.004 (0.0) | 0.864 (0.021) [0.838 to 0.882] | 0.427 [0.242 to 0.567] | 0.8889 | 0.522 (0.074) [0.401 to 0.638] | 0.774 | 0.011 (0.0) | 0.15 (0.001) |
| C7 WinCLIP, CLIP | 1 | 0.066 | 0.202 | 0.0 | 0.041 [0.0 to 0.118] | 0.394 [0.065 to 0.69] | 0.8889 | 0.174 [0.014 to 0.371] | 0.754 | 0.214 | 1.453 |
| C8 Reverse Distillation, Wide ResNet-50 | 1 | 0.046 | 0.194 | 0.0 | 0.476 [0.118 to 0.769] | 0.476 [0.118 to 0.769] | 0.8889 | 0.878 [0.747 to 0.986] | 0.851 | 0.027 | 0.941 |
| C6 at 512 pixels | 3 | 0.063 (0.006) | 0.236 (0.006) | 0.03 (0.001) | 0.878 (0.011) [0.857 to 0.889] | 0.523 [0.189 to 0.775] | 0.8889 | 0.631 (0.034) [0.402 to 0.824] | 0.748 | 0.078 (0.002) | 0.527 (0.0) |

Intervals come from drawing the 2 good and the defective parts of half B, 2,000 times. With so few good parts, they are wide and rough.

## vial

| Configuration | Seeds | AU-PRO 5% | AU-PRO 30% | Pixel F1 | Image F1, benchmark line [interval] | Image F1, cost-based line [interval] | Flag-everything F1 | Image AU-ROC [interval] | Half A AU-ROC | Seconds per photo | Peak GPU GB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 PaDiM, ResNet-18 | 1 | 0.0 | 0.52 | 0.086 | 0.862 [0.783 to 0.931] | 0.035 [0.0 to 0.102] | 0.8889 | 0.607 [0.452 to 0.699] | 0.741 | 0.006 | 0.326 |
| C2 PaDiM, Wide ResNet-50 | 1 | 0.033 | 0.713 | 0.144 | 0.918 [0.918 to 0.918] | 0.068 [0.0 to 0.161] | 0.8889 | 0.666 [0.583 to 0.735] | 0.685 | 0.018 | 5.612 |
| C3 PaDiM, EfficientNet-B0 | 1 | 0.0 | 0.181 | 0.028 | 0.852 [0.8 to 0.9] | 0.0 [0.0 to 0.0] | 0.8889 | 0.556 [0.531 to 0.577] | 0.534 | 0.006 | 0.306 |
| C4 PatchCore, ResNet-18 | 3 | 0.593 (0.009) | 0.895 (0.004) | 0.339 (0.014) | 0.894 (0.029) [0.775 to 0.949] | 0.667 [0.222 to 0.933] | 0.8889 | 0.904 (0.016) [0.761 to 0.991] | 0.846 | 0.017 (0.0) | 0.216 (0.0) |
| C5 PatchCore, Wide ResNet-50 | 3 | 0.582 (0.002) | 0.889 (0.002) | 0.281 (0.004) | 0.963 (0.004) [0.949 to 0.977] | 0.674 [0.273 to 0.924] | 0.8889 | 0.922 (0.0) [0.86 to 0.982] | 0.818 | 0.043 (0.0) | 0.562 (0.0) |
| C6 PatchCore, EfficientNet-B0 | 3 | 0.656 (0.008) | 0.925 (0.002) | 0.373 (0.013) | 0.949 (0.0) [0.949 to 0.949] | 0.703 [0.319 to 0.937] | 0.8889 | 0.899 (0.006) [0.781 to 0.977] | 0.871 | 0.013 (0.001) | 0.18 (0.0) |
| C7 WinCLIP, CLIP | 1 | 0.465 | 0.795 | 0.195 | 0.889 [0.889 to 0.889] | 0.759 [0.581 to 0.881] | 0.8889 | 0.657 [0.367 to 0.911] | 0.902 | 0.244 | 1.451 |
| C8 Reverse Distillation, Wide ResNet-50 | 1 | 0.682 | 0.933 | 0.321 | 0.896 [0.889 to 0.903] | 0.753 [0.389 to 0.933] | 0.8889 | 0.935 [0.819 to 1.0] | 0.508 | 0.026 | 0.941 |
| C6 at 512 pixels | 3 | 0.847 (0.003) | 0.972 (0.0) | 0.477 (0.036) | 0.889 (0.0) [0.889 to 0.889] | 0.703 [0.336 to 0.933] | 0.8889 | 0.915 (0.011) [0.79 to 0.994] | 0.808 | 0.153 (0.003) | 0.648 (0.0) |

Intervals come from drawing the 2 good and the defective parts of half B, 2,000 times. With so few good parts, they are wide and rough.

Pixel metrics are uncertain, because masks were drawn by people and their agreement cannot be measured here.
