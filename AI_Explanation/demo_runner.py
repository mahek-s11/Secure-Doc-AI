"""Generate demo AI underwriting reports for prepared scenarios."""

from pathlib import Path

from explanation import generate_demo_reports


if __name__ == "__main__":
    output_path = Path(__file__).resolve().parent.parent / "reports" / "ai_underwriting_report.json"
    result_path = generate_demo_reports(output_path)
    print(f"Demo AI report file created: {result_path}")
