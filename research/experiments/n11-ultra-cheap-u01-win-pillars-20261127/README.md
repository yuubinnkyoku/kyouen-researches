# n11 ultra-cheap u01 WIN-row pillars (C++ scrutiny gate + third-implementation corroboration)

Pillar kit of the single-owner declaration
`research/log/2026-11-27-n11-ultra-cheap-u01-pillars-declaration.md`
(commit `616bec32`) for the ultra-cheap batch u01 WIN row
(`1153485622925590528:0`, class 1849, legal 88, replica WIN(1) nodes
4,893,014 at the 15M budget, published in
`research/experiments/n11-ultra-cheap-batch-stage1-2m-20261127`).

## Result: 3/3 pillars complete (GATE-PASS + CORROBORATION-PASS)

- **C++ second-implementation scrutiny gate: PASS.**  Gate source
  `kyouen_dfpn_root.cpp` (`9193f5b6...` @`154f3b7a`) + headers
  (`5976935d...`, `2e36d694...`), byte-fetched from the published
  eleventh k01 cppgate kit and sha-verified, compiled with zig 0.13.0
  (`d45312e6...`) `-std=c++20 -O3`.  **u01 GATE-PASS
  `88,15000000,1,4893014`** (two fresh-cold passes, node-exact with the
  published replica raw).  Anchors GATE-PASS: at2m `98,2000000,0,2000000`,
  aj001 `84,30000000,2,5156075`, af039 `89,30000000,2,19234232`.
  Tamper battery 4/4 fail-closed (T1 wrong expected rc=43, T2 raw nodes
  edit rc=42, T3 missing input rc=2, T4 third_impl legal mismatch rc=1).
- **Third-implementation corroboration: CORROBORATION-PASS
  (verdict-level).**  Standing `third_impl.js` (`08ea958f...`),
  cap 400,000,000, wallcap 260, memo-power 22: both fresh
  post-declaration cold passes report **result 1 (WIN)**, expansions
  5,646,148 mutually identical and equal to the pre-registered value,
  ttHits 3,187,475, legal derived 88 = 88, reason clean, node_rc 0.
- Head freshness: u01 is ABSENT from the canonical head of record
  `1e2eeda2...` (6,890 rows WIN 208 / LOSS 6,682, fetched and
  sha-verified).

The u01 WIN row is now adoption-eligible (replica cold pair + C++ gate
+ third implementation).  Adoption remains a SEPARATE future Part
(fresh single-owner declaration, WIN/LOSS conflict review, standing
flip-census review - class 1849 completion would be Board-verified
free_now at adoption time - and the merger).  The verdict is NOT
consumed here.

## Files

- input/u01.input.csv, input/anchor-at2m/aj001/af039.input.csv - gate
  input rows (byte-clones of the batch kit and eleventh cppgate kit).
- input/gate-rows.json - pre-registered expectations (schema
  n11-ultra-cheap-u01-win-pillars-rows-v1).
- scripts/gate_runner.sh - comment-block-only transform of the
  published SW/SX runner (sha256 `e82d35e5...`).
- output/raw/*.out - 8 gate raws (u01 + 3 anchors, 2 passes each).
- output/gate-status.log - the four GATE-PASS status lines.
- output/ti/u01.p1.txt, u01.p2.txt - third-implementation raws.
- output/tamper-battery-stdout.log - the 4/4 fail-closed battery.
- output/pillars-summary.json - machine summary (schema
  n11-ultra-cheap-u01-win-pillars-summary-v1).
- Gate source, headers and third_impl.js are NOT republished here; they
  are pinned by sha256 and byte-fetched from the published kits on
  main, locally sha-verified before execution.

## Honest disclosures

- Pre-declaration third_impl calibration pair (disclosed in the
  declaration): result 1, expansions 5,646,148 x2 identical; the
  official pair was re-run fresh post-declaration and is
  expansions-identical to it.
- The gate binary emits a zig glibc-version warning (host 2.41 vs
  provided 2.39); all rows ran to replay_done.
- A first tamper-battery recording pass ran on an already-tampered copy
  (T1 then detected the stale p2 mismatch, rc=42); the battery was
  re-recorded on a fresh copy and that clean log is published.
- wall_s fields differ across passes; timing is not evidence.

## Meaning and non-meaning

Pillar bookkeeping only: NO verdict is consumed, no class-status
change, no adoption, no coverage claim.  Nodes and expansions are
never evidence of WIN or LOSS.  The standard 11x11 empty board, the
two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN.
