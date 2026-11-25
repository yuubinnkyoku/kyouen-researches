"""Task 1: verify the published board is PG(2,9) and relate it to a GF(9) model.

Steps
-----
A. Axioms of a projective plane of order 9 (91 points / 91 lines / 10 per line,
   point degree 10, every point pair on exactly one line, every line pair
   meeting in exactly one point).
B. Rebuild PG(2,9) from GF(9) = GF(3)[x]/(x^2+1) using *normals* (zero sets of
   linear forms), a different construction from the published builder
   (spans of point pairs).
C. Find an explicit permutation of the 91 points that maps the GF(9) line set
   onto the published line set.  The collineation group of PG(2,9) acts sharply
   transitively on ordered frames (quadrangles), so the isomorphism is unique
   once a frame is fixed; a propagation search either finds it or proves none
   exists.

Output: out/task1.json, out/iso_model_to_board.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pgcore as pc

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
BOARD = HERE.parent / "output" / "board_pg2q9.txt"


# ---------------------------------------------------------------------------
def line_tables(n, lines):
    """lid[a*n+b] = line id through points a,b;  lmask[li] = point mask."""
    lid = [-1] * (n * n)
    lmask = [0] * len(lines)
    lpts = []
    for li, L in enumerate(lines):
        m = 0
        for p in L:
            m |= 1 << p
        lmask[li] = m
        lpts.append(tuple(L))
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                a, b = L[i], L[j]
                lid[a * n + b] = li
                lid[b * n + a] = li
    return lid, lmask, lpts


def popcount(x: int) -> int:
    return bin(x).count("1")


def bits(x: int):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b


def pick_frame(lines, lmask, n):
    """Deterministic 4 points with no three collinear."""
    a, b = 0, 1
    lab = next(m for m in lmask if (m >> a) & 1 and (m >> b) & 1)
    c = next(p for p in range(n) if not (lab >> p) & 1)
    lac = next(m for m in lmask if (m >> a) & 1 and (m >> c) & 1)
    lbc = next(m for m in lmask if (m >> b) & 1 and (m >> c) & 1)
    forb = lab | lac | lbc
    d = next(p for p in range(n) if not (forb >> p) & 1)
    assert d not in (a, b, c)
    assert not (lab >> d) & 1 and not (lac >> d) & 1 and not (lbc >> d) & 1
    return [a, b, c, d]


def find_isomorphism(src_lines, tgt_lines, n, max_guesses=200000, verbose=False):
    """Return permutation pi (src point -> tgt point) mapping src lines onto tgt lines.

    Constraint propagation: a source line carrying >= 2 already-mapped points is
    a fixed target line, which confines the not-yet-mapped points of that source
    line to the still-unused target points of that target line.  Guesses are made
    on the currently most constrained point.
    """
    s_lid, s_lmask, s_lpts = line_tables(n, src_lines)
    t_lid, t_lmask, t_lpts = line_tables(n, tgt_lines)
    nlines = len(src_lines)
    tgt_lineset = set(t_lmask)
    full = (1 << n) - 1

    frame_src = pick_frame(src_lines, s_lmask, n)
    frame_tgt = pick_frame(tgt_lines, t_lmask, n)

    nodes = [0]
    result = None
    failed_at = [None]

    def assign(img, pre, cand, p, q):
        if p in img or q in pre:
            return False
        img[p] = q
        pre[q] = p
        cand[p] = 1 << q
        bq = ~(1 << q)
        for r in range(n):
            if r != p and r not in img:
                cand[r] &= bq
                if cand[r] == 0:
                    return False
        return True

    def propagate(img, pre, cand):
        changed = True
        while changed:
            changed = False
            for li in range(nlines):
                pts = s_lpts[li]
                mapped = [(p, img[p]) for p in pts if p in img]
                if len(mapped) < 2:
                    continue
                tq0 = mapped[0][1]
                tgt_li = t_lid[tq0 * n + mapped[1][1]]
                for _, q in mapped:
                    if q == tq0:
                        continue
                    if t_lid[tq0 * n + q] != tgt_li:
                        failed_at[0] = ("line image mismatch", li)
                        return False
                unk = [p for p in pts if p not in img]
                if not unk:
                    continue
                avail = t_lmask[tgt_li]
                for q in t_lpts[tgt_li]:
                    if q in pre:
                        avail &= ~(1 << q)
                if popcount(avail) != len(unk):
                    failed_at[0] = ("count mismatch", li)
                    return False
                for p in unk:
                    nc = cand[p] & avail
                    if nc != cand[p]:
                        cand[p] = nc
                        changed = True
                        if nc == 0:
                            failed_at[0] = ("empty candidate", p)
                            return False
                        if nc & (nc - 1) == 0:      # forced
                            if not assign(img, pre, cand, p, nc.bit_length() - 1):
                                failed_at[0] = ("forced assignment clash", p)
                                return False
                            changed = True
            if changed:
                sup = {}
                union = 0
                premask = 0
                for q in pre:
                    premask |= 1 << q
                for p in range(n):
                    if p in img:
                        continue
                    union |= cand[p]
                    for q in bits(cand[p]):
                        sup[q] = sup.get(q, 0) + 1
                if union != full ^ premask:
                    failed_at[0] = ("target point unreachable", None)
                    return False
                once = [q for q in sup if sup[q] == 1 and q not in pre]
                for q in once:
                    p = next(p for p in range(n)
                             if p not in img and (cand[p] >> q) & 1)
                    if not assign(img, pre, cand, p, q):
                        failed_at[0] = ("singleton support clash", p)
                        return False
                    changed = True
        return True

    def verify(img):
        imgset = set()
        for L in src_lines:
            m = 0
            for p in L:
                m |= 1 << img[p]
            if m not in tgt_lineset:
                return False
            imgset.add(m)
        return len(imgset) == nlines

    def search(img, pre, cand):
        nonlocal result
        nodes[0] += 1
        if nodes[0] > max_guesses:
            raise RuntimeError("guess budget exceeded")
        if not propagate(img, pre, cand):
            return False
        if len(img) == n:
            if verify(img):
                result = dict(img)
                return True
            failed_at[0] = ("final line check failed", None)
            return False
        best, bestc = None, None
        for p in range(n):
            if p in img:
                continue
            c = popcount(cand[p])
            if bestc is None or c < bestc:
                best, bestc = p, c
                if c == 1:
                    break
        if best is None:
            return False
        if verbose:
            print(f"  guess on point {best} ({bestc} candidates), depth {len(img)}")
        for q in bits(cand[best]):
            if q in pre:
                continue
            ni, np_, nc = dict(img), dict(pre), list(cand)
            if not assign(ni, np_, nc, best, q):
                continue
            if search(ni, np_, nc):
                return True
        return False

    img, pre, cand = {}, {}, [full] * n
    for ps, pt in zip(frame_src, frame_tgt):
        if not assign(img, pre, cand, ps, pt):
            raise AssertionError("frame seed clash")
    ok = search(img, pre, cand)
    if verbose:
        print("  nodes:", nodes[0], "failed_at:", failed_at[0])
    return (result if ok else None), nodes[0], frame_src, frame_tgt


# ---------------------------------------------------------------------------
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}

    n, lines = pc.load_board(BOARD)
    res["board_file"] = str(BOARD)
    res["board_axioms"] = pc.check_plane(n, lines)
    print("board axioms:", json.dumps(res["board_axioms"]))

    pts, mlines = pc.pg(9)
    res["model"] = {"q": 9, "points": len(pts), "lines": len(mlines),
                    "field": "GF(3)[x]/(x^2+1)",
                    "construction": "zero sets of nonzero normals"}
    res["model_axioms"] = pc.check_plane(len(pts), mlines)
    print("model axioms:", json.dumps(res["model_axioms"]))

    pi, nodes, fs, ft = find_isomorphism(mlines, lines, len(pts), verbose=True)
    res["iso_search_nodes"] = nodes
    res["iso_found"] = pi is not None
    if pi is None:
        print("NO ISOMORPHISM FOUND")
        (OUT / "task1.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
        return
    res["frame_model"] = [list(pts[p]) for p in fs]
    res["frame_board"] = ft
    bl = {pc.board_mask(L) for L in lines}
    mapped = set()
    for L in mlines:
        m = 0
        for p in L:
            m |= 1 << pi[p]
        assert m in bl, L
        mapped.add(m)
    res["iso_lines_mapped"] = len(mlines)
    res["iso_image_set_equals_board"] = (mapped == bl)
    assert mapped == bl
    print(f"isomorphism found after {nodes} search nodes; {len(mlines)} lines mapped 1-1")
    with (OUT / "iso_model_to_board.json").open("w", encoding="utf-8") as fh:
        json.dump({"perm_model_to_board": pi,
                   "model_points": [list(p) for p in pts]}, fh, indent=1)
    (OUT / "task1.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print("PASS: board == PG(2,9) up to relabeling")


if __name__ == "__main__":
    main()
