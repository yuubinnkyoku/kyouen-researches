# strip-wavetrain-z31-z35 micro-kit (2026-11-26)

Frozen pre-declaration micro-census executing the decay micro-kit
(commit `8d53f7d2`) log S5 handoffs: items #1-#3 the death-valley /
wave-birth / deep m=13 predictions of the SEPARATION LIFE-CYCLE
scaffold, item #4 the m=18/m=17 base-spot z=30 touch, item #5 the
k=39/k=40 tail supply pre-computations, plus three kit-added
first-contact rows.

## PRE-FREEZE REGISTRATION CORRECTION (disclosed before the run)

Re-deriving every registered collapse constant from the published
K0832 closed form under the published row convention R=m+z+1 (the
convention under which every measured decay-kit output reproduces)
found that the decay-kit log S5 contains THREE R off-by-one
constants: `v(33,32,49)` (S5#1, m=15@z=32; correct R=48,
v(33,32,48)=0), `v(34,33,51)` (S5#1, m=16@z=33; correct R=50,
v(34,33,50)=1), `v(32,31,47)` (S5#2, m=14@z=31; correct R=46,
v(32,31,46)=1) — and the two S5#2 "only separation" claims (m=15@z=33,
m=16@z=34) overlooked the surviving previous birth. The registered
ZERO-separation "death-valley" predictions rested on those faulty
constants and are RETRACTED before the run; original texts quoted
verbatim inside the frozen row records. The S5 m=13@z=31, S5#3
m=13@z=32, S5#4 touch and S5#5 tail registrations are arithmetically
consistent and were executed EXACTLY AS REGISTERED.

## Files

| file | sha256 | size |
|---|---|---|
| `explore_wavetrain_z31_z35.py` | `4a5f09019cdf7d8ca14fe02e8ab5a5f9653c6d5d2cbe1d8c26a53075a71e6a17` | 29254 B |
| `engine_block.py` | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` | 2540 B |
| `explore_wavetrain_z31_z35.out` | `a5c64df83725675282114a6be63c853f928fe0bf3221a2b3326a85ff34cf5e83` | 23457 B |

`engine_block.py` byte-identical to the series engine (pin
`bd5f22e4…`), embedded and asserted inside the explore script
(engine_gate PASS).

## Reproduce

```sh
python3 explore_wavetrain_z31_z35.py > outfile
cmp outfile explore_wavetrain_z31_z35.out
```

Determinism: 6/6 byte-identical runs (default x3,
`PYTHONHASHSEED=random`, `env -i` isolated-dir x2), ~13 s per run.
K0832 battery 64/64. Post-freeze ordered-engine audit: 18/18 new
positions (14 row separations + 4 touches) and 16/16 recheck anchors
identical.

## Headline results (finite machine observations)

- ALL TEN ROWS measure EXACTLY the frozen predictions — separation
  count, shape, engine value and direction — 14 predicted separations
  and exactly those 14 measured:
  - 6 ONE-PAST decays of the newest births (odd 2->1 UP 1v0:
    m=15 {15,18}@z=32, m=15 {15,20}@z=34, m=13 {13,20}@z=32; even
    2->0 DOWN 0v1: m=16 (16,18)@z=33, m=14 (14,18)@z=31, m=16
    (16,20)@z=35);
  - 4 TWO-PAST sticks (odd stuck 1 DOWN 1v2: m=15 {15,18}@z=33,
    m=13 {13,18}@z=31; even stuck 0 DOWN 0v2: m=16 (16,18)@z=34,
    m=14 (14,18)@z=32);
  - 4 WAVE BIRTHS completing the d=3 (fourth) wave 4/4: m=13
    {13,20}@S=33 UP 2v0, m=14 (14,20)@S=34 UP 2v1, m=15 {15,20}@S=35
    UP 2v0, m=16 (16,20)@S=36 UP 2v1 — gap 2d+1 (odd) / 2d (even), d=3.
- The registered "clean valley" (ZERO separations) is REFUTED for all
  three registered death-valley rows: at the z*(m)+odd offsets
  exactly ONE separation survives (the newest birth in its stuck
  phase). MEASURED WAVE PROFILE is strictly periodic-2 in the covered
  regime: exactly TWO separations at every birth slice z*(m)+2d
  (d>=1: the newborn + the previous birth stuck) and exactly ONE at
  every in-between slice; rows never empty.
- DEATH CURVE now 9/9 at birth+3, both parities, m in {13..16},
  d in {0,1,2}: {13,14}(died z=28), {13,16}(z=30), {13,18}(z=32 NEW),
  (14,14)(z=29), (14,16)(z=31 NEW), {15,16}(z=32 NEW), {15,18}(z=34
  NEW), (16,16)(z=33 NEW), (16,18)(z=35 NEW).
- ONE-PAST parity decay multi-datum: odd 2->1 now 8 observations,
  even 2->0 now 7; TWO-PAST stick 9 observations. Value trajectory
  2,1,1,dead (odd) / 2,0,0,dead (even) holds through every published
  slice.
- Four first-ever z=30 engine touches w1..w4 = 0,1,1,0 ALL CONFORM:
  the m=18 base-spot on-line z-sequence extends to 15 members
  (z=16..30 = 0,1,0,1,0,1,0,1,1,1,1,1,1,1,1); the m=17 members
  remain all zero through z=30.
- Recheck anchors 16/16 value==published (4 z=29 touches + 12
  decay-kit separations; `match` is the conform criterion, False BY
  DESIGN for separation anchors — see match_field_note).
- k=39 (thirtieth tail, ODD) CONFIRMED as registered: hold
  {0}U{12..39}, then UNIFORM 0v1 for ALL s in {40..73} (odd-z supply
  chain candidate 11/11). k=40 (thirty-first, EVEN) CONFIRMED: break
  0v2 at s=40, then UNIFORM 2v1 for ALL s in {41..74} (even chain
  candidate 11/11).

FINITE observations only; no universal statement; no K slot claimed;
11x11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots UNKNOWN, unchanged; no verdict consumed.
