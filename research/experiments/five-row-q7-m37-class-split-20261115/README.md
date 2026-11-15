# five-row-q7-m37-class-split-20261115

IN FLIGHT (claim) — 高速レーン・単一連続実行。5×37 q=7 の行欠損極大不存在を
class-split SAT（kissat 4.0.4・19行鏡映正準欠損クラス完全分解）で交叉確認として確定する。
**m=37 は band-closure レーン（five-row-q7-band-closure-35-157-20261115・IN FLIGHT）の
def-mode UNSAT で決着済み**のため、本レーンは同 README の並走協調ノートに従い
**独立符号化での交叉確認**として実施する（m=35〔K0849〕・m=36〔K0850〕に続き
3幅目の二重決着を目指す）。

## 計画

- 65 deciding CNF: 17直接クラス + {0},{1} krow k=0..4（10件）+
  {0},{1} k=5 × minpos=0..18（38件・19点×2クラス）。minpos の健全上限は
  floor((37−1)/2) = **18 に増加**（columns 0..36 で min(x_min, 36−x_max) ≤ 18）。
  lex=H 交差確認 {0,1}/{2} + 陽性対照 5×18 {0}。CNF 総数 68（対照込み）。
- スクリプト: sat.js/sat2.js/sat3.js は K0836..K0850 レーンと byte-identical
  （blob sha 6c3262d6 / edfae1d2 / 6dfa7db3）。mkcnf.sh/qrun.sh は m=36→m=37
  移植・旧識別子の残留なし（grep 検証済み）。対照 CNF c5x18q7_0.cnf は
  md5 同一再生成（0bb6187d36e537a170e4fb451359bb94・再生成済み照合）。
- deciding 見込み **~4.7M conflicts**（deciding 合計系列 m23→m36:
  20,916,467 → … → 5,423,024 → 5,011,486 の外挿・局所的非漸減は毎幅
  出るので近似扱い）。deciding 65例 + lex 2例 + 対照1例 = records 68件。
- 完了すれば (5,7) witness-free 幅集合（class-split 系）は **{19,...,37}**・
  集合形式 M∈{19,…,37} または ≥38・**鋭い形 M=19 または ≥39**
  （K0821 監査規約・M=38 は検証済み witness-free 幅 37 の witness を
  要求するため不可）。上界 158（K0332 代入）は不変。
- **band-closure レーンの残る前線 m=38, 39, 50..157 には本レーンは着手しない**
  （同レーンの領域）。
- ソルバ: kissat 4.0.4 official linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）。

## スコープ

有限機械検証（K0810 census・class-split 符号化・k×minpos 分解の正しさ
（K0816/K0818 で小盤 ground-truth 検証済み）・kissat 4.0.4 まで）。
m ≥ 38 の持続性は open（band-closure レーンが掃引中）。
