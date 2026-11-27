# 2026-11-27 n11 twelfth-cost ladder pre-audit instrument (pre-registration before wave B)

Completion log of the twelfth-cost ladder pre-audit Part. The
twelfth-cost batch stage-1 sweep (wave A single-owner declaration
`f6d29d16`, 51 exclusive keys of class `10376293541461626880:16777216`,
head basis `1e2eeda2`) had NOT published its wave-B raws on main at
any point during this session (checked repeatedly up to HEAD
`f2e09e1b8`, 18:52:27Z; the only twelfth-cost commits on main are the
selection `e588de1eb`, our independent selection cross-check
`5745ede1f`, and the declaration `f6d29d16` itself). Per the resume
note the batch is owned by the declaring lane, so this lane did not
run any of the 51 keys and instead published the audit instrument that
the raws will be held to, BEFORE they exist (pre-registration).

## Published

- Kit `research/experiments/n11-twelfthcost-ladder-preaudit-20261127/`
  (README, scripts/audit_twelfth_ladder.py, 3 clean run jsons + 3
  stdouts, preaudit-summary.json, MANIFEST-sha256.txt).
- Instrument sha256 `75a6ae6dafdb18fb64f7d0bf84c70a71cb251b37ed2e0fcb06271b22a1a1616a`.

## What the clean run verified (rc=0, 34 gates: 28 PASS + 6 PREREGISTERED)

- Stage S (selection-side, complete): selection json sha
  `1119d01b...` / schema / class / head_basis pins; 51 unique keys with
  pinned first/last; bands {5,041,585x1, 5,069,670x1, 5,234,938x11,
  5,932,112x38}; proxy_exclusive_sum 293,115,829 recomputed from the
  entries; selector `ea2b8331...`, jsreplay `84585617...`, kit README
  `74131df1...`, declaration `395cbeac...` (class + head-pin +
  WIN-stop-rule + single-owner markers); all 55 selection-kit files
  MANIFEST sha-verified; all 51 input CSVs order+legal-fidelity
  verified against exclusive_probe_order; head of record `1e2eeda2...`
  census 6,890 rows / WIN 208 / LOSS 6,682 with zero duplicate keys and
  51/51 key freshness.
- Stage B (batch-side, PRE-REGISTERED): six content gates for the
  wave-B raws (key subset, 2M cold-pair shape, result semantics,
  escalation discipline, WIN-stop content rule, per-(key,budget) node
  identity). They activate automatically once the raws appear under the
  selection kit's output/raw/.

## Verification

- Three cold passes byte-identical (json + stdout).
- Tamper battery 5/5 fail-closed: T1 k07 input CSV legal 97->98
  (byte-diff verified; the first sed attempt was a silent no-op because
  k07 legal is 97, redone), T2 phantom head row, T3 declaration
  one-char edit, T4 selection json key digit flip (rc=1 fail-closed but
  ungraceful: JSONDecodeError after the sha gate already failed, no
  gate JSON emitted, disclosed), T5 k03/k04 CSV swap. Clean control
  re-PASS byte-identical to run1.
- Batch-stage mock self-test on synthetic raws (not published as data):
  a WIN-stop violation (15M row for k03 after a 15M WIN at k02) is
  caught by B5 (rc=1) and a clean mock passes all six B-gates (rc=0).
  The mock caught a real stage-B bug before publication (escalation-order
  map keyed by key string vs (lo,hi) tuple grouping -> KeyError; fixed;
  stage-S output byte-unchanged).

## Resume

- On the next run, re-fetch main. If the wave-B raws of `f6d29d16` are
  published, run the instrument against them (same command; the six
  B-gates activate) and publish the full-audit result as a follow-up
  Part, then the WIN-row pillars (C++ gate + third-impl) and adoption
  follow the k01-eleventh precedent, owned by whoever declares first.
- Working tree of this session: selection kit copy + head cache +
  declaration fetched from main and sha-verified (not durable; all
  inputs are re-fetchable from main by sha pin).

## Guards

Scheduling and audit bookkeeping only; NO verdict is claimed or
consumed. The standard 11x11 empty board: UNKNOWN. All 19
central-reply roots: UNKNOWN. The two-stone root {60,27} and its
remaining third moves 100/108: UNKNOWN. Nodes and proxy values are
bookkeeping, never evidence of WIN or LOSS.
