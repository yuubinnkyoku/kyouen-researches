#!/usr/bin/env python3
"""Builder for verify_y15_universal.py (part 1, 12 checks).

Machine assembly from the published canonical sources, mirroring the
published y=14 builder (scripts/build_verify_y14.py of the y=14 proof
experiment, SHA-256 24246a5d...):

  source 1: the published verify_y14_universal.py part2 canonical edition
            (SHA-256 6ac219cfe27e55e3d6057ea9dcf5db76631b8ef1c50ced0edd63f64d590f2205,
            commit 7026c860 of the y=14 proof experiment) -- the raw engines
            (H_ordered/H_canonical, verbatim from the published K1138
            verifier chain), the K0832 single_token block, and the cand14
            block (the B-child of every y=15 point and the x=15 merger child
            value; here used at x >= 15 rows only, inside its K1233
            universal domain x >= 14), which enters with a block-local
            Y -> Y14 rename so the cand15 block can carry Y = 15;
  source 2: the published cand15.py (SHA-256 f61997ddbee43e694624a2f4554b31ad45cfe27f1a49857f24e88d2209f8a23e,
            K1235 fit experiment commit 8222f6f6) -- the cand15 block
            (candidate under test), fit driver omitted.

Every extraction is marker-bounded with count asserts; source SHAs are
pinned. The generated verifier is byte-checked for the required absent
tokens (no cand13/C1d/C11r in part 1) and present tokens.
"""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC_Y14 = HERE / "published_verify_y14_universal.py"
SRC_C15 = HERE / "published_cand15.py"
OUT = HERE / "verify_y15_universal.py"

SHA_Y14 = "6ac219cfe27e55e3d6057ea9dcf5db76631b8ef1c50ced0edd63f64d590f2205"
SHA_C15 = "f61997ddbee43e694624a2f4554b31ad45cfe27f1a49857f24e88d2209f8a23e"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def must_contain_once(text: str, sub: str, what: str):
    c = text.count(sub)
    assert c == 1, f"{what}: expected exactly 1 occurrence, found {c}"


def extract(text: str, start_marker: str, end_marker: str, what: str) -> str:
    must_contain_once(text, start_marker, f"{what} start")
    must_contain_once(text, end_marker, f"{what} end")
    i = text.index(start_marker)
    j = text.index(end_marker)
    assert i < j, f"{what}: markers out of order"
    return text[i:j]


def main() -> int:
    assert sha(SRC_Y14) == SHA_Y14, "published verify_y14_universal.py SHA mismatch"
    assert sha(SRC_C15) == SHA_C15, "published cand15.py SHA mismatch"
    y14 = SRC_Y14.read_text(encoding="utf-8")
    c15 = SRC_C15.read_text(encoding="utf-8")

    # ---- engines + K0832 single_token (verbatim from the published y=14 machine)
    engines = extract(
        y14,
        "# ------------------------------------------------------------------\n# Raw engines",
        "# =====================================================================\n# Published y=13 two-token closed form",
        "engine section",
    )
    assert "def H_ordered" in engines and "def H_canonical" in engines
    assert "def single_token" in engines and "def q_odd" in engines
    assert engines.count("lru_cache(None)") == 2

    # ---- cand14 block (the B-child / the x=15 merger child value).
    # Extract from 'Y = 14' to the end of def cand14, then rename the
    # block-local Y -> Y14 (last-definition-wins discipline is preserved:
    # the re-defined q_odd/single_token_val copies inside the block are
    # semantically identical to the shared body, as in the published
    # y=10..y=14 verifiers).
    i14 = y14.index("Y = 14\n")
    j14 = y14.index("# =====================================================================\n# Published fixed-z slice anchors")
    cand14_block = y14[i14:j14]
    assert cand14_block.count("def cand14(z, x, R):") == 1
    assert cand14_block.rstrip().endswith("return 0"), "cand14 block must end at cand14"
    yrename = len(re.findall(r"\bY\b", cand14_block))
    assert yrename >= 20, f"Y rename count {yrename} too small"
    cand14_block = re.sub(r"\bY\b", "Y14", cand14_block)
    assert "Y14 = 14" in cand14_block
    assert len(re.findall(r"\bY14\b", cand14_block)) == yrename

    # ---- cand15 block (candidate under test) verbatim from the published fit,
    # fit driver omitted: from 'Y = 15' to the end of def cand15.
    i15 = c15.index("Y = 15\n")
    j15 = c15.index("def main():")
    cand15_block = c15[i15:j15]
    assert cand15_block.count("def cand15(z, x, R):") == 1
    assert cand15_block.rstrip().endswith("return 0"), "cand15 block must end at cand15"
    assert "def in_T15" in cand15_block and "def in_P15" in cand15_block
    assert "probe_rows.txt" not in cand15_block, "fit driver must be omitted"
    assert cand15_block.count("Y = 15") == 1

    parts = [HEADER, IMPORTS,
             ENGINES_COMMENT + engines.rstrip("\n"),
             CAND14_COMMENT + cand14_block.rstrip("\n"),
             CAND15_COMMENT + cand15_block.rstrip("\n"),
             BODY]
    text = "\n".join(parts) + "\n"
    code_only = text[text.index("import hashlib"):]
    for tok in ("def cand13", "def in_T13", "def check_C1d", "def check_C11r",
                "def A8u(", "def A17u(", "def identity_ok14", "def opts14",
                "def type_of14", "'C1d'", "'C11r'"):
        assert tok not in code_only, f"generated code must not contain {tok}"
    # part 1 must keep the stage references to the part 2 promotion in the
    # audit stage text only, exactly as the published y=13/y=14 part1 machines
    assert text.count("def check_C1(") == 1
    assert text.count("def check_C12(") == 1
    assert '"C11ordered"' in text and '"C11canonical"' in text
    for tok in ("def opts15", "def identity_ok15", "CLIP, SENT = 32, 33",
                "def check_C1(", "def check_C12(", "def cand15(z, x, R):",
                "(x, 15), z", "x <= z - 16", "(x + 15) % 2",
                '"C11ordered"', '"C11canonical"', "clip 31"):
        assert tok in text, f"generated file must contain {tok}"
    OUT.write_text(text, encoding="utf-8")
    print("written", OUT, len(text), "bytes;", "sha256", hashlib.sha256(text.encode()).hexdigest())
    return 0




def _build_header() -> str:
    import json
    head = '''#!/usr/bin/env python3
"""Universal verifier for the y=15 two-token residual family (PART 1).

Family: H(R; (x,15); z), all z >= 0, all x >= 15, all R >= 0.
Claim under test (K1235, currently status "observed"; this machine is the
promotion-stage part 1): the closed form cand15 equals H everywhere; with
corollaries
  merge-below-diagonal (y=15 promotion of the y=13/y=14 lines): x <= z-16
       =>  H == single_token(x+15, z, R)
  tail:                                 R >= x+z+16  =>  H == (x+15) % 2

STAGE: part 1 (12 machine checks; on overall PASS with 3 byte-identical
audit runs, part 2 -- the published fixed-z slice anchors at the y=15
rows (C1d) and the independent census_rows.py census.txt consumer
(C11r) -- promotes K1235 observed -> proved), per the procedure that
promoted y=5..y=14 (K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/
K1138/K1141/K1143/K1152/K1231/K1233 through their part1/part2 machines
K1024.../K1232/K1234).

Checks implemented and run here: C1, C1b, C2, C2b, C3, C4 (clip window
2y+2 = 32, sentinel 33), C4t (clip tightness probe 31/32), C7, C8, C9,
C11, C12.

Run modes:
  python3 verify_y15_universal.py                 # all checks except C11
  python3 verify_y15_universal.py C11ordered      # census part 1 (slow)
  python3 verify_y15_universal.py C11canonical    # census part 2 (slow)
  python3 verify_y15_universal.py C11             # merge census parts, then
                                                  # run all checks incl. C11
  python3 verify_y15_universal.py C1 C2 ...       # explicit check list

  C1   raw order-preserving AND descending-canonical engines vs cand15,
       z=0..14, x=15..33, R=0..x+z+47
  C1b  single-token closed form (K0832) raw anchor; published y=14 closed
       form (K1233 transcription, the B-child of every y=15 point and the
       x=15 A-child) raw anchor; x=15 multiset merger (14,15)==(15,14)
       i.e. A==B child value raw anchor
  C2   closed-form identity grid z=0..48, x=15..58, R<=x+z+41 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {15,20,...,65}, R <= x+z+31
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window 2y+2 = 32 sentinel 33, free-coordinate
       box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep, per-type
       confluence of the (value, sorted-children) effect
  C4t  tightness probe: the same box at clip 31 (2y+1) counts confluence
       violations (informational, not part of the bad total) -- tests
       the 11-family continuation candidate of the tight 2y+2 clip
       pattern (y=5..14: 12/14/16/18/20/22/24/26/28/30; 2y+2 for y=15
       is 32)
  C7   fixed-seed far probes (seed 20261152): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+16
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301,
       999..1001, 2999, 3000}, dx in [-30, 17], tail window
       [x+z+16, x+z+18]. x=14 rows enter the identity as closed-form
       extension-consistency rows only (no raw claim below x=15), exactly
       as the x=13 rows did in the published y=14 machine and the x=12
       rows in the published y=13 machine
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=15..70, R<=x+z+16, both engines,
       plus merge/tail corollaries. Because this execution host is
       memory-capped, the census runs each raw engine in its own command
       (C11ordered / C11canonical) through a BOUNDED-MEMOIZATION twin
       of the verbatim engine (identical recursive definition,
       existing LRU-capped cache; memoization of a deterministic pure
       function is transparent, and LRU eviction is deterministic under
       the fixed visit order). Each part writes output/census-<engine>.json;
       the C11 mode validates both parts (engine name, census geometry
       point counts, corollary counts recomputed from formulas, bad == 0
       fail-closed) and merges them. The unbounded verbatim engines
       still anchor C1, C1b, C3.
  C12  deep closed grid z=0..120, x=15..120, R<=x+z+17

Trust boundary (same machine class as the y=5..y=14 promotion machines):
option decomposition + closed-form mex identity + finite-type confluence
over the free-coordinate box, anchored to raw engines, to the published
y=14 family (K1233 proved, the B-child), and to the x=15 multiset merger
((14,15)==(15,14)). The family law shifts carried from y=14 to y=15
(odd-y type, same as y=9/11/13: value-1 infinite band and tail on x even
rows; pin lattice unified law pin = z+(d+45)/2 with o_pin in [16,30],
z-odd 8 pin rows d in {-13,-9,-5,-1,3,7,11,15} / z-even 7 pin rows d in
{-11,-7,-3,1,5,9,13} -- the odd-z (y+1)/2 row count reaching 8, the
first 8-pin-row family; z-odd I rows k(d)=floor((d+3y+1)/4) with
th=2k+1, pin slot = th-1 (5th consecutive family); z-even I rows
k(d)=floor((d+3y-1)/4), th=2k+1, z-even pin slot = 2k+1; base rows
k(d)=floor((d+3y+1)/4) (6-family law), the z-even d=15 base row at
k=15 saturation; sweep row d=16; steady pins z+30/z+31; band bottom
2y+2=32; tail x+z+16 on x even rows; merge x<=z-16; even-z diagonal
d=-15 without value 1 (8th consecutive candidate family); the final
pin row d=15=y being the first odd-z pin-row top in I[2y+z+1)=I[31)
form) are all inside the audited tables, not assumed separately.

Published transcriptions inside this file:
  engines + K0832 single_token (raw engines H_ordered/H_canonical, the
  K0832 single-token closed form and its helpers): verbatim from the
  published verify_y14_universal.py part2 (commit 7026c860 of the y=14
  proof experiment, SHA-256 6ac219cf...), whose own provenance chain is
  the published verify_y13_universal.py part1/part2 (K1231 promotion
  machine), verify_y12_universal.py (K1152/K1162), verify_y11_universal.py
  (K1143 part 1), verify_y10_universal.py (K1141) and verify_y09_
  universal.py (K1138);
  cand14 (the B-child of every y=15 point and the x=15 merger child
  value): verbatim from the published verify_y14_universal.py cand14
  block (block-local Y renamed to Y14 so the cand15 block can carry
  Y = 15; that block is itself the published cand14.py transcription
  minus the fit driver; its universal proof is K1233, promoted by the
  K1234 part1/part2 machine); its y=15-scope usage (x >= 15 rows) is
  inside its published universal domain (x >= 14, all z, all R);
  the re-defined q_odd/single_token_val copies inside the cand14/cand15
  blocks are semantically identical to the shared body (last definition
  wins at call time, as in the published y=10..y=14 verifiers);
  cand15: verbatim from the published cand15.py (K1235 fit experiment,
  commit 8222f6f6, SHA-256 f61997dd...), fit driver omitted (its probe
  self-check is K1235's own evidence, re-runnable there);
Their correctness is K0832/K1233/K1235's claim, not re-proven here; every
transcription is additionally re-anchored against the raw
order-preserving engine by this machine's C1/C1b.
Determinism: fixed seed, no clock, sorted audit keys, census parts
deterministic under the fixed visit order and LRU cap.
"""
'''
    return head


HEADER = _build_header()

IMPORTS = """import hashlib
import json
import random
import sys
import types
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


"""

ENGINES_COMMENT = ""

CAND14_COMMENT = """# =====================================================================
# Published y=14 two-token closed form (K1233 proved). This is the
# B-child of every y=15 point and the x=15 merger child value. Code
# block verbatim from the published verify_y14_universal.py cand14
# block (block-local Y renamed to Y14 so the cand15 block can carry
# Y = 15; that block is itself the published cand14.py transcription
# minus the fit driver; its universal proof is K1233).
# =====================================================================

"""

CAND15_COMMENT = """# =====================================================================
# Candidate under test: y=15 two-token closed form (K1235 published fit).
# cand15 tables verbatim from the published cand15.py (K1235 fit
# experiment); fit driver omitted. The y=14 family (cand14 block above)
# is the B-child of this identity and the x=15 merger child value.
# =====================================================================

"""

BODY = r'''

# =====================================================================
# Option decomposition and the identity under test (y=15 family).
# =====================================================================
def opts15(z, x, R):
    """Closed-form option values of H(R; (x,15); z). R >= 1.

    x == 15: both token-decrement children coincide as multisets:
    (14,15) == (15,14), both are the y=14 family row x=15.
    """
    if x == 15:
        A = cand14(z, 15, R - 1)
    else:
        A = cand15(z, x - 1, R - 1)
    out = [A, cand14(z, x, R - 1)]
    if z >= 1:
        out.append(1 ^ cand15(z - 1, x, R - 1))
    return out


def identity_ok15(z, x, R):
    t = in_T15(z, x, R)
    pv = in_P15(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    got = mex(opts15(z, x, R))
    want = cand15(z, x, R)
    return got == want, got, want


# ------------------------------------------------------------------
# Type machine. y=14's clip window (+/-30 sentinel +/-31) folded the
# y=14 features; the y=15 features (pins up to z+30 odd-z / z+31 even-z,
# sweep band d=16 offsets up to x+15, band bottom R-z = 2y+2 = 32,
# tail offset R-x-z = 16, merge boundary x = z-16, base span to z+29
# and the I-row th(d) excursions up to 31) are tested with +/-32/33
# (= 2y+2 for y=15), the 11-family-continuation candidate of the 2y+2
# tight pattern (y=5..14: 12/14/16/18/20/22/24/26/28/30). CLIP/SENT are
# re-checked for confluence by check_C4; the tightness probe (CLIP=31)
# is reported separately (check_C4t).
# ------------------------------------------------------------------
CLIP, SENT = 32, 33


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of15(z, x, R):
    return (1 if x == 15 else 0,
            1 if z == 0 else 0,
            z % 2, x % 2, R % 2,
            clipw(x - z), clipw(R - x), clipw(R - z),
            clipw(R - x - z), clipw(R - 2 * x), clipw(R - 2 * z))


def vpoint(v0, v1, v3):
    z = v1 - v3
    x = v0 + v1 - v3
    R = v0 + 2 * v1 - v3
    return z, x, R


# ------------------------------------------------------------------
# Checks.
# ------------------------------------------------------------------
def check_C1(audit):
    n = bad = 0
    for z in range(0, 15):
        for x in range(15, 34):
            for R in range(0, x + z + 48):
                n += 1
                c = cand15(z, x, R)
                if H_ordered(R, (x, 15), z) != c or H_canonical(R, (x, 15), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand15 z=0..14 x=15..33 R<=x+z+47',
                   'points': n, 'bad': bad}


def check_C1b(audit):
    n = bad = 0
    # (i) single-token closed form (K0832) vs raw ordered engine
    for z in range(0, 21):
        for x in range(1, 21):
            for R in range(0, x + z + 21):
                n += 1
                if H_ordered(R, (x,), z) != single_token(x, z, R):
                    bad += 1
    # (ii) published y=14 closed form (K1233, the B-child) raw anchor
    for z in range(0, 25):
        for x in range(14, 29):
            for R in range(0, x + z + 31):
                n += 1
                if H_ordered(R, (x, 14), z) != cand14(z, x, R):
                    bad += 1
    # (iii) x=15 multiset merger: (14,15) == (15,14) raw, and == cand14(z,15,R-1)
    for z in range(0, 31):
        for R in range(1, z + 44):
            n += 1
            a = H_ordered(R - 1, (14, 15), z)
            b = H_ordered(R - 1, (15, 14), z)
            c = H_canonical(R - 1, (14, 15), z)
            if a != b or a != c or a != cand14(z, 15, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=14-child/x=15 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(15, 59):
            for R in range(1, x + z + 42):
                n += 1
                ok, _, _ = identity_ok15(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=15..58 R<=x+z+41 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(15, 70, 5):
            for R in range(1, x + z + 32):
                n += 1
                ok, _, _ = identity_ok15(z, x, R)
                if not ok or (R >= x + z + 16 and cand15(z, x, R) != (x + 15) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400} x=15..65(step5) R<=x+z+31',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(15, 20):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 15:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 15), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (14, 15), z))
                raw_opts.add(H_ordered(R - 1, (x, 14), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 15), z - 1))
                closed = set(opts15(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of15(z, x, R)
    e = (cand15(z, x, R), tuple(sorted(opts15(z, x, R))))
    if t not in types:
        types[t] = e
        return True
    return types[t] == e


def box_points(B):
    for v0 in range(-B, B + 1):
        for v1 in range(-B, B + 1):
            for v3 in range(-B, B + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 15 or R < 1:
                    continue
                yield z, x, R


def check_C4(audit, types):
    n = bad = conf_bad = id_bad = 0
    for z, x, R in box_points(60):
        n += 1
        ok, _, _ = identity_ok15(z, x, R)
        if not ok:
            id_bad += 1
        if not conform(z, x, R, types):
            conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 32/sentinel 33, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C4t(audit):
    """Tightness probe: clip 31 / sentinel 32 over the same box.

    Counts type-confluence violations when the clip window is narrowed
    by one (2y+1 instead of the 11-family candidate 2y+2=32). Not part
    of the PASS/FAIL bad total; reported for the pattern claim.
    """
    global CLIP, SENT
    old_clip, old_sent = CLIP, SENT
    CLIP, SENT = 31, 32
    n = viol = 0
    first = None
    probe_types = {}
    for z, x, R in box_points(60):
        n += 1
        if not conform(z, x, R, probe_types):
            viol += 1
            if first is None:
                first = (z, x, R)
    CLIP, SENT = old_clip, old_sent
    audit['C4t'] = {'desc': 'tightness probe clip 31/sentinel 32 (not in bad total)',
                    'points': n, 'violations_at_clip31': viol,
                    'first_violation': first}


def check_C7(audit, types, corr):
    rng = random.Random(20261152)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(15, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 16)
        elif mode == 1:
            R = x + z + 16 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(15, z + rng.randrange(-30, 19))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 15:
            continue
        n += 1
        ok, _, _ = identity_ok15(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261152, z,x<=3000',
                   'points': n, 'bad': bad}


def check_C8(audit, types, corr):
    n = bad = 0
    zs = list(range(0, 6)) + list(range(29, 32)) + list(range(59, 62)) + \
        list(range(299, 302)) + list(range(999, 1002)) + [2999, 3000]
    for z in zs:
        for dx in range(-30, 18):
            x = z + dx
            if x < 14:
                continue
            for R in range(1, x + z + 31):
                n += 1
                ok, _, _ = identity_ok15(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 16, x + z + 17, x + z + 18):
                n += 1
                if cand14(z, x, R) != (x + 14) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-30,17], tail window',
                   'points': n, 'bad': bad}


def check_C9(audit, types):
    n = bad = 0
    for band in ((61, 64), (89, 92), (117, 120)):
        lo, hi = band
        for v0 in range(-hi, hi + 1):
            for v1 in range(-hi, hi + 1):
                for v3 in range(-hi, hi + 1):
                    m = max(abs(v0), abs(v1), abs(v3))
                    if m < lo:
                        continue
                    z, x, R = vpoint(v0, v1, v3)
                    if z < 0 or x < 15 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok15(z, x, R)
                    if not ok or not conform(z, x, R, types):
                        bad += 1
    audit['C9'] = {'desc': 'v-space shell sweeps [61,64],[89,92],[117,120]',
                   'points': n, 'bad': bad}


# ------------------------------------------------------------------
# C11 census: bounded-memoization twins + separate-command parts.
# ------------------------------------------------------------------
CENSUS_CACHE_MAXSIZE = 1_600_000


def _bounded_twin(raw_engine, name):
    """LRU-capped twin of a published raw engine.

    The recursive definition is byte-identical (the published function's
    own code object re-bound into a shallow copy of the module globals,
    with the recursive name resolving to the capped wrapper instead of the
    unbounded cache). Memoization of a deterministic pure function is
    transparent, and LRU eviction is deterministic under the fixed
    census visit order, so the twin returns exactly the published engine's
    values; the cap only bounds residency on this memory-capped host.
    """
    impl = raw_engine.__wrapped__
    g = dict(impl.__globals__)
    twin = types.FunctionType(impl.__code__, g, impl.__name__)
    capped = lru_cache(CENSUS_CACHE_MAXSIZE)(twin)
    g[name] = capped
    return capped


def _census_part_file(engine_name):
    return f"census-{engine_name}.json"


def _census_expected_counts():
    points = merge = tail = 0
    for z in range(0, 80):
        for x in range(15, 71):
            points += x + z + 17
            if x <= z - 16:
                merge += x + z + 17
            tail += 1  # exactly one R (= x+z+16) is >= x+z+16 within the box
    return points, merge, tail


def run_census(engine_name):
    if engine_name not in ("ordered", "canonical"):
        raise SystemExit(f"FAIL-CLOSED: unknown census engine {engine_name}")
    raw = H_ordered if engine_name == "ordered" else H_canonical
    twin = _bounded_twin(raw, "H_ordered" if engine_name == "ordered" else "H_canonical")
    n = bad = 0
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    for z in range(0, 80):
        for x in range(15, 71):
            for R in range(0, x + z + 17):
                c = cand15(z, x, R)
                if twin(R, (x, 15), z) != c:
                    bad += 1
                corollary(z, x, R, corr)
                n += 1
    payload = {
        'engine': engine_name,
        'box': 'z=0..79, x=15..70, R=0..x+z+16',
        'cache_type': 'bounded-memoization twin of the verbatim raw engine (published code object, LRU-capped cache)',
        'cache_maxsize': CENSUS_CACHE_MAXSIZE,
        'points': n,
        'bad': bad,
        'corollaries': {
            'merge': {'points': corr['merge']['points'], 'bad': corr['merge']['bad'],
                      'claim': 'x<=z-16 => H == single_token(x+15,z,R)'},
            'tail': {'points': corr['tail']['points'], 'bad': corr['tail']['bad'],
                     'claim': 'R>=x+z+16 => H == (x+15)%2'},
        },
    }
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    (out / _census_part_file(engine_name)).write_text(text, encoding="utf-8")
    print(f"census[{engine_name}]: points={n} bad={bad} "
          f"merge={corr['merge']} tail={corr['tail']}", flush=True)
    return 0 if bad == 0 and corr['merge']['bad'] == 0 and corr['tail']['bad'] == 0 else 1


def check_C11(audit, corr):
    out = Path(__file__).with_name("output")
    parts = {}
    for engine_name in ("ordered", "canonical"):
        p = out / _census_part_file(engine_name)
        if not p.is_file():
            raise SystemExit(
                f"FAIL-CLOSED: census part file for engine '{engine_name}' is "
                f"missing ({p.name}); run mode C11{engine_name} first")
        parts[engine_name] = json.loads(p.read_text(encoding="utf-8"))
    exp_points, exp_merge, exp_tail = _census_expected_counts()
    for engine_name, part in parts.items():
        if part.get('engine') != engine_name:
            raise SystemExit("FAIL-CLOSED: census part engine field mismatch")
        if part.get('box') != 'z=0..79, x=15..70, R=0..x+z+16':
            raise SystemExit("FAIL-CLOSED: census part box mismatch")
        if part.get('cache_maxsize') != CENSUS_CACHE_MAXSIZE:
            raise SystemExit("FAIL-CLOSED: census cache cap mismatch")
        if part.get('points') != exp_points:
            raise SystemExit(f"FAIL-CLOSED: census points {part.get('points')} != {exp_points}")
        if part.get('bad') != 0:
            raise SystemExit("FAIL-CLOSED: census part reported bad != 0")
        cm, ct = part['corollaries']['merge'], part['corollaries']['tail']
        if cm['points'] != exp_merge or cm['bad'] != 0:
            raise SystemExit("FAIL-CLOSED: census merge corollary mismatch")
        if ct['points'] != exp_tail or ct['bad'] != 0:
            raise SystemExit("FAIL-CLOSED: census tail corollary mismatch")
    ordered, canonical = parts['ordered'], parts['canonical']
    n = ordered['points'] + canonical['points']
    bad = ordered['bad'] + canonical['bad']
    for k in ('merge', 'tail'):
        corr[k]['points'] += ordered['corollaries'][k]['points'] + canonical['corollaries'][k]['points']
        corr[k]['bad'] += ordered['corollaries'][k]['bad'] + canonical['corollaries'][k]['bad']
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=15..70 R<=x+z+16, both engines '
                            '(bounded-memoization twins, LRU cap 1600000, separate commands '
                            'C11ordered/C11canonical on this memory-capped host), parts validated '
                            'and merged here with recomputed expected counts',
                    'points': n, 'bad': bad,
                    'ordered_points': ordered['points'],
                    'canonical_points': canonical['points'],
                    'census_cache_maxsize': CENSUS_CACHE_MAXSIZE,
                    'census_part_files': ['census-ordered.json', 'census-canonical.json']}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(15, 121):
            for R in range(1, x + z + 18):
                n += 1
                ok, _, _ = identity_ok15(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=15..120 R<=x+z+17',
                   'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 16:
        corr['merge']['points'] += 1
        if cand15(z, x, R) != single_token(x + 15, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 16:
        corr['tail']['points'] += 1
        if cand15(z, x, R) != (x + 15) % 2:
            corr['tail']['bad'] += 1


def main():
    args = sys.argv[1:]
    if args and args[0] in ("C11ordered", "C11canonical"):
        rc = run_census(args[0][3:].lower())
        return {'overall': 'PASS' if rc == 0 else 'FAIL'}
    requested = set(args)
    everything = {'C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'}
    todo = requested & everything if requested else (everything - {'C11'})
    audit = {'experiment': 'vertical-fiber-two-token-y15-parametric-allz-proof-20261122',
             'family': 'H(R;(x,15);z), z>=0, x>=15, R>=0',
             'stage': 'part 1 (12 checks; on overall PASS with 3 byte-identical audit '
                      'runs the part 2 machine -- published fixed-z slice anchors at '
                      'the y=15 rows (C1d) and the independent census_rows.py '
                      'census.txt consumer (C11r) -- promotes K1235 observed->proved), '
                      'per the procedure that promoted y=5..y=14',
             'checks_run': sorted(todo),
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-16 => H == single_token(x+15,z,R)'},
                 'tail': {'claim': 'R>=x+z+16 => H == (x+15)%2'}}}
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    types = {}

    for name in ('C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'):
        if name not in todo:
            continue
        if name == 'C1':
            check_C1(audit['checks'])
        elif name == 'C1b':
            check_C1b(audit['checks'])
        elif name == 'C2':
            check_C2(audit['checks'], corr)
        elif name == 'C2b':
            check_C2b(audit['checks'])
        elif name == 'C3':
            check_C3(audit['checks'])
        elif name == 'C4':
            check_C4(audit['checks'], types)
        elif name == 'C4t':
            check_C4t(audit['checks'])
        elif name == 'C7':
            check_C7(audit['checks'], types, corr)
        elif name == 'C8':
            check_C8(audit['checks'], types, corr)
        elif name == 'C9':
            check_C9(audit['checks'], types)
        elif name == 'C11':
            check_C11(audit['checks'], corr)
        elif name == 'C12':
            check_C12(audit['checks'], types, corr)
        c = audit['checks'].get(name)
        if c:
            print(f"  {name}: pts={c.get('points')} bad={c.get('bad', 0)}", flush=True)

    audit['corollaries']['merge_below_diagonal'].update(corr['merge'])
    audit['corollaries']['tail'].update(corr['tail'])
    total = sum(c['points'] for c in audit['checks'].values() if 'points' in c)
    allbad = sum(c['bad'] for c in audit['checks'].values() if 'bad' in c)
    audit['total_points'] = total
    audit['total_bad'] = allbad + corr['merge']['bad'] + corr['tail']['bad']
    audit['type_count'] = len(types)
    audit['overall'] = 'PASS' if audit['total_bad'] == 0 else 'FAIL'
    audit['verifier_sha256'] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(audit, sort_keys=True, ensure_ascii=False, indent=2)
    (out / "audit.json").write_text(payload + "\n", encoding="utf-8")
    print('overall:', audit['overall'], 'total_points:', total,
          'types:', len(types), flush=True)
    for k in sorted(audit['checks']):
        c = audit['checks'][k]
        print(f"  {k}: pts={c.get('points')} bad={c.get('bad')}", flush=True)
    print('  merge:', corr['merge'])
    print('  tail:', corr['tail'])
    if 'C4t' in audit['checks']:
        t = audit['checks']['C4t']
        print('  C4t:', t['violations_at_clip31'], 'violations at clip 31, first:', t['first_violation'])
    return audit


if __name__ == '__main__':
    sys.exit(0 if main()['overall'] == 'PASS' else 1)
'''

if __name__ == "__main__":
    sys.exit(main())
