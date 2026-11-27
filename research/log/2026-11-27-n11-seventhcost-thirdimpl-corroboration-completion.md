# n11 Part SY completion log: seventh-cost full-batch third-impl corroboration (wave F)

Part SY closes complete. Waves A (declaration, HEAD pin 08013dec ->
published 47ae14ea) -> B kit ef598429 (53 files) -> C results 6148e568
(94 files: 84 target raws + 3 calibration raws + 4 audit runs + tamper
log + audit rev2 + tamper battery script) -> D c81f980b (run record +
MANIFEST-sha256.txt 143 files pinned). Fetch-back verification complete
at wave F time: all 143 MANIFEST files byte-identical via the raw CDN
(sha256 per file), plus the wave B/C/D push_files returns each carried
the new head sha.

Result: **42/42 verdict-level agreements.** The pinned third
implementation third_impl.js (08ea958f, the program's standing third
implementation, fresh host) corroborates every published seventh-cost
row: 41 LOSS rows (third-impl result 2, all of them) and the WIN row
k05 (third-impl **WIN(1)** expansions 18,822,048 x2 cold-identical) -
the third pillar of the k20/k33 WIN precedent is now in place for k05
as well. Every target ran two fresh-cold passes under the pinned
invocation (cap=400000000, wallcap=260, memo-power=22); every cold pair
byte-identical in (result, expansions, ttHits, ttOverwrites). Two-pass
expansion bill 529,416,996 (bookkeeping).

Calibration: C1a verify_tbl rc=0 (quads 95,670/95,670, triples 195,044
mismatches 0); C1b calib-k06 expansions 9,474,431 and calib-k38
expansions 25,898,941, both EXACT vs published values, re-executed after
the environment reset. Audit: rev2 (722175e7, rev1's two fail-closed
self-catches disclosed in the run record) 4 runs byte-identical sha256
5ce0151f, AUDIT-PASS G0-G6. Tamper battery 3/3 fail-closed (T1 expected
pin flip -> G3 / T2 raw expansion edit -> G4 / T3 phantom raw -> G5) +
clean control rc=0, scratch copy only.

Honest disclosures:
1. One environment reset mid-Part (artifact save failure after k23.p1
   of the first round): all pre-reset partial raws were lost and NOT
   trusted; the whole batch and calibration were re-run from scratch on
   the rebuilt host (kit bytes re-fetched from published main,
   pin-verified). The pre-reset round had agreed on every row it
   completed (observation only, not evidence).
2. The wave B published calibration raws lacked the trailing rc=0 line
   (formatting defect); wave C superseded them with rc-line-carrying
   raws, values identical.
3. The third implementation is the standing third_impl.js (not a fresh
   implementation), same pins as the sixth-cost corroboration program.
4. Verdict-level agreement is bookkeeping toward adoption eligibility
   only: NO verdict is consumed, no cache increment, no class-status
   change. The seventh-cost batch's adoption stays with a separately
   declared adoption Part under the parent batch's WIN/LOSS conflict
   policy against the canonical head of record 42dbb58f (6,832 rows WIN
   201 / LOSS 6,631), untouched by this Part.

Status guard: the standard 11x11 empty board is UNKNOWN. All 19
central-reply roots are UNKNOWN. The two-stone root {60,27} is UNKNOWN.
Its remaining third moves {100,108} are UNKNOWN. S2 and closure classes
1/2/4 and all closure classes are UNKNOWN. Expansions and nodes are
bookkeeping, never verdicts.
