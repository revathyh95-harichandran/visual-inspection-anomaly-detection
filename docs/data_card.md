# Data card: MVTec AD 2 (Sheet Metal and Vial)

**CRISP-DM stage:** Data understanding. This card grows during Phases 1 to 3. Integrity checks are still to come.

## Source and licence

- **Dataset:** [MVTec AD 2](https://www.mvtec.com/research-teaching/datasets/mvtec-ad-2), from MVTec Software GmbH. Download it from that page after filling in its short form. The images are not in this repository.
- **Licence:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Non-commercial use only, with credit, and anything built from it is shared under the same licence.
- **Citation:** Heckler-Kram, Neudeck, Scheler, König and Steger. The MVTec AD 2 Dataset: Advanced Scenarios for Unsupervised Anomaly Detection. *International Journal of Computer Vision* 134(4), 2026. DOI [10.1007/s11263-026-02743-0](https://doi.org/10.1007/s11263-026-02743-0).

This project uses two of the eight product types, unmodified: Sheet Metal and Vial.

## What each folder means

| Folder | What it holds | How this project uses it |
| --- | --- | --- |
| `train/good` | Images of good parts | Fitting or training every model |
| `validation/good` | Images of good parts | Settings and the benchmark threshold |
| `test_public/good` | Good parts, for testing | Split into half A and half B |
| `test_public/bad` | Defective parts, for testing | Split into half A and half B |
| `test_public/ground_truth/bad` | One mask per defective image, named `<image name>_mask.png` | Measuring where defects are found |
| `test_private` | Test images with no public answers | Scored only by the official evaluation server |
| `test_private_mixed` | Test images with no public answers, with mixed lighting | Scored only by the official evaluation server |

Good test images have no masks. Each archive also holds a `readme.txt` and a `license.txt`.

## File counts

Counted on Kaggle from the unmodified files. These counts match Table IV of the paper's arXiv version (2503.21622v1).

| Folder | Sheet Metal | Vial |
| --- | --- | --- |
| `train/good` | 137 | 291 |
| `validation/good` | 19 | 41 |
| `test_public/good` | 24 | 35 |
| `test_public/bad` | 90 | 105 |
| `test_public/ground_truth/bad` | 90 | 105 |
| `test_private` | 142 | 276 |
| `test_private_mixed` | 142 | 276 |

## Image format

Read through anomalib's `MVTecAD2` loader, with no resizing, from one training image and one defective image per product.

| | Sheet Metal | Vial |
| --- | --- | --- |
| Image shape (channels, height, width) | 3, 1056, 4224 | 3, 1900, 1400 |
| Mask shape (height, width) | 1056, 4224 | 1900, 1400 |
| Mask values | 0 and 1 | 0 and 1 |

## File naming

Files are named `<number>_<lighting>.png`.

- `train`, `validation` and `test_private` images are all named `regular`.
- `test_private_mixed` images are named `mixed`.
- `test_public` images use `regular`, `overexposed`, `underexposed` and `shift_1` to `shift_3`, plus `shift_4` for Vial.

## Known limits so far

- **Repeated scenes:** in `test_public`, each number appears once per lighting condition. Sheet Metal has 4 good and 15 defective numbers with 6 conditions each. Vial has 5 good and 15 defective numbers with 7 conditions each. This suggests far fewer distinct scenes than images, but it comes from file names and has not yet been checked by looking at the images.
- **Defect types:** no folder or file name gives a defect type, and the archive's readme does not mention one.
- **Share of defects:** the public test sets are about 75 to 80 percent defective, far more than a real production line.
- **Samples checked:** image and mask shapes above come from one sample per product. Every file is checked in the integrity step, which has not run yet.
