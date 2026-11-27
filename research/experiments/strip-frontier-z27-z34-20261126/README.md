# strip-frontier-z27-z34 micro-kit (2026-11-26)

Frozen pre-declaration micro-census executing the published z26f20 kit
log S5 handoffs (commit `68bc863d`): item #1 frontier test data, item #2
one-past datum candidates, item #3 the twenty-sixth-tail (k=35)
pre-computation, item #4 the m=18 base-spot z-sequence z=28 touch.

## Files

| file | sha256 | size |
|---|---|---|
| `explore_z27z34_frontier.py` | `0475c5d9ab9043234c0ae6405b1692cd87e00b8fb94b4d39274b5e6ce6f5edd1` | 26432 B |
| `engine_block.py` | `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0` | 2540 B |
| `explore_z27z34_frontier.out` | `fa55ae7b791e8d37058ec94b41d175de678fb59a72c07f7323b99b7b9a8800da` | 17897 B |

`engine_block.py` is byte-identical to the series engine (pin
`bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`),
embedded and asserted inside the explore script (engine_gate PASS).

## Reproduce

```sh
python3 explore_z27z34_frontier.py > outfile
cmp outfile explore_z27z34_frontier.out
```

Determinism: 6/6 byte-identical runs (default x3,
`PYTHONHASHSEED=random`, `env -i` isolated-dir x2), ~11 s per run.

## Headline results (all finite machine observations)

- FRONTIER parity-split candidate 4/4 HIT this kit: m=15@z=29
  {15,16}@31 UP 2v0, m=16@z=30 (16,16)@32 UP 2v1, m=17@z=33
  {17,18}@35 UP 2v0, m=18@z=34 (18,18)@36 UP 2v1 — carrying the
  registered z26f20 S5#1 law candidate to 6/6 (odd m=13/15/17, even
  m=14/16/18).
- One-past decay is PARITY-SPLIT (new): odd m drops 2->1 staying
  visible UP 1v0 (m=13 z=26 published, m=15@z=30 NEW); even m drops
  2->0 visible DOWN 0v1 (m=14@z=27, m=16@z=31 NEW). This REFUTES the
  naive z26f20 S5#2 drop-2to1 formulation as a uniform rule.
- Secondary separations are BORN at two-past: m=13 row z=27 gains
  {13,16}@29 UP 2v0 (decays to UP 1v0 at z=28); m=14 row z=28 gains
  (14,16)@30 UP 2v1. The original frontier shape of m=13
  ({13,14}@27) DIED (became conform) at three-past z=28.
- Four first-ever z=28 engine touches t1..t4 = 0,1,1,0 ALL CONFORM
  via the frozen option tables; m=18 base-spot on-line z-sequence now
  z in {16..28} = 0,1,0,1,0,1,0,1,1,1,1,1,1 (13 members), m=17 all
  zero (7 members).
- k=35 twenty-sixth tail CONFIRMED as registered (hold {0}U{12..35},
  uniform 0v1 s in {36..69}; odd-z supply chain candidate 9/9);
  k=36 twenty-seventh tail new registration (break 0v2@36, uniform
  2v1 s in {37..70}; even chain candidate 9/9).
- Rechecks: 4/4 published z=27 handoff values; 3/3 published z=25/26
  frontier separation engine values reproduced. NOTE (semantic
  disclosure): in `published_recheck_anchors` the `match` field is
  the collapse-CONFORM criterion `value == collapse ==
  published_value`; for the three separation anchors the engine value
  intentionally deviates from the collapse, so `match` is False BY
  DESIGN there — the recheck criterion for those rows is
  `value == published_value`, which holds 3/3. The four z=27 handoff
  anchors are conforming and show `match: true`.
- Post-freeze independent audit (not part of the frozen artifact):
  ordered-engine cross-check of all 12 row separations and 4 z=28
  touch spots: 16/16 identical.

FINITE observations only; no universal statement; no K slot claimed;
11x11 empty board, two-stone roots, S2, class 1/2/4 and all
central-reply roots UNKNOWN, unchanged; no verdict consumed.
