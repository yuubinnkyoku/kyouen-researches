# n11-ninthcost-k12-win-cppgate-20261127

Ninth-cost k12 WIN row C++ second-implementation scrutiny gate
(single WIN-side row, fourteenth execution of the C++ gate lineage after
EN, EO, EQ, ET, EV, SK, SM, SN, SR, SW, SX, the eighth-cost k01 WIN gate
and the ninth-cost 4 LOSS gate). Scope, protocol, pins and stop rules
are pre-registered in the wave A declaration
(research/log/2026-11-27-n11-ninthcost-k12win-cppgate-declaration.md,
publish-then-execute).

- Target: k12 (1297036692683751424:134217792, legal 92) at exact-replay
  budget 15000000, expected quadruple `92,15000000,1,14521862`
  (machine-derived from the published wave C7 at15m cold pair, both
  raws result 1 / nodes 14521862); the at2m UNKNOWN stage raws
  (result 0 / nodes 2000000 cold pair) are pinned (stage policy).
- Anchors: anchor-at2m / anchor-aj001 / anchor-af039 (byte-clones of
  the published SW kit inputs; quadruples == the SW kit anchors block).
- Freshness: the k12 [lo,hi] pair ABSENT from the canonical head of
  record 0935c94c (6,875 s5verdict rows WIN203/LOSS6672, sha-verified,
  absence machine-checked at kit assembly) - verdict-unconsumed at
  declaration, run and publication time.
- Audit: single-row fail-closed audit, DISCLOSED ADAPTATION of the
  published n11-ninthcost-4loss-cppgate batch audit (target set reduced
  to k12, all pins and schema names changed to the k12 values, G0-G6
  semantics unchanged), with the canonical-head freshness
  re-verification gate (G6, N9_HEAD, no skip).
- Third-implementation corroboration: ALREADY PUBLISHED
  (CORROBORATION-PASS, third_impl 08ea958f, WIN(1) expansions 17247041
  x2 identical cold passes, kit d9ce050a). A GATE-PASS here brings k12
  to implementation-pillar parity with the k05/eighth-k01 precedent
  (replica cold pair + C++ gate + third impl); adoption stays a
  separately declared Part under the parent batch's WIN/LOSS conflict
  policy.
- Disclosed kit-assembly deviations: (1) no maker script in this kit;
  all pins were extracted and byte-verified mechanically (sha256sum)
  from the published ninth-cost kit, the published 4loss gate kit and
  the published canonical head cache, and are re-enforced fail-closed
  by the audit G0/G5/G6 pins; (2) scripts/gate_runner.sh is a
  byte-clone of the published n11-ninthcost-4loss-cppgate runner (its
  comment block names that kit; machine-identical logic); (3) the gate
  binary is built from the pinned source 9193f5b6 @ 154f3b7a with zig
  0.13.0 (tarball sha d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad11
  6b66c9468211230ea); binary not pinned.

This kit consumes NO verdict. The k12 WIN row stays a gate-verified
UNCONSUMED label; a WIN(1) gate result is only a verdict-level
agreement of the second implementation with the published
first-implementation cold pair. The standard 11x11 empty board, every
central-reply root, the two-stone root {60,27}, its remaining third
moves {100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN.
Nodes are bookkeeping, never verdicts. S5 raws are not class closure
claims and not routes to the root certificate.

Kit layout: scripts/ (runner byte-clone, audit, tamper battery),
input/ (k12 + 3 anchors + gate-rows.json), output/ (gate-status.log,
raw p1/p2 per row, audit_gate.json) published by the run-record waves.
MANIFEST-sha256.txt published with the kit and refreshed with the run
record.
