# 6×21 q=8 行欠損極大配置の非存在 — rowY 分解 3クラス完全走査（M_{6,8} の候補が {19,20,21} ∪ [23,371] に）

日付: 2026-11-14（高速レーン・並走run）

## 主張

1. **6×21（w=6・q=8・q点共円/共線禁止）に行欠損の極大安全配置は存在しない**。
   証拠: def OR 実例（「ある行 ≤ 6 石」の完全符号化）は 240s cap で INDET
   （5,011,833 conflicts・正直な負記録）だったため、**rowY 行固定分解**
   （V 対称 y↔5−y で 3 標準クラス y=0,1,2 が 6 行を完全被覆）を走査したところ
   **全 3 クラスが kissat 4.0.4 で UNSAT**（exit 20）:

   | rowY | conflicts | wall | 判定 |
   |------|-----------|------|------|
   | 0 | 327,636 | 14.0s | UNSAT |
   | 1 | 2,862,649 | 180.8s | UNSAT |
   | 2 | 1,767,690 | 92.6s | UNSAT |

   被覆論: 欠損配置は「ある行が ≤ 6 石」を満たし、その行 y の rowfixed 実例
   （¬rowGe[y] 単一節）に解として現れる。行鏡映 y↔5−y は盤面対称
   （安全・極大・欠損すべて不変）なので rowfixed(y) ≡ rowfixed(5−y)。
   よって y∈{0,1,2} の 3 実例の UNSAT は全欠損配置の不在を意味する
   （K0825/K0826 で SAT 側に使った rowY 分解の UNSAT 側適用）。
2. **第二符号化交差確認**: 最難クラス rowY=1 を `--lex=H`
   （列鏡映 lex-leader・rowY 制約を保存するので健全）で再符号化しても
   **UNSAT**（2,337,998 conflicts・144.2s）。
3. **陽性対照**: 6×18 def OR 実例は SAT（492,432 conflicts）・モデルは
   **41石 witness rows [7,7,7,7,6,7]**（K0815 の witness 盤面の行鏡映版）。
   census 不使用 sat.js verifyConfig と Python Fraction 独立実装の
   **2系統検証で safe+maximal+行欠損 PASS**。
   注意: 本対照は sat2.js def OR 実例であり、K0818/K0819 の対照
   （511,895 conflicts）は sat3.js クラス {1} 分解実例 — 別実例なので
   conflicts 数は直接比較できない（両者とも 6×18 に 41石witness がある
   という同じ事実を独立に確認）。
4. よって (6,8) の witness-free 幅集合は **{19, 20, 21}** に拡大
   （witness は 6×9..6×18・K0815）、**M_{6,8} ∈ {19, 20, 21} または ≥ 23**
   （上界 371 は K0318/K0024 代入で不変）。**witness 探索前線は 6×22**。

## 手法

- 符号化: `sat2.js`（K0810 census + sequential counter + 極大性）を repo から
  verbatim（`research/experiments/seven-row-q7-witness-search-20261114/scripts/sat2.js`・
  同じく sat.js・verify_witness.py・decode_verify.js）。def 単一節は
  「総石数 < 42 ⟺ ある行 ≤ 6」の完全符号化（各行 ≤ 7 は安全側制約）。
- ソルバ: kissat 4.0.4 公式 linux-amd64 バイナリ（変更なし）。
- 実行コマンド: `node sat2.js 6 21 8 --deficient cnf` /
  `node sat2.js 6 21 8 --rowY=Y cnf` /
  `node sat2.js 6 21 8 --rowY=1 --lex=H cnf`、各 `timeout 240`。
- 決定性の背景: 同一 sat2.js 機械は本日 (7,7) m=24 def OR（2,105,329）・
  m=25 rowY=3（756,785）および (7,9) m=100 def（18,075）で既知の記録値と
  conflicts が bit-exact 一致した実績あり（並走独立run較正）。
  2×8/2×9 q=4 制御（fastsat 121/535・kissat 37/316）も同日に bit-exact
  （seven-row-q7-witness-search-20261114/output/results.jsonl・controls）。

## 正直な負記録

- 6×21 def OR: 240s cap INDET（5,011,833 conflicts）。不在主張は
  rowY 分解に基づく（上記）。
- rowY=1 の lex=H 以外の第二符号化（rowY=0/2 の lex=H）は未実施。
  ただし 3 クラス UNSAT の被覆論には lex 交差確認は本質的でない
  （第一符号化の完全走査で十分）。

## 範囲と限界

有限機械検証（census 完全性・符号化正しさ・kissat 4.0.4 正確性まで）。
数論的証明ではない。M_{6,8} の確定には 6×22..6×370 の評価
（または K0342 型の普遍 tail 論証）が残る。11×11 空盤面・二石 root
{49,60}・S2 {59,60}・class 2・class 4 には影響せず UNKNOWN のまま。

## 備考

K番号は作業時点での仮番号（AGENTS.md の再採番規則による）。
K0818/K0819 の 35クラス分解（欠損集合 D の完全分割）に対し、本実験は
より粗い 3クラス rowY 分解で m=21 の非存在を達成した — m=21 では
rowfixed 実例（他行を自由に残す分、refute が本来難しい）が
予算内で反証可能だったことを示す。m=22 以降で rowY 分解が壁に戻った
場合の次手段は 35クラス分解（K0818 機械）。

