#!/usr/bin/env python3
"""n11-residual72-full-cache-join-candidate-supply-20261120.

Single-owner lane (published single-owner note
research/log/2026-11-20-n11-residual72-candidate-supply-single-owner-note.md):
candidate-supply rebuild for the residual 72 five-parent target rows.
Complements the published-records-only resolve7 (K1072), which proved the
retired 39-root live witness plan supplies zero further depth-10 witnesses;
this machine rebuilds the full resolve6 universe and quantifies what remains.

Stage 1 (verbatim resolve6): rebuilds the published resolve6 (K1063-era)
canonical verdict cache and its full cache join from the on-main corpus and
records; the rebuilt join stats, universe hits and win-coverage rows must
byte-match the sha256-pinned published resolve6 record before anything
downstream is trusted.
Stage 2 adds the post-resolve6 published sources: the four windfall receipts
(fold9, thirteenth..sixteenth), the seventeenth receipt (fold10, triple
verification) and the 39-live-root both-order depth-10 sweep classification
(K1069), conflict-gated fail-closed at canonical-root level.
Stage 3 rebuilds the add-one-stone universe over the residual 72 rows
(78 - 4 windfall target rows - 2 seventeenth target rows, exact-match gated
against the pinned fold9/fold10/sv17 records, geometry rederivation of every
closed row), classifies the fresh-safe candidate pool, and re-solves the
maximum matching over the 72 rows.
Stage 4 publishes the candidate supply itself: per-row demand, pair/singleton
structure, the fresh witness plan it implies, windfall-type (corpus judged
WIN, unreceipted) 18th-certificate candidates with raw provenance, and
receipted-WIN coverage of still-open rows (free-fold supply), plus a
geometric recheck of the published resolve7 post-retire assignment
(34 x 2 + 4 x 1 over the same 72 rows) as an independent cross-lane gate.

Interpretation guard: REFUTED-D10 is not a LOSS proof; folds are row-coverage
bookkeeping; witness roots are a conditional plan, not certificates; the
residual 72 rows, the two-stone roots {49,60}/{59,60}, S2 {59,60}, classes
1/2/4 and the standard 11x11 empty board all remain UNKNOWN.

Determinism: stdlib only; two runs in separate processes/cwds produce
byte-identical output.
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
OUTPATH = os.path.join(OUTDIR, "residual72-full-cache-join-candidate-supply-20261120.json")

SCAN_DIR = os.path.join(ROOT, "research", "experiments",
                        "n11-class2-lane-sterile-unclosability-20261116")
SCAN_JSON = os.path.join(SCAN_DIR, "output",
                         "theorem-applicability-scan-20261116.json")
SCAN_SCRIPT = os.path.join(SCAN_DIR, "theorem_applicability_scan_20261116.py")

REFUTED = "REFUTED-D10"
WIN = "WIN7-D10"

# ---- published pins (sha256, fail-closed) -------------------------------
PINS = {
    "resolve5": {
        "path": "research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/fold/output/post-twelfth-receipt-cover-resolve5-20261119.json",
        "sha256": "5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e",
    },
    "sweep39": {
        "path": "research/experiments/n11-residual78-39witness-depth10-sweep-20261119/output/witness-39-root-depth10-sweep-20261119.json",
        "sha256": "f8608d0a04a132012f0aa692099cebe851cdf261a3ea916dc4c15d6841fc5246",
    },
    "resolve6out": {
        "path": "research/experiments/n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json",
        "sha256": "e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a",
    },
    "windfall4": {
        "path": "research/experiments/n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json",
        "sha256": "24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2",
    },
    "seventeenth_fold": {
        "path": "research/experiments/n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json",
        "sha256": "bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a",
    },
    "seventeenth_verify": {
        "path": "research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/output/seventeenth-cert-triple-verification-20261120.json",
        "sha256": "c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc",
    },
    "sweep39_live": {
        "path": "research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json",
        "sha256": "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc",
    },
    "resolve7out": {
        "path": "research/experiments/n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json",
        "sha256": "207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f",
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

    # ---- 5.5 stage-1 reproduction gates against the published resolve6 record
    need(all(c["pass"] for c in checks if c["name"].startswith("pin-")),
         "input sha256 pins")
    r6pub = load(PINS["resolve6out"]["path"])
    need(r6pub["status"] == "exact-live-candidate-cover"
         and r6pub["resolve"]["stranded_rows"] == 0,
         "published resolve6 status")
    need(sorted(r6pub["base_state"]["residual_row_hex"]) == residualRows,
         "resolve6 published rows == resolve5 residual rows")
    need(join_stats == r6pub["verdict_join"]["stats"],
         "stage-1 rebuilt join stats == published resolve6")
    uh = r6pub["verdict_join"]["universe_hits"]
    need((len(judged_ref), len(judged_win), len(fresh), len(fresh_safe),
          len(fresh_unsafe)) ==
         (uh["judged_refuted"], uh["judged_win"], uh["unjudged_fresh"],
          uh["fresh_safe"], uh["fresh_unsafe"]),
         "stage-1 universe hits == published resolve6")
    need(source_breakdown == uh["judged_source_breakdown_roots"],
         "stage-1 source breakdown == published resolve6")
    wcd = r6pub["resolve"]["win_cover_detail"]
    need(len(win_cover_hits) == wcd["win_cover_hits"]
         and sorted(rows_covered_by_win) == sorted(wcd["rows_covered_by_pending_win"]),
         "stage-1 win cover hits == published resolve6")
    pub_witness39 = [w["root"] for w in r6pub["witness_full"]]
    need(len(pub_witness39) == 39 and len(set(pub_witness39)) == 39,
         "published resolve6 witness 39 live roots")
    check("stage1-reproduction-vs-published-resolve6", True,
          {"join_stats": join_stats,
           "universe_hits": {"judged_refuted": len(judged_ref),
                             "judged_win": len(judged_win),
                             "unjudged_fresh": len(fresh),
                             "fresh_safe": len(fresh_safe),
                             "fresh_unsafe": len(fresh_unsafe)},
           "win_cover_hits": len(win_cover_hits),
           "witness_39_live_roots": len(pub_witness39)})

    # ---- 5.6 fold9 / fold10 / sv17 / live-sweep / resolve7 pinned records
    wf4 = load(PINS["windfall4"]["path"])
    f10 = load(PINS["seventeenth_fold"]["path"])
    sv17 = load(PINS["seventeenth_verify"]["path"])
    live39 = load(PINS["sweep39_live"]["path"])
    r7pub = load(PINS["resolve7out"]["path"])
    need(wf4["status"] == "fold-complete" and wf4["receipt_count"] == 4,
         "windfall4 fold record")
    need(f10["status"] == "fold-complete" and f10["receipt_count"] == 1,
         "seventeenth fold record")

    # windfall provenance: fold9 receipts are exactly the resolve6 win hits
    wf4_roots = []
    for rec in wf4["receipts"]:
        need(popcount(int(rec["root"], 16)) == 7,
             "windfall receipt seven stones " + rec["root"])
        canon = canon_hex(int(rec["root"], 16))
        need(rec.get("canonical_root_hex", canon) == canon,
             "windfall canonical root pin " + rec["root"])
        add_receipt = {"root": rec["root"], "canon": canon}
        wf4_roots.append(canon)
    wf4_roots = sorted(wf4_roots)
    need(len(wf4_roots) == 4 and len(set(wf4_roots)) == 4,
         "four windfall receipt roots")
    need(wf4_roots == sorted(win_cover_hits),
         "fold9 receipt roots == resolve6 win cover hits")

    # closed target rows (geometry rederivation, fold9)
    close4 = set()
    for rec in wf4["receipts"]:
        for r in rec["covered_five_parent_target_rows"]:
            close4.add(r)
    rows4 = {row["row_hex"] for row in wf4["new_receipt_coverage"]["rows"]}
    need(len(close4) == 4 and rows4 == close4 and close4 <= residualSet,
         "windfall4 closed rows: 4 rows, coverage record match, inside 78")
    for rec in wf4["receipts"]:
        cov = coverage_of(int(rec["root"], 16), residualSet)
        need(set(rec["covered_five_parent_target_rows"]) <= cov,
             "windfall geometry rederivation " + rec["root"])
    residualRows74 = [r for r in residualRows if r not in close4]
    need(len(residualRows74) == 74
         and residualRows74 == sorted(wf4["five_parent_target_after"]["residual_row_hex_after"]),
         "residual 74 == fold9 residual list")
    set74 = set(residualRows74)

    # closed target rows (geometry rederivation, fold10 / seventeenth)
    s17 = f10["receipts"][0]
    need(s17["receipt"] == "seventeenth"
         and popcount(int(s17["root"], 16)) == 7
         and s17["raw_root_is_d4_canonical"] is True
         and canon_hex(int(s17["root"], 16)) == s17["root"],
         "seventeenth receipt root canonical seven stones")
    s17_canon = canon_hex(int(s17["root"], 16))
    close2 = set(s17["covered_five_parent_target_rows"])
    need(len(close2) == 2 and close2 <= set74,
         "seventeenth two target rows inside residual 74")
    cov17_all = coverage_of(int(s17["root"], 16), set74)
    need(close2 <= cov17_all, "seventeenth geometry rederivation")
    need(len(s17["covered_s6_rows"]) == 3, "seventeenth covers 3 s6 rows")
    extras17 = set(s17["covered_s6_rows"]) - close2
    need(len(extras17) == 1 and not (extras17 & residualSet),
         "seventeenth extra row outside the 78-row plan")
    need(sorted(sv17["coverage_claim_pending_fold"]["covered_rows_per_resolve6_matching"])
         == sorted(close2), "sv17 coverage claim == fold10 target rows")
    need(sv17["gates_all_pass"] is True and sv17["gates_total"] == 38
         and sv17["root_hex"] == s17["root"]
         and sv17["certificate"]["sha256"] == s17["certificate_sha256"],
         "sv17 triple-verification record cross pins")
    residualRows72 = [r for r in residualRows74 if r not in close2]
    need(len(residualRows72) == 72
         and residualRows72 == sorted(f10["five_parent_target_after"]["residual_row_hex_after"]),
         "residual 72 == fold10 residual list")
    residualSet72 = set(residualRows72)
    for row in residualRows72:
        m = int(row, 16)
        need(popcount(m) == 6 and canon_hex(m) == row, "residual72 row canonical")
    check("residual72-derivation-exact", True,
          {"resolve5_rows": len(residualRows),
           "minus_windfall4_target_rows": len(close4),
           "minus_seventeenth_target_rows": len(close2),
           "residual": len(residualRows72)})
    need(r7pub["gates_all_pass"] is True and r7pub["gates_total"] == 27,
         "resolve7 published recheck gates")

    # ---- 5.7 phase-2 join: post-resolve6 published sources, fail-closed
    verdicts2 = {r: {"verdict": v["verdict"], "sources": list(v["sources"])}
                 for r, v in verdicts.items()}
    for canon in wf4_roots:
        add_join(verdicts2, canon, WIN, "receipt:windfall4_13_16")
    add_join(verdicts2, s17_canon, WIN, "receipt:seventeenth")
    live38_roots = []
    live_win_roots = []
    for rawr, v in sorted(live39["classification"].items()):
        need(v in (WIN, REFUTED), "live classification verdict " + rawr)
        c = canon_hex(int(rawr, 16))
        add_join(verdicts2, c, v, "sweep39_live_k1069")
        if v == WIN:
            live_win_roots.append(c)
        else:
            live38_roots.append(c)
    need(len(live39["classification"]) == 39
         and len(live38_roots) == 38 and len(live_win_roots) == 1,
         "39 live roots classified 1 WIN / 38 REFUTED")
    need(live_win_roots == [s17_canon], "live WIN root == seventeenth receipt root")
    ls = live39["summary"]
    need(ls["win"] == 1 and ls["refuted"] == 38 and ls["capped"] == 0
         and ls["order_conflicts"] == 0,
         "live sweep summary 1/38/0, zero order conflicts")
    need(len(live39["protocol"]["orderings"]) == 2,
         "live sweep is a two-ordering sweep")
    need(sorted(live38_roots + live_win_roots) ==
         sorted(set(canon_hex(int(r, 16)) for r in pub_witness39)),
         "live39 roots == published resolve6 witness roots")
    newly_judged = sorted(r for r in verdicts2 if r not in verdicts)
    need(len(newly_judged) == 39
         and sorted(r for r in newly_judged
                    if verdicts2[r]["verdict"] == WIN) == live_win_roots
         and sorted(r for r in newly_judged
                    if verdicts2[r]["verdict"] == REFUTED) == live38_roots,
         "newly judged roots are exactly the 39 live roots")
    conflicts2 = total_conflicts(verdicts2)
    check("phase2-join-conflict-free", not conflicts2, conflicts2)
    need(not conflicts2, "phase-2 canonical-root join conflict-free")
    cache_engine2 = sum(1 for v in verdicts2.values()
                        if "k0863-cache-engine" in v["sources"])
    transfer_only2 = sum(1 for v in verdicts2.values()
                         if "k0863-published-transfer" in v["sources"]
                         and "k0863-cache-engine" not in v["sources"])
    stats2 = {
        "canonical_roots_judged": len(verdicts2),
        "cache_engine_roots": cache_engine2,
        "published_transfer_only_roots": transfer_only2,
        "refuted_roots": sum(1 for v in verdicts2.values()
                             if v["verdict"] == REFUTED),
        "win_roots": sum(1 for v in verdicts2.values()
                         if v["verdict"] == WIN),
        "win_refuted_conflicts": len(conflicts2),
    }
    seventeenth_slot = verdicts2[s17_canon]
    need("receipt:seventeenth" in seventeenth_slot["sources"]
         and "sweep39_live_k1069" in seventeenth_slot["sources"],
         "seventeenth root is dual-sourced (receipt + live sweep)")

    # ---- 6. add-one-stone universe over the residual 72 rows
    universe72 = {}
    for row in residualRows72:
        m = int(row, 16)
        for p in range(121):
            if (m >> p) & 1:
                continue
            root = canon_hex(m | (1 << p))
            if root not in universe72:
                u = int(root, 16)
                universe72[root] = {
                    "covered": coverage_of(u, residualSet72),
                    "unsafe": unsafe_quadruples(u),
                }
    sub_bad = [r for r in universe72
               if r not in universe
               or universe[r]["unsafe"] != universe72[r]["unsafe"]]
    cov_bad = [r for r in universe72
               if not (universe72[r]["covered"] <= universe[r]["covered"])]
    need(not sub_bad, "universe72 is an unsafe-equal subuniverse of universe78")
    need(not cov_bad, "universe72 coverages are subsets of universe78 coverages")
    check("universe72-subset-of-universe78", True,
          {"rebuilt72": len(universe72), "universe78": len(universe)})

    judged_ref2 = [r for r in sorted(universe72)
                   if verdicts2.get(r, {}).get("verdict") == REFUTED]
    judged_win2 = [r for r in sorted(universe72)
                   if verdicts2.get(r, {}).get("verdict") == WIN]
    fresh2 = [r for r in sorted(universe72) if r not in verdicts2]
    fresh_safe2 = [r for r in fresh2 if universe72[r]["unsafe"] == 0]
    fresh_unsafe2 = [r for r in fresh2 if universe72[r]["unsafe"] > 0]

    # old dead-39 and retired live-39 accounting inside the 72-row universe
    dead_in_72 = [canon_hex(int(r, 16)) for r in dead_roots
                  if canon_hex(int(r, 16)) in universe72]
    live38_in_u72 = [r for r in live38_roots if r in universe72]
    live38_killed_open_supply = [r for r in live38_in_u72
                                 if universe72[r]["covered"]]
    need(all(verdicts2[canon_hex(int(r, 16))]["verdict"] == REFUTED
             for r in dead_roots), "dead39 stay REFUTED in phase-2 join")
    check("live39-supply-status", True,
          {"live38_in_universe72": len(live38_in_u72),
           "live38_killed_open_72row_supply": len(live38_killed_open_supply),
           "retired_win_root_in_universe72": s17_canon in universe72,
           "dead39_in_universe72": len(dead_in_72)})

    # ---- 7. WIN candidate supply over residual 72
    receipt_roots2 = set(r for r, v in verdicts2.items()
                         if any(s.startswith("receipt:") for s in v["sources"]))
    win_hits72 = {}
    for root, slot in sorted(verdicts2.items()):
        if slot["verdict"] != WIN:
            continue
        u = int(root, 16)
        if popcount(u) != 7:
            continue
        cov = coverage_of(u, residualSet72)
        if cov:
            win_hits72[root] = {"rows": sorted(cov), "sources": slot["sources"]}
    windfall_cands = sorted(r for r in win_hits72 if r not in receipt_roots2)
    receipted_open = sorted(r for r in win_hits72 if r in receipt_roots2)

    def build_evidence(hit_map):
        out = []
        for root, hit in sorted(hit_map.items()):
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
            out.append({
                "root": root,
                "popcount": popcount(u),
                "d4_canonical": canon_hex(u) == root,
                "unsafe_quadruples": unsafe_quadruples(u),
                "covered_residual_rows": hit["rows"],
                "join_sources": hit["sources"],
                "engine_entries": engine_entries,
            })
        return out

    windfall_evidence = build_evidence({r: win_hits72[r] for r in windfall_cands})

    def split_sources(slot_sources):
        kinds = set()
        for s in slot_sources:
            if s.startswith("receipt:"):
                kinds.add("receipt")
            elif s in ("k0863-cache-engine",):
                kinds.add("corpus-raw")
            elif s == "k0863-published-transfer":
                kinds.add("published-transfer")
            else:
                kinds.add("sweep-record")
        return sorted(kinds)

    windfall_supply = []
    for e in windfall_evidence:
        kinds = split_sources(e["join_sources"])
        ev_ok = _win_evidence_ok(e)
        need("receipt" not in kinds, "windfall candidate must be unreceipted")
        need(ev_ok or kinds == ["published-transfer"]
             or kinds == ["sweep-record"] or "published-transfer" in kinds,
             "windfall candidate evidence kind " + e["root"])
        windfall_supply.append({
            "root": e["root"],
            "covered_open_72_rows": e["covered_residual_rows"],
            "unsafe_quadruples": e["unsafe_quadruples"],
            "join_source_kinds": kinds,
            "raw_evidence_ok": ev_ok,
            "engine_entries": e["engine_entries"],
            "note": ("windfall-type candidate (unreceipted joined WIN covering "
                     "open residual-72 rows); NOT a receipt closure; certificate "
                     "extraction (child = root minus lowest set bit) plus "
                     "independent dual verification still required"),
        })
    receipted_free_fold_supply = []
    for root in receipted_open:
        receipted_free_fold_supply.append({
            "root": root,
            "covered_open_72_rows": win_hits72[root]["rows"],
            "receipt_sources": [s for s in win_hits72[root]["sources"]
                                if s.startswith("receipt:")],
            "other_sources": [s for s in win_hits72[root]["sources"]
                              if not s.startswith("receipt:")],
            "note": ("already-receipted WIN certificate still covering open "
                     "residual-72 rows: candidate zero-cost fold coverage "
                     "pending a receipt fold entry"),
        })
    rows_covered_by_pending_win72 = set()
    for r in windfall_cands:
        rows_covered_by_pending_win72 |= set(win_hits72[r]["rows"])
    check("win-supply-72", not windfall_supply or
          all(w["raw_evidence_ok"] for w in windfall_supply
              if "corpus-raw" in w["join_source_kinds"]),
          {"windfall_18th_candidates": len(windfall_cands),
           "receipted_win_covering_open_rows": len(receipted_open)})

    # ---- 8. pair structure / matching / stranded / witness over 72
    pairRoots72 = {}
    singleRoots72 = {}
    multiRoots72 = {}
    for root in fresh_safe2:
        rows = sorted(universe72[root]["covered"])
        if len(rows) >= 3:
            multiRoots72.setdefault(len(rows), []).append((root, rows))
        elif len(rows) == 2:
            pairRoots72.setdefault("|".join(rows), []).append(root)
        elif len(rows) == 1:
            singleRoots72.setdefault(rows[0], []).append(root)
    rowIndex72 = {h: i for i, h in enumerate(residualRows72)}
    graph72 = [[] for _ in residualRows72]
    for key in pairRoots72:
        a, b = key.split("|")
        i, j = rowIndex72[a], rowIndex72[b]
        graph72[i].append(j)
        graph72[j].append(i)
    for edges in graph72:
        edges.sort()
    matching_size72, match72 = maximum_matching(graph72)
    matchedRows72 = [h for i, h in enumerate(residualRows72) if match72[i] != -1]
    unmatched72 = [h for i, h in enumerate(residualRows72) if match72[i] == -1]
    unmatchedWithSingleton72 = [h for h in unmatched72 if h in singleRoots72]
    stranded72 = [h for h in unmatched72 if h not in singleRoots72
                  and h not in rows_covered_by_pending_win72]
    witness72 = []
    for i in range(len(residualRows72)):
        j = match72[i]
        if j is not None and j > i:
            key = "|".join(sorted([residualRows72[i], residualRows72[j]]))
            witness72.append({"root": sorted(pairRoots72[key])[0],
                              "rows": key.split("|")})
    for h in unmatchedWithSingleton72:
        witness72.append({"root": sorted(singleRoots72[h])[0], "rows": [h]})
    witness72.sort(key=lambda x: x["root"])
    rows_covered_by_fresh_safe72 = set()
    for r in fresh_safe2:
        rows_covered_by_fresh_safe72 |= universe72[r]["covered"]
    uncovered_by_pool72 = sorted(residualSet72 - rows_covered_by_fresh_safe72)
    greedy_rows72 = set(residualRows72)
    greedy_sel72 = []
    cand_map72 = {r: set(universe72[r]["covered"]) for r in fresh_safe2}
    while greedy_rows72:
        best = max(sorted(cand_map72),
                   key=lambda r: len(cand_map72[r] & greedy_rows72))
        gained = cand_map72[best] & greedy_rows72
        if not gained:
            break
        greedy_sel72.append((best, sorted(gained)))
        greedy_rows72 -= gained

    # per-row demand over the 72 residual rows
    row_demand = {}
    for row in residualRows72:
        row_demand[row] = {"fresh_safe_candidates": 0,
                           "judged_refuted_candidates": 0,
                           "judged_win_candidates_covering": 0}
    for root, meta in sorted(universe72.items()):
        covered = meta["covered"]
        if not covered:
            continue
        slot = verdicts2.get(root)
        for row in covered:
            d = row_demand[row]
            if slot is None and universe72[root]["unsafe"] == 0:
                d["fresh_safe_candidates"] += 1
            elif slot is not None:
                if slot["verdict"] == REFUTED:
                    d["judged_refuted_candidates"] += 1
                else:
                    d["judged_win_candidates_covering"] += 1
    for row, d in row_demand.items():
        d["fresh_safe_candidate_deficit"] = d["fresh_safe_candidates"] == 0

    # ---- 9. resolve7 post-retire assignment geometry recheck (cross-lane)
    pra = r7pub["recheck"]["post_retire_assignment"]["rows_per_root"]
    assigned_rows_union = set()
    geometry_bad = []
    for raw_root, rows in sorted(pra.items()):
        c = canon_hex(int(raw_root, 16))
        for row in rows:
            assigned_rows_union.add(row)
            if row not in coverage_of(int(raw_root, 16), residualSet):
                geometry_bad.append({"root": raw_root, "row": row})
    two_row_roots = [r for r, v in sorted(pra.items()) if len(v) == 2]
    one_row_roots = [r for r, v in sorted(pra.items()) if len(v) == 1]
    need(not geometry_bad, "resolve7 post-retire assignment geometry recheck")
    need(assigned_rows_union == residualSet72,
         "resolve7 assignment rows == residual 72 rows")
    need(len(two_row_roots) == 34 and len(one_row_roots) == 4,
         "resolve7 34x2 + 4x1 assignment")
    refuted_assignment_roots = [r for r in pra
                                if verdicts2[canon_hex(int(r, 16))]["verdict"] == REFUTED]
    need(len(refuted_assignment_roots) == 38,
         "all 38 post-retire assigned roots are REFUTED-D10 in the join")
    check("resolve7-postretire-geometry-recheck", True,
          {"assigned_rows_covered_geometrically": len(assigned_rows_union),
           "two_row_roots": len(two_row_roots),
           "one_row_roots": len(one_row_roots)})

    # ---- record
    result = {
        "schema": "n11-residual72-full-cache-join-candidate-supply-20261120-v1",
        "date": "2026-11-20",
        "single_owner_note": "research/log/2026-11-20-n11-residual72-candidate-supply-single-owner-note.md",
        "status": ("fresh-pool-exact-live-candidate-cover"
                   if not stranded72 and witness72
                   else "fresh-pool-partial-candidate-cover"),
        "base_state": {
            "residual_rows": len(residualRows72),
            "residual_row_hex": residualRows72,
            "derivation": ("resolve5 residual 78 minus windfall4 (fold9) 4 "
                           "target rows minus seventeenth (fold10) 2 target "
                           "rows, exact-match gated against the pinned "
                           "fold9/fold10/sv17 records with geometry "
                           "rederivation of every closed row"),
            "published_base": {
                "frontier_s6": 6206, "frontier_cost": 491497,
                "solved_s6": 1642, "five_parent_target": "40/112",
                "source": "K1071 fold10 + K1069 live sweep, published frontier"},
        },
        "verdict_join": {
            "definition": ("resolve6-verbatim canonical cache/join rebuild "
                           "(K0863 corpus + transfers + post-K0863 sweeps + "
                           "sweep6 + receipt roots, byte-stat-matched to the "
                           "pinned published resolve6 record) PLUS windfall4 "
                           "receipts + seventeenth receipt + the 39-root both-"
                           "order live depth-10 sweep classification, all "
                           "D4-canon root indexed, conflict-gated fail-closed"),
            "stats": stats2,
            "stage1_reproduction": {
                "resolve6_sha256_pin":
                    PINS["resolve6out"]["sha256"],
                "join_stats_match_published": True,
                "universe_hits_match_published": True,
                "win_cover_hits_match_published": True,
                "status": "stage-1 rebuild reproduces the published resolve6 "
                          "join exactly (all gates pass)",
            },
            "newly_judged_since_resolve6": {
                "roots": len(newly_judged),
                "win": live_win_roots,
                "refuted_38": len(live38_roots),
                "source": "sweep39_live_k1069 (two-order depth-10 sweep, "
                          "order_conflicts 0, capped 0); REFUTED-D10 is NOT "
                          "a LOSS proof",
            },
            "universe_hits_over_72": {
                "judged_refuted": len(judged_ref2),
                "judged_win": len(judged_win2),
                "unjudged_fresh": len(fresh2),
                "fresh_safe": len(fresh_safe2),
                "fresh_unsafe": len(fresh_unsafe2),
            },
            "corpus_verification": {
                "manifest_entries": len(manifest),
                "sha256_verified": 1272,
                "trust_boundary": ("the seven post-scan changed corpus files "
                                   "stay excluded exactly as in the published "
                                   "resolve6 run (recorded as missing on main); "
                                   "no verdict is taken from them"),
            },
        },
        "candidate_supply": {
            "universe72_roots": len(universe72),
            "fresh_safe_pool": len(fresh_safe2),
            "fresh_safe_72row_coverage": sorted(rows_covered_by_fresh_safe72),
            "rows_uncovered_by_fresh_safe_pool": uncovered_by_pool72,
            "pair_edges": len(pairRoots72),
            "singleton_eligible_rows": len(singleRoots72),
            "multi_cover_roots": {str(k): len(v)
                                  for k, v in sorted(multiRoots72.items())},
            "maximum_matching": matching_size72,
            "matched_rows": len(matchedRows72),
            "unmatched_rows": len(unmatched72),
            "unmatched_with_singleton": len(unmatchedWithSingleton72),
            "stranded_rows": len(stranded72),
            "stranded_row_hex": sorted(stranded72),
            "stranded_scope_note": ("stranded at THIS scope means: no unjudged "
                                    "fresh-safe add-one-stone candidate covers "
                                    "the row (pair or singleton) in the phase-2 "
                                    "full-cache join over residual 72, and no "
                                    "pending unreceipted WIN covers it. It is "
                                    "NOT an unclosability proof; multi-cover "
                                    "fresh-safe candidates, unsafe candidates, "
                                    "add-two-stones expansion, deeper search or "
                                    "other closure mechanisms may still close "
                                    "it."),
            "witness_size": len(witness72),
            "witness_rule": ("live fresh-safe candidate of the phase-2 join: "
                             "unjudged after corpus + sweeps + sweep39_live; "
                             "not REFUTED, not WIN, not a retired root; "
                             "a conditional depth-10 sweep plan, NOT a "
                             "certificate"),
            "greedy_set_cover_size": len(greedy_sel72),
            "greedy_leftover_rows": len(greedy_rows72),
            "row_demand": row_demand,
            "windfall_18th_certificate_candidates": windfall_supply,
            "receipted_win_covering_open_rows": receipted_free_fold_supply,
            "live38_killed_open_72row_supply": {
                "count": len(live38_killed_open_supply),
                "roots": live38_killed_open_supply,
                "note": ("these 38 retired live roots were fresh candidates "
                         "covering open residual-72 rows before the K1069 "
                         "live sweep judged them REFUTED-D10; REFUTED-D10 is "
                         "not a LOSS proof"),
            },
        },
        "witness_full": [
            {"root": w["root"], "rows": w["rows"],
             "covered": sorted(universe72[w["root"]]["covered"]),
             "safe": universe72[w["root"]]["unsafe"] == 0,
             "rule": ("live candidate: unjudged in the phase-2 full cache "
                      "join over residual 72 (not REFUTED, not WIN, not a "
                      "retired/dead root)")}
            for w in witness72],
        "resolve7_cross_check": {
            "record_sha256": PINS["resolve7out"]["sha256"],
            "post_retire_assignment_geometry_recheck": True,
            "assignment_34x2_plus_4x1": True,
            "k1069_plan_supply_zero_confirmed": ("the retired 39-root plan "
                                                 "supplies no depth-10 witness "
                                                 "for any of the 72 rows; the "
                                                 "fresh pool above is the "
                                                 "supply that remains"),
        },
        "checks": checks,
        "interpretation_guard": [
            "REFUTED-D10 is not a LOSS proof; depth-10 saturation labels are experimental node-identity judgements inside the runner v16/v17 move model.",
            "A fold is row-coverage bookkeeping and says nothing about game-theoretic values.",
            "Windfall candidates and witness roots are conditional depth-10 plans, not certificates; closure requires certificate extraction plus independent dual verification.",
            "Stranded rows at this scope do not preclude closure by multi-cover candidates, unsafe candidates, add-two-stones expansion, deeper search or other out-of-scope mechanisms.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
        "trust_boundary": ("engine depth-10 verdict soundness + D4 invariance, "
                           "identical to the published resolve6 join plus the "
                           "pinned fold9/fold10/sv17/live-sweep records; a "
                           "broken premise surfaces as a WIN/REFUTED conflict "
                           "at the same canonical root, and this run fails "
                           "closed on any conflict; stage-1 must reproduce the "
                           "published resolve6 stats exactly or the run aborts"),
    }
    os.makedirs(OUTDIR, exist_ok=True)
    with open(OUTPATH, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({
        "status": result["status"],
        "universe72": len(universe72),
        "judged_ref2": len(judged_ref2), "judged_win2": len(judged_win2),
        "fresh2": len(fresh2), "fresh_safe2": len(fresh_safe2),
        "pair_edges": len(pairRoots72),
        "singletons": len(singleRoots72),
        "matching": matching_size72, "witness": len(witness72),
        "stranded": len(stranded72),
        "uncovered_by_pool": len(uncovered_by_pool72),
        "greedy": len(greedy_sel72), "greedy_leftover": len(greedy_rows72),
        "windfall_cands": len(windfall_cands),
        "receipted_open": len(receipted_open),
        "live38_killed_supply": len(live38_killed_open_supply),
        "failed_checks": [c["name"] for c in checks if not c["pass"]],
    }, indent=1))


if __name__ == "__main__":
    main()
