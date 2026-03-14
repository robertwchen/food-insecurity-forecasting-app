from pathlib import Path
import os

BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent
DEFAULT_MODEL_PATH = REPO_ROOT / "training" / "artifacts" / "model.joblib"
DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

MODEL_ARTIFACT_PATH = Path(
    os.getenv("MODEL_ARTIFACT_PATH", str(DEFAULT_MODEL_PATH))
).resolve()


def get_cors_origins() -> list[str]:
    raw_value = os.getenv("ALLOWED_ORIGINS", "")
    if not raw_value.strip():
        return DEFAULT_CORS_ORIGINS

    origins = [origin.strip() for origin in raw_value.split(",")]
    return [origin for origin in origins if origin]
