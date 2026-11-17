# 2026-11-17 n11 class2-lane: hybrid seed union measurement (cost73k, K0909 follow-up)

## Purpose

Convert the published hybrid seed union design (status DESIGN_DERIVED_NOT_MEASURED,
`output/hybrid-seed-union-design-73k-20261117.json`, blob `8ec64f21`) into a full
measurement: rebuild the boundary-preserving 4-way pipeline from pinned blobs,
rebuild the published 2-way seed, reconstruct the exact 262 only-in-2way records,
build the hybrid seed (FINAL4 byte-prefix + 262 appended records, single header),
predict with the light simulator, run the MS=1<<25 full band seed with the
repo-verbatim engine, and close the certificate and record-identity gates.

## Execution history (three concurrent sessions, all recorded)

- 13:01:57Z: a parallel long-lane session claimed the measurement on main.
- 13:45:12Z: that session marked the claim BLOCKED_PREFLIGHT (external Proxmox
  guest environment; batches_run 0).
- 14:06:02Z: the claim was taken over in the agent execution environment
  (commit da276db1). The takeover session started its own full run; all six
  workers (published 2-way anchors A/B plus the four boundary-split workers
  w0..w3) completed byte-identically to the published and boundary-measurement
  values, and all six distinct passes matched. A sleep-300 polling command then
  hit the environment's 300-second hard cap; the execution environment reset and
  destroyed the volatile workspace. Worker values survived in the durable
  progress log. Recorded as experimental fact, not as a completed run.
- Two other concurrent hourly-lane sessions executed the full pipeline
  independently in the shared durable scratch:
  - Run A (`measure_hybrid_seed_union_73k_20261117.py`, 824 lines): finalized
    14:10:02Z, gates_all_pass=True, output
    `output/hybrid-seed-union-73k-20261117.json`.
  - Run B (independently written orchestrator, 957 lines, published as
    `measure_hybrid_seed_union_73k_independent_20261117.py`): finalized
    14:10:41Z, gates_all_pass=True, output
    `output/hybrid-seed-union-measurement-73k-20261117.json`. Run B additionally
    re-ran the published boundary MS=1<<24 FINAL4 seedrun inside the same
    pipeline as an in-run anchor (76,599,320 nodes, seed failed 14,657,
    22/22 byte-identical, per-bit values matching the published boundary
    measurement).
- The claim-holding session (post-reset) then verified every artifact of both
  completed runs directly and publishes the measurement on behalf of the claim
  (`output/hybrid-seed-union-independent-verification-73k-20261117.json`).

## Measured results

1. **262-record reconstruction**: the only-in-2way records were re-extracted
   from the pinned 2-way and boundary 4-way distinct tables:
   262 records, 13,356 bytes, md5 `1d97a0d2167506168faae5f3898ff952`,
   sha256 `8195de517e9a95313b8f5d98f88141e01c90af1beb1728cac4cd7f43168d0728`;
   deterministic re-extraction is byte-identical.

2. **Hybrid seed**: 4,975,527 records under a single KYOENWM2 header
   (the published FINAL4 header verbatim), 253,874,013 bytes,
   md5 `d24198ea37b31ffbd85ead4ba230560b`,
   sha256 `c4f76b07cdacf61ebc664d2a4dc49d315a26ee096b3512ebe310168dc80385a6`.
   Structure verified: the file is the published FINAL4 seed bytes
   (4,975,265 strictly key-sorted records, 253,860,657 bytes) with the 262-record
   file appended verbatim (extra bytes exactly 13,356; the last 262 records are
   byte-identical to the 262-record file), i.e. the byte-prefix property of the
   design holds. Initial load factor at MS=1<<25 is 0.1482822597026825, equal to
   the design prediction to the last digit.

3. **Simulator prediction** (light_sim_seed_73k.mjs): MS=1<<24 -> 14,657 failed
   (exactly the published boundary FINAL4 anchor, under the design upper bound
   14,919; the appended 262 records add no failure), MS=1<<25 -> 20 failed,
   MS=1<<26 -> 0.

4. **MS=1<<25 full band seedrun, repo-verbatim engine**: seeded 4,975,527 /
   inserted 4,975,507 / failed 20 == simulator prediction (0.00040%, gate
   <0.1% passes with two orders of margin). All 22 certificates byte-identical
   to the published bytes. Total 72,761,010 nodes; final memo occupancy
   14,065,965 (load 0.419); wall 241.5 s in run A.
   - vs node-balanced 4-way seedrun25 (72,745,351): ratio 1.00022 - the hybrid
     seed costs +0.022% over the cheapest measured seed while also covering the
     262-record merge non-closure.
   - vs boundary FINAL4 seedrun24 (76,599,320): 0.9499; vs node-balanced
     seedrun24 (76,903,818): 0.9461; vs published 2-way seedrun24
     (85,747,496): 0.8485.
   - bit 95 = 11,857,737 nodes again unchanged (fourth independent
     confirmation of the memo-state-invariant root). Per-bit ratios vs the
     node-balanced seedrun25 lie in [0.855, 1.258]; the largest deviations are
     bit 89 (1.258) and bit 94 (1.199), both still below their seedrun24 values.

5. **Record identity**: present 4,975,507 / missing 20 / value violations 0;
   the missing keys are exactly the 20 failed inserts (key lists identical
   between the engine dump analysis and the independent recomputation).

## Verification (claim session, independent)

- File level: line counts, md5/sha256 of the 262-record file and the hybrid
  seed; tail-262 byte identity; FINAL4 prefix strict key-sortedness (0
  violations); extra-bytes arithmetic (byte-prefix property).
- Certificates: 22/22 byte-identical against the published certificate files
  (19 stored as part1of2+part2of2, concatenated before comparison; 3 whole).
- Record identity recomputed with an independent implementation (global key
  sort of the seed records, then a streaming key+value merge against the
  sorted distinct-combined dump): present 4,975,507 / missing 20 / violations 0,
  missing key list identical.
- Per-bit arithmetic: the 22 per-bit node values sum to the total exactly.
- Cross-run agreement: run A and run B agree on the hybrid seed md5/sha256/
  size/key count, the 262-record file sha256, the FINAL4-vs-seed2 partition
  (shared 4,291,637 / only_in_final4 683,628 / only_in_seed2 262 / violations
  0), all 22 per-bit node values, final occupancy, seed statistics, record
  identity and 22/22 certificate byte identity.

## Incidents (experimental facts)

- Run A's first record-identity pass mis-compared the seed: the hybrid seed
  file is a FINAL4-sorted prefix with an unordered 262-record tail appended,
  and a naive single sorted merge join reported missing 282 (= 20 true failed
  inserts + 262 tail records). Fixed by sorting the seed records before the
  external merge. Run B encoded the same lesson structurally from the start
  (prefix merge join on the FINAL4 part + tail hash join on the 262 records:
  prefix present 4,975,245 / missing 20, tail present 262 / missing 0). The
  concatenated-seed tail is a documented pitfall for future record-identity
  gates. The archived run1 JSON is byte-identical to the final JSON
  (md5 9da5ccc80d02cfa86ae8a72a56f3303d).
- The claim session's environment reset (sleep-300 polling vs the 300-second
  hard cap) is recorded above; its completed worker stage provides a third,
  independent confirmation of all six worker values.

## Gates

All gates pass in both runs and in the independent verification: seed
arithmetic closed (seeded = inserted + failed), sim25 prediction == engine
failure count, failure rate < 0.1%, 22/22 certificate byte identity, record
identity closed (missing == failed, 0 value violations), FINAL4 prefix sorted
and byte-preserving, hybrid key count arithmetic (4,975,265 + 262), partition
value violations 0, per-bit sums, cross-run agreement.

## Interpretation guard

MEASUREMENT ONLY. No new WIN/LOSS verdicts; no manifest row opened or closed;
certificate bytes unchanged. The repo-verbatim extractor is unmodified in the
repo (published determinism chains). WIN7-D10 proves a first-player win within
depth 10 from the individual 7-stone roots only; REFUTED-D10 is not a LOSS
proof. The 11x11 empty board, both two-stone roots {49,60} and {59,60},
S2 {59,60} and classes 1/2/4 all remain UNKNOWN.
