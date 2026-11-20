---
id: K1172
title: "K1166（fold29証明書抽出外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "K1166 fold29 ext2 pristine re-execution third verification"
  - "K1136/K1137/K1139 WIN8-D10 certificate extraction battery third-environment reproduction"
  - "fold29 third-verification record a6a3e048"
relations:
  - type: verifies
    target: K1166
    note: "K1166の外部第二検証について、出版byte・61ファイル再構成・43 gate battery・監査正本の決定性を第三の実行環境で再確認した。"
artifacts:
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/README.md
    role: source
    note: "対象・受入条件・実施結果・限界・再現手順"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/output/third-verification.json
    role: verifier
    note: "20 gate全PASSの第三検証正本。SHA-256 a6a3e048…・4,363 bytes"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/output/reproduction.log
    role: data
    note: "2 batteryの実行記録・受入条件対照・負の制御"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/scripts/assemble_third_record.py
    role: verifier
    note: "stdlibのみ・fail-closed・決定的な20 gate記録組立器"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/scripts/reproduce.sh
    role: source
    note: "固定refからの出版byte取得・master再構成・2 battery再実行手順"
  - path: research/log/2026-11-21-n11-k1166-fold29-ext2-pristine-third-verification.md
    role: log
    note: "第三検証の実施判断・結果・出版記録"
---

# K1166外部第二検証の第三環境再実行

## 対象と範囲

K1166が対象としたK1136・K1137・K1139の3件のWIN8-D10証明書抽出について、外部第二検証の出版byteと実行手順を第三の実行環境で再実行した。単一オーナー宣言は `research/log/2026-11-20-n11-k1166-fold29-cert-extract-ext2-pristine-reexec-third-single-owner-note.md`（commit `ec24b235f806822086680fee4075820679c78acf`）。本項はその受入条件を満たした第三検証の記録であり、新しい証明書抽出器や第四の独立検証実装を意味しない。

## 検証結果

- K1166の出版byte 5点（README・取得器・pin表・harness・監査正本）を固定commit `1c42dcf25c78540033c5ec08c00952e4a939a8ee` から取得し、各SHA-256を照合した。出版監査正本は15,549 bytes・SHA-256 `cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f`・43 gate・PASS。
- 改変していない `fetch_master.py` で上流pin commit `28d223a2dd254b8a85cc342dff3f4bd801d1b31f` から3実験dirの61ファイルを再構成し、Git blob pin 61/61が一致した。
- 出版harnessを改変せず2 battery実行。第1回は通常の作業場所・HOME、第2回は隔離cwd・隔離HOME・`PYTHONHASHSEED=random`。各回とも43 gate全PASSで、監査正本は出版正本とbyte-identical。
- 2 batteryの監査正本に加え、pin・K1136・K1137・K1139・tamperの5分割記録もbattery間でbyte-identical。
- 出版harness内蔵のtamper 3件（証明書本文offset 300007、pin入力offset 1111、fresh nodes 2757→2758）は両batteryでreturncode 1・監査未書込となりfail-closedで捕捉された。
- 第三検証record組立器は20 gate全PASS。正本は4,363 bytes・SHA-256 `a6a3e0489411cd7f48fa53c2679505344f06389b8458b64c2b34e21fdf1fb18c`。既定hash seedで2回、`PYTHONHASHSEED=random`で1回実行し、3出力がbyte-identicalだった。
- 出版監査正本の未試験offset 8888を1 byte改変する追加の負の制御では、組立器がreturncode 1となり第三検証recordを新規出力しなかった。正本を復元した後のrecord SHA-256は元と一致した。

## 解釈と限界

この検証が確認するのは、K1166の外部第二検証の出版byte・入力再構成・実行結果・監査記録の再現性である。K1136/K1137/K1139のWIN8-D10証明書自体の適用範囲を広げず、追加のゲーム木やS6行を閉じない。残余20行と候補pool 120,416根は不変である。

WIN8-D10は記載された8石rootのゲーム木に限る。REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗と読まない。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4は引き続きUNKNOWN。
