#!/usr/bin/env python3
"""Minimal faithful YAML-subset parser for the kyouen knowledge corpus.

Reproduces the load failure modes of tools/knowledge/common.py
(UniqueLoader + PyYAML block-context plain-scalar hazards) without PyYAML.

Grammar = exactly what the corpus uses:
  * block mappings / sequences, any indent >= 0 (legacy style has sequence
    dashes at the same indent as the owning key)
  * values: plain, single/double quoted (multi-line quoted continuation
    accepted), flow lists [a, b], block scalars |/ >  with - / + / clip chomping
  * duplicate keys inside one mapping raise (UniqueLoader semantics)
Plain-scalar hazards raise exactly like PyYAML ScannerError:
  * ASCII ': ' inside a plain scalar or its continuation
  * ' #' comment marker inside a plain scalar
"""
import re


class YamlMinError(Exception):
    pass


_KEY = re.compile(r"([A-Za-z_][A-Za-z0-9_]*):")


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _skip(lines, i):
    while i < len(lines):
        ls = lines[i].strip()
        if ls == "" or ls.startswith("#"):
            i += 1
        else:
            break
    return i


def _strip_comment(raw):
    idx = raw.find(" #")
    return raw[:idx] if idx >= 0 else raw


def _plain_check(value, where):
    if ": " in value:
        raise YamlMinError(f"{where}: plain scalar contains ASCII ': '")
    if value.strip() and " #" in value:
        raise YamlMinError(f"{where}: plain scalar contains ' #'")
    if value.endswith(":") or ":\\n" in value:
        # 'key:' alone on a value line means the scanner would try to build a
        # nested node without a context -> treat as hazard (corpus never uses)
        if value.rstrip().endswith(":"):
            raise YamlMinError(f"{where}: bare ':' plain scalar")


def _unquote_single(s):
    return s.replace("''", "'")


def _unquote_double(s):
    out = []
    i = 0
    simple = {"n": "\n", "t": "\t", '"': '"', "\\": "\\", "0": "\0"}
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append(simple.get(s[i + 1], "\\" + s[i + 1]))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def _read_quoted(lines, i, raw, where):
    """raw starts with a quote at line i; consume continuation lines until
    the unescaped closing quote. Returns (value, next_i)."""
    q = raw[0]
    buf = raw
    j = i
    while True:
        # scan past the opening quote for an unescaped closing quote
        k = 1
        close = -1
        while k < len(buf):
            if q == '"' and buf[k] == "\\":
                k += 2
                continue
            if buf[k] == q:
                if q == "'" and k + 1 < len(buf) and buf[k + 1] == "'":
                    k += 2
                    continue
                close = k
                break
            k += 1
        if close >= 0:
            break
        j += 1
        if j >= len(lines):
            raise YamlMinError(f"{where}: unterminated quoted scalar")
        buf += "\n" + lines[j].lstrip(" ")
    body = buf[1:close]
    # fold newlines to spaces (PyYAML flow folding, first line kept as is)
    parts = body.split("\n")
    folded = parts[0] + "".join(("\n" if p == "" else " " + p) for p in parts[1:])
    if q == '"':
        return _unquote_double(folded), j + 1
    return _unquote_single(folded), j + 1


def _read_flow(raw, where):
    body = raw.strip()
    if not (body.startswith("[") and body.endswith("]")):
        raise YamlMinError(f"{where}: malformed flow collection")
    inner = body[1:-1].strip()
    if not inner:
        return []
    out, cur, quote = [], "", None
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
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    values = []
    for part in out:
        ps = part.strip()
        if not ps:
            raise YamlMinError(f"{where}: empty flow entry")
        if ps[0] in "\"'":
            q = ps[0]
            if len(ps) >= 2 and ps[-1] == q:
                values.append(_unquote_double(ps[1:-1]) if q == '"' else _unquote_single(ps[1:-1]))
            else:
                raise YamlMinError(f"{where}: malformed quoted flow entry")
        else:
            _plain_check(ps, where + " (flow entry)")
            values.append(ps)
    return values


def _read_block_scalar(lines, i, key_indent, style, chomp, where):
    """lines[i] is the line after 'key: |...'. Returns (value, next_i)."""
    content_indent = None
    collected = []
    j = i
    while j < len(lines):
        ln = lines[j]
        if ln.strip() == "":
            collected.append("")
            j += 1
            continue
        ind = _indent(ln)
        if content_indent is None:
            if ind <= key_indent:
                raise YamlMinError(f"{where}: block scalar has no content")
            content_indent = ind
        if ind < content_indent:
            break
        collected.append(ln[content_indent:])
        j += 1
    # trim trailing blanks
    while collected and collected[-1] == "":
        collected.pop()
    if style == "|":
        body = "\n".join(collected)
    else:  # folded
        para, out = [], []
        for ln in collected:
            if ln == "":
                out.append(" ".join(para))
                para = []
            else:
                para.append(ln)
        out.append(" ".join(para))
        body = "\n".join(out)
    if chomp == "-":
        return body, j
    if chomp == "+":
        return body + "\n", j
    return (body + "\n") if body else body, j


def _read_plain(lines, i, raw, key_indent, where):
    """Plain scalar starting on line i with content raw (already lstripped).
    Returns (value, next_i)."""
    value = _strip_comment(raw).rstrip()
    _plain_check(value, where)
    j = i + 1
    while j < len(lines):
        ln = lines[j]
        if ln.strip() == "":
            break
        ind = _indent(ln)
        ls = ln.lstrip(" ")
        if ls.startswith("#"):
            break
        if ind <= key_indent:
            break
        if ls.startswith("- ") or ls == "-":
            break
        mk = _KEY.match(ls)
        if mk and (len(ls) == len(mk.group(1)) + 1 or ls[len(mk.group(1)) + 1] in ": \n"):
            raise YamlMinError(f"{where}: plain scalar continuation became a mapping key@{j}")
        cont = _strip_comment(ls).rstrip()
        _plain_check(cont, f"{where} continuation@{j}")
        value = value + " " + cont
        j += 1
    return value, j


def _parse_sequence(lines, i, indent):
    """Sequence whose dashes are at exactly `indent`. Returns (list, next_i)."""
    out = []
    i = _skip(lines, i)
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "":
            i += 1
            continue
        ind = _indent(ln)
        ls = ln.lstrip(" ")
        if ind < indent or not (ls.startswith("- ") or ls == "-"):
            break
        if ind > indent:
            raise YamlMinError(f"sequence item deeper than dash indent @{i}")
        after = ls[2:] if ls.startswith("- ") else ""
        if ls == "-":
            val, i = _parse_node(lines, i + 1, indent + 2)
            out.append(val)
            continue
        stripped = after.strip()
        item_col = ind + (len(ls) - len(after.lstrip(" ")))
        if stripped == "":
            val, i = _parse_node(lines, i + 1, item_col)
            out.append(val)
            continue
        mk = _KEY.match(stripped)
        if mk and (len(stripped) == len(mk.group(1)) + 1 or stripped[len(mk.group(1)) + 1] in ": "):
            key = mk.group(1)
            raw = (stripped[len(key) + 1:]).strip()
            item = {}
            i = _assign_value(lines, i + 1, item, key, raw, item_col)
            out.append(item)
            # continue collecting keys of this inline mapping
            i = _parse_mapping_rest(lines, i, item_col, item)
            continue
        if stripped[0] in "\"'":
            val, i = _read_quoted(lines, i, stripped, f"seq item @{i}")
            out.append(val)
            continue
        if stripped.startswith("["):
            val = _read_flow(stripped, f"seq item @{i}")
            out.append(val)
            i += 1
            continue
        if stripped[0] in "|>":
            style = stripped[0]
            chomp = stripped[1:2] or ""
            val, i = _read_block_scalar(lines, i + 1, ind, style, chomp, f"seq item @{i}")
            out.append(val)
            continue
        val, i = _read_plain(lines, i, stripped, ind, f"seq item @{i}")
        out.append(val)
        continue
    return out, i


def _assign_value(lines, i, mapping, key, raw, key_indent):
    """Assign the value of mapping[key] where the inline raw text was on line
    i-1 (already consumed). Returns next index after the value."""
    if raw == "":
        val, i = _parse_value_nested(lines, i, key_indent)
        mapping[key] = val
        return i
    if raw[0] in "\"'":
        val, i = _read_quoted(lines, i - 1, raw, f"{key} line@{i-1}")
        mapping[key] = val
        return i
    if raw.startswith("["):
        mapping[key] = _read_flow(raw, f"{key}")
        return i
    if raw[0] in "|>":
        style = raw[0]
        chomp = raw[1:2] or ""
        val, i = _read_block_scalar(lines, i, key_indent, style, chomp, key)
        mapping[key] = val
        return i
    mapping[key] = None  # placeholder to make duplicate detection order-stable
    val, i = _read_plain(lines, i - 1, raw, key_indent, f"{key} line@{i-1}")
    mapping[key] = val
    return i


def _parse_mapping_rest(lines, i, indent, mapping):
    """Continue a mapping started with an inline entry; keys at `indent`."""
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "":
            i += 1
            continue
        ind = _indent(ln)
        ls = ln.lstrip(" ")
        if ls.startswith("#"):
            i += 1
            continue
        if ind < indent:
            break
        if ind > indent:
            raise YamlMinError(f"unexpected deeper line @{i}: {ln[:50]!r}")
        if ls.startswith("- ") or ls == "-":
            break
        mk = _KEY.match(ls)
        if not mk or ls[len(mk.group(1))] != ":":
            raise YamlMinError(f"orphan mapping line @{i}: {ln[:50]!r}")
        key = mk.group(1)
        if key in mapping:
            raise YamlMinError(f"duplicate YAML key: {key}")
        raw = ls[len(key) + 1:].strip()
        i = _assign_value(lines, i + 1, mapping, key, raw, indent)
    return i


def _parse_value_nested(lines, i, key_indent):
    """Value of 'key:' with nothing inline on lines[i..]."""
    j = _skip(lines, i)
    if j >= len(lines):
        return None, i
    ln = lines[j]
    ind = _indent(ln)
    ls = ln.lstrip(" ")
    if ls.startswith("- ") or ls == "-":
        if ind >= key_indent:
            return _parse_sequence(lines, j, ind)
        return None, i
    if ind <= key_indent:
        return None, i
    return _parse_mapping_rest_new(lines, j, ind)


def _parse_mapping_rest_new(lines, i, indent):
    mapping = {}
    i = _parse_mapping_rest(lines, i, indent, mapping)
    return mapping, i


def _parse_node(lines, i, indent):
    j = _skip(lines, i)
    if j >= len(lines):
        return None, i
    ln = lines[j]
    ind = _indent(ln)
    ls = ln.lstrip(" ")
    if ls.startswith("- ") or ls == "-":
        return _parse_sequence(lines, j, ind)
    return _parse_mapping_rest_new(lines, j, ind)


def parse_frontmatter(text):
    """Parse a front-matter string into a dict; raise YamlMinError on any
    construct outside the corpus subset or on PyYAML-equivalent hazards."""
    lines = text.split("\n")
    doc, i = _parse_node(lines, 0, 0)
    rest = lines[i:]
    for ln in rest:
        if ln.strip() and not ln.strip().startswith("#"):
            raise YamlMinError(f"trailing content after front matter node: {ln[:50]!r}")
    if not isinstance(doc, dict):
        raise YamlMinError("front matter must be a mapping")
    return doc
