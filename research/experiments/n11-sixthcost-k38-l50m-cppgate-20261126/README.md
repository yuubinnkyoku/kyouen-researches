# Part SS: k38 L50M follow-up LOSS row C++ scrutiny gate (2026-11-26)

Tenth execution of the C++ second-implementation scrutiny gate lineage
(after EN class-30484, EO class-34908, EQ class-30345 b38-win-18, ET
class-30345 ES-re-probe-6, EV closure-batch WIN-4, SK sixth-cost exclusive
k01..k08, SM parked4 k13/k19, SN parked4rest2 k20/k33, SR fifth-resumption
30 LOSS rows): the delegated pinned C++ gate of the single row k38
`10376293541461626880:66048` (legal 100), which the L50M follow-up
completion (commit `2bc21cf3`, this lane session) resolved as LOSS(2) at
21,839,049 nodes with a first-implementation (jsreplay pin 8458561...) cold
pair. All 4 rows (3 calibration anchors + the k38 target) GATE-PASSED: two
fresh-cold passes per row, node-exact, zero MISMATCH / GATE-FAIL /
GATE-CRASH / TRUNCATED.

k38 target quadruple `100,50000000,2,21839049` confirmed by the second
implementation against the published first-implementation raws
(at50m-run1/run2-k38.out.csv, shas in input/gate-rows.json). Anchors:
at2m (98,2000000,0,2000000), aj001 (84,30000000,2,5156075), af039
(89,30000000,2,19234232) - the same anchor set and expectations as
SK/SM/SN/SR (byte-cloned SR kit inputs).

This Part consumes NO verdict. k38 stays a gate-verified UNCONSUMED batch
row. Honest coverage note: unlike the 30 SR rows, k38 has NO
third-implementation corroboration yet (that vacancy stays open). Adoption
of LOSS rows remains a separately declared future Part under the parent
batch's WIN/LOSS conflict policy. The standard 11x11 empty board, every
central-reply root, the two-stone root {60,27}, its remaining third moves
{100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN. Nodes are
bookkeeping, never verdicts.

## Machine

* Gate source: `cpp/solvers/kyouen_dfpn_root.cpp` at commit
  `154f3b7a67b97e13acbaee8b04dc74ddca728d19`, sha256 9193f5b6...; headers
  kyouen_residual_micro.hpp 5976935d... / n11_s5_quarantine.hpp 2e36d694...
  at the same commit, all byte-verified this session. Built with zig 0.13.0
  `zig c++ -std=c++20 -O2` (tarball sha256
  d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad116b66c9468211230ea,
  byte-verified); binary sha256 fa724df3..., not pinned: source pins are
  authoritative (SK/SM/SN/SR protocol).
* Runner: `scripts/gate_runner.sh` sha256 d88e7f57... - machine-identical
  logic to the EN/EO/EQ/ET/SK/SM/SN/SR runner rev2 (SR bytes 59cbbefe...;
  diff = this comment block only). HARD-STOP on any mismatch; truncated
  artifacts re-run, never trusted (none occurred).
* Audit: `scripts/audit_gate.py` sha256 1f27629c... - a FRESH single-row
  implementation of the gate checks, disclosed as NOT a byte-transform of
  the SR audit script: G0 schema pins, G1 input byte pins (k38 input
  b6ef9f43... = published probe kit input clone; anchors = published SR
  kit input pins), G2 raw completeness, G3 per-row p1==p2==expected, G4
  phantom-raw and status-log consistency, G5 target freshness (k38 [lo,hi]
  pair absent from the canonical head of record 02db5ab3...,
  input/canonical-head.cache byte-clone, 6,801 rows Part SQ merged cache).
  7/7 gates PASS, rc=0 x4 runs byte-identical sha256 ca6d6eb0...
  (audit_gate.json == run1 == run3 published).
* Tamper battery (output/tamper.log): T1 gate-rows expectation flip ->
  rc=1; T2 raw k38.p1 node edit -> rc=1; T3 phantom raw -> rc=1; every
  restore byte-verified (gate-rows 0ec33dbf..., raw 11eba4b3...); clean
  control rc=0 with audit output ca6d6eb0... unchanged.

## Run record (2026-11-26, publish-then-execute per declaration, wave A commit 5447c7b4)

Waves A (declaration `5447c7b4`) and B (kit `9d2465b9` + canonical-head
byte-clone `71bcde8c`) published first; fetch-back 8/8 byte-identical.
Official execution 19:59:59Z-20:03:23Z sequential (anchors at2m / aj001 /
af039 then the k38 target - pre-registered order): 4/4 GATE-PASS,
node-exact against the published expectations (output/gate-status.log).
Results wave C `6d130982` (13 files), fetch-back 13/13 byte-identical.
Audit 4 runs and the 3-mode tamper battery completed after the official
passes. Counter-probe re-checked at each wave push (heads 2bc21cf3 /
5447c7b4 / 71bcde8c / 6d130982; no concurrent lane in this territory).

Honest environment disclosure (also in the declaration): this session ran
on an upgraded sandbox with a native C++ toolchain. One anchor-at2m
calibration run (PASS, 98,2000000,0,2000000, wall 3 s) was executed at
binary-build time BEFORE the declaration push as an environment sanity
check (SR precedent); NO target row ran before publication.

## Status guard

Scheduling and verification only. No verdict is consumed. The canonical
chain head of record (02db5ab3 after Part SQ) is untouched by this Part.
If a future adoption Part adopts this row, the flip set and class movement
are decided by the canonical chain merge under the parent batch's WIN/LOSS
conflict policy, not by this kit. The two-stone root {60,27}, its
remaining third moves {100,108}, and the 11x11 empty board remain UNKNOWN
throughout. S5 LOSS raws are not class closure claims and not routes to
the root certificate.

## MANIFEST

See `MANIFEST-sha256.txt` (21 files: 6 input, 2 scripts, 13 output).
