---
id: K1164
title: "fold24 receipt fold（root 438000000818）の外部第二検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold24外部第二検証 root 00000000000000043800000008180010"
  - "K1140出版byteの第三実装による値単位再確認"
  - "別実装外部検証機・gate 800・監査正本 c7e10332…"
relations:
  - type: depends_on
    target: K1140
    note: fold24 receipt fold正本（SHA-256 c4ab76d3…）・出版機（f462733d…）・同梱独立監査（49f330c6…）・出版再現log（cb01749a…）・reconstruct_inputs.py（f4e1fa8e…）の全出版byteを検証対象とする。
  - type: depends_on
    target: K1136
    note: 検証機がW再構成で再照合するK1136証明書（dbcb0bae…）・K1136検証記録（d0653834…）・runner v17 git blob（c132cc6425eee3feaeef1d697dd74f968cfedb59）。
  - type: depends_on
    target: K1133
    note: fold23正本（04f334ff…）。出版機pristine再実行はfold23機の隔離rerun gate込みで全chainを再計算する。
artifacts:
  - path: research/experiments/n11-fold24-external-second-verification-root438000000818-20261120/README.md
    role: source
    note: 位置づけ・固定pin・実施内容と結果・再現手順・限界
  - path: research/experiments/n11-fold24-external-second-verification-root438000000818-20261120/scripts/verify_fold24_external_20261120.py
    role: verifier
    note: 第三実装の外部検証機（stdlibのみ・fail-closed・SHA-256 9bc24e38…・55,555 bytes）
  - path: research/experiments/n11-fold24-external-second-verification-root438000000818-20261120/output/external-audit.json
    role: verifier
    note: 外部監査正本（status PASS・gate 800・36,605 bytes・SHA-256 c7e10332…）
  - path: research/experiments/n11-fold24-external-second-verification-root438000000818-20261120/output/reproduction.log
    role: data
    note: 3実行＋出版前確認1回のstdoutとbyte-identity記録
  - path: research/log/2026-11-20-n11-fold24-external-second-verification-single-owner-note.md
    role: log
    note: 単一オーナー宣言ノート（commit 434d53f3e3）・受入条件7項目
  - path: research/log/2026-11-20-n11-fold24-external-second-verification.md
    role: log
    note: 宣言から出版までの時系列記録
---

# fold24 receipt fold（root 438000000818）の外部第二検証

## 対象と範囲

K1140のfold24 receipt foldに対し、出版社以外の実行主体が別実装の検証機で出版byteを再確認した。
単一オーナー宣言（commit `434d53f3e3`）の受入条件7項目をすべて達成している。
fold25外部第二検証（`aad3b71ca3`）・fold26 receipt fold・round-5 refsolve・
WIN8-D10候補 `00000000010000809002000040002001` の証明書抽出は他レーン宣言済みであり着手していない。

## 結果

- 検証機はstdlibのみの第三実装で、出版機・同梱監査機と実装を共有しない。fail-closed・決定論的出力。
- 出版byte 5点のSHA-256 pin照合、W再構成61 pinの再照合、出版機pristine再実行4回
  （fold23機の隔離rerun chain込み・receipt byte-identical）、
  同梱独立監査の再実行46/46 byte-identical、tamper 2件のfail-closed捕捉、を確認した。
- 全chain再導出は出版receiptと値単位で一致: base 6,438行→fold23 frontier 6,126/485,438、
  C(8,6)=28部分幾何のD4正準行を2方法（224合成ops/28正準化）で再導出、主張3行・closed cost 225・
  余剰0行、親delta 4親class 2計6、frontier_after 1,725/6,123/485,213/4,431/351,661/11,660、
  五親target 86/112・残余26行。
- gate 800全PASS。監査正本（SHA-256 `c7e10332…`・36,605 bytes）は同一cwd 2回＋隔離cwd/HOME＋
  `PYTHONHASHSEED=random` の3実行でbyte-identical。出版直前に既定環境で4回目を再実行し、
  同一SHA-256を再確認した（実測49.5秒・script実行ごとに機械4回と同梱監査1回とtamper 2件を含む）。

実験事実として、検証機初版のK1091掃引pin定数SHA転写typo（`deda…`→正 `ded0…`）を
検証機自身のfail-closed pin gateが実行前に捕捉した（K1158・K1160と同じ防御パターン）。

## 限界

本検証はreceipt簿記の再検査であり、行を1行も閉じない。fold24 receiptが3行を閉じたのは出版社の成果簿記で、
本項目の成果はその外部第二検証の成立である。WIN8-D10は当該8石rootのゲーム木に限る証明書であり、
REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて**UNKNOWN**のまま。
