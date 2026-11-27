# Part SM completion: parked4 L50M WIN rows k13/k19 delegated pinned C++ scrutiny gate COMPLETE

Date: 2026-11-26 (long-term lane session)
Part SM closes complete. The two delegated sixth-cost parked-4-keys S5 L50M
ladder WIN rows now carry pin-verified second-implementation coverage:

- k13 1152921573327376384:536870912: GATE-PASS 95,50000000,1,16402480
  (2 fresh-cold passes, node-exact vs the published ladder raws)
- k19 10376293541461626880:65664: GATE-PASS 95,50000000,1,15379062
  (2 fresh-cold passes, node-exact)

## Wave chain (every wave fetch-back byte-verified)

- wave A declaration d21e506d:
  research/log/2026-11-26-part-sm-parked4-k13k19-cppgate-declaration.md
  (pre-registered protocol, expected quadruples, all 10 kit byte pins,
  counter-probe record, environment disclosure). Fetch-back byte-identical.
- wave B kit 332ce273: 10 files under
  research/experiments/n11-sixthcost-parked4-l50m-cppgate-20261126/
  (inputs byte-cloned from the ladder kit and the SK kit; gate-rows.json;
  maker 69 gates ALL PASS; audit and runner and tamper battery as machine
  transforms of the published SK kit scripts). Fetch-back 10/10
  byte-identical.
- Official execution 11:45:34Z-11:50:30Z (after waves A/B, per the
  publish-then-execute protocol): anchors at2m/aj001/af039 calibrated
  first, then k13, k19 (pre-registered order). All 5 rows GATE-PASS,
  zero MISMATCH / GATE-FAIL / GATE-CRASH / truncation. Per-pass node bill
  58,171,849 (targets 31,781,542 + anchors 26,390,307), two-pass bill
  116,343,698. Gate binary built from the pinned source
  9193f5b6...@154f3b7a with zig 0.13.0 (binary d376b9e7..., not pinned).
- wave C results e9be85ff: 17 files (10 raws, gate-status.log, 4
  byte-identical audit JSONs sha256 a11983dd..., tamper.log,
  t1_result.json). Fetch-back 17/17 byte-identical. Audit 26/26 gates
  PASS, 5 runs rc=0 byte-identical (run4 = clean-control regeneration
  after the battery, recorded in tamper.log). Tamper battery 3/3
  fail-closed: T1 audit-pin flip -> G3:k13 FAIL rc=1; T2 raw flip ->
  G2+G3:k13 FAIL rc=1; T3 phantom GATE-PASS line -> G4 FAIL 6/5 rc=1;
  all restores byte-verified; clean control rc=0.
- wave D 9fd08e79: kit README + MANIFEST-sha256 (28 entries incl. the
  README; every published kit byte pinned). Fetch-back byte-identical.

## Determined facts (all bookkeeping / scheduling, no outcome claims)

- The pinned C++ second implementation reproduces both ladder WIN rows
  node-exactly at budget 50M (16,402,480 / 15,379,062 expansions).
- Combined with Part SL's published third-implementation verdict-level
  batch (32/32; k13/k19 WIN x3 cold runs each), both rows are now
  adoption-eligible: primary 4-run ladder evidence + second (this gate) +
  third (Part SL) implementations all agree on WIN(1).
- The canonical chain head of record stays 16a12390 (6,797 rows,
  WIN197/LOSS6600): this Part consumed no verdict, published no cache
  row, flipped no class status. The halt-audit's if-adopted scenario (2
  hypothetical UNKNOWN->WIN keys: owner class 10376293541461626880:65536
  child 10376293541461626880:65664 and non-candidate
  1297600742147751936:0) remains recorded and NOT adopted; any adoption
  is a separately declared future adoption Part against a fresh BASE
  (16a12390) using the halt-audit's pinned expectations with this gate as
  the second-implementation leg.
- Honest disclosures: (a) the gate source pins are the 154f3b7a commit
  bytes (the solver has since moved on main to a0786acb - disclosed in
  the declaration and kit README; the pin is the authority); (b) the
  local kit output audit_gate.run4.json (5th run, byte-identical to the
  published audit JSONs) was left unpublished to keep the SK convention of
  4 published audit JSONs, with the 5th run recorded in tamper.log as the
  clean-control regeneration; (c) build-time runs of the maker happened
  pre-publication on the local SSOT mirror (halt-audit, ladder kit raws,
  SK kit bytes all fetched from pinned commits and sha-verified inside
  the maker), published kit bytes fetch-back verified; (d) two "No such
  file or directory" anomalies appeared on the final `cat` of
  shell-launch commands during the run (fuse transient); both files
  existed and verified byte-exact on immediate re-read; no raw or audit
  byte was affected (recorded as an environment fact).

## Resume notes (next sessions re-read latest main first; hourly parallel)

- Highest-value next step on this lane: a sixthwin2 adoption Part for
  k13/k19 (pattern: Part EW; fresh declaration required; BASE 16a12390;
  dossier increment/maker patterns exist in the EW kit; the halt-audit's
  NOT-ADOPTED scenario is the expected flip set, to be recomputed by the
  adoption Part itself).
- k20/k33 remain parked@15M with the L50M raise declaration vacant
  (precedent: the k13/k19 L50M ladder kit; jsreplay replica + stopping
  rules must be re-declared session-scoped).
- The remaining delegated pinned C++ gates without a second
  implementation: fifth-resumption 30 LOSS rows (k09..k43 minus
  resolved; expectations recorded in the Part SL batch ledger) - a
  future cppgate Part can acquire them with a fresh pin.
- The standard 11x11 empty board, the two-stone root {60,27}, its
  remaining third moves {100,108}, S2, class 1/2/4, and all closure
  classes remain UNKNOWN throughout this Part. No verdict was consumed
  anywhere in this Part.
