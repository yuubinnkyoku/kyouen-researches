# n11 Part SZ kit: seventh-cost 42-row canonical adoption

Kit of the wave A declaration
(research/log/2026-11-27-n11-seventhcost-sz-adoption-declaration.md).
Publish-then-execute: the maker and merger runs recorded here all
happened after that publication.

## Files

- scripts/make_kit_sz_adoption_20261127.py - fresh SZ maker
  (structural descendant of the Part ST maker, sha256 d4949f71...):
  G0 anchor byte gates (base head of record 42dbb58f, 6,832 rows
  WIN 201 / LOSS 6,631; merger 90711961; quarantine 81d23160; policy
  78655e94; frozen graph 54f9c364), G1/G2/G3 pillar gates (Part SW
  41-LOSS C++ gate kit 145/145 MANIFEST-verified + audit_gate.py
  re-run LIVE PASS; Part SX k05-WIN C++ gate kit 24/24 verified +
  audit LIVE PASS; Part SY third-impl corroboration kit 143/143
  verified + audit_sy.py LIVE AUDIT-PASS targets=42 raws=84),
  G4 the 42 adoption pins re-derived against the SW/SX gate-rows
  expected quadruples + replica_verdict and the SY gate-rows
  replica_expected_quad fields, G5 freshness 42 / WIN-LOSS conflict 0 /
  duplicate 0 / quarantine-free / canonical-safe per s5_evidence_policy,
  G6 increment emit (k05 emits result=1 nodes=15763505), G7 manifest.
  Two runs byte-identical (disclosed below).
- output/increment-seventhcost42-adoption-20261127.cache - the 42-row
  increment (24 comment lines + 42 rows: 41 LOSS + 1 WIN), sha256
  959ae2dd249a1d78be1f67f68640a4371fa13ca2e4b31d3b39bb44cb05519f1f.
- output/adoption-manifest.json - adoption manifest, sha256
  14ef4fc23cf6649b47fb67a9f544626ec3a4637d08c5e2b236e7906cbe0b9f82.
- output/merged/merged-exact-s5-chain-plus-seventhcost42-20261127.cache
  - the new canonical head of record, produced by the pinned merger
  s5_union_merge.py (sha256 90711961...) run THREE times byte-identical:
  6,874 rows, WIN 202 / LOSS 6,672, 287,763 bytes, sha256
  5b6e77f7d7832d4ce84cb1f080a93e066eb052dcf8b817e5d560f95499fcdde2.
  Exactly the pre-registered shape (6,832 + 42; WIN 201+1; LOSS
  6,631+41).
- output/merged/merge-audit-run1.json / run2 / run3 - the merger's own
  fail-closed audit records, byte-identical across the three runs.

## Maker run record (this host, Python 3.12)

- run1: SZ INCREMENT PASS rows=42 WIN=1 LOSS=41
  increment_sha256=959ae2dd... manifest_sha256=14ef4fc2...
- run2: byte-identical increment + manifest (cmp PASS).
- merger x3: MERGED unique=6874 dup_elided=0 WIN=202 LOSS=6672,
  three byte-identical outputs (audit output_sha256 5b6e77f7... x3).

## Meaning and non-meaning

Admission of published, corroborated S5 raw verdicts into the
canonical solver-trusted cache chain only. NO root verdict is
consumed, no class-status change, no closure claim. The standard
11x11 empty board, all 19 central-reply roots, the two-stone root
{60,27}, its remaining third moves {100,108}, S2 and all closure
classes are UNKNOWN. A WIN(1) or LOSS(2) S5 raw is not a class closure
claim, not a root verdict, and transfers nothing. Nodes and expansions
are bookkeeping, never verdicts.
