# strip-decay-z29-z35 micro-kit (2026-11-26)

Frozen pre-declaration micro-census executing the frontier micro-kit
(commit `d49b480a`) log S5 handoffs: item #1 one-past parity-decay
candidates at m=17/m=18, item #2 secondary-birth / death-curve next
slices, item #3 the m=18/m=17 base-spot z=29 touch, item #4 the
k=37/k=38 tail supply pre-computations.

## Files

| file | sha256 | size |
|---|---|---|
| `explore_decay_z29_z35.py` | `608eeec84cc216e3bcad441d6fc0c0bb7f173f850d69f3ed5901cf47dc84d4fd` | 24577 B |
| `engine_block.py` | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` | 2540 B |
| `explore_decay_z29_z35.out` | `9c4f18e7d782498418cb82e1a5320edaf427300068e3b0f4e025420c246835a4` | 17695 B |

`engine_block.py` byte-identical to the series engine (pin `bd5f22e4…`),
embedded and asserted inside the explore script (engine_gate PASS).

## Reproduce

```sh
python3 explore_decay_z29_z35.py > outfile
cmp outfile explore_decay_z29_z35.out
```

Determinism: 6/6 byte-identical runs (default x3,
`PYTHONHASHSEED=random`, `env -i` isolated-dir x2), ~9 s per run.

## Headline results (finite machine observations)

- ONE-PAST PARITY-DECAY now 3/3 per parity: m=17@z=34 {17,18}@35 UP
  1v0 (odd 2->1) and m=18@z=35 (18,18)@36 DOWN 0v1 (even 2->0), both
  EXACTLY-ONE separations as predicted.
- TWO-PAST SECONDARY-BIRTH 2/2 FULL HIT: m=15@z=31 shows exactly the
  predicted pair (original {15,16} DOWN 1v2 with the odd value stuck
  at 1; secondary {15,18}@33 born UP 2v0 — gap-3 rule) and m=16@z=32
  exactly ((16,16) DOWN 0v2; (16,18)@34 born UP 2v1 — gap-2 rule).
- THREE-PAST m=14@z=29: the boldest prediction (ZERO separations) is
  HALF-REFUTED: the original (14,14) DID die conform (as predicted),
  but the secondary (14,16) decayed 2->0 — the ROW-parity decay, not
  2->1 — and persists DOWN 0v1. LESSON: the parity decay applies to
  every separation of the row, the secondary included.
- FOUR-PAST m=13@z=29: the value-stick expectation held ({13,16}@29
  stuck at 1, DOWN 1v2) AND a NEW TERTIARY {13,18}@31 was BORN UP
  2v0 — the "only separation" wording falsified, the 4-past birth
  slot discovered.
- The kit-added rows extend the m=13 curve to z=30 (FIVE-past) and
  m=14 to z=30 (FOUR-past): {13,16} DIED conform at 3 slices after
  birth (3-slice lifetime datum 2), and (14,18) was BORN at 4-past UP
  2v1 (the even 4-past birth slot, datum 2 with m=13's {13,18}).
  Multi-datum SEPARATION LIFE-CYCLE structure now: births at
  2d-past (d=0,1,2) at gaps 2d+1 (odd m) / 2d (even m), value
  trajectory 2,1,1 (odd) / 2,0,0 (even), death at birth+3 so far.
- Four first-ever z=29 engine touches u1..u4 = 0,1,1,0 ALL CONFORM;
  m=18 base-spot z-sequence 14 members (z=16..29 =
  0,1,0,1,0,1,0,1,1,1,1,1,1,1), m=17 eight members all zero.
- Recheck anchors 12/12 value==published (the `match` field on
  separation anchors is the conform criterion, False BY DESIGN — see
  the kit's match_field_note).
- k=37 (twenty-eighth tail, ODD) CONFIRMED as registered (hold
  {0}U{12..37}, uniform 0v1 s in {38..71}; odd chain candidate
  10/10); k=38 (twenty-ninth, EVEN) CONFIRMED (break 0v2@38, uniform
  2v1 s in {39..72}; even chain candidate 10/10).
- K0832 battery 38/38; post-freeze ordered-engine audit of all 12
  separations + 4 touches: 16/16 identical.

FINITE observations only; no universal statement; no K slot claimed;
11x11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots UNKNOWN, unchanged; no verdict consumed.
