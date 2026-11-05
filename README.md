# Visual Quality Inspection with Anomaly Detection

## Business problem

Factories must stop defective parts before they ship, but defects are rare and unpredictable, so there are few examples to learn from. This project tests published methods that learn only from photos of good parts, then flag anything different and show where it is.

Both kinds of error cost money. A missed defect reaches the customer, and a false reject throws away a good part. I assume a missed defect costs 10 times a false reject, and test that assumption from 2 to 100 times, because real costs are not available for a benchmark. The goal is a pass or reject rule that keeps the total cost of errors low, and a recommendation per product type with its limits stated.

## Project status

This project follows CRISP-DM, a standard process for data science projects.

| Phase | CRISP-DM stage | What it produced |
| --- | --- | --- |
| 0. Setup and business understanding | Business understanding | Repository structure, licence, laptop environment, and a notebook that ran on a Kaggle GPU ([report](outputs/results/00_gpu_check/gpu_check_report.txt)) |
| 1. Data acquisition and integrity | Data understanding | Sheet Metal and Vial confirmed, a [data card](docs/data_card.md), and integrity checks on all 1,773 images and masks ([report](outputs/results/01_data_and_integrity/integrity_report.txt)) |
| 2. Exploring the images | Data understanding | A public test [summary](outputs/results/02_exploration/test_set_summary.txt), its one split into a development half and a final half ([A](outputs/results/02_exploration/half_a_files.csv), [B](outputs/results/02_exploration/half_b_files.csv)), [defect sizes](outputs/figures/defect_size_histogram.png), [defect locations](outputs/results/02_exploration/defect_location_summary.txt), [good-part variation](outputs/results/02_exploration/good_part_variation_summary.txt), and brightness charts ([Sheet Metal](outputs/figures/brightness_comparison_sheet_metal.png), [Vial](outputs/figures/brightness_comparison_vial.png)) |
| 3. Preparing the images | Data preparation | Image size 256 for the main experiments and 512 for the resolution test, chosen from a [GPU size check](outputs/results/03_gpu_size_check/gpu_size_results.csv). Squashing chosen after a [comparison](outputs/results/03_preprocessing/shape_options.txt) of squash, pad and crop. A [diagnosis](outputs/results/03_inverse_diagnosis/inverse_results.csv) and [real-model check](outputs/results/03_padim_real_check/padim_real_results.csv) of PaDiM's statistics step. A [prepared batch check](outputs/results/03_prepared_batch/prepared_batch_check.txt), and [configuration files](configs/) C1 to C8 |
| 4. First model run | Modelling | A PaDiM baseline with ResNet-18 on Sheet Metal ([metrics](outputs/results/04_padim_baseline/c1_sheet_metal_metrics.txt)), a repeat with the same seed and a [loose comparison with the paper](docs/c1_repeat_and_paper_notes.md), and an [EfficientNet-B0 check](outputs/results/04_efficientnet_check/efficientnet_check_results.csv). These are development numbers from half of the public test set, with one seed, not final results |

## Data

This project uses the Sheet Metal and Vial product types from [MVTec AD 2](https://www.mvtec.com/research-teaching/datasets/mvtec-ad-2), licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). See the [data card](docs/data_card.md) for what each folder holds and what the checks found.

Figures showing dataset images or masks are not in this repository. To remake them, run [the exploration notebook](notebooks/02_exploration.ipynb) with the dataset attached. They are saved as `gallery_*` files.

Heckler-Kram, Neudeck, Scheler, König and Steger. The MVTec AD 2 Dataset: Advanced Scenarios for Unsupervised Anomaly Detection. *International Journal of Computer Vision* 134(4), 2026. DOI [10.1007/s11263-026-02743-0](https://doi.org/10.1007/s11263-026-02743-0).

## Environments

The laptop and Kaggle use different versions of some libraries, so all reported results come from Kaggle only.

| | Used for | Python | PyTorch | anomalib | Exact versions |
| --- | --- | --- | --- | --- | --- |
| Laptop | Small tests, plots, the demo | 3.11.9 | 2.15.0 (CPU) | 2.7.0 | [requirements.txt](requirements.txt) |
| Kaggle | Fitting, training, full evaluation | 3.13.16 | 2.11.0 (GPU) | 2.7.0 | [kaggle_pip_freeze.txt](outputs/results/00_gpu_check/kaggle_pip_freeze.txt) |

## Licence

The MIT licence in [LICENSE](LICENSE) covers my code only. The [MVTec AD 2 dataset](https://www.mvtec.com/company/research/datasets/mvtec-ad-2) has its own licence (CC BY-NC-SA 4.0) and is not included in this repository. Download it from the official page.
