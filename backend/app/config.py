from pathlib import Path
import os

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent
DEFAULT_MODEL_PATH = REPO_ROOT / "training" / "artifacts" / "model.joblib"

MODEL_ARTIFACT_PATH = Path(
    os.getenv("MODEL_ARTIFACT_PATH", str(DEFAULT_MODEL_PATH))
).resolve()
