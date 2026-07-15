# Model-family selection

## Contents

- Selection rule
- Canonical families
- Three-level deepening
- Misuse checks

## Selection rule

Choose a mathematical family from the phenomenon, claim, data, and intervention—not from a desire for harder-looking equations. Multiple families may be composed only when their state and parameter semantics are compatible.

## Canonical families

| Missing mechanism or research need | Candidate structure | Canonical form | Required evidence |
| --- | --- | --- | --- |
| Topological interaction or flow | Graph/network model | `y = h(A, x, u; θ)`, `L = AᵀWA` | Nodes, edges, direction, conservation, topology source |
| Time evolution, inertia, delay | ODE/state space | `ẋ = f(x,u,w,t)`, `y = h(x,u)` | State definition, time scale, initial condition, parameter identification |
| Fast algebraic and slow dynamic coupling | DAE | `Mẋ = F(x,z,u)`, `0 = g(x,z,u)` | Index/regularity, consistent initialization, algebraic feasibility |
| Distributed spatial field | PDE/continuum | `∂x/∂t = F(x,∇x,∇²x,u)` | Spatial domain, boundary conditions, constitutive laws, discretization |
| Decision under constraints | Mathematical optimization | `min J(x,u)` s.t. `g=0`, `h≤0`, domains | Decision variables, feasible set, objective provenance, solver class |
| Marginal value or optimality structure | Lagrangian/KKT | `∇L=0`, primal/dual feasibility, complementarity | Differentiability, constraint qualification, convexity or local interpretation |
| Parameter/state estimation | Observation/state-space model | `xₖ₊₁=f(xₖ,uₖ,wₖ)`, `yₖ=h(xₖ,vₖ)` | Noise semantics, observability, prior/initial covariance, validation data |
| Random variability with known/estimated law | Stochastic model | `ξ~P`, `E[J]`, `Pr(g≤0)≥1-ε` | Distribution/support, sample adequacy, calibration, risk meaning |
| Distributional ambiguity or adversarial variation | Robust/DRO model | `min_x sup_{P∈𝒫} E_P[J]` | Ambiguity/uncertainty set, radius calibration, conservatism analysis |
| Multi-stage decisions | Dynamic/stochastic programming | Bellman or scenario-tree recursion | Information pattern, nonanticipativity, horizon, terminal value |
| Hierarchical or coupled actors | Bilevel/game model | leader-follower or equilibrium conditions | Actor objectives, information, equilibrium existence/selection |
| Local response and influence | Sensitivity/implicit differentiation | `dx*/dθ = -F_x^{-1}F_θ` | Nonsingularity, differentiability, perturbation regime |
| Interactions beyond additivity | Nonlinear/interaction model | cross terms, kernels, saturation, threshold laws | Mechanism or data evidence; identifiability and overfit control |
| Equation discovery from data | Sparse/symbolic regression | search over operator library with complexity penalty | Data quality, train/test separation, dimensional/physical priors, rediscovery tests |

## Three-level deepening

For a weak model such as `r = αa + βb + γc`, do not jump directly to an advanced form.

### Level 0: minimal correct baseline

- define variables, units, normalization, weight origin, and intended interpretation;
- quantify coefficient sensitivity and collinearity;
- state whether the score is descriptive, predictive, causal, or a utility function;
- retain it as a baseline even if a stronger model is selected.

### Level 1: structurally strengthened model

Add the single most important missing structure. Examples:

- interaction: `r = wᵀx + xᵀQx` when pairwise effects are defensible;
- network coupling: `r = wᵀx + ρ xᵀLx` when neighboring entities interact;
- dynamics: `xₖ₊₁ = Axₖ + Buₖ + Ewₖ` when memory or control matters;
- constraints: embed the score in a feasible decision model rather than treating it as reality;
- uncertainty: replace a safety multiplier with explicit scenarios, intervals, or chance constraints.

### Level 2: publication-grade advanced model

Compose only justified structures—for example a graph-coupled DAE with constrained stochastic control—and derive the computational form, identifiability conditions, and comparison experiment. Complexity must enable a claim unavailable to Levels 0 and 1.

## Misuse checks

- A matrix is meaningful only if rows, columns, ordering, sparsity, and operations are defined.
- A derivative is meaningful only if the independent variable, held-fixed quantities, domain, and regularity are defined.
- A Hessian does not establish convexity without its domain and definiteness conditions.
- KKT conditions are not automatically sufficient; distinguish necessary from sufficient conditions.
- A nonlinear term is not a mechanism merely because it fits data better.
- A stochastic model is not robust unless uncertainty semantics and calibration are explicit.
- A symbolic-regression equation is a candidate hypothesis, not a governing law, until tested out of sample and against physical limits.
