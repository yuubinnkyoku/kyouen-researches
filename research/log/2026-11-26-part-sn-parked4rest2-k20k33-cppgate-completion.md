# Part SN completion: parked4rest2 L50M WIN rows delegated pinned C++ scrutiny gate closes complete (k20/k33 GATE-PASS)

Date: 2026-11-26 (long-term lane session executing the Part SN declaration
research/log/2026-11-26-part-sn-parked4rest2-k20k33-cppgate-declaration.md
waves A 41a4d5d3 / B 08f9fd14, published earlier the same day).

## Outcome

The delegated pinned C++ second-implementation scrutiny gate for the two
UNCONSUMED sixth-cost parked4rest2 (k20/k33) S5 L50M ladder WIN rows ran
per the pre-registered protocol and closed complete:

- anchor-at2m 98,2000000,0,2000000 GATE-PASS (2 fresh-cold passes)
- anchor-aj001 84,30000000,2,5156075 GATE-PASS
- anchor-af039 89,30000000,2,19234232 GATE-PASS
- k20 10376293541461626880:33619968 -> 95,50000000,1,16196331 GATE-PASS
- k33 12682136550675320832:65536 -> 91,50000000,1,15842649 GATE-PASS

11/11 passes, zero MISMATCH / GATE-FAIL / GATE-CRASH / truncation,
node-exact against the published ladder raws (the SSOT quadruples).
Single-pass node bill 58,429,287 (targets 32,038,980 + anchors
26,390,307), bookkeeping only. Official execution window
14:00:08Z-14:04:07Z, pre-registered anchors-first order.

## Verification chain (fail-closed, no interpretation)

- All 10 published kit byte pins re-verified against the declaration
  BEFORE the build (inputs incl. gate-rows.json, runner, audit script,
  tamper battery, maker).
- Pinned gate source fetched from commit
  154f3b7a67b97e13acbaee8b04dc74ddca728d19: kyouen_dfpn_root.cpp
  9193f5b6... / kyouen_residual_micro.hpp 5976935d... /
  n11_s5_quarantine.hpp 2e36d694... all three sha256 pins verified
  byte-exact.
- zig 0.13.0 official tarball sha256 d45312e6... re-verified (the first
  download attempt timed out and replaced this session's host; every SSOT
  byte was re-fetched and re-pinned-verified afterward; nothing of record
  value was lost - honest environment disclosure, recorded below).
  Binary (unpinned per protocol, host codegen differs by design):
  sha256 3f4a426f...
- Kit audit_gate.py: 26/26 gates PASS; 4 published runs
  (audit_gate.json == run1 == run2 == run3) byte-identical sha256
  3fbb449d... ; the post-battery clean-control regeneration byte-identical
  too.
- Tamper battery 3/3 fail-closed: T1 audit ROWS pin flip (k20 nodes
  16196331->16196332) -> G3:k20 FAIL rc=1; T2 raw k20.p1 flip ->
  G2+G3:k20 FAIL rc=1; T3 phantom GATE-PASS line -> G4 FAIL 6/5 rc=1;
  each restore byte-verified; clean control rc=0 (tamper.log /
  t1_result.json published).
- Freshness re-verified on the CURRENT canonical head of record: both
  target (lo,hi) pairs are absent from cc3694bb (the Part SP advanced
  head, 6,799 s5verdict rows WIN199/LOSS6600; content sha256 verified
  against the published pin before grepping), so k20/k33 remain
  verdict-unconsumed and fresh for any future adoption Part.
- Counter-probe at wave-C push time: main head unchanged (8d21dbe8),
  code-search probes "Part SN" / "parked4rest2 cppgate" / "16196331"
  clean of any competing k20/k33 gate artifact.

## Waves (fetch-back byte-verified)

- Wave C results 17 files: commit 26a583d0, fetch-back 17/17 sha256
  byte-identical via raw-CDN pin comparison (raws x10, gate-status.log,
  audit JSON x4, t1_result.json, tamper.log).
- Wave D kit close-out: commit 148fd25e (README.md + MANIFEST-sha256.txt
  28 entries), fetch-back 2/2 sha256 byte-identical.
- This wave F: this completion log.

## Honest disclosures (this executing session)

1. The executing session started AFTER a host replacement mid zig-tarball
   download (the initial fetch hit the command timeout and the
   environment reset, losing local scratch only). Every gate SSOT byte
   was re-fetched from main or from the pinned commit and re-verified
   against published pins before the build; the published record is
   unaffected.
2. The fetch-back via the GitHub contents-API text path initially
   reported false mismatches on the .out/.json/.log files (a connector
   text-extraction artifact, not a data divergence); the authoritative
   fetch-back is the raw-CDN sha256 comparison, which was 17/17 and 2/2
   byte-identical. Lesson recorded: for byte verification use the raw
   CDN curl + sha256 comparison, not API text extraction.
3. The environment-restart risk (documented in kit-8b's recovery record)
   was respected: the zig tarball fetch was the only long step and was
   re-run under a larger timeout; all gate runs were short per-row
   commands.
4. The declaration's pre-registered binary
   (628bced4...) was built on a DIFFERENT host than this session's
   (3f4a426f...). Both are unpinned per the SK/SM protocol; the anchors
   calibrated node-exact on this session's binary before any target row
   ran, per protocol.

## Coverage asymmetry (decision-relevant, kept from the declaration)

k20/k33 now carry: ladder 4-run primary battery + this second-implementation
gate. They do NOT carry third-implementation verdict-level corroboration
(Part SL predates them and parks them explicitly). They are therefore NOT
at the k13/k19 coverage level. A separately declared third-impl part
(SL pattern) is the natural next step before any adoption Part weighs
them; adoption-eligibility language must keep this asymmetry.

## Status guard

Scheduling and verification only. No verdict consumed, no cache row
published, no class status flipped, no route to any root certificate laid.
The standard 11x11 empty board, the two-stone root {60,27}, its remaining
third moves {100,108}, S2, class 1/2/4, and every closure class remain
UNKNOWN throughout. Nodes are bookkeeping, never verdicts. S5 WIN raws
are not class closure claims.
