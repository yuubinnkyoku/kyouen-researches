# 2026-11-28 three-row q=4 m=28 SAT 行和分割 完了ログ（高速レーン）

単一オーナー継続宣言 `cfcdffdeb7afa26e000251c46edb27965bcce9f0`
（`2026-11-28-three-row-q4-m28-partition-continuation-note.md`・publish-then-execute・
宣言時 HEAD `548695e70c8544d8637fb26221c959a149092da9`）の実行完了記録。

## 実行概要

- 目的: P(28)（3×28・q=4 行欠損極大 witness 非存在・列挙閉包 ext28plus で既確定）の
  SAT 行和分割による独立確認 = 2方法化。m≥29 の新幅主張なし。
- 器材: m25/m26 kit と同一 pin（sat.js/sat2.js/sat3.js/sat4.js/verify34.py・
  split_piece.py m25 版・partition_closure_3row.py m26 版・kissat 4.0.4 公式
  linux-amd64〔zip sha256 `63282e51…`・binary sha256 `21da5d98…`〕・Node v22.20.0）。

## 較正（宣言前に実施・宣言文に開示）

1. m=26 全16 CNF を再生成し m26 kit 出版 `cnf_manifest_m26.txt` と **16/16 md5 一致**
   （rowY=1 は --lex=H,V・rspec は 0:a,1:b,2:c 形式）。
2. m=26 代表4片を pinned kissat で実行し出版 `records_m26.jsonl` と
   **4/4 conflicts bit-exact 一致**: s_0-2-0=1・k_r0_0=611・s_2-2-2=18,195・
   s_3-2-2=202,989（全 UNSAT・rc=20）。

## 本番実行（m=28）

- CNF 生成: cnf28/ 16件（row-k 4 + rspec 12）+ split28/ 56件
  （s323〔rowY=1〕28片 + s233〔rowY=0〕28片）。curves 10,269。
- 決定: **全70実行 UNSAT・INDET 0・呼び出し cap 超過片 0**（wall 予算駆動の逐次実行・
  最大片 s233_c11 318,508 conflicts / wall 44s）。
- 台帳合計: 8,381,193 conflicts（参考値・非加法）。
  row-k: (0,0) 408・(0,1) 82,598・(1,0) 380・(1,1) 78,112。
  row-sum: (0,2,0) 1・(1,2,0) 0・(1,2,1) 1,147・(2,2,0) 70・(2,2,1) 3,520・
  (2,2,2) 27,560・(2,3,2) 275,232・(3,2,0) 143・(3,2,1) 14,173・(3,2,2) 312,503。
  split: (3,2,3) 28片合計 3,364,388（max c07 264,558）・
  (2,3,3) 28片合計 4,220,958（max c11 318,508）。両家族の c27 は 0 conflicts
  （leftmost stone = 最右列は lex=H 制約で即時 UNSAT）。
- 閉包: `partition_closure_3row.py out28/records_m28.jsonl m28` が
  **decided 63 / pending 0 / uncovered 0 / SAT 0**（exit 0）。
- 決定性: 代表2件（s233_c11・(2,2,2)）の再実行で conflicts bit-exact 一致
  （318,508・27,560・rc とも一致）。

## 正直開示

- 本 session 開始時に m=27 は未宣言だったが、宣言ノート出版の直前チェックで
  並走 lane の m=27 宣言（`65e22558`）を発見したため、m=27 への着手を取りやめ
  m=28 に切り替えた（重複回避・宣言文に明記）。m=27 は同 lane が 19:55Z に完走
  （`ddbe1392`・全 UNSAT）したため、本レーンとの重複実行はゼロ。
- 分割治具は m25 kit の `split_piece.py` を byte-clone して使用（初版の改行 bug は
  m25 lane で修正済みの版）。本レーンでの治具バグ・fail-closed 事象なし
  （全片 rc=20 で終了・parse error 0）。
- (3,2,3)/(2,3,3) のベース片一体実行は実施していない（m25 lane の nohup 死滅の
  教訓により分割片の全 UNSAT で反証する方式を継承）。
- verdict NOT consumed。本レーンは w=3 固定幅で標準 11×11 盤に無関係。
  **標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN・conflicts は bookkeeping。**

## 意味

P(24), P(25), P(26), P(27), P(28) が SAT 分割・列挙閉包の2方法一致となった
（P(29..31) は列挙閉包単独のまま）。M_{3,4} ∈ [24,69] 不変・
witness-free 幅 {24..31} 不変・m≥32 は open（wsearch34.js 治具拡張が本命）。

## 成果物

- kit: `research/experiments/three-row-q4-m28-partition-20261128/`
  （README・scripts 2件〔split_piece.py・partition_closure_3row.py〕・
  output 5件〔cnf_manifest_m28.txt・records_m28.jsonl・m28_partition_closure.json・
  raw_decisions_m28.txt・determinism_m28.txt〕）
- K1183: artifacts・scope/evidence・追記3 を更新（同一 commit 鎖の別 commit）。
