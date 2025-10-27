from pathlib import Path
import os

BASE = Path.home() / "Dhara_DataLake"
DIRS = {k: BASE / k for k in ['raw','processed','datasets','features','exports']}
for d in DIRS.values(): os.makedirs(d, exist_ok=True)
