---
id: K0808
title: "6×m q=5/6/8 の欠損極大witness — M_{6,5}≥20・M_{6,6}≥16・M_{6,8}≥12（下界の初記録）"
kind: computation
status: computed
topics: [rectangles, maximal-safe, verification, stabilization-length]
aliases: []
scope: "6×m整数格子・q∈{5,6,8}。(6,5) m=8..19・(6,6) m=8..15・(6,8) m=9..11 の各mで石数<満容量の極大安全配置（欠損witness）の実在。いずれも貪欲探索+独立検証による実在証明であり、不在は主張しない"
evidence: "汎用(w,m,q)貪欲+shake探索機と、census不使用の独立検証（石ペア直線・石3点組外心の全列挙・厳密整数演算）で全witnessが safe+maximal PASS。制御4件（K0796・K0069・K0759・K0761 witness）全PASS"
relations:
- type: supports
  target: K0806
  note: K0806 が上界のみ記録した (6,5)/(6,6)/(6,8) に下界を与え、境界を [20,658]/[16,495]/[12,371] の両側にした
- type: depends_on
  target: K0318
  note: 上界は K0318 代入（U=658/495/371・K0024 の T 値に基づく）
- type: depends_on
  target: K0796
  note: 2×8 q=4 の5石witness再発見制御
- type: depends_on
  target: K0759
  note: 5×19 q=7 の全極大30石との一致制御
artifacts:
- path: research/experiments/six-row-deficient-witnesses-20261113/scripts/deficient_maximal_machine.ts
  role: source
  note: 汎用欠損極大探索機（3点外心完全census・ハイブリッド貪欲+shake・独立検証器内蔵）
- path: research/experiments/six-row-deficient-witnesses-20261113/output/scan_results.json
  role: data
  note: 全スキャン結果・witness座標・独立検証詳細・制御
- path: research/experiments/six-row-deficient-witnesses-20261113/report.md
  role: report
  note: 主結果表・バグ2件の教訓・レジューム
- path: research/log/2026-11-13-six-row-deficient-witnesses.md
  role: log
---

## 命題（計算された事実）

6×m 整数格子・q点共円共線禁止版において:

1. **(6,5)**: m=8..19 の各 m で石数 < 24（満容量）の極大安全配置が存在する。
   最小石数は 15（m=8）から 23（m=19）まで単調とは限らず推移。
   よって真の安定化長 **M_{6,5} ≥ 20**。6×19 witness（23石・独立検証 safe+maximal・
   worstLine=worstCirc=4・unblocked=0）の座標は scan_results.json に機械可読形式で収録。
2. **(6,6)**: m=8..15 で同様（29石@6×15 < 30）。**M_{6,6} ≥ 16**。
3. **(6,8)**: m=9..11 で同様（41石@6×11 < 42）。**M_{6,8} ≥ 12**。

K0806 の上界と合わせて M_{6,5} ∈ [20,658]・M_{6,6} ∈ [16,495]・M_{6,8} ∈ [12,371]。

## 根拠

- 各witnessは (a) census内蔵verify、(b) census不使用の独立検証
  （石3つ組外心列挙・厳密整数演算）の両方で safe+maximal。
- 修正したcensus（3点組外心完全列挙・接線時二重追加なし・r² は g² で正規化）は
  制御で K0796・K0069・K0759 の既知の値をすべて再現。
- 独立検証器は開発中の実装バグ2件（偽危険曲線による非極大候補・census脱落による
  非安全候補）を実際に捕捉した。全witnessは修正版で再検証済み。

## 限界・スコープ

- **非発見は不在証明ではない**: (6,5) m=20、(6,6) m=16、(6,8) m=12,13、
  (5,6) m=16..18、(5,7) m=19..21 は貪欲（≤1000リスタート）で発見できず満容量に到達。
  これらの m での存在是非はすべて未解決。
- 下界はwitnessの実在による証明だが、M 値の確定（上界との一致）はどこも主張しない。
- レジューム: (1) class-DFS（K0761式blocker分岐の一般化）で上記非発見 m を探索、
  (2) M_{6,7} 上界402の算術的縮小、(3) 幅5と幅6の欠損witness残存範囲の対比定式化。
