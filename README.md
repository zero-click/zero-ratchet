# hermes-ecc-profile

[中文说明 / Chinese README](./README.zh-CN.md)

Skill-first coding profile for Hermes, with:

- local workflow/gate skills (`woos-*`)
- imported ECC skills (`skills/ecc-import/*`)
- agent-adapter skills (`skills/ecc-agent-skills/*`)

## Vision and design highlights

- **Unattended delivery is the long-term vision**: use role-specialized agents and hard gates so more work can run reliably with minimal human intervention.
- **Design principles are the core differentiator**: this profile is not just a skill bundle. It enforces role separation, deterministic gate progression, and traceable review from intent/design to final implementation.

## What this profile installs

1. Local workflow skills:
    - `woos-development-workflow`
    - `woos-prd-authoring`
    - `woos-prd-review-gate`
    - `woos-feature-design`
    - `woos-design-review-gate`
    - `woos-code-review-gate`
    - `woos-pr-readiness`
    - `woos-setup-rules`
2. Imported skills:
   - `git-workflow`
   - `search-first`
   - `dmux-workflows`
   - `product-capability`
   - `tdd-workflow`
   - `coding-standards`
   - `verification-loop`
3. Agent-adapter skills:
   - `planner`
   - `architect`
   - `code-reviewer`
   - `security-reviewer`

## Install

```bash
cd /path/to/hermes-ecc-profile
python3 install-profile.py
```

The installer will prompt for local ECC repo path.

Optional:

```bash
python3 install-profile.py --ecc-path /path/to/ecc --profile-root ~/.hermes/profiles/coding --install-soul
```

Backup options:

```bash
# custom backup path
python3 install-profile.py --backup-dir ~/.hermes/profiles/coding.backup.manual

# skip backup (not recommended)
python3 install-profile.py --no-backup
```

MCP sync options:

```bash
# sync recommended MCP servers into <profile>/config.yaml (default interactive: yes)
python3 install-profile.py --sync-mcp

# skip MCP sync
python3 install-profile.py --no-sync-mcp
```

Rules sync options:

```bash
# sync ECC rule groups into <profile>/rules/ecc-import
python3 install-profile.py --sync-rules

# skip rules sync
python3 install-profile.py --no-sync-rules
```

`./install-profile.sh` remains as a thin wrapper to `python3 install-profile.py`.

Installed layout (default profile root: `~/.hermes/profiles/coding`):

- `skills/software-development/*` (local workflow skills)
- `skills/ecc-import/*` (imported ECC skills)
- `skills/ecc-agent-skills/*` (agent adapters)
- `SOUL.md` (only if `--install-soul`)

By default, if the target profile root already exists and is non-empty, the installer creates a timestamped backup before applying changes.

## MCP sync behavior

When enabled, installer syncs these MCP server configs from ECC `mcp-configs/mcp-servers.json` into `<profile>/config.yaml` under `mcp_servers`:

- `github`
- `context7`
- `exa-web-search`
- `firecrawl`
- `playwright`

Existing `mcp_servers.<name>` entries in profile config are preserved (not overwritten).

## Upgrade flow (ECC changes)

Agent-adapter skills include source tracking fields:

- `ecc_source_repo`
- `ecc_source_path`
- `ecc_source_commit`

When ECC updates, compare the source commit in each adapter skill with current ECC git history. If changed, re-run adapter conversion.

## Rules sync + routing in Hermes

Installer can sync all ECC rule groups into:

- `<profile>/rules/ecc-import/*`

Default exclusion (to avoid workflow conflict with this profile):

- `common/development-workflow.md`
- `common/agents.md`
- `common/hooks.md`
- `README.md`
- `zh/README.md`
- `zh/*.md` (translation pack excluded)
- `*/hooks.md` (hook-oriented rules excluded for Hermes profile sync)

Hermes rule routing should be defined at project level via context files:

- `.hermes.md` / `HERMES.md` (preferred)
- `AGENTS.md`
- `.cursorrules` or `.cursor/rules/*.mdc`

For better cross-tool compatibility, `woos-setup-rules` generates/updates `AGENTS.md` by default with language-aware rule routing.
