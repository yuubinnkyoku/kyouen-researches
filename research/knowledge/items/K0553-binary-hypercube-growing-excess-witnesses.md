---
id: K0553
title: 共超平面禁止二値立方体の安全石数下界の超過分は次元とともにd+3からd+7へ増える
kind: proposition
status: proved
topics: [variants, geometry, maximum-safe, statistics]
aliases: []
relations:
- type: generalizes
  target: K0552
  note: d=6..10のd+3下界をd=6..24に拡大し9次元以上で強める
- type: verifies
  target: K0552
  note: 既知のd=6..10証人を二方式で独立再検証し統計も一致
artifacts:
- path: research/experiments/binary-cube-hyperplane-large-d-20261025/README.md
  role: log
  note: 手法・制御・小素数の教訓・再現手順
- path: research/experiments/binary-cube-hyperplane-large-d-20261025/search.cpp
  role: solver
  note: 無作為順貪欲探索器。mod 2^61-1の超平面法線と厳密同値性
- path: research/experiments/binary-cube-hyperplane-large-d-20261025/verify_exact.py
  role: verifier
  note: 全小行列式の整数Bareiss検査と双対零空間小行列式検査
- path: research/experiments/binary-cube-hyperplane-large-d-20261025/verify_mod.cpp
  role: verifier
  note: 全部分集合のmod 2^61-1掃き出し。Hadamard限界により整数非特異と同値
- path: research/experiments/binary-cube-hyperplane-large-d-20261025/witnesses.txt
  role: data
  note: 全成功記録。mod検証器が全記録を検査
- path: research/experiments/binary-cube-hyperplane-large-d-20261025/frontier.txt
  role: data
  note: 各次元の最大m証人。二検証器が完全検査
- path: research/experiments/binary-cube-hyperplane-large-d-20261025/results.md
  role: data
  note: 最前線表・一様下界・大予算失敗の一覧・計算量の壁
- path: research/experiments/binary-cube-hyperplane-large-d-20261025/results.json
  role: data
  note: 機械可読な最前線と検証状況
- path: research/experiments/binary-cube-hyperplane-d25-d30-20261025/proof.md
  role: proof
  note: d=25..30のd+7石証人と有限体Gale双対判定の数学的証明
- path: research/experiments/binary-cube-hyperplane-d25-d30-20261025/witnesses.txt
  role: data
  note: 25〜30次元の全明示頂点一覧
- path: research/experiments/binary-cube-hyperplane-d25-d30-20261025/verify_gale_mod.cpp
  role: verifier
  note: 二素数それぞれで全Gale6行小行列式を完全検査
- path: research/experiments/binary-cube-hyperplane-d25-d30-20261025/verify_direct_spot.py
  role: verifier
  note: 600件の元の整数行列式の独立抜取照合
- path: research/experiments/binary-cube-hyperplane-d25-d30-20261025/results.md
  role: data
  note: 全件検査の件数と証拠の境界
scope: d=6..30の二値超立方体におけるd+1点共超平面禁止ゲームの最大安全石数の下界。上界・Grundy値・d>=31は対象外。
evidence: 各次元の明示証人について、全C(m,d+1)個のd+1点部分集合の増広行列式が、独立な二算法（整数Bareiss＋双対零空間、mod 2^61-1掃き出しとHadamard限界による同値性）で非零であることを完全検査。d=25..30の追加証人は二素数上のGale双対小行列式全件検査と独立な整数Bareiss抜取検査で照合。
---

# 安全石数下界の超過分は次元とともに増える

二値超立方体 $V_d=\{0,1\}^d$ で相異なる $d+1$ 点の実アフィン共超平面
（退化を含む）を禁止するゲームの最大安全石数を $K_d$ とすると、
次の明示証人が完全検証済みである。

- $K_d\ge d+3$：全 $d\in\{6,\dots,24\}$
- $K_d\ge d+4$：全 $d\in\{9,\dots,24\}$
- $K_d\ge d+5$：全 $d\in\{13,\dots,24\}$
- $K_d\ge d+6$：全 $d\in\{18,\dots,24\}$
- $K_d\ge d+7$：全 $d\in\{24,\dots,30\}$

一般位置は下方遺伝するため、各次元の最大証人（6→9, 7→10, 8→11,
9→13, 10→14, 11→15, 12→16, 13→18, 14→19, 15→20, 16→21, 17→22,
18→24, 19→25, 20→26, 21→27, 22→28, 23→29, 24→31）から
上記の一様主張が直ちに従う。d=6..10のd+3はK0552と一致する。

**観測**：無作為順貪欲で到達できる超過 $m-d$ の最少値は
d=9, 13, 18, 24で4, 5, 6, 7に上がる。この4〜6次元ごとの上昇は
$d/\ln d$ 型の成長と整合する。ただし予算を増やせば最前線はさらに伸びる
（d=9のd+4は1492再試行、d=20のd+6は追加予算で発見）ため、
貪欲の失敗は上界ではなく、上記の下界だけが証明済みである。
$d\ge31$ への外挿も主張しない。

**計算量の壁**：最終段の超平面数は $\binom{m-1}{d}$ に達するため、
(23,30) と (24,32) は1貪欲パスが時間単位になり本実験では未試行である。

K0546の全次元構成下界 $d+2$ はこれら全次数元で鋭くなく、
K0552の「十一次元以上で同じ改善が続くか」という問いには
「続く」以上の答えになる：改善量そのものが次元とともに増える。


## 25〜30次元でd+7石下界を拡張（2026-10-25）

新たに各d=25,26,27,28,29,30で**d+7個の二値頂点**を明示し、全てのd+1点部分集合が実アフィン独立であることを厳密に確認した。従って

$$\boxed{K_d\ge d+7\qquad(25\le d\le30)}$$

となり、既存のd=24の31石証人と合わせてd=24..30の一様下界を得る。元の増補座標行列は(d+7)行(d+1)列なので、左零空間の次元は6。**全6行Gale小行列式が非零であること**と、元の全(d+1)行小行列式が非零であることは同値。二つの大素数1000000007、1000000009のそれぞれで、全9,254,400件のGale小行列式を完全検査し零は0件だった。有限体で非零なら整数でも非零であるため、これは固定した6次元分の**厳密な下界証明**となる。

別実装で、各次元100個、合計600個の元の(d+1)次整数行列式をBareiss消去で独立照合した。こちらは**抜取照合**であり全件検証ではない。証人、数学的補題、全件検証器と結果表は[追加実験](../../experiments/binary-cube-hyperplane-d25-d30-20261025/proof.md)に保存した。**d>=31への一般化、上界、空盤勝敗は未解決**。
