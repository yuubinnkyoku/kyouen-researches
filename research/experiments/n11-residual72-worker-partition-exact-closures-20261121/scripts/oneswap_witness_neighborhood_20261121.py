#!/usr/bin/env python3
"""One-swap neighborhood certificates around the published UB witnesses (2026-11-21 addendum 2).

Exhaustively enumerates all balanced single-root swaps (same-size groups, so any
cross-group swap keeps 9 roots per worker) around two published witnesses:
  1. the W=4 super-witness (class10 1937 / pair10 1939 / cross9 47), and
  2. the distinct 9-stone-layer x9 witness (cross9 47),
and records for each objective whether any neighbor improves the witness value.
Outputs output/oneswap_witness_neighborhood_20261121.json. Fail-closed: fails on
input pin mismatch, witness load failure, or neighborhood count != 486 (4x9 groups).
This proves only 1-swap local optimality, NOT global optimality.
"""
import json, hashlib, sys, os

FILES = {
    "census.json":   "research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json",
    "mr10.json":      "research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-10stone-20261121.json",
    "mr09.json":      "research/experiments/n11-residual72-36root-exact-class-membership-20261121/output/multi-root-classes-09stone-20261121.json",
}
PINS = {
    "census.json":   "94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023",
    "mr10.json":     "5fec87afda5011243403d5efc71209cb9cd602eb3bb02bd833bd9341cb218b08",
    "mr09.json":     "68aa7df1e7b42c3661f404a6949439c31a3619140ae1ddf361001b375c0b6f9f",
}
OUT = "research/experiments/n11-residual72-worker-partition-exact-closures-20261121/output"

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

for name, want in PINS.items():
    if sha256(FILES[name]) != want:
        sys.exit("PIN FAIL " + name)

census = json.load(open(FILES["census.json"]))
mr10 = json.load(open(FILES["mr10.json"]))
mr09 = json.load(open(FILES["mr09.json"]))["classes"]
per_root = census["per_root"]
root_name = [r["root"] for r in per_root]
N = 36
idx = {n: i for i, n in enumerate(root_name)}

CE = [[0] * N for _ in range(N)]
PALL = [[0] * N for _ in range(N)]
W9 = [[0] * N for _ in range(N)]
triples = []
for c in mr10:
    m = c["roots"]
    if len(m) == 2:
        i, j = m
        CE[i][j] += 1; CE[j][i] += 1
        PALL[i][j] += 1; PALL[j][i] += 1
    else:
        triples.append(m)
        for x in range(len(m)):
            for y in range(x + 1, len(m)):
                PALL[m[x]][m[y]] += 1; PALL[m[y]][m[x]] += 1
for c in mr09:
    i, j = c["roots"]
    W9[i][j] += 1; W9[j][i] += 1

def class10(a):
    s = sum(CE[i][j] for i in range(N) for j in range(i + 1, N) if a[i] != a[j])
    for t in triples:
        s += len({a[r] for r in t}) - 1
    return s

def pair10(a):
    return sum(PALL[i][j] for i in range(N) for j in range(i + 1, N) if a[i] != a[j])

def cross9(a):
    return sum(W9[i][j] for i in range(N) for j in range(i + 1, N) if a[i] != a[j])

def load_witness(fn):
    d = json.load(open(os.path.join(OUT, fn)))
    gs = d["witness"]["groups"]
    a = [None] * N
    for w, g in enumerate(gs):
        for rn in g:
            a[idx[rn]] = w
    if None in a:
        sys.exit("witness load failure " + fn)
    return a

def neighborhood(a):
    """returns dict: objective -> {feasible, improving, best_neighbor, strict_best_worse}"""
    base = {"class10": class10(a), "pair10": pair10(a), "cross9": cross9(a)}
    res = {k: {"feasible": 0, "improving": 0, "best_neighbor": None} for k in base}
    for i in range(N):
        for j in range(i + 1, N):
            if a[i] == a[j]:
                continue
            b = a[:]
            b[i], b[j] = b[j], b[i]
            for k, f in (("class10", class10), ("pair10", pair10), ("cross9", cross9)):
                res[k]["feasible"] += 1
                v = f(b)
                if v < base[k]:
                    res[k]["improving"] += 1
                if res[k]["best_neighbor"] is None or v < res[k]["best_neighbor"]:
                    res[k]["best_neighbor"] = v
    for k in res:
        res[k]["base"] = base[k]
        res[k]["strict_local_opt"] = res[k]["improving"] == 0 and res[k]["best_neighbor"] > base[k]
        res[k]["nonstrict_local_opt"] = res[k]["improving"] == 0
    return res

sw = load_witness("w4class_result.json")
xw = load_witness("x9_result.json")
# cross-identity guard: super-witness must reproduce its claimed values
assert class10(sw) == 1937 and pair10(sw) == 1939 and cross9(sw) == 47, "super-witness mismatch"
assert cross9(xw) == 47, "x9 witness mismatch"
assert sorted(sw) != sorted(xw) or sw != xw, "witnesses unexpectedly identical"
super_res = neighborhood(sw)
x9_res = {"cross9": neighborhood(xw)["cross9"]}
for k in ("class10", "pair10", "cross9"):
    assert super_res[k]["feasible"] == 486, (k, super_res[k]["feasible"])
assert x9_res["cross9"]["feasible"] == 486

summary = {
    "schema": "n11-residual72-worker-partition-oneswap-witness-neighborhood-20261121-v1",
    "super_witness": super_res,
    "x9_witness": x9_res,
    "interpretation": "strict 1-swap local optimality only; NOT a global-optimality proof; T1/T2/W=4/W=6/x9 global optima remain UNKNOWN",
}
out_name = os.path.join(OUT, "oneswap_witness_neighborhood_20261121.json")
with open(out_name, "w") as f:
    json.dump(summary, f, indent=1)
print("super-witness:", {k: (v["improving"], v["best_neighbor"], v["strict_local_opt"]) for k, v in super_res.items()})
print("x9-witness cross9:", (x9_res["cross9"]["improving"], x9_res["cross9"]["best_neighbor"], x9_res["cross9"]["strict_local_opt"]))
print("DONE")
