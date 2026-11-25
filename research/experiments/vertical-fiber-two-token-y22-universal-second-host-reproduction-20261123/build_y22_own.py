#!/usr/bin/env python3
"""Sibling-lane independent build of verify_y22_universal.py.

Per the y=22 single-owner declaration note (commit e1e60cd4) and the
published single-edition transformation procedure (the same procedure the
y=19 -> y=20 -> y=21 -> y=22 machines inherited), this builder starts from
the published y=21 machine (git blob ca5e8284, SHA-256 0ab841d9...) and
applies the y=22 spec constants:

  - family H(R;(x,22);z), x >= 22; merge x <= z-23 => single_token(x+22,z,R);
    tail R >= x+z+23 => (x+22) % 2;
  - B-child: published cand21 (K1248 proved, series-first proved-universal
    B-child), block-local word-boundary rename Y -> Y21; A-child x=22 merger
    (21,22)==(22,21) -> cand21(z,22,R-1); C-child 1 xor cand22(z-1,x,R-1);
  - claim cand22 verbatim from the published cand22.py table block;
  - type machine CLIP, SENT = 2y+2, +1 = 46, 47; tightness probe 45, 46;
  - C7 seed 20261222 (series 20261192 / 20261202 / 20261212 / 20261222);
  - census geometry z=0..79, x=22..70 (80*49 rows), R<=x+z+23, C11r
    R=0..x+z+24, RBUF 24; C1 x=22..40 R<=x+z+53; C1b child x=21..34
    R<=x+z+36, merger R<=z+50; C2 x=22..64 R<=x+z+48; C2b x=22..76 step 5;
    C12 z<=120 x=22..120 R<=x+z+24; C8 dx crop x<21, dx in [-30,23],
    window (x+z+23, +24, +25), y=21 B-child tail claim at x>=21;
  - C1d anchors at the y=22 rows (x=22..159), low-R z=15..17.

Fail-closed: every replacement is asserted to occur with its expected
count before it is applied; any miss aborts the build.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
Y21M = ROOT / "repo/research/experiments/vertical-fiber-two-token-y21-universal-proof-20261123/verify_y21_universal.py"
C21 = ROOT / "repo/research/experiments/vertical-fiber-two-token-y21-parametric-fit-20261123/cand21.py"
C22 = ROOT / "repo/research/experiments/vertical-fiber-two-token-y22-parametric-fit-20261123/cand22.py"
OUT = HERE / "verify_y22_universal.py"

NEW_DOCSTRING = '''"""
Universal verifier for the y=22 two-token residual family.

Family: H(R; (x,22); z), all z >= 0, all x >= 22, all R >= 0.
Claim under test (K1256, observed at build time; promoted proved by the
published single-host run -- this is the sibling-lane independent build
of the same machine per the declaration recipe): the closed form cand22
equals H everywhere; with corollaries
  merge-below-diagonal (y=22 promotion of the y=12..y=21 lines):
       x <= z-23  =>  H == single_token(x+22, z, R)
  tail:                                 R >= x+z+23  =>  H == (x+22) % 2

Sibling-lane independent reproduction build (second host, 2026-11-23):
constructed from the published y=21 machine (git blob ca5e8284) by the
published single-edition transformation procedure with the y=22 constants
of the declaration note research/log/2026-11-23-y22-universal-verifier-
single-owner-note.md (commit e1e60cd4), with the three transcription
blocks taken verbatim from the published sources (engine: the y=21
machine's engine block; cand21: the published cand21.py table block with
the block-local Y -> Y21 rename; cand22: the published cand22.py table
block). AST-compared against the published verify_y22_universal.py
(SHA-256 96d9787f...): identical syntax tree modulo this module
docstring and comment text; the transcription blocks are byte-equal.

Run modes are unchanged from the published machine:
  python3 verify_y22_universal.py                 # all checks except C11,
                                                  # C11r
  python3 verify_y22_universal.py C11ordered      # census part 1 (slow)
  python3 verify_y22_universal.py C11canonical    # census part 2 (slow)
  python3 verify_y22_universal.py C11             # C11 only
  python3 verify_y22_universal.py C1 C2 ...       # explicit check list
"""

'''


def src_block(text: str, start_lit: str, end_marker: str) -> str:
    lines = text.split("\n")
    i_start = next(i for i, l in enumerate(lines) if l == start_lit)
    i_end = next(i for i, l in enumerate(lines)
                 if l.startswith(end_marker) and i > i_start)
    return "\n".join(lines[i_start:i_end]).rstrip("\n") + "\n"


def machine_block_span(text: str, marker: str):
    lines = text.split("\n")
    i_start = next(i for i, l in enumerate(lines)
                   if l == f"# @@TRANSCRIPTION-{marker}-START@@")
    i_end = next(i for i, l in enumerate(lines)
                 if l == f"# @@TRANSCRIPTION-{marker}-END@@" and i > i_start)
    return i_start, i_end


def main() -> int:
    y21 = Y21M.read_text(encoding="utf-8")
    c21 = C21.read_text(encoding="utf-8")
    c22 = C22.read_text(encoding="utf-8")

    # --- 1. module docstring: replace with the sibling-build docstring ---
    m = re.match(r'^(#!.*?\n)?("""(?:.|\n)*?"""\n)', y21, re.DOTALL)
    assert m, "module docstring not found"
    body = y21[m.end(2):]

    # --- 2. splice transcription blocks out as placeholders ---
    spans = {}
    for marker in ("ENGINE", "CAND20", "CAND21"):
        i0, i1 = machine_block_span(body, marker)
        spans[marker] = (i0, i1)
    assert spans["ENGINE"][1] < spans["CAND20"][0] < spans["CAND20"][1] < spans["CAND21"][0]
    lines = body.split("\n")
    # engine block stays verbatim inside seg_pre; only cand blocks spliced.
    new_b = ["# @@TRANSCRIPTION-CAND21-START@@",
             re.sub(r"\bY\b", "Y21", src_block(c21, "Y = 21", "def main")).rstrip("\n"),
             "# @@TRANSCRIPTION-CAND21-END@@"]
    new_c = ["# @@TRANSCRIPTION-CAND22-START@@",
             src_block(c22, "Y = 22", "def main").rstrip("\n"),
             "# @@TRANSCRIPTION-CAND22-END@@"]
    seg_pre = lines[:spans["CAND20"][0]]
    seg_mid = lines[spans["CAND20"][1] + 1:spans["CAND21"][0]]
    seg_suf = lines[spans["CAND21"][1] + 1:]
    joined = "\n".join(seg_pre) + "\n@@B@@\n" + "\n".join(seg_mid) + "\n@@C@@\n" + "\n".join(seg_suf)

    # --- 3. word-boundary renames FIRST (y=21 machine role renames) ---
    #     cand21 (claim) -> cand22; cand20 (B-child) -> cand21;
    #     in_T20/in_P20 (B-child helpers) -> in_T21/in_P21 outside blocks;
    #     opts/identity_ok/type_of suffixed 21 -> 22.
    for pat, repl, cnt in [
        (r"\bin_P20\b", "in_P21", 1),
        (r"\bin_T20\b", "in_T21", 1),
        (r"\bcand21\b", "cand22", None),
        (r"\bcand20\b", "cand21", None),
        (r"\bopts21\b", "opts22", None),
        (r"\bidentity_ok21\b", "identity_ok22", None),
        (r"\btype_of21\b", "type_of22", None),
    ]:
        joined, n = re.subn(pat, repl, joined)
        if cnt is not None:
            assert n == cnt, f"rename {pat}: {n} != {cnt}"
        else:
            assert n > 0, f"rename {pat}: zero occurrences"
        print(f"rename {pat}: {n}")

    # --- 4. constant/context replacement table (post-rename forms) ---
    replacements = [
        # C1
        ("for x in range(21, 40):", "for x in range(22, 41):", 1),
        ("for R in range(0, x + z + 53):", "for R in range(0, x + z + 54):", 1),
        ("if H_ordered(R, (x, 21), z) != c or H_canonical(R, (x, 21), z) != c:",
         "if H_ordered(R, (x, 22), z) != c or H_canonical(R, (x, 22), z) != c:", 1),
        ("'raw both engines vs cand22 z=0..14 x=21..39 R<=x+z+52'",
         "'raw both engines vs cand22 z=0..14 x=22..40 R<=x+z+53'", 1),
        # C1b
        ("for x in range(20, 34):", "for x in range(21, 35):", 1),
        ("for R in range(0, x + z + 36):", "for R in range(0, x + z + 37):", 1),
        ("if H_ordered(R, (x, 20), z) != cand21(z, x, R):",
         "if H_ordered(R, (x, 21), z) != cand21(z, x, R):", 1),
        ("for R in range(1, z + 50):", "for R in range(1, z + 51):", 1),
        ("a = H_ordered(R - 1, (20, 21), z)", "a = H_ordered(R - 1, (21, 22), z)", 1),
        ("b = H_ordered(R - 1, (21, 20), z)", "b = H_ordered(R - 1, (22, 21), z)", 1),
        ("c = H_canonical(R - 1, (20, 21), z)", "c = H_canonical(R - 1, (21, 22), z)", 1),
        ("if a != b or a != c or a != cand21(z, 21, R - 1):",
         "if a != b or a != c or a != cand21(z, 22, R - 1):", 1),
        ("'single_token/y=20-child/x=21 merger raw anchors'",
         "'single_token/y=21-child/x=22 merger raw anchors'", 1),
        ("'closed identity grid z=0..48 x=21..63 R<=x+z+47 (+merge,tail)'",
         "'closed identity grid z=0..48 x=22..64 R<=x+z+48 (+merge,tail)'", 1),
        # C2
        ("for x in range(21, 64):", "for x in range(22, 65):", 1),
        ("for R in range(1, x + z + 48):", "for R in range(1, x + z + 49):", 1),
        # C2b
        ("for x in range(21, 76, 5):", "for x in range(22, 77, 5):", 1),
        ("if not ok or (R >= x + z + 22 and cand22(z, x, R) != (x + 21) % 2):",
         "if not ok or (R >= x + z + 23 and cand22(z, x, R) != (x + 22) % 2):", 1),
        ("'deep tail identity rows z in {60..400} x=21..71(step5) R<=x+z+31'",
         "'deep tail identity rows z in {60..400} x=22..76(step5) R<=x+z+31'", 1),
        # C3
        ("for x in range(21, 26):", "for x in range(22, 27):", 1),
        ("if x > 21:", "if x > 22:", 1),
        ("raw_opts.add(H_ordered(R - 1, (x - 1, 21), z))",
         "raw_opts.add(H_ordered(R - 1, (x - 1, 22), z))", 1),
        ("raw_opts.add(H_ordered(R - 1, (20, 21), z))",
         "raw_opts.add(H_ordered(R - 1, (21, 22), z))", 1),
        ("raw_opts.add(H_ordered(R - 1, (x, 20), z))",
         "raw_opts.add(H_ordered(R - 1, (x, 21), z))", 1),
        ("raw_opts.add(1 ^ H_ordered(R - 1, (x, 21), z - 1))",
         "raw_opts.add(1 ^ H_ordered(R - 1, (x, 22), z - 1))", 1),
        # opts: the x=Y merger branch constants
        ("if x == 21:\n        A = cand21(z, 21, R - 1)",
         "if x == 22:\n        A = cand21(z, 22, R - 1)", 1),
        # C4 / C4t
        ("return (1 if x == 21 else 0,", "return (1 if x == 22 else 0,", 1),
        ("if z < 0 or x < 21 or R < 1:", "if z < 0 or x < 22 or R < 1:", 2),
        ("'type machine box +/-60, clip 44/sentinel 45, confluence'",
         "'type machine box +/-60, clip 46/sentinel 47, confluence'", 1),
        ("CLIP, SENT = 44, 45", "CLIP, SENT = 46, 47", 1),
        ("CLIP, SENT = 43, 44", "CLIP, SENT = 45, 46", 1),
        ("'tightness probe clip 43/sentinel 44 (not in bad total)'",
         "'tightness probe clip 45/sentinel 46 (not in bad total)'", 1),
        ("'violations_at_clip43': viol,", "'violations_at_clip45': viol,", 1),
        # C7
        ("rng = random.Random(20261212)", "rng = random.Random(20261222)", 1),
        ("x = rng.randrange(21, 3001)", "x = rng.randrange(22, 3001)", 1),
        ("R = rng.randrange(1, x + z + 22)", "R = rng.randrange(1, x + z + 23)", 1),
        ("R = x + z + 22 + rng.randrange(-3, 4)", "R = x + z + 23 + rng.randrange(-3, 4)", 1),
        ("x = max(21, z + rng.randrange(-30, 24))", "x = max(22, z + rng.randrange(-30, 25))", 1),
        ("if R < 1 or x < 21:", "if R < 1 or x < 22:", 1),
        ("'seeded far probes 200k, seed 20261212, z,x<=3000'",
         "'seeded far probes 200k, seed 20261222, z,x<=3000'", 1),
        # C8
        ("for dx in range(-30, 23):", "for dx in range(-30, 24):", 1),
        ("if x < 20:", "if x < 21:", 1),
        ("for R in range(1, x + z + 36):", "for R in range(1, x + z + 37):", 1),
        ("for R in (x + z + 22, x + z + 23, x + z + 24):",
         "for R in (x + z + 23, x + z + 24, x + z + 25):", 1),
        ("if cand21(z, x, R) != (x + 20) % 2:", "if cand21(z, x, R) != (x + 21) % 2:", 1),
        ("'boundary manifolds z<=3000, dx in [-30,22], tail window'",
         "'boundary manifolds z<=3000, dx in [-30,23], tail window'", 1),
        # C1d
        ("for x in range(21, 160):", "for x in range(22, 160):", 2),
        ("if fn(x, 21, r) != cand22(z0, x, r):", "if fn(x, 22, r) != cand22(z0, x, r):", 1),
        ("if cand22(z0, x, R) != single_token(x + 21, z0, R):",
         "if cand22(z0, x, R) != single_token(x + 22, z0, R):", 1),
        ("slices (y=21) '", "slices (y=22) '", 1),
        ("x=21..159 R<=x+61", "x=22..159 R<=x+61", 1),
        # C11r
        ("values = [cand22(z, x, R) for R in range(0, x + z + 24)]",
         "values = [cand22(z, x, R) for R in range(0, x + z + 25)]", 1),
        ("tail = (x + 21) % 2", "tail = (x + 22) % 2", 1),
        ("if rows != 80 * 50:", "if rows != 80 * 49:", 1),
        ('raise SystemExit(f"FAIL-CLOSED: census rows {rows} != 4000")',
         'raise SystemExit(f"FAIL-CLOSED: census rows {rows} != 3920")', 1),
        ("R=0..x+z+23, '", "R=0..x+z+24, '", 1),
        ("x=21..70 (T/P sets", "x=22..70 (T/P sets", 1),
        # C11 census twin
        ("for x in range(21, 71):", "for x in range(22, 71):", 2),
        ("points += x + z + 23", "points += x + z + 24", 1),
        ("if x <= z - 22:", "if x <= z - 23:", 2),
        ("merge += x + z + 23", "merge += x + z + 24", 1),
        ("for R in range(0, x + z + 23):", "for R in range(0, x + z + 24):", 1),
        ("if twin(R, (x, 21), z) != c:", "if twin(R, (x, 22), z) != c:", 1),
        ("'box': 'z=0..79, x=21..70, R=0..x+z+22',",
         "'box': 'z=0..79, x=22..70, R=0..x+z+23',", 1),
        ("part.get('box') != 'z=0..79, x=21..70, R=0..x+z+22'",
         "part.get('box') != 'z=0..79, x=22..70, R=0..x+z+23'", 1),
        ("'raw census anchor z=0..79 x=21..70 R<=x+z+22, both engines '",
         "'raw census anchor z=0..79 x=22..70 R<=x+z+23, both engines '", 1),
        ("x<=z-22 => H == single_token(x+21,z,R)",
         "x<=z-23 => H == single_token(x+22,z,R)", 2),
        ("R>=x+z+22 => H == (x+21)%2",
         "R>=x+z+23 => H == (x+22)%2", 2),
        # C12
        ("for x in range(21, 121):", "for x in range(22, 121):", 1),
        ("for R in range(1, x + z + 24):", "for R in range(1, x + z + 25):", 1),
        ("'deep closed grid z=0..120 x=21..120 R<=x+z+23'",
         "'deep closed grid z=0..120 x=22..120 R<=x+z+24'", 1),
        # corollary helper
        ("if cand22(z, x, R) != single_token(x + 21, z, R):",
         "if cand22(z, x, R) != single_token(x + 22, z, R):", 1),
        ("if R >= x + z + 22:", "if R >= x + z + 23:", 1),
        ("if cand22(z, x, R) != (x + 21) % 2:",
         "if cand22(z, x, R) != (x + 22) % 2:", 1),
        # main audit dict
        ("'experiment': 'vertical-fiber-two-token-y21-universal-proof-20261123'",
         "'experiment': 'vertical-fiber-two-token-y22-universal-proof-20261123'", 1),
        ("'family': 'H(R;(x,21);z), z>=0, x>=21, R>=0'",
         "'family': 'H(R;(x,22);z), z>=0, x>=22, R>=0'", 1),
        ("anchors at the y=21 rows, pre-flighted fail-closed ",
         "anchors at the y=22 rows, pre-flighted fail-closed ", 1),
        ("the y=21 single-owner declaration; census parts anchored ",
         "the y=22 single-owner declaration; census parts anchored ", 1),
        # final print
        ("print('  C4t:', t['violations_at_clip43'], 'violations at clip 43, first:', t['first_violation'])",
         "print('  C4t:', t['violations_at_clip45'], 'violations at clip 45, first:', t['first_violation'])", 1),
    ]

    for old, new, cnt in replacements:
        got = joined.count(old)
        assert got == cnt, f"replacement count mismatch: {got} != {cnt} for {old!r}"
        joined = joined.replace(old, new)

    # --- 5. splice new blocks back ---
    joined = joined.replace("@@B@@", "\n".join(new_b))
    joined = joined.replace("@@C@@", "\n".join(new_c))

    out_text = "#!/usr/bin/env python3\n" + NEW_DOCSTRING + joined
    if not out_text.endswith("\n"):
        out_text += "\n"
    OUT.write_text(out_text, encoding="utf-8")
    print(f"wrote {OUT} ({len(out_text.encode())} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
