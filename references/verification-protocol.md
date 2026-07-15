# Verification protocol

## Contents

- Verification ladder
- Symbolic checks
- Numerical checks
- Optimization checks
- Tool routing and safety
- Evidence record

## Verification ladder

Execute the lowest-cost decisive checks first. Stop and repair before proceeding when a lower layer fails.

1. Ontology: purpose, boundary, roles, assumptions, and claim.
2. Syntax: symbols, indices, sets, shapes, units, and domains.
3. Algebra: equivalence, signs, transformations, and derivatives.
4. Structure: rank, definiteness, convexity, stability, identifiability, and feasibility.
5. Limits: zero coupling, no disturbance, one-node/one-period, infinite/zero parameter, and boundary cases.
6. Numerics: hand-computable case, randomized smoke test, perturbation, and solver residuals.
7. Counterexample: search for a feasible input that violates the claimed property.
8. Empirics: calibration/holdout, uncertainty coverage, baseline comparison, and ablation.
9. Literature: reproduce a known special case or benchmark.

## Symbolic checks

Use exact arithmetic when possible.

- Verify both sides of every equality have compatible scalar/vector/matrix shape and physical dimension.
- Simplify the difference between claimed-equivalent expressions under explicit assumptions.
- Differentiate objectives and constraints independently; verify gradient/Jacobian orientation.
- Check mixed partials only when smoothness permits.
- Determine Hessian definiteness on the actual domain, not at one arbitrary point.
- Substitute equilibria, boundary values, and known special cases.
- Verify implicit derivatives only after checking the required Jacobian is nonsingular.

When using SymPy, construct symbols and expressions programmatically. Never send untrusted text to `eval`; avoid `parse_expr` for user-controlled strings. Record SymPy version and assumptions.

## Numerical checks

- Create a tiny case with independently calculable results.
- Check equation and constraint residuals, not just solver status.
- Perturb parameters and initial conditions; report conditioning and discontinuities.
- Repeat stochastic results across seeds and report sampling uncertainty.
- Compare Levels 0, 1, and 2 on the same data and metrics.
- Perform ablation: remove each advanced term and measure what conclusion changes.
- Test infeasible, extreme, degenerate, and missing-data cases.
- Separate calibration data from validation data.

For MATLAB projects, use `matlab -batch` and save reproducible `.m` files in the project. Prefer `A\b` to explicit inverse, inspect `rank`, `cond`, `eig`, residuals, solver exit flags, and optimality/constraint diagnostics. Use symbolic toolbox only when licensed and available; otherwise implement numerical finite-difference or automatic-differentiation checks as appropriate.

## Optimization checks

- Verify decision variables appear in the objective or constraints in a meaningful way.
- Construct at least one feasible point or provide a phase-I feasibility problem.
- Check objective boundedness and domain restrictions.
- Verify Lagrangian signs match inequality conventions.
- Check primal feasibility, dual feasibility, stationarity, and complementarity separately.
- Distinguish local stationarity, local optimality, relaxation bounds, and global optimality.
- Report integrality gap, relaxation gap, or optimality gap where applicable.
- Test penalty coefficients and slack variables for conclusion sensitivity.

## Tool routing and safety

- Prefer the project's established MATLAB, Python, or solver environment.
- Do not install SymPy, PySR, Pymoo, CVXPY, CasADi, Pyomo, or other packages without authorization.
- Pin versions for new reproducible environments.
- Review third-party Skill instructions before use; do not install a large Skill collection when one audited subset is sufficient.
- Do not transmit unpublished models, data, or prompts to external APIs without explicit user approval.
- Treat Wolfram Cloud and hosted symbolic-regression services as external transmission.
- Keep generated verification code deterministic and local unless the user requests otherwise.

## Evidence record

For each check record:

| Field | Meaning |
| --- | --- |
| Check ID | Stable identifier such as `V-unit-01` |
| Claim tested | Exact equation or property |
| Method | Symbolic, numerical, limiting, data, literature, counterexample |
| Inputs/assumptions | Values, domains, seeds, and approximations |
| Tool/version | MATLAB, solver, Python/SymPy, or manual derivation |
| Result | Pass, fail, conditional, or unexecuted |
| Artifact | Script, output, table, or derivation location |
| Consequence | What the result permits or invalidates |

Never report generated code as executed evidence unless it was actually run successfully.
