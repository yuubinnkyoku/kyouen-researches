# n11 fifteenth ladder-top class-5804 k03 canonical adoption

Execution kit of the Part declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k03-adoption-declaration.md`
(commit `764ee708`, single owner, publish-then-execute): the canonical
adoption (k03-only) of the fifteenth class 5804 k03 WIN row into the
head of record.

## Results (MAKER-PASS x2 byte-identical)

- **New head of record:
  `merged-exact-s5-chain-plus-fifteenth-k03-20261128.cache`
  sha256 `3a527d39db7acec32b4c688e0bbbafea8015d9d4aac778cf51e7e5c37afe6a3a`,
  6,899 rows WIN 217 / LOSS 6,682** - exactly the pre-registered
  shape (BASE `b5f322dd...` 6,898 rows WIN 216 / LOSS 6,682 + 1
  fresh WIN row).
- Increment: 1 WIN row, sha256 `16dd8594...`
  (`output/increment-fifteenth-k03-adoption-20261128.cache`);
  adopted node total 3,364,655 (bookkeeping).
- Manifest: `adoption-manifest.json` (schema
  n11-fifteenth-ladder-top-k03-win-adoption-manifest-v1).
- Merger `90711961...` x3 byte-identical (merge-audits in
  `output/merged/`).

## Gates (all PASS, fail-closed; maker x2 byte-identical)

G0 pins (merger/policy/quarantine/BASE head/gate source+headers) +
published-kit MANIFEST self-verification of all 3 source kits
(re-escalation kit `88a24418`/`09358acd`, cppgate kit `ea3f482f`,
thirdimpl kit `ea3f482f`, 0 self-referential manifest lines each);
G1 LIVE re-run of the published gate_runner.sh on a scratch kit copy
(fresh-cold C++ pair, node-exact vs the published raw,
`92,15000000,1,3364655`); G2 three-pillar re-parse (replica pair +
C++ gate pair + third_impl pair + summary cross-checks,
verdict/legal/key/expansions checks, TI expansions 3,906,063); G3
freshness (key absent from BASE) + no WIN/LOSS conflicts; G4
quarantine-free + canonical-safe per s5_evidence_policy; G5 increment
build; G6 merger x3 + shape check. Both maker runs (post-declaration)
produced byte-identical kit outputs (kitout recursive-diff clean).
Tamper battery 5/5 fail-closed (T1 result flip caught by the G2
replica-quad check, T2 third-impl expansions pin drift caught by the
G2 TI check, T3 gate quad flip caught by the G1 live re-run, T4
quarantine-key injection with a re-pinned registry sha and a fully
valid registry entry caught by the intended G4 gate ("quarantined key
k03"), T5 coherent freshness world with the k03 row injected into a
re-pinned BASE caught by the intended G3 gate - all stopped before
any output; registry and BASE restored byte-identical after T4/T5)
+ clean control re-PASS byte-identical (`output/tamper-battery-stdout.log`).

## Honest disclosures

- The gate binary was rebuilt from the pinned source `9193f5b6...`
  (zig 0.13.0, tarball pin `d45312e6...`) in this execution
  environment; it is the same binary that produced the published
  fifteenth k03 cppgate kit GATE-PASS this session. The live gate
  re-run re-verified the target row node-exact against the
  published raw (G1).
- The maker is a machine-adaptation of the published fifteenth k01
  adoption maker (`scripts/make_adoption_fifteenth.py`, kit
  `n11-fifteenth-ladder-top-k01-adoption-20261128`, sha256
  `cea18c48...`); every replacement was count-asserted (single
  occurrence) and the adapted script re-parsed. The policy module
  lives at a 4-deep scratch path `pol/w/x/y/s5_evidence_policy.py`
  so its parents[4] registry lookup resolves to
  `results/n11-s5-evidence-quarantine.json`, mirroring the published
  maker arrangement.
- The published merger `90711961...`, policy `78655e94...` and
  quarantine registry `81d23160...` were byte-fetched from their
  published locations and sha-verified before use.
- The published fifteenth k01 adoption increment's header comment
  contains a stale node figure ("nodes 4,360,661" vs the row's
  actual 12,803,283) - comment-block-only machine-adaptation bug,
  disclosed in the adoption declaration `764ee708`; the k01 data row
  and manifest are correct and the head of record chain is
  unaffected. This k03 increment's comment block is written from
  the measured k03 values (3,364,655).
- No cross-host replication kit exists for this row; the
  three-implementation pillar agreement plus this host's live gate
  re-run are the standing evidence (declared up front).
- Only the 1 declared row is adopted; nothing else is written.

## Follow-up Part (declared)

The WIN-side flip-census review (BASE `b5f322dd` -> SCEN `3a527d39`
measurement; owner class union derived from the frozen graph
`54f9c364` via `idx in s4_cost[ci]`; caveat: shared-owner
pre-exclusion as measured in the fifteenth k01 reaudit, where the
naive owner-union prediction over-predicted flips [5601, 5804, 8675]
vs measured [5601, 8675]). Class 5804 completion additionally
requires k02 `6052837899185946628:128` (15M UNKNOWN; parking/L50M
only under a fresh declaration) and Board-verified free_now at
audit time.

## Files

- adoption-manifest.json - machine manifest.
- output/increment-fifteenth-k03-adoption-20261128.cache - the 1-row
  increment.
- output/merged/merged-exact-s5-chain-plus-fifteenth-k03-20261128.cache
  - the new head of record (289,001 B).
- output/merged/merge-audit-run{1,2,3}.json - merger audits.
- output/tamper-battery-stdout.log - the 5/5 fail-closed battery.
- scripts/make_adoption_fifteenth_k03.py - the maker (machine
  adaptation of the fifteenth k01 adoption maker, sha-verified
  pins, fail-closed gates).
- MANIFEST-sha256.txt - sha256 of every published file (excluding
  itself).

## Status guard

Adoption bookkeeping only: the adopted row is cache bookkeeping,
NOT a class closure, NOT a root verdict, and transfers nothing.
The standard 11x11 empty board, the 19 central-reply roots, the
two-stone root {60,27} and its remaining third moves {100,108}
stay UNKNOWN. Nodes are bookkeeping, never verdicts.
