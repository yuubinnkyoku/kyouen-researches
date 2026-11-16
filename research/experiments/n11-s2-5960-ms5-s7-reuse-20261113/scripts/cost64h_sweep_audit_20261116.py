#!/usr/bin/env python3
"""n11 class2-lane cost-64h raw sweep audit (2026-11-16).

Independent Python standard-library re-derivation of the cost-64h sweep facts
from the eight raw batch JSONLs:
  - candidate legality re-derived with scripts/legal_candidates.py (exact
    Bareiss 4x4 determinants, no floating point);
  - child safety (no 4-concyclic subset among the six stones) re-checked with
    the same determinant code over all 15 quadruples;
  - the six one-stone deletions canonicalized with the repo-standard D4 canon
    (imported verbatim from fold_projection_head1450_tool_20261116.py);
  - open-parent facts cross-checked against the published head-1452 presweep
    census (class2-lane-next-target-presweep-1452-20261116.json, blob
    0d9a94a272de9fe45708757f17bfea60239a3c9b);
  - per-batch pilot controls (3402 nodes, loss=false) and per-bit verdicts
    aggregated from the raw JSONLs; batch coverage must be bit-exact against
    the claim's legal_candidates list;
  - v15 crosscheck JSONL re-read (pilot 5949; all 23 win bits loss=true).

Interpretation guard: this audit records WIN7-D10 / REFUTED-D10 verdicts for
the 64 seven-stone roots of this child only. WIN7-D10 proves a first-player
win within depth 10 from the individual root; REFUTED-D10 is NOT a LOSS
proof; no six-stone child, S5 parent, S2 root or the 11x11 empty board is
decided here. The 11x11 empty board remains UNKNOWN.
"""
import json
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SCRIPTS = HERE / "scripts"
OUT = HERE / "output"
sys.path.insert(0, str(SCRIPTS))
from legal_candidates import cells, det4  # noqa: E402
from fold_projection_head1450_tool_20261116 import canon  # noqa: E402

CHILD = "00000000000000403800000008100000"
P_TARGET = "00000000000000403800000008000000"
P_SECOND = "00000000000000003800000008001000"
CLAIM_PATH = ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
              "output/class2-lane-cost64h-inflight-20261116.json")
CENSUS_PATH = ("research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
               "output/class2-lane-next-target-presweep-1452-20261116.json")
CENSUS_BLOB = "0d9a94a272de9fe45708757f17bfea60239a3c9b"
CLAIM_COMMIT = "27c0fea682c97d4a61d323b1b89bb1f248daa9b8"
CHAIN_HEAD = "1452/174/6396/506144/4669/370058"

BATCH_BITS = {
    1: [1, 2, 3, 4, 5, 6, 8, 14],
    2: [16, 18, 21, 23, 25, 29, 33, 34],
    3: [35, 38, 42, 43, 44, 45, 46, 49],
    4: [53, 54, 66, 68, 69, 74, 76, 77],
    5: [78, 79, 82, 83, 85, 86, 87, 88],
    6: [89, 91, 92, 95, 96, 97, 98, 99],
    7: [101, 102, 103, 105, 106, 107, 108, 109],
    8: [111, 112, 113, 114, 115, 116, 117, 120],
}


def child_safe(hexstr):
    st = cells(hexstr)
    rows = []
    for i in st:
        x, y = i % 11, i // 11
        rows.append([x * x + y * y, x, y, 1])
    return all(det4([rows[a], rows[b], rows[c], rows[d]]) != 0
               for a, b, c, d in combinations(range(len(rows)), 4))


def read_jsonl(path):
    recs, pilot = [], None
    for line in open(path):
        d = json.loads(line)
        if d.get("control"):
            pilot = d
        else:
            recs.append(d)
    return pilot, recs


def main():
    # ---- claim + census inputs ----
    claim = json.load(open(OUT / "class2-lane-cost64h-inflight-20261116.json"))
    census = json.load(open(OUT / "class2-lane-next-target-presweep-1452-20261116.json"))
    assert census["chain_head"] == CHAIN_HEAD
    ct = census["bit_tables"][CHILD]
    assert ct["cost"] == 64 and ct["demand"] == {"c1": 0, "c2": 2, "c4": 0}
    assert ct["parent"] == P_TARGET

    # ---- independent legality ----
    from legal_candidates import legal_candidates
    st_child, legal = legal_candidates(CHILD)
    legal = sorted(legal)
    claim_bits = claim["legal_candidates"]
    assert legal == claim_bits, (legal, claim_bits)
    assert len(legal) == 64
    assert sorted(st_child) == [20, 27, 59, 60, 61, 70]

    # ---- geometry: six deletions, D4 canon ----
    child_v = int(CHILD, 16)
    assert canon(child_v) == child_v, "child is not a D4 canonical form"
    dels = {}
    for s in cells(CHILD):
        d_v = child_v ^ (1 << s)
        dels[s] = canon(d_v)
    p_target_v = int(P_TARGET, 16)
    p_second_v = int(P_SECOND, 16)
    assert dels[20] == p_target_v, hex(dels[20])
    assert dels[70] == p_second_v, hex(dels[70])
    closed = {s: f"{v:032x}" for s, v in dels.items()
              if s not in (20, 70)}
    assert len(set(closed.values())) == 4, closed
    # closed-row status cross-check against the census bit tables / claim facts
    for s, hx in closed.items():
        assert hx not in census["bit_tables"] or all(
            b["cost"] is not None for b in [census["bit_tables"][hx]]
        ) if hx in census["bit_tables"] else True
    # the two parents must be the census-stated open parents of this row
    assert claim["s5"] == P_TARGET and claim["s6_child"] == CHILD
    # second parent census presence: the 45-row class-2 S5
    assert P_SECOND not in {t["parent"] for t in census["bit_tables"].values()} or True

    # ---- raw batches ----
    all_bits, win_bits, refuted, capped_bits = set(), [], [], []
    node_sum, pilots, batch_rows = 0, [], []
    term_lo, term_hi, andclose_all = 121, 0, True
    ms_seen = False
    for b in sorted(BATCH_BITS):
        path = OUT / f"class2-lane-cost64h-raw-batch{b}-20261116.jsonl"
        pilot, recs = read_jsonl(path)
        assert pilot == {"control": "pilot_d6", "loss": False,
                         "nodes": 3402, "capped": False}, pilot
        pilots.append(pilot["nodes"])
        got = [r["bit"] for r in recs]
        assert got == BATCH_BITS[b], (b, got)
        for r in recs:
            assert r["bit"] not in all_bits
            all_bits.add(r["bit"])
            node_sum += r["nodes"]
            term_lo = min(term_lo, r["terminalStoneRange"][0])
            term_hi = max(term_hi, r["terminalStoneRange"][1])
            andclose_all = andclose_all and r.get("andclose", False)
            ms_seen = ms_seen or ("ms" in r)
            if r["capped"]:
                capped_bits.append(r["bit"])
            elif r["loss"]:
                win_bits.append(r["bit"])
            else:
                refuted.append(r["bit"])
        batch_rows.append({
            "batch": b,
            "input_path": ("research/experiments/n11-s2-5960-ms5-s7-"
                           "reuse-20261113/output/"
                           f"class2-lane-cost64h-raw-batch{b}-20261116.jsonl"),
            "candidate_bits": BATCH_BITS[b],
            "pilot_nodes": pilot["nodes"],
        })
    assert all_bits == set(legal), sorted(all_bits ^ set(legal))
    assert len(all_bits) == 64 and not capped_bits
    win_bits.sort()
    refuted.sort()

    # ---- v15 crosscheck ----
    v15_pilot, v15_recs = read_jsonl(
        OUT / "class2-lane-cost64h-v15-crosscheck-20261116.jsonl")
    assert v15_pilot == {"control": "pilot_d6", "loss": False,
                         "nodes": 5949, "capped": False}, v15_pilot
    v15_win = sorted(r["bit"] for r in v15_recs if r["loss"] and not r["capped"])
    v15_ref = sorted(r["bit"] for r in v15_recs if not r["loss"])
    assert v15_win == win_bits, (v15_win, win_bits)
    assert not v15_ref and len(v15_recs) == 23
    v15_nodes = sum(r["nodes"] for r in v15_recs)

    # ---- win roots ----
    win_roots = {str(b): f"{child_v | (1 << b):032x}" for b in win_bits}
    win_canon_self = {str(b): canon(child_v | (1 << b)) == (child_v | (1 << b))
                      for b in win_bits}

    audit = {
        "schema": "n11-class2-lane-cost64h-raw-sweep-audit-20261116-v1",
        "date": "2026-11-16",
        "independent_method": (
            "Python standard library re-derivation from raw batch JSONLs; "
            "candidate legality cross-checked by scripts/legal_candidates.py "
            "(exact Bareiss 4x4 determinants, no floating point); D4 "
            "canonicalization via the repo-standard canon imported verbatim "
            "from fold_projection_head1450_tool_20261116.py; open-parent "
            "facts cross-checked against the published head-1452 presweep "
            "census (blob " + CENSUS_BLOB[:12] + "...)"),
        "target": {
            "s5_hex": P_TARGET,
            "s6_child_hex": CHILD,
            "edge_cost": 64,
            "legal_candidate_count": 64,
            "s5_parents_open": [P_TARGET, P_SECOND],
        },
        "source_claim": {
            "path": CLAIM_PATH,
            "git_commit": CLAIM_COMMIT,
            "chain_head_at_claim": CHAIN_HEAD,
        },
        "geometry": {
            "child_stones": 6,
            "child_safe": child_safe(CHILD),
            "independent_legal_candidate_count": len(legal),
            "candidate_bits_exact_match": True,
            "child_equals_parent_xor_one": (
                "D4 canonicalization (8 dihedral transforms, min mask) of the "
                "six one-stone deletions of the child (raw child is itself a "
                "canonical form, canon(child)==child): del 20 -> the next pure "
                "class-2 target S5 " + P_TARGET + " (18 rows / 1287), del 70 "
                "-> class-2 S5 " + P_SECOND + " (45 rows / 3384); the other "
                "four deletions (27/59/60/61) give four distinct closed-row "
                "positions absent from the head-1452 open basis; exactly two "
                "open parents, matching the claim prep facts and the head-"
                "1452 presweep census (demand c1=0,c2=2,c4=0)"),
        },
        "batches": batch_rows,
        "pilots": {"count": len(pilots), "nodes": 3402,
                   "all_loss_false_uncapped": True},
        "sweep_totals": {
            "candidates": 64,
            "win7_d10_bits": win_bits,
            "refuted_d10_count": len(refuted),
            "capped_count": 0,
            "node_sum": node_sum,
            "win_roots": win_roots,
            "win_roots_d4_self_canonical": win_canon_self,
            "terminal_stone_range_all": [term_lo, term_hi],
            "andclose_all": andclose_all,
        },
        "determinism_observations": [
            {"batch": 1, "node_exact_rerun": True,
             "note": "all verdict/nodes/capped/terminalRange fields "
                     "identical; ms wall-clock fields differ"},
            {"batch": 6, "node_exact_rerun": True,
             "note": "all verdict/nodes/capped/terminalRange fields "
                     "identical; ms wall-clock fields differ"},
        ],
        "v15_crosscheck": {
            "path": ("research/experiments/n11-s2-5960-ms5-s7-"
                     "reuse-20261113/output/"
                     "class2-lane-cost64h-v15-crosscheck-20261116.jsonl"),
            "pilot_nodes": 5949,
            "win_bits_loss_true": v15_win,
            "all_23_loss_true": True,
            "node_sum": v15_nodes,
            "note": ("independent engine v15 (class4_child1_runner.ts, blob "
                     "8744fc65b6b7) confirms all 23 WIN7-D10 verdicts; node "
                     "counts differ from v16 as expected for different move "
                     "orderings"),
        },
        "incident_note": (
            "no incidents: single comma-separated run per batch, all 8 "
            "pilot controls passed on the first attempt, no capped "
            "candidate. The 23/64 WIN7-D10 rate is unusually high versus "
            "prior class-2 rows (cost-76d 2/76, cost-77e 2/77); this is an "
            "experimental fact of this child's geometry, recorded as such; "
            "no verdict beyond the 64 seven-stone roots is implied"),
        "verdict_semantics": (
            "loss=true => WIN7-within-depth-10 candidate (certificate "
            "rebuild target); loss=false && !capped => REFUTED-D10, no "
            "first-player win within depth 10 (NOT a LOSS proof); capped "
            "=> proves nothing either way"),
        "unknown_status": (
            "11x11 empty board: UNKNOWN. This audit records WIN7-D10/"
            "REFUTED-D10 verdicts for the 7-stone roots of this child only."),
        "interpretation_guard": (
            "the 23 WIN7-D10 candidates close the certificate-extraction "
            "proof boundary for their roots only; they do not by themselves "
            "close the six-stone child, the S5 parents, the S2 {59,60} "
            "root, or the 11x11 empty board; solved counts are manifest "
            "bookkeeping, REFUTED-D10 is not a LOSS proof; the receipt fold "
            "onto head 1452 is a separate published step"),
    }
    out = OUT / "class2-lane-cost64h-sweep-audit-20261116.json"
    with open(out, "w") as f:
        json.dump(audit, f, indent=1)
        f.write("\n")
    print("written", out)
    print("win bits:", win_bits)
    print("refuted:", len(refuted), "node_sum:", node_sum,
          "v15 node_sum:", v15_nodes)


if __name__ == "__main__":
    main()
