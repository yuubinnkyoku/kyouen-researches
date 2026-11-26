# Part SR: fifth-resumption 30 LOSS rows C++ scrutiny gate (2026-11-26)

Ninth execution of the C++ second-implementation scrutiny gate lineage (after
EN class-30484, EO class-34908, EQ class-30345 b38-win-18, ET class-30345
ES-re-probe-6, EV closure-batch WIN-4, SK sixth-cost exclusive k01..k08, SM
parked4 k13/k19, SN parked4rest2 k20/k33): the delegated pinned C++ gate of
the THIRTY fifth-resumption resolved-LOSS rows of the sixth-cost exclusive
S5 probe k09..k43 (parked k20/k33/k38 excluded, no new verdict for them) -
the coverage asymmetry the Part SQ completion log records as standing
unconsumed with "no delegated C++ gate". All 33 rows (3 calibration anchors
+ 30 targets) GATE-PASSED: two fresh-cold passes per row, node-exact against
the published fifth-resumption probe raws, zero MISMATCH / GATE-FAIL /
GATE-CRASH / TRUNCATED.

Coverage note (inverse of the SN disclosure): every one of the 30 rows
already HAS third-implementation verdict-level LOSS(2) corroboration (the
Part SL batch, audit-k09k43-summary all_pass, 32 rows, verdict-level
agreement on every row). With this gate the rows are second-implementation
gate-verified on top of the ladder primary cold pairs AND the third-impl
scrutiny - the k13/k19 coverage level (SM+SP precedent) minus adoption.

This Part consumes NO verdict. The 30 rows stay gate-verified UNCONSUMED
labels; none is adoption-eligible through this kit alone. Any adoption of
LOSS rows stays with a separately declared adoption Part under the parent
batch's WIN/LOSS conflict policy. k38 stays parked@15M with NO L50M
follow-up claimed by this Part. The standard 11x11 empty board, every
central-reply root, the two-stone root {60,27}, its remaining third moves
{100,108}, S2, class 1/2/4 and all closure classes stay UNKNOWN. Nodes are
bookkeeping, never verdicts.

## Rows (machine-derived by scripts/make_kit_fifthres30_cppgate_20261126.py, 231 maker gates ALL PASS)

| key | expected legal,budget,result,nodes | published label | status |
|---|---|---|---|
| anchor-at2m | 98,2000000,0,2000000 | anchor (budget-ceiling) | GATE-PASS |
| anchor-aj001 | 84,30000000,2,5156075 | anchor | GATE-PASS |
| anchor-af039 | 89,30000000,2,19234232 | anchor | GATE-PASS |
| k09..k43 (30 rows) | see input/gate-rows.json targets[] | fifth-resumption resolved-LOSS (15M/2M stage cold pairs; Part SL third-impl LOSS(2)) | GATE-PASS x30 |

Per-pass node total 208,140,422 (targets 181,750,115 + anchors 26,390,307;
equal per-pass anchor condition as SK/SM/SN) / two-pass bill 416,280,844
(bookkeeping, summed from the per-row raws, the SSOT). Gate run walls:
anchors 4/4 s + 22/22 s + 78/78 s; targets 4-62 s per row pass (output/
gate-status.log timestamps 16:57:41Z-17:13:05Z; environment bookkeeping,
never compared).

## Machine

* Gate source: cpp/solvers/kyouen_dfpn_root.cpp at commit
  154f3b7a67b97e13acbaee8b04dc74ddca728d19, sha256 9193f5b6... (the
  delegated pin, machine-read from the published SN kit gate-rows.json);
  headers kyouen_residual_micro.hpp 5976935d... / n11_s5_quarantine.hpp
  2e36d694... at the same commit, all three fetched from the pinned
  commit and byte-verified this session. Built with zig 0.13.0
  `zig c++ -std=c++20 -O2` (tarball zig-linux-x86_64-0.13.0.tar.xz sha256
  d45312e6... verified this session); binary sha256 3b42e226..., not
  pinned: source pins are authoritative (SK/SM/SN protocol).
* Runner: published SN kit runner byte-transform (diff = exactly the 2
  comment lines naming Part SR; asserted inside the maker G3) sha256
  59cbbefe...; HARD-STOP on any mismatch; truncated artifacts re-run,
  never trusted (none occurred).
* Audit: scripts/audit_gate.py (machine transform of the published SN kit
  audit script; diff: docstring + machine-generated ROWS/RAW_PROV +
  part/schema strings only, logic byte-identical, asserted by the maker
  G3) sha256 e8a139a7...; 4 runs rc=0 byte-identical sha256 44358ce2...
  (audit_gate.json == run1 == run2 == run3 published).
* Maker: scripts/make_kit_fifthres30_cppgate_20261126.py sha256
  1aef3633... - fail-closed G0/G1/G2/G3, ALL 231 gates PASS at kit build
  time (wave B); every per-row pin machine-derived (EP pin policy): the
  30 target expectations from the published probe-lane raws sha-verified
  against the published audit_k09k43.py ROWS/INPINS literals, the
  anchors from the published SN kit gate-rows.json.
* Tamper battery: SN kit battery transform (k09 quadruple): T1 audit
  ROWS pin flip -> G3:k09 FAIL rc=1; T2 raw k09.p1 flip -> G2+G3:k09
  FAIL rc=1; T3 phantom GATE-PASS line -> G4 FAIL 34/33 rc=1; every
  restore byte-verified; clean control rc=0 (tamper.log, t1_result.json).
* Freshness (maker G2): all 30 target [lo,hi] pairs ABSENT from the
  canonical head of record 02db5ab3 (Part SQ, 6,801 s5verdict rows WIN
  201 / LOSS 6,600, sha-verified) - verdict-unconsumed at declaration,
  run and publication time.

## Run record (2026-11-26, publish-then-execute per declaration, wave A commit 947cf9e6)

Waves A/B published first (declaration 947cf9e6; kit 9d543bdd with maker
231/231; fetch-back 38/38 byte-identical). Official execution
16:57:41Z-17:13:05Z sequential (anchors at2m/aj001/af039 calibrated
first, then the 30 targets ascending - pre-registered order), all 33
rows GATE-PASS with (legal,budget,result,nodes) exactly the published
values (output/gate-status.log). Results wave C 5d417167 (73 files) with
a disclosed publication repair: the wave C push wrote the 66 raws under
truncated names (<key>.p1/.p2 instead of .p1.out/.p2.out - a path-suffix
bug in the push payload builder, caught immediately by the raw-CDN
fetch-back 404s). Repair commits f07b6034 (66 correctly named raws,
byte-identical content) + 66 single-file deletions of the misnamed
copies; post-repair fetch-back 66/66 byte-identical, no stray names.
Audit 166/166 gates rc=0 x4 byte-identical and the 3-mode tamper battery
completed after the official passes. Counter-probe re-checked at wave-D
push time (head 8fda2888, no concurrent lane in this territory; "fifthres30"
code-search still 0 hits outside this kit).

Honest environment disclosure (also in the declaration): this executing
session ran on an upgraded sandbox WITH a native C++ toolchain (unlike
the third-impl batch hosts). One anchor-at2m calibration run (PASS,
98,2000000,0,2000000) was executed at binary-build time BEFORE the
declaration push as an environment sanity check; no target row ran
before publication. zig tarball sha re-verified before the build; all
three gate-source pins byte-verified against the pinned commit before
the build.

## Status guard

Scheduling and verification only. No verdict is consumed. The canonical
chain head of record (02db5ab3 after Part SQ) is untouched by this Part.
If a future adoption Part adopts these rows, the flip set and class
movement are decided by the canonical chain merge under the parent
batch's WIN/LOSS conflict policy, not by this kit. The two-stone root
{60,27}, its remaining third moves {100,108}, and the 11x11 empty board
remain UNKNOWN throughout. S5 LOSS raws are not class closure claims and
not routes to the root certificate.
