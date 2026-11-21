# fold10（第17 WIN7 receipt fold・外部第二検証）のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 [note](../../../log/2026-11-21-n11-fold10-17threceipt-ext2-pristine-reexec-third-single-owner-note.md)〔commit `4987c2b7dffd98d590ba65499bfb1caed3e1e939`・宣言 2026-11-21T05:58Z前後〕・t1期待値修正addendum [addendum](../../../log/2026-11-21-n11-fold10-17threceipt-ext2-pristine-reexec-third-single-owner-note-addendum.md)〔commit `274e3e28c43dc24e0c638f498051d75a75627bad`〕・受入条件5項目＋修正1項目）

## 位置づけ

fold10（root `00004000000000821082000000000100`・第17 WIN7-D10 receipt fold・K1071）に対して並走レーンが2026-11-19T21:11:45Z単一コミット `452af0c5cc91a195dd24f4e4086af9bba11e807f` で出版した外部第二検証（31 gate全PASS・チェーン入力非依存の幾何再導出+算術検証機・K番号なしのext2出版）を、出版社レーン以外の第三の実行環境（本sandbox）が**出版byteのみから再取得してpristine再実行・tamper・byte決定性を第三検査する**。n11検証ラティスではfold12〜16 ext2群（K1184〜K1188）・fold20（K1174）・fold21（K1168第三）・fold22（K1170）・fold24（K1165）・fold29 cert-extract（K1172）の第三検証が確定済みで、**WIN7 receipt fold系のext2に対する第三検証は本実験が初号**。対象ext2の構造上、W再構成はfold12〜16で用いた多段チェーン再構成ではなく**出版artifact 3点（fold10正本・fold9正本・第17証明書）のSHA-256 pin再取得のみ**で済み、検証機1回約1秒・battery 1巡約0.9秒とn11検証ラティス最小級である。

## 固定pin（出版byte・変更なしの再取得対象）

| file | bytes | SHA-256 |
|---|---|---|
| ext2 `README.md` | 3,982 | `240c8e588d07d72212bc5419d6606812d87f9181affe2ab0785ec336a14e3197` |
| ext2 `scripts/verify_fold10_second.py` | 11,145 | `7178fbe5fc31045ca36880863b72c6014c2997aa7e4731ac6dc20a88f85ac84f` |
| ext2 `output/fold10-second-verification-20261120.json`（出版監査正本） | 5,410 | `a62d6d50ffe3196ad2de1ff7b1df67ff8208b2a13510cce3f13aee0e9a085054` |

W入力（検証機内pin・走行時照合）:

| W | repo path | bytes | SHA-256 |
|---|---|---|---|
| fold10正本 | `n11-seventeenth-win7-receipt-fold-20261120/fold/output/seventeenth-win7-receipt-fold-20261120.json` | 12,918 | `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a` |
| fold9正本（windfall4=第13〜16 receipt） | `n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json` | 24,399 | `24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2` |
| 第17 WIN7-D10証明書 | `n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11` | 1,791,541 | `21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8` |

## 実施内容と結果（harness `scripts/verify_fold10ext2_third_20261121.py`・19,782 bytes・stage分割 pin/recon/rerun/tampers/finalize・stdlibのみ・fail-closed）

- **pin**（gate 6）: 上記3ファイルを出版byteのままpin commit `452af0c5…` のraw pinned URLから取得し、SHA-256・byte数を照合（6 gate all PASS）。
- **recon**（gate 15）: 3 W入力を2参照（ref_a = 宣言時HEAD `dcc5b96238c0232f0ff8eb07bd50be4243262938`・ref_b = 宣言commit `4987c2b7dffd98d590ba65499bfb1caed3e1e939`）のraw pinned URLから取得し、各SHA-256が検証機内pin（`bed7d331…`/`24db2352…`/`21dd2f0e…`）と一致・2参照間でbyte-identical・byte数一致・検証機の固定絶対pathへの配置後再照合（15 gate all PASS・12,918/24,399/1,791,541 bytes）。
- **rerun**（gate 24）: 出版検証機を改変せずpristine再実行4回（r1/r2 同一cwd〔共有run dir〕・r3 隔離copytree cwd+`env -i`隔離HOME/TMPDIR・r4 r3+`PYTHONHASHSEED=random`）。各回 rc=0・出力監査JSON（`gates_total 31`・`gates_all_pass true`・`status second-verified`・schema `n11-fold10-second-verification-20261120-v1`・`inputs_verified_by_sha256` 3点がW pinと一致）が出版正本 `a62d6d50…`（5,410 bytes）とbyte-identical・4回間でもbyte一致（24 gate all PASS・検証機1回約1秒）。
- **tampers**（gate 11）: 本レーン選択offset（fold12〜16第三検証各レーンoffset @{150,000,654,321}/{222,999,1,111,444}/{333,444,999,111}/{277,555,877,666}/{351,111,611,222}・fold20/21/22/24第三検証 @{7777,500000}/{253,17522}/{1234,17522,4096}/{117777,777777}・出版社試験位置 @{5077,28081}/{208,888,919,191}/{300,111,740,321} のいずれとも異なる）の1 byte XOR 0x01 をin-placeで実施:
  - t1 fold10正本 @12,345〔12,918 bytes内〕→ rc≠0・出力監査は `status gate-failed` で書込・**失敗gateはちょうど `fold10 正本 sha256 == published bed7d331...` の1件のみ**（証明書SHA-256 pin gate含む他30 gate全pass）・実施後復帰でbyte無改変。〔宣言ノート受入条件4の初回予測「json load失敗・監査未書込」は@12,345がメタデータ文字列 `_against_published_verdict_uni…` 内部でparse survivalする点で誤りであり、battery前にaddendum（commit `274e3e28`）で修正してから実施〕
  - t2 第17証明書 @1,234,567〔1,791,541 bytes内〕→ rc≠0・出力監査は `status gate-failed`・**失敗gateはちょうど `cert sha256 pin matches local byte-exact file` の1件のみ**（fold10 SHA-256 pin gateはpass）・実施後復帰でbyte無改変。
  - post: 3 W入力の再照合が全pin一致（無改変）（11 gate all PASS）。
- **finalize**: 以上を集計し、時刻・絶対path・実行時間（volatile）を含まないbyte決定的なharness監査JSON（**10,980 bytes・gate 56〔pin 6・recon 15・rerun 24・tampers 11〕・all_gates_pass true・解釈ガード5文+unknown guardつき・SHA-256 `2a97d052bd1f0de95331f6d2b62322b61b38af326743a3dc244e4064a9abd7aa`**）を書き出し。**3 battery**（B1 fresh base全stage→B2 同一base全stage再実行〔pin再取得込み〕→B3 隔離base+全体を`env -i`隔離HOME/TMPDIR+`PYTHONHASHSEED=random`で実行）で**byte-identical**を確認（battery 1巡約0.9秒・`cmp` 完全一致）。

## 実験事実

1. **t1予測の誤りをbattery前にaddendumで修正**: 宣言ノート初版のt1予測（「json load失敗で監査未書込」）に対し、予備探針で@12,345がfold10正本のメタデータ文字列内部でありparse survivalすることが判明。実際の挙動は「**対象入力のSHA-256 pin gateが単独で失敗**し、他30 gateは全pass、監査は`gate-failed`で書込」の、より精密なfail-closedであり、t2とあわせて**2種の入力pin gateが互いに独立して発火する**ことを1 battery内で実証する構成となった。誤った予測のままbatteryを実施せず、宣言ノート出版後に所有者addendum（commit `274e3e28`）で修正してから全batteryを実施した（batteryは修正後のものだけを正本とする）。
2. **n11検証ラティス最小級の第三検証対象**: 検証機1回約1秒・W再構成はraw pinned 3点取得のみ・battery 1巡約0.9秒×3巡。fold12〜16第三検証（1回約14.4〜215秒・battery 1巡約1〜14分）と対照的に、拡張対象が増えても低コストで再実行できる。
3. Byte決定性（絶対path固定のW配置・run dir copytree・`PYTHONHASHSEED=random`）は第三実装・第三環境で監査byte不変（3 battery byte一致・`ALL 56 GATES PASS`）。
4. 受入条件5項目＋addendum修正1項目すべてPASS。

## 再現手順

```sh
mkdir base && cd base
# 本dirの scripts/verify_fold10ext2_third_20261121.py を出版byteのまま配置
python3 scripts/verify_fold10ext2_third_20261121.py pin .      # 出版byte 3点取得+pin照合（network・raw固定commit URL）
python3 scripts/verify_fold10ext2_third_20261121.py recon .   # W 3点の2参照再取得+pin照合+配置
python3 scripts/verify_fold10ext2_third_20261121.py rerun .   # 検証機pristine再実行4回（各約1秒）
python3 scripts/verify_fold10ext2_third_20261121.py tampers . # tamper 2件 fail-closed
python3 scripts/verify_fold10ext2_third_20261121.py finalize .# harness監査JSON（byte決定的）
```

## 限界と解釈ガード

本検証はfold10外部第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない。WIN7-D10証明書は当該7石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## ファイル

- `scripts/verify_fold10ext2_third_20261121.py`: 第三検証harness（純stdlib・決定的・fail-closed・19,782 bytes・SHA-256 `cb0af4abffa7261314cc75774845361422357cc95f29fd08ae0c56d6896a9ca6`）
- `output/fold10ext2-third-harness-audit.json`: harness監査正本（10,980 bytes・gate 56・SHA-256 `2a97d052bd1f0de95331f6d2b62322b61b38af326743a3dc244e4064a9abd7aa`）
- `output/reproduction.log`: battery 3巡の実行記録（3,483 bytes・SHA-256 `7166137a1863effa070873a73641248932222f56704524258a57f78dafc70851`）
