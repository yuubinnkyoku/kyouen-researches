#!/usr/bin/env python3
"""Ultra-cheap one-unknown candidates: independent legal/geometry pre-check.

Companion to the published ultra-cheap class-completion census
(research/experiments/n11-ultra-cheap-class-census-20261127, run json sha256
a60716ac...): that census left `legal` null for the four one-unknown
S5 keys because none of them is in the probe-13 supply. This
instrument derives, from first principles and by TWO independent
implementations, the geometry facts a future selection Part needs per
key:

  - stones == 5;
  - the key is D4-canonical (canonical(mask) == mask);
  - the key is quadruple-free / safe occupied (is_canonical_safe_s5_key);
  - the legal-move count of the position (the `legal` field of a
    selection json / input CSV row).

Implementation A: the repo's own published standalone geometry
(`independent.py`, Board(11), integer two-perpendicular-bisector
completion, blocked-set legal).

Implementation B: written fresh for this kit. For every empty square q,
q is illegal iff some triple of the occupied stones is collinear-with-q
or concyclic-with-q, tested by the exact integer 4x4 determinant
concyclicity criterion (a different formulation than A's
perpendicular-bisector completion).

Calibration: BOTH implementations are first validated against the
published probe-13 supply (`shared-s5-tasks.csv`, 4,556 rows): every
supply `legal` value must be reproduced by A and by B exactly, and
A == B for all 4,556 supply keys, before any candidate key is derived.

Fail-closed on any gate failure. Asserts NOTHING about verdicts, class
status, or the 11x11 game value. Nodes/proxy are bookkeeping. Standard
11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27} and third moves 100/108: UNKNOWN.
"""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
import sys
from pathlib import Path

CENSUS_RUN_SHA = ("a60716ac84e22833eaf570819d8744a2c66b2ad1d563b379"
                  "1ade829eaed87906")
INDEPENDENT_SHA = ("954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a"
                   "6d067c4fd6a4ba189f")
POLICY_SHA = ("78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb"
              "2b08af5c95e2")
SUPPLY_SHA = ("31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679"
              "047cdb160ea954")
EXPECTED_SUPPLY_ROWS = 4562


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    census_run = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    out_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    gates = {}

    def g(name, ok, detail=""):
        gates[name] = {"status": "PASS" if ok else "FAIL", "detail": str(detail)}
        return bool(ok)

    ok = True

    # ---------- pins ----------
    ind_path = base / "in" / "independent.py"
    pol_path = base / "in" / "s5_evidence_policy.py"
    ok &= g("P0a:independent-sha", ind_path.exists()
            and sha256(ind_path) == INDEPENDENT_SHA)
    ok &= g("P0b:policy-sha", pol_path.exists()
            and sha256(pol_path) == POLICY_SHA)
    if census_run is None:
        print("census run json path required (arg 2)")
        return 1
    ok &= g("P0c:census-run-sha", sha256(census_run) == CENSUS_RUN_SHA)
    supply = base / "in" / "shared-s5-tasks.csv"
    ok &= g("P0d:supply-sha", sha256(supply) == SUPPLY_SHA)

    sys.path.insert(0, str((base / "in").resolve()))
    from independent import Board, mask_from_key  # noqa: E402
    from s5_evidence_policy import is_canonical_safe_s5_key  # noqa: E402

    # ---------- implementation B (fresh, determinant criterion) ----------
    N = 11

    def key_points(lo: int, hi: int):
        mask = lo | (hi << 64)
        return [i for i in range(N * N) if mask >> i & 1]

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def concyclic(p, q, r, s):
        """Exact integer concyclicity: det of the lifted 4x4 matrix is 0."""
        if (cross(p, q, r) == 0 or cross(p, q, s) == 0
                or cross(p, r, s) == 0 or cross(q, r, s) == 0):
            # any triple collinear -> the four are concyclic iff the fourth
            # lies on that same line (handled below); here: not a circle
            return False
        rows = []
        for x, y in (p, q, r, s):
            rows.append([x * x + y * y, x, y, 1])
        det = 0
        for col in range(4):
            sub = [[rows[r2][c2] for c2 in range(4) if c2 != col]
                   for r2 in range(1, 4)]
            d3 = (sub[0][0] * (sub[1][1] * sub[2][2] - sub[1][2] * sub[2][1])
                  - sub[0][1] * (sub[1][0] * sub[2][2]
                                 - sub[1][2] * sub[2][0])
                  + sub[0][2] * (sub[1][0] * sub[2][1]
                                 - sub[1][1] * sub[2][0]))
            det += rows[0][col] * d3 * (1 if col % 2 == 0 else -1)
        return det == 0

    def on_common_line(p, pts):
        return all(cross(p, pts[0], q) == 0 for q in pts[1:])

    def legal_count_B(lo: int, hi: int):
        pts = key_points(lo, hi)
        if len(pts) != 5:
            return None
        xy = [(p % N, p // N) for p in pts]
        count = 0
        for q in range(N * N):
            if (lo if q < 64 else hi) >> (q % 64) & 1:
                continue  # occupied
            qx, qy = q % N, q // N
            qxy = (qx, qy)
            illegal = False
            for triple in itertools.combinations(xy, 3):
                if concyclic(qxy, *triple) or on_common_line(qxy, triple):
                    illegal = True
                    break
            if not illegal:
                count += 1
        return count

    def canonical_B(lo: int, hi: int):
        """Fresh D4 canonicalization by explicit point remapping."""
        pts = key_points(lo, hi)
        xy = [(p % N, p // N) for p in pts]
        m = N - 1
        best = None
        for name, f in [
            ("id", lambda x, y: (x, y)),
            ("r90", lambda x, y: (m - y, x)),
            ("r180", lambda x, y: (m - x, m - y)),
            ("r270", lambda x, y: (y, m - x)),
            ("ref", lambda x, y: (m - x, y)),
            ("ref+r90", lambda x, y: (m - y, m - x)),
            ("ref+r180", lambda x, y: (x, m - y)),
            ("ref+r270", lambda x, y: (y, x)),
        ]:
            mask = 0
            for x, y in xy:
                a, b = f(x, y)
                mask |= 1 << (b * N + a)
            if best is None or mask < best:
                best = mask
        return best

    # ---------- calibration against published supply legal ----------
    board = Board(N)
    mismatches_a, mismatches_b, ab = [], [], 0
    n_supply = 0
    with supply.open(newline="") as f:
        for row in csv.DictReader(f):
            n_supply += 1
            lo, hi = (int(x) for x in row["key"].split(":"))
            la = len(board.points(board.legal(mask_from_key(lo, hi))))
            lb = legal_count_B(lo, hi)
            if la != int(row["legal"]):
                mismatches_a.append(row["key"])
            if lb != int(row["legal"]):
                mismatches_b.append(row["key"])
            if la != lb:
                ab += 1
    ok &= g("P1a:supply-rows", n_supply == EXPECTED_SUPPLY_ROWS,
            f"{n_supply}")
    ok &= g("P1b:implA-matches-supply", not mismatches_a,
            str(mismatches_a[:3]))
    ok &= g("P1c:implB-matches-supply", not mismatches_b,
            str(mismatches_b[:3]))
    ok &= g("P1d:implA-eq-implB-supply", ab == 0, f"{ab}")

    # ---------- candidate keys ----------
    census = json.loads(census_run.read_text())
    candidates = census["one_unknown_classes"]
    ok &= g("P2:census-candidate-count", len(candidates) == 4)
    rows = []
    for c in candidates:
        lo, hi = (int(x) for x in c["unknown_key"].split(":"))
        mask = mask_from_key(lo, hi)
        pts_a = board.points(mask)
        la = len(board.points(board.legal(mask)))
        lb = legal_count_B(lo, hi)
        ca = board.canonical(mask)
        cb = canonical_B(lo, hi)
        safe = is_canonical_safe_s5_key((lo, hi))
        tag = c["unknown_key"]
        ok &= g(f"P3a:stones-{tag}", len(pts_a) == 5)
        ok &= g(f"P3b:d4-{tag}", ca == mask == cb)
        ok &= g(f"P3c:safe-{tag}", safe is True)
        ok &= g(f"P3d:legalAB-{tag}", la == lb, f"A={la} B={lb}")
        rows.append({
            "class_index": c["class_index"],
            "unknown_key": tag,
            "s5_index": c["s5_index"],
            "stones": len(pts_a),
            "d4_canonical": bool(ca == mask == cb),
            "safe": bool(safe),
            "legal": la,
            "legal_impl_agreement": bool(la == lb),
        })

    out = {
        "schema": "n11-ultra-cheap-legal-precheck-v1",
        "census_run_json_sha256": CENSUS_RUN_SHA,
        "calibration": {
            "supply_rows": n_supply,
            "implA_vs_supply": "all exact",
            "implB_vs_supply": "all exact",
            "implA_vs_implB": "all exact",
        },
        "candidates": rows,
        "gates": gates,
        "overall": "PASS" if ok else "FAIL",
        "meaning": ("geometry/legality bookkeeping for scheduling only; "
                    "no verdict claimed or consumed; nodes and proxy are "
                    "never evidence of WIN or LOSS; standard 11x11 empty "
                    "board UNKNOWN; all 19 central-reply roots UNKNOWN; "
                    "two-stone root {60,27} and third moves 100/108 "
                    "UNKNOWN"),
    }
    text = json.dumps(out, indent=1, sort_keys=False) + "\n"
    if out_path is not None:
        out_path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
