---
id: K0289
title: 10×10では同じ二点間距離でも二石局面の勝敗が異なる
kind: proposition
status: computed
topics:
- first-moves
- geometry
aliases:
- H6
relations: []
artifacts:
- path: research/hypotheses.md
  role: source
  note: H6の原仮説と当時未実施だった検証計画
  commit: 9a574ca80380e35ef46fbbc99324218a38c7551e
evidence: research/exploration/fact_10x10_r_pairs_sigma_d.jsonで{90,61}=LOSS、{73,66}=WIN。id=y*10+xなので両方とも平方距離10。
---

# 10×10では同じ二点間距離でも二石局面の勝敗が異なる

H6「二石の勝敗は二点間距離だけでは決まらない」は、既存の8石LOSS根 R={90,61,2,73,69,66,13,91} 内の二石分類だけで決着する。

点IDは `id=y*10+x`。したがって

- `{90,61}`: (0,9) と (1,6) で平方距離 1²+3²=10、結果は **LOSS**
- `{73,66}`: (3,7) と (6,6) で平方距離 3²+1²=10、結果は **WIN**

である。同じ平方距離10にWINとLOSSが共存するため、10×10の二石局面の勝敗は距離だけの関数ではない。

旧H6メモは異なる距離の例しか挙げておらず未確定としていたが、後続の `research/exploration/fact_10x10_r_pairs_sigma_d.json` に上の二局面の確定ラベルが保存されていた。全120個の二石D4軌道を分類する必要はなく、この存在命題にはこの一組の反例対で十分である。
