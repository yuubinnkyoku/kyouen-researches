# n11-ninthcost-parked3-l50m-cppgate-20261127

Ninth-cost parked-3 L50M row C++ scrutiny gate (the three stage-3 50M
resolved rows k02/k04/k07 of class 1297036692683751424:134217728, wave B
commit 41b331d1, `output/batch-summary-l50m.json` of the ninth-cost
exclusive-probe kit). Sixteenth execution of the C++ gate lineage.
Scope, protocol, pins and stop rules are pre-registered in the wave A
declaration
(research/log/2026-11-27-n11-ninthcost-parked3-l50m-cppgate-declaration.md,
commit 30c7a43a, publish-then-execute).

- Targets (expected quadruples machine-derived from the published L50M
  cold pairs): k02 `87,50000000,1,18123017` / k04
  `98,50000000,2,24309957` / k07 `96,50000000,1,27621128`; the input
  pins are the L50M ledger `inputs` block values (8c2a0438... /
  dc3bfeb4... / 928a1b98...).
- Anchors: anchor-at2m / anchor-aj001 / anchor-af039 (byte-clones of
  the published SW kit inputs; quadruples == the SW kit anchors block).
- Freshness: all three [lo,hi] pairs ABSENT from the canonical head of
  record 0935c94c (6,875 s5verdict rows WIN203/LOSS6672, sha-verified,
  absence machine-checked at kit assembly and re-verified by audit G6)
  - verdict-unconsumed at declaration, run and publication time.
- Audit: batch fail-closed audit, DISCLOSED ADAPTATION of the published
  n11-ninthcost-4lossrest-cppgate batch audit (target pins, budgets,
  key-pairs and schema names changed to the parked3-L50M values; G0-G6
  semantics unchanged), canonical-head freshness re-verification gate
  (G6, N9_HEAD, no skip).
- Third-implementation corroboration: ALREADY PUBLISHED for all three
  rows (CORROBORATION-PASS, third_impl 08ea958f, kit
  n11-ninthcost-parked3-l50m-thirdimpl-corroboration-20261127, commit
  a8867e6a). A GATE-PASS here brings k02/k04/k07 to implementation
  pillar parity (replica cold pair + C++ gate + third impl); all twelve
  resolved ninth-cost rows (9 LOSS + 3 WIN) then have 3/3 pillars.
- Disclosed kit-assembly deviations: (1) no maker script; all pins
  extracted and byte-verified mechanically (sha256sum) from the
  published ninth-cost kit L50M ledger, the SW kit anchor inputs and
  the canonical head cache, re-enforced fail-closed by the audit
  G0/G5/G6 pins; (2) scripts/gate_runner.sh is a byte-clone of the
  published n11-ninthcost-4loss-cppgate runner (comment-block-only
  transform; code lines machine-identical, asserted at assembly);
  (3) the gate binary is built from the pinned source 9193f5b6 @
  154f3b7a with zig 0.13.0 (tarball sha d45312e61ebcc48032b77bc4cf7fd
  6915c11fa16e4aad116b66c9468211230ea); binary not pinned; (4) waves
  B (kit) and C (outputs) are published in this single commit, after
  the wave-A declaration push; the official run happened between the
  two pushes, in the pre-registered order.

This kit consumes NO verdict. The three rows stay gate-verified
UNCONSUMED labels; a WIN(1)/LOSS(2) gate result is only a verdict-level
agreement of the second implementation with the published
first-implementation L50M cold pairs. The standard 11x11 empty board,
every central-reply root, the two-stone root {60,27}, its remaining
third moves {100,108}, S2, class 1/2/4 and all closure classes stay
UNKNOWN. Nodes are bookkeeping, never verdicts. S5 raws are not class
closure claims and not routes to the root certificate.

Kit layout: scripts/ (runner byte-clone, audit, tamper battery),
input/ (3 target inputs + 3 anchor inputs + gate-rows.json), output/
(gate-status.log, raw p1/p2 per row, audit_gate.json + 3 audit runs,
tamper-battery-stdout.log). MANIFEST-sha256.txt published with the kit.

## Run record (2026-11-27, publish-then-execute per declaration 30c7a43a)

Official execution 12:42:43Z-12:50:10Z sequential (pre-registered
order anchor-at2m, anchor-aj001, anchor-af039, then k02, k04, k07 at
budget 50000000), all 6 rows GATE-PASS with (legal,budget,result,nodes)
exactly the published values (output/gate-status.log):

- anchor-at2m GATE-PASS 98,2000000,0,2000000
- anchor-aj001 GATE-PASS 84,30000000,2,5156075
- anchor-af039 GATE-PASS 89,30000000,2,19234232
- k02 GATE-PASS 87,50000000,1,18123017
- k04 GATE-PASS 98,50000000,2,24309957
- k07 GATE-PASS 96,50000000,1,27621128

The pinned C++ second implementation reproduces the published L50M
verdicts of the three cold pairs node-exactly, including the two
WIN-side rows k02/k07 (4th and 5th WIN-side gate rows of the gate
lineage). Two-pass node bill: k02 36,246,034 / k04 48,619,914 /
k07 55,242,256 + anchors 4,000,000+10,312,150+38,468,464 (bookkeeping).

Audit: batch audit PASS, 3 runs byte-identical (audit_gate.json sha256
3155fe0321571ecaa85549418e90ec9ad0c8dfe2bf233930fe8e7815bb5147c2).
Tamper battery 4/4 fail-closed (T1 expected-pin flip k02 -> G0+G3 /
T2 raw k02.p1 nodes edit -> G2+G3 / T3 phantom GATE-PASS -> G4
passes=7/6 / T4 head byte append -> G6) + clean control rc=0
(tamper-battery-stdout.log; scratch copies only).

Honest disclosure: pre-declaration host sanity run anchor-at2m @2M
(published anchor budget only) is disclosed in the declaration. The
runner's p1/p2 wall_s fields differ per pass; timing is not evidence.

Pillar status after this Part: ALL twelve resolved ninth-cost rows
(the nine 15M-stage rows k01/k03/k05/k06/k08..k11/k12 via the earlier
gate kits + k02/k04/k07 here) have all
three implementation pillars (replica cold pair + C++ gate + third
impl). Remaining for the batch: the separately declared adoption Part
(fresh single-owner declaration, WIN/LOSS conflict review, merger
90711961 + flip census review for the WIN rows per the SZ/EM
precedent, BASE 0935c94c).
