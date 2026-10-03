"""Load and validate the canonical knowledge items; no research is inferred here."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

import yaml

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "research/knowledge"
BEGIN = "<!-- BEGIN GENERATED SOLUTION STATUS -->"
END = "<!-- END GENERATED SOLUTION STATUS -->"


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_items(root=ROOT):
    items, errors = [], []
    for path in sorted((root / "research/knowledge/items").glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8-sig")
            match = re.fullmatch(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", text, re.S)
            if not match:
                raise ValueError("missing front matter")
            item = yaml.load(match[1], Loader=UniqueLoader)
            if not isinstance(item, dict):
                raise ValueError("front matter must be a mapping")
            item = dict(item, _path=path.relative_to(root).as_posix(), _body=match[2])
            items.append(item)
        except (ValueError, yaml.YAMLError, OSError, TypeError) as exc:
            errors.append(f"{path.name}: {exc}")
    if not items:
        errors.append("no knowledge items")
    return items, errors


def graph_cycles(items, relation):
    graph = {i["id"]: [r["target"] for r in i["relations"] if r["type"] == relation]
             for i in items}
    state, stack, cycles = {}, [], []

    def visit(node):
        state[node] = 1
        stack.append(node)
        for child in graph.get(node, []):
            if child == node:
                continue  # separate self-reference diagnostic
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


def validate(items, root=ROOT):
    vocab = yaml.safe_load((root / "research/knowledge/VOCABULARY.yaml").read_text(encoding="utf-8"))
    errors, warnings = [], []
    ids, aliases, incoming = set(), {}, Counter()
    allowed = {"id", "title", "kind", "status", "topics", "aliases", "relations", "artifacts",
               "scope", "evidence", "solution", "_path", "_body"}
    required = {"id", "title", "kind", "status", "topics", "aliases", "relations", "artifacts"}

    def error(ident, message):
        errors.append(f"{ident}: {message}")

    for item in items:
        ident = item.get("id", item["_path"])
        if required - item.keys():
            error(ident, f"missing fields: {sorted(required - item.keys())}")
        if item.keys() - allowed:
            error(ident, f"unknown fields: {sorted(item.keys() - allowed)}")
        if not isinstance(ident, str) or not re.fullmatch(r"K[0-9]{4,}", ident):
            error(str(ident), "invalid id")
        elif Path(item["_path"]).stem != ident:
            error(ident, "filename must equal id")
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
                    or PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts):
                error(str(ident), f"invalid artifact path: {path}")
            elif not (root / path).is_file() or not (root / path).resolve().is_relative_to(root.resolve()):
                error(str(ident), f"artifact missing or outside repository: {path}")
            if art.get("role") not in vocab["artifact_roles"]:
                error(str(ident), "unknown artifact role")
            if not isinstance(art.get("note"), str) or not art["note"].strip():
                error(str(ident), "artifact requires a useful note")
            if "commit" in art and not re.fullmatch(r"[0-9a-f]{40}", str(art["commit"])):
                error(str(ident), "commit must be a full SHA")
        solution = item.get("solution")
        if solution is not None:
            fields = {"board", "level", "outcome", "classification", "coverage", "conditions",
                      "verification", "certificate", "independent_check", "note"}
            if not isinstance(solution, dict) or set(solution) != fields:
                error(str(ident), f"solution must have exactly {sorted(fields)}")
            else:
                for field in fields - {"classification", "verification"}:
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
        if not item.get("artifacts") and not item.get("relations") and not item.get("evidence") and not incoming[str(ident)]:
            warnings.append(f"{ident}: isolated item with no evidence/relation/artifact")
    # Incoming edges may occur later in item order, so compute isolation again globally.
    warnings = [w for w in warnings if "isolated item" not in w]
    for item in items:
        if not item.get("artifacts") and not item.get("relations") and not item.get("evidence") and not incoming[str(item.get("id"))]:
            warnings.append(f"{item.get('id')}: isolated item with no evidence/relation/artifact")
        elif not item.get("artifacts") and not item.get("evidence"):
            warnings.append(f"{item.get('id')}: thin evidence (relations alone)")
    if not errors:
        for relation in ("depends_on", "supersedes"):
            for cycle in graph_cycles(items, relation):
                errors.append(f"{relation} cycle: {cycle}")
    return errors, sorted(warnings)


def checked(root=ROOT):
    items, errors = load_items(root)
    validation, warnings = validate(items, root)
    return items, errors + validation, warnings


def md(value):
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def link(item, prefix="../items/"):
    return f"[{item['id']}]({prefix}{item['id']}.md)"


def solution_table(items, prefix="../items/"):
    lines = ["| 盤面・条件 | K項目・状態 | 段階・勝敗 | 分類・範囲 | 検証 | 証明書・独立検査・留保 |",
             "|---|---|---|---|---|---|"]
    for item in items:
        s = item.get("solution")
        if not s:
            continue
        lines.append("| " + " | ".join([
            md(s["board"] + "; " + s["conditions"]),
            link(item, prefix) + " · " + item["status"],
            md(s["level"] + "; " + s["outcome"]),
            md(", ".join(s["classification"]) + "; " + s["coverage"]),
            md(", ".join(s["verification"])),
            md(s["certificate"] + "; " + s["independent_check"] + "; " + s["note"]),
        ]) + " |")
    return "\n".join(lines) + "\n"


def update_readme(text, block):
    """Only the managed region changes; ambiguous delimiters fail closed."""
    newline = "\r\n" if "\r\n" in text else "\n"
    block = block.replace("\r\n", "\n").replace("\n", newline)
    if BEGIN not in text and END not in text:
        return text + ("" if text.endswith("\n") else newline) + newline + BEGIN + newline + block + END + newline
    if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(BEGIN) > text.index(END):
        raise ValueError("README generation markers are missing, repeated, or out of order")
    start = text.index(BEGIN) + len(BEGIN)
    stop = text.index(END)
    return text[:start] + newline + block + text[stop:]


def views(items, warnings):
    output = {}
    output["index.md"] = "# K項目一覧\n\n| ID | 知識 | kind | status | topics |\n|---|---|---|---|---|\n" + "".join(
        f"| {link(i)} | {md(i['title'])} | {i['kind']} | {i['status']} | {', '.join(i['topics'])} |\n" for i in items)
    output["solutions.md"] = "# 解決状況\n\ncoverage・条件・検証境界はlevelと独立に読む。\n\n" + solution_table(items)
    alias_rows = sorted((a, i) for i in items for a in i["aliases"])
    output["aliases.md"] = "# 旧ID逆引き\n\n| alias | 正本 | 現在の知識 |\n|---|---|---|\n" + "".join(
        f"| {md(a)} | {link(i)} | {md(i['title'])} |\n" for a, i in alias_rows)
    artifacts = defaultdict(list)
    for item in items:
        for a in item["artifacts"]:
            artifacts[a["path"]].append((item, a))
    output["artifacts.md"] = "# artifact → K項目\n\n" + "\n".join(
        f"## [{path}](../../../{path})\n\n" + "\n".join(
            f"- {link(i)} ({a['role']}): {a['note']}" for i, a in entries)
        for path, entries in sorted(artifacts.items())) + "\n"
    output["relations.md"] = "# 関係と逆引き\n\n矢印はfront matterで宣言した方向。逆リンクはここだけで生成する。\n\n"
    reverse = defaultdict(list)
    by_id = {i["id"]: i for i in items}
    for item in items:
        for r in item["relations"]:
            reverse[r["target"]].append((item, r))
    for item in items:
        if not item["relations"] and not reverse[item["id"]]:
            continue
        output["relations.md"] += f"## {link(item)} {item['title']}\n\n"
        for r in item["relations"]:
            note = f": {r['note']}" if r.get("note") else ""
            output["relations.md"] += f"- → {r['type']} {link(by_id[r['target']])}{note}\n"
        for origin, r in reverse[item["id"]]:
            note = f": {r['note']}" if r.get("note") else ""
            output["relations.md"] += f"- ← {r['type']} {link(origin)}{note}\n"
        output["relations.md"] += "\n"
    output["relations.md"] = output["relations.md"].rstrip() + "\n"
    output["summary.md"] = f"# 移行集計\n\nK項目: {len(items)} / alias: {len(alias_rows)} / artifactファイル: {len(artifacts)}\n\n"
    for field in ("kind", "status", "topics"):
        counts = Counter(t for i in items for t in (i[field] if field == "topics" else [i[field]]))
        output["summary.md"] += f"## {field}\n\n| 値 | 件数 |\n|---|---:|\n" + "".join(
            f"| {key} | {value} |\n" for key, value in sorted(counts.items())) + "\n"
    output["summary.md"] += "## 未解決・要監査・範囲不明\n\n数学的未解決と監査不足の件数は合算しない。\n\n"
    for i in items:
        if i["status"] in {"open", "conjectured", "needs-review", "scope-unclear"}:
            output["summary.md"] += f"- {link(i)} [{i['status']}] {i['title']}\n"
    output["summary.md"] += "\n## 警告\n\n" + ("\n".join(f"- {w}" for w in warnings) if warnings else "なし。") + "\n"
    return output
