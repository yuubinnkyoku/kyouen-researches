# Session log: seven-row q=4 band width-69 extension (single-owner lane)

Session record of 2026-11-21 (batch 1 complete, batch 2 in progress).

## Batch 1 (complete, honest negative)

- Declaration: `research/log/2026-11-21-seven-row-q4-band-m69-single-owner-note.md`
  (declaration HEAD `94fe399ca6`), publication commit `b1f82cc3`.
- Results: fresh 2-for-2 sweep of all 199 published bases at width 69:
  426,099,795 row-capacity candidates / 43,009,353 safe / 0 safe maximal
  row-deficient. Holes-mode superset sweep: 435,695,973 / 45,368,697 / 0.
  1-for-0 (19-stone) checks over 199 x 20 removals: 0 maxima
  (`output/w69/selftest_1f0.json` positive/negative controls PASS).
- Interpretation: complete finite negative for those (fresh + holes) 2-for-2
  neighborhoods only; NOT a width-69 absence claim (3-edit surgery, seeded SA and
  other stone counts remain open). M_{7,4} remains in [69, 1929]; frontier 7x69;
  upper bound T_7 = 1929 (K0068) unchanged. K0827 not updated.
- Calibration at publication (5 blocks all PASS, `output/calibration.json`):
  pinned audit base53 at 7x57 = 1,436,643 / 60,921 / 2; width-68 witness width-69
  fresh neighborhood = 2,141,205 / 199,290 / 0 (= published stats_69.json); driver
  W=68 reproduces 11 published records and re-yields the width-68 witness
  stone-for-stone on all three positive w65 bases; holes mode at w57_0 width 60
  reproduces published fresh 1,599,648 / 95,722 / 4 ⊂ holes 1,641,372 / 103,379 / 23
  with the 4 fresh witnesses identical to `wit_w57_0_60.json`; 1-for-0 self-test.
- Determinism spot checks: repeated base runs deep-equal counters and witness
  arrays; ms fields are informal wall clock only.
- fetch-back at commit `b1f82cc3`: 11/11 published files byte-identical.

## Batch 2 (in progress) - restricted fresh 3-for-3, window x >= 52, width 69

- Declaration: `research/log/2026-11-21-seven-row-q4-band-m69-batch2-restricted-3edit-single-owner-note.md`
  (declaration HEAD `b1f82cc3`). Priority order w65 -> w66 -> w67(if present; the
  199-pool has no w67 tag) -> pool anchors -> w68witness seed; tier x=52 first.
- Engine notes (`scripts/enum_three.js`):
  - Reuses the pinned enum_two.js Board byte-identically; no geometry changes.
  - {3 additions + 1 kept} safety judged by direct 4x4 determinant instead of
    expanding the shared key3 curve cache (OOM avoidance for the long 200-base run).
  - Maximality: coverBy records are kept for ALL deficient-row targets including
    removed base cells. Pinned fresh-mode enum_two skipped occupied targets
    (a coverage gap case {1 add + 2 kept} on a removed cell); for batch 1 this was
    immaterial because the holes superset run (complete coverage, superset
    candidates) also returned 0. The batch-2 engine closes the gap directly.
  - Row-capacity pair/triple prechecks only cut candidates that provably violate
    the [3,3,3,3,3,3,2] shape; no valid candidate is excluded (case analysis in
    the session record; verified by control H set-equality against naive
    exhaustion without prechecks).
- Controls (11, all PASS, `output/w69/three/calibration.json`): A known-answer
  re-find of the published w68 witness in holes-refill mode (also re-verifies that
  coverage cases involving removed-cell targets are reachable); B window negative;
  C unsafe-base guard; D determinism; E fresh join; F brute re-judge of all
  emitted witnesses; G window monotonicity; H naive independent exhaustion
  cross-check (window x >= 56: 31,932 holes combos / 27,072 fresh combos, maximal
  sets exactly equal in both modes); I fresh |final ∩ base| = 17 invariant.
- Performance record: initial per-cell re-query maximality made some bases ~50x
  slower (base 173: 85/1140 removal triples in 150s); reworked to per-candidate
  curve marking + generation stamps, base 173 then completed in 57s. Typical
  40-60s per base. Two-core shard parallelism measured no net gain (each process
  ~2x slower); sequential budget chunks adopted.
- Operational notes: one execution-environment reset happened mid-lane before
  batch-2 scripts were published; part-1 artifacts survived because they were
  published to main immediately (policy: push early). Two shard-era result records
  (bases 175, 176) were lost in a local merge-file mistake and restored
  byte-identically from the run console record (noted in
  `output/w69/three/results.jsonl` `record_note`).
- Sweep progress at this checkpoint: 19/200 bases complete (w65 family first),
  56,663,096 triples examined / 43,160,550 safe / 0 safe maximal row-deficient;
  1 base (189) deferred for escalated retry. NOT complete; no negative claim yet.
- Next steps (this lane): finish 200/200 at tier x=52 including escalation
  retries; then the declared tier x=48; any found witness must pass the batch-1
  acceptance gates (independent two-system verification + negative controls)
  before K0827 / README headline changes; otherwise honest negative recorded in
  this dir.
