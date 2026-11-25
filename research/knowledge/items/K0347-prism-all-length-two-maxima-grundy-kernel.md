---
id: K0347
title: 奇数列の平行列版は全長・全局面のGrundyを二最大占有数の表と偶奇へ縮約できる
kind: proposition
status: proved
topics: [variants, grundy, residual-games, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0340
  note: 三次元格子から全ペア容量ゲームへの正確な縮約
- type: generalizes
  target: K0341
  note: 長盤条件を外した有限長全局面の評価方法。長盤閉公式も再現する
- type: depends_on
  target: K0345
  note: 偶数rの空盤閉式と空盤安定化長の系
artifacts:
- path: research/experiments/prism-two-maxima-20261005/proof.md
  role: proof
  note: 全称mex帰納、二変数表、有限一括手budgetのgap閉公式
- path: research/experiments/prism-two-maxima-20261005/audit.md
  role: proof
  note: 別担当による全称証明の独立監査
- path: research/experiments/prism-two-maxima-20261005/kernel.py
  role: solver
  note: 最大・第二最大と残り偶奇によるO(min(m,r)²)初期表
- path: research/experiments/prism-two-maxima-20261005/verify.py
  role: verifier
  note: 別ラベル付き全座標mexと有限budget gap DP
- path: research/experiments/prism-two-maxima-20261005/verified.json
  role: data
  note: 各パラメータで全安全状態の値・閉式の完了数を照合
scope: 奇数w≥3、0≤x_i≤m、全ペアx_i+x_j≤rの一点増加通常ゲーム、m,r非負整数。三次元格子ではK0340の底面条件とq=r+1>2wを仮定する。
evidence: 最大・第二最大・それ未満の三種の手と、偶数個の残り列から導く全称mex帰納。有限検算は実装監査。
---

# 全長の二最大値Grundy縮約

a,bを占有数xの最大・第二最大（重複を含む）、e=(Σx−a) mod2とする。
`0≤b≤a≤m,a+b≤r` の二変数表を

```
F(a,b)=mex({F(a+1,b):a<m,a+b+1≤r}
          ∪{F(a,b+1) xor1:b<a,a+b+1≤r})
```

と定めると、任意有限長・任意の奇数列数w≥3で `g(x)=F(a,b) xor e`。
Fは常に0,1,2なので全Grundyは0..3。初期表はO(min(m,r)²)であり、
列数に依存する全占有数ベクトルを列挙する必要がない。

全手は最大列追加・第二最大列追加・第二最大未満の追加に尽くされる。
最後の型はe=1なら必ず存在し、e=0では有無にかかわらずmexが変わらない。
二選択肢のmex補題と帰納で全称証明する。

支配列a>r/2では、他列gap y_i=r−a−x_iと残り列端budget z=m−aを用い、
t=min y,E=Σy mod2として `g=(E+z) mod2`（z<t）、
`g=2(t mod2)+E`（z≥t）の有限budget閉公式も得る。
長盤用の式を短盤へそのまま流用できない。

空盤はr奇数で `g(0)=min(m,(r+1)/2) mod2`、
r偶数でm<rならm mod2、m≥rなら0。
前者は二変数再帰の対角・隣接対角の下降帰納、後者はK0345で証明する。
r≥1の真の空盤勝敗安定化長は、それぞれ(r+1)/2、rである。
これは全安全配置の満容量安定化とは別の明示的な定義である。

ラベル付き全座標mexと独立gap DPで保存した有限範囲を全検査した。
無界な全w,m,rへの根拠は証明であり、この表の外挿ではない。
偶数列はK0340の0/1公式を使う。標準二次元盤のGrundy無界性と11×11の
勝敗は本定理の対象外で、11×11は引き続きUNKNOWN。
