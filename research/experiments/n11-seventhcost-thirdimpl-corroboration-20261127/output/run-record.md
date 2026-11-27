# n11 Part SY run record: seventh-cost full-batch third-impl corroboration (waves C-D)

Result: **42/42 verdict-level agreements.** The pinned third
implementation third_impl.js (08ea958f) corroborates every published
seventh-cost row: the 41 LOSS rows (k01..k42 minus k05, all third-impl
result 2) and the WIN row k05 (1152921504607932416:536870912, third-impl
**WIN(1)** expansions 18,822,048, cold pair identical). Each of the 42
targets ran two fresh-cold passes (one node process per pass, serial,
pinned invocation cap=400000000 wallcap=260 memo-power=22); every cold
pair is byte-identical in (result, expansions, ttHits, ttOverwrites).
Total two-pass expansion bill 529,416,996 (bookkeeping, never verdicts).
Official execution post-wave-B, on the post-reset host (see disclosure 1).

Calibration (post-declaration, this host, Node v22.20.0, re-executed
after the environment reset): C1a verify_tbl rc=0, quads 95,670/95,670,
triples 195,044 mismatches 0; C1b calib-k06 LOSS(2) expansions 9,474,431
EXACT vs the published sixth-cost k06-cold-a raw; C1b calib-k38 LOSS(2)
expansions 25,898,941 EXACT vs the Part SU publication. The wave B
published calibration raws lacked the trailing rc=0 line (formatting
defect); the wave C published calibration raws carry it and supersede
them (values identical, disclosed).

Audit: scripts/audit_sy.py rev2 (sha256 722175e7...; rev1 failed closed
on its own G1/G1-parse expectations - the c1a/c1b raws' rc line and the
calib row label - before any raw was accepted, and was fixed with the
one-line label correction and the rc-line-carrying calibration raws;
fail-closed behavior held). 4 runs rc=0 byte-identical, sha256
5ce0151f... AUDIT-PASS: targets=42 (41 LOSS + 1 WIN), raws=84, pairs=42,
all G0-G6 gates.

Tamper battery (published scripts/tamper_battery.sh, scratch copy only,
deleted after): T1 k05 expected_result pin flip -> G3 FAIL; T2 k10.p2
expansion edit -> G4 cold-pair FAIL; T3 phantom k99 raw -> G5 count
FAIL; clean control rc=0.

Honest disclosures:
1. Environment reset once mid-Part (Koyeb artifact save failure after
   k23.p1 of the first execution round): the pre-reset partial target
   raws (k01..k22 complete pairs + k23.p1) were LOST and were NOT
   trusted; the entire batch (all 84 passes) and the calibration were
   re-run from scratch on the rebuilt host (kit bytes re-fetched from
   published main and pin-verified). The pre-reset round's observed
   values agreed with the official round on every row it completed
   (disclosed as an observation only, not evidence).
2. The third implementation is the program's standing third_impl.js
   (same implementation as the sixth-cost corroboration program), run on
   a fresh host; not a fresh implementation.
3. Expansion counts are compared only across third-impl cold pairs,
   never against replica node counts or C++ gate node counts.
4. Verdict-level agreement is bookkeeping toward adoption eligibility
   only. NO verdict is consumed, no cache increment, no class-status
   change. Adoption stays with a separately declared adoption Part
   under the parent batch's WIN/LOSS conflict policy against the
   canonical head of record 42dbb58f (6,832 rows WIN 201 / LOSS 6,631),
   which this Part does not touch.

Status guard: the standard 11x11 empty board is UNKNOWN. All 19
central-reply roots are UNKNOWN. The two-stone root {60,27} is UNKNOWN.
Its remaining third moves {100,108} are UNKNOWN. S2 and closure classes
1/2/4 and all closure classes are UNKNOWN. Expansions and nodes are
bookkeeping, never verdicts.
