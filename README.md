# Visual Quality Inspection with Anomaly Detection

## Business problem

Factories must stop defective parts before they ship, but defects are rare and unpredictable, so there are few examples to learn from. This project tests published methods that learn only from photos of good parts, then flag anything different and show where it is.

Both kinds of error cost money. A missed defect reaches the customer, and a false reject throws away a good part. I assume a missed defect costs 10 times a false reject, and test that assumption from 2 to 100 times, because real costs are not available for a benchmark. The goal is a pass or reject rule that keeps the total cost of errors low, and a recommendation per product type with its limits stated.

## Project status

This project follows CRISP-DM, a standard process for data science projects.

| Phase | CRISP-DM stage | What it produced |
| --- | --- | --- |
| 0. Setup and business understanding | Business understanding | Repository structure, licence, laptop environment, and a notebook that ran on a Kaggle GPU ([report](outputs/results/00_gpu_check/gpu_check_report.txt)) |

## Environments

The laptop and Kaggle use different versions of some libraries, so all reported results come from Kaggle only.

| | Used for | Python | PyTorch | anomalib | Exact versions |
| --- | --- | --- | --- | --- | --- |
| Laptop | Small tests, plots, the demo | 3.11.9 | 2.15.0 (CPU) | 2.7.0 | [requirements.txt](requirements.txt) |
| Kaggle | Fitting, training, full evaluation | 3.13.16 | 2.11.0 (GPU) | 2.7.0 | [kaggle_pip_freeze.txt](outputs/results/00_gpu_check/kaggle_pip_freeze.txt) |

## Licence

The MIT licence in [LICENSE](LICENSE) covers my code only. The [MVTec AD 2 dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad-2) has its own licence (CC BY-NC-SA 4.0) and is not included in this repository. Download it from the official page.
