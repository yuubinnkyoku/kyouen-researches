# n11 fifteenth ladder-top class-5804 k02 canonical adoption

Execution kit of the Part declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k02-adoption-declaration.md`
(commit `12d43eb9`, single owner, publish-then-execute): the canonical
adoption (k02-only) of the fifteenth class 5804 k02 WIN row into the
head of record.

## Results (MAKER-PASS x2 byte-identical)

- **New head of record:
  `merged-exact-s5-chain-plus-fifteenth-k02-20261128.cache`
  sha256 `58110025dd5cca7f1e824d8871b50462dc9fcbeac8b9aa69c5f4d33299c894ae`,
  6,900 rows WIN 218 / LOSS 6,682** - exactly the pre-registered
  shape (BASE `3a527d39...` 6,899 rows WIN 217 / LOSS 6,682 + 1
  fresh WIN row).
- Increment: 1 WIN row, sha256 `2b96a3a911063a9d1ac48edf9264bdc844841e688bb4efc520069c0837dd76b3`
  (`output/increment-fifteenth-k02-adoption-20261128.cache`);
  adopted node total 18,247,029 (bookkeeping).
- Manifest: `adoption-manifest.json` (schema
  n11-fifteenth-ladder-top-k02-win-adoption-manifest-v1).
- Merger `90711961...` x3 byte-identical (merge-audits in
  `output/merged/`).

## Gates (all PASS, fail-closed; maker x2 byte-identical)

G0 pins (merger/policy/quarantine/BASE head/gate source+headers) +
published-kit MANIFEST self-verification of all 3 source kits
(L50M escalation kit `5cc8e1fb`/`48ea76d8`, cppgate kit `f2b8f744`,
thirdimpl kit `f2b8f744`, 0 self-referential manifest lines each);
G1 LIVE re-run of the published gate_runner.sh on a scratch kit copy
at the 50M budget (fresh-cold C++ pair, node-exact vs the published
raw, `87,50000000,1,18247029`); G2 three-pillar re-parse (replica pair
node-identical (wall_s-only diff, the published k02 host-footprint
pattern) + C++ gate pair + third_impl pair + summary cross-checks,
verdict/legal/key/expansions checks, TI expansions 21,587,934); G3
freshness (key absent from BASE) + no WIN/LOSS conflicts; G4
quarantine-free + canonical-safe per s5_evidence_policy; G5 increment
build; G6 merger x3 + shape check. Both maker runs (post-declaration)
produced byte-identical kit outputs (kitout recursive-diff clean).
Tamper battery 5/5 fail-closed (T1 replica result flip caught by the
G2 replica-pair check, T2 third-impl expansions drift caught by the
G2 TI check, T3 gate quad flip caught by the G1 live re-run, T4
quarantine-key injection with a re-pinned registry sha and a fully
valid registry entry caught by the intended G4 gate ("quarantined key
k02"), T5 coherent freshness world with the k02 row injected into a
re-pinned BASE caught by the intended G3 gate - all stopped before
any output; registry and BASE restored byte-identical after T4/T5)
+ clean control re-PASS byte-identical (`output/tamper-battery-stdout.log`).

## Honest disclosures

- The gate binary was rebuilt from the pinned source `9193f5b6...`
  (zig 0.13.0, tarball pin `d45312e6...`) in this execution
  environment; the G1 live re-run re-verified the target row
  node-exact against the published raw.
- The maker is a machine-adaptation of the published fifteenth k03
  adoption maker (`scripts/make_adoption_fifteenth_k03.py`, kit
  `n11-fifteenth-ladder-top-k03-adoption-20261128`, commit `bc535153`);
  every replacement was count-asserted (single occurrence) and the
  adapted script re-parsed. Two adaptation slips (the REPL/GATEKIT/
  TIKIT dict keys and the G2 gate-quad budget literal initially kept
  k03/15M values) were caught by residue grep before any maker run.
- The published merger `90711961...`, policy `78655e94...` and
  quarantine registry `81d23160...` were byte-fetched from their
  published locations and sha-verified before use.
- The k02 replica 50M pair is node-identical but not byte-identical
  (wall_s 98/102), the published host-footprint pattern; the maker's
  G2 compares (legal,budget,result,nodes)+key fields, never wall_s.
- No cross-host replication kit exists for this row; the
  three-implementation pillar agreement plus this host's live gate
  re-run are the standing evidence (declared up front).
- Only the 1 declared row is adopted; nothing else is written.

## Follow-up Part (declared)

The WIN-side flip-census review (BASE `3a527d39` -> SCEN `58110025`
measurement; owner class union precheck [5788, 5804, 5815, 7678]
derived from the frozen graph `54f9c364` via `idx in s4_cost[ci]`;
caveat: shared-owner pre-exclusion - serving class 5804 is already
excluded_now on BASE, as measured in the fifteenth k01/k03 reaudits).
If this adoption closes class 5804's last cost-unknown child, the
closure-ladder exit of class 5804 is measured in that Part
(Board-verified free_now at audit time).

## Files

- adoption-manifest.json - machine manifest.
- output/increment-fifteenth-k02-adoption-20261128.cache - the 1-row
  increment.
- output/merged/merged-exact-s5-chain-plus-fifteenth-k02-20261128.cache
  - the new head of record (289,048 B).
- output/merged/merge-audit-run{1,2,3}.json - merger audits.
- output/tamper-battery-stdout.log - the 5/5 fail-closed battery.
- scripts/make_adoption_fifteenth_k02.py - the maker (machine
  adaptation of the fifteenth k03 adoption maker, sha-verified
  pins, fail-closed gates).
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Adoption bookkeeping only: the adopted row is cache bookkeeping,
NOT a class closure, NOT a root verdict, and transfers nothing.
The standard 11x11 empty board, the 19 central-reply roots, the
two-stone root {60,27} and its remaining third moves {100,108}
stay UNKNOWN. Nodes are bookkeeping, never verdicts.
