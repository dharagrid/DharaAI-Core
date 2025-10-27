import rasterio, numpy as np, pandas as pd, sqlite3
from dhara.config import DIRS
from dhara.feature_store import FEAT_DB

def process_ndvi(tif_path, farm_id, scan_date):
    with rasterio.open(tif_path) as src:
        arr = src.read(1).astype(float)

    mean_ndvi = float(np.nanmean(arr))
    std_ndvi = float(np.nanstd(arr))
    min_ndvi = float(np.nanmin(arr))
    max_ndvi = float(np.nanmax(arr))

    out_csv = DIRS["exports"] / f"{farm_id}_summary.csv"
    pd.DataFrame([{
        "farm_id": farm_id, "scan_date": scan_date,
        "mean_ndvi": mean_ndvi, "std_ndvi": std_ndvi,
        "min_ndvi": min_ndvi, "max_ndvi": max_ndvi
    }]).to_csv(out_csv, index=False)

    with sqlite3.connect(FEAT_DB) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO field_features VALUES (?, ?, ?, ?, ?, ?, ?)",
            (farm_id, scan_date, mean_ndvi, std_ndvi, min_ndvi, max_ndvi, "auto-logged")
        )
        conn.commit()

    print("✅ NDVI processed:", out_csv)
    return {"mean": mean_ndvi, "std": std_ndvi, "min": min_ndvi, "max": max_ndvi}
