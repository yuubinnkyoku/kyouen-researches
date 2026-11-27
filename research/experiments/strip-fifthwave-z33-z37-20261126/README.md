# strip-fifthwave-z33-z37 micro-kit (2026-11-26)

Frozen pre-declaration micro-census executing the wave-train micro-kit
(commit `69c4009a`, tail-range-corrected) log S5 handoffs: item #1 the
six TWO-PAST + NEW-WAVE rows (including the FIRST m=17 and m=18 second
births), item #2 the six ONE-PAST ladder rows (measuring SIX birth+3
deaths in one kit), item #3 the m=18/m=17 base-spot z=31 touch, item
#4 the k=41/k=42 tail supply pre-computations.

## Files

| file | sha256 | size |
|---|---|---|
| `explore_fifthwave_z33_z37.py` | `036294eff66fb995aedfaf5a45ae5234de037a3fa2a8dc779fd7dc28ab7cdc07` | 28458 B |
| `engine_block.py` | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` | 2540 B |
| `explore_fifthwave_z33_z37.out` | `28a10304ad2f923af12ffda13df34bba6a6bcf0ee18402572d7b5b175b6dbb58` | 24499 B |

`engine_block.py` byte-identical to the series engine (pin
`bd5f22e4…`), embedded and asserted inside the explore script
(engine_gate PASS).

## Reproduce

```sh
python3 explore_fifthwave_z33_z37.py > outfile
cmp outfile explore_fifthwave_z33_z37.out
```

Determinism: 6/6 byte-identical runs (default x3,
`PYTHONHASHSEED=random`, `env -i` isolated-dir x2), ~15 s per run.
K0832 battery 68/68. Post-freeze ordered-engine audit: 40/40
positions (18 new row separations + 4 touches + 18 recheck anchors)
identical.

## Headline results (finite machine observations)

- ALL TWELVE ROWS measure EXACTLY the frozen predictions — separation
  count, shape, engine value and direction, 18 predicted separations
  and exactly those 18 measured:
  - 6 TWO-PAST + NEW-WAVE rows, each EXACTLY TWO separations (stick +
    newborn): m=17 @z=35 {17,18}@S=35 DOWN 1v2 + NEW {17,20}@S=37 UP
    2v0 (FIRST m=17 second birth, gap 3 = 2d+1 with d=1); m=18 @z=36
    (18,18)@S=36 DOWN 0v2 + NEW (18,20)@S=38 UP 2v1 (FIRST m=18 second
    birth, gap 2 = 2d with d=1); m=13 @z=33 {13,20}@S=33 DOWN 1v2 +
    NEW {13,22}@S=35 UP 2v0 (d=4 seat, gap 9); m=14 @z=34 (14,20)@S=34
    DOWN 0v2 + NEW (14,22)@S=36 UP 2v1 (d=4 seat, gap 8); m=15 @z=35
    {15,20}@S=35 DOWN 1v2 + NEW {15,22}@S=37 UP 2v0 (d=3 seat, gap
    7); m=16 @z=36 (16,20)@S=36 DOWN 0v2 + NEW (16,22)@S=38 UP 2v1
    (d=3 seat, gap 6) — every new birth again at shape (m, m+2d+1)
    odd / (m, m+2d) even, born value 2, following the slot law.
  - 6 ONE-PAST ladder rows, each EXACTLY ONE separation (odd 2->1 UP
    1v0: m=13 {13,22}@S=35, m=15 {15,22}@S=37, m=17 {17,20}@S=37;
    even 2->0 DOWN 0v1: m=14 (14,20)@S=34, m=16 (16,22)@S=38,
    m=18 (18,20)@S=38).
- DEATH CURVE 15/15 at birth+3, BOTH parities, now across ALL SIX
  bands m in {13..18}, d in {0..4}: the six new conform-deaths are
  {13,20}@z=34, (14,18)@z=33, {15,20}@z=36, (16,20)@z=37, {17,18}@
  z=36 (FIRST m=17 death), (18,18)@z=37 (FIRST m=18 death). Value
  trajectory 2,1,1,dead (odd) / 2,0,0,dead (even) holds through
  every published slice.
- THE WAVE PROFILE strictly periodic-2 now holds across ALL SIX
  bands m in {13..18} through z <= 37: EXACTLY TWO separations at
  every birth slice z*(m)+2d (d>=1) and EXACTLY ONE at every
  in-between slice over the covered rectangle; rows never empty.
- FOUR first-ever z=31 engine touches ALL CONFORM: x1 = 0 (m=17-row
  z=31 co-token, collapse-conform), y1 = 1 (m=16-row), x3 = 1 and
  x4 = 0 via the frozen option tables (x3 = mex{x1, 0} since
  1^w3 = 0; x4 = mex{y1, 1} = 0 since w4 = 0 iff y1 = 1). The m=18
  base-spot on-line z-sequence extends to 16 members
  (z=16..31 = 0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1); the m=17 members
  remain all zero through z=31.
- Recheck anchors 18/18 value==published (4 z=30 touches + 14
  wave-train row separation values; `match` is the conform criterion,
  False BY DESIGN for separation anchors — see match_field_note).
- k=41 (thirty-second tail, ODD) CONFIRMED as registered: hold
  {0}U{12..41}, then UNIFORM 0v1 for ALL s in {42..75} (odd-z supply
  chain candidate 12/12). k=42 (thirty-third, EVEN) CONFIRMED: hold
  {0}U{12..41}, break 0v2 at s=42, then UNIFORM 2v1 for ALL s in
  {43..76} (even chain candidate 12/12).

FINITE observations only; no universal statement; no K slot claimed;
11x11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots UNKNOWN, unchanged; no verdict consumed.
