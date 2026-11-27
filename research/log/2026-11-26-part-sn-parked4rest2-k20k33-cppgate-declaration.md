# Part SN declaration: parked4rest2 L50M WIN rows delegated pinned C++ scrutiny gate (publish-then-execute)

Date: 2026-11-26 (long-term lane session; this lane continues the
parked4rest2 ladder whose kit waves A/B/C landed earlier today at commits
2d918c32/44d8d90b, 28ed5748, f60350ea).

## Scope (single-owner claim, publish-then-execute)

Part SN executes the delegated pinned C++ second-implementation scrutiny
gate for the two UNCONSUMED sixth-cost parked4rest2 (k20/k33) S5 L50M ladder
WIN rows (the ladder resolved both to WIN(1) at budget 50,000,000):

- k20 10376293541461626880:33619968 (legal 95), expected
  legal,budget,result,nodes = 95,50000000,1,16196331
- k33 12682136550675320832:65536 (legal 91), expected
  legal,budget,result,nodes = 91,50000000,1,15842649

These are the "win_raws_needing_scrutiny" /
"delegated_cpp_gate_targets" rows of the parked4rest2 ladder halt-audit
(research/experiments/n11-sixthcost-class10376293541461626880-parked4rest2-s5-l50m-ladder-20261126/
output/halt-audit.json, kit commit 28ed5748; gates_passed_count 75,
ALL PRE-WIN GATES PASS -> HALTED ON WIN (stopping rule 1)); its
"determinism" field records verbatim that the pinned C++
kyouen_dfpn_root.cpp re-verification is REQUIRED before any row may be
consumed and that, per the Part SM precedent, it runs as a
publish-then-execute gate kit (zig 0.13.0 build of source
sha256 9193f5b6..., expected quadruples pre-registered in the audit JSON)
failing closed on any disagreement.

Honest coverage disclosure (pre-registered scope delta vs Part SM): NO
third-implementation verdict-level corroboration exists for k20/k33. The
Part SL batch (out/audit-k09k43-summary.json: all_pass, 32 rows audited)
predates this ladder; its claim string records "k20/k33/k38 stay parked
with no new verdict" and its row table contains no k20/k33 entry. The
SN kit maker therefore records
third_impl_verdict_level_corroboration=false for both targets and its G2
cross-SSOT section verifies this absence (plus the SL summary pins)
instead of the SM maker's third-impl agreement gates. Consequence recorded
up front: after a GATE-PASS here the two rows are
second-implementation-verified on top of the ladder's 4-run primary
battery (50M cold pair + 32M margin + voluntary third cold 50M verify,
each reproduced on the pinned 15M park baseline), but they are NOT at the
k13/k19 coverage level (which included the SL third-impl verdict-level
batch) until a separately declared third-impl part admits them; any
adoption decision must weigh that asymmetry.

This Part consumes NO verdict, publishes NO cache row, flips NO class
status, and lays NO route to any root certificate. The standard 11x11
empty board, the two-stone root {60,27}, its remaining third moves
{100,108}, S2, class 1/2/4, and every closure class stay UNKNOWN
throughout. Nodes are bookkeeping, never verdicts.

## Pre-registered protocol (fail-closed, no interpretation)

- Gate source: the delegated pin cpp/solvers/kyouen_dfpn_root.cpp at
  commit 154f3b7a67b97e13acbaee8b04dc74ddca728d19 sha256
  9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e with
  headers kyouen_residual_micro.hpp 5976935d... and n11_s5_quarantine.hpp
  2e36d694... at the same commit (pins machine-read from the published
  Part SK kit gate-rows.json by the kit maker; the source bytes fetched
  from the pinned commit verify all three pins - maker G0). Disclosure
  kept from SK/SM: the solver file has since moved on main; the pin, not
  the current main copy, is the source authority.
- Build: zig 0.13.0 official tarball zig-linux-x86_64-0.13.0.tar.xz
  sha256 d45312e61ebcc48032b77bc4cf7fd6915c11fa16e4aad116b66c9468211230ea
  (re-verified this session after the restart below), `zig c++ -std=c++20
  -O2` on the pinned source.
- Binary disclosure (honest, differs from Part SM's run): built on THIS
  sandbox host the binary hashes
  628bced4101a7d1bdebbd9614c3d0abbe58606faa0c3111403715b9fd7a0f109, NOT
  the Part SM recorded binary d376b9e7... Per the SK/SM protocol the
  binary is recorded-not-pinned: source pins are authoritative, host
  codegen differences are expected, and the byte-identity observed
  between two builds earlier the same day (before the environment
  restart, same host) was a host coincidence, not a protocol requirement.
  Acceptance is anchored by the calibration anchors below: the three
  anchor rows MUST reproduce the published C++ raw quadruples node-exact
  on THIS binary before either target row is trusted (pre-registered
  anchors-first order), and the runner enforces two-pass determinism per
  row anyway. If an anchor disagrees: HARD-STOP, no interpretation, no
  target rows run.
- Runner: the published Part SM kit runner byte-clone (diff = exactly the
  2 comment lines naming Part SN; asserted inside the maker; template
  MANIFEST-pinned). Row order: 3 calibration anchors first (SK kit
  byte-cloned inputs, SK kit MANIFEST pins, published expected
  quadruples), then k20, k33. Two fresh-cold passes per row, one process
  per pass. Acceptance per row: p1 == p2 on (legal,budget,result,nodes)
  AND both == the pre-registered expected quadruple above. Any MISMATCH /
  GATE-FAIL / GATE-CRASH / truncated output: HARD-STOP, no
  interpretation, no re-run-and-trust, honest disclosure in the
  completion log. wall_s is never compared.
- Anchors (calibration, expectations machine-read from the SK kit
  gate-rows.json anchors block):
  - anchor-at2m 1152921504606851072:536870946 budget 2,000,000 expected
    98,2000000,0,2000000
  - anchor-aj001 1152922604269469696:65536 budget 30,000,000 expected
    84,30000000,2,5156075
  - anchor-af039 1152921504607895681:68719476736 budget 30,000,000
    expected 89,30000000,2,19234232
- Audit: kit scripts/audit_gate.py (machine transform of the published SM
  kit audit script; diff = module docstring + machine-generated
  ROWS/RAW_PROV + part/schema strings, asserted inside the maker) over
  the kit outputs (raw shape, per-row p1/p2 determinism except wall_s,
  published-raw pins, gate-status accounting, input byte-clones). Tamper
  battery: kit tamper_battery.sh (machine transform of the SM battery:
  k20 quadruple flip on the audit pin / on a raw / a phantom third
  GATE-PASS line; restore + byte-verified; clean control rc=0).
- Freshness (maker G4): both target (lo,hi) pairs are absent from the
  canonical merged head of record 16a12390... (Part EW close-out, 6,797
  s5verdict rows WIN 197 / LOSS 6,600, published file
  research/experiments/n11-centralreply-sixthwin5-adoption-predecl-20261126/
  output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache), so both
  rows are verdict-unconsumed labels at declaration time.
- Kit maker: scripts/make_kit_parked4rest2_cppgate_20261126.py (structural
  clone of the published Part SM maker; full delta list in its docstring:
  part/schema strings, KEYS/TARGETS k20/k33 with the parked4rest2 pin
  locations incl. this lane's root status.log accounting lines, SM-kit
  transform templates, and the third-impl disclosed-absence section), 70
  fail-closed gates ALL PASS at build time (G0 gate-source pins; G1
  parked4rest2-kit SSOT discipline incl. base15m park baselines, the
  l50m-run1/run2 pairs, the 32M margin re-proof raws, the voluntary
  run3-verify raws, the published two-target validation rows, the
  status.log accounting; G2 cross-SSOT vs the halt-audit
  per_key/delegated blocks + the ladder kit README lines + the pinned
  solver/jsreplay pins + the disclosed SL third-impl absence; G3 anchor
  byte-pins vs the SK kit MANIFEST; G4 canonical-head freshness; G8 emit
  + ASCII-only assertion + clone byte-verification). Maker stdout
  byte-identical across two runs; emitted kit bytes byte-identical
  across those runs (determinism pre-checked).

## Pre-registered kit byte pins (published in wave B right after this log)

Kit root: research/experiments/n11-sixthcost-parked4rest2-l50m-cppgate-20261126/

- input/k20.input.csv =
  0984400f8aa99735e11e2638f5bc9a9273ddd296e845f7b7118f3ada81adddad
  (byte-clone of the parked4rest2 ladder kit input/batch-k20.input.csv)
- input/k33.input.csv =
  ca081b0f2f85e62b39cbbd1178a7be839c87e3446b2357657bbfe8681f82e2f4
  (byte-clone of the parked4rest2 ladder kit input/batch-k33.input.csv)
- input/anchor-at2m.input.csv =
  ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348
  (byte-clone of the SK kit input; == EQ/EN/EO/EV/SM kit input)
- input/anchor-aj001.input.csv =
  2f6daea5ca3b3fe6b7713c8d450af3f3c9f203acacb8a1340255d8e8f656496c
- input/anchor-af039.input.csv =
  e51a3c9de08c62a54d80547c520876af4245394d05e37bbebf01d74204f64691
- input/gate-rows.json =
  b72105bca125354456161469f4bf5bb218b6d155e4ac91045291bab813affec8
  (schema n11-sixthcost-parked4rest2-cppgate-rows-v1)
- scripts/make_kit_parked4rest2_cppgate_20261126.py = (byte-clone of the
  maker that emitted this kit; its own sha256 is in the wave B commit and
  the kit README/MANIFEST of wave D)
- scripts/audit_gate.py =
  23aa7d523721eb2d277bf80e7826685c7ae0b9c440380f56fd53937db76bdf0c
- scripts/gate_runner.sh =
  f2534b76e95959ccba0057edca8576d0a442ab4a52ac76d1b306b51dfff8a852
- tamper_battery.sh =
  482bcf313e99dff14b15021f362e68b71324ff417f31d26ccefa2062ea8c0787

## Counter-probe record (claim-clean)

Content probes run at build time via the authenticated code-search API:
query "Part SN" over the repo returns only 2 paths, both non-claims (the
Part SM declaration's free-slot note and the parked4rest2 lane
single-owner declaration's future-work prediction); "parked4rest2" +
"cppgate" returns only the lane declaration. The k20/k33 expectation
numbers (16196331, 15842649) were not yet in the code-search index at
probe time (the wave B kit landed ~30 minutes earlier; index lag
disclosed; the raw-CDN fetch-back of the wave B kit README/audit files
during this session's SSOT rebuild DID contain both numbers, published
byte-exactly). No competing k20/k33 C++ gate artifacts exist on main. To
be re-probed at push time.

## Environment disclosure (restart incident, recorded honestly)

Between this lane's wave C push (f60350ea) and this Part's build, the
session's execution environment was replaced (stale host gone mid-session).
ALL local state was destroyed; nothing of record value was lost because
every wave was already published and fetch-back byte-verified. The entire
gate SSOT was re-fetched from published pins and byte-re-verified against
them in this session before the build: the parked4rest2 ladder kit (all
27 files vs its published MANIFEST-sha256.txt), the SK kit template files
(vs its MANIFEST), the SM kit template files (vs its MANIFEST), the
canonical head of record 16a12390 (byte-verified), the pinned three
source files from commit 154f3b7a (all three pins verified), the Part SL
summary (published path
research/experiments/n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122/out/audit-k09k43-summary.json),
and the zig 0.13.0 tarball (sha d45312e6... re-verified). This session
runs without access to the user's machine; every repo interaction happens
through the GitHub API/raw CDN, and every published wave gets fetch-back
byte verification. If any push fetch-back fails, or a concurrent lane
pushes into the same territory first, this Part re-reads the latest main,
does not force its way, and records the situation honestly instead.

## Status guard

Scheduling and verification only. No verdict is consumed. Unknown stays
unknown. If any row GATE-FAILs, both rows stay exactly as the canonical
chain has them and the failure is recorded as an experimental fact with
full raws. The standard 11x11 empty board, the two-stone root {60,27},
its remaining third moves {100,108}, S2, class 1/2/4 and every closure
class remain UNKNOWN throughout.
