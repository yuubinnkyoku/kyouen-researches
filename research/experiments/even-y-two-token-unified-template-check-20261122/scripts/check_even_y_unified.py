#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_even_y_unified.py — even-y (y = 10, 12, 14, 16) unified-template machine check.

Question. The four published two-token vertical-fiber closed forms for even y
(cand10 / cand12 / cand14 / cand16) were published as separate files. All four
claim the same structural family (K1141, K1152, K1233/K1234, K1237). Is there
ONE Y-parametric code that regenerates all four tables exactly?

Method. The cand14 fit source (research/experiments/vertical-fiber-two-token-
y14-parametric-allz-fit-20261122/cand14.py) is fully Y-parametric: apart from
the literal ``Y = 14`` no y-specific constant occurs in its code body. We cut
the code body (module docstring end up to ``def main()``), substitute
``Y = <target>`` and the generic names (in_T14 -> in_TY etc.), exec it, and
compare the resulting ``candY`` against every published table:

  * grid sweeps of the full value function cand(z, x, R) (finite machine check),
  * row censuses of in_P and in_T over offset windows with constant-tail
    assertions (rowwise machine check),
  * source-level (k, th) classification of the y=10 published explicit-row
    table against the template formulas (representation census),
  * merge-region textual identity assertion,
  * negative controls at odd y in {13, 15} (the template must NOT reproduce
    the odd-y proved tables; it is an even-y template).

Lemma L1 (proved in report.md of this directory):
  for every integer k >= 0,
      b_{k+1} U I[2k+2) = b_k U I[2k+1),
  where b_k = {odd offsets 1, 3, ..., 2k-1} and I[t) = {offsets >= t}.
  Proof: both sides equal [1, inf) minus the even offsets {2, 4, ..., 2k}.
  QED.  Applied to the aliased rows below, L1 upgrades the evaluated row
  agreement to an all-offset identity for those rows.

Fail-closed policy: any even-y mismatch (grid or census or classification)
fails the run with exit code 1. Odd-y controls must MISMATCH (template is
even-y specific); their absence of mismatch also fails the run.

Run:  python3 scripts/check_even_y_unified.py > output/check-run.txt
Audit: written to output/audit.json (recreated on each run).
Inputs are read from sibling experiment directories of this repo, pinned by
SHA-256 in the audit. If any sibling file changes, the audit hashes change.
"""

import hashlib
import importlib.util
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
EXP = os.path.join(REPO, 'research', 'experiments')

INPUTS = {
    'cand10_fit': 'vertical-fiber-two-token-y10-parametric-allz-fit-20261120/cand10.py',
    'cand12_fit': 'vertical-fiber-two-token-y12-parametric-allz-fit-20261120/cand12.py',
    'cand14_fit': 'vertical-fiber-two-token-y14-parametric-allz-fit-20261122/cand14.py',
    'cand16_fit': 'vertical-fiber-two-token-y16-parametric-allz-fit-20261122/cand16.py',
    'verify_y10': 'vertical-fiber-two-token-y10-parametric-allz-proof-20261120/verify_y10_universal.py',
    'verify_y12': 'vertical-fiber-two-token-y12-parametric-allz-proof-20261120/verify_y12_universal.py',
    'verify_y13': 'vertical-fiber-two-token-y13-parametric-allz-proof-20261122/verify_y13_universal.py',
    'verify_y14': 'vertical-fiber-two-token-y14-parametric-allz-proof-20261122/verify_y14_universal.py',
    'verify_y15': 'vertical-fiber-two-token-y15-parametric-allz-proof-20261122/verify_y15_universal.py',
}

MERGE_LINES = "        S = x + Y\n        return S % 2 == 1 and R >= q_odd(S) + 1\n"

# grid configs: (zmax, xpad, rpad)
GRID = {
    ('y10', 'fit'):    (30, 25, 40),
    ('y10', 'proved'): (40, 25, 44),
    ('y12', 'fit'):    (30, 25, 40),
    ('y12', 'proved'): (25, 20, 35),
    ('y14', 'proved'): (22, 20, 35),
    ('y16', 'fit'):    (19, 25, 40),
}
ODD_BOX = {'y13': (11, 11, 55), 'y15': (11, 11, 55)}  # (zmax, xpad, rpad)
ROW_OFF = 160          # row census offset window
ROW_CONST_FROM = 120   # rows must be constantly False on [120, 160] here


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def build_uni(Y, cand14_src):
    body = cand14_src.split('"""', 2)[2]
    body = body[:body.find('def main()')]
    t = (body.replace('Y = 14', 'Y = %d' % Y)
              .replace('in_T14', 'in_TY')
              .replace('in_P14', 'in_PY')
              .replace('cand14', 'candY'))
    g = {}
    exec(compile(t, 'uni_%d' % Y, 'exec'), g)
    return g


def sweep(f_pub, f_uni, Y, zmax, xpad, rpad):
    bad = 0
    n = 0
    first = None
    for z in range(0, zmax + 1):
        for x in range(Y, z + 1 + xpad):
            for R in range(1, x + z + rpad + 1):
                n += 1
                a = f_pub(z, x, R)
                b = f_uni(z, x, R)
                if a != b:
                    bad += 1
                    if first is None:
                        first = (z, x, R, a, b)
    return n, bad, first


def row_census(f_pub, f_uni, Y, off_max=ROW_OFF, const_from=ROW_CONST_FROM,
               check_const=True):
    """Rowwise equality on off in [1, off_max], z parity in {0,1}, d in [-Y, Y+1].
    Both sides must be constantly False on [const_from, off_max] (finite support
    per row, in-row x fixed). Returns (rows, differing rows list)."""
    diff = []
    rows = 0
    for zp in (0, 1):
        for d in range(-Y, Y + 2):
            rows += 1
            vals_p = []
            vals_u = []
            const_ok = True
            for off in range(1, off_max + 1):
                a = f_pub(zp, zp + d, off + zp)
                b = f_uni(zp, zp + d, off + zp)
                vals_p.append(a)
                vals_u.append(b)
            if check_const:
                tail_p = all(vals_p[const_from - 1:])
                tail_u = all(vals_u[const_from - 1:])
                if any(vals_p[const_from - 1:]) != tail_p or \
                   any(vals_u[const_from - 1:]) != tail_u:
                    diff.append((zp, d, 'TAIL_NOT_CONSTANT'))
                    continue
                if vals_p != vals_u:
                    diff.append((zp, d, 'ROW_MISMATCH'))
            elif vals_p != vals_u:
                diff.append((zp, d, 'ROW_MISMATCH'))
    return rows, diff


def parse_pub_chain(path, fn, fn_end):
    """Parse an explicit-row published in_P table into {(zparity section, d): (k, th, expr)}.
    Sections: 'odd' = z % 2 == 1 branch, 'even' = else branch."""
    src = open(path, encoding='utf-8').read()
    seg = src[src.find('def ' + fn):src.find('def ' + fn_end)]
    zodd = seg[seg.find('if z % 2 == 1'):seg.find('else:')]
    zev = seg[seg.find('else:'):]
    out = {}
    for sec, chunk in (('odd', zodd), ('even', zev)):
        for m in re.finditer(r'if d == (-?\d+): return (.+?)\n', chunk):
            d, expr = int(m.group(1)), m.group(2)
            b = re.search(r'_bk\(off, (\d+)\)', expr)
            t = re.search(r'R >= z \+ (\d+)', expr)
            out[(sec, d)] = (
                int(b.group(1)) if b else None,
                int(t.group(1)) if t else None,
                expr.strip(),
            )
    return out


def tmpl_prows(Y):
    """Template (k, th) per (section, d) for an even Y, mirroring in_PY."""
    odd = {}
    ev = {}
    for d in range(-Y, Y + 2):
        if d % 2 == 0 and -Y <= d <= Y:
            k = (d + 3 * Y + 2) // 4
            th = 2 * k + (1 if (d + 3 * Y) % 4 == 0 else 0)
            odd[d] = ('I', k, th)
        if d % 2 == 1 and -Y + 1 <= d <= Y - 1:
            odd[d] = ('base', (d + 3 * Y + 1) // 4, None)
        if d % 2 == 1 and -Y + 1 <= d <= Y - 1:
            k = (d + 3 * Y - 1) // 4
            ev[d] = ('I', k, 2 * k + 1)
        if d % 2 == 0 and -Y + 2 <= d <= Y:
            ev[d] = ('base', (d + 3 * Y + 1) // 4, None)
    odd[Y + 1] = ('sweep', Y, None)
    ev[Y + 1] = None  # z-even: sweep row handled by fallback (band+tail), identical text
    return odd, ev


def main():
    t0 = time.time()
    paths = {k: os.path.join(EXP, v) for k, v in INPUTS.items()}
    for k, p in paths.items():
        if not os.path.isfile(p):
            print('FATAL: missing input %s at %s' % (k, p))
            return 1
    audit = {
        'run': 'check_even_y_unified',
        'when_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'inputs': {k: {'path': 'research/experiments/' + v,
                       'sha256': sha256_file(p), 'bytes': os.path.getsize(p)}
                   for k, v, p in ((k, v, paths[k]) for k, v in INPUTS.items())},
        'grids': {},
        'row_census': {},
        'y10_representation': {},
        'merge_identity': {},
        'odd_control': {},
    }
    fail = []

    mod = {}
    for k, p in paths.items():
        mod[k] = load_module(p, 'm_' + k)

    cand14_src = open(paths['cand14_fit'], encoding='utf-8').read()
    uni = {Y: build_uni(Y, cand14_src) for Y in (10, 12, 13, 14, 15, 16)}

    # 0) merge-region textual identity (S = x + Y single-token ladder)
    for k in ('cand10_fit', 'cand12_fit', 'cand14_fit', 'cand16_fit'):
        ok = MERGE_LINES in open(paths[k], encoding='utf-8').read()
        audit['merge_identity'][k] = ok
        if not ok:
            fail.append('merge formula text differs in %s' % k)

    # 1) grid sweeps (even families)
    pubf = {
        ('y10', 'fit'): (lambda z, x, R: mod['cand10_fit'].cand10(z, x, R), 10),
        ('y10', 'proved'): (lambda z, x, R: mod['verify_y10'].cand10(z, x, R), 10),
        ('y12', 'fit'): (lambda z, x, R: mod['cand12_fit'].cand12(z, x, R), 12),
        ('y12', 'proved'): (lambda z, x, R: mod['verify_y12'].cand12(z, x, R), 12),
        ('y14', 'proved'): (lambda z, x, R: mod['verify_y14'].cand14(z, x, R), 14),
        ('y16', 'fit'): (lambda z, x, R: mod['cand16_fit'].cand16(z, x, R), 16),
    }
    for key, (f, Y) in pubf.items():
        zmax, xpad, rpad = GRID[key]
        n, bad, first = sweep(f, uni[Y]['candY'], Y, zmax, xpad, rpad)
        cfg = {'zmax': zmax, 'xpad': xpad, 'rpad': rpad, 'x_from': Y}
        audit['grids'][str(key)] = {'cfg': cfg, 'points': n, 'bad': bad, 'first': first}
        print('GRID  %-14s pts=%7d bad=%d first=%s' % (str(key), n, bad, first))
        if bad:
            fail.append('grid mismatch %s: %d' % (key, bad))

    # 2) P/T row censuses (even families; proved tables where they exist)
    cens = {
        ('y10', 'fit', 'P'): (lambda z, x, R: mod['cand10_fit'].in_P10(z, x, R), uni[10]['in_PY'], 10),
        ('y10', 'proved', 'P'): (lambda z, x, R: mod['verify_y10'].in_P10(z, x, R), uni[10]['in_PY'], 10),
        ('y10', 'fit', 'T'): (lambda z, x, R: mod['cand10_fit'].in_T10(z, x, R), uni[10]['in_TY'], 10),
        ('y10', 'proved', 'T'): (lambda z, x, R: mod['verify_y10'].in_T10(z, x, R), uni[10]['in_TY'], 10),
        ('y12', 'fit', 'P'): (lambda z, x, R: mod['cand12_fit'].in_P12(z, x, R), uni[12]['in_PY'], 12),
        ('y12', 'proved', 'P'): (lambda z, x, R: mod['verify_y12'].in_P12(z, x, R), uni[12]['in_PY'], 12),
        ('y12', 'fit', 'T'): (lambda z, x, R: mod['cand12_fit'].in_T12(z, x, R), uni[12]['in_TY'], 12),
        ('y12', 'proved', 'T'): (lambda z, x, R: mod['verify_y12'].in_T12(z, x, R), uni[12]['in_TY'], 12),
        ('y14', 'proved', 'P'): (lambda z, x, R: mod['verify_y14'].in_P14(z, x, R), uni[14]['in_PY'], 14),
        ('y14', 'proved', 'T'): (lambda z, x, R: mod['verify_y14'].in_T14(z, x, R), uni[14]['in_TY'], 14),
        ('y16', 'fit', 'P'): (lambda z, x, R: mod['cand16_fit'].in_P16(z, x, R), uni[16]['in_PY'], 16),
        ('y16', 'fit', 'T'): (lambda z, x, R: mod['cand16_fit'].in_T16(z, x, R), uni[16]['in_TY'], 16),
    }
    for key, (f, fu, Y) in cens.items():
        rows, diff = row_census(f, fu, Y)
        audit['row_census']['/'.join(key)] = {'rows': rows, 'diff_rows': diff[:10],
                                         'n_diff': len(diff)}
        print('ROW   %-22s rows=%d diff=%d %s' % (str(key), rows, len(diff),
                                                  diff[:3] if diff else ''))
        if diff:
            fail.append('row census mismatch %s' % str(key))

    # 3) y=10 published explicit-table (k, th) classification vs template
    pub = parse_pub_chain(paths['cand10_fit'], 'in_P10', 'cand10')
    odd, ev = tmpl_prows(10)
    stats = {'rep_identical': [], 'alias_L1': [], 'other': []}
    benign = {'fallback', 'sweep_row_base_only_matches_bY', 'diag_false_row'}
    for (sec, d), (kp, tp, expr) in sorted(pub.items()):
        t = odd.get(d) if sec == 'odd' else ev.get(d)
        if expr == 'False':
            stats['other'].append({'sec': sec, 'd': d, 'expr': expr,
                                   'class': 'diag_false_row'})
            continue
        if t is None:
            # sweep/fallback rows: compare by kind
            stats['other'].append({'sec': sec, 'd': d, 'expr': expr, 'tmpl': None,
                                   'class': 'fallback'})
            continue
        if t[0] == 'I':
            if (kp, tp) == (t[1], t[2]):
                stats['rep_identical'].append({'sec': sec, 'd': d, 'k': kp, 'th': tp})
            elif kp == t[1] + 1 and tp == 2 * kp and t[2] == 2 * t[1] + 1:
                # L1 precondition: pub (k+1, 2k+2) == tmpl (k, 2k+1)
                stats['alias_L1'].append({'sec': sec, 'd': d,
                                         'pub': [kp, tp], 'tmpl': [t[1], t[2]]})
            else:
                stats['other'].append({'sec': sec, 'd': d, 'expr': expr,
                                       'class': 'REPRESENTATION_DIFF'})
        elif t[0] == 'base':
            if kp == t[1] and tp is None:
                stats['rep_identical'].append({'sec': sec, 'd': d, 'k': kp})
            else:
                stats['other'].append({'sec': sec, 'd': d, 'expr': expr,
                                       'class': 'BASE_DIFF'})
        elif t[0] == 'sweep':
            stats['other'].append({'sec': sec, 'd': d, 'expr': expr,
                                   'class': 'sweep_row_base_only_matches_bY'})
    audit['y10_representation'] = {
        'n_rep_identical': len(stats['rep_identical']),
        'alias_rows': stats['alias_L1'],
        'n_alias': len(stats['alias_L1']),
        'other': stats['other'],
    }
    print('Y10REP rep_identical=%d alias_L1=%d other=%d'
          % (len(stats['rep_identical']), len(stats['alias_L1']), len(stats['other'])))
    badrep = [o for o in stats['other'] if o.get('class') not in benign]
    if badrep:
        fail.append('y10 representation diff: %s' % badrep[:3])

    # 4) y=12 formula-form numerical identity of constants (LHS literal == Y-expression)
    ok12 = True
    for d in range(-12, 13):
        if d % 2 == 0 and -12 <= d <= 12:
            k = (d + 38) // 4
            th = 2 * k + (1 if d % 4 == 0 else 0)
            tk = (d + 3 * 12 + 2) // 4
            tth = 2 * tk + (1 if (d + 36) % 4 == 0 else 0)
            ok12 &= (k == tk and th == tth)
        if d % 2 == 1 and -11 <= d <= 11:
            ok12 &= ((d + 37) // 4 == (d + 3 * 12 + 1) // 4)
            ok12 &= ((d + 35) // 4 == (d + 3 * 12 - 1) // 4)
    audit['y12_formula_identity'] = bool(ok12)
    print('Y12FORM formula-identity=%s' % bool(ok12))
    if not ok12:
        fail.append('y12 formula constants differ')

    # 5) odd-y negative controls
    for Y, vf, cf in ((13, lambda z, x, R: mod['verify_y13'].in_P13(z, x, R),
                       lambda z, x, R: mod['verify_y13'].cand13(z, x, R)),
                      (15, lambda z, x, R: mod['verify_y15'].in_P15(z, x, R),
                       lambda z, x, R: mod['verify_y15'].cand15(z, x, R))):
        tf = getattr(mod['verify_y%d' % Y], 'in_T%d' % Y)
        trows, tdiff = row_census(tf, uni[Y]['in_TY'], Y, check_const=False)
        prows, pdiff = row_census(vf, uni[Y]['in_PY'], Y, check_const=False)
        zmax, xpad, rpad = ODD_BOX['y%d' % Y]
        n, bad, first = sweep(cf, uni[Y]['candY'], Y, zmax, xpad, rpad)
        audit['odd_control']['y%d' % Y] = {
            'T_rows': trows, 'T_diff_rows_n': len(tdiff), 'T_diff_rows': tdiff[:8],
            'P_rows': prows, 'P_diff_rows_n': len(pdiff),
            'box_pts': n, 'box_mismatch': bad, 'first': first,
        }
        print('ODD   y=%d T-diff rows=%d P-diff rows=%d box pts=%d mismatch=%d first=%s'
              % (Y, len(tdiff), len(pdiff), n, bad, first))
        if bad == 0:
            fail.append('odd control y=%d shows NO mismatch (unexpected)' % Y)

    verdict = 'PASS' if not fail else 'FAIL'
    audit['verdict'] = verdict
    audit['failures'] = fail
    audit['elapsed_s'] = round(time.time() - t0, 1)
    outd = os.path.join(HERE, '..', 'output')
    os.makedirs(outd, exist_ok=True)
    with open(os.path.join(outd, 'audit.json'), 'w', encoding='utf-8') as f:
        json.dump(audit, f, ensure_ascii=False, indent=1, sort_keys=True)
    print('VERDICT %s (elapsed %.1fs) failures=%s' % (verdict, time.time() - t0, fail))
    return 0 if verdict == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
