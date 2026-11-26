# kit-18x: independent blind second census of the kit-18 registered rows (m51/m52 frontier cross-check)

## What this is

An independent blind second census of the 49 rows registered for kit-18 (the
`strip-newband` m=51/m=52 frontier + m=49/m=50 windows + m19..m32 ladder
next-depth + even-m z=3m+16 rows), built and measured by a fresh harness in a
separate lane session while the concurrent kit-18 build was in progress.
This census was **frozen and audited before any kit-18 output was read**; the
concurrent kit-18 explorer source and its frozen output were never used for
registration or measurement.

Registration authority: the published kit-17 frozen `.out`
(sha256 `420d1c83...`, commit `f90d5d5e`), section
`future_slice_registration_constants` (34 items) plus its window proposals
(m=49 z{89..96} / m=50 z{90..97}) and the even-m z=3m+16 continuation
(NON-BINDING, contingent on the published kit-17 z=3m+14 rows measuring
EXACT, which the harness validation pass confirms from the published kit-17
`.out` itself). Nothing was registered from any unpublished source.

## Pins

| file | sha256 |
| --- | --- |
| engine_block.py (published byte-clone) | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` |
| engine startup pin (published kit-17 engine_gate) | `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92` |
| published kit-17 frozen .out (registration source) | `420d1c83350e5a1c38d1282fa974a3e91d3e50ddd26d82b4c069ea82c4367d95` |
| census_kit18x.py | `58b8e3aa81d5fa1f9dd6ccedd55dc0501b14edd9f1b4a94933d568d7add78350` |
| census_kit18x.out (frozen) | `97b6ebef02b290d7f047722f997dc4ec8b6cee8e65bce3fc0cd18bfbf287c776` |
| audit_kit18x.py | `7cb3fee4db12f76ec2b82bc96dad01da0cb855dacecd8d30a562a07fee355768` |
| tamper_kit18x.py | `0a17abf2a7dd8eb4399dbe94b084e6dac4fdc30e8d5a155172efd860a5e66f72` |

## Method and independence statement

- Row semantics were independently reconstructed and validated: the harness
  reproduced ALL 49 published kit-17 rows (shape counts and separation
  content, order-independent) BEFORE any kit-18 row was measured.
- The harness implementation is fresh (nested-loop enumeration, no `parts()`
  recursion, no transform of any published explorer). The concurrent kit-18
  explorer source was never read by this lane; its local frozen artifact was
  read only AFTER this census froze, as an informational (non-authoritative)
  comparison (see Honest disclosure).
- Engine is the published `engine_block.py` byte-clone (SSOT), with per-S
  `H_canonical.cache_clear()` (memory-safety, values unchanged).
- Determinism: the audit's checkpointed full live recompute of all 49 census
  rows reproduced the frozen census content identically (49/49, order
  independent), on top of the incremental census checkpoint file.

## Results (all finite observations)

- **Frontier 38th datum: m=51@z=101 R=153: {51,52}@S=103 UP 2v0 EXACT**
  (independently confirmed blind; parity scaffold observation count 40/40,
  m=13..52; first-ever m>50 row).
- **Frontier 39th datum: m=52@z=102 R=155: (52,52)@S=104 UP 2v1 EXACT**
  (independently confirmed; first-ever m>51 row).
- Windows m=49 z{89..96}, m=50 z{90..97}: 16/16 CLEAN (0 separations each).
- 28 ladder next-depth rows (m19..m32 one-past + birth): all registered
  prediction seats FULL HIT in the blind census (43 named seats verified by
  the audit gate G5, including stick/NEW seats and conform-DEAD absences);
  m19/m20 birth rows at z=77/78 are the new series deepest observations.
- Even-m lifecycle z=3m+16 (m=14 z=58, m=16 z=64, m=18 z=70): 3/3 EXACT
  (stick {m,2m+16} DOWN 0v2 + NEW {m,2m+18} UP 2v1 + shadows; 21 separations
  per row, all conforming to the parity-flipped template).
- Census totals: 49 rows / 241 separations.

## Independent audit (fresh implementation, 10 gates)

`audit_kit18x.py` re-implements the fail-closed checks with a checkpointed
live recompute (G2 spot-validates 13 published kit-17 rows; G8 recomputes all
49 census rows live and compares with the frozen census):

```
G0 kit-17 sha PASS   G1 engine gate PASS   G2 harness validation PASS (13 spot rows)
G3 row set PASS (exactly the registration)   G4 frontier exact PASS
G5 binding hits PASS (43 seats, 0 fails)   G6 windows PASS (16 clean)
G7 evenlife template PASS   G8 full recompute PASS 49/49
G9 totals PASS (49 rows / 241 seps)     AUDIT-PASS
```

Tamper battery 3/3 fail-closed (tamper_kit18x.py): T1 frontier separation
value flip in the frozen census -> G4+G8 FAIL, T2 phantom separation injected
into a clean window row -> G6+G8 FAIL, T3 audit recompute entry value flip ->
G8 FAIL; post-restore clean control rc=0 and the frozen census byte-identical
(sha256 re-verified).

## Honest disclosure

1. The authoritative cross-check against the kit-18 record of record is
   **pending**: at the time this census froze and was published, the
   concurrent kit-18 build had not published its frozen `.out` to main. After
   this census froze, an **informational** comparison against the concurrent
   lane's local (unpublished, subject-to-change) frozen artifact matched
   49/49 rows exactly (shapes, R, and all 241 separations). This comparison
   is not a record-of-record cross-check; the next execution should compare
   this census against the published kit-17 frozen `.out`'s successor (the
   published kit-18 frozen `.out`) once it reaches main.
2. One argument-passing slip occurred while driving the census in chunks
   (`census census18.json 27 49` was parsed with the start index as the
   output path); the resulting empty stray file was deleted and the run
   restarted with the correct arguments. No measurement was affected; the
   incremental census file is the one whose rows the audit recomputed.
3. The audit's G2 gate recomputes a 13-row subset (every 4th row) of the
   published kit-17 rows rather than all 49 (290s-wall chunking); the full
   49/49 pre-measurement validation is recorded in the census script's
   `validate` mode run (VALIDATE 49/49 ok, bad=[]).
4. All pins are machine-extracted (sha256sum); no hand-typed 64-hex constant
   was entered except by copying from `sha256sum` output.

## Standing claims status

Standard 11x11 empty board, all 19 central-reply roots, the two-stone root
{60,27}, the third move {100,108}, S2, and closure classes 1/2/4 remain
UNKNOWN at all times. No verdict is consumed. The frontier parity scaffold
count (40/40), the rule v2 shadows, the early-follow observations, and the
even-m lifecycle template are finite observations, not laws. No K-slot claim
is made.
