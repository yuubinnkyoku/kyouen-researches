# NEWK-r4: K item for verified 12-stone maximal safe set on 12×12

## Created item

- ID: `K0436`
- File: `research/knowledge/items/K0436-n12-twelve-stone-maximal-safe-set-verified.md`
- Kind: `proposition`
- Status: `computed`
- Topics: `maximal-safe`, `geometry`

## Basis

Source research report: `scratchpad/NEW12-r3-report.md`.

Verified witness (row-major `p = x + 12*y`):

`5, 50, 56, 57, 61, 66, 68, 72, 77, 88, 98, 107`

Coordinates:

`(5,0), (2,4), (8,4), (9,4), (1,5), (6,5), (8,5), (0,6), (5,6), (4,7), (2,8), (11,8)`

Independent verification (`scratchpad/verify_new12.py`):

- Safety: 0 forbidden quadruples among `C(12,4)=495` 4-subsets.
- Maximality: 0 unblocked among 132 empty points.
- Block-count distribution: `{1:34, 2:32, 3:33, 4:16, 5:11, 6:4, 7:2}`.
- Density: `12/144 = 8.33%`.

## Schema validation

- `uv run --locked python tools/knowledge/check.py`: 431 items, 0 errors, 0 warnings.
- `uv run --locked python tools/knowledge/build.py`: generated 6 views from 431 items.

## Artifacts

- `scratchpad/NEW12-r3-report.md` (source)
- `scratchpad/verify_new12.py` (verifier)

## Scope and limitations

The item records only the existence of one verified 12-stone maximal safe set on 12×12. It does not change `s_12 <= 11` or `K_12 >= 22`, and does not claim that 12 is minimal or maximal. No complete enumeration or upper bound is claimed.