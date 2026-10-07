# TruthNet AI

TruthNet AI is a professional misinformation analysis platform designed for the Social Network Analysis subject. It combines NLP, evidence checking, graph analytics, multimodal analysis, propagation studies, and explainable AI to assess whether online content is likely true, misleading, manipulated, or unverified.

## Project goals

- Analyze claims from text, URL, image, and social-network datasets
- Extract and evaluate individual claims
- Retrieve and compare authoritative evidence
- Detect suspicious propagation and coordinated behavior
- Examine multimodal consistency and media integrity
- Produce explainable risk and credibility results
- Provide demo-ready research workflows for academic evaluation

## Repository structure

- `backend/` – FastAPI backend and analysis services
- `frontend/` – React + TypeScript UI
- `scripts/` – dataset and model utility scripts
- `docs/` – project notes and documentation
- `docker/` – container-related configuration
- `reports/` – generated reports
- `datasets/` – demo datasets
- `models/` – trained model artifacts

## Quick start

### One-click startup (Windows)

Double-click the launcher in the project root:

- `run-project.bat`

Or run this PowerShell command:

```powershell
./run-project.ps1
```

This launches the FastAPI backend on port 8000 and the Vite frontend on port 5173, with API calls proxied correctly between them.

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```powershell
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

### Docker

```bash
docker compose up --build
```

## Demo mode

The app includes demo investigations and synthetic network data so the platform works without external APIs. Any external service can be marked as unavailable and the system gracefully falls back to local demo logic.

## Local text model

The claim text classifier is trained on an exactly 800-row stratified sample of the research-use-only LIAR benchmark: 640 training rows, 80 validation rows, and 80 held-out test rows. It uses TF-IDF features with logistic regression; regularization is selected against the validation split. Training and evaluation are reproducible with:

```powershell
python scripts/train_model.py
python scripts/evaluate_model.py
```

The dataset is saved to `datasets/liar_800.csv`, the fitted model to `models/liar_text_model.joblib`, and measured metrics to `reports/liar_800_evaluation.json`. The model predicts the LIAR statement-rating labels; it does not verify claims against live sources. Evidence and propagation results remain illustrative demo data. Consult `datasets/liar-source/README` and the cited paper for dataset terms and limitations.

On this sample, the held-out test accuracy is 25.0% and macro-F1 is 23.2%. This is a modest research baseline, not a production-grade fact checker; the test set contains only 80 examples.

## Important note

This project is an academic prototype that emphasizes a realistic investigation workflow and responsible AI messaging. It does not claim to prove truth; it estimates risk using structured evidence, propagation patterns, and model output.
