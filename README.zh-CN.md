# hermes-ecc-profile（中文）

[English README](./README.md)

这是一个面向 Hermes 的 skill-first 编码 profile，包含：

- 本地工作流/门禁 skills（`woos-*`）
- 导入 skills（`skills/ecc-import/*`）
- agent 适配 skills（`skills/ecc-agent-skills/*`）

## 愿景与设计亮点

- **无人值守交付是长期愿景**：通过角色化 agent 分工 + 硬门禁，让更多需求在最少人工介入下稳定推进。
- **设计原则是核心亮点**：它不是单纯的技能打包，而是把角色分离、可确定的 gate 流转、从意图/设计到实现的可追溯评审固化为默认工作方式。

## 安装内容

1. 本地 workflow skills：
   - `woos-development-workflow`
   - `woos-prd-authoring`
   - `woos-prd-review-gate`
   - `woos-feature-design`
   - `woos-design-review-gate`
   - `woos-code-review-gate`
   - `woos-pr-readiness`
   - `woos-setup-rules`
2. 导入 skills：
   - `git-workflow`
   - `search-first`
   - `dmux-workflows`
   - `product-capability`
   - `tdd-workflow`
   - `coding-standards`
   - `verification-loop`
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
