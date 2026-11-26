# strip-sixthwave-z35-z39 micro-kit (2026-11-26)

Frozen pre-declaration micro-census executing the fifth-wave micro-kit
(commit `c66b9022`) log S5 handoffs: item #1 the six TWO-PAST +
NEW-WAVE rows (including the FIRST d=5 seats for m=13/m=14 and the
FIRST d=2 seats for m=17/m=18), item #2 the six ONE-PAST ladder rows
(measuring SIX birth+3 deaths, datums 16-21, including the DEFERRED
(14,20) death at z=35), item #3 the m=18/m=17 base-spot z=32 touch,
item #4 the k=43/k=44 tail supply pre-computations.

## Files

| file | sha256 | size |
|---|---|---|
| `explore_sixthwave_z35_z39.py` | `5ed30a19d6e1f8168697ec2e0231e17918fbedf0b5c58f1857c70f1457e17a08` | 30041 B |
| `engine_block.py` | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` | 2540 B |
| `explore_sixthwave_z35_z39.out` | `7d2c28b935cad1f4ad93d88c125ada85d770025ec8f624a04ffa31a602b8d044` | 26119 B |

`engine_block.py` byte-identical to the series engine (pin
`bd5f22e4…`), embedded and asserted inside the explore script
(engine_gate PASS).

## Reproduce

```sh
python3 explore_sixthwave_z35_z39.py > outfile
cmp outfile explore_sixthwave_z35_z39.out
```

Determinism: 6/6 byte-identical runs (default x3,
`PYTHONHASHSEED=random`, `env -i` isolated-dir x2), ~17 s per run.
K0832 battery 78/78. Post-freeze ordered-engine audit: 44/44
positions (18 new row separations + 4 touches + 22 recheck anchors)
identical.

## Headline results (finite machine observations)

- ALL TWELVE ROWS measure EXACTLY the frozen predictions — separation
  count, shape, engine value and direction, 18 predicted separations
  and exactly those 18 measured:
  - 6 TWO-PAST + NEW-WAVE rows, each EXACTLY TWO separations (stick +
    newborn): m=13 @z=35 {13,22}@S=35 DOWN 1v2 + NEW {13,24}@S=37 UP
    2v0 (d=5 seat, gap 11, the FIRST sixth-wave birth of the series);
    m=15 @z=37 {15,22}@S=37 DOWN 1v2 + NEW {15,24}@S=39 UP 2v0 (d=4
    seat, gap 9); m=14 @z=36 (14,22)@S=36 DOWN 0v2 + NEW (14,24)@S=38
    UP 2v1 (d=5 seat, gap 10); m=16 @z=38 (16,22)@S=38 DOWN 0v2 + NEW
    (16,24)@S=40 UP 2v1 (d=4 seat, gap 8); m=17 @z=37 {17,20}@S=37
    DOWN 1v2 + NEW {17,22}@S=39 UP 2v0 (d=2 seat, gap 5); m=18 @z=38
    (18,20)@S=38 DOWN 0v2 + NEW (18,22)@S=40 UP 2v1 (d=2 seat, gap
    4) — every new birth again at slot-law shape (m, m+2d+1) odd /
    (m, m+2d) even, born value 2.
  - 6 ONE-PAST ladder rows, each EXACTLY ONE separation (odd 2->1 UP
    1v0: m=13 {13,24}@S=37, m=15 {15,24}@S=39, m=17 {17,22}@S=39;
    even 2->0 DOWN 0v1: m=14 (14,22)@S=36, m=16 (16,24)@S=40,
    m=18 (18,22)@S=40).
- DEATH CURVE 21/21 at birth+3, BOTH parities, across ALL SIX bands
  m in {13..18}, shapes now d in {0..4}: the six new conform-deaths
  are {13,22}@z=36 (the FIRST d=4-shape death), (14,20)@z=35 (the
  DEFERRED death noted in the fifth-wave log S3), {15,22}@z=38,
  (16,22)@z=39, {17,20}@z=38, (18,20)@z=39. Value trajectory 2,1,1,
  dead (odd) / 2,0,0,dead (even) holds through every published slice.
- THE WAVE PROFILE strictly periodic-2 now holds across ALL SIX
  bands m in {13..18} through z <= 39: EXACTLY TWO separations at
  every birth slice z*(m)+2d (d>=1) and EXACTLY ONE at every
  in-between slice over the covered rectangle; rows never empty.
- FOUR first-ever z=32 engine touches ALL CONFORM: x1 = 0 (m=17-row
  z=32 co-token, collapse-conform), y1 = 1 (m=16-row), x3 = 1 and
  x4 = 0 via the frozen option tables (x3 = mex{x1, 0} since the
  published z=31 x3 gives C-child 0; x4 = mex{y1, 1} = 0 iff y1 = 1).
  The m=18 base-spot on-line z-sequence extends to 17 members
  (z=16..32 = 0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1); the m=17 members
  remain all zero through z=32.
- Recheck anchors 22/22 value==published (18 fifth-wave row
  separation values + 4 z=31 touches; `match` is the conform
  criterion, False BY DESIGN for separation anchors — see
  match_field_note).
- k=43 (thirty-fourth tail, ODD) CONFIRMED as registered: hold
  {0}U{12..43}, then UNIFORM 0v1 for ALL s in {44..77} (odd-z supply
  chain candidate 13/13). k=44 (thirty-fifth, EVEN) CONFIRMED: hold
  {0}U{12..43}, break 0v2 at s=44, then UNIFORM 2v1 for ALL s in
  {45..78} (even chain candidate 13/13).

FINITE observations only; no universal statement; no K slot claimed;
11x11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots UNKNOWN, unchanged; no verdict consumed.
