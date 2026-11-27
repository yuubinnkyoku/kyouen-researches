# 2026-11-27 n11 eleventh-cost class 1297036696978718720:0 exclusive S5 probe batch (single-owner declaration)

Wave A declaration of the eleventh-cost long-lane Part. The adaptive
coordinator's next batch after the tenth-cost 2-row canonical adoption
closed the tenth-cost batch (canonical head of record 16b34014...,
6,889 rows WIN 207 / LOSS 6,682; flip-census + reaudit refresh published
at commits a50dc1af / 31b6d110).

## Selection (published, fail-closed, 246 gates; commits 56787fe0 / f8dd2c81)

- Selected class: `1297036696978718720:0` (rank 11 of the published
  class-closure-priority table; coverage third moves {100, 108, 112, 118}),
  the first unclaimed live class after the ten claimed classes
  (focus-35, cert-38, third-39, fourth-41, fifth-44, sixth-43,
  seventh-42, eighth-43, ninth-45, tenth-44).
- Re-validated against the CURRENT canonical head 16b34014...: 108 S5
  children; 102 unknown before head; 46 exclusive (single-live-parent)
  unknown children; 56 shared; proxy_exclusive_sum 249,214,113; bands
  5,041,585 x7 / 5,234,938 x25 / 5,932,112 x14. The tenth-cost serving
  class 1297036692683751424:131072 is excluded_now under the head,
  so it cannot be re-selected.
- Authoritative selection list: output/eleventh-cost-exclusive-keys.json
  (schema n11-eleventhcost-exclusive-selection-v1, sha256 5a29b5be...,
  46 keys; first 1297036696978718720:64, last
  10376293541465821184:268435456). Selector select_eleventh_exclusive.py
  (sha256 431e3f55...), jsreplay byte-clone 84585617..., input CSVs
  k01..k46 generated and cross-checked against the shared-s5 supply.
- Disjointness of the 46 keys from all thirteen published claim sets
  (focus/cert/third/fourth/fifth/sixth/seventh/eighth/ninth/tenth,
  sbd-101, parked-2, parked-4) is machine-gated inside the selector;
  head freshness (all 46 absent from head 16b34014) is machine-gated.

## Execution plan (publish-then-execute; wave B publishes the raws)

Per key k01..k46 (ascending truncated-cost proxy, then key): a
2,000,000-budget cold pair with the published jsreplay 84585617 under
the published input CSVs. A node-identical exact-LOSS resolution stops
the key; a 2M UNKNOWN pair escalates to a 15M-budget cold pair; a 15M
UNKNOWN pair parks the key (L50M escalation candidate). WIN stopping
rule: no new key is started after a key resolves WIN(1). All rows are
single-implementation (Node.js replica); a C++ second-implementation
scrutiny gate and a third-implementation corroboration are separate
future Parts before any adoption. Any WIN row requires both pillars
before adoption; WIN-side flip-census review at adoption follows the
k12/k02/k07/k02-tenth precedent.

## Honest disclosures

- Before this wave A publication, this host fetched the published kit
  from main and byte-verified: jsreplay.js sha256 84585617..., keys
  JSON sha256 5a29b5be..., and all 46 input CSVs (curl from raw CDN at
  main; fetch-back 51/51 byte-identical after the kit commit).
- One pre-declaration sanity run of k01 at 2M was executed on this host
  (result 0, nodes 2,000,000, wall ~9s; UNKNOWN as expected). No other
  eleventh-cost key was run before this declaration.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only. Before each push the
  latest main is re-fetched; concurrent-lane conflicts are recorded,
  not forced.

## Guards

Scheduling only; no verdict is claimed or implied. The standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. The
two-stone root {60,27} and its remaining third moves 100/108: UNKNOWN.
Nodes and proxy values are bookkeeping, never evidence of WIN or LOSS.
