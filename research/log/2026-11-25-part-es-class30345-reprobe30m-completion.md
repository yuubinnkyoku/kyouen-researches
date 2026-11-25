# Part ES completion log: class 30345 exhausted-6 re-probe at the 30M condition (2026-11-25)

Close-out of Part ES.  Every drive phase was executed after the kit
publication, in this single session, and is recorded in the kit README;
this log records the results and the publication waves.

## Result (all six targets resolved; honest labels; NOTHING consumed)

The 6 batch-38 honest-EXHAUSTED keys of closure class 30345 were re-probed
at the DIFFERENT 30M condition with the pinned jsreplay engine
(byte-clone 84585617) via the disclosed runbatch30m.sh fork
(f591f8c2 -> 44674932: budget 30M + WIN-CONTINUE).  All six RESOLVED:

* ai007 WIN 16,090,493 nodes and ai040 WIN 20,711,023 nodes -
  UNCONSUMED probe-level WINs; canonical adoption is the scrutiny-owner
  C++ second-implementation gate's exclusive right (not exercised here);
* ai024 LOSS 19,127,057, ai030 LOSS 16,504,156, ai038 LOSS 19,851,840,
  ai041 LOSS 15,781,960 - unconsumed, Part-EM loss-only adoption
  territory;
* all six resolutions sit strictly inside the (15M, 30M] window
  (15,781,960 .. 20,711,023): the 15M EXHAUSTED dispositions were budget
  artifacts; the different-condition route retired these unknowns
  without a single new exhaustion;
* every key is two-pass fresh-cold node-exact; zero MISMATCH, zero
  truncation events, zero runner failures; val-gate 8/8 against the
  published batch-38 baselines ran BEFORE any target and passed.

The same-condition re-probe ban is untouched (no completed exhaustion
row re-probed at its own condition).  b018 (the 7th class-30345
unknown) stays excluded and untouched.  The canonical chain head
9c4dd94e... (Part ER head) and all class scheduling are untouched: no
merge, no refresh, no adoption in this Part.  The standard 11x11 empty
board stays UNKNOWN; all 19 central-reply roots stay UNKNOWN; nodes are
bookkeeping, never verdicts; no coverage or secured-coverage claim is
made anywhere.

## Publication waves (all landed on main)

* A de2e8bf3  declaration log (publish-then-execute, pre-registered
  targets/condition/stop rules/val-gate)
* B e84ab297  kit 17 files: jsreplay.js byte-clone, runbatch30m.sh
  (disclosed fork), 6 target CSV byte-clones, targets-30m.json
  (SSOT-extracted, 1c27a238), 8 val-gate molecule byte-clones
* C 9d0e9459  outputs 21 files: 12 two-pass raws + 8 val-gate run raws
  + status.log (8 lines)
* D 2f22aa3b  close-out: README.md + MANIFEST-sha256.txt (38 entries)
* E this completion log

Each wave was preceded by a fresh main head fetch; the concurrent conic
lane (K1339..K1343 and the W_24 Grundy proven-size work) is fully
orthogonal (no Part ES path touched).

## Drive record (2026-11-25, this session)

Val-gate first (8/8 PASS, ~2 min); then the 6-key drive 21:47:46Z -
22:09:01Z (about 21 minutes including compare steps; foreground split
calls; ai007's two passes in one 2-worker call, the remaining keys one
pass per call, per the measured ~190-210K nodes/s and the 300 s tool
cap; the pinned per-key runbatch30m.sh invocation re-verified completion
and performed every MISMATCH comparison itself).  Per-pass node sum
108,066,529; two-pass total 216,133,058 expansions.

## Resume

* The 2 WIN rows await the scrutiny C++ second-implementation gate
  (ai007/ai040; the EN/EO/EQ-pattern zig build route is documented in
  the Part EN/EO kits); after GATE-PASS, an EP/ER-pattern adoption Part
  could consume them, and class 30345 would then hold only b018 as an
  unknown member.
* The 4 LOSS rows sit in Part-EM loss-only adoption territory.
* b018 remains scrutiny-owner-pending.
* Nothing here changes the canonical head; every future adoption /
  refresh / extractor must re-baseline at 9c4dd94e... (third-host
  reproducible, verified this same day at pinned commit bc70b536).
