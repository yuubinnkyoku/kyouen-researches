#!/usr/bin/env python3
"""YAML-subset front matter scanner for the kyouen corpus (2026-11-21)."""
import re

_KEY = re.compile(r"([A-Za-z_][A-Za-z0-9_]*):(.*)")


class YamlError(Exception):
    pass


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _is_blank(line):
    return line.strip() == ""


def _is_comment(line):
    return line.lstrip(" ").startswith("#")


def _plain_hazards(value, where, errs):
    if ": " in value:
        errs.append(f"{where}: plain scalar contains ASCII ': '")
    if " #" in value:
        errs.append(f"{where}: plain scalar contains ' #'")


def _strip_comment(raw):
    idx = raw.find(" #")
    return raw[:idx] if idx >= 0 else raw


def _scan_flow(value, where, errs):
    body = value.strip()
    if not (body.startswith("[") and body.endswith("]")):
        raise YamlError(f"{where}: malformed flow collection")
    inner = body[1:-1].strip()
    if not inner:
        return
    quote = None
    cur = ""
    parts = []
    for ch in inner:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            cur += ch
        elif ch == ",":
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    for p in parts:
        ps = p.strip()
        if not ps:
            raise YamlError(f"{where}: empty flow entry")
        if ps[0] in "\"'":
            continue
        _plain_hazards(ps, where + " (flow entry)", errs)


def _scan_block_scalar(lines, i, mapping_indent):
    """lines[i] is the first candidate content line of 'key: |...' / 'key: >...'.
    Returns index just past the block scalar. Content must be indented strictly
    deeper than the owning mapping; otherwise the block scalar ends (or never
    started, which callers treat as an empty scalar)."""
    content_indent = None
    j = i
    while j < len(lines):
        ln = lines[j]
        if _is_blank(ln):
            j += 1
            continue
        ind = _indent(ln)
        if content_indent is None:
            if ind <= mapping_indent:
                return j
            content_indent = ind
        if ind < content_indent:
            return j
        j += 1
    return j


def _count_unescaped(buf, q):
    cnt = 0
    k = 0
    while k < len(buf):
        if q == '"' and buf[k] == "\\":
            k += 2
            continue
        if buf[k] == q:
            cnt += 1
        k += 1
    return cnt


def _scan_plain(lines, i, mapping_indent, label, errs):
    """Scan continuation lines of a plain scalar owned by a mapping at
    mapping_indent. lines[i] is the first candidate continuation line.
    Returns the index where the plain scalar ended."""
    j = i
    while j < len(lines):
        ln = lines[j]
        if _is_blank(ln):
            j += 1
            continue
        if _is_comment(ln):
            return j
        ind = _indent(ln)
        if ind <= mapping_indent:
            return j
        ls = ln.lstrip(" ")
        m = _KEY.match(ls)
        if m and ": " in ls + " " and (ls[len(m.group(1)) + 1:].strip() or ls.rstrip().endswith(":")):
            errs.append(f"{label} @line{j}: plain scalar continuation contains key-like ': '")
            return j
        if ls.startswith("- "):
            errs.append(f"{label} @line{j}: plain scalar continuation contains sequence marker")
            return j
        _plain_hazards(_strip_comment(ls), f"{label} @line{j}", errs)
        j += 1
    return j


def scan_frontmatter(lines, errs):
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if _is_blank(line) or _is_comment(line):
            i += 1
            continue
        ind = _indent(line)
        ls = line.lstrip(" ")
        m = _KEY.match(ls)
        if m and ls[len(m.group(1))] == ":":
            key = m.group(1)
            raw = (ls[len(key) + 1:]).strip()
            where = f"{key} @line{i}"
            if raw == "":
                i += 1
                continue
            if raw[0] == "[":
                if not raw.endswith("]"):
                    raise YamlError(f"{where}: unterminated flow collection")
                _scan_flow(raw, where, errs)
                i += 1
                continue
            if raw[0] in "\"'":
                q = raw[0]
                buf = raw
                bi = i
                while _count_unescaped(buf, q) < 2:
                    bi += 1
                    if bi >= n:
                        raise YamlError(f"{where}: unterminated quoted scalar")
                    nxt = lines[bi]
                    if nxt.lstrip().startswith("---") and not nxt.strip() == "---":
                        raise YamlError(f"{where}: unterminated quoted scalar")
                    buf += "\n" + nxt.lstrip(" ")
                i = bi + 1
                continue
            if raw[0] in "|>":
                i = _scan_block_scalar(lines, i + 1, ind)
                continue
            _plain_hazards(_strip_comment(raw), where, errs)
            i += 1
            i = _scan_plain(lines, i, ind, where, errs)
            continue
        if ls.startswith("- "):
            dash_indent = ind
            item = ls[2:].strip()
            ik = _KEY.match(item)
            if ik and ":" in item and item[len(ik.group(1))] == ":":
                key = ik.group(1)
                raw = (item[item.index(":") + 1:]).strip()
                key_col = ind + 2 + (len(ls[2:]) - len(ls[2:].lstrip(" ")))
                where = f"- {key} @line{i}"
                if raw == "":
                    i += 1
                    continue
                if raw[0] == "[":
                    if not raw.endswith("]"):
                        raise YamlError(f"{where}: unterminated flow collection")
                    _scan_flow(raw, where, errs)
                    i += 1
                    continue
                if raw[0] in "\"'":
                    i += 1
                    continue
                if raw[0] in "|>":
                    i = _scan_block_scalar(lines, i + 1, key_col)
                    continue
                _plain_hazards(_strip_comment(raw), where, errs)
                i += 1
                i = _scan_plain(lines, i, key_col, where, errs)
                continue
            if item:
                if item[0] == "[":
                    if not item.endswith("]"):
                        raise YamlError(f"seq @line{i}: unterminated flow collection")
                    _scan_flow(item, f"seq @line{i}", errs)
                elif item[0] in "|>":
                    i = _scan_block_scalar(lines, i + 1, dash_indent + 1)
                    continue
                elif item[0] not in "\"'":
                    _plain_hazards(_strip_comment(item), f"seq @line{i}", errs)
            i += 1
            continue
        if ls.startswith("---"):
            raise YamlError(f"@line{i}: stray fence inside front matter")
        raise YamlError(f"@line{i}: orphan line: {line[:60]!r}")
