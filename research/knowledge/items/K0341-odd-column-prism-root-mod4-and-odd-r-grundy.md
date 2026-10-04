---
id: K0341
title: 奇数列の三次元長盤はq≡2 mod4でだけ先手勝ち、奇数rの全Grundyは閉公式を持つ
kind: proposition
status: proved
topics: [variants, geometry, grundy]
aliases: []
relations:
- type: depends_on
  target: K0340
  note: 三次元平行列の安全性を全ペア容量へ縮約する
artifacts:
- path: research/experiments/prism-hyperplane-2026-10-05/odd-root-proof.md
  role: proof
  note: 偶数個のgapゲームのmex公式、奇数r全Grundy、偶数rの応答戦略
- path: research/experiments/prism-hyperplane-2026-10-05/odd_root_verify.py
  role: verifier
  note: 独立ラベル付き完全mexと共有占有数DP、gap補助ゲームの全検算
- path: research/experiments/prism-hyperplane-2026-10-05/odd-root-output.json
  role: data
  note: 全状態の有限検算。無界主張の根拠はproof artifact
scope: 三次元B×{0,...,m−1}、Bのどの三点も共線でない、奇数列数w≥3、超平面または超球面上のq点禁止、q>2w,r=q−1,m≥r、通常プレイ。
evidence: 占有数縮約後の全称mex帰納と、偶数rで同じ列をもう一度増やす後手応答戦略。
---

# 奇数列の長盤の空盤mod4則と奇数rの全Grundy公式

scopeの三次元変種では、空盤Grundy値は `q≡2 (mod4)` のとき1、その他は0。
したがって先手勝ちは正確にq≡2 mod4である。

r=2k+1が奇数の場合、全安全占有数xに対し、a=max xとして

```
a≤k:       g(x)=(k+1−Σx) mod2.
a≥k+1:     最大列aは一意。その他の列でy_i=r−a−x_iとすると
           g(x)=2(min y mod2)+(Σy mod2).
```

支配列領域は、偶数個のgapを「一つまたは全部、一つ減らす」ゲームへ
正確に縮約される。その全Grundy式を0..3の四場合のmex帰納で証明した。
低占有領域の各手と支配列へ出る各手を照合すると前半の公式が従う。
空盤は前半に入るので、r≡1 mod4の場合だけGrundy1となる。

q>2wの条件下では、r=2k+1の占有数
`(k+1,k−2,k−1,...,k−1)` がg=3を持つ。
全公式と合わせて、奇数rの全安全局面に現れる最大Grundy値は正確に3。

偶数rの空盤では、後手が先手の増やした列をもう一度増やし、全列数を
偶数に保つ応答が常に合法である。ペア和と列端の偶奇による全称証明でg=0。
偶数rの全局面閉公式、m<rの全勝敗、二次元標準盤の無界Grundy数、11×11の
勝敗は本項目の結論ではない。有限DP検算を全称証明と混同しない。
