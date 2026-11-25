---
id: K0662
title: サイクル型グラフ星共円ゲームの中心付き終局長多項式は全根が負の実数
kind: proposition
status: proved
topics: [geometry, maximal-safe, statistics, strategy-length, variants]
aliases: []
relations:
- type: depends_on
  target: K0602
  note: グラフ星型共円構成と許容削除集合の極大配置重みを使用
- type: depends_on
  target: K0656
  note: サイクルの削除区間分類と係数の全範囲正性を使用
artifacts:
- path: research/experiments/cycle-terminal-real-roots-20261103/proof.md
  role: proof
  note: 長さ2・3の巡回区間の競合グラフをclaw-freeと証明し、真の双子置換とChudnovsky–Seymour定理で実根性を示す
- path: research/experiments/cycle-terminal-real-roots-20261103/verify.py
  role: verifier
  note: 38競合グラフ・28全単射と係数比較・444強対数凹性検査
scope: K0602の整数平面グラフ星型構成でG=C_n（n>=3）、整数q>=4、中心点を含む極大配置の最短石数からの差の係数多項式。中心なしの極大配置および標準全格子盤は対象外。
evidence: 巡回区間の競合グラフがclaw-freeである全称証明、整数の真の双子置換、およびChudnovsky–Seymour (2007) の実根定理。有限監査は独立検証。
---

# サイクル型の中心付き終局長分布は独立Bernoulli和になる

K0602の整数点構成で G=C_n、n>=3、r=q-3>=1 とする。最短石数 s=1+rn からの差を記録する**中心点を含む**極大配置の多項式を

\[
F_{n,r}(u)=\sum_{k=0}^{h}a_{n,k}(r)u^k,\quad h=\lfloor n/2\rfloor
\]

とすると、**全ての根は負の実数**である。したがって

\[
\boxed{a_{n,k}^2\ge\frac{(k+1)(h-k+1)}{k(h-k)}a_{n,k-1}a_{n,k+1}}\quad(1\le k<h)
\]

という強い対数凹性と単峰性が成立する。中心付き極大配置を一様に選ぶと、その終局長差は h 個の独立Bernoulli変数の和と**分布が厳密に一致**する。

**証明の要点：** 長さ2または3の巡回区間を頂点とし、重なる区間を隣接させた競合グラフ H_n は誘導爪 K_{1,3} を持たない。長さ2区間を r 個の真の双子へ置換した H_{n,r} も同様であり、

\[
\boxed{F_{n,r}(u)=r^n I(H_{n,r},u/r^3)}
\]

が成立する。Chudnovsky–Seymour (2007) の claw-free グラフ独立集合多項式の実根定理から結論が出る。詳細は[全称証明](../../experiments/cycle-terminal-real-roots-20261103/proof.md)、[独立検証器](../../experiments/cycle-terminal-real-roots-20261103/verify.py)。38競合グラフの誘導爪検査、28条件の全単射・三方式係数照合、444条件のNewton不等式照合で不一致0。

**適用範囲に注意：** 中心なしの一通りを加えた全終局多項式は一般には実根でない。n=4,q=4 で P(u)/u^s=1+8u+2u^2+u^3 の判別式は -1563 であり非実根を持つ。標準全格子盤の最短極大配置数や11×11の勝敗には直接適用しない。
