import json
from pathlib import Path

import pandas as pd
import streamlit as st

from ai_reviewer import review_file, save_suggestions
from audit_logger import append_audit_log
from metrics import calculate_metrics
from test_generator import suggest_tests


AUTH_FILE = "sample_project/auth.py"

AI_SUGGESTIONS_PATH = Path("data/ai_suggestions.json")
DECISIONS_PATH = Path("data/decisions.json")
TEST_SUGGESTIONS_PATH = Path("data/test_suggestions.json")
AUDIT_LOG_PATH = Path("data/audit_log.csv")


def load_json(path: Path):
    if not path.exists():
        return []

    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )


def show_code():
    code = Path(AUTH_FILE).read_text(encoding="utf-8")
    st.code(code, language="python")


st.set_page_config(
    page_title="CollabQA",
    page_icon="🧪",
    layout="wide"
)

st.title("CollabQA")
st.subheader("Human–AI Collaboration in Software Quality for Authentication Modules")

st.write(
    "This prototype demonstrates how AI suggestions can support software quality "
    "activities while keeping human validation, traceability and accountability."
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Code Review",
    "2. Human Decisions",
    "3. Test Suggestions",
    "4. Metrics",
    "5. Audit Log"
])


with tab1:
    st.header("AI-assisted Code Review")

    st.write("Authentication module under analysis:")

    with st.expander("Show source code"):
        show_code()

    if st.button("Run AI-assisted review"):
        suggestions = review_file(AUTH_FILE)
        save_suggestions(suggestions, str(AI_SUGGESTIONS_PATH))
        st.success("AI-assisted review completed.")
        st.session_state["suggestions"] = suggestions

    suggestions = st.session_state.get(
        "suggestions",
        load_json(AI_SUGGESTIONS_PATH)
    )

    if suggestions:
        st.subheader("AI Suggestions")

        for suggestion in suggestions:
            risk = suggestion["risk"]

            if risk == "High":
                st.error(f"{suggestion['id']} — {suggestion['title']}")
            elif risk == "Medium":
                st.warning(f"{suggestion['id']} — {suggestion['title']}")
            else:
                st.info(f"{suggestion['id']} — {suggestion['title']}")

            st.write(f"**Category:** {suggestion['category']}")
            st.write(f"**Risk:** {suggestion['risk']}")
            st.write(f"**Description:** {suggestion['description']}")
            st.write(f"**Recommendation:** {suggestion['recommendation']}")
            st.write("---")
    else:
        st.info("No AI suggestions found yet. Run the AI-assisted review first.")


with tab2:
    st.header("Human Decision Layer")

    suggestions = load_json(AI_SUGGESTIONS_PATH)

    if not suggestions:
        st.warning("Run the AI-assisted review before registering decisions.")
    else:
        responsible = st.text_input("Responsible reviewer", value="Guilherme Vicente")

        decisions = []

        for suggestion in suggestions:
            st.subheader(f"{suggestion['id']} — {suggestion['title']}")
            st.write(f"**Risk:** {suggestion['risk']}")
            st.write(suggestion["description"])

            decision = st.selectbox(
                "Human decision",
                [
                    "Accepted",
                    "Rejected",
                    "Partially accepted",
                    "Needs human review"
                ],
                key=f"decision_{suggestion['id']}"
            )

            justification = st.text_area(
                "Justification",
                key=f"justification_{suggestion['id']}",
                placeholder="Explain why this suggestion was accepted, rejected or requires review."
            )

            decisions.append({
                "suggestion_id": suggestion["id"],
                "category": suggestion["category"],
                "risk": suggestion["risk"],
                "title": suggestion["title"],
                "human_decision": decision,
                "justification": justification,
                "responsible": responsible,
                "human_validation_required": suggestion["human_validation_required"]
            })

            st.write("---")

        if st.button("Save human decisions"):
            missing_justification = any(
                not decision["justification"].strip()
                for decision in decisions
            )

            if missing_justification:
                st.error("All decisions require a justification.")
            elif not responsible.strip():
                st.error("Responsible reviewer is required.")
            else:
                save_json(DECISIONS_PATH, decisions)

                for decision in decisions:
                    append_audit_log(decision)

                st.success("Human decisions saved and audit log updated.")


with tab3:
    st.header("AI-assisted Test Suggestions")

    decisions = load_json(DECISIONS_PATH)

    if not decisions:
        st.warning("Save human decisions before generating test suggestions.")
    else:
        code = Path(AUTH_FILE).read_text(encoding="utf-8")

        if st.button("Generate test suggestions"):
            test_suggestions = suggest_tests(code, decisions)
            save_json(TEST_SUGGESTIONS_PATH, test_suggestions)
            st.success("Test suggestions generated.")

        test_suggestions = load_json(TEST_SUGGESTIONS_PATH)

        if test_suggestions:
            for test in test_suggestions:
                st.subheader(f"{test['id']} — {test['title']}")
                st.write(f"**Related suggestion:** {test['related_suggestion']}")
                st.write(f"**Priority:** {test['priority']}")
                st.write(f"**Purpose:** {test['purpose']}")
                st.write(f"**Risk addressed:** {test['risk_addressed']}")
                st.code(test["test_code"], language="python")
                st.write("---")
        else:
            st.info("No test suggestions generated yet.")


with tab4:
    st.header("Evaluation Metrics")

    if st.button("Calculate metrics"):
        metrics = calculate_metrics()
        save_json(Path("reports/final_summary.json"), metrics)

        df = pd.DataFrame(
            list(metrics.items()),
            columns=["Metric", "Value"]
        )

        st.dataframe(df, use_container_width=True)

    summary = load_json(Path("reports/final_summary.json"))

    if summary:
        st.subheader("Latest metrics summary")

        df = pd.DataFrame(
            list(summary.items()),
            columns=["Metric", "Value"]
        )

        st.dataframe(df, use_container_width=True)

        st.write("Key result:")
        st.success(
            "The human-validated AI suggestion led to a new test that first failed, "
            "confirmed the expired-session defect, and then passed after the fix."
        )


with tab5:
    st.header("Audit Log")

    if AUDIT_LOG_PATH.exists() and AUDIT_LOG_PATH.stat().st_size > 0:
        df = pd.read_csv(AUDIT_LOG_PATH)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No audit log entries found yet.")