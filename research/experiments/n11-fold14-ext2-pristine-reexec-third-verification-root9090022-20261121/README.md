# K1178（fold14 receipt fold・外部第二検証）のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 `research/log/2026-11-21-n11-k1178-fold14-ext2-pristine-reexec-third-single-owner-note.md`・commit `369b0c3028cda2a987b3dcd08cd718af703d2fbf`・宣言 2026-11-21T03:2xZ・受入条件5項目）

## 位置づけ

K1178（fold14 receipt fold・root `00000000000000909002200080100000`・第21 receipt・4番目WIN8 receipt foldの出版byteに対する第三実装外部第二検証・2026-11-21T01:23Z出版・part1 commit `23de00dc7ad8d49747c9de9cc021fd35e542f77c`〔検証機・再構成機・監査正本・README・reproduction.log一括〕・part2 commit `30239f51`〔K1178 item〕・part3 commit `132364c9`〔knowledge README bullet〕）に対し、出版社レーン以外の第三の実行環境（本sandbox）が出版byteのみから実験dir・W再構成機・検証機・監査正本を再取得し、pristine再実行・tamper・byte決定性を第三検査した。n11検証ラティスの fold24 ext2（K1164→K1165第三）・fold22 ext2（K1167→K1170第三）・fold29 cert-extract ext2（K1166→K1172第三）・fold20 ext2（K1173→K1174第三）・fold21 ext2（K1168第三）・fold12 ext2（K1175→K1184第三）・fold13 ext2（K1176→K1185第三）と同一手続き系列であり、fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180）の第三検証の第三号である。

## 固定pin（出版byte・変更なしの再取得対象）

すべて commit `23de00dc7ad8d49747c9de9cc021fd35e542f77c`（K1178 part1・5ファイル一括commit）から取得しSHA-256照合（harness pin stage・fail-closed）:

| file | bytes | SHA-256 |
|---|---|---|
| `README.md` | 6,534 | `0d3b4e06b6c53ea6d7c123a7744e1eb04854c33a00260f02f2cbcf64ffef4764` |
| `scripts/reconstruct_fold14_inputs.py` | 11,543 | `62a72b36eb70a74c3b9fcc85c10c59a7bab73550807e957382645d38866d5d59` |
| `scripts/verify_fold14_external_20261121.py` | 58,352 | `d966dad55d54b6c1608f5f046469b2fd9a95b3b38c4f12a69f516e83fb708b0c` |
| `output/external-audit.json` | 91,543 | `fe6370f7e9cd30eaca7cc0ce3a61d39e9a6dd1eb47c8ba4f300e680f5d55b102` |
| `output/reproduction.log` | 3,065 | `5d28aa0e67d77f527c6901030ca125c3ba359a94bd26ad57056cba48ffa831fa` |

## 実施内容と結果（harness `verify_k1178_fold14ext2_third_20261121.py`・18,921 bytes・stage分割 pin/recon/rerun/tampers/finalize・stdlibのみ・fail-closed）

- **pin**（gate 10）: 上記5ファイルを出版byteのままraw pinned URLから取得し、SHA-256・byte数を照合。
- **recon**（gate 16）: 出版再構成機 `reconstruct_fold14_inputs.py` を改変せず2参照（ref_a = 宣言時HEAD `eda86d47bc050bea48ee6ed8e27a8afe6bef1685`・ref_b = 検証時main〔宣言commit〕`369b0c3028cda2a987b3dcd08cd718af703d2fbf`）で実行し、W treeを2回再構成。各回 12 Git blob pin + 19 SHA-256 pin = 31 pin + fold11機・fold12機・fold13機・fold14機の4 chain機・計35ファイル、`diff -r W_A W_B` が完全byte一致、fold11機入力pinの部分集合連鎖の機械確認（`subset-check fold11 pins 12 pin256 10 fold12 pins 12 pin256 13 fold13 pins 12 pin256 16 subset of fold14 12+19 OK` 行・値照合）が両参照で成立。1参照約1〜7秒でapi.github.com非依存（raw固定commit URL）。
- **rerun**（gate 19）: 出版検証機 `verify_fold14_external_20261121.py` を改変せずpristine再実行4回（r1/r2 同一cwd・r3 隔離copytree W/cwd/HOME〔隔離HOME/TMPDIR〕・r4 隔離+`PYTHONHASHSEED=random`）。全回 rc=0・`ALL 880 GATES PASS` 行・gate count 880（ok:true総数・all_gates_pass true）・出力監査JSON（91,543 bytes）が出版正本 `fe6370f7…` とbyte-identical・4回間でもbyte一致。検証機1回約53.1〜53.4秒（機内のfold14機4回プリ実行・fold11/12/13機独立rerun・機内tamper 2件〔出版社試験offset @200,222/@888,222〕込み）。
- **tampers**（gate 8）: 本レーン選択offset（出版社試験位置 worklist @200,222・証明書 @888,222、fold12第三検証レーン〔K1184〕の @150,000/@654,321、fold13第三検証レーン〔K1185〕の @222,999/@1,111,444、fold20/21/22/24第三検証・fold15/16 ext2の各レーンoffset群 @{7777,500000}/{253,17522}/{1234,17522,4096}/{117777,777777}/{208888,919191}/{300111,740321} とすべて別位置）の1 byte XOR 0x01 を隔離copytree W 上で実施:
  - t1 `inputs/worklist.csv` @333,444 → rc=1・`GATE FAILED [i]: W blob pin inputs/worklist.csv`・監査未書込（I-section legacy blob pin gate）
  - t2 `k1109/certs/win8-root-00000000000000909002200080100000-20261120.n11` @999,111 → rc=1・`GATE FAILED [i]: W sha256 pin …`・監査未書込（I-section sha256 pin gate）
  - 両実施後に本番Wを再照合（worklist SHA-256 `6d8a449e…`・K1109証明書 SHA-256 `b8a15f9a…`・無改変）。事前の手動探針（XOR 0x20・同offset）でも同一メッセージで発火することを別途確認済み。
- **finalize**: 以上partsを集計し、時刻・絶対path・実行時間（volatile）を含まないbyte決定的なharness監査JSON（6,723 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・解釈ガード5文つき・SHA-256 `717b7c9b392c0af2907bff6d874765292c87e7b82302101e94ceefb5f527f117`）を書き出し。**3実行**（battery 1・2 = 同一baseでの全stage再実行〔pin再取得込み〕・battery 3 = 隔離base+隔離cwd/HOME/TMPDIR+`PYTHONHASHSEED=random`）で**byte-identical**を確認。3 battery合計で出版検証機のpristine実行12回（+手動試行1回）・出版再構成機の実行6回・本レーンoffset tamper 6回がすべて受入条件どおりの結果。

## 実験事実

1. **fold14検証機はfold13機の約1.8倍・1回約53秒**: gate 880（fold13機は774）・1回53.1〜53.4秒。W treeは35ファイル（31 pin + 4 chain機・fold11〜14の全機がWに入る初の規模）。battery 1巡あたり約4分20秒（検証機pristine 4回+再構成2回+tamper 2件）。
2. **worklistはfold12/13と同一seriesファイルの3レーン連続再利用**（`inputs/worklist.csv`・SHA-256 `6d8a449e…`・360,834 bytes）。本レーンtamper offset（@333,444）はfold12第三（@150,000）・fold13第三（@222,999）と衝突せず、worklistのtamper探針位置が3レーンで別々である。
3. **K1109証明書はfold14 root初出の1,082,873 bytes**（`b8a15f9a…`）。第三検証側でもgate数880・監査91,543 bytesを出版値どおり再現。
4. **api.github.com枯渇の影響圏外**: 本batteryの全stage（pin・recon含む）はraw固定commit URLのみでapi.github.comを一度も呼ばない。手動探針・pin試行・fetch-backもすべてapi非依存で待機ゼロの冪等運転だった（同一sandboxで実施したK1185 batteryと同一の設計・K1185での環境リセット事故〔harness再構成・battery完全再生成で監査byte再現〕の教訓を本batteryでも時刻・絶対path排除として継承）。

## 再現手順

```sh
mkdir base && cd base
# 本dirの scripts/verify_k1178_fold14ext2_third_20261121.py を出版byteのまま配置
python3 scripts/verify_k1178_fold14ext2_third_20261121.py pin .       # 出版byte 5点取得+pin照合（network）
python3 scripts/verify_k1178_fold14ext2_third_20261121.py recon .    # W再構成2参照（raw固定commit URL）
python3 scripts/verify_k1178_fold14ext2_third_20261121.py rerun .    # 検証機pristine 4回（各約53秒）
python3 scripts/verify_k1178_fold14ext2_third_20261121.py tampers .  # tamper 2件 fail-closed
python3 scripts/verify_k1178_fold14ext2_third_20261121.py finalize . # harness監査JSON（byte決定的）
```

## 限界と解釈ガード

本検証はK1178第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない（fold14時点残余62→58行は当該receiptの既出版簿記・pool 120,416根は不変）。WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
