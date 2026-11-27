# n11-ninthcost-4lossrest-cppgate-20261127

Ninth-cost k08-k11 LOSS row C++ scrutiny gate (the four REMAINING
15M-stage LOSS rows of class 1297036692683751424:134217728, wave C7
commit 838ee2f2; complements n11-ninthcost-4loss-cppgate-20261127
which gated k01/k03/k05/k06). Fifteenth execution of the C++ gate
lineage. Scope, protocol, pins and stop rules are pre-registered in the
wave A declaration (research/log/2026-11-27-n11-ninthcost-4lossrest-cppgate-declaration.md,
publish-then-execute).

- Targets (expected quadruples machine-derived from the published wave
  C7 at15m cold pairs): k08 `98,15000000,2,3306768` / k09
  `92,15000000,2,4711230` / k10 `96,15000000,2,5542083` / k11
  `97,15000000,2,5931960`; the at2m UNKNOWN stage raws of all four keys
  are pinned (stage policy).
- Anchors: anchor-at2m / anchor-aj001 / anchor-af039 (byte-clones of
  the published SW kit inputs; quadruples == the SW kit anchors block).
- Freshness: all four [lo,hi] pairs ABSENT from the canonical head of
  record 0935c94c (6,875 s5verdict rows WIN203/LOSS6672, sha-verified,
  absence machine-checked at kit assembly) - verdict-unconsumed at
  declaration, run and publication time.
- Audit: batch fail-closed audit, DISCLOSED ADAPTATION of the published
  n11-ninthcost-4loss-cppgate batch audit (target pins and schema
  names changed to the k08-k11 values, G0-G6 semantics unchanged),
  with the canonical-head freshness re-verification gate (G6, N9_HEAD,
  no skip).
- Third-implementation corroboration: ALREADY PUBLISHED for all four
  rows (CORROBORATION-PASS, third_impl 08ea958f, kit
  n11-ninthcost-4loss-rest-thirdimpl-corroboration-20261127, commit
  bfe4f240). A GATE-PASS here brings k08-k11 to implementation-pillar
  parity (replica cold pair + C++ gate + third impl).
- Disclosed kit-assembly deviations: (1) no maker script; all pins
  extracted and byte-verified mechanically (sha256sum) from the
  published ninth-cost kit and canonical head cache, re-enforced
  fail-closed by the audit G0/G5/G6 pins; (2) scripts/gate_runner.sh
  is a byte-clone of the published n11-ninthcost-4loss-cppgate runner;
  (3) the gate binary is built from the pinned source 9193f5b6 @
  154f3b7a with zig 0.13.0 (tarball sha d45312e61ebcc48032b77bc4cf7fd
  6915c11fa16e4aad116b66c9468211230ea); binary not pinned.

This kit consumes NO verdict. The four LOSS rows stay gate-verified
UNCONSUMED labels; a LOSS(2) gate result is only a verdict-level
agreement of the second implementation with the published
first-implementation cold pairs. The standard 11x11 empty board, every
central-reply root, the two-stone root {60,27}, its remaining third
moves {100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN.
Nodes are bookkeeping, never verdicts. S5 raws are not class closure
claims and not routes to the root certificate.

Kit layout: scripts/ (runner byte-clone, audit, tamper battery),
input/ (4 target inputs + 3 anchor inputs + gate-rows.json), output/
(gate-status.log, raw p1/p2 per row, audit_gate.json) published by the
run-record waves. MANIFEST-sha256.txt published with the kit and
refreshed with the run record.

## Run record (2026-11-27, publish-then-execute per declaration, wave A/B commit 95988209)

Official execution 10:57:34Z-11:00:55Z sequential (pre-registered order
anchor-at2m, anchor-aj001, anchor-af039, then k08, k09, k10, k11 at
budget 15000000), all 7 rows GATE-PASS with (legal,budget,result,nodes)
exactly the published values (output/gate-status.log):

- k08 GATE-PASS 98,15000000,2,3306768
- k09 GATE-PASS 92,15000000,2,4711230
- k10 GATE-PASS 96,15000000,2,5542083
- k11 GATE-PASS 97,15000000,2,5931960

The pinned C++ second implementation reproduces the published LOSS(2)
verdicts of the four at15m cold pairs node-exactly.

Audit: batch audit PASS, 3 runs byte-identical (audit_gate.json sha256
46f44f28e8f0713fe94a8ee612da7cfcd184eb984fe65bd6ba65a2e01a6b1af9).
Tamper battery 4/4 fail-closed (T1 expected-pin flip k08 -> G0+G3 /
T2 raw k08.p1 nodes edit -> G2+G3 / T3 phantom GATE-PASS -> G4
passes=8/7 / T4 head byte append -> G6) + clean control rc=0
(tamper-battery-stdout.log; scratch copies only).

Honest disclosure (kit-assembly defect caught by the kit's own
fail-closed gate): the wave B published audit contained a
hand-transcribed 63-character k09 input pin (one character dropped).
The first audit run FAIL-closed at G5:k09 exactly as designed; the pin
was re-extracted mechanically (sha256sum of input/k09.input.csv ==
published ninth-cost kit MANIFEST pin 2d11337df8ac75cc25f9d7a550f3f9
c76e7df25e25e4ab99f7184c06880684687) and the corrected audit_gate.py
is republished with this run record. No target row had run before the
fix; the gate-status log and all raws are unaffected.

Pillar status after this Part: ALL eight resolved ninth-cost LOSS rows
(k01/k03/k05/k06 via the 4loss gate, k08/k09/k10/k11 via this Part) and
the k12 WIN row (k12 gate kit) have all three implementation pillars.
Remaining for the batch: L50M escalation declarations for the parked
k02/k04/k07, and the separately declared adoption Part (fresh
single-owner declaration, WIN/LOSS conflict review, merger + flip
census per the SZ/EM precedent, BASE 0935c94c).
