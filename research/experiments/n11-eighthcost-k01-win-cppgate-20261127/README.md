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

## Run record

PENDING (wave A declaration published at HEAD 28b01ced; official
execution to follow on this host: zig 0.13.0 tarball sha256
d45312e6..., zig c++ -O2, binary not pinned; pre-registered order
anchor-at2m, anchor-aj001, anchor-af039, then the single k01 target at
budget 15000000; 2 fresh-cold passes per row, HARD-STOP on mismatch).
A pre-declaration sanity run of anchor-at2m on this host already
reproduced 98,2000000,0,2000000 (disclosed; before the declaration
push, on the probe copy, not the kit).
