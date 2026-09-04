from pathlib import Path
import runpy

SCRIPT_PATH = Path(__file__).resolve().parent / "venv" / "predict_new_image.py"

if not SCRIPT_PATH.is_file():
    raise FileNotFoundError(f"Prediction script not found: {SCRIPT_PATH}")

runpy.run_path(str(SCRIPT_PATH), run_name="__main__")
