import csv
import json
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "datasets"
SOURCE_DIR = DATASET_DIR / "liar-source"
DATASET_PATH = DATASET_DIR / "liar_800.csv"
MODEL_PATH = BASE_DIR / "models" / "liar_text_model.joblib"
METRICS_PATH = BASE_DIR / "reports" / "liar_800_evaluation.json"
SOURCE_URL = "https://www.cs.ucsb.edu/~william/data/liar_dataset.zip"
LABELS = ("pants-fire", "false", "barely-true", "half-true", "mostly-true", "true")
SEED = 42
SPLIT_SIZES = {"train": 640, "validation": 80, "test": 80}
SOURCE_SPLITS = {"train": "train.tsv", "validation": "valid.tsv", "test": "test.tsv"}


def ensure_source_dataset() -> None:
    required_files = [SOURCE_DIR / filename for filename in SOURCE_SPLITS.values()]
    if all(path.is_file() for path in required_files):
        return

    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = DATASET_DIR / "liar_dataset.zip"
    if not archive_path.is_file():
        request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "TruthNet-AI-research/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            archive_path.write_bytes(response.read())

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path) as archive:
        root = SOURCE_DIR.resolve()
        for entry in archive.infolist():
            destination = (SOURCE_DIR / entry.filename).resolve()
            if destination != root and root not in destination.parents:
                raise ValueError(f"Unsafe path in LIAR archive: {entry.filename}")
        archive.extractall(SOURCE_DIR)

    missing = [path.name for path in required_files if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"LIAR archive is missing expected files: {', '.join(missing)}")


def read_source_split(filename: str, split_name: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with (SOURCE_DIR / filename).open(encoding="utf-8", newline="") as source_file:
        for fields in csv.reader(source_file, delimiter="\t"):
            if len(fields) < 14 or fields[1] not in LABELS:
                continue
            statement = fields[2].strip()
            if not statement:
                continue
            rows.append(
                {
                    "source_id": fields[0],
                    "label": fields[1],
                    "statement": statement,
                    "subject": fields[3],
                    "speaker": fields[4],
                    "party": fields[7],
                    "source_split": split_name,
                }
            )
    return rows


def stratified_sample(rows: list[dict[str, str]], count: int, seed: int) -> list[dict[str, str]]:
    labels = [row["label"] for row in rows]
    if count >= len(rows):
        raise ValueError(f"Requested {count} rows, but source split only has {len(rows)}")
    selected, _ = train_test_split(
        rows,
        train_size=count,
        random_state=seed,
        stratify=labels,
    )
    return selected


def prepare_dataset() -> list[dict[str, str]]:
    ensure_source_dataset()
    selected_rows: list[dict[str, str]] = []
    for offset, (split_name, filename) in enumerate(SOURCE_SPLITS.items()):
        source_rows = read_source_split(filename, split_name)
        selected_rows.extend(
            stratified_sample(source_rows, SPLIT_SIZES[split_name], SEED + offset)
        )

    if len(selected_rows) != 800:
        raise ValueError(f"Expected exactly 800 dataset rows, got {len(selected_rows)}")

    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    with DATASET_PATH.open("w", encoding="utf-8", newline="") as dataset_file:
        writer = csv.DictWriter(dataset_file, fieldnames=list(selected_rows[0]))
        writer.writeheader()
        writer.writerows(selected_rows)
    return selected_rows


def make_pipeline(regularization: float) -> Pipeline:
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=2,
                    max_features=50000,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    C=regularization,
                    class_weight="balanced",
                    max_iter=2000,
                    random_state=SEED,
                ),
            ),
        ]
    )


def score_metrics(actual: list[str], predicted: list[str]) -> dict[str, float]:
    return {
        "accuracy": float(accuracy_score(actual, predicted)),
        "macro_precision": float(precision_score(actual, predicted, labels=LABELS, average="macro", zero_division=0)),
        "macro_recall": float(recall_score(actual, predicted, labels=LABELS, average="macro", zero_division=0)),
        "macro_f1": float(f1_score(actual, predicted, labels=LABELS, average="macro", zero_division=0)),
    }


def train() -> dict[str, Any]:
    rows = prepare_dataset()
    training_rows = [row for row in rows if row["source_split"] == "train"]
    validation_rows = [row for row in rows if row["source_split"] == "validation"]
    test_rows = [row for row in rows if row["source_split"] == "test"]

    x_train = [row["statement"] for row in training_rows]
    y_train = [row["label"] for row in training_rows]
    x_validation = [row["statement"] for row in validation_rows]
    y_validation = [row["label"] for row in validation_rows]

    candidates = []
    for regularization in (0.5, 1.0, 2.0, 4.0):
        candidate = make_pipeline(regularization)
        candidate.fit(x_train, y_train)
        predicted = candidate.predict(x_validation).tolist()
        candidates.append(
            {
                "regularization": regularization,
                "metrics": score_metrics(y_validation, predicted),
            }
        )
    best = max(
        candidates,
        key=lambda item: (
            item["metrics"]["macro_f1"],
            item["metrics"]["accuracy"],
            -item["regularization"],
        ),
    )

    final_rows = training_rows + validation_rows
    pipeline = make_pipeline(best["regularization"])
    pipeline.fit(
        [row["statement"] for row in final_rows],
        [row["label"] for row in final_rows],
    )
    x_test = [row["statement"] for row in test_rows]
    y_test = [row["label"] for row in test_rows]
    predicted_test = pipeline.predict(x_test).tolist()
    probabilities = pipeline.predict_proba(x_test)
    try:
        auc = float(
            roc_auc_score(
                y_test,
                probabilities,
                labels=list(pipeline.classes_),
                multi_class="ovr",
                average="macro",
            )
        )
    except ValueError:
        auc = None

    test_metrics = score_metrics(y_test, predicted_test)
    test_metrics["macro_roc_auc_ovr"] = auc
    report = {
        "model": "TF-IDF + Logistic Regression",
        "dataset": "LIAR benchmark",
        "dataset_rows": len(rows),
        "split_counts": {name: len(split) for name, split in (("train", training_rows), ("validation", validation_rows), ("test", test_rows))},
        "classes": list(LABELS),
        "seed": SEED,
        "selected_regularization": best["regularization"],
        "validation_candidates": candidates,
        "validation_metrics": best["metrics"],
        "test_metrics": test_metrics,
        "classification_report": classification_report(
            y_test,
            predicted_test,
            labels=LABELS,
            output_dict=True,
            zero_division=0,
        ),
        "citation": "William Yang Wang. 2017. Liar, Liar Pants on Fire: A New Benchmark Dataset for Fake News Detection. ACL 2017.",
        "dataset_notice": "LIAR is provided for research use; consult its README and original paper for terms and limitations.",
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(report, indent=2, allow_nan=False), encoding="utf-8")
    return report


if __name__ == "__main__":
    result = train()
    print(f"Saved {result['dataset_rows']} labeled examples to {DATASET_PATH}")
    print(f"Saved trained model to {MODEL_PATH}")
    print(f"Held-out test metrics: {json.dumps(result['test_metrics'], sort_keys=True)}")
