# n11 sixth-cost class 10376293541461626880:65536 parked4-rest2 (k20/k33) S5 L50M ladder - session log (2026-11-26, halted on WIN at BOTH claimed keys)

Session of the recurring n11 long-term lane; declaration
`research/log/2026-11-26-n11-sixthcost-class10376293541461626880-parked4rest2-s5-l50m-ladder-single-owner.md`
(push `2d918c32` 12:01:02Z, wording-typo repair `44d8d90b` 12:01:39Z, both
fetch-back byte-verified; HEAD immediately before the declaration push was
`9d9be4b6` = the Part SM wave F completion log). Kit:
`research/experiments/n11-sixthcost-class10376293541461626880-parked4rest2-s5-l50m-ladder-20261126/`,
published as wave B commit `28ed5748` (RIGHT after the concurrent kit-9 commit
`c660fe15` 12:24:19Z; all 27 kit files fetch-back byte-verified against the
kit MANIFEST-sha256.txt via the contents API, local == remote == manifest).
Completion: this log (wave C).

## Why this lane

The parked4 L50M lane (same class, kit commit 73dfd4a7) halted on WIN at its
two started keys k13/k19 and recorded, under stopping rule 1, that its two
never-started claimed keys remain parked@15M, claimable by a later lane:
k20 `10376293541461626880:33619968` (legal 95, machine-order position 20) and
k33 `12682136550675320832:65536` (legal 91, position 33). Part SM closed the
k13/k19 delegated C++ gate (GATE-PASS, node-exact), leaving k20/k33 as the last
two minimal blockers of the sixth-cost class's parked set. This lane raised
their budget 15M -> 50M on the identical exact-replay protocol (third-cost
parked2 L50M precedent, inherited via the parked4 lane), as a SINGLE-OWNER
lane in a new experiment directory with no shared files, after re-cloning all
six pinned corpora and re-verifying every sha.

## Protocol deltas vs the parked4 lane (all pre-registered in the declaration)

- LANE_KEYS = k20/k33 only (k13/k19 belong to the parked4 lane and its closed
  Part SM gate; nothing of theirs was re-run or re-claimed here).
- BASE retargeted from the Part EM head `6e49dd84` (6,792 rows) to the Part EW
  sixthwin5 adoption head `16a12390` (6,797 rows, WIN 197 / LOSS 6,600), the
  chain head of record at lane time. MY_CLASS before was machine-derived from
  the pinned cache + frozen geometry BEFORE drafting: 5 WIN / 8 LOSS / 95
  UNKNOWN of 108 children, i.e. exactly the Part EW win-hit (excluded_now)
  state of serving class 3077; under the audit's local status rule
  (any child WIN => class WIN) the class reads WIN before this lane.
- Audit script `scripts/audit_parked4rest2_l50m.py` is a structural clone of
  the parked4 `scripts/audit_parked4_l50m.py` (clone-commit disclosure in its
  docstring; no gate added, removed or weakened).

## Timeline (UTC, this host; Node v22.20.0; serial per-key stages, 2 concurrent
worker processes, nohup launch pattern throughout)

- Session start: six SSOT pins re-downloaded and sha-verified (selection
  `d5e9b059`, supply `31f0d29b`, policy `78655e94`, independent `954d3a10`,
  quarantine `81d23160`, geometry `146be80b`); BASE retargeted to
  `16a12390...` (6,797 rows) and MY_CLASS-before machine-computed (5/8/95);
  both exact keys machine-verified ABSENT from `16a12390`, from the
  quarantine registry and canonical-safe-policy-safe.
- Fresh-session validation gates (before any ladder row was trusted): the four
  published two-target validation rows reproduced node-exact on this host
  (at2m x2: result 0 / nodes 2,000,000 / legal 98, 99; 15M rows: result 2 /
  nodes 3,651,923 and 5,040,200 / legal 98, 99; walls 20/21/40/49 s).
- 12:01:02  declaration pushed `2d918c32`; fetch-back caught one corrupted
  wording line in a claim-hygiene bullet; wording-only repair `44d8d90b`
  pushed 12:01:39 and re-verified via the API blob (no gate, claim or number
  changed; raw-CDN lag noted, the blob API is the authoritative check).
- 12:01-12:04  per-key fresh 15M baselines reproduced the parent batch's
  published parked state exactly: k20 0/15,000,000 (wall 185 s), k33
  0/15,000,000 (wall 188 s). Both gates PASSED for both keys BEFORE any 50M
  stage started (k20+k33 baselines launched together at 12:01, before any 50M
  result existed).
- 12:04:23-12:08:25  l50m-run1 (both keys, cold, fresh solvers): k20
  **WIN(1) nodes 16,196,331** (wall 200 s), k33 **WIN(1) nodes 15,842,649**
  (wall 194 s).
- 12:08:25-12:12:10  l50m-run2 determinism pair: both keys identical to run1
  (k20 1,16,196,331 wall 203 s; k33 1,15,842,649 wall 201 s).
- 12:12:10-12:16:22  32M budget-margin re-proofs: both keys identical again
  (k20 1,16,196,331 wall 197 s; k33 1,15,842,649 wall 193 s) - both WINs are
  full df-pn proofs completing at ~1.080x (k20) and ~1.056x (k33) of the 15M
  park budget, which explains the parent probe's parking on the WIN side.
- 12:16:22-12:19:38  voluntary third cold 50M verification runs (honestly
  labeled, k02..k08 precedent): both identical (k20 1,16,196,331 wall 191 s;
  k33 1,15,842,649 wall 195 s). FOUR post-baseline identical WIN executions
  per key (run1 + run2 + margin + run3-verify) plus the reproduced parked
  baseline.
- ~12:20  fail-closed audit `scripts/audit_parked4rest2_l50m.py`: **ALL 75
  PRE-WIN GATES PASS -> HALTED ON WIN [k20, k33]**, rc=2,
  `output/halt-audit.json` written, NO OK audit, NO cache file (declared
  no-increment rule). Audit regeneration: two further runs byte-identical to
  the first halt-audit.json. Tamper battery on scratch clones: T1 raw run1
  node flip 16,196,331 -> 16,196,331+1 -> GATE FAIL `k20.determinism` rc=1;
  T2 BASE cache pin flip `16a12390...` -> `06a12390...` -> GATE FAIL
  `base_chain_cache_sha` rc=1; T3 val-row result flip 2 -> 0 -> GATE FAIL
  `validation_val-first-15m` rc=1; all restores byte-verified; clean control
  re-run rc=2 halt-intact, twice.
- C++ second-implementation preparation: the three pinned source files
  re-fetched and sha-verified (`kyouen_dfpn_root.cpp` `9193f5b6...`, plus the
  root batch header and the kit-9-era anchors used by the Part SM gate); a
  fresh zig 0.13.0 build of the pinned source was verified BYTE-IDENTICAL to
  the Part SM gate binary (sha256 `d376b9e7...`), so this sandbox family's
  reproducible-build property held; the binary stays recorded-not-pinned,
  the source pins are authoritative.
- Honest environment disclosure (also in the kit README and status.log): the
  session.environment zig background-build experiment (outside the lane's
  stages) died twice by silent background-kill during the ladder runs; it
  touched no lane artifact and was rebuilt cleanly in the foreground
  afterward. `output/status.log` was re-authored at the declaration wave with
  clean per-stage lines; the raw rows under `output/raw/` are the
  byte-authoritative artifacts.
- Concurrent lane commits observed mid-lane (territory-disjoint from this
  lane's keys and files): parked4-referenced Part SM waves
  `9fd08e79`/`9d9be4b6` (11:52Z), kit-9 `c660fe15` (12:24:19Z). HEAD
  immediately before the wave B push was `c660fe15`.

## Results (all verdict-unconsumed raw evidence; no cache row)

- k20 `10376293541461626880:33619968` (legal 95, machine-order position 20):
  **WIN(1) in nodes 16,196,331**, identical across 2 cold 50M runs + 32M
  margin + voluntary third cold 50M verify (4-run battery) on the reproduced
  parked 15M baseline.
- k33 `12682136550675320832:65536` (legal 91, position 33): **WIN(1) in nodes
  15,842,649**, identical across the same 4-run battery.
- With k13/k19 (parked4 lane, Part SM gate closed), the sixth-cost class's
  parked set now has four fresh WIN raws pending or through scrutiny; k20/k33
  are the ELEVENTH and TWELFTH fresh WIN children in the unconsumed batch
  record (after k02/k03/k04/k05/k08/k13/k19), and like k13/k19 they were
  first parked by a 15M probe and are the second pair found completing just
  above the 15M budget line (1.080x / 1.056x).
- If-adopted (NOT adopted; recorded only in `output/halt-audit.json` against
  the head of record `16a12390`): the class would hold 7 WIN / 8 LOSS / 93
  UNKNOWN of its 108 children (local rule WIN; it was already win-hit on the
  head); the recorded hypothetical global status changes beyond that count
  are classes `1297037794341814272:0` UNKNOWN -> WIN and
  `1873498544497754112:0` UNKNOWN -> WIN. The root impact through the
  depth-2/depth-1 chain is NOT computed by this lane (K0414/K0416 lineage
  owners).

## Mandatory scrutiny before any consumption (handed to scrutiny owners)

1. Second-implementation re-verification for BOTH fresh WIN rows, per the
   Part SM precedent a publish-then-execute C++ gate kit (zig 0.13.0 build of
   the pinned `cpp/solvers/kyouen_dfpn_root.cpp`, source sha `9193f5b6...`;
   expected quadruples pre-registered in `output/halt-audit.json`:
   `target,0,5,10376293541461626880,33619968,95,0,0,0,0,0` @ 50,000,000
   expected result 1, nodes 16,196,331;
   `target,0,5,12682136550675320832,65536,91,0,0,0,0,0` @ 50,000,000 expected
   result 1, nodes 15,842,649). The kit clone of `gate_runner.sh` and the
   anchor gates must be re-published for THIS lane's targets before
   execution (this session did not publish the gate kit; the build
   reproducibility check above is preparation, not the gate).
2. Game-theoretic consistency review against the historical WIN rows in the
   chain and the class-vs-root backward chain (K0414/K0416 lineage owners).
3. Only then: cache emission through the parent batch's full audit under the
   WIN/LOSS conflict policy. Until then both rows stay unconsumed. The
   witness-side asymmetry stands as in the parked4 record: the parent's
   witness scripts have not been extended to these keys by this lane.

## Resume notes for the next run (re-fetch latest main before starting)

- The natural continuation is the Part SN-equivalent C++ gate kit for
  k20/k33 (web A/B/C/D/F pattern), then the four-key k13/k19/k20/k33 adoption
  part (EW pattern: fresh BASE at the post-gate head of record, halted-scenario
  recompute, counter-probe). Nothing else claims these two keys.
- The parent batch's other unconsumed rows are untouched by this lane; the
  sixth-cost class killer question remains open (91 unknown children remain
  in the if-adopted scenario; a class is NOT closed by win-hit evidence, and
  no route to the root certificate exists through this batch alone).

## Status guard

The standard 11x11 empty board remains UNKNOWN. The two-stone root {60,27}
and its remaining third moves 100/108 remain UNKNOWN at every point of this
session. Nodes, budgets, solver counts and proxy values are never verdicts.
Nothing was adopted, no cache file was written, no class/root/board claim is
made by this session.
