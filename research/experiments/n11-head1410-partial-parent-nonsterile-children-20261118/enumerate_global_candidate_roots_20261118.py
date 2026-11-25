#!/usr/bin/env python3
"""Phase 1 (chunked): global D4 candidate-root enumeration for all open,
non-STERILE S6 rows of the head-1410 worklist (post-fold-chain head-1476 state).

For each row: enumerate candidate 7th stones d (det4 of every stone triple
with d nonzero -> d completes no degenerate circle with 3 existing stones? no:
d is a valid candidate extension iff no triple of the row's 6 stones is
co-circular with d... actually: d is a candidate iff for ALL triples (i,j,k)
det4(stones_i, stones_j, stones_k, d) != 0, matching the published
own_candidates_s6_s7_edge_cost). For each candidate emit the D4-canonical
root hex (row | 1<<d canonized) and the bit.

Output: JSONL, one line per row: {"row": hex, "cost": int,
 "cands": [[root_hex, bit], ...]}
"""
import json, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 11

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()

def read_pinned(rel, pin):
    with open(os.path.join(ROOT, rel), "rb") as f:
        data = f.read()
    if git_blob_sha(data) != pin:
        raise SystemExit("pin mismatch: " + rel)
    return data

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

def canon_hex(mask):
    best = None
    for to in TO:
        out = 0
        for i in range(121):
            if (mask >> i) & 1:
                qx, qy = to[i]
                out |= 1 << (qy * N + qx)
        if best is None or out < best:
            best = out
    return format(best, "032x")

def det3(a, b, c):
    x1, y1 = a % N, a // N
    x2, y2 = b % N, b // N
    x3, y3 = c % N, c // N
    A, B, C = x1 * x1 + y1 * y1, x1, y1
    D, E, F = x2 * x2 + y2 * y2, x2, y2
    G, H, I = x3 * x3 + y3 * y3, x3, y3
    return A * (E * I - F * H) - B * (D * I - F * G) + C * (D * H - E * G)

def det4(a, b, c, d):
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)

def main():
    frm = int(sys.argv[1]); to = int(sys.argv[2])
    out_path = os.path.join(HERE, "output", "global-candidate-roots-20261118.jsonl")
    wl = read_pinned("research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
                     "2fee1d0718547a62e346d35f5858d7913e37c097").decode().rstrip("\r\n").split("\n")
    headers = [h.strip() for h in wl[0].split(",")]
    rows = {}
    for line in wl[1:]:
        vals = line.split(",")
        r = {h: (vals[i].strip() if i < len(vals) else "") for i, h in enumerate(headers)}
        rows[r["s6_canonical_hex"]] = r
    cen = json.loads(read_pinned("research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
                                 "9c251da3138c5cb0516e097be5e5d0427dfaf5f0"))
    led = json.loads(read_pinned("research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
                                 "e8785d509e8a11a37c0d03cc450455a14708c34d"))
    closed = set(led["derived"]["closed_rows_66"])
    sterile = {x["hex"] for x in cen["sterile_row_registry"]}
    open_rows = sorted(h for h in rows if h not in closed and h not in sterile)
    if to > len(open_rows):
        to = len(open_rows)
    part = open_rows[frm:to]
    mode = "a" if frm > 0 else "w"
    with open(out_path, mode) as out:
        for h in part:
            m = int(h, 16)
            stones = [i for i in range(121) if (m >> i) & 1]
            cost = int(rows[h]["own_candidates_s6_s7_edge_cost"])
            cands = []
            for d in range(121):
                if (m >> d) & 1:
                    continue
                ok = True
                for i in range(6):
                    if not ok: break
                    for j in range(i + 1, 6):
                        if not ok: break
                        for k in range(j + 1, 6):
                            if det4(stones[i], stones[j], stones[k], d) == 0:
                                ok = False
                                break
                if ok:
                    cands.append([canon_hex(m | (1 << d)), d])
            assert len(cands) == cost, (h, len(cands), cost)
            out.write(json.dumps({"row": h, "cost": cost, "cands": cands}, separators=(",", ":")) + "\n")
    print("chunk", frm, to, "rows", len(part), "total_open", len(open_rows))

if __name__ == "__main__":
    main()
