# hermes-ecc-profile（中文）

[English README](./README.md)

这是一个面向 Hermes 的 skill-first 编码 profile，包含：

- 本地工作流/门禁 skills（`woos-*`）
- 导入 skills（`skills/ecc-import/*`）
- agent 适配 skills（`skills/ecc-agent-skills/*`）

## 愿景与设计亮点

- **无人值守交付是长期愿景**：通过角色化 agent 分工 + 硬门禁，让更多需求在最少人工介入下稳定推进。
- **设计原则是核心亮点**：它不是单纯的技能打包，而是把角色分离、可确定的 gate 流转、从意图/设计到实现的可追溯评审固化为默认工作方式。
- **基线优先治理**：默认采用主流、可维护、可演进的工程基线；偏离必须提供 ADR 与明确审批。

## 工作流分层（Lite / Standard / Strict）

为了避免小任务被全流程拖慢，工作流支持三档执行：

1. **Lite**：`Run Orchestrator -> Git Workflow -> Requirement Contract -> Implement -> Verify -> Code/Security Review -> PR Readiness`
2. **Standard（默认）**：在 Lite 基础上增加 PRD/设计评审与 workflow memory（同样从 `Run Orchestrator` 开始）
3. **Strict**：完整硬门禁流程（含 research/capability/TDD/acceptance/deviation，以及条件性 API/Browser QA；同样从 `Run Orchestrator` 开始）

## 安装内容

1. 本地 workflow skills：
   - `woos-development-workflow`
   - `woos-requirement-contract`
   - `woos-prd-authoring`
   - `woos-prd-review-gate`
   - `woos-feature-design`
   - `woos-design-review-gate`
   - `woos-executable-acceptance-gate`
   - `woos-failure-state-machine`
   - `woos-deviation-control-gate`
   - `woos-run-orchestrator`
   - `woos-human-handoff`
   - `woos-workflow-memory`
   - `woos-review-context`
   - `woos-agent-decision`
   - `woos-code-review-gate`
   - `woos-pr-readiness`
   - `woos-setup-rules`
2. 导入 skills：
   - `git-workflow`
   - `search-first` / `deep-research`（按需升级）
   - `dmux-workflows`
   - `product-capability`
   - `tdd-workflow`
   - `coding-standards`
   - `verification-loop`
   - `api-design`（REST/GraphQL 设计校验）
   - `browser-qa`（前端浏览器测试）
3. agent 适配 skills：
   - `planner`
   - `architect`
   - `code-reviewer`
   - `security-reviewer`

## 安装

```bash
cd /path/to/hermes-ecc-profile
python3 install-profile.py
```

脚本会提示输入本地 ECC 仓库路径。

可选参数：

```bash
python3 install-profile.py --ecc-path /path/to/ecc --profile-root ~/.hermes/profiles/coding --install-soul
```

备份参数：

```bash
# 指定备份目录
python3 install-profile.py --backup-dir ~/.hermes/profiles/coding.backup.manual

# 跳过备份（不推荐）
python3 install-profile.py --no-backup
```

MCP 同步参数：

```bash
# 同步推荐 MCP 配置到 <profile>/config.yaml（交互默认是）
python3 install-profile.py --sync-mcp

# 跳过 MCP 同步
python3 install-profile.py --no-sync-mcp
```

Rules 同步参数：

```bash
# 同步 ECC rule 分组到 <profile>/rules/ecc-import
python3 install-profile.py --sync-rules

# 跳过 rules 同步
python3 install-profile.py --no-sync-rules
```

`./install-profile.sh` 仍保留为 `python3 install-profile.py` 的薄封装入口。

默认安装目录（`~/.hermes/profiles/coding`）：

- `skills/software-development/*`（本地 workflow skills）
- `skills/ecc-import/*`（导入 skills）
- `skills/ecc-agent-skills/*`（agent 适配 skills）
- `SOUL.md`（仅 `--install-soul` 时安装）

默认情况下，如果目标 profile root 已存在且非空，安装脚本会先创建带时间戳的备份，再执行覆盖安装。

## MCP 同步行为

启用后，安装脚本会从 ECC 的 `mcp-configs/mcp-servers.json` 同步以下 MCP server 配置到 `<profile>/config.yaml` 的 `mcp_servers`：

- `github`
- `context7`
- `exa-web-search`
- `firecrawl`
- `playwright`

如果 profile 里已存在同名 `mcp_servers.<name>`，会保留原配置，不覆盖。


## 升级流程（ECC 更新后）

agent 适配 skills 中包含源追踪字段：

- `ecc_source_repo`
- `ecc_source_path`
- `ecc_source_commit`

当 ECC 升级后，对比这些 commit 与 ECC 当前历史；若有变化，重新做一次 adapter 转换。

## Hermes 中的 rules 同步与路由

安装脚本可将 ECC 全量 rules 同步到：

- `<profile>/rules/ecc-import/*`

默认会排除（避免与本 profile 工作流冲突）：

- `common/development-workflow.md`
- `common/agents.md`
- `common/hooks.md`
- `README.md`
- `zh/README.md`
- `zh/*.md`（中文翻译规则包不做 profile 同步）
- `*/hooks.md`（与 hooks 机制强绑定的规则默认不同步）

Hermes 的规则路由建议放在项目上下文文件中：

- `.hermes.md` / `HERMES.md`（推荐）
- `AGENTS.md`
- `.cursorrules` 或 `.cursor/rules/*.mdc`

为了更好的跨工具兼容性，`woos-setup-rules` 默认会生成/更新项目 `AGENTS.md` 的多语言规则路由。

## 近无人值守执行基础

当前 profile 已内置 7 个关键基础能力：

1. `woos-requirement-contract`：结构化需求输入契约
2. `woos-executable-acceptance-gate`：可执行完成定义与自动验收
3. `woos-failure-state-machine`：失败后的重试/降级/升级状态机
4. `woos-deviation-control-gate`：实现与规格偏离拦截
5. `woos-workflow-memory`：失败与返工模式沉淀
6. `woos-run-orchestrator`：运行编排（队列/并发/超时/重试）
7. `woos-human-handoff`：人工接管与恢复协议

## Agent 协作加固

为减少长时间评审循环，新增两项协作控制能力：

1. `woos-review-context`：跨 gate 的共享评审上下文（已解决/待继承问题）
2. `woos-agent-decision`：reviewer 结论冲突时的确定性决策机制

## ADR 治理要求

- ADR 模板：`docs/adr/ADR-template.md`
- 设计/代码评审 gate 必须输出并校验：
  - `baseline_compliance_status`
  - `deviation_detected`
  - `deviation_adr_path` 与 `approval_ref`（存在偏离时必填）
  - `unconfirmed_constraints_frozen=false`
- 运行结束前必须通过 run manifest 校验：
  - `<workspace_root>/hep/runs/<run_id>/run-manifest.yaml`
- `runs/` 与 `review-context/` 目录由 orchestrator 在运行启动时按需创建，不要求预先存在。
