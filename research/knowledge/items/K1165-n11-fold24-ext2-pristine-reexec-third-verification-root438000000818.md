---
id: K1165
title: "fold24外部第二検証（K1164）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "K1164出版byteの第三者環境からのbyte再生確定"
  - "fold24外部第二検証harness gate 66・監査正本 efffaab8…"
  - "第三検証 root 00000000000000043800000008180010"
relations:
  - type: depends_on
    target: K1164
    note: 検証対象の外部第二検証。検証機（9bc24e38…）・監査正本（c7e10332…・gate 800）・実験README・実行記録のK1164出版byte一式を再取得・pin照合し、検証機を第三者環境で再実行した。
  - type: depends_on
    target: K1140
    note: fold24 receipt foldの出版byte（receipt c4ab76d3…・出版機 f462733d…・同梱独立監査 49f330c6…・再現log cb01749a…・reconstruct_inputs.py f4e1fa8e…）はK1164検証機の入力であり、本検証で再feedした。
  - type: depends_on
    target: K1136
    note: W再構成で検証機が再照合するK1136証明書（dbcb0bae…）・K1136監査正本（d0653834…）・K1091掃引記録（edd7ac84…）・runner v17 git blob（c132cc64…）。
  - type: depends_on
    target: K1133
    note: fold23 receipt正本（04f334ff…）。検証機の各実行はfold23機の隔離pristine rerun chainを含む。
artifacts:
  - path: research/experiments/n11-fold24-ext2-pristine-reexec-third-verification-root438000000818-20261120/README.md
    role: source
    note: 位置づけ・固定pin・実施内容と結果・再現手順・限界
  - path: research/experiments/n11-fold24-ext2-pristine-reexec-third-verification-root438000000818-20261120/scripts/verify_k1164_pristine_third_20261120.py
    role: verifier
    note: 第三検証harness（stdlibのみ・fail-closed・SHA-256 f45aa1ac…・14,351 bytes）
  - path: research/experiments/n11-fold24-ext2-pristine-reexec-third-verification-root438000000818-20261120/output/harness-audit.json
    role: verifier
    note: harness監査正本（status PASS・gate 66・3,184 bytes・SHA-256 efffaab8…）
  - path: research/experiments/n11-fold24-ext2-pristine-reexec-third-verification-root438000000818-20261120/output/reproduction.log
    role: data
    note: smoke実行1回＋battery 3実行（計13回の検証機再実行）の実行記録とbyte-identity
  - path: research/experiments/n11-fold24-ext2-pristine-reexec-third-verification-root438000000818-20261120/staged/k1164/README.md
    role: data
    note: K1164出版byte 4点のstaged copy（pin照合済み）
  - path: research/experiments/n11-fold24-ext2-pristine-reexec-third-verification-root438000000818-20261120/staged/k1140/README.md
    role: data
    note: K1140出版byte 8ファイルのstaged copy（receipt・出版機・同梱監査等・pin照合済み、この行は代表パス）
  - path: research/log/2026-11-20-n11-k1164-fold24-ext2-pristine-reexec-third-single-owner-note.md
    role: log
    note: 単一オーナー宣言ノート（commit 3c88de5ce4）・受入条件6項目
  - path: research/log/2026-11-20-n11-k1164-fold24-ext2-pristine-reexec-third-verification.md
    role: log
    note: 宣言から出版までの時系列記録
---

# fold24外部第二検証（K1164）のpristine再実行第三検証

## 対象と範囲

K1164（fold24 receipt fold＝K1140に対する外部第二検証）の出版byte一式に対し、
出版後の第三者がGitHubのpinned commitから取得したbyteのみを用いて、
K1164検証機の監査正本（`c7e10332…`・gate 800）がbyte単位で再生できることを確定した。
単一オーナー宣言（commit `3c88de5ce4`・2026-11-20T19:15:00Z）の受入条件6項目はすべて達成している。
fold23外部第二検証（`90ac8eed`）・fold25外部第二検証（`aad3b71c`）・
WIN8証明書行共有監査（`c403614f`）・fold26 receipt fold（`23bffdd4e4`）・
round-5 refsolve（`ace38772d9`）・WIN8-D10候補 `00000000010000809002000040002001`
の証明書抽出（`63877ffd2e`）は他レーン宣言済みであり着手していない。

## 結果

- harness `verify_k1164_pristine_third_20261120.py`（SHA-256 `f45aa1ac…`・stdlibのみ・fail-closed）は、
  staged出版byte 12点のSHA-256 pin照合、W入力treeの**2回独立再構成**のbyte一致
  （70ファイル・manifest digest `1426b676…`）、K1164検証機のpristine再実行
  （1 battery 4回: 同一cwd 2回・隔離cwd/HOME・隔離+`PYTHONHASHSEED=random`）、
  出版社T-gate未使用offsetによるtamper 3件のfail-closed捕捉、を1 batteryとして実行する。
- 3 battery（同一cwd 2回＋隔離HOME/cwd＋`PYTHONHASHSEED=random`）すべてPASS。
  検証機再実行はbattery内4回×3＋smoke 1回の計13回で、**全回の監査JSONが出版正本
  `c7e10332…` とbyte-identical**（各回はfold24機4回の再実行・fold23隔離rerun chain・
  同梱独立監査の再実行46/46・検証機自身のtamper 2件を含む）。
- 本レーン固有のtamper 3件（W worklist offset 404・W fold23 receipt記録 offset 3456・
  pub receipt offset 2024）はいずれもreturncode 1・監査未書込でfail-closed捕捉。
  出版社T-gateのoffset（777・12345）とは完全に別位置・別surfaceである。
- harness監査正本（`efffaab8…`・gate 66・3,184 bytes）は3実行でbyte-identical。
  出版byteはfetch-back照合16/16 byte-identical（curl・pinned commit SHA URL）。

実験事実として、harness初版のW manifest digest定数がshell側正準形（`./`接頭辞）で
書かれており、harness自身のfail-closed digest pin gateが最初のbattery前に捕捉した
（K1158・K1160・K1164出版時のpin転写typo捕捉と同じ防御パターンが第三検証harness側でも有効）。

## 限界

本検証は「検証の検証」であり、S6行・五親target行を1行も閉じない。
fold24 receiptが3行を閉じたのはfold24出版社の成果簿計、K1164はその外部第二検証の成立、
本項目は第三者による再現性の確定である。WIN8-D10証明書は当該8石rootのゲーム木に限られ、
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4は**すべてUNKNOWNのまま**。
