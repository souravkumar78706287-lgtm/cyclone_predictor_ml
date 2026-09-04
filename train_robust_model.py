from pathlib import Path
import runpy

SCRIPT_PATH = Path(__file__).resolve().parent / "venv" / "train_robust_model.py"

if not SCRIPT_PATH.is_file():
    raise FileNotFoundError(f"Training script not found: {SCRIPT_PATH}")

runpy.run_path(str(SCRIPT_PATH), run_name="__main__")
