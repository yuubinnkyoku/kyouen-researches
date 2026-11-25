#!/usr/bin/env python3
"""Independent verification of the STERILE-row depth-10 unclosability
theorem for the n11 class-2 lane (2026-11-16).

THEOREM.  Let R be a 6-stone manifest row whose own sweep is STERILE:
every legal candidate root R+t (t in legal_candidates(R)) has verdict
REFUTED-D10 with 0 capped.  Then no WIN7-D10 receipt root X covers R -
neither from R's own row nor by cross-cover from any other child.

LEMMA (position level, no engine involved).
    X covers R  <=>  canon(X) in {canon(R+t) : t in legal_candidates(R)}.
Proof.  X covers R iff some deletion canon(X-s) equals canon(R), i.e.
iff X = sigma(R+t) for some sigma in D4 and some cell t with
canon(R+t) = canon(X).  A receipt root X is safe (concyclic-free);
sigma preserves safety; hence R+t is safe, i.e. t is a legal candidate
of R.  QED.

THEOREM PROOF.  Suppose a WIN7-D10 receipt root X covers the STERILE
row R.  By the lemma X = sigma(R+t) with t a legal candidate of R.
R is STERILE, so the published own-row sweep gives verdict(R+t) =
REFUTED-D10.  The rules of the game are invariant under the D4
isometries of the 11x11 board, so the game trees from X and from
sigma^-1(X) = R+t are isomorphic and the depth-10 verdicts agree:
verdict(X) = REFUTED-D10.  This contradicts X being a WIN7-D10
receipt root.  QED

TRUST BOUNDARY (identical to every other verdict claim of this lane):
the engine's depth-10 verdicts are sound and D4-invariant.  The
machine checks below verify the position-level lemma, the published
data, and 8 cross-sweep verdict agreements (6 REFUTED-REFUTED swept
routes + 1 WIN-WIN precedent route, 0 conflicts); they cannot verify
engine soundness itself.

Checks:
  V0  reproduce all published candidate lists bit-exact (3 STERILE
      rows, 4 swept children) and the 70g-child WIN-bit legality;
      safety of all embedded positions.
  V1  canon/covers positive controls (published ROOT_D4, the
      bit-92 marginal record incl. its fold semantics, bit-6/bit-84
      child covers).
  V2  reproduce the published cost<=70 route map exactly (17
      children, candidate counts, covers bit-exact).
  V2s swept-route witnesses: every swept cross-cover route maps to
      an own candidate of the covered row whose published verdict is
      REFUTED-D10 (60c bit 119; 62b bits 21/109; 64c bits 111/119 ->
      70j, 64c bit 119 -> 65k).
  V3  the 5 recent WIN receipt roots (75e bits 6/10/11/37, 60c bit
      92) cover no STERILE row.
  V4  precedent reconciliation: the 70f bit-84 cross-cover closed the
      cost-70g child, whose own sweep found 8 WIN7-D10 (non-STERILE);
      V4c WIN-WIN agreement: canon(70f bit-84 root) equals canon(70g
      child + own WIN bit 29).  The 75e bit-10 marginal closed an
      unswept row of two parents.  Neither precedent row is D4-equal
      to any STERILE row, so both are consistent with the theorem.
  V5  complete route exhaustion per STERILE row: canonical
      one-stone-replacement neighbor count (689/636/689, matching the
      published analysis), and the complete route map (own + cross)
      over ALL neighbors at ALL costs: every covering route is
      exhibited as (sigma, own candidate t) with t in the published
      REFUTED-D10 list, i.e. every depth-10 route to close a STERILE
      row is dead.  The published cost<=70 map and the swept routes
      are exact subsets.
  V6  determinism: the audit is generated twice in-process and must
      be byte-identical.

Python standard library only; exact integer Bareiss determinants;
no repository engine/solver/cache, no floating point, no network.
Bookkeeping and position-level verification only; 11x11 empty board
and all roots/classes remain UNKNOWN.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")

SOURCES = {
    "neighbor_analysis":
        "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/"
        "class2-lane-sterile-rows-neighbor-analysis-20261116.json "
        "(commit d5d3d532)",
    "claim_65k": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost65k-inflight-20261115.json",
    "claim_70j": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost70j-inflight-20261116.json",
    "claim_74h": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost74h-inflight-20261115.json",
    "claim_75e": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost75e-inflight-20261116.json",
    "claim_60c": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost60c-inflight-20261116.json",
    "claim_62b": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost62b-inflight-20261116.json",
    "claim_64c": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost64c-inflight-20261116.json",
    "audit_60c": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost60c-sweep-audit-20261116.json",
    "audit_62b": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost62b-sweep-audit-20261116.json",
    "audit_64c": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost64c-sweep-audit-20261116.json",
    "fold_60c": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class-frontier-cost60c-receipts-recompute-20261116.json",
    "fold_75e": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class-frontier-cost75e-receipts-recompute-20261116.json",
    "fold_70f": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class-frontier-cost70f-receipts-recompute-20261115.json",
    "fold_70g_1115": "research/experiments/n11-s2-5960-ms5-s7-reuse-"
        "20261113/output/class-frontier-cost70g-receipts-"
        "recompute-20261115.json",
    "erratum_70j": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/"
        "output/class2-lane-cost70j-inflight-20261116.json "
        "erratum_note (schema v3, commit 834c7e2e line)",
}

ROOT_BIT92 = "00000000100000003800000008008020"      # 60c child + bit 92
ROOT_BIT92_D4 = "00000000000000801292200000000000"    # published ROOT_D4
BIT92_MARGINAL_MANIFEST = [
    "00000000000000003800000008008020",
    "00000000000000801092200000000000",
    "00000000000000801292000000000000",
]
BIT92_MARGINAL_NON_MANIFEST = [
    "00000000000000001292200000000000",
    "00000000000000800292200000000000",
    "00000000000000801290200000000000",
]
# the seventh deletion-canon of the bit-92 root (delete stone 5); absent
# from the fold record's marginal lists because marg = covers - s_1407
# and the record publishes covers=7 / marginal=6, which forces this row
# to have been already covered at head 1407 by an earlier receipt.
BIT92_SEVENTH_DELETION = "00000000000000801212200000000000"

ROOT_75E = {
    6: "00000000040000809002000000000042",
    10: "00000000040000809002000000000402",
    11: "00000000040000809002000000000802",
    37: "00000000040000809002002000000002",
}
BIT10_MARGINAL_ROW = "00000000000000801202000000000201"

ROOT_70F_BIT84 = "00000000001000801202000002200000"

WIN_ROOTS_RECENT = [
    ("75e", 6, ROOT_75E[6]), ("75e", 10, ROOT_75E[10]),
    ("75e", 11, ROOT_75E[11]), ("75e", 37, ROOT_75E[37]),
    ("60c", 92, ROOT_BIT92),
]

# ---- embedded published data (sources cited in SOURCES) ----
# extracted from the published claim/audit/fold JSONs listed in SOURCES;
# every list below is a byte-exact copy of the corresponding published field.

STERILE_ROWS = {
    '65k': dict(
        hex='00000000020000801202000000200000', edge_cost=65,
        open_rows=55, unswept_open_rows=53,
        canonical_neighbors=689,
        candidates=[0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 14, 15, 17, 18, 22, 24, 28, 29, 31, 32, 33, 35, 39, 40, 41, 42, 43, 44, 50, 51, 52, 54, 55, 56, 58, 61, 64, 65, 66, 72, 73, 74, 75, 76, 77, 79, 83, 84, 86, 87, 88, 92, 95, 97, 99, 100, 102, 105, 106, 108, 110, 113, 114, 116, 118],
        win_bits=[], refuted_bits=[0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 14, 15, 17, 18, 22, 24, 28, 29, 31, 32, 33, 35, 39, 40, 41, 42, 43, 44, 50, 51, 52, 54, 55, 56, 58, 61, 64, 65, 66, 72, 73, 74, 75, 76, 77, 79, 83, 84, 86, 87, 88, 92, 95, 97, 99, 100, 102, 105, 106, 108, 110, 113, 114, 116, 118], capped_bits=[],
    ),
    '70j': dict(
        hex='00000000000000801282000000200000', edge_cost=70,
        open_rows=113, unswept_open_rows=108,
        canonical_neighbors=636,
        candidates=[0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 17, 18, 22, 23, 26, 28, 29, 30, 32, 33, 34, 39, 40, 41, 42, 43, 50, 51, 52, 54, 67, 72, 73, 74, 75, 76, 77, 78, 83, 84, 85, 86, 87, 88, 89, 92, 94, 95, 96, 97, 99, 100, 101, 102, 103, 105, 106, 108, 110, 111, 112, 113, 114, 116, 117, 118],
        win_bits=[], refuted_bits=[0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 17, 18, 22, 23, 26, 28, 29, 30, 32, 33, 34, 39, 40, 41, 42, 43, 50, 51, 52, 54, 67, 72, 73, 74, 75, 76, 77, 78, 83, 84, 85, 86, 87, 88, 89, 92, 94, 95, 96, 97, 99, 100, 101, 102, 103, 105, 106, 108, 110, 111, 112, 113, 114, 116, 117, 118], capped_bits=[],
    ),
    '74h': dict(
        hex='00000000000000889002000000000800', edge_cost=74,
        open_rows=73, unswept_open_rows=71,
        canonical_neighbors=689,
        candidates=[0, 2, 3, 4, 6, 7, 8, 9, 10, 14, 15, 18, 19, 20, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 36, 41, 42, 43, 44, 46, 47, 48, 54, 58, 59, 62, 64, 65, 66, 68, 69, 70, 76, 77, 78, 80, 85, 86, 87, 89, 90, 91, 92, 94, 95, 96, 97, 98, 100, 102, 103, 105, 106, 107, 108, 112, 113, 114, 116, 117, 118, 119, 120],
        win_bits=[], refuted_bits=[0, 2, 3, 4, 6, 7, 8, 9, 10, 14, 15, 18, 19, 20, 22, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 36, 41, 42, 43, 44, 46, 47, 48, 54, 58, 59, 62, 64, 65, 66, 68, 69, 70, 76, 77, 78, 80, 85, 86, 87, 89, 90, 91, 92, 94, 95, 96, 97, 98, 100, 102, 103, 105, 106, 107, 108, 112, 113, 114, 116, 117, 118, 119, 120], capped_bits=[],
    ),
}

SWEPT_CHILDREN = {
    '75e': dict(
        hex='00000000040000809002000000000002', candidates=[3, 4, 6, 7, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 28, 29, 30, 31, 32, 33, 34, 37, 41, 42, 43, 44, 45, 46, 47, 48, 53, 54, 56, 57, 59, 61, 62, 64, 65, 67, 68, 69, 70, 75, 76, 77, 78, 80, 85, 87, 88, 92, 94, 95, 96, 98, 101, 102, 103, 105, 106, 107, 108, 109, 110, 112, 114, 116, 117, 119, 120],
        win_bits=[6, 10, 11, 37],
        refuted_bits=None, capped_bits=[],
    ),
    '60c': dict(
        hex='00000000000000003800000008008020', candidates=[0, 2, 3, 7, 10, 11, 14, 19, 32, 33, 34, 42, 43, 44, 46, 52, 54, 66, 68, 69, 72, 73, 74, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 90, 91, 92, 94, 95, 96, 98, 99, 100, 101, 102, 105, 106, 107, 108, 109, 110, 112, 113, 114, 116, 117, 118, 119, 120],
        win_bits=[92],
        refuted_bits=[0, 2, 3, 7, 10, 11, 14, 19, 32, 33, 34, 42, 43, 44, 46, 52, 54, 66, 68, 69, 72, 73, 74, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 90, 91, 94, 95, 96, 98, 99, 100, 101, 102, 105, 106, 107, 108, 109, 110, 112, 113, 114, 116, 117, 118, 119, 120], capped_bits=[],
    ),
    '62b': dict(
        hex='00000000000000801282020000000000', candidates=[0, 1, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 21, 22, 26, 28, 29, 31, 32, 33, 42, 43, 45, 50, 52, 54, 67, 72, 73, 77, 78, 84, 86, 87, 88, 89, 92, 94, 97, 98, 99, 100, 101, 102, 103, 105, 106, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120],
        win_bits=[],
        refuted_bits=[0, 1, 3, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 21, 22, 26, 28, 29, 31, 32, 33, 42, 43, 45, 50, 52, 54, 67, 72, 73, 77, 78, 84, 86, 87, 88, 89, 92, 94, 97, 98, 99, 100, 101, 102, 103, 105, 106, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120], capped_bits=[],
    ),
    '64c': dict(
        hex='00000000000000003800000008002020', candidates=[0, 1, 2, 3, 7, 8, 9, 10, 11, 12, 17, 21, 32, 33, 34, 42, 43, 44, 53, 54, 66, 67, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 92, 94, 95, 96, 98, 99, 100, 101, 102, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120],
        win_bits=[],
        refuted_bits=[0, 1, 2, 3, 7, 8, 9, 10, 11, 12, 17, 21, 32, 33, 34, 42, 43, 44, 53, 54, 66, 67, 69, 70, 72, 73, 74, 75, 76, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 92, 94, 95, 96, 98, 99, 100, 101, 102, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 116, 117, 118, 119, 120], capped_bits=[],
    ),
}

CHILD_70G = dict(hex='00000000000100809002000000000800', win_bits=[9, 20, 29, 34, 62, 70, 76, 119], refuted_count=62, capped=0)

ROUTE_MAP_COST_LE_70 = {
    '00000000000000003800000008000022': dict(cost=65, legal=65, covers={'70j': [119]}),
    '00000000000000003800000008001020': dict(cost=65, legal=65, covers={'70j': [111, 119]}),
    '00000000000000003800000008002002': dict(cost=64, legal=64, covers={'65k': [119]}),
    '00000000000000003800000008002020': dict(cost=64, legal=64, covers={'65k': [119], '70j': [111, 119]}),
    '00000000000000003800000008003000': dict(cost=64, legal=64, covers={'65k': [119]}),
    '00000000000000003800000008400020': dict(cost=64, legal=64, covers={'70j': [111, 119]}),
    '00000000000000003800000008800020': dict(cost=65, legal=65, covers={'70j': [111, 119]}),
    '0000000000000000380000000a002000': dict(cost=64, legal=64, covers={'65k': [119]}),
    '00000000000000083800000008000020': dict(cost=66, legal=66, covers={'70j': [111, 119]}),
    '00000000000000403800000008002000': dict(cost=64, legal=64, covers={'65k': [119]}),
    '0000000000000080120a000000800000': dict(cost=64, legal=64, covers={'65k': [109]}),
    '00000000000000801222000000800000': dict(cost=69, legal=69, covers={'65k': [109], '74h': [109]}),
    '00000000000000801222000002000000': dict(cost=69, legal=69, covers={'74h': [109]}),
    '00000000000000801226000000000000': dict(cost=66, legal=66, covers={'74h': [109]}),
    '00000000000000805222000000000000': dict(cost=66, legal=66, covers={'74h': [109]}),
    '00000000000000889002000000008000': dict(cost=68, legal=68, covers={'74h': [11]}),
    '00000000000000889002000080000000': dict(cost=67, legal=67, covers={'74h': [11]}),
}

# ---- independent implementations ----

def stones(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(121) if (v >> i) & 1]


def row_of(cell):
    x = cell % 11
    y = cell // 11
    return [x * x + y * y, x, y, 1]


def bareiss4(m):
    m = [r[:] for r in m]
    prev = 1
    for k in range(3):
        if m[k][k] == 0:
            for r in range(k + 1, 4):
                if m[r][k] != 0:
                    m[k], m[r] = m[r], m[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
            m[i][k] = 0
        prev = m[k][k]
    return m[3][3]


def det4(cells):
    return bareiss4([row_of(c) for c in cells])


def is_safe(hexstr):
    st = stones(hexstr)
    assert len(st) == 7 or len(st) == 6
    n = len(st)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    if det4([st[i], st[j], st[k], st[l]]) == 0:
                        return False
    return True


def legal_candidates(hexstr):
    st = stones(hexstr)
    out = []
    for p in range(121):
        if p in st:
            continue
        bad = False
        n = len(st)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if det4([st[i], st[j], st[k], p]) == 0:
                        bad = True
                        break
                if bad:
                    break
            if bad:
                break
        if not bad:
            out.append(p)
    return st, out


D4 = []
for _swap in (0, 1):
    for _fx in (0, 1):
        for _fy in (0, 1):
            def _mk(c, _swap=_swap, _fx=_fx, _fy=_fy):
                x, y = c % 11, c // 11
                a, b = (y, x) if _swap else (x, y)
                if _fx:
                    a = 10 - a
                if _fy:
                    b = 10 - b
                return a + 11 * b
            D4.append(_mk)


def apply_d4(v, idx):
    w = 0
    for c in stones(format(v, "032x")):
        w |= 1 << D4[idx](c)
    return w


def canon_int(v):
    best = None
    for idx in range(8):
        w = apply_d4(v, idx)
        if best is None or w < best:
            best = w
    return best


def canon_hex(hexstr):
    return format(canon_int(int(hexstr, 16)), "032x")


def covers_set(X):
    """All 7 deletion-canons of the 7-stone position X (int)."""
    return {canon_int(X - (1 << s)) for s in stones(format(X, "032x"))}


def covers(X, R):
    return R in covers_set(X)


def cover_witness(X, R):
    """Return (sigma_idx, t, s): sigma(X - s) == R, sigma(X) == R + t."""
    for s in stones(format(X, "032x")):
        rest = X - (1 << s)
        for idx in range(8):
            if apply_d4(rest, idx) == R:
                return (idx, D4[idx](s), s)
    return None


def canonical_neighbors(R):
    """Canonical one-stone-replacement neighbors of the canonical row R."""
    st = stones(format(R, "032x"))
    nb = set()
    for s in st:
        for p in range(121):
            if p in st or p == s:
                continue
            v = 0
            for x in st:
                if x != s:
                    v |= 1 << x
            v |= 1 << p
            nb.add(canon_int(v))
    return nb


def route_map_complete(R, legal_R):
    """Complete (child, bit) routes whose root covers R, with witnesses.

    Direct enumeration: a root X covers R iff X = sigma(R+t) for an own
    candidate t; each 6-subset N of X (delete stone u) yields the route
    (canon(N), bit) in the canonical child's frame.  This is exhaustive
    by the lemma; the caller cross-checks it against the per-neighbor
    enumeration of the published analysis.
    """
    routes = {}
    for t in legal_R:
        for idx in range(8):
            X = apply_d4(R, idx) | (1 << D4[idx](t))
            for u in stones(format(X, "032x")):
                Np = X - (1 << u)
                nh = canon_int(Np)
                for tau in range(8):
                    if apply_d4(Np, tau) == nh:
                        b = D4[tau](u)
                        break
                key = (nh, b)
                if key not in routes:
                    routes[key] = (idx, t)
    return routes


# ---- audit construction ----

def build_audit():
    A = {
        "schema": "n11-class2-lane-sterile-unclosability-audit-20261116-v1",
        "date": "2026-11-16",
        "method": "Python standard library only; exact integer Bareiss "
                  "determinants; independent legality/canonicalization/"
                  "covers implementations; no repository engine, no "
                  "network, no floating point",
        "theorem": {
            "statement": "a STERILE 6-stone row (all legal candidates "
                         "REFUTED-D10, 0 capped) cannot be covered by any "
                         "WIN7-D10 receipt root, own-row or cross-cover",
            "lemma": "X covers R <=> canon(X) in {canon(R+t): t in "
                     "legal_candidates(R)} (position level, no engine)",
            "premises": [
                "engine depth-10 verdicts are sound (same trust boundary "
                "as every published verdict of this lane)",
                "game rules and hence verdicts are D4-invariant on the "
                "11x11 board",
                "receipt roots are safe positions (sweeps run on safe "
                "children at legal candidate bits)",
            ],
        },
        "sources": SOURCES,
        "checks": {},
    }
    C = A["checks"]

    # ---------- V0 ----------
    v0 = {}
    ok = True
    for name, d in STERILE_ROWS.items():
        st, legal = legal_candidates(d["hex"])
        match = legal == d["candidates"]
        ok = ok and match and is_safe(d["hex"])
        v0[name] = {
            "hex": d["hex"], "published_candidates": len(d["candidates"]),
            "reproduced": len(legal), "bit_exact": match,
            "safe": is_safe(d["hex"]),
            "sterile_record": (d["win_bits"] == [] and d["capped_bits"] == []
                               and sorted(d["refuted_bits"]) == sorted(d["candidates"])),
        }
    for name, d in SWEPT_CHILDREN.items():
        st, legal = legal_candidates(d["hex"])
        match = legal == d["candidates"]
        ok = ok and match and is_safe(d["hex"])
        v0[name] = {
            "hex": d["hex"], "published_candidates": len(d["candidates"]),
            "reproduced": len(legal), "bit_exact": match,
            "safe": is_safe(d["hex"]),
            "verdict_record": {
                "win_bits": d["win_bits"], "capped": d["capped_bits"],
                "win_bits_legal": all(b in legal for b in d["win_bits"]),
            },
        }
    g = CHILD_70G
    _, glegal = legal_candidates(g["hex"])
    v0["70g_child"] = {
        "hex": g["hex"], "reproduced_candidates": len(glegal),
        "published_candidates": 70, "safe": is_safe(g["hex"]),
        "win_bits": g["win_bits"],
        "win_bits_legal": all(b in glegal for b in g["win_bits"]),
    }
    ok = ok and len(glegal) == 70 and v0["70g_child"]["win_bits_legal"]
    for _n, _b, h in WIN_ROOTS_RECENT:
        ok = ok and is_safe(h)
    v0["embedded_positions_safe"] = True
    C["V0_candidate_reproduction"] = {"detail": v0, "pass": bool(ok)}

    # ---------- V1 ----------
    v1 = {}
    X92 = int(ROOT_BIT92, 16)
    mycanon = canon_hex(ROOT_BIT92)
    v1["root_bit92_canon_matches_published_ROOT_D4"] = (
        mycanon == ROOT_BIT92_D4)
    dels = covers_set(X92)
    published6 = {int(h, 16) for h in
        BIT92_MARGINAL_MANIFEST + BIT92_MARGINAL_NON_MANIFEST}
    seventh = format(
        canon_int(int(BIT92_SEVENTH_DELETION, 16)), "032x")
    v1["bit92_deletion_canons"] = {
        "count": len(dels),
        "equals_published_six_plus_seventh":
            dels == published6 | {int(BIT92_SEVENTH_DELETION, 16)},
        "seventh_absent_from_marginal_record": (
            int(BIT92_SEVENTH_DELETION, 16) not in published6),
        "seventh": BIT92_SEVENTH_DELETION,
        "seventh_is_canonical": seventh == BIT92_SEVENTH_DELETION,
        "fold_semantics_consistency": "the fold publishes covers=7 / "
            "marginal=6 with marg = covers - s_1407, so exactly one of "
            "the seven deletion-canons was already covered at head 1407; "
            "it is necessarily this seventh canon (the other six are "
            "listed); not independently re-derived here (chain run "
            "omitted) - recorded as published-record consistency",
    }
    X6 = int(ROOT_75E[6], 16)
    v1["bit6_covers_75e_child"] = covers(
        X6, int(SWEPT_CHILDREN["75e"]["hex"], 16))
    X84 = int(ROOT_70F_BIT84, 16)
    v1["bit84_covers_70g_child"] = covers(
        X84, int(CHILD_70G["hex"], 16))
    X10 = int(ROOT_75E[10], 16)
    v1["bit10_covers_published_marginal_row"] = covers(
        X10, int(BIT10_MARGINAL_ROW, 16))
    C["V1_canon_covers_controls"] = {
        "detail": v1,
        "pass": bool(v1["root_bit92_canon_matches_published_ROOT_D4"]
                     and v1["bit92_deletion_canons"]
                     ["equals_published_six_plus_seventh"]
                     and v1["bit6_covers_75e_child"]
                     and v1["bit84_covers_70g_child"]
                     and v1["bit10_covers_published_marginal_row"]),
    }

    # ---------- V2 ----------
    v2 = {"children": {}, "published_route_instances": 0}
    ok2 = True
    targets = {n: int(d["hex"], 16) for n, d in STERILE_ROWS.items()}
    for child, dd in ROUTE_MAP_COST_LE_70.items():
        st, legal = legal_candidates(child)
        mine = {}
        for b in legal:
            X = int(child, 16) | (1 << b)
            for rn, Rv in targets.items():
                if covers(X, Rv):
                    mine.setdefault(rn, []).append(b)
        same = (mine == dd["covers"]) and (len(legal) == dd["legal"])
        ok2 = ok2 and same
        v2["children"][child] = {
            "cost": dd["cost"], "published_legal": dd["legal"],
            "reproduced_legal": len(legal),
            "published_covers": dd["covers"], "reproduced_covers": mine,
            "match": same,
        }
        v2["published_route_instances"] += sum(
            len(bits) for bits in dd["covers"].values())
    v2["children_count"] = len(ROUTE_MAP_COST_LE_70)
    C["V2_route_map_reproduction"] = {"detail": v2, "pass": bool(ok2)}

    # ---------- V2s swept routes ----------
    swept_expected = {
        "60c": {"70j": [119]},
        "62b": {"70j": [21, 109]},
        "64c": {"70j": [111, 119], "65k": [119]},
    }
    v2s = []
    oks = True
    for cname, exp in swept_expected.items():
        d = SWEPT_CHILDREN[cname]
        child = d["hex"]
        st, legal = legal_candidates(child)
        mine = {}
        for b in legal:
            X = int(child, 16) | (1 << b)
            for rn, Rv in targets.items():
                if covers(X, Rv):
                    mine.setdefault(rn, []).append(b)
        oks = oks and (mine == exp)
        for rn, bits in exp.items():
            Rv = targets[rn]
            for b in bits:
                X = int(child, 16) | (1 << b)
                w = cover_witness(X, Rv)
                own_legal = w[1] in STERILE_ROWS[rn]["candidates"]
                own_refuted = w[1] in STERILE_ROWS[rn]["refuted_bits"]
                bit_verdict_refuted = (
                    d["refuted_bits"] is not None and b in d["refuted_bits"])
                v2s.append({
                    "child": cname, "child_hex": child, "bit": b,
                    "covered_row": rn,
                    "published_sweep_verdict_of_bit":
                        "REFUTED-D10" if bit_verdict_refuted else "?",
                    "witness": {"sigma_idx": w[0], "own_candidate_t": w[1],
                                "deleted_stone_s": w[2]},
                    "own_candidate_legal": own_legal,
                    "own_candidate_published_verdict":
                        "REFUTED-D10" if own_refuted else "?",
                    "verdict_agreement": (
                        bit_verdict_refuted and own_legal and own_refuted),
                })
                oks = oks and bit_verdict_refuted and own_legal and own_refuted
    C["V2s_swept_route_witnesses"] = {
        "detail": v2s, "routes": len(v2s),
        "all_refuted_refuted_agree": bool(oks), "pass": bool(oks),
    }

    # ---------- V3 ----------
    v3 = []
    ok3 = True
    for cname, b, h in WIN_ROOTS_RECENT:
        X = int(h, 16)
        hit = [rn for rn, Rv in targets.items() if covers(X, Rv)]
        legal = SWEPT_CHILDREN[cname]["candidates"]
        ok3 = ok3 and not hit and (b in legal) and is_safe(h)
        v3.append({
            "receipt": cname, "bit": b, "root": h,
            "covers_sterile_rows": hit,
            "bit_is_legal_candidate_of_child": b in legal,
            "safe": is_safe(h),
        })
    C["V3_recent_win_roots_noncover"] = {"detail": v3, "pass": bool(ok3)}

    # ---------- V4 ----------
    v4 = {}
    ghex = CHILD_70G["hex"]
    gR = int(ghex, 16)
    v4["70g_child_not_d4_equal_to_any_sterile_row"] = not any(
        canon_int(gR) == canon_int(Rv) for Rv in targets.values())
    v4["70g_child_own_sweep_non_sterile"] = len(CHILD_70G["win_bits"]) == 8
    w84 = cover_witness(X84, gR)
    v4["bit84_witness_to_70g_child"] = {
        "sigma_idx": w84[0], "own_candidate_t": w84[1],
        "deleted_stone_s": w84[2],
    }
    v4c_hits = [t for t in CHILD_70G["win_bits"]
                if canon_int(gR | (1 << t)) == canon_int(X84)]
    v4["V4c_win_win_agreement"] = {
        "own_win_bits_d4_equal_to_bit84_root": v4c_hits,
        "exactly_one": len(v4c_hits) == 1,
        "note": "the 70f bit-84 WIN7-D10 receipt root and the 70g child's "
                "own WIN bit 29 root are the same position up to D4; two "
                "independent sweeps agree WIN7-D10 (positive control of "
                "the theorem's D4 verdict-transfer premise)",
    }
    row10 = int(BIT10_MARGINAL_ROW, 16)
    v4["bit10_marginal_row_not_d4_equal_to_any_sterile_row"] = not any(
        canon_int(row10) == canon_int(Rv) for Rv in targets.values())
    v4["bit10_marginal_row_status_at_closure"] = (
        "open unswept row of two parents at the 75e fold "
        "(published fold record; not itself swept before closure - "
        "consistent with the theorem, which only forbids closing "
        "rows that ARE sterile)")
    ok4 = (v4["70g_child_not_d4_equal_to_any_sterile_row"]
           and v4["70g_child_own_sweep_non_sterile"]
           and v4["V4c_win_win_agreement"]["exactly_one"]
           and v4["bit10_marginal_row_not_d4_equal_to_any_sterile_row"]
           and w84 is not None)
    C["V4_precedent_reconciliation"] = {"detail": v4, "pass": bool(ok4)}

    # ---------- V5 ----------
    v5 = {}
    ok5 = True
    for name, d in STERILE_ROWS.items():
        R = int(d["hex"], 16)
        st, legal = legal_candidates(d["hex"])
        nb = canonical_neighbors(R)
        nb_match = len(nb) == d["canonical_neighbors"]
        routes = route_map_complete(R, legal)
        own = {k: v for k, v in routes.items() if k[0] == R}
        cross = {k: v for k, v in routes.items() if k[0] != R}
        # every route child is the own row or a canonical neighbor
        all_in_nb = all(k[0] in nb or k[0] == R for k in routes)
        # every own candidate t is in the published REFUTED list
        verdicts_ok = all(v[1] in d["refuted_bits"] for v in routes.values())
        # witnesses: route root canon in S_R
        S_R = {canon_int(R | (1 << t)) for t in legal}
        canon_ok = True
        for (nh, b), (idx, t) in routes.items():
            if canon_int(nh | (1 << b)) not in S_R:
                canon_ok = False
        # published cost<=70 map subset
        pub = set()
        for child, dd in ROUTE_MAP_COST_LE_70.items():
            for rn, bits in dd["covers"].items():
                if rn == name:
                    pub |= {(int(child, 16), bb) for bb in bits}
        mine_keys = {(k[0], k[1]) for k in cross}
        subset = pub <= mine_keys
        # swept routes subset (already covered by swept_expected)
        ok5 = ok5 and nb_match and all_in_nb and verdicts_ok and canon_ok and subset
        v5[name] = {
            "row_hex": d["hex"],
            "edge_cost": d["edge_cost"],
            "legal_candidates": len(legal),
            "canonical_neighbors": len(nb),
            "published_canonical_neighbors": d["canonical_neighbors"],
            "neighbor_count_match": nb_match,
            "own_routes": len(own),
            "cross_routes": len(cross),
            "distinct_cross_children": len({k[0] for k in cross}),
            "all_route_children_in_own_row_or_neighborhood": all_in_nb,
            "all_route_own_candidates_in_published_refuted": verdicts_ok,
            "all_route_roots_d4_equal_to_own_candidate_root": canon_ok,
            "published_cost_le_70_routes_subset": subset,
            "published_cost_le_70_route_count": len(pub),
            "complete_route_map": [
                [format(k[0], "032x"), k[1], v[1], v[0]]
                for k, v in sorted(routes.items())
            ],
        }
    C["V5_complete_route_exhaustion"] = {
        "detail": v5,
        "route_totals": {
            n: (v5[n]["own_routes"], v5[n]["cross_routes"]) for n in v5},
        "pass": bool(ok5),
    }

    # ---------- summary ----------
    C["verdict_agreement_summary"] = {
        "refuted_refuted_swept_routes": len(v2s),
        "win_win_precedent_routes": 1,
        "conflicts": 0,
        "out_of_sample_prediction_confirmed": (
            "the theorem (registered before the parallel cost-64c sweep "
            "landed) predicted REFUTED-D10 for the covering bits 111/119; "
            "the completed sweep (commit 909b7690) returned 64/64 "
            "REFUTED-D10 with v16+v15 agreeing on both bits"),
    }
    A["all_checks_pass"] = all(
        C[k]["pass"] for k in C if isinstance(C[k], dict) and "pass" in C[k])
    A["interpretation"] = (
        "Position-level lemma and route exhaustion verified exactly. "
        "Within the depth-10 WIN7-receipt system, the three STERILE rows "
        "65k/70j/74h of the best coverable class-2 S5 "
        "00000000000000801202000000200000 are unclosable: every route "
        "(own-row or cross-cover, any neighbor, any cost) maps to an own "
        "candidate whose published verdict is REFUTED-D10. STERILE is NOT "
        "a LOSS proof and unclosable-at-D10 is NOT a game-theoretic "
        "result; the rows remain open pending depth>10 evidence. 11x11 "
        "empty board, both two-stone roots {49,60}/{59,60}, S2 {59,60}, "
        "class 1, class 2 and class 4 all remain UNKNOWN.")
    return A


def main():
    a1 = build_audit()
    a2 = build_audit()
    s1 = json.dumps(a1, indent=1, sort_keys=False) + "\n"
    s2 = json.dumps(a2, indent=1, sort_keys=False) + "\n"
    assert s1 == s2, "determinism failure: two in-process runs differ"
    os.makedirs(OUT, exist_ok=True)
    out_path = os.path.join(OUT, "audit.json")
    with open(out_path, "w") as f:
        f.write(s1)
    digest = hashlib.sha256(s1.encode()).hexdigest()
    checks = a1["checks"]
    print("V0 candidate reproduction:", checks["V0_candidate_reproduction"]["pass"])
    print("V1 canon/covers controls:", checks["V1_canon_covers_controls"]["pass"])
    print("V2 route map reproduction:", checks["V2_route_map_reproduction"]["pass"])
    print("V2s swept route witnesses:",
          checks["V2s_swept_route_witnesses"]["pass"], "(",
          checks["V2s_swept_route_witnesses"]["routes"], "routes )")
    print("V3 recent WIN roots non-cover:", checks["V3_recent_win_roots_noncover"]["pass"])
    print("V4 precedent reconciliation:", checks["V4_precedent_reconciliation"]["pass"])
    print("V5 complete route exhaustion:", checks["V5_complete_route_exhaustion"]["pass"])
    for n, d in checks["V5_complete_route_exhaustion"]["detail"].items():
        print("   ", n, "legal", d["legal_candidates"], "neighbors",
              d["canonical_neighbors"], "own", d["own_routes"], "cross",
              d["cross_routes"], "children", d["distinct_cross_children"])
    print("determinism: two in-process builds byte-identical")
    print("all_checks_pass:", a1["all_checks_pass"])
    print("output:", out_path)
    print("sha256:", digest)
    assert a1["all_checks_pass"]
    print("PASS")


if __name__ == "__main__":
    main()
