# 2026-11-15：cost63g の14 WIN7 receipt fold完了（head 1199 → 1216）

入力取得時main: `e039e43a`（cost63g証明書manifest着地直後）。fold実行中に並走レーンのcost65l raw artifacts（`1d08a5fc`）が着地し、top-candidates CSVの初回pushが一度だけ409競合した。最新mainを取り直して再pushし、以後の競合なし。規約どおりmainを基準にし、ブランチ・PRは作らない。

## 実施内容

`scripts/recompute_frontier_cost63g_receipts_20261115.py` を新規作成し、cost63gの14 WIN7-D10 receipt（bits 0, 9, 12, 50, 54, 58, 62, 64, 72, 94, 96, 99, 105, 113）をchain head 1199にfoldした。

スクリプトの全制御は以下のとおり、すべてPASS。

1. runpyチェーンでcost63f head `1199/6648/524616/4918/388339` を再現し、head JSON・ranking CSV・top-candidates CSVの3ファイルがmainのblobとbyte-identicalであることをassert（76a 1195 headはチェーン内部で再現済み）。
2. cost63g入力14ファイル（sweep audit、raw batch 1..8、v16 determinism rerun、v15 crosscheck、claim、証明書manifest、parent-lift影響監査）をgit blob shaでbyte-exact検証。
3. 子S6 `00000000080000801202000000200000` が1199 headで本当に未解決であることを検証（両開放親S5 `00000000000000801202000000200000` 38行/2,837と `00000000000000003800000808000000` 71行/5,281の両方が子行を保持、子はmanifest内・未解決、需要 c1=0,c2=2,c4=0 を残りincidencesから再導出、lift石 91/21）。
4. sweep auditを8個のraw batchから再導出（63候補が各1回・claim列挙と一致、14 WIN7-D10 / 49 REFUTED-D10 / 打切り0、合計75,637,935節点・WIN合計15,742,818、root == child|1<<bit、14個の異なるD4軌道、各batchにpilot 3402、batch-5 determinism rerun 8/8 node-exact）。
5. v15交差検証アンカー（WIN 14/14 loss=true、節点合計31,368,332がmanifestと一致、REFUTEDアンカー bits 1/32/116 loss=false がraw判定と一致、pilot 5949 ×5）。
6. 14証明書をローカルbytesで検証（md5・sha256・git blob sha、bit113は2 partedの結合がwholeと一致、rows sorted-unique、root同定、sub-roots == loser mobility == len(loser_first_moves)、終端[13,17]、fbt_drops 0、d4_canonical_hex == canon(root)、d4_parent_orbitsが全てcanon不変かつ各々が子を含む、v15/v16節点一致）。manifest totals再合計は419,398行 / 15,142,573 bytes / **54,670,850** extraction nodes / 667 sub-roots。claim v2/v3に記載の54,670,950はこの再合計で置き換えられる（claim retireに訂正記録を明記）。
7. 14 rootが既存98 root（96 pre-63f + 2 cost-63f）とraw hex・D4正準形の両方でdisjoint、かつ14個の異なるD4軌道。
8. 公開bit順に14 receiptをfoldし、各recordのmarginalを成長する和集合から再導出。子軌道は最初のreceipt（bit0）で閉じる。set等式 `s_after == s_1199 ∪ covers(14 roots)` を検証。並走公開済みのparent-lift影響監査の予測（対象S5 33行/2,470）とfold結果が完全一致。

## 結果

- 新canonical head: **`1216/6631/523382/4901/387105`**（solved 1199 → 1216、in-manifest marginal 17、raw marginal 73）。
- 子軌道 `00000000080000801202000000200000` はbit0 receiptで閉鎖。zero-marginal-in-manifest receiptはbit58・bit64。
- 対象S5（2番目のcoverable class-2）は **38/2,837 → 33/2,470**（parent-lift監査予測どおり5行喪失）。
- もう一方の開放親S5 `00000000000000003800000808000000` は **71/5,281 → 58/4,351**（13行喪失、子を含む）。
- 両S5 parentとも未解決のまま。fold後のbest coverable class-2は `00000000000000809102000000000000`（3行 / 221）。
- 出力: head JSON（blob `e311e24346adad570e42f145f9190fe8427ae921`, 17,292 bytes）、ranking CSV（`15eb7f9684bb715bcfa2090dc989e92b4c9b4989`）、top-candidates CSV（`77c12f798e9aa3341d1aa1e4e3481e955ebd51f6`）。2回実行でbyte-identical、claim retire（v3）後の再実行でもbyte-identical（retired claim controlがfold数値とhead blobを再assert）。
- claimはv3でretire（status completed、fold記録・訂正・出力blobを記載）。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- 証明書木そのものの再走査は本スクリプトの範囲外。証明書はmanifest記載の二重検証（BigInt独立検証器 + perm-det4 Bareiss）に依拠し、本foldはbytes・root同定・sub-roots・終端範囲・親軌道の整合を再検証した。
- cost65l（2 WIN7-D10 bits 21/48のsweep raw artifacts着地済み）、cost78a証明書、cost69g/65j/74eレーンは本foldに含めない。次のfoldは新head 1216に再基準化することが必須。

## 再現

```sh
python3 research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost63g_receipts_20261115.py
```

runpyチェーン（63f→76a→72b→74d→warm3→…）全体を再実行し、head 1199のbyte-identical再現から全制約を再検証した上でfoldする。実行時間は約3分。

## 勝敗

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、類2・類4はすべて **UNKNOWN**。今回のfoldは勝敗判定を変更しない。
