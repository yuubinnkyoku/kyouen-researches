# K1176（fold13 receipt fold・外部第二検証）のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 `research/log/2026-11-21-n11-k1176-fold13-ext2-pristine-reexec-third-single-owner-note.md`・commit `48c6c2c366c4023279272ced0bf5675726ea5e3d`・宣言 2026-11-21T03:00Z・受入条件5項目）

## 位置づけ

K1176（fold13 receipt fold・root `0000000000000000380000000984004`・第20 receipt・3番目WIN8 receipt foldの出版byteに対する第三実装外部第二検証・2026-11-21T01:05-01:10Z出版・part1最終〔実験dir5ファイル出揃い〕commit `51d86169c1af5e7a880261e76c6f43ea7652d4d4`）に対し、出版社レーン以外の第三の実行環境（本sandbox）が出版byteのみから実験dir・W再構成機・検証機・監査正本を再取得し、pristine再実行・tamper・byte決定性を第三検査した。n11検証ラティスの fold24 ext2（K1164→K1165第三）・fold22 ext2（K1167→K1170第三）・fold29 cert-extract ext2（K1166→K1172第三）・fold20 ext2（K1173→K1174第三）・fold21 ext2（K1168第三）・fold12 ext2（K1175→K1184第三）と同一手続き系列であり、fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180）の第三検証の第二号である。

## 固定pin（出版byte・変更なしの再取得対象）

すべて commit `51d86169c1af5e7a880261e76c6f43ea7652d4d4`（part1最終・実験dir5ファイル出揃いcommit）から取得しSHA-256照合（harness pin stage・fail-closed）:

| file | bytes | SHA-256 |
|---|---|---|
| `README.md` | 5,856 | `28e40ce3eb2a99372995df8848d22c292c91ae9673da9e7939e01b579642f0b0` |
| `scripts/reconstruct_fold13_inputs.py` | 10,204 | `1b54624fe1ccbbb91d390895aa4669fc1aa1c411ac884b750bc7e694389114e9` |
| `scripts/verify_fold13_external_20261121.py` | 57,284 | `aeda41e1df244cf331a9435260d8ed83652971af8e29bfa289648cf981abf6bc` |
| `output/external-audit.json` | 81,632 | `4fe40fa254b4d2658bb0fadbc47dadb43c3d85214be8a9517b525693b416be81` |
| `output/reproduction.log` | 5,691 | `224272ee1e5533dcb56d3889a6ae0d5d173076a22ba786e8ef2bce453dc764ec` |

## 実施内容と結果（harness `verify_k1176_fold13ext2_third_20261121.py`・18,746 bytes・stage分割 pin/recon/rerun/tampers/finalize・stdlibのみ・fail-closed）

- **pin**（gate 10）: 上記5ファイルを出版byteのままraw pinned URLから取得し、SHA-256・byte数を照合。
- **recon**（gate 16）: 出版再構成機 `reconstruct_fold13_inputs.py` を改変せず2参照（ref_a = 宣言時HEAD `0af2ac836a9442e76d1d27cc100ec6243440063c`・ref_b = 検証時main〔宣言commit〕`48c6c2c366c4023279272ced0bf5675726ea5e3d`）で実行し、W treeを2回再構成。各回 12 Git blob pin + 16 SHA-256 pin = 28 pin + fold11機・fold12機・fold13機の3 chain機・計31ファイル、`diff -r W_A W_B` が完全byte一致、fold11機入力pinの部分集合性の機械確認（`subset-check fold11 pins 12 pin256 10 fold12 pins 12 pin256 13 subset of fold13 12+16 OK` 行・値照合）が両参照で成立。1参照約1〜6秒でapi.github.com非依存（raw固定commit URL）。
- **rerun**（gate 19）: 出版検証機 `verify_fold13_external_20261121.py` を改変せずpristine再実行4回（r1/r2 同一cwd・r3 隔離copytree W/cwd/HOME〔隔離HOME/TMPDIR〕・r4 隔離+`PYTHONHASHSEED=random`）。全回 rc=0・`ALL 774 GATES PASS` 行・gate count 774（ok:true総数・all_gates_pass true）・出力監査JSON（81,632 bytes）が出版正本 `4fe40fa2…` とbyte-identical・4回間でもbyte一致。検証機1回約28.5〜29.1秒（機内のfold13機4回プリ実行・fold11/fold12機独立rerun・機内tamper 2件〔出版社試験offset @117,777/@777,777〕込み）。
- **tampers**（gate 8）: 本レーン選択offset（出版社試験位置 worklist @117,777・証明書 @777,777、fold12第三検証レーン〔K1184〕の @150,000/@654,321、fold20/21/22/24第三検証・fold14-16 ext2の各レーンoffset群 @{7777,500000}/{253,17522}/{1234,17522,4096}/{200222,888222}/{208888,919191}/{300111,740321} とすべて別位置）の1 byte XOR 0x01 を隔離copytree W 上で実施:
  - t1 `inputs/worklist.csv` @222,999 → rc=1・`GATE FAILED [i]: W blob pin inputs/worklist.csv`・監査未書込（I-section legacy blob pin gate）
  - t2 `k1108/certs/win8-root-00000000000000003800000009840004-20261120.n11` @1,111,444 → rc=1・`GATE FAILED [i]: W sha256 pin …`・監査未書込（I-section sha256 pin gate）
  - 両実施後に本番Wを再照合（worklist SHA-256 `6d8a449e…`・K1108証明書 SHA-256 `5b114b9e…`・無改変）。事前の手動探針（XOR 0x20・同offset）でも同一メッセージで発火することを別途確認済み。
- **finalize**: 以上partsを集計し、時刻・絶対path・実行時間（volatile）を含まないbyte決定的なharness監査JSON（6,668 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・解釈ガード5文つき・SHA-256 `701bdfebab8b728d2b7f705e0837f5b625ae5e35bfff57a3990e4b4cee8342d6`）を書き出し。**6実行**（リセット前 battery 1・2 = 同一baseでの全stage再実行〔pin再取得込み〕・battery 3 = 隔離base+隔離cwd/HOME/TMPDIR+`PYTHONHASHSEED=random`、リセット後の全完全再生成 battery 1'・2'・3'）が**すべてbyte-identical**（後述の環境リセット事故を参照）。

## 実験事実

1. **実行環境リセット事故が交叉環境のbyte決定性の実証となった**: battery 3巡（監査正本 `701bdfeb…`）完了直後に実行環境がリセットされ、pubfetch・W tree・battery成果物・harnessファイルを含む全ローカル成果物を喪失した。harnessを記録済みソースから再構成（byte数照合 18,746 = 18,746・再入力時に紛れ込んだ24 bytesの余分行はbyte数照合が捕捉し除去）し、battery 3巡をfresh baseでゼロから完全再実行したところ、再生成監査正本はリセット前記録値 `701bdfeb…` とbyte一致した。計6回のfinalize監査（リセット前3+後3）が同一byteであり、意図せず「別環境実体・別base・別取得経路でも同一監査byte」という交叉環境検証が成立した。
2. **fold13検証機は1回約29秒と n11検証ラティス内で最重量級**: gate 774・57,284 bytesでfold12機（655 gate・1回約14〜15秒）の約2倍。W treeは31ファイル（fold12の27ファイルに対しfold13機pinが16個に増分）。battery 1巡あたり検証機pristine 4回+再構成2回+tamper 2回で約2.5分。
3. **worklistはfold12第二検証と同一seriesファイルの再利用**（`inputs/worklist.csv`・SHA-256 `6d8a449e…`・360,834 bytes・両receiptとも第3勝利候補root列挙の同一1410系列）であり、本lane tamper offset（@222,999）はfold12第三検証レーンの選択（@150,000）と衝突しない。
4. **api.github.com枯渇の影響圏外**: 本batteryの全stage（pin・recon含む）はraw固定commit URLのみでapi.github.comを一度も呼ばない。api quotaは本セッション中に403枯渇し、コミット列挙に限って必要最小回数だけ使ったが、監査byte・pin照合には影響ゼロ。

## 再現手順

```sh
mkdir base && cd base
# 本dirの scripts/verify_k1176_fold13ext2_third_20261121.py を出版byteのまま配置
python3 scripts/verify_k1176_fold13ext2_third_20261121.py pin .       # 出版byte 5点取得+pin照合（network）
python3 scripts/verify_k1176_fold13ext2_third_20261121.py recon .    # W再構成2参照（raw固定commit URL）
python3 scripts/verify_k1176_fold13ext2_third_20261121.py rerun .    # 検証機pristine 4回（各約29秒）
python3 scripts/verify_k1176_fold13ext2_third_20261121.py tampers .  # tamper 2件 fail-closed
python3 scripts/verify_k1176_fold13ext2_third_20261121.py finalize . # harness監査JSON（byte決定的）
```

## 限界と解釈ガード

本検証はK1176第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない（fold13時点残余65→62行は当該receiptの既出版簿記・pool 120,416根は不変）。WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
