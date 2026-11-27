# n11-tenthcost-k01k02-adoption-20261127

Canonical adoption kit of the two resolved tenth-cost rows (k01
LOSS, k02 WIN of class 1297036692683751424:131072). Declared in
research/log/2026-11-27-n11-tenthcost-k01k02-adoption-declaration.md
(commit fecb961a, publish-then-execute; pre-registered merged shape
6,889 rows WIN 207 / LOSS 6,682).

## Head of record advance

- BASE: merged-exact-s5-chain-plus-ninthcost12-20261127.cache,
  sha256 47280073... (6,887 rows WIN 206 / LOSS 6,681), re-verified.
- increment-tenthcost2-adoption-20261127.cache (sha256 9a1c672b...):
  exactly 2 fresh rows, k01 `1297036692683751424,131074,5,2,6783438`
  and k02 `1297036692683751424,131136,5,1,8799140` (nodes
  bookkeeping, total 15,582,578).
- merged-exact-s5-chain-plus-tenthcost-k01k02-20261127.cache, sha256
  16b34014... : 6,889 rows WIN 207 / LOSS 6,682, exactly the
  pre-registered shape, produced by the pinned union merger
  90711961 (s5_union_merge.py) x3 byte-identical
  (output/merged/merge-audit-run{1,2,3}.json).
- The 6,887 BASE rows are preserved verbatim; duplicates elided 0;
  WIN/LOSS conflict abort active (fail-closed).

## Maker gates (scripts/make_adoption.py, 3 runs byte-identical)

- G0 pins: merger 90711961..., policy 78655e94..., quarantine
  81d23160..., BASE 47280073... sha-verified; all three pillar kits
  re-verified file-by-file against their published
  MANIFEST-sha256.txt (replica b8049d8b, C++ gate 55b65a7f,
  third-impl 232a4a52 + MANIFEST correction 309ed661).
- G1: the published C++ gate audit re-run LIVE from the published
  kit's own scripts/audit_gate.py: rc=0 and output byte-equal to the
  published audit_gate_run1.json.
- G2: re-parse of all three pillars per row: replica 15M cold pairs
  node-identical with quad (legal,budget,result,nodes) == expected;
  C++ gate raws node-identical with the same quad; third-impl results
  agree (k01 LOSS(2), k02 WIN(1)), cold pairs identical, reason clean.
- G3: freshness: both keys absent from BASE; duplicate-key gate;
  WIN/LOSS conflict review vs BASE.
- G4: quarantine-free and canonical-safe per the pinned
  s5_evidence_policy (both keys PASS, machine-checked).
- G5: deterministic increment + adoption-manifest build.
- G6: merger x3 byte-identical + merged shape gates (6,889 / 207 /
  6,682).

## Honest disclosures

- The third-impl corroboration kit (232a4a52) was published without
  its MANIFEST-sha256.txt due to a kit-assembly tooling defect (same
  class as the ninth k12 stale-MANIFEST precedent); the MANIFEST was
  published as correction commit 309ed661 with all 6 file shas
  re-verified against the 232a4a52 pinned bytes before the push. No
  raw or verdict changed.
- The maker's QUAR_SHA constant initially contained a hand-typed
  transposition (e1aadda4 vs e1aadde4); the G0 pin gate failed
  closed and the pin was re-derived mechanically. No output existed
  before the first PASS run.
- The maker script records this lane's work-tree layout (paths
  relative to the script's directory); all inputs are pinned and
  re-derivable from the published kits via their MANIFESTs.
- All three pillar kits were produced and published earlier this
  session by this same lane (declaration 8e60224f / b8049d8b /
  3485348c / 55d4a33a / 232a4a52 / 506c5f16 / 55b65a7f).
- The flip-census / reaudit refresh review for the k02 WIN row
  (win-hit owner-class flips, ninth-cost k12/k02/k07 precedent) is a
  SEPARATE follow-up Part, exactly as in the ninth-cost batch
  (adoption 6da937d9 then reaudit 55fcc97e). The k01 LOSS row is
  expected to flip nothing.
- The 42 suppressed keys k03..k44 stay 2M-UNKNOWN bookkeeping and are
  NOT adopted by this Part.

## Meaning and non-meaning

Adoption is cache bookkeeping only: no root verdict is consumed, no
class is freed or excluded, no coverage claim is made. The standard
11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN.
Every closure class: UNKNOWN unless a published Part says otherwise.
Nodes are never evidence of WIN or LOSS.
