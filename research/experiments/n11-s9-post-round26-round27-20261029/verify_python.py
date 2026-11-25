#!/usr/bin/env python3
"""Independent Python N11 round27 certificate verifier: no Node, cache or df-pn."""
import base64
import functools
import hashlib
import itertools
import json
from pathlib import Path

base = Path(__file__).resolve().parent
plan = json.loads((base / "../n11-s9-post-round26-replan-20261029/next-plan.json").read_text())
cert = json.loads((base / "certificate.json").read_text())
keys = plan["newSelectedKeys"]
claims = base64.b64decode(cert["witnessBase64"])
assert len(keys) == len(claims) == 1
assert hashlib.sha256(("\n".join(keys) + "\n").encode()).hexdigest() == plan["newSelectionSha256"]
assert hashlib.sha256(claims).hexdigest() == cert["witnessSha256"]
assert cert["selectionSha256"] == plan["newSelectionSha256"]
assert cert["sourcePlanSha256"] == plan["newSelectionSha256"]
prior = json.loads((base / "../n11-s9-post-round25-round26-20261029/certificate.json").read_text())
assert cert["sourcePriorWitnessSha256"] == prior["witnessSha256"]
assert plan["sourceWitnessSha256"] == prior["witnessSha256"]
assert cert["format"] == "n11-s9-post-round26-round27-terminal-v1"
assert plan["emptyBoard"] == cert["emptyBoard"] == "UNKNOWN"
assert plan["selectedCount"] == 1 and plan["legal10Children"] == 29
xy = [(i % 11, i // 11) for i in range(121)]
transforms = []
for t in range(8):
    mapping = []
    for x, y in xy:
        xx, yy = (
            (x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
            (10-x, y), (10-y, 10-x), (x, 10-y), (y, x)
        )[t]
        mapping.append(11*yy + xx)
    transforms.append(mapping)

def pts(b):
    return [i for i in range(121) if b & (1 << i)]

def key(b):
    return f"{b:032x}"

def canonical(b):
    pp = pts(b)
    return min(sum(1 << tr[p] for p in pp) for tr in transforms)

def det3(q):
    x, y = xy[q[3]]
    u, v, w = [(a-x, b-y, a*a+b*b-x*x-y*y) for a, b in (xy[p] for p in q[:3])]
    return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0])

def det4(q):
    m = [[x, y, x*x+y*y, 1] for x, y in (xy[p] for p in q)]
    sign = prev = 1
    for k in range(3):
        if not m[k][k]:
            j = next((j for j in range(k+1, 4) if m[j][k]), None)
            if j is None:
                return 0
            m[k], m[j] = m[j], m[k]
            sign = -sign
        pivot = m[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                num = m[i][j]*pivot - m[i][k]*m[k][j]
                assert num % prev == 0
                m[i][j] = num // prev
        for i in range(k+1, 4):
            m[i][k] = 0
        prev = pivot
    return sign*m[3][3]

def legal(b, determinant):
    pp = pts(b)
    triples = list(itertools.combinations(pp, 3))
    return [p for p in range(121)
            if not b & (1 << p) and
            not any(determinant((*t, p)) == 0 for t in triples)]

def solve10(h):
    b = int(h, 16)
    pp = pts(b)
    assert len(pp) == 10 and key(canonical(b)) == h
    moves = legal(b, det4)
    n = len(moves)
    assert n <= 30
    bad = []
    for i, j in itertools.combinations(range(n), 2):
        if any(det4((u, v, moves[i], moves[j])) == 0
               for u, v in itertools.combinations(pp, 2)):
            bad.append((1 << i) | (1 << j))
    def has_sub(mask):
        return any((mask & v) == v for v in bad)
    for i, j, k in itertools.combinations(range(n), 3):
        mask = (1 << i) | (1 << j) | (1 << k)
        if not has_sub(mask) and any(det4((p, moves[i], moves[j], moves[k])) == 0 for p in pp):
            bad.append(mask)
    for i, j, k, l in itertools.combinations(range(n), 4):
        mask = (1 << i) | (1 << j) | (1 << k) | (1 << l)
        if not has_sub(mask) and det4((moves[i], moves[j], moves[k], moves[l])) == 0:
            bad.append(mask)
    bans = [[] for _ in range(n)]
    for mask in bad:
        for i in range(n):
            if mask & (1 << i):
                bans[i].append(mask ^ (1 << i))
    @functools.lru_cache(None)
    def win(state):
        for i in range(n):
            bit = 1 << i
            if state & bit or any((state & v) == v for v in bans[i]):
                continue
            if not win(state | bit):
                return True
        return False
    result = win(0)
    return result, win.cache_info().currsize

memo = {}
states = obligations = wins = losses = win_edges = 0
loss_parents = set()
win8_parents = set()
for root, witness in zip(keys, claims):
    b = int(root, 16)
    assert len(pts(b)) == 9 and key(canonical(b)) == root
    assert all(det3(q) != 0 and det4(q) != 0
               for q in itertools.combinations(pts(b), 4))
    children3 = sorted({key(canonical(b | (1 << p))) for p in legal(b, det3)})
    children4 = sorted({key(canonical(b | (1 << p))) for p in legal(b, det4)})
    assert children3 == children4
    def terminal(h):
        global states
        if h not in memo:
            verdict, visited = solve10(h)
            memo[h] = verdict
            states += visited
        return memo[h]
    if witness == 255:
        wins += 1
        for h in children3:
            obligations += 1
            assert terminal(h), ("forged WIN9", root, h)
        win_edges += len(children3)
        for p in pts(b):
            win8_parents.add(key(canonical(b ^ (1 << p))))
    else:
        losses += 1
        assert witness < len(children3)
        h = children3[witness]
        obligations += 1
        assert not terminal(h), ("forged LOSS9", root, h)
        leaf = int(h, 16)
        for p in pts(leaf):
            loss_parents.add(key(canonical(leaf ^ (1 << p))))
assert wins == cert["win9"] and losses == cert["loss9"]
assert win_edges == cert["win10Edges"]
assert len(loss_parents) == cert["loss9ParentClosure"]
assert hashlib.sha256(("\n".join(sorted(loss_parents)) + "\n").encode()).hexdigest() == cert["loss9ParentSha256"]
assert all(h not in loss_parents for h in cert["win9Keys"])
# Cross-batch polarity check: all earlier independently audited WIN9 roots.
for n in range(9, 27):
    day = "20261028" if n <= 12 else "20261029"
    earlier = json.loads((base / f"../n11-s9-post-round{n-1}-round{n}-{day}/certificate.json").read_text())
    assert loss_parents.isdisjoint(earlier["win9Keys"]), ("cross-batch WIN9/LOSS9 conflict", n)

assert len(memo) <= obligations == cert['win10Edges'] + cert['loss9']
assert states <= cert['terminalStatesPerGeometry']
print(json.dumps({"verified": True, "win9": wins, "loss9": losses,
                  "terminalLeaves": len(memo), "terminalStates": states,
                  "win8Parents": len(win8_parents), "loss9Parents": len(loss_parents),
                  "emptyBoard": "UNKNOWN"}, indent=2))
