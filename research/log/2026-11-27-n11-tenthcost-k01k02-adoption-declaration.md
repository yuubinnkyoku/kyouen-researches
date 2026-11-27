# 2026-11-27 n11 tenth-cost k01/k02 canonical adoption: wave A declaration

Single-owner declaration of the canonical adoption Part for the two
resolved tenth-cost batch rows. Both rows have all three
implementation pillars published:

- replica stage-2 15M cold pairs (kit
  n11-tenthcost-batch-stage1-2m-20261127, commits b8049d8b / 3485348c)
- C++ second-implementation scrutiny gate 5/5 GATE-PASS (kit
  n11-tenthcost-k01k02-cppgate-20261127, commit 55b65a7f)
- third-implementation corroboration CORROBORATION-PASS (kit
  n11-tenthcost-k01k02-thirdimpl-corroboration-20261127, commit
  232a4a52).

## Adopted rows (2)

- k01 `1297036692683751424:131074`: LOSS(2), nodes 6,783,438
  (bookkeeping).
- k02 `1297036692683751424:131136`: WIN(1), nodes 8,799,140
  (bookkeeping).

## Pre-registered merged shape

BASE = canonical head of record
merged-exact-s5-chain-plus-ninthcost12-20261127.cache, sha256
47280073... (6,887 rows WIN 206 / LOSS 6,681). The 2-row increment
merges to exactly 6,889 rows, WIN 207 / LOSS 6,682, by the pinned
union merger 90711961 (s5_union_merge.py). Freshness: both keys are
absent from BASE (machine-checked at kit assembly and by the maker's
fail-closed gates); WIN/LOSS conflict review is the merger's
fail-closed conflict abort plus the maker's re-parse gates;
quarantine-free and canonical-safe per s5_evidence_policy (sha
78655e94) and the quarantine registry (sha 81d23160) on this host.

## Honest disclosures

- All three pillar kits were produced and published earlier this
  session by this same lane; the maker re-verifies their published
  bytes (sha256 against each kit's published MANIFEST-sha256.txt) and
  re-runs the published C++ gate audit live before building the
  increment.
- The flip-census / reaudit refresh review (the k02 WIN row may flip
  owner classes to excluded_now per the win-hit mechanism, ninth-cost
  k12/k02/k07 precedent) is a SEPARATE follow-up Part after this
  adoption, exactly as in the ninth-cost batch (adoption 6da937d9 then
  reaudit 55fcc97e). The k01 LOSS row is expected to flip nothing.
- The 42 suppressed keys k03..k44 stay 2M-UNKNOWN bookkeeping and are
  NOT adopted by this Part.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only. Before each push the
  latest main is re-fetched; concurrent-lane conflicts are recorded,
  not forced.

## Guards

Adoption is cache bookkeeping only; no root verdict is consumed, no
class freed or excluded. The standard 11x11 empty board: UNKNOWN. All
19 central-reply roots: UNKNOWN. Two-stone root {60,27}: UNKNOWN.
Third-move pair {100,108}: UNKNOWN. Every closure class: UNKNOWN
unless a published Part says otherwise. Nodes are never evidence.
