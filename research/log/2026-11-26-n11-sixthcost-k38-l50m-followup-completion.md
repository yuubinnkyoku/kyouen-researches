# k38 L50M follow-up completion (sixth-cost exclusive S5 probe, fifth parked key)

Date: 2026-11-26 (long-term lane session, runner). This Part executes the
pre-registered publish-then-execute escalation declared at commit `a798427`
(`research/log/2026-11-26-n11-sixthcost-k38-l50m-followup-declaration.md`,
2026-11-26T18:55:06Z) for the single key k38
`10376293541461626880:66048` (legal 100, sixth-cost exclusive S5 batch,
machine order position 38, fifth resumption).

## Runner role and territory check

The declaring session published the declaration at 18:55:06Z and had NOT
published any result raw 52 minutes later (counter-probe at 19:46Z: latest
main HEAD `5e8f48c`, no `at50m-*` file in the kit output/raw listing). This
session therefore took the runner role under the Part SN precedent
(declaration published by one session, execution published by another) and
executed the pre-registered protocol unchanged. Counter-probe immediately
before the results push (19:54:40Z): HEAD still `5e8f48c`, zero `at50m` raws,
no commit touching k38 / L50M / parked escalation territory between the
declaration and this push.

## Pre-run state (honest)

- jsreplay.js byte-verified at HEAD `5e8f48c` from the kit path
  `research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/scripts/jsreplay.js`:
  sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (matches the declaration pin). Note: the declaration writes the path as
  `scripts/jsreplay.js`; the pinned bytes live in the kit `scripts/`
  subdirectory (108 byte-identical copies exist across experiment kits); the
  pin, not the abbreviated path, is the authority.
- Input `input/k38.input.csv` byte-clone verified:
  `target,0,5,10376293541461626880,66048,100,0,0,0,0,0`.
- Execution host: upgraded sandbox, Node.js v22.20.0 (same version family
  as the declaration host).

## Validation gate (before target runs, this host)

4/4 node-exact against the published expected quadruples (wall differs):

- at2m 98: (98, 2000000, 0, 2000000), wall 9 s
- at2m 99: (99, 2000000, 0, 2000000), wall 9-10 s
- 15M 98: (98, 15000000, 2, 3651923), wall 18 s
- 15M 99: (99, 15000000, 2, 5040200), wall 26 s

## Target runs (pre-registered budget 50,000,000, fresh cold process each)

- run1 (started 19:50:01Z): LOSS(2), nodes 21,839,049, wall 125 s
  -> `output/raw/at50m-run1-k38.out.csv`
- run2 (started 19:52:09Z): LOSS(2), nodes 21,839,049, wall 127 s
  -> `output/raw/at50m-run2-k38.out.csv`

Both cold runs agree exactly on (result, nodes). Pre-registered outcome (a)
applies: k38 is now a loss-resolved row of the sixth-cost exclusive S5 batch
(2M UNKNOWN -> 15M parked pair exhausted -> 50M cold pair LOSS(2) at
21,839,049 nodes, below the 50M budget).

## Verdict scope (unchanged)

NO verdict is consumed. This is a batch row, not an adoption: no cache
increment, no class-status change, no coverage claim, no freshness change of
any canonical head. Adoption of the k38 LOSS row (with the parent batch
WIN/LOSS conflict policy review and a fresh declaration) remains a separately
declared future Part, exactly as for the 30 fifth-resumption LOSS rows.
The standard 11x11 empty board, the 19 central-reply roots, the two-stone
root {60,27}, its remaining third moves {100,108}, S2, class 1/2/4 and all
closure classes stay UNKNOWN throughout. Nodes are bookkeeping, never
verdicts.

## Published artifacts

- `.../output/raw/at50m-run1-k38.out.csv` (281 bytes, sha256
  f7e519586d8e9dd7c8378aef2c96ccd70479816056954e93ffdf16732178bfcc)
- `.../output/raw/at50m-run2-k38.out.csv` (281 bytes, sha256
  53d0f69d03d0b04520f9f832e517f177ed9b0e33c917db3f114a5a77a602fe03)
- `.../output/raw/status.log` addendum (5464 bytes; the 5113-byte published
  prefix byte-verified at HEAD `5e8f48c` before appending)
- this completion log

## Honest disclosures

1. Runner-role takeover: the declarer session published the declaration and
   its own pre-declaration D2 validation gate run (recorded in the
   declaration), but did not publish target results within 52 minutes. This
   session re-ran the full validation gate fresh on this host before the
   target runs (4/4 node-exact) rather than trusting the declarer's
   unpublished environment claim.
2. The wall-clock fields are host-specific and are NOT expected to match any
   other host; only (id, legal, budget, result, nodes) are node-exact
   reproducibles.
3. The status.log addendum times are second-resolution UTC of this host;
   run1 started 19:50:01Z (finished 19:52:06Z), run2 finished 19:54:16Z.
