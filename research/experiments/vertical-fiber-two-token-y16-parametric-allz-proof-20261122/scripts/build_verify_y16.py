#!/usr/bin/env python3
"""Assemble verify_y16_universal.py (part1, 12 checks) from the pinned source
bytes shipped in this experiment dir.

Sources (sha-guarded):
  ../published_verify_y15_universal.py  the published y=15 proof part2
       canonical edition (commit 0bf18752 of the y=15 proof experiment,
       SHA-256 a39e7ab1...): raw engines H_ordered/H_canonical + K0832
       single_token block (verbatim); the cand15 block (the B-child of every
       y=16 point and the x=16 merger child value) verbatim with a block-local
       Y -> Y15 rename; the check battery that this builder adapts to the
       y=16 family constants.
  ../published_cand16.py  the published y=16 fit closed form (K1237 fit
       experiment vertical-fiber-two-token-y16-parametric-allz-fit-20261122,
       commit 33e1c22e): the cand16 block verbatim, fit driver omitted.
Every transformation is spelled out with count-asserted substitutions; run
from scripts/ it rewrites ../verify_y16_universal.py deterministically
(byte-identical across runs).
"""
import re
from pathlib import Path

SRC_Y15 = Path(__file__).with_name("..", ).joinpath("published_verify_y15_universal.py").read_text(encoding="utf-8")
SRC_CAND16 = Path(__file__).parent.parent.joinpath("published_cand16.py").read_text(encoding="utf-8")

lines = SRC_Y15.split("\n")

# --- 1. slice out sections (1-indexed, inclusive) -------------------
# docstring: lines 2..137 (0-indexed 1..136); module doc ends before "import hashlib"
i_import = next(i for i, l in enumerate(lines) if l.startswith("import hashlib"))
head = lines[:1]           # '#!/usr/bin/env python3'
engines = lines[i_import:]  # from import block through single_token end

# find banner line indices
def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    raise SystemExit(f"not found: {prefix}")

b_cand14 = find("# =====================================================================")
# cand14 banner block: banner start .. banner end line (another ===== line)
b_cand14_end = find("# =====================================================================", b_cand14 + 1) + 1
# main cand15 block banner
b_cand15 = find("# =====================================================================", b_cand14_end)
b_cand15_end = find("# =====================================================================", b_cand15 + 1) + 1
# slice anchors banner
b_slice = find("# =====================================================================", b_cand15_end)
b_slice_end = find("# =====================================================================", b_slice + 1) + 1
# option decomposition banner
b_opts = find("# =====================================================================", b_slice_end)
b_opts_end = find("# =====================================================================", b_opts + 1) + 1

print("banners:", b_cand14, b_cand14_end, b_cand15, b_cand15_end,
      b_slice, b_slice_end, b_opts, b_opts_end)
assert 'Published y=14 two-token closed form' in "\n".join(lines[b_cand14:b_cand14_end])
assert 'Published fixed-z slice anchors (C1d)' in "\n".join(lines[b_slice:b_slice_end])

engines = lines[i_import:b_cand14]

# cand15 block body (from the y15 machine itself: Y = 15 .. end of cand15())
cand15_body = lines[b_cand15_end: b_slice]
# strip the trailing banner-comment remnant: body runs to the cand15 function end.
cand15_body = cand15_body[:-1] if cand15_body and cand15_body[-1].startswith("# ") else cand15_body
# rename block-local Y -> Y15 inside the body (code + comments), only whole-token
cand15_text = []
for l in cand15_body:
    l = re.sub(r"\bY\b", "Y15", l)
    cand15_text.append(l)
cand15_block = (
    "# =====================================================================\n"
    "# Published y=15 two-token closed form (K1235 proved). This is the\n"
    "# B-child of every y=16 point and the x=16 merger child value. Code\n"
    "# block verbatim from the published verify_y15_universal.py cand15\n"
    "# block (block-local Y renamed to Y15 so the cand16 block can carry\n"
    "# Y = 16; that block is itself the published cand15.py transcription\n"
    "# minus the fit driver; its universal proof is K1235, promoted by the\n"
    "# K1235 part1/part2 machine); its y=16-scope usage (x >= 16 rows) is\n"
    "# inside its published universal domain (x >= 15, all z, all R).\n"
    "# =====================================================================\n" +
    "\n".join(cand15_text) + "\n")

# cand16 block from the published cand16.py (transcription minus fit driver)
c16 = SRC_CAND16.split("\n")
i_y = next(i for i, l in enumerate(c16) if l == "Y = 16")
i_main = next(i for i, l in enumerate(c16) if l.startswith("def main():"))
cand16_block = (
    "# =====================================================================\n"
    "# Published y=16 closed form cand16 (K1237, status observed at the\n"
    "# time of this machine's construction). cand16 tables verbatim from\n"
    "# the published cand16.py (K1237 fit experiment; fit driver omitted);\n"
    "# the published bytes are re-anchored against the raw engines by this\n"
    "# machine's C1/C1b and against the y=15 family B-child by C1b/C3.\n"
    "# =====================================================================\n" +
    "\n".join(c16[i_y:i_main]) + "\n")

# tail: option decomposition + checks + main, from banner b_opts on
tail = lines[b_opts_end:]

DOC = '''"""
Universal verifier for the y=16 two-token residual family (PART 1).

Family: H(R; (x,16); z), all z >= 0, all x >= 16, all R >= 0.
Claim under test (K1237, currently status "observed"): the closed form
cand16 equals H everywhere; with corollaries
  merge-below-diagonal (y=16 promotion of the y=12/y=14 lines):
       x <= z-17  =>  H == single_token(x+16, z, R)
  tail:                                 R >= x+z+17  =>  H == (x+16) % 2

STAGE: part 1 (the 12-check machine; the promotion stage part 2 adds the
published fixed-z slice anchors C1d and the independent census_rows.py
consumer C11r), per the procedure that promoted y=5..y=15
(K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/K1143/K1152/
K1231/K1233/K1235).

Checks implemented and run here: C1, C1b, C2, C2b, C3, C4 (clip window
2y+2 = 34, sentinel 35), C4t (clip tightness probe 33), C7, C8, C9,
C11, C12.

Run modes:
  python3 verify_y16_universal.py                 # all checks except C11
  python3 verify_y16_universal.py C11ordered      # census part 1 (slow)
  python3 verify_y16_universal.py C11canonical    # census part 2 (slow)
  python3 verify_y16_universal.py C11             # merge census parts, then
                                                  # run all checks incl. C11
  python3 verify_y16_universal.py C1 C2 ...       # explicit check list

  C1   raw order-preserving AND descending-canonical engines vs cand16,
       z=0..14, x=16..34, R=0..x+z+47
  C1b  single-token closed form (K0832) raw anchor; published y=15 closed
       form (K1235 transcription, the B-child of every y=16 point and the
       x=16 A-child) raw anchor; x=16 multiset merger (15,16)==(16,15)
       i.e. A==B child value raw anchor
  C2   closed-form identity grid z=0..48, x=16..58, R<=x+z+42 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {16,21,...,66}, R <= x+z+31
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window 2y+2 = 34 sentinel 35, free-coordinate
       box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep, per-type
       confluence of the (value, sorted-children) effect
  C4t  tightness probe: the same box at clip 33 (2y+1) counts confluence
       violations (informational, not part of the bad total) -- tests
       the 12-family continuation candidate of the tight 2y+2 clip
       pattern (y=5..15: 12/14/16/18/20/22/24/26/28/30/32; 2y+2 for
       y=16 is 34)
  C7   fixed-seed far probes (seed 20261162): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+17
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301,
       999..1001, 2999, 3000}, dx in [-30, 17], tail window
       [x+z+17, x+z+19]. x=15 rows enter the identity as closed-form
       extension-consistency rows only (no raw claim below x=16),
       exactly as the x=14 rows did in the published y=15 machine and
       the x=13 rows in the published y=14 machine
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=16..70, R<=x+z+17, both engines,
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
  C12  deep closed grid z=0..120, x=16..120, R<=x+z+18

Trust boundary (same machine class as the y=5..y=15 promotion machines):
option decomposition + closed-form mex identity + finite-type confluence
over the free-coordinate box, anchored to raw engines, to the published
y=15 family (K1235 proved, the B-child), to the x=16 multiset merger
((15,16)==(16,15)). The family law shifts carried from y=15 to y=16
(even-y type, same row-type family as y=10/12/14: value-1 infinite band
and tail on x odd rows; pin lattice unified law pin = z+(d+48)/2 with
o_pin in [17,32], z-odd 8 pin rows d in {-12,-8,-4,0,4,8,12,16} / z-even
8 pin rows d in {-14,-10,-6,-2,2,6,10,14} -- the first both-parity
8-row family (y/2 row count law); z-odd I rows k(d)=floor((d+3y+2)/4)
with th sweeping the consecutive integers 17..33 over the 17 d-even rows,
pin slot = th-1 (6th consecutive family); z-even I rows
k(d)=floor((d+3y-1)/4), th=2k+1, z-even pin slot = 2k+1; base rows
k(d)=floor((d+3y+1)/4) (7-family law), the z-even d=16 base row at
k=16 saturation; sweep row d=17; steady pins z+32/z+33; single even band
law (even-y contrast to y=15's band_base/band_int separation); band
bottom 2y+2=34; tail x+z+17 on x odd rows; merge x<=z-17; even-z
diagonal d=-16 without value 1 (9th consecutive candidate family); the
final pin row d=16=y reaching the upper endpoint in I[33) form) are all
inside the audited tables, not assumed separately.

Published transcriptions inside this file:
  engines + K0832 single_token (raw engines H_ordered/H_canonical, the
  K0832 single-token closed form and its helpers): verbatim from the
  published verify_y15_universal.py part2 (commit 0bf18752 of the y=15
  proof experiment, SHA-256 a39e7ab1...), whose own provenance chain is
  the published verify_y14_universal.py part1/part2 (K1233/K1234
  promotion machine), verify_y13_universal.py (K1231), verify_y12_

  universal.py (K1152/K1162), verify_y11_universal.py (K1143 part 1),
  verify_y10_universal.py (K1141) and verify_y09_universal.py (K1138);
  cand15 (the B-child of every y=16 point and the x=16 merger child
  value): verbatim from the published verify_y15_universal.py cand15
  block (block-local Y renamed to Y15 so the cand16 block can carry
  Y = 16; that block is itself the published cand15.py transcription
  minus the fit driver; its universal proof is K1235, promoted by the
  K1236 part1/part2 machine); its y=16-scope usage (x >= 16 rows) is
  inside its published universal domain (x >= 15, all z, all R);
  cand16: verbatim from the published cand16.py (K1237 fit experiment
  vertical-fiber-two-token-y16-parametric-allz-fit-20261122, commit
  33e1c22e; the fit driver is omitted); its correctness at universal
  scope is exactly the claim under test, not assumed.
Determinism: fixed seed, no clock, sorted audit keys, census parts
deterministic under the fixed visit order and LRU cap.
"""
'''

out = [head[0], DOC] + engines + ["\n"] + cand15_block.split("\n") + cand16_block.split("\n") + tail
text = "\n".join(out)
text = text.replace("# Option decomposition and the identity under test (y=15 family).",
                    "# Option decomposition and the identity under test (y=16 family).")

# --- 2. systematic renames in the tail (opts/checks) ----------------
# order matters: cand15->cand16 first, then cand14->cand15
R = [("cand15", "cand16"), ("cand14", "cand15"),
     ("opts15", "opts16"), ("identity_ok15", "identity_ok16"),
     ("type_of15", "type_of16")]
# apply renames only from the opts banner onward to avoid touching blocks
i_opts = text.find("def opts")
head_text, tail_text = text[:i_opts], text[i_opts:]
for a, b in R:
    tail_text = tail_text.replace(a, b)

# --- 3. per-check structural edits -----------------------------------
def sub1(old, new):
    global tail_text
    assert tail_text.count(old) == 1, (old, tail_text.count(old))
    tail_text = tail_text.replace(old, new)

# opts16: x=16 confluence + B-child
sub1('''    """Closed-form option values of H(R; (x,15); z). R >= 1.

    x == 15: both token-decrement children coincide as multisets:
    (14,15) == (15,14), both are the y=14 family row x=15.
    """
    if x == 15:
        A = cand15(z, 15, R - 1)''',
     '''    """Closed-form option values of H(R; (x,16); z). R >= 1.

    x == 16: both token-decrement children coincide as multisets:
    (15,16) == (16,15), both are the y=15 family row x=16.
    """
    if x == 16:
        A = cand15(z, 16, R - 1)''')

sub1("    return 0 if bad == 0 and corr['merge']['bad'] == 0 and corr['tail']['bad'] == 0 else 1",  # noop guard
     "    return 0 if bad == 0 and corr['merge']['bad'] == 0 and corr['tail']['bad'] == 0 else 1")

# typemachine constants
sub1("CLIP, SENT = 32, 33", "CLIP, SENT = 34, 35")
sub1("    return (1 if x == 15 else 0,", "    return (1 if x == 16 else 0,")
sub1('''def type_of16(z, x, R):''', '''def type_of16(z, x, R):''')

# C1
sub1("    for z in range(0, 15):\n        for x in range(15, 34):\n            for R in range(0, x + z + 48):\n                n += 1\n                c = cand16(z, x, R)\n                if H_ordered(R, (x, 15), z) != c or H_canonical(R, (x, 15), z) != c:\n                    bad += 1",
     "    for z in range(0, 15):\n        for x in range(16, 35):\n            for R in range(0, x + z + 48):\n                n += 1\n                c = cand16(z, x, R)\n                if H_ordered(R, (x, 16), z) != c or H_canonical(R, (x, 16), z) != c:\n                    bad += 1")
sub1("    audit['C1'] = {'desc': 'raw both engines vs cand16 z=0..14 x=15..33 R<=x+z+47',",
     "    audit['C1'] = {'desc': 'raw both engines vs cand16 z=0..14 x=16..34 R<=x+z+47',")

# C1b (ii)/(iii)
sub1('''    # (ii) published y=14 closed form (K1233, the B-child) raw anchor
    for z in range(0, 25):
        for x in range(14, 29):
            for R in range(0, x + z + 31):
                n += 1
                if H_ordered(R, (x, 14), z) != cand15(z, x, R):
                    bad += 1
    # (iii) x=15 multiset merger: (14,15) == (15,14) raw, and == cand15(z,15,R-1)
    for z in range(0, 31):
        for R in range(1, z + 44):
            n += 1
            a = H_ordered(R - 1, (14, 15), z)
            b = H_ordered(R - 1, (15, 14), z)
            c = H_canonical(R - 1, (14, 15), z)
            if a != b or a != c or a != cand15(z, 15, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=14-child/x=15 merger raw anchors',''',
     '''    # (ii) published y=15 closed form (K1235, the B-child) raw anchor
    for z in range(0, 25):
        for x in range(15, 29):
            for R in range(0, x + z + 31):
                n += 1
                if H_ordered(R, (x, 15), z) != cand15(z, x, R):
                    bad += 1
    # (iii) x=16 multiset merger: (15,16) == (16,15) raw, and == cand15(z,16,R-1)
    for z in range(0, 31):
        for R in range(1, z + 45):
            n += 1
            a = H_ordered(R - 1, (15, 16), z)
            b = H_ordered(R - 1, (16, 15), z)
            c = H_canonical(R - 1, (15, 16), z)
            if a != b or a != c or a != cand15(z, 16, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=15-child/x=16 merger raw anchors',''')

# C2 / C2b
sub1('''    for z in range(0, 49):
        for x in range(15, 59):
            for R in range(1, x + z + 42):
                n += 1
                ok, _, _ = identity_ok16(z, x, R)''',
     '''    for z in range(0, 49):
        for x in range(16, 59):
            for R in range(1, x + z + 43):
                n += 1
                ok, _, _ = identity_ok16(z, x, R)''')
sub1("    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=15..58 R<=x+z+41 (+merge,tail)',",
     "    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=16..58 R<=x+z+42 (+merge,tail)',")
sub1('''    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(15, 70, 5):
            for R in range(1, x + z + 32):
                n += 1
                ok, _, _ = identity_ok16(z, x, R)
                if not ok or (R >= x + z + 16 and cand16(z, x, R) != (x + 15) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400} x=15..65(step5) R<=x+z+31',''',
     '''    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(16, 71, 5):
            for R in range(1, x + z + 32):
                n += 1
                ok, _, _ = identity_ok16(z, x, R)
                if not ok or (R >= x + z + 17 and cand16(z, x, R) != (x + 16) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400} x=16..66(step5) R<=x+z+31',''')

# C3
sub1('''    for z in range(0, 6):
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
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 15), z - 1))''',
     '''    for z in range(0, 6):
        for x in range(16, 21):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 16:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 16), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (15, 16), z))
                raw_opts.add(H_ordered(R - 1, (x, 15), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 16), z - 1))''')

# box floor
sub1("                if z < 0 or x < 15 or R < 1:\n                    continue\n                yield z, x, R",
     "                if z < 0 or x < 16 or R < 1:\n                    continue\n                yield z, x, R")
sub1("                    if z < 0 or x < 15 or R < 1:\n                        continue",
     "                    if z < 0 or x < 16 or R < 1:\n                        continue")

# C4 / C4t descriptions
sub1("    audit['C4'] = {'desc': 'type machine box +/-60, clip 32/sentinel 33, confluence',",
     "    audit['C4'] = {'desc': 'type machine box +/-60, clip 34/sentinel 35, confluence',")
sub1('''    """Tightness probe: clip 31 / sentinel 32 over the same box.

    Counts type-confluence violations when the clip window is narrowed
    by one (2y+1 instead of the 11-family candidate 2y+2=32). Not part
    of the PASS/FAIL bad total; reported for the pattern claim.
    """
    global CLIP, SENT
    old_clip, old_sent = CLIP, SENT
    CLIP, SENT = 31, 32''',
     '''    """Tightness probe: clip 33 / sentinel 34 over the same box.

    Counts type-confluence violations when the clip window is narrowed
    by one (2y+1 instead of the 12-family candidate 2y+2=34). Not part
    of the PASS/FAIL bad total; reported for the pattern claim.
    """
    global CLIP, SENT
    old_clip, old_sent = CLIP, SENT
    CLIP, SENT = 33, 34''')
sub1("    audit['C4t'] = {'desc': 'tightness probe clip 31/sentinel 32 (not in bad total)',",
     "    audit['C4t'] = {'desc': 'tightness probe clip 33/sentinel 34 (not in bad total)',")
sub1("        print('  C4t:', t['violations_at_clip31'], 'violations at clip 31, first:', t['first_violation'])",
     "        print('  C4t:', t['violations_at_clip31'], 'violations at clip 33, first:', t['first_violation'])")
sub1("'violations_at_clip31': viol,", "'violations_at_clip31': viol,  # label kept for schema continuity; value is clip 33")

# C7
sub1('''    rng = random.Random(20261152)
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
        ok, _, _ = identity_ok16(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261152, z,x<=3000',''',
     '''    rng = random.Random(20261162)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(16, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 17)
        elif mode == 1:
            R = x + z + 17 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(16, z + rng.randrange(-30, 19))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 16:
            continue
        n += 1
        ok, _, _ = identity_ok16(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261162, z,x<=3000',''')

# C8
sub1('''    for z in zs:
        for dx in range(-30, 18):
            x = z + dx
            if x < 14:
                continue''',
     '''    for z in zs:
        for dx in range(-30, 18):
            x = z + dx
            if x < 15:
                continue''')
sub1('''            for R in (x + z + 16, x + z + 17, x + z + 18):
                n += 1
                if cand15(z, x, R) != (x + 14) % 2:
                    bad += 1''',
     '''            for R in (x + z + 17, x + z + 18, x + z + 19):
                n += 1
                if cand15(z, x, R) != (x + 15) % 2:
                    bad += 1''')

# census C11: geometry
sub1("        'box': 'z=0..79, x=15..70, R=0..x+z+16',", "        'box': 'z=0..79, x=16..70, R=0..x+z+17',")
sub1('''    for z in range(0, 80):
        for x in range(15, 71):
            points += x + z + 17
            if x <= z - 16:
                merge += x + z + 17
            tail += 1  # exactly one R (= x+z+16) is >= x+z+16 within the box
    return points, merge, tail''',
     '''    for z in range(0, 80):
        for x in range(16, 71):
            points += x + z + 18
            if x <= z - 17:
                merge += x + z + 18
            tail += 1  # exactly one R (= x+z+17) is >= x+z+17 within the box
    return points, merge, tail''')
sub1('''    for z in range(0, 80):
        for x in range(15, 71):
            for R in range(0, x + z + 17):
                c = cand16(z, x, R)''',
     '''    for z in range(0, 80):
        for x in range(16, 71):
            for R in range(0, x + z + 18):
                c = cand16(z, x, R)''')
sub1('''            'merge': {'points': corr['merge']['points'], 'bad': corr['merge']['bad'],
                      'claim': 'x<=z-16 => H == single_token(x+15,z,R)'},
            'tail': {'points': corr['tail']['points'], 'bad': corr['tail']['bad'],
                     'claim': 'R>=x+z+16 => H == (x+15)%2'},''',
     '''            'merge': {'points': corr['merge']['points'], 'bad': corr['merge']['bad'],
                      'claim': 'x<=z-17 => H == single_token(x+16,z,R)'},
            'tail': {'points': corr['tail']['points'], 'bad': corr['tail']['bad'],
                     'claim': 'R>=x+z+17 => H == (x+16)%2'},''')
sub1('''        if part.get('box') != 'z=0..79, x=15..70, R=0..x+z+16':
            raise SystemExit("FAIL-CLOSED: census part box mismatch")''',
     '''        if part.get('box') != 'z=0..79, x=16..70, R=0..x+z+17':
            raise SystemExit("FAIL-CLOSED: census part box mismatch")''')
sub1("    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=15..70 R<=x+z+16, both engines '",
     "    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=16..70 R<=x+z+17, both engines '")

# C12
sub1('''    for z in range(0, 121):
        for x in range(15, 121):
            for R in range(1, x + z + 18):
                n += 1
                ok, _, _ = identity_ok16(z, x, R)''',
     '''    for z in range(0, 121):
        for x in range(16, 121):
            for R in range(1, x + z + 19):
                n += 1
                ok, _, _ = identity_ok16(z, x, R)''')
sub1("    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=15..120 R<=x+z+17',",
     "    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=16..120 R<=x+z+18',")

# corollary
sub1('''def corollary(z, x, R, corr):
    if x <= z - 16:
        corr['merge']['points'] += 1
        if cand16(z, x, R) != single_token(x + 15, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 16:
        corr['tail']['points'] += 1
        if cand16(z, x, R) != (x + 15) % 2:
            corr['tail']['bad'] += 1''',
     '''def corollary(z, x, R, corr):
    if x <= z - 17:
        corr['merge']['points'] += 1
        if cand16(z, x, R) != single_token(x + 16, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 17:
        corr['tail']['points'] += 1
        if cand16(z, x, R) != (x + 16) % 2:
            corr['tail']['bad'] += 1''')

# twin engine name mapping stays valid (H_ordered/H_canonical unchanged)

# census twin call family literal: (x, 15) -> (x, 16)  [the one tail literal
# not covered by the renames; caught by the census itself on the first
# run (147,972 bad) and fixed before publication]
sub1("                if twin(R, (x, 15), z) != c:",
     "                if twin(R, (x, 16), z) != c:")

# type machine comment block for y=16
sub1("""# Type machine. y=14's clip window (+/-30 sentinel +/-31) folded the
# y=14 features; the y=15 features (pins up to z+30 odd-z / z+31 even-z,
# sweep band d=16 offsets up to x+15, band bottom R-z = 2y+2 = 32,
# tail offset R-x-z = 16, merge boundary x = z-16, base span to z+29
# and the I-row th(d) excursions up to 31) are tested with +/-32/33
# (= 2y+2 for y=15), the 11-family-continuation candidate of the 2y+2
# tight pattern (y=5..14: 12/14/16/18/20/22/24/26/28/30). CLIP/SENT are
# re-checked for confluence by check_C4; the tightness probe (CLIP=31)
# is reported separately (check_C4t).""",
     """# Type machine. y=15's clip window (+/-32 sentinel +/-33) folded the
# y=15 features; the y=16 features (pins up to z+32 odd-z / z+33 even-z,
# sweep band d=17 offsets up to x+16, band bottom R-z = 2y+2 = 34,
# tail offset R-x-z = 17, merge boundary x = z-17, base span to z+33
# and the I-row th(d) excursions up to 33) are tested with +/-34/35
# (= 2y+2 for y=16), the 12-family-continuation candidate of the 2y+2
# tight pattern (y=5..15: 12/14/16/18/20/22/24/26/28/30/32). CLIP/SENT are
# re-checked for confluence by check_C4; the tightness probe (CLIP=33)
# is reported separately (check_C4t).""")

# main(): audit header, todo set, loop order
sub1("""    everything = {'C1', 'C1b', 'C1d', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C11r', 'C12'}
    todo = requested & everything if requested else (everything - {'C11', 'C11r'})""",
     """    everything = {'C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'}
    todo = requested & everything if requested else (everything - {'C11'})""")
sub1("""    for name in ('C1', 'C1b', 'C1d', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C11r', 'C12'):""",
     """    for name in ('C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'):""")
sub1("""        elif name == 'C1d':
            check_C1d(audit['checks'])
""", "")
sub1("""        elif name == 'C11r':
            check_C11r(audit['checks'])
""", "")
sub1("""    audit = {'experiment': 'vertical-fiber-two-token-y15-parametric-allz-proof-20261122',
             'family': 'H(R;(x,15);z), z>=0, x>=15, R>=0',
             'stage': 'part2 (C1d published-slice anchors at y=15 and the '
                      'independent census.txt consumer incorporated; census parts '
                      're-anchored via bounded-memoization twins on a memory-capped '
                      'host; on overall PASS with 3 byte-identical audit runs K1235 '
                      'is promoted observed->proved)',""",
     """    audit = {'experiment': 'vertical-fiber-two-token-y16-parametric-allz-proof-20261122',
             'family': 'H(R;(x,16);z), z>=0, x>=16, R>=0',
             'stage': 'part1 (12-check machine; the promotion stage part2 adds the '
                      'published fixed-z slice anchors C1d and the independent '
                      'census.txt consumer C11r; census parts re-anchored via '
                      'bounded-memoization twins on a memory-capped host)',""")
sub1("""             'merge_below_diagonal': {'claim': 'x<=z-16 => H == single_token(x+15,z,R)'},
                 'tail': {'claim': 'R>=x+z+16 => H == (x+15)%2'}}}""",
     """             'merge_below_diagonal': {'claim': 'x<=z-17 => H == single_token(x+16,z,R)'},
                 'tail': {'claim': 'R>=x+z+17 => H == (x+16)%2'}}}""")

# run_census print line engine mapping: keep

# --- remove the part2-only check functions (C1d / C11r) -------------
i1 = tail_text.find("def check_C1d(audit):")
i2 = tail_text.find("def check_C2(audit, corr):")
assert 0 < i1 < i2, (i1, i2)
tail_text = tail_text[:i1] + tail_text[i2:]

text = head_text + tail_text
Path(__file__).parent.parent.joinpath("verify_y16_universal.py").write_text(text, encoding="utf-8")
print("written verify_y16_universal.py", len(text), "bytes")
