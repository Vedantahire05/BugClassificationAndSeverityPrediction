import pandas as pd
from pathlib import Path

def load_msr_dataset(filepath):
    path = Path(filepath)
    assert path.exists(), f"File not found: {path}"
    df = pd.read_csv(path)
    return df
