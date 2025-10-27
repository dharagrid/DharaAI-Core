import rasterio, numpy as np, os, random
from pathlib import Path
from PIL import Image
from dhara.config import DIRS

TILE_SIZE = 256
TRAIN_SPLIT, VAL_SPLIT, TEST_SPLIT = 0.7, 0.2, 0.1

def build_dataset(ndvi_tif_path, farm_id):
    os.makedirs(DIRS["datasets"], exist_ok=True)
    with rasterio.open(ndvi_tif_path) as src:
        ndvi = src.read(1)
    h, w = ndvi.shape
    tiles = []
    for y in range(0, h, TILE_SIZE):
        for x in range(0, w, TILE_SIZE):
            window = ndvi[y:y+TILE_SIZE, x:x+TILE_SIZE]
            if window.shape != (TILE_SIZE, TILE_SIZE): continue
            m = np.nanmean(window)
            if m < 0.3: label = "stressed"
            elif m < 0.6: label = "moderate"
            else: label = "healthy"
            tiles.append((window, label))

    random.shuffle(tiles)
    total = len(tiles)
    n_train, n_val = int(total*TRAIN_SPLIT), int(total*VAL_SPLIT)
    splits = {"train": tiles[:n_train], "val": tiles[n_train:n_train+n_val], "test": tiles[n_train+n_val:]}

    for split, data in splits.items():
        for arr, label in data:
            folder = DIRS["datasets"] / split / label
            os.makedirs(folder, exist_ok=True)
            fname = f"{farm_id}_{random.randint(10000,99999)}.png"
            arr_u8 = ((arr + 1) / 2 * 255).astype(np.uint8)
            Image.fromarray(arr_u8).save(folder / fname)
    print(f"✅ Dataset built: {total} tiles ({n_train} train / {n_val} val / {total-n_train-n_val} test)")
