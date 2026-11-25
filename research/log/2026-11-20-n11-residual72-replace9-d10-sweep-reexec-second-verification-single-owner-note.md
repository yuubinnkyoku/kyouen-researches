# n11 残余23行 代替9根 depth-10掃引 全件再実行による独立第二検証の単一オーナー宣言（2026-11-20）

宣言時点の main: HEAD は 2026-11-20T14:14:15Z 時点の内容を確認済み。
対象K項目: K1146（残余23行の代替9根depth-10掃引・掃引正本 SHA-256
`e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`）。

## 着手する課題

K1146の18 probes（9根×両AND順序×depth 10）のうち掃引機が出版時に再実行したのは
4件のspot-checkのみであり、上流4掃引（K1086/K1089/K1091/K1095）に対して
K1144が確立した「全probe再実行による第二検証」の replace9 版を行う。

- pass A（本tree）と pass B（隔離cwd・別HOME・入力複写の別tree）の2パスで
  18 probe全件を runner v17（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`
  固定・Node.js）で再実行し、nodes/loss/capped/terminalStoneRange が
  出版記録（probe-records-replace9.jsonl・掃引正本per_root）と全件一致すること、
  新規実行から独立に再分類して WIN8-D10 candidate 1根
  `00000000010000809002000040002001`（両順序 uncapped loss=true）と
  REFUTED-D10 8根・nodes総計 3,574,172 が再現することを検査する。
- 出版掃引機械 `replace9_d10_sweep_20261120.py`（SHA-256
  `d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e5925b7d2512bcd41`）を
  隔離treeでpristine実行（assemble）し、20 gate PASS・正本JSON byte-identical
  を確認する。
- 残余23行宇宙（K1085→K1086→K1089→K1091→K1095の連鎖）と9根の被覆幾何
  （exactly-once・D4方位・gains hist {3:6,2:2,1:1}・child=root−最小セットビット）
  を本検証機械内で独立に再導入し、K1097 scope1 greedy選定・掃引正本と一致すること、
  probe-recordsと掃引正本per_rootの全項目一致を検査する。
- 入力はSHA-256 pinでfail-closed読み出し（K1085 `5fdd342d…`・
  K1086 `3045e152…`・K1089 `808fbda1…`・K1091 `edd7ac84…`・
  K1095 `335eca5e…`・K1097 `2896deb0…`・掃引正本 `e8f5d674…`）。
- 検証機械は stdlib のみ・乱数・時刻なし。監査正本JSONは同一cwd2回+別cwd別HOME
  1回の3実行でbyte-identicalを要する。
- 公表前に runner v17 の pilot_d6 制御（nodes 3,402・loss=false）と最小probe
  1件の出版記録一致を単独実行で確認済み。

## やらないこと

- 行の閉鎖claim・receipt fold（fold26 は先行レーンの宣言 `e53cc60c87` が所有）・
  証明書抽出（root `00000000010000809002000040002001` は宣言 `63877ffd2e` が所有）は
  対象外。
- 第5ラウンドrefsolve計画簿記（宣言 `ace38772d9` 所有）は対象外。
- REFUTED-D10をLOSS証明として読まない。node数・solved数を勝敗として読まない。

## 解釈規約

本検証は出版probe事実の再実行照合であり、いかなる新規の勝敗判定・行閉鎖も含まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて
UNKNOWN のまま。**

本課題の実行・出版の単一オーナーは本宣言の著者とする。
