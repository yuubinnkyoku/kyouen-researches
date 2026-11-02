---
id: K0650
title: 11×11中央49の46証人条件付き七石義務を三証人交換2回で2,154類から2,094類に削減
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0003
  note: 条件付き証明計画と勝敗の区別
- type: depends_on
  target: K0646
  note: 確定WIN6を除外した現行46証人・2,154七石類の出発点
- type: depends_on
  target: K0644
  note: 五つの終局戦略と八石親から導出したLOSS7の23類
- type: supersedes
  target: K0646
  note: 同じ94五石被覆を保ったまま追加で60七石類を削減した条件付き計画
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/conditional_s6_cover_46_post_seven_win6_2094_three_swaps.json
  role: certificate
  note: 三証人交換2回、正準七石義務数、終局証明再利用数
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_2094_three_swap_descent.py
  role: verifier
  note: 2,154類の独立監査と五終局証明の再生成、4×4整数幾何による交換再検証、3×3幾何との照合
- path: .github/workflows/n11-central49-2094-three-swap.yml
  role: source
  note: 改変負例6件を含む独立検証CI
- path: research/log/2026-11-03-n11-central49-2094-two-three-swaps.md
  role: log
  note: 交換経緯、検証境界、探索手順
scope: 標準11×11完全指摘・通常プレイ。中央49の優先四石からの94五石局面を46六石LOSS候補で被覆する条件付き計画。六石LOSS・二石root・空盤勝敗は対象外。
evidence: K0646の46証人から三証人交換を2回構成。最初は2,154→2,098、次は2,098→2,094正準七石類。独立4×4整数Bareissと3×3差分行列式で最終46証人・2,987合法辺・2,094正準類を照合。既知WIN6 145類とWIN7 23類に衝突せず、94/94五石被覆とK0644由来の終局証明済みLOSS7 6類を維持。新六石LOSSや二石rootの閉鎖はない。
---

# 中央49の条件付き七石義務を2,094類へ縮小

K0646の2,154類は、既知WIN6を含まない46六石証人による条件付き被覆だった。二証人以下の交換では改善不能だったが、**三証人交換2回で2,094類に縮小**した。追加削減は60類（約2.79%）、K0641の2,301類からは207類（約9.00%）。

| 段階 | 相異なる七石類 | 合法七石辺 | 終局証明済みLOSS7 |
| --- | ---: | ---: | ---: |
| K0646出発点 | 2,154 | 2,990 | 6 |
| 三証人交換1回目 | 2,098 | 2,991 | 6 |
| 三証人交換2回目 | **2,094** | **2,987** | **6** |

46六石証人、94/94五石被覆、既知WIN6 145類・WIN7 23類との非衝突を維持。既存の終局証明で確保できていない七石類は、この証明系列に限れば**2,088類**である。

探索側では94五石のうち92類が46証人に完全マッチングされる構造を利用し、三証人を除いた六端点の完全マッチング15通りから置換候補を生成した。候補は既知WIN6・WIN7との衝突を除外し、七石正準類の重複を計数した。局所探索で発見した二つの交換は、探索器とは別の4×4整数Bareissで再計算し、さらに3×3差分行列式の結果と一致した。再現用の固定交換と負例検査は添付の検証器にある。

**2,094類は大域的最小値ではない。** さらに三証人以上の交換で改善する可能性がある。また、確定WIN6の除外は候補をLOSSと証明するものではない。選択六石LOSSは未証明、二石局面 {49,60} は未閉鎖で、標準11×11空盤の勝敗は **UNKNOWN**。
