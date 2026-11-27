# 2026-11-27 n11 tenth-cost k01/k02 canonical adoption completion

Wave C completion log of the adoption declared in
research/log/2026-11-27-n11-tenthcost-k01k02-adoption-declaration.md
(commit fecb961a). Kit published in commit 3128558c
(research/experiments/n11-tenthcost-k01k02-adoption-20261127/, 9
files, fetch-back 9/9 byte-identical via raw CDN pinned to the
publishing commit).

## Head of record advance

- New canonical head of record:
  merged-exact-s5-chain-plus-tenthcost-k01k02-20261127.cache,
  sha256
  16b340146fe8a01667ae31fc2f0534a8a3977e56b7c701803d621edc23312ef3,
  6,889 s5verdict rows WIN 207 / LOSS 6,682 (exactly the
  pre-registered shape 6,887+2 / 206+1 / 6,681+1).
- BASE 47280073... (6,887 rows WIN 206 / LOSS 6,681) preserved
  verbatim; 2-row increment (sha256 9a1c672b...): k01
  `1297036692683751424,131074,5,2,6783438` (LOSS) + k02
  `1297036692683751424,131136,5,1,8799140` (WIN); node total
  15,582,578 (bookkeeping).
- Pinned union merger 90711961 (s5_union_merge.py) x3 byte-identical
  (merge-audit-run{1,2,3}.json); duplicates elided 0; WIN/LOSS
  conflict abort active.

## Pillar provenance (all published this session by this lane)

- Replica 15M cold pairs: kit n11-tenthcost-batch-stage1-2m-20261127
  (b8049d8b / completion 3485348c).
- C++ second-implementation scrutiny gate: kit
  n11-tenthcost-k01k02-cppgate-20261127 (55b65a7f), 5/5 GATE-PASS.
- Third-implementation corroboration: kit
  n11-tenthcost-k01k02-thirdimpl-corroboration-20261127 (232a4a52),
  CORROBORATION-PASS verdict-level, plus MANIFEST correction commit
  309ed661 (kit was published without its MANIFEST due to a
  kit-assembly tooling defect; all 6 file shas re-verified against
  the 232a4a52 pinned bytes before the correction push; no raw or
  verdict changed).
- Maker (scripts/make_adoption.py, 3 runs byte-identical): G0 pins
  (merger/policy/quarantine/BASE + all three kit MANIFESTs
  file-by-file), G1 live re-run of the published C++ gate audit
  (rc=0, byte-equal to the published audit JSON), G2 three-pillar
  re-parse per row, G3 freshness 2/2 absent from BASE + WIN/LOSS
  conflict review vs BASE, G4 quarantine-free + canonical-safe per
  s5_evidence_policy, G5 deterministic increment build, G6 merge x3 +
  shape gates.

## Honest disclosures

- The maker's hand-typed QUAR_SHA pin contained a transposition
  (e1aadda4 vs e1aadde4); the G0 pin gate failed closed and the pin
  was re-derived mechanically. No output existed before the first
  PASS run.
- The k02 WIN row may flip owner classes to excluded_now per the
  win-hit mechanism (ninth-cost k12/k02/k07 precedent): the
  flip-census / reaudit refresh review is the NEXT Part, exactly as
  pre-registered in the declaration (ninth precedent: adoption
  6da937d9 then reaudit 55fcc97e). The k01 LOSS row is expected to
  flip nothing. Until that Part is published, no class-status claim
  of any kind is made here.
- The 42 suppressed keys k03..k44 stay 2M-UNKNOWN bookkeeping; the
  tenth-cost ladder is otherwise closed for this batch (2 resolved,
  0 parked at L50M candidates because escalation stopped at the k02
  WIN).
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only. No concurrent-lane
  conflict was observed (main HEAD was this lane's previous commit
  before each push).

## Guards

Adoption is cache bookkeeping only; no root verdict is consumed, no
class freed or excluded, no coverage claim. The standard 11x11 empty
board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root
{60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure
class: UNKNOWN unless a published Part says otherwise. Nodes and
proxy values are never evidence of WIN or LOSS.
