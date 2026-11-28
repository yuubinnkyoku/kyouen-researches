import os
"""Full 2^n Gray-code enumeration of maximal-safe and minimal-double-blocking
families in PG(2,q) for q=3,4.

Definitions (matching K1370/K1371 conventions):
  safe(s): every line meets S in <= s points
  maximal safe: safe and no point outside S can be added keeping safety
  double blocking: every line meets S in >= 2 points
  minimal double blocking: double blocking and every member is critical
    (some line through it has exactly 2 points of S)

Implementation: reflected Gray code with O(1)-per-flip violation counters:
  violating = #lines with count > s
  deficient = #lines with count < 2
"""
import json, time

def enumerate_families(board, s):
    n = board['n']
    lines = board['lines']
    inc = board['inc']
    nl = len(lines)
    cnt = [0]*nl
    violating = 0   # lines with cnt > s
    deficient = nl  # lines with cnt < 2
    maximal_safe = []
    minimal_db = []
    full = (1 << n) - 1
    prev_gray = 0
    start = time.time()
    for i in range(1, 1 << n):
        g = i ^ (i >> 1)
        diff = g ^ prev_gray
        p = diff.bit_length() - 1
        adding = (g >> p) & 1
        prev_gray = g
        for li in inc[p]:
            c = cnt[li]
            if adding:
                cnt[li] = c + 1
                if c == s:
                    violating += 1
                if c == 1:
                    deficient -= 1
            else:
                cnt[li] = c - 1
                if c == s + 1:
                    violating -= 1
                if c == 2:
                    deficient += 1
        if violating == 0:
            # maximality: every non-member has an incident line with cnt == s
            outside = full & ~g
            maximal = True
            m = outside
            while m:
                b = m & -m
                q = b.bit_length() - 1
                if not any(cnt[li] == s for li in inc[q]):
                    maximal = False
                    break
                m ^= b
            if maximal:
                maximal_safe.append((bin(g).count('1'), g))
        if deficient == 0:
            # minimality: every member has an incident line with cnt == 2
            minimal = True
            m = g
            while m:
                b = m & -m
                q = b.bit_length() - 1
                if not any(cnt[li] == 2 for li in inc[q]):
                    minimal = False
                    break
                m ^= b
            if minimal:
                minimal_db.append((bin(g).count('1'), g))
    return maximal_safe, minimal_db, time.time()-start

def summary(fam):
    from collections import Counter
    return dict(sorted(Counter(sz for sz, _ in fam).items()))

def main():
    boards = json.load(open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/boards.json'))
    results = {}
    for q in (3, 4):
        b = boards[f'pg2q{q}']
        s = {3: 2, 4: 3}[q]
        ms, mdb, wall = enumerate_families(b, s)
        results[f'pg2q{q}'] = {
            's': s,
            'maximal_safe_by_size': summary(ms),
            'minimal_double_blocking_by_size': summary(mdb),
            'wall_s': round(wall, 2),
        }
        print(f'PG(2,{q}) s={s}: maximal_safe={summary(ms)} '
              f'minimal_db={summary(mdb)} wall={wall:.1f}s')
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+f'/out/pg2q{q}_maximal_safe.txt', 'w') as f:
            for sz, g in ms:
                f.write(f'{sz} {g}\n')
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+f'/out/pg2q{q}_minimal_db.txt', 'w') as f:
            for sz, g in mdb:
                f.write(f'{sz} {g}\n')
    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/enumeration.json', 'w') as f:
        json.dump(results, f, indent=1)

if __name__ == '__main__':
    main()
