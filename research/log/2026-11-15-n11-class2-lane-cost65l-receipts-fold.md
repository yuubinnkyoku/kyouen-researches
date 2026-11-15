# 2026-11-15：cost-65l receipts fold — canonical head 1257 → 1261（stale fence 1227からのrebase・class-2/class-4二重需要childの着地）

開始時main: HEADは73h fold着地後（`568575d6` 修复込み）。本foldのsweep・証明書・claim v1（fence baseline 1227）は以前のセッションで完了済みだったが、70g・73h両foldが先に着地したためfenceはstaleになり、**canonical head 1257へのrebaseが必須**だった（73h logの最後に明記済み）。baseline: cost-73h chain head **1257/6590/520380/4860/384103**（`class-frontier-cost73h-receipts-recompute-20261115.json`・blob `71f79b4b`）。本セッションはrebaseした上でfold実行・claim v2まで実施した。

## このfoldの特殊事情：class-2/class-4の二重需要child

65lのchild `00000000220000003800000000000200`（cost 65・stones [9,59,60,61,89,93]）は**class-2とclass-4の双方に需要を持つ**特殊な行（demand c1=0, c2=1, c4=1）:

- **del89 → parent1（class-2）**: 第2 coverable class-2 target S5 `00000000000000801202000000200000`（D4-canon）。
- **del93 → class-4 S5 `00000000020000003800000000000200`**（D4-canon）。73hのparent2 `0000000000000038002000080000000`とは別親。
- 残り4削除（del9/del59/del60/del61）は閉行（両親ともに非開）。

rebase controlとして、head 1227→1257の7 fold分の進展の後でも**childはgenuinely remaining**（manifest内かつ未解決）・**class-2親は31行→18行/1390に縮小してもchild行を保持**・**class-4親は77行/5655で無傷**であることをfold script内でassertした。rebaseが結果に与える影響はbaseline数値のみ。

## fold scriptと統制

`recompute_frontier_cost65l_receipts_20261115.py`（73h/70g版を雛形・blob `01a73f2f`）を書き、**3回連続実行すべてbyte-identical**を確認。統制:

- **baseline再構成**: 70g fold scriptを起点とするrunpy鎖（70g→73h→65l。1257 head JSON blob `71f79b4b`・両CSVともblob-identical再生成）。
- **入力検証**: 17 published cost-65l input files（8 raw batches・determinism rerun・v15 crosscheck・extraction summaries 2件・BigInt cert-verify records 2件・parent-lift analysis・証明書single files 2件）をgit blob shaでbyte-exact検証。claimsは内容検証。
- **child/両親の再検証**: child genuinely remaining・demand c1=0,c2=1,c4=1再導出・開な1石削除は2親のみ・D4-canon lift対応。
- **sweep再導出**: 65候補一度ずつ（claim列挙とaudit batch planの両方に一致）・2 WIN7-D10 [21, 48]（nodes {21: 712,251, 48: 882,679}）・63 REFUTED-D10・0 capped・総nodes 44,268,335・pilot 3402×8・determinism rerun batch-2 node-exact・v15交差 2/2 WIN node-matched（1,772,664 / 2,492,516）+ REFUTEDアンカーbit54（raw verdict一致）・全65候補 terminal [13,17]。
- **証明書検証**: 2証明書の実bytes検証（git blob sha == fold claim receipts `6cdd6d0d`/`06bc8da7`・rows sorted-unique 28,523+31,817=60,340・extraction summaries per-move ok/uncapped・per-move terminalRangeは[13,17]の部分集合（[13,15]/[15,17]を含む正しい挙動）・BigInt verify records union 0/0・sub-roots 51+50（loser mobility一致）・extraction nodes 3,110,330+4,694,247=7,804,577再総和・parent-lift analysis cross-check）。
- **root-orbit簿記**: 2新root vs **532 fold済みroot**（520 through 73g + 8 70g + 4 73h）raw-hex disjoint・2新D4 orbitはfold済みrootのD4 canonと重複なし（fence v1の121-root統制より大幅に強い）。

## fold結果

公開順 [21, 48] でfoldし、**総marginal 10・in-manifest 4**（zero-mim/zero-marginalなし）:

| bit | root hex | covers | marginal | in-manifest | marginal manifest hexes |
|---|---|---|---|---|---|
| 21 | `00000000220000003800000000200200` | 7 | 5 | 2 | child `00000000220000003800000000000200`, `00000000220000003800000000200000` |
| 48 | `00000000220000003801000000000200` | 7 | 5 | 2 | `00000000000000403800000008800000`, `00000000020000003801000000000200` |

- **child orbit `00000000220000003800000000000200` はbit21（公開順最初）で閉鎖**。set等式 `s_after == s_1257 UNION covers(2 roots)` 統制PASS。
- **class-2親（第2 coverable target S5 `00000000000000801202000000200000`）はchild行のみ喪失し 18行/1390 → 17行/1325**。
- **class-4親（`00000000020000003800000000000200`）はchild + bit48 marginal由来の1行 `00000000020000003801000000000200` を喪失し 77行/5655 → 75行/5519**。喪失行はすべてcovers内。
- **fold後 head: solved 1261 / unique 6586 / cost 520,097 / open 4,856 / open_cost 383,820**。両S5親ともまだ多数のrowを残し未解決。

## push

5ファイル（fold script・head JSON `0b523e70`・ranking CSV `af64bbe3`・top-candidates CSV `1b2b66fe`・claim v2 `dea8bd08`）を単一コミット `97d99a11` でpush、remote raw CDNで照合（3出力blob一致・script cmp一致）。claim v2（schema `n11-class2-lane-cost65l-fold-inflight-20261115-v2`・status completed）のfold recordはfold scriptのsection 9が再assert（実行確認済み）。

なお本セッションでは、K0783のpush時に`tools.file_system.read_file`の約64KB/呼び出し制限でbyte切り詰めが発生したインシデント（約200KB損失）をchunked read + remote照合で修復した（commit `568575d6`）。以後の大きなファイルのpushはchunked readで連結し、push後にremote byte長+cmp照合を必須とする。

REFUTED-D10はLOSS証明ではなく、2証明書は個別7石rootの深さ10以内の先手勝ちのみを証明する。solved 1261はmanifest被覆の簿記であり盤全体の勝敗ではない。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class1・class2・class4は引き続きUNKNOWN**。次のfold baselineはhead **1261**。69g/65j/74e/74g並走中。

詳細: [head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost65l-receipts-recompute-20261115.json)、[claim v2](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65l-fold-inflight-20261115.json)、[ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost65l-receipts-20261115.csv)、[top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost65l-receipts-20261115.csv)。
