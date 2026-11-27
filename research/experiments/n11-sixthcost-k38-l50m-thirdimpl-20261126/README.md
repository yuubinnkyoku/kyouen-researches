# n11 sixth-cost k38 L50M third-impl verdict re-verification kit (2026-11-26)

Part SU. Closes the single-owner fresh declaration
research/log/2026-11-26-n11-sixthcost-k38-thirdimpl-verdict-single-owner-note.md
(wave A push f8b456e7): the k38 L50M LOSS row
(10376293541461626880:66048, legal 100) had a first-implementation L50M cold
pair (published at 2bc21cf3, both LOSS(2) nodes 21,839,049) and a delegated
pinned C++ second-implementation scrutiny gate (Part SS, 4/4 GATE-PASS,
target quadruple 100,50000000,2,21839049), but no third implementation. This
kit executes and publishes that third implementation.

## Outcome

Verdict-level agreement. third_impl.js (sha256 08ea958f...) resolves k38 as
LOSS(2), expansions 25,898,941, ttHits 13,358,093, ttOverwrites 21,704,637,
identical on all three cold runs (a 75.49s, b 75.73s, verify-legal 137.41s),
vs the published replica raws LOSS(2) nodes 21,839,049 x2 (L50M pair).
Anti-copy holds (expansions differ from replica nodes). No C5 hard stop.

C1 fresh calibration on this host: verify_tbl replica quads battery 95,670 ==
95,670, 195,044 triples checked, 0 mismatches, rc=0; anchor w2
10376293541461626880:131328 WIN(1) expansions 7,583,990, ttHits 4,157,314,
ttOverwrites 3,390,391 on two executions, identical quadruple (walls
22.57 / 22.46s; identical to the published k05/k20k33 calibration values).

C4 fail-closed input gates 2/2 GATE_FAIL with process exit status 1
(legal 101 -> derived=100 declared=101; stones 6 -> bits=5 declared=6).

Freshness: the k38 pair is machine-verified ABSENT from the canonical head
of record byte-clone input/canonical-head.cache
(dade15780ce6625cc70d93ba77b1560145dd2b9f096a53dce556d2fccf7e312b,
6,832 lines, fetched at HEAD 1f1577b0).

With this Part, k38 reaches the k13/k19/k20/k33 coverage level (ladder
primary L50M cold pair + Part SS delegated pinned C++ second-implementation
gate GATE-PASS node-exact + this third-implementation verdict-level
corroboration) and becomes an adoption-eligible input for a future adoption
Part against BASE dade15780. That adoption Part is explicitly NOT this kit;
it requires its own fresh declaration and a WIN/LOSS conflict policy review.

## Audit record

audit_k38.py: 31/31 gates ALL PASS, rc=0, deterministic byte-identical
across two runs (sha256 b6a403b2...); tamper battery 3/3 fail-closed
(T1 k38 verdict flip 2->1 -> determinism + verdict-level + verify-legal
gates rc=1; T2 replica at50m-run1 nodes edit -> repl_sha + repl_row +
stage-structure gates rc=1; T3 anchor w2 expansions edit -> C1 anchor gates
rc=1); every tamper touched only a full kit copy; the post-tamper clean
control rc=0 byte-identical to the baseline audit output
(out/tamper-log.txt pins the control-output sha inside).

## Layout

- scripts/third_impl.js, scripts/verify_tbl.js, scripts/jsreplay.js:
  byte-clones of the pinned scripts (pins checked by audit G1-G3).
  verify_tbl.js consumes the jsreplay.js byte-clone placed at its expected
  fixed host path /home/user/knowledge/kyouen-research/_class1297036830122704896-lane-kit/inv/jsreplay.js
  (same host-path disclosure as the k20/k33 Part; the byte-clone shipped
  here makes the kit self-contained).
- input/k38.input.csv: byte-clone of the published probe-kit input
  (sha256 b6ef9f43..., row target,0,5,10376293541461626880,66048,100,...).
- input/canonical-head.cache: byte-clone of the canonical head of record
  (Part ST merged cache, 285,726 B) for the freshness gate G7.
- out/: calib raws x3, k38 cold runs x3 (a/b/verify-legal), negative-gate
  raws x2, k38-replica-raws/ x5 (byte-copies of the published first-impl
  raws, sha-pinned), tamper-log.txt.
- audit_k38.py: the fail-closed auditor.

## Honest disclosures (this executing session)

1. Wave A's published declaration file is missing its final trailing
   newline (bash-wrapper transport artifact, 5,042 -> 5,041 bytes); the
   5,041-byte published byte is the authoritative declaration and its
   content is otherwise identical to the drafted text. Disclosed here
   because this lane byte-verifies every push.
2. The first anchor-w2 invocation on this host used the k20/k33 session's
   summary "legal 95" for the w2 anchor and fail-closed GATE_FAIL'd
   (derived=80 declared=95) before any run of the k38 target; the published
   k20k33 calibration raws (legalIn -1, legalDerived 80) were then fetched
   and the anchor re-run correctly with --legal=80. No k38 target execution
   happened before the correct calibration. Lesson reconfirmed: expected
   values are machine-extracted from published raws, never hand-copied from
   summaries.
3. All five replica raws were consumed at HEAD 1f1577b0 and sha-verified
   against the published probe-kit paths before the wave A push; they are
   re-published inside this kit so the auditor is self-contained.
4. Sandbox environment: Node.js v22.20.0, Python3; the delegated pinned C++
   gate remains run-and-published by Part SS and is NOT re-run here (its
   raws are unchanged).

## Status guard

Verification only. No verdict consumed, no cache row published, no class
status flipped, no route to any root certificate laid. The standard 11x11
empty board, the two-stone root {60,27}, its remaining third moves
{100,108}, S2, class 1/2/4, and every closure class remain UNKNOWN
throughout. Nodes and expansions are bookkeeping, never verdicts. An S5
LOSS raw is not a class closure claim, and LOSS rows transfer no root
verdict. The canonical head of record dade15780... is untouched by this Part.
