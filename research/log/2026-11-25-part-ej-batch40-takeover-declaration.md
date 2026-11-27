# Part EJ (batch-40, closure class 30118) takeover declaration (single-owner)

## 0. Ownership state and takeover criterion (machine-verified at declaration time)

- Part EJ owner publications stopped at drive inc1 (`519438b519dedeed48f723e577e3e5e0e303aaad`,
  2026-11-25T13:01:14Z); the published `output/status.log` last line is stamped
  2026-11-25T13:00:27Z with 10/50 keys resolved: ak001..ak010 (9 LOSS + 1 WIN-HALT
  ak002, 0 EXHAUSTED; 20 two-pass raws published, all byte-pinned by the
  second-environment verification lane `3765ffa1e8`).
- Takeover criterion (repo convention, precedents Part DH / Part EF): owner outputs
  stalled >= 3.5h with no counter-publication. At this declaration the stall is
  > 5h (inc1 end 13:01Z, this declaration ~18:3xZ).
- Honest context: the main mass-deletion incident at `d0755ecc` (16:02Z) forced a
  31-chunk content restore that completed only ~18:0xZ (independently
  spot-verified at tip 567.. second-lane log). All lanes paused additive
  publishing during the window; the Part EJ drive has not resumed since inc1.
- Counter-declaration sweep (machine, 40-commit tip listing at `d455e2b077f36a8b62732fd3ca4f0caefe713206`
  2026-11-25T18:13:21Z + kit-output path commit list):
  - No EJ inc2+ / EJ audit / EJ completion-log commit exists.
  - No takeover or counter-takeover declaration for Part EJ / batch-40 exists
    ("takeover|Part EJ|batch-40|ak011|inc2" scan of the 40 most recent commit
    messages: 0 drive-step hits).
  - The only kit-output commits are: val-gate wave 3b, drive inc1, and
    RESTORE chunk 13/31 (byte restore of already-published content, not a drive step).
  - Other lanes in flight (PG(2,8) 6-arc invariants, Part EM/EL chainwork,
    K1328 z-slice) do not intersect batch-40 ak-keys.
- Observed HEAD-before-push: `d455e2b077f36a8b62732fd3ca4f0caefe713206`
  (2026-11-25T18:13:21Z).

## 1. Scope: complete the pre-declared batch-40 drive, nothing else

- Remaining keys (machine-derived from `input/batch-keys-b40.json` sha256
  `2414d6444e3d6bdf538b8669da41d041a688778ab80ca9d7c7fcecbe64d8e0af`
  (50 keys, `consumed_into_canonical_cache=false`, claim-reserved ai033/ai034
  excluded by the published kit) minus the published status.log done-set:
  **ak011..ak050, 40 keys**, all serving_class 30118, all fresh targets of the
  pre-declared Part EJ plan (probe_order 556..597 extract rows).
- No published row is re-probed (the 10 done keys keep their published honest
  labels; same-condition re-probe prohibition untouched). The 20 inc1 raws are
  byte-fetched as seed files (concat sha256 `396abf1d...`) with their
  `# replay_done` terminal lines, so the pinned runner treats them as complete
  passes and never re-runs them.
- ak002 (solver-reported WIN, unconsumed) stays exactly as published:
  any WIN adoption is scrutiny-owner C++ gate `9193f5b6...` exclusive.
- The pre-drive status.log snapshot on this host is byte-identical to the
  published file (sha256 `12ae117842af0e13449c536191594790aa2dbe76a3d4cedf07e988f057c5138c`).

## 2. Pinned kit bytes (fetched from main at declaration time, pins verified on this host)

- `scripts/jsreplay.js` `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (= the published chain engine, byte-identical)
- `scripts/runbatch.sh` `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
  (BUDGET=15000000, WIN rc=45 / MISMATCH rc=42 / P1,P2-fail rc=43,44)
- `scripts/drive40_local_step.sh` `5e613cce8e67d30632388f83b6201786b6e2f69071fc3ed80f4e67c95d5abb18`
  (the corrected ak-regex edition on main; the wave-1 aj-regex defect `01a61daa`
  noted in its header is superseded and does not affect this drive)
- `scripts/make_batch40_keys.py` `e8588eb66bc84331ace3605e30c1f71e18c9e961dcfd07294c69e0399de66eaa`
- `input/ak001..ak050.input.csv` 50 files byte-fetched from the published kit
  (concat sha256 `8b9199c5f17ca3e903efb9c55c960d8c52051c78844f7648253669880835c75c`)
- val-gate: 4 molecule inputs + published baselines byte-fetched from
  `output/val-gate-host/` (byte-clones of the published batch-39 val-gate set).

## 3. Host val-gate re-run (drive-start requirement for a host change)

Replayed on this host with the pinned engine and pinned inputs, compared
node-exact on the `replay,` fields (budget,result,nodes) against the published
baselines:

- at2m-s5-1152921504606851072-536870946 @2M: (2000000,0,2000000) MATCH
- at2m-s5-1188950301626860544-536870912 @2M: (2000000,0,2000000) MATCH
- first-15m-s5-1152921504606851072-536870946 @15M: (15000000,2,3651923) MATCH
- second-15m-s5-1188950301626860544-536870912 @15M: (15000000,2,5040200) MATCH

4/4 node-exact: engine-equivalence on this host is established to the same
standard the original drive-start required.

## 4. Drive protocol (as pre-declared by Part EJ, unchanged)

- two-pass fresh-cold replay per key @ 15,000,000 nodes / order 0, key-by-key,
  2 workers max; increments of up to 10 keys + status.log snapshots; the final
  increment carries the complete 50.50 status.log.
- WIN rows append the pre-registered WIN-HALT marker and the drive CONTINUES
  (verdicts never consumed here; scrutiny-owner C++ gate exclusive for adoption).
- EXHAUSTED rows continue (honest UNKNOWN, no same-condition re-probe).
- Deterministic-mismatch HARD-STOP rc=42; inner `timeout 260` cap;
  `# replay_done` truncation guard (a truncated pass is re-run fresh-cold and
  never counts as evidence).
- Before every push the latest main is re-fetched and the design is
  append-only: only NEW raw files and the growing status.log are published;
  if any competing drive-step publication appears, this takeover defers
  immediately (record + next run).

## 5. Guardrails

- Every number derived here is bookkeeping; no root verdict, no coverage, no
  secured coverage is claimed or changed.
- Loss-only canonical adoption of the accumulated fresh exact-LOSS rows is a
  SEPARATE future Part with its own single-owner declaration (precedent EM/EL);
  nothing here adopts anything.
- **The standard 11x11 empty board, the 19 central-reply roots, the two-stone
  roots {49,60}/{59,60}, S2 {59,60}, and closure classes
  1/2/4/16371/20421/34908/30484/30345/30118 all remain UNKNOWN. Nothing in this
  Part changes that.**
