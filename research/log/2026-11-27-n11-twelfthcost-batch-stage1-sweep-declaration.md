# 2026-11-27 n11 twelfth-cost class 10376293541461626880:16777216 exclusive S5 probe batch (single-owner declaration)

Wave A declaration of the twelfth-cost long-lane Part. The adaptive
coordinator's next batch after the eleventh-cost k01 canonical adoption
closed the eleventh-cost batch (canonical head of record 1e2eeda2...,
6,890 rows WIN 208 / LOSS 6,682; flip-census + reaudit refresh published
at commit 2cd58330).

## Selection (published, fail-closed, 270 gates; commit e588de1e)

- Selected class: `10376293541461626880:16777216` (rank 12 of the
  published class-closure-priority table; coverage third moves
  {100, 108, 112, 118}), the first unclaimed live class after the
  eleven claimed classes (focus-35, cert-38, third-39, fourth-41,
  fifth-44, sixth-43, seventh-42, eighth-43, ninth-45, tenth-44,
  eleventh-46).
- Re-validated against the CURRENT canonical head 1e2eeda2...: 100 S5
  unknown before head; 51 exclusive (single-live-parent) unknown
  children; 49 shared; proxy_exclusive_sum 293,115,829; bands
  5,041,585 x 1 / 5,069,670 x 1 / 5,234,938 x 11 / 5,932,112 x 38.
  The eleventh-cost serving class 1297036696978718720:0 is excluded_now
  under the head, so it cannot be re-selected.
- Authoritative selection list: output/twelfth-cost-exclusive-keys.json
  (schema n11-twelfthcost-exclusive-selection-v1, sha256 1119d01b...,
  51 keys; first 1152921504607895556:603979776, last
  14987979559889014784:16777216). Selector select_twelfth_exclusive.py
  (sha256 ea2b8331...), jsreplay byte-clone 84585617..., input CSVs
  k01..k51 generated and cross-checked against the shared-s5 supply.
- Disjointness of the 51 keys from all published claim sets
  (focus/cert/third/fourth/fifth/sixth/seventh/eighth/ninth/tenth/
  eleventh, sbd-101, parked-2, parked-4) is machine-gated inside the
  selector; head freshness (all 51 absent from head 1e2eeda2) is
  machine-gated.

## Execution plan (publish-then-execute; wave B publishes the raws)

Per key k01..k51 (ascending truncated-cost proxy, then key): a
2,000,000-budget cold pair with the published jsreplay 84585617 under
the published input CSVs. A node-identical exact-LOSS resolution stops
the key; a 2M UNKNOWN pair escalates to a 15M-budget cold pair; a 15M
UNKNOWN pair parks the key (L50M escalation candidate). WIN stopping
rule: no new key is started after a key resolves WIN(1). All rows are
single-implementation (Node.js replica); a C++ second-implementation
scrutiny gate and a third-implementation corroboration are separate
future Parts before any adoption. Any WIN row requires both pillars
before adoption; WIN-side flip-census review at adoption follows the
k12/k02/k07/k02-tenth/k01-eleventh precedent.

## Honest disclosures

- Before this wave A publication, this host fetched the published kit
  from main and byte-verified: jsreplay.js sha256 84585617..., keys
  JSON sha256 1119d01b..., and all 51 input CSVs (curl from raw CDN at
  main; all 51 sha256 values verified against the published kit
  MANIFEST) plus a machine check that the 51 input CSV keys match the
  authoritative exclusive_probe_order exactly.
- One pre-declaration sanity run of k01 at 2M was executed on this host
  (result 0, nodes 2,000,000, wall ~9s; UNKNOWN as expected). No other
  twelfth-cost key was run before this declaration.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only. Before each push the
  latest main is re-fetched; concurrent-lane conflicts are recorded,
  not forced. Declared against HEAD fbf11c4f.

## Guards

Scheduling only; no verdict is claimed or implied. The standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. The
two-stone root {60,27} and its remaining third moves 100/108: UNKNOWN.
Nodes and proxy values are bookkeeping, never evidence of WIN or LOSS.
