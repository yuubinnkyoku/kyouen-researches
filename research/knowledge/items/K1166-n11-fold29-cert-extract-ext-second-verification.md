---
id: K1166
title: "K1136/K1137/K1139 WIN8-D10証明書抽出の外部再実行第二検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "残余29行レーン3証明書抽出の外部第二検証 gate 43"
  - "fold29 cert-extract外部第二検証 監査正本 cf6a26ab…"
  - "root 00000000000000043800000008180010・00000000000200003800200008180000・0000000800000000380000000810000a の証明書byte再生"
relations:
  - type: depends_on
    target: K1136
    note: root 00000000000000043800000008180010 の証明書抽出実験（証明書dbcb0bae…・34,845行・監査正本d0653834…）の出版byte一式をpin commit 28d223a2dから再取得し、probe・抽出・検証器・監査機械を再実行して出版正本と照合した。
  - type: depends_on
    target: K1137
    note: root 00000000000200003800200008180000 の証明書抽出実験（証明書7bd64a47…・19,527行・監査正本dafa177b…）の出版byte一式を同様に再検証した。
  - type: depends_on
    target: K1139
    note: root 0000000800000000380000000810000a の証明書抽出実験（証明書089e175d…・48,020行・監査正本e706ca6f…）の出版byte一式を同様に再検証した。出版社ext-summaryの行順序はK1139のみ辞書順で、行順序はpublisher transport detailとして再現対象外と規約化した。
artifacts:
  - path: research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120/README.md
    role: source
    note: 位置づけ・受入条件対達成結果・行順序規約・msの扱い・再現手順・限界
  - path: research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120/verify_cert_extract_ext_second_20261120.py
    role: verifier
    note: 第二検証harness（stdlibのみ・fail-closed・SHA-256 ca662e57…・30,141 bytes・stage分割・43 gate・監査JSONは時刻なしbyte決定的）
  - path: research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120/fetch_master.py
    role: data
    note: pin commit 28d223a2ddから出版61ファイルを取得しgit blob SHA照合する取得器
  - path: research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120/pin-manifest.json
    role: data
    note: 61ファイル分のgit blob pin正本（runner v17 git blob c132cc64… 3点込み）
  - path: research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120/output/harness-audit.json
    role: verifier
    note: harness監査正本（status PASS・gate 43・15,549 bytes・SHA-256 cf6a26ab…・3巡byte一致）
  - path: research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120/output/fresh/k1136/probe-fresh.jsonl
    role: data
    note: 3根の本レーンfresh実行記録一式（probe・ext-summary a1/a2/b・bigint・bareiss・監査×3・fresh-data差し替え分。この行は代表パス）
  - path: research/log/2026-11-20-n11-k1136-k1137-k1139-cert-extract-ext-second-verification-single-owner-note.md
    role: log
    note: 単一オーナー宣言ノート（commit c9d5b415a84e）・受入条件7項目
  - path: research/log/2026-11-20-n11-fold29-cert-extract-ext-second-verification.md
    role: log
    note: 宣言から出版までの時系列記録
---

# K1136/K1137/K1139 WIN8-D10証明書抽出の外部再実行第二検証

## 対象と範囲

残余29行レーンの3証明書抽出
（K1136: root `00000000000000043800000008180010`・K1137: root
`00000000000200003800200008180000`・K1139: root
`0000000800000000380000000810000a`・各8石WIN8-D10）に対し、
出版社の3実験dir全61ファイルをgit blob SHAでbyte pin
（pin commit `28d223a2dd`）し、pin byteだけからprobe・抽出A1/A2/B・
BigInt検証・Bareiss検証・19 gate監査機械を新規再実行して出版正本と照合した。
単一オーナー宣言（commit `c9d5b415a8`・2026-11-20T19:43:48Z）の
受入条件7項目はすべて達成した。fold/fold23/fold25/fold26外部第二検証・
round-5 refsolve・WIN8-D10 root `00000000010000809002000040002001` 証明書抽出・
WIN8証明書行共有監査は他レーン宣言済みであり着手していない。

## 結果

- harness `verify_cert_extract_ext_second_20261120.py`（SHA-256 `ca662e57…`・
  stdlibのみ・fail-closed・監査JSONは`ms`等時刻依存字段を含まないbyte決定的設計）は
  stage分割（pin → root k1136/k1137/k1139 → tampers → finalize）で1 battery約8分を
  3回実行し、**全回gate 43 PASS・監査正本 `cf6a26ab…`（15,549 bytes）
  byte-identical**（慣行最小限界の3実行一致）。
- pin 61/61（runner v17 git blob `c132cc64…` 3点・証明書3点
  `dbcb0bae…`/`7bd64a47…`/`089e175d…` 込み）。probe fresh再実行は3根×8レコード
  全決定論的字段一致。抽出A1/A2/Bのper-move値は出版と完全一致
  （A1総計 3,539,166/1,399,389/3,515,506・B 2,564,865/1,057,553/2,808,991・
  A1==A2 per-move byte一致）し、A1証明書組立が出版証明書3点とbyte-identical、
  BigInt・Bareiss再実行も出版byteとbyte-identical。
- 出版監査機のpristine再実行3回（同一cwd 2回＋隔離EXPERIMENT_ROOT 1回）と
  本レーンfresh記録差し替え実行がいずれも19/19 PASS・監査正本が出版正本
  `d0653834…`/`dafa177b…`/`e706ca6f…` とbyte-identical。
- tamper 3件（出版社未試験offset: 証明書本文offset 300007・監査pin入力
  offset 1111・fresh summary nodes 2757→2758）はいずれもreturncode 1・
  監査未書込・gate failでfail-closed捕捉。t1では `bareiss --root-check` が
  strategy行由来の改変を見ない（returncode 0）ことを副次的に実測し、
  root-check単独では防衛として不十分なことを機械記録した（防衛の深さ）。
- 実験事実として、出版ext-summary-a1/a2の行順序はK1136/K1137はxargs数値順・
  **K1139は辞書順**であった。行順序はpublisher transport detailであり
  再現対象外と規約化し、per-move値照合（order非依存）で判定した。
  実行中にsandbox環境リセットが1回発生したが、当局pin表からmasterを再取得・
  git blob再照合してbatteryを再開した（中断も実験事実として記録）。
- 出版byteはfetch-back照合44/44 byte-identical（curl・pinned commit SHA URL・
  part1 commit `80ce56914d`）。

## 限界

本検証は「検証の検証」であり、行を1行も閉じない。
残余20行・pool P⁗ 120,416根は不変。WIN8-D10証明書は当該8石rootのゲーム木に
限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4は
**すべてUNKNOWNのまま**。
