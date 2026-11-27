"""Independent verification of the board geometry and PGL(3,4) transitivity.

Board: research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q4.txt
Everything is written under independent/.  Python standard library only.
"""
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOARD = HERE.parent.parent / "projective-blocking-kyouen-20261125" / "output" / "board_pg2q4.txt"

# ---------------------------------------------------------------- F_4
# elements 0,1,2,3 with 2 = w, 3 = w^2 = w+1, w^2+w+1 = 0
ADD = lambda a, b: a ^ b
MUL = (
    (0, 0, 0, 0),
    (0, 1, 2, 3),
    (0, 2, 3, 1),
    (0, 3, 1, 2),
)
INV = {1: 1, 2: 3, 3: 2}
ZERO = (0, 0, 0)


def vadd(u, v):
    return (ADD(u[0], v[0]), ADD(u[1], v[1]), ADD(u[2], v[2]))


def vscale(a, v):
    return (MUL[a][v[0]], MUL[a][v[1]], MUL[a][v[2]])


def canon(v):
    """Canonical representative of a nonzero vector class: first nonzero entry 1."""
    for c in v:
        if c:
            return vscale(INV[c], v)
    raise ValueError("zero vector")


def matvec(M, v):
    return tuple(
        ADD(ADD(MUL[M[i][0]][v[0]], MUL[M[i][1]][v[1]]), MUL[M[i][2]][v[2]])
        for i in range(3)
    )


# ---------------------------------------------------------------- coordinate model
def build_coord_plane():
    vectors = [v for v in itertools.product(range(4), repeat=3) if v != ZERO]
    reps = sorted({canon(v) for v in vectors})
    assert len(reps) == 21, len(reps)
    idx = {r: i for i, r in enumerate(reps)}
    # coordinate point index -> canonical vector
    vec = reps
    # lines: nonzero covector (a,b,c) up to scalar -> line of points with a.x+b.y+c.z=0
    line_sets = set()
    for a in itertools.product(range(4), repeat=3):
        if a == ZERO:
            continue
        ca = canon(a)
        pts = frozenset(
            i for i in range(21) if ADD(ADD(MUL[ca[0]][vec[i][0]], MUL[ca[1]][vec[i][1]]), MUL[ca[2]][vec[i][2]]) == 0
        )
        line_sets.add(pts)
    lines = sorted(line_sets)
    assert len(lines) == 21, len(lines)
    return vec, idx, lines


# ---------------------------------------------------------------- board
def read_board(path):
    rows = path.read_text().splitlines()
    n, nb = map(int, rows[0].split())
    blocks = []
    for row in rows[1:]:
        vals = list(map(int, row.split()))
        assert vals[0] == 5
        blocks.append(frozenset(vals[1:]))
    assert len(blocks) == nb
    return n, blocks


def check_pg(n, blocks):
    problems = []
    if n != 21:
        problems.append(f"n={n}")
    if len(blocks) != 21:
        problems.append(f"#lines={len(blocks)}")
    if any(len(b) != 5 for b in blocks):
        problems.append("not all lines have 5 points")
    if len(set(blocks)) != len(blocks):
        problems.append("duplicate lines")
    seen = {}
    for i, b in enumerate(blocks):
        for a, c in itertools.combinations(sorted(b), 2):
            seen[(a, c)] = seen.get((a, c), 0) + 1
    if len(seen) != n * (n - 1) // 2:
        problems.append("pair coverage incomplete")
    bad = [k for k, v in seen.items() if v != 1]
    if bad:
        problems.append(f"{len(bad)} pairs covered != 1 time")
    if any(sum(1 for b in blocks if p in b) != 5 for p in range(n)):
        problems.append("some point is not on exactly 5 lines")
    return problems


def board_to_coord_index(p):
    """Explicit isomorphism from the handed board labels to the coordinate model.

    Board structure (discovered from the incidence data):
      points 0..4 are the points at infinity (directions), points 5..20 are AG(2,4)
      with  p = 5 + 4*y + x  <-> (x,y).
      directions:  0 -> slope 0, 2 -> slope 1, 3 -> slope 3, 4 -> slope 2, 1 -> vertical.
    """
    if p <= 4:
        return {
            0: (1, 0, 0),  # slope 0
            1: (0, 1, 0),  # vertical
            2: (1, 1, 0),  # slope 1
            3: (1, 3, 0),  # slope 3
            4: (1, 2, 0),  # slope 2
        }[p]
    q = p - 5
    y, x = divmod(q, 4)
    return (x, y, 1)


def build_generators():
    """A generating set for GL(3,4) (hence, modulo scalars, PGL(3,4))."""
    E = lambda i, j: [[1 if a == b else 0 for b in range(3)] for a in range(3)]
    gens = []
    for i, j in [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]:
        M = E(0, 0)  # identity
        M = [row[:] for row in M]
        M[i][j] = 1
        gens.append(M)
    D = [[2, 0, 0], [0, 1, 0], [0, 0, 1]]
    gens.append(D)
    return gens


def perm_of_matrix(M, vec, idx):
    return tuple(idx[canon(matvec(M, vec[i]))] for i in range(21))


def compose(p, q):
    """p after q."""
    return tuple(p[q[i]] for i in range(21))


def main():
    out = {}
    n, blocks = read_board(BOARD)
    board_pts = set(range(n))
    problems = check_pg(n, blocks)
    out["board_pg_problems"] = problems

    vec, idx, coord_lines = build_coord_plane()
    out["coord_plane"] = {"points": 21, "lines": len(coord_lines)}
    out["coord_pg_ok"] = (
        len(coord_lines) == 21
        and all(len(l) == 5 for l in coord_lines)
        and len({frozenset(l) for l in coord_lines}) == 21
    )
    # verify coordinate model pair coverage too
    cl = [set(l) for l in coord_lines]
    pairs = {}
    for l in cl:
        for a, b in itertools.combinations(sorted(l), 2):
            pairs[(a, b)] = pairs.get((a, b), 0) + 1
    out["coord_pairs_once"] = len(pairs) == 210 and all(v == 1 for v in pairs.values())

    # ---- explicit board -> coordinate isomorphism
    phi = {p: idx[canon(board_to_coord_index(p))] for p in range(n)}
    assert len(set(phi.values())) == 21
    coord_line_sets = {frozenset(l) for l in coord_lines}
    images = [frozenset(phi[p] for p in b) for b in blocks]
    iso_ok = len(set(images)) == 21 and all(im in coord_line_sets for im in images)
    out["explicit_isomorphism_ok"] = iso_ok
    out["isomorphism_images_are_all_coord_lines"] = set(images) == coord_line_sets

    board_of_coord = {v: k for k, v in phi.items()}

    # ---- generators as permutations of board labels; check they preserve lines
    gens_coord = build_generators()
    board_line_set = {frozenset(b) for b in blocks}
    gens_board = []
    gen_line_preserving = True
    for M in gens_coord:
        pc = perm_of_matrix(M, vec, idx)
        pb = tuple(board_of_coord[pc[phi[p]]] for p in range(n))
        gens_board.append(pb)
        if any(frozenset(pb[p] for p in b) not in board_line_set for b in blocks):
            gen_line_preserving = False
    out["generators_line_preserving"] = gen_line_preserving

    # ---- closure (order of the generated permutation group on 21 points)
    ident = tuple(range(21))
    seen = {ident}
    stack = [ident]
    while stack:
        e = stack.pop()
        for g in gens_board:
            ng = compose(e, g)
            if ng not in seen:
                seen.add(ng)
                stack.append(ng)
    out["generated_group_order"] = len(seen)

    # ---- |GL(3,4)| by brute force over all 3x3 matrices, |PGL|=|GL|/(q-1)
    def det3(M):
        a, b, c = M[0]
        d, e, f = M[1]
        g, h, i = M[2]
        # a(ei - fh) - b(di - fg) + c(dh - eg)
        t1 = MUL[a][ADD(MUL[e][i], MUL[f][h])]
        t2 = MUL[b][ADD(MUL[d][i], MUL[f][g])]
        t3 = MUL[c][ADD(MUL[d][h], MUL[e][g])]
        return ADD(ADD(t1, t2), t3)

    n_gl = 0
    for flat in itertools.product(range(4), repeat=9):
        M = [flat[0:3], flat[3:6], flat[6:9]]
        if det3(M) != 0:
            n_gl += 1
    out["gl34_order"] = n_gl
    out["pgl34_order_formula"] = n_gl // 3

    # ---- ordered frames: 4 points, no 3 collinear
    line_of = {}
    for bi, b in enumerate(blocks):
        for a, c in itertools.combinations(sorted(b), 2):
            line_of[(a, c)] = bi
            line_of[(c, a)] = bi

    def collinear(t):
        a, b, c = t
        return c in blocks[line_of[(a, b)]]

    n_frames = 0
    for q in itertools.permutations(range(21), 4):
        if collinear(q[:3]) or collinear((q[0], q[1], q[3])) or collinear((q[0], q[2], q[3])) or collinear((q[1], q[2], q[3])):
            continue
        n_frames += 1
    out["ordered_frames_bruteforce"] = n_frames
    out["ordered_frames_formula"] = 21 * 20 * 16 * 9

    # ---- orbits on triangles / frames
    def orbit_of_tuple(t, ordered=True):
        if ordered:
            return {tuple(e[x] for x in t) for e in seen}
        return {frozenset(e[x] for x in t) for e in seen}

    all_triples = list(itertools.combinations(range(21), 3))
    col_triples = [t for t in all_triples if collinear(t)]
    ncol_triples = [t for t in all_triples if not collinear(t)]
    out["triples_total"] = len(all_triples)
    out["triples_collinear"] = len(col_triples)
    out["triples_nonline"] = len(ncol_triples)
    out["triples_collinear_formula"] = 21 * 10
    out["triples_nonline_formula"] = 1330 - 210

    orb_nc = orbit_of_tuple((0, 1, 5), ordered=False)
    orb_col = orbit_of_tuple((0, 1, 2), ordered=False)
    orb_nc_ord = orbit_of_tuple((0, 1, 5), ordered=True)
    orb_col_ord = orbit_of_tuple((0, 1, 2), ordered=True)
    frame = (0, 1, 5, 10)  # 0,1,5 non-collinear; 10 not on any of the 3 joins
    assert not any(collinear(t) for t in itertools.combinations(frame, 3)), "representative frame not a frame"
    orb_frame = orbit_of_tuple(frame, ordered=True)
    out["orbit_nonline_triangle"] = len(orb_nc)
    out["orbit_collinear_triangle"] = len(orb_col)
    out["orbit_ordered_nonline_triangle"] = len(orb_nc_ord)
    out["orbit_ordered_collinear_triangle"] = len(orb_col_ord)
    out["orbit_ordered_frame"] = len(orb_frame)
    out["transitive_on_nonline_triangles"] = len(orb_nc) == len(ncol_triples)
    out["transitive_on_collinear_triples"] = len(orb_col) == len(col_triples)
    out["transitive_on_ordered_frames"] = len(orb_frame) == n_frames
    out["frame_stabilizer_trivial"] = len(orb_frame) == len(seen)

    # group order sanity from the frame argument
    out["group_order_equals_frames"] = len(seen) == n_frames

    # ---- every group element preserves the line system?  generators do, so yes;
    #      demonstrate a random check over all elements for line preservation is
    #      unnecessary, but verify the generators generate a subgroup of collineations
    out["all_generated_are_collineations"] = gen_line_preserving

    print(json.dumps(out, indent=1))
    (HERE / "group_out.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
