"""Visual inspection demo: PatchCore with EfficientNet-B0 (configuration C6) on MVTec AD 2.

CRISP-DM stage: deployment.

How Streamlit works, in short:
- Streamlit runs this whole file from top to bottom, and draws each st.something
  call on the page in that order.
- Every time someone clicks or picks something, the whole file runs again from
  the top, with the new choice. There is no "main loop" to write.
- Work that should not be repeated on every rerun, like loading the model, is
  wrapped in a function marked with st.cache_resource. Streamlit then runs it
  once and hands back the same result on later reruns.

Start it from the project folder with:  streamlit run app/app.py

Two modes:
- Live: pick a photo (or upload one). The model scores it on the laptop's
  processor and shows the verdict, the score, the heat map and the locked line.
- Saved results: the half B results of the Final test, read from the saved
  files, so the presentation never waits for the model.

The demo model and its lines were fixed in the Lock (DECISIONS.md, 17 Nov 2026).
It is a demonstration of a locked configuration, not a new recommendation. On
half B this configuration failed on Sheet Metal, and the demo shows that too.
"""

import csv
import json
import sys
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st
import torch
from anomalib.data.utils import read_image, read_mask
from anomalib.models import Padim
from anomalib.models.image.patchcore.torch_model import PatchcoreModel

# The project folder is the one above app/, so the app works from any start folder
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_FOLDER))
from src import final_test

MODEL_FOLDER = PROJECT_FOLDER / "data/demo_models"
PHOTO_FOLDER = PROJECT_FOLDER / "data/demo_photos"
RESULTS = PROJECT_FOLDER / "outputs/results"
FIGURES = PROJECT_FOLDER / "outputs/figures"
PRODUCTS = {"Sheet Metal": "sheet_metal", "Vial": "vial"}
CONFIG_ID = "C6"
SEED = "42"
# The project's main business setting, the same as in the Lock
DEFECT_RATE = 0.01
COST_RATIO = 10
# Half A parts, the same lists as in every notebook, so each photo can be labelled with its half
HALF_A_PARTS = {
    "sheet_metal": {"good": ["001", "002"], "bad": ["000", "004", "005", "007", "009", "012", "013"]},
    "vial": {"good": ["000", "002", "003"], "bad": ["001", "008", "010", "011", "012", "013", "014"]},
}


@st.cache_resource
def load_model(product):
    """Rebuild C6 for one product from its saved memory bank. Runs once per product."""
    saved = torch.load(MODEL_FOLDER / (CONFIG_ID + "_" + product + "_seed" + SEED + "_memory_bank.pt"),
                       map_location="cpu", weights_only=True)
    # The pretrained network is downloaded once by timm; the memory bank comes from the Kaggle run
    model = PatchcoreModel(backbone=saved["backbone"], layers=saved["layers"], pre_trained=True,
                           num_neighbors=saved["num_neighbors"])
    model.memory_bank = saved["memory_bank"]
    model.eval()
    # The same preparation as in every notebook: squash to 256 x 256, ImageNet normalisation
    recipe = Padim.configure_pre_processor(image_size=(saved["image_size"], saved["image_size"])).transform
    return model, recipe


@st.cache_data
def locked_lines(product):
    """Return the two locked lines for C6 seed 42: the benchmark line and the cost-based line."""
    with open(RESULTS / "07_core/C6" / ("C6_" + product + "_seed42_metrics.json"), encoding="utf-8") as file:
        benchmark = json.load(file)["threshold"]
    cost_line = None
    with open(RESULTS / "07_evaluation/cost_by_run.csv", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if (row["config"] == CONFIG_ID and row["product"] == product and row["seed"] == SEED
                    and float(row["defect_rate"]) == DEFECT_RATE and float(row["cost_ratio"]) == COST_RATIO):
                cost_line = float(row["cheapest_threshold"])
    return benchmark, cost_line


@st.cache_data
def kaggle_scores(product):
    """Return the scores Kaggle gave each photo, from the saved half A and half B files."""
    scores = {}
    files = [RESULTS / "final_test/half_a_rerun/C6" / ("C6_" + product + "_seed42_photo_scores.csv"),
             RESULTS / "final_test/half_b/C6" / ("C6_" + product + "_seed42_halfB_photo_scores.csv")]
    for score_file in files:
        with open(score_file, encoding="utf-8") as file:
            for row in csv.DictReader(file):
                scores[(row["label"], row["file_name"])] = float(row["score"])
    return scores


def half_of(product, label, file_name):
    """Say which half of the public test set a photo belongs to."""
    part = file_name.split("_")[0]
    if part in HALF_A_PARTS[product][label]:
        return "half A (development)"
    if part in final_test.HALF_B_PARTS[product][label]:
        return "half B (final test)"
    return "not in the public test set"


def score_photo(model, recipe, image_path, mask_path):
    """Prepare one photo, score it, and return the prepared photo, the mask, the heat map and the score."""
    image = read_image(image_path, as_tensor=True)
    if mask_path is not None:
        mask = read_mask(mask_path, as_tensor=True)
        # The recipe resizes the mask with nearest-neighbour, so it stays pure defect or no defect
        image, mask = recipe(image, mask)
    else:
        image = recipe(image)
        mask = None
    with torch.no_grad():
        output = model(image.unsqueeze(0))
    heat_map = output.anomaly_map.squeeze()
    score = float(output.pred_score.reshape(-1)[0])
    return image, mask, heat_map, score


def draw(recipe, image, mask, heat_map):
    """Draw the photo and its heat map side by side, with the mask outline in red."""
    normalize_step = recipe.transforms[1]
    means = torch.tensor(normalize_step.mean).view(3, 1, 1)
    stds = torch.tensor(normalize_step.std).view(3, 1, 1)
    # Undo the normalisation, so the photo looks as it did before preparation
    photo = (image * stds + means).clamp(0, 1)
    figure, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    axes[0].imshow(photo[0], cmap="gray", vmin=0, vmax=1)
    axes[0].set_title("Photo, as the model sees it")
    picture = axes[1].imshow(heat_map, cmap="Blues")
    axes[1].set_title("Heat map: darker is more suspicious")
    figure.colorbar(picture, ax=axes[1], fraction=0.046)
    if mask is not None and bool(mask.any()):
        for axis in axes:
            axis.contour(mask.squeeze().float(), levels=[0.5], colors="red", linewidths=0.8)
    for axis in axes:
        axis.axis("off")
    figure.tight_layout()
    return figure


def live_mode(product, product_label):
    """Score one photo on the laptop and explain the verdict."""
    model_file = MODEL_FOLDER / (CONFIG_ID + "_" + product + "_seed" + SEED + "_memory_bank.pt")
    if not model_file.exists():
        st.error("The demo model is missing. Download it from the Kaggle run phase-9-demo-model-c6 into "
                 + str(MODEL_FOLDER) + ". See app/README.md.")
        return
    model, recipe = load_model(product)
    benchmark, cost_line = locked_lines(product)

    source = st.radio("Photo", ["Pick from the public test set", "Upload my own"], horizontal=True)
    image_path = None
    mask_path = None
    label = None
    file_name = None
    if source == "Pick from the public test set":
        test_folder = PHOTO_FOLDER / product / "test_public"
        if not test_folder.exists():
            st.error("No photos found in " + str(test_folder) + ". See app/README.md.")
            return
        label = st.selectbox("Good or defective part", ["good", "bad"])
        names = []
        for photo_file in sorted((test_folder / label).glob("*.png")):
            names.append(photo_file.name)
        file_name = st.selectbox("Photo", names)
        image_path = test_folder / label / file_name
        candidate_mask = test_folder / "ground_truth" / label / file_name.replace(".png", "_mask.png")
        if candidate_mask.exists():
            mask_path = candidate_mask
        st.caption(product_label + ", " + label + " part, " + file_name + ", " + half_of(product, label, file_name)
                   + ". MVTec AD 2, CC BY-NC-SA 4.0.")
    else:
        uploaded = st.file_uploader("A photo of the same product", type=["png", "jpg", "jpeg"])
        if uploaded is None:
            return
        # anomalib reads photos from a file, so the upload is saved to a temporary file first
        temporary = Path(tempfile.gettempdir()) / ("inspection_upload" + Path(uploaded.name).suffix)
        temporary.write_bytes(uploaded.getvalue())
        image_path = temporary

    image, mask, heat_map, score = score_photo(model, recipe, image_path, mask_path)
    rejected = score > cost_line
    column_1, column_2, column_3 = st.columns(3)
    # Short words, so the verdict fits in its column
    column_1.metric("Verdict", "Reject" if rejected else "Pass")
    column_2.metric("Anomaly score", str(round(score, 2)))
    column_3.metric("Locked cost-based line", str(round(cost_line, 2)))
    st.write("**Why this line:** it was chosen on half A as the cheapest line, assuming 1 percent of parts are "
             "defective and a missed defect costs 10 times a wrongly rejected good part. The benchmark line "
             "(mean plus 3 standard deviations of good validation pixels) is " + str(round(benchmark, 2))
             + ", which would " + ("reject" if score > benchmark else "pass") + " this photo.")
    st.pyplot(draw(recipe, image, mask, heat_map))
    st.caption("The score is not the darkest pixel of the map: PatchCore re-weights its most unusual patch "
               "to make the photo's score, and the map is smoothed afterwards.")
    if file_name is not None:
        saved = kaggle_scores(product).get((label, file_name))
        if saved is not None:
            st.caption("Check: Kaggle's GPU gave this photo a score of " + str(round(saved, 4))
                       + ". The laptop's processor gives " + str(round(score, 4)) + ".")
        if (label == "bad") != rejected:
            st.warning("The verdict is wrong for this photo: it is a " + ("defective" if label == "bad" else "good")
                       + " part. See the saved results for how often this happens on half B.")


def saved_mode(product, product_label):
    """Show the Final test results on half B from the saved files."""
    st.write("**Final test, half B.** Every configuration was scored once, with settings and lines locked "
             "beforehand on half A. These are the reported results.")
    st.image(str(FIGURES / "final_half_a_vs_half_b_auroc.png"),
             caption="Did half A predict half B? Each point is one configuration.")
    st.image(str(FIGURES / "final_cost_at_locked_lines.png"),
             caption="Expected cost per part at the locked lines. Passing everything costs 0.10.")
    st.image(str(FIGURES / "final_recommended_scores_and_confusion.png"),
             caption="The locked recommendations: C6 on Sheet Metal and C7 on Vial, at their cost-based lines.")
    rows = []
    with open(RESULTS / "final_test/final_cost_main_setting.csv", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            if row["product"] == product:
                rows.append({"configuration": row["config"], "cost per part": float(row["cost_line"]),
                             "share of defects missed": float(row["cost_line_miss"]),
                             "share of good parts rejected": float(row["cost_line_false_reject"])})
    st.write("**" + product_label + ", at the locked cost-based lines**")
    st.dataframe(rows, hide_index=True)
    # The galleries show dataset photos, so they are not in git; they appear only if downloaded
    gallery = FIGURES / ("gallery_halfB_failures_C6_" + product + "_seed42.png")
    if gallery.exists():
        with st.expander("Half B failure gallery for C6 (hits, hardest defective, hardest good)"):
            st.image(str(gallery), caption="MVTec AD 2, CC BY-NC-SA 4.0.")


st.set_page_config(page_title="Visual inspection demo", layout="wide")
st.title("Visual inspection: is this part defective?")
st.write("PatchCore with EfficientNet-B0 (configuration C6), fitted on good parts only. "
         "A student project on the MVTec AD 2 benchmark; not for commercial use.")
product_label = st.sidebar.selectbox("Product", list(PRODUCTS.keys()))
mode = st.sidebar.radio("Mode", ["Live", "Saved results"])
if mode == "Live":
    live_mode(PRODUCTS[product_label], product_label)
else:
    saved_mode(PRODUCTS[product_label], product_label)
st.sidebar.caption("Lines and settings locked on 17 Nov 2026. Half B: the final test set.")
