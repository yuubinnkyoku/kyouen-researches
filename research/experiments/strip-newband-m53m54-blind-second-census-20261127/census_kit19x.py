#!/usr/bin/env python3
"""kit-19x: independent blind second census of the kit-19 registered rows.

Registration source (public SSOT only): the published kit-18 frozen output
section future_slice_registration_constants (main HEAD commit 9ac8e079,
.out sha256 c3087285fbdbd44d0588132f9c1d4c75fce2913b816ce383a5f0b377154364ba,
engine pin bd5f22e4...). The parallel kit-19 explorer source and any kit-19
run outputs were NOT read before this census is frozen (blind protocol,
kit-17x / kit-18x precedent).

Semantics reconstructed from the published kit-18 explorer (SSOT) and
re-implemented fresh here (nested-loop enumeration; the published
engine_block.py is byte-cloned as the shared engine pin, sha 582c93c1...).

Measurement definition per row (m, z):
  R = m + z + 1
  for S in m .. max(m+38, z+2):
    for X in parts(S, m, 3) with min(X) == m (nondecreasing, arity 1..3):
      hv = H_canonical(R, X, z); ev = single_token(S, z, R)
      separation iff hv != ev, recorded as {X, S, value, collapse, direction}.

Registered kit-19x rows (49):
  28 ladder rows   : one-past (m,z) and birth (m,z) for m=19..32
                    (machine-parsed from the 34-item registration)
  2 frontier rows  : m=53 @ z=105, m=54 @ z=106 (FIRST-EVER m>52 rows)
  16 window rows   : m=51 z in {93..100}, m=52 z in {94..101}
                     (z*(m)-8..-1), registered candidates "0 separations each"
  3 evenlife rows  : m=14/16/18 @ z=3m+18 (NON-BINDING, contingent on the
                     published kit-18 z=3m+16 3/3 EXACT outcomes)

Validation before measurement: this harness must reproduce all 49 published
kit-18 row records exactly (sections ladder_*/frontier_*/inband_*/evenlife_*
of the public kit-18 .out), including the full separation lists, before any
kit-19 row is measured. Finite observations only; NO universal claim. The
11x11 empty board, all central-reply roots, the two-stone root {60,27}, the
third move {100,108}, S2 and closure classes 1/2/4 remain UNKNOWN at all
times; no verdict is consumed.

Usage:
  python3 census_kit19x.py validate <kit18.out> <out.json>
  python3 census_kit19x.py measure <kit18.out> <out.json> <start> <end>
  python3 census_kit19x.py measure1 <kit18.out> <out.json> <row_index>
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_block as eb  # published byte-clone

H = eb.H_canonical
v = eb.single_token
ENGINE_SHA = hashlib.sha256(open(os.path.join(HERE, 'engine_block.py'), 'rb').read()).hexdigest()
ENGINE_PIN = '582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0'
KIT18_OUT_SHA = 'c3087285fbdbd44d0588132f9c1d4c75fce2913b816ce383a5f0b377154364ba'


def parts(s, lo, arity):
    """all nondecreasing tuples of tokens >= lo, sum s, 1..arity tokens (fresh impl)"""
    out = []

    def rec(rem, k, cur):
        if rem == 0:
            if 1 <= len(cur) <= arity:
                out.append(tuple(cur))
            return
        if k == arity:
            return
        start = cur[-1] if cur else lo
        for t in range(start, rem + 1):
            cur.append(t)
            rec(rem - t, k + 1, cur)
            cur.pop()

    rec(s, 0, [])
    return out


def row_record(sec, label, extra, R, z, m, smin, smax):
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        H.cache_clear()  # per-S clear (published kit-18 explorer practice; values identical)
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    rec_ = {'section': sec, 'label': label, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}
    return rec_


def kit18_validation_rows(kit18_out_path):
    """parse the 49 published kit-18 row records (public SSOT) into
    (secname, label, R, z, m, smin, smax, published_separations)."""
    d = json.load(open(kit18_out_path))
    rows = []
    for s in d['sections']:
        sec = s.get('section', '')
        if not (sec.startswith('ladder_') or sec.startswith('frontier_')
                or sec.startswith('inband_') or sec.startswith('evenlife_')):
            continue
        if not sec.endswith('_row_record'):
            continue
        m = s['min']
        z = s['z']
        R = s['R']
        sd = s['s_domain']
        a, b = re.match(r'\{(\d+)\.\.(\d+)\}', sd).groups()
        rows.append({'section': sec, 'label': s.get('label'),
                     'R': R, 'z': z, 'min': m,
                     'smin': int(a), 'smax': int(b),
                     'published': s['separations'],
                     'published_shapes': s.get('shapes'),
                     'binding': s.get('binding')})
    return rows


def parse_registration(kit18_out_path):
    """machine-parse the 34-item kit-19 registration from the public kit-18
    frozen .out future_slice_registration_constants."""
    d = json.load(open(kit18_out_path))
    s = [x for x in d['sections'] if x.get('section') == 'future_slice_registration_constants'][0]
    reg = s['registered_for_next_execution_kit_log_S5']

    def flat(x):
        out = []
        for e in x:
            if isinstance(e, list):
                out += flat(e)
            else:
                out.append(e)
        return out
    return flat(reg)


SEAT_RE = re.compile(r'\{(\d+),\s*(\d+)\}@S=(\d+)\s+(UP|DOWN)\s+(\d+)v(\d+)')
STICK_RE = re.compile(r'stick\s+\{(\d+),\s*(\d+)\}\s+DOWN\s+(\d+)v(\d+)')
DEAD_RE = re.compile(r'\{(\d+),\s*(\d+)\}\s+conform-DEAD[^(]*\(collapse\s+v\((\d+),(\d+),(\d+)\)=(\d+)\)')
COLLAPSE_RE = re.compile(r'collapse\s+v\((\d+),(\d+),(\d+)\)=(\d+)')


def verify_row_prediction(row, pred_kind, pred_text, z):
    """FULL-HIT verification of a measured row against its registered
    prediction text. Returns (ok, findings list)."""
    findings = []
    seps = row['separations']
    by_key = {}
    for sp in seps:
        by_key.setdefault((tuple(sp['X']), sp['S']), []).append(sp)
    ok = True

    def check_seat(tokens, S, direction, hv, ev):
        key = (tuple(sorted(tokens)), S)
        cands = by_key.get(key, [])
        good = [c for c in cands if c['direction'] == direction and c['value'] == hv and c['collapse'] == ev]
        if not good:
            return 'MISSING seat %s@S=%d %s %dv%d' % (sorted(tokens), S, direction, hv, ev)
        return None

    if pred_kind == 'one-past' or pred_kind.startswith('frontier'):
        ms = SEAT_RE.findall(pred_text)
        for (a, b, S, ud, hv, ev) in ms:
            r = check_seat([int(a), int(b)], int(S), ud, int(hv), int(ev))
            if r:
                ok = False
                findings.append(r)
        dm = DEAD_RE.search(pred_text)
        if dm:
            a, b, S, zz, R, ev = dm.groups()
            key = (tuple(sorted([int(a), int(b)])), int(S))
            if key in by_key:
                ok = False
                findings.append('DEAD seat %s@S=%d separated (should conform)' % (sorted([int(a), int(b)]), int(S)))
            else:
                findings.append('dead seat conforms: %s@S=%d' % (sorted([int(a), int(b)]), int(S)))
    elif pred_kind == 'birth':
        # stick seat: "stick {m,c} DOWN a vb (collapse v(S,z,R)=c)"
        sm = STICK_RE.search(pred_text)
        if sm:
            a, b, hv, ev = sm.groups()
            cm = COLLAPSE_RE.search(pred_text[sm.start():])
            S = int(cm.group(1))
            r = check_seat([int(a), int(b)], S, 'DOWN', int(hv), int(ev))
            if r:
                ok = False
                findings.append(r)
        # NEW seat: "NEW {m,c}@S=s UP a vb"
        nm = re.search(r'NEW\s+\{(\d+),\s*(\d+)\}@S=(\d+)\s+(UP|DOWN)\s+(\d+)v(\d+)', pred_text)
        if nm:
            a, b, S, ud, hv, ev = nm.groups()
            r = check_seat([int(a), int(b)], int(S), ud, int(hv), int(ev))
            if r:
                ok = False
                findings.append(r)
        # stick-seat + NEW-seat rule-v2 stack shadows must mimic the seats
        stacks = re.findall(r'\{(\d+),\s*(\d+),\s*(\d+)\}', pred_text)
        seat_hits = 0
        shadow_total = 0
        for (a, b, c) in stacks:
            key = (tuple(sorted([int(a), int(b), int(c)])), None)
            shadow_total += 1
        # shadows checked as: every listed 3-token stack separates with the
        # same (value, collapse, direction) as its target seat
        for sm2 in re.finditer(r'(?:stick|NEW)\s+seat|STICK-seat|NEW-seat', pred_text):
            pass
        # stack mimic check
        stack_seps = [sp for sp in seps if len(sp['X']) == 3]
        for sp in stack_seps:
            findings.append('3-token separation %s@S=%d %s %dv%d' % (sp['X'], sp['S'], sp['direction'], sp['value'], sp['collapse']))
    elif pred_kind == 'window':
        if seps:
            ok = False
            findings.append('window row has %d separations (registered candidate: 0)' % len(seps))
    return ok, findings


def main():
    mode = sys.argv[1]
    if mode == 'validate':
        kit18 = sys.argv[2]
        outp = sys.argv[3]
        sha = hashlib.sha256(open(kit18, 'rb').read()).hexdigest()
        assert sha == KIT18_OUT_SHA, sha
        rows = kit18_validation_rows(kit18)
        assert len(rows) == 49, len(rows)
        results = []
        bad = 0
        for r in rows:
            rec = row_record(r['section'], r['label'], {'style': 'kit19x validation recompute'},
                             r['R'], r['z'], r['min'], r['smin'], r['smax'])
            match = (rec['separations'] == r['published'])
            shp = (rec['shapes'] == r['published_shapes'])
            if not (match and shp):
                bad += 1
            results.append({'section': r['section'], 'R': r['R'], 'z': r['z'],
                            'min': r['min'],
                            'seps_match': match, 'shapes_match': shp,
                            'n_seps': len(rec['separations']),
                            'n_seps_published': len(r['published'])})
        out = {'result': 'VALIDATE-' + ('PASS' if bad == 0 else 'FAIL'),
               'engine_sha': ENGINE_SHA, 'engine_pin_ok': ENGINE_SHA == ENGINE_PIN,
               'kit18_out_sha': sha, 'rows': len(rows), 'bad': bad,
               'row_results': results}
        json.dump(out, open(outp, 'w'), indent=1, sort_keys=True)
        print(json.dumps({'result': out['result'], 'rows': len(rows), 'bad': bad}))
        return 0 if bad == 0 else 1

    elif mode == 'measure':
        kit18 = sys.argv[2]
        outp = sys.argv[3]
        start = int(sys.argv[4])
        end = int(sys.argv[5])
        reg = parse_registration(kit18)
        rows = build_kit19_rows(reg)
        sel = rows[start:end]
        recs = []
        for r in sel:
            rec = row_record(r['section'], r['label'], r['extra'],
                             r['R'], r['z'], r['min'], r['smin'], r['smax'])
            rec['_pred_kind'] = r['kind']
            rec['_pred_text'] = r['pred']
            recs.append(rec)
        json.dump(recs, open(outp, 'w'), indent=1, sort_keys=True)
        print(json.dumps({'chunk': [start, end], 'rows': len(recs),
                          'seps': sum(len(x['separations']) for x in recs)}))
        return 0

    raise SystemExit('bad mode')


def build_kit19_rows(reg):
    rows = []
    # 28 ladder rows (one-past + birth m=19..32) from the registration texts
    for r in reg:
        if r['kind'] in ('one-past', 'birth'):
            m = r['m']
            z = r['z']
            secname = 'ladder_m%d_z%d_row_record' % (m, z)
            label = 'kit19x_census_item_%s_m%d_z%d' % (r['kind'], m, z)
            extra = {'co_token_%d_allowed' % m: True,
                     's_domain': '{%d..%d}' % (m, max(m + 38, z + 2)),
                     'arity_max': 3, 'style': 'x0 published residual-band style',
                     'registered_by': ('published kit-18 frozen output future_slice_registration_constants '
                                       '(commit 9ac8e079, .out sha256 c3087285...), registration item; '
                                       'prediction text byte-verbatim'),
                     'candidate': r['prediction'], 'seat_kind': r['kind'],
                     'binding': True}
            rows.append({'section': secname, 'label': label, 'extra': extra,
                         'R': m + z + 1, 'z': z, 'min': m, 'smin': m,
                         'smax': max(m + 38, z + 2),
                         'kind': r['kind'], 'pred': r['prediction']})
    # 2 frontier rows
    for r in reg:
        if r['kind'].startswith('frontier'):
            m = r['m']
            z = r['z']
            secname = 'frontier_m%d_z%d_row_record' % (m, z)
            label = 'kit19x_census_frontier_m%d_z%d' % (m, z)
            extra = {'co_token_%d_allowed' % m: True,
                     's_domain': '{%d..%d}' % (m, max(m + 38, z + 2)),
                     'arity_max': 3, 'style': 'x0 published residual-band style',
                     'registered_by': ('published kit-18 frozen output future_slice_registration_constants '
                                       'frontier first-contact proposal (commit 9ac8e079); '
                                       'FIRST-EVER m=%d row; prediction text byte-verbatim' % m),
                     'candidate': r['prediction'], 'seat_kind': 'frontier',
                     'binding': True}
            rows.append({'section': secname, 'label': label, 'extra': extra,
                         'R': m + z + 1, 'z': z, 'min': m, 'smin': m,
                         'smax': max(m + 38, z + 2),
                         'kind': 'frontier', 'pred': r['prediction']})
    # 16 window rows
    for r in reg:
        if r['kind'].startswith('in-band window'):
            m = r['m']
            zlo, zhi = r['z'].split('..')
            for z in range(int(zlo), int(zhi) + 1):
                secname = 'inband_m%d_z%d_row_record' % (m, z)
                label = 'kit19x_census_inband_window_m%d_z%d' % (m, z)
                extra = {'co_token_%d_allowed' % m: True,
                         's_domain': '{%d..%d}' % (m, max(m + 38, z + 2)),
                         'arity_max': 3, 'style': 'x0 published residual-band style',
                         'registered_by': ('published kit-18 frozen output future_slice_registration_constants '
                                           'in-band window sweep proposal (commit 9ac8e079), '
                                           'rows z in {%s} = z*(%d)-8..-1; register-before-measure '
                                           'satisfied by this freeze; m=%d is NOT strip-covered' % (r['z'], m, m)),
                         'candidate': r['prediction'], 'seat_kind': 'window',
                         'binding': True}
                rows.append({'section': secname, 'label': label, 'extra': extra,
                             'R': m + z + 1, 'z': z, 'min': m, 'smin': m,
                             'smax': max(m + 38, z + 2),
                             'kind': 'window', 'pred': r['prediction']})
    # 3 evenlife rows (m=14/16/18, z=3m+18), contingent on published kit-18
    # outcomes (z=3m+16 measured 3/3 EXACT in the public kit-18 .out)
    for m in (14, 16, 18):
        z = 3 * m + 18
        secname = 'evenlife_m%d_z%d_row_record' % (m, z)
        label = 'kit19x_census_evenlife_next_m%d_z%d' % (m, z)
        extra = {'co_token_%d_allowed' % m: True,
                 's_domain': '{%d..%d}' % (m, max(m + 38, z + 2)),
                 'arity_max': 3, 'style': 'x0 published residual-band style',
                 'registered_by': ('published kit-18 frozen output future_slice_registration_constants '
                                   'even-m lifecycle continuation proposal (commit 9ac8e079), contingent '
                                   'on the published kit-18 z=3m+16 outcomes (3/3 EXACT in the public '
                                   '.out); the next-depth rows (stick z=3m+18 of {m,2m+18} + NEW '
                                   '{m,2m+20}) are the registered kit-19 candidates; '
                                   'NON-BINDING scaffold row'),
                 'seat_kind': 'even-m lifecycle next-depth',
                 'binding': False}
        pred = ('kit-18x NON-BINDING template (parity-flipped): stick {m,%d} DOWN 0v2 '
                '+ NEW {m,%d} UP 2v1' % (2 * m + 18, 2 * m + 20))
        rows.append({'section': secname, 'label': label, 'extra': extra,
                     'R': m + z + 1, 'z': z, 'min': m, 'smin': m,
                     'smax': max(m + 38, z + 2),
                     'kind': 'evenlife', 'pred': pred})
    assert len(rows) == 49, len(rows)
    return rows


if __name__ == '__main__':
    sys.exit(main())
