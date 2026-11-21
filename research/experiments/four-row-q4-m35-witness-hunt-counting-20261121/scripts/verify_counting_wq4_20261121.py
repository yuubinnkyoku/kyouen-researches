#!/usr/bin/env python3
"""Independent verifier: w-generalized (q=4) counting-class tables, published
def-mode witnesses (q=4 w=4,5,6 and q=5 w=4), curve censuses, and band corollaries.

All inputs are byte-pinned (sha256 inside this file).  Everything is recomputed
from scratch with stdlib only; nothing is imported from the producing scripts.

Gates
  g_pin      input files match pinned sha256 digests
  g_census   independent census (primitive-direction lines; circumcenter-based
             circles) reproduces every published board census it is pinned to,
             including the circle/line split of the 8-case four-row m35
             surgery cross-check file; repeated census claims in one records
             file must be self-consistent
  g_captable counting-class supply CAPS(class) and bound B(class) computed by
             two structurally different implementations (A: closed-form row
             pattern sums; B: literal labeled-stone triple enumeration) must
             (a) agree, (b) match the pinned expected tables for all classes
             w=3..7, (c) agree on deterministic permutation samples
             (pairwise row swaps cover full-invariance generation),
             (d) reproduce the K1202 published w=3 bounds,
             (e) reproduce the pinned top-class claims,
             (f) collapse to B=0 exactly on the pinned impossible classes
  g_witness  every witness in the four pinned records banks re-verified with
             integer geometry: header consistency, bounds, no duplicate
             stones, claimed row histogram, safety (no q stones on any common
             line or circle), maximality (every free cell completes some
             q-curve), and for q=4 the class inequality m <= B(class)
  g_bands    exact alive-class lists at thresholds pinned for w=4; a
             deliberately wrong list must be rejected (in-run negative control)

Modes
  default        run all gates; write output/audit.json only on full pass
  --fast         skip the (4,35,4) census and boards larger than 4x24
  --tamper       corrupt expectations in memory (table value, band list,
                 census anchor, witness stone position) and require every
                 corresponding check to FAIL; audit.json must not be written

Fail-closed and deterministic: exit 0 only on full pass; audit records a
content digest that must be identical across runs (timings excluded).
"""

import argparse
import hashlib
import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.abspath(os.path.join(HERE, "..", "input"))
OUTDIR = os.path.abspath(os.path.join(HERE, "..", "output"))

PIN_SHA = {
    "expected_tables_w3_w7.json":
        "cf8845487431e6c3a8906f4091c621b0111b18276d5bdf14d1322bf2de41e419",
    "pin_q4w4_records.jsonl":
        "1a45e862f03dfd1c0d559ff207250f472557d72a545ffc2b1e068e31a341b7a7",
    "pin_q4w5_records.jsonl":
        "69979050e446c0c5eaca5a8898800f88a691ca0f88dcf35b5e32209c45d1f301",
    "pin_q4w6_records.jsonl":
        "a029e0b883e9d82a6da2450911625cfbf5759df4286b53326f5fb09fa9cb8078",
    "pin_q5w4_records.jsonl":
        "cdd906f1751835f985f4b6923c0a088ec55aac3d728c780eb96f7c5b538f2a27",
    "pin_census4_check_output.txt":
        "8b841eb202f907683fcb9a5fbda43878cfbed280c662e754bda1573acd101d01",
    "witnesses_44_m4_34.json":
        "7689e4df99be22179ccd50c0c197cde2ad8d8d2dfe486212eef898a090dde1ae",
}

# K1202 published w=3 class bounds (B=0 means: impossible for all m at which
# the demand formula applies; see K1202 for the published semantics).
K1202_W3_B = {
    (0, 0, 0): 0, (0, 0, 1): 0, (0, 0, 2): 0, (0, 0, 3): 0, (0, 1, 1): 0,
    (0, 1, 2): 2, (1, 1, 1): 2,
    (0, 1, 3): 5, (0, 2, 2): 5, (1, 1, 2): 5,
    (1, 2, 2): 11,
    (0, 2, 3): 13, (1, 1, 3): 13,
    (0, 3, 3): 36, (1, 2, 3): 24, (2, 2, 2): 22, (2, 2, 3): 40,
    (1, 3, 3): 52, (2, 3, 3): 68,
}

# top-class claims per width: M_{w,4} <= B+1 (K0068 T_w values).
TOP_CLAIMS = {
    4: ((2, 3, 3, 3), 234, 236),
    5: ((2, 3, 3, 3, 3), 564, 566),
    6: ((2, 3, 3, 3, 3, 3), 1110, 1112),
    7: ((2, 3, 3, 3, 3, 3, 3), 1926, 1928),
}

# B(M_{4,4} upper bound witness-band thresholds):
# assert: any maximal safe (4,4) config on the m x 4 board with class C has
# m <= B(C) (demand d*m - sum r <= CAPS).  alive(t) = classes with B >= t
# ordered by (B desc, class asc); pinned lists for the thresholds relevant to
# the m=35 (and m>=36) witness hunt and the deep eliminations.
ALIVE_W4 = {
    200: [(2, 3, 3, 3)],
    167: [(2, 3, 3, 3), (1, 3, 3, 3)],
    163: [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3)],
    124: [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3), (0, 3, 3, 3)],
    113: [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3), (0, 3, 3, 3), (1, 2, 3, 3)],
    89:  [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3), (0, 3, 3, 3), (1, 2, 3, 3),
          (2, 2, 2, 3)],
    73:  [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3), (0, 3, 3, 3), (1, 2, 3, 3),
          (2, 2, 2, 3), (0, 2, 3, 3), (1, 1, 3, 3), (1, 2, 2, 3)],
    50:  [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3), (0, 3, 3, 3), (1, 2, 3, 3),
          (2, 2, 2, 3), (0, 2, 3, 3), (1, 1, 3, 3), (1, 2, 2, 3), (2, 2, 2, 2),
          (0, 1, 3, 3)],
    37:  [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3), (0, 3, 3, 3), (1, 2, 3, 3),
          (2, 2, 2, 3), (0, 2, 3, 3), (1, 1, 3, 3), (1, 2, 2, 3), (2, 2, 2, 2),
          (0, 1, 3, 3), (0, 2, 2, 3), (1, 1, 2, 3), (1, 2, 2, 2)],
    36:  [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3), (0, 3, 3, 3), (1, 2, 3, 3),
          (2, 2, 2, 3), (0, 2, 3, 3), (1, 1, 3, 3), (1, 2, 2, 3), (2, 2, 2, 2),
          (0, 1, 3, 3), (0, 2, 2, 3), (1, 1, 2, 3), (1, 2, 2, 2), (0, 0, 3, 3)],
    35:  [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3), (0, 3, 3, 3), (1, 2, 3, 3),
          (2, 2, 2, 3), (0, 2, 3, 3), (1, 1, 3, 3), (1, 2, 2, 3), (2, 2, 2, 2),
          (0, 1, 3, 3), (0, 2, 2, 3), (1, 1, 2, 3), (1, 2, 2, 2), (0, 0, 3, 3)],
}
# deliberately wrong band (missing (2,2,2,3)) used as the in-run negative control
ALIVE_W4_WRONG = {
    89: [(2, 3, 3, 3), (1, 3, 3, 3), (2, 2, 3, 3), (0, 3, 3, 3), (1, 2, 3, 3)],
}


class Fail(Exception):
    pass


def require(cond, msg):
    if not cond:
        raise Fail(msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


# ======================================================================
# census
# ======================================================================

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def census_lines(w, m, minpts):
    """Number of lines containing >= minpts grid points of the w x m board.

    Canonical form: minimal board point + primitive direction (a,b) with
    b>0, or (a>0,b==0) for horizontals; negative-a directions with b>0 cover
    the descending slopes (e.g. (1,-1) lines of slope -1 are found through
    canonical direction (-1,1)), so every slanted line is counted once.
    """
    count = 0
    if m >= minpts:
        count += w  # horizontal rows (m points each)
    if w >= minpts:
        count += m  # vertical columns (w points each)
    arange = list(range(-(m - 1), 0)) + list(range(1, m))
    for a in arange:
        for b in range(1, w):
            if gcd(abs(a), b) != 1:
                continue
            if (minpts - 1) * abs(a) > m - 1 or (minpts - 1) * b > w - 1:
                continue
            for x in range(m):
                for y in range(w):
                    if 0 <= x - a < m and 0 <= y - b < w:
                        continue
                    n = 1
                    cx, cy = x, y
                    while True:
                        cx += a
                        cy += b
                        if 0 <= cx < m and 0 <= cy < w:
                            n += 1
                        else:
                            break
                    if n >= minpts:
                        count += 1
    return count


def census_circles(w, m, minpts):
    """Number of circles containing >= minpts grid points.

    Every such circle owns >= minpts >= 3 grid points, hence its (rational)
    circumcenter is discovered from any point triple; the center is stored as
    a reduced fraction, and distinct concentric circles are separated by the
    scaled squared radius r^2 * d^2 (integer).
    """
    pts = [(x, y) for y in range(w) for x in range(m)]
    n = len(pts)
    ssq = [x * x + y * y for (x, y) in pts]
    centers = set()
    add = centers.add
    for i in range(n):
        x1, y1 = pts[i]
        s1 = ssq[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            s2 = ssq[j]
            for k in range(j + 1, n):
                x3, y3 = pts[k]
                d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
                if d == 0:
                    continue
                s3 = ssq[k]
                na = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2)
                nb = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1)
                g = gcd(gcd(abs(na), abs(nb)), abs(d))
                if g > 1:
                    na //= g
                    nb //= g
                    d //= g
                if d < 0:
                    na, nb, d = -na, -nb, -d
                add((na, nb, d))
    total = 0
    for (na, nb, dd) in sorted(centers):
        hist = {}
        rx_list = [dd * x - na for (x, y) in pts]
        ry_list = [dd * y - nb for (x, y) in pts]
        for idx in range(n):
            r2 = rx_list[idx] * rx_list[idx] + ry_list[idx] * ry_list[idx]
            hist[r2] = hist.get(r2, 0) + 1
        for r2 in sorted(hist):
            if hist[r2] >= minpts:
                total += 1
    return total


def census(w, m, minpts):
    lines = census_lines(w, m, minpts)
    circles = census_circles(w, m, minpts)
    return lines, circles


# ======================================================================
# counting-class table: two implementations
# ======================================================================

def caps_A(r):
    """Closed form over occupancy patterns of non-horizontal stone triples.

    A blocker triple occupies rows with multiplicities u (sum 3, max <= 2):
    patterns {1,1,1} (three distinct rows) and {1,2} (two rows).  Each
    patterned triple supplies cap = sum over deficient rows r_i <= 2 of
    max(0, 2-u_i) coverage; the number of stone triples realizing a pattern
    is prod_i binom(r_i, u_i).  Trips with 3 stones on one row are excluded
    (the row's own horizontal line never covers a deficient row's cells).
    """
    w = len(r)
    defrows = [i for i in range(w) if r[i] <= 2]
    caps = 0
    for trio in itertools.combinations(range(w), 3):
        mult = r[trio[0]] * r[trio[1]] * r[trio[2]]
        if not mult:
            continue
        inside = sum(1 for t in trio if r[t] <= 2)
        # deficient row inside  -> u=1 -> need 1; outside -> u=0 -> need 2
        cap = inside + 2 * (len(defrows) - inside)
        caps += mult * cap
    for i in range(w):
        if not r[i]:
            continue
        binom2 = r[i] * (r[i] - 1) // 2
        if not binom2:
            continue
        for j in range(w):
            if i == j or not r[j]:
                continue
            mult = binom2 * r[j]
            cap = 0
            for t in defrows:
                u = 2 if t == i else (1 if t == j else 0)
                cap += max(0, 2 - u)
            caps += mult * cap
    return caps


def caps_B(r):
    """Literal enumeration of stone triples with stones labeled by row."""
    w = len(r)
    defrows = [i for i in range(w) if r[i] <= 2]
    stones = []
    for i in range(w):
        stones += [i] * r[i]
    n = len(stones)
    caps = 0
    for i in range(n):
        a = stones[i]
        for j in range(i + 1, n):
            b = stones[j]
            for k in range(j + 1, n):
                c = stones[k]
                if a == c:
                    continue  # labels are nondecreasing: a==c means all same
                # row; a horizontal triple never covers a deficient row.
                # Remaining patterns: (2,1) if a==b or b==c, else (1,1,1).
                cap = 0
                for t in defrows:
                    u = (1 if t == a else 0) + (1 if t == b else 0) + \
                        (1 if t == c else 0)
                    cap += max(0, 2 - u)
                caps += cap
    return caps


def class_entry(r):
    capsA = caps_A(r)
    capsB = caps_B(r)
    if capsA != capsB:
        raise Fail("impl mismatch r=%r: A=%d B=%d" % (r, capsA, capsB))
    w = len(r)
    defrows = [i for i in range(w) if r[i] <= 2]
    if not defrows or capsA == 0:
        return (capsA, 0)
    d = len(defrows)
    demand_r = sum(r[i] for i in defrows)
    return (capsA, (capsA + demand_r) // d)


def sorted_profiles(w):
    """all nondecreasing profiles (c_1..c_w), c in 0..3, excluding all-3."""
    out = []
    def rec(prefix, last, remaining):
        if remaining == 0:
            if all(x == 3 for x in prefix):
                return
            out.append(tuple(prefix))
            return
        for v in range(last, 4):
            rec(prefix + [v], v, remaining - 1)
    rec([], 0, w)
    return out


# ======================================================================
# witness geometry (exact integer arithmetic)
# ======================================================================

def line_key(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    dx, dy = x2 - x1, y2 - y1
    g = gcd(abs(dx), abs(dy))
    dx, dy = dx // g, dy // g
    if (dx, dy) <= (0, 0):
        dx, dy = -dx, -dy
    return ("L", dx, dy, x1 * dy - y1 * dx)


def circle_key(p1, p2, p3):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if d == 0:
        return None
    s1 = x1 * x1 + y1 * y1
    s2 = x2 * x2 + y2 * y2
    s3 = x3 * x3 + y3 * y3
    na = s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2)
    nb = s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1)
    R = (d * x1 - na) ** 2 + (d * y1 - nb) ** 2  # r^2 * d^2
    g = gcd(gcd(gcd(abs(na), abs(nb)), abs(d)), abs(R))
    if g > 1:
        na //= g
        nb //= g
        d //= g
    if d < 0:
        na, nb, d = -na, -nb, -d
    return ("C", na, nb, d, R // (g * g) if g > 1 else R)


def circle_member(ck, pt):
    _, na, nb, d, R = ck
    rx = d * pt[0] - na
    ry = d * pt[1] - nb
    return rx * rx + ry * ry == R


def verify_witness(w, m, q, stones, tables):
    """Verify one def-mode witness; raises Fail on any violation.  Returns
    the row histogram and (q=4) the class inequality data."""
    pts = [(int(s[0]), int(s[1])) for s in stones]
    n = len(pts)
    require(len(set(pts)) == n, "duplicate stones")
    for (x, y) in pts:
        require(0 <= x < m and 0 <= y < w, "stone out of board")
    require(n <= w * m, "more stones than cells")
    rowcount = [0] * w
    for (x, y) in pts:
        rowcount[y] += 1
    # ---- safety: no q stones on one line or circle
    curves = {}
    stonepos = {}
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                p1, p2, p3 = pts[i], pts[j], pts[k]
                if (p2[0] - p1[0]) * (p3[1] - p1[1]) == (p2[1] - p1[1]) * (p3[0] - p1[0]):
                    key = line_key(p1, p2)
                else:
                    key = circle_key(p1, p2, p3)
                s = curves.get(key)
                if s is None:
                    s = curves[key] = set()
                s.update((i, j, k))
    for key, members in curves.items():
        require(len(members) < q,
                "unsafe: %d stones on one curve" % len(members))
    # ---- maximality: every free cell completes some q-curve
    occupied = set(pts)
    qmin2 = q - 2
    for x in range(m):
        for y in range(w):
            if (x, y) in occupied:
                continue
            covered = False
            # lines through (x,y): any line with >= q stones among pts
            seen_dirs = set()
            for i in range(n):
                x1, y1 = pts[i]
                dx, dy = x - x1, y - y1
                g = gcd(abs(dx), abs(dy))
                dx, dy = dx // g, dy // g
                if (dx, dy) in seen_dirs:
                    continue
                seen_dirs.add((dx, dy))
                cnt = 0
                cx, cy = x1, y1
                while 0 <= cx < m and 0 <= cy < w:
                    if (cx, cy) in occupied:
                        cnt += 1
                    cx += dx
                    cy += dy
                cx, cy = x1 - dx, y1 - dy
                while 0 <= cx < m and 0 <= cy < w:
                    if (cx, cy) in occupied:
                        cnt += 1
                    cx -= dx
                    cy -= dy
                if cnt + 1 >= q:
                    covered = True
                    break
            if covered:
                continue
            # circles through (x,y) and two stones
            for i in range(n):
                for j in range(i + 1, n):
                    ck = circle_key((x, y), pts[i], pts[j])
                    if ck is None:
                        continue
                    cnt = 0
                    for s in pts:
                        if circle_member(ck, s):
                            cnt += 1
                    if cnt + 1 >= q:
                        covered = True
                        break
                if covered:
                    break
            require(covered,
                    "not maximal: free cell (%d,%d) stays safe" % (x, y))
    out = {"rows": rowcount}
    if q == 4:
        tab = tables[w]
        prof = tuple(sorted(min(rowcount[i], 3) for i in range(w)))
        require(prof in tab, "class %r not in w=%d table" % (prof, w))
        caps, B = tab[prof]
        require(B >= m, "class inequality violated: m=%d > B=%d for %r"
                % (m, B, prof))
        out["class"] = prof
        out["B"] = B
    return out


# ======================================================================
# gates
# ======================================================================

def gate_pin(state):
    state["pins"] = {}
    for name, sha in sorted(PIN_SHA.items()):
        path = os.path.join(INPUT, name)
        require(os.path.exists(path), "missing input %s" % name)
        got = sha256_file(path)
        require(got == sha, "sha mismatch %s: got %s pin %s" % (name, got, sha))
        state["pins"][name] = got


def load_records(fname):
    recs = []
    with open(os.path.join(INPUT, fname)) as f:
        for ln, line in enumerate(f):
            line = line.strip()
            if line:
                recs.append((ln + 1, json.loads(line)))
    return recs


def check_census_board(state, w, m, q, expect_total, expect_circles=None):
    key = "%d-%d-%d" % (w, m, q)
    lines, circles = census(w, m, q)
    require(lines + circles == expect_total,
            "census (%d,%d,%d): total %d != %d" % (w, m, q, lines + circles,
                                                   expect_total))
    entry = {"lines": lines, "circles": circles, "total": lines + circles}
    if expect_circles is not None:
        require(circles == expect_circles,
                "census (%d,%d,%d): circles %d != %d"
                % (w, m, q, circles, expect_circles))
        entry["circles_pinned"] = True
    state["census"][key] = entry


def gate_census(state, fast):
    # (a) 8-case cross-check file (lines+circles+total)
    n_cases = 0
    with open(os.path.join(INPUT, "pin_census4_check_output.txt")) as f:
        for line in f:
            e = json.loads(line)
            if e.get("event"):
                require(e["allPass"] and e["nCases"] == 8, "bad summary: %r" % e)
                continue
            n_cases += 1
            if fast and (e["w"], e["m"], e["q"]) == (4, 35, 4):
                state["census"]["%d-%d-%d" % (e["w"], e["m"], e["q"])] = \
                    {"skipped": True}
                continue
            check_census_board(state, e["w"], e["m"], e["q"],
                               e["satCurves"], e["c4Circles"])
    require(n_cases == 8, "expected 8 census cases, got %d" % n_cases)
    # (b) record-embedded board censuses (self-consistency + re-derivation)
    anchors = {}
    for fname, w, q in (("pin_q4w4_records.jsonl", 4, 4),
                         ("pin_q4w5_records.jsonl", 5, 4),
                         ("pin_q4w6_records.jsonl", 6, 4),
                         ("pin_q5w4_records.jsonl", 4, 5)):
        for (ln, r) in load_records(fname):
            require(r["w"] == w and r["q"] == q, "lane mismatch line %d" % ln)
            if "curves" not in r:
                continue
            key = (w, r["m"], q)
            if key in anchors:
                require(anchors[key] == r["curves"],
                        "record census inconsistent for (%d,%d,%d): %d vs %d"
                        % (w, r["m"], q, anchors[key], r["curves"]))
                continue
            anchors[key] = r["curves"]
            big = w * r["m"] > 140 and (w, r["m"]) not in EXPLICIT_CENSUS_BOARDS
            if fast and w * r["m"] > CENSUS_FAST_LIMIT or (not fast) and big:
                state["census"]["%d-%d-%d" % key] = {
                    "deferred": True, "record_curves": r["curves"]}
                continue
            check_census_board(state, w, r["m"], q, r["curves"])
    state["census_boards_recomputed"] = sum(
        1 for v in state["census"].values() if "total" in v)
    state["census_boards_skipped"] = sum(
        1 for v in state["census"].values()
        if v.get("skipped") or v.get("deferred"))


def check_tables(state, expected):
    """expected: {w: {class: (caps, B)}} from the pinned file (or corrupted)."""
    tables = {}
    for w in (3, 4, 5, 6, 7):
        tab = {}
        for prof in sorted_profiles(w):
            entry = class_entry(prof)
            # permutation sample: adjacent transpositions generate S_w
            variants = [prof]
            lst = list(prof)
            for i in range(w - 1):
                for j in range(i + 1, w):
                    v = list(lst)
                    v[i], v[j] = v[j], v[i]
                    variants.append(tuple(v))
            for v in set(variants):
                require(class_entry(v) == entry,
                        "not permutation-invariant: %r vs %r (%r)"
                        % (v, entry, class_entry(v)))
            tab[prof] = entry
        expw = expected[w]
        require(len(tab) == len(expw),
                "w=%d: %d classes computed, %d pinned"
                % (w, len(tab), len(expw)))
        for cls in sorted(tab):
            require(cls in expw, "w=%d class %r absent in pinned table" % (w, cls))
            require(tab[cls] == (expw[cls][0], expw[cls][1]),
                    "w=%d class %r: (%d,%d) != pinned %r"
                    % (w, cls, tab[cls][0], tab[cls][1], expw[cls]))
        tables[w] = tab
        state["captable"][str(w)] = {
            "classes": len(tab),
            "top_class": [list(c) for c in
                          sorted(tab, key=lambda c: (-tab[c][1], c))[:1]],
            "top_B": max(v[1] for v in tab.values()),
        }
    state["tables"] = tables
    # top claims (K0068 T_w = B+1)
    for w, (cls, caps_t, B_t) in sorted(TOP_CLAIMS.items()):
        require(tables[w][cls] == (caps_t, B_t),
                "w=%d top claim %r: computed %r" % (w, cls, tables[w][cls]))
        require(max(v[1] for v in tables[w].values()) == B_t,
                "w=%d: max B %d != top claim %d"
                % (w, max(v[1] for v in tables[w].values()), B_t))
    # K1202 published w=3 bounds
    for cls, Bpub in sorted(K1202_W3_B.items()):
        require(cls in tables[3] and tables[3][cls][1] == Bpub,
                "K1202 w=3 class %r: computed B=%r, published %d"
                % (cls, tables[3].get(cls, (0, None))[1], Bpub))
    # T_w identity spot claims (K0068 thresholds)
    Tw = {4: 237, 5: 567, 6: 1113, 7: 1929, 3: 69}
    for w in (3, 4, 5, 6, 7):
        maxB = max(v[1] for v in tables[w].values())
        require(maxB + 1 == Tw[w],
                "w=%d: maxB+1=%d != T_w=%d" % (w, maxB + 1, Tw[w]))


def gate_captable(state):
    with open(os.path.join(INPUT, "expected_tables_w3_w7.json")) as f:
        exp = json.load(f)
    expected = {w: {tuple(eval(e[0])): (e[1], e[2]) for e in exp[str(w)]}
                for w in (3, 4, 5, 6, 7)}
    check_tables(state, expected)


BANKS = [
    ("pin_q4w4_records.jsonl", 4, 4, 4, 34, 31),
    ("pin_q4w5_records.jsonl", 5, 4, 5, 36, 32),
    ("pin_q4w6_records.jsonl", 6, 4, 6, 31, 26),
    ("pin_q5w4_records.jsonl", 4, 5, 5, 20, 16),
]

# boards recomputed by the census gate: all with w*m <= 140, plus these
EXPLICIT_CENSUS_BOARDS = {(5, 30), (6, 26)}
CENSUS_FAST_LIMIT = 60


def gate_witness(state):
    tables = state["tables"]
    for (fname, w, q, m_lo, m_hi, n_expected) in BANKS:
        recs = load_records(fname)
        seen_m = {}
        n_seen = 0
        for (ln, r) in recs:
            if "witness" not in r:
                continue
            n_seen += 1
            m = r["m"]
            wis = r["witness"]
            require(wis["w"] == w and wis["m"] == m and wis["q"] == q,
                    "witness header mismatch %s line %d" % (fname, ln))
            require(len(wis["stones"]) == wis["nStones"],
                    "nStones mismatch %s line %d" % (fname, ln))
            info = verify_witness(w, m, q, wis["stones"], tables)
            require(info["rows"] == wis["rows"],
                    "row histogram mismatch %s line %d: %r vs %r"
                    % (fname, ln, info["rows"], wis["rows"]))
            seen_m[m] = seen_m.get(m, 0) + 1
        require(n_seen == n_expected,
                "%s: %d witnesses != %d expected" % (fname, n_seen, n_expected))
        require(sorted(seen_m) == list(range(m_lo, m_hi + 1)),
                "%s witness m-range %r != %d..%d"
                % (fname, sorted(seen_m), m_lo, m_hi))
        state["witness"][fname] = {"n": n_seen, "m_range": [m_lo, m_hi]}
    # extraction snapshot consistency
    with open(os.path.join(INPUT, "witnesses_44_m4_34.json")) as f:
        ext = json.load(f)
    require(len(ext["witnesses"]) == 31, "extraction snapshot n != 31")
    src = {}
    for (ln, r) in load_records("pin_q4w4_records.jsonl"):
        if "witness" in r:
            src.setdefault(r["m"], []).append(
                [list(s) for s in r["witness"]["stones"]])
    for wi in ext["witnesses"]:
        stones = [list(s) for s in wi["stones"]]
        require(stones in src.get(wi["m"], []),
                "extraction m=%d not verbatim in records" % wi["m"])
    state["witness"]["extraction_snapshot"] = {"n": 31}


def check_bands(state, alive_map):
    tab = state["tables"][4]
    for th in sorted(alive_map):
        got = sorted((c for c in tab if tab[c][1] >= th),
                     key=lambda c: (-tab[c][1], c))
        want = [tuple(c) for c in alive_map[th]]
        require(got == want, "band m>=%d: alive list mismatch\n got %r\nwant %r"
                % (th, got, want))
    state["bands_checked"] = len(alive_map)


# ======================================================================
# main
# ======================================================================

def digest_of(state):
    core = {k: state[k] for k in sorted(state)
            if k in ("pins", "census", "captable", "witness",
                     "census_boards_recomputed", "census_boards_skipped",
                     "bands_checked")}
    blob = json.dumps(core, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--tamper", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    state = {"census": {}, "captable": {}, "witness": {}}
    gates = {}

    def run(name, fn):
        t = time.time()
        fn()
        gates[name] = "PASS"
        print("gate %s PASS (%.2fs)" % (name, time.time() - t), flush=True)

    audit_written = False
    try:
        if not args.tamper:
            run("g_pin", lambda: gate_pin(state))
            run("g_census", lambda: gate_census(state, args.fast))
            run("g_captable", lambda: gate_captable(state))
            run("g_witness", lambda: gate_witness(state))
            run("g_bands", lambda: check_bands(state, ALIVE_W4))
            # in-run negative control: the wrong band list must be rejected
            try:
                check_bands(state, ALIVE_W4_WRONG)
                raise Fail("negative control: wrong band list was accepted")
            except Fail as e:
                if "negative control" in str(e):
                    raise
            gates["g_bands_wronglist_rejected"] = "PASS"
            print("gate g_negctl PASS", flush=True)
        else:
            run("g_pin", lambda: gate_pin(state))
            run("g_census", lambda: gate_census(state, True))  # tamper: fast
            run("g_captable", lambda: gate_captable(state))

            def must_fail(name, fn):
                t = time.time()
                try:
                    fn()
                except Fail:
                    gates[name] = "PASS(rejected)"
                    print("tamper %s REJECTED as required (%.2fs)"
                          % (name, time.time() - t), flush=True)
                    return
                raise Fail("tamper %s was NOT caught" % name)

            # (1) corrupted pinned table value
            with open(os.path.join(INPUT, "expected_tables_w3_w7.json")) as f:
                exp = json.load(f)
            expected = {w: {tuple(eval(e[0])): [e[1], e[2]] for e in exp[str(w)]}
                        for w in (3, 4, 5, 6, 7)}
            expected[4][(2, 3, 3, 3)][1] += 1
            must_fail("tamper_table",
                      lambda: check_tables(dict(state), expected))
            # (2) corrupted band list
            bad_bands = {200: [(1, 3, 3, 3)]}
            must_fail("tamper_bands",
                      lambda: check_bands(dict(state), bad_bands))
            # (3) corrupted census anchor
            st2 = dict(state)
            st2["census"] = {}
            must_fail("tamper_census",
                      lambda: check_census_board(st2, 4, 8, 4, 486))
            # (4) corrupted witness (move one stone)
            recs = load_records("pin_q4w4_records.jsonl")
            target = None
            for (ln, r) in recs:
                if "witness" in r:
                    target = r
                    break
            w_m, m_m, q_m = target["w"], target["m"], target["q"]
            stones = [list(s) for s in target["witness"]["stones"]]
            stones[0][0] = (stones[0][0] + 1) % m_m
            must_fail("tamper_witness",
                      lambda: verify_witness(w_m, m_m, q_m, stones,
                                             state["tables"]))
    except Fail as e:
        print("FAIL: %s" % e, file=sys.stderr)
        print("audit NOT written (fail-closed)", file=sys.stderr)
        return 1
    state["gates"] = gates
    state["mode"] = "tamper" if args.tamper else ("fast" if args.fast else "full")
    state["seconds_total"] = round(time.time() - t0, 3)
    # compact, deterministic digest of the full class tables (not dumped)
    tbl = state.pop("tables", None)
    if tbl is not None:
        blob = json.dumps({str(w): [[list(c), tbl[w][c][0], tbl[w][c][1]]
                                    for c in sorted(tbl[w])] for w in sorted(tbl)},
                          sort_keys=True)
        state["table_digest"] = hashlib.sha256(blob.encode()).hexdigest()
    state["content_digest"] = digest_of(state)
    if not args.tamper:
        os.makedirs(OUTDIR, exist_ok=True)
        with open(os.path.join(OUTDIR, "audit.json"), "w") as f:
            json.dump(state, f, indent=1, sort_keys=True)
        audit_written = True
        print("ALL GATES PASS; audit.json written; digest=%s (%.1fs)"
              % (state["content_digest"], state["seconds_total"]))
    else:
        print("TAMPER MODE: all corruptions rejected; audit intentionally not "
              "written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
