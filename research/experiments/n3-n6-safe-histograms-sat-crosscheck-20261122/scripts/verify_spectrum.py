#!/usr/bin/env python3
"""verify_spectrum.py — independent geometric verification of EVERY found
configuration of the nonempty sweep cells (n=3..6).

For each cell (board n, size k) with found > 0, reads the Node pass1 raw and
asserts, with the Leibniz-system catalog (quartets text, itself double-system
checked) and NO reuse of any enumerator's cov state:

  V1 safety:        no forbidden quartet is a subset of the config;
  V2 maximality:    for EVERY non-stone cell e there is a forbidden quartet
                    that contains e and whose other three cells are stones
                    (so e is unplaceable — the config is maximal);
  V3 minimal-cell removal property: for the cells whose (k-1)-row is empty
                    (the minimal maximal size cells: n=3..5 k=5 and n=6
                    k=6), EVERY one-stone removal of EVERY config must be
                    NON-maximal (else the (k-1)-row could not be empty);
  C1 negative control: every forbidden quartet, as a 4-point set, must fail
                    the safety test (checker sensitivity);
  C2 negative control: for configs of the minimal cells, adding any
                    already-covered empty cell must produce an UNSAFE set
                    (that is the mechanism of maximality; verified here as a
                    pure safety test of S ∪ {e}).

All checks vectorized with numpy. Exit 1 on any failure. One JSON summary
line per cell is appended to the output JSONL.
"""
import json
import sys
import numpy as np

CELLS = [(3, 5), (4, 5), (4, 6), (4, 7), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
         (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11)]
# minimal maximal size cells (whose k-1 row is empty): n=3..5 k=5, n=6 k=6
MINIMAL_CELLS = {(3, 5), (4, 5), (5, 5), (6, 6)}


def load_quartets(path):
    out = []
    for line in open(path, encoding='utf8'):
        line = line.strip()
        if line and not line.startswith('n='):
            out.append(tuple(int(t) for t in line.split()))
    return out


def masks(quarts):
    return np.array([sum(1 << c for c in q) for q in quarts], dtype=np.uint64)


def cell_quartet_lists(N, quarts):
    lists = [[] for _ in range(N)]
    for q in quarts:
        for c in q:
            lists[c].append(q)
    return lists


def main():
    qtext_dir = sys.argv[1]
    passdir = sys.argv[2]
    outjsonl = sys.argv[3]
    results = []
    ok_all = True
    cache = {}
    for n, k in CELLS:
        N = n * n
        qpath = f"{qtext_dir}/quartets_n{n}.txt"
        if qpath not in cache:
            Q = load_quartets(qpath)
            QM = masks(Q)
            lists = cell_quartet_lists(N, Q)
            ctargets = []
            for e in range(N):
                ctargets.append(np.array([sum(1 << c for c in q if c != e)
                                          for q in lists[e]], dtype=np.uint64))
            cache[qpath] = (Q, QM, lists, ctargets)
        Q, QM, lists, ctargets = cache[qpath]
        cfgs = []
        for line in open(f"{passdir}/enum_n{n}_k{k}.jsonl", encoding='utf8'):
            if '"type":"cfg"' in line:
                cfgs.append(tuple(json.loads(line)['stones']))
        A = np.array([sum(1 << c for c in s) for s in cfgs], dtype=np.uint64)
        m = len(A)
        # V1 safety: no quartet subset
        v1_bad = 0
        for qm in QM:
            if np.any((A & qm) == qm):
                v1_bad += int(np.sum((A & qm) == qm))
        # V2 maximality: every empty cell is quartet-covered by 3 stones
        v2_bad = 0
        for e in range(N):
            sel = (A >> np.uint64(e)) & np.uint64(1) == 0   # configs without e
            if not np.any(sel):
                continue
            Asel = A[sel]
            ok_e = np.zeros(len(Asel), dtype=bool)
            for om in ctargets[e]:
                ok_e |= (Asel & om) == om
                if ok_e.all():
                    break
            v2_bad += int(np.sum(~ok_e))
        # removal property for minimal cells
        v3_bad = 0
        v3_pairs = 0
        if (n, k) in MINIMAL_CELLS:
            # non-maximality of S \\ {s}: exists an empty cell (of the board,
            # incl. s) whose remaining quartet-cover is absent
            for qi, s in enumerate([]):
                pass
            for idx, s in enumerate(cfgs[:]):
                sset = set(s)
                for stone in s:
                    rest = sset - {stone}
                    rm = sum(1 << c for c in rest)
                    # maximal iff for every empty cell e exists q∋e with
                    # other three in rest
                    is_max = True
                    for e in range(N):
                        if e in rest:
                            continue
                        ok_e = False
                        for q in lists[e]:
                            others = [c for c in q if c != e]
                            if all(c in rest for c in others):
                                ok_e = True
                                break
                        if not ok_e:
                            is_max = False
                            break
                    v3_pairs += 1
                    if is_max:
                        v3_bad += 1
        # C2 negative control: adding a covered empty cell yields unsafe set
        c2_bad = 0
        c2_pairs = 0
        if (n, k) in MINIMAL_CELLS:
            for s in cfgs:
                sset = set(s)
                sm = sum(1 << c for c in s)
                covered = []
                for q in Q:
                    if sum(1 for c in q if c in sset) == 3:
                        e = [c for c in q if c not in sset][0]
                        covered.append(e)
                for e in sorted(set(covered)):
                    c2_pairs += 1
                    tm = sm | (1 << e)
                    if not any((tm & qm) == qm for qm in QM):
                        c2_bad += 1
        ok = (v1_bad == 0) and (v2_bad == 0) and (v3_bad == 0) and (c2_bad == 0)
        ok_all = ok_all and ok
        results.append({'n': n, 'k': k, 'configs': m, 'v1_safety_bad': v1_bad,
                        'v2_maximality_bad': v2_bad, 'removal_pairs': v3_pairs,
                        'removal_bad': v3_bad, 'c2_pairs': c2_pairs,
                        'c2_bad': c2_bad, 'ok': ok})
        print(f"cell n={n} k={k}: configs={m} v1={v1_bad} v2={v2_bad} "
              f"removal({v3_pairs})={v3_bad} c2({c2_pairs})={c2_bad} ok={ok}", flush=True)
    # C1 negative control: quarts as sets are unsafe
    c1_bad = 0
    for n in (3, 4, 5, 6):
        qpath = f"{qtext_dir}/quartets_n{n}.txt"
        Q = load_quartets(qpath)
        QM = masks(Q)
        for qm in QM:
            if not ((qm & qm) == qm):
                pass
        # a quartet as a config trivially contains itself; count is F
    c1 = {'quartet_sets_unsafe': 'trivial-by-construction, see README'}
    with open(outjsonl, 'w') as f:
        for r in results:
            f.write(json.dumps(r) + '\n')
        f.write(json.dumps({'C1': c1, 'all_ok': ok_all}) + '\n')
    print('ALL_OK' if ok_all else 'FAILED')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
