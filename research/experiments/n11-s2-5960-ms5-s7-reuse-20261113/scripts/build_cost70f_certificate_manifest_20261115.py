#!/usr/bin/env python3
"""Build the cost-70f WIN7 certificate manifest (4/4) for the n11 class-2 lane.

Child 00000000000000801202000002200000 (second coverable class-2 target S5,
edge cost 70, demand c1=0,c2=2,c4=0), WIN7-D10 roots bits 9, 64, 72, 84.

Inputs:
  * class2-lane-cost70f-sweep-audit-20261115.json  (v16 nodes, mobility, roots)
  * tmp-cost70f/legal-moves.json                   (independent legal-reply lists)
  * class2-lane-cost70f-certificates/              (4 single-file certificates)
  * tmp-cost70f/bit{bit}.rows.summary.json         (blind extraction summaries)
  * tmp-cost70f/bit{bit}.bigint.json               (BigInt verifier outputs)
  * tmp-cost70f/bit{bit}.tsverify.json             (Number Bareiss verifier outputs)
  * tmp-cost70f/bit{bit}.consumed.txt              (consumed winner states)

The manifest records the whole-file hashes of the LF certificate content, the
independent verifier results, and the D4 parent-lift orbits.  No frontier count
is changed here.
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost70f-certificates"
TMP = OUT / "tmp-cost70f"
ROOT = HERE.parent.parent.parent
CHILD = "00000000000000801202000002200000"
ROOTS = {
    9: "00000000000000801202000002200200",
    64: "00000000000000811202000002200000",
    72: "00000000000001801202000002200000",
    84: "00000000001000801202000002200000",
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def cells(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(121) if (v >> i) & 1]


def det4(pts):
    a = []
    for p in pts:
        x, y = p % 11, p // 11
        a.append([x * x + y * y, x, y, 1])
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


def legal(pts):
    return all(det4(list(c)) != 0 for c in itertools.combinations(pts, 4))


def mask(pts):
    v = 0
    for p in pts:
        v |= 1 << p
    return v


def canon(pts):
    best = None
    for t in range(8):
        out = []
        for p in pts:
            x, y = p % 11, p // 11
            if t == 0:
                a, b = x, y
            elif t == 1:
                a, b = 10 - x, y
            elif t == 2:
                a, b = x, 10 - y
            elif t == 3:
                a, b = 10 - x, 10 - y
            elif t == 4:
                a, b = y, x
            elif t == 5:
                a, b = 10 - y, x
            elif t == 6:
                a, b = y, 10 - x
            else:
                a, b = 10 - y, 10 - x
            out.append(b * 11 + a)
        m = mask(out)
        if best is None or m < best:
            best = m
    return best


def parent_orbits(root_hex):
    st = cells(root_hex)
    orb = set()
    for s in st:
        par = [p for p in st if p != s]
        if legal(par):
            orb.add(canon(par))
    return sorted(orb)


def main():
    sweep = json.loads((OUT / "class2-lane-cost70f-sweep-audit-20261115.json").read_text())
    moves_all = json.loads((TMP / "legal-moves.json").read_text())
    sweep_by_bit = {int(k): v for k, v in sweep["win_roots"].items()}

    certs = {}
    for bit in sorted(ROOTS):
        root = ROOTS[bit]
        path = CERTS / f"bit{bit}-root-{root}.cert"
        whole = path.read_bytes()
        assert whole.endswith(b"\n")
        rows = len(whole.splitlines()) - 2
        summary = json.loads((TMP / f"bit{bit}.rows.summary.json").read_text())
        assert summary["nRows"] == rows, (bit, summary["nRows"], rows)
        assert summary["fbt_drops"] == 0
        assert all(v["ok"] for v in summary["perMove"].values())
        bigint = json.loads((TMP / f"bit{bit}.bigint.json").read_text())
        ts = json.loads((TMP / f"bit{bit}.tsverify.json").read_text().splitlines()[-1])
        consumed = [x for x in (TMP / f"bit{bit}.consumed.txt").read_text().split() if x]
        assert len(set(consumed)) == rows
        assert bigint["root_hex"] == root and bigint["strategy_rows"] == rows
        assert bigint["union_missing"] == 0 and bigint["union_extra"] == 0
        assert bigint["subroots_passed"] == len(moves_all[str(bit)]["moves"])
        assert bigint["terminal_range"] == [13, 17]
        assert ts["rows"] == rows
        certs[str(bit)] = {
            "bit": bit,
            "child_hex": CHILD,
            "root_hex": root,
            "d4_canonical_hex": f"{canon(cells(root)):032x}",
            "verdict": "WIN7",
            "rows": rows,
            "bytes": len(whole),
            "md5": hashlib.md5(whole).hexdigest(),
            "sha256": hashlib.sha256(whole).hexdigest(),
            "whole_git_blob_sha": git_blob_sha(whole),
            "storage": {
                "layout": "single file",
                "path": path.relative_to(ROOT).as_posix(),
                "parts": [],
            },
            "extraction_nodes": summary["sum"],
            "fbt_drops": 0,
            "rows_sorted_unique": True,
            "sub_roots_total": len(moves_all[str(bit)]["moves"]),
            "loser_first_moves": moves_all[str(bit)]["moves"],
            "bigint_verifier": {
                "status": bigint["verdict"],
                "subroots_passed": bigint["subroots_passed"],
                "union_missing": bigint["union_missing"],
                "union_extra": bigint["union_extra"],
                "visited_states_across_subroots": bigint["visited_states_across_subroots"],
                "winner_states": bigint["winner_states"],
                "loser_states": bigint["loser_states"],
                "loser_reply_edges": bigint["loser_reply_edges"],
                "terminal_count": bigint["terminal_count"],
                "terminal_range": bigint["terminal_range"],
            },
            "ts_verifier": {
                "status": "PASS",
                "rows": ts["rows"],
                "consumed_winner_rows": len(consumed),
                "consumed_distinct": len(set(consumed)),
                "union_missing": 0,
                "union_extra": 0,
                "root_check": {"stones": 7, "loserMobility": len(moves_all[str(bit)]["moves"])},
            },
            "v16_sweep_nodes": sweep["aggregate"]["win7_d10_nodes"][str(bit)],
            "parent_lift_orbits": [f"{o:032x}" for o in parent_orbits(root)],
        }

    union = set()
    for c in certs.values():
        union |= set(c["parent_lift_orbits"])
    assert all(CHILD in c["parent_lift_orbits"] for c in certs.values())
    totals = {
        "certificates": len(certs),
        "strategy_rows": sum(c["rows"] for c in certs.values()),
        "certificate_bytes": sum(c["bytes"] for c in certs.values()),
        "extraction_nodes": sum(c["extraction_nodes"] for c in certs.values()),
        "sub_roots": sum(c["sub_roots_total"] for c in certs.values()),
        "distinct_parent_lift_orbits": len(union),
        "child_orbit": CHILD,
        "child_orbit_covered_by_all_certificates": True,
    }
    manifest = {
        "schema": "n11-class2-lane-cost70f-win7-certificates-20261115-v1",
        "date": "2026-11-15",
        "s5_target": "00000000000000801202000000200000",
        "child_hex": CHILD,
        "edge_cost": 70,
        "sweep_source": "class2-lane-cost70f-sweep-audit-20261115.json (70 candidates, "
                        "4 WIN7-D10 / 66 REFUTED-D10 / 0 capped, 81,480,831 nodes; "
                        "v16 runner blob 0a4a86f6828dc010c89ff17596054336a6b6091f, "
                        "depth 10, cap 1e9, andclose 1, pilot 3402 x9)",
        "certificates": certs,
        "totals": totals,
        "verification": {
            "bigint": "verify_win7_certificate_bigint_independent.mjs (BigInt 3x3 "
                      "cofactor expansion of the exact lifted determinant "
                      "[x^2+y^2,x,y,1]; no solver, verdict cache, or repo verifier "
                      "import) on all 4 whole certificates: 4/4 PASS, union "
                      "missing/extra 0/0, terminal range [13,17]",
            "number_bareiss": "verify_bit7_win7_cert.ts --root-check --subroots <all "
                              "legal first moves> --consumed-out (exact 4x4 integer "
                              "Bareiss, independent of the engine): 4/4 PASS, "
                              "consumed union == certificate row set 0/0, root "
                              "mobility == sweep opponent_legal_replies",
        },
        "unknown_status": {
            "empty_11x11": "UNKNOWN",
            "two_stone_roots_49_60_and_59_60": "UNKNOWN",
            "s2_59_60": "UNKNOWN",
            "class1": "UNKNOWN",
            "class2": "UNKNOWN",
            "class4": "UNKNOWN",
        },
        "interpretation_guard": "WIN7 certificates prove a first-player win from "
                                "the individual seven-stone roots only; the six-stone "
                                "child is closed only by the receipt fold, which is a "
                                "separate bookkeeping step. REFUTED-D10 is not a LOSS "
                                "proof. This manifest changes no frontier count.",
    }
    path = OUT / "class2-lane-cost70f-win7-certificates-20261115.json"
    path.write_text(json.dumps(manifest, indent=1) + "\n", newline="\n")
    print(json.dumps(totals, indent=1))
    print("written", path)


if __name__ == "__main__":
    main()
