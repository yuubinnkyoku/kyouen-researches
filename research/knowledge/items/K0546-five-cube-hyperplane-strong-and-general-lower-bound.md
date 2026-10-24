---
id: K0546
title: 五次元二値立方体の6点共超平面禁止版の強解決と全次元の構成下界
kind: proposition
status: proved
topics: [variants, geometry, grundy, first-moves, maximum-safe, maximal-safe, statistics]
aliases: []
relations:
- type: depends_on
  target: K0544
  note: 五石極大のアフィン階数条件との照合
artifacts:
- path: research/experiments/coplanar-5cube-q6-20261024/proof.md
  role: proof
  note: 任意次元の構成下界と五次元盤の完全列挙の正当化
- path: research/experiments/coplanar-5cube-q6-20261024/solve.cpp
  role: verifier
  note: 5×5整数Bareiss行列式と増分安全集合列挙およびGrundy再帰
- path: research/experiments/coplanar-5cube-q6-20261024/independent.cpp
  role: verifier
  note: 素数1009上の6×6増補行列階数と全組合せ直接列挙
- path: research/experiments/coplanar-5cube-q6-20261024/results.md
  role: data
  note: 両独立検証器で一致した安全局面・極大配置・Grundy分布
scope: 五次元二値超立方体の6点共超平面禁止版の全安全局面と任意d≥2のd+1点共超平面禁止版の構成下界
evidence: 任意次元の明示的安全配置の全称証明と五次元の全1108073安全局面の二方式完全列挙
solution:
  board: 2×2×2×2×2・6点共超平面禁止
  level: strong
  outcome: first-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy, safe-layers]
  coverage: 全1108073安全局面・通常版とmisère版・全32初手
  conditions: 五次元二値立方体の6点が一つのアフィン超平面に入ると禁止、退化含む
  verification: [mathematical-proof, exhaustive-enumeration, independent-enumeration]
  certificate: 全906192個の6点組と全8石候補を二方式で完全検査
  independent_check: 5×5整数Bareiss行列式と6×6増補行列mod1009、増分列挙と直接組合せ列挙で一致
  note: K=7、s=5。通常先手必勝・全32初手勝ち、misère後手必勝。全局面で0↔1交換則成立
---

# 五次元二値立方体の強解決と任意次元の下界

5次元32頂点盤で、6点が同一アフィン超平面に入ること（退化を含む）を禁止する。

**有限完全列挙による確定値**：

- 禁止6点組350000、全安全局面1108073。
- 最大安全石数 $K=7$、最小極大石数 $s=5$。
- 極大配置は5石22240、6石46080、7石309056。
- 空盤の通常Grundy値 $g(\varnothing)=1$、misère補助値 $h(\varnothing)=0$。
- 全32初手後は $(g,h)=(0,1)$。通常版では全初手勝ち、misère版では全初手負け。
- 全安全局面で通常・misère値の0↔1交換則が成立する。通常Grundy値は0、1、2だけで、2は五石局面107040個に限る。

**別途全称証明**：任意の $d\ge2$ で、$d+1$ 点共超平面禁止版の二値超立方体には $d+2$ 石の安全配置

$$
\{0,e_1,\ldots,e_d,\mathbf{1}\}
$$

が存在する。したがって最大安全石数 $K_d\ge d+2$。五次元ではこれが最適である。一方、六〜十次元ではK0552が $d+3$ 石の明示配置を与えるため、この下界は鋭くない。十一次元以上で同じ改善が続くかは未解決。

[証明と検証範囲](../../experiments/coplanar-5cube-q6-20261024/proof.md)、[整数検証器](../../experiments/coplanar-5cube-q6-20261024/solve.cpp)、[独立検証器](../../experiments/coplanar-5cube-q6-20261024/independent.cpp)、[結果表](../../experiments/coplanar-5cube-q6-20261024/results.md)。無界次元のGrundy値や勝敗は主張しない。
