# Parameter-Uniform Solver Toolkit for Singularly Perturbed Problems

This project solves the singularly perturbed reaction-diffusion boundary-value problem

`-eps^2 u''(x) + u(x) = 1,  0 < x < 1`

with

`u(0) = u(1) = 0`.

For small `eps`, the solution contains boundary layers near both endpoints.

## What the project demonstrates

- construction of a Shishkin fitted mesh
- nonuniform finite-difference discretization
- stable exact solution for verification
- multi-epsilon convergence experiments
- parameter-uniform error envelopes
- scientific visualization of the layer solution

## Numerical experiment

The script tests perturbation parameters from `1e-1` down to `1e-4` over mesh sizes `N = 32, 64, 128, 256`.

The parameter-uniform maximum nodal error decreases from about `1.07e-2` at `N=32` to about `4.59e-4` at `N=256` in the demonstration experiment.

## Run

```bash
pip install -r requirements.txt
python spp_solver.py
```

## Output files

The script creates an `outputs/` directory containing:
- `convergence.csv`
- `parameter_uniform_error.csv`
- `spp_solution.png`
- `uniform_error.png`

## Skills demonstrated

Numerical Analysis · Singular Perturbation · Scientific Computing · Finite Difference Methods · Python · Applied Mathematics
