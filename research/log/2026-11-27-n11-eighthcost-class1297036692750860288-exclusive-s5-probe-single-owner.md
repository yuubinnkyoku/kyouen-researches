# 2026-11-27 n11 eighth-cost class 1297036692750860288:0 exclusive S5 probe (single-owner declaration)

Wave A declaration of the eighth-cost long-lane Part. The adaptive
coordinator's next selection after the Part SZ canonical adoption closed the
seventh-cost batch (42 rows adopted, canonical head of record 5b6e77f7...,
6,874 rows WIN 202 / LOSS 6,672; Part SZ reaudit census published at commit
2d3c43f1).

## Selection (head basis, fail-closed, 220 gates)

- Selected class: `1297036692750860288:0` (rank 8 of the published
  class-closure-priority table; coverage {46, 52, 100, 108}), the first
  unclaimed live class after the seven claimed classes (focus-35, cert-38,
  third-39, fourth-41, fifth-44, sixth-43, seventh-42).
- 108 S5 children; 100 unknown under the head; 43 exclusive (single-live-
  parent) unknown children; 57 shared; proxy_exclusive_sum 233,896,005;
  bands 5,041,585 x5 / 5,234,938 x24 / 5,932,112 x14.
- Selector: `select_eighth_exclusive.py` (fresh structural descendant of the
  published seventh-cost selector, sha256 ac896d94...), pinned to the
  CURRENT canonical head 5b6e77f7 (Part SZ merged seventhcost42 cache) and
  to all 17 published input pins (geometry 146be80b, supply 31f0d29b,
  ledger 2a4c2382, CCP 139eb0a0, quarantine 81d23160, p13 cache 60e0dc34,
  keymap 0aa054c8, fifth keys 2d7d3a9d, sixth keys d5e9b059, seventh keys
  c395fe03, fifth selector af68af3c, ladder B1 8e530240, ladder B2 d22df157,
  jsreplay 84585617, parked-4 inputs). Deterministic: two runs
  byte-identical (stdout, keys JSON, all 43 input CSVs).
- Independent cross-check (same session): a fresh reimplementation that does
  not read the selector source reproduced the class, all 43 keys, the probe
  order, the bands, the proxy sums and all disjointness gates exactly
  (CROSSCHECK-PASS).
- Validation gate: jsreplay 84585617 reproduced the published two-target
  expectations node-exact on this host (2M x2: result 0 / nodes 2,000,000
  for both targets; 15M x2: result 2 / nodes 3,651,923 and 5,040,200).

## Execution plan (publish-then-execute, wave C and later)

Per key k01..k43 (ascending truncated-cost proxy): a 2M-budget cold pair; a
node-identical exact-LOSS resolution stops the key; a 2M UNKNOWN pair
escalates to a 15M-budget cold pair; a 15M UNKNOWN pair parks the key (L50M
escalation candidate). WIN stopping rule: no new key is started after a key
resolves WIN(1). All rows are single-implementation (Node.js replica).
The C++ second-implementation scrutiny gate and a third-implementation
corroboration are separate future Parts before any adoption; the pre-audit
ladder instrument must gain the eighth-cost ledger pin before reuse.

## Honest disclosures

- The selector runs, the independent cross-check and the validation-gate
  runs happened on this host before this wave A publication (the ladder
  raws of wave C are the publish-then-execute payload). One selector
  adaptation defect (a corrupted SEVENTHKEYS pin path) was caught by the
  selector's own fail-closed pin gate before any output existed and fixed.
- This lane runs without access to the user's computer (scheduled task);
  publication is via the GitHub API only. Before each push the latest main
  is re-fetched; concurrent-lane conflicts are recorded, not forced.

## Guards

Selection and scheduling only; no verdict is claimed or implied. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every
closure class: UNKNOWN unless a published Part says otherwise. Nodes and
proxy values are never evidence of WIN or LOSS.
