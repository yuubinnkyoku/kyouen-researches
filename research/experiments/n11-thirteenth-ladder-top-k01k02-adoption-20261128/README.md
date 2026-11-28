# n11 thirteenth ladder-top class-16757 k01+k02 canonical adoption

Execution kit of the Part declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-k01k02-adoption-declaration.md`
(commit `5cb113c5`, single owner, publish-then-execute): the canonical
adoption of the two thirteenth ladder-top WIN rows into the head of
record.

## Results (MAKER-PASS x2 byte-identical)

- **New head of record:
  `merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache`
  sha256 `d772f73c68bf051e7b90e5cd6cfef2a7b1c8e07da888c5f728f7a04b39edd1ec`,
  6,896 rows WIN 214 / LOSS 6,682** - exactly the pre-registered
  shape (BASE `beecb024...` 6,894 rows WIN 212 / LOSS 6,682 + 2 fresh
  WIN rows).
- Increment: 2 WIN rows, sha256 `cebd8dc9...`
  (`output/increment-thirteenth-k01k02-adoption-20261128.cache`);
  adopted node total 6,163,868 (bookkeeping).
- Manifest: `adoption-manifest.json` (schema
  n11-thirteenth-ladder-top-k01k02-win-adoption-manifest-v1).
- Merger `90711961...` x3 byte-identical (merge-audits in
  `output/merged/`).

## Gates (all PASS, fail-closed; maker x2 byte-identical)

G0 pins (merger/policy/quarantine/BASE head/gate source+headers) +
published-kit MANIFEST self-verification of all 6 source kits (both
escalation kits, both cppgate kits, both thirdimpl kits); G1 LIVE
re-run of BOTH published gate_runner.sh instances on scratch kit
copies (4 fresh-cold C++ passes total, node-exact vs the published
raws, `72,15000000,1,2678305` and `72,15000000,1,3485963`); G2
six-pillar re-parse (both replica pairs, both C++ gate pairs, both
third_impl pairs + summary cross-checks, verdict/legal/key/expansions
checks); G3 freshness (both keys absent from BASE) + no duplicates +
no WIN/LOSS conflicts; G4 quarantine-free + canonical-safe per
s5_evidence_policy; G5 increment build; G6 merger x3 + shape check.
Both maker runs (post-declaration) produced byte-identical outputs
(merged sha256 x2, kitout byte-identical by recursive hash).

## Honest disclosures

- The gate binary was rebuilt from the pinned source `9193f5b6...`
  (zig 0.13.0, tarball pin `d45312e6...`) in this execution
  environment; the live gate re-runs re-verified both target rows
  node-exact against the published raws (G1).  This same binary
  already produced the two XHOST-PASS replication kits (`eb542121`,
  `8cc714bf`, this lane).
- First maker invocation died fail-closed on a pin-typo in
  `n11_s5_quarantine.hpp`'s full sha (no output written); fixed and
  re-run, disclosed here.
- **Known source-kit defect (disclosed in the declaration before
  execution): the published k02 cppgate kit's MANIFEST-sha256.txt
  contains a self-referential `MANIFEST-sha256.txt` line** (a
  manifest cannot contain its own sha256; its value does not match
  the file).  The maker excludes that single line from verification;
  all 19 other lines verify.  Owner-lane fix is a future cosmetic
  repair, recorded here.
- Only the 2 declared rows are adopted; nothing else is written.

## Follow-up Part (declared)

The WIN-side flip-census review (BASE `beecb024` -> SCEN `d772f73c`
measurement): owner-union prediction pre-registered in
`n11-thirteenth-owner-union-precheck-20261128` (`fdb704d7`) -
combined owner union [16612, 16740, 16757, 30542]; serving class 16757
leaves the 800-row closure ladder (unknown_now 2 -> 0); u03
pre-exclusion and u04 zero-churn caveats recorded there; measurement
replaces prediction.  Class 16757 completion additionally requires
Board-verified free_now at adoption time.

## Files

- adoption-manifest.json - machine manifest.
- output/increment-thirteenth-k01k02-adoption-20261128.cache - the
  2-row increment.
- output/merged/merged-exact-s5-chain-plus-thirteenth-k01k02-20261128.cache
  - the new head of record (288,866 B).
- output/merged/merge-audit-run{1,2,3}.json - merger audits.
- scripts/make_adoption_thirteenth.py - the maker (fresh structural
  descendant of the u04 adoption maker, sha-verified pins, fail-closed
  gates).
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Adoption bookkeeping only: the 2 adopted rows are cache bookkeeping,
NOT a class closure, NOT a root verdict, and transfer nothing.  The
standard 11x11 empty board, the 19 central-reply roots, the two-stone
root {60,27} and its remaining third moves {100,108} stay UNKNOWN.
Nodes are bookkeeping, never verdicts.
