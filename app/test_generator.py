import json
import sys
from pathlib import Path


DECISIONS_PATH = Path("data/decisions.json")
TEST_SUGGESTIONS_PATH = Path("data/test_suggestions.json")


def load_decisions(path: Path = DECISIONS_PATH) -> list[dict]:
    """
    Loads human decisions about AI suggestions.
    """
    if not path.exists():
        raise FileNotFoundError(
            "No human decisions found. Run: python app/human_decision.py"
        )

    return json.loads(path.read_text(encoding="utf-8"))


def suggest_tests(code: str, decisions: list[dict]) -> list[dict]:
    """
    Suggests tests based on AI findings that were validated by a human.

    This represents the test generation support layer of CollabQA.
    The tests are suggestions and still require human validation before
    being added to the project.
    """
    test_suggestions = []

    accepted_decision_ids = {
        decision["suggestion_id"]
        for decision in decisions
        if decision["human_decision"] in ["Accepted", "Partially accepted"]
    }

    if "AI-SEC-001" in accepted_decision_ids:
        test_suggestions.append({
            "id": "TEST-SEC-001",
            "related_suggestion": "AI-SEC-001",
            "title": "Expired session should be rejected",
            "purpose": (
                "Verify that validate_session returns False when the token exists "
                "but the session expiration date is in the past."
            ),
            "risk_addressed": "Expired sessions may still be accepted",
            "priority": "High",
            "test_code": '''
def test_expired_session_is_invalid():
    token = login("admin", "admin123")
    SESSIONS[token]["expires_at"] = datetime.now() - timedelta(minutes=1)

    assert validate_session(token) is False
'''
        })

    if "AI-AUTH-002" in accepted_decision_ids:
        test_suggestions.append({
            "id": "TEST-AUTH-002",
            "related_suggestion": "AI-AUTH-002",
            "title": "Admin permission behaviour should be explicit",
            "purpose": (
                "Verify and document the current behaviour where the admin user "
                "automatically receives permissions."
            ),
            "risk_addressed": "Admin user receives permissions automatically",
            "priority": "Medium",
            "test_code": '''
def test_admin_has_delete_permission_by_policy():
    assert has_permission("admin", "delete") is True
'''
        })

    if "AI-REL-003" in accepted_decision_ids:
        test_suggestions.append({
            "id": "TEST-REL-003",
            "related_suggestion": "AI-REL-003",
            "title": "Multiple logins should generate unique tokens",
            "purpose": (
                "Verify that two login attempts for the same user do not generate "
                "the same predictable token."
            ),
            "risk_addressed": "Session token is predictable",
            "priority": "Medium",
            "test_code": '''
def test_multiple_logins_generate_different_tokens():
    first_token = login("admin", "admin123")
    second_token = login("admin", "admin123")

    assert first_token != second_token
'''
        })

    return test_suggestions


def save_test_suggestions(test_suggestions: list[dict]) -> None:
    """
    Saves test suggestions to a JSON file.
    """
    TEST_SUGGESTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)

    TEST_SUGGESTIONS_PATH.write_text(
        json.dumps(test_suggestions, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python app/test_generator.py <source_file>")
        sys.exit(1)

    source_file = Path(sys.argv[1])

    if not source_file.exists():
        raise FileNotFoundError(f"File not found: {source_file}")

    code = source_file.read_text(encoding="utf-8")
    decisions = load_decisions()

    test_suggestions = suggest_tests(code, decisions)

    print("\nAI-assisted test suggestions based on human-validated risks:\n")
    print(json.dumps(test_suggestions, indent=4, ensure_ascii=False))

    save_test_suggestions(test_suggestions)

    print("\nTest suggestions saved to data/test_suggestions.json")


if __name__ == "__main__":
    main()