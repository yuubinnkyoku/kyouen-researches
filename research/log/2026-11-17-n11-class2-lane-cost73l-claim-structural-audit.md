# 2026-11-17：cost73l claim v1 の独立構造監査

## 開始時点

作業開始時の main は `43838dec48c863589d897a32497c59524b6be071`。最新の `AGENTS.md`、`research/knowledge/README.md`、K0023、K0863、K0865、K0868、および head-1473 census v8・cost73l claim v1 を確認した。

cost73l は6石 child `00000000000000c09002000000400000` の73候補を対象とする未実行claimで、66 open + 7 confirmation。claim v1 の次段階は depth-10 sweep と raw batch監査であり、この時点でengine結果は存在しない。

## 独立構造監査

新規スクリプト `audit_cost73l_claim_structure_20261117.py` を追加した。既存の `legal_candidates.py` や census v8 スクリプトをimportせず、K0868の整数det4式とD4変換を独立実装する。

入力は次のGit blob SHAに固定した。

- claim v1: `fa13a0ada22e3de95c06e9a3101ce6d2a738f5b1`
- census v8: `2542914e02db14a8426a1a16ef1c2cfcd9817375`

### 結果

対象childの石位置は `[22,49,60,63,70,71]`。

- K0868のdet4から生残候補73個を再導出し、claimの73個と完全一致。
- 残る42空セルはすべて、少なくとも1つの石3点組に対するdet4=0の証人を持つ。
- open 66 bitとconfirmation 7 bitは互いに素で、73候補を過不足なく分割。
- S5 parent `00000000000000403800000008000000` は、childからbit22を除いた局面のD4正準形と一致。
- census v8の選択child・parent・cost・open bits・confirmation bitsはclaimと一致。
- ranking上位1位はcost 73 / open 66の選択対象、2位はcost 74 / open 69の記録済みrunner-up。
- confirmation 7 bitすべてについて、childに当該bitを追加した7石rootのD4正準形を再計算し、claimのtransfer rootと7/7一致。
- confirmation verdictの内訳はWIN7-D10が2件、REFUTED-D10が5件で、census記載と一致。

構造検査18項目はすべてPASS。欠落候補・重複候補・open bit欠落・transfer root改変・選択child改変の5種類の破損試験もすべて拒否した。

実行確認の境界は明記する。BigIntによるJavaScript監査はGitHubから取得した完全なclaim/censusファイルを直接入力として実行した。Pythonの任意精度整数実装は、その取得内容から切り出したclaim/census構造データで正例と5種類の拒否試験を実行した。公開スクリプトはcheckout上でblob pinを検査して全監査を再実行する形にしたが、この実行環境には対象repoのcheckoutがなく、公開スクリプトそのものをrepo checkout上で実行したとは主張しない。

## 解釈境界

今回確認したのは候補集合・作業分割・親局面・転送rootの構造だけである。

- 66 open bitのdepth-10 engine sweepは未実行。
- 7 confirmation verdictの元証明書を今回再検証したわけではない。
- raw batch、per-bit node table、別プロセス決定性、v15 cross-engine照合は未確認。
- receipt抽出・foldは未実施。
- WIN7-D10は個別7石rootの深さ10以内の先手勝ちだけを意味する。
- REFUTED-D10はLOSS証明ではない。

外部計算環境も確認したが、利用可能なVMは実行環境（Node/Python/Git）が見つからず、ホスト側メモリ余裕も小さかったため、今回は長時間sweepを起動しなかった。共有環境を圧迫して未完ジョブを残すより、再現可能な構造監査を先に出版した。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべてUNKNOWNのまま。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost73l_claim_structure_20261117.py`（Git blob `fbd8cd768ad97812afbc72176acd6be2c7912b70`）
- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73l-claim-structural-audit-20261117.json`（Git blob `a9989cdd4e122c8693f44646d99fb644f28835a6`）

作業中にmainはK0900の出版修正で前進した。比較結果は開始headから最新headへのfast-forward 4 commitで、今回追加した監査スクリプトとJSONは最新mainの履歴に含まれている。branch / PRは作成していない。

## 次の作業

cost73lの所管レーンによる66 open bitのsweep完了とraw batch公開を待ち、公開後にper-bit verdict/node/cap、pilot control、重いbatchとbatch 1の別プロセス再実行、v15 cross-engine一致を独立監査する。WIN7-D10 bitだけを証明書抽出対象にし、証明書の独立検証とWIN/LOSS conflict検査が終わるまでreceipt foldは行わない。
