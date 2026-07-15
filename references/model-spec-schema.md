# Model specification schema

## Contents

- Purpose
- Required structure
- Example
- Validator behavior

## Purpose

Use this JSON record for substantial models. It creates traceability between assumptions, symbols, equations, verification, and literature baselines. It does not replace the mathematical derivation.

## Required structure

```text
model_id             stable model identifier
domain               scientific domain
purpose              explanation|prediction|estimation|control|optimization|decision|discovery
claim                exact conclusion the model is intended to support
boundary             object with spatial, temporal, and resolution descriptions
assumptions          list of {id, text, testable}
sets                 object keyed by set symbol; each has meaning and optional cardinality
symbols              object keyed by symbol; each has role, meaning, shape, unit, source, observability
equations            list of equation records
validation           list of validation records
literature_status    {status, reason}; status is verified|unexecuted|not_required
literature_baselines list of closest-model records
computational_plan   solver, initialization, and complexity description
levels               minimal, strengthened, and advanced equation-ID lists
```

Allowed symbol roles:

`state`, `algebraic`, `control`, `decision`, `disturbance`, `parameter`, `observation`, `output`, `dual`, `random`, `index`, `auxiliary`.

Allowed equation kinds:

`definition`, `algebraic`, `dynamic`, `observation`, `objective`, `equality_constraint`, `inequality_constraint`, `boundary`, `initial`, `stochastic`, `equilibrium`, `sensitivity`.

Each equation record contains:

- `id`, `kind`, `latex`, and `symbols`;
- `defines`: symbols introduced or determined by the equation;
- `assumptions`: referenced assumption IDs;
- `validation`: referenced validation IDs;
- `mechanism`: physical, empirical, statistical, or decision meaning;
- optional `regularity`, `lhs_shape`, `rhs_shape`, `lhs_unit`, and `rhs_term_units`.

Each validation record contains `id`, `kind`, `description`, and `status`. Use status `planned`, `passed`, `failed`, `conditional`, or `unexecuted`. An executed status also needs `artifact`, pointing to the derivation, script, solver output, table, or result record.

## Example

```json
{
  "model_id": "network-dynamic-risk-v1",
  "domain": "power_systems",
  "purpose": "control",
  "claim": "Quantify and reduce short-horizon network risk under bounded disturbances.",
  "boundary": {
    "spatial": "n-bus transmission network",
    "temporal": "0-10 s",
    "resolution": "continuous-time electromechanical approximation"
  },
  "assumptions": [
    {"id": "A1", "text": "Topology is fixed within the horizon.", "testable": true}
  ],
  "sets": {
    "N": {"meaning": "buses", "cardinality": "n"},
    "E": {"meaning": "branches", "cardinality": "m"}
  },
  "symbols": {
    "x": {"role": "state", "meaning": "dynamic state", "shape": ["n_x", 1], "unit": "mixed; component table required", "source": "estimated", "observability": "partial"},
    "u": {"role": "control", "meaning": "control action", "shape": ["n_u", 1], "unit": "p.u.", "source": "decision", "observability": "known"},
    "A_s": {"role": "parameter", "meaning": "linearized state matrix", "shape": ["n_x", "n_x"], "unit": "1/s with component scaling", "source": "derived", "observability": "identified"}
  },
  "equations": [
    {
      "id": "E1",
      "kind": "dynamic",
      "latex": "\\dot{x}=A_s x+B_s u+E_s w",
      "symbols": ["x", "A_s", "u"],
      "defines": ["x"],
      "assumptions": ["A1"],
      "validation": ["V1"],
      "mechanism": "Local state evolution around a defined equilibrium.",
      "regularity": "Matrices are constant in the local operating region."
    }
  ],
  "validation": [
    {"id": "V1", "kind": "numerical", "description": "Compare linear and nonlinear trajectories under bounded perturbations.", "status": "planned"}
  ],
  "literature_status": {"status": "unexecuted", "reason": "No browsing was authorized for this example."},
  "literature_baselines": [
    {"id": "B1", "citation": "verified citation required", "difference": "Adds topology-aware disturbance coupling."}
  ],
  "computational_plan": {"solver": "MATLAB ode15s", "initialization": "consistent equilibrium", "complexity": "sparse Jacobian"},
  "levels": {"minimal": ["E1"], "strengthened": ["E1"], "advanced": ["E1"]}
}
```

The example is structural only; it intentionally omits several symbols used by the displayed equation so the validator will expose the missing definitions.

## Validator behavior

`scripts/audit_model_spec.py` checks required fields, IDs, references, symbol metadata, equation traceability, literature status, and common purpose/structure inconsistencies. It never parses or executes LaTeX. Use `--strict` to fail on warnings during a quality gate. An `unexecuted` literature status records an intentional no-browse or unavailable-source condition but still prevents a strict pass and an unconditional novelty claim.
