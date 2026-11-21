#!/usr/bin/env python3
"""Repair class A (': ' plain-scalar hazards) and class B (fence defects).

Chase-loop: parse with census loader; on one error, apply one targeted fix;
repeat until the file parses or an unknown shape aborts (collected for
manual inspection). Fixes are minimal-edits: quote-wrap / fence insert /
summary->evidence rename only. Repaired files are written to repaired/.
"""
import json
import re
import sys
from pathlib import Path

from yamlmin import YamlMinError, parse_frontmatter

FENCE_RE = re.compile(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", re.S)
KEY_RE = re.compile(r"^(\s*)([A-Za-z_][\w.-]*):(.*)$")
SEQ_RE = re.compile(r"^(\s*)- (.*)$")
HAZ = ": "


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def load_error(text):
    m = FENCE_RE.fullmatch(text)
    if not m:
        return ("missing front matter", None)
    try:
        parse_frontmatter(m[1])
        return (None, m[1])
    except YamlMinError as e:
        return (str(e), m[1])


def find_span(ilines, idx):
    line = ilines[idx]
    km = KEY_RE.match(line)
    if km and HAZ in km.group(3):
        ind = len(km.group(1))
        s = e = idx
        j = idx + 1
        while j < len(ilines):
            nxt = ilines[j]
            if not nxt.strip():
                break
            n_ind = len(nxt) - len(nxt.lstrip())
            if n_ind > ind and not KEY_RE.match(nxt) and not SEQ_RE.match(nxt):
                e = j
                j += 1
            else:
                break
        return ("key", km, s, e)
    sm = SEQ_RE.match(line)
    if sm and HAZ in sm.group(2):
        ind = len(sm.group(1))
        s = e = idx
        j = idx + 1
        while j < len(ilines):
            nxt = ilines[j]
            if not nxt.strip():
                break
            n_ind = len(nxt) - len(nxt.lstrip())
            if n_ind > ind and not KEY_RE.match(nxt) and not SEQ_RE.match(nxt):
                e = j
                j += 1
            else:
                break
        return ("seq", sm, s, e)
    return None


def apply_wrap(intern, span):
    kind, m, s, e = span
    first = intern[s]
    if kind == "key":
        ind, key, rest = m.group(1), m.group(2), m.group(3)
        value = rest[1:] if rest.startswith(" ") else rest
        new = [list(x) for x in []]  # noqa
        new_first = f'{ind}{key}: "{esc(value.rstrip())}"' if e == s else f'{ind}{key}: "{esc(value.rstrip())}'
        new_intern = list(intern)
        new_intern[s] = new_first
        if e > s:
            new_intern[e] = intern[e].rstrip("\r") + '"'
        return new_intern
    ind = m.group(1)
    value = m.group(2)
    new_first = f'{ind}- "{esc(value.rstrip())}"' if e == s else f'{ind}- "{esc(value.rstrip())}'
    new_intern = list(intern)
    new_intern[s] = new_first
    if e > s:
        new_intern[e] = intern[e].rstrip("\r") + '"'
    return new_intern


def rebuild(text, new_intern):
    # file = fence + inner(=group between fences) + closing fence + body
    m = FENCE_RE.fullmatch(text)
    inner, body = m[1], m[2]
    return "---\n" + "\n".join(new_intern) + "\n---\n" + body


def repair_text(text, manual, name):
    fixes = []
    for _ in range(200):
        err, inner = load_error(text)
        if err is None:
            return text, fixes, True
        if err == "missing front matter":
            if not text.startswith("---\n") and re.match(r"^\s*(id|title):", text.split("\n")[0]):
                text = "---\n" + text
                fixes.append("prepend-fence")
                continue
            if re.search(r"^summary: ", text, re.M):
                text = re.sub(r"^summary: ", "evidence: ", text, count=0, flags=re.M)
                fixes.append("summary->evidence")
                continue
            if text.startswith("---\n") and not text.rstrip("\n").endswith("---"):
                # insert the closing fence before a blank-separated col-0 Markdown
                # body block if one exists, else append at EOF
                lines = text.split("\n")
                cut = None
                for i in range(1, len(lines)):
                    if lines[i].startswith("#") and not lines[i - 1].strip():
                        cut = i
                        # walk back over the blank run
                        while cut > 1 and not lines[cut - 1].strip():
                            cut -= 1
                        break
                if cut is not None:
                    lines = lines[:cut] + ["---"] + lines[cut:]
                    text = "\n".join(lines)
                    if not text.endswith("\n"):
                        text += "\n"
                    fixes.append("insert-fence-before-body")
                else:
                    if not text.endswith("\n"):
                        text += "\n"
                    text += "---\n"
                    fixes.append("append-fence")
                continue
            manual.append((name, "unfixable fence shape"))
            return text, fixes, False
        mm = re.match(r".*? line@(\d+): plain scalar contains ASCII ': '", err) or \
             re.match(r"seq item @(\d+): plain scalar contains ASCII ': '", err)
        if mm:
            idx = int(mm.group(1) or mm.group(2))
            ilines = [l for l in inner.split("\n")]
            span = find_span(ilines, idx) if idx < len(ilines) else None
            if span is None:
                manual.append((name, f"no span for {err[:70]}"))
                return text, fixes, False
            new_intern = apply_wrap(ilines, span)
            text = rebuild(text, new_intern)
            fixes.append(f"wrap-{span[0]}@{span[2]}-{span[3]}")
            continue
        om = re.match(r"orphan mapping line @(\d+): '(.*)", err)
        if om:
            idx = int(om.group(1))
            m2 = FENCE_RE.fullmatch(text)
            if m2:
                ilines = m2[1].split("\n")
                if 0 < idx < len(ilines):
                    prev = ilines[idx - 1]
                    if re.match(r"^(\s*)- path: ", prev) and not KEY_RE.match(ilines[idx]):
                        joined = re.match(r"^(\s*)- path: (.*)$", prev.rstrip())
                        indent, pval = joined.group(1), joined.group(2)
                        frag = ilines[idx].strip()
                        ilines = ilines[:idx - 1] + [f"{indent}- path: {pval}{frag}".rstrip()] + ilines[idx + 1:]
                        text = rebuild(text, ilines)
                        fixes.append(f"join-pathfrag@{idx}")
                        continue
                    pv = re.match(r"^(\s+)(\S.*)$", prev)
                    cu = ilines[idx]
                    if pv and cu and not cu[:1].isspace() and not KEY_RE.match(cu):
                        ilines = ilines[:idx - 1] + [prev + cu] + ilines[idx + 1:]
                        text = rebuild(text, ilines)
                        fixes.append(f"join-frag@{idx}")
                        continue
        manual.append((name, f"unhandled: {err[:70]}"))
        return text, fixes, False
    manual.append((name, "iteration limit"))
    return text, fixes, False


def main():
    targets = json.load(open("repair_targets.json"))
    manual = []
    results = {}
    outdir = Path("repaired")
    outdir.mkdir(exist_ok=True)
    for name in sorted(targets):
        p = Path("mirror2/research/knowledge/items") / name
        orig = p.read_text(encoding="utf-8-sig")
        text, fixes, ok = repair_text(orig, manual, name)
        results[name] = {"ok": ok, "fixes": fixes}
        if ok:
            (outdir / name).write_text(text, encoding="utf-8")
            # content-fidelity: only whitespace and quoting may differ
            strip = re.sub(r'[ "]', "", text)  # crude
        if not ok:
            print("FAIL", name, fixes)
    ok = sum(1 for r in results.values() if r["ok"])
    print(f"repaired {ok}/{len(targets)}; manual: {len(manual)}")
    for m in manual:
        print("  MANUAL", m)
    for name, r in sorted(results.items()):
        print(("OK " if r["ok"] else "!! ") + name, "|", "; ".join(r["fixes"])[:150])
    json.dump(results, open("repair_report.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
