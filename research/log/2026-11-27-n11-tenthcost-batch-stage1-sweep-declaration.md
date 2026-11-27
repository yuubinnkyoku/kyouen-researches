# 2026-11-27 n11 tenth-cost class 1297036692683751424:131072 exclusive S5 probe batch (single-owner declaration)

Wave A declaration of the tenth-cost long-lane Part. The adaptive
coordinator's next batch after the ninth-cost 12-row canonical adoption
closed the ninth-cost batch (canonical head of record 47280073...,
6,887 rows WIN 206 / LOSS 6,681; flip-census + reaudit refresh published
at commits 55fcc97e / 1fb65f45).

## Selection (published, fail-closed, 234 gates; commit 1ab5d6e1)

- Selected class: `1297036692683751424:131072` (rank 10 of the published
  class-closure-priority table; coverage third moves {47, 51, 100, 108}),
  the first unclaimed live class after the nine claimed classes
  (focus-35, cert-38, third-39, fourth-41, fifth-44, sixth-43,
  seventh-42, eighth-43, ninth-45).
- Re-validated against the CURRENT canonical head 47280073...: 108 S5
  children; 100 unknown before head; 44 exclusive (single-live-parent)
  unknown children; 56 shared; proxy_exclusive_sum 234,754,546; bands
  5,041,585 x6 / 5,234,938 x30 / 5,932,112 x8. The ninth-cost serving
  class 1297036692683751424:134217728 is excluded_now under the head,
  so it cannot be re-selected.
- Authoritative selection list: output/tenth-cost-exclusive-keys.json
  (schema n11-tenthcost-exclusive-selection-v1, sha256 3d0f791e...,
  44 keys; first 1297036692683751424:131074, last
  10376293541461626880:268959744). Selector select_tenth_exclusive.py
  (sha256 0a45a650...), jsreplay byte-clone 84585617..., input CSVs
  k01..k44 generated and cross-checked against the shared-s5 supply.
- Disjointness of the 44 keys from all twelve published claim sets
  (focus/cert/third/fourth/fifth/sixth/seventh/eighth/ninth, sbd-101,
  parked-2, parked-4) is machine-gated inside the selector; head
  freshness (all 44 absent from head 47280073) is machine-gated.

## Execution plan (publish-then-execute; wave B publishes the raws)

Per key k01..k44 (ascending truncated-cost proxy, then key): a
2,000,000-budget cold pair with the published jsreplay 84585617 under
the published input CSVs. A node-identical exact-LOSS resolution stops
the key; a 2M UNKNOWN pair escalates to a 15M-budget cold pair; a 15M
UNKNOWN pair parks the key (L50M escalation candidate). WIN stopping
rule: no new key is started after a key resolves WIN(1). All rows are
single-implementation (Node.js replica); a C++ second-implementation
scrutiny gate and a third-implementation corroboration are separate
future Parts before any adoption. Any WIN row requires both pillars
before adoption; WIN-side flip-census review at adoption follows the
k12/k02/k07 precedent.

## Honest disclosures

- Before this wave A publication, this host fetched the published kit
  from main and byte-verified: jsreplay.js sha256 84585617..., keys
  JSON sha256 3d0f791e..., and all 44 input CSVs (curl from raw CDN at
  main).
- One pre-declaration sanity run of k01 at 2M was executed on this host
  (result 0, nodes 2,000,000, wall ~10s; UNKNOWN as expected). No other
  tenth-cost key was run before this declaration.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only. Before each push the
  latest main is re-fetched; concurrent-lane conflicts are recorded,
  not forced.

## Guards

Scheduling only; no verdict is claimed or implied. The standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone
root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every
closure class: UNKNOWN unless a published Part says otherwise. Nodes
and proxy values are never evidence of WIN or LOSS.
