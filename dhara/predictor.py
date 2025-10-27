import numpy as np, tensorflow as tf, rasterio
from PIL import Image
from dhara.config import DIRS

MODEL_PATH = DIRS["exports"] / "dhara_baseline_model.keras"

def load_model():
    try:
        return tf.keras.models.load_model(MODEL_PATH)
    except Exception:
        print("⚠️ No model found, using dummy mode.")
        return None

def predict_health(ndvi_tif):
    model = load_model()
    with rasterio.open(ndvi_tif) as src:
        arr = src.read(1)
    arr_u8 = ((arr + 1) / 2 * 255).astype(np.uint8)
    img = Image.fromarray(arr_u8).resize((64, 64))
    x = np.expand_dims(np.expand_dims(np.array(img), -1), 0) / 255.0

    classes = ["healthy", "moderate", "stressed"]
    if model is None:
        return {"predicted_class": "moderate", "probabilities": {"healthy": 0.3, "moderate": 0.4, "stressed": 0.3}}
    preds = model.predict(x)
    i = int(np.argmax(preds))
    return {"predicted_class": classes[i], "probabilities": {classes[j]: float(preds[0][j]) for j in range(3)}}
