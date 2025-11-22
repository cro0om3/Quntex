import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent.parent


def load_json(filename: str) -> Any:
    """Load demo JSON data from the demo_data folder with relaxed encoding handling."""
    data_path = BASE_DIR / "demo_data" / filename
    encodings = ("utf-8", "utf-8-sig", "cp1252", "latin-1")
    last_error = None
    for enc in encodings:
        try:
            with data_path.open("r", encoding=enc) as f:
                return json.load(f)
        except Exception as exc:
            last_error = exc
            continue
    raise last_error
