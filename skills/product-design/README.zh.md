# 产品设计工作流

[English](./README.md) | [中文](./README.zh.md)

流水线的产品侧。把一个原始想法走完 capture → discovery → PRD，每步都有评审 gate，工程动手前还有一道强制的人工批准点。

入口 skill：**`woos-idea-to-design`**（伞型 orchestrator）。

## Quick Start

跟 agent 说一个想法——"我有个想法……"、"我们来做……"、"设计一下这个 feature"、"start V1" 这类触发短语会路由到 `woos-idea-to-design`。Orchestrator 自己处理阶段推进、子 agent 调度、gate 卡控。你只在决策点被问到。

## 流水线

```
原始想法
   │
   ▼  woos-idea-capture
ideas/<slug>/00-idea-capture.md
   │
   │  trivial？─是→ 用户确认 Lite ─────────────┐
   │                                          │
   ▼  woos-product-discovery                  │
docs/product/<project>-roadmap.md             │
docs/product/<project>-architecture.md        │
   │                                          │
   ▼  🚦 强制人工批准                          │
   │                                          │
   ▼  woos-product-design-flow                │
docs/prd/<version>/<feature-id>.md  ◀─────────┘
docs/prd/<version>/<feature-id>-interface.md（仅 Strict）
docs/design/<version>/<feature-id>-ui-brief.md（涉及 UI 时）
```

模式由系统自动推断，不是手动选：

| 模式 | 何时 | Phase 3 步骤 |
|------|------|--------------|
| Lite | 琐碎，< 2 天 | PRD |
| Standard | 单 feature，中等风险 | PRD → PRD Review |
| Strict | 多 feature、UX 重、高不确定性 | 每个 feature 跑全：PRD → PRD Review → UI → UI Review → Analyze → Interface Summary → Integration |

## Phase 1 —— Capture

| | |
|---|---|
| Skill | `woos-idea-capture` |
| 干啥 | 引导式访谈，把原始想法变成结构化的产品意图文档 |
| 输出 | `ideas/<slug>/00-idea-capture.md` |

## Phase 2 —— Discovery

| | |
|---|---|
| Skill | `woos-product-discovery`（orchestrator） |
| 干啥 | 验证问题、调研空间、产出 roadmap 和架构草图——每一步都有独立评审 gate |
| 输出 | `docs/product/<project>-roadmap.md` + `docs/product/<project>-architecture.md` |
| 子 skill | `woos-problem-validation`、`woos-product-research`、`woos-roadmap-authoring`（+ review gate）、`woos-architecture-overview`（+ review gate） |
| 出口 | 🚦 强制人工批准后才进 Phase 3 |

## Phase 3 —— Design Flow

| | |
|---|---|
| Skill | `woos-product-design-flow`（orchestrator） |
| 干啥 | 逐 feature：把 roadmap 条目变成一份经评审的 PRD（Strict 模式下还含 UI brief 和接口摘要） |
| 输出 | `docs/prd/<version>/<feature-id>.md` 及其同伴文件 |

Strict 模式的步骤：

| Step | Skill / 动作 | 输出 |
|------|--------------|------|
| 1 | Orchestrator 选定版本范围 | — |
| 1.5 | Orchestrator 分析 feature 依赖、确定执行顺序 | — |
| 2 | `woos-prd-authoring` | `<feature-id>.md` |
| 3 | `woos-product-prd-review-gate`（fresh context） | PRD 评审结论 |
| 4 | `woos-ui-design-brief`（涉及 UI 时） | `<feature-id>-ui-brief.md` |
| 4R | `woos-ui-brief-review`（fresh context） | UI 评审结论 |
| 5 | `woos-prd-consistency-audit`（fresh context） | 一致性审计结论 |
| 5.5 | Orchestrator 抽取共享接口契约 | `<feature-id>-interface.md` |
| 6 | `woos-version-integration-audit`（fresh context，从第 2 个 feature 起增量执行） | 集成审计结论 |

Lite 和 Standard 只跑子集——逐模式步骤清单见 [`woos-product-design-flow` SKILL](./woos-product-design-flow/SKILL.md)。

每个 feature 跑完：⭐ checkpoint——现在就交付给工程，还是先设计下一个 feature？

## 强制规则（P0–P7）

`woos-product-design-flow` 中不可妥协的规则，阻止跳步、忽略模板、敷衍评审：

| 规则 | 原则 |
|------|------|
| P0 | 显式 step dispatch——每步前声明 skill、输入、输出 |
| P1 | Orchestrator 不亲自写 artifact（仅 Step 1、1.5、6.5 例外） |
| P2 | 不合并、不跳过步骤 |
| P3 | 前进前验证输出文件存在且结构合规 |
| P4 | 不许自我评审——每个 gate 在 fresh 子 agent context 中跑 |
| P5 | Step 4、5R、6、7 强制子 agent 隔离 |
| P6 | 修复传播——任何重命名/改动必须 grep 并同步所有 version 文档 |
| P7 | 上游接口感知——下游 feature 接收上游 feature 的接口摘要作为附加输入 |

## DCR（从工程返回）

实现过程中发现产品假设有错时，工程会在 `docs/feedback/<version>/<feature-id>-dcr-<NNN>.md` 写一份 Design Change Request。Orchestrator 读完后判断范围：小改直接更新 PRD；大改从 Step 3 / Step 5 重跑。

## 知识层

产品流基于 [BMAD](https://github.com/bmad-agent/bmad-agent) 方法论，通过以下方式投递给子 agent：

- **Personas**：注入到特定评审步骤（UX Designer "Sally" 用于 UI brief 评审，PRD Validator 用于 PRD 和 roadmap 评审）
- **Frameworks**：PRD 形态、UX 校验、市场调研、架构一致性
- **Templates**：带 `[NEEDS CLARIFICATION: …]` 标记，阻止弱规格过 gate
- **单 PRD artifact 形态**：requirements 直接写进 PRD，不再额外维护一份并行的 per-feature `requirements.md`

权威细节在每个 skill 的 `SKILL.md` 及其引用的 framework 文件里。
