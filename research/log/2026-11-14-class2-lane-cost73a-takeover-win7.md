# 2026-11-14 class2-lane: cost-73a completed by takeover - WIN7 bit81 certificate fully verified; the cost-73 band and the best class-2 S5 target's child sweeps are complete (session 11)

Long-term lane, 11th session. Started from HEAD `6ebceabb` (after-cost73d frontier:
solved 920, remaining 6,927, sum 545,068, open 5,196/408,718; best class-2 target
11 orbits / 771). The parallel class4-lane was mid-flight on cost-84/cost-86a, and the
parallel class2 sessions 9/10 had completed 73b/73c/73d/73e/74, leaving cost-73a as the
only unfinished child of the best class-2 S5 target `00000000000000809082000000000000`
(session 9 had claimed it, found 1 WIN7 (bit 81) at 64/73 candidates, then lost its
environment with the raw batches unpushed).

## Takeover and full deterministic re-run

- Claim updated on main before any batch push (commit `cee436dc`); raw batches 1-11
  pushed as completed (73 candidates in 11 batches + pilot d6 control per batch).
- **73 candidates: 1 WIN7-D10 (bit 81) + 72 REFUTED, 0 capped, 383,290,602 nodes.**
- **Cross-restart control PASS**: the 64 candidates session 9 had resolved sum to
  exactly 324,426,606 nodes in this session's independent re-run (node-exact), including
  the WIN7 bit 81 at exactly 5,530,773 nodes. Remaining 9 candidates (bits
  110,111,112,113,116,117,118,119,120): 58,863,996 nodes, all REFUTED.
- Determinism rerun of the heaviest bits 92 (20,603,022), 23 (18,497,705), 48
  (16,806,863) and the WIN7 bit 81 (5,530,773): fresh separate processes, node-exact.
- Cross-engine check with `runner_fbs20.ts` (repo FBS=1<<20 instrumented engine from
  `n11-fbt-saturation-audit-20261114`): verdicts and node counts bit-exact identical,
  fbtDrops=0, fbtMaxProbe<=6 on all four.

## WIN7 bit 81 certificate - all verification PASS

- Root `00000000000200809082000000000010` (7 stones; child | (1<<81), arithmetic
  cross-checked against the known bit103/bit37 root reproductions).
- Extraction: `class4_child1_cert_extractor_exact.ts` (repo-verbatim, blind kill table,
  FBS=1<<20): 37,309 rows, 8,777,255 extraction nodes, fbt_drops=0, fatal=null, all 51
  per-move extractions ok and uncapped. Rows sorted (no duplicates) before verification
  per the established extractor note.
- Independent verifier `verify_bit7_win7_cert.ts`: root-check PASS (stones=7,
  loserMobility=51 = independent legal_candidates.py enumeration); 51/51 sub-roots
  PASS; union of consumed winner states equals the row set exactly (0 missing /
  0 extra); terminal ranges within [13,17].
- Pushed as a line-boundary 2-part split + README with join md5
  `ecf3ab773961f877c3044862ba2ad7b7`; remote md5s verified identical after re-push.
- Root absent from all 20 published win7-certificates records (grepped: 0 hits).

## Operational findings

1. **push_files drops exactly one trailing newline**: the first certificate-part push
   landed without the final newline (line-count off by one, join corrupted at the
   seam). Re-pushing with an explicit extra trailing newline restored byte-exact
   content; remote md5 now equals local. Any future part push must append one extra
   newline and verify by md5 after landing.
2. Background jobs (`cmd1 & cmd2 & wait`) do NOT die at the command boundary in this
   environment: an orphan process appended a duplicate copy to a batch file while the
   sequential rerun wrote the same path. Both copies were bit-exact (identical
   verdicts/nodes, ms differs only), but the file was reconstructed clean. Sequential
   single-process batches remain the safe mode.
3. Sequential batch speed: ~430k nodes/s single process; an 8-candidate batch of this
   child runs ~110-160 s, safely inside the 280 s budget.

## Lane state after this sweep

- The cost-73 band is complete: 73a WIN7 (bit81, this record), 73b/73c/73e sterile,
  73d WIN7 (bit48, integrated at solved 920).
- **Every one of the best class-2 S5 target's remaining S6 children has now been
  swept** (65b/66a/66b/69b/69d/70/73a/73b/73c/73d/73e/74); the frontier can now move
  only through the 73a receipt integration (frontier recompute after cost-73a follows
  in this session).
- Next class-2 blocker candidates after this target closes (from the after-cost73d
  S5 ranking): `00000000000000809102000000000000` (40 orbits / 2,850) and
  `00000000000000803202000000000000` (41 / 2,776).

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}: UNKNOWN.
class 2 / class 4 blockers: UNKNOWN. (REFUTED-D10 decides nothing about the child;
WIN7 certificates prove only individual 7-stone roots.)