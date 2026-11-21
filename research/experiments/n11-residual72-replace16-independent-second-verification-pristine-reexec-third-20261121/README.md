# replace16（K1089）独立第二検証のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 [note](../../../log/2026-11-21-n11-replace16-second-verification-pristine-reexec-third-single-owner-note.md)〔commit `19c4eea1774c972c93ba38e58be9476ae39a809e`・宣言 2026-11-21T06:2xZ・受入条件5項目・erratum織込み修正版受入条件3・先行宣言の不在を機械列挙で確認〕+ [addendum](../../../log/2026-11-21-n11-replace16-second-verification-pristine-reexec-third-single-owner-note-addendum.md)〔commit `f89d5ae6`・宣言文中のgainsHist例示値誤記の訂正〕）

## 位置づけ

replace16（K1089・残余72行の代替16根掃引・16 gate・出版正本 `808fbda1…`）に対する独立第二検証（commit `45a3f3b2b1394fc259ba3269b0a11b37fab20a57`・2026-11-20T00:44:22Z単一コミット出版・README `e304a654…`〔1,691 bytes〕/検証機 `c43ab3ac…`〔9,270 bytes・純stdlib・16 gate・別実装D4変換と4×4整数行列式で16根1,120四点組・72基底行1,080四点組を再検査〕/監査 `1486d35e…`〔5,728 bytes〕+K1093 item+研究log）を、出版社レーン以外の第三の実行環境（本sandbox）が**出版byteのみから再取得してpristine再実行・erratum確定・tamper・監査byte決定性を第三検査する**。residual72系の第三検証はresolve7（K1190）に続き、**replace16分の第三検証は本実験が初号**。本対象は16 gate・検証機1回約0.2秒のn11検証ラティス最小級である。

## 対象・固定pin

| file | bytes | SHA-256 |
| --- | --- | --- |
| 対象README（第二検証実験dir） | 1,691 | `e304a654275b555a53a0746056b7b04a84dcc3d6b2fcd91d379a225f8542fc09` |
| 対象検証機 `verify_replace16_second_20261120.py` | 9,270 | `c43ab3ac2cd89a36a6ed2a47149d36e2eaf69da54cfd2912ec9caf3054a007d9` |
| 対象監査 `output/audit.json` | 5,728 | `1486d35e8740a594ec54f683eb36996967056d0b5fedeafe07db7da663a42949` |
| K1093 item（出版記録・機械入力ではない） | 2,311 | `00d2c4cacb0670ebd2df67966be4a328f525201af8f93757a34273e3385d7a83` |
| 対象研究log（出版記録・機械入力ではない） | 1,177 | `ee4d947dd885e8149df9264ed091824742861bc22f39acf1aca66105dd05d24a` |
| 宣言ノート | 10,990 | 宣言commit `19c4eea1` で fetch-back byte一致確認済み |
| 宣言addendum（gainsHist例示値誤記訂正） | 2,021 | addendum commit `f89d5ae6` で fetch-back byte一致確認済み |

3つの機械ファイルはpin commit `45a3f3b2` のraw pinned URLから取得（api.github.com非依存）。宣言時現main HEAD `4c3dd3af` で3ファイルともpin byteと一致した。

## W入力（5点の出版正本・検証機内pinと一致必須・fail-closed）

| 正規名 | bytes | pin |
| --- | --- | --- |
| `K1085` unsafe-classification-add2stones | 39,221 | SHA-256 `5fdd342d624abec9b8478b69b13fc63a2dbbec99d227da4740cfe068647e688e` |
| `K1086` addtwo-greedy23-d10-sweep | 21,835 | SHA-256 `3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced` |
| `K1088` safe8-refuted16-refsolve | 46,123 | SHA-256 `16b38d04a488617b1b8c002c6a5f3171038f557cd3cca8b8e4dbd4657bc2f724` |
| `K1089` replace16-d10-sweep | 17,511 | SHA-256 `808fbda1152cb492bb76641a101660f965f2801c0b74790d20a0d998d5b747fc` |
| `runner_v17.ts` | 12,481 | SHA-256 `192903714b1b06a8ea58aa80e22da23fcf9d9ef175830a65a0da5eb0ca64f3d4`・Git blob SHA-1 `c132cc6425eee3feaeef1d697dd74f968cfedb59`（検証機はblob SHA-1 pin） |

第三検証では ref_a = 宣言時HEAD `4c3dd3af58b9273de8e10892fb3be143e9a66228`・ref_b = 宣言commit `19c4eea1774c972c93ba38e58be9476ae39a809e` の2参照で固定する。検証機は合成tree（ROOT = 検証機fileのparents[3]）上の正規pathで読む。

## 実施内容と結果（harness `scripts/verify_replace16v_third_20261121.py`）

harness: `scripts/verify_replace16v_third_20261121.py`（SHA-256 `e8a1431a036246b7da8f42ffe30bf81534487d47b12a2fc83376afa25e9affd9`・18,919 bytes・stdlibのみ・stage分割 pin/recon/rerun/erratum/tampers/finalize・fail-closed・時刻/絶対path/volatile排除のbyte決定的監査JSON出力）。

- **pin**（gate 9）: 対象3ファイル（README・検証機・監査）をpin commit `45a3f3b2` のraw pinned URLから取得しSHA-256+byte数を照合（6 gate）し、さらに宣言時HEAD `4c3dd3af` の同3ファイルがpin byteと一致することをbyte比較（3 gate）（計9 gate all PASS）。
- **recon**（gate 22）: W 5入力を2参照（ref_a・ref_b）のraw pinned URLから取得し、各SHA-256が機械pinと一致・ref間byte-identical・合成tree正規path配置後に再照合（5点×4 gate）+ runner Git blob SHA-1 pin照合（1）+ 検証機本文の合成tree配置後再照合（1）（計22 gate all PASS）。
- **rerun**（gate 23）: 出版検証機を改変なしpristine再実行4回/battery（r1/r2 同一合成tree・r3 隔離copytree+隔離env PATH/HOME/TMPDIR・r4 r3+`PYTHONHASHSEED=random`）。各回 rc=0・stdout `PASS 16/16 roots=16 rows=49 probes=32 nodes=6339079`・出力監査が機械master `1741ca0114c244ed6aa5e61b91d48593acbf4cc18cc5f66673f2dc38c43bb1bb`〔5,730 bytes〕とbyte-identical・4回間でbyte一致（x4 5gate相当+相互3 gate、計23 gate all PASS・検証機1回約0.2秒）。
- **erratum**（gate 10）: **出版監査 `1486d35e…`〔5,728 bytes〕は出版検証機からbyte再現不能であることを機械確定**。差分は正確に2箇所のみ: (a) `replacement-gains-histogram-reproduces` の `gainsHist` キー順〔出版はソート順 `"2","3","4"` vs 機械は挿入順 `"4","3","2"`・値は同一 `{"2":2,"3":11,"4":3}`〕・(b) `interpretation_guard` 最終文の文末句点〔出版 ASCII `.` vs 機械 `。` U+3002・それ以外文同一〕。その他の全構造〔checks 16 gate・summary・inputs・runner〕が意味完全一致であることをcanonical化比較でassert（計10 gate all PASS）。**検証数値〔16/16 gate・roots=16/rows=49/probes=32/nodes=6,339,079〕はすべて第三環境で同一再現しており、本erratumは監査jsonの同定問題であって検証の失敗ではない**。
- **tampers**（gate 11）: 本レーン選択offsetの1 byte XOR 0x20（既知の全レーン探針位置 @{12,345,1,234,567}/{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}/{7,777,500,000}/{253,17,522}/{1,234,17,522,4,096}/{117,777,777,777}/{5,077,28,081}/{208,888,919,191}/{300,111,740,321}/{2,345,23,456} のいずれとも別位置）、**監査不在のfresh tree**（rerun後監査を除去し事前不在をassert）で実施:
  - t1 `K1086` @5,678〔21,835 bytes内〕→ rc==1・stderr `K1086 SHA-256 mismatch: 28e251b7dd5b571d3cdf65081b3a7b5cc1100479803179988cd005a8e3f9ad10`〔改変後SHA-256〕・監査未書込・本番tree W無改変。
  - t2 `K1089` @9,012〔17,511 bytes内〕→ rc==1・stderr `K1089 SHA-256 mismatch: afb504844db6f1e255baca9f92487401ac4a613e7f672dc856e90e5c07dddde9`・監査未書込・本番tree W無改変。
  - 2つのstderrは互いに異なる入力名と改変SHAを特定し、**K1086/K1089の2入力pin gateが互いに独立して発火する**ことを1 battery内で実証（harness gate `tamper-independent-errors`）。**readpの最初のSHA不一致でSystemExitし監査JSONを一切書かない強fail-closed**（fold10 ext2第三検証のgate-failed書込型と対照。第三検証の実験事実として記録）。
- **finalize**: 監査正本 **10,189 bytes・gate 75〔pin 9・recon 22・rerun 23・erratum 10・tampers 11〕・all_gates_pass true・解釈ガード5文+unknown guard**・SHA-256 `569c6bbda909d4f3993ffaee64395d9a62911e7cddb49added51abb87393e545`。**3 battery**（B1 fresh base全stage〔1.7s〕→B2 同一base全stage再実行〔pin再取得込み・1.1s〕→B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd〔1.3s〕）で**byte-identical**（`cmp`完全一致）。

## 実験事実

1. **出版監査のerratum確定**: replace16第二検証の出版監査json（`1486d35e…`）は出版済み検証機（`c43ab3ac…`）+pin済みWからはbyte再現不能であり、差分は2箇所のみ〔gainsHistキー順・最終guard文末句点〕で数値・構造は全一致。出版監査はファイナル前ビルドの出力と推定される。一方で**検証内容自体（16 gate・全再検査数値）は第三環境で完全再現**しており、第二検証の結論は影響を受けない。宣言ノート本文中のgainsHist例示値（`{"2":2,"3":1,"4":3}`）の誤記はaddendumで訂正した（正 `{"2":2,"3":11,"4":3}`）。
2. replace16第二検証機はresolve7第二検証機と同じ設計（最初のpin不一致で即SystemExit・監査不書込）の強fail-closedであり、K1086/K1089の2入力pin gateは独立に発火した（fold10 gate-failed書込型との対照は3設計目の実測として累積）。
3. n11検証ラティス最小級（検証機1回約0.2秒・battery 1巡約1.1〜1.7秒）で、erratum確定込みの独立再現性・入力pin独立性・監査byte決定性が第三環境から独立検証可能。

## 解釈規約（不変）

本第三検証はreplace16独立第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性（および監査jsonのerratum確定）の第三検査であり、探索・根の新規判定・行の閉鎖・候補universe再構築・receiptの再発行は一切行わない。nodes数・solved数・coverage数を勝敗として読まない。WIN8-D10 candidateは証明書ではない。REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 再現

```sh
python3 research/experiments/n11-residual72-replace16-independent-second-verification-pristine-reexec-third-20261121/scripts/verify_replace16v_third_20261121.py <base_dir>
# battery: B1 fresh base → B2 同一base再実行 → B3 隔離base+env -i 隔離HOME/TMPDIR+PYTHONHASHSEED=random+別cwd
# 監査: <base_dir>/output/replace16v-third-harness-audit.json（byte決定的）
```
