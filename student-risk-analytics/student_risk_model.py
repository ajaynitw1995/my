from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
FEATURES = [
    "attendance_pct", "quiz_avg", "assignment_avg",
    "midterm_score", "participation_score", "engagement_score"
]


def generate_synthetic_data(n=400, seed=17):
    rng = np.random.default_rng(seed)
    ability = rng.normal(0, 1, n)

    attendance = np.clip(78 + 8*ability + rng.normal(0, 8, n), 35, 100)
    quiz = np.clip(66 + 12*ability + rng.normal(0, 10, n), 0, 100)
    assignment = np.clip(70 + 10*ability + rng.normal(0, 10, n), 0, 100)
    midterm = np.clip(62 + 15*ability + rng.normal(0, 12, n), 0, 100)
    participation = np.clip(68 + 9*ability + rng.normal(0, 14, n), 0, 100)
    engagement = np.clip(72 + 9*ability + rng.normal(0, 12, n), 0, 100)

    composite = (
        0.10*attendance + 0.15*quiz + 0.20*assignment +
        0.30*midterm + 0.10*participation + 0.15*engagement
    )
    final_score = np.clip(composite - 8 + rng.normal(0, 7, n), 0, 100)

    df = pd.DataFrame({
        "student_id": [f"STU{i:03d}" for i in range(1, n+1)],
        "attendance_pct": attendance.round(1),
        "quiz_avg": quiz.round(1),
        "assignment_avg": assignment.round(1),
        "midterm_score": midterm.round(1),
        "participation_score": participation.round(1),
        "engagement_score": engagement.round(1),
        "final_score": final_score.round(1),
    })
    df["failed"] = (df["final_score"] < 50).astype(int)
    return df


def main():
    df = generate_synthetic_data()
    X, y = df[FEATURES], df["failed"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scale", StandardScaler()),
        ("logit", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]

    metrics = pd.DataFrame({
        "metric": ["accuracy", "roc_auc", "fail_rate"],
        "value": [accuracy_score(y_test, pred), roc_auc_score(y_test, prob), y.mean()],
    })

    model.fit(X, y)
    df["risk_probability"] = model.predict_proba(X)[:, 1]
    df["risk_band"] = pd.cut(
        df["risk_probability"],
        bins=[-0.01, 0.30, 0.60, 1.0],
        labels=["Low", "Medium", "High"],
    )

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)

    metrics.to_csv(out / "model_metrics.csv", index=False)
    df.sort_values("risk_probability", ascending=False).to_csv(
        out / "scored_students.csv", index=False
    )
    df[df["risk_probability"] >= 0.60].sort_values(
        "risk_probability", ascending=False
    ).to_csv(out / "at_risk_students.csv", index=False)

    summary = df.groupby("risk_band", observed=False).agg(
        students=("student_id", "count"),
        avg_attendance=("attendance_pct", "mean"),
        avg_midterm=("midterm_score", "mean"),
        avg_final=("final_score", "mean"),
    ).reset_index()
    summary.to_csv(out / "risk_band_summary.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.hist(df["risk_probability"], bins=20)
    plt.xlabel("Predicted risk probability")
    plt.ylabel("Students")
    plt.title("Distribution of Academic-Risk Probability")
    plt.tight_layout()
    plt.savefig(out / "risk_distribution.png", dpi=180)
    plt.close()

    print(metrics.round(3))
    print(summary.round(1))


if __name__ == "__main__":
    main()
