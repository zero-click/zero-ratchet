# Learning Log

Project-level learnings from building hermes-ecc-profile. Each entry is dated, names the failure mode observed, the fix shipped, and the residual question. Bilingual: 中文 first, English second.

---

## 2026-06-16 — PRD review gate: structural completeness ≠ quality

### 中文

**观察到的失败模式**（来自 cos-agent V4-F6/F7 实战）：

PRD review gate 即使 7 个 required section 全在、看起来"结构完整"，第一轮也会放过下面这些质量问题：

1. **把某个具体例子当成问题本体** — PRD 写"X 系统日志坏了"，但真正的问题是通用的 egress 可见性不够，X 系统只是暴露这个问题的那个例子
2. **多关系 FR** — 一个 functional requirement 一句话塞了路由 + 可观测性 + fallback + scope 边界。下游没法测，也没法干净拆 story
3. **隐藏的 AI 推断** — 默认路径、优先级规则、阈值数字这些 AI 脑补出来的决定，混在散文里，没标记"用户没确认"。整份 PRD 零个 `[ASSUMPTION]` 标签照样过
4. **persona theater** — 内部工具 feature 硬填一个"主要用户"表格只为过结构检查
5. **success metrics 写成活动计数** — 类似"用户能无困惑地完成"这种 bullet，没量化指标也没 counter-metric

**修复路径**：

光有结构 checklist 不够。AI 评 AI 时 gate 必须有两个东西：

- **Calibration anchors**：让同一份 PRD 评两次得到同一个评级。例如 P0 问题描述质量分 `strong / adequate / thin / broken` 四档，每档有明确的判断锚点（"observable problem 描述的是通用问题还是当前例子？"），`thin/broken` 直接 hard-fail
- **Positive-evidence requirement**：reviewer 必须**主动找出**问题，不是"没看到红旗就 PASS"。例如 P9 要求 reviewer 必须从 PRD 里找出 ≥2 个领域特定推断（路径、默认值、优先级、阈值这些 source 没说的东西），逐一验证它们是已标记还是真能追溯到用户输入。一份非平凡 PRD 零个 `[ASSUMPTION]` 标签现在是红旗，不是绿灯

其它配套：
- 每个 FR 必须带可测试的 consequences bullet（带具体阈值）。"graceful handling" / "reasonable performance" 被重写或拒
- 新增 FR 原子性检查（一个 FR 只能表达一个能力或一个关系）
- personas/flows 改 conditional（consumer-product/多 stakeholder 才必须；internal-tool/CLI 直接省，不要写填空式占位）
- 对称纪律：REQUEST_CHANGES 的 finding 也必须 cite 位置 + 引用原句，不能"不够清晰"这种泛批
- 加 `Shape:` 字段在 Background 第一行声明 feature shape，Phase A 据此决定 conditional sections

**核心 insight**：

> 当 AI 评 AI 的输出时，gate 默认会收敛到"第一轮 PASS"。要打破这个默认，必须强制 reviewer 做**有难度的主动判断**（rate + anchor，find + verify），而不是被动 checklist 打勾。

**遗留问题**：

- `[ASSUMPTION]` 机制隐含 human-in-the-loop 不可避免：要么人确认推断（HITL），要么默认通过靠下游 test 兜底（长 feedback loop），AI 自己确认 AI 推断 = 又掉回 "AI judges AI" 这个 Limitation #1
- 务实做法是把 HITL 的颗粒度从"读全 PRD 找 bug"压缩到"扫 Assumptions Index list 打勾叉"（5 分钟批量 triage），不是消灭 HITL
- "Fully unattended" 是 long-term vision，不是绝对 target；"unattended-by-default + 人偶尔被叫醒做 5 分钟批量 triage" 才是可达的

**Dogfood 验证**：

我自己 ship 这次 PRD skill 加固之后，reverse-engineer 自己刚做的改动，能列出 11 条没标记的设计推断（Shape 字段机制、Shape 取值分类、P9 的"2"这个数字、counter-metric mandatory vs recommended，等等）。正好印证了 Assumptions Index 的价值——reviewer 看 list 批量 triage 的工作量是合理的。

**关联文件**：
- `skills/product-design/woos-product-prd-review-gate/SKILL.md`
- `skills/product-design/woos-prd-authoring/SKILL.md`
- `skills/product-design/woos-requirement-contract/SKILL.md`
- PR #23

---

### English

**Observed failure mode** (from cos-agent V4-F6/F7 runs):

The PRD review gate was passing structurally-complete PRDs on the first round despite real quality problems:

1. **One channel mistaken for the general problem** — PRD said "X-system logging is broken" when the actual issue was general egress visibility and X-system was just the example that exposed it
2. **Multi-relationship FRs** — a single functional requirement bundled routing + observability + fallback + scope boundary in one sentence; impossible to test, impossible to split into stories cleanly
3. **Hidden AI inferences** — default paths, precedence rules, threshold numbers fabricated by the AI, buried in prose with no flag that they weren't user-confirmed; zero `[ASSUMPTION]` tags in the whole doc and it still passed
4. **Persona theater** — internal-tool features with manufactured "primary user" tables filled in only to satisfy a structural check
5. **Success metrics as activity counters** — "users complete without confusion" type bullets, no quantitative target, no counter-metric

**Fix**:

Structural checklists aren't enough. When AI reviews AI, the gate needs two things:

- **Calibration anchors** — so the same PRD gets the same rating twice. Example: P0 problem-framing rated `strong / adequate / thin / broken` with explicit anchors per tier ("does the observable problem describe the general problem, or just the current example?"). `thin/broken` hard-fails the gate.
- **Positive-evidence requirement** — reviewer must **proactively find** problems, not "no red flag therefore PASS". Example: P9 requires the reviewer to identify ≥2 domain-specific inferences in the PRD (specific paths, defaults, precedences, thresholds not stated in the source) and verify they are either tagged or genuinely traced to user input. A non-trivial PRD with zero `[ASSUMPTION]` tags is now a red flag, not a green light.

Supporting changes:
- Every FR must carry a testable consequences bullet with a concrete threshold; "graceful handling" / "reasonable performance" gets rewritten or rejected
- New FR atomicity check (one capability or one relationship per FR)
- Personas/flows became conditionally required (mandatory for consumer-product / multi-stakeholder; omit entirely for internal-tool / CLI rather than write filler)
- Symmetric discipline: REQUEST_CHANGES findings must also cite location + quoted phrase, no abstract "could be tighter" criticism
- Added a `Shape:` field declared at the top of Background; Phase A uses it to decide which conditional sections apply

**Core insight**:

> When AI reviews AI output, the gate converges on first-round PASS by default. To break that default, the reviewer must be forced to make **hard active judgments** (rate against anchors, find and verify), not passive checklist ticks.

**Open questions**:

- The `[ASSUMPTION]` mechanism implies human-in-the-loop is unavoidable: either a human confirms inferences (HITL), or they're silently accepted and downstream tests catch the wrong ones (long feedback loop). Having AI confirm AI's own inferences falls right back into Limitation #1 ("AI judges AI")
- The pragmatic move is to compress HITL granularity from "read the full PRD to find bugs" down to "scan the Assumptions Index list and approve/reject" (5-minute batch triage), not to eliminate HITL
- "Fully unattended" is a long-term vision, not an absolute target. "Unattended-by-default + occasional 5-minute human triage" is the realistic target

**Dogfood validation**:

After shipping this hardening, I reverse-engineered my own changes and was able to list 11 unsurfaced design inferences I'd just made (the existence of the `Shape:` field mechanism, the Shape taxonomy, the "2" threshold in P9, counter-metric mandatory-vs-recommended, etc.). This directly validates the Assumptions Index pattern — the reviewer's workload to triage a list of 11 items is manageable.

**Related files**:
- `skills/product-design/woos-product-prd-review-gate/SKILL.md`
- `skills/product-design/woos-prd-authoring/SKILL.md`
- `skills/product-design/woos-requirement-contract/SKILL.md`
- PR #23
