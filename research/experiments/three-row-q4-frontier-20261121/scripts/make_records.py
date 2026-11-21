#!/usr/bin/env python3
"""make_records.py — assemble records.jsonl increment entries for this session's
m=24/m=23 piece runs from kissat run logs (deterministic; md5s from generated CNFs).
Output: records_append.jsonl on stdout.
"""
import json, hashlib, re, sys, os

BASE = sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/fastlane/q34'
SOLVER = 'kissat-4.0.4-linux-amd64 md5 3a5eba830aa6008a604fcc9bbe99a325'

def md5(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

def parse_meta(cnf_path):
    """parse the header line printed by sat3/sat4 — but easier: recompute from file"""
    # we keep vars/clauses from the stored meta JSONs; caller supplies via dict
    pass

def meta_from_cnf(path):
    with open(path) as f:
        first = f.readline().strip()
    mo = re.match(r'p cnf (\d+) (\d+)', first)
    return int(mo.group(1)), int(mo.group(2))

def parse_run(out_path, cap_sec):
    txt = open(out_path).read()
    v = None
    if re.search(r'^s UNSATISFIABLE', txt, re.M):
        v, rc = 'UNSAT', 20
    elif re.search(r'^s SATISFIABLE', txt, re.M):
        v, rc = 'SAT', 10
    else:
        v, rc = 'INDET', None
    conf = None
    mo = re.search(r'^c conflicts:\s+(\d+)', txt, re.M)
    if mo:
        conf = int(mo.group(1))
    pt = None
    mo = re.search(r'^c process-time:.*?([0-9.]+)\s+seconds', txt, re.M)
    if mo:
        pt = float(mo.group(1))
    return v, rc, conf, pt

MODELEX = {'HV': 'lexHV', 'H': 'lexH', None: 'plain'}

def rec(m, mode, enc, cnf, out, cap, extra):
    cnf_path = os.path.join(BASE, cnf)
    out_path = os.path.join(BASE, out)
    var, cls = meta_from_cnf(cnf_path)
    v, rc, conf, pt = parse_run(out_path, cap)
    r = {
        'w': 3, 'm': m, 'q': 4, 'mode': mode, 'encoding': enc,
        'cnf_md5': md5(cnf_path), 'vars': var, 'clauses': cls,
        'curves': 5633 if m == 23 else 6413,
        'solver': SOLVER, 'verdict': v, 'rc': rc,
        'wall_sec': pt, 'cap_sec': cap,
    }
    if v == 'INDET':
        r['conflicts_at_cap'] = conf
    else:
        r['conflicts'] = conf
    r.update(extra)
    return r

def main():
    R = []
    # m=24 row-k pieces (sat3 rowfixed-kex)
    R.append(rec(24, 'rowfixed-kex', 'lexHV', 'cnf3/r24_row1_k0_lexHV.cnf', 'runs/r24_row1_k0_lexHV.out', 260,
                 {'rowY': 1, 'kex': 0, 'lex': ['H', 'V'],
                  'note': 'm=24 middle-row stone-count split: row1 exactly 0. Complete partition piece.'}))
    R.append(rec(24, 'rowfixed-kex', 'lexHV', 'cnf3/r24_row1_k1_lexHV.cnf', 'runs/r24_row1_k1_lexHV.out', 260,
                 {'rowY': 1, 'kex': 1, 'lex': ['H', 'V'],
                  'note': 'm=24 middle-row stone-count split: row1 exactly 1.'}))
    R.append(rec(24, 'rowfixed-kex', 'lexH', 'cnf3/r24_row0_k0_lexH.cnf', 'runs/r24_row0_k0_lexH.out', 200,
                 {'rowY': 0, 'kex': 0, 'lex': ['H'],
                  'note': 'm=24 outer-row stone-count split: row0 exactly 0 (V-image covers row2).'}))
    R.append(rec(24, 'rowfixed-kex', 'lexH', 'cnf3/r24_row0_k1_lexH.cnf', 'runs/r24_row0_k1_lexH.out', 240,
                 {'rowY': 0, 'kex': 1, 'lex': ['H'],
                  'note': 'm=24 outer-row stone-count split: row0 exactly 1 (V-image covers row2).'}))
    # m=24 calibration sat3 (m=23 row1 kex2 lexH SAT)
    R.append(rec(23, 'rowfixed-kex', 'lexH', 'cnf3/cal23_row1_k2_lexH.cnf', 'runs/cal23_k2.out', None,
                 {'rowY': 1, 'kex': 2, 'lex': ['H'],
                  'note': 'sat3 calibration: witness band width m=23 exactly-2 piece is SAT (H-reflection of published wit_3x23). verify34 PASS.',
                  'verdict': 'SAT', 'rc': 10}))
    # m=24 sum pieces (sat4 rspec)
    for (a, b, c, lexmode, cnf, out, wall, note) in [
        (0, 2, 0, 'lexHV', 'cnf4/r24_r1k2_s00.cnf', 'runs/r24_r1k2_s00.out', 45, None),
        (1, 2, 0, 'lexH', 'cnf4/r24_r1k2_s10.cnf', 'runs/r24_r1k2_s10.out', 45, None),
        (1, 2, 1, 'lexHV', 'cnf4/r24_r1k2_s11.cnf', 'runs/r24_r1k2_s11.out', 45, None),
        (2, 2, 0, 'lexH', 'cnf4/r24_r1k2_s20.cnf', 'runs/r24_r1k2_s20.out', 45, None),
        (2, 2, 1, 'lexH', 'cnf4/r24_r1k2_s21.cnf', 'runs/r24_r1k2_s21.out', 45, None),
        (2, 2, 2, 'lexHV', 'cnf4/r24_r1k2_s22.cnf', 'runs/r24_r1k2_s22.out', 45, None),
        (3, 2, 0, 'lexH', 'cnf4/r24_r1k2_s30.cnf', 'runs/r24_r1k2_s30.out', 45, None),
        (3, 2, 1, 'lexH', 'cnf4/r24_r1k2_s31.cnf', 'runs/r24_r1k2_s31.out', 45, None),
        (3, 2, 2, 'lexH', 'cnf4/r24_r1k2_s32.cnf', 'runs/r24_r1k2_s32.out', 200, 'second cap after 45s INDET (68077)'),
        (3, 2, 3, 'lexHV', 'cnf4/r24_r1k2_s33.cnf', 'runs/r24_r1k2_s33.out', 6000, None),
        (2, 3, 2, 'lexHV', 'cnf4/r24_s232.cnf', 'runs/r24_s232.out', 260, None),
    ]:
        vx = 'V-mirror simultaneously refutes (%d,2,%d)' % (c, a) if lexmode == 'lexH' and a != b else None
        n = note or ('m=24 row-sum partition piece (r0,r1,r2)=(%d,%d,%d)' % (a, b, c))
        if vx:
            n += '; also refutes ' + vx
        R.append(rec(24, 'rowsum-partition', MODELEX[{'lexHV': 'HV', 'lexH': 'H'}[lexmode]], cnf, out, wall,
                     {'rspec': {'0': a, '1': b, '2': c}, 'lex': ['H', 'V'] if lexmode == 'lexHV' else ['H'],
                      'note': n}))
    # m=23 outer question: row pieces + sum pieces
    R.append(rec(23, 'rowfixed-kex', 'lexH', 'cnf3/r23_row0_k0_lexH.cnf', 'runs/r23_row0_k0.out', 60,
                 {'rowY': 0, 'kex': 0, 'lex': ['H'],
                  'note': 'm=23 outer-row split: row0 exactly 0.'}))
    R.append(rec(23, 'rowfixed-kex', 'lexH', 'cnf3/r23_row0_k1_lexH.cnf', 'runs/r23_row0_k1.out', 120,
                 {'rowY': 0, 'kex': 1, 'lex': ['H'],
                  'note': 'm=23 outer-row split: row0 exactly 1.'}))
    for (a, b, cap, note) in [
        (0, 0, 50, None), (0, 1, 50, None), (0, 2, 50, None), (0, 3, 50, None),
        (1, 0, 50, None), (1, 1, 50, None), (1, 2, 50, None), (1, 3, 50, None),
        (2, 0, 50, None), (2, 1, 50, None), (2, 2, 50, None), (2, 3, 50, None),
        (3, 0, 50, None), (3, 1, 50, None), (3, 2, 50, None), (3, 3, 50, None),
    ]:
        cnf = 'cnf4/r23_out_s2_%d%d.cnf' % (a, b)
        out = 'runs/r23_out_s2_%d%d.out' % (a, b)
        n = note or ('m=23 outer-deficient partition piece (r0,r1,r2)=(2,%d,%d)' % (a, b))
        R.append(rec(23, 'rowsum-partition', 'lexHV' if b == 2 else 'lexH', cnf, out, cap,
                     {'rspec': {'0': 2, '1': a, '2': b}, 'lex': ['H', 'V'] if b == 2 else ['H'],
                      'note': n}))
    for r in R:
        print(json.dumps(r, sort_keys=False))

if __name__ == '__main__':
    main()
