#!/usr/bin/env python3
"""Independently check the reservoir-sampled caps from cap_census.exe.

For every sampled cap:
  * validate that it is a cap (<=2 points on every line),
  * recompute its addable-point set TWO ways in pure Python:
      (a) direct: q not in S is addable iff every line through q and a point of S
          contains exactly one point of S,
      (b) secant-union mask: U = union of line(a,b) over pairs of S;
          q is addable iff q is in neither S nor U,
  * check the reported maximal / non-maximal status,
  * print an explicit addable point for the non-maximal classes.
"""
import sys
from collections import Counter, defaultdict


def parse_board(path):
    with open(path, encoding="utf-8") as f:
        raw = [ln.split() for ln in f if ln.strip()]
    n, b = int(raw[0][0]), int(raw[0][1])
    lines = []
    for row in raw[1:]:
        vals = [int(t) for t in row]
        k = vals[0]
        assert len(vals[1:]) == k
        lines.append(vals[1:])
    assert len(lines) == b
    return n, lines


def build_index(n, lines):
    pair_line = {}
    line_mask = []
    for li, L in enumerate(lines):
        m = 0
        for p in L:
            m |= 1 << p
            for q in L:
                if p < q:
                    pair_line[(p, q)] = li
        line_mask.append(m)
    return pair_line, line_mask


def is_cap(S, lines):
    for L in lines:
        c = sum(1 for p in L if p in S)
        if c > 2:
            return False, (L, c)
    return True, None


def addable_direct(S, n, lines, pair_line):
    out = []
    for q in range(n):
        if q in S:
            continue
        good = True
        for a in S:
            key = (a, q) if a < q else (q, a)
            L = lines[pair_line[key]]
            c = 0
            for p in L:
                if p in S:
                    c += 1
            if c >= 2:
                good = False
                break
        if good:
            out.append(q)
    return out


def addable_union(S, n, line_mask, pair_line):
    U = 0
    Sl = sorted(S)
    for i in range(len(Sl)):
        for j in range(i + 1, len(Sl)):
            U |= line_mask[pair_line[(Sl[i], Sl[j])]]
    Sm = 0
    for p in Sl:
        Sm |= 1 << p
    return [q for q in range(n) if not ((Sm >> q) & 1) and not ((U >> q) & 1)]


def main():
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    boards = {
        "PG": parse_board("../output/board_pg2q8.txt"),
        "AG": parse_board("../output/board_ag2q8.txt"),
    }
    idx = {}
    for tag, (n, lines) in boards.items():
        idx[tag] = (n, lines) + build_index(n, lines)

    logs = ["census_pg_main.log", "census_ag_main.log"]
    samples = []
    for log in logs:
        with open(log, encoding="utf-8") as f:
            for ln in f:
                t = ln.split()
                if t and t[0] == "SAMPLE":
                    label = t[1]
                    size = int(t[2])
                    pts = tuple(int(x) for x in t[3:])
                    assert len(pts) == size, (ln, size)
                    samples.append((label, size, pts))

    by_label = defaultdict(list)
    for label, size, pts in samples:
        by_label[label].append((size, pts))

    print("=" * 78)
    print("Independent verification of reservoir-sampled caps")
    print("=" * 78)
    failures = 0
    for label in sorted(by_label):
        tag = label[:2]
        n, lines, pair_line, line_mask = idx[tag]
        expect_max = label.endswith("max")
        expect_nonmax = label.endswith("non")
        items = by_label[label]
        bad_cap = 0
        bad_status = 0
        mismatch_methods = 0
        addable_counts = Counter()
        completion_sizes = Counter()
        completion_caps = 0
        examples = []
        for size, pts in items:
            S = set(pts)
            ok, info = is_cap(S, lines)
            if not ok:
                bad_cap += 1
                print(f"  FAIL {label}: not a cap: {info}")
                continue
            A = addable_direct(S, n, lines, pair_line)
            B = addable_union(S, n, line_mask, pair_line)
            if set(A) != set(B):
                mismatch_methods += 1
            addable_counts[len(A)] += 1
            # structural check: S plus all its addable points
            T = S | set(A)
            okT, _ = is_cap(T, lines)
            completion_sizes[len(T)] += 1
            completion_caps += 1 if okT else 0
            if expect_max and A:
                bad_status += 1
                print(f"  FAIL {label}: marked maximal but addable {A[:5]}")
            if (expect_nonmax or label.endswith(("7", "8", "9"))) and not A:
                bad_status += 1
                print(f"  FAIL {label}: expected an addable point but none found")
            if A and len(examples) < 3:
                examples.append((pts, A[0]))
        print(f"  {label}: {len(items)} samples of size {items[0][0]}; "
              f"cap-valid={len(items)-bad_cap}/{len(items)}; "
              f"addable-count histogram={dict(addable_counts)}; "
              f"two-method mismatches={mismatch_methods}")
        print(f"    S u (all addable points): sizes {dict(completion_sizes)}, "
              f"all caps: {completion_caps}/{len(items) - bad_cap}")
        status_ok = (bad_status == 0)
        print(f"    {'PASS' if (bad_cap == 0 and status_ok and mismatch_methods == 0) else 'FAIL'}"
              f"  status as expected ({'maximal' if expect_max else 'non-maximal' if expect_nonmax else 'any, must be non-maximal'})")
        for pts, a in examples:
            print(f"    example: cap {pts} -> addable point {a}")
        if bad_cap or bad_status or mismatch_methods:
            failures += 1

    print()
    print("=" * 78)
    print(f"RESULT: {'PASS' if failures == 0 else 'FAIL'} ({failures} failing classes)")
    print("=" * 78)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
