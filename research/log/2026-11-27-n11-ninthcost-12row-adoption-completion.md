# 2026-11-27 n11 ninth-cost 12-row canonical adoption completion

Completion log of the ninth-cost 12-row canonical adoption Part
(wave A). Commit chain: declaration
`research/log/2026-11-27-n11-ninthcost-12row-adoption-declaration.md`
(7780e2f8, publish-then-execute) -> kit + merged head of record
(6da937d9, `research/experiments/n11-ninthcost-12row-adoption-20261127/`).

## What was done

- Fresh single-owner maker
  (`scripts/make_kit_ninthcost12_adoption_20261127.py`) ran twice
  byte-identical. G0 anchor byte gates (BASE head
  `0935c94c...` 6,875 rows WIN 203 / LOSS 6,672; merger `90711961`;
  quarantine `81d23160`; policy `78655e94`; frozen graph `54f9c364`),
  G1 all four C++ scrutiny gate kits re-verified file-by-file with
  live audit re-run (4loss 33/33, 4lossrest 32/32, k12 23/23,
  parked3-L50M 29/29, audit_gate.py PASS each), G2 all four third-impl
  corroboration kits re-verified per-file byte pins + raw re-parse
  (third_impl.js `08ea958f` in all four; DISCLOSED: no audit script
  exists for the ninth-cost third-impl kits, so no live audit re-run
  for them), G3 the 12 adoption pins re-derived and cross-checked
  against gate quadruples and third-impl raw fields, G4 freshness
  12/12 absent from BASE, WIN/LOSS conflict 0 (vacuous), duplicate 0,
  canonical-safe, G5 increment emit, G6 manifest.
- Increment: 12 rows (9 LOSS + 3 WIN k12/k02/k07), sha256
  `72eac70c1503e7bfafcbdbe66adb12b1a1e52224ffca3eac296e2118c47a6bb0`.
- Merge by pinned `s5_union_merge.py` (sha256 `90711961...`) run THREE
  times byte-identical: new canonical head of record
  `merged-exact-s5-chain-plus-ninthcost12-20261127.cache`, 288,440
  bytes, sha256
  `4728007306598298f7fdb43d0368bc4e5fbd6c9435a38f8d1732d1df8368a622`,
  6,887 rows WIN 206 / LOSS 6,681 - exactly the pre-registered shape
  (6,875 + 12; WIN 203+3; LOSS 6,672+9). Machine-checked: 12/12 adopted
  rows present, 6,875/6,875 BASE rows preserved, duplicate_rows_elided
  0, no WIN/LOSS conflict.
- Publication verified commit-pinned (`6da937d9`) via authenticated
  fetch-back: all 9 kit files byte-identical to host bytes (MANIFEST
  included; merged cache sha256 re-confirmed
  `47280073...` on the published side).

## Defects disclosed, not fixed by this lane

- k12 third-impl kit's published MANIFEST-sha256.txt carries a stale
  README.md line (pins third_impl.js's sha/size instead of the README
  actually on main, sha256 `07515850...`, 2,645 bytes). Bookkeeping
  only; recorded in the adoption manifest; correction belongs to that
  kit's owner lane.
- Maker self-bugfixes (all caught fail-closed before any output
  publication): THIRD_IMPL_SHA typo, TI-kit column index bug, raw
  row-label strictness (4loss kit labels rows "k01" without ".p1"),
  gate-rows key-field polymorphism ("key" string vs lo/hi split).
  Expected quadruples never relaxed.

## Position and next work

The canonical S5 solver-trusted chain head is now
`merged-exact-s5-chain-plus-ninthcost12-20261127.cache`
(`47280073...`, 6,887 rows WIN 206 / LOSS 6,681). Verdict scope of
this Part was exactly those 12 S5 rows: NO root verdict consumed, NO
class freed or excluded, NO closure claim. Next: the flip-census /
reaudit Part (SZ wave E precedent) of the three WIN rows
(k12/k02/k07) against this new head, then worklist regen and the
tenth-cost selection (BASE = this new head). The standard 11x11 empty
board, all 19 central-reply roots, the two-stone root {60,27}, its
remaining third moves {100,108}, S2 and all closure classes remain
UNKNOWN. Nodes and expansions are bookkeeping, never verdicts.
