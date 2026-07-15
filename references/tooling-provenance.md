# Tooling and provenance

## Contents

- Reviewed public sources
- Recommended composition
- Installation and data-safety rules

## Reviewed public sources

This Skill's workflow was informed by, but does not copy or automatically execute, these public resources:

- K-Dense Scientific Agent Skills collection: https://github.com/K-Dense-AI/scientific-agent-skills
- K-Dense SymPy Skill: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/sympy
- K-Dense Scientific Critical Thinking Skill: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-critical-thinking
- K-Dense Scientific Brainstorming Skill: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-brainstorming
- K-Dense MATLAB Skill: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/matlab
- K-Dense Pymoo Skill: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/pymoo
- SymPy official documentation: https://docs.sympy.org/
- SymPy dimensions documentation: https://docs.sympy.org/latest/modules/physics/units/dimensions.html
- PySR official repository: https://github.com/MilesCranmer/PySR
- Wolfram official MCP documentation: https://www.wolfram.com/artificial-intelligence/mcp/cloud/wolfram-mcp-cloud/

The K-Dense repository's own security guidance recommends reviewing individual skills and avoiding an indiscriminate full-repository installation. Its security report notes low-level concerns in the SymPy Skill, including unsafe-parser patterns in examples and ambiguous missing-file references. This Skill therefore uses a local-first workflow and forbids unsafe expression parsing.

## Recommended composition

- Use this Skill as the reasoning and quality gate.
- Use MATLAB or SymPy as deterministic verification backends, not as model inventors.
- Use PySR only when data-driven equation discovery is appropriate; constrain operators with units, symmetry, conservation, monotonicity, and known limits.
- Use multi-objective optimization only after objectives, constraints, and decision variables are physically and mathematically justified.
- Use literature retrieval to determine whether a proposed structure is established, adapted, or genuinely new.
- Use MathType only for final representation after verification.

## Installation and data-safety rules

- Do not install the full public collection by default.
- Review the exact `SKILL.md`, references, scripts, dependency versions, external API calls, and license before installing any third-party Skill.
- Prefer a pinned commit or release and a topical subset.
- Do not run examples that contain `eval`, unsafe `parse_expr`, shell interpolation, or automatic secret loading.
- Do not send unpublished equations, datasets, paper drafts, patents, or project details to Wolfram Cloud, OpenRouter, hosted symbolic-regression systems, or other third parties without explicit approval.
- Prefer local MATLAB and local deterministic Python environments.
- Record tool and package versions in the verification evidence.
