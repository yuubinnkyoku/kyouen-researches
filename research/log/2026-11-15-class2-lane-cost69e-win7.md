# 2026-11-15 class2-lane: cost-69e sweep — 11 WIN7-D10 (all 11 WIN7 bits certified: 10 lane certificates incl. warm rebuilds, bit 2 by the parallel cost-65g-warm bit-15 rebuild; all 11 v15-anchored), frontier 1012 -> 1023 (merged baseline)

Long-term lane parallel execution, continuing after the cost-68c frontier
recompute (after-cost-68c solved 998; commit `368e2b1f`). Sweep target: the
cost-69 child `00000000000000803202000000008000` of the second class-2 target
S5 `00000000000000803202000000000000`, named cost-69e (cost-69a/b/c/d
occupied by earlier lanes on other parents; this child was one of the two
cheapest remaining unswept children of the parent, 12 orbits / 864 after
cost-68c).

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `41693097`):
  `class2-lane-cost69e-inflight-20261114.json`, 69 candidates bit-exact with
  the published edge cost 69 (independent `legal_candidates.py` Bareiss
  enumeration).
- **Per the cost-61e correction lesson**, the child's membership among the
  parent's remaining children and its non-empty demand (c1=0, c2=2, c4=0)
  were re-verified from
  `class-frontier-top-candidates-s6-after-cost68c-20261114.csv` BEFORE the
  claim.
- Engine: the v16 runner (`class4_child1_runner_v16.ts`, repo-verbatim), depth
  10, andclose=1, cap 1e9; pilot d6 control loss=false at exactly 3,402 nodes
  in all 9 batch invocations.

## Mid-flight manifest closure (cross-lane coordination fact)

While this sweep was in flight, the parallel lane published the merged
warm+sweep frontier recompute
(`class-frontier-merged-recompute-after65h65i-warm67b68c-20261115.json`,
commit `a7f3fc97`, solved 1012), whose **cost-65g-warm bit-15 receipt (root
`00000000000000803202000000008004`) closed this child in the manifest** —
the same 7-stone root this sweep independently re-derived as WIN7 bit 2 (an
unplanned cross-lane reproduction: v16 1,999,371 nodes / v15 5,510,814
nodes, both engines WIN7-D10). The sweep therefore completed on an
already-receipt-closed child; its receipts are pure new-coverage additions.
The parallel lane simultaneously claimed the parent's cost-70 child as
cost-70c (`00000000000000803242000000000000`, commit `fee1a57b`).

## Sweep result

**69/69 candidates: 11 WIN7-D10 + 58 REFUTED, 0 capped, 80,172,332 v16
nodes** (9 batches 8x8+5, raw JSONL pushed per batch — commit `cd7d558f`;
terminal range [13,17] on every candidate).

- WIN7 bits: 2, 21, 76, 84, 87, 89, 90, 94, 99, 108, 116.
- Heaviest candidates: bit 116 (6,683,450, WIN7), bit 44 (5,674,763,
  REFUTED), bit 33 (5,104,350, REFUTED), bit 4 (3,692,028, REFUTED), bit
  22 (3,141,962, REFUTED), bit 94 (2,679,844, WIN7).
- Determinism: bit 116 (WIN7, 6,683,450) and bit 44 (REFUTED, 5,674,763)
  re-solved fresh in a separate process, node-exact identical
  (`class2-lane-cost69e-v16-determinism-rerun-20261114.jsonl`, commit
  `49e36f19`).
- v15 cross-engine anchors (pilot 5,949 PASS): **all 11 WIN7 bits** loss=true
  at 1,131,809 (21) / 1,746,232 (99) / 4,764,589 (87) / 9,765,935 (84) /
  5,510,814 (2) / 5,109,539 (76) / 6,478,505 (90) / 5,747,330 (108) /
  5,599,058 (89) / 6,171,899 (94) / 16,776,783 (116) nodes — verdicts
  identical to v16 (`class2-lane-cost69e-v15-crosscheck-20261114.jsonl`,
  same commit).
- Duplicate-root check: all 11 WIN7 root hexes code-searched over
  yuubinnkyoku/kyouen-researches before pushing certificates. 9 roots 0 hits.
  Two cross-child duplicates: (1) the bit-2 root
  `00000000000000803202000000008004` duplicates the cost-65g bit-15 listing
  AND the parallel cost-65g-warm bit-15 rebuild certificate (cross-lane
  reproduction, no new certificate needed); (2) the bit-21 root
  `00000000000000803202000000208000` duplicates the cost-60b bit-15
  win7_roots listing (cost-61e bit-1 pattern) but had NO prior published
  certificate (cost-60b certified bits 117/96/94/105/73/23 only), so its
  certificate is new coverage and also closes the cost-60b bit-15 warm
  entry.

## Three WIN7 certificates — all verification PASS

Three WIN7 candidates (the cheapest per certificate) were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
fbt_drops=0 on all three; rows sorted unique; verified with
`verify_bit7_win7_cert.ts` (root-check + all sub-roots + consumed/rows
union).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 21 | `00000000000000803202000000208000` | 22,261 | 1,878,783 | 45 | 45/45 | 0/0 | `b229fe7c...` |
| 99 | `00000008000000803202000000008000` | 25,149 | 3,059,688 | 50 | 50/50 | 0/0 | `69f5fae1...` |
| 87 | `00000000008000803202000000008000` | 43,838 | 7,331,883 | 59 | 59/59 | 0/0 | `5f506323...` |

- All three landed byte-exact with full paged reads (commits `2583540f` /
  `c9185bb2` / `278ed8c9`); remote md5 verified (bit 21
  `b229fe7c0c96901fe04ddf05763ffb9e`, bit 99
  `69f5fae13d3c712df7b2883ec79d7c2a`, bit 87
  `5f5063233ff919b704e01a105e1fb132`). Operational note: the bit-87 push hit
  the sandbox memory limit AFTER the push call completed; the remote file was
  verified byte-exact afterwards.
- Certificates: `class2-lane-cost69e-certificates/bit{21,99,87}-root-<hex>.cert`.
- After the warm rebuilds of 84/76/90, the remaining 4 WIN7-D10 bits
  (89, 94, 108, 116) were rebuilt as warm certificates in a follow-up
  session (next section); bit 2 is certified by the parallel cost-65g-warm
  bit-15 rebuild, so **all 11 WIN7 bits of this sweep now have
  certificates**.
- Records pushed (commit `6f776bef`): sweep record + win7-certificates record
  (schema-consistent with the cost-65h/67b/68c records) + inflight updated to
  completed.

## Warm certificate rebuilds (same session)

Three more WIN7-D10 candidates were rebuilt as warm certificates in the same
session and fully verified (same blind extraction and verification pipeline;
root-check mobility match, all sub-roots PASS in 2 splits, consumed/rows
union 0/0):

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 84 | `00000000001000803202000000008000` | 29,614 | 9,940,934 | 50 | 50/50 | 0/0 | `41adac3c...` |
| 76 | `00000000000010803202000000008000` | 45,665 | 8,663,434 | 57 | 57/57 | 0/0 | `2358870d...` |
| 90 | `00000000040000803202000000008000` | 46,959 | 10,061,833 | 58 | 58/58 | 0/0 | `b0e6f779...` |

- All three landed byte-exact (commits `53102729` and the memory-limit-after-
  push landings verified by remote md5: bit 76
  `2358870d7a2625b4d40a0c178f8cba66`, bit 90
  `b0e6f779b229ef4993c8715691db7ede`, bit 84
  `41adac3c1d684d4b4dde25c416c2ae20`).
- Records updated (commit `53511442`): 6 certificates total; unverified WIN7
  bits then 89/94/108/116 (bit 2 already certified by the parallel
  cost-65g-warm bit-15 rebuild).
- Records extended to the complete 10-certificate set (commit `8c5561ee`):
  bits 89/94/108/116 appended with full verification metadata;
  `unverified_win7_bits` now empty. Bit-116 is published as base64(gzip -9)
  (`.../bit116-root-00100000000000803202000000008000.cert.gz.b64`, 445,162
  bytes, commit `ce7d862d`; restore with `base64 -d | gunzip`; uncompressed
  2,670,116 bytes / 74,115 lines, md5
  `691140486067132237d8c11d93a12559`, sha256
  `20c0f5edf05f9f45cd0e5d3331a22ec3a39ac001b28428a51d79eefda4498159`;
  roundtrip verified locally and via the SHA-pinned raw URL).
  Remote md5 verified for all 10 lane certificates (bits
  21/99/87/84/76/90/89/94/108 plain, 116 via the uncompressed md5 of the
  base64(gzip) publication).

## Second warm rebuild batch: bits 89 / 94 / 108 / 116

A follow-up session (2026-11-15) rebuilt the remaining four WIN7-D10
candidates as warm certificates (same blind extraction + verification
pipeline: root-check mobility match, all sub-roots PASS, consumed/rows
union 0/0):

| bit | root hex | rows | extraction nodes | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---|---|
| 89 | `00000000020000803202000000008000` | 47,035 | 8,642,394 | 54/54 | 0/0 | `1e2c8db6...` |
| 94 | `00000000400000803202000000008000` | 42,538 | 8,681,404 | 52/52 | 0/0 | `4dc6076b...` |
| 108 | `00001000000000803202000000008000` | 33,942 | 7,620,433 | 51/51 | 0/0 | `74d07146...` |
| 116 | `00100000000000803202000000008000` | 74,113 | 22,683,171 | 59/59 | 0/0 | `69114048...` (uncompressed) |

- Full md5s: bit 89 `1e2c8db6cd9303fcf0167f59ccb83bae`, bit 94
  `4dc6076b96edc3a472b4b23f38739451`, bit 108
  `74d071466140e1b0a48b67134431a570`, bit 116 (uncompressed)
  `691140486067132237d8c11d93a12559`. Certificates 89/94/108 pushed as
  plain `.cert` files; 116 as base64(gzip -9) per the 16 MiB sandbox
  payload limit (commit `ce7d862d`; relay part files removed in commits
  `f31cb81f` / `064bd6d3`).

## Frontier recompute after cost-69e

`recompute_frontier_cost69e_20261115.py` (direct runpy extension of the
published merged recompute script; first pushed at commit `b37252d3`,
extended to the 6-receipt version at commits `7cec3e7e` / `93c90db6`, and
to the 10-receipt final version (schema v2) after the second warm-rebuild
batch): the merged baseline reproduced exactly (asserted
1012/6,835/538,670/5,105/402,393), the child's remaining membership
re-derived from the merged frontier (confirmed closed mid-flight; demand
bookkeeping recorded), the completed cost-69e sweep asserted from the
published raw batches (69 candidates, 9 pilots, 11 WIN7 + 58 REFUTED,
80,172,332 nodes; determinism + v15 anchors asserted from the published
JSONL files), and the ten verified receipts added in the published record
order (21/99/87 sweep certificates, then the 84/76/90 and 89/94/108/116
warm rebuilds; bit-116 md5 asserted as the uncompressed certificate md5
since the file is published as base64(gzip)).

- cost-69e additions (covers / marginal / in-manifest): bit 21: 7/5/1, bit
  99: 7/5/1, bit 87: 7/5/1, bit 84: 7/5/1, bit 76: 7/6/2, bit 90: 7/5/1
  (each receipt covers 7 S6 orbits; the in-manifest marginals are outside
  this target's parent).
- **after cost-69e (6 receipts): solved 1019 · unique remaining 6,832 with 3
  receipts -> 6,828 with 6 · sum 538,445 -> 538,143 · open 5,102/402,168 ->
  5,098/401,866** (net in-manifest +7 from 1012). The intermediate 3-receipt
  state (solved 1015) was published first; the 6-receipt state was the
  final state at commits `7cec3e7e` + method-text fix `93c90db6`.
- cost-69e additions from the second warm-rebuild batch (covers /
  marginal / in-manifest): bits 89/94/108/116 each 7/5/1, closing exactly
  one additional manifest S6 orbit per bit:
  `00000000000000003800200008080000` (89),
  `00000000000000103820000008000000` (94),
  `00000000200000083800000000100000` (108),
  `00000000000000043820000008000000` (116) — all outside this target's
  parent.
- **after cost-69e (10 receipts, schema v2, final): solved 1023 · unique
  remaining 6,824 · sum 537,833 · open 5,094/401,556** (net in-manifest
  +11 from 1012). Two consecutive v2 runs byte-identical (JSON + both
  CSVs); remote md5 to be verified after push.
- Notably the warm bit-76 receipt marginally covers **the cost-70 child
  `00000000000000803242000000000000` claimed in parallel as cost-70c** (its
  other in-manifest marginal is `00000000000000849002000000020000`): the
  parallel lane's cost-70c recompute will find that child already
  receipt-closed in the manifest by this receipt.
- Second class-2 target S5 `00000000000000803202000000000000`:
  7 -> 6 orbits / 513 -> 443, still the best coverable class-2 target. Next
  cheapest remaining children: the cost-70 child
  `00000000000000803242000000000000` (claimed in parallel as cost-70c,
  commit `fee1a57b`) and the cost-71 child
  `00000000000000803202000400000000`. Best class-4 unchanged (18 / 1,460).
- Two consecutive recompute runs byte-identical (JSON + both CSVs); remote
  md5 verified for the recompute JSON, ranking CSV, top-candidates CSV and
  the script.

## Independent audit of all ten certificates (2026-11-15)

A fully independent Python audit of all ten lane certificates (script
`scripts/audit_cost69e_win7_certs_20261115.py`, record
`output/class2-lane-cost69e-10cert-python-independent-audit-20261115.json`):
fresh implementation written from the published game-rule description only —
no repository verifier import, no engine, no verdict cache, no floating
point; the kyouen predicate is an exact integer Bareiss 4x4 determinant of
[x^2+y^2, x, y, 1] on arbitrary-precision integers, forbidden-by-triple masks
recomputed from scratch.

Checks per certificate: file md5/sha256 against the records file (bit-116
restored from the base64(gzip -9) publication and checked against the
records-pinned uncompressed hashes and byte size 2,670,116); exact
header/root lines; root = child | 1<<bit with 7 stones and all C(7,4)=35
root determinants non-zero; loser mobility re-enumerated independently and
matched to the records root_check and the one-bit strategy rows; full
sub-root decomposition with every strategy move legal, all loser replies
expanded, terminals loser-stuck at 13..17 stones, no strategy rows at
loser or terminal states; exact consumed/rows union over all sub-roots
(0 missing / 0 extra).

**All 10 certificates PASS every check**: 411,114 strategy rows,
893,019 visited states, 830,898 loser reply edges, 535/535 sub-roots,
terminal range [13, 17] on every certificate; wall ~51 s for the full set
(two consecutive runs identical modulo per-certificate wall times). Per
certificate (rows / mobility = sub-roots / visited / loser edges): 21
22,261/45/51,285/48,620 · 99 25,149/50/55,552/50,571 · 87
43,838/59/93,566/85,999 · 84 29,614/50/69,534/65,303 · 76
45,665/57/96,678/89,709 · 90 46,959/58/98,588/90,977 · 89
47,035/54/106,325/101,069 · 94 42,538/52/99,751/94,297 · 108
33,942/51/75,305/69,644 · 116 74,113/59/146,435/134,709.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
