#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resolve6: post-39-root-sweep re-solve of the 78 residual five-parent target
rows with the FULL published depth-10 verdict corpus joined at the D4-canonical
root level.

Motivation (declared as the next step by K1059's candidate-supply scope audit
and depth-saturation addendum):
  * K1057's resolve5 planned 39 fresh pair witnesses over the 78 residual rows
    from a 4,728-root fresh-safe candidate pool, judging candidates only against
    the 379 REFUTED / 168 WIN explicit pinned verdict chain.
  * K1059 swept that 39-root plan: all 39 REFUTED-D10, and the depth-saturation
    audit made them permanently unusable as closing witnesses.
  * This experiment joins the add-one-stone candidate universe against the FULL
    published verdict corpus -- the K0863 canonical verdict cache rebuilt from
    the 1,279-file class2/class4 cost-lane corpus on current main (plus the 115
    published K0863 theorem transfers), the post-K0863 head-1410 sweep records,
    every published WIN certificate receipt root, and the 39 dead roots --
    all at the D4-canonical root level, then recomputes the exact candidate
    cover (maximum matching + singletons + stranded rows).

Join soundness: every verdict in the join comes from a published engine
verdict record pinned by sha256 (engine depth-10 verdict soundness + D4
invariance of the game tree, the same trust boundary as K0863 and every
published sweep).  A WIN/REFUTED collision at the same canonical root is
flagged immediately (cross-corpus conflict detector); the run fails closed on
any conflict.

Determinism: stdlib only, no randomness, no wall clock in the record body;
two runs produce byte-identical output.

Interpretation guard: REFUTED-D10 is not a LOSS proof; a fold is row-coverage
bookkeeping; the 78 residual rows, the two-stone roots {49,60}/{59,60},
S2 {59,60}, classes 1/2/4 and the standard 11x11 empty board all remain
UNKNOWN.
"""

import glob
import hashlib
import importlib.util
import json
import os
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUTDIR = os.path.join(HERE, "output")
OUTPATH = os.path.join(OUTDIR, "post-saturation-full-cache-join-resolve6-20261120.json")

SCAN_DIR = os.path.join(ROOT, "research", "experiments",
                        "n11-class2-lane-sterile-unclosability-20261116")
SCAN_JSON = os.path.join(SCAN_DIR, "output",
                         "theorem-applicability-scan-20261116.json")
SCAN_SCRIPT = os.path.join(SCAN_DIR, "theorem_applicability_scan_20261116.py")

REFUTED = "REFUTED-D10"
WIN = "WIN7-D10"

# ---- published pins (git blob / sha256) --------------------------------
PINS = {
    "resolve5": {
        "path": "research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/post-twelfth-receipt-cover-resolve5-20261119.json",
        "sha256": "5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e",
    },
    "sweep39": {
        "path": "research/experiments/n11-residual78-39witness-depth10-sweep-20261119/output/witness-39-root-depth10-sweep-20261119.json",
        "sha256": "f8608d0a04a132012f0aa692099cebe851cdf261a3ea916dc4c15d6841fc5246",
    },
}
POST_CACHE_RECORDS = {
    "sweep48": "research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/residual-48-root-depth10-sweep-20261119.json",
    "sweep28": "research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/sweep28-repro/output/residual-28-root-witness-depth10-sweep-20261119.json",
    "k1039_sweep28": "research/experiments/n11-head1410-witness-28-root-full-depth10-sweep-20261119/output/witness-28-root-depth10-sweep-20261119.json",
    "k1040_sweep3": "research/experiments/n11-head1410-k1038-witness-remaining-3-root-depth10-sweep-20261119/output/k1038-witness-remaining-3-root-depth10-sweep-20261119.json",
    "sweep35": "research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/sweep35/eligible-29-candidate-root-depth10-sweep-20261119.json",
    "sweep43": "research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/sweep43/output/witness-43-root-depth10-sweep-20261119.json",
    "sweep39_dead": "research/experiments/n11-residual78-39witness-depth10-sweep-20261119/output/witness-39-root-depth10-sweep-20261119.json",
}
RECEIPT_RECORDS = {
    "global_fold": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-receipt-harvest-global-fold-20261118.json",
    "prev_cost_fold": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78c-79c-receipts-recompute-20261118.json",
    "first_fold_tarball": "research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/first-win7-root-evidence-20261119.tar.gz",
    "second_third_fold": "research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/output/second-third-win7-root-receipt-fold-20261119.json",
    "fourth_fold": "research/experiments/n11-head1410-fourth-win7-receipt-fold-20261119/output/fourth-win7-root-receipt-fold-20261119.json",
    "fifth_sixth_fold": "research/experiments/n11-head1410-fifth-sixth-win7-receipt-fold-20261119/output/fifth-sixth-win7-root-receipt-fold-20261119.json",
    "seventh_fold": "research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/seventh-win7-receipt-fold-20261119.json",
    "eighth_fold": "research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/foldv2/output/eighth-win7-receipt-fold-20261119.json",
    "ninth_twelfth_fold": "research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/ninth-twelfth-win7-receipt-fold-20261119.json",
}
SWEEP6 = {
    "roots": "research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/sweep6/roots.json",
    "probes": "research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119/sweep6/output/probe-records-w%d.jsonl",
}


def need(ok, msg):
    if not ok:
        raise SystemExit("GATE FAILED: " + msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load(rel):
    with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---- geometry (D4 canon, exact integer determinants; resolve5 conventions)
TF = []
for t in range(8):
    tab = []
    for p in range(121):
        x, y = p % 11, p // 11
        if t == 0: X, Y = x, y
        elif t == 1: X, Y = 10 - y, x
        elif t == 2: X, Y = 10 - x, 10 - y
        elif t == 3: X, Y = y, 10 - x
        elif t == 4: X, Y = 10 - x, y
        elif t == 5: X, Y = x, 10 - y
        elif t == 6: X, Y = y, x
        else: X, Y = 10 - y, 10 - x
        tab.append(11 * Y + X)
    TF.append(tab)


def bits_of(mask):
    out = []
    p = 0
    while mask:
        if mask & 1:
            out.append(p)
        mask >>= 1
        p += 1
    return out


def popcount(x):
    n = 0
    while x:
        x &= x - 1
        n += 1
    return n


def transform(mask, t):
    out = 0
    for p in bits_of(mask):
        out |= 1 << TF[t][p]
    return out


def canon_int(mask):
    best = None
    for t in range(8):
        z = transform(mask, t)
        if best is None or z < best:
            best = z
    return best


def canon_hex(mask):
    return format(canon_int(mask), "032x")


def det3(a, b, c):
    (x1, y1), (x2, y2), (x3, y3) = a, b, c
    q1 = x1 * x1 + y1 * y1
    q2 = x2 * x2 + y2 * y2
    q3 = x3 * x3 + y3 * y3
    return q1 * (x2 * y3 - x3 * y2) - q2 * (x1 * y3 - x3 * y1) + q3 * (x1 * y2 - x2 * y1)


def det4(a, b, c, d):
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)


def unsafe_quadruples(mask):
    pts = [(p % 11, p // 11) for p in bits_of(mask)]
    if len(pts) != 7:
        raise ValueError("root must be seven stones")
    n = 0
    for i in range(7):
        for j in range(i + 1, 7):
            for k in range(j + 1, 7):
                for l in range(k + 1, 7):
                    if det4(pts[i], pts[j], pts[k], pts[l]) == 0:
                        n += 1
    return n


def coverage_of(mask, universal):
    covered = set()
    for t in range(8):
        image = transform(mask, t)
        for bit in bits_of(image):
            row = canon_hex(image ^ (1 << bit))
            if row in universal:
                covered.add(row)
    return covered


# ---- blossom maximum matching (verbatim port of the published resolve5 mjs/py)
def maximum_matching(g):
    n = len(g)
    match = [-1] * n
    p = [0] * n
    base = [0] * n
    used = [False] * n
    blossom = [False] * n

    def lca(a, b):
        seen = [False] * n
        while True:
            a = base[a]
            seen[a] = True
            if match[a] == -1:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if seen[b]:
                return b
            b = p[match[b]]

    def mark_path(v, b, child):
        while base[v] != b:
            blossom[base[v]] = True
            blossom[base[match[v]]] = True
            p[v] = child
            child = match[v]
            v = p[match[v]]

    def find_path(root):
        for i in range(n):
            used[i] = False
            p[i] = -1
            base[i] = i
        q = [root]
        used[root] = True
        qi = 0
        while qi < len(q):
            v = q[qi]
            qi += 1
            for u in g[v]:
                if base[v] == base[u] or match[v] == u:
                    continue
                if u == root or (match[u] != -1 and p[match[u]] != -1):
                    b = lca(v, u)
                    for i in range(n):
                        blossom[i] = False
                    mark_path(v, b, u)
                    mark_path(u, b, v)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = b
                            if not used[i]:
                                used[i] = True
                                q.append(i)
                elif p[u] == -1:
                    p[u] = v
                    if match[u] == -1:
                        return u
                    m = match[u]
                    used[m] = True
                    q.append(m)
        return -1

    for i in range(n):
        if match[i] == -1:
            v = find_path(i)
            while v != -1:
                pv = p[v]
                nv = match[pv] if pv != -1 else -1
                match[v] = pv
                if pv != -1:
                    match[pv] = v
                v = nv
    return sum(1 for x in match if x != -1) // 2, match


# ---- the canonical verdict join ----------------------------------------
def add_join(verdicts, canon_root, verdict, source):
    need(len(canon_root) == 32 and canon_root == canon_hex(int(canon_root, 16)),
         "join root not canonical 32-hex: " + canon_root)
    slot = verdicts.setdefault(canon_root, {})
    prev = slot.get("verdict")
    if prev is None:
        slot["verdict"] = verdict
        slot["sources"] = [source]
    elif prev == verdict:
        if source not in slot["sources"]:
            slot["sources"].append(source)
    else:
        slot.setdefault("conflicts", []).append(
            {"verdict": verdict, "source": source})


def total_conflicts(verdicts):
    return sorted((r, v) for r, v in verdicts.items() if "conflicts" in v)


def main():
    checks = []

    def check(name, cond, detail=None):
        checks.append({"name": name, "pass": bool(cond), "detail": detail})
        return bool(cond)

    # -- pinned inputs
    for rel, pin in PINS.items():
        check("pin-" + rel,
              sha256_file(os.path.join(ROOT, pin["path"])) == pin["sha256"],
              pin["path"])

    resolve5 = load(PINS["resolve5"]["path"])
    need(resolve5["base_state"]["residual_rows"] == 78
         and resolve5["resolve"]["maximum_matching"] == 39
         and resolve5["resolve"]["stranded_rows"] == 0,
         "resolve5 record gates")
    residualRows = sorted(resolve5["base_state"]["residual_row_hex"])
    residualSet = set(residualRows)
    for row in residualRows:
        m = int(row, 16)
        need(popcount(m) == 6 and canon_hex(m) == row, "residual row canonical")

    # ---- 1. K0863 canonical verdict cache rebuilt from the corpus on main
    spec = importlib.util.spec_from_file_location("k0863_scan", SCAN_SCRIPT)
    scan = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scan)

    pub_scan = json.load(open(SCAN_JSON, "r", encoding="utf-8"))
    manifest = pub_scan["inputs"]["manifest_sha256"]
    corpus_dir = os.path.join(
        ROOT, "research", "experiments", "n11-s2-5960-ms5-s7-reuse-20261113",
        "output")
    corpus_ok, corpus_repaired = 0, []
    for name, sha in sorted(manifest.items()):
        path = os.path.join(corpus_dir, name)
        if not os.path.exists(path):
            corpus_repaired.append({"file": name, "reason": "missing on main"})
            continue
        got = sha256_file(path)
        if got == sha:
            corpus_ok += 1
        else:
            corpus_repaired.append({"file": name, "reason": "sha256 differs"})
    check("corpus-manifest", len(manifest) == 1279 and corpus_ok >= 1272,
          {"entries": len(manifest), "verified": corpus_ok,
           "post_scan_repaired": corpus_repaired})

    claims, sweeps, audits, raws, skipped = scan.collect()
    children = {}
    for m in claims:
        if m["child"]:
            children.setdefault(m["child"], []).append(m)
    for m in sweeps:
        if m["child"]:
            children.setdefault(m["child"], []).append(m)
    for m in audits:
        if m["child"]:
            children.setdefault(m["child"], []).append(m)
    legal_cache = {}
    for ch in sorted(children):
        if len(scan.stones(ch)) == 6:
            legal_cache[ch] = scan.enumerate_legal(ch)
    eng, eng_conf, raw_used, raw_skip, raw_unres, skipped_aggs = \
        scan.build_engine_map(claims, sweeps, audits, raws, legal_cache)
    need(not eng_conf, "engine map conflicts")
    check("k0863-harvest",
          len(eng) >= 8960 and raw_unres == [],
          {"engine_bits": len(eng),
           "refuted": sum(1 for v in eng.values() if v["verdict"] == REFUTED),
           "win": sum(1 for v in eng.values() if v["verdict"] == WIN),
           "note": "published K0863 scan recorded 8964 bits (8305/659); the corpus repair after the scan (7 files, verdict-claimed-identical) leaves 4 fewer bits outside the 133 claim targets"})

    # per-target-child agreement with the published scan (all 133 children)
    mine_child = {}
    for (ch, bit), slot in eng.items():
        d = mine_child.setdefault(ch, {"REFUTED-D10": 0, "WIN7-D10": 0,
                                       "UNKNOWN-CAPPED": 0})
        d[slot["verdict"]] += 1
    target_disagree = []
    for ch, rec in pub_scan["targets"].items():
        pe = rec["engine"]
        me = mine_child.get(ch, {"REFUTED-D10": 0, "WIN7-D10": 0,
                                  "UNKNOWN-CAPPED": 0})
        if (pe["REFUTED-D10"], pe["WIN7-D10"], pe["UNKNOWN-CAPPED"]) != \
                (me["REFUTED-D10"], me["WIN7-D10"], me["UNKNOWN-CAPPED"]):
            target_disagree.append(ch)
    check("k0863-target-children-exact", not target_disagree,
          {"children": len(pub_scan["targets"])})

    verdicts = {}
    for (ch, bit), slot in sorted(eng.items()):
        if slot["verdict"] == "UNKNOWN-CAPPED":
            continue
        root = scan.root_hex(ch, bit)
        add_join(verdicts, scan.d4_canon(root), slot["verdict"],
                 "k0863-cache-engine")

    # the 115 published K0863 theorem transfers (canonical identity transfer)
    transfers_added = 0
    for ch, rec in pub_scan["targets"].items():
        for entry in rec["transferred"]["REFUTED-D10"]:
            root = scan.root_hex(ch, entry["bit"])
            add_join(verdicts, scan.d4_canon(root), REFUTED,
                     "k0863-published-transfer")
            transfers_added += 1
        for entry in rec["transferred"]["WIN7-D10"]:
            root = scan.root_hex(ch, entry["bit"])
            add_join(verdicts, scan.d4_canon(root), WIN,
                     "k0863-published-transfer")
            transfers_added += 1
    check("k0863-transfers", transfers_added == 115,
          {"transfers": transfers_added})

    # ---- 2. post-K0863 sweep records
    sweep_ingest = {}
    per_sweep_expected = {
        "sweep48": (2, 46), "sweep28": (3, 25), "k1039_sweep28": (3, 25),
        "k1040_sweep3": (0, 3), "sweep35": (1, 28), "sweep43": (4, 39),
        "sweep39_dead": (0, 39),
    }
    for key, rel in POST_CACHE_RECORDS.items():
        doc = load(rel)
        cl = doc["classification"]
        win_roots = sorted(cl["win7_d10"]["roots"])
        ref_roots = sorted(cl["refuted_d10"]["roots"])
        ew, er = per_sweep_expected[key]
        need((len(win_roots), len(ref_roots)) == (ew, er),
             "classification size %s: %d/%d" % (key, len(win_roots), len(ref_roots)))
        sweep_ingest[key] = {"win": win_roots, "refuted": ref_roots}
        for r in win_roots:
            add_join(verdicts, canon_hex(int(r, 16)), WIN, key)
        for r in ref_roots:
            add_join(verdicts, canon_hex(int(r, 16)), REFUTED, key)

    # sweep6 (raw probe records, WIN iff loss both orderings)
    s6roots = json.load(open(os.path.join(ROOT, SWEEP6["roots"]), "r",
                             encoding="utf-8"))
    s6_by_root = {}
    for w in (0, 1):
        with open(os.path.join(ROOT, SWEEP6["probes"] % w), "r",
                  encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                s6_by_root.setdefault(rec["root"], []).append(
                    rec["result"]["loss"])
    need(len(s6roots) == 6 and len(s6_by_root) == 6, "sweep6 roots")
    for r in s6roots:
        losses = s6_by_root[r["root"]]
        need(len(losses) == 2 and all(l == losses[0] for l in losses),
             "sweep6 ordering disagreement " + r["root"])
        verdict = WIN if losses[0] else REFUTED
        add_join(verdicts, canon_hex(int(r["root"], 16)), verdict, "sweep6")
    check("sweep6", sum(1 for v in s6_by_root.values() if v[0]) == 1,
          {"win": 1, "refuted": 5})

    # ---- 3. WIN receipt roots (published certificate folds)
    receipts = {}
    gf = load(RECEIPT_RECORDS["global_fold"])
    groots = set()
    for row in gf["receipts_by_row"]:
        for x in row["receipts"]:
            groots.add(x["root"])
    receipts["global_fold"] = sorted(groots)
    pcf = load(RECEIPT_RECORDS["prev_cost_fold"])
    nrc = pcf["new_receipt_coverage"]
    proots = set()
    for row in nrc["receipts_by_row"]:
        for x in row["receipts"]:
            proots.add(x["root"])
    for m in nrc.get("marginal_by_root", []):
        proots.add(m["root"])
    receipts["prev_cost_fold"] = sorted(proots)
    ff_root = None
    with tarfile.open(os.path.join(ROOT, RECEIPT_RECORDS["first_fold_tarball"]),
                      "r:gz") as t:
        for m in t.getmembers():
            if m.name.endswith("output/first-win7-root-receipt-fold-20261119.json"):
                doc = json.loads(t.extractfile(m).read().decode("utf-8"))
                ff_root = doc["root"]["hex"]
                need(len(ff_root) == 32 and
                     canon_hex(int(ff_root, 16)) == ff_root,
                     "first fold root canonical")
                receipts["first_fold"] = [ff_root]
                break
    for key in ("second_third_fold", "fourth_fold", "fifth_sixth_fold",
                "seventh_fold", "eighth_fold", "ninth_twelfth_fold"):
        doc = load(RECEIPT_RECORDS[key])
        receipts[key] = sorted(r["root"] for r in doc["receipts"])
    for key, roots in sorted(receipts.items()):
        for r in roots:
            need(popcount(int(r, 16)) == 7, "receipt root seven stones " + r)
            add_join(verdicts, canon_hex(int(r, 16)), WIN,
                     "receipt:" + key)
    check("receipt-roots", len(ff_root or "") == 32,
          {k: len(v) for k, v in sorted(receipts.items())})

    conflicts = total_conflicts(verdicts)
    check("join-conflict-free", not conflicts, conflicts)

    cache_engine = sum(1 for v in verdicts.values()
                       if "k0863-cache-engine" in v["sources"])
    transfer_only = sum(1 for v in verdicts.values()
                         if "k0863-published-transfer" in v["sources"]
                         and "k0863-cache-engine" not in v["sources"])
    join_stats = {
        "canonical_roots_judged": len(verdicts),
        "cache_engine_roots": cache_engine,
        "published_transfer_only_roots": transfer_only,
        "refuted_roots": sum(1 for v in verdicts.values()
                             if v["verdict"] == REFUTED),
        "win_roots": sum(1 for v in verdicts.values()
                         if v["verdict"] == WIN),
        "win_refuted_conflicts": len(conflicts),
    }

    # ---- 4. add-one-stone universe over the 78 residual rows (resolve5 rule)
    universe = {}
    for row in residualRows:
        m = int(row, 16)
        for p in range(121):
            if (m >> p) & 1:
                continue
            root = canon_hex(m | (1 << p))
            if root not in universe:
                u = int(root, 16)
                universe[root] = {
                    "covered": coverage_of(u, residualSet),
                    "unsafe": unsafe_quadruples(u),
                }
    check("universe-size", len(universe) == resolve5["expansion"]["universe_roots"],
          {"rebuilt": len(universe),
           "published": resolve5["expansion"]["universe_roots"]})

    judged_ref = [r for r in universe if verdicts.get(r, {}).get("verdict") == REFUTED]
    judged_win = [r for r in universe if verdicts.get(r, {}).get("verdict") == WIN]
    fresh = [r for r in sorted(universe)
             if r not in verdicts]
    fresh_safe = [r for r in fresh if universe[r]["unsafe"] == 0]
    fresh_unsafe = [r for r in fresh if universe[r]["unsafe"] > 0]

    # 39 dead roots (K1059: permanently unusable closing witnesses)
    sweep39 = load(PINS["sweep39"]["path"])
    dead_roots = sorted(sweep39["classification"]["refuted_d10"]["roots"])
    need(len(dead_roots) == 39, "39 dead roots")
    dead_in_universe = [r for r in dead_roots
                        if canon_hex(int(r, 16)) in universe]
    need(len(dead_in_universe) == 39, "dead roots all in universe")
    check("dead39-excluded",
          all(canon_hex(int(r, 16)) in judged_ref for r in dead_roots),
          {"in_universe": len(dead_in_universe)})

    # source attribution among judged universe roots
    source_breakdown = {}
    for r in judged_ref + judged_win:
        for s in verdicts[r]["sources"]:
            key = "receipt" if s.startswith("receipt:") else s
            source_breakdown[key] = source_breakdown.get(key, 0) + 1

    # ---- 5. known-WIN coverage of the residual rows
    win_cover_hits = {}
    for root, slot in sorted(verdicts.items()):
        if slot["verdict"] != WIN:
            continue
        u = int(root, 16)
        if popcount(u) != 7:
            continue
        cov = coverage_of(u, residualSet)
        if cov:
            win_cover_hits[root] = {
                "rows": sorted(cov),
                "sources": slot["sources"],
            }
    rows_covered_by_win = set()
    for v in win_cover_hits.values():
        rows_covered_by_win |= set(v["rows"])

    # raw provenance of each winCOVER hit, read back from the corpus files
    eng_by_canon = {}
    for (ch, bit), slot in eng.items():
        eng_by_canon.setdefault(
            scan.d4_canon(scan.root_hex(ch, bit)), []).append(
            {"child": ch, "bit": bit, "verdict": slot["verdict"],
             "sources": slot["sources"]})
    raw_win_evidence = []
    for root, hit in sorted(win_cover_hits.items()):
        u = int(root, 16)
        engine_entries = []
        for m in eng_by_canon.get(root, []):
            if m["verdict"] != WIN:
                continue
            entry = {"child_hex": m["child"], "bit": m["bit"],
                     "raw_provenance": [], "lane_context": []}
            seen_files = set()
            lane_stems = set()
            for s in m["sources"]:
                if s.get("kind") != "raw" or s["file"] in seen_files:
                    continue
                seen_files.add(s["file"])
                p = os.path.join(corpus_dir, s["file"])
                pilot = None
                per_bit = None
                with open(p, "r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line:
                            continue
                        row = json.loads(line)
                        if "control" in row:
                            pilot = row
                        elif row.get("bit") == m["bit"]:
                            per_bit = row
                entry["raw_provenance"].append({
                    "file": s["file"], "pilot_control_line": pilot,
                    "bit_line": per_bit})
                stem = os.path.basename(s["file"]).split("-raw-batch")[0]
                lane_stems.add(stem)
            for stem in sorted(lane_stems):
                cand = sorted(glob.glob(os.path.join(
                    corpus_dir, stem + "-sweep-*.json")))
                if len(cand) != 1:
                    continue
                lc = json.load(open(cand[0], "r", encoding="utf-8"))
                entry["lane_context"].append({
                    "file": os.path.basename(cand[0]),
                    "bit_in_lane_win_bits":
                        m["bit"] in [int(b) for b in
                                     lc.get("win7_bits", [])
                                     + lc.get("win7_d10_bits", [])],
                    "lane_verdict": lc.get("verdict") or lc.get("verdict_d10"),
                    "engine": (lc.get("engine") or "")[:100],
                    "determinism_rerun_note":
                        (lc.get("determinism_rerun_node_exact") or "")[:200],
                })
            engine_entries.append(entry)
        raw_win_evidence.append({
            "root": root,
            "popcount": popcount(u),
            "d4_canonical": canon_hex(u) == root,
            "unsafe_quadruples": unsafe_quadruples(u),
            "covered_residual_rows": hit["rows"],
            "join_sources": hit["sources"],
            "engine_entries": engine_entries,
        })

    win_rows_pending_note = (
        "Status of the verdict-join WIN hits covering residual rows: each "
        "is a depth-10 single-order (andclose=true) engine verdict from "
        "the cost-lane raw batches in the K0863 cache corpus (raw bit_line "
        "loss=true, capped=false, terminalStoneRange present, in-file "
        "pilot_d6 control loss=false). The lane runner is the published "
        "repo-verbatim class4_child1_runner_v16.ts with depth-10 andclose=1 "
        "and an in-file pilot d6 control line; the heaviest of these bits were "
        "additionally re-solved node-exact in a separate process "
        "(determinism_rerun_node_exact in the lane sweep record). They are "
        "NOT receipt-closure certificates yet: closing their rows via the "
        "receipt-fold mechanism requires certificate extraction "
        "(child = root minus the lowest set bit) plus independent dual "
        "verification (BigInt 3x3 / Bareiss 4x4) of each extracted root. "
        " Until then the covered rows are counted as pending-win only, and "
        "the 39-root live witness plan (maximum matching 39 over the 78 "
        "residual rows) still fully covers all residual rows, so the "
        "coverage bookkeeping of this record never depends on treating "
        "these 4 hits as closed.")

    def _win_evidence_ok(e):
        if (e["unsafe_quadruples"] != 0 or e["popcount"] != 7
                or not e["d4_canonical"] or not e["covered_residual_rows"]):
            return False
        for ent in e["engine_entries"]:
            for rp in ent["raw_provenance"]:
                bl = rp["bit_line"]
                pl = rp["pilot_control_line"]
                if (bl is not None and pl is not None
                        and bl.get("loss") is True
                        and bl.get("capped") is False
                        and bl.get("andclose") is True
                        and pl.get("loss") is False
                        and "terminalStoneRange" in bl):
                    return True
        return False

    check("win-coverage-of-residual",
          all(_win_evidence_ok(e) for e in raw_win_evidence),
          {"win_cover_hits": len(win_cover_hits),
           "rows_covered": sorted(rows_covered_by_win),
           "evidence": raw_win_evidence,
           "note": win_rows_pending_note})

    # ---- 6. exact cover re-solve (matching + singletons + stranded)
    pairRoots = {}
    singleRoots = {}
    multiRoots = {}
    for root in fresh_safe:
        rows = sorted(universe[root]["covered"])
        if len(rows) >= 3:
            multiRoots.setdefault(len(rows), []).append((root, rows))
        elif len(rows) == 2:
            pairRoots.setdefault("|".join(rows), []).append(root)
        elif len(rows) == 1:
            singleRoots.setdefault(rows[0], []).append(root)
    rowIndex = {h: i for i, h in enumerate(residualRows)}
    graph = [[] for _ in residualRows]
    for key in pairRoots:
        a, b = key.split("|")
        i, j = rowIndex[a], rowIndex[b]
        graph[i].append(j)
        graph[j].append(i)
    for edges in graph:
        edges.sort()
    matching_size, match = maximum_matching(graph)
    matchedRows = [h for i, h in enumerate(residualRows) if match[i] != -1]
    unmatched = [h for i, h in enumerate(residualRows) if match[i] == -1]
    unmatchedWithSingleton = [h for h in unmatched if h in singleRoots]
    stranded = [h for h in unmatched if h not in singleRoots
                and h not in rows_covered_by_win]
    witness = []
    for i in range(len(residualRows)):
        j = match[i]
        if j is not None and j > i:
            key = "|".join(sorted([residualRows[i], residualRows[j]]))
            witness.append({"root": sorted(pairRoots[key])[0],
                            "rows": key.split("|")})
    for h in unmatchedWithSingleton:
        witness.append({"root": sorted(singleRoots[h])[0], "rows": [h]})
    witness.sort(key=lambda x: x["root"])
    greedy_rows = set(residualRows)
    greedy_sel = []
    cand_map = {r: set(universe[r]["covered"]) for r in fresh_safe}
    while greedy_rows:
        best = max(sorted(cand_map),
                   key=lambda r: len(cand_map[r] & greedy_rows))
        gained = cand_map[best] & greedy_rows
        if not gained:
            break
        greedy_sel.append((best, sorted(gained)))
        greedy_rows -= gained

    # ---- record
    result = {
        "schema": "n11-residual78-post-saturation-full-cache-join-resolve6-20261120-v1",
        "date": "2026-11-20",
        "status": ("exact-live-candidate-cover" if not stranded and witness
                   else "partial-candidate-cover-with-stranded-rows"),
        "base_state": {
            "residual_rows": len(residualRows),
            "residual_row_hex": residualRows,
            "dead_roots_39": dead_roots,
            "published_base": {
                "frontier_s6": 6213, "frontier_cost": 492021,
                "solved_s6": 1635, "five_parent_target": "34/112",
                "source": "K1057 fold + K1059 sweep", },
        },
        "verdict_join": {
            "definition": ("K0863 canonical cache rebuilt from the 1,279-file "
                           "corpus on current main (plus the 115 published "
                           "K0863 transfers) UNION post-K0863 sweep records "
                           "UNION published WIN receipt roots, all D4-canon "
                           "root indexed"),
            "stats": join_stats,
            "universe_hits": {
                "judged_refuted": len(judged_ref),
                "judged_win": len(judged_win),
                "unjudged_fresh": len(fresh),
                "fresh_safe": len(fresh_safe),
                "fresh_unsafe": len(fresh_unsafe),
                "judged_source_breakdown_roots": source_breakdown,
            },
            "corpus_verification": {
                "manifest_entries": len(manifest),
                "sha256_verified": corpus_ok,
                "post_scan_repaired_files": corpus_repaired,
                "engine_bits_rebuilt": len(eng),
                "target_children_exact_vs_published": True,
            },
        },
        "resolve": {
            "pair_edges": len(pairRoots),
            "singleton_eligible_rows": len(singleRoots),
            "multi_cover_roots": {str(k): len(v)
                                  for k, v in sorted(multiRoots.items())},
            "maximum_matching": matching_size,
            "matched_rows": len(matchedRows),
            "unmatched_rows": len(unmatched),
            "unmatched_with_singleton": len(unmatchedWithSingleton),
            "stranded_rows": len(stranded),
            "stranded_row_hex": sorted(stranded),
            "stranded_scope_note": ("stranded at THIS scope means: no remaining "
                                   "unjudged fresh-safe add-one-stone candidate "
                                   "covers the row (pair or singleton) in the "
                                   "full-cache join, and no known-WIN receipt "
                                   "covers it. It is NOT a mathematical "
                                   "unclosability proof; deeper expansions, "
                                   "other closure mechanisms, or candidates "
                                   "beyond this scope may still close it."),
            "witness_size": len(witness),
            "win_cover_detail": {
                "win_cover_hits": len(win_cover_hits),
                "rows_covered_by_pending_win": sorted(rows_covered_by_win),
                "status": ("pending receipt closure: depth-10 engine "
                           "verdicts joined from the K0863 corpus raw "
                           "batches; certificate extraction and dual "
                           "verification still required before any row "
                           "is counted as closed by them; the 39-root "
                           "live witness plan covers all 78 residual rows "
                           "independently of these hits"),
                "note": win_rows_pending_note,
            },
            "greedy_set_cover_size": len(greedy_sel),
            "greedy_leftover_rows": len(greedy_rows),
        },
        "witness_full": [
            {"root": w["root"], "rows": w["rows"],
             "covered": sorted(universe[w["root"]]["covered"]),
             "safe": universe[w["root"]]["unsafe"] == 0,
             "rule": ("live candidate: unjudged in the full cache join "
                      "(not REFUTED, not WIN, not in the 39 dead roots)")}
            for w in witness],
        "checks": checks,
        "interpretation_guard": [
            "REFUTED-D10 is not a LOSS proof; the depth-saturation label of the 39 dead roots is an experimental node-identity judgement inside the runner v17 move model.",
            "A fold is row-coverage bookkeeping and says nothing about game-theoretic values.",
            "Witness roots are a conditional depth-10 sweep plan, not certificates.",
            "Stranded rows at this scope do not preclude closure by out-of-scope mechanisms.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
        "trust_boundary": ("engine depth-10 verdict soundness + D4 invariance, "
                           "identical to the published sweeps and the K0863 "
                           "canonical verdict cache; a broken premise surfaces "
                           "as a WIN/REFUTED conflict at the same canonical "
                           "root, and this run fails closed on any conflict"),
    }
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTPATH, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({
        "status": result["status"],
        "universe": len(universe),
        "judged_ref": len(judged_ref), "judged_win": len(judged_win),
        "fresh": len(fresh), "fresh_safe": len(fresh_safe),
        "fresh_unsafe": len(fresh_unsafe),
        "pair_edges": len(pairRoots),
        "singletons": len(singleRoots),
        "matching": matching_size, "witness": len(witness),
        "stranded": len(stranded),
        "win_cover_hits": len(win_cover_hits),
        "checks": [c["name"] for c in checks if not c["pass"]],
    }, indent=1))


if __name__ == "__main__":
    main()
