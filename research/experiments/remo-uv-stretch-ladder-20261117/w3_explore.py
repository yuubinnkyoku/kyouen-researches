#!/usr/bin/env python3
"""Explore the internal structure of the weight-3 families W3/H3/G3.

W3(n): n players each holding 3, pot 3, ptr 0.
H3(n): [3]*(n-1) + [4], pot 3, ptr 0 (one hot stone at the last position).
G3(n): [3]*(n-2) + [4, 4], pot 3, ptr 0 (two hot at the last two).

For each n we record:
  - survivor position (0-based)
  - stretch decomposition (list of (pot, count))
  - the end state of the stretch-3 run (pot-3 phases)
  - death stretch of watched positions
and look for sieve-like laws (survivor/death level vs factorizations).
"""
import json
import sys
from collections import Counter


def play_trace(counts, pot, watch=None):
    """Full trace. Returns (survivor, trace, death_of_watch).
    trace[i] = (pot, loser_pos_orig, held).
    watch: dict orig_pos -> placeholder filled with (pot_at_death, held)."""
    n = len(counts)
    lab = list(range(n))
    cts = list(counts)
    k = n
    ptr = 0
    p = pot
    tr = []
    dw = {}
    while k > 1:
        for i in range(p):
            cts[(ptr + i) % k] += 1
        li = (ptr + p) % k
        held = cts[li]
        tr.append((p, lab[li], held))
        if lab[li] in (watch or ()):
            dw[lab[li]] = (p, held)
        del cts[li]; del lab[li]
        ptr = li if li < k - 1 else 0
        p = held
        k -= 1
    return lab[0], tr, dw


def state_after(counts, pot, t):
    """State (labels from ptr, counts, pot) after t phases."""
    n = len(counts)
    lab = list(range(n))
    cts = list(counts)
    k = n
    ptr = 0
    p = pot
    for i in range(t):
        for j in range(p):
            cts[(ptr + j) % k] += 1
        li = (ptr + p) % k
        held = cts[li]
        del cts[li]; del lab[li]
        ptr = li if li < k - 1 else 0
        p = held
        k -= 1
    order = [(lab[(ptr + j) % k], cts[(ptr + j) % k]) for j in range(k)]
    return order, p


def stretches(tr):
    out = []
    for pot, _, _ in tr:
        if out and out[-1][0] == pot:
            out[-1][1] += 1
        else:
            out.append([pot, 1])
    return out


def spf(n):
    p = 2
    while p * p <= n:
        if n % p == 0:
            return p
        p += 1
    return n


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    out = {"W3": [], "H3": [], "G3": []}
    # W3
    for n in range(2, N + 1):
        counts = [3] * n
        sv, tr, dw = play_trace(counts, 3, watch={0, 1, 2})
        st = stretches(tr)
        # end state of stretch-3
        p3 = 0
        for pot, _, _ in tr:
            if pot == 3:
                p3 += 1
            else:
                break
        order, pot_after = state_after(counts, 3, p3)
        shapes = Counter(c for _, c in order)
        out["W3"].append(dict(n=n, sv=sv, str=[list(x) for x in st],
                              p3=p3, end_n=len(order),
                              end_shape=sorted(shapes.items()),
                              end_circle=[l for l, _ in order][:8],
                              end_counts=[c for _, c in order][:8],
                              dw={str(k): v for k, v in dw.items()}))
    # H3
    for n in range(2, N + 1):
        counts = [3] * (n - 1) + [4]
        sv, tr, dw = play_trace(counts, 3, watch={0, n - 1})
        st = stretches(tr)
        p3 = 0
        for pot, _, _ in tr:
            if pot == 3:
                p3 += 1
            else:
                break
        order, pot_after = state_after(counts, 3, p3)
        shapes = Counter(c for _, c in order)
        out["H3"].append(dict(n=n, sv=sv, str=[list(x) for x in st],
                              p3=p3, end_n=len(order),
                              end_shape=sorted(shapes.items()),
                              dw={str(k): v for k, v in dw.items()}))
    # G3
    for n in range(3, N + 1):
        counts = [3] * (n - 2) + [4, 4]
        sv, tr, dw = play_trace(counts, 3, watch={0, n - 2, n - 1})
        st = stretches(tr)
        p3 = 0
        for pot, _, _ in tr:
            if pot == 3:
                p3 += 1
            else:
                break
        order, pot_after = state_after(counts, 3, p3)
        shapes = Counter(c for _, c in order)
        out["G3"].append(dict(n=n, sv=sv, str=[list(x) for x in st],
                              p3=p3, end_n=len(order),
                              end_shape=sorted(shapes.items()),
                              dw={str(k): v for k, v in dw.items()}))
    write_json(out, "data/w3_explore.json")


def write_json(out, path):
    """One record per line (line-oriented, easy to page/inspect)."""
    lines = ["{"]
    for gi, g in enumerate(["W3", "H3", "G3"]):
        lines.append(f' "{g}": [')
        recs = [json.dumps(r, ensure_ascii=False, separators=(",", ": "))
                for r in out[g]]
        for i, rec in enumerate(recs):
            lines.append("  " + rec + ("," if i < len(recs) - 1 else ""))
        lines.append(" ]" + ("," if gi < 2 else ""))
    lines.append("}")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

    # quick pattern reports
    print("=== W3: stretch-3 end shapes by n mod 4 ===")
    by = {}
    for e in out["W3"]:
        r = e["n"] % 4
        by.setdefault(r, Counter())
        by[r][tuple(e["end_shape"])] += 1
    for r in sorted(by):
        print(" n%4 ==", r, dict(by[r].most_common(6)))
    print("=== W3: pos0 death stretch vs candidates ===")
    bad = Counter()
    for e in out["W3"]:
        n = e["n"]
        d = e["dw"].get("0")
        if d is None:
            bad["survive"] += 1
            # when does pos 0 survive?
        else:
            bad[("die", d[0])] += 1
    print(" pos0 fate counts:", dict(bad))
    # correlate: pos0 survives W3(n) iff ... ?
    surv = [e["n"] for e in out["W3"] if e["dw"].get("0") is None]
    print(" n with pos0 surviving:", surv[:40])
    print(" survivors W3(n) values sample:",
          [(e["n"], e["sv"]) for e in out["W3"][:20]])
    print("=== H3: hot(last) death stretch ===")
    bad = Counter()
    for e in out["H3"]:
        d = e["dw"].get(str(e["n"] - 1))
        if d is None:
            bad["survive"] += 1
        else:
            bad[("die", d[0])] += 1
    print(" hot fate counts:", dict(bad))
    print("=== G3: hot deaths ===")
    bad = Counter()
    for e in out["G3"]:
        d1 = e["dw"].get(str(e["n"] - 2))
        d2 = e["dw"].get(str(e["n"] - 1))
        bad[(d1[0] if d1 else None, d2[0] if d2 else None)] += 1
    print(" (hot1, hot2) death pots:", dict(bad))


if __name__ == "__main__":
    main()
