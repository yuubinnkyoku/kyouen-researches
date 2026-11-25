#!/usr/bin/env python3
"""Third independent audit of the five cost-70e WIN7 certificates (2026-11-15).

The cost-70e sweep (second coverable class-2 target S5
00000000000000801202000000200000, child 00000000000000801202000000200004,
edge cost 70) produced 5 WIN7-D10 roots (bits 0, 8, 24, 66, 79).  The
certificate bodies were published as 2-part files.  This audit:

  1. joins each published certificate's two parts at the line boundary,
     normalises CRLF to LF (the canonical git-blob content), and records the
     whole-file md5/sha256/git-blob-sha and the part blobs;
  2. re-runs the independent BigInt 3x3 cofactor verifier
     (verify_win7_certificate_bigint_independent.mjs) on every whole
     certificate;
  3. re-runs the independent Number Bareiss 4x4 verifier
     (verify_bit7_win7_cert.ts --root-check --subroots <all legal moves>
     --consumed-out) and checks that the consumed winner-state union equals
     the certificate row set exactly (0 missing / 0 extra);
  4. re-derives each root's D4 canonical form and its six-stone parent-lift
     orbits with an exact-integer dihedral canonicalisation, and asserts the
     cost-70e child orbit is covered by every certificate;
  5. writes class2-lane-cost70e-certificates-third-independent-audit-20261115.json.

No solver, verdict cache, repo engine or repo verifier module is imported by
the BigInt verifier; the TS verifier is a separate exact-integer Bareiss
implementation.  This audit changes no frontier count and no game verdict.
"""
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
CERTS = OUT / "class2-lane-cost70e-certificates"
TMP = OUT / "tmp-cost70e"
SCRIPTS = HERE / "scripts"
CHILD = "00000000000000801202000000200004"
ROOTS = {
    0: "00000000000000801202000000200005",
    8: "00000000000000801202000000200104",
    24: "00000000000000801202000001200004",
    66: "00000000000000841202000000200004",
    79: "00000000000080801202000000200004",
}

sys.path.insert(0, str(SCRIPTS))
from legal_candidates import legal_candidates  # noqa: E402


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


def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(HERE))
    return res


def main():
    TMP.mkdir(exist_ok=True)
    records = {}
    total_rows = total_bytes = total_subroots = 0
    for bit in sorted(ROOTS):
        root = ROOTS[bit]
        parts = sorted(CERTS.glob(f"bit{bit}-root-{root}.cert.part*of2"))
        assert len(parts) == 2, (bit, parts)
        part_data = []
        part_records = []
        for p in parts:
            d = p.read_bytes().replace(b"\r\n", b"\n")
            part_data.append(d)
            part_records.append({
                "path": p.relative_to(HERE.parent.parent.parent).as_posix(),
                "bytes": len(d),
                "git_blob_sha": git_blob_sha(d),
            })
        whole = b"".join(part_data)
        assert whole.endswith(b"\n")
        lines = whole.splitlines()
        assert lines[0] == b"n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"
        assert lines[1] == b"root " + root.encode()
        rows = len(lines) - 2
        _, moves = legal_candidates(root)
        assert len(moves) == len(set(moves))
        whole_path = TMP / f"{root}.cert"
        whole_path.write_bytes(whole)

        bigint = run(["node",
                      str(SCRIPTS / "verify_win7_certificate_bigint_independent.mjs"),
                      str(whole_path), str(len(moves))])
        assert bigint.returncode == 0, bigint.stderr
        bj = json.loads(bigint.stdout)
        assert bj["root_hex"] == root and bj["strategy_rows"] == rows
        assert bj["subroots_passed"] == len(moves)
        assert bj["union_missing"] == 0 and bj["union_extra"] == 0
        assert bj["terminal_range"] == [13, 17]

        consumed_path = TMP / f"bit{bit}.consumed.txt"
        if consumed_path.exists():
            consumed_path.unlink()
        ts = run(["node", "--experimental-strip-types",
                  str(SCRIPTS / "verify_bit7_win7_cert.ts"),
                  "--cert", str(whole_path), "--root", root,
                  "--root-check", "--subroots", ",".join(map(str, moves)),
                  "--consumed-out", str(consumed_path)])
        assert ts.returncode == 0, ts.stderr
        ts_lines = [ln for ln in ts.stdout.splitlines() if ln.strip()]
        ts_root = json.loads(ts_lines[0])
        ts_stats = json.loads(ts_lines[1])
        assert ts_root == {"stones": 7, "loserMobility": len(moves)}
        assert ts_stats["rows"] == rows
        consumed = [x for x in consumed_path.read_text().split() if x]
        consumed_set = set(consumed)
        assert len(consumed_set) == rows, (bit, len(consumed_set), rows)
        assert len(set(consumed_set)) == rows
        cert_rows = {ln.split()[0].decode() for ln in lines[2:] if ln.strip()}
        assert consumed_set == cert_rows, (bit, len(cert_rows - consumed_set),
                                           len(consumed_set - cert_rows))

        records[str(bit)] = {
            "bit": bit,
            "root_hex": root,
            "d4_canonical_hex": f"{canon(cells(root)):032x}",
            "rows": rows,
            "bytes": len(whole),
            "md5": hashlib.md5(whole).hexdigest(),
            "sha256": hashlib.sha256(whole).hexdigest(),
            "whole_git_blob_sha": git_blob_sha(whole),
            "storage": {"layout": "2 parts", "parts": part_records},
            "root_check": {"stones": 7, "loser_mobility": len(moves)},
            "sub_roots": len(moves),
            "bigint_verifier": {
                "status": bj["verdict"],
                "subroots_passed": bj["subroots_passed"],
                "union_missing": bj["union_missing"],
                "union_extra": bj["union_extra"],
                "visited_states_across_subroots": bj["visited_states_across_subroots"],
                "winner_states": bj["winner_states"],
                "loser_states": bj["loser_states"],
                "loser_reply_edges": bj["loser_reply_edges"],
                "terminal_count": bj["terminal_count"],
                "terminal_range": bj["terminal_range"],
            },
            "number_bareiss_verifier": {
                "status": "PASS",
                "rows": ts_stats["rows"],
                "consumed_winner_rows": len(consumed),
                "consumed_distinct": len(consumed_set),
                "union_missing": 0,
                "union_extra": 0,
            },
            "parent_lift_orbits": [f"{o:032x}" for o in parent_orbits(root)],
        }
        assert CHILD in records[str(bit)]["parent_lift_orbits"], bit
        total_rows += rows
        total_bytes += len(whole)
        total_subroots += len(moves)

    union = set()
    for r in records.values():
        union |= set(r["parent_lift_orbits"])
    audit = {
        "schema": "n11-class2-lane-cost70e-certificates-third-independent-audit-20261115-v1",
        "date": "2026-11-15",
        "status": "PASS",
        "scope": "the five cost-70e WIN7 certificates (bits 0, 8, 24, 66, 79) "
                 "published as 2-part files for child "
                 "00000000000000801202000000200004 (edge cost 70, second "
                 "coverable class-2 target S5 00000000000000801202000000200000)",
        "method": "join the published parts at the line boundary, normalise "
                  "CRLF to LF (canonical git-blob content), then (a) re-run the "
                  "independent BigInt 3x3 cofactor verifier "
                  "(verify_win7_certificate_bigint_independent.mjs; no solver, "
                  "verdict cache, repo engine or repo verifier import) and (b) "
                  "re-run the independent Number Bareiss 4x4 verifier "
                  "(verify_bit7_win7_cert.ts --root-check --subroots all --"
                  "consumed-out), asserting the consumed winner-state union "
                  "equals the certificate row set exactly; D4 canonical forms "
                  "and six-stone parent-lift orbits are re-derived with an "
                  "exact-integer dihedral canonicalisation",
        "certificates": records,
        "totals": {
            "certificates": len(records),
            "strategy_rows": total_rows,
            "certificate_bytes": total_bytes,
            "sub_roots": total_subroots,
            "distinct_parent_lift_orbits": len(union),
            "child_orbit": CHILD,
            "child_orbit_covered_by_all_certificates": all(
                CHILD in r["parent_lift_orbits"] for r in records.values()),
        },
        "frontier_tie_in": {
            "canonical_chain_head": "1227/6620/522561/4890/386284 "
                                    "(class-frontier-cost69h-receipts-recompute-20261115.json)",
            "child_still_remaining_at_head_1227": True,
            "s6_frontier_contribution": 0,
            "rebase_requirement": "the eventual cost-70e receipt fold must "
                                  "rebase on the canonical head at fold time "
                                  "and assert it before extending",
        },
        "unknown_status": {
            "empty_11x11": "UNKNOWN",
            "two_stone_roots_49_60_and_59_60": "UNKNOWN",
            "s2_59_60": "UNKNOWN",
            "class1": "UNKNOWN",
            "class2": "UNKNOWN",
            "class4": "UNKNOWN",
        },
        "interpretation_guard": "WIN7 certificates prove a first-player win "
                                "within depth 10 from the individual seven-stone "
                                "roots only; they do not close the six-stone "
                                "child until the receipt fold. This audit is "
                                "independent verification bookkeeping over "
                                "published material and changes no frontier "
                                "count and no game-theoretic verdict.",
    }
    path = OUT / "class2-lane-cost70e-certificates-third-independent-audit-20261115.json"
    path.write_text(json.dumps(audit, indent=2) + "\n", newline="\n")
    print(json.dumps(audit["totals"], indent=1))
    print("written", path)


if __name__ == "__main__":
    main()
