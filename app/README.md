# Visual inspection demo

A small Streamlit app that shows the locked configuration C6 (PatchCore with EfficientNet-B0) at work on MVTec AD 2 photos. It runs on a laptop's processor, with no GPU.

- **Live mode:**
  - Pick a photo from the public test set, or upload one.
  - The app shows the verdict (pass or reject), the anomaly score, the heat map with the defect mask outlined, and the locked line with the cost assumption behind it.
  - For public test photos, it also shows the score Kaggle's GPU gave the same photo, as a check.
- **Saved results mode:** the half B results of the Final test, read from saved files. This mode is for a smooth presentation.

The demo shows one locked configuration, not a new recommendation. On half B, C6 failed on Sheet Metal at its locked line, and the demo shows that too.

## What it needs (none of it is in git)

1. **The demo model.** Download the output of the Kaggle notebook `phase-9-demo-model-c6` ([09_demo_model_C6.ipynb](../notebooks/09_demo_model_C6.ipynb)) and put `C6_sheet_metal_seed42_memory_bank.pt` and `C6_vial_seed42_memory_bank.pt` in `data/demo_models/`.
2. **Photos.** Download MVTec AD 2 from the [official page](https://www.mvtec.com/research-teaching/datasets/mvtec-ad-2) (CC BY-NC-SA 4.0). Put the `test_public` folders in `data/demo_photos/sheet_metal/test_public/` and `data/demo_photos/vial/test_public/`.
3. **The pretrained EfficientNet-B0.** The `timm` library downloads it the first time the app starts. It is about 20 MB.

## Start it

From the project folder, with the project's environment active:

```bash
streamlit run app/app.py
```

Streamlit opens the app in the browser, at `http://localhost:8501` by default.
