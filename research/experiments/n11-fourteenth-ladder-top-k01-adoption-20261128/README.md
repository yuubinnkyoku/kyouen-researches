# n11 fourteenth ladder-top class-5804 k01 canonical adoption

Execution kit of the Part declared in
`research/log/2026-11-28-n11-fourteenth-ladder-top-k01-adoption-declaration.md`
(commit `d5eaaba6`, single owner, publish-then-execute): the canonical
adoption of the fourteenth ladder-top k01 WIN row into the head of
record.

## Results (MAKER-PASS x2 byte-identical)

- **New head of record:
  `merged-exact-s5-chain-plus-fourteenth-k01-20261128.cache`
  sha256 `a66f636ed4314b7385b713ed6e24798409db0b284eb252a9bda626ad3dcd67dc`,
  6,897 rows WIN 215 / LOSS 6,682** - exactly the pre-registered
  shape (BASE `d772f73c...` 6,896 rows WIN 214 / LOSS 6,682 + 1
  fresh WIN row).
- Increment: 1 WIN row, sha256 `c87d9afb...`
  (`output/increment-fourteenth-k01-adoption-20261128.cache`);
  adopted node total 4,360,661 (bookkeeping).
- Manifest: `adoption-manifest.json` (schema
  n11-fourteenth-ladder-top-k01-win-adoption-manifest-v1).
- Merger `90711961...` x3 byte-identical (merge-audits in
  `output/merged/`).

## Gates (all PASS, fail-closed; maker x2 byte-identical)

G0 pins (merger/policy/quarantine/BASE head/gate source+headers) +
published-kit MANIFEST self-verification of all 3 source kits
(escalation kit `5c670bc6`, cppgate kit, thirdimpl kit, 0
self-referential manifest lines each); G1 LIVE re-run of the
published gate_runner.sh on a scratch kit copy (fresh-cold C++
pair, node-exact vs the published raw, `86,15000000,1,4360661`);
G2 three-pillar re-parse (replica pair + C++ gate pair + third_impl
pair + summary cross-checks, verdict/legal/key/expansions checks);
G3 freshness (key absent from BASE) + no WIN/LOSS conflicts; G4
quarantine-free + canonical-safe per s5_evidence_policy; G5
increment build; G6 merger x3 + shape check.  Both maker runs
(post-declaration) produced byte-identical kit outputs (kitout
recursive-diff clean).  Tamper battery 4/4 fail-closed (T1 BASE pin
digit flip, T2 replica raw nodes edit caught by the kit MANIFEST
gate, T3 third-impl expansions pin drift, T4 quarantine-key
injection with re-pinned registry sha - all stopped before any
output) + clean control re-PASS.

## Honest disclosures

- The gate binary was rebuilt from the pinned source `9193f5b6...`
  (zig 0.13.0, tarball pin `d45312e6...`) in this execution
  environment; it is the same binary that produced the published
  fourteenth cppgate kit GATE-PASS this session.  The live gate
  re-run re-verified the target row node-exact against the
  published raw (G1).
- The maker is a fresh structural descendant of the published
  thirteenth adoption maker `3600ce8a...` (single-row adaptation;
  the policy module lives at a 4-deep scratch path
  `pol/w/x/y/s5_evidence_policy.py` so its parents[4] registry
  lookup resolves to `results/n11-s5-evidence-quarantine.json`,
  mirroring the thirteenth maker's `a/b/c/d/` arrangement).
- The published merger `90711961...` and policy `78655e94...` were
  byte-fetched from their published kit locations and sha-verified
  before use.
- Unlike the thirteenth adoption, no cross-host replication kit
  exists for this row yet; the three-implementation pillar
  agreement plus this host's live gate re-run are the standing
  evidence (declared up front).
- Only the 1 declared row is adopted; nothing else is written.

## Follow-up Part (declared)

The WIN-side flip-census review (BASE `d772f73c` -> SCEN
`a66f636e` measurement, owner-union prediction [5308, 5804, 8811]
from `n11-fourteenth-owner-union-precheck-20261128` (`509afbdb`)):
serving class 5804 stays in the 799-row closure ladder (unknown_now
4 -> 3, NOT a ladder exit); owner 8811 is itself a ladder row
(rank 17) whose census status must be measured.  Class 5804
completion additionally requires k02/k03/k04 (still 2M UNKNOWN)
and Board-verified free_now at adoption time.

## Files

- adoption-manifest.json - machine manifest.
- output/increment-fourteenth-k01-adoption-20261128.cache - the
  1-row increment.
- output/merged/merged-exact-s5-chain-plus-fourteenth-k01-20261128.cache
  - the new head of record (288,910 B).
- output/merged/merge-audit-run{1,2,3}.json - merger audits.
- scripts/make_adoption_fourteenth.py - the maker (fresh structural
  descendant of the thirteenth adoption maker, sha-verified pins,
  fail-closed gates).
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Adoption bookkeeping only: the adopted row is cache bookkeeping,
NOT a class closure, NOT a root verdict, and transfers nothing.
The standard 11x11 empty board, the 19 central-reply roots, the
two-stone root {60,27} and its remaining third moves {100,108}
stay UNKNOWN.  Nodes are bookkeeping, never verdicts.
