"""Check current filesystem layout and live repository references, not provenance text."""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

LEGACY_DIRECTORIES = ("night-research", "research/verification")
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)")
SOURCE_PATH = re.compile(
    r"(?<![\w/])(?:research/experiments|scripts|cpp|tools|rust|Kyouen)/"
    r"[A-Za-z0-9_./-]+\.(?:py|sh|ps1|cpp|h|hpp|inc|rs|lean)(?![\w.])"
)


def repository_files(root):
    # Include new authored files before staging, but exclude ignored runtime data.
    if (root / ".git").exists():
        output = subprocess.check_output(
            ["git", "ls-files", "-co", "--exclude-standard"], cwd=root, text=True
        )
        return sorted({root / name for name in output.splitlines() if (root / name).is_file()})
    return sorted(p for p in root.rglob("*") if p.is_file())


def frozen_link_targets(root):
    """Recognize exact, hash-bound provenance links without rewriting frozen evidence."""
    manifest = root / "research/knowledge/frozen_links.json"
    if not manifest.exists():
        return {}, []
    targets, errors = {}, []
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate manifest key")
            result[key] = value
        return result
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"), object_pairs_hook=unique)
        if set(data) != {"version", "files"} or data["version"] != 1 or not isinstance(data["files"], dict):
            raise ValueError("invalid manifest format")
        for source, spec in data["files"].items():
            if (not source.startswith("research/experiments/") or not source.endswith(".md")
                    or not isinstance(spec, dict) or set(spec) != {"sha256", "targets"}
                    or not isinstance(spec["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", spec["sha256"])
                    or not isinstance(spec["targets"], dict) or not spec["targets"]):
                raise ValueError("invalid frozen source entry")
            original = (root / source).resolve()
            if (not original.is_relative_to((root / "research/experiments").resolve())
                    or not original.is_file()):
                errors.append(f"{manifest.relative_to(root)}: missing frozen source: {source}")
                continue
            if hashlib.sha256(original.read_bytes()).hexdigest() != spec["sha256"]:
                errors.append(f"{manifest.relative_to(root)}: frozen source hash mismatch: {source}")
                continue
            for retired, current in spec["targets"].items():
                if (not isinstance(current, str) or not retired.startswith("research/knowledge/items/")
                        or not current.startswith("research/knowledge/items/")):
                    raise ValueError("invalid frozen knowledge target")
                old, new = (root / retired).resolve(), (root / current).resolve()
                item_root = (root / "research/knowledge/items").resolve()
                if (not old.is_relative_to(item_root) or not new.is_relative_to(item_root)
                        or not new.is_file()):
                    errors.append(f"{manifest.relative_to(root)}: missing or unsafe frozen target: {current}")
                    continue
                targets[(original, old)] = new
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        errors.append(f"{manifest.relative_to(root)}: invalid frozen link manifest: {exc}")
    return targets, errors


def markdown_errors(path, root, *, skip_solution_block=False, frozen_targets=None):
    errors = []
    text = path.read_text(encoding="utf-8-sig")
    if skip_solution_block:
        # The builder replaces this derived block, then validates the result.
        # Human-authored README links must still be checked before generation.
        text = re.sub(
            r"(?s)<!-- BEGIN GENERATED SOLUTION STATUS -->.*?<!-- END GENERATED SOLUTION STATUS -->",
            "", text,
        )
    # Example snippets are not live hyperlinks.
    text = re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1[^\n]*$", "", text)
    for match in LINK.finditer(text):
        target = match[1].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        local = unquote(parsed.path)
        destination = (root / local.lstrip("/")) if local.startswith("/") else path.parent / local
        inside = destination.resolve().is_relative_to(root.resolve())
        historical = inside and (path.resolve(), destination.resolve()) in (frozen_targets or {})
        if not inside or (not destination.exists() and not historical):
            errors.append(f"{path.relative_to(root).as_posix()}: broken local link: {target}")
    return errors


def layout_errors(root, *, include_generated=True):
    frozen_targets, errors = frozen_link_targets(root)
    for name in LEGACY_DIRECTORIES:
        if (root / name).exists():
            errors.append(f"forbidden legacy filesystem path: {name}")
    for path in repository_files(root):
        relative = path.relative_to(root).as_posix()
        if not include_generated and relative.startswith("research/knowledge/generated/"):
            continue
        if path.suffix == ".md":
            errors.extend(markdown_errors(
                path, root, skip_solution_block=not include_generated and relative == "README.md",
                frozen_targets=frozen_targets
            ))
        # Historical scripts/receipts are sources, not current executable paths.
        if relative.startswith("research/archive/"):
            continue
        if path.suffix == ".py":
            try:
                tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=relative)
            except SyntaxError as exc:
                errors.append(f"{relative}: Python syntax error: {exc}")
                continue
            strings = [n.value for n in ast.walk(tree)
                       if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        elif relative.startswith(".github/workflows/"):
            strings = [path.read_text(encoding="utf-8-sig")]
        else:
            continue
        for text in ([] if "/tests/" in relative or relative.startswith("tests/") else strings):
            for match in SOURCE_PATH.finditer(text):
                if not (root / match[0]).is_file():
                    errors.append(f"{relative}: missing source/runner path: {match[0]}")
        if relative.startswith(".github/workflows/"):
            for match in re.finditer(r"(?m)^\s*working-directory:\s*['\"]?([^\s'\"]+)", strings[0]):
                directory = match[1]
                if "$" not in directory and not (root / directory).is_dir():
                    errors.append(f"{relative}: missing workflow working-directory: {directory}")
    return sorted(set(errors))
