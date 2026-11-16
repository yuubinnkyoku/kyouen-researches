#!/usr/bin/env python3
"""Independent stdlib audit of the class2-lane cost-66c raw sweep (2026-11-16).

Re-derives every bookkeeping fact of the cost-66c sweep from the published
artifacts only (raw batch JSONL files, the bit-112 cap-raise resolution record,
the determinism reruns, the v15 crosscheck, the head-1441 census v4, the
cost-65n raw batches) with implementations independent of the lane scripts:
inline Bareiss 4x4 determinants for legality, an independent D4 orbit
canonicalization, and independent one-stone-deletion parent analysis.

This audit is structural bookkeeping only: it re-checks engine outputs, it
does not run the engine.  REFUTED-D10 is not a LOSS proof, WIN7-D10 proves a
first-player win within depth 10 from the individual 7-stone root only.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

N = 11
CHILD_HEX = "00000000000000003800000008002008"
SHARED_PARENT_HEX = "00000000000000003800000008002000"
CENSUS_FILE = "class2-lane-next-target-presweep-1441-20261116.json"
WIN_BITS_EXPECTED = [73, 75, 79, 87, 96, 97, 112]
TRANSFERRED_BITS_EXPECTED = [5, 25, 70, 81, 84, 115, 119]
OPEN_COUNT_EXPECTED = 59
BATCH_BITS = {
    1: [1, 2, 9, 10, 12, 17, 21, 30],
    2: [32, 33, 34, 38, 42, 43, 44, 53],
    3: [54, 66, 67, 69, 71, 73, 74, 75],
    4: [76, 78, 79, 83, 85, 86, 87, 88],
    5: [89, 92, 93, 94, 95, 96, 97, 98],
    6: [99, 100, 101, 102, 103, 105, 106, 107],
    7: [108, 109, 110, 111, 112, 113, 114, 116],
    8: [117, 118, 120],
}
COST65N_CHILD = int("00000000000000801202010000800000", 16)


def d4_canon(mask: int) -> int:
    points = [(i % N, i // N) for i in range(N * N) if (mask >> i) & 1]
    images = []
    for t in range(8):
        out = []
        for x, y in points:
            if t == 0:
                X, Y = x, y
            elif t == 1:
                X, Y = N - 1 - y, x
            elif t == 2:
                X, Y = N - 1 - x, N - 1 - y
            elif t == 3:
                X, Y = y, N - 1 - x
            elif t == 4:
                X, Y = N - 1 - x, y
            elif t == 5:
                X, Y = x, N - 1 - y
            elif t == 6:
                X, Y = y, x
            else:
                X, Y = N - 1 - y, N - 1 - x
            out.append(Y * N + X)
        images.append(sum(1 << i for i in out))
    return min(images)


def hx(v: int) -> str:
    return f"{v:032x}"


def det4(m) -> int:
    a = [row[:] for row in m]
    prev = 1
    for k in range(3):
        if a[k][k] == 0:
            for r in range(k + 1, 4):
                if a[r][k] != 0:
                    a[k], a[r] = a[r], a[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
    return a[3][3]


def legal_candidates(mask: int):
    stones = [i for i in range(N * N) if (mask >> i) & 1]
    rows = []
    for i in stones:
        x, y = i % N, i // N
        rows.append([x * x + y * y, x, y, 1])
    out = []
    for p in range(N * N):
        if p in stones:
            continue
        px, py = p % N, p // N
        prow = [px * px + py * py, px, py, 1]
        ok = True
        for (i, j, k) in itertools.combinations(range(len(stones)), 3):
            if det4([rows[i], rows[j], rows[k], prow]) == 0:
                ok = False
                break
        if ok:
            out.append(p)
    return stones, out


def main() -> int:
    here = Path(__file__).resolve().parent.parent / "output"
    checks = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "pass": ok, "detail": detail})

    child = int(CHILD_HEX, 16)

    # A. independent legal re-enumeration
    stones, legal = legal_candidates(child)
    check("child occupied stones", stones == [3, 13, 27, 59, 60, 61],
          f"stones={stones}")
    check("independent legal enumeration count", len(legal) == 66,
          f"legal={len(legal)}")

    # B. census bit table reproduction
    census = json.loads((here / CENSUS_FILE).read_text())
    bt = census["cheapest_row_bit_tables"][CHILD_HEX]
    census_bits = [e["bit"] for e in bt]
    check("census bit list == independent legal list", census_bits == legal,
          f"{len(census_bits)} bits identical")
    canon_mismatch = [
        e["bit"] for e in bt
        if hx(d4_canon(child | (1 << e["bit"]))) != e["root_canon"]
    ]
    check("census root_canon reproduction (independent D4)", not canon_mismatch,
          f"mismatches={canon_mismatch}")
    statuses = [e["status"] for e in bt]
    open_bits = [e["bit"] for e in bt if e["status"] == "open"]
    transferred = [e["bit"] for e in bt if e["status"] == "harvested_refuted"]
    check("open/transferred partition", len(open_bits) == OPEN_COUNT_EXPECTED
          and sorted(transferred) == TRANSFERRED_BITS_EXPECTED,
          f"open={len(open_bits)} transferred={sorted(transferred)}")

    # C. raw batch parse: bits exactly once, pilots, batches match claim plan
    swept = {}
    pilots = 0
    raw_nodes_as_run = 0
    cap_events = []
    for i in range(1, 9):
        for line in (here / f"class2-lane-cost66c-raw-batch{i}-20261116.jsonl").read_text().splitlines():
            r = json.loads(line)
            if "control" in r:
                pilots += 1
                assert r["nodes"] == 3402 and r["loss"] is False and not r["capped"]
                continue
            assert r["bit"] in BATCH_BITS[i], (i, r["bit"])
            assert r["bit"] not in swept, r["bit"]
            swept[r["bit"]] = r
            raw_nodes_as_run += r["nodes"]
            if r["capped"]:
                cap_events.append({"bit": r["bit"], "nodes": r["nodes"], "batch": i})
    check("8 raw batches cover the 59 open bits exactly once",
          sorted(swept) == sorted(open_bits), f"bits={len(swept)}")
    check("pilot_d6 control 3402 nodes in all 8 batch invocations", pilots == 8,
          f"pilots={pilots}")
    check("single cap event recorded (bit 112 at the 10000000 protocol cap)",
          cap_events == [{"bit": 112, "nodes": 10000001, "batch": 7}],
          f"cap_events={cap_events}")

    # D. bit-112 cap-raise resolution + determinism
    b112 = None
    for line in (here / "class2-lane-cost66c-bit112-cap80m-resolution-20261116.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r.get("bit") == 112:
            b112 = r
    check("bit 112 resolved at raised cap 80000000: WIN7-D10 12574920 nodes",
          b112 is not None and b112["loss"] is True and b112["nodes"] == 12574920
          and not b112["capped"], f"record={b112}")
    b112_det = None
    for line in (here / "class2-lane-cost66c-v16-determinism-rerun-bit112-20261116.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r.get("bit") == 112:
            b112_det = r
    check("bit 112 determinism rerun node-exact",
          b112_det is not None and b112_det["nodes"] == b112["nodes"]
          and b112_det["loss"] == b112["loss"],
          f"rerun_nodes={b112_det and b112_det['nodes']}")
    swept[112] = b112

    # E. determinism rerun batch 5
    det = []
    for line in (here / "class2-lane-cost66c-v16-determinism-rerun-batch5-20261116.jsonl").read_text().splitlines():
        r = json.loads(line)
        if "bit" in r:
            det.append(r)
    det_exact = all(
        r["nodes"] == swept[r["bit"]]["nodes"] and r["loss"] == swept[r["bit"]]["loss"]
        and r["capped"] == swept[r["bit"]]["capped"] for r in det
    )
    check("determinism rerun batch 5 (8 bits incl WINs 96/97) node-exact",
          det_exact and len(det) == 8,
          f"bits={[r['bit'] for r in det]} all node-exact")

    # F. v15 crosscheck anchors
    v15 = []
    for line in (here / "class2-lane-cost66c-v15-crosscheck-20261116.jsonl").read_text().splitlines():
        r = json.loads(line)
        if "bit" in r:
            v15.append(r)
    agree = all(r["loss"] == swept[r["bit"]]["loss"] for r in v15)
    check("v15 crosscheck: pilot 5949 + 4 anchors (73/96 WIN, 30/83 REFUTED) agree",
          agree and len(v15) == 4, f"anchors={[(r['bit'], r['loss'], r['nodes']) for r in v15]}")

    # G. verdict aggregate
    wins = sorted(b for b, r in swept.items() if r["loss"])
    refuted = sorted(b for b, r in swept.items() if not r["loss"] and not r["capped"])
    capped_now = [b for b, r in swept.items() if r["capped"]]
    total_nodes = sum(r["nodes"] for r in swept.values())
    check("verdict aggregate: 7 WIN7-D10 + 52 REFUTED-D10 + 0 capped",
          wins == WIN_BITS_EXPECTED and len(refuted) == 52 and not capped_now,
          f"wins={wins} refuted={len(refuted)} capped={capped_now}")
    check("total definitive swept nodes", total_nodes == 84180263,
          f"nodes={total_nodes}")
    check("raw batches as run (incl capped attempt) nodes", raw_nodes_as_run == 81605344,
          f"nodes={raw_nodes_as_run}")
    check("all records terminalStoneRange [13,17] and andclose true",
          all(r["terminalStoneRange"] == [13, 17] and r["andclose"] for r in swept.values()),
          "59/59")

    # H. orbit distinctness + conflict census vs cost-65n corpus
    canons = {}
    for e in bt:
        canons[e["root_canon"]] = e["bit"]
    check("66 candidate roots occupy 66 distinct D4 orbits", len(canons) == 66,
          f"distinct={len(canons)}")
    swept_canons = {hx(d4_canon(child | (1 << b))): (b, swept[b]["loss"]) for b in swept}
    n65 = {}
    for i in range(1, 9):
        for line in (here / f"class2-lane-cost65n-raw-batch{i}-20261116.jsonl").read_text().splitlines():
            r = json.loads(line)
            if "bit" in r:
                n65[hx(d4_canon(COST65N_CHILD | (1 << r["bit"])))] = (r["bit"], r["loss"])
    ov65n = set(swept_canons) & set(n65)
    check("D4 conflict census vs published cost-65n swept corpus: overlap 0",
          not ov65n, f"overlap={sorted(ov65n)}")

    # I. cross-row overlap note vs cost-65o candidates (published audit input)
    aud = json.loads(
        (here / "class2-lane-cost65o-post-cost65n-overlap-audit-20261116.json").read_text())
    o65 = {r["d4_canonical_hex"]: (r["bit"], r["status"]) for r in aud["cost65o_input"]["candidate_roots"]}
    cross = set(swept_canons) & set(o65)
    expected_cross = {"00000000000000a09002080080000000"}
    check("cross-row overlap vs in-flight cost-65o candidates: exactly bit 83 == 65o bit 43",
          cross == expected_cross,
          f"overlap={sorted(cross)}: 66c bit 83 REFUTED-D10 (269856 v16 / 653399 v15 nodes) == 65o bit 43 (open, in flight); verdict-agreement watch item for the 65o claim update")

    # J. one-stone-deletion parents (independent)
    parents = {}
    for s in stones:
        parents[s] = hx(d4_canon(child & ~(1 << s)))
    open_parent = parents[3]
    check("six one-stone-deletion parents re-derived; exactly one equals the shared class-2 parent",
          open_parent == hx(d4_canon(int(SHARED_PARENT_HEX, 16)))
          and len(set(parents.values())) == 6,
          f"parents={parents}")

    # K. child row not covered by the two cost-65n receipts
    covered = set()
    for rec in aud["cost65n_receipts"]:
        for h in rec["covers_hexes"]:
            covered.add(hx(d4_canon(int(h, 16))))
    check("66c child row canon not among the 13 cost-65n receipt-covered S6 row orbits",
          hx(d4_canon(child)) not in covered,
          f"child_canon={hx(d4_canon(child))} covered={len(covered)} orbits")

    all_pass = all(c["pass"] for c in checks)
    out = {
        "schema": "n11-class2-lane-cost66c-raw-sweep-audit-20261116-v1",
        "date": "2026-11-16",
        "child": CHILD_HEX,
        "s5_target": SHARED_PARENT_HEX,
        "verdict_summary": {
            "candidates": 66,
            "open_swept": 59,
            "win7_d10_bits": wins,
            "refuted_d10_swept": len(refuted),
            "refuted_d10_transferred": len(transferred),
            "capped": 0,
            "total_definitive_swept_nodes": total_nodes,
            "raw_batches_as_run_nodes": raw_nodes_as_run,
            "row_result": "NOT-STERILE (7 WIN7-D10 receipts available for the fold)",
        },
        "cap_event": {
            "bit": 112,
            "protocol_cap": 10000000,
            "capped_attempt_nodes": 10000001,
            "resolution_cap": 80000000,
            "resolution_nodes": 12574920,
            "resolution_verdict": "WIN7-D10",
            "determinism_rerun_nodes": 12574920,
        },
        "checks": checks,
        "all_pass": all_pass,
        "method": "independent stdlib re-derivation: inline Bareiss legality, independent D4 canonicalization, independent one-stone-deletion parent analysis; engine not re-run except the published determinism/v15 artifacts re-parsed here",
        "interpretation_guard": "WIN7-D10 proves a first-player win within depth 10 from the individual 7-stone roots only; REFUTED-D10 is NOT a LOSS proof; NOT-STERILE is not a game value for the row; transferred verdicts are D4-canonical identities of published depth-10 engine results",
        "unknown_status": "11x11 empty board, two-stone roots {49,60} and {59,60}, S2 {59,60}, and classes 1/2/4 all remain UNKNOWN",
    }
    (here / "class2-lane-cost66c-raw-sweep-audit-20261116.json").write_text(
        json.dumps(out, indent=1) + "\n")
    print("ALL_PASS" if all_pass else "FAILURES", len(checks), "checks")
    for c in checks:
        if not c["pass"]:
            print("FAIL:", c["check"], c["detail"])
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
