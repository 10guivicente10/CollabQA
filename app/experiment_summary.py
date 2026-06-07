import json
from pathlib import Path

import pandas as pd


EXPERIMENTS_DIR = Path("experiments")
REPORTS_DIR = Path("reports")

INPUT_FILES = [
    EXPERIMENTS_DIR / "human_alone_results.csv",
    EXPERIMENTS_DIR / "ai_alone_results.csv",
    EXPERIMENTS_DIR / "human_ai_results.csv"
]

OUTPUT_CSV = REPORTS_DIR / "experiment_comparison.csv"
OUTPUT_JSON = REPORTS_DIR / "experiment_comparison.json"


def load_experiment_results() -> pd.DataFrame:
    frames = []

    for file_path in INPUT_FILES:
        if file_path.exists():
            frames.append(pd.read_csv(file_path))

    if not frames:
        raise FileNotFoundError("No experiment result files were found.")

    df = pd.concat(frames, ignore_index=True)

    numeric_columns = [
        "relevant_problems_found",
        "false_positives",
        "useful_tests_suggested",
        "human_validated_decisions",
        "audit_log_entries"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="raise")

    return df


def calculate_best_mode(df: pd.DataFrame) -> dict:
    """
    Selects the best mode using a simple scoring strategy.

    Relevant problems found, useful tests, human decisions and audit entries
    increase the score. False positives reduce the score.
    """
    scored_df = df.copy()

    scored_df["score"] = (
        scored_df["relevant_problems_found"] * 3
        + scored_df["useful_tests_suggested"] * 2
        + scored_df["human_validated_decisions"] * 2
        + scored_df["audit_log_entries"] * 2
        - scored_df["false_positives"] * 2
    )

    best_row = scored_df.sort_values(by="score", ascending=False).iloc[0]

    return {
        "best_mode": best_row["mode"],
        "score": int(best_row["score"]),
        "reason": (
            "This mode achieved the best balance between relevant findings, "
            "useful test suggestions, human validation and traceability."
        )
    }


def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_experiment_results()
    best_mode = calculate_best_mode(df)

    df.to_csv(OUTPUT_CSV, index=False)

    output = {
        "results": df.to_dict(orient="records"),
        "best_mode": best_mode
    }

    OUTPUT_JSON.write_text(
        json.dumps(output, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\nExperiment comparison:\n")
    print(df.to_string(index=False))

    print("\nBest mode:")
    print(json.dumps(best_mode, indent=4, ensure_ascii=False))

    print("\nSaved reports:")
    print(f"- {OUTPUT_CSV}")
    print(f"- {OUTPUT_JSON}")


if __name__ == "__main__":
    main()