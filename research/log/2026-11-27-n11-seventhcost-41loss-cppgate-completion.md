# n11 Part SW completion log: seventh-cost 41 LOSS rows C++ scrutiny gate (wave F)

Part SW closes complete. Waves A dfb6b357 (declaration) -> B 2f7dec1e
(kit, maker all-gates PASS, 2 runs byte-identical, fetch-back 49/49) ->
C 45a1bbc6 (93 result files, fetch-back 93/93 git-blob-sha byte-identical)
-> D 3b3e07b2 (README run record + MANIFEST-sha256.txt 145 files pinned +
tamper battery). All fetch-back verification used GitHub contents API git
blob sha (sha1("blob <size>\0"+bytes)); raw CDN not relied on.

Result: 44/44 GATE-PASS (3 calibration anchors + 41 targets k01..k42 minus
k05, two fresh-cold passes per row, node-exact (legal,budget,result,nodes)
against the published seventh-cost probe raws). Official execution
02:54:05Z-03:10:46Z ascending, zero MISMATCH / GATE-FAIL / GATE-CRASH /
TRUNCATED. Per-pass node bill targets 211,789,419 + anchors 26,390,307;
two-pass bill 476,359,452 (bookkeeping). Audit 221/221 gates rc=0 x4
byte-identical sha256 7d60409c. Tamper battery (published script, scratch
copy only, deleted after): T1 audit ROWS pin flip -> G3:k01 FAIL; T2 raw
k01.p1 nodes edit -> G2+G3:k01 FAIL; T3 phantom GATE-PASS line -> G4 FAIL
45/44; restores byte-verified; clean control rc=0 (kit tamper.log).

Meaning and non-meaning: the 41 seventh-cost resolved-LOSS rows are now
second-implementation gate-verified (pinned C++ source 9193f5b6 @154f3b7a,
zig 0.13.0 d45312e6) on top of the ladder primary cold pairs. This is
scheduling and verification only: NO verdict is consumed, no cache
increment, no class-status change. Third-implementation corroboration is
still ABSENT for every seventh-cost row (and for the k05 WIN row, whose
C++ gate is also vacant), so no seventh-cost row is adoption-eligible yet;
adoption stays with a separately declared adoption Part under the parent
batch's WIN/LOSS conflict policy. The canonical chain head of record
42dbb58f (6,832 rows WIN 201 / LOSS 6,631) is untouched by this Part.

Honest disclosures (also in the declaration and kit README):
1. The executing session ran on an upgraded sandbox WITH a native C++
   toolchain; one anchor-at2m calibration run (PASS) was executed at
   binary-build time BEFORE the declaration push (SR precedent, disclosed
   there too); no target row ran before publication.
2. The 124 published probe raws were read from a local cache
   (_seventhkit-raws, populated by an earlier lane) sha-verified against
   the published MANIFEST-raw-sha256.txt fetched from the pinned HEAD
   f38d2b43 - a fetch-route optimization only; the published manifest pins
   are the raw SSOT (all 124/124 verified byte-identical before any
   expectation was derived).
3. The audit script is a machine transform of the published Part SR audit
   (docstring + machine-generated ROWS/RAW_PROV + part/schema strings
   only, logic byte-identical, asserted by the maker G3); the runner is
   the published SR runner with the comment block naming Part SW only.
4. The maker is a fresh structural clone of the published SR maker with
   the pre-registered deltas (part/schema strings, the 41 seventh-cost
   keys and their pin sources, third-impl ABSENCE section); two build
   bugs (a %-format arity typo and a dropped list/tuple paren, both caught
   by the maker's own Python syntax gate before any kit byte was emitted)
   were fixed before the first passing run; the emitted kit is from the
   final maker only.
5. Target wall batching (rows per shell command) was chosen to fit the
   sandbox 290s wall per command; rows are resume-safe (the runner re-runs
   truncated artifacts, never trusts them); the official sequence and
   order were exactly the pre-registered one.

Status guard: the standard 11x11 empty board is UNKNOWN. All 19
central-reply roots are UNKNOWN. The two-stone root {60,27} is UNKNOWN.
Its remaining third moves {100,108} are UNKNOWN. S2 and closure classes
1/2/4 and all closure classes are UNKNOWN. Nodes are bookkeeping, never
verdicts. S5 LOSS raws are not class closure claims and not routes to the
root certificate.
