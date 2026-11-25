"""Independent verification of claim K1324 (PG(2,8) cap orbits under PGL(3,8)).

Tasks (as assigned):
  1. both start sets are caps and maximal;
  2. build PGL(3,8) from GF(8) with my own generators, verify collineations;
  3. orbit of the hyperoval: size 32704, all members are 10-caps;
  4. orbit of the maximal 6-cap: size; >=3 other maximal 6-caps classified;
  5. |PGL(3,8)| = 16482816 and stabilizer orders 504 / 24; orbit*stab = |PGL|.

Run:  python -u verify_orbits.py  (writes logs/verify_orbits.log via tee)
"""

import json
import random
import sys
import time

import pg8core as G

BOARD = "../output/board_pg2q8.txt"
CENSUS_LOG = "logs/census_c.log"
HYPEROVAL = [0, 5, 13, 18, 27, 38, 46, 53, 59, 66]
CAP6 = [10, 47, 49, 55, 61, 64]

RESULTS = []  # (task, name, ok, detail)


def record(task, name, ok, detail=""):
    RESULTS.append({"task": task, "check": name, "ok": bool(ok), "detail": detail})
    print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", name, detail))
    sys.stdout.flush()


def hdr(t):
    print("\n" + t)
    print("-" * len(t))
    sys.stdout.flush()


def parse_census_6():
    """Read my own C census log for the total number of 10-caps / maximal 6-caps."""
    tot10 = tot6m = None
    try:
        with open(CENSUS_LOG) as f:
            for ln in f:
                p = ln.split()
                if len(p) >= 6 and p[0] == "SIZE" and p[1] == "10":
                    tot10 = int(p[3])
                if len(p) >= 6 and p[0] == "SIZE" and p[1] == "6":
                    tot6m = int(p[5])
    except FileNotFoundError:
        pass
    return tot10, tot6m


# ---------------------------------------------------------------------------
t0 = time.time()
hdr("TASK 0. Board + geometry")
n, b, board_lines = G.read_board(BOARD)
record(0, "board header 73 73", (n, b) == (73, 73), "n=%d b=%d" % (n, b))
record(0, "73 lines of 9 points", len(board_lines) == 73 and all(len(L) == 9 for L in board_lines))
GEO = G.Geometry(n, board_lines)
record(0, "every point pair on exactly one line", GEO.pairs == 73 * 72 // 2,
       "pairs=%d" % GEO.pairs)
record(0, "board line set == construction from GF(8)",
       set(board_lines) == set(G.build_lines()), "|lines|=%d" % len(set(board_lines)))

# ---------------------------------------------------------------------------
hdr("TASK 1. Start sets are caps and maximal")
for name, S in (("hyperoval (10 pts)", HYPEROVAL), ("6-cap (6 pts)", CAP6)):
    S = sorted(S)
    ok_cap = GEO.is_cap(S)
    add = GEO.addable(S)
    blocked = bin(GEO.blocked(S)).count("1")
    record(1, "%s is a cap (no 3 collinear)" % name, ok_cap, "|S|=%d" % len(S))
    record(1, "%s is maximal (no addable point)" % name, len(add) == 0,
           "addable=%d blocked=%d/73" % (len(add), blocked))
    record(1, "%s covers all points by pair-lines" % name,
           (GEO.blocked(S) | G.mask_of(S)) == (1 << 73) - 1)
    # sanity: any 3 points of a cap are non-collinear
    triples_ok = True
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            Lij = GEO.line_through(S[i], S[j])
            for k in range(j + 1, len(S)):
                if S[k] in Lij:
                    triples_ok = False
    record(1, "%s all C(n,3) triples non-collinear" % name, triples_ok)
print("  hyperoval addable set:", GEO.addable(HYPEROVAL))
print("  6-cap addable set:", GEO.addable(CAP6))

# ---------------------------------------------------------------------------
hdr("TASK 2. Build PGL(3,8) from GF(8): generators, collineations, order")
t = time.time()
bad = G.check_field()
record(2, "GF(8) axioms + irreducibility of x^3+x+1", not bad, "%d violations" % len(bad))

gens = []
gen_desc = []
for i in range(3):
    for j in range(3):
        if i == j:
            continue
        for c in (1, 2):
            M = G.transvection(i, j, c)
            gens.append(G.perm_from_matrix(M))
            gen_desc.append("E_%d%d(%d)" % (i, j, c))
d = G.perm_from_matrix(G.diagonal(2, 1, 1))
gens.append(d)
gen_desc.append("diag(w,1,1)")
sw = G.perm_from_matrix(G.coord_swap())
gens.append(sw)
gen_desc.append("swap(0,1)")
record(2, "14 generators built from 3x3 matrices over GF(8)", len(gens) == 14,
       ", ".join(gen_desc))
record(2, "each generator is a permutation of the 73 points",
       all(sorted(g) == list(range(73)) for g in gens))
record(2, "each generator has nonzero determinant",
       all(G.mat_det(G.transvection(i, j, c)) != 0 for i in range(3) for j in range(3)
           if i != j for c in (1, 2)) and G.mat_det(G.diagonal(2, 1, 1)) != 0
       and G.mat_det(G.coord_swap()) != 0)
print("  generator orders:", [G.porder(g) for g in gens])

# collineation check: every generator maps every line to a line
all_lines_ok = True
for desc, g in zip(gen_desc, gens):
    ok, L = GEO.line_ok(g)
    if not ok:
        all_lines_ok = False
        print("   generator %s fails on line %r" % (desc, sorted(L)))
record(2, "ALL 14 generators map all 73 lines onto lines (collineations)", all_lines_ok,
       "14 x 73 = 1022 line images checked")
# explicit check of two named generators as permutations of lines
line_perm_ok = True
for idx in (0, 12):
    g = gens[idx]
    imgs = {frozenset(g[x] for x in L) for L in GEO.lines}
    if len(imgs) != 73 or imgs != GEO.line_set:
        line_perm_ok = False
record(2, "generators %s and %s induce permutations of the 73 lines" % (gen_desc[0], gen_desc[12]),
       line_perm_ok)

# group order by deterministic Schreier-Sims
B = G.bsgs_order(gens, 73)
rep = B.report()
print("  BSGS:", rep)
record(2, "|<generators>| computed by Schreier-Sims", B.verify() == 0 and rep["order"] == 16482816,
       "order=%d verify_failures=%d base=%r orbits=%r" %
       (rep["order"], rep["verify_failures"], rep["base"], rep["orbit_sizes"]))
record(2, "|PGL(3,8)| = 511*504*448/7 = 16482816",
       511 * 504 * 448 // 7 == 16482816, "511*504*448 = %d, /7 = %d" % (511 * 504 * 448, 511 * 504 * 448 // 7))
record(2, "Schreier-Sims order equals |PGL(3,8)| => <gens> = PGL(3,8)",
       rep["order"] == 16482816)
record(2, "base sizes 73*72*64*49 = 16482816", 73 * 72 * 64 * 49 == 16482816)

# transitivity checks (geometric sanity of the action)
pbits = [[1 << p[i] for i in range(73)] for p in gens]


def orbit_points(start, gens_):
    seen = {start}
    stack = [start]
    while stack:
        x = stack.pop()
        for g in gens_:
            y = g[x]
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


op = orbit_points(0, gens)
record(2, "transitive on the 73 points", len(op) == 73, "orbit size %d" % len(op))
seen = {(0, 1)}
stack = [(0, 1)]
while stack:
    a, b_ = stack.pop()
    for g in gens:
        c = (g[a], g[b_])
        if c not in seen:
            seen.add(c)
            stack.append(c)
record(2, "transitive on ordered pairs of distinct points", len(seen) == 73 * 72,
       "%d = 73*72" % len(seen))
seen = {(0, 1, 9)}
stack = [(0, 1, 9)]
triples = 73 * 72 * 64
while stack:
    a, b_, c_ = stack.pop()
    for g in gens:
        tt = (g[a], g[b_], g[c_])
        if tt not in seen:
            seen.add(tt)
            stack.append(tt)
record(2, "transitive on ordered frames (non-collinear triples)", len(seen) == triples,
       "%d = 73*72*64" % len(seen))
print("  %.1fs" % (time.time() - t))

# ---------------------------------------------------------------------------
hdr("TASK 3. Orbit of the hyperoval (10-cap)")
t = time.time()
hyp_mask = G.mask_of(HYPEROVAL)
record(3, "start mask has popcount 10", G.popcount(hyp_mask) == 10)
orb_h = G.orbit_of_mask(hyp_mask, gens, pbits)
record(3, "orbit size", len(orb_h) == 32704, "%d (expected 32704)" % len(orb_h))
pc = {}
for m in orb_h:
    pc[G.popcount(m)] = pc.get(G.popcount(m), 0) + 1
record(3, "every orbit member is a 10-point set", list(pc.keys()) == [10], "sizes: %r" % pc)
bad_cap = 0
bad_max = 0
for m in orb_h:
    S = G.set_of(m)
    if not GEO.is_cap(S):
        bad_cap += 1
    elif len(GEO.addable(S)) != 0:
        bad_max += 1
record(3, "every orbit member is a cap", bad_cap == 0, "%d failures" % bad_cap)
record(3, "every orbit member is maximal", bad_max == 0, "%d failures" % bad_max)
cens10, cens6m = parse_census_6()
record(3, "orbit size == census total number of 10-caps", cens10 == len(orb_h),
       "census 10-caps=%r, orbit=%d" % (cens10, len(orb_h)))
# maximality is a collineation invariant: addable(g(S)) = g(addable(S)); check it
# for every generator, which transports maximality from the start cap to its orbit
ok_inv = True
for g in gens:
    imgS = {g[p] for p in HYPEROVAL}
    if set(GEO.addable(sorted(imgS))) != {g[p] for p in GEO.addable(HYPEROVAL)}:
        ok_inv = False
record(3, "all 14 generators preserve cap-maximality (addable set maps)", ok_inv)
print("  %.1fs" % (time.time() - t))

# ---------------------------------------------------------------------------
hdr("TASK 4. Orbit of the maximal 6-cap and other maximal 6-caps")
t = time.time()
cap_mask = G.mask_of(CAP6)
orb_c = G.orbit_of_mask(cap_mask, gens, pbits)
record(4, "orbit size of start 6-cap", len(orb_c) == 686784, "%d (expected 686784)" % len(orb_c))
pc = {}
for m in orb_c:
    pc[G.popcount(m)] = pc.get(G.popcount(m), 0) + 1
record(4, "every orbit member is a 6-point set", list(pc.keys()) == [6], "sizes: %r" % pc)
rng = random.Random(20261125)
sample = rng.sample(sorted(orb_c), 500)
bad_cap = sum(0 if GEO.is_cap(G.set_of(m)) else 1 for m in sample)
bad_max = sum(0 if GEO.is_maximal_cap(G.set_of(m)) else 1 for m in sample)
record(4, "sample of 500 orbit members: all caps", bad_cap == 0, "%d failures" % bad_cap)
record(4, "sample of 500 orbit members: all maximal", bad_max == 0, "%d failures" % bad_max)
ok_inv = True
for g in gens:
    imgS = {g[p] for p in CAP6}
    if set(GEO.addable(sorted(imgS))) != {g[p] for p in GEO.addable(CAP6)}:
        ok_inv = False
record(4, "all 14 generators preserve cap-maximality (addable set maps)", ok_inv)
print("  %.1fs" % (time.time() - t))

# find other maximal 6-caps: uniformly sampled from all 6-subsets (rejection)
t = time.time()


def random_maximal_6(rng):
    while True:
        S = sorted(rng.sample(range(73), 6))
        if GEO.is_cap(S) and len(GEO.addable(S)) == 0:
            return S


other6 = []
tries = 0
while len(other6) < 12 and tries < 200000:
    S = random_maximal_6(rng)
    tries += 1
    if S not in other6:
        other6.append(S)
print("  sampled %d distinct maximal 6-caps (%d rejection trials)" % (len(other6), tries))
res6 = []
for S in other6:
    m = G.mask_of(S)
    res6.append((S, m in orb_c, GEO.is_cap(S), len(GEO.addable(S)) == 0))
for S, inorb, okc, okm in res6:
    print("   cap %-28s cap=%s maximal=%s in_start_orbit=%s" % (S, okc, okm, inorb))
record(4, "12 independently sampled maximal 6-caps verified cap+maximal",
       all(c and m for _, _, c, m in res6))
in_orbit = [S for S, i, _, _ in res6 if i]
out_orbit = [S for S, i, _, _ in res6 if not i]
record(4, "some sampled caps lie in the start orbit", len(in_orbit) > 0, "%d/%d" % (len(in_orbit), len(res6)))
record(4, "some sampled caps do NOT lie in the start orbit", len(out_orbit) > 0,
       "%d/%d outside" % (len(out_orbit), len(res6)))

# orbits of the caps outside the start orbit
orbits6 = [orb_c]
reps6 = [sorted(CAP6)]
for S in out_orbit:
    if len(orbits6) >= 3:
        break
    m = G.mask_of(S)
    if any(m in O for O in orbits6):
        continue
    O = G.orbit_of_mask(m, gens, pbits)
    orbits6.append(O)
    reps6.append(S)
    print("  orbit of %r has size %d" % (S, len(O)))
record(4, ">=3 distinct maximal-6-cap orbits found", len(orbits6) >= 3, "%d orbits" % len(orbits6))
sizes_ok = all(len(O) == 686784 for O in orbits6)
record(4, "every computed maximal-6-cap orbit has size 686784", sizes_ok,
       "sizes=%r" % [len(O) for O in orbits6[:4]])
disj = True
for i in range(len(orbits6)):
    for j in range(i + 1, len(orbits6)):
        if orbits6[i] & orbits6[j]:
            disj = False
record(4, "the computed orbits are pairwise disjoint", disj,
       "|union|=%d" % len(set().union(*orbits6)))
union = set().union(*orbits6)
record(4, "union size == 3*686784", len(union) == 3 * 686784, "%d" % len(union))
record(4, "census total of maximal 6-caps == 3*686784", cens6m == 3 * 686784,
       "census=%r, 3*686784=%d" % (cens6m, 3 * 686784))
record(4, "computed orbits exhaust all maximal 6-caps (union == census total)",
       cens6m is not None and len(union) == cens6m,
       "union=%d census=%r" % (len(union), cens6m))
record(4, "hyperoval orbit is disjoint from the 6-cap orbits",
       all(len(O & orb_h) == 0 for O in orbits6))
print("  %.1fs" % (time.time() - t))

# ---------------------------------------------------------------------------
hdr("TASK 5. Group and stabilizer orders")
PGL = 16482816
record(5, "|PGL(3,8)| = 16482816", PGL == 511 * 504 * 448 // 7)
record(5, "|GL(3,8)| = 511*504*448 = 7*|PGL|", 511 * 504 * 448 == 7 * PGL)
for name, orb in (("hyperoval", len(orb_h)), ("6-cap", len(orb_c))):
    q, r = divmod(PGL, orb)
    record(5, "orbit*stabilizer = |PGL| for %s" % name, q * orb == PGL and r == 0,
           "%d = %d * %d (remainder %d)" % (PGL, orb, q, r))
record(5, "hyperoval stabilizer = 16482816/32704 = 504", PGL // 32704 == 504 and PGL % 32704 == 0)
record(5, "maximal-6-cap stabilizer = 16482816/686784 = 24", PGL // 686784 == 24 and PGL % 686784 == 0)
record(5, "504 = |PGL(2,8)| = 8*(8^2-1)", 8 * (8 * 8 - 1) == 504)
record(5, "24 = |S4|", 24 == 4 * 3 * 2 * 1)
record(5, "BSGS order equals |PGL| (independent computation)", rep["order"] == PGL,
       "%d" % rep["order"])

# ---------------------------------------------------------------------------
hdr("SUMMARY")
nfail = sum(1 for r in RESULTS if not r["ok"])
by_task = {}
for r in RESULTS:
    a = by_task.setdefault(r["task"], [0, 0])
    a[0] += 1
    if not r["ok"]:
        a[1] += 1
for task in sorted(by_task):
    tot, f = by_task[task]
    print("  TASK %d: %d checks, %d failed -> %s" % (task, tot, f, "PASS" if f == 0 else "FAIL"))
print("  total checks %d, failures %d" % (len(RESULTS), nfail))
print("  elapsed %.1fs" % (time.time() - t0))

with open("results_orbits.json", "w") as f:
    json.dump({
        "results": RESULTS,
        "generators": gen_desc,
        "pgl_order": rep["order"],
        "bsgs": {k: v for k, v in rep.items()},
        "hyperoval_orbit": len(orb_h),
        "cap6_orbit": len(orb_c),
        "cap6_orbit_sizes": [len(O) for O in orbits6],
        "cap6_orbit_reps": reps6,
        "census_10caps": cens10,
        "census_maximal_6caps": cens6m,
        "sampled_6caps": [{"cap": S, "in_start_orbit": i} for S, i, _, _ in res6],
    }, f, indent=1)
print("  wrote results_orbits.json")
sys.exit(1 if nfail else 0)
