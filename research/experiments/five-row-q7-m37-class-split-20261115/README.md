# five-row-q7-m37-class-split-20261115

COMPLETE — 高速レーン・単一連続実行（リセットなし）。5×37 q=7 の行欠損極大不存在を
class-split SAT（kissat 4.0.4・19行鏡映正準欠損クラス完全分解）で確定。
**band-closure レーン（five-row-q7-band-closure-35-157-20261115）の def-mode 決着と
独立な符号化で一致 — 5×37 は3幅目の二重決着**（m=35 K0849・m=36 K0850 に続き）。

## 結果

- 17 直接クラスすべて UNSAT（合計 **1,480,209** — m36 の 1,535,197 より **3.6%減**・
  最難 {0,1} 223,591 は m36 対応 257,251 より **13.0%減** で m36 の直接最難
  非漸減〔+1.9%〕は一時的と確定）。
- {0},{1} krow k=0..4 すべて UNSAT（合計 **467,058** — m36 の 524,103 より **10.9%減**・
  {1}k4 172,488 は22.1%減・{0}k4 133,829 は10.2%減）。
- {0},{1} k=5 × minpos=0..18（**19点×2クラス**・健全上限は floor((37−1)/2)=**18 に増加**）
  38点すべて UNSAT（{0}k5p 合計 1,149,751・{1}k5p 合計 1,632,290・最難 {1}k5p0
  **472,443/18.82s** — m36 対応 492,545 より4.1%減・{0}k5p0 345,111 は m36 対応
  298,680 より **+15.6% で m37 で唯一の局所的非漸減**・新minpos=18 点は 5,019/6,218）。
- deciding 65例合計 **4,729,308 conflicts**・INDET 0・SAT 0（事前予想 ~4.7M は0.6%誤差で
  的中・m23→m37: 20,916,467 → … → 5,423,024 → 5,011,486 → 4,729,308）。
  lex=H 交差確認 {0,1}/{2} UNSAT（200,526/98,758）・lexH込み 5,028,592
  （=total_conflicts_37）・records 68件総計 5,371,726。
- 陽性対照 5×18 {0} SAT **343,134** が K0821..K0850 15レーン対照と bit-exact
  （**16度目の cross-lane 再現**）・verifyConfig PASS（29石 rows 5,6,6,6,6）。
- 生ログ68件は batch ごとに push・**remote blob sha をローカル git-hash と全件照合**。
  records/summary は mkrecords5737.js で生成・push 前に node で records.jsonl を
  独立再計算（直接 1,480,209 + krow 467,058 + k5p 2,782,041 = deciding 4,729,308）。

## 位置づけ — band-closure レーンとの交叉確認

- m=37 は **five-row-q7-band-closure-35-157-20261115（IN FLIGHT）の def-mode UNSAT
  で決着済み**（genfast3 弦対抽象円 census・1インスタンス）。本実験は同レーン README の
  並走協調ノートに従い、**異なる census・異なる符号化（class-split 65 deciding
  instances）での交叉確認**として実施し、**両者は一致**。m=35〔K0849〕・m=36〔K0850〕
  に続き3幅目の二重決着。
- class-split レーンとしての系譜は K0821(m21)..K0850(m36) と同一。
- **band-closure レーンの残る前線は m=38, 39, 50..157 — 本レーンはそれらには着手しない**
  （同レーンの領域）。

## 境界

- (5,7) witness-free 幅集合（class-split 系）は **{19,...,37}**。
  集合形式 M∈{19,…,37} または ≥38・**鋭い形 M=19 または ≥39**（K0821 監査規約を
  拡大集合に適用・M=38 は検証済み witness-free 幅 37 の witness を要求するため不可）。
  上界 158（K0332 代入）は不変。

## 手法（K0850 から m=37 への移植・minpos 健全上限は 18 に増加）

- 65 deciding CNF: 17直接クラス + {0},{1} krow k=0..4（10件）+
  {0},{1} k=5 × minpos=0..18（38件・19点×2クラス）。minpos の健全上限は
  floor((37−1)/2) = **18 に増加**（columns 0..36 で min(x_min, 36−x_max) ≤ 18）。
  lex=H 交差確認 {0,1}/{2} + 陽性対照 5×18 {0}。CNF 総数 68（対照込み）。
- スクリプト: sat.js/sat2.js/sat3.js は K0836..K0850 レーンと byte-identical
  （blob sha 6c3262d6 / edfae1d2 / 6dfa7db3）。mkcnf.sh/qrun.sh は m=36→m=37
  移植・旧識別子の残留なし。対照 CNF c5x18q7_0.cnf は md5 同一再生成
  （0bb6187d36e537a170e4fb451359bb94）。
- **mkrecords5737.js の訂正記録**: claim 時版の minpos レコードリストから '18' が
  欠落していた（sed アンカー不一致）・records 生成前に発見・修正し本コミットで
  差し替え。CNF・生ログには影響なし（mkcnf.sh の minpos ループは最初から 0..18 で
  68 CNF が正しく生成済み・qrun も 19点ずつ完走）。
- ソルバ: kissat 4.0.4 official linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）。

## スコープ

有限機械検証（K0810 census・class-split 符号化・k×minpos 分解の正しさ
（K0816/K0818 で小盤 ground-truth 検証済み）・kissat 4.0.4 まで）。
m ≥ 38 の持続性は open（band-closure レーンが掃引中・残り m=38, 39, 50..157）。
