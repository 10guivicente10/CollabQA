import csv
import json
import re
from pathlib import Path


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")

AI_SUGGESTIONS_PATH = DATA_DIR / "ai_suggestions.json"
DECISIONS_PATH = DATA_DIR / "decisions.json"
TEST_SUGGESTIONS_PATH = DATA_DIR / "test_suggestions.json"
AUDIT_LOG_PATH = DATA_DIR / "audit_log.csv"

FAILING_TEST_OUTPUT_PATH = REPORTS_DIR / "failing_test_output.txt"
PASSING_TEST_OUTPUT_PATH = REPORTS_DIR / "passing_test_output.txt"
COVERAGE_AFTER_FIX_PATH = REPORTS_DIR / "coverage_after_fix.txt"

FINAL_RESULTS_CSV = REPORTS_DIR / "final_results.csv"
FINAL_SUMMARY_JSON = REPORTS_DIR / "final_summary.json"


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []

    return json.loads(path.read_text(encoding="utf-8"))


def count_audit_log_entries(path: Path) -> int:
    if not path.exists():
        return 0

    with path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return sum(1 for _ in reader)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")


def parse_pytest_output(output: str) -> dict:
    passed_match = re.search(r"(\d+)\s+passed", output)
    failed_match = re.search(r"(\d+)\s+failed", output)

    return {
        "passed": int(passed_match.group(1)) if passed_match else 0,
        "failed": int(failed_match.group(1)) if failed_match else 0
    }


def parse_total_coverage(output: str) -> int | None:
    for line in output.splitlines():
        if line.strip().startswith("TOTAL"):
            match = re.search(r"(\d+)%", line)
            if match:
                return int(match.group(1))

    return None


def calculate_metrics() -> dict:
    ai_suggestions = load_json(AI_SUGGESTIONS_PATH)
    decisions = load_json(DECISIONS_PATH)
    test_suggestions = load_json(TEST_SUGGESTIONS_PATH)

    failing_output = read_text(FAILING_TEST_OUTPUT_PATH)
    passing_output = read_text(PASSING_TEST_OUTPUT_PATH)
    coverage_output = read_text(COVERAGE_AFTER_FIX_PATH)

    failing_results = parse_pytest_output(failing_output)
    passing_results = parse_pytest_output(passing_output)
    coverage_after_fix = parse_total_coverage(coverage_output)

    accepted = [
        decision for decision in decisions
        if decision["human_decision"] == "Accepted"
    ]

    partially_accepted = [
        decision for decision in decisions
        if decision["human_decision"] == "Partially accepted"
    ]

    rejected = [
        decision for decision in decisions
        if decision["human_decision"] == "Rejected"
    ]

    high_risk_suggestions = [
        suggestion for suggestion in ai_suggestions
        if suggestion["risk"] == "High"
    ]

    high_priority_tests = [
        test for test in test_suggestions
        if test["priority"] == "High"
    ]

    metrics = {
        "ai_suggestions": len(ai_suggestions),
        "human_validated_suggestions": len(decisions),
        "accepted_suggestions": len(accepted),
        "partially_accepted_suggestions": len(partially_accepted),
        "rejected_suggestions": len(rejected),
        "high_risk_suggestions": len(high_risk_suggestions),
        "test_suggestions": len(test_suggestions),
        "high_priority_test_suggestions": len(high_priority_tests),
        "audit_log_entries": count_audit_log_entries(AUDIT_LOG_PATH),
        "failing_stage_failed_tests": failing_results["failed"],
        "failing_stage_passed_tests": failing_results["passed"],
        "passing_stage_failed_tests": passing_results["failed"],
        "passing_stage_passed_tests": passing_results["passed"],
        "coverage_after_fix_percent": coverage_after_fix
    }

    return metrics


def save_metrics(metrics: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with FINAL_RESULTS_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["metric", "value"])

        for key, value in metrics.items():
            writer.writerow([key, value])

    FINAL_SUMMARY_JSON.write_text(
        json.dumps(metrics, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    metrics = calculate_metrics()
    save_metrics(metrics)

    print("\nCollabQA metrics summary:\n")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    print("\nMetrics saved to:")
    print(f"- {FINAL_RESULTS_CSV}")
    print(f"- {FINAL_SUMMARY_JSON}")


if __name__ == "__main__":
    main()