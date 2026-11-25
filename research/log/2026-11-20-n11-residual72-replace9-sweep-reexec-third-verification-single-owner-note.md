# 単一オーナー宣言： 残余23行 代替9根掃引再実行第二検証（K1149）の pristine再実行による第三検証（2026-11-20）

- 宣言時刻： 2026-11-20T16:01:30Z
- 宣言者： n11長期レーン（第三検証系譜： K1153・K1155・K1157と同型）
- 対象： [K1149](../knowledge/items/K1149-n11-residual72-replace9-sweep-reexec-second-verification.md)
  （残余23行 代替9根depth-10掃引の全18 probe再実行による独立第二検証。item側の二重採番（six-row K1149 `6e05d59b`）には関与しない。実験dir `n11-residual72-replace9-sweep-reexec-second-verification-20261120/`・検証機 commit `7ab77aa1` 刊行・検証機 SHA-256 `77cdd9e3…` 41,175 bytes・監査正本 SHA-256 `27fc420c58ac0c979e09c3a35b0b0b886fe1b521efea9de8f9f98e51e6264072` 11,242 bytes・24/24 gate）
- 実施内容： GitHub上の出版byteのみから
  (1) 検証機 `verify_replace9_reexec_20261120.py`（SHA-256 pin）・runner v17固定コピー（git blob pin `c132cc6425eee3feaeef1d697dd74f968cfedb59`）・入力8正本（K1085 `5fdd342d…`・K1086 `3045e152…`・K1089 `808fbda1…`・K1091 `edd7ac84…`・K1095 `335eca5e…`・K1097 `2896deb0…`・出版probe-records `bdacf0e7…`・出版掃引正本 `e8f5d674…`）・出版掃引機 `d163b2a1…`・出版監査正本 `27fc420c…` を再取得してpin照合、
  (2) 18 probeをpass A（本tree・4 workers・budget 240s・Node runner v17 azul固定）とpass B（隔離cwd/HOME入力複写tree）で新規再実行し、両パスの決定性字段（nodes/loss/capped/terminalStoneRange）が出版記録と全件一致・nodes総計 3,574,172 であることを確認、
  (3) 出版掃引機を隔離treeでpristine再assembleし出力が出版正本 `e8f5d674…` とbyte-identicalであることを確認、
  (4) 検証機assembleをpassA/passB/pristine入力で実行し出力が出版監査 `27fc420c…` とbyte-identical（24/24 gate PASS）であることを確認、
  (5) 1 byte tamperをfail-closed pinが捕捉することを確認、
  (6) 第三検証harnessとその監査正本を自完結実験dirとして出版。
- CPU並列： 4 workers（repo方針の目安内）。実行時間は各パス数十秒の見込み。
- 編成： 宣言 → part1（実験dir： README+harness+監査）→ part2（K item+研究log）→ part3（knowledge README末尾bullet）。K番号はpush直前に3点確認で確定する。
- 着手しない領域： K1147外部第二検証の第三検証（宣言 `887e594d`）・fold26 receipt fold（`23bffdd4e4`）・第5ラウンドrefsolve（`ace38772d9`）・WIN8-D10証明書抽出 root `00000000010000809002000040002001`（`63877ffd2e`）・K1149二重採番の解消（管轄外・six-row側itemには一切触れない）はいずれも本宣言の範囲外。
- 解釈規約： loss=true（uncapped）はdepth-10内必敗のprobe事実の再現であり証明書抽出の資格を本検証は与えない。loss=false（uncapped）はREFUTED-D10 probe事実の再現でありLOSS証明ではない。nodes数・solved数を勝敗として読まない。本検証は行を1行も閉じない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
