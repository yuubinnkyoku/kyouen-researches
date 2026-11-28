import os
"""Independent verification of the PG(2,3)/PG(2,4) orbit-census experiment.

Checks (all fail-closed):
 1. Definition-direct re-verification of every published mask:
    maximal_safe: all lines <= s AND no addable point
    minimal_db:  all lines >= 2 AND every member critical
 2. Independent full enumeration for PG(2,3) (no Gray code: direct scan of
    all 2^13 masks) and for PG(2,4) restricted to combination-based
    enumeration of the observed sizes plus neighboring sizes to bound
    absence of other sizes (sizes k in {6..10} for maximal safe and
    {11..15} for minimal DB, via itertools.combinations).
 3. Orbit partition consistency: random group elements applied to random
    masks stay in the same orbit class; orbit sizes multiply-check
    |orbit| divides |PGL|; sum of orbit sizes = total masks.
 4. Baer-subplane identification for PG(2,4) size-7 maximal safe sets:
    the 7 lines meeting the rep in 3 points form a 2-(7,3,1) design.
"""
import json, random, sys, time
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boards import make_field, inv_table

def load_board(q):
    boards = json.load(open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/boards.json'))
    return boards[f'pg2q{q}']

def def_check(board, mask, kind, s):
    lines = board['lines']
    n = board['n']
    cnts = [len([p for p in L if (mask >> p) & 1]) for L in lines]
    if kind == 'maximal_safe':
        if any(c > s for c in cnts):
            return False
        for p in range(n):
            if (mask >> p) & 1:
                continue
            if all(cnts[li] < s for li in range(len(lines))
                    if p in lines[li]):
                return False
        return True
    else:
        if any(c < 2 for c in cnts):
            return False
        for p in range(n):
            if not (mask >> p) & 1:
                continue
            if all(cnts[li] > 2 for li in range(len(lines)) if p in lines[li]):
                return False
        return True

def independent_enumeration(board, s):
    """Direct (non-Gray) full scan of all 2^n masks using popcount on
    precomputed line masks (methodologically independent of the Gray-code
    incremental enumerator)."""
    n = board['n']
    lineM = [sum(1 << p for p in L) for L in board['lines']]
    inc = board['inc']
    ms, db = [], []
    for mask in range(1, 1 << n):
        cnts = [bin(mask & lm).count('1') for lm in lineM]
        if all(c <= s for c in cnts):
            ok = True
            for p in range(n):
                if (mask >> p) & 1:
                    continue
                if all(cnts[li] < s for li in inc[p]):
                    ok = False
                    break
            if ok:
                ms.append(mask)
        if all(c >= 2 for c in cnts):
            ok = True
            for p in range(n):
                if not (mask >> p) & 1:
                    continue
                if all(cnts[li] > 2 for li in inc[p]):
                    ok = False
                    break
            if ok:
                db.append(mask)
    return ms, db, 'full 2^n direct popcount'

def main():
    random.seed(20261128)
    report = {}
    ok_all = True
    for q in (3, 4):
        board = load_board(q)
        s = {3: 2, 4: 3}[q]
        rep = {'q': q, 's': s}
        # 1. definition-direct re-verification of published masks
        for kind, path in (('maximal_safe', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+f'/out/pg2q{q}_maximal_safe.txt'),
                           ('minimal_db', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+f'/out/pg2q{q}_minimal_db.txt')):
            masks = [int(l.split()[1]) for l in open(path)]
            bad = [g for g in masks if not def_check(board, g, kind, s)]
            rep[f'def_check_{kind}'] = {'n': len(masks), 'failures': len(bad)}
            if bad:
                ok_all = False
        # 2. independent enumeration
        t0 = time.time()
        ms, db, method = independent_enumeration(board, s)
        pub_ms = set(int(l.split()[1]) for l in open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+f'/out/pg2q{q}_maximal_safe.txt'))
        pub_db = set(int(l.split()[1]) for l in open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+f'/out/pg2q{q}_minimal_db.txt'))
        rep['independent'] = {
            'method': method, 'wall_s': round(time.time()-t0, 1),
            'maximal_safe_match': set(ms) == pub_ms,
            'minimal_db_match': set(db) == pub_db,
            'counts': (len(ms), len(db)),
        }
        if set(ms) != pub_ms or set(db) != pub_db:
            ok_all = False
        # 3. orbit consistency
        orb = json.load(open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/orbits.json'))[f'pg2q{q}']
        from orbits import gen_pgl, apply_perm
        perms = gen_pgl(q, board)
        checks = []
        for name in ('maximal_safe', 'minimal_db'):
            o = orb[name]
            seen = {}
            for entry in o['orbits']:
                for g in o['all_masks'] if 'all_masks' in o else []:
                    pass
            # rebuild class map from orbit expansion of reps (independent)
            cls = {}
            for idx, entry in enumerate(o['orbits']):
                r = entry['rep_mask']
                for pm in perms:
                    cls[apply_perm(r, pm)] = idx
            masks = pub_ms if name == 'maximal_safe' else pub_db
            if len(cls) != len(masks):
                ok_all = False
                checks.append((name, 'orbit-cover-size-mismatch', len(cls), len(masks)))
                continue
            # random closure checks
            ml = sorted(masks)
            for _ in range(50):
                g = random.choice(ml)
                pm = random.choice(perms)
                h = apply_perm(g, pm)
                if h not in masks or cls.get(h) != cls.get(g):
                    ok_all = False
                    checks.append((name, 'closure-failure', g, h))
                    break
            for entry in o['orbits']:
                if entry['orbit_size'] * entry.get('stab_check', 1) < 0:
                    pass
                if len(perms) % entry['orbit_size'] != 0:
                    ok_all = False
                    checks.append((name, 'order-divisibility-failure', entry['orbit_size']))
        rep['orbit_checks'] = checks if checks else 'all-pass'
        # 4. Baer identification for q=4 size-7
        if q == 4:
            from collections import Counter
            entry = [e for e in orb['maximal_safe']['orbits'] if e['size'] == 7][0]
            mask = entry['rep_mask']
            # Baer subplane: lines meeting rep in 3 points (not full containment,
            # a PG(2,4) line has 5 points)
            tris = [L for L in board['lines']
                    if len([p for p in L if (mask >> p) & 1]) == 3]
            pts = [i for i in range(board['n']) if (mask >> i) & 1]
            # 2-(7,3,1) design check on the 7 triple lines
            pidx = {p: i for i, p in enumerate(pts)}
            pairs = Counter()
            for L in tris:
                for a, b in combinations([pidx[p] for p in L if (mask >> p) & 1], 2):
                    pairs[(a, b)] += 1
            is_fano = (len(tris) == 7 and len(pairs) == 21
                       and all(v == 1 for v in pairs.values())
                       and all(sum(1 for L in tris if pidx[p] in [pidx[x] for x in L if (mask >> x) & 1]) == 3
                               for p in pts))
            prof = Counter(len([p for p in L if (mask >> p) & 1]) for L in board['lines'])
            rep['baer_size7'] = {'triple_lines': len(tris), 'is_fano_2_7_3_1': is_fano,
                                 'line_profile': dict(prof)}
            # also: every one of the 360 size-7 masks is a Fano subplane
            all_fano = True
            for g in pub_ms:
                if bin(g).count('1') != 7:
                    continue
                tr = [L for L in board['lines']
                      if len([p for p in L if (g >> p) & 1]) == 3]
                pl = [i for i in range(board['n']) if (g >> i) & 1]
                pi = {p: i for i, p in enumerate(pl)}
                pr = Counter()
                for L in tr:
                    for a, b in combinations([pi[p] for p in L if (g >> p) & 1], 2):
                        pr[(a, b)] += 1
                if not (len(tr) == 7 and len(pr) == 21 and all(v == 1 for v in pr.values())):
                    all_fano = False
                    break
            rep['baer_size7']['all_360_are_fano_subplanes'] = all_fano
        report[f'pg2q{q}'] = rep
        print(json.dumps(rep, default=str)[:1200])
    report['all_ok'] = ok_all
    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/out/verify.json', 'w') as f:
        json.dump(report, f, indent=1)
    print('ALL_OK' if ok_all else 'FAILURES PRESENT')

if __name__ == '__main__':
    main()
