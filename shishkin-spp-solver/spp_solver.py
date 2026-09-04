from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent


def exact_solution(x, eps):
    x = np.asarray(x)
    ratio = (np.exp(-x/eps) + np.exp(-(1-x)/eps)) / (1 + np.exp(-1/eps))
    return 1 - ratio


def shishkin_mesh(N, eps, sigma=2.0):
    if N % 4 != 0:
        raise ValueError("N must be divisible by 4.")
    tau = min(0.25, sigma * eps * np.log(N))
    n1, n2, n3 = N // 4, N // 2, N // 4
    left = np.linspace(0, tau, n1 + 1)
    middle = np.linspace(tau, 1 - tau, n2 + 1)[1:]
    right = np.linspace(1 - tau, 1, n3 + 1)[1:]
    return np.concatenate([left, middle, right])


def solve_spp(N, eps):
    x = shishkin_mesh(N, eps)
    n = len(x)
    A = np.zeros((n - 2, n - 2))
    rhs = np.ones(n - 2)

    for j, i in enumerate(range(1, n - 1)):
        hL = x[i] - x[i - 1]
        hR = x[i + 1] - x[i]

        cL = -eps**2 * 2.0 / (hL * (hL + hR))
        cR = -eps**2 * 2.0 / (hR * (hL + hR))
        cC = 1.0 - cL - cR

        if j - 1 >= 0:
            A[j, j - 1] = cL
        A[j, j] = cC
        if j + 1 < n - 2:
            A[j, j + 1] = cR

    interior = np.linalg.solve(A, rhs)
    u = np.zeros(n)
    u[1:-1] = interior
    return x, u


def max_error(N, eps):
    x, u = solve_spp(N, eps)
    return float(np.max(np.abs(u - exact_solution(x, eps))))


def main():
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)

    eps_values = [1e-1, 1e-2, 1e-3, 1e-4]
    N_values = [32, 64, 128, 256]

    rows = []
    for eps in eps_values:
        previous = None
        for N in N_values:
            err = max_error(N, eps)
            order = np.nan if previous is None else np.log(previous / err) / np.log(2)
            rows.append({
                "epsilon": eps,
                "N": N,
                "max_error": err,
                "observed_order": order,
            })
            previous = err

    convergence = pd.DataFrame(rows)
    convergence.to_csv(out / "convergence.csv", index=False)

    eps = 1e-3
    N = 128
    x, u = solve_spp(N, eps)
    dense = np.linspace(0, 1, 2000)

    plt.figure(figsize=(9, 5))
    plt.plot(dense, exact_solution(dense, eps), label="Exact")
    plt.plot(x, u, marker=".", linestyle="none", label="Shishkin FD")
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.title(f"Singularly Perturbed Reaction-Diffusion Solution (eps={eps:g}, N={N})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "spp_solution.png", dpi=180)
    plt.close()

    worst = convergence.groupby("N")["max_error"].max().reset_index()
    worst.to_csv(out / "parameter_uniform_error.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.loglog(worst["N"], worst["max_error"], marker="o")
    plt.xlabel("N")
    plt.ylabel("max over epsilon of nodal error")
    plt.title("Parameter-Uniform Error Trend")
    plt.tight_layout()
    plt.savefig(out / "uniform_error.png", dpi=180)
    plt.close()

    print(convergence.to_string(index=False))
    print("\nParameter-uniform envelope:")
    print(worst.to_string(index=False))


if __name__ == "__main__":
    main()
