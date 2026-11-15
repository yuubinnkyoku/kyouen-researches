# five-row-q7-m36-class-split-20261115

IN FLIGHT (claim) — 高速レーン。5×36 q=7 の行欠損極大不存在を class-split SAT
（kissat 4.0.4・19行鏡映正準欠損クラス完全分解）で判定する。

## 位置づけ — band-closure レーンとの交叉確認

- m=36 は **five-row-q7-band-closure-35-157-20261115（IN FLIGHT）の def-mode
  UNSAT で既に witness-free と決着済み**（genfast3 弦対抽象円 census・
  1インスタンス）。本実験は同レーン README の並走協調ノートに従い、
  **異なる census（sat3.js 全三つ組相当の弦対・別実装）・異なる符号化
  （class-split 63 deciding instances）での交叉確認**として実施する。
  両者が一致すれば m=36 の非存在は2系統の独立符号化で確定。
- class-split レーンとしての系譜は K0821(m21)..K0849(m35) と同一
  （直接17クラス + {0},{1} の k×minpos 完全分解 + lex=H 交差確認 + 陽性対照）。
- m=38, 39, 50..157 の帯掃引には着手しない（band-closure レーンの領域）。

## 手法（K0849 から m=36 への移植・minpos 健全上限は 17 のまま）

- 63 deciding CNF: 17直接クラス + {0},{1} krow k=0..4（10件）+
  {0},{1} k=5 × minpos=0..17（36件・18点×2クラス）。minpos の健全上限は
  floor((36−1)/2) = **17 のまま**（columns 0..35 で min(x_min, 35−x_max) ≤ 17）。
  lex=H 交差確認 {0,1}/{2} + 陽性対照 5×18 {0}。CNF 総数 66。
- スクリプト: sat.js/sat2.js/sat3.js は K0836..K0849 レーンと byte-identical
  （blob sha 6c3262d6 / edfae1d2 / 6dfa7db3）。mkcnf.sh/qrun.sh は m=35→m=36
  移植・旧識別子の残留なし。対照 CNF c5x18q7_0.cnf は md5 同一再生成
  （0bb6187d36e537a170e4fb451359bb94）。
- 較正: 対照 5×18 {0} kissat SAT **343,134 conflicts 再現済み**
  （K0821..K0849 14レーン対照と bit-exact・**15度目の cross-lane 再現**）。
- ソルバ: kissat 4.0.4 official linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）。

## 進捗

- IN FLIGHT claim + scripts push（本コミット）。
- 対照 343,134 bit-exact 再現・CNF 66件生成済み。
- 帯掃引（batch-1: 17直接+2lexH・batch-2: krow 10件・batch-3: {0}k5p 18件・
  batch-4: {1}k5p 18件）→ 生ログは batch ごとに push。

## スコープ

有限機械検証（K0810 census・class-split 符号化・k×minpos 分解の正しさ
（K0816/K0818 で小盤 ground-truth 検証済み）・kissat 4.0.4 まで）。
全 deciding CNF が UNSAT なら 5×36 の行欠損極大不存在は class-split 系として
確定し、witness-free 幅集合（class-split 系）は {19,...,36}・
鋭い形 M_{5,7} = 19 または ≥38。上界 158（K0332 代入）は不変。
m ≥ 37 の持続性は open（band-closure レーンが掃引中）。
