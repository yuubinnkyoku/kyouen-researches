# n11-fifthcost-class-s5-exclusive-probe-1152921504612089856-20261121 (checkpoint state: probes in progress)

Exclusive single-live-parent S5 probe batch for the fifth-cost candidate class
`1152921504612089856:536870912` (coverage {88, 98, 100, 108}), declared in
`research/log/2026-11-21-n11-fifthcost-class1152921504612089856-exclusive-s5-probe-single-owner.md`.

Status at this checkpoint commit:

- Validation gate 4/4 reproduced on this execution host (`output/val/`):
  the pinned Node.js replica reproduces all four published two-target-design
  replay rows exactly (at2m x2: result 0 / nodes 2,000,000 / legal 98,99;
  15M x2: result 2 / nodes 3,651,923 and 5,040,200 / legal 98,99), only
  `wall_s` differs.
- `output/fifth-cost-exclusive-keys.json` is the authoritative 44-key machine
  selection (216 fail-closed gates; disjoint from all concurrent-lane claims;
  every key: 5 stones, D4-canonical, safe, derived legal == supply ledger,
  live parent exactly the declared class, absent from the base cache and the
  quarantine registry).
- Per-key raw rows are pushed incrementally to `output/raw/` as checkpoints
  (`at2m-...`, `at15m-a-...`, `at15m-b-...` per key; both stages, 15M run
  twice for the determinism gate). No verdict of this table may be consumed
  before the full batch audit (`output/probe-audit.json`), the merged cache
  increment and the SHA-256 manifest are published by the final commit of
  this lane.
- Expected per-key outcome under the pre-registered stopping rules: exact
  LOSS within 15M (two identical runs), or parked UNKNOWN (both stages both
  runs recorded, no cache row). Any WIN stops further claimed-key starts
  this session and triggers witness publication instead.

Inputs and consumed pins (sha-verified, not duplicated here):

- base cache `merged-exact-s5-after-js-probe-13.cache` (sha256 `60e0dc34...`)
  at `research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/`;
- geometry `geometry.json.gz` (sha256 `146be80b...`) and
  `historical-cost-profile.json` at
  `research/experiments/n11-strategy-redesign-20261010/output/`;
- published class-closure-priority measurement
  `research/experiments/n11-s5-class-closure-priority-20261121/output/class-closure-priority.csv`;
- `independent.py` (sha256 `954d3a10...`) at
  `research/experiments/n11-independent-exact-audit-20261010/scripts/`;
- `s5_evidence_policy.py` (sha256 `78655e94...`) at
  `research/experiments/n11-frontier-selection-20261005/scripts/`;
- quarantine registry `results/n11-s5-evidence-quarantine.json`
  (sha256 `81d23160...`);
- sbd keymap `research/experiments/n11-s4bd-fresh-corpus-regen-20261121/input/keymap.json`
  (sha256 `0aa054c8...`).

Execution constraints honored: at most 2 workers (2-core host), fresh 2^22 PnTT
per row, one solver per row, publish=ALL, exact order=count, <= 15,000,000
node budget, cold runs only.

Status guard: nodes, solved counts and proxy values are never verdicts. The
standard 11x11 empty board, the two-stone root {60,27}, and its remaining
third moves 100/108 remain UNKNOWN.
