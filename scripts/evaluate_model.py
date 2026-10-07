import json
from pathlib import Path

from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "datasets" / "liar_800.csv"
MODEL_PATH = BASE_DIR / "models" / "liar_text_model.joblib"


def evaluate() -> dict[str, object]:
	if not DATASET_PATH.is_file() or not MODEL_PATH.is_file():
		raise FileNotFoundError("Run scripts/train_model.py before evaluating the model")

	import csv

	with DATASET_PATH.open(encoding="utf-8", newline="") as dataset_file:
		test_rows = [row for row in csv.DictReader(dataset_file) if row["source_split"] == "test"]
	pipeline = joblib.load(MODEL_PATH)
	actual = [row["label"] for row in test_rows]
	predicted = pipeline.predict([row["statement"] for row in test_rows]).tolist()
	metrics = {
		"test_examples": len(test_rows),
		"accuracy": float(accuracy_score(actual, predicted)),
		"macro_precision": float(precision_score(actual, predicted, average="macro", zero_division=0)),
		"macro_recall": float(recall_score(actual, predicted, average="macro", zero_division=0)),
		"macro_f1": float(f1_score(actual, predicted, average="macro", zero_division=0)),
		"classification_report": classification_report(actual, predicted, output_dict=True, zero_division=0),
	}
	print(json.dumps(metrics, indent=2))
	return metrics


if __name__ == "__main__":
	evaluate()
