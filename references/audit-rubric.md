# Mathematical model audit rubric

## Contents

- Fatal-flaw gate
- Scored dimensions
- Simplicity and complexity alarms
- Verdict rules

## Fatal-flaw gate

Any unresolved item below overrides the numerical score:

- the claimed output is not determined by the equations, constraints, or observations;
- symbols, indices, sets, units, or shapes are inconsistent in a way that changes meaning;
- a definition is circular or double-counts the same physical quantity;
- coefficients or weights determine the conclusion but have no source, calibration, or sensitivity analysis;
- an optimization problem has no decision variables, no feasible set, an unbounded objective, or inconsistent constraints;
- a dynamic model lacks initial/boundary conditions or mixes incompatible time scales without approximation;
- a stochastic or robust model has no random object, ambiguity set, distribution, support, or risk semantics;
- a derivative, Jacobian, Hessian, or KKT system is taken with respect to the wrong object or under unstated regularity;
- a causal conclusion is drawn from a descriptive weighted index without an identification strategy;
- a model is numerically solvable only because invalid constraints or physical laws were omitted.

Use `REBUILD` when the research question is plausible but the mathematical ontology is wrong. Use `NO-GO` when no available data, mechanism, or experiment can identify the claimed result.

## Scored dimensions

Score only after the fatal-flaw gate.

| Dimension | Weight | Full-credit evidence |
| --- | ---: | --- |
| Physical and logical closure | 20 | Boundary, mechanisms, assumptions, and conclusions form a traceable chain |
| Symbol, unit, index, and shape closure | 15 | Every object is defined and all operations are valid |
| Mechanistic depth | 15 | Coupling, dynamics, constraints, or uncertainty are included only where causally relevant |
| Identifiability and observability | 10 | Required states and parameters can be measured, estimated, bounded, or explicitly treated as latent |
| Well-posedness and solvability | 10 | Existence, feasibility, initialization, regularity, and solver implications are addressed |
| Verification and falsifiability | 15 | Symbolic/numeric checks, limits, perturbations, counterexamples, and data tests are specified |
| Literature and novelty position | 10 | Closest models are identified and the mathematical difference enables a new result |
| Reproducibility and presentation | 5 | Derivation, symbol table, code, parameter sources, and versions can be audited |

Do not award points for equation count, matrix size, nonlinear notation, or fashionable terminology.

## Simplicity alarm

Investigate rather than automatically reject when one or more conditions hold:

- the core relation is only `y = Σ w_i x_i` or an equivalent weighted score;
- coefficients appear only to tune importance and are neither derived nor estimated;
- all interactions are assumed additive despite network, temporal, saturation, threshold, or conservation effects;
- a static scalar represents a phenomenon whose state evolves over time;
- normalization choices can reverse the ranking or conclusion;
- the same aggregate is used as both cause and outcome;
- constraints are discussed in prose but absent from the mathematical model;
- uncertainty appears only as a safety coefficient rather than an explicit random, scenario, interval, or ambiguity model.

A weighted sum is acceptable as a transparent baseline, a proven separable model, a local linearization, or a calibrated utility function. Require evidence for one of those interpretations.

## Complexity alarm

Reject additions that exhibit complexity theater:

- converting a vector of indicators into a diagonal matrix without introducing coupling;
- writing `∇`, `J`, or `H` without a downstream sensitivity, Newton, convexity, or stability use;
- adding nonlinear powers or exponentials only to make a curve look sophisticated;
- introducing random variables without data, support, or a probability law;
- introducing dual variables without a meaningful constrained optimization problem;
- replacing a scalar equation with a neural network without an identification or generalization plan;
- adding graph, tensor, or Kronecker notation when topology or multi-index structure is unused;
- citing a method whose assumptions are violated by the available data.

## Verdict rules

| Verdict | Rule |
| --- | --- |
| `GO` | No fatal flaw, score at least 80, and decisive checks have been executed |
| `REVISE` | No fatal flaw, score 60–79, or a repair is local and testable |
| `REBUILD` | Fatal structural flaw or score below 60, but a defensible alternative model exists |
| `NO-GO` | Central claim is not identifiable, testable, or supported by available evidence |

State score uncertainty. A high score does not replace domain review or empirical validation.
