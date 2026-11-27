# Part SW: seventh-cost 41 LOSS rows C++ scrutiny gate (2026-11-27)

Tenth execution of the C++ second-implementation scrutiny gate lineage
(after EN class-30484, EO class-34908, EQ class-30345 b38-win-18, ET
class-30345 ES-re-probe-6, EV closure-batch WIN-4, SK sixth-cost exclusive
k01..k08, SM parked4 k13/k19, SN parked4rest2 k20/k33, SR fifthres30): the
delegated pinned C++ gate of the FORTY-ONE resolved-LOSS rows of the
seventh-cost exclusive S5 probe batch (k01..k42 minus k05). Scope,
protocol, pins and stop rules are pre-registered in the wave A
declaration (research/log/2026-11-27-n11-seventhcost-41loss-cppgate-declaration.md,
commit dfb6b357).

- Targets: 41 rows (39 stage-15m at budget 15000000, k16/k17 stage-2m at
  budget 2000000), expected quadruples machine-derived from the published
  probe raws (SSOT) and cross-checked against the published selection JSON
  (c395fe03) and batch-summary ledger (6881eaaf); per-pass target node bill
  211,789,419 + anchors 26,390,307 (bookkeeping).
- Anchors: anchor-at2m / anchor-aj001 / anchor-af039 (byte-clones of the
  published SR kit inputs; quadruples == the SR kit anchors block).
- Freshness: all 41 target [lo,hi] pairs ABSENT from the canonical head of
  record 42dbb58f (6,832 s5verdict rows WIN 201 / LOSS 6,631,
  sha-verified) - verdict-unconsumed at declaration, run and publication
  time.
- k05 (parked-then-L50M WIN row) is NOT a row of this kit; its C++ gate
  and third-impl corroboration stay separate future Parts.
- Third-implementation corroboration: ABSENT for every target row
  (seventh-cost batch is single-implementation Node replica + this gate;
  SN disclosed-absence pattern; a third-impl Part is required before any
  adoption).

This Part consumes NO verdict. The 41 rows stay gate-verified UNCONSUMED
labels; adoption stays with a separately declared adoption Part under the
parent batch's WIN/LOSS conflict policy. The standard 11x11 empty board,
every central-reply root, the two-stone root {60,27}, its remaining third
moves {100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN.
Nodes are bookkeeping, never verdicts. S5 LOSS raws are not class closure
claims and not routes to the root certificate.

Kit layout: scripts/ (maker, runner, audit), input/ (44 input.csv +
gate-rows.json), output/ (gate-status.log, raw p1/p2 per row,
audit_gate.json x4). MANIFEST-sha256.txt published with the run record
(wave D).
