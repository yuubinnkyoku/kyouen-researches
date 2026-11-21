# K1208: cross-engine agreement on the (4,4) m=35/36 frontier-neighborhood hunt, deficient-row coverage of near-frontier placements, and fresh fixed-width census values

Date: 2026-11-21
Lane: standard-rule fixed-width q=4 (single-owner declaration
`a423c2f0`, part 1 = K1207). Part 2 of the lane — the bounded-neighborhood
witness engine around all published (4,4) def-mode witnesses — was executed
**twice in parallel by two instances of the same hourly task**. This item
records the collision, the resolution, and the results that survive it.
Every statement below is a finite, exactly-scoped record; **no witness
absence or existence claim is made at (4,4) m=35 or m=36** — both remain
UNDETERMINED.

## The collision and its resolution

Instance A (the author of this item) completed an independent part-2 engine
(E-kit: window-translation placement grid, layers L1A1/L1A2/L2A0/L2A1/L3A2,
maximality-based essentiality gating, same witness definition and K1207
class-alive gate as published elsewhere) and ran it to completion on m=35
(2,040 placements over all 31 published base records, translate families
deduplicated to one representative) and m=36 (2,148 placements): **zero
def-mode witnesses in the declared <=2-removal/<=2-addition neighborhoods**,
0 budget caps, 0 dead-class candidates passing the K1207 gate, and every
maximal safe configuration found in the neighborhoods row-saturated
(min row >= 3; 2,538,192 at m=35, 3,013,268 at m=36). Its positive controls
rediscover the published m=34 witness exactly (target board 4x34 from
bases <= 33: 4 witnesses = the published set + 3 images; 4x33 rediscovery
of the published m=33 witness: 8), a corrupted-base hazard dies loudly, and
an isolated-cwd rerun is byte-identical. Full tables: session log
`research/log/2026-11-21-four-row-q4-m35-part2-crosscheck-session.md`.

Instance B, running the same lane in parallel, had already published the
engine as commit `cf88217d`
(`research/experiments/four-row-q4-m35-neighborhood-hunt-20261121/`,
bounding-box-translation placement grid, validation battery V1-V3: census
anchors 8/8, verify-published 31/31, layered-vs-brute EQUIV on 20
placements), announcing the m35/36 hunt runs as its pending publish.

To avoid double work and simultaneous writes, instance A did not publish a
competing experiment directory. Instead it re-fetched B's engine byte-exact
(sha256-verified against the cf88217d README pins) and **re-ran it as an
independent cross-check on targeted single-base slices**, published as
`research/experiments/four-row-q4-m35-crosscheck-slices-20261121/`.

## Cross-check results (published engine re-run; both engines, same input pins)

| slice | placements (bbox grid) | result | agreement with E-kit |
|---|---|---|---|
| 4x34, base 32 | 52 | 4 distinct witness stone sets | **identical** to E-kit's Ctrl34 finds, incl. published m=34 witness `11:15:20:54:60:74:77:89:126:128:129` (268 witness records = 67 R-config hits x 4 sets) |
| 4x35, base 32 | 56 | **0 witnesses** | U0 profiles and lone cells identical on the 16 shared window placements; lone cells `(34,2),(0,2),(1,2)` on the id image |
| 4x35, base 34 | 56 | **0 witnesses** | new finer-grid slice (E-kit covered this family only on the window grid) |
| 4x36, base 32 | 60 | **0 witnesses** | U0 = 1 at 8 placements, lone cells again in the deficient row |

Two independently written engines with independently validated completeness
arguments (E-kit: layer lemmas + controls + hazard + determinism; E-pub:
census anchors + published-witness reverification + brute-force EQUIV
battery) therefore agree exactly on the shared slices, on the positive
control, and on census(4,35,4) = 413 lines + 41,194 circles = 41,607.

**Addendum (same session, addendum commit)**: two further family slices with
the published engine extend the record: 4x35 base 28 (52 placements, **0
witnesses**, min U0 = 5) and 4x35 base 30 (60 placements, **0 witnesses**,
min U0 = 2, the U0 = 2 pairs straddling the left and right board edges). In
both, every placement's R=empty uncovered set again lies entirely inside
the (image-y-flipped) deficient row. The deficient-row coverage observation
of the next section therefore spans **284 placements across five family
representatives** (m=28, 30, 32, 34 at 4x35; m=32 at 4x36) on the published
fine grid, while the distance-1 boundary (U0 = 1) remains specific to the
m=32-family placements so far.

Placement-grid note for verification use: E-pub translates each reflected
pattern's bounding box (the m=32 family box has width 21, so 56 placements
on 4x35); E-kit translates the full m_base-wide window of the canonical
published placement (16 placements for that family on 4x35). E-pub's grid is
the finer one; E-kit's is the grid of "translate the published board window".
Both are legitimate bounded neighborhoods; the cross-check compares the
shared placements and extends the negative record to the finer grid for
these families.

## Deficient-row coverage structure (finite observation; no universal claim)

On 4x35 with the m=32 and m=34 bases (56 placements each) and on 4x36 with
the m=32 base (60 placements), for every bounding-box placement the R=empty
uncovered set U0 lies **entirely inside the deficient row** (row 2 for the
id/fx images, row 1 for the y-flipped images). U0 = 1 is attained at four
consecutive translations on 4x35 (lone cells `(34,2)`, `(0,2)`, `(1,2)`,
`(2,2)` on the id image) and at eight placements on 4x36 (e.g. `(1,2)` at
id-image tx=8); each lone cell sits on no 3-curve, so adding it is safe,
but it saturates the deficient row to [3,3,3,3], a non-deficient maximal
configuration. Interpretation (heuristic, marked as such): on this
frontier the witness condition fails on the covering side, not the safety
side, and the failure is exactly "one stone short of row saturation" —
consistent with K1207's band result (15/34 classes alive at m >= 35, the
deficient classes forced toward saturation), but the observation itself is
only these slices.

## Fresh census determinations (independent first-principles builder)

The builder enumerates all census curves (lines and circles with >= 4
grid points) with explicit point lists; it reproduces all 28 published
curve totals in the pinned (4,4) record bank (m=4..34) and all 8 pin cases
including (4,35,4) = 41,607. Constructive records without published totals,
determined here (independent computation; cross-check if published
elsewhere):

- **(4,31,4) = 325 lines + 28,562 circles = 28,887**
- **(4,33,4) = 367 lines + 34,500 circles = 34,867**
- **(4,34,4) = 390 lines + 37,749 circles = 38,139**
- **(4,36,4) = 436 lines + 44,835 circles = 45,271**

## What this is not

- No absence or existence claim at m=35/36; the full fine-grid hunt over all
  bases is instance B's pending publish, deliberately not pre-empted here.
- The stalled `four-row-q4-m35-class-split-20261115` lane is another owner's
  IN FLIGHT work and is untouched; no SAT/kissat work, no 11x11 work.
- The K1207 tables and the m <= B(class) inequality are used as published,
  verified input; this item does not re-derive them.
- E-kit's full artifacts (46 files incl. per-phase ledgers/summaries/keys
  and sha manifests) are preserved in the author's durable kit and recorded
  in the session log; they are offered as independent-replication material
  for verifying instance B's forthcoming m35/36 hunt ledgers (window grid
  subset of the bbox grid; candidate check list: per-family negative
  containment, the Ctrl34 four-stone-set equality, U0 profiles, census
  values).

## Relations

- Extends K1207 (part 1 class tables/captable are the shared input of both
  engines; part 2 execution record).
- Cross-check counterpart: `cf88217d`
  (`research/experiments/four-row-q4-m35-neighborhood-hunt-20261121/`).
- Evidence: `research/experiments/four-row-q4-m35-crosscheck-slices-20261121/`
  (README, probe, 4 ledgers, run log, sha256 pins) and
  `research/log/2026-11-21-four-row-q4-m35-part2-crosscheck-session.md`
  (instance A's full completion tables, bug-history honesty record,
  collision resolution, next-run handoff).
