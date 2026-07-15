#!/usr/bin/env python3
"""Audit structural completeness of a scientific mathematical-model JSON record.

This script does not parse or execute LaTeX and cannot establish physical truth.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

MAX_BYTES = 5 * 1024 * 1024

PURPOSES = {
    "explanation",
    "prediction",
    "estimation",
    "control",
    "optimization",
    "decision",
    "discovery",
}

SYMBOL_ROLES = {
    "state",
    "algebraic",
    "control",
    "decision",
    "disturbance",
    "parameter",
    "observation",
    "output",
    "dual",
    "random",
    "index",
    "auxiliary",
}

EQUATION_KINDS = {
    "definition",
    "algebraic",
    "dynamic",
    "observation",
    "objective",
    "equality_constraint",
    "inequality_constraint",
    "boundary",
    "initial",
    "stochastic",
    "equilibrium",
    "sensitivity",
}

VALIDATION_STATUSES = {"planned", "passed", "failed", "conditional", "unexecuted"}
VALIDATION_KINDS = {
    "symbolic",
    "numerical",
    "limit",
    "data",
    "literature",
    "counterexample",
    "dimensional",
    "shape",
    "feasibility",
    "sensitivity",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a mathematical-model specification JSON without executing equations."
    )
    parser.add_argument("spec", type=Path, help="Path to model-spec JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return failure when warnings remain as well as when errors exist",
    )
    return parser.parse_args()


def is_nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def add_issue(
    issues: list[dict[str, str]], severity: str, code: str, path: str, message: str
) -> None:
    issues.append({"severity": severity, "code": code, "path": path, "message": message})


def require_keys(
    obj: Any,
    keys: list[str],
    path: str,
    issues: list[dict[str, str]],
) -> None:
    if not isinstance(obj, dict):
        add_issue(issues, "error", "TYPE-OBJECT", path, "Expected an object.")
        return
    for key in keys:
        if key not in obj:
            add_issue(issues, "error", "MISSING-KEY", f"{path}.{key}", "Required key is missing.")


def unique_ids(
    records: Any, path: str, issues: list[dict[str, str]]
) -> tuple[set[str], list[dict[str, Any]]]:
    if not isinstance(records, list):
        add_issue(issues, "error", "TYPE-LIST", path, "Expected a list.")
        return set(), []
    ids: set[str] = set()
    valid_records: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        item_path = f"{path}[{index}]"
        if not isinstance(record, dict):
            add_issue(issues, "error", "TYPE-OBJECT", item_path, "Expected an object.")
            continue
        valid_records.append(record)
        record_id = record.get("id")
        if not is_nonempty_text(record_id):
            add_issue(issues, "error", "MISSING-ID", f"{item_path}.id", "A non-empty ID is required.")
        elif record_id in ids:
            add_issue(issues, "error", "DUPLICATE-ID", f"{item_path}.id", f"Duplicate ID {record_id!r}.")
        else:
            ids.add(record_id)
    return ids, valid_records


def validate(spec: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    require_keys(
        spec,
        [
            "model_id",
            "domain",
            "purpose",
            "claim",
            "boundary",
            "assumptions",
            "sets",
            "symbols",
            "equations",
            "validation",
            "literature_status",
            "literature_baselines",
            "computational_plan",
            "levels",
        ],
        "$",
        issues,
    )

    for key in ("model_id", "domain", "claim"):
        if key in spec and not is_nonempty_text(spec[key]):
            add_issue(issues, "error", "EMPTY-TEXT", f"$.{key}", "Expected non-empty text.")

    purpose = spec.get("purpose")
    if purpose not in PURPOSES:
        add_issue(
            issues,
            "error",
            "PURPOSE-INVALID",
            "$.purpose",
            f"Expected one of {sorted(PURPOSES)}.",
        )

    boundary = spec.get("boundary")
    require_keys(boundary, ["spatial", "temporal", "resolution"], "$.boundary", issues)
    if isinstance(boundary, dict):
        for key in ("spatial", "temporal", "resolution"):
            if key in boundary and not is_nonempty_text(boundary[key]):
                add_issue(issues, "error", "EMPTY-TEXT", f"$.boundary.{key}", "Expected non-empty text.")

    assumption_ids, assumptions = unique_ids(spec.get("assumptions"), "$.assumptions", issues)
    for index, item in enumerate(assumptions):
        require_keys(item, ["id", "text", "testable"], f"$.assumptions[{index}]", issues)
        if "text" in item and not is_nonempty_text(item["text"]):
            add_issue(issues, "error", "EMPTY-TEXT", f"$.assumptions[{index}].text", "Expected non-empty text.")
        if "testable" in item and not isinstance(item["testable"], bool):
            add_issue(issues, "error", "TYPE-BOOL", f"$.assumptions[{index}].testable", "Expected true or false.")

    sets = spec.get("sets")
    if not isinstance(sets, dict):
        add_issue(issues, "error", "TYPE-OBJECT", "$.sets", "Expected an object keyed by set symbol.")
        sets = {}
    for name, item in sets.items():
        item_path = f"$.sets.{name}"
        require_keys(item, ["meaning"], item_path, issues)
        if not is_nonempty_text(name):
            add_issue(issues, "error", "EMPTY-SET", item_path, "Set key cannot be empty.")
        if isinstance(item, dict) and not is_nonempty_text(item.get("meaning")):
            add_issue(issues, "error", "EMPTY-TEXT", f"{item_path}.meaning", "Expected non-empty text.")

    symbols = spec.get("symbols")
    if not isinstance(symbols, dict):
        add_issue(issues, "error", "TYPE-OBJECT", "$.symbols", "Expected an object keyed by symbol.")
        symbols = {}
    symbol_names = set(symbols)
    required_symbol_fields = ["role", "meaning", "shape", "unit", "source", "observability"]
    symbol_metadata_complete = 0
    roles: dict[str, int] = {}
    for name, item in symbols.items():
        item_path = f"$.symbols.{name}"
        require_keys(item, required_symbol_fields, item_path, issues)
        if not isinstance(item, dict):
            continue
        if all(field in item and item[field] not in (None, "", []) for field in required_symbol_fields):
            symbol_metadata_complete += 1
        role = item.get("role")
        if role not in SYMBOL_ROLES:
            add_issue(issues, "error", "ROLE-INVALID", f"{item_path}.role", f"Expected one of {sorted(SYMBOL_ROLES)}.")
        else:
            roles[role] = roles.get(role, 0) + 1
        if not is_nonempty_text(item.get("meaning")):
            add_issue(issues, "error", "EMPTY-TEXT", f"{item_path}.meaning", "Expected non-empty text.")
        shape = item.get("shape")
        if not isinstance(shape, list) or not shape:
            add_issue(issues, "error", "SHAPE-MISSING", f"{item_path}.shape", "Use a non-empty list; use [1] for a scalar.")
        if not is_nonempty_text(item.get("unit")):
            add_issue(issues, "error", "UNIT-MISSING", f"{item_path}.unit", "State a unit or 'dimensionless'.")

    validation_ids, validations = unique_ids(spec.get("validation"), "$.validation", issues)
    executed_validation_count = 0
    for index, item in enumerate(validations):
        item_path = f"$.validation[{index}]"
        require_keys(item, ["id", "kind", "description", "status"], item_path, issues)
        kind = item.get("kind")
        if kind not in VALIDATION_KINDS:
            add_issue(issues, "error", "VALIDATION-KIND", f"{item_path}.kind", f"Expected one of {sorted(VALIDATION_KINDS)}.")
        status = item.get("status")
        if status not in VALIDATION_STATUSES:
            add_issue(issues, "error", "VALIDATION-STATUS", f"{item_path}.status", f"Expected one of {sorted(VALIDATION_STATUSES)}.")
        elif status in {"passed", "failed", "conditional"}:
            executed_validation_count += 1
            if not is_nonempty_text(item.get("artifact")):
                add_issue(
                    issues,
                    "warning",
                    "VALIDATION-ARTIFACT",
                    f"{item_path}.artifact",
                    "Executed evidence needs an artifact, derivation, output, or result location.",
                )
        if not is_nonempty_text(item.get("description")):
            add_issue(issues, "error", "EMPTY-TEXT", f"{item_path}.description", "Expected non-empty text.")

    equation_ids, equations = unique_ids(spec.get("equations"), "$.equations", issues)
    used_symbols: set[str] = set()
    kinds: dict[str, int] = {}
    traced_equations = 0
    additive_candidates = 0
    for index, item in enumerate(equations):
        item_path = f"$.equations[{index}]"
        require_keys(
            item,
            ["id", "kind", "latex", "symbols", "defines", "assumptions", "validation", "mechanism"],
            item_path,
            issues,
        )
        kind = item.get("kind")
        if kind not in EQUATION_KINDS:
            add_issue(issues, "error", "EQUATION-KIND", f"{item_path}.kind", f"Expected one of {sorted(EQUATION_KINDS)}.")
        else:
            kinds[kind] = kinds.get(kind, 0) + 1
        latex = item.get("latex")
        if not is_nonempty_text(latex):
            add_issue(issues, "error", "EMPTY-LATEX", f"{item_path}.latex", "Expected a non-empty equation string.")
            latex = ""
        eq_symbols = item.get("symbols")
        if not isinstance(eq_symbols, list):
            add_issue(issues, "error", "TYPE-LIST", f"{item_path}.symbols", "Expected a list of symbol keys.")
            eq_symbols = []
        for symbol in eq_symbols:
            if symbol not in symbol_names:
                add_issue(issues, "error", "SYMBOL-UNDEFINED", f"{item_path}.symbols", f"Undefined symbol {symbol!r}.")
            elif isinstance(symbol, str):
                used_symbols.add(symbol)
        defines = item.get("defines")
        if not isinstance(defines, list):
            add_issue(issues, "error", "TYPE-LIST", f"{item_path}.defines", "Expected a list of symbol keys.")
        elif kind not in {"objective", "equality_constraint", "inequality_constraint", "boundary", "initial"} and not defines:
            add_issue(issues, "warning", "DEFINE-EMPTY", f"{item_path}.defines", "State what this equation determines or defines.")
        if isinstance(defines, list):
            for symbol in defines:
                if symbol not in symbol_names:
                    add_issue(issues, "error", "DEFINE-UNDEFINED", f"{item_path}.defines", f"Undefined symbol {symbol!r}.")
        assumption_refs = item.get("assumptions")
        if not isinstance(assumption_refs, list):
            add_issue(issues, "error", "TYPE-LIST", f"{item_path}.assumptions", "Expected a list of assumption IDs.")
            assumption_refs = []
        for assumption in assumption_refs:
            if assumption not in assumption_ids:
                add_issue(issues, "error", "ASSUMPTION-REF", f"{item_path}.assumptions", f"Unknown assumption ID {assumption!r}.")
        validation_refs = item.get("validation")
        if not isinstance(validation_refs, list):
            add_issue(issues, "error", "TYPE-LIST", f"{item_path}.validation", "Expected a list of validation IDs.")
            validation_refs = []
        for validation_id in validation_refs:
            if validation_id not in validation_ids:
                add_issue(issues, "error", "VALIDATION-REF", f"{item_path}.validation", f"Unknown validation ID {validation_id!r}.")
        if validation_refs and is_nonempty_text(item.get("mechanism")):
            traced_equations += 1
        else:
            add_issue(issues, "warning", "TRACEABILITY", item_path, "Equation needs both a mechanism and a validation link.")
        if kind in {"dynamic", "sensitivity"} or re.search(r"\\(?:dot|partial|nabla)|d\s*[/]d", latex):
            if not is_nonempty_text(item.get("regularity")):
                add_issue(issues, "warning", "REGULARITY-MISSING", f"{item_path}.regularity", "State differentiability, operating region, or nonsingularity conditions.")
        if latex.count("+") >= 2 or "\\sum" in latex:
            additive_candidates += 1

    unused_symbols = sorted(
        name
        for name, item in symbols.items()
        if name not in used_symbols and isinstance(item, dict) and item.get("role") not in {"index", "output"}
    )
    for name in unused_symbols:
        add_issue(issues, "warning", "SYMBOL-UNUSED", f"$.symbols.{name}", "Symbol is defined but not referenced by any equation record.")

    if purpose in {"optimization", "decision", "control"}:
        if kinds.get("objective", 0) == 0:
            add_issue(issues, "warning", "OBJECTIVE-MISSING", "$.equations", "Purpose normally requires an explicit objective or decision criterion.")
        if roles.get("decision", 0) + roles.get("control", 0) == 0:
            add_issue(issues, "error", "DECISION-MISSING", "$.symbols", "No decision or control variable is defined.")
    if kinds.get("objective", 0) and roles.get("decision", 0) + roles.get("control", 0) == 0:
        add_issue(issues, "error", "OBJECTIVE-NO-DECISION", "$.equations", "Objective exists without a decision or control variable.")
    if purpose == "estimation" and kinds.get("observation", 0) == 0:
        add_issue(issues, "warning", "OBSERVATION-MISSING", "$.equations", "Estimation purpose needs an observation model.")
    if kinds.get("dynamic", 0) and not (kinds.get("initial", 0) or kinds.get("boundary", 0)):
        add_issue(issues, "warning", "INITIAL-MISSING", "$.equations", "Dynamic model has no initial or boundary equation record.")
    if roles.get("random", 0) and kinds.get("stochastic", 0) == 0:
        add_issue(issues, "warning", "STOCHASTIC-SEMANTICS", "$.equations", "Random symbols exist without a stochastic equation or probability semantics.")

    literature_status = spec.get("literature_status")
    require_keys(literature_status, ["status", "reason"], "$.literature_status", issues)
    literature_state = None
    if isinstance(literature_status, dict):
        literature_state = literature_status.get("status")
        if literature_state not in {"verified", "unexecuted", "not_required"}:
            add_issue(
                issues,
                "error",
                "LITERATURE-STATUS",
                "$.literature_status.status",
                "Expected 'verified', 'unexecuted', or 'not_required'.",
            )
        if not is_nonempty_text(literature_status.get("reason")):
            add_issue(issues, "error", "EMPTY-TEXT", "$.literature_status.reason", "Expected non-empty text.")

    baselines = spec.get("literature_baselines")
    if not isinstance(baselines, list):
        add_issue(issues, "error", "TYPE-LIST", "$.literature_baselines", "Expected a list.")
        baselines = []
    if not baselines:
        if literature_state == "verified":
            add_issue(issues, "error", "BASELINE-MISSING", "$.literature_baselines", "Verified literature status requires at least one closest model.")
        elif literature_state == "unexecuted":
            add_issue(issues, "warning", "BASELINE-UNEXECUTED", "$.literature_status", "Literature comparison is unexecuted; novelty and unconditional GO claims are unavailable.")
        elif literature_state == "not_required":
            add_issue(issues, "warning", "BASELINE-NOT-REQUIRED", "$.literature_status", "Confirm that the task truly makes no literature or novelty claim.")
    for index, item in enumerate(baselines):
        item_path = f"$.literature_baselines[{index}]"
        require_keys(item, ["id", "citation", "difference"], item_path, issues)
        if isinstance(item, dict):
            for key in ("id", "citation", "difference"):
                if not is_nonempty_text(item.get(key)):
                    add_issue(issues, "error", "EMPTY-TEXT", f"{item_path}.{key}", "Expected non-empty text.")

    computational_plan = spec.get("computational_plan")
    require_keys(computational_plan, ["solver", "initialization", "complexity"], "$.computational_plan", issues)
    if isinstance(computational_plan, dict):
        for key in ("solver", "initialization", "complexity"):
            if key in computational_plan and not is_nonempty_text(computational_plan[key]):
                add_issue(issues, "error", "EMPTY-TEXT", f"$.computational_plan.{key}", "Expected non-empty text.")

    levels = spec.get("levels")
    require_keys(levels, ["minimal", "strengthened", "advanced"], "$.levels", issues)
    if isinstance(levels, dict):
        for level in ("minimal", "strengthened", "advanced"):
            refs = levels.get(level)
            if not isinstance(refs, list) or not refs:
                add_issue(issues, "error", "LEVEL-EMPTY", f"$.levels.{level}", "Expected a non-empty equation-ID list.")
                continue
            for equation_id in refs:
                if equation_id not in equation_ids:
                    add_issue(issues, "error", "LEVEL-REF", f"$.levels.{level}", f"Unknown equation ID {equation_id!r}.")
        if levels.get("minimal") == levels.get("advanced"):
            add_issue(issues, "warning", "LEVELS-IDENTICAL", "$.levels", "Minimal and advanced levels are identical; explain why no structural deepening is needed.")

    if len(equations) <= 2 and additive_candidates and not any(
        kinds.get(kind, 0)
        for kind in ("dynamic", "stochastic", "equality_constraint", "inequality_constraint", "sensitivity")
    ):
        add_issue(
            issues,
            "warning",
            "SIMPLICITY-ALARM",
            "$.equations",
            "Model is dominated by an additive relation with no explicit dynamics, constraints, uncertainty, or sensitivity. Justify it as a baseline or add the missing mechanism.",
        )

    if validations and executed_validation_count == 0:
        add_issue(issues, "warning", "VALIDATION-UNEXECUTED", "$.validation", "No validation has executed evidence yet.")

    error_count = sum(issue["severity"] == "error" for issue in issues)
    warning_count = sum(issue["severity"] == "warning" for issue in issues)
    equation_count = len(equations)
    symbol_count = len(symbols)
    metrics = {
        "assumption_count": len(assumptions),
        "set_count": len(sets),
        "symbol_count": symbol_count,
        "equation_count": equation_count,
        "validation_count": len(validations),
        "executed_validation_count": executed_validation_count,
        "literature_baseline_count": len(baselines),
        "literature_status": literature_state,
        "symbol_metadata_coverage": round(symbol_metadata_complete / symbol_count, 3) if symbol_count else 0.0,
        "equation_traceability_coverage": round(traced_equations / equation_count, 3) if equation_count else 0.0,
    }
    verdict = "structural_fail" if error_count else "structural_review" if warning_count else "structural_pass"
    return {
        "ok": error_count == 0,
        "verdict": verdict,
        "errors": error_count,
        "warnings": warning_count,
        "metrics": metrics,
        "issues": issues,
        "limitations": [
            "LaTeX was not parsed or executed.",
            "Physical truth, empirical validity, novelty, and solver correctness require independent review.",
        ],
    }


def main() -> int:
    args = parse_args()
    try:
        path = args.spec.resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Model spec not found: {path}")
        if path.stat().st_size > MAX_BYTES:
            raise ValueError(f"Model spec exceeds {MAX_BYTES} bytes")
        with path.open("r", encoding="utf-8") as handle:
            spec = json.load(handle)
        if not isinstance(spec, dict):
            raise ValueError("Top-level JSON value must be an object")
        result = validate(spec)
        result["path"] = str(path)
        print(json.dumps(result, ensure_ascii=True, indent=2))
        if not result["ok"]:
            return 1
        if args.strict and result["warnings"]:
            return 1
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
