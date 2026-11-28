# n11 thirteenth closure-ladder top-candidate selection (2026-11-28)

Execution kit of the selection declared in
`research/log/2026-11-28-n11-thirteenth-ladder-top-selection-declaration.md`
(publish-then-execute, declaration commit `7583169d`, single owner).
Under the canonical head of record `beecb024...`
(`merged-exact-s5-chain-plus-ultra-cheap-u04-20261127.cache`, 6,894
rows WIN 212 / LOSS 6,682) and the published ultra-cheap u04 adoption
reaudit closure ladder (`ef344748...`, 800 data rows).

## Result (PASS, rc=0, 42 gates, 3 cold runs byte-identical)

All 800 published closure-ladder rows have their `unknown_now`
independently recomputed from the frozen dependency graph `54f9c364...`
+ head `beecb024...` + update8 receipts `b658290a...` (fresh
re-implementation of the refresh's trust boundary; the refresh
machinery itself is NOT read or executed): **800/800 exact match**.

Top-5 ladder rows gated exactly as pre-registered: class 16757 (2) /
5804 (4) / 20421 (5) / 34269 (11) / 12264 (33).

**Selection: class 16757** (`1153204079095185408:65536`,
`class_rank` 1, exactly **2 remaining unknown S5 keys**), the first
ladder class whose remaining unknown keys are ALL unclaimed, fresh,
quarantine-free, 5-stone, D4-canonical and canonical-safe:

| # | key | s5_index | legal (Board / fresh det) | probe-13 supply |
|---|---|---|---|---|
| k01 | 1153204147814662144:65536 | 556117 | 72 / 72 | absent (proxy null) |
| k02 | 1152922672837951488:65792 | 558553 | 72 / 72 | absent (proxy null) |

Both keys' legal move counts were re-derived by two independent
implementations (the repo `independent.py` Board and a fresh integer
4x4-determinant concyclicity implementation inside the selector) and
agree. Resolving both keys would complete class 16757 (a candidate
free_now flip, Board-verified at adoption time).

Scanned candidates: ladder ranks 1-12 are ALL fully available (no
blocked keys among ranks 1-12; the first 12 classes carry 2/4/5/11/33/
46/50/50/51/51/51/51 unknown keys respectively); class 16757 wins by
class_rank order.

## Claim status

Both selected keys are UNCLAIMED against focus_35, cert_38, third_39,
fourth_41, fifth_44, sixth_43, seventh_42, eighth_43, ninth_45,
tenth_44, eleventh_46, twelfth_51 (including the concurrent
twelfth-cost takeover lane, declaration commit `768d2e5a`), sbd_101,
parked_6 and the adopted ultra-cheap 4; both are fresh vs the head;
neither is in the 2-entry quarantine registry.

## Files

- `scripts/select_thirteenth_ladder_top.py` - fresh selector, a
  structural adaptation of the published ultra-cheap census instrument
  `ultra_cheap_census.py` (sha256 `c5e7b88e...`): head pin beecb024,
  closure-ladder pin ef344748 (800 rows), pre-registered top-5 and
  selection gates, claim-set machinery (fifth-selector AST extraction
  + 8 selection jsons + keymap + parked CSVs + ultra-cheap 4 in-head
  gate), and the dual-implementation legal derivation added.  sha256
  `e2986020b3a7be399568d82e93ad3b0bead7485302a06619c23d78ea614a7e1d`.
- `output/run{1,2,3}.json` + `output/stdout-run{1,2,3}.txt` - three
  cold passes, byte-identical (run json sha256
  `fd9e21d73ebc346730710a2e4415ccea41cb8fef666e50e7b97e4a314035ff2c`).
- `input/k01.input.csv` / `input/k02.input.csv` - the 2 probe input
  rows generated from the machine selection.
- `MANIFEST-sha256.txt` - sha256 of every file in this kit.

## Inputs (published elsewhere, sha-pinned in-script)

dependency graph `54f9c364...`, update8 receipts `b658290a...`, head of
record `beecb024...`, closure ladder `ef344748...`, probe-13 supply
`31f0d29b...` + candidate ledger `2a4c2382...` (shape gates),
quarantine `81d23160...`, geometry `146be80b...`, Board
`954d3a10...`, policy `78655e94...`, fifth selector `af68af3c...`
(focus/cert/third/fourth claim lists), the eight cost-selection key
lists (fifth through twelfth), the sbd-101 keymap `0aa054c8...`, and
the parked-2/parked-4 batch CSVs.

## Tamper battery (5/5 fail-closed; clean control re-PASS byte-identical)

- T1 closure-ladder rank-1 `unknown_now` 2->3 with the pin patched to
  the tampered file -> caught by BOTH the P2 800-row recomputation
  gate and the P2 top-5 gate, rc=1
- T2 head verdict-row deletion -> P0 head-sha + P1 head-shape, rc=1
- T3 duplicate key appended to the seventh claim list with the pin
  patched -> P3 claim-sizes gate, rc=1
- T4 dependency-graph `s4_cost` edit (class 16757 unknown removed)
  with the pin patched -> P2 recomputation + P4 selection gates, rc=1
- T5 update8 receipt deletion -> P0 update8-sha + P1 receipts + P2
  recomputation, rc=1

## Meaning and non-meaning

Selection and scheduling only: NO verdict is claimed or implied.
Nodes, proxy and legal counts are bookkeeping, never evidence of WIN
or LOSS. Resolving the selected keys requires a separate future
single-owner escalation declaration and, before any adoption, the
standing cold-pair + C++-gate + third-implementation pillars. The
standard 11x11 empty board, all 19 central-reply roots, the two-stone
root {60,27} and its remaining third moves 100/108 stay UNKNOWN.

## Honest disclosures

- Two in-session selector pin typos (the seventh-cost selection json
  sha and a parked-4 sha list comparison) were caught fail-closed by
  the selector's own P0 gates on the first run and fixed before any
  PASS run; all published runs used the fixed selector.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- All pinned inputs were present locally byte-verified against the
  published sha256 pins before the run.
