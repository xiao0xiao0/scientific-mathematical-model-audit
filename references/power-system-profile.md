# Power-system modeling profile

## Contents

- Pre-model questions
- Network and power-flow structures
- Dynamic and DAE structures
- Optimization and market structures
- Uncertainty and multi-timescale structures
- Sensitivity, stability, and identifiability
- Power-system red flags

## Pre-model questions

Determine before deriving equations:

- AC, DC, electromagnetic transient, electromechanical, quasi-steady, or data-driven regime;
- transmission, distribution, microgrid, integrated energy, device, market, or cyber-physical boundary;
- balanced/unbalanced phases and per-unit/base conventions;
- buses, branches, devices, areas, scenarios, and time indices;
- state, control, forecast, disturbance, contingency, and uncertain parameter roles;
- centralized, distributed, hierarchical, or market-clearing decision architecture;
- whether the claim concerns feasibility, economics, security, stability, resilience, estimation, or control.

## Network and power-flow structures

Use topology explicitly when interactions follow a network.

- Define oriented node-branch incidence `A`, branch parameters, admittance matrix `Y`, and ordering.
- Express conservation at nodes and constitutive laws on branches before writing compact matrices.
- For DC approximations, state angle, voltage-magnitude, resistance, and loss assumptions.
- For AC models, preserve real/reactive coupling and voltage/angle domains unless an approximation is justified.
- For distribution systems, state radial/meshed topology, phase balance, and chosen branch-flow or nodal formulation.

Typical compact structures include:

- branch differences `Aθ`;
- Laplacian-like coupling `L = AᵀBA`;
- complex nodal relation `i = Yv`;
- nonlinear injections `p + jq = diag(v)(Yv)*`;
- block real-imaginary or phase-coupled forms when solver compatibility requires them.

Do not replace independent bus indicators by a diagonal matrix and call it network modeling. Off-diagonal/topological coupling must have a defined physical role.

## Dynamic and DAE structures

Use a DAE when device/controller dynamics coexist with algebraic network constraints:

`ẋ = f(x,z,u,w;θ)`, `0 = g(x,z,u,w;θ)`, `y = h(x,z,u)`.

Require:

- dynamic states and algebraic variables separated;
- consistent initial conditions satisfying `g=0`;
- time constants and controller blocks traceable to devices or identified data;
- DAE index/regularity or at least a nonsingular algebraic Jacobian in the operating region;
- discretization method and step size justified for the time scale;
- equilibrium definition before linearization.

For local analysis, derive rather than assert:

`Δẋ = A_s Δx + B_s Δu + E_s Δw`, where the reduced Jacobian accounts for eliminated algebraic variables. State the operating point and conditions under which elimination is valid.

## Optimization and market structures

Write the complete problem:

`min_{x,u} J(x,u;θ)`

subject to power balance, network equations, operating limits, intertemporal constraints, reserve/security constraints, and variable domains.

Audit:

- whether every prose requirement appears mathematically;
- whether costs, penalties, and weights have units and economic meaning;
- whether slack variables are penalized strongly enough but not used to conceal infeasibility;
- whether binary/logical decisions are represented consistently;
- whether nonlinear/nonconvex physics are retained, approximated, relaxed, or linearized;
- whether relaxation exactness or optimality-gap evidence is supplied;
- whether decomposition follows genuine separability and coupling variables.

Use a Lagrangian or KKT system only when it enables marginal-price interpretation, sensitivity, equilibrium reformulation, bilevel reduction, or solution analysis. State constraint qualifications and whether KKT conditions are necessary, sufficient, or only local.

## Uncertainty and multi-timescale structures

Replace ad hoc safety coefficients with explicit uncertainty semantics:

- scenario model with scenario probabilities and nonanticipativity;
- chance constraint with violation probability and distributional assumptions;
- robust model with an interval/polyhedral/ellipsoidal uncertainty set;
- distributionally robust model with a defined ambiguity set and radius calibration;
- stochastic dynamics with process and observation noise distinguished.

For day-ahead, intraday, real-time, and control layers, define information arrival and coupling across time. Do not let a later-stage decision use future information.

When using Kronecker products or block matrices for time-area-device coupling, define each factor, ordering, and sparsity. The notation must reduce implementation ambiguity rather than conceal it.

## Sensitivity, stability, and identifiability

Use derivatives to answer a stated question:

- Jacobian for power-flow solvability, linearization, Newton steps, observability, or local sensitivity;
- Hessian for curvature, convexity, second-order optimality, or uncertainty propagation;
- eigenvalues/damping for small-signal stability;
- singular values/condition numbers for ill-conditioning and weak observability;
- adjoint or implicit differentiation for parameter influence and gradient-based design.

Check:

- rank of measurement or sensitivity matrices;
- reference angle/gauge freedoms and other non-identifiabilities;
- parameter collinearity and whether estimates are unique;
- observability/controllability for the selected state and input sets;
- stability only within the regime supported by the linearization or Lyapunov argument;
- nonsingularity assumptions used by implicit differentiation.

## Power-system red flags

- mixing physical power, normalized index values, costs, and probabilities in one additive objective without scaling semantics;
- using a resilience/reliability/security score as a causal physical state;
- assigning weights solely by expert preference and then claiming objective optimality;
- omitting reactive power or voltage constraints while claiming AC feasibility;
- using DC power flow without stating approximation limits;
- treating forecast errors at all buses/times as independent without evidence;
- adding an uncertainty coefficient while ignoring correlation, support, and time dependence;
- presenting a centralized formulation while claiming distributed implementation without messages, local subproblems, or convergence conditions;
- claiming global optimality from a local nonlinear solver;
- claiming stability from simulation alone without perturbation scope or analytical support;
- comparing only with an intentionally weak weighted-sum baseline.

For literature positioning, retrieve the closest same-problem formulations, not merely papers sharing keywords. Compare state choice, physical equations, uncertainty semantics, decision architecture, proof obligations, and computational evidence.
