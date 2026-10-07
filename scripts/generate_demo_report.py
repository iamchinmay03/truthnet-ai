from pathlib import Path

report = Path(__file__).resolve().parent.parent / "reports" / "demo_report.md"
report.parent.mkdir(parents=True, exist_ok=True)
report.write_text(
    "# TruthNet AI Demo Investigation Report\n\n- Claim: Government announced a complete shutdown of all digital payments.\n- Verdict: Likely False\n- Risk: 84/100\n- Confidence: 89%\n- Recommendation: Do not share without independent verification.\n",
    encoding="utf-8",
)
print(f"Saved report to {report}")
