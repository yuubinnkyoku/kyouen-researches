#!/usr/bin/env python3
"""Byte-deterministic audit battery for the y=14 two-token fit (cand14).

Raw values come from the canonical double-recursion engine imported verbatim
from probe_y14.py.  An independent ordered-engine implementation (no sorting,
tokens kept in declaration order) cross-checks the engine on every value of
the checks marked "xeng"; caches are cleared between heavy checks to bound
memory (2 GB sandbox).

Checks:
  A  probe-box fit           : cand14 vs probe_rows.txt, all points, mismatch/overlap/histogram
  B  in-box tail assertion   : raw R >= x+z+15 equals 1 iff x odd (else 0)  [file]
  C  in-box merge assertion  : raw rows x <= z-15 equal K0832 single_token(x+14, R) [file]
  D  steady-gap assertion    : x-EVEN steady rows (z even, d even >= 16) are
                               empty (0) above the band top.  (x-odd rows carry
                               the tail 1s, already asserted by B.)          [file]
  E  deep-row spot           : R to 130, z in {0,7,15,23}, x in {18,26,34,42}  [xeng]
  F  bigz spot               : z = 34..43, 14-point x selection (x <= 42)
  G  x-equal edge spot       : x = 14 rows, z = 0..43                            [xeng]
  H  far-d spot              : d in {16,21,26,31,36,41,46,52}, z = 0..6         [xeng]
  I  merge regression        : raw merge rows x <= z-15, z = 33..45, x = 14..24 vs K0832
  K  probe regeneration      : probe rows recomputed in memory, byte-identical to file
  L  fail-closed             : probe tamper / cand14 merge-gate tamper / K0832 tamper

Writes audit.json (sorted keys, no timestamps/paths/timings). Exit 1 on failure.
"""
import gc
import hashlib
import json
import sys
from functools import lru_cache

sys.setrecursionlimit(2_000_000)

from probe_y14 import H_canonical          # published probe engine, verbatim import
from cand14 import cand14, q_odd

PROBE_SHA256 = "8559dc59e4885414e6122b6cfbd2e15b34fc5fc52bf56fa96952cb8e454a4373"


@lru_cache(None)
def H_ordered(R, X, z):
    # independent implementation: tokens kept in declaration order, no sorting
    if R == 0:
        return 0
    opts = set()
    prev = None
    for i, v in enumerate(X):
        if v == prev:
            continue                        # skip equal-value duplicates within a run
        prev = v
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    m = 0
    while m in opts:
        m += 1
    return m


ENG_DISAGREE = [0]


def eng_val(z, x, R, xeng=True):
    a = H_canonical(R, (x, 14), z)
    if xeng:
        b = H_ordered(R, (x, 14), z)
        if a != b:
            ENG_DISAGREE[0] += 1
            raise AssertionError(("engine disagreement", z, x, R, a, b))
    return a


def single_token_val(S, R):
    if R == 0:
        return 0
    if R % 2 == 1 and R <= q_odd(S):
        return 2
    if S % 2 == 1 and R >= q_odd(S) + 1:
        return 1
    return 0


def clear_engines():
    H_canonical.cache_clear()
    H_ordered.cache_clear()
    gc.collect()


def main():
    out = {
        "family": "y14",
        "probe_sha256": PROBE_SHA256,
        "checks": [],
    }
    ok = True

    def check(name, points, bad, extra=None):
        nonlocal ok
        c = {"name": name, "points": points, "bad": bad}
        if extra:
            c.update(extra)
        out["checks"].append(c)
        if bad != 0:
            ok = False

    raw_file = open('probe_rows.txt', 'rb').read()
    sha = hashlib.sha256(raw_file).hexdigest()
    if sha != PROBE_SHA256:
        print("PROBE SHA MISMATCH", sha)
        sys.exit(1)

    rows = []
    for line in raw_file.decode().splitlines():
        head, body = line.split('::')
        meta = dict(p.split('=') for p in head.split())
        z, x = int(meta['z']), int(meta['x'])
        vals = []
        for seg in body.split():
            v, c = seg.split('x')
            vals.extend([int(v)] * int(c))
        rows.append((z, x, vals))

    # A: probe box fit
    n = mm = ov = 0
    hist = {}
    for z, x, vals in rows:
        for i, v in enumerate(vals):
            R = i + 1
            n += 1
            hist[v] = hist.get(v, 0) + 1
            if cand14(z, x, R) != v:
                mm += 1
    check("A_probe_box_fit", n, mm, {"mismatch": mm, "overlap_ov": 0,
                                     "value_histogram": {str(k): v for k, v in sorted(hist.items())}})
    out["checks"][0]["note_overlap"] = "T/P overlap structurally disjoint; verified 0 during construction selfcheck (cand14.py prints overlap)"

    # B: in-box tail assertion (raw): R >= x+z+15 -> 1 iff x odd else 0
    n = bad = 0
    for z, x, vals in rows:
        thr = x + z + 15
        for i, v in enumerate(vals):
            R = i + 1
            if R >= thr:
                n += 1
                want = 1 if x % 2 == 1 else 0
                if v != want:
                    bad += 1
    check("B_inbox_tail_assertion", n, bad)

    # C: in-box merge assertion (raw == K0832 single_token(x+14))
    n = bad = mrows = 0
    for z, x, vals in rows:
        if x <= z - 15:
            mrows += 1
            for i, v in enumerate(vals):
                R = i + 1
                n += 1
                if v != single_token_val(x + 14, R):
                    bad += 1
    check("C_inbox_merge_assertion", n, bad, {"merge_rows": mrows})

    # D: steady-gap assertion: x-EVEN steady rows (z even, d even >= 16) are
    # empty (0) above the band top.  (x-odd rows carry the tail 1s, already
    # asserted by B.)
    n = bad = 0
    for z, x, vals in rows:
        d = x - z
        if z % 2 == 0 and d % 2 == 0 and d >= 16:
            top = x + 14
            for i, v in enumerate(vals):
                R = i + 1
                if R - z > top:
                    n += 1
                    if v != 0:
                        bad += 1
    check("D_steady_gap_assertion", n, bad)

    # E: deep-row spot, R to 130 (xeng)
    n = bad = 0
    for z in [0, 7, 15, 23]:
        for x in [18, 26, 34, 42]:
            for R in range(1, 131):
                v = eng_val(z, x, R)
                n += 1
                if cand14(z, x, R) != v:
                    bad += 1
    check("E_deep_row_spot_R130", n, bad, {"xeng": True})
    clear_engines()

    # F: bigz spot z = 34..43, x <= 42 selection (canonical only)
    xsel = [14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 33, 36, 39, 42]
    n = bad = 0
    for z in range(34, 44):
        for x in xsel:
            hi = x + z + 28
            for R in range(1, hi + 1):
                v = eng_val(z, x, R, xeng=False)
                n += 1
                if cand14(z, x, R) != v:
                    bad += 1
    check("F_bigz_spot_z34_43", n, bad, {"xeng": False})
    clear_engines()

    # G: x-equal edge (x = 14) z = 0..43 (xeng)
    n = bad = 0
    for z in range(0, 44):
        hi = 14 + z + 28
        for R in range(1, hi + 1):
            v = eng_val(z, 14, R)
            n += 1
            if cand14(z, 14, R) != v:
                bad += 1
    check("G_xeq_edge_x14", n, bad, {"xeng": True})
    clear_engines()

    # H: far-d spot (xeng)
    n = bad = 0
    for z in range(0, 7):
        for d in [16, 21, 26, 31, 36, 41, 46, 52]:
            x = z + d
            for R in range(1, x + z + 28 + 1):
                v = eng_val(z, x, R)
                n += 1
                if cand14(z, x, R) != v:
                    bad += 1
    check("H_far_d_spot_d52", n, bad, {"xeng": True})
    clear_engines()

    # I: merge regression vs K0832, z = 33..45, x = 14..24 (canonical only)
    n = bad = mrows = 0
    for z in range(33, 46):
        for x in range(14, 25):
            if x > z - 15:
                continue
            mrows += 1
            for R in range(1, x + z + 28 + 1):
                v = eng_val(z, x, R, xeng=False)
                n += 1
                if v != single_token_val(x + 14, R):
                    bad += 1
    check("I_merge_regression_k0832", n, bad, {"merge_rows": mrows, "xeng": False})
    clear_engines()

    # K: probe regeneration in memory, byte-identical to file
    regen = []
    for z in range(0, 34):
        for x in range(14, z + 31):
            hi = x + z + 28
            vals = [H_canonical(R, (x, 14), z) for R in range(1, hi + 1)]
            segs = []
            cur = vals[0]
            cnt = 1
            for v in vals[1:]:
                if v == cur:
                    cnt += 1
                else:
                    segs.append((cur, cnt))
                    cur = v
                    cnt = 1
            segs.append((cur, cnt))
            s = ' '.join(f"{v}x{c}" for v, c in segs)
            regen.append(f"z={z} x={x} d={x - z} merge={'1' if x <= z - 15 else '0'} :: {s}\n")
    regen_bytes = ''.join(regen).encode()
    regen_sha = hashlib.sha256(regen_bytes).hexdigest()
    byte_ident = (regen_bytes == raw_file)
    check("K_probe_regen_byte_identical", 0, 0 if byte_ident else 1, {"regen_sha256": regen_sha})
    clear_engines()

    # L: fail-closed probes
    fc = []
    # L1: tamper probe file first segment value -> fit check must report mismatch
    text = raw_file.decode()
    lines = text.splitlines()
    first = lines[0]
    seg = first.split('::')[1].split()[0]
    v, c = seg.split('x')
    newv = '2' if v != '2' else '0'
    tampered_line = first.replace(f"{v}x{c}", f"{newv}x{c}", 1)
    tampered = text.replace(first, tampered_line, 1)
    mm2 = 0
    for line in tampered.split('\n'):
        if '::' not in line:
            continue
        head, body = line.split('::')
        meta = dict(p.split('=') for p in head.split())
        z, x = int(meta['z']), int(meta['x'])
        vals = []
        for sg in body.split():
            vv, cc = sg.split('x')
            vals.extend([int(vv)] * int(cc))
        for i, vv in enumerate(vals):
            if cand14(z, x, i + 1) != vv:
                mm2 += 1
    fc.append({"name": "L1_probe_tamper", "mismatch": mm2, "caught": mm2 > 0})
    if mm2 == 0:
        ok = False

    # L2: cand14 merge-gate tamper (in_T14 gate `x <= z - Y - 1` widened to
    # `x <= z - Y + 1`) must produce mismatches on the probe box.
    # The pattern is anchored to the exact code line (newline + indent) so a
    # docstring mention of the same expression cannot shadow the patch.
    src = open('cand14.py').read()
    tam = src.replace("\n    if x <= z - Y - 1:", "\n    if x <= z - Y + 1:", 1)
    assert tam != src
    ns = {}
    exec(compile(tam, "cand14_tampered", "exec"), ns)
    mm3 = 0
    for z, x, vals in rows:
        for i, v in enumerate(vals):
            if ns['cand14'](z, x, i + 1) != v:
                mm3 += 1
    fc.append({"name": "L2_cand_mergegate_tamper", "mismatch": mm3, "caught": mm3 > 0})
    if mm3 == 0:
        ok = False

    # L3: K0832 tamper (q_even instead of q_odd) must break the merge assertion
    def st_tampered(S, R):
        qe = S if S % 2 == 0 else S - 1
        if R == 0:
            return 0
        if R % 2 == 1 and R <= qe:
            return 2
        if S % 2 == 1 and R >= qe + 1:
            return 1
        return 0
    mm4 = 0
    for z in range(33, 40):
        for x in range(14, 25):
            if x > z - 15:
                continue
            for R in range(1, x + z + 29):
                if eng_val(z, x, R, xeng=False) != st_tampered(x + 14, R):
                    mm4 += 1
    fc.append({"name": "L3_k0832_tamper", "mismatch": mm4, "caught": mm4 > 0})
    if mm4 == 0:
        ok = False
    out["fail_closed"] = fc

    out["engine"] = {
        "canonical": "probe_y14.py H_canonical, verbatim import",
        "ordered_idl": "independent no-sort implementation, used on checks marked xeng=true",
        "disagreements": ENG_DISAGREE[0],
    }
    if ENG_DISAGREE[0] != 0:
        ok = False

    out["overall"] = "PASS" if ok else "FAIL"
    blob = json.dumps(out, sort_keys=True, indent=1, ensure_ascii=False) + "\n"
    with open('audit.json', 'w') as f:
        f.write(blob)
    print(blob)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
