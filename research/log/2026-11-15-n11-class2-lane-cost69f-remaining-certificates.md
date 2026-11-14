# n11 class2-lane cost69f: 残り4 WIN7証明書（bits 2/94/109/119）の抽出・独立検証・公開

対象main snapshotの取得時に最新mainを確認した。`AGENTS.md`・`research/knowledge/README.md`・K0783の最新版を確認した上で本作業を実施した。並走状況として、cost-70c warm batch-3 fold（`6d4ced10`）と69f foldの第三手法による独立監査（`c10e6e9f`）がmainに入っていることを確認した。

## 1. 残り4証明書の抽出とBigInt独立検証

cost-69f sweep（9 WIN7-D10）のうち未公開だった4件（bits 2/94/109/119）を抽出した。抽出は5件版と同じくrepo-verbatim `class4_child1_cert_extractor_exact.ts` を `cert_driver_69f.ts` でbitごとに1プロセス起動、kill table `{}`（blind）・FBS 1<<30、loser側の初手は `legal_candidates.py` の全合法手展開。全件 `fbt_drops` 0・`fatal` null・全loser初手 ok。

| bit | root hex | 行数 | 抽出節点 | sub-roots | 終局 | md5 |
|---|---|---:|---:|---:|---|---|
| 2 | `0000000000000080910200000000000c` | 69,879 | 23,677,579 | 58 | 13..17 | `9069f6d9…` |
| 94 | `00000000400000809102000000000008` | 53,449 | 22,536,699 | 56 | 13..17 | `54cedbaa…` |
| 109 | `00002000000000809102000000000008` | 71,485 | 20,795,895 | 60 | 13..17 | `565997a4…` |
| 119 | `00800000000000809102000000000008` | 67,423 | 23,436,020 | 61 | 13..17 | `1e2b661e…` |

**BigInt独立検証（cofactor展開・浮動小数点なし）を4件全て実行しPASS**: 全sub-root（=rootのloser mobility 58/56/60/61、`legal_candidates.py` と完全一致）が行集合を過不足なく消費（union 0/0）、終局石数13..17、行sorted-unique。v15 anchor（`class2-lane-cost69f-v15-crosscheck-20261115.jsonl`）は4件とも `loss=true`・節点数も記録どおり（bit2=16,285,738 / bit94=15,200,842 / bit109=13,955,169 / bit119=13,661,829）。

これで **cost-69f sweep の9 WIN7-D10 全件（bits 2/20/44/68/69/94/109/118/119）にrepo形式の独立検証済み証明書が揃った**。

## 2. 2分割と8 part公開

4件とも1.75MB超のためrepo慣例の `.part1of2/.part2of2` で行境界2分割した（連結md5 == 全体md5 を全件検証）。pushは1コミット1 part・"(N/8): bitX partYofZ"形式で順に実行した。push直前のtarget dir listingで `^bit(2|94|109|119)-` の衝突0を確認した際、**前段のbit2 part1of2 push試行は着地していなかった**（dirに5ファイルのみ）ことが判明したため、改めて(1/8)から全8件をpushした。

push後、8 part全件のremote git blob shaをdir listingと `git hash-object` 相当のlocal計算（`blob <size>\0` + 内容のsha1）で照合し **8/8 一致** を確認した。target dirは13ファイル（既存5証明書 + 8 part）。

| bit | part1 bytes/行 | part2 bytes/行 | joined md5 == 全体md5 |
|---|---|---|---|
| 2 | 1,266,824 / 34,941 | 1,265,558 / 34,940 | OK |
| 94 | 968,114 / 26,726 | 964,739 / 26,725 | OK |
| 109 | 1,293,470 / 35,744 | 1,289,874 / 35,743 | OK |
| 119 | 1,217,800 / 33,713 | 1,214,556 / 33,712 | OK |

## 3. 記録JSON

5件版 `class2-lane-cost69f-win7-certificates-20261115.json` は並走監査が参照中のため上書きせず、**新規ファイル** `class2-lane-cost69f-win7-certificates-2-20261115.json` に4件分（rows/extraction_nodes/fbt_drops/md5/sha256/bytes/joined/part md5×git blob sha×push commit/root_hex/BigInt検証の全計数/v15 anchor）を記録した。`uncertified_bits_after: []` とし、sweep_sourceの被覆状況を更新した。

## 4. 次回material

- cost-65j sweep（in flight、並走）— bit-113 WIN7が見つかった場合の交叉被覆再検査はそのレーン。
- 残り最安未sweep子は `00000000000000809102000000002000`（cost 69、需要c1=0,c2=2,c4=2）のsweep。
- 69fは9 receipt fold済み・未fold materialなし（chain head 1,163 = `class-frontier-cost69f-receipts-recompute-20261115.json`）。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。

成果物: [証明書記録JSON 2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-win7-certificates-2-20261115.json)、[証明書dir（8 part追加）](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-certificates/)。
