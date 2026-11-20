#!/usr/bin/env python3
"""n11 residual-72 replace-9 whole-record independent second verification (2026-11-20).

Single-owner undertaking per
research/log/2026-11-20-n11-residual72-replace9-whole-record-second-verification-single-owner-note.md
(commit edc231213f). Whole-record path: this machine reads ONLY published records
(SHA-256 pinned) and re-derives every accounting and geometry fact with an
independent implementation. It does NOT run the DFPN engine; the full probe
re-execution belongs to a different single-owner lane (commit 3f34046621).

What is verified:
  * the 18 published probe records of the replace-9 sweep agree, field by field
    (nodes / loss / capped / terminalStoneRange, ms and wall_s excluded), with the
    published sweep record per_root values, including the pilot_d6 control,
    the raw-child-hex rule and both-AND-order consistency;
  * the residual row universe chain 72 -> 49 -> 40 -> 30 -> 23 is independently
    re-derived from the pinned K1085 base state plus each round's WIN8 claimed
    rows and cross-checked against the K1097 per-row ledger, the eight-root
    cover-decision universe, and the K1147 external-verification audit inputs;
  * every round's claims (WIN + REFUTED) partition the then-current residual
    universe exactly once and every claimed row is a 6-stone subset of some D4
    image of its 8-stone root (exact integer geometry, Bareiss determinants);
  * the K1097 scope1 greedy selection coincides root-by-root with the 9 swept
    roots and their claimed coverage; gains histogram {3:6, 2:2, 1:1};
  * a five-sweep cumulative verdict census: 17 WIN8-D10 candidates (52 claimed
    rows), 58 REFUTED-D10 facts, pool arithmetic safe8 120,474 - 50 - 8 = 120,416,
    D4 min-canonical uniqueness of all 75 probed roots, and a cross-sweep
    WIN-vs-REFUTED canonical conflict scan (must be 0);
  * the K1097 win16 intrinsic footprints are independently re-derived over the
    residual-72 universe, and the newest WIN candidate's intrinsic footprint is
    first-registered here for the round-5 planners.

FAIL-CLOSED: every gate must pass; any mismatch exits 1 with no output.
Deterministic: stdlib only, no randomness, no wall-clock in the audit JSON.
Three runs (same cwd twice + isolated cwd/HOME once) must be byte-identical.

REFUTED-D10 is not a LOSS proof. node counts are not win/loss evidence.
This verification closes no row and claims no game-theoretic value for any row.
The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and
classes 1/2/4 all remain UNKNOWN.

Usage:
  python3 verify_replace9_whole_record_20261120.py
"""
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
OUT = EXP / "output"
AUDIT = OUT / "replace9-whole-record-second-verification-20261120.json"
SCHEMA = "n11-residual72-replace9-whole-record-second-verification-20261120-v1"
SINGLE_OWNER_NOTE = "commit edc231213f (2026-11-20T14:29Z declaration, first-published-priority)"

PINS = {
    "k1085": "5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e",
    "k1086": "3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced",
    "k1089": "808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc",
    "k1091": "edd7ac84f47268adcc8a3364a5ff687499cb2a76ded0c0fa379506af02f40b25",
    "k1095": "335eca5ecb7c72e6fb0ee41eb740de736bf4eb78791823ae55f6375a68cb4707",
    "k1097": "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40",
    "replace9": "e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e",
    "probes": "bdacf0e7056093145bef917ad384220b70c06be68bdd892b56dd23b3a7d4cb06",
    "decision": "c5aaf83e23b6a716e981aaff745996668c60edba164fb3f5288b60ff9b8ac4d1",
    "k1147audit": "17dbd6ab3a9a9b5aef1cf1cf517a5a0fd216dff755f0ed86fcf029e1612cabcb",
}
INPUT_PATHS = {
    "k1085": OUT / ".input-k1085.json",
    "k1086": OUT / ".input-k1086.json",
    "k1089": OUT / ".input-k1089.json",
    "k1091": OUT / ".input-k1091.json",
    "k1095": OUT / ".input-k1095.json",
    "k1097": OUT / ".input-k1097.json",
    "replace9": OUT / ".input-replace9.json",
    "probes": OUT / ".input-probe-records-replace9.jsonl",
    "decision": OUT / ".input-cover-decision.json",
    "k1147audit": OUT / ".input-k1147-external-audit.json",
}
ROUND_FILES = ["k1086", "k1089", "k1091", "k1095", "replace9"]
ROUND_META = [  # (record tag, win count, refuted count, win claimed rows, residual after)
    ("k1086", 7, 16, 23, 49),
    ("k1089", 3, 13, 9, 40),
    ("k1091", 3, 12, 10, 30),
    ("k1095", 3, 9, 7, 23),
    ("replace9", 1, 8, 3, 20),
]
RUNNER_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
CAP = 30_000_000
TIMEOUT = 280
DEPTH = 10
PILOT_NODES = 3402
PILOT_LOSS = False
N = 121

GATES = []


def gate(name, ok, detail=None):
    GATES.append({"name": name, "pass": bool(ok), "detail": detail or {}})
    if not ok:
        fail_fast(name, detail)


def fail_fast(name, detail):
    print(f"GATE FAILED: {name}: {detail}", file=sys.stderr)
    print(json.dumps({"status": "FAIL", "failed_gate": name,
                      "detail": detail}, ensure_ascii=False, sort_keys=True))
    sys.exit(1)


# ---------------------------------------------------------------- local inputs
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pinned(tag):
    path = INPUT_PATHS[tag]
    got = sha256_file(path)
    gate(f"pin-{tag}", got == PINS[tag], {"sha256": got, "expected": PINS[tag]})
    if tag == "probes":
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return json.loads(path.read_text())


# ---------------------------------------------------------------- independent
# exact integer geometry (fresh implementation; mathematics identical to the
# published conventions: 11x11 board, cells 0..120, hex = 128-bit mask)
def cells_of(v):
    return [i for i in range(N) if (v >> i) & 1]


def to_hex(v):
    return f"{v:032x}"


def _rot(x, y):
    return (y, 10 - x)


def _ref(x, y):
    return (x, 10 - y)


def xy_of(c):
    return (c % 11, c // 11)


def idx(x, y):
    return 11 * y + x


def orbit_cells(cset):
    """all 8 D4 images of a cell set, as frozensets (identity first)."""
    pts = [xy_of(c) for c in cset]
    out = []
    cur = pts
    for _ in range(4):
        out.append(frozenset(idx(*p) for p in cur))
        cur = [_rot(*p) for p in cur]
    cur = [_ref(*p) for p in pts]
    for _ in range(4):
        out.append(frozenset(idx(*p) for p in cur))
        cur = [_rot(*p) for p in cur]
    uniq = []
    for img in out:
        if img not in uniq:
            uniq.append(img)
    return uniq


def orbit_masks(v):
    return [sum(1 << c for c in img) for img in orbit_cells(cells_of(v))]


def canon_hex(v):
    return to_hex(min(orbit_masks(v)))


def popcount(v):
    return bin(v).count("1")


def bareiss_det4(m):
    """exact Bareiss determinant of a 4x4 integer matrix (lists of rows)."""
    a = [row[:] for row in m]
    n = 4
    sign = 1
    prev = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            for r in range(k + 1, n):
                if a[r][k] != 0:
                    a[k], a[r] = a[r], a[k]
                    sign = -sign
                    break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
            a[i][k] = 0
        prev = a[k][k]
    return sign * a[n - 1][n - 1]


def quadruple_free_cells(cset):
    """no 4 stones concyclic or collinear: the 4x4 generalized-circle
    determinant must be nonzero for every 4-subset."""
    pts = [xy_of(c) for c in cset]
    for quad in combinations(range(len(pts)), 4):
        m = []
        for i in quad:
            x, y = pts[i]
            m.append([x * x + y * y, x, y, 1])
        if bareiss_det4(m) == 0:
            return False, quad
    return True, None


def covered_by(row_v, root_v):
    """row (|stones|=6) is covered by root (|stones|=8) iff cells(row) is a
    subset of some D4 image of the root's stones."""
    for img in orbit_cells(cells_of(root_v)):
        row_cells = cells_of(row_v)
        if all(c in img for c in row_cells):
            return True
    return False


def root_of(h):
    return int(h, 16)


# ---------------------------------------------------------------- machine
def main():
    inputs = {tag: load_pinned(tag) for tag in PINS}

    k1085 = inputs["k1085"]
    k1097 = inputs["k1097"]
    rec = inputs["replace9"]
    probes = inputs["probes"]
    decision = inputs["decision"]
    k1147 = inputs["k1147audit"]
    rounds = {tag: inputs[tag] for tag in ROUND_FILES}

    # ---- protocol field agreement of the replace-9 record -------------------
    gate("replace9-protocol", (
        rec["runner_git_blob"] == RUNNER_BLOB and rec["cap"] == CAP
        and rec["timeout_s"] == TIMEOUT
        and rec["targets"]["replacement_roots"] == 9
        and rec["targets"]["probes_planned"] == 18),
        {"runner_blob": rec["runner_git_blob"], "cap": rec["cap"], "timeout_s": rec["timeout_s"]})
    gate("replace9-input-pins-recorded", all(
        rec["inputs"][f"{t}_sha256"] == PINS[t] for t in ("k1085", "k1086", "k1089", "k1091", "k1095", "k1097")),
        {"inputs": rec["inputs"]})

    # ---- probe JSONL --------------------------------------------------------
    gate("probes-count-18", len(probes) == 18, {"n": len(probes)})
    seen = set()
    for pr in probes:
        rootv = root_of(pr["root"])
        bit = pr["bit"]
        gate(f"probe-raw-child-{pr['root'][:6]}-{pr['ordering']}", (
            pr["child"] == to_hex(rootv - (1 << bit))
            and bit == (rootv & -rootv).bit_length() - 1
            and pr["depth"] == DEPTH and pr["cap"] == CAP and pr["timeout_s"] == TIMEOUT
            and pr["runner_blob"] == RUNNER_BLOB
            and pr["k1097_input_sha256"] == PINS["k1097"]
            and pr["ordering"] in ("andclose0", "andclose1")
            and pr["control"] == {"capped": False, "control": "pilot_d6",
                                  "loss": PILOT_LOSS, "nodes": PILOT_NODES}
            and pr["result"]["andclose"] == (pr["ordering"] == "andclose1")
            and pr["result"]["bit"] == bit and pr["result"]["capped"] is False
            and pr["result"]["nodes"] > 0
            and isinstance(pr["result"]["terminalStoneRange"], list)
            and len(pr["result"]["terminalStoneRange"]) == 2
            and pr["result"]["terminalStoneRange"][0] <= pr["result"]["terminalStoneRange"][1]),
            {"root": pr["root"], "ordering": pr["ordering"], "bit": bit, "child": pr["child"]})
        seen.add((pr["root"], pr["ordering"]))
    gate("probes-unique-pairs", len(seen) == 18, {"unique": len(seen)})
    gate("probes-both-orderings",
         len({r for r, o in seen}) == 9 and all(
             (r, "andclose0") in seen and (r, "andclose1") in seen for r, o in seen),
         {"roots": len({r for r, o in seen})})

    # ---- record per_root vs JSONL (nodes/loss/capped/range; ms & wall skipped)
    per_root = rec["per_root"]
    for rhex, entry in per_root.items():
        rv = root_of(rhex)
        gate(f"popcount8-{rhex[:6]}", popcount(rv) == 8, {"root": rhex})
        probe_map = {}
        for pr in probes:
            if pr["root"] == rhex:
                probe_map[pr["ordering"]] = pr
        for ordering, pv in entry["probes"].items():
            jpr = probe_map[ordering]["result"]
            gate(f"record-vs-jsonl-{rhex[:6]}-{ordering}", (
                pv["nodes"] == jpr["nodes"] and pv["loss"] == jpr["loss"]
                and pv["capped"] == jpr["capped"]
                and pv["terminalStoneRange"] == jpr["terminalStoneRange"]
                and pv["ordering"] == ordering),
                {"root": rhex, "ordering": ordering, "nodes": (pv["nodes"], jpr["nodes"]),
                 "loss": (pv["loss"], jpr["loss"]),
                 "range": (pv["terminalStoneRange"], jpr["terminalStoneRange"])})

    # ---- classification rederivation ----------------------------------------
    loss_true = set()
    loss_false = set()
    for pr in probes:
        (loss_true if pr["result"]["loss"] else loss_false).add(pr["root"])
    both_win = {r for r in loss_true if (r, "andclose0") in seen and (r, "andclose1") in seen}
    win_pub = {r["root"] for r in rec["classification"]["win8_d10_candidates"]}
    ref_pub = {r["root"] for r in rec["classification"]["refuted_d10_facts"]}
    gate("classification-win-rederive", both_win == win_pub and len(win_pub) == 1,
        {"derived": sorted(both_win), "published": sorted(win_pub)})
    gate("classification-ref-rederive", loss_false == ref_pub and len(ref_pub) == 8,
        {"derived": sorted(loss_false), "published": sorted(ref_pub)})
    nodes_sum = sum(p["result"]["nodes"] for p in probes)
    gate("classification-nodes-total",
         rec["classification"]["nodes_total"] == nodes_sum == 3_574_172,
         {"published": rec["classification"]["nodes_total"], "derived": nodes_sum})
    cov_hist = {}
    for rhex, entry in per_root.items():
        gate(f"gained-eq-len-{rhex[:6]}",
             entry["gained_rows"] == len(entry["covered_rows"]),
             {"root": rhex, "gained": entry["gained_rows"], "n": len(entry["covered_rows"])})
        cov_hist[entry["gained_rows"]] = cov_hist.get(entry["gained_rows"], 0) + 1
    gate("classification-gains-hist", cov_hist == {3: 6, 2: 2, 1: 1},
        {"derived": cov_hist})
    tmin = min(p["result"]["terminalStoneRange"][0] for p in probes)
    tmax = max(p["result"]["terminalStoneRange"][1] for p in probes)
    gate("classification-terminal-union",
         rec["classification"]["terminalStoneRange_union"] == [tmin, tmax] == [14, 18],
        {"published": rec["classification"]["terminalStoneRange_union"], "derived": [tmin, tmax]})
    gate("classification-capped-error-zero",
         rec["classification"]["capped_probes"] == 0 and rec["classification"]["error_probes"] == 0
         and rec["classification"]["unresolved"] == [],
        {"capped": rec["classification"]["capped_probes"], "error": rec["classification"]["error_probes"]})
    for cand in rec["classification"]["win8_d10_candidates"]:
        gate(f"win-claimed-rows-{cand['root'][:6]}",
             per_root[cand["root"]]["covered_rows"] == cand["covered_rows"]
             and cand["gained_rows"] == len(cand["covered_rows"]),
            {"root": cand["root"], "rows": cand["covered_rows"]})

    # ---- residual universe chain (independent re-derivation) ---------------
    base_rows = k1085["base_state"]["residual_row_hex"]
    gate("base72", len(base_rows) == 72 and len(set(base_rows)) == 72,
        {"n": len(base_rows), "unique": len(set(base_rows))})
    gate("safe8-recorded", k1085["add_two_stones_census"]["safe8"] == 120_474,
        {"safe8": k1085["add_two_stones_census"]["safe8"]})
    residual = set(base_rows)
    residual_chain = {"72": sorted(residual)}
    hist = [72]  # residual sizes; current residual = hist[-1]
    for tag, n_win, n_ref, n_claim, size_after in ROUND_META:
        r = rounds[tag]
        start = hist[-1]
        size_before_start = hist[-2] if len(hist) >= 2 else None
        hist.append(size_after)
        wins = r["classification"]["win8_d10_candidates"]
        refs = r["classification"]["refuted_d10_facts"]
        gate(f"round-{tag}-counts", len(wins) == n_win and len(refs) == n_ref,
            {"win": len(wins), "refuted": len(refs)})
        # win claims
        win_rows = []
        for w in wins:
            prows = r["per_root"][w["root"]]["covered_rows"]
            gate(f"round-{tag}-win-rows-match-{w['root'][:6]}",
                 prows == w["covered_rows"] and w["gained_rows"] == len(prows),
                {"root": w["root"], "n": len(prows)})
            win_rows.extend(prows)
        gate(f"round-{tag}-win-rows-distinct", len(win_rows) == len(set(win_rows)) == n_claim,
            {"claimed": len(win_rows), "distinct": len(set(win_rows))})
        gate(f"round-{tag}-win-rows-in-residual", set(win_rows) <= residual,
            {"outside": sorted(set(win_rows) - residual)})
        # refuted claims
        ref_rows = []
        for rr in refs:
            prows = r["per_root"][rr["root"]]["covered_rows"]
            gate(f"round-{tag}-ref-rows-match-{rr['root'][:6]}",
                 prows != [] and rr["gained_rows"] == len(prows),
                {"root": rr["root"], "gained": rr["gained_rows"], "n": len(prows)})
            ref_rows.extend(prows)
        # full partition of the current residual by win+refuted claims
        all_rows = win_rows + ref_rows
        gate(f"round-{tag}-exactly-once-partition",
             len(all_rows) == len(set(all_rows)) and set(all_rows) == residual,
            {"claimed_total": len(all_rows), "distinct": len(set(all_rows)),
             "uncovered": sorted(residual - set(all_rows)),
             "extra": sorted(set(all_rows) - residual)})
        residual = residual - set(win_rows)
        gate(f"round-{tag}-residual-size", len(residual) == size_after,
            {"size": len(residual), "expected": size_after})
        residual_chain[str(size_after)] = sorted(residual)
        # the record's own rederivation bookkeeping for its START universe:
        # its win*/ref* claimed-row counts must partition the previous residual
        own = r.get(f"residual{start}_rederivation")
        if own is not None and size_before_start is not None:
            row_counts = sorted(v for k, v in own.items() if k.endswith("_claimed_rows"))
            expected = sorted([start, size_before_start - start])
            gate(f"round-{tag}-own-red-bookkeeping", row_counts == expected,
                {"own_row_counts": row_counts, "expected": expected})

    # ---- identity of the residual-23 universe across published documents ----
    mine23 = set(residual_chain["23"])
    k1097_rows = {r["row"] for r in k1097["per_row_residual23"]}
    gate("residual23-mine-vs-k1097", len(k1097_rows) == 23 and mine23 == k1097_rows,
        {"mine": len(mine23), "k1097": len(k1097_rows)})
    # cover-decision universe bookkeeping (independent re-derivation of the
    # K1147-audited identities from the pinned decision master)
    pu = decision["provider_universe_rederivation"]
    hist = pu["provider_coverage_hist"]
    gate("decision-universe-bookkeeping", (
        pu["generation_events"] == 23 * 6555 == 150_765
        and pu["universe_touching23_unique_roots"] == pu["safe8_touching23"] + pu["unsafe8_touching23"]
        and pu["P3_touching23"] == pu["safe8_touching23"] - pu["refuted_touching23"]
        and pu["refuted_touching23"] + pu["refuted_not_touching23"] == 50
        and sum(hist.values()) == pu["P3_touching23"] == 45_219
        and pu["per_row_demand_sum"] == sum(int(k) * v for k, v in hist.items()) == 50_670
        and pu["eligible_triple_providers"] == 297 and pu["eligible_pair_providers"] == 4_857
        and pu["ineligible_singletons"] == 40_065),
        {"P3_touching23": pu["P3_touching23"],
         "demand_sum": pu["per_row_demand_sum"], "hist": pu["provider_coverage_hist"]})
    gate("decision-master-byte-ledger",
         decision["decision"]["decision"] == "UNSAT"
         and decision["decision"]["minimum_cover_size_over_P3"] == 9
         and decision["decision"]["interval_after"] == [9, 9]
         and k1147["published_decision_sha256"] == PINS["decision"]
         and k1147["checks_all_ok"] is True,
        {"decision": decision["decision"]["decision"], "min_cover": 9})

    # ---- greedy selection identity K1097 vs swept roots ---------------------
    greedy = k1097["scope1_refsolve_residual23"]["greedy_selection"]
    gate("greedy-size-9", len(greedy) == 9, {"n": len(greedy)})
    pub9 = {}
    for g in greedy:
        pub9[g["root"]] = (g["gained_rows"], g["covered_rows"])
    mine9 = {}
    for rhex, entry in per_root.items():
        mine9[rhex] = (entry["gained_rows"], entry["covered_rows"])
    gate("greedy-identity-root-by-root", pub9 == mine9,
        {"k1097": sorted(pub9), "replace9": sorted(mine9)})
    gre = k1097["scope1_refsolve_residual23"]
    gate("greedy-plan-bookkeeping",
         gre["greedy_size"] == 9 and gre["leftover_rows"] == []
         and gre["stranded_rows"] == [] and gre["max_matching"] == 23
         and gre["probes_two_orderings"] == 18,
        {"bookkeeping": {k: gre[k] for k in
                         ("greedy_size", "leftover_rows", "stranded_rows",
                          "max_matching", "probes_two_orderings")}})

    # ---- cover geometry of the 9 swept roots (fresh implementation) ---------
    covered_all = []
    for rhex, entry in per_root.items():
        rv = root_of(rhex)
        qf, quad = quadruple_free_cells(cells_of(rv))
        gate(f"quad-free-{rhex[:6]}", qf, {"root": rhex, "bad_quad": quad})
        gate(f"d4-min-canonical-{rhex[:6]}", canon_hex(rv) == rhex,
            {"root": rhex, "canon": canon_hex(rv)})
        for row in entry["covered_rows"]:
            rowv = root_of(row)
            gate(f"row-popcount6-{row[:6]}", popcount(rowv) == 6, {"row": row})
            if not covered_by(rowv, rv):
                gate(f"row-covered-geometry-{row[:6]}", False,
                    {"row": row, "root": rhex})
            covered_all.append(row)
    gate("exactly-once-over-residual23",
         len(covered_all) == 23 and len(set(covered_all)) == 23
         and set(covered_all) == set(residual_chain["23"]),
        {"n": len(covered_all), "distinct": len(set(covered_all))})

    # ---- five-sweep cumulative verdict census (novel cross-checks) ---------
    census_roots = {}
    for tag in ROUND_FILES:
        r = rounds[tag]
        for rhex in r["per_root"]:
            census_roots[(tag, rhex)] = r["per_root"][rhex]
    n_probed = sum(len(rounds[t]["per_root"]) for t in ROUND_FILES)
    gate("census-probed-75", n_probed == 75, {"probed": n_probed})
    canon_seen = {}
    dup = []
    for (tag, rhex) in census_roots:
        c = canon_hex(root_of(rhex))
        if c in canon_seen:
            dup.append((c, canon_seen[c], tag))
        else:
            canon_seen[c] = tag
        gate(f"census-popcount-{rhex[:6]}", popcount(root_of(rhex)) == 8, {"root": rhex})
    gate("census-canonical-uniqueness-75", len(dup) == 0 and len(canon_seen) == 75,
        {"duplicates": dup})
    # world-record pool arithmetic and verdict classes
    win_all, ref_all = [], []
    for tag, n_win, n_ref, n_claim, _ in ROUND_META:
        wins = rounds[tag]["classification"]["win8_d10_candidates"]
        refs = rounds[tag]["classification"]["refuted_d10_facts"]
        win_all.extend(w["root"] for w in wins)
        ref_all.extend(r["root"] for r in refs)
    gate("census-win-17", len(win_all) == 17 and len(set(win_all)) == 17,
        {"win": len(win_all)})
    gate("census-refuted-58", len(ref_all) == 58 and len(set(ref_all)) == 58,
        {"refuted": len(ref_all)})
    winc = {canon_hex(root_of(x)) for x in win_all}
    refc = {canon_hex(root_of(x)) for x in ref_all}
    gate("census-win-refuted-disjoint", winc.isdisjoint(refc),
        {"conflicts": sorted(winc & refc)})
    gate("census-poolarithmetic",
         k1097["exclusion"]["pool_P_triple_prime_size"] == 120_424
         and 120_474 - 50 == 120_424 and 120_474 - 58 == 120_416,
        {"P3": k1097["exclusion"]["pool_P_triple_prime_size"], "P4": 120_416})
    ex_rows = sorted(k1097["exclusion"]["refuted_d10_roots_excluded"])
    gate("exclusion-list-identity-50", ex_rows == sorted(ref_all[:50]),
        {"excluded_n": len(ex_rows)})
    ref58c = {canon_hex(root_of(x)) for x in ex_rows + [r["root"] for r in rec["classification"]["refuted_d10_facts"]]}
    gate("refuted58-canonical-unique", len(ref58c) == 58, {"unique": len(ref58c)})

    # ---- win16 intrinsic footprints (K1097) re-derived over residual-72 -----
    base_set = set(residual_chain["72"])
    foot = k1097["win16_intrinsic_footprints"]
    gate("footprints-16", len(foot) == 16, {"n": len(foot)})
    eq_claimed = 0
    for rhex, f in foot.items():
        rv = root_of(rhex)
        intr = sorted(row for row in base_set if covered_by(root_of(row), rv))
        gate(f"footprint-rederive-{rhex[:6]}",
             intr == sorted(f["intrinsic"]) and set(f["claimed"]) <= set(intr)
             and f["intrinsic_equals_claimed"] == (intr == sorted(f["claimed"])),
            {"root": rhex, "mine": intr, "published": sorted(f["intrinsic"])})
        if f["intrinsic_equals_claimed"]:
            eq_claimed += 1
    gate("footprints-15-equal-claimed", eq_claimed == 15, {"equal": eq_claimed})
    gate("footprints-16th-surplus-row",
         sorted(foot["0000000800000000380000000810000a"]["intrinsic"]) ==
         sorted(foot["0000000800000000380000000810000a"]["claimed"] +
                ["00000000000000003800000008001080"]),
        {"intrinsic": foot["0000000800000000380000000810000a"]["intrinsic"]})
    # newest WIN candidate: intrinsic footprint over the base-72 universe
    new_root = rec["classification"]["win8_d10_candidates"][0]["root"]
    new_rv = root_of(new_root)
    new_intr = sorted(row for row in base_set if covered_by(root_of(row), new_rv))
    new_claimed = per_root[new_root]["covered_rows"]
    gate("new-win-claim-subset-intrinsic", set(new_claimed) <= set(new_intr),
        {"claimed": new_claimed, "intrinsic": new_intr})
    # win16 footprint over residual23 must be empty (K1097 claim)
    hit23 = sorted(row for rhex, f in foot.items()
                   for row in f["intrinsic"] if row in set(residual_chain["23"]))
    gate("win16-intrinsic-hits-residual23-empty", hit23 == [], {"hits": hit23})

    # ---- census body --------------------------------------------------------
    verified_table = []
    for tag, n_win, n_ref, n_claim, size_after in ROUND_META:
        r = rounds[tag]
        for rhex, entry in r["per_root"].items():
            p = entry["probes"]
            cls = ("WIN8-D10-candidate" if rhex in {w["root"] for w in r["classification"]["win8_d10_candidates"]}
                   else "REFUTED-D10")
            verified_table.append({
                "record": tag, "root": rhex, "canonical": canon_hex(root_of(rhex)),
                "verdict": cls, "gained_rows": entry["gained_rows"],
                "andclose1": p["andclose1"]["nodes"], "andclose0": p["andclose0"]["nodes"],
                "order_loss_pair": (p["andclose1"]["loss"], p["andclose0"]["loss"]),
            })
    census = {
        "probed_roots_total": 75,
        "win8_d10_candidates_17": sorted(w for w in win_all),
        "refuted_d10_facts_58": sorted(ref_all),
        "pool_p_triple_prime": 120_424,
        "pool_P4_after_replace9": 120_416,
        "win_claimed_rows_cumulative_52": 23 + 9 + 10 + 7 + 3,
        "residual_after_k1146_win_folds_only_20_rows": len(residual_chain["20"]),
        "new_win_candidate_intrinsic_over_base72": {
            "root": new_root,
            "claimed": new_claimed,
            "intrinsic": new_intr,
            "intrinsic_equals_claimed": new_intr == sorted(new_claimed),
            "intrinsic_rows_within_residual23_beyond_claim":
                sorted(set(new_intr) & set(residual_chain["23"]) - set(new_claimed)),
        },
        "cross_sweep_canonical_win_refuted_conflicts": sorted(winc & refc),
        "per_record": [
            {"record": t, "win": n_win, "refuted": n_ref,
             "nodes_total": rounds[t]["classification"]["nodes_total"],
             "terminal_union": rounds[t]["classification"].get("terminalStoneRange_union")}
            for t, n_win, n_ref, _, _ in ROUND_META],
        "per_root_table": verified_table,
    }
    residual_chain_out = {k: v for k, v in residual_chain.items()}

    audit = {
        "schema": SCHEMA,
        "single_owner_note": SINGLE_OWNER_NOTE,
        "inputs": {tag: {"path": str(INPUT_PATHS[tag].name), "sha256": PINS[tag]} for tag in PINS},
        "gates": GATES,
        "gates_total": len(GATES),
        "gates_all_pass": all(g["pass"] for g in GATES),
        "census": census,
        "residual_chain_row_hex": residual_chain_out,
        "trust_boundary": ("whole-record re-derivation of published artifacts only; "
                           "the DFPN engine was not re-run; verdicts are accepted as "
                           "published probe facts, independently re-checked only at the "
                           "record bookkeeping/geometry/accounting level"),
        "interpretation_guard": [
            "WIN8-D10 candidate is not a certificate until extraction, independent "
            "double verification and the 8-stone receipt fold; no row was closed here",
            "REFUTED-D10 is not a LOSS proof; it only erodes the replacement pool",
            "node counts and solved counts are not win/loss evidence",
            "greedy and witness selections are conditional planning bookkeeping, "
            "not certificates",
            "the standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60} and classes 1/2/4 all remain UNKNOWN",
        ],
        "status": "PASS" if all(g["pass"] for g in GATES) else "FAIL",
    }

    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, sort_keys=True,
                                indent=2) + "\n")
    print(f"gates: {len(GATES)} all_pass={audit['gates_all_pass']}")
    print(f"audit sha256: {sha256_file(AUDIT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
