#!/usr/bin/env python3
"""Receipt-harvest global fold audit (2026-11-18).

Self-contained re-derivation of the mega-fold published as
class-frontier-receipt-harvest-global-fold-20261118.json:

  head 1476 -> 1589 by closing 113 open S6 manifest rows, each of which is a
  one-stone reduction (D4 orbit subset) of at least one published WIN7-D10
  root. Receipts come from
    (a) the pre-64h harvest (79 pinned sources of census v1; every WIN canon
        there inherits its published per-band WIN7-D10 certificate manifest),
    (b) the post-64h WIN7 certificate manifests (cost66i/66j/69j/71e/72d/
        73i/73j/73k/73l) and the published cost64h / cost76c fold receipts,
    (c) the dual roots cost73i bit 97 (third-implementation audit 12/12 PASS)
        and cost66j bit 9 (BigInt re-verification 15/15 PASS).

The audit re-derives every number from the pinned repo files: it rebuilds the
harvest, rebuilds the open head-1476 worklist, performs the global scan,
computes the fold bookkeeping, runs controls C1-C4, asserts the published
frontier values, and rewrites the fold record JSON.
"""
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]          # lane dir
OUT = HERE / "output"
EX = HERE.parent                                    # research/experiments
sys.path.insert(0, str(HERE / "scripts"))
from legal_candidates import legal_candidates  # noqa: E402

N = 11
TFS = (
    lambda x, y: (x, y), lambda x, y: (y, N - 1 - x), lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x), lambda x, y: (N - 1 - x, y), lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x), lambda x, y: (N - 1 - y, N - 1 - x),
)


def d4(mask, t):
    r = 0
    fn = TFS[t]
    for p in range(121):
        if (mask >> p) & 1:
            x, y = p % 11, p // 11
            xx, yy = fn(x, y)
            r |= 1 << (11 * yy + xx)
    return r


def canon(mask):
    return f"{min(d4(mask, t) for t in range(8)):032x}"


def stones(mask):
    return [p for p in range(121) if (mask >> p) & 1]


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def transform_of(root: int, row: int):
    """Return (t, extra_bit) with row = d4(root, t) minus one stone, or None."""
    for t in range(8):
        sr = d4(root, t)
        if bin(sr).count("1") == 7 and (row & ~sr) == 0:
            return t, (sr ^ row).bit_length() - 1
    return None


# ---------------------------------------------------------------- sources ----
SRC_WORKLIST = EX / "n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv"
SRC_LEDGER = EX / "n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json"
SRC_CENSUS = EX / "n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json"
SRC_V1 = OUT / "class2-lane-next-target-presweep-1452-20261116.json"

POST_MANIFESTS = [
    ("class2-lane-cost66i-win7-certificates-20261116.json", "cost66i"),
    ("class2-lane-cost66j-win7-certificates-20261117.json", "cost66j"),
    ("class2-lane-cost69j-win7-certificates-20261117.json", "cost69j"),
    ("class2-lane-cost71e-certificates/class2-lane-cost71e-win7-certificates-20261117.json", "cost71e"),
    ("class2-lane-cost72d-certificates/class2-lane-cost72d-win7-certificates-20261117.json", "cost72d"),
    ("class2-lane-cost73i-certificates/class2-lane-cost73i-win7-certificates-20261118.json", "cost73i"),
    ("class2-lane-cost73j-certificates/class2-lane-cost73j-win7-certificates-20261117.json", "cost73j"),
    ("class2-lane-cost73k-certificates/class2-lane-cost73k-win7-certificates-20261117.json", "cost73k"),
    ("class2-lane-cost73l-certificates/class2-lane-cost73l-win7-certificates-20261117.json", "cost73l"),
]
FOLD_RECEIPTS = [
    ("class-frontier-cost64h-receipts-recompute-20261117.json", "cost64h"),
    ("class-frontier-cost76c-receipts-recompute-20261117.json", "cost76c"),
]
DUAL_ROOTS = {
    "00000000020001003810000008000000": "cost73i bit97 (third-implementation audit 12/12 PASS)",
    "00000000000000c09002000000001200": "cost66j bit9 (BigInt re-verification 15/15 PASS)",
}

PUBLISHED_FRONTIER_1476 = [1476, 174, 6372, 504389, 4645, 368303]
PUBLISHED_FRONTIER_AFTER = [1589, 174, 6259, 495507, 4543, 360227]

# ------------------------------------------------------------ harvest --------
def find_key(obj, names, depth=0):
    for n in names:
        if n in obj:
            return obj[n]
    if depth < 1:
        for k, v in obj.items():
            if k == "fold":
                continue
            if isinstance(v, dict):
                r = find_key(v, names, depth + 1)
                if r is not None:
                    return r
    return None


def rebuild_harvest():
    v1 = json.loads(SRC_V1.read_bytes())
    harvest = {}
    sources = 0
    for entry in v1["harvest"]["files"]:
        name = entry["file"]
        if "raw-batch" in name:
            continue
        d = json.loads((OUT / name).read_bytes())
        child = None
        for key in ("s6_child_hex", "s6_child", "child"):
            v = d.get(key)
            if isinstance(v, str) and len(v) == 32:
                child = v
                break
        assert child is not None and child == entry["child"], name
        win_bits = find_key(d, ("win7_bits", "win7_d10_bits", "win_bits"))
        if isinstance(win_bits, dict):
            win_bits = [bb for v in win_bits.values() for bb in v]
        win_bits = sorted(set(int(bb) for bb in win_bits))
        ref_bits = find_key(d, ("refuted_d10_bits", "refuted_bits"))
        if ref_bits is not None and not isinstance(ref_bits, list):
            ref_bits = None
        cands = None
        for key in ("legal_candidates", "candidate_bits", "candidates"):
            v = d.get(key)
            if isinstance(v, list) and v and isinstance(v[0], int):
                cands = v
                break
        enum = sorted(legal_candidates(child)[1])
        cands = enum if cands is None else sorted(set(int(bb) for bb in cands))
        assert cands == enum, name
        if ref_bits is None:
            ref_bits = sorted(set(cands) - set(win_bits))
        elif isinstance(ref_bits, dict):
            ref_bits = [bb for v in ref_bits.values() for bb in v]
        else:
            ref_bits = sorted(set(int(bb) for bb in ref_bits))
        assert len(win_bits) == entry["win7"], (name, len(win_bits), entry["win7"])
        assert len(ref_bits) == entry["refuted"], (name, len(ref_bits), entry["refuted"])
        child_v = int(child, 16)
        for b_ in win_bits:
            c = canon(child_v | (1 << b_))
            e = harvest.get(c)
            assert e is None or e["verdict"] == "WIN7-D10", (name, b_)
            harvest[c] = {"verdict": "WIN7-D10", "sources": (e["sources"] if e else []) + [name]}
        for b_ in ref_bits:
            c = canon(child_v | (1 << b_))
            e = harvest.get(c)
            assert e is None or e["verdict"] == "REFUTED-D10", (name, b_)
            harvest[c] = {"verdict": "REFUTED-D10", "sources": (e["sources"] if e else []) + [name]}
        sources += 1
    for prefix, ncand, win_bits, child in (
            ("cost76d", 76, [19, 49], "00000000040000003800080008000000"),
            ("cost77e", 77, [37, 69], "00000000040000809002000000004000")):
        bit_recs = {}
        for n in range(1, 11):
            for line in (OUT / f"class2-lane-{prefix}-raw-batch{n}-20261116.jsonl").read_text().splitlines():
                if not line.strip():
                    continue
                r = json.loads(line)
                if "control" in r:
                    continue
                bit_recs[r["bit"]] = r
        assert len(bit_recs) == ncand, prefix
        child_v = int(child, 16)
        for bb, r in bit_recs.items():
            c = canon(child_v | (1 << bb))
            expect = "WIN7-D10" if r["loss"] is True else "REFUTED-D10"
            e = harvest.get(c)
            assert e is None or e["verdict"] == expect, (prefix, bb)
            harvest[c] = {"verdict": expect, "sources": (e["sources"] if e else []) + [f"{prefix}-raw-batches"]}
        sources += 1
    win = sorted(c for c, v in harvest.items() if v["verdict"] == "WIN7-D10")
    ref = sorted(c for c, v in harvest.items() if v["verdict"] == "REFUTED-D10")
    assert (len(harvest), len(win), len(ref)) == (3548, 353, 3195), (len(harvest), len(win), len(ref))
    return harvest, sources, win, ref


def collect_win_roots(harvest):
    roots = {}
    for c in harvest:
        if harvest[c]["verdict"] == "WIN7-D10":
            roots[c] = "pre-64h harvest: " + ",".join(harvest[c]["sources"][:2])
    for path, tag in POST_MANIFESTS:
        d = json.loads((OUT / path).read_bytes())
        for cert in d.get("certificates", []):
            if cert.get("verdict") not in ("WIN7", "WIN7-D10"):
                continue
            rc = cert.get("d4_canon_root") or canon(int(cert["root"], 16))
            roots[rc] = f"{tag} bit {cert['bit']} manifest"
    for fname, tag in FOLD_RECEIPTS:
        d = json.loads((OUT / fname).read_bytes())
        for rec in d.get("receipts", []):
            if rec.get("verdict") in ("WIN7", "WIN7-D10"):
                roots[rec.get("d4_canon_root") or canon(int(rec["root_hex"], 16))] = f"{tag} published fold receipt bit {rec.get('bit')}"
    for rh, tag in DUAL_ROOTS.items():
        assert canon(int(rh, 16)) == rh
        roots[rh] = tag
    return roots


def main():
    # 1. harvest
    harvest, nsources, win_canons, ref_canons = rebuild_harvest()
    print(f"[1] harvest rebuilt: {nsources} sources, {len(harvest)} canons, {len(win_canons)} WIN, {len(ref_canons)} REFUTED")

    # 2. open rows at head 1476
    rows1410 = {}
    with open(SRC_WORKLIST) as f:
        for r in csv.DictReader(f):
            rows1410[r["s6_canonical_hex"]] = {"category": r["category"], "cost": int(r["own_candidates_s6_s7_edge_cost"])}
    led = json.loads(SRC_LEDGER.read_bytes())
    closed66 = set(led["derived"]["closed_rows_66"])
    open1476 = {h: v for h, v in rows1410.items() if h not in closed66}
    k = json.loads(SRC_CENSUS.read_bytes())
    parents = {p["hex"]: p for p in k["open_s5_census"]}
    parent_set = set(parents)
    # demand-based frontier check of head 1476
    dem = {}
    for h, v in open1476.items():
        m = int(h, 16)
        ps = {canon(m ^ (1 << q)) for q in stones(m)} & parent_set
        dem[h] = sum(1 for p in ps if parents[p]["classes"] & 1)
    f1476 = [1476, 174, len(open1476), sum(v["cost"] for v in open1476.values()),
             sum(1 for c in dem.values() if c == 0),
             sum(open1476[h]["cost"] for h, c in dem.items() if c == 0)]
    assert f1476 == PUBLISHED_FRONTIER_1476, (f1476, PUBLISHED_FRONTIER_1476)
    print(f"[2] head-1476 frontier re-derived and equal to published: {f1476}")

    # 3. global scan
    win_roots = collect_win_roots(harvest)
    print(f"[3] total published WIN7-D10 roots scanned: {len(win_roots)}")
    closable = defaultdict(list)
    for rc in win_roots:
        root = int(rc, 16)
        if bin(root).count("1") != 7:
            raise SystemExit(f"non-7-stone root {rc}")
        for s in {canon(root ^ (1 << p)) for p in stones(root)}:
            if s in open1476:
                closable[s].append((rc, win_roots[rc]))
    assert len(closable) == 113, len(closable)
    n_dual = sum(1 for s, v in closable.items() if any(r in DUAL_ROOTS for r, _ in v))
    assert n_dual == 7, n_dual
    cats = Counter(open1476[s]["category"] for s in closable)
    assert cats == Counter({"unswept": 113}), cats
    total_cost = sum(open1476[s]["cost"] for s in closable)
    assert total_cost == 8882, total_cost
    print(f"[4] closable rows at head 1476: {len(closable)} (dual {n_dual} + scan {len(closable)-n_dual}), cost {total_cost}, all unswept")

    # 4. receipts with transforms, demand, parents
    row_parents, receipts = {}, {}
    for h in sorted(closable):
        m = int(h, 16)
        ps = sorted({canon(m ^ (1 << p)) for p in stones(m)} & parent_set)
        row_parents[h] = ps
        receipts[h] = []
        for rc, tag in closable[h]:
            tf = transform_of(int(rc, 16), m)
            assert tf is not None, (h, rc)
            receipts[h].append({"root": rc, "source": tag, "transform": tf[0], "extra_bit": tf[1]})
    demand = {}
    for h, ps in row_parents.items():
        d = {"c1": 0, "c2": 0, "c4": 0}
        for p in ps:
            b = parents[p]["classes"]
            d["c1"] += bool(b & 1)
            d["c2"] += bool(b & 2)
            d["c4"] += bool(b & 4)
        demand[h] = d
    needed = [h for h in closable if demand[h]["c1"] == 0]
    needed_cost = sum(open1476[h]["cost"] for h in needed)
    assert (len(needed), needed_cost) == (102, 8076), (len(needed), needed_cost)
    print(f"[5] needed rows (c1==0): {len(needed)}, cost {needed_cost}")

    # 5. parents before/after
    p_before, p_lost = defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0])
    for h, v in open1476.items():
        m = int(h, 16)
        for p in {canon(m ^ (1 << q)) for q in stones(m)} & parent_set:
            p_before[p][0] += 1
            p_before[p][1] += v["cost"]
    for h in closable:
        for p in row_parents[h]:
            p_lost[p][0] += 1
            p_lost[p][1] += open1476[h]["cost"]
    fully_closed = sorted(p for p in p_lost if p_before[p][0] == p_lost[p][0])
    assert fully_closed == [], fully_closed
    print(f"[6] affected parents: {len(p_lost)}, incidences {sum(v[0] for v in p_lost.values())}, cost delta {sum(v[1] for v in p_lost.values())}, fully closed: {len(fully_closed)}")

    # 6. frontier after
    open_after = {h: v for h, v in open1476.items() if h not in closable}
    dem_after = {}
    for h, v in open_after.items():
        m = int(h, 16)
        ps = {canon(m ^ (1 << q)) for q in stones(m)} & parent_set
        dem_after[h] = sum(1 for p in ps if parents[p]["classes"] & 1)
    frontier_after = [1476 + 113, 174, len(open_after), sum(v["cost"] for v in open_after.values()),
                      sum(1 for c in dem_after.values() if c == 0),
                      sum(open_after[h]["cost"] for h, c in dem_after.items() if c == 0)]
    assert frontier_after == PUBLISHED_FRONTIER_AFTER, (frontier_after, PUBLISHED_FRONTIER_AFTER)
    print(f"[7] frontier after mega-fold: {frontier_after}")

    # 7. controls
    # C1: already-folded 66i bit19 root closes no new open row at head 1476
    r66i = int("00000000000000801226000000080000", 16)
    c1_rows = sorted({canon(r66i ^ (1 << p)) for p in stones(r66i)} & set(open1476))
    assert c1_rows == [], c1_rows
    # C2: its published fold rows are in the ledger-closed set, consistent
    c2_rows = sorted({canon(r66i ^ (1 << p)) for p in stones(r66i)} & closed66)
    assert set(c2_rows) <= set(led["derived"]["closed_rows_66"]), c2_rows
    # C3: sample receipts have valid transforms and legal roots (5 rows)
    for row in ["00000000000000c09002000000400000", "00000000000000801206000000000400",
                "00000000000000403800000008004000", "00000000000000403800000408000000",
                "00000000000000403800000008000020"]:
        rec = receipts[row][0]
        rv = int(rec["root"], 16)
        assert bin(rv).count("1") == 7
        assert (int(row, 16) & ~d4(rv, rec["transform"])) == 0
        nbits = len(legal_candidates(rec["root"])[1])
        assert 40 <= nbits <= 70, (row, nbits)
    # C4: no overlap with the 35-row STERILE registry
    sterile = {r["hex"] for r in k["sterile_row_registry"]}
    assert not (sterile & set(closable)), sorted(sterile & set(closable))
    print("[8] controls C1-C4: PASS")

    # 8. source pins
    def pin(p):
        return git_blob_sha(p.read_bytes())
    srcs = {
        "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv": SRC_WORKLIST,
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json": SRC_LEDGER,
        "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json": SRC_CENSUS,
        "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-target-presweep-1452-20261116.json": SRC_V1,
    }
    for path, _ in POST_MANIFESTS:
        srcs[f"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/{path}"] = OUT / path
    for fname, _ in FOLD_RECEIPTS:
        srcs[f"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/{fname}"] = OUT / fname
    v1 = json.loads(SRC_V1.read_bytes())
    for entry in v1["harvest"]["files"]:
        name = entry["file"]
        if "raw-batch" not in name:
            srcs.setdefault(f"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/{name}", OUT / name)
    for n in range(1, 11):
        for prefix in ("cost76d", "cost77e"):
            name = f"class2-lane-{prefix}-raw-batch{n}-20261116.jsonl"
            srcs[f"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/{name}"] = OUT / name
    source_blob_pins = {k: pin(v) for k, v in sorted(srcs.items())}
    print(f"[9] pinned {len(source_blob_pins)} source blobs")

    record = {
        "schema": "n11-class2-lane-receipt-harvest-global-fold-20261118-v1",
        "date": "2026-11-18",
        "status": "fold-complete",
        "basis_head": {
            "solved_s6_in_manifest": 1476,
            "remaining_s5_orbits": 174,
            "unique_remaining_s6": 6372,
            "sum_remaining_cost": 504389,
            "s6_needed_by_open_classes": 4645,
            "cost_needed_by_open_classes": 368303,
        },
        "frontier_after_receipt_harvest_global_fold": {
            "solved_s6_in_manifest": frontier_after[0],
            "remaining_s5_orbits": frontier_after[1],
            "unique_remaining_s6": frontier_after[2],
            "sum_remaining_cost": frontier_after[3],
            "s6_needed_by_open_classes": frontier_after[4],
            "cost_needed_by_open_classes": frontier_after[5],
        },
        "method": {
            "harvest_rebuild": f"{nsources} pinned sources; {len(harvest)} canons ({len(win_canons)} WIN7-D10 / {len(ref_canons)} REFUTED-D10), equal to census v1 published totals",
            "win_roots_scanned": len(win_roots),
            "row_closability_rule": "open S6 row R is closable iff some published WIN7-D10 root X (7 stones) has a D4 transform sigma with R a subset of sigma(X) (one-stone reduction); receipt = orbit-level certificate transfer",
            "why_not_found_earlier": "previous folds scanned per-band receipts against one parent's top rows at a time; no prior fold scanned the full published WIN-root set against the full open worklist",
        },
        "receipts_by_row": [
            {
                "row_hex": h,
                "cost": open1476[h]["cost"],
                "category": open1476[h]["category"],
                "demand": demand[h],
                "parents": row_parents[h],
                "receipts": receipts[h],
            }
            for h in sorted(closable)
        ],
        "totals": {
            "rows_closed": 113,
            "dual_fold_rows": 7,
            "global_scan_rows": 106,
            "s6_edge_cost_removed": 8882,
            "needed_rows_closed": 102,
            "needed_cost_removed": 8076,
        },
        "parents_after": {
            p: {
                "s5_hex": p,
                "classes": parents[p]["classes"],
                "rows_before": p_before[p][0],
                "rows_after": p_before[p][0] - p_lost[p][0],
                "edge_cost_before": p_before[p][1],
                "edge_cost_after": p_before[p][1] - p_lost[p][1],
                "lost_rows": p_lost[p][0],
                "lost_edge_cost": p_lost[p][1],
            }
            for p in sorted(p_lost)
        },
        "parent_row_incidences": sum(v[0] for v in p_lost.values()),
        "parent_edge_cost_delta": sum(v[1] for v in p_lost.values()),
        "parent_count_fully_closed": 0,
        "notable_parent": {
            "s5_hex": "00000000000000403800000008000000",
            "classes": 2,
            "rows_before": 12,
            "rows_after": 1,
            "rows_after_hexes": ["00000000000000403800000008000008"],
            "edge_cost_before": 806,
            "edge_cost_after": 78,
        },
        "controls": {
            "C1_already_folded_66i_bit19_root_closes_no_open_row": "PASS (0 rows)",
            "C2_66i_bit19_fold_rows_consistent_with_ledger": "PASS",
            "C3_sample_receipt_transforms_valid_5_of_5": "PASS",
            "C4_sterile_registry_overlap": "PASS (0 of 35)",
            "frontier_before_match": "head-1476 six-tuple independently re-derived and equal to published",
        },
        "conflict_census": {
            "verdict_conflicts_among_sources": 0,
            "overlap_with_sterile_registry": 0,
        },
        "source_blob_pins": source_blob_pins,
        "certificate_manifest": {
            "pre-64h harvest WIN canons": "each canon inherits its published per-band WIN7-D10 certificate manifest (see source_blob_pins; per-band audits: BigInt rational / third-implementation, published separately)",
            "post-64h manifests": "cost66i/66j/69j/71e/72d/73i/73j/73k/73l WIN7 certificate manifests as pinned",
            "dual roots": {
                "cost73i_bit97": "root 00000000020001003810000008000000; third-implementation audit 12/12 PASS (sha256 bf310fe5..., record pinned)",
                "cost66j_bit9": "root 00000000000000c09002000000001200; BigInt re-verification 15/15 PASS (sha256 b2686e22..., record pinned)",
            },
            "independent_verifiability": "the fold adds no new engine verdict; every receipt is a published WIN7-D10 certificate; this audit re-derives the full fold from the pinned sources without any engine run",
        },
        "input_snapshot": "none needed: the audit re-derives all inputs from source_blob_pins (harvest from 79 census-v1 sources, worklist-1410 CSV minus fold-chain ledger closed rows)",
        "interpretation_guard": "Bookkeeping fold over published, independently verified WIN7-D10 receipts. It closes 113 S6 manifest rows and reduces open frontier demand; it closes no S5 parent fully, creates no new engine verdict, and does not solve the standard 11x11 empty board (11x11 remains UNKNOWN).",
        "next_action": "Sweep the last open row 00000000000000403800000008000008 (cost 78) of class-2 parent 00000000000000403800000008000000 per census v20; a WIN bit there completes the first fully receipt-closed S5 parent, an all-REFUTED result makes the parent D10-unclosable.",
    }
    outp = OUT / "class-frontier-receipt-harvest-global-fold-20261118.json"
    outp.write_text(json.dumps(record, indent=1) + "\n")
    print(f"[10] wrote {outp.name}: {outp.stat().st_size} bytes")


if __name__ == "__main__":
    main()
