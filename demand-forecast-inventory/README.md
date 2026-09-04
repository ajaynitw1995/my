# Demand Forecasting & Inventory Optimization under Uncertainty

A reproducible decision-analytics project that turns seasonal demand forecasts into uncertainty-aware inventory recommendations.

## Objective
The project demonstrates how predictive analytics can be converted into an operational decision. It estimates future demand, measures forecast uncertainty, calculates service-level safety stock, and produces monthly order-up-to targets.

## Workflow
1. Fit a trend + seasonal regression model.
2. Evaluate performance on a 12-month holdout period.
3. Estimate forecast-error uncertainty.
4. Convert a 95% service-level target into safety stock.
5. Generate a 12-month inventory plan.

## Demonstration results

| Metric | Result |
|---|---:|
| 12-month holdout MAE | 4.85 units |
| Residual standard deviation | 6.34 units |
| Target service level | 95% |
| Safety stock | 10.4 units |

The included dataset is synthetic and is used only to demonstrate the workflow.

## Run
```bash
pip install -r requirements.txt
python forecast_inventory.py
```

## Files
- `forecast_inventory.py` — forecasting and inventory decision pipeline
- `data/monthly_demand.csv` — synthetic monthly demand data
- `outputs/model_metrics.csv` — holdout metrics
- `outputs/inventory_plan.csv` — 12-month forecast and recommended order-up-to levels

Running the script also generates `outputs/forecast_plot.png` locally.

## Skills demonstrated
Forecasting · Inventory Optimization · Operations Research · Decision Science · Python · Predictive Analytics
