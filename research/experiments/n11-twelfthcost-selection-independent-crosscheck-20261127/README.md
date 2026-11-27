# n11 twelfth-cost selection: independent cross-check (CROSSCHECK-PASS)

Independent second-implementation cross-check of the published twelfth-cost
selection kit `n11-twelfthcost-class-s5-exclusive-probe-20261127` (commit
`e588de1e`, selector `select_twelfth_exclusive.py` sha256 `ea2b8331...`,
authoritative list `twelfth-cost-exclusive-keys.json` sha256 `1119d01b...`).
The concurrent lane that declared the twelfth-cost batch stage-1 sweep
(declaration commit `f6d29d16`) is unaffected: this kit only re-derives the
SELECTION; no probe of any twelfth-cost key was executed here.

## Method (selector source NOT read, NOT executed)

`scripts/crosscheck_twelfth_selection.py` (sha256 `9078ac44...`) is a fresh
Python reimplementation. It re-derives the selection from the underlying
frozen data only:

- geometry `n11-strategy-redesign-20261010/output/geometry.json.gz`
  (sha256 `146be80b...100b54`; the parent map is rebuilt from the 3,384
  classes x 367,228 child edges, never from the selector),
- probe-13 post-probe candidate ledger `candidate-classes.csv`
  (`2a4c2382...da80`, 115 classes: 62 UNKNOWN / 53 WIN),
- probe-13 post-probe supply `shared-s5-tasks.csv` (`31f0d29b...ea954`,
  4,562 rows: legal + truncated-cost proxy per key),
- published priority table `class-closure-priority.csv` (62 rows),
- probe-13 base cache `merged-exact-s5-after-js-probe-13.cache`
  (`60e0dc34...bc28c6`),
- canonical head of record `merged-exact-s5-chain-plus-eleventhcost-k01-
  20261127.cache` (sha256 `1e2eeda2...`, 6,890 rows WIN 208 / LOSS 6,682),
- the 14 published concurrent claim key lists + `results/n11-s5-evidence-
  quarantine.json` (`81d23160...17fe9`, 2 entries).

Definitions were fixed and CALIBRATED before any head-side comparison:

- calibration-1: the independent live-parent rule (candidate class with
  probe-13 status UNKNOWN, parents taken from the geometry parent map)
  reproduces the published supply `live_parent_keys` column for ALL 4,562
  supply rows with 0 mismatches;
- calibration-2: under the probe-13 base cache the re-derivation reproduces
  the published priority row of the selected class exactly:
  114 children / 101 unknown / 44 exclusive / 57 shared, proxy_total
  571,078,241, proxy_exclusive_sum 252,985,393, proxy_shared_sum 318,092,848.

Win-hit exclusion under the head (the rule the adoption flip-census parts
measure): a parent class is excluded when it owns a WIN row of the cache.

## Result (CROSSCHECK-PASS, rc=0, 3 runs byte-identical)

- class `10376293541461626880:16777216` (rank 12, 0-based index 11 of the
  published priority table): the top-11 rows are exactly the 11 claimed
  serving classes (focus-35 / cert-38 / third-39 / fourth-41 / fifth-44 /
  sixth-43 / seventh-42 / eighth-43 / ninth-45 / tenth-44 / eleventh-46);
  the class is live (not win-hit excluded) under the head; the eleventh-cost
  serving class `1297036696978718720:0` is excluded_now, so it cannot be
  re-selected.
- re-derived under head `1e2eeda2...`: 114 children, 100 unknown before
  head, 51 exclusive / 49 shared, proxy_exclusive_sum_head 293,115,829,
  bands 5,041,585 x 1 / 5,069,670 x 1 / 5,234,938 x 11 / 5,932,112 x 38.
- the re-derived 51-entry list (key, legal, proxy, ordering = ascending
  truncated-cost proxy then key id/mask) is EXACTLY EQUAL, entry by entry,
  to the published `exclusive_probe_order`.
- freshness: all 51 keys absent from the head (51/51).
- claim disjointness: 14/14 published claim sets (focus_35, cert_38,
  third_39, fourth_41, fifth_44, sixth_43, seventh_42, eighth_43, ninth_45,
  tenth_44, eleventh_46, sbd_101, parked_2, parked_4) have empty intersection
  with the 51 keys.  sbd_101 = the 101 targets of
  `n11-s4bd-fresh-corpus-regen-20261121/input/keymap.json`; parked_2/parked_4
  = the claimed_keys of the published L50M ladder halt-audits.
- quarantine absent (2-entry registry, no overlap).
- input CSVs: all 51 published `input/kNN.input.csv` byte-verified against
  the kit MANIFEST and their target/legal fields re-checked against the
  re-derived list (51/51).

## Fail-closed battery (5/5 fail-closed; clean control re-PASS byte-identical)

- T1 published-list key flip -> order-difference gate, rc=1
- T2 phantom row appended to the head cache -> head-shape gate, rc=1
- T3 sixth-claim overlap injection -> claim-disjointness gate, rc=1
- T4 input-CSV legal flip -> csv legal gate, rc=1
- T5 supply proxy +1000 on a selected key -> proxy sum/bands gate, rc=1

## Honest disclosures

- T5's first attempt was a harness no-op (the tampering one-liner raised
  NameError before writing, so the run correctly stayed rc=0); the tamper
  was re-applied with a verified 1-row write and then detected.  No gate
  ever passed a tampered input.
- The frozen inputs are not republished in this kit (size policy): they are
  sha256-pinned above and re-downloadable from the repo paths given.
- This lane runs without access to the user's computer (scheduled task);
  publication is via the GitHub API only.  Before the push the latest main
  is re-fetched; concurrent-lane conflicts are recorded, not forced.
- A full-repo tarball download was attempted once for input reconstruction
  and abandoned (too slow); inputs were then fetched individually from the
  raw CDN with sha256 verification.

## Meaning and non-meaning

Scheduling cross-check only: NO verdict is claimed or implied.  Nodes and
proxy values are never evidence of WIN or LOSS.  The standard 11x11 empty
board: UNKNOWN.  All 19 central-reply roots: UNKNOWN.  The two-stone root
{60,27} and its remaining third moves 100/108: UNKNOWN.  The concurrent
twelfth-cost batch stage-1 sweep (single-owner declaration f6d29d16) keeps
full ownership of the probe execution, its raws, and any escalation.
