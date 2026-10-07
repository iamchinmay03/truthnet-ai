from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "models" / "liar_text_model.joblib"
LABEL_RISK = {
    "pants-fire": 98,
    "false": 88,
    "barely-true": 70,
    "half-true": 50,
    "mostly-true": 30,
    "true": 12,
}
LABEL_VERDICT = {
    "pants-fire": "LIKELY FALSE",
    "false": "LIKELY FALSE",
    "barely-true": "MISLEADING",
    "half-true": "PARTLY TRUE",
    "mostly-true": "MOSTLY TRUE",
    "true": "LIKELY TRUE",
}


@lru_cache(maxsize=1)
def _load_pipeline() -> Any | None:
    if not MODEL_PATH.is_file():
        return None
    return joblib.load(MODEL_PATH)


def predict_claim(text: str) -> dict[str, Any] | None:
    pipeline = _load_pipeline()
    if pipeline is None:
        return None

    probabilities = pipeline.predict_proba([text])[0]
    best_index = int(probabilities.argmax())
    label = str(pipeline.classes_[best_index])
    return {
        "label": label,
        "verdict": LABEL_VERDICT[label],
        "confidence": float(probabilities[best_index]),
        "risk_score": LABEL_RISK[label],
    }