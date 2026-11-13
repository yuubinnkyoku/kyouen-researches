---
id: K0795
title: 固定幅盤のP(w)とM_{w,q}の横断表 — 合成分離帯 M_{w,q}=q−1（q≥max(P(w),w)+1・w=6..64）の統一とresults/統合
kind: proposition
status: proved
topics: [rectangles, geometry, variants, grundy]
aliases: []
scope: "標準整数格子の固定幅 w×m 盤。P(w) は全幅 w=6..64 で確定済み（K0763..K0794）。本項目は(1) K0767の系「q>P(w) かつ q>w なら行分離し M_{w,q}=q−1」を P(w) 確定値と合成した閉じた形 q≥max(P(w),w)+1（w=6..64）を統一命題として明示化し、(2) 真の満容量安定化長の確定値7件・open境界4件・parametric無限族とともに results/fixed-width/ に機械可読化した。合成帯は既存の全列挙（289点）を包含し矛盾しないことを機械検証済み"
evidence: "純粋な合成（corollary composition）であり新しい数学を含まない: 円は全m≥1で高々P(w)点・非水平直線は高々w点なので q>P(w)∧q>w なら禁止q点集合は単一行内のみ → 各行は容量q−1の独立成分 → g(S)=(w·min(m,q−1)−|S|) mod2・M_{w,q}=q−1（K0767系・K0025と同一導出）。整合性検証は独立スクリプトで289点全包含・P(w)単調非減少・K0784奇数w系包含の3検査すべてPASS"
solution:
  board: 幅w固定長m可変の標準整数格子（w×m・全m≥1）
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: 合成分離帯の(w,q)で全m≥1・全安全局面
  conditions: 連続整数行・q≥max(P(w),w)+1（w=6..64）またはparametric行の条件
  verification: [mathematical-proof]
  certificate: K0767系（行分離帰着）とP(w)確定値（K0763..K0794の全称証明）の合成
  independent_check: 289点の文書化済み(w,q)決定の全包含検査・P(w)単調性・K0784奇数w系包含（scripts/mwq_results_check.ts）
  note: "合成分離帯はw=43..64の帯（例: w=49ではq≥50・w=64ではq≥65）を含み、従来項目ごとに列挙されていた新規q帯を単一の閉じた形に統一。P(w)改訂時はresults表の追従更新が必要"
relations:
- type: depends_on
  target: K0767
  note: 行分離系（q>P(w)かつq>w⟹M=q−1）と会計の枠組み。合成の本体
- type: depends_on
  target: K0025
  note: q>2w無限族とg公式の枠組み
- type: depends_on
  target: K0302
  note: 確定閾値5件（M_{3,4}..M_{4,8}）の出典
- type: depends_on
  target: K0794
  note: P(w)全幅確定（w=6..64）の最終幅。合成帯の全幅性はK0763..K0794に依存
- type: supports
  target: K0332
  note: 安定化長M_{w,q}の定義と枠組み。本項目で確定値・境界・分離帯が機械可読化された
artifacts:
- path: results/fixed-width/pw_circle_point_max.csv
  role: data
  note: P(w)確定値 w=6..64（出典・witness付き）
- path: results/fixed-width/mwq_stabilization.csv
  role: data
  note: M_{w,q}の確定閾値7件・open境界4件・合成分離帯59行・parametric無限族6行
- path: results/fixed-width/README.md
  role: source
  note: 列定義と正本ポインタ
- path: research/experiments/mwq-results-integration-20261113/scripts/mwq_results_check.ts
  role: verifier
  note: 289点包含・単調性・奇数w系包含の独立検査
- path: research/experiments/mwq-results-integration-20261113/output/mwq_results_check.json
  role: data
  note: 検査結果（nChecks=289・fails=0・monotone=true）
- path: research/experiments/mwq-results-integration-20261113/reports/mwq-results-integration.md
  role: proof
  note: 統合の設計・合成帯の導出・検証・限界
---

# K0795: 固定幅盤のP(w)とM_{w,q}の横断表 — 合成分離帯の統一

## 命題

1. **合成分離帯（proved・全称）**: 標準整数格子の幅 w（w=6..64・P(w) 確定幅）に対し、
   q ≥ max(P(w), w) + 1 ならば行を跨ぐ禁止 q 点集合は存在せず、全 m ≥ 1・全安全局面で

   g(S) = (w·min(m, q−1) − |S|) mod 2,　M_{w,q} = q−1。

   P(w) は円の格子点数の全称上限（全 m ≥ 1）で、K0763..K0794 により
   全幅 w=6..64 で確定済み（8,10,12,12,12,14,16×10（w=12..21）,18,20,20,22,
   24×17（w=26..42）,26,28,28,30,30,32,32×16（w=49..64））。
   導出は K0767 の系（円 ≤ P(w) < q・非水平直線 ≤ w < q → 単一行内の禁止のみ →
   行独立性）の P(w) 確定値への適用であり、新しい数学ではない。
2. **既存列挙との整合（機械検証済み）**: K0072/K0763/K0764/K0765/K0767/K0776/K0778/
   K0782/K0784 が明示的に列挙した新規 (w,q) 決定 289 点はすべて合成帯に包含される
   （下回り 0 件）。K0784 の奇数 w 系 (w, w+1)（w=21..63 奇数）も包含。
   合成帯はこれらを一般化する閉じた形である。
3. **真の満容量安定化長の現況（表化）**:
   確定 7 件 — M_{3,4}=24・M_{3,5}=12・M_{3,6}=9・M_{4,6}=16・M_{4,7}=13・
   M_{4,8}=11（K0302・K0077）・M_{5,8}=16（K0331）。
   open 4 件 — M_{2,4}≤9（K0069・最小性未検証）・M_{5,6}∈[16,249]（K0723）・
   M_{5,7}∈[19,158]（K0332・5×19の完全列挙は m=19 のみで上界にならない）・
   M_{6,7}≥20（K0761）。
   P(w) 未確定幅（w≥65）に効く parametric 無限族 — K0025（q>2w）・
   K0072（q=2w, w≥5・q=2w−1, w≥6・q>w+⌈w/2⌉, w≥15）・K0776（q>2⌈w/2⌉, w≥19）・
   K0784（奇数 w≥21 で (w,w+1)）。

## 成果物の置き場所

results/fixed-width/（pw_circle_point_max.csv・mwq_stabilization.csv・README.md）と
research/experiments/mwq-results-integration-20261113/（検証スクリプト・出力・報告）。

## 限界

- 合成帯の数学的内容は K0767 系と P(w) 各項目の全称証明に完全依存。
  P(w) が改訂された場合は results 表と本項目の追従更新が必要。
- 標準整数格子限定。任意間隔平行行には主張しない。
- results/ は計算時の集計資料であり、命題の正本は本項目が保持する。
