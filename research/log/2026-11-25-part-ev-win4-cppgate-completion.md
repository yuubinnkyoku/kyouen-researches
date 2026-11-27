# Part EV completion: closure-batch WIN-4 C++ scrutiny gate (b018/d002/e002/f017, 2026-11-25/26)

COMPLETED. The fifth C++ second-implementation scrutiny gate in the
central-reply chain closed the last four 2026-11-22 closure-batch WIN rows
that were still awaiting a scrutiny owner. Publish-then-execute, all waves
landed on main, every fetch-back byte-verified:

* Wave A declaration 666fefd3 (Part EV declaration, target pool machine-derived,
  third-impl cross-SSOT, honest notes incl. the ET cwd lesson).
* Wave B kit b2f54948 (7 input CSVs, gate-rows-ev.json SSOT registry, runner
  31dc23c3 / audit cfbba264 / maker 5bc40ab9); pre-run fetch-back 11/11
  byte-identical.
* Official execution 2026-11-25T23:58:30Z - 2026-11-26T00:02:02Z, sequential,
  anchors first: 7/7 GATE-PASS - anchor-at2m 98,2000000,0,2000000;
  anchor-aj001 84,30000000,2,5156075; anchor-af039 89,30000000,2,19234232;
  b018 60,15000000,1,3549602; d002 73,15000000,1,5359994;
  e002 79,15000000,1,14112632; f017 82,15000000,1,3522635. Two fresh-cold
  passes per row, node-exact vs the published batch-kit raws, zero
  MISMATCH / GATE-FAIL / GATE-CRASH / TRUNCATED. Gate binary built from the
  pinned source at 154f3b7a (binary sha256 06be2036, not pinned: source
  pins authoritative).
* Audit 4/4 runs byte-identical (canonical audit_gate.json sha256
  0327dad83f7c33d475656d8d1f9ccd2e67c3b78f8f394b9a5daf74c2b96c91c4), G1-G5
  all PASS, every audit invocation with absolute-path cwd (ET lesson).
* Tamper battery 3/3 fail-closed: T1 audit-ROWS pin break -> G3:b018 rc1;
  T2 raw d002.p1 node byte-alter -> G2:d002 + G3:d002 rc1; T3 phantom
  GATE-PASS -> G4 passes=8/7 rc1. Protocol order pin-assert -> backup ->
  tamper -> pre-assert -> audit -> restore -> restore-assert held on every
  tamper; all restores byte-verified; clean controls rc0. Honest note: T1/T2
  were each run twice with identical tamper bytes because the first
  gate-name capture probe used wrong JSON key names (KeyError, no effect on
  run artifacts); the recheck recorded G3:b018 and G2:d002+G3:d002.
* Wave C f6ab5c30 (14 raws + gate-status.log + audit_gate.json + run1-4 +
  tamper.log + t1/t2 result JSON + both battery scripts); fetch-back
  36/36 byte-identical.
* Wave D (this commit): kit README.md b0416d96 + MANIFEST-sha256.txt
  34d7768b (36/36 kit-file pins, README/MANIFEST excluded per convention,
  sha256sum -c all OK) at
  research/experiments/n11-centralreply-closure-wins-b018d002e002f017-cppgate-20261125/.

What this changes: the four WIN rows (b018 class 16757 batch-1 dual-class,
d002 class 20421 batch-3, e002 class 16371 batch-4, f017 class 12264
batch-5) are now gate-verified UNCONSUMED labels eligible for a future
adoption Part in the EP/ER/EU pattern (declare; re-derive from SSOT; merge
into the canonical head with WIN/LOSS conflict check). Nothing is consumed
here. Single-pass node total 52,935,170 / two-pass bill 105,870,340 are
bookkeeping.

Guarantee text: the standard 11x11 empty board, all 19 central-reply roots,
S2, class 1/2/4, and all closure classes remain UNKNOWN at all times.
Verdicts are not consumed. nodes are bookkeeping. No win/loss, coverage, or
secured-coverage claim is made or implied.
