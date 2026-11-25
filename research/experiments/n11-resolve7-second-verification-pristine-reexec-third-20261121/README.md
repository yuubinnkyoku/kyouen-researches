# resolve7（K1072）第二検証のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 [note](../../../log/2026-11-21-n11-resolve7-second-verification-pristine-reexec-third-single-owner-note.md)〔commit `86c6d546e20b4b1809425dbdf8270700186d955a`・宣言 2026-11-21T06:10Z・受入条件5項目・先行宣言の不在を機械列挙で確認〕）

## 位置づけ

resolve7（K1072・残余72行のpost-fold witness再照合・出版正本 `207f4094…`・27 gate）に対する独立第二検証（commit `e836dd127a90e520d8e2801e62b59eb4966f0ed8`・2026-11-19T21:33:29Z単一コミット出版・README `2a9405aa…`〔5,772 bytes〕/検証機 `695e56d7…`〔29,959 bytes・純stdlib・76 gate・route A-Dの4独立経路+r7全フィールド照合〕/監査正本 `42861008…`〔21,842 bytes〕+研究log）を、出版社レーン以外の第三の実行環境（本sandbox）が**出版byteのみから再取得してpristine再実行・tamper・監査byte決定性を第三検査する**。residual72系では4-sweep（K1144）・replace9 sweep/whole-record・verdict-sweepsの第三検証が確定済みで、**resolve7分の第三検証は本実験が初号**。本対象は76 gate・検証機1回約0.07秒のn11検証ラティス最小級（PRISTINE予備実行0.07秒で出版監査正本にbyte一致）である。

## 対象・固定pin

| file | bytes | SHA-256 |
| --- | --- | --- |
| 対象README（第二検証実験dir） | 5,772 | `2a9405aacb98b1a8558e1ec1a4642776479bd9a46ac7c8c2a7b73eb5938a3ead` |
| 対象検証機 `resolve7_second_verification.py` | 29,959 | `695e56d7371e4ee974eab8aa67fab5477c7afd9c78eaabbc5c012c8501cb9773` |
| 対象監査正本 `resolve7-second-verification-20261120.json` | 21,842 | `4286100804d82376418066da89167c50017244f2c6f02b81ad76a07b45bd91d6` |
| 対象研究log（出版記録・機械入力ではない） | 4,378 | `0659272dd3e3d8bae3171f4b6cc05f8a2a1fc821034cbc6911efb49b9996dca1` |
| 宣言ノート | 8,718 | 宣言commit `86c6d546` で fetch-back byte一致確認済み |

3つの機械ファイルはpin commit `e836dd12` のraw pinned URLから取得（api.github.com非依存）。

## W入力（12点の出版正本・検証機内SHA-256 pinと一致必須・fail-closed）

| 正規名 | bytes | SHA-256（機械pin） |
| --- | --- | --- |
| `fold10.json` | 12,918 | `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a` |
| `fold10second.json` | 5,410 | `a62d6d50ffe3196ad2de1ff7b1df67ff8208b2a13510cce3f13aee0e9a085054` |
| `fold9.json` | 24,399 | `24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2` |
| `probes-w0.jsonl` | 13,206 | `6b045eaefdd59e2c0fbd0f9b4a1e876b89c3f8b03cfade8f0ab1f8192cd0a984` |
| `probes-w1.jsonl` | 13,221 | `4aaa4d0a691f6da40e68dbaa41a353aaf3ea518a6863aec04886c17197e00967` |
| `probes-w2.jsonl` | 11,266 | `2d4ff7dd40b2fc66745068f6772724f38ccd04dd2a65507af925fb85252b3032` |
| `probes-w3.jsonl` | 10,293 | `e04e20bdadd1cba94cd0a285ff9fb72bb9e9d0a2d5a687f1d76ceccc7d0ccb0c` |
| `resolve6.json` | 34,984 | `e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a` |
| `resolve7.json` | 19,817 | `207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f` |
| `roots.json` | 9,231 | `9f0161a8a61d311534fd3a4035b1c367426691c72ad5eb44efd01a5fae37e0cc` |
| `sweep39.json` | 5,097 | `22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc` |
| `sv17.json` | 9,713 | `c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc` |

`probes-w{0..3}.jsonl` と `roots.json` のpinは main@`ba5f9f4aad` 時点のsnapshot pinだが、宣言時点main（宣言時HEAD `12eefdeae…`）で12点すべてが機械pinとbyte一致することを確認済み（append-resume corpusの現況安定）。第三検証では ref_a = 宣言時HEAD `12eefdeae3198852cd0a8ca14f42457547b92773`・ref_b = 宣言commit `86c6d546e20b4b1809425dbdf8270700186d955a` の2参照で固定する。

## 実施内容と結果（harness `scripts/verify_resolve7v_third_20261121.py`）

harness: `scripts/verify_resolve7v_third_20261121.py`（SHA-256 `9d7557807f9fd500a4164d4ba0780ad5221aa8156c22ef18e5ae73a059b1fa6b`・14,754 bytes・stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・時刻/絶対path/volatile排除のbyte決定的監査JSON出力）。

- **pin**（gate 6）: 対象3ファイル（README・検証機・監査正本）をpin commit `e836dd12` のraw pinned URLから取得しSHA-256+byte数を照合（6 gate all PASS）。
- **recon**（gate 48）: 12 W入力を2参照（ref_a・ref_b）のraw pinned URLから取得し、各SHA-256が検証機内pinと一致（12）・ref間byte-identical（12）・ref_b SHA-256一致（12を含めて各入力4 gate・計48 gate all PASS）・検証機の入力dir正規名配置後に再照合。
- **rerun**（gate 25）: 出版検証機を改変なしpristine再実行4回/battery（r1/r2 同一cwd〔battery baseを共有〕・r3 隔離copytree cwd+`env`隔離HOME/TMPDIR・r4 r3+`PYTHONHASHSEED=random`）。各回 rc=0・出力監査JSON（gates_total 76・all_pass true・resolve7_record_faithful true）が出版正本 `42861008…`（21,842 bytes）とbyte-identical・4回間でもbyte一致・4出力互いに同一（6 gate×4+相互1 gateで25 gate all PASS・検証機1回約0.07秒）。
- **tampers**（gate 11）: 本レーン選択offsetの1 byte XOR 0x01（既知の全レーン探針位置 @{12,345,1,234,567}/{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}/{7,777,500,000}/{253,17,522}/{1,234,17,522,4,096}/{117,777,777,777}/{5,077,28,081}/{208,888,919,191}/{300,111,740,321}/{96,300,456,789} のいずれとも別位置）:
  - t1 `sweep39.json` @2,345〔5,097 bytes内〕→ rc≠0・stderr `pin mismatch for sweep39.json`（対象を正しく特定）・監査未書込でfail-closed・W復帰後byte無改変。
  - t2 `resolve6.json` @23,456〔34,984 bytes内〕→ rc≠0・stderr `pin mismatch for resolve6.json`・監査未書込・W復帰後byte無改変。
  - 2つのstderrは互いに異なる入力名を特定し、**2種の入力pin gateが互いに独立して発火する**ことを1 battery内で実証（harness gate `tamper-independent-gates`）。
  - **fold10 ext2第三検証のt1（監査が`gate-failed`で書込される型）と対照的に、resolve7第二検証機はpin loopの最初の不一致でSystemExitし監査JSONを一切書かない強fail-closedである**（第三検証の実験事実として記録）。
- **finalize**: 監査正本 **11,948 bytes・gate 90〔pin 6・recon 48・rerun 25・tampers 11〕・all_gates_pass true・解釈ガード5文+unknown guard**・SHA-256 `0797c44e1df1ce7bbc16873da335e888110b3db2a0822d152a5f28074fecfdee`。**3 battery**（B1 fresh base全stage→B2 同一base全stage再実行〔pin再取得込み〕→B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`）で**byte-identical**（battery 1巡約1.1秒・`cmp`完全一致）。

## 実験事実

1. resolve7第二検証機はfold10第二検証機と異なるfail-closed設計（最初のpin不一致で即SystemExit・監査不書込）を持つ。両設計とも第三環境から指定挙動どおりに作動した。
2. 12 W入力のsnapshot pin（probes-w*/roots.json・main@`ba5f9f4aad`基準）は宣言時点mainで既に成長せず安定しており、2参照byte一致が成立した（append-resume corpusの現況安定を第三環境から確認）。
3. n11検証ラティス最小級（検証機1回約0.07秒・battery 1巡約1.1秒）で、fold10 ext2第三検証（battery 0.9秒）と同程度の第三検査コストで76 gateの独立再現性・入力pin独立性・監査byte決定性が独立検証可能。

## 解釈規約（不変）

本第三検証はresolve7第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、探索・根の新規判定・行の閉鎖・候補universe再構築・receiptの再発行は一切行わない。nodes数・solved数・coverage数を勝敗として読まない。WIN7/WIN8-D10証明書は当該rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 再現

```sh
python3 research/experiments/n11-resolve7-second-verification-pristine-reexec-third-20261121/scripts/verify_resolve7v_third_20261121.py <base_dir>
# battery: B1 fresh base → B2 同一base再実行 → B3 隔離base+env -i 隔離HOME/TMPDIR+PYTHONHASHSEED=random
# 監査: <base_dir>/output/resolve7v-third-harness-audit.json（byte決定的）
```
