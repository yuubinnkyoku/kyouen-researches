# n11 sixth-cost k38 L50M third-impl verdict re-verification: completion log (2026-11-26)

Part SU closes complete. Closes the single-owner fresh declaration
research/log/2026-11-26-n11-sixthcost-k38-thirdimpl-verdict-single-owner-note.md
(wave A push f8b456e7), executing the third-implementation corroboration
that the Part SS completion and the Part ST completion both left open for the
k38 row of the sixth-cost exclusive S5 batch.

## Outcome

Verdict-level agreement. The third implementation (third_impl.js sha256
08ea958f..., the same pinned script the k20/k33 Part used) resolves:

- k38 `10376293541461626880:66048` (legal 100): **LOSS(2)**, expansions
  25,898,941, ttHits 13,358,093, ttOverwrites 21,704,637, identical on all
  three cold runs (a 75.49s, b 75.73s, verify-legal 137.41s, identical
  verdict/expansions/ttHits), vs the published first-implementation L50M
  cold pair LOSS(2) nodes 21,839,049 x2 (at 2bc21cf3) and the Part SS
  delegated pinned C++ second-implementation gate (GATE-PASS, target
  quadruple 100,50000000,2,21839049 node-exact). Anti-copy holds
  (expansions 25,898,941 != 21,839,049).

C1 fresh calibration on this host: verify_tbl replica quads battery 95,670
== 95,670, 195,044 triples checked, 0 mismatches, rc=0; anchor w2
`10376293541461626880:131328` WIN(1) expansions 7,583,990, ttHits
4,157,314, ttOverwrites 3,390,391 on two executions, identical quadruple
(walls 22.57 / 22.46s; identical to the published k05/k20k33 calibration
values).

C4 fail-closed input gates 2/2 GATE_FAIL with process exit status 1
(legal 101, stones 6). No C5 hard stop occurred; no disagreement exists
between the third implementation and the published replica raws.

With this Part, k38 reaches the k13/k19/k20/k33 coverage level (ladder
primary L50M cold pair + delegated pinned C++ second-implementation gate +
this third-implementation verdict-level corroboration) and becomes an
adoption-eligible input. It is the LAST unconsumed loss-resolved row of the
sixth-cost exclusive S5 batch: the next adoption Part against BASE
`dade15780` (6,831 rows WIN201/LOSS6630) now has k38 as the only fresh
loss-resolved candidate on the table. That adoption Part is explicitly NOT
this record; it requires its own fresh declaration and a WIN/LOSS conflict
policy review.

## Waves (fetch-back byte-verified)

- Wave A declaration: commit `f8b456e7` (fetch-back: content identical,
  final trailing newline stripped by the bash transport wrapper, 5,041
  published bytes; disclosed in the kit README, disclosure 1).
- Wave B kit 22 files: commit `db0f5dda`, fetch-back 21/21 kit files
  byte-identical via raw-CDN curl + sha256 against MANIFEST-sha256.txt
  (the 285,726-byte canonical-head byte-clone traveled as five 60KB
  sentinel chunks; all pins inside MANIFEST).
- Wave C: this completion log.

## Audit record

`audit_k38.py` (kit-shipped): 31/31 gates ALL PASS, rc=0, deterministic
byte-identical across two runs (output sha256 b6a403b2...); tamper battery
3/3 fail-closed on full kit copies (T1 k38 verdict flip 2->1 ->
determinism + verdict-level + verify-legal gates rc=1; T2 replica
at50m-run1 nodes edit 21839049->21839048 -> repl_sha + repl_row +
stage-structure gates rc=1; T3 anchor w2 expansions edit 7583990->7583991 ->
C1 anchor gates rc=1); every restore byte-verified; post-tamper clean
control rc=0 byte-identical to the baseline (out/tamper-log.txt). The
auditor additionally machine-verifies: script pins (G1-G3), input pin (G4),
canonical-head byte-clone pin (G6) and k38 freshness vs head (G7),
replica stage structure (G18: at2m/at15m pair UNKNOWN at budget, at50m
pair LOSS(2) 21,839,049), C1 calibration, determinism, verdict-level,
verify-legal equality, anti-copy, fail-closed inputs, and scope.

## Honest disclosures (this executing session)

1. Wave A's published declaration is missing its final trailing newline
   (bash transport artifact); the published byte is authoritative and the
   content is otherwise identical.
2. The first anchor-w2 invocation hand-copied "legal 95" from a summary and
   fail-closed GATE_FAIL'd (derived=80) before any k38 target execution; the
   published calibration raws (legalDerived 80) were fetched and the anchor
   re-run correctly. Lesson reconfirmed: expected values are machine-extracted
   from published raws, never hand-copied from summaries.
3. All five replica raws were consumed at HEAD `1f1577b0` and sha-verified
   against the published probe-kit paths before the wave A push; they are
   re-published inside the kit (out/k38-replica-raws/) so the auditor is
   self-contained. The canonical head byte-clone (dade15780..., 285,726 B)
   ships in input/ for the freshness gate, following the Part SS wave-B2
   self-sufficiency precedent.
4. Sandbox environment: Node.js v22.20.0, Python3; the delegated pinned C++
   gate remains run-and-published by Part SS and is NOT re-run here.
5. A first wave-B push attempt failed locally with zero output for a chunk
   read (a `$1` shell-expansion bug in the chunk command), fail-closed on
   the in-assembly length check; nothing was pushed and the corrected
   assembly pushed byte-exactly. No remote state was affected.

## Status guard

Verification only. No verdict consumed, no cache row published, no class
status flipped, no route to any root certificate laid. The standard 11x11
empty board, the two-stone root {60,27}, its remaining third moves
{100,108}, S2, class 1/2/4, and every closure class remain UNKNOWN
throughout. Nodes and expansions are bookkeeping, never verdicts. An S5
LOSS raw is not a class closure claim, and LOSS rows transfer no root
verdict. The canonical head of record `dade15780...` (6,831 rows WIN201 /
LOSS6630) is untouched by this Part.

## Resume notes (next session, hourly concurrency caution)

- Before any work, re-fetch latest main. BASE for the next adoption Part
  is `dade15780`; k38 is now adoption-eligible (this Part + Part SS), and it
  is the only unconsumed loss-resolved candidate. Any adoption Part needs a
  fresh declaration and a WIN/LOSS conflict policy review of the parent
  batch.
- Kit dir: research/experiments/n11-sixthcost-k38-l50m-thirdimpl-20261126/
  (MANIFEST-sha256.txt pins 21 files).
- 11x11 empty board and every closure class: UNKNOWN, unchanged.
