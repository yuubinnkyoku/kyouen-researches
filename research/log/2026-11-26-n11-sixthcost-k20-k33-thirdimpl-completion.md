# n11 sixth-cost k20/k33 third-impl verdict re-verification: completion log (2026-11-26)

Closes the single-owner fresh declaration
research/log/2026-11-26-n11-sixthcost-k20-k33-thirdimpl-verdict-single-owner-note.md
(wave A push `449ab209`), executing the third-impl Part that the Part SN
completion pre-registered as the natural next step before any adoption Part
weighs the two unconsumed parked4rest2 L50M WIN rows.

## Outcome

Verdict-level agreement on BOTH rows. The third implementation (third_impl.js
sha256 `08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998`)
resolves:

- k20 `10376293541461626880:33619968` (legal 95): **WIN(1)**, expansions
  19,455,330, ttHits 10,071,309, ttOverwrites 15,261,026, identical on all
  three cold runs (a 57.46s, b 57.61s, verify-legal 103.59s, identical
  verdict/expansions/ttHits), vs the published replica raws WIN(1) nodes
  16,196,331 x4 (base15m parked baseline UNKNOWN 15,000,000).
- k33 `12682136550675320832:65536` (legal 91): **WIN(1)**, expansions
  18,829,006, ttHits 10,066,094, ttOverwrites 14,634,702, identical on all
  three cold runs (a 56.47s, b 56.24s, verify-legal 102.23s), vs the
  published replica raws WIN(1) nodes 15,842,649 x4 (base15m parked baseline
  UNKNOWN 15,000,000).

C1 fresh calibration on this new host (honest non-reuse, per the k05
precedent): verify_tbl completion-table battery replica quads 95,670 ==
mine 95,670, 195,044 triples checked, 0 mismatches, rc=0 (identical counts
to the published k05 calibration); anchor w2 `10376293541461626880:131328`
WIN(1) expansions 7,583,990 == the published witness value on two
executions, identical quadruple (walls 22.98 / 23.07s).

C4 fail-closed input gates 4/4 GATE_FAIL with process exit status 1
(k20 legal 96, k20 stones 6, k33 legal 92, k33 stones 6). No C5 hard stop
occurred; no disagreement exists between the third implementation and the
published replica raws on either row.

With this Part, k20/k33 reach the k13/k19 coverage level (ladder 4-run
primary battery + Part SN delegated pinned C++ second-implementation gate
GATE-PASS node-exact + this third-implementation verdict-level
corroboration) and become adoption-eligible inputs for a future adoption
Part against BASE `cc3694bb`. That adoption Part is explicitly NOT this
record; it requires its own fresh declaration, must weigh the coverage
asymmetry (30 SL LOSS rows remain without delegated C++ gate; k38's L50M
follow-up remains unclaimed), and stays with the scrutiny owner.

## Waves (all fetch-back byte-verified via raw-CDN curl + cmp/sha256)

- Wave A declaration: commit `449ab209`, fetch-back byte-identical.
- Wave B kit 27 files: commit `855c2c48`, fetch-back 27/27
  byte-identical (auditor audit_k20k33.py sha256
  `32893172386f002b551b6380b71d44ba0bc18ef8f2ab6bbcaf78228e4de2c172`,
  run raws x6, calibration raws x3, negative-gate raws x4, tamper log,
  per-row replica-raw copies 5+5, row-spec inputs x2).
- Wave C: this completion log + the parent dir README addendum (README pin
  re-pinned in MANIFEST.sha256; 27 new entries appended, 344 -> 371 lines).

## Audit record

`audit_k20k33.py`: 49/49 gates ALL PASS, rc=0, deterministic byte-identical
across two runs; the tamper battery failed closed 3/3 on full kit copies
(T1 k20 verdict flip 1->2 -> determinism + verdict-level + verify-legal
gates rc=1; T2 k33 verdict flip 1->2 -> same gates rc=1; T3 base15m-k33
replica-raw nodes edit 15,000,000 -> 14,999,999 -> repl_sha + repl_row +
stage-unanimity gates rc=1); every restore byte-verified; the final clean
control rc=0 byte-identical to the baseline audit output
(`out/audit-tamper-controls-k20k33.txt`, control-output shas pinned
inside).

## Honest disclosures (this executing session)

1. The auditor went through three pre-publication parse-bug iterations on
   the local kit (replica CSV column offsets in parse_repl, and a
   GATE_FAIL short-row parse crash); all were caught by the auditor's own
   crash / fail-closed behavior before any publication, and only the final
   byte is published. No published byte of any earlier wave was affected.
2. All ten replica raws were consumed at HEAD `a0166a12` (the head at the
   wave A push) and were sha-verified against the parked4rest2 ladder kit
   MANIFEST BEFORE the declaration was pushed; they were re-published inside
   the third-impl dir so the auditor is self-contained.
3. The verify_tbl.js byte-clone expects the replica at a fixed host path
   (the historical lane-kit path); the byte-clone of jsreplay.js
   (`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`)
   was placed there verbatim and sha-verified before the C1 run. Only
   verify_tbl.js consumes it.
4. Sandbox environment: Node.js v22.20.0, Python3, no C++ toolchain; the
   delegated pinned C++ gate remains run-and-published by Part SN and is
   NOT re-run here (its raws are unchanged).

## Status guard

Verification only. No verdict consumed, no cache row published, no class
status flipped, no route to any root certificate laid. The standard 11x11
empty board, the two-stone root {60,27}, its remaining third moves
{100,108}, S2, class 1/2/4, and every closure class remain UNKNOWN
throughout. Nodes and expansions are bookkeeping, never verdicts. S5 WIN
raws are not class closure claims. The canonical head of record
`cc3694bb` (6,799 rows, WIN199/LOSS6600) is untouched by this Part.
