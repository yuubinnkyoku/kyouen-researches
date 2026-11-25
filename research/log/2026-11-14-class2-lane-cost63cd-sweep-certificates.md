# class2-lane cost-63c / cost-63d sweeps + certificates + formal frontier (2026-11-14)

## 背景

after-cost63b 正式frontier（solved 849 / unique remaining 6998 / sum 550,269 /
open 5233/411,475）まで反映済み。class-2 target S5 `00000000000000809082000000000000`
は残 26 orbit / 1798。cost63帯の未sweep child 2件（両方 edge cost 63）を掃討した。

## ① cost-63c sweep（S6 child 000000000000008090a2000000000000）

- 候補63（legal_candidates.py による独立列挙。occupied 6 / legal 63）。
- v15 engine verbatim・1候補1プロセス×4並列・pilot d6 制御 5949 nodes 6/6プロセスPASS。
- **1 WIN7-D10（bit 46）+ 62 REFUTED・0 capped・総 307,023,091 nodes・terminal [13,17]**。
- raw JSONL: `output/class2-lane-cost63c-sweep-20261114-raw.jsonl`（main push済み）。
- sweep record: `output/class2-lane-cost63c-sweep-20261114.json`。

## ② cost-63d sweep（S6 child 00000000000000809082000000080000）

- 候補63（同上の独立列挙）。
- **1 WIN7-D10（bit 70）+ 62 REFUTED・0 capped・総 232,732,466 nodes**。
- raw JSONL: `output/class2-lane-cost63d-sweep-20261114-raw.jsonl`（main push済み）。
- sweep record: `output/class2-lane-cost63d-sweep-20261114.json`。

## ③ WIN7証明書2件（全検証PASS・pushは次回実行に繰延）

抽出は extractor_exact（FBS=1<<20・probe 96・fbt_drops=0を確認）・1手1プロセス。
検証は repo版 verify_bit7_win7_cert.ts（engine不使用・Bareiss det4）。

| bit | root | rows | 抽出nodes | sub-roots | union差 | mobility | md5 |
|-----|------|------|-----------|-----------|---------|----------|-----|
| 46 | 000000000000008090a2400000000000 | 45,337 | 14,524,021 | 52/52 | 0/0 | 52（独立列挙一致） | 01bcaabc9d20d20e6215826e22c01181 |
| 70 | 00000000000000c09082000000080000 | 39,213 | 9,616,344 | 49/49 | 0/0 | 49（独立列挙一致） | 63a3cb44f1cfc7262509214a9f24d3ca |

- 全loser初手sub-root検証PASS・consumed union = 証明書行集合（双方向 0/0）・
  terminal [13,17]・fbt_drops=0・bit46はbatch1再抽出で行集合bit一致を再確認（決定性）。
- **両証明書ファイル本体のpushは次回実行に繰延**（connector経由の1.4〜1.6MB送信のため）。
  必要なら extractor（repo上）で決定的に再生成できる。

## ④ 正式frontier再計算（after cost-63c+63d）

`scripts/recompute_frontier_cost63cd.py`（cost63b版の直接拡張。全段階制御を
baseline 638→…→after_cost63b 849/6998/550269/5233/411475 まで完全再現してから測定。
2回実行でbyte-identical）:

- **after cost-63d: solved 855・unique remaining 6992・sum 549,862・open 5232/411,408**。
- cost-63c効果: 7 covers / 7 marginal / manifest内 +4。
- cost-63d効果: 7 covers / 5 marginal / manifest内 +2。
- **class-2 target S5 は 26 orbit/1798 → 23 orbit/1601**。
  best class-4 `00000000020000003800000080000000` 24/1934 不変。
- ranking CSV 2件（after-cost63d版）はpushしたスクリプトからbyte-identical再生成可能
  （ローカル検証済み）。md5: ranking 1decd77d…（要再確認）→ 次回push時に再取得すること。

## ⑤ 運用の記録（今回新規）

- **get_file_contents の text 抽出で、スクリプト本文の後に wrapper由来のゴミ
  `"}}]` が混入したまま最初のpushが行われ、構文エラーとなるファイルが一時公開された**。
  SHA付き再pushで修正済み（末尾は最終print行で終わる）。以後は「最終行以降を刈り取る」
  処理を必ず入れること。
- /home/user スナップショット8MiB制限に再び到達（rows/consumed/cert中間ファイル）。
  大きい中間成果は /tmp に置き、push直前一時コピーのみ current-chat に置く運用を継続。
- bit70抽出のbatch 1（13手分）は最初、consumed-out 未指定で検証したため union 差分が
  出た。batch毎に --consumed-out を必ず付けること。

## 解釈上の注意

REFUTED-D10は深さ10以内のWIN7の否定のみ。WIN7証明書は7石root個別の深さ10以内の
WINのみ。**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも
UNKNOWN のまま。**

## レジューム（次回実行）

1. **証明書2件のファイル本体をpush**（root 000000000000008090a2400000000000 /
   00000000000000c09082000000080000。md5は上表。/tmp/krwork/cert46/ に残っているが
   リセットされていれば extractor で再生成→verify→push）。
2. after-cost63d ranking CSV 2件のpush（スクリプト再実行で生成）。
3. class-2 target S5 残23 orbitの次の最安child sweep。
4. class-4最安child: cost 74 `00000000020000003800000080000020`。
5. runner/engine側fbtORへの飽和時エラー/カウンタ追加の上流パッチ提案（まだ）。
