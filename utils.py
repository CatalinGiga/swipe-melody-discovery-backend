from typing import List, Dict, Any
import json
from pathlib import Path

# Data access functions
def read_data(file_path: Path) -> List[Dict[str, Any]]:
    with open(file_path, "r") as f:
        return json.load(f)

def write_data(file_path: Path, data: List[Dict[str, Any]]) -> None:
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2) 