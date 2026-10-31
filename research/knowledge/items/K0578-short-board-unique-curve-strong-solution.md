---
id: K0578
title: 平面q点禁止ゲームはN≤2q−3で禁止曲線が一意となり全安全局面を偶奇で強解決できる
kind: proposition
status: proved
topics: [geometry, variants, grundy, first-moves, maximal-safe, strategy-length]
aliases: []
relations:
- type: generalizes
  target: K0577
  note: N=q+1の三分律を全q≤N≤2q−3へ拡張し、上界の鋭さも証明
- type: depends_on
  target: K0002
  note: 通常・misère補助mex値の定義
artifacts:
- path: research/experiments/short-board-unique-carrier-20261031/proof.md
  role: proof
  note: 一曲線剛性、整数格子での全候補実現、終局長・全履歴・Grundyの閉公式、境界の整数反例
- path: research/experiments/short-board-unique-carrier-20261031/verify.py
  role: verifier
  note: 4×4格子31616盤の禁止辺全列挙、160盤の全安全局面再帰、q=4とq=5の鋭い境界反例
scope: q≥4、q≤N≤2q−3の相異なる実平面点、共線・共円q点組禁止の未着手盤、通常版とmisère版の全安全局面
evidence: 二つの禁止q点組の交わりが3点以上という幾何学的全称証明。境界N=2q−2では任意qの整数格子反例を構成。4×4格子の31616盤と160盤の全安全局面を整数演算で独立検査。
---

# 少数点盤の一曲線剛性・全局面偶奇則

相異なる実平面点の総数が $q\le N\le2q-3$（$q\ge4$）なら、共線または共円の禁止$q$点組は存在しないか、**ただ一つの直線・円 $C$ 上の $m\ge q$ 点から選ぶすべての$q$点組**に限られる。禁止辺数は $0$ または $\binom mq$（$q\le m\le N$）であり、すべての候補値を整数格子で実現できる。

禁止辺がない場合 $L=N$、ある場合 $L=N-m+q-1$ と置く。任意の安全局面 $S$ で終局までの手数は必ず $L-|S|$ となり、通常Grundy値は $g(S)=(L-|S|)\bmod2$、misère補助値は $h(S)=1-g(S)$。非終局局面の全合法手の勝敗分類は同じで、通常版とmisère版では逆転する。

禁止辺があるとき、$a=|S\cap C|$ とすれば、$S$ を含む極大安全集合数は $\binom{m-a}{q-1-a}$、そこに至る順序付き着手履歴数は $\binom{m-a}{q-1-a}(L-|S|)!$。

上界 $N\le2q-3$ は**整数格子上で鋭い**。$N=2q-2$ では任意の$q\ge4$について異なる二つの円がそれぞれ禁止辺を作り、極大安全集合の石数が $N-1$ と $N-2$ に分かれる構成がある。

全称証明と具体的な整数反例は証明文書に記録した。4×4格子の31,616盤の禁止辺構造、160盤の全安全局面と履歴を検証器で独立検査した。これは実平面上の**未着手盤**の定理であり、大きな盤の途中局面で占有点が禁止組に含まれる場合の残余ゲームへ無条件に適用できない。
