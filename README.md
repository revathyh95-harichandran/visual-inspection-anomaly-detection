# Visual Quality Inspection with Anomaly Detection

## Licence

The MIT licence in [LICENSE](LICENSE) covers my code only. The [MVTec AD 2 dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad-2) has its own licence (CC BY-NC-SA 4.0) and is not included in this repository. Download it from the official page.

## Environments

The laptop and Kaggle use different versions of some libraries, so all reported results come from Kaggle only.

| | Used for | Python | PyTorch | anomalib | Exact versions |
| --- | --- | --- | --- | --- | --- |
| Laptop | Small tests, plots, the demo | 3.11.9 | 2.15.0 (CPU) | 2.7.0 | [requirements.txt](requirements.txt) |
| Kaggle | Fitting, training, full evaluation | 3.13.16 | 2.11.0 (GPU) | 2.7.0 | [kaggle_pip_freeze.txt](outputs/results/00_gpu_check/kaggle_pip_freeze.txt) |
