# 36root-three-ply frontier（K1084）独立第二検証のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 [note](../../../log/2026-11-21-n11-36root-three-ply-frontier-second-verification-pristine-reexec-third-single-owner-note.md)〔commit `ffba79856ecbc4e915d01a4b74c4b1bfeee62f31`・宣言 2026-11-21T06:5xZ・受入条件5項目・受入条件3の根拠となる出版監査byte再生性を宣言前に予備実測・先行宣言の不在を機械列挙で確認〕）

## 位置づけ

residual72の36-root三手先D4重複census（K1075候補供給正本による36 fresh-safe 7石root・三点組132,291個・点判定16,007,211回・root安全性四点組1,260個）に対する独立第二検証（K1084・commit `67766eac2f30c856543a1319cdfc5d1458382c73`・2026-11-19T23:25:16Z単一コミット出版・README `bbc9b255…`〔2,782 bytes〕/検証機 `d8876e5b…`〔14,671 bytes・Python 3.13純stdlib・19 gate・元JSをimportせず整数放物面持ち上げの3次元外積・内積で4点行列式零判定・D4 8変換は座標写像直接列挙〕/監査正本 `a6272056…`〔55,614 bytes〕+K1084 item+研究log）を、出版社レーン以外の第三の実行環境（本sandbox）が**出版byteのみから再取得してpristine再実行・tamper・監査byte決定性を第三検査する**。residual72系の第三検証は4-sweep（K1144）・replace9 sweep/whole-record・verdict-sweeps・resolve7（K1190）・replace16（K1191）に続き、**36root-three-ply分の第三検証は本実験が初号**。本対象は19 gate・検証機1回約16秒の中堅規模である。

## 対象・固定pin

| file | bytes | SHA-256 |
| --- | --- | --- |
| 対象README（第二検証実験dir） | 2,782 | `bbc9b255e63e46941b372b145f2440b0d6a774c7c455f23d573af374db9ee34c` |
| 対象検証機 `scripts/verify_frontier.py` | 14,671 | `d8876e5b61d7df02cca4958407ad310b3ceba4de8746f04657598df471834481` |
| 対象監査正本 `output/independent-second-verification-20261120.json` | 55,614 | `a6272056df6aa1dc348a00e1961a95223b4642a230a7da95a04b857bd9118b83` |
| K1084 item（出版記録・機械入力ではない） | 3,253 | pin commit `67766eac` から取得記録 |
| 対象研究log（出版記録・機械入力ではない） | 2,743 | pin commit `67766eac` から取得記録 |

3つの機械ファイルはpin commit `67766eac` のraw pinned URLから取得（api.github.com非依存）。宣言時現main HEAD `3ba28e88` で3ファイルともpin byteと一致した。

## W入力（2点の出版正本・検証機内SHA-256 pinと一致必須・fail-closed）

| 正規名 | bytes | SHA-256（機械pin） |
| --- | --- | --- |
| K1075候補供給正本 | 54,282 | `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa` |
| 先行三手先census正本 | 53,914 | `94fdb0c6e3503f1e9d19aaaf345f4478157c5a44374f10642c52325f346c2023` |

第三検証では ref_a = 宣言時HEAD `3ba28e88fd1d5c0fffaa9ae042fe3dfa68318ca0`・ref_b = 宣言commit `ffba79856ecbc4e915d01a4b74c4b1bfeee62f31` の2参照で固定する。検証機は合成tree（ROOT = 検証機fileのparents[4]）上の正規pathで読む。

## 実施内容と結果（harness `scripts/verify_t36v_third_20261121.py`）

harness: `scripts/verify_t36v_third_20261121.py`（SHA-256 `cf5b5f4762ff0ac95525f3d45f21f6ce0de7ac3d7035a6b15bd1c3296410e649`・15,153 bytes・stdlibのみ・stage分割 pin/recon/rerun/tampers/finalize・fail-closed・時刻/絶対path/volatile排除のbyte決定的監査JSON出力）。

- **pin**（gate 9）: 対象3ファイル（README・検証機・監査正本）をpin commit `67766eac` のraw pinned URLから取得しSHA-256+byte数を照合（6 gate）し、さらに宣言時HEAD `3ba28e88` の同3ファイルがpin byteと一致することをbyte比較（3 gate）（計9 gate all PASS）。
- **recon**（gate 9）: W 2入力を2参照（ref_a・ref_b）のraw pinned URLから取得し、各SHA-256が機械pinと一致・ref間byte-identical・合成tree正規path配置後に再照合（2点×4 gate）+ 検証機本文の合成tree配置後再照合（1 gate）（計9 gate all PASS）。
- **rerun**（gate 23）: 出版検証機を改変なしpristine再実行4回/battery（r1/r2 同一合成tree・r3 隔離copytree+隔離env PATH/HOME/TMPDIR・r4 r3+`PYTHONHASHSEED=random`）。各回 rc=0・stdout JSON `status=second-verified・check_count=19・all_pass=true`・出力監査が出版正本 `a6272056…`〔55,614 bytes〕とbyte-identical・4回間でbyte一致（x4 5gate+相互3 gate、計23 gate all PASS・検証機1回約16秒）。**replace16第三検証（K1191）で確立した「rerun受入はbyte再生性を宣言前に予備実測してから課す」運用を本対象で先に適用し、宣言ノート受入条件3は当初からbyte一致条件で確定した**（本対象はerratumなし・出版監査byte再生が成立）。
- **tampers**（gate 15）: 本レーン選択offsetの1 byte XOR 0x20（既知の全レーン探針位置 @{12,345,1,234,567}/{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}/{7,777,500,000}/{253,17,522}/{1,234,17,522,4,096}/{117,777,777,777}/{5,077,28,081}/{208,888,919,191}/{300,111,740,321}/{2,345,23,456}/{5,678,9,012} のいずれとも別位置〔@51,234/@8,765〕）、**監査不在のfresh tree**（rerun後監査を除去し事前不在をassert後に探針）で実施:
  - t1 K1075候補供給正本 @51,234〔54,282 bytes内〕→ rc==1・stdout空・stderr末行 `RuntimeError: K1075 source SHA-256 mismatch`・監査未書込・本番tree W無改変。
  - t2 先行census正本 @8,765〔53,914 bytes内〕→ rc==1・stdout空・stderr末行 `RuntimeError: published frontier SHA-256 mismatch`・監査未書込・本番tree W無改変。
  - 2つのstderr末行は互いに異なる入力を特定し、**K1075供給正本とcensus正本の2入力pin gateが互いに独立して発火する**ことを1 battery内で実証（gate `tamper-independent-errors`・t1は読み取り1点目・t2は2点目のfailで読み取り順独立性を含む）。**raise RuntimeError型（Python traceback・監査不書込）はfail-closed設計4種目**（fold10 gate-failed監査書込型・resolve7 SystemExit不書込型・replace16 SystemExit不書込型に続き）。stderrのtracebackには実行file絶対pathが含まれるため、harnessのgateは**末行のRuntimeErrorメッセージ特定**で行い、stderr全文byte一致は要求しない（宣言ノートに明記）。
- **finalize**: 監査正本 **7,729 bytes・gate 56〔pin 9・recon 9・rerun 23・tampers 15〕・all_gates_pass true・解釈ガード5文+unknown guard**・SHA-256 `407d649dde8e791447d160dab39ebc71f50ea2aed704e7b145153b494c7b6156`。**4 battery実行**（B1 fresh base全stage〔1m4.9s〕→B2 同一base全stage再実行〔pin再取得込み・1m2.7s〕→B1f fresh base独立capture〔1m2.9s〕→B3 隔離fresh base+全体`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`+別cwd〔1m3.3s〕）すべて56/56 PASSで**監査byte-identical**（`cmp`完全一致・B1f==B2==B3）。

## 実験事実

1. **本対象の出版監査はbyte再生可能**: pristine再実行（宣言前予備・本battery 12回）はすべて出版正本 `a6272056…` とbyte-identical（replace16 K1191のerratum型とは対照的）。K1191で確立した「rerun受入は宣言前にbyte再生性を予備実測してから課す」運用の適用第1号であり、運用の有効性を示す。
2. **fail-closed設計4種目の実測**（raise RuntimeError traceback型・監査不書込）: pin loop読み取り直後の不一致で例外終了し監査JSONを一切書かない。tracebackは絶対pathを含むため非byte決定的だが、末行メッセージは入力名で決定的であり、第三検証gateは末行特定で機械記録可能。
3. **中堅規模の第三検査コスト**: 検証機1回約16秒・battery 1巡約63〜65秒（12回のrerunで出版正本byte一致・2回のtamper探針で入力pin独立性を1 battery内で実証）。第二検証出版（2026-11-19T23:25Z）から約1.6日で第三検証確定。

## 解釈規約（不変）

本第三検証は36root-three-ply frontier第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、探索・根の新規判定・行の閉鎖・候補universe再構築・receiptの再発行・36-root depth-10 sweep（別単一オーナーレーン所属）の起動・変更は一切行わない。幾何censusの重複率はDFPN節点数・共有表命中率・証明状態再利用性を測るものではなく、共有表実装やworker分割変更の正当化ではない。nodes数・solved数・coverage数を勝敗として読まない。REFUTED-D10はLOSS証明ではない。36 rootは候補rootであってWIN証明書ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 再現

```sh
python3 research/experiments/n11-residual72-36root-three-ply-frontier-independent-second-verification-pristine-reexec-third-20261121/scripts/verify_t36v_third_20261121.py <base_dir>
# battery: B1 fresh base → B2 同一base再実行 → B1f fresh base独立capture → B3 隔離base+env -i 隔離HOME/TMPDIR+PYTHONHASHSEED=random+別cwd
# 監査: <base_dir>/output/frontier-third-harness-audit.json（byte決定的）
```
