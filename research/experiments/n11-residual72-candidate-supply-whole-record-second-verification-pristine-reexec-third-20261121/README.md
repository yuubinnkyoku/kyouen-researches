# candidate-supply whole-record（K1075正本側）独立第二検証のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 [note](../../../log/2026-11-21-n11-candidate-supply-whole-record-second-verification-pristine-reexec-third-single-owner-note.md)〔commit `9e7ac2a1fe6233ca1913acb4b495f8c5f64b7496`・宣言 2026-11-21T07:xxZ・受入条件5項目・受入条件3の根拠となる出版監査byte再生性を宣言前に予備実測・先行宣言の不在を機械列挙で確認〕）

## 位置づけ

K1075（残余72行のfull cache-join候補供給再構築・出版正本 `49b6f85f…` 54,282 bytes）の**whole-record経路の独立第二検証**（87 gate: 生4-worker probe corpusからのK1069 live sweep分類再構成・K1059 dead sweep REFUTED-D10再構成・resolve6値同一性・fold鎖/frontier数値・join統計・phase-2供給解剖・resolve7クロスレーン整合）を、出版社レーン以外の第三の実行環境（本sandbox）が**出版byteのみから再取得してpristine再実行・tamper・監査byte決定性を第三検査する**。対象は commit `3e0d2df9af0361fa73e000724ea5a0c458517250`（2026-11-19T21:55:31Z単一コミット出版: README `69db6635…`〔9,065 bytes〕/検証機 `k1075_second_verification.py` `f808279d…`〔35,127 bytes・純stdlib・87 gate〕/監査正本 `753f9a07…`〔16,462 bytes〕+研究log `9724e961…`〔3,331 bytes〕。出版社レーンの単一オーナー宣言ノートが2026-11-20に先行出版済み）。residual72系の第三検証は4-sweep（K1144）・replace9 sweep/whole-record・verdict-sweeps・resolve7（K1190）・replace16（K1191）・36root-three-ply frontier（K1192）に続き、**candidate-supply whole-record分の第三検証は本実験が初号**。本対象は87 gate・検証機1回約0.07秒の軽量・W 15入力の対象。幾何レーン（44 gate・D4/Bareiss）の再検査は行わない。

## 対象・固定pin

| file | bytes | SHA-256 |
| --- | --- | --- |
| 対象README（第二検証実験dir） | 9,065 | `69db6635a0eb178047573f71c8067776cbd8964ae1b4da9736adcb7aa76c277b` |
| 対象検証機 `scripts/k1075_second_verification.py` | 35,127 | `f808279d82927ed7ab8abdeedb6a266c75537490edf2e2fe7b2fa231b0cc0847` |
| 対象監査正本 `output/candidate-supply-whole-record-second-verification-20261120.json` | 16,462 | `753f9a07599525ae17eb66cb1a72f59164d995190d50b182bf26a6e7f07f9de9` |
| 対象研究log（出版記録・機械入力ではない） | 3,331 | `9724e961ffdd2df702b9f100fdb21cbc36b9bb2e574d073563a55abc50ffe9f0` |

4ファイルはpin commit `3e0d2df9` のraw pinned URLから取得（api.github.com非依存）。宣言時現main HEAD `5487dad0` で4ファイルともpin byteと一致した。

## W入力（15点の出版正本・検証機内SHA-256 pinと一致必須・fail-closed）

| 正規名 | bytes | SHA-256（機械pin） |
| --- | --- | --- |
| k1075.json（K1075正本） | 54,282 | `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa` |
| resolve5.json | 31,099 | `5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e` |
| resolve6.json | 34,984 | `e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a` |
| fold9.json | 24,399 | `24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2` |
| fold10.json | 12,918 | `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a` |
| sv17.json | 9,713 | `c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc` |
| sweep39.json | 5,097 | `22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc` |
| sweep39dead.json | 38,166 | `f8608d0a04a132012f0aa692099cebe851cdf261a3ea916dc4c15d6841fc5246` |
| resolve7.json | 19,817 | `207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f` |
| r7second.json | 21,842 | `4286100804d82376418066da89167c50017244f2c6f02b81ad76a07b45bd91d6` |
| roots.json | 9,231 | `9f0161a8a61d311534fd3a4035b1c367426691c72ad5eb44efd01a5fae37e0cc` |
| probes-w0.jsonl | 13,206 | `6b045eaefdd59e2c0fbd0f9b4a1e876b89c3f8b03cfade8f0ab1f8192cd0a984` |
| probes-w1.jsonl | 13,221 | `4aaa4d0a691f6da40e68dbaa41a353aaf3ea518a6863aec04886c17197e00967` |
| probes-w2.jsonl | 11,266 | `2d4ff7dd40b2fc66745068f6772724f38ccd04dd2a65507af925fb85252b3032` |
| probes-w3.jsonl | 10,293 | `e04e20bdadd1cba94cd0a285ff9fb72bb9e9d0a2d5a687f1d76ceccc7d0ccb0c` |

第三検証では ref_a = 宣言時HEAD `5487dad0442b9744a4206ceef7a026a2946c97d5`・ref_b = 宣言commit `9e7ac2a1fe6233ca1913acb4b495f8c5f64b7496` の2参照で固定する。roots.jsonは `n11-residual78-39livewitness-depth10-sweep-20261120/` 直下・probe記録は同dir `output/probe-records-w{0..3}.jsonl`。

## 実施内容と結果（harness `scripts/verify_k1075_third_20261121.py`）

harness: `scripts/verify_k1075_third_20261121.py`（SHA-256 `14857ca9071f248e27fb4d6a96336089c22c710a16da66533f99404c20c0ba1a`・18,523 bytes・stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・時刻/絶対path/volatile排除のbyte決定的監査JSON出力）。

- **pin**（gate 12）: 対象4ファイル（README・検証機・監査正本・研究log）をpin commit `3e0d2df9` のraw pinned URLから取得しSHA-256+byte数を照合（4点×2 gate）し、さらに宣言時HEAD `5487dad0` の同4ファイルがpin byteと一致することをbyte比較（4 gate）（計12 gate all PASS）。
- **recon**（gate 61）: W 15入力を2参照（ref_a・ref_b）のraw pinned URLから取得し、各SHA-256が検証機内pin（`sorted(PINS)`読み取り順: fold10→fold9→k1075→probes-w0..3→r7second→resolve5→resolve6→resolve7→roots→sv17→sweep39→sweep39dead）と一致・ref間byte-identical・合成input_dir正規名配置後に再照合（15点×4 gate）+ 検証機本文の配置後再照合（1 gate）（計61 gate all PASS）。
- **rerun**（gate 23）: 出版検証機を改変なしpristine再実行4回/battery（r1/r2 同一base・r3 隔離copytree+隔離env PATH/HOME/TMPDIR・r4 r3+`PYTHONHASHSEED=random`）。各回 rc=0・stdout `gates 87 all_pass True faithful True`・出力監査が出版正本 `753f9a07…`〔16,462 bytes〕とbyte-identical・4回間でbyte一致（x4 5 gate+相互3 gate・計23 gate all PASS・検証機1回約0.07秒）。**出版監査byte再生成立（erratumなし・replace16 K1191の「出版監査byte再現不能」型と対照的）**。rerun受入はbyte一致条件で確定（宣言前予備実測でbyte再生性を確認済み・K1191運用の適用例）。
- **tampers**（gate 15）: 本レーン選択offsetの1 byte XOR 0x20（既知の全レーン探針位置 @{12,345,1,234,567}/{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}/{7,777,500,000}/{253,17,522}/{1,234,17,522,4,096}/{117,777,777,777}/{5,077,28,081}/{208,888,919,191}/{300,111,740,321}/{2,345,23,456}/{5,678,9,012}/{51,234,8,765} のいずれとも別位置〔@33,333/@44,456〕）、**監査不在の探針環境**（probe-local出力pathの事前不在+事後不在をassert）で実施:
  - t1 `sweep39dead.json` @33,333〔38,166 bytes内〕（読み取り15番目=最終）→ rc==1・stdout空・stderr末行 `pin mismatch for sweep39dead.json`・監査未書込・本番input W無改変。
  - t2 `k1075.json` @44,456〔54,282 bytes内〕（読み取り3番目）→ rc==1・stdout空・stderr末行 `pin mismatch for k1075.json`・監査未書込・本番input W無改変。
  - 2つのstderr文言は互いに異なる入力を特定し、**sweep39dead正本とK1075正本の2入力pin gateが互いに独立して発火する**ことを1 battery内で実証（gate `tamper-independent-errors`・t1は読み取り15番目〔最終〕・t2は3番目のfailで読み取り順独立性を含む）。検証機は最初のSHA不一致で `raise SystemExit("pin mismatch for <name>")`（tracebackを伴わない）となり監査JSONを一切書かない「監査不書込」型fail-closed（resolve7/replace16と同じSystemExit不書込型）。
- **finalize**: 監査正本 **14,992 bytes・gate 111〔pin 12・recon 61・rerun 23・tampers 15〕・all_gates_pass true・解釈ガード5文+unknown guard**・SHA-256 `365fbdfc81d4d642a5a047e7cf50a531ebc9ded75a5d0ce778b354f2ce421798`。**4 battery実行**（B1 fresh base全stage〔1.4s〕→B2 同一base全stage再実行〔pin/recon再取得込み・1.4s〕→B1f fresh base独立capture〔1.5s〕→B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd〔1.4s〕）すべて111/111 PASSで**監査byte-identical**（`cmp`完全一致・B1==B1f==B2==B3）。

## 実験事実

1. **出版監査byte再生の成立とK1191運用の適用例**: 予備実測1回+本battery rerun 4回/battery×4 battery（計16回+予備1回）すべて出版正本 `753f9a07…` とbyte-identical（erratumなし）。宣言前のbyte再生性予備実測（K1191で確立した運用）を経て受入条件3は当初からbyte一致条件で確定した。
2. **fail-closed設計はSystemExit不書込型**（resolve7 K1190・replace16 K1191と同型・tracebackを伴わない）: 検証機は `sorted(PINS)` 読み取り順の最初のSHA不一致で `raise SystemExit("pin mismatch for <name>")` となり監査JSONを一切書かない。stderr文言は入力名で決定的であり末行特定でgate記録可能。
3. **軽量対象の第三検査コスト**: 検証機1回約0.07秒・battery 1巡約1.4-1.5秒（pin fetch 8点+recon 15点×2参照+rerun 4回+tampers 2探針）。W 15点という多数入力でもreconはraw fetch完動で完結し、第二検証出版（2026-11-19T21:55Z）から約1.6日で第三検証確定。

## 解釈規約（不変）

本第三検証はcandidate-supply whole-record第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、探索・根の新規判定・行の閉鎖・候補universe再構築・receiptの再発行・幾何レーン（44 gate）の再検査は一切行わない。幾何censusの重複率はDFPN節点数・共有表命中率・証明状態再利用性を測るものではなく、共有表実装やworker分割変更の正当化ではない。nodes数・solved数・coverage数を勝敗として読まない。REFUTED-D10はLOSS証明ではない。witness根・候補供給は条件付きdepth-10掃引計画で証明書ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 再現

```sh
python3 research/experiments/n11-residual72-candidate-supply-whole-record-second-verification-pristine-reexec-third-20261121/scripts/verify_k1075_third_20261121.py <base_dir>
# battery: B1 fresh base → B2 同一base再実行 → B1f fresh base独立capture → B3 隔離base+env -i 隔離HOME/TMPDIR+PYTHONHASHSEED=random+別cwd
# 監査: <base_dir>/output/k1075-third-harness-audit.json（byte決定的）
```
