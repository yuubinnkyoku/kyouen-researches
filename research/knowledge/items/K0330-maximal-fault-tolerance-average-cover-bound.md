---
id: K0330
title: 極大配置の故障耐性は三石被覆の平均多重度で上から抑えられる
kind: proposition
status: proved
topics: [maximal-safe, geometry]
aliases: []
relations:
- type: depends_on
  target: K0026
  note: 安全極大配置と空点を対象にする
- type: depends_on
  target: K0328
  note: K0328の故障耐性ρの定義を用いる
artifacts: []
---

# 極大配置の故障耐性は三石被覆の平均多重度で上から抑えられる

標準 (n\times n) 盤（(n\ge2)）の安全極大配置 (S) を (|S|=k) とする。空点 (p\notin S) に対し、(S) の三石組 (T\in\binom S3) で (T\cup\{p\}) が禁止四点組となるものの個数を (b_S(p)) と書く。このとき

[
\rho(S)
\le \min_{p\notin S} b_S(p)
\le
\left\lfloor
\frac{\binom{k}{3}(2n-3)}{n^2-k}
\right\rfloor .
]

したがって特に (ho(S)\ge r) なら

[
r(n^2-k)\le \binom{k}{3}(2n-3)
]

が必要である。

## 証明

空点 (p) を固定し、(p) を禁止する三石組全体を超グラフ (\mathcal F_p) とみなす。(p) を合法に戻すには (\mathcal F_p) の全辺を少なくとも一石ずつ壊せばよい。各辺から一頂点ずつ選べば横断集合が得られるので、その最小横断数は

[
\tau(\mathcal F_p)\le |\mathcal F_p|=b_S(p).
]

(ho(S)) は空点を一つでも合法に戻す最小除去数だから、全空点について最小を取って

[
\rho(S)\le\min_{p\notin S}b_S(p)
]

を得る。

次に二重計数する。固定三石組 (T) が禁止できる盤内点を数える。

- (T) が非共線なら三点を通る円は一意である。この円は各縦列と高々2点で交わるので盤内格子点は高々 (2n) 個。既に (T) の3点を含むため、追加で禁止できる空点は高々 (2n-3) 個。
- (T) が共線なら第四点も同一直線上でなければ行列式は0にならない。盤内の一直線上の格子点数は高々 (n) なので、追加点は高々 (n-3\le2n-3) 個。

従って禁止関係 ((T,p)) の総数は

[
\sum_{p\notin S}b_S(p)
\le \binom{k}{3}(2n-3).
]

空点は (n^2-k) 個なので平均値以下の空点が少なくとも一つあり、

[
\min_{p\notin S}b_S(p)
\le
\left\lfloor
\frac{\binom{k}{3}(2n-3)}{n^2-k}
\right\rfloor .
]

以上で示された。

## 意味と限界

K0328の一様定数上界そのものはまだ従わない。右辺は (k) と (n) に依存する。ただし高い故障耐性を持つ反例候補には石数・三石被覆密度の必要条件を課すので、探索時の事前排除に使える。

また最初の不等式 (ho(S)\le\min b_S(p)) は平均評価とは独立で、最小極大配置の一重被覆点問題K0297が成立すればK0298の (ho=1) が直ちに従うことも同じ横断集合の見方で説明できる。


## 局所点対計数による追加上界

さらに各空点 \(p\) ごとに

\[
\boxed{b_S(p)\le\left\lfloor\frac{k(k-1)}6\right\rfloor}
\]

が成り立つ。従って主結果は

\[
\boxed{
\rho(S)\le \min_{p\notin S}b_S(p)
\le
\min\left\{
\left\lfloor\frac{k(k-1)}6\right\rfloor,\,
\left\lfloor\frac{\binom{k}{3}(2n-3)}{n^2-k}\right\rfloor
\right\}.
}
\]

実際、固定した空点 \(p\) を禁止する異なる二つの三石組は、\(S\) の二石を共有できない。二石 \(a,b\) と \(p\) が非共線なら三点を通る円は一意であり、安全性からその円上には \(a,b\) 以外の \(S\) の石を高々一つしか置けない。三点が共線なら同一直線上について同じことが言える。したがって blocker 三石組全体は線形3一様超グラフで、各辺が使う3個の石対は互いに異なる。ゆえに

\[
3b_S(p)\le\binom{k}{2}.
\]

この評価は盤の大きさ \(n\) を使わない。特に \(\rho(S)\ge r\) の反例候補には \(k(k-1)\ge6r\) も必要となる。
