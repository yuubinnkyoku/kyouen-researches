# K1175（fold12 receipt fold・外部第二検証）のpristine再実行第三検証

実験日: 2026-11-21
担当: n11長期レーン（単一オーナー宣言 `research/log/2026-11-21-n11-k1175-fold12-ext2-pristine-reexec-third-single-owner-note.md`・commit `4c7a12f1aed44205f20824be024a382d161a7a4c`・宣言 2026-11-21T02:50Z・受入条件5項目）

## 位置づけ

K1175（fold12 receipt fold・root `00000000000000003800000008005021`・第19 receipt・2番目WIN8 receipt foldの出版byteに対する第三実装外部第二検証・2026-11-21T00:53Z出版・part1 `20e5f2f215`→`984c48a767`→`adb1e8f605`〔監査正本まで5ファイル出揃い〕・part2 `49ddfc3468`〔K item〕・part3 `928ae7834e`〔knowledge README bullet〕）に対し、出版社レーン以外の第三の実行環境（本sandbox）が出版byteのみから実験dir・W再構成機・検証機・監査正本を再取得し、pristine再実行・tamper・byte決定性を第三検査した。n11検証ラティスの fold24 ext2（K1164→K1165第三）・fold22 ext2（K1167→K1170第三）・fold29 cert-extract ext2（K1166→K1172第三）・fold20 ext2（K1173→K1174第三）・fold21 ext2（K1168第三）と同一手続き系列であり、fold12〜16単体ext2第二検証群（K1175/K1176/K1178/K1179/K1180）の第三検証の第一号である。

## 固定pin（出版byte・変更なしの再取得対象）

すべて commit `adb1e8f605b6903f6a671d9447c001b79f401398`（part1最終・実験dir5ファイル出揃いcommit）から取得しSHA-256照合（harness pin stage・fail-closed）:

| file | bytes | SHA-256 |
|---|---|---|
| `README.md` | 5,258 | `d1eae7793398051b44c1a0d1ecf65404e239e13e1e63a90d7da240d329cc6a1e` |
| `scripts/reconstruct_fold12_inputs.py` | 8,906 | `caa30f346ede97324f0cc268c2b3adf74ae8ce26a8691be4dadbaf66f3da6710` |
| `scripts/verify_fold12_external_20261121.py` | 53,934 | `43afc1cd31d5d731858388532d5b07266ac60b2e7265f2490fc6574d5a6578f9` |
| `output/external-audit.json` | 70,149 | `c309d69337461518390b7a5cb466e49da6c5c98b7fbcd0a4fd187bf03b52eb07` |
| `output/reproduction.log` | 5,668 | `d85d8c3d59a406f2a798716ad779d916cf4d45193cd4bee567dd0fb956d7e199` |

## 実施内容と結果（harness `verify_k1175_fold12ext2_third_20261121.py`・18,624 bytes・stage分割 pin/recon/rerun/tampers/finalize・stdlibのみ・fail-closed）

- **pin**（gate 10）: 上記5ファイルを出版byteのままraw pinned URLから取得し、SHA-256・byte数を照合。
- **recon**（gate 16）: 出版再構成機 `reconstruct_fold12_inputs.py` を改変せず2参照（ref_a = 宣言時HEAD `91f2f0f13164bfe3bd4734f907d5ea3fd27e1c7c`・ref_b = 検証時main〔宣言commit〕`4c7a12f1aed44205f20824be024a382d161a7a4c`）で実行し、W treeを2回再構成。各回 12 Git blob pin + 13 SHA-256 pin = 25 pin + fold11機 `9b3e06c8…`・fold12機 `706bfa7a…` の両chain機・計27ファイル、`diff -r W_A W_B` が完全byte一致、fold11機入力pin（12 blob + 10 SHA-256）の25 pin部分集合性の機械確認（`subset-check … OK` 行・値照合）が両参照で成立。1参照約7秒でapi.github.com非依存（raw固定commit URL）。
- **rerun**（gate 19）: 出版検証機 `verify_fold12_external_20261121.py` を改変せずpristine再実行4回（r1/r2 同一cwd・r3 隔離copytree W/cwd/HOME〔隔離HOME/TMPDIR〕・r4 隔離+`PYTHONHASHSEED=random`）。全回 rc=0・`ALL 655 GATES PASS` 行・gate count 655（ok:true総数・all_gates_pass true）・出力監査JSON（70,149 bytes）が出版正本 `c309d693…` とbyte-identical・4回間でもbyte一致。検証機1回約14〜15秒（機内のfold12機4回プリ実行・fold11機独立rerun〔vr〕・機内tamper 2件〔出版社試験offset @96300/@456789〕込み）。
- **tampers**（gate 8）: 本レーン選択offset（出版社試験位置 worklist@96300・K1106証明書@456789、およびfold20/21/22/24第三検証・fold13-16 ext2の各レーンoffset群 @{7777,500000}/{253,17522}/{1234,17522,4096}/{117777,777777}/{200222,888222}/{208888,919191}/{300111,740321} とすべて別位置）の1 byte XOR 0x01 を隔離copytree W 上で実施:
  - t1 `inputs/worklist.csv` @150000 → rc=1・`GATE FAILED [i]: W blob pin inputs/worklist.csv`・監査未書込（I-section legacy blob pin gate）
  - t2 `k1106/certs/win8-root-00000000000000003800000008005021-20261120.n11` @654321 → rc=1・`GATE FAILED [i]: W sha256 pin …`・監査未書込（I-section sha256 pin gate）
  - 両実施後に本番Wを再照合（worklist SHA-256 `6d8a449e…`・K1106証明書 SHA-256 `69f32661…`・無改変）。
- **finalize**: 以上partsを集計し、時刻・絶対path・実行時間（volatile）を含まないbyte決定的なharness監査JSON（6,587 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・all_gates_pass true・解釈ガード5文つき・SHA-256 `06750caa90188ec3c7203d2b2b80eb0bfb61f818f29727a5d13ee5f3cb2137f2`）を書き出し。**3実行**（battery 1・2 = 同一baseでの全stage再実行〔pin再取得込み〕・battery 3 = 隔離base+隔離cwd/HOME/TMPDIR+`PYTHONHASHSEED=random`・各battery約60〜62秒）で**byte-identical**を確認。3 battery合計で出版検証機のpristine実行12回・出版再構成機の実行6回・本レーンoffset tamper 6回がすべて受入条件どおりの結果。

## 実験事実

1. **harness初版の転写誤りを自レーンpin gateが捕捉**:FILES表の検証機SHA-256に1文字の誤植（正 `…43afc1cd31d5d73185…` に対し `…31d5f73185…`）があり、pin stageが取得byte実測値との不一致で即 `STAGE FAILED [pin]` で捕捉した（K1158/K1160/K1164/K1170/K1174と同じ「打鍵定数はfail-closed pinが捕捉する」防御の再実証・出版物は無被害・harness修正後にbatteryを最初からやり直した）。
2. **fold12第二検証batteryは第三環境で最軽量級**: 検証機1回約14〜15秒（fold20第三検証の約21秒・fold22の約34秒と比べても軽い）。W treeが27ファイルと判明（fold20の53ファイルと対照的・fold12機の入力pinが25個相当）。stage分割なしでも単一bash呼び出しで完走可能な規模だが、300秒上限の運用規律通りstage分割した。
3. **出版検証機の内部scratchは絶対path固定**（`/home/user/work/f12ext/runs`）で環境隔離r3/r4でも同一pathを用いる設計のため、harnessは検証機を厳密に逐次実行した（実行の重なりによるscratch競合は発生条件ごと排除・audit byteへの影響なし）。
4. **ref_a・ref_bともにapi.github.com非依存のraw固定commit URLでW再構成冪等**: 6回の再構成（battery 1〜3 × 2参照）すべて待機ゼロ・全pin照合・2 W tree byte一致。api.github.comは本batteryで一度も呼んでいない（K1175出版時とは対照的にquota枯渇の影響圏外）。

## 再現手順

```sh
mkdir base && cd base
# 本dirの scripts/verify_k1175_fold12ext2_third_20261121.py を出版byteのまま配置
python3 scripts/verify_k1175_fold12ext2_third_20261121.py pin .       # 出版byte 5点取得+pin照合（network）
python3 scripts/verify_k1175_fold12ext2_third_20261121.py recon .    # W再構成2参照（raw固定commit URL）
python3 scripts/verify_k1175_fold12ext2_third_20261121.py rerun .    # 検証機pristine 4回（各約15秒）
python3 scripts/verify_k1175_fold12ext2_third_20261121.py tampers .  # tamper 2件 fail-closed
python3 scripts/verify_k1175_fold12ext2_third_20261121.py finalize .  # harness監査JSON（byte決定的）
```

## 限界と解釈ガード

本検証はK1175第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない（fold12時点残余68→65行は当該receiptの既出版簿記・pool P⁗ 120,416根は不変）。WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
