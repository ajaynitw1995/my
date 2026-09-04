from pathlib import Path
from statistics import NormalDist
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

ROOT = Path(__file__).resolve().parent


def make_features(t):
    t = np.asarray(t)
    return np.column_stack([
        t,
        np.sin(2*np.pi*t/12),
        np.cos(2*np.pi*t/12),
        np.sin(2*np.pi*t/6),
        np.cos(2*np.pi*t/6),
    ])


def main():
    df = pd.read_csv(ROOT / "data" / "monthly_demand.csv", parse_dates=["month"])
    n = len(df)
    train_n = n - 12

    X = make_features(np.arange(n))
    model = LinearRegression().fit(X[:train_n], df["demand"].iloc[:train_n])

    fitted = model.predict(X[:train_n])
    residual_sd = float(np.std(df["demand"].iloc[:train_n] - fitted, ddof=1))

    future_t = np.arange(n, n + 12)
    future_dates = pd.date_range(
        df["month"].max() + pd.offsets.MonthBegin(1), periods=12, freq="MS"
    )
    forecast = model.predict(make_features(future_t))

    service_level = 0.95
    z = NormalDist().inv_cdf(service_level)
    safety_stock = z * residual_sd
    order_up_to = np.ceil(forecast + safety_stock).astype(int)

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)

    plan = pd.DataFrame({
        "month": future_dates,
        "forecast_demand": np.round(forecast, 1),
        "forecast_error_sd": round(residual_sd, 2),
        "service_level": service_level,
        "safety_stock": round(safety_stock, 1),
        "recommended_order_up_to": order_up_to,
    })
    plan.to_csv(out / "inventory_plan.csv", index=False)

    holdout_pred = model.predict(X[train_n:])
    mae = np.mean(np.abs(df["demand"].iloc[train_n:].to_numpy() - holdout_pred))
    metrics = pd.DataFrame({
        "metric": ["holdout_MAE", "residual_SD", "service_level"],
        "value": [mae, residual_sd, service_level],
    })
    metrics.to_csv(out / "model_metrics.csv", index=False)

    plt.figure(figsize=(9, 5))
    plt.plot(df["month"], df["demand"], label="Historical demand")
    plt.plot(future_dates, forecast, marker="o", label="Forecast")
    plt.axvline(df["month"].max(), linestyle="--")
    plt.ylabel("Demand units")
    plt.title("Demand Forecast and 12-Month Outlook")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "forecast_plot.png", dpi=180)
    plt.close()

    print(metrics.round(3))
    print("\nInventory plan:")
    print(plan.head())


if __name__ == "__main__":
    main()
