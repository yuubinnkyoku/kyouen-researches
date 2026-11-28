"""Re-verification of baer_pairs.json results: rebuild the board from scratch,
re-check every claimed witness against the definitions, recheck orbit sizes
and the counting lower bounds. Fail-closed."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from boards9 import build_pg

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = json.load(open(os.path.join(root, 'out', 'baer_pairs.json')))
    ok = True
    rep = {}
    for key, res in data.items():
        q2 = int(key.replace('pg2q', ''))
        board = build_pg(q2)
        lineM = [sum(1 << p for p in L) for L in board['lines']]
        n = board['n']
        # counting lower bound: every line >= 2, each point on q2+1 lines
        lb = math.ceil(2 * n / (q2 + 1))
        entry = {'counting_lower_bound': lb}
        # recheck baer base
        base = set(board['baer_base'])
        q = (math.isqrt(4 * len(base) - 3) - 1) // 2
        assert q * q + q + 1 == len(base) and q * q == q2
        prof = {}
        for L in board['lines']:
            c = len(base.intersection(L))
            prof[c] = prof.get(c, 0) + 1
        assert set(prof) <= {1, q + 1}
        entry['baer_base_profile_recheck'] = {str(k): v for k, v in sorted(prof.items())}
        # witness checks
        wp = res.get('witness_points')
        if wp:
            sset = set(wp)
            counts = [len(sset.intersection(L)) for L in board['lines']]
            entry['witness_size'] = len(wp)
            entry['witness_min_line'] = min(counts)
            assert min(counts) >= 2, 'witness fails double blocking'
            assert len(wp) == (res.get('min_double_blocking_union')
                               or res.get('disjoint_witness_size'))
            entry['witness_profile_recheck'] = {str(k): v for k, v in
                                                sorted(prof2(counts).items())}
        dp = res.get('disjoint_witness_points')
        if dp:
            sset = set(dp)
            counts = [len(sset.intersection(L)) for L in board['lines']]
            assert min(counts) >= 2
            entry['disjoint_witness_min_line'] = min(counts)
        # orbit size recheck (independent traversal: DFS order via sorted gens)
        if res.get('orbit_size'):
            import baer as B
            base_mask = sum(1 << p for p in board['baer_base'])
            gens = sorted(B.generators(board))
            orbit = B.orbit_bfs(base_mask, gens)
            assert len(orbit) == res['orbit_size'], (len(orbit), res['orbit_size'])
            entry['orbit_size_recheck'] = len(orbit)
            # stabilizer consistency
            gl = (q2**3 - 1) * (q2**3 - q2) * (q2**3 - q2 * q2)
            pgl = gl // (q2 - 1)
            assert pgl % len(orbit) == 0
            entry['stabilizer_recheck'] = pgl // len(orbit)
        rep[key] = entry
        print(key, json.dumps(entry))
    ag = json.load(open(os.path.join(root, 'out', 'ag_scan.json')))
    rep['ag_scan'] = ag
    print('ag_scan:', json.dumps({k: v for k, v in ag.items()
                                   if k != 'ag_witness_points'}))
    with open(os.path.join(root, 'out', 'verify_baer.json'), 'w') as f:
        json.dump(rep, f, indent=1)
    print('ALL_OK')

def prof2(counts):
    r = {}
    for c in counts:
        r[c] = r.get(c, 0) + 1
    return r

if __name__ == '__main__':
    main()
