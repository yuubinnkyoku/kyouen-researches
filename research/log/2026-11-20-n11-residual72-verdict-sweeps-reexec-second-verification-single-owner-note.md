# 単一オーナー宣言ノート: 残余72行の第1〜4ラウンド代替根 depth-10掃引 probe 全件再実行による独立第二検証（2026-11-20）

本レーンは、残余72行 safe8 候補供給の証拠基盤である第1〜4ラウンド代替根 depth-10掃引
（K1086 addtwo-greedy23・K1089 replace16・K1091 replace15・K1095 replace12）の
**出版probe記録（計132 probes = 46+32+30+24）の全件runner再実行・独立第二検証**について
単一オーナーとして着手する。並走レーンは本宣言項目に着手しないこと。

## 動機と位置づけ

K1097（残余23行 greedy9計画・replace9掃引の直接上流）の独立第二検証
（refuted50-refsolve-second-verification）と replace16 幾何・台帳第二検証（K1093）は
いずれも明示的に「DFPNエンジンの再実行は対象外」としており、4掃引132 probesのうち
出版機械自身が再実行したのは3件ずつのspot-check（計12 probes）のみである。
REFUTED-D10 50根の除外が作った pool P‴（120,424根）と WIN8-D10候補16根の判定は
1度だけのengine実行に依存している。本検証はこの面を独立実行で強化する。

## 範囲（やること）

- 対象: K1086掃引正本（SHA-256 `3045e152…`・46 probes）・K1089掃引正本（`808fbda1…`・
  32 probes）・K1091掃引正本（`edd7ac84…`・30 probes）・K1095掃引正本（`335eca5e…`・
  24 probes）の、各自のprobe-record JSONLに記録された全(root, ordering, depth-10)について
  runner v17（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`・固定コピー）を
  cap 30,000,000・timeout 280s・pilot_d6制御必須（nodes 3,402・loss=false・不成立時abort）で
  再実行し、nodes・loss・capped・terminalStoneRange が出版記録と**全件一致**するかを
  fail-closed検査する（ms/wall時刻値は除外）。
- 生child hex規約の独立再導入: child = root − 最小セットビット（簿記のみでverdictは指定に
  依存しない）を各記録について再導入し一致を要求する。
- 2パス実行: 同一機材でfresh 1パス（resume-safe記録）と、別cwd・別HOME・別EXPERIMENT_ROOTの
  隔離環境で第2パスを実行し、決定論的数値面（nodes/loss/capped/terminalStoneRange）が
  パス間でも一致することを確認する（出版値を含め3独立実行合意となる）。
- 判定分類・nodes総計の独立再導入: fresh結果からWIN8-D10候補/REFUTED-D10 fact分類と
  nodes総計（18,032,471 / 6,339,079 / 7,383,022 / 5,700,222）を再構成し出版正本と照合する。
- assemble gateは同一cwd 2回＋隔離環境1回の計3実行で正本JSON byte-identicalを要求する。

## やらないこと

- 行の閉鎖claim・receipt fold・証明書抽出・新規probe・新規掃引・計画変更は一切行わない。
- REFUTED-D10をLOSS証明として読まない。node数・solved数を勝敗として読まない。
- depth-10 を超えるVERDICTの主張は行わない。

## 解釈規約

本検証は出版済みverdict probe facts の再実行照合であり、行のゲーム理論的値には一切言及しない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
残余72行（現レーンの五親target残余23行を含む）は本検証では1行も閉じない。
fold26（宣言 `e53cc60c`/`ba659878`）・replace9掃引（宣言ノート
`research/log/2026-11-20-n11-residual72-replace9-d10-sweep-single-owner-note.md`）は
本宣言と対象が異なるため本宣言の影響を受けない。

- 宣言日時 (UTC): 2026-11-20T12:04:00Z
- 宣言時点の main HEAD: f519ccf560af326b088f746b5b759db45b12b0ee
