#!/usr/bin/env python3
"""Census v3: PyYAML-free faithful port of check.py (load_items + validate).

Run: python3 census_v3_classE.py <mirror_root>
mirror_root must contain:
  research/knowledge/items/*.md
  research/knowledge/VOCABULARY.yaml
  tree_manifest.txt          (one repo-relative path per line; file oracle)

Output: JSON census on stdout. Exit 0 always (red corpus is a valid census);
exit 1 only on machine failure.
Fail-closed: any parse construct outside the corpus subset is a load error.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

from yamlmin import YamlMinError, parse_frontmatter

FENCE_RE = re.compile(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", re.S)

ROOT = None
TREE = set()

SOLUTION_FIELDS = {"board", "level", "outcome", "classification", "coverage", "conditions",
                   "verification", "certificate", "independent_check", "note"}
ALLOWED = {"id", "title", "kind", "status", "topics", "aliases", "relations", "artifacts",
           "scope", "evidence", "solution", "date", "created", "tags", "_path", "_body"}
REQUIRED = {"id", "title", "kind", "status", "topics", "aliases", "relations", "artifacts"}


def load_vocab(path):
    vocab = {}
    from yamlmin import parse_frontmatter as pf
    text = path.read_text(encoding="utf-8")
    vocab = pf(text)
    return vocab


def graph_cycles(items, relation):
    graph = {i["id"]: [r["target"] for r in i["relations"] if r["type"] == relation]
             for i in items}
    state, stack, cycles = {}, [], []

    def visit(node):
        state[node] = 1
        stack.append(node)
        for child in graph.get(node, []):
            if child == node:
                continue
            if state.get(child) == 1:
                cycles.append(" -> ".join(stack[stack.index(child):] + [child]))
            elif not state.get(child):
                visit(child)
        stack.pop()
        state[node] = 2

    for node in graph:
        if not state.get(node):
            visit(node)
    return cycles


def validate(items, vocab):
    errors, warnings = [], []
    status_by_kind = vocab.get("status_by_kind", {})
    if not isinstance(status_by_kind, dict) or set(status_by_kind) != set(vocab["kinds"]):
        errors.append("VOCABULARY: status_by_kind must cover exactly all kinds")
        status_by_kind = {}
    elif any(not isinstance(values, list) or not values or any(s not in vocab["statuses"] for s in values)
             for values in status_by_kind.values()):
        errors.append("VOCABULARY: status_by_kind must contain nonempty lists of known statuses")
        status_by_kind = {}
    ids, aliases, incoming = set(), {}, Counter()

    def error(ident, message):
        errors.append(f"{ident}: {message}")

    for item in items:
        ident = item.get("id", item["_path"])
        if REQUIRED - item.keys():
            error(ident, f"missing fields: {sorted(REQUIRED - item.keys())}")
        if item.keys() - ALLOWED:
            error(ident, f"unknown fields: {sorted(item.keys() - ALLOWED)}")
        if not isinstance(ident, str) or not re.fullmatch(r"K[0-9]{4,}", ident):
            error(str(ident), "invalid id")
        elif not re.fullmatch(re.escape(ident) + r"(?:-[a-z0-9]+(?:-[a-z0-9]+)*)?", Path(item["_path"]).stem):
            error(ident, "filename must be <id>.md or <id>-<lowercase-slug>.md")
        if str(ident) in ids:
            error(str(ident), "duplicate id")
        ids.add(str(ident))
        for field in ("title", "scope", "evidence"):
            if field in item and (not isinstance(item[field], str) or not item[field].strip()):
                error(str(ident), f"{field} must be a nonempty string")
        if len(item["_body"].strip()) < 60:
            warnings.append(f"{ident}: short knowledge body")
        for field, values in (("kind", "kinds"), ("status", "statuses")):
            if item.get(field) not in vocab[values]:
                error(str(ident), f"invalid {field}: {item.get(field)}")
        kind = item.get("kind")
        if isinstance(kind, str) and kind in status_by_kind and item.get("status") not in status_by_kind[kind]:
            error(str(ident), f"status {item.get('status')} is not allowed for kind {kind}")
        for field in ("topics", "aliases", "relations", "artifacts"):
            if not isinstance(item.get(field), list):
                error(str(ident), f"{field} must be a list")
        for topic in item.get("topics", []) if isinstance(item.get("topics"), list) else []:
            if topic not in vocab["topics"]:
                error(str(ident), f"unknown topic: {topic}")
        if not item.get("topics"):
            error(str(ident), "at least one topic required")
        for alias in item.get("aliases", []) if isinstance(item.get("aliases"), list) else []:
            if not isinstance(alias, str) or not alias.strip():
                error(str(ident), "alias must be a nonempty string")
                continue
            if re.fullmatch(r"K[0-9]{4,}", alias):
                error(str(ident), "alias must not impersonate a K id")
            if alias in aliases:
                error(str(ident), f"duplicate alias {alias} (also {aliases[alias]})")
            aliases[alias] = ident
        for art in item.get("artifacts", []) if isinstance(item.get("artifacts"), list) else []:
            if not isinstance(art, dict):
                error(str(ident), "artifact must be a mapping")
                continue
            if set(art) - {"path", "role", "note", "commit", "anchor"}:
                error(str(ident), "unknown artifact field")
            path = art.get("path", "")
            if (not isinstance(path, str) or not path or "\\" in path or ":" in path
                    or path.startswith("/") or ".." in path.split("/")):
                error(str(ident), f"invalid artifact path: {path}")
            elif path not in TREE:
                error(str(ident), f"artifact missing or outside repository: {path}")
            if art.get("role") not in vocab["artifact_roles"]:
                error(str(ident), "unknown artifact role")
            if not isinstance(art.get("note"), str) or not art["note"].strip():
                error(str(ident), "artifact requires a useful note")
            if "commit" in art and not re.fullmatch(r"[0-9a-f]{40}", str(art["commit"])):
                error(str(ident), "commit must be a full SHA")
        solution = item.get("solution")
        if solution is not None:
            if not isinstance(solution, dict) or set(solution) != SOLUTION_FIELDS:
                error(str(ident), f"solution must have exactly {sorted(SOLUTION_FIELDS)}")
            else:
                for field in SOLUTION_FIELDS - {"classification", "verification"}:
                    if not isinstance(solution[field], str) or not solution[field].strip():
                        error(str(ident), f"solution.{field} must be nonempty text")
                for field, enum in (("level", "solution_levels"), ("outcome", "outcomes")):
                    if solution[field] not in vocab[enum]:
                        error(str(ident), f"unknown solution.{field}")
                for field, enum in (("classification", "classifications"), ("verification", "verification_methods")):
                    if not isinstance(solution[field], list) or any(v not in vocab[enum] for v in solution[field]):
                        error(str(ident), f"invalid solution.{field}")
                classification = solution["classification"]
                all_safe = isinstance(classification, list) and any(
                    isinstance(value, str) and value in {"all-safe-win-loss", "all-safe-grundy"}
                    for value in classification)
                if solution["level"] == "strong" and not all_safe:
                    error(str(ident), "strong solution requires all-safe classification")
                if solution["outcome"] == "unknown" and solution["level"] != "unsolved":
                    error(str(ident), "unknown outcome must remain unsolved")
    for item in items:
        ident = item.get("id", item["_path"])
        for rel in item.get("relations", []) if isinstance(item.get("relations"), list) else []:
            if not isinstance(rel, dict) or set(rel) - {"type", "target", "note"}:
                error(str(ident), "invalid relation mapping")
                continue
            if rel.get("type") not in vocab["relations"]:
                error(str(ident), f"unknown relation type: {rel.get('type')}")
            target = rel.get("target")
            if not isinstance(target, str) or target not in ids:
                error(str(ident), f"unknown relation target: {target}")
            else:
                incoming[target] += 1
            if target == ident and rel.get("type") in {"depends_on", "supersedes"}:
                error(str(ident), f"{rel['type']} self-reference")
    for item in items:
        if not item.get("artifacts") and not item.get("relations") and not item.get("evidence") \
                and not incoming[str(item.get("id"))]:
            warnings.append(f"{item.get('id')}: isolated item with no evidence/relation/artifact")
        elif not item.get("artifacts") and not item.get("evidence"):
            warnings.append(f"{item.get('id')}: thin evidence (relations alone)")
    if not errors:
        for relation in ("depends_on", "supersedes"):
            for cycle in graph_cycles(items, relation):
                errors.append(f"{relation} cycle: {cycle}")
    return errors, sorted(warnings)


def main():
    root = Path(sys.argv[1])
    items, errors = [], []
    global TREE
    for ln in (root / "tree_manifest.txt").read_text(encoding="utf-8").splitlines():
        if ln.strip():
            p = ln.strip()
            if p.startswith("./"):
                p = p[2:]
            TREE.add(p)
    vocab = load_vocab(root / "research/knowledge/VOCABULARY.yaml")
    for path in sorted((root / "research/knowledge/items").glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8-sig")
            match = FENCE_RE.fullmatch(text)
            if not match:
                raise ValueError("missing front matter")
            item = parse_frontmatter(match[1])
            item = dict(item, _path=(path.relative_to(root).as_posix()), _body=match[2])
            items.append(item)
        except (ValueError, YamlMinError) as exc:
            errors.append(f"{path.name}: {exc}")
    validation, warnings = validate([dict(i) for i in items], vocab)
    census = {
        "machine": "census_v3 (yamlmin + faithful validate port)",
        "n_files": len(list((root / "research/knowledge/items").glob("*.md"))),
        "n_loaded": len(items),
        "load_errors": errors,
        "validate_errors": validation,
        "warnings": warnings,
    }
    print(json.dumps(census, ensure_ascii=False, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
