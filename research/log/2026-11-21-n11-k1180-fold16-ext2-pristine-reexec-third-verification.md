# 2026-11-21 n11 K1180 fold16 ext2 pristine re-exec 第三検証（単一オーナー・part1〜3）

## 経緯

- 前回まで: fold12/K1184・fold13/K1185・fold14/K1186・fold15/K1187の第三検証が出版済み。fold12〜16単体ext2第二検証群
  （K1175/K1176/K1178/K1179/K1180）の第三検証は第五号のfold16が最後の対象。
- K1180対象の固定値: root `00000000010000889002000080100000`〔root 8890020・第23 receipt・6番目WIN8
  receipt fold〕・pin commit `056b8470`（part1・5ファイル一括）・出版社監査正本 `09f80902…`
  （108,139 bytes・gate 1061〔P 12/I 75/C 932/X 26/T 16〕）・W16再構成機 `c70cbc45…`（11,601 bytes）・
  第三実装検証機 `32917945…`（61,627 bytes・1実行約210秒）・README `76071006…`（6,831 bytes）・
  reproduction.log `78dea747…`（4,101 bytes）。
- 単一オーナー宣言: `research/log/2026-11-21-n11-k1180-fold16-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `65653082…`・宣言時HEAD `4cf3144e`〔n11 S5 recovery〕・受入条件5項目）を先に出版し
  fetch-back byte一致を確認（7,534 bytes）。
- 実験dir: `research/experiments/n11-fold16-ext2-pristine-reexec-third-verification-root8890020-20261121/`。
- harnessはK1187出版harness（`76cb4690…`・19,208 bytes）からのbyte asserted外科的置換で構成
  （36置換ブロック全部数一致assert・残存fold15参照grep排除・py_compile確認後、
  最終 19,261 bytes・SHA-256 `c0b0aec797aed776034fd7d5dfac4fe61488238e6ef7d9047f5afc565ffcc1e5`）。
- tamper offsetは本レーン選択 worklist @351,111 / K1113証明書 @611,222（既知群
  @96,300/@456,789・@117,777/@777,777・@200,222/@888,222・@208,888/@919,191・@300,111/@740,321・
  @150,000/@654,321・@222,999/@1,111,444・@333,444/@999,111・@277,555/@877,666・
  fold20/21/22/24群とすべて別位置）。

## 実施（受入条件対照）

宣言の受入条件5項目に対する実施結果:

1. **出版byte 5点pin** — harness pin stageがpin commit `056b8470`から実験dir 5ファイルを自力取得し
   SHA-256+byte数10 gate PASS（battery 3巡いずれも）。手動pin試行でも5点同一SHAを確認済み。
2. **W16再構成2実装参照** — ref_a `4cf3144e`（宣言時HEAD）・ref_b `65653082`（宣言commit）の両pinned
   refで改変なし再構成機を2回実行し、W16 tree（12 blob + 25 SHA-256 = 37 pin +
   fold11/12/13/14/15/16の6 chain機・43ファイル）を再構成、`diff -r` byte一致。subset-checkは
   fold16再構成機の単行連鎖形式（fold11(10) <= fold12(13) <= fold13(16) <= fold14(19) <= fold15(22) <=
   fold16(12+25) OK）で両参照とも成立、最終行「RECONSTRUCTED W at … PINS 12 PIN256 25」。
3. **検証機pristine 4回** — rerun stage 19 gate。battery 3巡で計12回すべて rc=0・
   `ALL 1061 GATES PASS` 行・出力監査JSONが出版正本 `09f80902…` とbyte-identical。
   1回約209.0〜215.3秒（fold12〜16の第三検証機では約14.4→29→53→106→209.0〜215.3秒と
   ほぼ倍々）。
4. **本レーンoffset tamper 2件** — tampers stage 8 gate。XOR 0x01 @351,111/@611,222 が
   いずれも rc≠0・`GATE FAILED [i]: W blob pin inputs/worklist.csv` /
   `GATE FAILED [i]: W sha256 pin k1113/certs/win8-root-…-20261120.n11`・監査未書込で捕捉。
   battery 3巡で計6回、本番W無改変を事後再照合。
5. **harness監査正本の3実行byte一致** — battery 1（fresh base）・battery 2（同一base全stage再実行）・
   battery 3（隔離base+隔離cwd/HOME/TMPDIR+`PYTHONHASHSEED=random`）のfinalize監査
   （gate 53〔pin 10/recon 16/rerun 19/tampers 8〕・all_gates_pass true・解釈ガード5文）が
   byte-identical（SHA-256 `37154fa95b75d4c2e2c1ff822bd996640540d48907d370799ca5d295da3f3475`・6,958 bytes）。

受入条件5項目すべてPASS。

## 実験事実・知見

- fold16検証機はgate 1061で第三検証群最多。W16は43ファイルでfold11〜16の全6 chain機がWに入る初の規模。
  battery 1巡約14〜15分（rerun 4回が律速・1回約209.0〜215.3秒）。
- worklistはfold12/13/14/15第三に続き5レーン連続同一series再利用（`6d8a449e…`・360,834 bytes）で、
  tamper探針位置は5レーン互いに別々。K1113証明書（775,317 bytes・`105e1e2a…`・21,446行）の探針@611,222は初位置。
- api.github.com非依存の設計を5号連続で維持（全stage raw固定commit URL・待機ゼロ）。
- fold16 receiptのIV.source_recordはK1113実験（root 8890020）を正しく指す（fold12/fold15 receiptの
  stale参照erratumと対照のclean pattern）。

## 出版

- part1 commit `da415ecd`（実験dir 4ファイル一括・単一push_filesコミット）: README.md 8,751 bytes・
  scripts/verify_k1180_fold16ext2_third_20261121.py 19,261 bytes・output/harness-audit.json 6,958 bytes・
  output/reproduction.log 5,874 bytes。fetch-back 4/4 byte一致。
- part2: 本K item（K1188・push直前3点確認で採番）+本log。
- part3: knowledge README末尾bullet（最新main再取得・自file非接触確認後にappend・fetch-back byte一致）。

## 解釈ガード

行は1行も閉じない（fold16時点残余55→51行はK1116 receiptの既出版簿記・pool 120,416根は不変）。
nodes数・solved数・coverage数を勝敗として読まない。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4はすべてUNKNOWNのまま。**
