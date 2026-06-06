import csv
from datetime import datetime
from pathlib import Path


AUDIT_LOG_PATH = Path("data/audit_log.csv")


def append_audit_log(entry: dict) -> None:
    """
    Saves one human decision in the audit log.

    The audit log is used to preserve traceability and accountability:
    it records what the AI suggested, what the human decided, who was
    responsible and why the decision was made.
    """
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    file_exists = AUDIT_LOG_PATH.exists()
    file_is_empty = not file_exists or AUDIT_LOG_PATH.stat().st_size == 0

    with AUDIT_LOG_PATH.open("a", newline="", encoding="utf-8") as file:
        fieldnames = [
            "timestamp",
            "suggestion_id",
            "category",
            "risk",
            "title",
            "human_decision",
            "justification",
            "responsible",
            "human_validation_required"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file_is_empty:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "suggestion_id": entry["suggestion_id"],
            "category": entry["category"],
            "risk": entry["risk"],
            "title": entry["title"],
            "human_decision": entry["human_decision"],
            "justification": entry["justification"],
            "responsible": entry["responsible"],
            "human_validation_required": entry["human_validation_required"]
        })