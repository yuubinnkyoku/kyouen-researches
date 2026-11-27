# n11 ultra-cheap u02 WIN-row pillars (C++ scrutiny gate + third-implementation corroboration)

Pillar kit of the single-owner declaration
`research/log/2026-11-27-n11-ultra-cheap-u02-pillars-declaration.md`
(commit `20360db5`) for the ultra-cheap u02 escalation WIN row
(`1297036830121656320:131074`, class 2251, legal 80, replica WIN(1)
nodes 3,167,121 at the 15M budget, published in
`research/experiments/n11-ultra-cheap-u02-escalation-15m-20261127`).

## Result: 3/3 pillars complete (GATE-PASS + CORROBORATION-PASS)

- **C++ second-implementation scrutiny gate: PASS.**  Gate source
  `kyouen_dfpn_root.cpp` (`9193f5b6...`) + headers (`5976935d...`,
  `2e36d694...`), byte-fetched from the published eleventh k01 cppgate
  kit and sha-verified, compiled with zig 0.13.0
  (`d45312e6...`) `-std=c++20 -O3`.  **u02 GATE-PASS
  `80,15000000,1,3167121`** (two fresh-cold passes, node-exact with the
  published replica raw).  Anchors GATE-PASS: at2m `98,2000000,0,2000000`,
  aj001 `84,30000000,2,5156075`, af039 `89,30000000,2,19234232`.
  Tamper battery 4/4 fail-closed (T1 wrong expected rc=43, T2 raw nodes
  edit rc=42, T3 missing input rc=2, T4 third_impl legal mismatch rc=1).
- **Third-implementation corroboration: CORROBORATION-PASS
  (verdict-level).**  Standing `third_impl.js` (`08ea958f...`),
  cap 400,000,000, wallcap 260, memo-power 22: both fresh
  post-declaration cold passes report **result 1 (WIN)**, expansions
  3,595,562 mutually identical and equal to the pre-registered value,
  ttHits 2,114,848, legal derived 80 = 80, reason clean, node_rc 0.
- Head freshness: u02 is ABSENT from the canonical head of record
  `0ec4080d...` (6,891 rows WIN 209 / LOSS 6,682, fetched and
  sha-verified).

The u02 WIN row is now adoption-eligible (replica cold pair + C++ gate
+ third implementation).  Adoption remains a SEPARATE future Part
(fresh single-owner declaration, WIN/LOSS conflict review, standing
flip-census review - class 2251 completion would be Board-verified
free_now at adoption time - and the merger).  The verdict is NOT
consumed here.

## Files

- input/u02.input.csv, input/anchor-at2m/aj001/af039.input.csv - gate
  input rows (byte-clones of the escalation kit and the u01-pillars kit).
- input/gate-rows.json - pre-registered expectations (schema
  n11-ultra-cheap-u02-win-pillars-rows-v1).
- scripts/gate_runner.sh - comment-block-only transform of the
  published u01-pillars runner (body byte-identical from `set -u`
  onward, diff-verified).
- output/raw/*.out - 8 gate raws (u02 + 3 anchors, 2 passes each).
- output/gate-status.log - the four official GATE-PASS status lines.
- output/ti/u02.p1.txt, u02.p2.txt - third-implementation raws.
- output/tamper-battery-stdout.log - the 4/4 fail-closed battery.
- output/pillars-summary.json - machine summary (schema
  n11-ultra-cheap-u02-win-pillars-summary-v1).
- Gate source, headers and third_impl.js are NOT republished here; they
  are pinned by sha256 and byte-fetched from the published kits on
  main, locally sha-verified before execution.

## Honest disclosures

- Pre-declaration third_impl calibration pair (disclosed in the
  declaration): result 1, expansions 3,595,562 x2 identical; the
  official pair was re-run fresh post-declaration and is
  expansions-identical to it.
- The gate binary emits a zig glibc-version warning (host 2.41 vs
  provided 2.39); all rows ran to replay_done.
- The tamper battery ran on the same kit after the official passes;
  its FAIL lines are recorded only in `tamper-battery-stdout.log`
  (removed from `gate-status.log`, which keeps the 4 official GATE-PASS
  lines).
- wall_s fields differ across passes; timing is not evidence.

## Meaning and non-meaning

Pillar bookkeeping only: NO verdict is consumed, no class-status
change, no adoption, no coverage claim.  Nodes and expansions are
never evidence of WIN or LOSS.  The standard 11x11 empty board, the
two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN.
