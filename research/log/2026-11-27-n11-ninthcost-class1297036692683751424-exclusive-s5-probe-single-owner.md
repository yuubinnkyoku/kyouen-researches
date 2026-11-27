# 2026-11-27 n11 ninth-cost class 1297036692683751424:134217728 exclusive S5 probe (single-owner declaration)

Wave A declaration of the ninth-cost long-lane Part. The adaptive
coordinator's next selection after the eighth-cost k01 WIN-row canonical
adoption closed the eighth-cost batch (canonical head of record 0935c94c...,
6,875 rows WIN 203 / LOSS 6,672; flip-census + reaudit refresh published at
commits 067394d7 / 229fcf74).

## Selection (head basis, fail-closed, 234 gates)

- Selected class: `1297036692683751424:134217728` (rank 9 of the published
  class-closure-priority table; coverage {35, 41, 100, 108}), the first
  unclaimed live class after the eight claimed classes (focus-35, cert-38,
  third-39, fourth-41, fifth-44, sixth-43, seventh-42, eighth-43).
- 112 S5 children; 99 unknown under the head; 45 exclusive (single-live-
  parent) unknown children; 54 shared; proxy_exclusive_sum 247,541,283;
  bands 5,041,585 x3 / 5,234,938 x24 / 5,932,112 x18.
- Under the CURRENT head there are 58 live active classes (the head
  resolves 1297036692683752448:0 to LOSS-stage and the sixth/seventh/
  eighth-cost serving classes to WIN-stage; the eighth-cost serving class
  therefore cannot be re-selected).
- Selector: `select_ninth_exclusive.py` (fresh structural descendant of the
  published eighth-cost selector, sha256 ac896d94...), pinned to the CURRENT
  canonical head 0935c94c (eighth-cost k01 merged cache) and to all published
  input pins (geometry 146be80b, supply 31f0d29b, ledger 2a4c2382, CCP
  139eb0a0, quarantine 81d23160, p13 cache 60e0dc34, keymap 0aa054c8, fifth
  keys 2d7d3a9d, sixth keys d5e9b059, seventh keys c395fe03, eighth keys
  691dcd80, fifth selector af68af3c, ladder B1 8e530240, ladder B2 d22df157,
  parked-4 inputs). Deterministic: two runs byte-identical (stdout, keys
  JSON, all 45 input CSVs).
- Independent cross-check (same session): a fresh reimplementation that does
  not read the selector source reproduced the class, all 45 keys, the probe
  order, the bands, the proxy sums, the 58-live-class count and all
  disjointness gates exactly (CROSSCHECK-PASS; `crosscheck_ninth.py` in the
  kit, `output/crosscheck-summary.json`).
- Validation gate: jsreplay 84585617 reproduced the published two-target
  expectations node-exact on this host (2M x2 per target: result 0 / nodes
  2,000,000; 15M x2 per target: result 2 / nodes 3,651,923 and 5,040,200);
  8/8 rows pass.

## Execution plan (publish-then-execute, wave C and later)

Per key k01..k45 (ascending truncated-cost proxy, then key): a 2M-budget
cold pair; a node-identical exact-LOSS resolution stops the key; a 2M
UNKNOWN pair escalates to a 15M-budget cold pair; a 15M UNKNOWN pair parks
the key (L50M escalation candidate). WIN stopping rule: no new key is
started after a key resolves WIN(1). All rows are single-implementation
(Node.js replica). A C++ second-implementation scrutiny gate and a
third-implementation corroboration are separate future Parts before any
adoption.

## Honest disclosures

- The selector runs, the independent cross-check and the validation-gate
  runs happened on this host before this wave A publication (the ladder
  raws of wave C are the publish-then-execute payload). Two selector
  adaptation defects (a hand-transcribed EIGHTHKEYS pin sha256 typo and a
  head_basis output-path field pointing at a nonexistent `output/merged/`
  subdirectory) were caught before the first passing run; the fail-closed
  pin gate would have refused the wrong pin independently.
- This lane runs without access to the user's computer (scheduled task);
  publication is via the GitHub API only. Before each push the latest main
  is re-fetched; concurrent-lane conflicts are recorded, not forced.

## Guards

Selection and scheduling only; no verdict is claimed or implied. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every
closure class: UNKNOWN unless a published Part says otherwise. Nodes and
proxy values are never evidence of WIN or LOSS.
