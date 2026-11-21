# K1173（fold20 receipt fold・外部第二検証）のpristine再実行第三検証

実験日: 2026-11-20〜21
担当: n11長期レーン（単一オーナー宣言 `research/log/2026-11-20-n11-k1173-fold20-ext2-pristine-reexec-third-single-owner-note.md`・commit `1d68addb2f5acc98f4a182877922c2ffe8235b26`・宣言 2026-11-20T23:45:26Z・受入条件5項目）

## 位置づけ

K1173（fold20 receipt fold・root `00000000000000003800000008d10000`・K1129出版byteの第三実装による外部第二検証・2026-11-20T23:26-23:30Z出版・part1 `f2213982`+監査修正commit `cf453602`・part2 `268a061f`〔K item〕・part3 `33633f7b`〔knowledge README bullet〕）に対し、出版社レーン以外の第三の実行環境（本sandbox）が出版byteのみから実験dir・検証機・監査正本を再取得し、pristine再実行・tamper・byte決定性を第三検査した。n11検証ラティスの fold24 ext2（K1164→K1165第三）・fold22 ext2（K1167→K1170第三）・fold29 cert-extract ext2（K1166→K1172第三）と同一手続き系列の第三verificationである。

## 固定pin（出版byte・変更なしの再取得対象）

すべて commit `cf45360245f66489c8364ac16df7eda0fc01e22e`（part1修正・実験dir最終変更commit）から取得しSHA-256照合（harness pin stage・fail-closed）:

| file | bytes | SHA-256 |
|---|---|---|
| `README.md` | 11,503 | `66511c69c0eaab81f81bfab57f1f04912ecb39531ffcb4266dc55ded009013fa` |
| `scripts/reconstruct_fold20_inputs.py` | 10,168 | `bf21d0428300168a8c8bf90637334c35250b91786fc784b53bfdfef1104a92b8` |
| `scripts/verify_fold20_external_20261120.py` | 52,131 | `30877beff08f5647ffac6455c0f6aa50f716078791e9c022f80886909f03755b` |
| `output/external-audit.json` | 128,175 | `5a9bb98feb907ebefe5eeddf1c15acd241eae7911ae0cc258ff27f4dc3e3e5ad` |
| `output/reproduction.log` | 6,992 | `e34224288a48b785cc338887f3bd18f7d35c8b0509b420892e398a6e2df85a3b` |

## 実施内容と結果（harness `verify_k1173_fold20ext2_third_20261120.py`・17,424 bytes・stage分割 pin/recon/rerun/tampers/finalize・stdlibのみ・fail-closed）

- **pin**（gate 10）: 上記5ファイルを出版byteのままraw pinned URLから取得し、SHA-256・byte数を照合。
- **recon**（gate 12）: 出版再構成機 `reconstruct_fold20_inputs.py` を改変せず2参照（ref_a = 宣言時HEAD `992851e21eebeaa5883c3a6fa0230e2a79f46bba`・ref_b = 検証時main `bb4d147b36a605ab5605bbac105d570a4818893f`）で実行し、W treeを2回再構成。各回 12 Git blob pin + 37 SHA-256 pin = 49 pin + chain機4台（fold19機 `51442d96…`・fold18機 `dcdfbf92…`・fold18 preverified写し `d342f1f8…`・fold20機 `9e141d4a…` ルート配置）・計53ファイル、`diff -r W_A W_B` が完全byte一致、fold19機入力pin（12 blob + 34 SHA-256）の49 pin部分集合性の機械確認が両参照で成立。
- **rerun**（gate 19）: 出版検証機 `verify_fold20_external_20261120.py` を改変せずpristine再実行4回（r1/r2 同一cwd・r3 隔離copytree W/cwd/HOME〔`env -i`・隔離HOME/TMPDIR〕・r4 隔離+`PYTHONHASHSEED=random`・`FOLD_PREVERIFIED_CHAIN` 不使用・各回fold19機pristine rerun gate→fold18 preverified→K1120 gate群の推移的再検証込み）。全回 rc=0・`ALL 1317 GATES PASS`・出力監査JSONが出版正本 `5a9bb98f…`（128,175 bytes）とbyte-identical・gate count 1,317（ok:true総数）・4回間でもbyte一致。検証機1回約20〜21秒。
- **tampers**（gate 8）: 本レーン選択offset（出版社試験位置 worklist@5077・K1121証明書@28081 と別位置）の1 byte XOR 0x01 を隔離copytree W 上で実施:
  - t1 `inputs/worklist.csv` @7777 → rc=1・`GATE FAILED [i]: W blob pin inputs/worklist.csv`・監査未書込（I-section legacy blob pin gate）
  - t2 `k1121/certs/win8-root-00000000000000003800000008d10000-20261120.n11` @500000 → rc=1・`GATE FAILED [i]: W sha256 pin …`・監査未書込（I-section sha256 pin gate）
  - 両実施後に本番Wを再照合（worklist SHA-256 `6d8a449e…`・K1121証明書 SHA-256 `8513e366…`・無改変）。
- **finalize**: 以上partsを集計し、時刻・絶対path・実行時間（volatile）を含まないbyte決定的なharness監査JSON（6,213 bytes・gate 49〔pin 10・recon 12・rerun 19・tampers 8〕・all_gates_pass true・解釈ガード5文つき・SHA-256 `24fac0b91c6e0e15a12a9f9a36b4b9f684dac7d25503801ceef3f45e0296834c`）を書き出し。**3実行**（battery 1・2 = 同一baseでの全stage再実行・battery 3 = 隔離base+隔離cwd/HOME+`PYTHONHASHSEED=random`・各battery約90〜100秒）で**byte-identical**を確認。

## 実験事実

1. **api.github.com無認証quotaの共有IP枯渇**: battery 2巡目の recon ref_b 実行が `HTTP Error 403: rate limit exceeded`（core remaining 0・reset 00:23:59Z表示）で中断した。1巡目の両参照と2巡目ref_aは同一実行で成功。参照は固定refのため再実行は冪等で、quota復旧後（00:04Z時点でremaining 60を確認）にbatteryを最初からやり直して3巡完走させた。K1167第三検証レーンの21:45Z枯渇（quota共有IP共喰い）と同じ失敗モード。出版物は再実行後のbatteryのみを使用（中断時の成果物は不採用）。
2. **harness開発中の転写誤りを自レーンpin gateが捕捉**: 初版harnessのFILES表で出版監査正本SHA-256に1文字余分の `7` を誤挿入（正 `…ff27f4dc…` が `…ff277f4dc…`）し、pin stageが取得byte実測値との不一致で即 `STAGE FAILED [pin]` で捕捉した。K1158/K1160/K1164/K1170の「打鍵定数はfail-closed pinが捕捉する」防御パターンの再実証（出版物は無被害・harness修正後にbatteryをやり直した）。
3. **byte決定性バグを出版前に捕捉**: 初版harnessのfinalizeがpartsを丸ごとauditに写したため `wall_ms_not_in_audit` フィールド（実行時間・毎回変動）がaudit JSONに混入し、3実行byte一致を壊す設計になっていた。finalizeに再帰的なvolatile-key除去（`*_not_in_audit` 接尾辞）を追加して修正し、batteryを最初からやり直した（publication後であれば監査正本のbyte不変性を毀損する事故になった）。
4. **実行環境リセット事故（00:02Z頃・300秒超過bash呼び出し起因）**: harness開発と予備実行が完了した直後の待機pollingが300秒上限に到達してsandbox環境がリセットされ、出版前の作業dir一式（予備pristine 4回・隔離実行・tamper・draft）が消失した。宣言ノートは出版済み（repoが正本）のため無被害。batteryは固定refから出版byteを再取得・再実行する設計なので、復旧後にbattery 3巡を最初から完走させた（成果物の正本は最終3巡batteryのみ）。**教訓: 待機pollingは240秒以内に区切る・成果物はrepo出版を正本とする**。
5. **出版社batteryの第三環境での素直な完走**: K1173の第二検証battery（検証機1回約21秒・純python）は300秒bash上限のstage分割で第三環境でも素直に完走する。K1172（battery 1巡約8分）と対照的に軽量で、再実行コストが低い。

## 再現手順

```sh
mkdir base && cd base
# 本dirの scripts/verify_k1173_fold20ext2_third_20261120.py を出版byteのまま配置
python3 scripts/verify_k1173_fold20ext2_third_20261120.py pin .       # 出版byte 5点取得+pin照合（network）
python3 scripts/verify_k1173_fold20ext2_third_20261120.py recon .    # W再構成2参照（raw+api trees・3 call/参照）
python3 scripts/verify_k1173_fold20ext2_third_20261120.py rerun .    # 検証機pristine 4回（各約21秒）
python3 scripts/verify_k1173_fold20ext2_third_20261120.py tampers .  # tamper 2件 fail-closed
python3 scripts/verify_k1173_fold20ext2_third_20261120.py finalize .  # harness監査JSON（byte決定的）
```

## 限界と解釈ガード

本検証はK1173第二検証の再現性・入力pin・fail-closed防衛・監査byte決定性の第三検査であり、receiptの再発行・行の追加閉鎖・WIN/LOSS verdictの追加は行わない。行は1行も閉じない（fold20時点残余41→38行はK1129の既出版簿記・pool P⁗ 120,416根は不変）。WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
