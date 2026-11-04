# Data card: MVTec AD 2 (Sheet Metal and Vial)

**CRISP-DM stage:** Data understanding. This card grows during Phases 1 to 3.

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

Read directly from all 1,773 files on Kaggle.

| | Sheet Metal | Vial |
| --- | --- | --- |
| Width × height, for every image and mask | 4224 × 1056 | 1400 × 1900 |
| Stored channels, for every image and mask | 1, greyscale (mode `L`) | 1, greyscale (mode `L`) |
| Raw mask values | 0 and 255 | 0 and 255 |

anomalib's `MVTecAD2` loader changes this when it reads a file. In one sample per product, images came back with 3 channels, and masks held 0 and 1.

## File naming

Files are named `<number>_<lighting>.png`.

- `train`, `validation` and `test_private` images are all named `regular`.
- `test_private_mixed` images are named `mixed`.
- `test_public` images use `regular`, `overexposed`, `underexposed` and `shift_1` to `shift_3`, plus `shift_4` for Vial.

## Integrity checks

Run on Kaggle on all 1,773 images and masks. The checks only read files, and nothing was changed. Full results are in [integrity_report.txt](../outputs/results/01_data_and_integrity/integrity_report.txt) and [image_inventory.csv](../outputs/results/01_data_and_integrity/image_inventory.csv).

| Check | Result |
| --- | --- |
| Counts against the paper's Table IV (arXiv version) | All 14 folder counts match |
| Every file opens and decodes | All open |
| Size and channels | One size and one mode per product, and sizes match the paper |
| Masks | Every defective image has a mask of the same size, holding only 0 and 255, with at least one defect pixel. Every mask has an image. No good image has a mask |
| Byte-identical images | 65 pairs, all between `test_private` and `test_private_mixed`. None involves `train`, `validation` or `test_public` |
| Lighting conditions per scene number | Consistent within each product |

**The 65 pairs:** 27 for Sheet Metal and 38 for Vial. The paper describes `test_private_mixed` as the same scenes as `test_private` under seen and unseen lighting, so a likely reading is that these are scenes that kept regular lighting. I have not confirmed that with MVTec.

**Limit of the duplicate check:** it finds byte-identical files only. It does not find the same scene under different lighting, or a re-saved copy.

## Known limits so far

- **Repeated scenes:** in `test_public`, each number appears once per lighting condition. Sheet Metal has 4 good and 15 defective numbers with 6 conditions each. Vial has 5 good and 15 defective numbers with 7 conditions each. Masks support this: a scene number has one identical mask across all conditions for 12 of 15 Sheet Metal numbers and 9 of 15 Vial numbers. Looking at defective scene `000` of each product, the same physical part appears under every lighting condition. In Vial, its mask outlines visibly differ between conditions, which may explain some of the differing masks. This was checked by eye on one scene per product, so it does not prove the pattern for every scene.
- **Defect types:** no folder or file name gives a defect type, and the archive's readme does not mention one.
- **Share of defects:** the public test sets are about 75 to 80 percent defective, far more than a real production line.
