# 2026-11-28 five-row q5 5x28 class {0} krow=0:3 minpos sweep — declaration (single-owner, publish-then-execute)

- 前回レーン (宣言 `24736c72`・完了 log `61c7e431`) で **(5,5) 5×27 c0k3p9 SAT** (1,556,533
  conflicts・witness 19石 rows [3,4,4,4,4]) により **M_{5,5} ∈ [28, 336]**・前線は 5×28 に前進。
  本宣言はその直接継続として **(5,5) 前線 5×28 class {0} krow=0:3 minpos p=0..13 掃引**を着手する
  (sound H-split bound: min(x1, 27−x3) ≤ ⌊(m−1)/2⌋ = 13)。
- 実行時 HEAD: 61c7e431d5523b9948d779c18c7fb2eae1af6351。
- probe 順序 (WIN-stop 効率・5×27 の SAT が p=9 だった観察から中心から外へ):
  **9, 10, 8, 11, 7, 12, 6, 13, 5, 0, 4, 1, 3, 2** (各 cap 285s・kissat 4.0.4)。
  SAT 検出で WIN-stop (残り probe は未掃引として記録)。
- 目標: SAT ⟹ 5×28 witness で witness 帯 m=5..28 延伸・**M_{5,5} ∈ [29, 336]**
  (CSV/K0833 更新・witness は decode + verifyConfig + verify_frac.py の複数系統検証・
  cold pair bit-exact 確認)。UNSAT は当該サブインスタンスの決定的除外。
  INDET は honest negative であり**不在主張ではない** (k=0..2・他クラス・p10..p13 相当の
  残り minpos が残る)。全 14 probe 走査後の戦略 (k=0..2・他クラス・rowY 分解) は別宣言。
- 手法・較正: 生成器 sat3.js md5 d03f908ea99ba819caee2a6fbb471c1b・kissat 4.0.4
  md5 3a5eba830aa6008a604fcc9bbe99a325 (前レーンと同一 toolchain・較正は直前 Part で
  5×25 SAT 35,972・5×26 SAT 1,631,556 conflicts 出版値 bit-exact 検証済み・
  5×27 c0k3p0/p1/p2 CNF md5 bit-exact)。
- cap 285s (実行環境の呼び出し上限 300s 内・前レーンと同一)。
- 標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・
  全 closure class は全時点 UNKNOWN・verdict 不消費・conflicts は bookkeeping。
