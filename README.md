# Scientific Mathematical Model Audit | 科研数学模型审查

`scientific-mathematical-model-audit` is a Codex Skill for auditing, repairing, deepening, and verifying scientific mathematical models before publication or implementation.

`scientific-mathematical-model-audit` 用于在论文、专利、科研项目和代码实现之前，检查并修复数学模型的变量、单位、维度、假设、公式链、目标函数、约束、推导和验证闭环。

## 主要能力

- 重建研究问题、系统边界、状态、控制、扰动、参数、观测量和目标量组成的模型卡。
- 识别未定义变量、量纲或矩阵形状冲突、循环定义、任意权重、不可辨识量和不可行约束等致命缺陷。
- 区分“最小正确模型、结构增强模型、发表级高级模型”，说明每一层新增结构的机制、数据要求和计算代价。
- 审查矩阵、图模型、微分方程、优化、随机、鲁棒、敏感性和状态空间结构是否真正必要。
- 检查雅可比矩阵、Hessian、KKT 条件、稳定性、可观性、可控性、极限情形和基线对照。
- 为电力系统建模提供网络、动态、OPF、不确定性、稳定性和可观测性专项规则。
- 使用结构化 JSON 模型规格记录变量、方程、假设、证据和验证状态，并通过脚本执行完整性门禁。
- 输出可追溯的审查结论、变量维度表、推导链、验证证据和 MATLAB/SymPy 交接建议。

## 安装

```powershell
git clone https://github.com/xiao0xiao0/scientific-mathematical-model-audit.git "$env:USERPROFILE\.codex\skills\scientific-mathematical-model-audit"
```

安装后重新打开 Codex 会话。

## 典型调用

```text
请使用 $scientific-mathematical-model-audit 审查这个目标函数、约束和变量定义，先指出致命问题，再给出最小正确模型和可验证的增强模型。
```

```text
请使用 $scientific-mathematical-model-audit 检查这套电力系统模型的量纲、矩阵形状、KKT 条件、可辨识性和数值验证方案。
```

## 结构化检查

按照 [`references/model-spec-schema.md`](references/model-spec-schema.md) 建立模型规格后运行：

```powershell
python scripts/audit_model_spec.py model-spec.json --strict
```

该脚本只检查结构完整性，不能单独证明物理真实性、新颖性或经验有效性。

## 结果等级

- `structural pass`：结构闭环且没有未解决的严格模式警告。
- `mathematical pass`：与结论相关的符号和数值检查已经通过。
- `scientific pass`：物理假设、经验依据和文献位置能够支持目标结论。

只有所有相关门槛都通过时，才应将模型简称为“通过”。

## 使用边界

- 数学形式复杂不等于科学解释力强；正确的简单模型应当保留。
- 不得用任意加权、装饰性矩阵或没有概率模型的随机符号伪装创新性。
- 符号工具能够化简、数值求解器能够返回结果，都不能自动证明模型有效。
- 数据不足时，高级模型只能标记为研究设计建议，不能冒充已验证模型。
- 文献新颖性判断必须基于可核验来源。

## 文件结构

- `SKILL.md`：完整工作流和输出要求。
- `references/audit-rubric.md`：模型质量判据。
- `references/model-families.md`：候选模型结构及适用条件。
- `references/model-spec-schema.md`：结构化模型规格。
- `references/power-system-profile.md`：电力系统专项规则。
- `references/verification-protocol.md`：符号、数值和科学验证协议。
- `scripts/audit_model_spec.py`：模型规格完整性检查脚本。

## License

MIT License. See [`LICENSE`](LICENSE).
