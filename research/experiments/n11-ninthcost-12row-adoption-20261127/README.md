# n11-ninthcost-12row-adoption-20261127

Ninth-cost 12-row canonical adoption kit (9 LOSS rows + 3 WIN rows
k12/k02/k07, class `1297036692683751424:134217728` exclusive-probe
batch). Kit of the wave A declaration
(research/log/2026-11-27-n11-ninthcost-12row-adoption-declaration.md,
commit 7780e2f8, publish-then-execute: the maker and merger runs
recorded here all happened after that publication).

## Files

- scripts/make_kit_ninthcost12_adoption_20261127.py - fresh single-owner
  maker, structural descendant of the published Part SZ maker
  (make_kit_sz_adoption_20261127.py): G0 anchor byte gates (base head
  of record 0935c94c, 6,875 rows WIN 203 / LOSS 6,672; merger 90711961;
  quarantine 81d23160; policy 78655e94; frozen graph 54f9c364), G1 the
  four C++ scrutiny gate kits re-verified file-by-file (4loss 33/33,
  4lossrest 32/32, k12 23/23, parked3-L50M 29/29) with every
  audit_gate.py re-run LIVE PASS (N9_HEAD), G2 the four third-impl
  corroboration kits re-verified per-file byte pins + raw re-parse
  (verdict-level agreement, node_rc=0, per-key pairs identical;
  third_impl.js pin 08ea958f in all four; DISCLOSED deviation: the
  ninth-cost third-impl kits carry no audit script, so no live audit
  re-run exists for them), G3 the 12 adoption pins re-derived against
  the four gate-rows expected quadruples and cross-checked against the
  third-impl raw result fields, G4 freshness 12 / WIN-LOSS conflict 0
  (vacuously clean, 12/12 absent) / duplicate 0 / quarantine-free /
  canonical-safe per s5_evidence_policy, G5 increment emit, G6
  manifest. Two runs byte-identical.
- output/increment-ninthcost12-adoption-20261127.cache - the 12-row
  increment (24 comment lines + 12 rows: 9 LOSS + 3 WIN), sha256
  72eac70c1503e7bfafcbdbe66adb12b1a1e52224ffca3eac296e2118c47a6bb0.
- output/adoption-manifest.json - adoption manifest, sha256
  db43c1a52171df30b10ff4b65dfd28eb2eb1435b41b2a95ff721852577f4537e.
- output/merged/merged-exact-s5-chain-plus-ninthcost12-20261127.cache
  - the new canonical head of record, produced by the pinned merger
  s5_union_merge.py (sha256 90711961...) run THREE times
  byte-identical: 6,887 rows, WIN 206 / LOSS 6,681, 288,440 bytes,
  sha256 4728007306598298f7fdb43d0368bc4e5fbd6c9435a38f8d1732d1df8368a622.
  Exactly the pre-registered shape (6,875 + 12; WIN 203+3; LOSS
  6,672+9). Machine-checked on this host: all 12 adopted rows present,
  all 6,875 BASE rows preserved, zero duplicates elided.
- output/merged/merge-audit-run1.json / run2 / run3 - the merger's own
  fail-closed audit records, byte-identical across the three runs
  (sha256 5d1032a5...).

## Known published defect (disclosed, not fixed by this lane)

The k12 third-impl kit's own MANIFEST-sha256.txt pins README.md with a
stale line (third_impl.js's sha256 and size 2259; the README on main
is 2,645 bytes, sha256 07515850...). This maker verifies that README
against the main-actual pin and records the stale published line in
the adoption manifest instead of trusting it. The defect is
bookkeeping-only (no raw, no pin of record is affected); correction
belongs to that kit's owner lane.

## Maker run record (this host, Python 3.12)

- run1: N12 INCREMENT PASS rows=12 WIN=3 LOSS=9
  increment_sha256=72eac70c... manifest_sha256=db43c1a5...
- run2: byte-identical increment + manifest (cmp PASS).
- merger x3: MERGED unique=6887 dup_elided=0 WIN=206 LOSS=6681, three
  byte-identical outputs (audit output_sha256 47280073... x3).
- Maker self-bugfix disclosures (all caught by the maker's own
  fail-closed gates or assertions before any output was published):
  a THIRD_IMPL_SHA constant typo (fail-closed T4L sha drift), a TI-kit
  column index bug (KeyError, no output), a raw row-label
  strictness bug (the 4loss kit labels rows "k01" without the .p1
  suffix - label check relaxed to accept both published label forms),
  and a gate-rows key-field polymorphism (the parked3 gate-rows uses a
  "key" string instead of separate lo/hi - derived by split). The
  gate-rows expected quadruples themselves were never relaxed.

## Meaning and non-meaning

Admission of published, corroborated S5 raw verdicts into the canonical
solver-trusted cache chain only. NO root verdict is consumed, no
class-status change, no closure claim. The flip-census review of the
three WIN rows (k12/k02/k07) is a separately declared Part (SZ wave E /
Part EM precedent) and must run against this new head before any
class-status use of the WIN rows. The standard 11x11 empty board, all
19 central-reply roots, the two-stone root {60,27}, its remaining third
moves {100,108}, S2 and all closure classes are UNKNOWN. A WIN(1) or
LOSS(2) S5 raw is not a class closure claim, not a root verdict, and
transfers nothing. Nodes and expansions are bookkeeping, never
verdicts.
