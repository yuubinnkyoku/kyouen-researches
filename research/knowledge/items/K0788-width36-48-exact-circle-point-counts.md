---
id: K0788
title: "幅36..48の円点数の完全決定 P(36)..P(42)=24・P(43)=26・P(44)=P(45)=28・P(46)=P(47)=30・P(48)=32 — level分類のstreaming bitset DFS完了・g0証明書のconvention B厳密化（既存定理は不変）"
kind: proposition
status: computed
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子（K0784と同一のstrip窓意味論）。全称：level L全滅（窓マスクDFS零生残＋g0≧2会計）⇒P≦2(L−1)、witness下界と等号。convention B厳密化はK0767..K0784の同パリティclassMax計算の証明基盤の修正だが、数値検証により既存の結論は全て不変"
evidence: "streaming bitset DFS（候補Set不使用・メモリ一定・w=42で1.10M nodes）。制御3系統: w=26 L12がちょうどS*（650円）を1生残として再現・w=27/35 L13全滅がK0784と一致・独立参照実装subsetOKによる乱数サンプリング800件全滅。g0会計: g0=2は全点行偶数を強制し偶数法ではu=q奇（u奇制限でclassMax 13→7・w=41,42を閉じる）・g0=3は係数36でclassMax 8..11・g0≧4は類サイズ≦12。witness下界は650円24点（w=36..42）と2210円strip 26/28/28/30/30/32点（w=43..48・K0786と同一・独立再計数で一致）"
relations:
- type: depends_on
  target: K0784
  note: level会計・窓マスク・証明書の枠組みと24プラトーw=26..35・普遍上界。本項目はK0784レジューム「level 13のw=36..42分類（streaming）」の完了
- type: depends_on
  target: K0786
  note: witness下界（650円・2210円strip）。本項目の等号の下界側
- type: depends_on
  target: K0332
  note: 固定幅盤の枠組みと円点数P(w)の定義
- type: supports
  target: K0778
  note: "convention監査: K0767..K0784で使われた同パリティ係数16 classMaxは行値y座標（=64t²）で計算されており導出不能。正当な証明書は類変数tの4g0²（convention B）。数値検証でK0778のw=17..20 classMaxはBでも6/6/7/7<9で結論不変・法9周期最大もBで6のまま"
- type: supports
  target: K0025
  note: P(w)の新確定値は行分離公式の M_{w,q}=q−1 帯の基礎データを更新（K0784系の系と同じ導出で拡張可能）
artifacts:
- path: research/experiments/width36-48-level-classification-20261113/scripts/width36_48_level_classify.ts
  role: verifier
  note: streaming bitset DFS機械の単独再現（決定的・STAGE分割実行・制御・g0会計・witness検証込み）
- path: research/experiments/width36-48-level-classification-20261113/output/width36_48_level_classify.json
  role: data
  note: 全段階の機械出力（分類12件・制御・g0会計・witness・主張）
- path: research/experiments/width36-48-level-classification-20261113/reports/width36-48-level-classification.md
  role: proof
  note: 意味論・証明の構造・convention監査・制御・限界
---

## 主張

1. **P(36) = ... = P(42) = 24**（全称・等号付き）。上界: level 13 全滅
   （窓マスクDFS零生残・ノード84k..1.10M・dedup Set不使用のstreaming実装）。
   下界: 650円の24点（行0..25 ⊆ 0..w−1）。
   **24プラトーは w=26..42 に拡大**（K0784の26..35を延長）。
2. **P(43) = 26・P(44) = P(45) = 28・P(46) = P(47) = 30・P(48) = 32**
   （全称・等号付き）。上界: level 14/15/15/16/16/17 全滅。
   下界: 2210円strip 26/28/28/30/30/32点（K0786 witness・独立再計数で一致）。
   **26..32帯の初の厳密値。K0786のwitness族が各wで最適と確定**。
3. **g0証明書のconvention B厳密化（監査）**: 非標準形 e=q/g0 の証明書は
   類変数 t=(y−r)/g0 に対する係数 **4g0²**（convention B）でのみ導出できる。
   過去の同パリティclassMax（K0767..K0784）は行値 y での 16y²（=64t²）で
   計算されており、これは導出できない convention A である。
   **ただし数値検証で既存定理の結論は全て不変**: 法9係数16周期最大はBでも6
   （K0784の普遍上界の根拠は不変）・K0778のw=17..20のg0=2 classMaxは
   Bで6/6/7/7<9。さらに2つの正当な強化を証明: **g0=2は全点行を偶数に強制**
   （奇行クラスはg0=2になり得ない）・**偶数法では線形係数u=qは奇**
   （u奇制限でclassMaxは13→7に落ち、w=41,42の境界ケースを閉じる）。

## 構造

- 跳躍構造の完全決定（w≤48）: 24プラトー（650円）→ w=43で26 → 2210円族が
  w=43..48で最適。次の跳躍はP(49+)で、より大きなr₂類（11050円・K0785）が
  候補。level 18分類は本機械で同様に可能。
- 候補爆発の解消: K0784のSetベース列挙（w=35で36,920候補・w=36でメモリ限界）を
  窓マスク上のDFS+ビットセットAND枝刈りで置換。多重列挙は全滅主張に無害で
  メモリ一定。生残がいた場合のみ重複排除してrealizability掃引に回す。

## 限界

- P(19),P(20)（予想16）とP(21)∈{16,17,18}はopenのまま。
- w=49以上はopen（level 18+の分類・2210/11050族のw=49..106帯の予測）。
- convention Aの是正としてK0778/K0784のevidence本文の記載更新は
  統合時の対応事項（結論の変更なし・本項目が根拠）。
