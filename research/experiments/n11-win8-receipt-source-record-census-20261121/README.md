# n11-win8-receipt-source-record-census-20261121

既刊 WIN8 receipt fold 11〜25（第18〜第32 receipt・全15通りの
`receipt-fold` 実験）に対する**読み取り専用 provenance census** の成果物一式。
単一オーナー宣言:
`research/log/2026-11-21-n11-win8-receipt-source-record-census-single-owner-note.md`
（commit `32cb492c5b`・先行宣言なしを直近コミット列で確認済み）。
本censusは各receiptの `independent_verification.source_record` と
`certificate_source` の記載正誤を機械判定した**報告**であり、
検証の本体ではない。行は1行も閉じず、証明書内容の検証・receipt fold・
既存正本の変更は一切行わない。

## 主結果（2026-11-21時点）

- **全180 structural gate PASS**（15 receipt × 12 gate: ordinal連続・
  singleton receipts・WIN8-D10・stones=8・root/raw_root_hex一致・
  repo path形式4種・自dir証明書SHA-256一致・自dir検証JSON SHA-256一致）。
  fetch・parse・gateの全失敗はfail-closed（出力未書込）。
- **IV.source_record分類: own 12 / stale 3**。
  - stale 3例: **fold12**（第19 receipt `8005021`・K1175 erratum対照と
    同一内容の機械的再確認）・**fold15**（第22 receipt `120000038`・
    K1179 erratum対照と同一内容）・**fold18**（第25 receipt `00901010`・**本censusによる新規発見**）。
  - fold18 receiptの `independent_verification.source_record` は
    `research/experiments/n11-residual55-win8-cert-extract-root22081000-20261120`
    （fold17証明書抽出実験）を指しており、正しくは自rootの証明書抽出実験
    `research/experiments/n11-residual48-win8-cert-extract-root00901010-20261120`
    を指すべきである。fold17/18/19/23/25 単体ext2（他レーン宣言済み）への
    事前通知として記録する。なお当該レーンはそれらreceiptを出版した
    実験の改変・erratum判断の権限を持たない。
- **コピー仮説の機械的裏付け**: stale 3例すべて
  `iv_equals_previous_fold_iv = true` かつ
  `iv_dir_equals_previous_fold_own_dir = true`
  （fold12←fold11・fold15←fold14・fold18←fold17。
  直前fold receiptからsource_record欄を写したと読める挙動が3/3で成立）。
- **certificate_source は15/15で清潔**: 全receiptの
  `certificate_source.record` は自rootの証明書抽出実験dirを指し、
  `certificate_path` の実在byteの SHA-256 がreceipt記載
  `certificate_sha256` に、自dir検証JSONのSHA-256が
  `verification_sha256` に、証明書bytes数が `certificate_bytes` に
  それぞれ15/15で一致（`certificate_source_blocks_correct_count = 15`）。
  clean 12 foldは fold11/13/14/16/17/19/20/21/22/23/24/25。
- 入力は全て raw.githubusercontent.com の**固定commit URL**（pin
  `32cb492c5b13bdab00f5bdad11de06391fcb1274` = 宣言ノート出版HEAD）から
  静的fetch。api.github.com非依存。15 receipt JSON + 15 証明書 `.n11`
  + 15 検証JSON の計45 fetch、1実行約1.4秒。
- census正本 `output/census.json`（34,758 bytes・
  sha256 `c801564d907efb7697717034360e09bae77f1634903adbad38db71c7e93bcca8`）は
  同一cwd 5回＋隔離cwd/HOME＋`env -i`+`PYTHONHASHSEED=random` 1回の
  計6実行でbyte-identical。時刻・乱数・環境依存値を含まない。

## 位置づけ

- stale判定はprovenance上の記録誤り候補の報告であり、当該rootの証明書・
  検証の成否そのものを左右しない。fold18を含む全15 certificate・
  verificationのSHA参照は今回の機械照合で部品単位では全て正しい。
- WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10は
  LOSS証明ではない。receipt foldは行の閉鎖簿記であり、閉じた行の
  ゲーム理論的値を主張しない。nodes数・solved数・coverage数を勝敗として
  読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

## レイアウト

```
scripts/
  win8_receipt_source_record_census.py  # census機械（stdlibのみ・決定的・fail-closed）
                                        # sha256 e7cffd18f218445a40ae4cea220b998b9b85dc1af80ef456b67bc1bb1c6ab975
output/
  census.json                           # census正本（6実行byte一致）
                                        # sha256 c801564d907efb7697717034360e09bae77f1634903adbad38db71c7e93bcca8
  reproduction.log                      # 実行記録
```

## 実行方法

```sh
python3 scripts/win8_receipt_source_record_census.py
# cwd直下に output/census.json を書く。pinは機械内定数
# 32cb492c5b13bdab00f5bdad11de06391fcb1274（宣言ノート出版HEAD）。
```

初版機械草案はroot末尾比較を整数比較で実装していたため出版前に
suffix比較へ修正しbatteryを実施し直した（旧2案 sha256
`fec82a94…`/`e822f45c…` は未出版破棄・旧batteryは無効）。
