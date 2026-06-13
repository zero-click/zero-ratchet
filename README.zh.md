# zero-ratchet

[English](./README.md) | [中文](./README.zh.md)

面向 AI 编程 agent 的完整 **想法 → 交付** skill 集合：产品发现、PRD、设计、故事计划、TDD 循环、门禁、可追溯、PR——每个阶段都有明确的角色分工和硬性检查点。

Host 无关。任何能从目录加载 skill 的 agent runtime（Claude Code、Cursor、Hermes ……）都能用。

**核心 thesis：** 你只需要记住两个入口（产品工作用 `woos-idea-to-design`，工程工作用 `woos-development-workflow`）。内部的 orchestrator 自己加载子 skill、在 fresh context 里调度评审、卡 gate 推进。Skill 是写给 AI 读的，不是给人背的。人只在刻意安排的 checkpoint 重新介入。

## 这里有什么

| 目录 | 用途 | 维护方式 |
|------|------|----------|
| `skills/product-design/` | 产品流程：idea → discovery → PRD → roadmap → UI brief | 本地维护，`woos-*` |
| `skills/software-development/` | 工程流程：设计 → 故事计划 → TDD 循环 → 评审 → PR | 本地维护，`woos-*` |
| `skills/ecc/` | 工程流程依赖的上游 [ECC](https://github.com/everything-claude-code/everything-claude-code) skill（tdd-workflow、security-review……） | 快照——不要手改 |

三个目录互相独立，按需取用。

## 安装

没有安装脚本。把你想用的目录拷贝或软链到 agent host 加载 skill 的位置。软链可以让上游 `git pull` 的更新自然生效：

```bash
ln -s "$PWD/skills/product-design"       ~/.claude/skills/product-design
ln -s "$PWD/skills/software-development" ~/.claude/skills/software-development
ln -s "$PWD/skills/ecc"                  ~/.claude/skills/ecc
```

把 `.claude/skills/` 换成 `.cursor/skills/`、`~/.hermes/profiles/coding/skills/`、或你 runtime 期望的路径。

## 命名约定

- **`woos-*`** —— 本地编写的 skill，可以随意改
- **无前缀**（仅出现在 `skills/ecc/` 下）—— 上游快照，不要手改；用刷新脚本同步

## 流水线总览

```
┌──────────────────────────────────┐        ┌──────────────────────────────────┐
│   产品设计阶段                    │   PRD  │   软件开发阶段                    │
│   skills/product-design/         │──────▶ │   skills/software-development/   │
│                                  │ Roadmap│                                  │
│   Idea → Capture → Discovery     │ Arch   │   Design → 故事计划 → TDD 循环   │
│   → 🚦 人工 Gate                  │        │   → 评审 → 追溯 → PR             │
│                                  │        │                                  │
│   入口：woos-idea-to-design       │        │   入口：woos-development-workflow │
│   模式：Lite / Standard / Strict  │        │   模式：Lite / Standard           │
└──────────────────────────────────┘        └──────────────────────────────────┘
                                                          │
                                                  DCR（反馈回路）
                                                          ▼
                                              docs/feedback/<ver>/...
```

**两阶段之间的 handoff 契约：**

- `docs/product/<project>-roadmap.md` —— 版本范围、目标
- `docs/product/<project>-architecture.md` —— 顶层组件图
- `docs/prd/<version>/<feature-id>.md` —— 单 feature PRD（问题、功能性 + 非功能性需求、行为契约）
- `docs/prd/<version>/<feature-id>-interface.md` —— 当其他 feature 依赖这个 feature 时的共享接口摘要（枚举、数据模型、事件/接口形状）
- `docs/design/<version>/<feature-id>-ui-brief.md` —— 涉及 UI 时的 UI 方向

剩下的归工程：代码组织、库选型、内部数据结构、测试策略、部署。

**DCR 回路：** 工程发现产品假设有错时，发起 Design Change Request 回到产品侧——PRD 更新后工程继续。

## 产品设计阶段

完整流程见 [`skills/product-design/README.md`](./skills/product-design/README.md)。

| Skill | 角色 |
|-------|------|
| `woos-idea-to-design` | 总入口——从原始想法到工程就绪的伞型 orchestrator |
| `woos-idea-capture` | 想法访谈与结构化 |
| `woos-product-discovery` | 研究、roadmap、架构 |
| `woos-product-design-flow` | PRD 流水线 orchestrator |
| `woos-ui-design-brief` | UI 方向与原型 |

强制规则：7 条不可妥协的 E1–E7，阻止跳步、忽略模板、敷衍评审。

## 软件开发阶段

完整流程见 [`skills/software-development/README.md`](./skills/software-development/README.md)。

入口：`woos-development-workflow`。Standard 模式：

```
Run Orchestrator → Git → Product Intake
  → Gate 1  Feature Plan（架构 + 故事表）          (woos-feature-plan)
  → Gate 1R Plan Review（双评审，fresh context）   (woos-plan-review-gate)
  → Gate 3  Story Loop（每个 story：TDD + Implement + Verify）
  → Gate 4  Executable Acceptance
  → Gate 5  Deviation Control
  → Gate 6  Traceability
  → Gate 7  Code / Security Review
  → Gate 8  PR Readiness
  → Workflow Memory
```

Lite 模式跳过 Gate 1、1R、4、5、6——适用于低风险小改动。

**Gate 1 的产物**是单个 per-feature `docs/engineering/<version>/<feature-id>-plan.md`：包含架构决策、测试策略、rollout/rollback、baseline/deviation 记录，以及 story 执行表（`ID | AC | Depends | Diff Scope`）。Interface 契约住在 PRD 的 `<feature-id>-interface.md` 里，这里不重复。PRD AC 是规约，diff scope 里的测试就是验证，`git restore -- <diff_scope>` 就是回滚。

## 与同类对比

| 框架 | 强项 | 这个 repo 为什么和它并存 |
|------|------|--------------------------|
| [ECC](https://github.com/everything-claude-code/everything-claude-code) | 高质量工程 skill 库（TDD、security、deployment……） | ECC 是自助餐——50+ skill、无 orchestrator、每次靠用户自己挑。本 repo 在 ECC 之上加了 gate 推进、条件触发规则，并覆盖了产品侧。 |
| [BMAD](https://github.com/bmadcode/BMAD-METHOD) | persona 主导的产品 + agile 流程 | BMAD 是对话主导（"跟 PM agent 聊"），本 repo 是工作流主导（两个触发短语，AI 自己跑）。persona 表面更轻，gate 更机器可校验。 |
| Superpowers | 实战派工程循环，TDD/debug 纪律强 | Superpowers 只覆盖工程侧。本 repo 在工程循环前加了完整产品流水线（discovery、PRD、接口摘要、UI brief）。 |

**适用：** 长跨度、多 feature、需要 gate 与可追溯、AI 主导跑、人只在特定 checkpoint 介入。

**多半 overkill：** 两句话能讲完的单个小改动——直接用 Superpowers 或裸 ECC 更快。

## 已知盲区

诚实清单——这些是真的问题，本周内不会修：

- **AI 在评 AI。** 每个 gate 的 PASS 都由 LLM 给出。`fresh_context` 防的是共谋，没法引入外部判断。**第一轮错误地 PASS 是最大盲区**——只有失败才会升级到 `woos-human-handoff`，成功不会。
- **`invocation_evidence` 是自证的。** 本该调用某子 skill 的 AI，也是写"我调用了"那段 JSON 的 AI。要根治得有外部 process 记录 dispatch 事件，目前没有。
- **Skill 间引用没 CI 校验。** SKILL.md 之间靠字符串相互引用（`woos-architect`、`woos-product-planner`……）。重命名/删除只有当 orchestrator 真去 dispatch 失败时才暴露。
- **"完成"的定义停在 PR 合并。** 没有 post-merge 钩子，没有部署/观测/"roadmap 的成功指标真的动了吗"的回环。
- **单人在用，没经过实战。** ECC/BMAD/Superpowers 有社区帮你踩坑，这条流水线只跑过一个人手上的少数 feature，很多失败模式还潜伏。
- **DCR 摩擦可能反向激励隐藏偏离。** Gate 5 把未授权偏离当 blocker，AI 的最优策略可能是少报而不是诚实报。目前没有反向激励机制。
- **DAG rollback 模糊。** 如果下游 story 已经基于上游 story commit，而上游需要 revert，级联回滚步骤是丢给 AI 想，没有写进工作流。

## 更新 `skills/ecc/`

`skills/ecc/` 是上游 ECC 的快照。从本地 ECC checkout 刷新并提交 diff：

```bash
scripts/refresh-ecc-skills.sh /path/to/everything-claude-code
git diff skills/ecc
git add skills/ecc && git commit
```

## 设计原则

- **无人值守交付是长期目标。** 角色化 agent + 硬性 gate，让更多工作可以可靠地无人介入完成。
- **角色分离、确定性 gate 推进、从想法到 PR 全程可追溯的评审。**
- **基线优先治理。** 默认走主流、可维护的基线；偏离需要 ADR 和明确批准。

### 无人值守执行基座

让整套 gated flow 能持续无人值守跑起来的 7 个基础设施 skill：

| Skill | 角色 |
|-------|------|
| `woos-run-orchestrator` | 运行队列、并发、超时/重试 |
| `woos-executable-acceptance-gate` | 机器可检查的完成标准 |
| `woos-failure-state-machine` | 确定性的重试/降级/升级 |
| `woos-deviation-control-gate` | 实现 vs 规约的漂移拦截 |
| `woos-workflow-memory` | 失败/返工模式的持久捕获 |
| `woos-human-handoff` | 显式人工接管与恢复协议 |
| `woos-review-context` | 跨 gate 的累积发现 |

### ADR 治理

- ADR 模板位于消费方项目：`docs/adr/ADR-template.md`
- 设计/代码评审 gate 必须输出 `baseline_compliance_status`、`deviation_detected`、`deviation_adr_path`
- Run 结束时需要一份已验证的 run-manifest：`<workspace_root>/hep/runs/<run_id>/run-manifest.yaml`
