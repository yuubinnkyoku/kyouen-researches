# Declaration: takeover of the stalled n11 twelfth-cost batch stage-1 sweep (single-owner, publish-then-execute)

The original lane declared the twelfth-cost batch stage-1 sweep in
wave A (`f6d29d16`, 2026-11-27T16:41:12Z) and has published no
wave-B raws for 6h40m as of this declaration (23:21Z).  Following
the stalled-lane takeover precedent (`cc152b71`), this lane takes
over execution of the sweep.  Kit (wave B):
`research/experiments/n11-twelfthcost-batch-stage1-2m-20261127`.

## Re-validation performed by this lane before this declaration

- Selection kit
  `research/experiments/n11-twelfthcost-class-s5-exclusive-probe-20261127`
  fetched from main: all 54 MANIFEST files sha256-verified (selector
  `ea2b8331...`, jsreplay `84585617...`, authoritative keys JSON
  `1119d01b...`, input CSVs k01..k51).
- Serving class `10376293541461626880:16777216` (coverage third
  moves {100, 108, 112, 118}), 51 exclusive keys, first
  `1152921504607895556:603979776`, last
  `14987979559889014784:16777216`.
- **Freshness re-validated against the CURRENT head of record
  `beecb024...` (6894 rows WIN 212 / LOSS 6682)**: all 51 keys
  absent (0 stale).  The original selection was made against head
  `1e2eeda2...`; the four ultra-cheap adoptions since then touch
  only their own keys.
- k01 at 2M was run once by the ORIGINAL lane before its wave A
  (disclosed there: result 0, nodes 2,000,000).  This lane runs a
  k01 2M cold pair first as calibration and discloses the
  comparison; no other twelfth key has been run by this lane before
  this declaration.

## Execution plan (publish-then-execute; wave B publishes the raws)

Identical to the original wave-A declaration: per key k01..k51
(ascending truncated-cost proxy, then key) a 2,000,000-budget cold
pair with jsreplay `84585617...` under the published input CSVs.
Node-identical exact-LOSS resolves the key; a 2M UNKNOWN pair
escalates to a 15M-budget cold pair; a 15M UNKNOWN pair parks the
key (L50M candidate).  WIN stopping rule: no new key is started
after a key resolves WIN(1); keys already in flight complete their
pairs as bookkeeping.  All rows are single-implementation
(Node.js replica); C++ gate + third-impl pillars are separate
future Parts before any adoption.  Runs are sequential
(CPU-conservative), resumable, and every raw is published.

If the original lane publishes wave-B raws concurrently, both sets
are kept and compared (cross-host determinism data); conflicts are
recorded, not forced.

## Guards

Scheduling only; no verdict is claimed or implied.  The standard
11x11 empty board: UNKNOWN.  All 19 central-reply roots: UNKNOWN.
The two-stone root {60,27} and its remaining third moves
100/108: UNKNOWN.  Nodes and proxy values are bookkeeping, never
evidence of WIN or LOSS.  Declared against HEAD `bcdaa79c`.
