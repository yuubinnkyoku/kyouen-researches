# Part ET completion log: ES-re-probe-6 C++ scrutiny gate (closure class 30345, 2026-11-25)

Part ET closed.  Four published waves, all landed on main:

* A 78ad43f4  declaration log
  (research/log/2026-11-25-part-et-es6-cppgate-declaration.md)
* B c17a7663  kit 14 files (declaration mirror, 9 input CSVs = 6 ES
  targets byte-cloned from the ES kit + 3 EQ anchors byte-cloned from
  the EQ kit, gate-rows-et.json SSOT registry, disclosed-fork runner +
  regenerated audit + fail-closed maker)
* C 76697c6c  outputs 24 files (18 raws, gate-status.log 9 GATE-PASS
  lines, audit_gate.json + run1..3, tamper.log)
* D this wave  close-out (README.md run record, MANIFEST-sha256.txt 38
  entries, this completion log)

## Result

ALL 9 rows GATE-PASS, two fresh-cold passes per row, node-exact against
the published raws, zero MISMATCH / GATE-FAIL / GATE-CRASH / TRUNCATED:

* WIN (unconsumed, adoption-ready for a separately declared adoption
  Part): ai007 84/30,000,000/1/16,090,493 and ai040 85/30,000,000/1/
  20,711,023 - the two Part ES 30M WIN rows of closure class 30345.
* LOSS (unconsumed, EM-pattern loss-adoption territory): ai024
  86/30M/2/19,127,057, ai030 91/30M/2/16,504,156, ai038
  89/30M/2/19,851,840, ai041 91/30M/2/15,781,960.
* Anchors: at2m 98/2M/0/2,000,000, aj001 84/30M/2/5,156,075, af039
  89/30M/2/19,234,232 - EQ/EO/EN lineage quadruples reproduced
  node-exact by this lane's independently built binary (zig 0.13.0,
  binary 0a0199fe..., source pins authoritative per EN/EO/EQ policy).

Chain significance: with Part ET, every Part ES verdict now has a
C++ second-implementation, third-host, two-pass node-exact
reproduction.  The 2 WIN rows are the first batch-30345 rows verified
at the 30M condition and are adoptable; class 30345's unknown census
after the ES re-probe (50 unknown - 2 members resolved at 30M, subject
to adoption) can move in a future adoption Part.  THIS Part consumes
nothing.

## Machine record

* Maker: G0-G8 ALL PASS at fetch-frozen head 3683bf7d.  ES kit MANIFEST
  38/38 byte verify; EQ kit subset 13/13; ES status.log == targets-30m
  SSOT quadruples with WIN-line consistency (2 WIN = ai007/ai040);
  per-target p1==p2 discipline; (lo,hi) freshness vs ER canonical head
  9c4dd94e (6,765 rows WIN186/LOSS6579, ER increment 4f6b7797 verified
  to survive into the head); anchor quadruples regenerated from the
  published EQ raws.
* Runner: EQ rev2 byte-clone with exactly the 3 naming-comment lines
  differing (disclosed diff verified by byte-diff before the run).
* Official execution: 22:20:33Z-22:30:05Z, sequential per-key calls
  (anchors calibrated first), 9/9.
* Audit: 4 runs, all rc0, byte-identical sha256
  2c6d7441d6f752f160efbe7e275b807ff174d8cd70ece3c85aed135ead11c0d0
  (audit_gate.json = run1 = run2 = run3).
* Tamper battery 3/3 fail-closed (pre-asserted byte changes, restore
  byte-verified, clean control rc0 output identical):
  T1 audit-pin break -> FAIL G3:ai007; T2 raw nodes byte-alter ->
  FAIL G2:ai024 + G3:ai024; T3 phantom GATE-PASS -> FAIL G4
  passes=10/9.

## Honest record

1. Declaration erratum: the single-pass node bill in the wave-A
   declaration prose (134,449,387) is a mis-sum; the machine SSOT
   single-pass total is 134,456,836 (summed from the per-row raws).
   Per-row pins - what the audit enforces - are unaffected.  The
   EQ-declaration mis-sum precedent is kept (prose sums are
   bookkeeping, per-row SSOT authoritative).
2. One pre-declaration anchor-at2m smoke pass ran in a scratch
   directory for build sanity and was discarded; every published raw
   is a fresh official pass (declared in wave A).
3. The binary (0a0199fe...) is host-dependent and not pinned; the
   gate-source pins (9193f5b6 @ 154f3b7a + both headers) are the
   authority, per the EN/EO/EQ disclosure chain.
4. Orthogonality: waves were pushed on top of strip-lane commits
   (fb215b76, daa9a805); no competing ET/ES-row claim appeared between
   the pre-push refetches.

## Standard guarantees

The standard 11x11 empty board stays UNKNOWN.  All 19 central-reply
roots, S2, class 1/2/4, and closure class 30345 stay UNKNOWN.  No
verdict is consumed by this Part; the 2 WIN + 4 LOSS rows stay
unconsumed labels.  nodes are bookkeeping, never verdicts.  No
free/secured coverage or root resolution claim is made anywhere.
