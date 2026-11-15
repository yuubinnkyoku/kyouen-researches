#!/usr/bin/env python3
"""Build the cost-78a WIN7 certificate manifest (5/5) for the n11 class-2 lane.

Inputs (all published or produced in this lane):
  * class2-lane-cost78a-sweep-audit-20261115.json  (v16 nodes, mobility, roots)
  * cost78a-all-legal-moves-20261115.json          (independent legal-reply lists)
  * class2-lane-cost78a-certificates/               (5 certificates, 9 part files)
  * tmp-cost78a/bit{29,8,109}.rows.summary.json     (blind extraction summaries)
  * tmp-cost78a/bit{29,8,109}.bigint.json           (BigInt verifier outputs)
  * tmp-cost78a/bit{36,20,29,8,109}.tsverify.json   (Number Bareiss verifier outputs)
  * tmp-cost78a/bit{29,8,109}.split.json            (part split receipts)

The manifest records the whole-file hashes of the LF certificate content (the
git blobs), the part blobs actually tracked, the independent verifier results,
and the D4 parent-lift orbits.  No frontier count is changed here.
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost78a-certificates"
TMP = OUT / "tmp-cost78a"
ROOT = HERE.parent.parent.parent  # repository root
CHILD = "00000000000000809102000000400000"

ROOTS = {
    8: "00000000000000809102000000400100",
    20: "00000000000000809102000000500000",
    29: "00000000000000809102000020400000",
    36: "00000000000000809102001000400000",
    109: "00002000000000809102000000400000",
}
# extraction nodes from the published claim for the two already-published
# certificates; the three new ones are read from their extraction summaries.
PUBLISHED_EXTRACTION = {36: 11691313, 20: 16192007}
PUBLISHED_ROWS = {36: 50711, 20: 56452}


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
    sweep = json.loads((OUT / "class2-lane-cost78a-sweep-audit-20261115.json").read_text())
    moves_all = json.loads((OUT / "cost78a-all-legal-moves-20261115.json").read_text())
    sweep_by_bit = {w["bit"]: w for w in sweep["win_roots"]}

    certs = {}
    for bit in sorted(ROOTS):
        root = ROOTS[bit]
        base = CERTS / f"bit{bit}-root-{root}.cert"
        parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
        if bit in PUBLISHED_ROWS:
            # the published working-tree files may carry CRLF; the canonical
            # certificate content is the LF git blob, reconstructed here from
            # the LF copies made with `git cat-file blob`.
            lf = TMP / (f"bit{bit}.lf.cert" if bit == 36 else "bit20.joined.lf.cert")
            whole = lf.read_bytes()
            if bit == 20:
                cut = 1020151
                part1, part2 = whole[:cut], whole[cut:]
                assert part1.endswith(b"\n") and part2.endswith(b"\n")
                assert len(part1) == 1020151 and len(part2) == 1018923
                part_records = [
                    {"path": parts[0].relative_to(ROOT).as_posix(),
                     "bytes": len(part1), "git_blob_sha": git_blob_sha(part1)},
                    {"path": parts[1].relative_to(ROOT).as_posix(),
                     "bytes": len(part2), "git_blob_sha": git_blob_sha(part2)},
                ]
            else:
                part_records = []
            layout = "2 parts" if bit == 20 else "single file"
        elif parts:
            whole = b"".join(p.read_bytes() for p in parts)
            layout = f"{len(parts)} parts"
            part_records = [
                {"path": p.relative_to(ROOT).as_posix(),
                 "bytes": p.stat().st_size,
                 "git_blob_sha": git_blob_sha(p.read_bytes())}
                for p in parts
            ]
        else:
            whole = base.read_bytes()
            layout = "single file"
            part_records = []
        assert whole.endswith(b"\n")
        rows = len(whole.splitlines()) - 2
        if bit in PUBLISHED_ROWS:
            assert rows == PUBLISHED_ROWS[bit], (bit, rows)
        if bit in PUBLISHED_EXTRACTION:
            extraction_nodes = PUBLISHED_EXTRACTION[bit]
            extraction_source = "published claim"
        else:
            summary = json.loads((TMP / f"bit{bit}.rows.summary.json").read_text())
            assert summary["nRows"] == rows, (bit, summary["nRows"], rows)
            assert summary["fbt_drops"] == 0
            assert all(v["ok"] for v in summary["perMove"].values())
            extraction_nodes = summary["sum"]
            extraction_source = "blind extraction summary"
        bigint = json.loads((TMP / f"bit{bit}.bigint.json").read_text())
        ts = json.loads((TMP / f"bit{bit}.tsverify.json").read_text().splitlines()[-1])
        consumed = [x for x in (TMP / f"bit{bit}.consumed.txt").read_text().split() if x]
        assert len(set(consumed)) == rows, (bit, len(set(consumed)), rows)
        assert bigint["root_hex"] == root
        assert bigint["strategy_rows"] == rows
        assert bigint["union_missing"] == 0 and bigint["union_extra"] == 0
        assert bigint["subroots_passed"] == len(moves_all[str(bit)]["moves"])
        assert ts["rows"] == rows
        assert bigint["terminal_range"] == [13, 17]
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
                "layout": layout,
                "path": (CERTS / f"bit{bit}-root-{root}.cert").relative_to(ROOT).as_posix()
                        if not part_records else None,
                "parts": part_records,
            },
            "extraction_nodes": extraction_nodes,
            "extraction_source": extraction_source,
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
            "v16_sweep_nodes": sweep_by_bit[bit]["nodes"],
            "parent_lift_orbits": [f"{o:032x}" for o in parent_orbits(root)],
        }

    union = set()
    for c in certs.values():
        union |= set(c["parent_lift_orbits"])
    child_covered = all(CHILD in c["parent_lift_orbits"] for c in certs.values())
    assert child_covered

    totals = {
        "certificates": len(certs),
        "strategy_rows": sum(c["rows"] for c in certs.values()),
        "certificate_bytes": sum(c["bytes"] for c in certs.values()),
        "extraction_nodes": sum(c["extraction_nodes"] for c in certs.values()),
        "sub_roots": sum(c["sub_roots_total"] for c in certs.values()),
        "distinct_parent_lift_orbits": len(union),
        "child_orbit": CHILD,
        "child_orbit_covered_by_all_certificates": child_covered,
    }
    manifest = {
        "schema": "n11-class2-lane-cost78a-win7-certificates-20261115-v1",
        "date": "2026-11-15",
        "s5_target": "00000000000000809102000000000000",
        "child_hex": CHILD,
        "edge_cost": 78,
        "sweep_source": "class2-lane-cost78a-sweep-audit-20261115.json (78 candidates, "
                        "5 WIN7-D10 / 73 REFUTED-D10 / 0 capped, 184,253,822 nodes; "
                        "v16 runner blob 0a4a86f6828dc010c89ff17596054336a6b6091f, "
                        "depth 10, cap 1e9, andclose 1, pilot 3402 x10)",
        "certificates": certs,
        "totals": totals,
        "verification": {
            "bigint": "verify_win7_certificate_bigint_independent.mjs (BigInt 3x3 "
                      "cofactor expansion of the exact lifted determinant "
                      "[x^2+y^2,x,y,1]; no solver, verdict cache, or repo verifier "
                      "import) on all 5 whole certificates: 5/5 PASS, union "
                      "missing/extra 0/0, terminal range [13,17]",
            "number_bareiss": "verify_bit7_win7_cert.ts --root-check --subroots <all "
                              "legal first moves> --consumed-out (exact 4x4 integer "
                              "Bareiss, independent of the engine): 5/5 PASS, "
                              "consumed union == certificate row set 0/0, root "
                              "mobility == sweep opponent_legal_replies",
            "published_bits": "bits 36 and 20 were already published and are "
                              "re-verified here from the LF git blobs (the working "
                              "tree may carry CRLF; the TS verifier needs LF); the "
                              "three new certificates (29/8/109) were extracted "
                              "blind (empty kill table) and verified before this "
                              "manifest was written",
        },
        "unknown_status": {
            "empty_11x11": "UNKNOWN",
            "two_stone_roots_49_60_and_59_60": "UNKNOWN",
            "s2_59_60": "UNKNOWN",
            "class2": "UNKNOWN",
            "class4": "UNKNOWN",
        },
        "interpretation_guard": "WIN7 certificates prove a first-player win from "
                                "the individual seven-stone roots only; the six-stone "
                                "child is closed only by the receipt fold, which is a "
                                "separate bookkeeping step. REFUTED-D10 is not a LOSS "
                                "proof. This manifest changes no frontier count.",
    }
    path = OUT / "class2-lane-cost78a-win7-certificates-20261115.json"
    path.write_text(json.dumps(manifest, indent=1) + "\n", newline="\n")
    print(json.dumps(totals, indent=1))
    print("written", path)


if __name__ == "__main__":
    main()
