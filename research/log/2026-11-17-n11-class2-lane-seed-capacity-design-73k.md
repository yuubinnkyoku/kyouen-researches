# 2026-11-17 n11 class2-lane: N-way merge seed capacity design (K0909 follow-up, gate constant redesign)

Lane: 11x11 class2-lane long-term (cost73k). Kind: measurement only.
Outcome: seed insertion-failure design rule for N-way merged worker-memo
seeds established and cross-validated against the verbatim engine at the
design point MS=1<<25 (sim 28 / engine 28); the design point is also 5.4%
cheaper for the band run itself. All 16 gates pass. No verdict change;
11x11 remains UNKNOWN.

## Context

Two independent K0909-line measurements (node-balanced 4-way, and the
boundary-preserving 4-way) both broke the pre-run gate "seed insertion
failure < 0.1%" when seeding a merged worker-memo table into the verbatim
engine at MS=1<<24:

- 4-way seed (4,985,986 keys, md5 7b098aeb...): 16,137 failed (0.324%),
- boundary 4-way seed (4,975,265 keys): 14,657 failed (0.295%),

while the published 2-way seed (4,291,899 keys) failed only 1,448 (0.034%).
In every case the record-identity gate closed (missing == failed exactly,
value violations 0, certificates 22/22 byte-identical), so the failure is
a performance issue, not a soundness issue. Both measurements left the
gate-constant redesign open: what table size MS makes an N-way merged seed
safe, and where is the failure knee in seed size S?

## Design

1. Rebuild the published 4-way pipeline from pinned blobs (orchestrator
   blob 50b60247, extractor blob 52bcaf50, manifest blob 0892aed0, legal
   blob 8e97082c; raw-CDN fetch + git blob sha verification) and re-close
   the published gates (workers W1-W4, N-way merge, seed md5, seedrun4,
   record identity). All values must equal the K0909 publication.
2. Light occupancy-only seeding simulator (light_sim_seed_73k.mjs):
   replicates the verbatim mHash (4-word Math.imul XOR, masked) and the
   64-slot linear probe window, storing only per-base occupancy counters
   (no key arrays). With distinct-key seeds the engine's key-match branch
   is unreachable during seeding, so occupancy-only replication is exact.
   Validate at MS=1<<24 against BOTH engine anchors: 4-way 16,137 and
   2-way 1,448.
3. Sweep MS=1<<25, 1<<26 with the simulator (engine runs at MS>=1<<26
   exceed this environment's ~1.09 GiB cgroup).
4. Prefix sweep at MS=1<<24 (real seed keys, merged insertion order) to
   localise the failure knee in seed size S.
5. Full band seedrun at the design point MS=1<<25 with the verbatim
   engine and 4-way seed, closing: certificates 22/22 byte-identical,
   seed failure < 0.1%, engine failure count == simulator prediction,
   record identity (violations 0, missing == failed).

## Findings

1. **Reproducibility (full rebuild after an environment reset)**: all
   published values re-reproduced exactly - workers W1 29,193,572 /
   W2 30,417,638 / W3 31,104,578 / W4 22,025,713 nodes (certificates
   7/7, 6/6, 5/5, 4/4 byte-identical), distincts 1,979,858 / 1,793,658 /
   1,544,867 / 1,565,935, merge occupied_after 4,985,986, shared
   1,592,504, conflicts 0, merged seed md5 7b098aeb625f722e5bfb13fcc615652a
   (merge deterministic, 2 runs byte-identical), seedrun4 76,903,818
   nodes with seed failure 16,137, record identity closed. Reproduces
   the K0909 publication gate-by-gate (13/14; the single failing gate is
   the known <0.1% pre-run gate, recorded as fact).
2. **Simulator validation at MS=1<<24 (both anchors exact)**:
   sim(4-way seed) = 16,137 failed = engine seedrun4 exactly;
   sim(2-way seed, rebuilt workers A 48,482,011 / B 71,480,136 nodes,
   distincts 2,619,833 / 2,554,155, merged seed record-identical to the
   published md5 e7c2c17e... after header-line substitution, see note 6)
   = 1,448 failed = published engine value exactly. The occupancy-only
   design is therefore exact for distinct-key seeding at the anchor
   point; its MS and S extrapolations are predictions, cross-checked at
   the design point in finding 5.
3. **MS sweep (4-way seed, 4,985,986 keys)**: MS=1<<24 -> 16,137 failed
   (0.324%, load 0.296); **MS=1<<25 -> 28 failed (0.00056%, load 0.149,
   passes the 0.1% gate by two orders of magnitude)**; MS=1<<26 -> 0
   failed (load 0.074). The 0.1% gate is met from MS=1<<25. Failure
   attribution at MS=1<<24 (simulator): the largest hash base index
   carries 109 distinct keys (bases>=64 keys: 250 of 1,224,783 non-empty
   bases); 2,278 of the 16,137 failures are own-cluster saturation
   (>=64-key bases), 13,859 are spill-over into saturated clusters. The
   failure mechanism is verbatim-hash clustering, not table size alone.
4. **Failure knee in seed size S (MS=1<<24, real 4-way seed keys in
   merged insertion order)**: S=1M -> 0 failed, 2M -> 0, 3M -> 26,
   3.5M -> 256, 4M -> 2,017, 4.29M (=2-way size) -> 5,969, 4.5M ->
   8,233, 4.75M -> 11,410, 4.99M (full) -> 16,137. The knee is sharp and
   superlinear: the 0.1%-gate boundary sits at S~4.1-4.2M keys at
   MS=1<<24, which is why the 2-way seed (4.29M, 0.034%) passed and both
   4-way seeds (~4.99M, ~0.3%) failed. Gate constants should therefore
   be set on S and MS jointly (seed load S/MS), not on a fixed failure
   rate at a fixed MS.
5. **Design point MS=1<<25, full band, verbatim engine**: seeded
   4,985,986, inserted 4,985,958, **failed 28 - equal to the simulator
   prediction of 28 exactly (0.00056% < 0.1%)**; certificates 22/22
   byte-identical; record identity closed (present 4,985,958,
   missing 28 == seed failed, value violations 0).
   **The design point is also cheaper: total 72,745,351 nodes = 0.9459
   of the MS=1<<24 seedrun (76,903,818)** - every bit except bit 95 is
   less expensive at MS=1<<25 (per-bit ratios 0.878-0.986), because at
   MS=1<<24 the 64-slot probe windows saturate during the band search
   itself, silently discarding memo entries and forcing re-expansion;
   final occupancy 14,073,139 (load 0.419) vs 10,526,730 (load 0.627)
   shows the smaller table lost ~3.5M entries in-run. Bit 95 is
   11,857,737 nodes at both MS (ratio exactly 1.0): third independent
   confirmation of the memo-state-invariant root (K0907).
   **Design rule for N-way merged seeds on this band: seed at
   MS=1<<25 (load <= ~0.15); MS=1<<24 tolerates only S <~ 4.1-4.2M keys
   under a 0.1% failure gate, and running the band at MS=1<<24 after a
   large merged seed both wastes gate margin and costs ~5% extra
   compute.**
6. **2-way header byte-identity note**: the rebuilt 2-way merge reuses
   the 4-way orchestrator's merge_pass_nway, whose seed header line
   hardcodes a 4-way provenance string. Substituting the published 2-way
   header line into the rebuilt file reproduces the published md5
   e7c2c17e7a91d8ea17f433f3bb482f29 exactly, i.e. record-level byte
   identity; the rebuilt file differs only in that one header line
   (rebuilt raw md5 1599c496...).

## Environment facts (recorded as experiment facts)

- A workspace environment reset (bash 120 s default timeout exceeded by
  a blocking `/dev/kmsg` read) destroyed the local work tree mid-session;
  this measurement is a full rebuild from pinned blobs. Cross-environment
  determinism held at every step (all published values re-reproduced
  exactly, including both merged-seed md5s).
- Three OOM kills of the MS=1<<25 seedrun were needed to characterise
  the environment limit (~1.09 GiB cgroup; MS=1<<25 typed arrays alone
  are 672 MB): cap 500 died during dumpMemo at 26% of slots written;
  cap 200 completed the full 22-bit search but died during dumpMemo at
  61% (~426 MB written, VmRSS steady 806 MB); cap 150 with a clean
  cgroup but ~5.6 GB of prior dumps in page cache died mid-search
  before bit 15 (memory.peak hit the cgroup limit exactly). An isolated
  reproduction (672 MB of MS=1<<25 typed arrays + the verbatim dumpMemo
  chunk loop, cap 200) writing 678 MB SURVIVES, so the kill is not
  explained by arrays + dump loop alone. The completed redo ran at cap
  200 after (a) deleting ~5.1 GB of no-longer-needed dump/sort/distinct
  intermediates and dropping the page cache, and (b) hardening the
  MS=1<<25 variant's dumpMemo with fs.fsyncSync() every 32 MiB plus one
  final fsync (dump BYTES unchanged; only write scheduling differs;
  measured cost ~36 ms per 32 MiB chunk+fsync). The dump (840 MB,
  14.07M records) completed without an OOM event.
- MS=1<<26 and 1<<27 full engine runs are infeasible in this cgroup
  (~1.09 GiB: typed arrays alone are 1.34 GB / 2.68 GB); the simulator
  carries the sweep there instead and is anchored at MS=1<<24 twice and
  cross-validated at MS=1<<25 once.

## Gates (output/seed-capacity-design-73k-20261117.json, 16/16 pass)

- repro_4way_seed_md5_matches_published - True
- repro_workers_match_published - True
- repro_distincts_match_published - True
- repro_seedrun4_seed_failed_matches_published_16137 - True
- repro_seedrun4_nodes_match_published - True
- sim24_4way_failed_equals_engine - True
- sim24_2way_seed_md5_matches_published - True
- sim24_2way_failed_equals_engine - True
- sim25_design_point_failure_below_0.1pct - True
- two_way_workers_match_published - True
- two_way_distincts_match_published - True
- seedrun25_byte_identical_22 - True
- seedrun25_seed_failed_equals_sim25 - True
- seedrun25_seed_failure_below_0.1pct - True
- seedrun25_record_identity_no_violations - True
- seedrun25_record_identity_missing_equals_seed_failed - True

## Interpretation guard

Measurement only. No new WIN/LOSS verdicts, no manifest row opened or
closed, certificate bytes unchanged, repo-verbatim extractor unmodified
(published determinism chains). WIN7-D10 proves a first-player win within
depth 10 from the individual 7-stone roots only; REFUTED-D10 is not a
LOSS proof. The 11x11 empty board, both two-stone roots {49,60} and
{59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.
