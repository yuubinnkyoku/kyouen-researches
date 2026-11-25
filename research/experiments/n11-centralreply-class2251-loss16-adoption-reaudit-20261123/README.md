# n11 central-reply class 2251 batch-29 16-LOSS canonical adoption + reaudit (Part CU, 2026-11-23)

Part CU single-owner canonical adoption of the batch-29 (class 2251)
takeover drive-1 checkpoint 1/3 evidence: the 16 resolved fresh LOSS keys
ab001..ab016 (2-pass node-exact at budget 15M, total nodes 57,463,971 per
pass, status.log 16 PASS rows), merged into the canonical exact-S5 chain
cache behind the Part CO base (854800f3..., 6,301 rows) as BASE + 16 = 6,317
rows (158 WIN / 6,159 LOSS).

## Declaration (publish-then-execute)

Single-owner declaration published before the official run:
`research/log/2026-11-24-part-cu-b29loss16-adoption-single-owner-note.md`
(commit d8276573; byte-verified by git blob sha d274d5fc...). Observed HEAD
at declaration time d06c4d92 with no counter-claim on this adoption lane.

## Contents

- `scripts/make_increments_b29loss16.py` — fail-closed adoption increment
  maker (kit MANIFEST 71-file sha verification, val-gate double-host
  node-exact cross-check, raw 2-pass discipline, status.log strict parse,
  BASE/quarantine absence gates).
- `scripts/s5_union_merge.py` — byte-clone fail-closed union merger
  (selftest PASS; WIN/LOSS conflict abort).
- `reaudit/scripts/refresh_adoption_b29loss16.py` — post-adoption 19-root
  joint-plan refresh against the merged chain cache (read-only).
- `scripts/compare_deltas_b29loss16_adoption.py` — fail-closed delta
  extractor (pin pile: increment / manifest / scenario / BASE reaudit
  outputs / status.log / batch-keys / kit MANIFEST / 16 val-gate files).
- `output/increment-b29loss16-20261123.cache` — 16 LOSS rows
  (sha256 bab011e3...).
- `output/increments-manifest.json` — b29loss16-increments-manifest-v1
  (sha256 f9f58ee1...; full_packet_eq_loss_only=true ON THE PROBED SET,
  win_scenario_exists=false, fileless 38).
- `output/merge-audit-run{1,2,3}.json` — audits (sha256 8f611fe1... x3,
  identical; merged output sha256 30ddad9d...).
- `output/merged-exact-s5-chain-...-b29loss16-20261123.cache` — the
  canonical merged chain cache, 6,317 rows (260,590 B).
- `reaudit/output/refresh-summary.json` / `closure-classes.csv` /
  `per-root-coverage.csv` — post-adoption reaudit outputs
  (sha256 b60d71a2... / 3019d37f... / 61dbd39a...). probe-worklist.csv
  (sha256 0d7474e1... at generation time) is reproducible from the
  refresh script and is NOT committed for volume.
- `output/decomp-deltas-b29loss16-adoption.json` — base->scenario delta
  book (sha256 3274a297...).

## Run record (official, publish-then-execute)

1. Pre-declaration scouting (declaration note section 3): kit MANIFEST
   71/71 file shas verified; status.log 16 PASS rows; raw inventory
   exactly ab001..ab016 x {p1,p2}; val-gate 4 patterns x 3 hosts
   node-exact; BASE reaudit outputs reproduced byte-identical.
2. Declaration published (d8276573), then official rerun in a fresh
   scratch tree (cp -a, no hardlinks):
   - D1 maker x4: increment bab011e3... + manifest f9f58ee1... byte
     identical every run (PASS x4).
   - D2 merger: selftest PASS + merge x3: merged cache 30ddad9d... and
     audit 8f611fe1... byte identical x3 (PASS).
   - D3 refresh x3: all four outputs byte identical to pins every run
     (PASS x3; ~59 s/run single-threaded).
   - D4 extractor x4: all gates PASS, decomp-deltas 3274a297... byte
     identical x4 (PASS).
   - D5 isolated rerun (second tree, env -i, PYTHONHASHSEED=random):
     refresh + extractor byte identical (PASS).
3. Tamper battery (protocol 5, probes a-n): 14/14 fail-closed captures,
   each probe restored and sha-verified, final clean pass reconfirmed.
   Captured gates: raw 2-pass mismatch (a/b/c), kit MANIFEST sha drift
   (d), merger WIN/LOSS conflict (e: BASE-forged duplicate / h: injected
   forged WIN duplicate), extractor increment sha drift (f/i), manifest
   sha drift (g), status.log sha drift (j), val-gate takeover-host sha
   drift (k), scenario cache sha drift (l), scenario summary sha drift
   (m), scenario closure-classes sha drift (n). First battery pass had
   3 tampers that failed to APPLY due to a probe-side format mismatch
   (assertion-caught, so no false capture was claimed); they were
   re-run with corrected tampers and captured (honest note).
4. Publication A-E (5 commits), each fetch-back verified byte-exactly
   against the local official-rerun tree by git blob sha1.

## Adoption effects (machine-observed, none misread as verdicts)

- class 2251 (batch-29, fileless mostly): unknown_now 54 -> 38 (closure
  rank 35 -> 4). class 2251 is NOT freed: 38 fileless keys
  (ab017..ab054) are UNPROBED.
- Class-status counts unchanged: excluded 390 / excluded_now 23 /
  free_now 38 / unknown 34,498 on both sides; no excluded_now flip; no
  newly freed class; anchors 23101 / 1849 / 16757 stable; closure rows
  808 -> 808.
- Holder-only unknown deltas: 1181 (102->101), 1182 (104->103),
  11426 (60->59); stable-unknown rank churn 125 (tie-swap left
  {1945,19645} / entered {386,1044}).
- Metrics: joint greedy union 38,310 -> 35,691; probe worklist
  64,828 -> 64,809 (class 2251 serving rows 54 -> 38; adopted 16 keys
  vanish from the scenario worklist); update8 unchanged (resolved 141 /
  remaining 31,718; the 16 adopted s5 indices do NOT intersect the
  update8 baseline requirement set); per-root greedy movers root 16
  (2,971 -> 2,970) and root 37 (4,001 -> 3,852); roots_summary_moved
  none; root 27 baseline 119/119 unchanged.
- holder union 48 (class 2251 own 16; 47 other classes own 1 each).
- batch-29 is PARTIALLY probed: the adopted packet is loss-only ON THE
  PROBED SET (16/16 LOSS so far); NO WIN and NO EXHAUSTED row observed
  in the batch so far; NO completeness claim for the batch as a whole.

## Concurrent lanes (honest contact observation)

- Part CV (a8592d9c, 2026-11-24T00:17:04Z) declared row-audit +
  pinned-replica + third-implementation cross-validation of the SAME 16
  keys ab001..ab016. It is a scrutiny lane, not an adoption lane: no
  counter-claim on this adoption chain, no file overlap with this
  experiment dir. This adoption's own gates (val-gate 3-host
  node-exact x4 patterns, raw 2-pass, kit MANIFEST 71/71) stand
  independently of it; its outcome will further corroborate or
  challenge the 16 rows.
- Part CT completed concurrently: batch-28 last-EXHAUSTED aa050
  resolved WIN (25,541,199 nodes, 2-pass) — a WIN row outside this
  lane's scope (WIN adoption is the scrutiny owner C++ pin's domain);
  this adoption's BASE is untouched by it.

## Interpretation guard

Verdicts are consumed ONLY as exact LOSS rows of probed keys. Nodes and
budget are bookkeeping. Adopting 16 of 54 keys does NOT free class 2251
and does NOT decide anything about the 19 central-reply roots or the
standard 11x11 empty board. **11x11 stays UNKNOWN.**
