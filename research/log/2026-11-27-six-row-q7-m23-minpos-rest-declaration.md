# (6,7) 6x23 class {2} krow=2:5 minpos 残り全値: 単一オーナー宣言 (2026-11-27 fast lane)

## 宣言内容

- 対象: (6,7) の未解決 frontier 幅 **6x23**。class {2} krow=2:5 の minpos (first deficient row の最左石) 分解のうち、出版済みの P=6/7/8 (INDET 4,968,075 / 5,055,896 / 4,935,522 @262s caps, six-row-q7-m22-class-split-20261127) を除く **P=0..5, 9..18 の計16 probe** を 262s cap で実行する。
- 機材: kit byte-clone scripts (sat.js fcc0cfd8 / sat2.js 14ceb854 / sat3.js e04581eb / verify_frac.py 837fe24b) + kissat 4.0.4 official linux-amd64 (zip sha 63282e51, binary sha 21da5d98)。
- 正制御 (宣言前に実施・開示): 6x22 q=7 class {2} krow=2:5 minpos=7 SAT **2,050,424 conflicts bit-exact** (出版値と完全一致)。encoder meta: 6x23 p6 vars 12556 / clauses 44937 出版 meta と一致、6x22 p7 vars 11682 / clauses 41800。
- 判定規約: **SAT => 35石欠損極大witness が 6x23 に実在 => M_{6,7} >= 24 (frontier 更新)**。全 INDET => honest negative (不在主張ではない)。UNSAT は class {2} krow=2:5 minpos 分解のその値の不在のみ (他 class/krow 未掃引)。
- 検証: SAT の場合は sat.js verifyConfig + verify_frac.py (fresh Fraction) の二系統 + 負制御 (remove->not maximal / add->reject) + 決定CNFの cold pair。
- 重複回避: six-row-q7-m22-class-split-20261127 の拡張 probe 群と disjoint (P=6/7/8 のみ既刊)。6x26 (6,6) four-lane (a9dde1d3/f9a982d2/e61acf82/9e703319b) とは無関係。並走 lane はこの P 値に着手しないこと。
- publish-then-execute。verdict 不消費。標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN。conflicts は bookkeeping。

- 宣言時 HEAD: 4aec0c19 (n11 eleventh-cost batch stage-1 completion log)。
