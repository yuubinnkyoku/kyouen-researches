# 2026-11-27 n11 eleventh-cost k01 canonical adoption completion

Completion log of the Part declared at commit 3ee0c6bd.  Kit:
`research/experiments/n11-eleventhcost-k01-win-adoption-20261127/`
(commit 0a9c75e4, 9 files).

## New head of record

- merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache
  sha256 1e2eeda2db33738de99612531f9bb67456f90c81ceedf123c8bbba117aff2a17
  **6,890 rows WIN 208 / LOSS 6,682** - exactly the pre-registered
  shape (6,889+1 / 207+1 / 6,682+0).
- 1-row increment: k01 `1297036696978718720:64` WIN(1) nodes
  12,755,963 (increment sha256 0f627887..., manifest 6442d01d...).

## Maker verification (3 runs byte-identical, MAKER-PASS)

- G0 pins (merger 90711961 / policy 78655e94 / quarantine 81d23160 /
  BASE 16b34014) + the three pillar kit MANIFESTs re-verified from
  byte-clones of the published kits.
- G1 live re-run of the published C++ gate audit: rc=0, output
  byte-equal to the published audit_gate_run1.json.
- G2 re-parse of all three k01 pillars (replica pair, C++ gate pair,
  third-impl pair) - verdict-level WIN(1) everywhere, legal 88.
- G3 freshness (absent from BASE), duplicate check, WIN/LOSS conflict
  review vs BASE (none).
- G4 quarantine-free, canonical-safe.
- G6 merger 3 runs byte-identical (audits e1b50786... x3); merged
  shape exactly as pre-registered.

## Honest disclosures

- The maker's G4 quarantine lookup needed the policy script's
  hardcoded registry path (/home/results/...); the pinned quarantine
  file was staged there byte-identically.
- The replica, C++ gate and third-impl results this adoption consumes
  were produced and published earlier this session by this same lane.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Next work

- Flip-census/reaudit review of the serving class
  `1297036696978718720:0` owner set (BASE 16b34014 vs SCEN 1e2eeda2;
  SZ/EM/ninth/tenth precedent, measurer + refresh byte-clone).
- Next selection (twelfth cost) under the new head 1e2eeda2 with the
  fresh selector lineage (eleventh selector 431e3f55 as the next
  template; the eleventh serving class 1297036696978718720:0 is
  excluded_now under the new head and cannot be re-selected).
- The 45 suppressed keys (k02..k46) stay 2M-UNKNOWN bookkeeping.

## Guards

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO class excluded.  The standard 11x11 empty board: UNKNOWN.
All 19 central-reply roots: UNKNOWN.  Two-stone root {60,27}:
UNKNOWN.  Third-move pair {100,108}: UNKNOWN.  Nodes are bookkeeping,
never verdicts.
