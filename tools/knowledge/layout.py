"""Check current filesystem layout and live repository references, not provenance text."""
from __future__ import annotations

import ast
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


def markdown_errors(path, root):
    errors = []
    text = path.read_text(encoding="utf-8-sig")
    # Example snippets are not live hyperlinks.
    text = re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1[^\n]*$", "", text)
    for match in LINK.finditer(text):
        target = match[1].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        local = unquote(parsed.path)
        destination = (root / local.lstrip("/")) if local.startswith("/") else path.parent / local
        if not destination.resolve().is_relative_to(root.resolve()) or not destination.exists():
            errors.append(f"{path.relative_to(root).as_posix()}: broken local link: {target}")
    return errors


def layout_errors(root, *, include_generated=True):
    errors = []
    for name in LEGACY_DIRECTORIES:
        if (root / name).exists():
            errors.append(f"forbidden legacy filesystem path: {name}")
    for path in repository_files(root):
        relative = path.relative_to(root).as_posix()
        if not include_generated and relative.startswith("research/knowledge/generated/"):
            continue
        if path.suffix == ".md":
            errors.extend(markdown_errors(path, root))
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
