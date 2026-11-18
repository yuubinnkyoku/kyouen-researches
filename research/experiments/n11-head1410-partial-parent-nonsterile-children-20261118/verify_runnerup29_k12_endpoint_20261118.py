#!/usr/bin/env python3
"""Standalone re-verification of the k=12 endpoint of the published ban
survival curve for 00000000000000003800000009000000.

Recomputes A_12 / B_12 / total_12 from scratch (fresh PmLazy over the
parent with the top-12 membership pair types deleted) and compares against
the published curve output (run 1, all 15 checks). Designed to complete in
about 70 s so it fits in a single command window on this host, where
longer background runs get killed near the end.
"""
import json, os, sys, hashlib, time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
TARGET = "00000000000000003800000009000000"
STATE_CAP = 12_000_000
BUDGET_SECONDS = 1500.0

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()

def read_pinned(rel, pin):
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    if git_blob_sha(data) != pin:
        raise SystemExit("pin mismatch: " + rel)
    return data

N = 11
T = [
    lambda x, y: (x, y),
    lambda x, y: (y, N - 1 - x),
    lambda x, y: (N - 1 - x, N - 1 - y),
    lambda x, y: (N - 1 - y, x),
    lambda x, y: (N - 1 - x, y),
    lambda x, y: (x, N - 1 - y),
    lambda x, y: (y, x),
    lambda x, y: (N - 1 - y, N - 1 - x),
]
TO = [tuple(t(i % N, i // N) for i in range(121)) for t in T]

def orbit_masks(mask):
    outs = []
    for to in TO:
        out = 0
        for i in range(121):
            if (mask >> i) & 1:
                qx, qy = to[i]
                out |= 1 << (qy * N + qx)
        outs.append(out)
    return outs

class PmLazy:
    def __init__(self, edge_w, r):
        self.edge_w = edge_w
        self.r = r
        self.memo = {0: 1}
        self.t0 = time.time()
        self.gets = 0

    def get(self, mask):
        memo = self.memo
        if mask in memo:
            self.gets += 1
            return memo[mask]
        edge_w = self.edge_w
        stack = [mask]
        seen = {mask}
        order = []
        while stack:
            m = stack.pop()
            if m in memo:
                continue
            order.append(m)
            if len(memo) + len(seen) > STATE_CAP or time.time() - self.t0 > BUDGET_SECONDS:
                raise MemoryError("pm state cap or budget exceeded")
            if m == 0:
                continue
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            mm = rest
            while mm:
                jbit = mm & -mm
                mm ^= jbit
                j = jbit.bit_length() - 1
                key = (first, j) if first < j else (j, first)
                if edge_w.get(key, 0):
                    sub = rest & ~jbit
                    if sub not in memo and sub not in seen:
                        seen.add(sub)
                        stack.append(sub)
        for m in sorted(order, key=lambda x: bin(x).count("1")):
            if m in memo:
                continue
            low = m & -m
            first = low.bit_length() - 1
            rest = m ^ low
            acc = 0
            mm = rest
            while mm:
                jbit = mm & -mm
                mm ^= jbit
                j = jbit.bit_length() - 1
                key = (first, j) if first < j else (j, first)
                w = edge_w.get(key, 0)
                if w:
                    acc += w * memo[rest & ~jbit]
            memo[m] = acc
        self.gets += 1
        return memo[mask]

def main():
    pub = json.loads(read_pinned(
        "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/runnerup29-cover-membership-20261118.json",
        "05f54eb58baad66403b327696b9a63f7433a13c3"))
    curve = json.load(open(os.path.join(
        HERE, "output", "runnerup29-ban-survival-curve-20261118.json")))
    exp = [e for e in curve["derived"]["curve"] if e["k"] == 12][0]

    row_cands = {}
    with open(os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")) as f:
        for line in f:
            e = json.loads(line)
            row_cands[e["row"]] = e
    p_orbit = {format(m, "032x") for m in orbit_masks(int(TARGET, 16))}
    target = sorted(h for h in row_cands
                   if any(format(int(h, 16) ^ (1 << b), "032x") in p_orbit
                          for b in range(121) if (int(h, 16) >> b) & 1))
    idx = {h: i for i, h in enumerate(target)}
    proot_rows = defaultdict(set)
    for h in target:
        e = row_cands[h]
        for root, bit in e["cands"]:
            proot_rows[root].add(h)
    del row_cands
    r = len(target)
    pair_roots = defaultdict(list)
    singleton_roots = defaultdict(list)
    for root, cov in proot_rows.items():
        if len(cov) == 2:
            a, b = sorted(idx[h] for h in cov)
            pair_roots[(a, b)].append(root)
        else:
            (s,) = [idx[h] for h in cov]
            singleton_roots[s].append(root)
    edge_w = {e: len(rl) for e, rl in pair_roots.items()}
    w1 = {s: len(rl) for s, rl in singleton_roots.items()}
    for s in range(r):
        w1.setdefault(s, 0)

    pub_mem = pub["derived"]["membership"]
    by_mem = sorted(pub_mem, key=lambda x: (-pub_mem[x], x))
    top12 = by_mem[:12]
    root_pair = {root: e for e, rl in pair_roots.items() for root in rl}
    for root in top12:
        e = root_pair[root]
        assert edge_w[e] == 1
        edge_w[e] = 0

    full = (1 << r) - 1
    pm = PmLazy({k: v for k, v in edge_w.items() if v}, r)
    A = 0
    for s in range(r):
        if w1[s]:
            A += w1[s] * pm.get(full ^ (1 << s))
    B = 0
    for d in range(r):
        dbit = 1 << d
        nbrs = [a for a in range(r) if a != d and edge_w.get((min(d, a), max(d, a)))]
        for i in range(len(nbrs)):
            a = nbrs[i]
            wa = edge_w[(min(d, a), max(d, a))]
            for j in range(i + 1, len(nbrs)):
                b = nbrs[j]
                wb = edge_w[(min(d, b), max(d, b))]
                B += wa * wb * pm.get(full ^ dbit ^ (1 << a) ^ (1 << b))
    total = A + B
    ok = (total == exp["total"] and A == exp["type_A"] and B == exp["type_B"])
    print(json.dumps({
        "match": bool(ok),
        "total": total, "expected_total": exp["total"],
        "A": A, "expected_A": exp["type_A"],
        "B": B, "expected_B": exp["type_B"],
        "memo_states": len(pm.memo), "pm_gets": pm.gets,
        "expected_memo_states": exp["memo_states"], "expected_pm_gets": exp["pm_gets"],
    }, indent=1))
    if not ok:
        sys.exit(1)

if __name__ == "__main__":
    main()
