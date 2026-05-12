#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import fnmatch
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


LOCAL_PROFILE_SKILLS = [
    "woos-development-workflow",
    "woos-prd-authoring",
    "woos-prd-review-gate",
    "woos-feature-design",
    "woos-design-review-gate",
    "woos-requirement-contract",
    "woos-executable-acceptance-gate",
    "woos-failure-state-machine",
    "woos-deviation-control-gate",
    "woos-run-orchestrator",
    "woos-human-handoff",
    "woos-workflow-memory",
    "woos-code-review-gate",
    "woos-pr-readiness",
    "woos-setup-rules",
]

ECC_AGENT_ADAPTER_SKILLS = [
    "planner",
    "architect",
    "code-reviewer",
    "security-reviewer",
]

ECC_SKILLS = [
    "git-workflow",
    "search-first",
    "deep-research",
    "dmux-workflows",
    "product-capability",
    "tdd-workflow",
    "coding-standards",
    "verification-loop",
    "api-design",
    "browser-qa",
]

MCP_SERVERS = [
    "github",
    "context7",
    "exa-web-search",
    "firecrawl",
    "playwright",
]

RULES_EXCLUDE_RELATIVE_PATHS = [
    "common/development-workflow.md",
    "common/agents.md",
    "common/hooks.md",
    "README.md",
    "zh/README.md",
]

RULES_EXCLUDE_GLOBS = [
    "zh/*.md",
    "*/hooks.md",
]


def style(text: str, code: str) -> str:
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text


def print_header() -> None:
    print()
    print(style("Hermes ECC Profile Installer", "1;36"))
    print(style("-" * 32, "36"))
    print("Interactive setup mode (press Enter to accept defaults).")


def print_step(label: str) -> None:
    print()
    print(style(label, "1"))


def prompt_text(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        print("Please enter a value.")


def validate_ecc_path(ecc_path: Path) -> str | None:
    if not ecc_path.is_dir():
        return f"Path does not exist: {ecc_path}"
    if not (ecc_path / "skills").is_dir():
        return f"Missing skills/: {ecc_path}"
    if not (ecc_path / "mcp-configs" / "mcp-servers.json").is_file():
        return f"Missing mcp-configs/mcp-servers.json: {ecc_path}"
    if not (ecc_path / "rules").is_dir():
        return f"Missing rules/: {ecc_path}"
    return None


def fail(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def prompt_yes_no(question: str, default_yes: bool = True) -> bool:
    suffix = "[Y/n]" if default_yes else "[y/N]"
    default = "y" if default_yes else "n"
    while True:
        reply = input(f"{question} {suffix} ").strip().lower() or default
        if reply in {"y", "yes"}:
            return True
        if reply in {"n", "no"}:
            return False
        print("Please answer y or n.")


def copy_dir(src: Path, dst: Path) -> None:
    if not src.is_dir():
        fail(f"Missing skill directory: {src}")
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def ensure_backup(profile_root: Path, backup_enabled: bool, backup_dir: Path | None) -> Path | None:
    if not profile_root.exists() or not profile_root.is_dir():
        return None
    if not any(profile_root.iterdir()):
        return None
    if not backup_enabled:
        return None

    if backup_dir is None:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = Path(f"{str(profile_root).rstrip('/')}.backup.{ts}")
    if backup_dir.exists():
        fail(f"Backup path already exists: {backup_dir}")
    backup_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(profile_root, backup_dir)
    print(f"  ✓ profile backup created: {backup_dir}")
    return backup_dir


def load_yaml(path: Path) -> dict[str, Any]:
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            fail(f"profile config is not a YAML mapping: {path}")
        return data
    return {}


def save_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def sync_profile_mcp_config(profile_root: Path, ecc_path: Path) -> None:
    profile_cfg_path = profile_root / "config.yaml"
    ecc_mcp_json_path = ecc_path / "mcp-configs" / "mcp-servers.json"
    if not ecc_mcp_json_path.is_file():
        fail(f"Missing ECC MCP config: {ecc_mcp_json_path}")

    data = load_yaml(profile_cfg_path)
    source = json.loads(ecc_mcp_json_path.read_text(encoding="utf-8"))
    source_servers = source.get("mcpServers", {})
    if not isinstance(source_servers, dict):
        fail(f"Invalid mcpServers in {ecc_mcp_json_path}")

    mcp_servers = data.get("mcp_servers")
    if mcp_servers is None:
        mcp_servers = {}
        data["mcp_servers"] = mcp_servers
    elif not isinstance(mcp_servers, dict):
        fail("existing mcp_servers is not a mapping in profile config")

    added: list[str] = []
    kept: list[str] = []
    missing: list[str] = []

    for name in MCP_SERVERS:
        cfg = source_servers.get(name)
        if cfg is None:
            missing.append(name)
            continue
        if name in mcp_servers:
            kept.append(name)
            continue
        mcp_servers[name] = copy.deepcopy(cfg)
        added.append(name)

    save_yaml(profile_cfg_path, data)
    if added:
        print(f"  ✓ mcp_servers added: {', '.join(added)}")
    if kept:
        print(f"  • mcp_servers kept (already present): {', '.join(kept)}")
    if missing:
        print(f"  ! mcp server defs missing in ECC config: {', '.join(missing)}")


def sync_profile_rules(profile_root: Path, ecc_path: Path) -> None:
    ecc_rules_dir = ecc_path / "rules"
    profile_rules_root = profile_root / "rules" / "ecc-import"
    if not ecc_rules_dir.is_dir():
        fail(f"Missing ECC rules directory: {ecc_rules_dir}")

    if profile_rules_root.exists():
        shutil.rmtree(profile_rules_root)
    profile_rules_root.mkdir(parents=True, exist_ok=True)

    for rule_group_dir in sorted(ecc_rules_dir.iterdir()):
        if rule_group_dir.is_dir():
            shutil.copytree(rule_group_dir, profile_rules_root / rule_group_dir.name)

    excluded_count = 0
    for rel in RULES_EXCLUDE_RELATIVE_PATHS:
        p = profile_rules_root / rel
        if p.is_file():
            p.unlink()
            excluded_count += 1

    for p in profile_rules_root.rglob("*.md"):
        rel = p.relative_to(profile_rules_root).as_posix()
        for glob_pat in RULES_EXCLUDE_GLOBS:
            if fnmatch.fnmatch(rel, glob_pat):
                p.unlink(missing_ok=True)
                excluded_count += 1
                break

    copied_count = sum(1 for p in profile_rules_root.iterdir() if p.is_dir())
    print(f"  ✓ rules synced: {copied_count} groups -> {profile_rules_root}")
    if excluded_count:
        print(f"  • rules excluded by path: {' '.join(RULES_EXCLUDE_RELATIVE_PATHS)}")
        print(f"  • rules excluded by glob: {' '.join(RULES_EXCLUDE_GLOBS)}")


def install_core_skills(script_dir: Path, profile_root: Path, ecc_path: Path) -> None:
    (profile_root / "skills" / "software-development").mkdir(parents=True, exist_ok=True)
    (profile_root / "skills" / "ecc-import").mkdir(parents=True, exist_ok=True)
    (profile_root / "skills" / "ecc-agent-skills").mkdir(parents=True, exist_ok=True)

    for skill in LOCAL_PROFILE_SKILLS:
        copy_dir(script_dir / "skills" / "software-development" / skill, profile_root / "skills" / "software-development" / skill)
        print(f"  ✓ local skill: {skill}")

    for skill in ECC_SKILLS:
        copy_dir(ecc_path / "skills" / skill, profile_root / "skills" / "ecc-import" / skill)
        print(f"  ✓ imported skill: {skill}")

    for skill in ECC_AGENT_ADAPTER_SKILLS:
        copy_dir(script_dir / "ecc-agent-skills" / skill, profile_root / "skills" / "ecc-agent-skills" / skill)
        print(f"  ✓ agent-adapter skill: {skill}")


def install_profile_soul(script_dir: Path, profile_root: Path) -> None:
    soul_src = script_dir / "SOUL.md"
    if not soul_src.is_file():
        fail("Missing SOUL.md in profile repo")
    shutil.copy2(soul_src, profile_root / "SOUL.md")
    print("  ✓ profile SOUL.md installed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install Hermes ECC profile")
    parser.add_argument("--ecc-path", help="Local ECC repo path")
    parser.add_argument("--profile-root", help="Hermes coding profile root")
    parser.add_argument("--install-soul", action="store_true", help="Install SOUL.md into profile root")
    parser.add_argument("--backup-dir", help="Backup destination path for existing profile root")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup of existing profile root")
    parser.add_argument("--sync-mcp", dest="sync_mcp", action="store_true", help="Sync recommended MCP servers")
    parser.add_argument("--no-sync-mcp", dest="sync_mcp", action="store_false", help="Skip MCP sync")
    parser.add_argument("--sync-rules", dest="sync_rules", action="store_true", help="Sync ECC rules")
    parser.add_argument("--no-sync-rules", dest="sync_rules", action="store_false", help="Skip rules sync")
    parser.set_defaults(sync_mcp=None, sync_rules=None)
    return parser.parse_args()


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    args = parse_args()
    interactive_mode = (
        args.ecc_path is None
        or args.profile_root is None
        or not args.install_soul
        or args.sync_mcp is None
        or args.sync_rules is None
    )

    profile_root_default = Path(
        os.environ.get("HERMES_PROFILE_ROOT", str(Path.home() / ".hermes" / "profiles" / "coding"))
    ).expanduser()
    profile_root = Path(args.profile_root).expanduser() if args.profile_root else profile_root_default

    ecc_path = Path(args.ecc_path).expanduser() if args.ecc_path else None
    install_soul = args.install_soul
    install_soul_set = args.install_soul
    backup_enabled = not args.no_backup
    backup_set = args.no_backup or bool(args.backup_dir)
    backup_dir = Path(args.backup_dir).expanduser() if args.backup_dir else None
    sync_mcp = args.sync_mcp
    sync_rules = args.sync_rules
    backup_done = False
    mcp_synced = False
    rules_synced = False

    if ecc_path is None:
        if interactive_mode:
            print_header()
            print_step("Step 1/5 - ECC repository path")
            print("Needs: skills/, rules/, mcp-configs/mcp-servers.json")
            while True:
                ecc_path = Path(prompt_text("ECC repo path")).expanduser()
                issue = validate_ecc_path(ecc_path)
                if issue is None:
                    print(f"  ✓ ECC path verified: {ecc_path}")
                    break
                print(f"  ! {issue}")
        else:
            ecc_path = Path(prompt_text("ECC repo path")).expanduser()
    else:
        issue = validate_ecc_path(ecc_path)
        if issue is not None:
            fail(f"Invalid ECC path: {issue}")

    if not args.profile_root:
        if interactive_mode:
            print_step("Step 2/5 - Profile target + core skills")
        profile_root_input = prompt_text("Profile root", str(profile_root_default))
        profile_root = Path(profile_root_input).expanduser()

    if not backup_set and profile_root.is_dir() and any(profile_root.iterdir()):
        backup_enabled = prompt_yes_no("Backup existing profile root before install?", True)
        if backup_enabled:
            backup_dir = ensure_backup(profile_root, True, backup_dir)
            backup_done = True

    if not backup_done:
        backup_dir = ensure_backup(profile_root, backup_enabled, backup_dir)

    if interactive_mode:
        print(f"Target profile: {profile_root}")
        print("Applying core skill installation now...")
    install_core_skills(script_dir, profile_root, ecc_path)

    if not install_soul_set:
        if interactive_mode:
            print_step("Step 3/5 - SOUL.md")
        install_soul = prompt_yes_no("Install SOUL.md into profile root?", True)
    if install_soul:
        install_profile_soul(script_dir, profile_root)

    if sync_mcp is None:
        if interactive_mode:
            print_step("Step 4/5 - MCP sync")
        sync_mcp = prompt_yes_no("Sync recommended MCP servers into profile config.yaml?", True)
    if sync_mcp:
        sync_profile_mcp_config(profile_root, ecc_path)
        mcp_synced = True

    if sync_rules is None:
        if interactive_mode:
            print_step("Step 5/5 - Rules sync")
        sync_rules = prompt_yes_no("Sync ECC rule packs into profile rules/ecc-import?", True)
    if sync_rules:
        sync_profile_rules(profile_root, ecc_path)
        rules_synced = True

    print("\nInstall complete.")
    print(f"Profile root: {profile_root}")
    print(f"ECC path: {ecc_path}")
    if backup_dir is not None and backup_enabled:
        print(f"Backup: {backup_dir}")
    print("MCP sync: enabled (profile config updated)" if mcp_synced else "MCP sync: skipped")
    print("Rules sync: enabled (rules/ecc-import updated)" if rules_synced else "Rules sync: skipped")


if __name__ == "__main__":
    main()
