# Part SR completion: fifth-resumption 30 LOSS rows C++ scrutiny gate closes complete

Date: 2026-11-26 (long-term lane session). This completion log closes
Part SR (declaration log
research/log/2026-11-26-part-sr-fifthres30-cppgate-declaration.md,
commit 947cf9e6).

## What closed

The delegated pinned C++ second-implementation scrutiny gate (9th
execution of the gate lineage) was obtained, executed and published for
the THIRTY fifth-resumption resolved-LOSS rows of the sixth-cost
exclusive S5 probe (k09..k43 minus the parked k20/k33/k38) - the
coverage asymmetry the Part SQ completion log records as standing
unconsumed with "no delegated C++ gate". All 33 rows GATE-PASSED
(3 calibration anchors + 30 targets), two fresh-cold passes per row,
node-exact against the published probe-lane raws: zero MISMATCH /
GATE-FAIL / GATE-CRASH / TRUNCATED. Per-pass node total 208,140,422
(targets 181,750,115 + anchors 26,390,307; bookkeeping, never verdicts).

Coverage position after this Part: every one of the 30 rows now has (a)
the ladder primary cold pairs (15M stage; k28/k32 and the k17/k18 2M
determinism pairs at the 2M stage), (b) Part SL third-implementation
verdict-level LOSS(2) corroboration (batch 32/32 all-pass), and (c) this
pinned C++ second-implementation gate GATE-PASS - the k13/k19 coverage
level (SM+SP precedent) minus adoption. Verdict NOT consumed: the 30
rows stay UNCONSUMED labels, absent from the canonical head of record
02db5ab3 (maker G2 freshness, re-verified at run time).

## Kit of record

research/experiments/n11-sixthcost-fifthres30-cppgate-20261126 (112
files pinned in MANIFEST-sha256.txt, verified 112/112 against main).
gate-rows.json 66250267... (schema n11-sixthcost-fifthres30-cppgate-rows-v1,
maker 231/231 gates ALL PASS); runner 59cbbefe... (SN byte-transform);
audit_gate.py e8a139a7... (SN machine transform), audit 166/166 gates
rc=0 x4 byte-identical 44358ce2...; tamper battery 3/3 fail-closed
(T1 audit pin flip -> G3:k09; T2 raw nodes edit -> G2+G3:k09; T3
phantom GATE-PASS -> G4 34/33) with byte-verified restores and clean
control rc=0; 66 GATE-PASS raws + gate-status.log (16:57:41Z-17:13:05Z).

## Wave chain (fetch-back byte verification per wave)

A declaration 947cf9e6 (fetch-back sha256 match). B kit 9d543bdd (38
files, fetch-back 38/38 byte-identical). C results 5d417167 (73 files)
PLUS a disclosed publication repair: the wave C push wrote the 66 raws
under truncated names (<key>.p1/.p2 instead of .p1.out/.p2.out - a
path-suffix bug in the push payload builder; the raw-CDN fetch-back
returned 404s immediately). Repair: f07b6034 re-pushed the 66 correctly
named raws (content byte-identical), followed by 66 single-file
deletions of the misnamed copies (delete_file is one commit per file;
the history carries 66 repair commits, disclosed here and in the kit
README). Post-repair fetch-back 66/66 byte-identical, stray-name probe
clean. D README + MANIFEST 76ab55c8 (MANIFEST machine-verified 112/112
against main). F this log.

## Determinism, battery, honesty

Official run serial, pre-registered order (anchors at2m/aj001/af039
then 30 targets ascending), each row two independent fresh-cold
processes with p1 == p2 on (legal,budget,result,nodes) and both equal to
the published replica quadruple. Audit 4 runs byte-identical. Tamper 3/3
fail-closed with byte-verified restores.

Honest disclosures (also in the declaration and kit README):
(a) One anchor-at2m calibration run (GATE-equivalent quadruple
98,2000000,0,2000000) was executed at binary-build time BEFORE the
declaration push as an environment sanity check; no target row ran
before publication, and the anchor is part of the pre-registered
official order re-run inside the execution.
(b) The wave C raw-name defect and its repair are disclosed above; the
published kit bytes are the correct final state only.
(c) Build environment: upgraded sandbox with native C++ toolchain; zig
0.13.0 tarball sha256 d45312e6... verified before the build; binary
3b42e226... unpinned per protocol (source pins authoritative; all three
gate-source pins byte-verified against the pinned commit 154f3b7a).
(d) The maker fetched every cross-SSOT artifact (SN kit gate-rows.json,
audit_k09k43.py, SL summary, canonical head, probe raws) from main at
the recorded HEAD and pin-verified before emitting gate-rows.json.

## Verdict scope

NO verdict is consumed. The 30 rows become second-implementation
gate-verified UNCONSUMED labels. Any adoption of these LOSS rows stays
with a separately declared adoption Part under the parent batch's
WIN/LOSS conflict policy. k38 stays parked@15M with NO L50M follow-up
claimed. The standard 11x11 empty board and every central-reply root,
the two-stone root {60,27}, its remaining third moves {100,108}, S2,
class 1/2/4 and all closure classes stay UNKNOWN throughout. Nodes are
bookkeeping, never verdicts.
