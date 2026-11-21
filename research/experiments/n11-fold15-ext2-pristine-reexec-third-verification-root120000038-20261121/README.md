# K1179（fold15 receipt fold・外部第二検証）のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 `research/log/2026-11-21-n11-k1179-fold15-ext2-pristine-reexec-third-single-owner-note.md`・commit `04b4ed9d7f279b299d71eb2749728aa741116fe5`・宣言 2026-11-21T04:03Z・受入条件5項目）

## 位置づけ

K1179（fold15 receipt fold・root `00000000012000003800080009000000`〔root 120000038〕・第22 receipt・5番目WIN8 receipt foldの出版byteに対する第三実装外部第二検証・2026-11-21T01:2xZ出版・part1 commit `2e1bc1eab0fa7f66810d839ca91dd2fae3a50962`〔検証機・再構成機・監査正本・README・reproduction.log一括〕・part2 commit `0a472863`〔K1179 item〕・part3 commit `563cf9b6`〔knowledge README bullet〕）に対し、出版社レーン以外の第三の実行環境（本sandbox）が出版byteのみから実験dir・W15再構成機・検証機・監査正本を再取得し、pristine再実行・tamper・byte決定性を第三検査した。n11検証ラティスの fold24 ext2（K1164→K1165第三）・fold22 ext2（K1167→K1170第三）・fold29 cert-extract ext2（K1166→K1172第三）・fold20 ext2（K1173→K1174第三）・fold21 ext2（K1168第三）・fold12 ext2（K1175→K1184第三）・fold13 ext2（K1176→K1185第三）・fold14 ext2（K1178→K1186第三）と同一手続き系列であり、fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180）の第三検証の第四号である。

## 固定pin（出版byte・変更なしの再取得対象）

すべて commit `2e1bc1eab0fa7f66810d839ca91dd2fae3a50962`（K1179 part1・5ファイル一括commit）から取得しSHA-256照合（harness pin stage・fail-closed）:

| file | bytes | SHA-256 |
|---|---|---|
| `README.md` | 6,683 | `20a2d1042412fd2620ed6fc40be383e656064ade8b201dc13a5e7e43892d0bfa` |
| `scripts/reconstruct_fold15_inputs.py` | 10,644 | `7757cb5130942e8891697fcf0903f37d9c8d27f3ed6a8ca1b85a5fc07fd582be` |
| `scripts/verify_fold15_external_20261121.py` | 62,390 | `ade19de29fa34bb8f0f7913ece230daa428797792c9db59279e8489d872eac99` |
| `output/external-audit.json` | 101,443 | `6800759ea5e899b84866079ac36fae2316d78a85620e1b32187abc26a0fed717` |
| `output/reproduction.log` | 2,106 | `579f178a44f5a7ee75ff84c6ee771894f95e9cfaf93df4624135e7ddcc3c9ecc` |

## 実施内容と結果（harness `verify_k1179_fold15ext2_third_20261121.py`・19,208 bytes・stage分割 pin/recon/rerun/tampers/finalize・stdlibのみ・fail-closed）

- **pin**（gate 10）: 上記5ファイルを出版byteのままraw pinned URLから取得し、SHA-256・byte数を照合。
- **recon**（gate 16）: 出版再構成機 `reconstruct_fold15_inputs.py` を改変せず2参照（ref_a = 宣言時HEAD `b619261ae0243573031c4314582d580c51b7712f`・ref_b = 検証時main〔宣言commit〕`04b4ed9d7f279b299d71eb2749728aa741116fe5`）で実行し、W15 treeを2回再構成。各回 12 Git blob pin + 22 SHA-256 pin = 34 pin + fold11機・fold12機・fold13機・fold14機・fold15機の5 chain機・計39ファイル、`diff -r W_A W_B` が完全byte一致、4本の部分集合確認行（fold11機入力pinの部分集合連鎖 `subset-check fold11 12+10 … subset-check fold14 12+19 subset of fold15 12+22 OK`）が両参照で成立。1参照約10秒でapi.github.com非依存（raw固定commit URL）。
- **rerun**（gate 19）: 出版検証機 `verify_fold15_external_20261121.py` を改変せずpristine再実行4回（r1/r2 同一cwd・r3 隔離copytree W/cwd/HOME〔隔離HOME/TMPDIR〕・r4 隔離+`PYTHONHASHSEED=random`）。全回 rc=0・`ALL 981 GATES PASS` 行・gate count 981（ok:true総数・all_gates_pass true）・出力監査JSON（101,443 bytes）が出版正本 `6800759e…` とbyte-identical・4回間でもbyte一致。検証機1回約105.6〜106.0秒（機内のfold15機4回プリ実行・vr14 fold14機独立rerun・fold11/12/13機rerun・機内tamper 2件〔出版社試験offset @208,888/@919,191〕込み）。
- **tampers**（gate 8）: 本レーン選択offset（出版社試験位置 worklist @208,888・証明書 @919,191、fold12第三検証レーン〔K1184〕の @150,000/@654,321、fold13第三検証レーン〔K1185〕の @222,999/@1,111,444、fold14第三検証レーン〔K1186〕の @333,444/@999,111、fold20/21/22/24第三検証・fold16 ext2の各レーンoffset群 @{7777,500000}/{253,17522}/{1234,17522,4096}/{117777,777777}/{300111,740321} とすべて別位置）の1 byte XOR 0x01 を隔離copytree W 上で実施:
  - t1 `inputs/worklist.csv` @277,555 → rc=1・`GATE FAILED [i]: W blob pin inputs/worklist.csv`・監査未書込（I-section legacy blob pin gate）
  - t2 `k1114/certs/win8-root-00000000012000003800080009000000-20261120.n11` @877,666 → rc=1・`GATE FAILED [i]: W sha256 pin …`・監査未書込（I-section sha256 pin gate）
  - 両実施後に本番Wを再照合（worklist SHA-256 `6d8a449e…`・K1114証明書 SHA-256 `5a135903…`・無改変）。事前の手動探針（XOR 0x20・同offset）でも同一メッセージで発火することを別途確認済み。
- **finalize**: 以上partsを集計し、時刻・絶対path・実行時間（volatile）を含まないbyte決定的なharness監査JSON（6,858 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・解釈ガード5文つき・SHA-256 cfb6879a8f2d97d478942c33973bcd87eb774abc15fe94f591ff537747185b7f）を書き出し。**3実行**（battery 1・2 = 同一baseでの全stage再実行〔pin再取得込み〕・battery 3 = 隔離base+隔離cwd/HOME/TMPDIR+`PYTHONHASHSEED=random`）で**byte-identical**を確認。3 battery合計で出版検証機のpristine実行12回（+手動試行1回=13回）・出版再構成機の実行6回・本レーンoffset tamper 6回（+手動XOR-0x20探針2回）がすべて受入条件どおりの結果。

## 実験事実

1. **fold15検証機はfold14機の約2倍・1回約106秒**: gate 981（fold14機は880）・1回約105.6〜106.0秒。W15 treeは39ファイル（34 pin + 5 chain機・fold11〜15の全機がWに入る初の規模）。battery 1巡あたり約7分15秒（検証機pristine 4回+再構成2回+tamper 2件）。fold15 root（合法手53）のWIN8証明書はK1114の1,171,958 bytes（`5a135903…`）。
2. **worklistはfold12/13/14に続き同一seriesファイルの4レーン連続再利用**（`inputs/worklist.csv`・SHA-256 `6d8a449e…`・360,834 bytes）。本レーンtamper offset（@277,555）はfold12第三（@150,000）・fold13第三（@222,999）・fold14第三（@333,444）と衝突せず、worklistのtamper探針位置が4レーンで別々である。
3. **K1114証明書のtamper探針は初位置 @877,666**（1,171,958 bytes内）。fold15第二検証レーンの @919,191・fold14第三の @999,111（K1109証明書）と別位置。
4. **api.github.com枯渇の影響圏外**: 本batteryの全stage（pin・recon含む）はraw固定commit URLのみでapi.github.comを一度も呼ばない。手動探針・pin試行・fetch-backもすべてapi非依存で待機ゼロの冪等運転（K1184〜K1186の第三検証batteryと同一の設計・時刻・絶対path排除）。

## 再現手順

```sh
mkdir base && cd base
# 本dirの scripts/verify_k1179_fold15ext2_third_20261121.py を出版byteのまま配置
python3 scripts/verify_k1179_fold15ext2_third_20261121.py pin .       # 出版byte 5点取得+pin照合（network）
python3 scripts/verify_k1179_fold15ext2_third_20261121.py recon .    # W15再構成2参照（raw固定commit URL）
python3 scripts/verify_k1179_fold15ext2_third_20261121.py rerun .    # 検証機pristine 4回（各約106秒）
python3 scripts/verify_k1179_fold15ext2_third_20261121.py tampers .  # tamper 2件 fail-closed
python3 scripts/verify_k1179_fold15ext2_third_20261121.py finalize . # harness監査JSON（byte決定的）
```

## 限界と解釈ガード

本検証はK1179第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない（fold15時点残余58→55行は当該receiptの既出版簿記・pool 120,416根は不変）。WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
