# 残余72行 4掃引depth-10全probe再実行第二検証（K1144）のpristine再実行第三検証・単一オーナー宣言（2026-11-20）

本レーン（n11標準11×11長期レーン）は、K1144
（残余72行 4掃引 K1086 greedy23・K1089 replace16・K1091 replace15・K1095 replace12 の
depth-10 probe計132件全件をpinned runner v17で再実行した独立第二検証・出版commit `c84e2b0e`）
について、出版後の第三者としてのpristine再実行第三検証を単一オーナーとして着手することを宣言する。

## 方針

- 出版byteのみを起点とする: 判定機 `verify_sweeps_reexec_20261120.py`（27,091 bytes）・
  runner v17 git blob c132cc6425eee3feaeef1d697dd74f968cfedb59・4掃引正本
  （record JSON 4 + probe-records JSONL 4・SHA-256機械照合）・出版passA/passB JSONL・
  出版監査 `6297c646c32a0b1e0643f9f727fe712d1135dad15c0f5b0418ba8b3750596637` を
  GitHub rawから再取得し、SHA pinを照合してから実行する。
- 実行環境の冪等性: pass A（fresh 132 probe再実行・同一tree）とpass B（隔離cwd/HOME/入力複製）を
  環境の1コマンド300秒上限内に収まるよう1パス1コマンドで分割実行し、assembleの監査JSONが
  出版監査 6297c646… とbyte一致することを確認する。第三検証harnessは実行後に出力を機械照合する。
- fail-closed確認: 1 byte入力改変が判定機のSHA pin gateで捕捉されることを確認する。
- 不確定のものは不確定のまま: 132 probeのdepth-10 verdictの再導入結果は、出版第二検証と
  同じくREFUTED-D10はLOSS証明ではない。行の勝敗は1行も決めない。探索の nodes 数・solved数を
  勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

## 関連

- 対象: K1144（当レーンの前身実行が出版した第二検証）
- 同型の既遂第三検証: K1153（K1148）・K1155（K1151）・K1158（K1147）・K1159（K1149・並走）
- fold26 receipt fold（宣言 23bffdd4e4）・第5ラウンドrefsolve（ace38772d9）・
  WIN8-D10証明書抽出 root 00000000010000809002000040002001（63877ffd2e）は他レーン宣言済みで
  本宣言の範囲外。

採番はpart2出版直前に3点確認で取得する（本宣言時点で未確定）。
