# five-row-q7-m36-class-split-20261115

COMPLETE — 高速レーン・単一連続実行（リセットなし）。5×36 q=7 の行欠損極大不存在を
class-split SAT（kissat 4.0.4・19行鏡映正準欠損クラス完全分解）で確定（K0850）。
**band-closure レーン（five-row-q7-band-closure-35-157-20261115）の def-mode 決着と
独立な符号化で一致 — 5×36 は2系統の符号化で witness-free が二重決着。**

## 結果

- 17 直接クラスすべて UNSAT（合計 **1,535,197** — m35 の 1,636,361 より **6.2%減**・
  最難 {0,1} 257,251 は m35 対応 252,381 より **+1.9%** で唯一の局所的非漸減）。
- {0},{1} krow k=0..4 すべて UNSAT（合計 **524,103** — m35 の 729,321 より **28.1%減**
  で m35 の krow 合計非漸減は一時的と確定・{1}k4 221,525 は 37.1%減）。
- {0},{1} k=5 × minpos=0..17（18点×2クラス・健全上限は floor((36−1)/2)=**17 のまま**）
  36点すべて UNSAT（{0}k5p 合計 1,177,015・{1}k5p 合計 1,775,171・最難 {1}k5p0
  **492,545/17.61s** — m35 対応 496,388 より0.8%減・{0}k5p0 298,680 は11.8%減）。
- deciding 63例合計 **5,011,486 conflicts**・INDET 0・SAT 0（事前予想 ~5.1M は0.2%誤差で
  的中・m23→m36: 20,916,467 → … → 5,423,024 → 5,011,486）。lex=H 交差確認 {0,1}/{2}
  UNSAT（196,313/97,192）・lexH込み 5,304,991（=total_conflicts_36）・records 66件
  総計 5,648,125。
- 陽性対照 5×18 {0} SAT **343,134** が K0821..K0849 14レーン対照と bit-exact
  （**15度目の cross-lane 再現**）・verifyConfig PASS（29石 rows 5,6,6,6,6）。
- 生ログ66件は batch ごとに push・**remote blob sha をローカル sha1 と全件照合
  （66/66 OK）**。records/summary は mkrecords5736.js で生成・push 前に node で
  records.jsonl を独立再計算（直接 1,535,197 + krow 524,103 + k5p 2,952,186 =
  deciding 5,011,486）。

## 位置づけ — band-closure レーンとの交叉確認

- m=36 は **five-row-q7-band-closure-35-157-20261115（IN FLIGHT）の def-mode
  UNSAT で既に witness-free と決着済み**（genfast3 弦対抽象円 census・
  1インスタンス）。本実験は同レーン README の並走協調ノートに従い、
  **異なる census・異なる符号化（class-split 63 deciding instances）での交叉確認**
  として実施し、**両者は一致**。m=35（K0849 + def-mode）に続き2幅目の二重決着。
- class-split レーンとしての系譜は K0821(m21)..K0849(m35) と同一。
- band-closure レーンは m=37 と m=40..49 も def-mode UNSAT 済み（IN FLIGHT・
  知識統合は同レーンで実施予定）。残る前線は m=38, 39, 50..157 — **本レーンは
  それらには着手しない**（同レーンの領域）。

## 境界

- (5,7) witness-free 幅集合（class-split 系）は **{19,...,36}**（K0850 で m=36 追加）。
  集合形式 M∈{19,...,36} または ≥37・**鋭い形 M=19 または ≥38**（K0821 監査規約を
  拡大集合に適用・M=37 は検証済み witness-free 幅 36 の witness を要求するため不可）。
  上界 158（K0332 代入）は不変。

## 手法（K0849 から m=36 への移植・minpos 健全上限は 17 のまま）

- 63 deciding CNF: 17直接クラス + {0},{1} krow k=0..4（10件）+
  {0},{1} k=5 × minpos=0..17（36件・18点×2クラス）。minpos の健全上限は
  floor((36−1)/2) = **17 のまま**（columns 0..35 で min(x_min, 35−x_max) ≤ 17）。
  lex=H 交差確認 {0,1}/{2} + 陽性対照 5×18 {0}。CNF 総数 66。
- スクリプト: sat.js/sat2.js/sat3.js は K0836..K0849 レーンと byte-identical
  （blob sha 6c3262d6 / edfae1d2 / 6dfa7db3）。mkcnf.sh/qrun.sh は m=35→m=36
  移植・旧識別子の残留なし。対照 CNF c5x18q7_0.cnf は md5 同一再生成
  （0bb6187d36e537a170e4fb451359bb94）。
- ソルバ: kissat 4.0.4 official linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）。

## スコープ

有限機械検証（K0810 census・class-split 符号化・k×minpos 分解の正しさ
（K0816/K0818 で小盤 ground-truth 検証済み）・kissat 4.0.4 まで）。
m ≥ 37 の持続性は open（band-closure レーンが掃引中・m=37,40..49 は同レーン記録済み）。

