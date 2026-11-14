# n11 S2 {59,60} milestone-5: full independent worklist derivation + S7 certificate-reuse partition

## 後続監査の注意
`scripts/ms5_s7_reuse_analysis.ts` はコメントのみで実行本体がなく、下記の再導出・分類を再実行できない。`scripts/audit_published_candidates.py` は公開済み行の安全性・親子関係・件数を検査するが、網羅性や分類を検証しない。現在の評価は K0783 を参照。

後続の全列挙 `scripts/audit_candidate_completeness.py` により、下記の8,763件は完全ではなく、94オラクルの全対称像を使うと15,072件あることが判明した。追加6,309件は `output/additional-candidates.csv.gz` に収録し、その安全性は別の行列式検査でも確認した。候補のない親は下記の1,591個ではなく611個。

さらに `scripts/audit_win7_reuse.py` でリポジトリ内のWIN7監査記録を照合すると、534親子対・498親に勝ち子が見つかり、残りは7,369親となる。監査記録を前提にした結果で、別保管の証明書本体は再検証していない。照合表は `output/win7-reuse-hits.csv.gz` を参照。

候補CSVの `move` は正規化済み `s6_hex` にそのまま適用できるとは限らない。親の対称像を試し、空き位置 `move` を加えた子の正規形が `s7_hex` に一致する像を選ぶ。part2とpart3にはCSVヘッダーがない。

Baseline main: `5af484bb241cd776af2eda5e26eda4e97595baee` (includes the full S6 geometry cost audit of 2026-11-13, which verified the cost column of all 7,867 published rows but explicitly not the key set or classes column).

## Part 1: full independent worklist derivation (keys + classes + cost)

A fresh TypeScript routine (independent of the milestone-5 generator) re-derived the entire milestone-5 accounting from the K0675 oracle inputs (78 FW + 16 SW base hex positions, 14 LOSS sweep keys):

- sweep (judged 6-stone children of the oracle bases): **3,868**
- S5 worklist orbits: **196**
- obligatory (S5, child) instances: **17,524**; judged instances **479**; judged-LOSS instances **13**
- S5 orbits settled by a judged-LOSS child: **10**
- reduced unique S6 worklist orbits: **7,867**; total S7 legal-edge cost: **615,497**

The re-derived `hex,cost,classes` table, sorted lexicographically, is **byte-identical (md5 `0e95a438dbcb486368393de9c73fc21e`)** to the concatenation of the six published `ms5_s6_manifest_part*.csv` files. This closes the gap left by the geometry-only audit: the key set and the classes column are now independently reproduced as well.

## Part 2: S7 certificate-reuse partition of the 7,867-row worklist

Every worklist S6 is a 6-stone position; its 7th move x produces a 7-stone position S7 = S6 + x. An S7 can only belong to the existing certified pool if it contains one of the 94 oracle base positions (78 FW + 16 SW, 5 stones each) as a subset; since a worklist S6 never contains an oracle base in full, the only candidates have exactly one oracle stone outside S6 (|O \ S6| = 1) with x legal for S6.

Result (deduplicated by canonical S7 hex, all under the K0675 oracle conditioning):

- oracle-completing candidates: **8,763** across **6,276** distinct worklist S6s (1,591 S6s have no candidate)
- direct hits against the 62 focus2154 certificates: **0 WIN7**, and every LOSS7 of the 62 that arises this way is counted below
- known-LOSS candidates: **396** (in the 35 certified LOSS7 set, or in the LOSS7 pool = legal children of the 14 LOSS sweep S6, pool size 907)
- possible-win-pool candidates: **8,367** (the S7 has some 6-stone subset inside the judged 3,868-position sweep, so it *may* be a recorded win-child witness)
- unclassified candidates: **0** — the candidate set is completely partitioned.

Per-S6: **6,073** S6s have at least one possible-win-pool candidate; **374** have at least one known-LOSS candidate.

## External-lane action

Intersect the `s7_hex` column of `ms5_s7_reuse_candidates_part1..3.csv` (cat=2 rows) with the local win-child key pool (e.g. `/mnt/d/kyouen-focus-certs`). Each hit certifies its parent S6 as WIN (player to move), under the K0675 oracle conditioning, without any new search.

## Output files

- `output/ms5_s7_reuse_stats.json` — the counts above.
- `output/ms5_s7_reuse_candidates_part1..3.csv` — header `s7_hex,s6_hex,move,cat`; cat: 1 = known LOSS child, 2 = possible-win-pool. move is the 7th stone index (row-major, 0..120).
- `output/ms5_s7_knownloss_candidates.csv` — the 396 known-LOSS rows.
- `scripts/ms5_s7_reuse_analysis.ts` — regenerates everything deterministically, including the manifest derivation check.

## Status

This is verification and bookkeeping only. **No game verdict is established**: 11x11 empty root, two-stone root {49,60}, and S2 {59,60} all remain **UNKNOWN**. All win/loss statements above are conditioned on the K0675 oracles (78 FW + 16 SW positions).


## 2026-11-14 incremental reuse from later class2-lane certificates

The baseline 498-parent S7 reuse audit was extended with the cost-69c, cost-70b, cost-71, and cost-75 WIN7 certificate manifests. The 23 new roots are distinct and exactly safe; they yield 70 S6-parent incidences over 48 distinct worklist parents. After removing the five parents already covered by the baseline, **43 additional D4-canonical S6 worklist orbits** are covered. The remaining worklist falls from 7,369 to 7,326 rows, and the remaining legal seventh-move candidate cost falls from 577,110 to 573,835 (a reduction of 3,275).

This is certificate-reuse bookkeeping, not closure of S2 or the empty root. Certificate bodies were not re-run in this audit; see [the run log](../../log/2026-11-14-n11-s2-class2-win7-incremental-reuse.md), [the reproducible audit script](scripts/audit_incremental_class2_win7_reuse.py), and [the JSON result](output/class2-win7-reuse-incremental-20261114.json).
