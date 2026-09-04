# AI Mathematical Reasoning & Reward Validation Framework

A transparent, reproducible prototype for evaluating structured mathematical AI responses.

## What it demonstrates
- Benchmark construction across multiple mathematics domains
- Rule-based final-answer validation
- Reasoning-concept coverage checks
- Constraint checks
- Weighted reward computation
- Domain-level evaluation summaries

## Reward rubric
- Final answer correctness: 65%
- Required-concept coverage: 20%
- Constraint compliance: 10%
- Reasoning present: 5%

This is intentionally a transparent prototype rather than a claim of full formal proof verification. The included demonstration outputs contain six deliberately incorrect answers so the evaluation pipeline can be tested against known failures.

## Run
```bash
pip install -r requirements.txt
python evaluate.py
```

## Inputs
- `data/problems.csv`
- `data/model_outputs.csv`

## Outputs
- `outputs/evaluation_results.csv`
- `outputs/summary_by_domain.csv`
- `outputs/reward_breakdown.png` (generated when the script is run)

## Demonstration results

| Metric | Result |
|---|---:|
| Exact-answer accuracy | 80.0% |
| Mean composite reward | 0.870 |
| Benchmark size | 30 tasks |
| Domains | 5 |

## Extension ideas
Replace the rule-based concept checker with symbolic verification, theorem-prover checks, or an LLM-as-judge benchmark with human calibration.
