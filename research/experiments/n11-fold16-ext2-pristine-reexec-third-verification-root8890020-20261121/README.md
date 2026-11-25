# K1180（fold16 receipt fold・外部第二検証）のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 `research/log/2026-11-21-n11-k1180-fold16-ext2-pristine-reexec-third-single-owner-note.md`・commit `6565308232d0c3bff5c205ff6e948efa9edfde99`・宣言 2026-11-21T04:5xZ・受入条件5項目）

## 位置づけ

K1180（fold16 receipt fold・root `00000000010000889002000080100000`〔root 8890020〕・第23 receipt・6番目WIN8 receipt foldの出版byteに対する第三実装外部第二検証・2026-11-21T01:5xZ出版・part1 commit `056b8470acda7450e70270e7d10a376a90ccd1ab`〔検証機・再構成機・監査正本・README・reproduction.log一括〕・part2 commit `091455c92eee64c31a4c9112bd62498f1c46e88c`〔K1180 item〕・part3 commit `edb61c42374b84b2f394f4ed1c0e154e52a8834b`〔knowledge README bullet〕）に対し、出版社レーン以外の第三の実行環境（本sandbox）が出版byteのみから実験dir・W16再構成機・検証機・監査正本を再取得し、pristine再実行・tamper・byte決定性を第三検査した。n11検証ラティスの fold24 ext2（K1164→K1165第三）・fold22 ext2（K1167→K1170第三）・fold29 cert-extract ext2（K1166→K1172第三）・fold20 ext2（K1173→K1174第三）・fold21 ext2（K1168第三）・fold12 ext2（K1175→K1184第三）・fold13 ext2（K1176→K1185第三）・fold14 ext2（K1178→K1186第三）・fold15 ext2（K1179→K1187第三）と同一手続き系列であり、fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180）の第三検証の第五号である。

## 固定pin（出版byte・変更なしの再取得対象）

すべて commit `056b8470acda7450e70270e7d10a376a90ccd1ab`（K1180 part1・5ファイル一括commit）から取得しSHA-256照合（harness pin stage・fail-closed）:

| file | bytes | SHA-256 |
|---|---|---|
| `README.md` | 6,831 | `760710062ce37d1dc63c1ca920b25c1b2c0bff8543b63dce939c0dd4048312f0` |
| `scripts/reconstruct_fold16_inputs.py` | 11,601 | `c70cbc453a1f712fa51d66123790cd053d7198edd4bdcf53aa6ec055b78594d4` |
| `scripts/verify_fold16_external_20261121.py` | 61,627 | `3291794504d98f2c7d7204f623325c92d2d898ea6e246ede476e6e736ac51627` |
| `output/external-audit.json` | 108,139 | `09f80902d8c2159b26db971504a582d43acb77879021e684c56bbbdcbe7cf19d` |
| `output/reproduction.log` | 4,101 | `78dea7476a08baced0878d4ebb4c0c3f77edd39c59e601358ff2f54bf70dac74` |

## 実施内容と結果（harness `verify_k1180_fold16ext2_third_20261121.py`・19,261 bytes・stage分割 pin/recon/rerun/tampers/finalize・stdlibのみ・fail-closed）

- **pin**（gate 10）: 上記5ファイルを出版byteのままraw pinned URLから取得し、SHA-256・byte数を照合。
- **recon**（gate 16）: 出版再構成機 `reconstruct_fold16_inputs.py` を改変せず2参照（ref_a = 宣言時HEAD `4cf3144eb2166a1d9f07d65b278470184b7eeb89`・ref_b = 検証時main〔宣言commit〕`6565308232d0c3bff5c205ff6e948efa9edfde99`）で実行し、W16 treeを2回再構成。各回 12 Git blob pin + 25 SHA-256 pin = 37 pin + fold11機・fold12機・fold13機・fold14機・fold15機・fold16機の6 chain機・計43ファイル、`diff -r W_A W_B` が完全byte一致、部分集合確認行（fold11機入力pin（12+10）⊂fold12機（12+13）⊂fold13機（12+16）⊂fold14機（12+19）⊂fold15機（12+22）⊂fold16機（12+25）の連鎖）が両参照で成立。raw固定commit URLのみでapi.github.com非依存。
- **rerun**（gate 19）: 出版検証機 `verify_fold16_external_20261121.py` を改変せずpristine再実行4回（r1/r2 同一cwd・r3 隔離copytree W/cwd/HOME〔隔離HOME/TMPDIR〕・r4 隔離+`PYTHONHASHSEED=random`）。全回 rc=0・`ALL 1061 GATES PASS` 行・gate count 1061（ok:true総数・all_gates_pass true）・出力監査JSON（108,139 bytes）が出版正本 `09f80902…` とbyte-identical・4回間でもbyte一致。検証機1回約209.0〜215.3秒（機内のfold16機4回プリ実行・vr15 fold15機独立rerun・fold11/12/13/14機rerun・機内tamper 2件〔出版社試験offset @300,111/@740,321〕込み）。
- **tampers**（gate 8）: 本レーン選択offset（出版社試験位置 worklist @300,111・証明書 @740,321、fold12第三検証レーン〔K1184〕の @150,000/@654,321、fold13第三検証レーン〔K1185〕の @222,999/@1,111,444、fold14第三検証レーン〔K1186〕の @333,444/@999,111、fold15第三検証レーン〔K1187〕の @277,555/@877,666、fold20/21/22/24第三検証の各レーンoffset群 @{7777,500000}/{253,17522}/{1234,17522,4096}/{117777,777777} とすべて別位置）の1 byte XOR 0x01 を隔離copytree W 上で実施:
  - t1 `inputs/worklist.csv` @351,111 → rc=1・`GATE FAILED [i]: W blob pin inputs/worklist.csv`・監査未書込（I-section legacy blob pin gate）
  - t2 `k1113/certs/win8-root-00000000010000889002000080100000-20261120.n11` @611,222 → rc=1・`GATE FAILED [i]: W sha256 pin …`・監査未書込（I-section sha256 pin gate）
  - 両実施後に本番Wを再照合（worklist・K1113証明書とも無改変）。
- **finalize**: 以上partsを集計し、時刻・絶対path・実行時間（volatile）を含まないbyte決定的なharness監査JSON（6,958 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・解釈ガード5文つき・SHA-256 `37154fa9…`）を書き出し。**3実行**（battery 1・2 = 同一baseでの全stage再実行〔pin再取得込み〕・battery 3 = 隔離base+隔離cwd/HOME/TMPDIR+`PYTHONHASHSEED=random`）で**byte-identical**を確認。3 battery合計で出版検証機のpristine実行12回・出版再構成機の実行6回・本レーンoffset tamper 6回がすべて受入条件どおりの結果。

## 実験事実

1. **fold16検証機はgate 1061（P 12/I 75/C 932/X 26/T 16）で第三検証群最多gate数**: W16 treeは43ファイル（37 pin + 6 chain機・fold11〜16の全機がWに入る初の規模）。battery 1巡あたり約14分10秒〜14分22秒（実測 B1 04:53:45-05:07:55・B2 05:09:12-05:23:30・B3 05:23:55-05:38:17）。fold16 root（合法手50）のWIN8証明書はK1113の775,317 bytes（`105e1e2a…`・21,446行）。
2. **worklistはfold12/13/14/15に続き同一seriesファイルの5レーン連続再利用**（`inputs/worklist.csv`・SHA-256 `6d8a449e…`・360,834 bytes）。本レーンtamper offset（@351,111）はfold12第三（@150,000）・fold13第三（@222,999）・fold14第三（@333,444）・fold15第三（@277,555）・出版社（@300,111）と衝突せず、worklistのtamper探針位置が5レーンで別々である。
3. **K1113証明書のtamper探針は初位置 @611,222**（775,317 bytes内）。fold16第二検証レーンの @740,321・fold15第三の K1114証明書 @877,666・fold14第三の K1109証明書 @999,111と別位置。
4. **api.github.com枯渇の影響圏外**: 本batteryの全stage（pin・recon含む）はraw固定commit URLのみでapi.github.comを一度も呼ばない。時刻・絶対path排除でbyte決定的（K1184〜K1187の第三検証batteryと同一の設計）。
5. **fold16 receiptのIV.source_record clean pattern維持をW16再構成経由で再確認**（K1180監査の摘記再照合・fold12/fold15 receiptのstale参照erratumと対照的に、fold16 receiptは自実験dirを記載）。

## 再現手順

```sh
mkdir base && cd base
# 本dirの scripts/verify_k1180_fold16ext2_third_20261121.py を出版byteのまま配置
python3 scripts/verify_k1180_fold16ext2_third_20261121.py pin .       # 出版byte 5点取得+pin照合（network）
python3 scripts/verify_k1180_fold16ext2_third_20261121.py recon .    # W16再構成2参照（raw固定commit URL）
python3 scripts/verify_k1180_fold16ext2_third_20261121.py rerun .    # 検証機pristine 4回（各約210秒）
python3 scripts/verify_k1180_fold16ext2_third_20261121.py tampers .  # tamper 2件 fail-closed
python3 scripts/verify_k1180_fold16ext2_third_20261121.py finalize . # harness監査JSON（byte決定的）
```

## 限界と解釈ガード

本検証はK1180第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない（fold16時点残余55→51行は当該receiptの既出版簿記・pool 120,416根は不変）。WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
