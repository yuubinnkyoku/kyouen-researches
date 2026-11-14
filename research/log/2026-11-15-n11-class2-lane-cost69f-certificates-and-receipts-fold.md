# n11 class2-lane cost69f: WIN7証明書5件の公開（truncated repush含む）と9 receipt fold — chain head 1,163

対象main snapshotの取得時に最新mainを確認した（unified merge 1154 = 7aaa7d83/625b0e0c の二重独立実行済み、cost-70c warm batch-3 証明書4件が公開された直後）。`AGENTS.md`・`research/knowledge/README.md`・K0783の最新版を確認した上で本作業を実施した。

## 1. bit-20 truncated pushの全数再push

前回実行でbit-20証明書（root `00000000000000809102000000100008`）が **63,965バイト（1,770行）で途中切断したまま着地**していた（e36a6b3a。64KB capのあるpaged readerを経由したcontentの長さassert前にpushした事故）。本実行は全1,741,046バイト（48,171行）を再pushし、remote git blob sha `8111cff29c3f0d3d2ef66e9e64e64a8b0968c453` がlocal計算と一致することを確認した。事故の簿記は証明書記録JSONに `incident_bit20_truncated_push` として記録した。

## 2. 証明書5件の公開（bits 20/44/68/69/118）

cost-69f sweep（9 WIN7-D10）のうち5件をrepo形式の証明書として公開した。抽出はrepo-verbatim `class4_child1_cert_extractor_exact.ts`・kill table `{}`（blind）・FBS 1<<20、loser側の初手は `legal_candidates.py` の全合法手展開。行はLC_ALL=C相当のbyte順でsort、`fbt_drops` 0全件。

| bit | root hex | 行数 | 抽出節点 | sub-roots | 終局 | md5 |
|---|---|---:|---:|---:|---|---|
| 20 | `00000000000000809102000000100008` | 48,171 | 12,532,657 | 56 | 13..17 | `8b749069…` |
| 44 | `00000000000000809102100000000008` | 49,220 | 17,969,541 | 55 | 13..17 | `2b496240…` |
| 68 | `00000000000000909102000000000008` | 47,977 | 11,305,750 | 58 | 13..17 | `d77201b6…` |
| 69 | `00000000000000a09102000000000008` | 35,501 | 11,977,137 | 51 | 13..17 | `f86e1394…` |
| 118 | `00400000000000809102000000000008` | 52,480 | 16,075,742 | 54 | 13..17 | `7e4812d5…` |

**BigInt独立検証（cofactor展開・浮動小数点なし）を5件全て再実行しPASS**: 全sub-root（=rootのloser mobility 56/55/58/51/54）が行集合を過不足なく消費（union 0/0）、終局石数13..17、行sorted-unique。loser mobilityは `legal_candidates.py`（独立Bareiss 4×4）の列挙と完全一致。v15 anchor（`class2-lane-cost69f-v15-crosscheck-20261115.jsonl`）は9 WIN7全件 `loss=true` で節点数も記録どおり（bit-20は8,760,558等）。全5件のremote git blob shaをdir listingと照合した。

残り4件（bits 2/94/109/119）は証明書抽出が未了。raw sweep + audit + v15/v16制御は既にmainにあるため、本foldではraw receiptとして処理した。

## 3. 9 receipt fold — chain head 1,163

`recompute_frontier_cost69f_receipts_20261115.py` でunified merge 1,154をbaselineとしてfoldした。

**baseline再現**: runpyチェーン（full→…→cost75c→…→unified merge）を通し実行し、1,154/6,693/527,949/4,963/391,672を再現。再生unified head JSONのgit blob shaがmain値 `a0789eedd5b81d1c9ea96220acfb487f38e70e08` と一致（byte-identical）。child `00000000000000809102000000000008`（cost 69）がbaselineで本当に残存していることをassert。

**入力検査**: sweep-audit JSONを9 raw batchから独立再導出（候補bit列・pilot 3,402×9・判決数・節点和112,752,229・batch blob sha・root == child | 1<<bit）。v15 anchor（9 WIN7 `loss=true`・REFUTED anchor 99/112 `loss=false`・pilot 5,949×3）とv16 determinism rerun（bits 2/118 node-exact・anchor 112）をJSONLからassert。証明書5件はlocal bytes×md5×sha256×git blob sha×行sorted-unique×sub-roots==mobility×union 0/0×terminal 13..17×v15節点照合で検査。

**fold結果**（公開bit順 2, 20, 44, 68, 69, 94, 109, 118, 119）:

| bit | marginal | in-manifest | marginal manifest hex |
|---:|---:|---:|---|
| 2 | 6 | **2** | `…80120200000000180`（+child `…8091020000000008`） |
| 20 | 4 | 0 | （事前被覆 — 正の重複照合） |
| 44 | 5 | 1 | `…8012420000000080` |
| 68 | 5 | 1 | `…9090020000000008` |
| 69 | 5 | 1 | `…a090020000000008` |
| 94 | 5 | 1 | `…20003810000008000000` |
| 109 | 5 | 1 | `…20003800000008000200` |
| 118 | 5 | 1 | `…20003800000108000000` |
| 119 | 5 | 1 | `…20003800000008200000` |

合計 **+9 manifest軌道**。bit-20はmarginal-0（その7個のremoval軌道が全て既被覆）— 正の重複照合として記録。最初のreceipt（bit 2）がchild軌道を閉鎖したことをassertし、fold後にchildが親のremainingから消えたことを確認した。

**新chain head: 解消S6 1,163・unique残り6,684・費用527,280・open需要4,954/391,003**（残りS5軌道175）。ヒストグラム `c2=2,c4=0` は1,034→1,025。親S5 `00000000000000809102000000000000` は **7軌道・519不変**（childの69が消えた）。

**制御**: 2回実行byte-identical。push後、4ファイル（スクリプト・frontier JSON・ranking CSV・top-candidates CSV）のremote git blob shaがlocal生成物と一致することを確認した（初回pushで末尾に紛れ込んだ1バイトの余分な改行を検出し、byte-exact版でrepush済み）。

## 4. 未fold・次回material

- cost-70c warm batch-3証明書4件（bits 3/42/86/103、claim closure 6751e21e/267762ab）— 本foldでは未処理。次のrecomputeでfoldする。
- cost-65j sweep（in flight）— bit-113 WIN7が見つかった場合、このchildと軌道を共有するため交叉被覆を再検査すること。
- 残り最安未sweep子は `00000000000000809102000000002000`（cost 69、需要c1=0,c2=2,c4=2）。
- 69f残り4証明書（bits 2/94/109/119）の抽出。

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き **UNKNOWN**。

成果物: [frontier JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost69f-receipts-recompute-20261115.json)、[ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost69f-receipts-20261115.csv)、[top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost69f-receipts-20261115.csv)、[foldスクリプト](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost69f_receipts_20261115.py)、[証明書記録JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-win7-certificates-20261115.json)、[証明書5件](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-certificates/)。
