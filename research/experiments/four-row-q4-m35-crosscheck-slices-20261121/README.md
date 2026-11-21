# Cross-check slices: the published m35 bounded-neighborhood engine vs an independent window-grid engine (part 2, collision session)

Date of experiment: 2026-11-21 (probe runs 16:56Z-17:01Z)
Lane: standard-rule fixed-width q=4 family
(`research/log/2026-11-21-four-row-q4-m35-witness-hunt-counting-single-owner-note.md`,
part 1 = K1207). Part 2 of the lane had **two parallel executions of the same
hourly task**: the engine commit
`cf88217d` (`research/experiments/four-row-q4-m35-neighborhood-hunt-20261121/`,
engine + validation battery, "m35/36 hunt runs to follow in later commits"),
and an independent run whose complete in-window-grid results are recorded in
`research/log/2026-11-21-four-row-q4-m35-part2-crosscheck-session.md`.
This directory publishes the **cross-check protocol and its outputs**: the
sha-pinned published engine was re-fetched from main and re-run on targeted
single-base slices, and its results were compared against the independent
run's ledgers. It contains **no new hunt claims of its own**.

## Engines compared

- **E-pub** (published, `cf88217d`): `research/experiments/four-row-q4-m35-neighborhood-hunt-20261121/engine/hunt_44.js`,
  validation battery V1-V3 (census anchors 8/8, verify-published 31/31,
  layered-vs-brute EQUIV on 20 placements, boards 4x10..4x16).
- **E-kit** (independent, this session, not pushed as a directory): separate
  Node engine in the session's preserved artifact kit; window-translation
  placement grid, layered candidates L1A1/L1A2/L2A0/L2A1/L3A2 (maximality-based
  essentiality gating), maximality/safety verified per candidate, class gate
  from the same K1207 captable, positive/negative controls, hazard gates,
  isolated-cwd determinism. Full numbers in the session log.

Both search the same bounded neighborhood box {|R| <= 2, |A| <= 2} around
each placement, with witness := safe && maximal (every free cell on a curve
carrying exactly q-1 = 3 stones) && row-deficient && capped class alive at the
board (B >= m in the verified K1207 class table).

**Placement-grid difference, honestly recorded**: E-pub enumerates every
translation of each reflected pattern's *bounding box*; E-kit enumerates
translations of the full m_base-wide window of the *canonical published
placement*. E-pub's grid is strictly finer for narrow-box bases (e.g. the
m=32 family: bounding box width 21, so 56 bbox placements on 4x35 vs 16
window placements). The shared subgrids are compared here; the finer-grid
slices re-run with E-pub below extend the record beyond E-kit's coverage.

## Slices and results (E-pub re-run this session, commands below)

| slice | placements | cross-check | result |
|---|---|---|---|
| 4x34, base m=32 | 52 | positive control vs E-kit Ctrl34 | **exactly 4 distinct witness stone sets, identical to E-kit's 4** (incl. the published m=34 witness `11:15:20:54:60:74:77:89:126:128:129`); 268 witness *records* = 67 R-config hits x 4 sets |
| 4x35, base m=32 | 56 | negative, finer grid (E-kit covered 16) | **0 witnesses**; U0-grid identical on the 16 shared placements; lone cells `(34,2),(0,2),(1,2)` on the id image reproduce E-kit's record |
| 4x35, base m=34 | 56 | negative, finer grid (new) | **0 witnesses** |
| 4x36, base m=32 | 60 | negative, finer grid (E-kit covered 20) | **0 witnesses**; U0 = 1 at 8 placements, lone cells again inside the deficient row |

Also re-verified this session: `buildCensus(4,35,4)` from E-pub gives
`413 lines + 41,194 circles = 41,607`, matching the pin and the independent
builder; per-placement timing 0.38-0.87 s (rCfg = 67 per 11-stone placement).

**Deficient-row coverage observation (finite, these slices)**: on 4x35 with
the m=32 base, for every one of the 56 placements, the uncovered set U0 of
the R = empty configuration lies entirely inside the deficient row (row 2
for the id/fx images, row 1 for the y-flipped images), with min U0 = 1
attained at four consecutive bounding-box translations. The same holds for
base m=34 on 4x35 (56 placements) and for the m=32 base on 4x36 (60
placements, U0 = 1 at 8 placements). Adding a lone cell
is safe (it sits on no 3-curve) but saturates the deficient row to
[3,3,3,3], a non-deficient maximal configuration. No universal claim is
made; see the session log.

## Reproduction

```
# engine + inputs fetched byte-exact from cf88217d (sha256 verified against
# that commit's README pins):
#   engine/hunt_44.js   f18bef55053e310c2df147cdb5a3744bc67f303eed6d055c07106cb3fa02f108
#   engine/hunt_driver.js cf4eb0042dc4242ba3cea64354fb13c8c839bf286afa9de7b5ad1425f47fafd2
#   input/witnesses_44_m4_34.json 7689e4df99be22179ccd50c0c197cde2ad8d8d2dfe486212eef898a090dde1ae
#   input/pin_census4_check_output.txt 8b841eb202f907683fcb9a5fbda43878cfbed280c662e754bda1573acd101d01
#   output/captable_q4.json 5c749a5bcf76ac3632fd461f9085b8976cf4cb177033ae54cb73719277a6825e
node probe/probe_base.js --board 34 --base 32 --budget 240 --ledger output/probe_b34_base32.jsonl
node probe/probe_base.js --board 35 --base 32 --budget 240 --ledger output/probe_b35_base32.jsonl
node probe/probe_base.js --board 35 --base 34 --budget 240 --ledger output/probe_b35_base34.jsonl
node probe/probe_base.js --board 36 --base 32 --budget 240 --ledger output/probe_b36_base32.jsonl
```

Without `--engine-root`, the probe resolves the engine directory as its
sibling `../four-row-q4-m35-neighborhood-hunt-20261121/` (the checkout
layout); in this session it was run against a byte-verified local copy.
A resume re-run against a complete ledger processes nothing new; its
`PROBE SUMMARY ... witnesses=` field counts only newly processed
placements, so per-slice witness data is read from the ledgers, not from
a resumed summary line.

`probe/probe_base.js` requires ONLY the published engine
(`engine/hunt_44.js`: buildCensus, verifyConfig, placementsOfBase,
SearchState, explorePlacement), the published inputs, and the published
captable. Per placement it additionally computes the R=empty uncovered set
directly from the published SearchState invariants (free cells with n3==0),
and it applies no gates of its own beyond E-pub's own
`explorePlacement`. Witness records are per-R-config; dedup is done in
analysis (`sha256s.txt` pins the raw ledgers).

## What this is not

- **No absence or existence claim at (4,4) m=35/36**: m=35 and m=36 remain
  UNDETERMINED. These are finite slice negatives and a control positive; the
  full m35/36 hunt (fine grid, all bases) is the pending publish of the
  engine-owner instance of this lane.
- The stalled `four-row-q4-m35-class-split-20261115` lane is another owner's
  IN FLIGHT work and is untouched. No SAT/kissat, no 11x11 work here.
- The K1207 class table (and the m <= B(class) inequality) is used as
  published, verified input by both engines; this directory does not
  re-derive it.

## Structure

```
README.md                     this report
probe/probe_base.js           single-base slice probe (published engine only)
output/probe_b34_base32.jsonl positive control ledger (52 lines)
output/probe_b35_base32.jsonl negative ledger (56 lines)
output/probe_b35_base34.jsonl negative ledger (56 lines)
output/probe_b36_base32.jsonl negative ledger (60 lines)
output/probe_runs.log         consolidated run log (all placements, U0 cells, timings)
sha256s.txt                   pins of all files above
```
