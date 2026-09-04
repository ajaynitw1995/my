from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent

def canonical(s):
    return re.sub(r"\s+", "", str(s).strip().lower())

def numeric(s):
    try:
        return float(str(s).strip())
    except Exception:
        return None

def answer_correct(got, expected, tol=1e-6):
    g, e = numeric(got), numeric(expected)
    if g is not None and e is not None:
        return abs(g-e) <= tol * max(1.0, abs(e))
    if "," in str(expected):
        return sorted(canonical(got).split(",")) == sorted(canonical(expected).split(","))
    return canonical(got) == canonical(expected)

def score_row(row):
    final_correct = float(answer_correct(row["answer"], row["expected_answer"]))
    concept = canonical(row["required_concept"])
    reasoning = canonical(row["reasoning"])
    concept_coverage = float(all(tok in reasoning for tok in concept.split() if tok))

    raw_constraint = row.get("constraint", "")
    constraint = "" if pd.isna(raw_constraint) else str(raw_constraint).strip()
    constraint_ok = 1.0 if not constraint else float(canonical(constraint) in reasoning)
    nonempty_reasoning = float(len(str(row["reasoning"]).strip()) >= 15)

    reward = (
        0.65 * final_correct +
        0.20 * concept_coverage +
        0.10 * constraint_ok +
        0.05 * nonempty_reasoning
    )
    return pd.Series({
        "final_correct": final_correct,
        "concept_coverage": concept_coverage,
        "constraint_ok": constraint_ok,
        "reasoning_present": nonempty_reasoning,
        "reward": reward,
    })

def main():
    problems = pd.read_csv(ROOT/"data"/"problems.csv")
    outputs = pd.read_csv(ROOT/"data"/"model_outputs.csv")
    df = problems.merge(outputs, on="problem_id", how="left")
    scores = df.apply(score_row, axis=1)
    result = pd.concat([df, scores], axis=1)

    out = ROOT/"outputs"
    out.mkdir(exist_ok=True)
    result.to_csv(out/"evaluation_results.csv", index=False)

    summary = result.groupby("domain")[["final_correct","concept_coverage","reward"]].mean()
    summary.loc["OVERALL"] = result[["final_correct","concept_coverage","reward"]].mean()
    summary.to_csv(out/"summary_by_domain.csv")

    plt.figure(figsize=(8,5))
    result.groupby("domain")["reward"].mean().sort_values().plot(kind="bar")
    plt.ylabel("Mean reward")
    plt.title("AI Math Evaluation Reward by Domain")
    plt.tight_layout()
    plt.savefig(out/"reward_breakdown.png", dpi=180)
    plt.close()

    print(summary.round(3))
    print(f"\nOverall exact-answer accuracy: {result['final_correct'].mean():.1%}")
    print(f"Overall mean reward: {result['reward'].mean():.3f}")

if __name__ == "__main__":
    main()
