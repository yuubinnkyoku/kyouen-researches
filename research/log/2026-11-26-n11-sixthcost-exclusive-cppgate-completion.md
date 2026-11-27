# Part SK completion: sixth-cost exclusive-probe k01..k08 C++ scrutiny gate GATE-PASS (2026-11-26)

Completion log for the sixth execution of the C++ second-implementation
scrutiny gate (after EN class-30484, EO class-34908, EQ class-30345
b38-win-18, ET class-30345 ES-re-probe-6, EV closure-batch WIN-4) - the
FIRST outside the central-reply closure-batch chain. This Part took the
delegated pinned C++ gate of the sixth-cost exclusive-probe batch
(declared since 2026-11-21, recorded unexecuted in every sixth-cost lane
session's "no C++ toolchain in this sandbox" note) on a host that does
have a C++ toolchain, per the single-owner declaration.

## Publish-then-execute timeline (all commits on main, no branch/PR)

| wave | commit (UTC) | content | fetch-back |
|---|---|---|---|
| A | e42e44a4 08:21:17Z | declaration log (kit + plan before any solver pass) | byte-identical |
| B | 2112241a 08:21:30Z | kit 16 files (inputs 12 byte-pinned / scripts 3 / battery) | 16/16 byte-identical |
| - | 08:22:15Z-08:28:25Z | official execution (22 fresh-cold passes, sequential) | - |
| - | ~08:28:41Z-08:28:42Z | audit x3 + tamper battery (post-run, kit-local) | - |
| C | c5a67038 | results 29 files (raws 22 / status / audit x4 / tamper.log / t1_result.json) | 29/29 byte-identical |
| D | 342abc50 | kit README + MANIFEST-sha256 (46 entries) | byte-identical |

## Execution record

Anchors first (at2m@2M, aj001@30M, af039@30M), then k01..k08 in key
order (k07 at its published 2M resolution condition), one pass = one
fresh cold process:

| key | expected legal,budget,result,nodes | status |
|---|---|---|
| anchor-at2m | 98,2000000,0,2000000 | GATE-PASS |
| anchor-aj001 | 84,30000000,2,5156075 | GATE-PASS |
| anchor-af039 | 89,30000000,2,19234232 | GATE-PASS |
| k01 | 87,15000000,2,10369650 | GATE-PASS |
| k02 | 87,15000000,1,7717432 | GATE-PASS |
| k03 | 81,15000000,1,9255414 | GATE-PASS |
| k04 | 83,15000000,1,9433024 | GATE-PASS |
| k05 | 88,15000000,1,13397611 | GATE-PASS |
| k06 | 89,15000000,2,8182231 | GATE-PASS |
| k07 | 87,2000000,2,1419823 | GATE-PASS |
| k08 | 89,15000000,1,6195897 | GATE-PASS |

Every row: two fresh-cold passes, p1 == p2 on
(legal,budget,result,nodes), both == the published replica raw,
acceptance node-exact. Zero MISMATCH / GATE-FAIL / GATE-CRASH /
TRUNCATED. Per-pass node bill 92,361,389 (anchors 26,390,307 + targets
65,971,082); two-pass bill 184,722,778 (bookkeeping, never verdicts).
Binary sha256 efb30000c792f1ab... (not pinned; source pins 9193f5b6 /
5976935d / 2e36d694 at 154f3b7a are the authority, EN/EO/EQ/ET/EV
disclosure kept).

## Audit and tamper battery

Audit (EQ rev4 structure, emitted by the maker): 4 executions
byte-identical sha256 ad139eceee6bd9e9... (audit_gate.json == run1 ==
run2 == run3, overall PASS). Tamper battery (sha256 2b1c60c901199725)
3/3 fail-closed: T1 ROWS-pin break k01 10369650->10369651 -> rc1 with
gates.G3:k01 FAIL (t1_result.json); T2 raw k01.p1 byte-alter
nodes 10369650->10369651 -> rc1 with G2:k01 + G3:k01 FAIL; T3 phantom
GATE-PASS line in gate-status.log -> rc1 with G4 pass-count 12/11.
Every tamper byte-change asserted before the audit run, every restore
byte-verified (pin == restore sha), final clean control rc0. Full pin /
pre / restore sha chain in the published tamper.log.

Honest deviation note (recorded, not silently dropped): the EV battery
emitted both t1_result.json and t2_result.json; this kit's battery
emits t1_result.json only. T2/T3 named-gate details are session-stdout
facts recorded in this log, backed by the tamper.log rc lines and sha
assertions; NO result JSON was fabricated post-hoc (publishing only
what the battery emitted).

Honest k02 disclosure (kept from the declaration): k02 has NO published
third-implementation reproduction - the C++ gate IS the second
implementation for k02. k01/k03/k04/k05/k06/k07/k08 have published
third-impl verdict-level agreement; the concurrent third-impl batch
(4d1b7db7, 30 fifth-resumption LOSS rows + k13/k19) does not cover k02
either. A future third-impl reproduction of k02 remains open and
welcome; any future disagreement with this gate fails closed in favor
of discarding the row.

## What this does and does NOT establish

The 8 rows stay gate-verified UNCONSUMED labels. The 5 WIN rows
(k02/k03/k04/k05/k08) BECOME adoptable by a separately declared adoption
Part (EP/ER/EU/EV pattern) against the already-published if-adopted
scenario `win-finding-ifadopted-k08.json` (five UNKNOWN->WIN class
flips; sixth-cost class children 101->93; remaining third moves
{100,108} unchanged - scheduling facts, not outcome claims). The 3
LOSS rows (k01/k06/k07) stay unconsumed probe labels.

Out of scope (consumed NOWHERE): every adopted canonical row, the
k13/k19 L50M WINs, the 30 fifth-resumption LOSS rows (no pinned C++
expectations yet; a future cppgate Part can take them with fresh pinned
targets), the third-implementation program (parallel lane), the
parked-4 L50M ladder territory, the canonical adoption machinery (no
cache file touched), the probe dir (no probe-kit raw/output path
written by this Part).

## Guarantees

The standard 11x11 empty board stays UNKNOWN. All 19 central-reply
roots, S2, class 1/2/4, the two-stone root {60,27}, and its remaining
third moves {100,108} stay UNKNOWN. nodes are bookkeeping, never
verdicts. No coverage, no secured-coverage, no root-verdict claim is
made anywhere.

## Concurrency record

Pre-declaration HEAD re-fetch 4d1b7db7 (the concurrent lane's third-impl
batch declaration); wave C pre-push HEAD re-fetch 2112241a (unchanged);
wave D pre-push HEAD re-fetch c5a67038 (unchanged). No concurrent push
occurred between our waves (no conflict, no retry needed). Territory
disjointness as declared in the declaration log is preserved by
construction: this Part wrote only its own experiment dir and logs.
