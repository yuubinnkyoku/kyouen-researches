#!/usr/bin/env python3
"""Independent published-record geometry check for K1075 (stdlib only).

This verifier does not import or call candidate_supply_rebuild_20261120.py.
It rebuilds the residual-72 add-one-stone universe from the published rows,
uses a 4x4 Bareiss determinant (rather than the producer's cofactor formula)
for safety, and independently reconstructs D4 deletion coverage for both the
36-root fresh witness and resolve7's 38-root retired assignment.
It intentionally does not rebuild the K0863 corpus verdict join or run any
new depth-10 probes.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "candidate-supply-second-verification-20261120.json"

PINS = {
    "candidate_supply": (
        "output/residual72-full-cache-join-candidate-supply-20261120.json",
        "49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa",
    ),
    "resolve7": (
        "../n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json",
        "207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f",
    ),
    "fold9": (
        "../n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json",
        "24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2",
    ),
    "fold10": (
        "../n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json",
        "bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a",
    ),
    "seventeenth_verify": (
        "../n11-residual78-seventeenth-win7-cert-extract-20261120/output/seventeenth-cert-triple-verification-20261120.json",
        "c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc",
    ),
    "live_sweep": (
        "../n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json",
        "22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc",
    ),
}

gates = []
def gate(name: str, ok: bool, detail=None):
    gates.append({"name": name, "pass": bool(ok), "detail": detail})

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()

def popcount(x: int) -> int:
    return x.bit_count()

def points(mask: int):
    return [p for p in range(121) if (mask >> p) & 1]

# D4 is reconstructed from coordinate actions, not imported from the producer.
def transform(mask: int, t: int) -> int:
    out = 0
    for p in points(mask):
        x, y = p % 11, p // 11
        if t == 0: X, Y = x, y
        elif t == 1: X, Y = 10 - y, x
        elif t == 2: X, Y = 10 - x, 10 - y
        elif t == 3: X, Y = y, 10 - x
        elif t == 4: X, Y = 10 - x, y
        elif t == 5: X, Y = x, 10 - y
        elif t == 6: X, Y = y, x
        else: X, Y = 10 - y, 10 - x
        out |= 1 << (11 * Y + X)
    return out

def canonical(mask: int) -> int:
    return min(transform(mask, t) for t in range(8))

def hx(mask: int) -> str:
    return f"{mask:032x}"

def bareiss_det(matrix):
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot_row = next((r for r in range(k + 1, n) if a[r][k] != 0), None)
            if pivot_row is None:
                return 0
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss division was not exact")
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[n - 1][n - 1]

def unsafe_count(mask: int) -> int:
    pts = [(p % 11, p // 11) for p in points(mask)]
    if len(pts) != 7:
        raise ValueError("expected seven-stone root")
    bad = 0
    for a, b, c, d in itertools.combinations(pts, 4):
        rows = [[x, y, x*x + y*y, 1] for x, y in (a, b, c, d)]
        if bareiss_det(rows) == 0:
            bad += 1
    return bad

def deletion_coverage(mask: int, residual_set: set[str]) -> set[str]:
    out = set()
    for t in range(8):
        image = transform(mask, t)
        for bit in points(image):
            row = hx(canonical(image ^ (1 << bit)))
            if row in residual_set:
                out.add(row)
    return out

# Read and pin all published inputs.
paths = {name: HERE / rel for name, (rel, _) in PINS.items()}
actual_hashes = {name: sha256(path) for name, path in paths.items()}
for name, (_, expected) in PINS.items():
    gate("pin-" + name, actual_hashes[name] == expected,
         {"expected": expected, "actual": actual_hashes[name]})
cs = read_json(paths["candidate_supply"])
r7 = read_json(paths["resolve7"])
f9 = read_json(paths["fold9"])
f10 = read_json(paths["fold10"])
sv17 = read_json(paths["seventeenth_verify"])
live = read_json(paths["live_sweep"])

residual = sorted(cs["base_state"]["residual_row_hex"])
residual_set = set(residual)
r7_rows = sorted(r7["recheck"]["residual_72_after"]["rows"])
f10_rows = sorted(f10["five_parent_target_after"]["residual_row_hex_after"])
f9_rows = sorted(f9["five_parent_target_after"]["residual_row_hex_after"])
fold9_closed = sorted(x["row_hex"] for x in f9["new_receipt_coverage"]["rows"])
fold10_closed = sorted(x["row_hex"] for x in f10["new_receipt_coverage"]["rows"])
fold10_target_closed = sorted(x["row_hex"] for x in f10["new_receipt_coverage"]["rows"]
                              if x["row_hex"] in set(f9_rows))

# Chain and provenance checks.
gate("residual72-equals-resolve7", residual == r7_rows,
     {"candidate_rows": len(residual), "resolve7_rows": len(r7_rows)})
gate("residual72-equals-fold10-after", residual == f10_rows,
     {"candidate_rows": len(residual), "fold10_rows": len(f10_rows)})
gate("fold9-residual74", len(f9_rows) == 74)
gate("fold9-closed-four", len(fold9_closed) == 4)
gate("fold10-closed-three", len(fold10_closed) == 3)
gate("fold10-target-two-extra-one", len(fold10_target_closed) == 2 and
     len(set(fold10_closed) - set(fold10_target_closed)) == 1,
     {"target": len(fold10_target_closed), "extra": len(set(fold10_closed)-set(fold10_target_closed))})
gate("fold-chain-disjoint-closures", not (set(fold9_closed) & set(fold10_closed)))
gate("fold-chain-residual-subtraction", set(f9_rows) - set(fold10_target_closed) == residual_set)
gate("rows-are-six-stone-d4-canonical", len(residual_set) == 72 and
     all(len(h) == 32 and popcount(int(h, 16)) == 6 and canonical(int(h, 16)) == int(h, 16)
         for h in residual))
gate("sv17-root-matches-retired-root", sv17["root_hex"] == r7["retired_witness_root"])
gate("sv17-coverage-matches-fold10-target", sorted(sv17["coverage_claim_pending_fold"]["covered_rows_per_resolve6_matching"]) == fold10_target_closed)
gate("sv17-38-gates", sv17["gates_total"] == 38 and sv17["gates_all_pass"] is True)
gate("live-sweep-39x2-summary", live["summary"]["roots"] == 39 and
     live["summary"]["probes"] == 78 and live["summary"]["win"] == 1 and
     live["summary"]["refuted"] == 38 and live["summary"]["capped"] == 0 and
     live["summary"]["order_conflicts"] == 0, live["summary"])
gate("resolve7-cross-check-flags", all(cs["resolve7_cross_check"].get(k) is True for k in (
     "assignment_34x2_plus_4x1", "post_retire_assignment_geometry_recheck")))

# Rebuild the entire add-one-stone universe from the 72 rows.
universe = set()
for row in residual:
    m = int(row, 16)
    for p in range(121):
        if not ((m >> p) & 1):
            universe.add(canonical(m | (1 << p)))
universe_hex = {hx(x) for x in universe}
gate("universe72-independent-rebuild", len(universe) == 7448 and
     len(universe_hex) == cs["candidate_supply"]["universe72_roots"],
     {"rebuilt": len(universe), "published": cs["candidate_supply"]["universe72_roots"]})

# Independent exact-integer geometry for every member of the 7,448-root universe.
unsafe_by_root = {}
coverage_by_root = {}
coverage_hist = {}
safe_pair_edges = set()
safe_rows_covered = set()
for root in universe:
    bad = unsafe_count(root)
    unsafe_by_root[root] = bad
    cov = deletion_coverage(root, residual_set)
    coverage_by_root[root] = cov
    coverage_hist[len(cov)] = coverage_hist.get(len(cov), 0) + 1
    if bad == 0:
        safe_rows_covered.update(cov)
        if len(cov) == 2:
            safe_pair_edges.add(tuple(sorted(cov)))
safe_total = sum(1 for v in unsafe_by_root.values() if v == 0)
unsafe_total = len(universe) - safe_total
hits = cs["verdict_join"]["universe_hits_over_72"]
csupply = cs["candidate_supply"]
gate("independent-safe-universe-count", safe_total == 4577,
     {"safe": safe_total, "unsafe": unsafe_total})
gate("safe-fresh-judged-partition-arithmetic",
     safe_total == hits["fresh_safe"] + hits["judged_refuted"] + hits["judged_win"] and
     unsafe_total == hits["fresh_unsafe"],
     {"safe_total": safe_total, "fresh_safe": hits["fresh_safe"],
      "judged_refuted": hits["judged_refuted"], "judged_win": hits["judged_win"],
      "unsafe_total": unsafe_total, "fresh_unsafe": hits["fresh_unsafe"]})
gate("all-safe-universe-has-no-multicover", max(coverage_hist) <= 2,
     {"coverage_size_histogram": dict(sorted(coverage_hist.items()))})
gate("safe-universe-covers-residual", safe_rows_covered == residual_set,
     {"covered_rows": len(safe_rows_covered), "residual_rows": len(residual_set)})

# Independently verify all 36 fresh witness roots by D4 x one-stone deletion.
witnesses = cs["witness_full"]
witness_roots = [w["root"] for w in witnesses]
witness_covered = []
witness_bad = []
witness_rows_match = True
for w in witnesses:
    root = int(w["root"], 16)
    cov = deletion_coverage(root, residual_set)
    witness_covered.append(cov)
    if popcount(root) != 7 or canonical(root) != root or unsafe_count(root) != 0:
        witness_bad.append(w["root"])
    if sorted(cov) != sorted(w["covered"]) or sorted(cov) != sorted(w["rows"]):
        witness_rows_match = False
witness_union = set().union(*witness_covered) if witness_covered else set()
witness_memberships = sum(len(x) for x in witness_covered)
witness_overlap = witness_memberships - len(witness_union)
gate("witness36-count-and-unique-roots", len(witnesses) == 36 and len(set(witness_roots)) == 36)
gate("witness36-root-shape-and-safety", not witness_bad,
     {"bad_roots": witness_bad[:5], "bad_count": len(witness_bad)})
gate("witness36-coverage-rederived", witness_rows_match)
gate("witness36-is-36-pairs", all(len(x) == 2 for x in witness_covered),
     {"coverage_sizes": sorted({len(x) for x in witness_covered})})
gate("witness36-exact-one-cover", witness_union == residual_set and witness_overlap == 0,
     {"union_rows": len(witness_union), "overlap_memberships": witness_overlap})
gate("witness36-disjoint-from-retired38", not (set(witness_roots) &
     set(csupply["live38_killed_open_72row_supply"]["roots"])))
gate("matching36-optimality", csupply["maximum_matching"] == 36 and
     csupply["matched_rows"] == 72 and csupply["unmatched_rows"] == 0 and
     36 == len(residual_set) // 2 and witness_overlap == 0)

# Independently verify the 38-root retired assignment from resolve7.
assignment = r7["recheck"]["post_retire_assignment"]["rows_per_root"]
assignment_roots = set(assignment)
assignment_union = set()
assignment_overlap = 0
assignment_bad = []
assignment_sizes = []
for root_hex, recorded_rows in assignment.items():
    root = int(root_hex, 16)
    cov = deletion_coverage(root, residual_set)
    assignment_sizes.append(len(cov))
    if popcount(root) != 7 or canonical(root) != root or unsafe_count(root) != 0:
        assignment_bad.append(root_hex)
    if sorted(cov) != sorted(recorded_rows):
        assignment_bad.append(root_hex + ":coverage")
    assignment_overlap += len(cov & assignment_union)
    assignment_union.update(cov)
live38_roots = sorted(csupply["live38_killed_open_72row_supply"]["roots"])
gate("retired38-count-and-root-identity", len(assignment) == 38 and
     set(live38_roots) == assignment_roots)
gate("retired38-root-shape-safety-and-coverage", not assignment_bad,
     {"bad": assignment_bad[:5], "bad_count": len(assignment_bad)})
gate("retired38-34-pair-4-singleton", assignment_sizes.count(2) == 34 and
     assignment_sizes.count(1) == 4 and len(assignment_sizes) == 38,
     {"size_histogram": {str(n): assignment_sizes.count(n) for n in sorted(set(assignment_sizes))}})
gate("retired38-one-cover-72-rows", assignment_union == residual_set and assignment_overlap == 0,
     {"union_rows": len(assignment_union), "overlap_memberships": assignment_overlap})

# Published summary consistency and demand arithmetic.
row_demand = csupply["row_demand"]
demand_values = [v["fresh_safe_candidates"] for v in row_demand.values()]
refuted_values = [v["judged_refuted_candidates"] for v in row_demand.values()]
win_values = [v["judged_win_candidates_covering"] for v in row_demand.values()]
gate("row-demand-exact-72-keys", set(row_demand) == residual_set)
gate("row-demand-all-positive", len(demand_values) == 72 and min(demand_values) > 0 and
     not any(v["fresh_safe_candidate_deficit"] for v in row_demand.values()))
gate("row-demand-range-and-arithmetic", min(demand_values) == 52 and max(demand_values) == 76 and
     sum(demand_values) == 4678 and sum(refuted_values) == 638 and sum(win_values) == 0,
     {"fresh_safe_min": min(demand_values), "fresh_safe_max": max(demand_values),
      "fresh_safe_incidence": sum(demand_values), "refuted_incidence": sum(refuted_values),
      "win_incidence": sum(win_values)})
gate("candidate-summary-values", csupply["fresh_safe_pool"] == 4109 and
     csupply["fresh_safe_72row_coverage"] == residual and
     csupply["rows_uncovered_by_fresh_safe_pool"] == [] and
     csupply["pair_edges"] == 536 and csupply["singleton_eligible_rows"] == 72 and
     csupply["multi_cover_roots"] == {} and csupply["stranded_rows"] == 0 and
     csupply["witness_size"] == 36 and csupply["greedy_set_cover_size"] == 40 and
     csupply["greedy_leftover_rows"] == 0)
gate("no-windfall-or-free-fold-supply", csupply["windfall_18th_certificate_candidates"] == [] and
     csupply["receipted_win_covering_open_rows"] == [])
gate("published-25-gates-all-pass", len(cs["checks"]) == 25 and all(x["pass"] for x in cs["checks"]))
gate("stage1-resolve6-exact-reproduction-claimed", all(
     cs["verdict_join"]["stage1_reproduction"].get(k) is True for k in (
         "join_stats_match_published", "universe_hits_match_published", "win_cover_hits_match_published")))
gate("phase2-join-conflict-free", cs["verdict_join"]["stats"]["win_refuted_conflicts"] == 0 and
     cs["verdict_join"]["stats"]["canonical_roots_judged"] == 7532 and
     cs["verdict_join"]["stats"]["refuted_roots"] == 6745 and
     cs["verdict_join"]["stats"]["win_roots"] == 787)

failures = [g for g in gates if not g["pass"]]
result = {
    "schema": "n11-residual72-candidate-supply-independent-second-verification-20261120-v1",
    "date": "2026-11-20",
    "status": "verified" if not failures else "failed",
    "method": "published-record-only; independent D4 coordinate actions; 4x4 exact-integer Bareiss determinant; independent add-one-stone universe and deletion-coverage reconstruction",
    "scope": "K1075 candidate geometry, residual-row provenance, 36-root fresh witness cover, resolve7 38-root retired assignment, and published count consistency; no corpus verdict join rebuild and no new game-tree search",
    "pins": {k: {"sha256": actual_hashes[k], "expected": PINS[k][1]} for k in PINS},
    "gates_total": len(gates),
    "gates_passed": len(gates) - len(failures),
    "gates_failed": len(failures),
    "gates": gates,
    "metrics": {
        "residual_rows": len(residual),
        "universe72_roots_rebuilt": len(universe),
        "safe_universe_roots_bareiss": safe_total,
        "unsafe_universe_roots_bareiss": unsafe_total,
        "universe_coverage_size_histogram": dict(sorted(coverage_hist.items())),
        "fresh_safe_pool_published": csupply["fresh_safe_pool"],
        "fresh_safe_row_demand_min_max": [min(demand_values), max(demand_values)],
        "fresh_safe_row_incidence_sum": sum(demand_values),
        "pair_edges_published": csupply["pair_edges"],
        "witness_roots_rechecked": len(witnesses),
        "witness_rows_covered": len(witness_union),
        "witness_overlap_memberships": witness_overlap,
        "matching_upper_bound": len(residual_set) // 2,
        "retired_roots_rechecked": len(assignment),
        "retired_assignment_pair_roots": assignment_sizes.count(2),
        "retired_assignment_singleton_roots": assignment_sizes.count(1),
        "retired_assignment_rows_covered": len(assignment_union),
        "retired_assignment_overlap_memberships": assignment_overlap,
    },
    "limitations": [
        "The K0863 1,279-file corpus and phase-2 verdict join were not rebuilt; their published hash-pinned aggregate is treated as input.",
        "The 536 distinct fresh-safe pair-edge count is checked against K1075's published field and its witness consequences, not independently enumerated from the full fresh verdict-root set.",
        "This is a coverage-plan verification, not a WIN/LOSS proof or a depth-10 sweep.",
        "REFUTED-D10 is not a LOSS proof; standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
    ],
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": result["status"], "gates_total": len(gates),
                  "gates_passed": len(gates)-len(failures), "gates_failed": len(failures),
                  "metrics": result["metrics"], "failed": failures}, ensure_ascii=False, sort_keys=True))
if failures:
    raise SystemExit(1)
