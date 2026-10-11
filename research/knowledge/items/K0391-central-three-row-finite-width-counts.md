---
id: K0391
title: 3行盤の中央弦型2+1+1共円四点組の有限幅厳密計数
kind: proposition
status: proved
topics:
- geometry
- statistics
aliases: []
relations: []
artifacts:
- path: research/experiments/geometry/reports/central-211-finite-width-and-mod4-20261011.md
  role: proof
  note: 二平方和表現の最小包含幅・有限窓計数・4の合同式の全称証明
- path: research/experiments/geometry/scripts/audit_central_211_finite_width.py
  role: verifier
  note: 独立整数行列式による55条件の有限完全列挙と4800条件の表現監査
- path: research/experiments/geometry/output/central_211_finite_width_audit_20261011.json
  role: data
  note: 有限監査結果
---

# 等間隔三行の中央弦型共円四点組の有限幅厳密計数と4の合同式

## 命題・範囲

正整数 h,d に対して y=0 の二点 (0,0),(d,0) と y=±h の各一点でできる共円四点組を考える。整数表現 a²+b²=d²−4h² に対応する完成点は u=(d+a+b)/2, v=(d+a−b)/2 であり、最小包含横幅（最大x−最小x）は d+e、ただし e=max(0,(|a|+|b|−d)/2)。

幅mの整数窓に入る中央弦型2+1+1共円四点組の個数は

```
C_h(m)=Σ_{d=1}^{m−1} Σ_{a²+b²=d²−4h²} max(0,m−d−e).
```

さらに C_h(m)≡max(0,m−2h) (mod 4)。個々の完成点が弦の閉区間内にある必要十分条件は |ab|≤2h²、厳密な内側なら |ab|<2h²。

## 現在の根拠と限界

全称証明は上記 proof artifact に記載。独立4×4整数行列式による55条件の有限完全列挙と4,800条件の追加検査は証明の代用ではなく監査である。11×11で等間隔三行の中央弦型だけを合計した部分和は2,037個。非等間隔三行、外側行に二点ある型、2+2型などを含まない。既存の中央弦二平方和公式の有限窓への精密化である。
