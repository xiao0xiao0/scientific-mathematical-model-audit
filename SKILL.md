---
name: scientific-mathematical-model-audit
description: Audit, repair, deepen, and verify scientific mathematical models, equation chains, objectives, constraints, and derivations before writing or publication. Use when Codex must critique shallow AI-generated formulas or arbitrary weighted sums; close inconsistent variables, units, shapes, assumptions, and logic; choose justified matrix, graph, differential, optimization, stochastic, robust, sensitivity, or state-space structures; verify derivatives, Jacobians, Hessians, KKT systems, stability, identifiability, and limiting cases; compare a model with literature and baselines; or prepare a validated model package for power-system papers, patents, reports, MATLAB, SymPy, LaTeX, MathType, or Word.
---

# Scientific Mathematical Model Audit

Treat mathematical sophistication as explanatory and inferential power, not symbol count. Preserve a simple model when it is the correct model. Reject decorative matrices, derivatives, random variables, and optimization notation that add no mechanism, identifiable quantity, testable prediction, or computational value.

On Windows, read this Skill and its bundled files explicitly as UTF-8. If formulas or connecting characters appear garbled, reread with UTF-8 before reasoning; never copy or interpret mojibake.

## Establish the task once

Inspect the supplied idea, equations, draft, code, data description, and target venue before asking questions. Infer context when evidence is clear. Ask once only for unresolved choices that materially change the model:

- domain and phenomenon;
- purpose: explanation, prediction, estimation, control, optimization, decision, or mechanism discovery;
- system boundary, spatial and temporal scale, and static/dynamic/stochastic character;
- available observations, parameters, experiments, literature, and computational tools;
- desired output level and publication, patent, report, or software constraints.

For a power-system artifact, use the power-system profile by default. For an underspecified task, produce a conditional audit rather than inventing measurements or physics.

When observations or parameters needed by a stronger model do not exist, present Levels 1 and 2 as conditional research designs with explicit data requirements. Do not claim that an uncalibrated advanced model is valid merely because it is plausible.

## Enforce the modeling contract

- Define every set, index, variable, parameter, state, control, disturbance, observation, unit, domain, and matrix dimension before use.
- Separate measured data, estimated latent states, decision variables, fixed parameters, and uncertain quantities.
- Derive coefficients from physics, calibration, estimation, normalization, or a cited convention. Flag arbitrary weights.
- Connect every equation to an assumption or governing principle and to at least one verification route.
- State initial, boundary, feasibility, regularity, probability, and identifiability conditions when applicable.
- Keep a minimal baseline. Demonstrate what each strengthened term changes relative to that baseline.
- Never infer that a model is valid merely because symbolic software simplifies it or numerical software returns a solution.

Read [audit-rubric.md](references/audit-rubric.md) before issuing a model-quality judgment.

## Run the audit and deepening workflow

### 1. Reconstruct the model card

Write a compact model card containing:

- research question and claimed conclusion;
- system boundary and time/space resolution;
- entities and interaction topology;
- state, control, disturbance, parameter, and output vectors;
- assumptions and data provenance;
- governing laws, empirical relations, and target quantities;
- intended solver and validation evidence.

Do not repair formulas until the model card exposes what the formulas are supposed to represent.

### 2. Stop on fatal flaws

Identify fatal flaws before deepening: undefined or circular quantities, incompatible units or shapes, double counting, causal claims from association alone, an objective without decision variables, unconstrained or infeasible variables, dynamics without initial conditions, stochastic notation without a probability model, derivatives without independent variables or regularity, or a model whose claimed output is not identifiable from available observations.

When a fatal flaw exists, give a precise repair requirement. Do not hide it under more advanced notation.

### 3. Trigger the simplicity alarm

Flag a model for structural review when it is only a sum of elements, a coefficient-scaled indicator, a normalization followed by arbitrary weighting, or a single static mapping despite a clearly networked, dynamic, constrained, uncertain, or strategic phenomenon.

Do not automatically make it nonlinear. First decide which missing mechanism matters. Read [model-families.md](references/model-families.md) and select only justified structures.

### 4. Produce three model levels

Provide all three unless the user requests only an audit:

1. **Minimal correct model** — simplest closed and testable baseline.
2. **Structurally strengthened model** — adds the most important missing mechanism.
3. **Publication-grade advanced model** — adds only defensible coupling, dynamics, uncertainty, constraints, hierarchy, or sensitivity needed for the research claim.

For every added structure, state:

- the mechanism it represents;
- the assumption it introduces;
- the new data or parameter it requires;
- whether it is identifiable;
- the computational burden and solver implications;
- the observable prediction or conclusion it enables;
- how it will be falsified or compared with the baseline.

If the available data cannot support a level, stop at the last identifiable level and label the unsupported level `design proposal`, not `recommended model`.

### 5. Derive, do not jump

Present the logic chain in order:

`phenomenon → assumptions → primitive relations → local equations → aggregation/coupling → compact vector or matrix form → objective and constraints → derivative/KKT/sensitivity form → computable form → validation claim`

Show intermediate steps whenever a sign, normalization, aggregation, linearization, relaxation, or probabilistic transformation changes meaning. Label approximations and state their valid regimes.

For power-system work, read [power-system-profile.md](references/power-system-profile.md) before selecting network, dynamic, OPF, uncertainty, stability, or observability structures.

### 6. Verify independently

Read [verification-protocol.md](references/verification-protocol.md). Run checks proportional to the claim:

- symbol, set, index, unit, and shape closure;
- algebraic equivalence and derivative checks;
- Jacobian, Hessian, rank, definiteness, convexity, stability, observability, or controllability where relevant;
- KKT sign and complementarity checks for optimization;
- initial/boundary conditions and limiting or degenerate cases;
- numerical smoke tests, perturbation tests, counterexamples, and baseline comparison;
- sensitivity to arbitrary coefficients and normalization choices.

Prefer MATLAB when the project already uses MATLAB. Use SymPy when an approved environment already provides it. Do not silently install packages. Do not parse untrusted mathematical strings with `eval` or unsafe symbolic parsers.

### 7. Ground novelty in literature

For power-system research, use available PowerLit literature retrieval before claiming novelty or selecting a fashionable mathematical structure. Otherwise browse primary papers and official technical documentation. Identify the closest model family, what is inherited, what is changed, and what new conclusion becomes possible. Never cite a method merely to decorate a formula.

Honor an explicit no-browse or local-only constraint. In that case, use only supplied or verified local sources, record literature and novelty checks as `unexecuted`, and do not issue an unconditional novelty or `GO` claim.

### 8. Validate the structural record

Treat a task as substantial when its model supports a paper, patent, project decision, or claimed contribution; contains dynamics, constraints, uncertainty, optimization, or three or more linked equations; or will be handed to code or a solver. Create a model specification using [model-spec-schema.md](references/model-spec-schema.md) and run:

```text
python scripts/audit_model_spec.py model-spec.json --strict
```

Treat the script as a structural completeness gate only. It cannot establish physical truth, novelty, or empirical validity.

If the user requests only a named deliverable, keep the model specification as an internal validation artifact and do not add it to the delivered files unless requested.

## Return an auditable result

Use this order:

1. **Verdict:** GO, REVISE, REBUILD, or NO-GO, with fatal flaws first.
2. **Model card:** boundary, roles, assumptions, data, and claim.
3. **Logic-chain audit:** where the current derivation holds or breaks.
4. **Three model levels:** formulas plus the meaning and cost of every addition.
5. **Variable and dimension table:** role, shape, unit, source, observability.
6. **Verification evidence:** symbolic, numerical, limiting-case, and counterexample results.
7. **Literature position:** closest baselines and defensible novelty.
8. **Recommended model:** exact reason for choosing one level.
9. **Handoff package:** numbered derivation, MATLAB/SymPy verification code, and MathType-ready TeX only after the model passes.

Distinguish facts, assumptions, derivations, numerical evidence, and speculative extensions. Report unexecuted checks explicitly.

Use precise pass labels:

- `structural pass`: schema closure and no unresolved strict structural warnings;
- `mathematical pass`: claim-relevant symbolic and numerical checks executed successfully;
- `scientific pass`: physical assumptions, empirical evidence, and literature position support the intended claim.

Call a model simply `passed` only when all claim-relevant gates pass. Otherwise report the highest achieved gate and remaining conditions.

## Coordinate with other skills

- Use PowerLit literature intelligence for closest-competitor and citation evidence when available.
- Use a power-system prewriting or paper-review skill for venue-level acceptance risk after the mathematical audit.
- Use the Word MathType skill only after the equation chain is approved; formatting must not precede model correctness.
- Read [tooling-provenance.md](references/tooling-provenance.md) before importing third-party skill instructions or installing mathematical packages.
