# n11-ultra-cheap-u01-win-adoption-20261127

Ultra-cheap u01 WIN row canonical adoption kit.  Declared in
research/log/2026-11-27-n11-ultra-cheap-u01-adoption-declaration.md
(commit `7fe17f62`, publish-then-execute).  The canonical head of
record advances from merged-exact-s5-chain-plus-eleventhcost-k01
(sha256 `1e2eeda2...`, 6,890 rows WIN 208 / LOSS 6,682) by consuming
exactly the one published ultra-cheap batch resolved row.

## New head of record

- merged-exact-s5-chain-plus-ultra-cheap-u01-20261127.cache
  sha256 `0ec4080da825a344a8dbbe0835da80dd506b06fa45f9f926b401d2387f3ed1e5`
  **6,891 rows WIN 209 / LOSS 6,682** - exactly the pre-registered
  shape 6,890+1 / 208+1 / 6,682+0.
- Increment (1 row): u01 `1153485622925590528:0` WIN(1) nodes
  4,893,014 (bookkeeping).  Increment sha256 `5d2d89dd...`.

## Maker verification (3 runs byte-identical, MAKER-PASS x3)

- G0 pins: merger `90711961...`, policy `78655e94...`, quarantine
  `81d23160...`, BASE `1e2eeda2...`, gate source `9193f5b6...` +
  headers `5976935d...`/`2e36d694...`; both source kit MANIFESTs fully
  re-verified from byte-fetched copies (replica kit
  n11-ultra-cheap-batch-stage1-2m-20261127, pillars kit
  n11-ultra-cheap-u01-win-pillars-20261127).
- G1 (adapted, disclosed): LIVE re-run of the published gate_runner.sh
  on a scratch copy of the pillars kit (2 fresh-cold C++ passes,
  quadruple `88,15000000,1,4893014`, raw node-exact vs published);
  binary provenance by this-session build from the sha-pinned source
  (zig 0.13.0 `d45312e6...`, -std=c++20 -O3) plus the live re-run.
- G2: re-parse of all three pillars for u01 (replica 15M cold pair
  quad `88,15000000,1,4893014`; C++ gate pair node-exact; third-impl
  pair result 1, reason clean, legal 88).
- G3: freshness (u01 absent from BASE), duplicate-key check,
  WIN/LOSS conflict review vs BASE (none).
- G4: quarantine-free and canonical-safe per s5_evidence_policy.
- G6: merger 3 runs byte-identical with audits; merged shape exactly
  as pre-registered.

## Files

- scripts/make_adoption.py - the fresh maker (structural descendant of
  the published eleventh-cost k01 adoption maker).
- output/increment-ultra-cheap-u01-adoption-20261127.cache - the 1-row
  increment (with provenance comment block).
- adoption-manifest.json - schema
  n11-ultra-cheap-u01-win-adoption-manifest-v1.
- output/merged/merged-exact-s5-chain-plus-ultra-cheap-u01-20261127.cache
  - the new canonical head of record (byte-copy of merger run1; runs
  1-3 byte-identical).
- output/merged/merge-audit-run{1,2,3}.json - the three merger audits
  (byte-identical).
- MANIFEST-sha256.txt - sha256 of every file in this kit.

## Honest disclosures

- The maker's G4 quarantine lookup required the policy script's
  parents[4]-relative registry path; the pinned quarantine file
  (`81d23160...`) was staged at that path in the work tree
  (byte-identical copy, disclosed).
- The G1 live gate re-run is this lane's adaptation of the eleventh
  G1 (live audit re-run): this lane's pillar kit ships the runner +
  raws + tamper battery instead of a separate audit script.
- The replica, C++ gate and third-impl results this adoption consumes
  were produced and published earlier this session by this same lane.
- The flip-census/reaudit review of class 1849 (the u01 WIN row's
  owner class, expected to close under the head) is the next
  follow-up Part (SZ/ninth/tenth/eleventh precedent).
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Guards

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO class excluded.  Nodes are bookkeeping, never verdicts.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.
