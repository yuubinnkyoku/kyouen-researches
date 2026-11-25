# Part EJ batch-40 inc1 second-environment verification (declaration through drive inc1)

- Executing lane: independent long-term-lane run (this session). NOT the Part EJ
  single-owner. The EJ owner's chain verified here, byte-frozen at commit
  `e0ca8d75` (2026-11-25T13:40:08Z): declaration `2baf7e34` -> kit 1/4 `c2019313`
  -> kit 2/4 `c91a8ece` -> kit 3/4 `c3aca5b1` -> val-gate `10259859` ->
  drive-step correction `62a0bff9` -> drive inc1 `519438b5`.
- Verification tree: all 99 published EJ files (4 scripts + 11 sources + 51 input
  + status.log + 20 inc1 raws + 12 val-gate-host) fetched from raw CDN at
  `e0ca8d75` and re-verified on this host from published bytes only.
- Untouched by this verification: the EJ drive state (inc2+ is the owner's),
  batch-38 keys (ai001..ai049 remain Part EF / now also EK-adjacent claim scope),
  aj030/aj039 (claimed by Part EK `dd448fec`, not touched here), every unconsumed
  WIN row, all verdicts. Nothing here consumes a verdict or changes coverage.
- **The standard 11x11 empty board, the 19 central-reply roots, the two-stone
  roots {49,60}/{59,60}, S2 {59,60}, and closure classes 1/2/4/16371/20421/34908/
  30484/30118 all remain UNKNOWN. This verification does not change that.**

## E1 pin / fetch verification (ALL PASS)

All kit pins re-derived from the fetched bytes match the published kit commit
messages AND the maker-internal G1 pins:

- scripts: make_batch40_keys.py `e8588eb6...`, drive40_local_step.sh `5e613cce...`
  (the corrected wave, commit `62a0bff9`), runbatch.sh `f591f8c2...`,
  jsreplay.js `84585617...` (batch-38/39 chain byte-clone).
- sources: batch-keys-b38 `29807104...`, batch-keys-b39 `5e25b550...`,
  canonical cache `73482be0...` (6,712 s5verdict rows), closure-classes
  `e12bf328...`, refresh-summary `414314eb...`, quarantine `81d23160...`,
  universe base `6deee846...` (2,104), universe ext `09332448...` (2,154),
  ext-meta `61a71240...`, freshness-ranks1to21 `b80f581b...`,
  worklist-class30118-extract `8ed13b8b...`.
- input: batch-keys-b40.json `2414d644...` + ak001..ak050.input.csv.

**Honest note H1 (declaration pin drift, no functional impact).** The declaration
log (`2baf7e34`) carries two PRE-publication pins that do not match the published
bytes: freshness-ranks1to21-b40.csv declared `1e6125a7...` vs published
`b80f581b...`, and worklist-class30118-extract.csv declared `e3d05647...` vs
published `8ed13b8b...`. The kit 2/4 commit message and the maker G1 internal
pins agree with the published bytes, and the maker G-gates re-derive every
downstream assertion from those bytes, so the drift is provenance-text drift only
(same pattern as the Part EG maker-pin incident; published bytes are the SSOT).
The EJ owner is invited to append a one-line honest note if convenient.

**Honest note H2 (near-miss in THIS verification, caught before any claim).** The
first val-gate replica attempt on this host wrapped the node invocation in
`/usr/bin/time`, which is not installed here; the shell printed "command not
found" into the redirected time file, node never ran, and the loop's `|| true`
swallowed the failure. The strict output-accounting comparison (empty "replay,"
line -> IndexError) caught it BEFORE any pass/fail claim was recorded. The four
molecules were then re-run properly (results below). Lesson recorded: in a
verification harness never tolerate a missing expected stdout marker, and never
`|| true` a probe invocation.

## E2 maker re-execution (3x byte-identical, ALL GATES PASS)

`make_batch40_keys.py` (published bytes, sha `e8588eb6...`) re-executed 3 times in
3 clean trees (scripts + sources only): all runs rc=0 "ALL GATES PASS, wrote 50
inputs + batch-keys-b40.json", and `diff -r` of each run's `input/` against the
published `input/` is clean for all 51 files, including batch-keys-b40.json
`2414d644...` in every run. The published input wave is byte-reproducible from
the published kit with zero local state.

## E3 tamper battery on this host (5/5 fail-closed + control PASS)

Deep tamper cases with pin-rewire methodology (rewire the tampered source's pin in
a script copy; control proves the rewire itself is harmless):

- t0 control (pin re-rewired to the identical sha, no mutation): rc=0 PASS.
- t1 G1: quarantine 1-byte text flip, NO rewire -> rc=1 "ABORT: G1 pin mismatch
  on quarantine".
- t2 G4: canonical-cache row `s5verdict,<ak001 lo>,<ak001 hi>,5,2,0` injected
  (sorted position) + PIN_CANONICAL_CACHE rewired -> rc=1 "ABORT: G4 canonical
  cache already contains key(s): [(10376294640973250561, 65536)]".
- t3 G5: ak001 pair injected as an active quarantine entry + PIN_QUARANTINE
  rewired -> rc=1 "ABORT: G5 key ak001 is quarantined".
- t4 G7: ak001 pair added to prior-probe-universe-b40.csv + PIN_UNIVERSE_EXT
  rewired -> rc=1 "ABORT: G7 extended universe lines = 2155, want 2154" (the
  line-count assertion inside the same gate trips first; fail-closed confirmed).
- t5 G3b: rank-21 fresh column 50 -> 51 + PIN_FRESHNESS rewired -> rc=1
  "ABORT: G3b rank 21 children != prior+cache_hit+claimed+fresh:
  ['21','30118','52','52','0','0','2','51']".

No tampered run wrote any `input/` output (fail-closed, no partial outputs).

## E4 val-gate molecules (4/4 node-exact on this host)

Fresh-cold re-runs with the published jsreplay bytes on this host, compared to
BOTH the published baselines and the owner's host sidecars (wall_s excluded from
the gate, reported for context):

- at2m A (budget 2M): result 0, nodes 2,000,000; walls mine/owner-host 9/9.
- at2m B (budget 2M): result 0, nodes 2,000,000; walls 9/9.
- first-15m A (budget 15M): result 2, nodes 3,651,923; walls 17/17.
- second-15m B (budget 15M): result 2, nodes 5,040,200; walls 25/25.

4/4 node-exact vs published baseline AND vs owner host sidecar (this host class
matches the owner host class; wall_s agreement is informational only).

## E5 drive inc1 replica (10 keys x 2 passes @ 15M, 20/20 node-exact)

Full replica of the published inc1 using the published jsreplay bytes and the
published per-key inputs, budget 15,000,000, order 0, fresh-cold two passes per
key (2 workers), result+nodes+budget+key_lo+key_hi compared against all 20
published raws:

- 9 keys LOSS (result 2), both passes node-equal to the published values:
  ak001 2,842,496 / ak003 4,585,240 / ak004 2,884,442 / ak005 1,746,353 /
  ak006 1,956,792 / ak007 2,480,327 / ak008 2,018,866 / ak009 3,478,444 /
  ak010 2,876,544 nodes.
- ak002 result=1 (solver-reported WIN) at 14,557,681 nodes in BOTH passes,
  exactly the published values (pre-registered WIN-HALT marker; verdict NOT
  consumed; adoption remains scrutiny-owner C++ gate `9193f5b6...` exclusive).
- 20/20 node-exact excluding wall_s; every pass carries the terminal
  `# replay_done` line; 8/20 wall_s values also byte-equal to the published
  raws (same host class); total replica probe nodes 78,854,370; total replica
  wall 689s (per-pass walls 18-112s).

## E6 independent re-derivation of the selection (28/28 PASS, own Python)

Independent of the maker, from published bytes only:

- R1 ext universe integrity: ext (2,154) == base (2,104) UNION exactly the 50
  published batch-39 keys; sorted-unique; ext-meta base sha/pairs and added set
  machine-verified.
- R2 freshness table: 21 rows, ranks 1..20 all fresh==0, rank-21 row exactly
  [21, 30118, 52, 52, 0, 0, 2, 50], per-row accounting equation
  children == prior + cache_hit + claimed + fresh holds on all 21 rows.
- R3 closure-classes row class 30118: unique, unknown_now 52.
- R4 worklist extract: 52 rows, probe_order 546..597 contiguous; extract ∩
  published batch-38 target set == {ai033@586, ai034@596} exactly; the 50 target
  pairs == extract minus the two reserved, in order ak001..ak050; every b40 key's
  lo/hi/legal matches its extract row.
- R5 absence matrix: all 52 extract pairs absent from the canonical cache
  (re-counted 6,712 s5verdict rows), the 50 targets absent from base and ext
  universes, no extract pair in active quarantine; input csvs match the
  batch-keys template byte-exactly; consumed_into_canonical_cache == false.

## E7 inc1 status accounting (PASS)

Published status.log: 11 lines = 10 PASS + 1 WIN-HALT, zero other lines; every
PASS line's (budget,result,nodes) equals the corresponding published raw's
replay fields (10/10); ak002's p1 and p2 replay lines agree on every field
except wall_s.

## Resume (for the next runs, before touching anything: re-fetch latest main)

1. Part EJ single-owner continues the batch-40 drive (inc2..inc5 + audit +
   README + completion log). This verification log does not touch drive state;
   its replica outputs live only in this session's scratch, published nowhere.
2. Part EK (aj030/aj039 30M ladder, `dd448fec`) and Part EF (batch-38) remain
   their owners'; ai033/ai034 stay claim-reserved.
3. If the EJ owner publishes inc2+ while this log is in flight, nothing here
   conflicts: this log freezes its target at `e0ca8d75` / inc1.
4. All quantities here are bookkeeping or verification evidence; no root
   verdict, no coverage, no secured coverage. **11x11 stays UNKNOWN.**
