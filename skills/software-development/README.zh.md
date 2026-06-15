# 软件开发工作流

[English](./README.md) | [中文](./README.zh.md)

流水线的工程侧。把产品设计阶段的 artifact（PRD + roadmap + architecture）经过 gated TDD 和评审，变成一个可合并的、production-ready 的 PR。

入口 skill：**`woos-development-workflow`**。

## Quick Start

1. 确认产品输入齐全：PRD、roadmap、architecture。少任意一个 = `BLOCKED`。
2. 让 agent 进入 `woos-development-workflow`。
3. 模式根据 PRD 范围与风险自动选（Lite 或 Standard）。每个 gate 必须 PASS 才能进下一个。

## 流水线

```
产品输入（PRD + roadmap + architecture）
   │
   ▼  Bootstrap   woos-run-orchestrator → git-workflow
   ▼  Gate 0      Product Intake——校验输入、写入 run-manifest
   ▼  Gate 1      Feature Plan（架构 + 故事表）            woos-feature-plan
   ▼  Gate 1R     Plan Review（fresh context，双评审）     woos-plan-review-gate
   ▼  Gate 2      Task Loop（story 间按 `Depends` 排序，同 story 内 task 按声明顺序）
   │              ├─ 2.1 TDD             tdd-workflow
   │              ├─ 2.2 Implement       coding-standards
   │              └─ 2.3 Verify          verification-loop
   ▼  Gate 3      Review（代码 + 安全 + AC 覆盖 + 范围漂移）  woos-code-review-gate
   ▼  Gate 4      Ship（追溯矩阵 + PR Readiness）              woos-pr-readiness
   ▼  Post        Workflow Memory                  woos-workflow-memory
   ▼
PR 创建完成 ✅

遇到无法解决的设计问题 → DCR → docs/feedback/<version>/<feature-id>-dcr-<NNN>.md
```

## 执行模式

| 模式 | 何时 | 跳过的 gate |
|------|------|-------------|
| Lite | 低风险、单点小改、不动架构 | Gate 1、1R；Gate 3 仍跑但跳过 AC 覆盖 / 范围漂移检查；Gate 4 跳过追溯矩阵生成 |
| Standard（默认） | 来自产品设计流水线的任何 feature | 无 |

模式由 PRD 范围与风险决定，不是开发者选。

## 逐 Gate 说明

| Gate | Skill | 产物 |
|------|-------|------|
| 0 Product Intake | （内置） | 校验 PRD + roadmap + architecture；路径写入 `run-manifest.yaml`。首次跑这个 repo：触发 `codebase-onboarding`。 |
| 1 Feature Plan | `woos-feature-plan`（内部调度 `woos-architect` `mode: author` + `woos-product-planner` `mode: planning`） | 单个 per-feature `docs/engineering/<version>/<feature-id>-plan.md`：包含 Architecture / Test Strategy / Rollout & Rollback / Security & Risk / Baseline & Deviation / **Stories**（敏捷 `As a / I want / so that` + AC 列表 + commit 粒度 Tasks，每个 task 有具体 `Diff Scope`）。Interface/API 契约与 data model 由 PRD 的 `<feature-id>-interface.md` 持有，这里不重复。 |
| 1R Plan Review | `woos-plan-review-gate`（调度 `woos-architect` `mode: review` + `woos-product-planner` `mode: story-review`） | 一轮 review 同时覆盖架构决策与 stories/tasks 拆分，fresh context 双评审；`PASS` / `REQUEST_CHANGES`。连续 2 轮失败 → `woos-human-handoff`。 |
| 2 Task Loop | `tdd-workflow`、`coding-standards`、`verification-loop` | 按 DAG 顺序逐 task 执行（story 间按 `Depends` 排序，同 story 内 task 按声明顺序）：RED→GREEN→REFACTOR → 实现 → 验证。条件触发：`database-migrations`、`e2e-testing`、`browser-qa`。被 block 的 task 不阻塞独立 task/story。 |
| 3 Review | `woos-code-review-gate` → `woos-code-reviewer`（命中触发条件时加 `woos-security-reviewer`、适用时加 `woos-production-audit`） | Fresh context + 知识注入（E1）。一次过的硬性检查：代码 / 安全 findings（结构化表 E2）、**AC 覆盖**（每条 PRD AC 在其所属 story 下都有通过的测试）、**范围漂移**（diff 内每个文件都在某个 task 的 Diff Scope 里）、baseline / deviation 对齐。 |
| 4 Ship | `woos-pr-readiness` + `git-workflow` | 再跑一次 `verification-loop` 作为兜底，机械地从 Plan 的 Stories/Tasks + 最后一次测试结果生成 `docs/traceability/<version>/<feature-id>-traceability.md`，附到 PR body，然后 `gh pr create`。 |
| Post Workflow Memory | `woos-workflow-memory` | 持久化失败/返工模式与 plan 质量信号，供下次运行参考。 |
| Post Workflow Memory | `woos-workflow-memory` | 持久化失败/返工模式与 plan 质量信号，供下次运行参考。 |

## Stories & Tasks（嵌在 Gate 1 的 Plan 文档里）

Gate 1 把 stories/tasks section 嵌在 `docs/engineering/<version>/<feature-id>-plan.md` 里。**Story** 是一条用户可感知价值的垂直切片（敏捷 INVEST）；**Task** 是 story 下的 commit 粒度实现单元：

```markdown
### S1 — 会话在重启后恢复
**As a** 重新登录的运维人员, **I want** 我的会话在服务重启后被恢复, **so that** 我不丢失上下文.
- **AC**: FR-1.a, FR-1.b
- **Tasks**:
  | Task | Diff Scope | Notes |
  |------|------------|-------|
  | t1: 落盘 session | store/persist.go, store/persist_test.go | TDD；覆盖 FR-1.a |
  | t2: 启动时加载 | store/persist.go, store/persist_test.go | 覆盖 FR-1.b |
- **Depends**: -
```

为什么这么写：敏捷 story 给出真实 persona 与价值；PRD AC 是规约；每个 task 的 diff scope 内的测试是验证；`git restore -- <diff_scope>` 是 per-task 回滚。Story / task 的状态与失败日志属于运行时状态，存在 `run-manifest.yaml` 里。Sizing：story 按 INVEST（用户价值、单 review-round），task 按 commit 原子性 —— 不按 AC 数封顶。不存在依赖关系的两个 story 下的 task 不能共享文件。权威 schema 见 `woos-feature-plan/SKILL.md`。

## 强制规则

从生产 agent 失败中学到的 3 条不可妥协：

- **E1 知识注入** —— 调度评审子 agent 前，orchestrator 必须把相关 skill 的全文注入。只给一个角色名（"你是 code reviewer"）会出敷衍结果。
- **E2 结构化评审输出** —— 每个评审 gate 必须输出 findings 表（severity、category、finding、location、recommendation）+ verdict + 证据。裸 "PASS" 或 "LGTM" 无效，必须重跑。
- **E3 条件 skill 激活** —— 条件 skill（`browser-qa`、`e2e-testing`、`database-migrations`、`security-review` 等）有明确触发规则。命中即强制激活，不许"看情况"。

## Skill 一览

**本地（`woos-*`）：**
`woos-development-workflow`（入口）、`woos-feature-plan`、`woos-plan-review-gate`、`woos-code-review-gate`、`woos-pr-readiness`、`woos-workflow-memory`、`woos-run-orchestrator`、`woos-failure-state-machine`、`woos-human-handoff`、`woos-review-context`、`woos-systematic-debugging`、`woos-architect`、`woos-product-planner`、`woos-code-reviewer`、`woos-security-reviewer`、`woos-production-audit`。

**导入（`skills/ecc/`）：**
`git-workflow`、`tdd-workflow`、`coding-standards`、`verification-loop`、`api-design`、`browser-qa`、`e2e-testing`、`security-review`、`architecture-decision-records`、`database-migrations`、`deployment-patterns`、`codebase-onboarding`。

## DCR（Design Change Request）

当工程遇到 scope 内无法解决的设计问题：

1. 写 `docs/feedback/<version>/<feature-id>-dcr-<NNN>.md`（问题、影响、建议修复、优先级）。`NNN` 从 `001` 开始零填充；绝不覆盖——总是分配下一个空号。
2. 停止受影响的 story / task。继续不受影响的部分。
3. 产品流水线读 DCR、更新 PRD、重新下发。工程从受影响 gate 续跑。

## 文件布局

```
<project-root>/
├── .ratchet/
│   ├── runs/<run_id>/run-manifest.yaml      ← gate 进度 + 运行时 story/task 状态
│   └── review-context/<run_id>.yaml         ← 跨 gate 累积发现
└── docs/
    ├── product/<project>-roadmap.md         ← 输入
    ├── product/<project>-architecture.md    ← 输入
    ├── prd/<version>/<feature-id>.md        ← 输入
    ├── prd/<version>/<feature-id>-interface.md     ← 可选（Strict）
    ├── design/<version>/<feature-id>-ui-brief.md   ← 可选（涉及 UI）
    ├── engineering/<version>/<feature-id>-plan.md  ← Gate 1（含 Stories & Tasks）
    ├── adr/                                  ← ADR 记录
    ├── feedback/<version>/<feature-id>-dcr-<NNN>.md  ← DCR
    └── traceability/<version>/<feature-id>-traceability.md  ← Gate 4（自动生成）
```
