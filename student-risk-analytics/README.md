# Student Performance Analytics & Early-Warning System

A reproducible education-analytics prototype for identifying students who may require early academic intervention.

## What the project does

The workflow uses attendance, quiz performance, assignments, midterm scores, participation, and engagement indicators to estimate academic-risk probability.

It produces:
- student-level risk probabilities
- Low / Medium / High risk bands
- a ranked intervention list
- model accuracy and ROC-AUC
- Power BI-ready CSV outputs

## Model

A standardized logistic-regression classifier with balanced class weights is used to keep the model interpretable.

## Demonstration results

Using the included synthetic-data generator:

| Metric | Result |
|---|---:|
| Accuracy | ~84% |
| ROC-AUC | ~0.946 |
| Synthetic fail rate | ~21.5% |

> The dataset is synthetic and contains no real student or institutional information.

## Run

```bash
pip install -r requirements.txt
python student_risk_model.py
```

## Output files

The script creates an `outputs/` directory containing:
- `model_metrics.csv`
- `scored_students.csv`
- `at_risk_students.csv`
- `risk_band_summary.csv`
- `risk_distribution.png`

## Skills demonstrated

Python · Predictive Analytics · Logistic Regression · Education Analytics · Data Visualization · Power BI-ready Analytics
