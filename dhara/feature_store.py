import sqlite3
from dhara.config import DIRS

FEAT_DB = DIRS["features"] / "features.db"

def init_feature_store():
    schema = '''
    CREATE TABLE IF NOT EXISTS field_features (
        farm_id TEXT,
        scan_date TEXT,
        mean_ndvi REAL,
        std_ndvi REAL,
        min_ndvi REAL,
        max_ndvi REAL,
        notes TEXT,
        PRIMARY KEY(farm_id, scan_date)
    );
    '''
    with sqlite3.connect(FEAT_DB) as conn:
        conn.executescript(schema)
    print("✅ Feature Store initialized at", FEAT_DB)
