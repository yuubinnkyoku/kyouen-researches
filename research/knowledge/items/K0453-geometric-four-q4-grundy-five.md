---
id: K0453
title: 整数6×6内の11点と4共円禁則でGrundy値5が実現し、点数・包含正方形が最小
kind: proposition
status: needs-review
topics:
- geometry
- grundy
- residual-games
- variants
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 整数行列式による共円・共線四点禁則
- type: depends_on
  target: K0002
  note: mexによるGrundy値と通常プレイ
artifacts:
- path: research/experiments/geometric-four-q4-grundy-five-20261018/proof.md
  role: proof
  note: 具体証人、量化範囲、有限型分類と5×5完全列挙の証明
- path: research/experiments/geometric-four-q4-grundy-five-20261018/verify_geometry.py
  role: verifier
  note: 円係数と共線判定、mex、5×5の独立枝刈り列挙
- path: research/experiments/geometric-four-q4-grundy-five-20261018/verify_independent.cpp
  role: verifier
  note: 行列式と密配列mex、5×5の全4457400組の枝刈りなし検証
- path: research/experiments/geometric-four-q4-grundy-five-20261018/verify_abstract.py
  role: verifier
  note: 4禁則4079所属型の完全列挙と11点未満の排除
- path: research/experiments/fastlane-four-edge-geometry-20261019/README.md
  role: proof
  note: 11点の明示的整数座標、4本の円方程式、有限完全列挙の説明
- path: research/experiments/fastlane-four-edge-geometry-20261019/verify.py
  role: verifier
  note: 全330組の整数行列式と全2048集合のmex検査
- path: research/experiments/fastlane-four-edge-geometry-20261019/independent.cpp
  role: verifier
  note: 独立の直線・円生成と全局面mex検査
- path: research/experiments/fastlane-four-edge-geometry-20261019/output.json
  role: data
  note: 4禁止組、1635安全局面、Grundy値分布と全初手
scope: 任意有限整数点集合の4点共円・共線禁止通常ゲーム。禁止四点組が高々4個でg(empty)=5なら点数11以上。11点かつ禁則4個以下なら包含軸平行整数正方形の一辺は6以上。標準6×6全点盤は対象外。
evidence: 2026-10-20添付統合。元資料では proved または computed と報告（個別の元statusは保存ZIPを参照）。本項目の全量化範囲に対する証明・計算の再監査は未完了。有限検証の実行範囲は統合実験のVALIDATION.mdを参照。
---


> 統合監査: 以下は取込元の主張・報告。全称証明・完全列挙の監査が未完了のため、現在の採用状態は needs-review。本文中の「証明」「一致」は元資料での報告を表す。


# 6×6内の11点・4禁則で空盤Grundy値5

盤点集合を

```
(0,0),(0,4),(1,1),(1,3),(3,1),(3,2),
(3,4),(4,1),(4,5),(5,0),(5,2)
```

とすると、共円・共線禁止四点組は4個だけで、全安全局面は1635個、空盤Grundy値は5。

抽象的な禁止4点集合が4個以下の有限ゲームでg(empty)=5を実現する最小点数は11。これは禁則所属型4079種の全称有限帰着と完全列挙による。

さらに5×5の全4457400通りの11点部分集合では禁止四点組が必ず5個以上あり、最小5を達成する集合は8個。よって11点かつ4禁則以下という条件での最小包含正方形は6×6。

**限定**：標準6×6盤の空盤Grundy値や、標準盤の合法残余局面での実現は主張しない。

追加の同一命題資料: `K0456-four-edge-integer-lattice-grundy-five.md`。詳細と独立証人・検算範囲は追加artifactを参照。原文は取込元ZIPに保存。
