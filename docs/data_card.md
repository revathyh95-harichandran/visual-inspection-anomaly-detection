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

## Public test set

Counted from file names on Kaggle.

| | Sheet Metal | Vial |
| --- | --- | --- |
| Good images | 24 | 35 |
| Defective images | 90 | 105 |
| Defective share | 78.9 percent | 75.0 percent |
| Good scene numbers | 4 | 5 |
| Defective scene numbers | 15 | 15 |
| Lighting conditions | 6 | 7 |
| Images in `regular` lighting, good and defective | 4 and 15 | 5 and 15 |

Every lighting condition has the same number of images, so only one image in 6 (Sheet Metal) or 7 (Vial) has the training images' lighting.

**Flag-everything baseline:** a system that calls every image defective would score an image-level F1 of 0.882 on Sheet Metal and 0.857 on Vial, and accuracy of 0.789 and 0.75. A method's image-level F1 on this set only means something if it beats these numbers.

**Defect types:** `test_public/bad` has no subfolders, and file names give only a scene number and a lighting condition, so the files do not label defect types.

## Half A and half B

The public test set is split once, with fixed seed 42. Half A is the development set, and half B is kept for final results only. The file lists are [half_a_files.csv](../outputs/results/02_exploration/half_a_files.csv) and [half_b_files.csv](../outputs/results/02_exploration/half_b_files.csv).

| | Sheet Metal: A / B | Vial: A / B |
| --- | --- | --- |
| Good parts | 2 / 2 | 3 / 2 |
| Defective parts | 7 / 8 | 7 / 8 |
| Images | 54 / 60 | 70 / 70 |

All lighting versions of a part stay in one half. Good and defective parts are shuffled separately. Defect types cannot be balanced, because the files do not label them. An extra good part goes to half A and an extra defective part goes to half B, to keep the halves as even as possible.

## Defect sizes, half A only

Measured from the masks of half A's defective images. White shapes that touch, including at corners, count as one defect. Full results are in [defect_sizes.csv](../outputs/results/02_exploration/defect_sizes.csv) and [defect_size_summary.txt](../outputs/results/02_exploration/defect_size_summary.txt), and the chart is [defect_size_histogram.png](../outputs/figures/defect_size_histogram.png).

| | Sheet Metal | Vial |
| --- | --- | --- |
| Defective parts | 7 | 7 |
| Defective images | 42 | 49 |
| Separate defects, counting every lighting version | 240 | 56 |
| Smallest area | 7 pixels, 0.00016 percent | 5,621 pixels, 0.21132 percent |
| Median area | 965.5 pixels, 0.02165 percent | 41,550 pixels, 1.56203 percent |
| Largest area | 168,272 pixels, 3.77245 percent | 344,970 pixels, 12.9688 percent |

**Limits:** half B's defects were not measured, so its smallest defect is unknown. The same defect is counted once per lighting condition. Width and height come from a box around the defect, so thin diagonal defects can look wider than they are.

## Defect locations, half A only

Measured from the masks of half A's defective images. Each count includes every lighting version of a defect. Full results are in [defect_location_summary.txt](../outputs/results/02_exploration/defect_location_summary.txt). The location maps are mask-derived, so they are not in this repository.

| | Sheet Metal | Vial |
| --- | --- | --- |
| Defects touching a photo edge | 48 of 240 | 0 of 56 |
| Defects within 5 percent of a photo edge | 72 of 240 | 0 of 56 |
| Defects within 10 percent of a photo edge | 96 of 240 | 21 of 56 |
| Parts with a defect within 10 percent of a photo edge | 6 of 7 | 3 of 7 |

| What a crop would lose | Sheet Metal | Vial |
| --- | --- | --- |
| Square from the centre: defects fully lost | 186 of 240 | 14 of 56 |
| Square from the centre: defects partly cut | 12 of 240 | 7 of 56 |
| Square from the centre: defect pixels lost | 91.5 percent | 10.2 percent |
| Central 90 percent: defects fully lost | 0 of 240 | 0 of 56 |
| Central 90 percent: defects partly cut | 72 of 240 | 0 of 56 |
| Central 90 percent: defect pixels lost | 9.2 percent | 0.0 percent |

**Limits:** these are 7 parts per product, and half B's defects are unseen. Distance is measured from the photo's edge, which is not always the part's edge. "Near" at 5 and 10 percent is a working choice, not an official meaning.

## How much good parts vary

Measured on all good training photos. Full results are in [good_part_variation_summary.txt](../outputs/results/02_exploration/good_part_variation_summary.txt) and [good_part_positions.csv](../outputs/results/02_exploration/good_part_positions.csv). The average images look like the dataset's parts, so they are not in this repository.

| | Sheet Metal | Vial |
| --- | --- | --- |
| Photos used | 137 | 291 |
| Typical pixel's variation, in brightness units from 0 to 255 | 39.2 | 2.5 |
| Most varying 1 percent of pixels start at | 75.9 | 92.2 |
| Typical move needed to match the other photos, up or down / sideways | 0 / 0 pixels | 0 / 8 pixels |
| Largest move, up or down / sideways | 88 / 64 pixels | 4 / 32 pixels |
| Photos moved more than 10 pixels | 8 of 137 | 78 of 291 |
| Photos moved more than 50 pixels | 3 of 137 | 0 of 291 |

**Seen in the figures:** Sheet Metal's surface pattern varies across its whole middle area, while its side bands stay steady. Vial's background stays steady, and variation gathers along the vial's outline, lid and contents.

**Limits:** the movement check only measures sliding, in steps of 4 pixels. It does not measure turning. Parts of the photo that stay still can pull answers towards 0, so movement may be understated.

## Brightness: training against half A

Each photo's average brightness, on a scale from 0 (black) to 255 (white). Good and defective half A photos are combined. Full results are in [brightness_summary.txt](../outputs/results/02_exploration/brightness_summary.txt), and the charts are [Sheet Metal](../outputs/figures/brightness_comparison_sheet_metal.png) and [Vial](../outputs/figures/brightness_comparison_vial.png).

| Middle value (lowest to highest) | Sheet Metal | Vial |
| --- | --- | --- |
| Training | 52.6 (44.9 to 65.6) | 210.3 (204.8 to 215.5) |
| `regular` | 52.3 (48.3 to 60.9) | 207.7 (204.6 to 213.0) |
| `overexposed` | 60.4 (56.4 to 70.4) | 215.0 (212.6 to 221.0) |
| `underexposed` | 43.8 (40.1 to 50.9) | 185.6 (180.4 to 190.2) |
| `shift_1` | 53.9 (51.6 to 62.6) | 209.0 (205.8 to 214.2) |
| `shift_2` | 60.9 (58.5 to 70.8) | 210.1 (207.3 to 215.4) |
| `shift_3` | 46.6 (44.4 to 54.1) | 207.9 (204.8 to 213.3) |
| `shift_4` | Does not exist | 209.2 (206.1 to 214.5) |

**Limits:** half A has 9 or 10 photos per condition, from 9 or 10 parts. A histogram does not show where light falls. The private test sets were not looked at, so this says nothing about their lighting.

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
