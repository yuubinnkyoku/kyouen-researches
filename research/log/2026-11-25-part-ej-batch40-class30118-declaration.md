# Part EJ declaration (single-owner): batch-40 probe of closure class 30118 (rank-21 post-EI fresh frontier)

- observed main HEAD at declaration: `6273d010` (2026-11-25T12:31:16Z); counter-declaration
  search for "Part EJ" / "batch-40" / "class 30118" in commit messages at declaration time:
  0 hits. Part EH/EI knowledge (rank-22 class 23964 / rank-24 class 8811 as next fresh
  classes) was a PRE-EI derivation; this declaration supersedes it on the basis of the
  machine re-derivation below, computed from published bytes only.
- Part EF (batch-38 class 30345) is another lane's in-flight single-owner drive. The
  present Part does not touch any batch-38 key except the two claim-reserved dual-class
  children that intersect the target class boundary (ai033/ai034), which are excluded
  from the target set and handled as claim-reserved bookkeeping exactly as batch-39
  handled ai044/ai048.

## Machine basis (fail-closed, published bytes only)

1. Part EI reaudit regen: the published refresh fork
   `refresh_adoption_ei.py` (sha256 `1bcf1972...`) was byte-fetch'd and re-executed in a
   clean room against the published canonical cache `73482be0...` (6,712 rows WIN 158 /
   LOSS 6,554) and its four pinned dependencies (dependency-graph `54f9c364...`,
   repaired-joint-plan-update8 `b658290a...`, independent.py `954d3a10...`,
   s5_evidence_policy.py `78655e94...`, quarantine `81d23160...`). All four outputs
   reproduced byte-identically: closure-classes `e12bf328...`, per-root-coverage
   `2525f306...`, refresh-summary `414314eb...`, probe-worklist (regen pin
   `98529a8d...`).
2. Fresh-frontier scan (3-way cross: EI worklist regen x prior-probe universe x EI
   canonical cache, extended for post-EI honesty):
   - extended prior-probe universe `prior-probe-universe-b40.csv` (sha256 `09332448...`,
     2,154 pairs) = the published universe `6deee846...` (2,104 pairs, byte-pinned,
     unchanged) UNION exactly the 50 probed batch-39 keys (aj001..aj050 per published
     batch-keys-b39.json `5e25b550...`). Provenance machine-written to
     `prior-probe-universe-b40.ext-meta.json` (`61a71240...`).
   - claimed set = the 49 in-flight batch-38 target pairs (published
     batch-keys-b38.json `29807104...`); batch-38 verdicts unconsumed, Part EF owner.
   - result, freshness-ranks1to21-b40.csv (sha256 `1e6125a7...`, columns
     rank,class_index,unknown_now,children,prior_probe,cache_hit,claimed,fresh):
     ranks 1..20 ALL fresh 0. Rank 9 (class 30484): 4 prior (batch-39 honest labels
     aj030/aj039/aj049/aj050) + 2 claimed (ai044/ai048). Rank 13 (class 30345,
     Part EF's class): 1 prior + 49 claimed. Ranks 14..20: all-prior. **Rank 21
     (class 30118): children 52 == unknown_now 52 = 2 claimed + 50 fresh.**
   - class 30118 rank 21 = the lowest-rank fresh class in the post-EI regen (pre-EI it
     was rank 39, outside the EH ranks-13..20 scan; its own 2 adopted dual-class rows
     moved it to rank 21 in the EI reaudit). Context (not selected, machine-derived):
     rank 23 class 23964 fresh 51, rank 25 class 8811 fresh 51.
   - the 52 class-30118 extract rows (worklist probe_order 546..597 contiguous,
     sha256 `e3d05647...`): 50 targets fresh (not in universe-b40, not in the EI
     canonical cache, not quarantined, not claimed), 2 claim-reserved (ai033 at
     probe_order 586, ai034 at 596; dual-class 30345/30118 children, batch-38
     in-flight, same-condition re-probe prohibited).
3. Nothing in this declaration is a verdict. All quantities above are bookkeeping.

## Part EJ scope (single-owner, kit-next-run within this same run)

- experiment dir: `research/experiments/n11-centralreply-closure-class30118-batch40-20261125/`
- kit scripts (wave 1, publish-then-execute):
  - `scripts/make_batch40_keys.py` - fork of the published batch-39 maker
    `make_batch39_keys.py` (`425329c0...`): class params rank 21 / class 30118 /
    mask [1152922604118474753, 65536] / unknown_now 52 / probe_order 546..597; the
    claim-reserved slot re-pointed to ai033/ai034 (batch-38 provenance); G3b extended
    to the ranks-1..21 freshness table with the claimed column (fresh-0 assertion for
    all ranks 1..20 + rank-21 accounting 52 == 2 claimed + 50 fresh); G7 freshness
    now gated against BOTH universes (published `6deee846...` and extended
    `09332448...`); new G9 asserts extended-universe integrity
    (ext == base UNION the 50 batch-39 probed keys, provenance meta
    `61a71240...` + published batch-keys-b39 `5e25b550...`).
  - `scripts/runbatch.sh` byte-clone (`f591f8c2...`), `scripts/jsreplay.js`
    byte-clone (`84585617...`): engine and runner unchanged.
  - `scripts/drive40_local_step.sh` - fork of `drive39_local_step.sh`
    (`49ec1dd5...`): key-id regex aj -> ak (4 spots), batch-keys json b39 -> b40,
    batch-38 -> batch-40 in comments. One invocation = at most 2 keys / 2 workers
    (2-core host), WIN-CONTINUE, MISMATCH hard-stop, `timeout 260` inner cap.
- kit sources (wave 2): batch-keys-b38.json `29807104...`, batch-keys-b39.json
  `5e25b550...`, canonical-cache-73482be0.cache `73482be0...`, closure-classes.csv
  `e12bf328...`, refresh-summary.json `414314eb...`, quarantine.json `81d23160...`,
  prior-probe-universe.csv `6deee846...`, prior-probe-universe-b40.csv `09332448...`,
  prior-probe-universe-b40.ext-meta.json `61a71240...`, freshness-ranks1to21-b40.csv
  `1e6125a7...`, worklist-class30118-extract.csv `e3d05647...`.
- kit input (wave 3): maker run 3x byte-identical + tamper battery fail-closed, then
  input/ak001..ak050.input.csv (50 files) + input/batch-keys-b40.json (schema
  n11-centralreply-closure-batch40-keys-v1, target_key_count 50,
  consumed_into_canonical_cache=false, claim_reserved_excluded ai033/ai034).
- val-gate (wave 3b): 4 molecules byte-cloned from the published batch-39 val-gate
  (identical sha set ecc0299b/6e902ab1/56aacb71/eeafe3ac/8035fe54/91dffdec), fresh
  node-exact 4/4 vs published baselines is the drive-start requirement; host sidecars
  published under output/val-gate-host/.
- drive protocol (executed waves): two-pass fresh-cold @ 15,000,000 nodes / order 0,
  key-by-key, 2 workers, deterministic-mismatch HARD-STOP, EXHAUSTED honest UNKNOWN
  (no same-condition re-probe), WIN honest label WIN-HALT marker and drive continues
  (verdicts never consumed here; any WIN adoption is scrutiny-owner C++ gate
  `9193f5b6...` exclusive), increments of up to 10 keys + status.log snapshots, final
  increment carries the complete 50/50 status.log.
- machine audit (audit_b40.py, fork of audit_b39.py at audit time), README +
  MANIFEST-sha256, completion log at the end.

## Guardrails

- every number derived here is bookkeeping; no root verdict, no coverage, no secured
  coverage is claimed or changed.
- batch-38 keys: only ai033/ai034 appear and only as excluded claim-reserved rows;
  ai001..ai032, ai035..ai049 untouched; Part EF single-owner.
- aj030/aj039 (EXHAUSTED @15M): same-condition re-probe prohibited; the registered
  high-budget ladder remains a SEPARATE future Part's declaration (not this one).
- aj049/aj050 and every other unconsumed WIN row: unchanged, scrutiny C++ gate
  exclusive.
- **The standard 11x11 empty board, the 19 central-reply roots, the two-stone roots
  {49,60}/{59,60}, S2 {59,60}, and closure classes 1/2/4/16371/20421/34908/30484/30118
  all remain UNKNOWN. Nothing in this Part changes that.**
