from pathlib import Path

output = Path(__file__).resolve().parent.parent / "datasets" / "demo_cases.json"
output.parent.mkdir(parents=True, exist_ok=True)

payload = [
    {
        "id": "INV-2026-000118",
        "claim": "Government announced a complete shutdown of all digital payments.",
        "status": "LIKELY FALSE",
        "risk": 84,
        "confidence": 89,
        "platform": "X",
        "category": "Financial scam",
    },
    {
        "id": "INV-2026-000119",
        "claim": "A viral image shows a city under water despite no rainfall warning.",
        "status": "MISLEADING",
        "risk": 67,
        "confidence": 74,
        "platform": "Facebook",
        "category": "Disaster misinformation",
    },
]

output.write_text(__import__("json").dumps(payload, indent=2), encoding="utf-8")
print(f"Wrote demo dataset to {output}")
