#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""K0863 canonical verdict-cache applicability scan (2026-11-16).

Motivation
----------
K0863 (STERILE-row depth-10 unclosability) transferred a published
REFUTED-D10 root verdict to cost-69a bit 109 purely through D4 canonical
identity (69a:109 == 65k:75 == 74h:97).  That application used one
canonical collision.  This scan generalises the mechanism into a
reusable canonical verdict cache:

  * collect every per-bit depth-10 engine verdict published on main
    (raw sweep batch lines, sweep records, sweep audits) for every
    class-2 / class-4 lane child,
  * key each root position by its D4 canonical mask,
  * transfer verdicts to every in-flight lane claim's candidate roots
    by canonical identity, iterating to a fixpoint,
  * use the same index as a corpus-wide WIN/LOSS conflict detector:
    any position determined twice with different verdicts (engine vs
    engine, or engine vs transfer) is flagged immediately.

Trust boundary: identical to the published sweeps (engine depth-10
verdict soundness + D4 invariance of the game tree).  Verdict transfer
says nothing about row closure, receipt coverage, or game-theoretic
values.  11x11 empty board remains UNKNOWN.

Determinism: no randomness, no wall clock, sorted file iteration and
sort_keys serialisation; two runs produce byte-identical output.
"""

import glob
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
S2OUT = os.path.abspath(os.path.join(
    HERE, "..", "n11-s2-5960-ms5-s7-reuse-20261113", "output"))
OUTDIR = os.path.join(HERE, "output")
OUTPATH = os.path.join(OUTDIR, "theorem-applicability-scan-20261116.json")

SCAN_DATE = "2026-11-16"
MAX_ITERATIONS = 8
DATE_RE = re.compile(r"-(2026\d{4})")
HEX_RE = re.compile(r"^[0-9a-f]{32}$")

REFUTED = "REFUTED-D10"
WIN = "WIN7-D10"
UNKNOWN = "UNKNOWN-CAPPED"


# ---------------------------------------------------------------- geometry

def stones(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(121) if (v >> i) & 1]


def d4_canon(hexstr):
    st = stones(hexstr)
    best = None
    for swap in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                t = []
                for c in st:
                    x, y = c % 11, c // 11
                    a, b = (y, x) if swap else (x, y)
                    if fx:
                        a = 10 - a
                    if fy:
                        b = 10 - b
                    t.append(a + 11 * b)
                v = 0
                for i in t:
                    v |= 1 << i
                h = format(v, "032x")
                if best is None or h < best:
                    best = h
    return best


def bareiss4(m):
    m = [row[:] for row in m]
    prev = 1
    for k in range(3):
        if m[k][k] == 0:
            for r in range(k + 1, 4):
                if m[r][k] != 0:
                    m[k], m[r] = m[r], m[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
            m[i][k] = 0
        prev = m[k][k]
    return m[3][3]


def det4(cells):
    return bareiss4([[(c % 11) ** 2 + (c // 11) ** 2, c % 11, c // 11, 1]
                     for c in cells])


def enumerate_legal(hexstr):
    st = stones(hexstr)
    legal = []
    for p in range(121):
        if p in st:
            continue
        ok = True
        for i in range(len(st)):
            for j in range(i + 1, len(st)):
                for k in range(j + 1, len(st)):
                    if det4([st[i], st[j], st[k], p]) == 0:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            legal.append(p)
    return legal


def root_hex(child, bit):
    return format(int(child, 16) | (1 << bit), "032x")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- harvest

def split_label_date(filename, marker):
    stem = filename[: filename.rfind(".")]
    idx = stem.find(marker)
    label = stem[:idx]
    m = DATE_RE.search(stem)
    return label, (m.group(1) if m else None)


def child_of(doc):
    for key in ("s6_child", "s6_child_hex", "child"):
        v = doc.get(key)
        if isinstance(v, str) and HEX_RE.match(v):
            return v
    t = doc.get("target")
    if isinstance(t, dict):
        v = t.get("s6_child_hex")
        if isinstance(v, str) and HEX_RE.match(v):
            return v
    return None


def collect():
    claims = []      # dicts: label, date, path, child, legal, status
    sweeps = []     # dicts: label, date, path, child
    audits = []     # dicts: label, date, path, child, doc
    raws = []       # dicts: label, date, path
    skipped = []

    for p in sorted(glob.glob(os.path.join(
            S2OUT, "class[24]-lane-cost*-inflight-*.json"))):
        fn = os.path.basename(p)
        label, date = split_label_date(fn, "-inflight-")
        try:
            doc = load_json(p)
        except Exception as e:
            skipped.append({"file": fn, "reason": "json parse: %s" % e})
            continue
        ch = child_of(doc)
        legal = doc.get("legal_candidates")
        status = doc.get("status")
        claims.append({"label": label, "date": date, "path": fn,
                        "child": ch, "legal": legal,
                        "status": status if isinstance(status, str)
                        else (json.dumps(status) if status is not None
                              else None)})
    for p in sorted(glob.glob(os.path.join(
            S2OUT, "class[24]-lane-cost*-sweep-20261*.json"))):
        fn = os.path.basename(p)
        label, date = split_label_date(fn, "-sweep-")
        try:
            doc = load_json(p)
        except Exception as e:
            skipped.append({"file": fn, "reason": "json parse: %s" % e})
            continue
        sweeps.append({"label": label, "date": date, "path": fn,
                       "child": child_of(doc)})
    for p in sorted(glob.glob(os.path.join(
            S2OUT, "class[24]-lane-cost*-sweep-audit-*.json"))):
        fn = os.path.basename(p)
        label, date = split_label_date(fn, "-sweep-audit-")
        try:
            doc = load_json(p)
        except Exception as e:
            skipped.append({"file": fn, "reason": "json parse: %s" % e})
            continue
        audits.append({"label": label, "date": date, "path": fn,
                        "child": child_of(doc), "doc": doc})
    for pat in ("class[24]-lane-cost*-raw-batch*-20261*.jsonl",
                "class[24]-lane-cost*-raw-20261*.jsonl"):
        for p in sorted(glob.glob(os.path.join(S2OUT, pat))):
            fn = os.path.basename(p)
            label, date = split_label_date(fn, "-raw-")
            raws.append({"label": label, "date": date, "path": fn})
    return claims, sweeps, audits, raws, skipped


def resolve_child(label, date, meta_by_label):
    """child hex for a (label, date) pair; falls back to a unique child."""
    per = meta_by_label.get(label, [])
    if not per:
        return None, "no claim/sweep/audit metadata for lane"
    same_date = [m["child"] for m in per
                 if m.get("date") == date and m.get("child")]
    if same_date:
        if len(set(same_date)) == 1:
            return same_date[0], None
        return None, "conflicting child hexes for (label, date)"
    uniq = set(m["child"] for m in per if m.get("child"))
    if len(uniq) == 1:
        return uniq.pop(), "date fallback (lane has a unique child)"
    return None, "lane label reused for multiple children; no same-date match"


# ------------------------------------------------------------ engine map

def add_engine(eng, child, bit, verdict, source):
    if child is None or bit is None:
        return
    key = (child, bit)
    slot = eng.setdefault(key, {"verdict": verdict, "sources": []})
    if slot["verdict"] != verdict:
        slot.setdefault("conflicts", []).append(
            {"verdict": verdict, "source": source})
    slot["sources"].append(source)


def build_engine_map(claims, sweeps, audits, raws, legal_cache):
    eng = {}
    eng_conflicts = []
    skipped_aggs = []
    meta_by_label = {}
    for group in (claims, sweeps):
        for m in group:
            meta_by_label.setdefault(m["label"], []).append(m)
    for m in audits:
        meta_by_label.setdefault(m["label"], []).append(m)

    # raw batch lines (uniform per-bit schema)
    raw_skipped_lines = 0
    raw_files_used = 0
    raw_unresolved = []
    for r in raws:
        child, reason = resolve_child(r["label"], r["date"], meta_by_label)
        if child is None:
            raw_unresolved.append({"file": r["path"], "reason": reason})
            continue
        raw_files_used += 1
        with open(os.path.join(S2OUT, r["path"]), "r",
                  encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    bit = row["bit"]
                    capped = bool(row.get("capped", False))
                    loss = bool(row.get("loss", False))
                except Exception:
                    raw_skipped_lines += 1
                    continue
                verdict = UNKNOWN if capped else (WIN if loss else REFUTED)
                add_engine(eng, child, bit, verdict,
                           {"kind": "raw", "file": r["path"]})

    def add_bits(child, win_bits, refuted_bits, capped_bits, source):
        for b in (win_bits or []):
            add_engine(eng, child, int(b), WIN, source)
        for b in (refuted_bits or []):
            add_engine(eng, child, int(b), REFUTED, source)
        for b in (capped_bits or []):
            add_engine(eng, child, int(b), UNKNOWN, source)

    for m in audits:
        doc = m["doc"]
        child = m["child"]
        src = {"kind": "audit", "file": m["path"]}
        agg = doc.get("aggregate")
        if isinstance(agg, dict) and "refuted_d10_bits" in agg:
            add_bits(child, agg.get("win7_d10_bits"),
                     agg.get("refuted_d10_bits"), agg.get("capped_bits"),
                     src)
            continue
        st = doc.get("sweep_totals")
        if isinstance(st, dict) and "win7_d10_bits" in st:
            derived = False
            if child is not None and \
                    int(st.get("capped_count", -1)) == 0 and \
                    child in legal_cache:
                legal = legal_cache[child]
                win = set(int(b) for b in st["win7_d10_bits"])
                refuted = sorted(b for b in legal if b not in win)
                if len(refuted) == int(st.get("refuted_d10_count", -1)):
                    add_bits(child, sorted(win), refuted, [], src)
                    derived = True
            if not derived:
                add_bits(child, st.get("win7_d10_bits"), None, None, src)
            continue
        if child is not None and "win7_d10_bits" in doc:
            add_bits(child, doc["win7_d10_bits"], None, None, src)
            continue
        skipped_aggs.append({"file": m["path"],
                             "reason": "unrecognised audit schema"})

    for m in sweeps:
        doc = load_json(os.path.join(S2OUT, m["path"]))
        child = m["child"] or child_of(doc)
        src = {"kind": "sweep", "file": m["path"]}
        cands = doc.get("candidates")
        if isinstance(cands, list) and cands and child and \
                isinstance(cands[0], dict) and "bit" in cands[0]:
            # per-bit verdict rows (2026-11-14 era sweep records)
            for row in cands:
                bit = row.get("bit")
                verdict = row.get("verdict")
                capped = bool(row.get("capped", False))
                if verdict == "REFUTED-D10" and not capped:
                    add_engine(eng, child, bit, REFUTED, src)
                elif verdict == "WIN7-D10" and not capped:
                    add_engine(eng, child, bit, WIN, src)
                else:
                    add_engine(eng, child, bit, UNKNOWN, src)
            summ = doc.get("summary")
            if isinstance(summ, dict):
                ssrc = {"kind": "sweep-summary", "file": m["path"]}
                s_win = summ.get("win7_d10")
                s_ref = summ.get("refuted_d10")
                s_cap = summ.get("capped")
                if isinstance(s_win, list) and isinstance(s_ref, list):
                    add_bits(child, s_win, s_ref,
                             s_cap if isinstance(s_cap, list) else None,
                             ssrc)
            continue
        agg = doc.get("aggregate")
        if isinstance(agg, dict) and "win7_d10_bits" in agg and child:
            capped = int(agg.get("capped", 0) or 0)
            if "refuted_d10_bits" in agg:
                add_bits(child, agg["win7_d10_bits"],
                         agg.get("refuted_d10_bits"),
                         agg.get("capped_bits"), src)
            elif capped == 0 and child in legal_cache:
                legal = legal_cache[child]
                win = set(int(b) for b in agg["win7_d10_bits"])
                refuted = sorted(b for b in legal if b not in win)
                if int(agg.get("refuted_d10", -1)) == len(refuted) and \
                        int(agg.get("candidates", -1)) == len(legal):
                    add_bits(child, agg["win7_d10_bits"], refuted, [], src)
                else:
                    add_bits(child, agg["win7_d10_bits"], None, None, src)
            else:
                add_bits(child, agg["win7_d10_bits"], None, None, src)
        elif child and "win7_d10_bits" in doc and \
                isinstance(doc.get("win7_d10_bits"), list):
            add_bits(child, doc["win7_d10_bits"], None, None, src)

    for (child, bit) in sorted(eng):
        slot = eng[(child, bit)]
        if "conflicts" in slot:
            eng_conflicts.append({"child": child, "bit": bit,
                                  "primary": slot["verdict"],
                                  "conflicts": slot["conflicts"]})
    return (eng, eng_conflicts, raw_files_used, raw_skipped_lines,
            raw_unresolved, skipped_aggs)


# ------------------------------------------------------------------- main

def main():
    checks = []

    def check(name, cond, detail=None):
        checks.append({"name": name, "pass": bool(cond),
                       "detail": detail if detail is not None else None})
        return bool(cond)

    claims, sweeps, audits, raws, skipped_files = collect()

    # ---- child metadata and independent legal enumeration
    children = {}
    for m in claims:
        ch = m["child"]
        if ch:
            children.setdefault(ch, {"claims": [], "sweeps": [],
                                     "audits": []})["claims"].append(m)
    for m in sweeps:
        ch = m["child"]
        if ch:
            children.setdefault(ch, {"claims": [], "sweeps": [],
                                     "audits": []})["sweeps"].append(m)
    for m in audits:
        ch = m["child"]
        if ch:
            children.setdefault(ch, {"claims": [], "sweeps": [],
                                     "audits": []})["audits"].append(m)
    legal_cache = {}
    stone_count_bad = []
    for ch in sorted(children):
        st = stones(ch)
        if len(st) != 6:
            stone_count_bad.append(ch)
            continue
        legal_cache[ch] = enumerate_legal(ch)
    check("C1a-children-parsed",
          len(legal_cache) > 100,
          {"children_seen": len(children),
           "six_stone_children": len(legal_cache),
           "non_six_stone_skipped": stone_count_bad})

    # claim legal list agreement with independent enumeration
    legal_agree = 0
    legal_disagree = []
    for m in claims:
        ch = m["child"]
        if ch not in legal_cache or not m["legal"]:
            continue
        mine = set(legal_cache[ch])
        theirs = set(int(b) for b in m["legal"])
        if mine == theirs:
            legal_agree += 1
        else:
            legal_disagree.append({"label": m["label"], "date": m["date"],
                                   "claim": sorted(theirs),
                                   "independent": sorted(mine)})
    check("C1b-claim-legal-agreement",
          not legal_disagree,
          {"agree": legal_agree, "disagree": legal_disagree})

    # ---- engine verdict map
    eng, eng_conflicts, raw_files_used, raw_skipped_lines, \
        raw_unresolved, skipped_aggs = build_engine_map(
            claims, sweeps, audits, raws, legal_cache)
    skipped_files.extend(skipped_aggs)
    skipped_files.extend(raw_unresolved)
    check("C5-engine-map-conflict-free", not eng_conflicts,
          {"conflicts": eng_conflicts,
           "raw_files_used": raw_files_used,
           "raw_unresolved": len(raw_unresolved),
           "raw_skipped_lines": raw_skipped_lines,
           "engine_determined_bits": len(eng)})
    eng_refuted = sum(1 for v in eng.values() if v["verdict"] == REFUTED)
    eng_win = sum(1 for v in eng.values() if v["verdict"] == WIN)
    eng_unknown = sum(1 for v in eng.values() if v["verdict"] == UNKNOWN)

    # ---- bit convention control (published win_roots hexes)
    conv_ok = []
    for m in audits:
        doc = m["doc"]
        st = doc.get("sweep_totals") or {}
        win_roots = st.get("win_roots")
        child = m["child"]
        if isinstance(win_roots, dict) and child:
            for bit_s, hex_ in sorted(win_roots.items()):
                conv_ok.append(root_hex(child, int(bit_s)) == hex_)
    check("C2-bit-convention-against-win-roots",
          bool(conv_ok) and all(conv_ok),
          {"checked": len(conv_ok)})

    # ---- iterate: canonical index + transfer to a fixpoint
    transfers = {}   # (child, bit) -> record
    canon_conflicts = []
    per_iteration = []
    iteration = 0
    while iteration < MAX_ITERATIONS:
        iteration += 1
        index = {}
        for (child, bit) in sorted(eng):
            slot = eng[(child, bit)]
            if slot["verdict"] == UNKNOWN:
                continue
            canon = d4_canon(root_hex(child, bit))
            index.setdefault(canon, []).append(
                {"child": child, "bit": bit, "verdict": slot["verdict"],
                 "kind": "engine"})
        for (child, bit) in sorted(transfers):
            rec = transfers[(child, bit)]
            canon = d4_canon(root_hex(child, bit))
            index.setdefault(canon, []).append(
                {"child": child, "bit": bit, "verdict": rec["verdict"],
                 "kind": "transfer",
                 "iteration": rec["iteration"]})
        # corpus-wide canonical conflict detection
        new_canon_conflicts = []
        for canon in sorted(index):
            entries = index[canon]
            verdicts = set(e["verdict"] for e in entries)
            if len(verdicts) > 1:
                new_canon_conflicts.append({"canonical": canon,
                                            "entries": entries})
        if new_canon_conflicts:
            canon_conflicts = new_canon_conflicts
            break
        # scan every child's undetermined candidate roots
        new_transfers = 0
        for ch in sorted(legal_cache):
            for bit in legal_cache[ch]:
                if (ch, bit) in eng or (ch, bit) in transfers:
                    continue
                canon = d4_canon(root_hex(ch, bit))
                hits = index.get(canon)
                if not hits:
                    continue
                verdict = hits[0]["verdict"]
                transfers[(ch, bit)] = {
                    "verdict": verdict, "iteration": iteration,
                    "via": [{"child": h["child"], "bit": h["bit"],
                             "kind": h["kind"]}
                            for h in hits]}
                new_transfers += 1
        per_iteration.append({"iteration": iteration,
                              "index_entries": len(index),
                              "new_transfers": new_transfers})
        if new_transfers == 0:
            break

    check("C4-canonical-index-conflict-free", not canon_conflicts,
          {"conflicts": canon_conflicts})

    # ---- regression: K0863 bit-109 application must re-derive
    claim69a = None
    for m in claims:
        if m["label"] == "class2-lane-cost69a" and m["date"] == "20261116":
            claim69a = m
    bit109_ok = False
    bit109_detail = None
    if claim69a and claim69a["child"] == \
            "00000000000000801222000000800000":
        rec = transfers.get((claim69a["child"], 109))
        if rec and rec["verdict"] == REFUTED:
            via = rec["via"]
            bit109_ok = any(v["child"] ==
                            "00000000020000801202000000200000"
                            and v["bit"] == 75 for v in via) or \
                any(v["child"] == "00000000000000889002000000000800"
                    and v["bit"] == 97 for v in via)
            bit109_detail = {"via": via}
    check("C3-k0863-bit109-regression", bit109_ok, bit109_detail)

    # ---- per-child classification
    targets = {}
    for ch in sorted(legal_cache):
        legal = legal_cache[ch]
        rec = {"child": ch,
               "legal_count": len(legal),
               "claims": sorted({"%s/%s" % (m["label"], m["date"])
                                 for m in children[ch]["claims"]}),
               "engine": {"REFUTED-D10": 0, "WIN7-D10": 0,
                          "UNKNOWN-CAPPED": 0},
               "transferred": {"REFUTED-D10": [], "WIN7-D10": []},
               "open": 0}
        for bit in legal:
            slot = eng.get((ch, bit))
            if slot is not None:
                rec["engine"][slot["verdict"]] += 1
                continue
            tr = transfers.get((ch, bit))
            if tr is not None:
                rec["transferred"][tr["verdict"]].append(
                    {"bit": bit, "iteration": tr["iteration"],
                     "via": tr["via"][:6]})
            else:
                rec["open"] += 1
        targets[ch] = rec

    # ---- cross-child engine agreement on identical positions
    agreement_pairs = 0
    agreement_conflicts = 0
    canon_of = {}
    for (child, bit) in eng:
        canon_of[(child, bit)] = d4_canon(root_hex(child, bit))
    by_canon = {}
    for k, c in canon_of.items():
        by_canon.setdefault(c, []).append(k)
    for c in sorted(by_canon):
        keys = by_canon[c]
        if len(keys) < 2:
            continue
        verdicts = set(eng[k]["verdict"] for k in keys)
        if len(verdicts) == 1:
            agreement_pairs += 1
        else:
            agreement_conflicts += 1
    check("C8-cross-sweep-same-position-agreement",
          agreement_conflicts == 0,
          {"same_position_groups": agreement_pairs,
           "conflicting_groups": agreement_conflicts})

    # ---- STERILE detection (complete + all REFUTED + 0 capped)
    sterile = []
    for ch, rec in sorted(targets.items()):
        if rec["legal_count"] > 0 and \
                rec["engine"]["UNKNOWN-CAPPED"] == 0 and \
                rec["engine"]["WIN7-D10"] == 0 and \
                rec["transferred"]["WIN7-D10"] == [] and \
                rec["engine"]["REFUTED-D10"] + \
                len(rec["transferred"]["REFUTED-D10"]) == \
                rec["legal_count"]:
            sterile.append({"child": ch,
                            "engine_refuted": rec["engine"]["REFUTED-D10"],
                            "transferred_refuted":
                                len(rec["transferred"]["REFUTED-D10"])})
    known_sterile = {
        "00000000020000801202000000200000": "65k",
        "00000000000000801282000000200000": "70j",
        "00000000000000889002000000000800": "74h",
        "00000000000000003800000008002020": "64c",
    }
    check("C7-known-sterile-rows-present",
          all(any(s["child"] == ch for s in sterile)
              for ch in known_sterile),
          {"known": sorted(known_sterile.values()),
           "sterile_found": len(sterile)})

    # ---- input manifest
    manifest = {}
    all_files = sorted(set(
        [m["path"] for m in claims] + [m["path"] for m in sweeps] +
        [m["path"] for m in audits] + [m["path"] for m in raws]))
    for fn in all_files:
        manifest[fn] = sha256_file(os.path.join(S2OUT, fn))

    # ---- summary numbers
    new_refuted = [k for k, v in transfers.items()
                   if v["verdict"] == REFUTED]
    new_win = [k for k, v in transfers.items() if v["verdict"] == WIN]
    unswept_targets = 0
    unswept_new_refuted = 0
    unswept_open_after_transfer = 0
    for ch, rec in targets.items():
        if rec["engine"]["REFUTED-D10"] + rec["engine"]["WIN7-D10"] + \
                rec["engine"]["UNKNOWN-CAPPED"] == 0:
            unswept_targets += 1
            unswept_new_refuted += len(rec["transferred"]["REFUTED-D10"])
            unswept_open_after_transfer += rec["open"]

    result = {
        "schema": "n11-k0863-theorem-applicability-scan-20261116-v1",
        "date": SCAN_DATE,
        "method": {
            "statement": ("depth-10 root verdicts are D4-invariant; a "
                          "candidate root whose canonical mask equals a "
                          "published root with a determined verdict "
                          "inherits that verdict (canonical identity "
                          "transfer, the mechanism K0863 applied to 69a "
                          "bit 109)"),
            "index_sources": ["raw-batch jsonl per-bit lines",
                              "sweep audit aggregates",
                              "sweep record aggregates"],
            "bit_convention": ("root = child | (1 << bit) over the "
                               "32-hex 128-bit board mask, bits 0..120"),
            "iterations": per_iteration,
            "max_iterations": MAX_ITERATIONS,
        },
        "trust_boundary": ("engine depth-10 verdict soundness + D4 "
                           "invariance, identical to the published sweeps; "
                           "a broken premise surfaces as a verdict conflict "
                           "between two determinations of the same "
                           "position"),
        "inputs": {
            "experiment_output_dir": ("research/experiments/"
                                      "n11-s2-5960-ms5-s7-reuse-20261113"
                                      "/output"),
            "claims": len(claims), "sweeps": len(sweeps),
            "audits": len(audits), "raw_files": len(raws),
            "raw_files_resolved": raw_files_used,
            "raw_unresolved": len(raw_unresolved),
            "raw_skipped_lines": raw_skipped_lines,
            "manifest_sha256": manifest},
        "engine_map": {"determined_bits": len(eng),
                       "REFUTED-D10": eng_refuted, "WIN7-D10": eng_win,
                       "UNKNOWN-CAPPED": eng_unknown,
                       "source_conflicts": eng_conflicts},
        "transfers": {"total": len(transfers),
                      "REFUTED-D10": len(new_refuted),
                      "WIN7-D10": len(new_win),
                      "by_iteration": {str(i): sum(
                          1 for v in transfers.values()
                          if v["iteration"] == i)
                          for i in range(1, MAX_ITERATIONS + 1)
                          if any(v["iteration"] == i
                                 for v in transfers.values())}},
        "unswept_targets": {"children": unswept_targets,
                            "new_refuted_on_unswept":
                                unswept_new_refuted,
                            "still_open_on_unswept":
                                unswept_open_after_transfer},
        "targets": targets,
        "sterile_rows_detected": sterile,
        "same_position_cross_sweeps": {
            "agreement_groups": agreement_pairs,
            "conflict_groups": agreement_conflicts},
        "checks": checks,
        "skipped_files": skipped_files,
        "interpretation": ("canonical verdict transfer only determines "
                           "individual 7-stone root verdicts; it does not "
                           "close any manifest row, does not create a "
                           "receipt, and says nothing about game-theoretic "
                           "values"),
        "unknown_status": ("11x11 empty board, two-stone roots {49,60}/"
                           "{59,60}, S2 {59,60} and classes 1/2/4 all "
                           "remain UNKNOWN"),
    }
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTPATH, "w", encoding="utf-8") as fh:
        json.dump(result, fh, sort_keys=True, indent=1)
        fh.write("\n")
    print("K0863_APPLICABILITY_SCAN_WRITTEN %s" % OUTPATH)
    print("engine_bits=%d refuted=%d win=%d unknown=%d transfers=%d "
          "(new_refuted=%d new_win=%d) conflicts(engine=%d canon=%d "
          "samepos=%d)" % (
              len(eng), eng_refuted, eng_win, eng_unknown, len(transfers),
              len(new_refuted), len(new_win), len(eng_conflicts),
              len(canon_conflicts), agreement_conflicts))
    failed = [c["name"] for c in checks if not c["pass"]]
    print("checks: %d pass, %d fail%s" % (
        len(checks) - len(failed), len(failed),
        (" -> " + ", ".join(failed)) if failed else ""))
    return bool(failed) or bool(eng_conflicts) or bool(canon_conflicts) \
        or bool(agreement_conflicts)


if __name__ == "__main__":
    raise SystemExit(main())
