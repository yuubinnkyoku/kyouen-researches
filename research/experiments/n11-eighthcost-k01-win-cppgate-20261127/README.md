# Eighth-cost k01 WIN row C++ scrutiny gate (2026-11-27)

Delegated pinned C++ second-implementation scrutiny gate on the SINGLE
eighth-cost WIN row k01 (1297036692750860288:64). Twelfth execution of
the C++ gate lineage (after EN, EO, EQ, ET, EV, SK, SM, SN, SR, SW, SX),
the second WIN-side row after SX (seventh-cost k05). Scope, protocol,
pins and stop rules are pre-registered in the wave A declaration
(research/log/2026-11-27-n11-eighthcost-k01-win-cppgate-declaration.md,
publish-then-execute).

- Target: k01 at exact-replay budget 15000000, expected quadruple
  84,15000000,1,8514427 (machine-derived from the published at15m cold
  pair, both raws sha256 3be9db9b76f5dbd2756ffe51a2eb4e2c62c09f12d
  6999f7bc9a0376075479062); the at2m UNKNOWN stage raws (result 0 /
  nodes 2000000) are also pinned (stage policy: the 15M escalation was
  declared after the published 2M UNKNOWN raws).
- Anchors: anchor-at2m / anchor-aj001 / anchor-af039 (byte-clones of
  the published SW kit inputs; quadruples == the SW kit anchors block).
- Freshness: the k01 [lo,hi] pair ABSENT from the canonical head of
  record 5b6e77f7 (6,874 s5verdict rows WIN 202 / LOSS 6,672,
  sha-verified) - verdict-unconsumed at declaration, run and
  publication time.
- Audit: FRESH single-row fail-closed implementation (Part SS/SX
  precedent, disclosed) - not a byte transform of the batch audit; adds
  a G6 canonical-head freshness re-verification gate.
- Third-implementation corroboration: ALREADY PUBLISHED
  (CORROBORATION-PASS, third_impl 08ea958f, WIN(1) expansions 9987963
  x2 identical cold passes). A GATE-PASS here brings k01 to
  implementation-pillar parity with the k05 precedent (replica cold
  pair + C++ gate + third impl); adoption stays a separately declared
  Part under the parent batch's WIN/LOSS conflict policy.

This kit consumes NO verdict. The k01 WIN row stays a gate-verified
UNCONSUMED label; a WIN(1) gate result is only a verdict-level agreement
of the second implementation with the published first-implementation
cold pair. The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27}, its remaining third moves {100,108}, S2, class
1/2/4 and all closure classes stay UNKNOWN. Nodes are bookkeeping, never
verdicts. S5 raws are not class closure claims and not routes to the
root certificate.

Kit layout: scripts/ (maker, runner, audit, tamper battery),
input/ (k01 + 3 anchors + gate-rows.json), output/ (gate-status.log,
raw p1/p2 per row, audit_gate.json x4) published by the run-record
waves. MANIFEST-sha256.txt published with the kit and refreshed with
the run record.

## Run record (2026-11-27, publish-then-execute per declaration, wave A)

Waves A/B published first (declaration commit 28b01ced; kit commit
7ed92d18 with maker gates all PASS, 2 runs byte-identical). Official
execution 07:11:06Z-07:13:29Z sequential (pre-registered order
anchor-at2m, anchor-aj001, anchor-af039, then the single k01 target at
budget 15000000), all 4 rows GATE-PASS with (legal,budget,result,nodes)
exactly the published values (output/gate-status.log):
**k01 GATE-PASS 84,15000000,1,8514427 - the pinned C++ second
implementation reproduces the published WIN(1) verdict of the at15m
cold pair (3be9db9b x2) node-exactly** (second WIN-side row of the
gate lineage after SX). Results wave C 86d9659e.

Audit: fresh single-row audit PASS, 31/31 gates, 3 runs
byte-identical (audit_gate.json sha256 4c3a81fc575f7e36aa85f09e3b0bef
b30d5def5c6c4ea4df8cb7e017eb038b7e). Tamper battery 3/3 fail-closed
(T1 audit expected pin flip -> G0:target-expected + G3:k01 / T2 raw
k01.p1 nodes edit -> G2:k01 + G3:k01 / T3 phantom GATE-PASS line ->
G4) + clean control rc=0 (tamper.log, scratch copy only).

Pillar status after this Part: k01 (1297036692750860288:64) has the
replica cold pair (3be9db9b x2), the C++ second-implementation gate
(this Part) and the published third-implementation CORROBORATION-PASS
(third_impl 08ea958f) - implementation-pillar parity with the k05
precedent. Adoption stays a separately declared Part under the parent
batch's WIN/LOSS conflict policy. No verdict consumed: the k01 WIN row
stays a gate-verified UNCONSUMED label; the canonical head 5b6e77f7
(6,874 rows WIN202/LOSS6672) keeps it absent (G6 re-verified at audit
time). The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27}, its remaining third moves {100,108}, S2, class
1/2/4 and all closure classes stay UNKNOWN. Nodes are bookkeeping.

Host disclosure: zig 0.13.0 (tarball sha256 d45312e6...), zig c++ -O2,
binary not pinned. A pre-declaration sanity run of anchor-at2m on this
host (probe copy, before the declaration push) already reproduced
98,2000000,0,2000000.
