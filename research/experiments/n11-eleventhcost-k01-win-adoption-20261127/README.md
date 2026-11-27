# n11-eleventhcost-k01-win-adoption-20261127

Eleventh-cost k01 WIN row canonical adoption kit.  Declared in
research/log/2026-11-27-n11-eleventhcost-k01-adoption-declaration.md
(commit 3ee0c6bd, publish-then-execute).  The canonical head of
record advances from merged-exact-s5-chain-plus-tenthcost-k01k02
(sha256 16b34014..., 6,889 rows WIN 207 / LOSS 6,682) by consuming
exactly the one published eleventh-cost resolved row.

## New head of record

- merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache
  sha256 1e2eeda2db33738de99612531f9bb67456f90c81ceedf123c8bbba117aff2a17
  **6,890 rows WIN 208 / LOSS 6,682** - exactly the pre-registered
  shape 6,889+1 / 207+1 / 6,682+0.
- Increment (1 row): k01 `1297036696978718720:64` WIN(1) nodes
  12,755,963 (bookkeeping).  Increment sha256 0f627887....

## Maker verification (3 runs byte-identical)

- G0 pins: merger 90711961..., policy 78655e94..., quarantine
  81d23160..., BASE 16b34014... + the three pillar kit MANIFESTs
  fully re-verified from local byte-clones of the published kits
  (replica kit aaeb282c, cppgate kit 25cef9e9, thirdimpl kit
  26c7b04d).
- G1: live re-run of the published C++ gate audit rc=0, output
  byte-equal to the published audit_gate_run1.json (AUDIT-PASS,
  head 16b34014).
- G2: re-parse of all three pillars for k01 (replica 15M cold pair
  quad `88,15000000,1,12755963`; C++ gate pair node-exact;
  third-impl pair result 1, reason clean, legal 88).
- G3: freshness (k01 absent from BASE), duplicate-key check,
  WIN/LOSS conflict review vs BASE (none).
- G4: quarantine-free and canonical-safe per s5_evidence_policy.
- G6: merger 3 runs byte-identical with audits; merged shape exactly
  as pre-registered.

## Files

- scripts/make_adoption.py - the fresh maker (machine-derived
  structural adaptation of the published tenth-cost adoption maker
  c153f6f2...: single-row ROWS with per-row legal, eleventh-cost kit
  paths/commits, BASE/OUT shapes, increment/merged filenames).
- output/increment-eleventhcost-k01-adoption-20261127.cache - the
  1-row increment (with provenance comment block).
- adoption-manifest.json - schema
  n11-eleventhcost-k01-win-adoption-manifest-v1.
- output/merged/merged-exact-s5-chain-plus-eleventhcost-k01-20261127.cache
  - the new canonical head of record (byte-copy of merger run1; runs
  1-3 byte-identical).
- output/merged/merge-audit-run{1,2,3}.json - the three merger
  audits (byte-identical).

## Honest disclosures

- The maker's G4 quarantine lookup required the policy script's
  hardcoded registry path (/home/results/n11-s5-evidence-quarantine.json);
  the pinned quarantine file (81d23160...) was staged at that path on
  this host (byte-identical copy, disclosed).
- The replica, C++ gate and third-impl results this adoption consumes
  were produced and published earlier this session by this same lane.
- The flip-census/reaudit review of the serving class
  1297036696978718720:0 owner set is the next follow-up Part
  (SZ/EM/ninth/tenth precedent).
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Guards

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO class excluded.  The adopted row is cache bookkeeping.  The
standard 11x11 empty board: UNKNOWN.  All 19 central-reply roots:
UNKNOWN.  Two-stone root {60,27}: UNKNOWN.  Third-move pair
{100,108}: UNKNOWN.  Nodes are bookkeeping, never verdicts.
