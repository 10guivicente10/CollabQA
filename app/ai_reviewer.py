import json
import sys
from pathlib import Path


def review_code(code: str) -> list[dict]:
    """
    Analyses source code and returns AI-like quality suggestions.

    This module represents the AI assistance layer of CollabQA.
    The suggestions are treated as hypotheses that must be validated
    by a human reviewer.
    """
    suggestions = []

    if "def validate_session" in code and "return token in SESSIONS" in code:
        suggestions.append({
            "id": "AI-SEC-001",
            "category": "Security",
            "risk": "High",
            "title": "Expired sessions may still be accepted",
            "description": (
                "The validate_session function only checks if the token exists "
                "in the active sessions dictionary. It does not verify whether "
                "the session has expired."
            ),
            "recommendation": (
                "Update validate_session to check the expires_at timestamp before "
                "accepting a session as valid."
            ),
            "affected_quality_attributes": [
                "Security",
                "Reliability",
                "Correctness"
            ],
            "human_validation_required": True
        })

    if 'if username == "admin":' in code and "return True" in code:
        suggestions.append({
            "id": "AI-AUTH-002",
            "category": "Authorization",
            "risk": "Medium",
            "title": "Admin user receives permissions automatically",
            "description": (
                "The has_permission function gives all permissions to the admin "
                "user without checking the configured permission list."
            ),
            "recommendation": (
                "Validate admin permissions explicitly or document this behaviour "
                "as an intentional policy decision."
            ),
            "affected_quality_attributes": [
                "Security",
                "Maintainability"
            ],
            "human_validation_required": True
        })

    if 'token = f"token_{username}"' in code:
        suggestions.append({
            "id": "AI-REL-003",
            "category": "Reliability",
            "risk": "Medium",
            "title": "Session token is predictable",
            "description": (
                "The session token is generated directly from the username. "
                "This can overwrite previous sessions and is not suitable for "
                "real authentication scenarios."
            ),
            "recommendation": (
                "Use a random and unique token generation mechanism, such as "
                "the secrets module."
            ),
            "affected_quality_attributes": [
                "Security",
                "Reliability"
            ],
            "human_validation_required": True
        })

    return suggestions


def review_file(file_path: str) -> list[dict]:
    """
    Reads a source file and analyses it.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    code = path.read_text(encoding="utf-8")
    return review_code(code)


def save_suggestions(suggestions: list[dict], output_path: str) -> None:
    """
    Saves AI suggestions to a JSON file.
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        json.dumps(suggestions, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python app/ai_reviewer.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    suggestions = review_file(source_file)

    print("\nAI-assisted code review suggestions:\n")
    print(json.dumps(suggestions, indent=4, ensure_ascii=False))

    save_suggestions(suggestions, "data/ai_suggestions.json")

    print("\nSuggestions saved to data/ai_suggestions.json")


if __name__ == "__main__":
    main()