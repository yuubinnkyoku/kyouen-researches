---
id: K0807
title: "w=83正制御の完走 — REST6掃引機の生存検出感度を実証（生残ちょうど2件・両方11050円の両端83幅窓で実現・certificate-phantom 0件）・level 17復活点の実測確定はちょうどw=83・w=83の生残パターン完全特定（2.42G nodes・leaves=2・実現可能）"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w=83・長さm可変の標準整数格子におけるlevel 17 REST6生残パターンの完全決定（有限計算の全称: 全3,300 maximal mask走査）。主張: (1) w=83のREST6生残17行パターンはちょうど2件 {0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82} と {0,5,7,19,27,32,40,52,54,59,63,70,73,76,77,81,82}（他は全滅）。(2) 両パターンともREST16の16法全てで生残（phase 2でも死なない）。(3) 両パターンとも11050円（(2x−105)²+(2y−105)²=11050・48点）の83幅窓 x∈[0,82] と x∈[23,105] で実現（各34点・17行・行集合はパターンと完全一致）→ certificate-phantom 0件・REST6⊇REST16⊇実現可能 の差分は w=83・level 17 では空。(4) したがってlevel 17の復活点は実測でちょうど w=83（K0804のP(w)=32 for w≤82 と合成し、(82,83]が閉区間として確定）。P(83)≥34 は witness で既知・P(83)の上界はopen"
evidence: "数学的証明（K0804機 width_sweep.mjs の w=83 完走 + 3段階の追試）。(a) 完走走査: node width_sweep.mjs 83（5G budget・505チャンク・2,420,302,072 nodes・capEsc 72・unique 3,456・maximal 3,300・done=true・leaves=2・生残2・2.4M capプロトコル・最終チャンクabortedなし）。(b) 生存帰属: width83_survivor_probe.mjs（同一アルゴリズム+帰属ログ）で生残mask 456（1 leaf・101,881 nodes再現）と 3119（1 leaf・156,184 nodes再現）を特定・生残17行集合を抽出（state_w83.json の2生残チャンク from=454/3114 と一致）。(c) REST16再検査: 両パターンが16法 [19,23,7,5,27,43,47,13,17,8,16,25,29,31,37,41] 全てで共通証明書非空。(d) 実現の直接検証: 11050円の点を独立直接列挙し、窓 x∈[0,82] が34点・17行（パターン3119と完全一致）・窓 x∈[23,105] が34点・17行（パターン456と完全一致）を確認。(e) 有限実在スキャン: R'≤1e6・1mod4-smooth・prod(e+1)≥9 の全1,964円・3実現形でこの2 maskを実現するのは R'=5525 のみ。正制御: witness（K0785・11050円34点・最小幅83）が予測する生残が機械検出側でちょうど再現 → 生存検出感度が実証され、w≤82の全滅結果（K0801..K0804）の誤殺なしの裏付けになる"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: w=83の生残パターン完全特定は全3,300 maximal maskの全走査による全称（有限計算）。P(83)≥34は全m≥1でのwitness
  conditions: 連続整数行
  verification: [mathematical-proof, exhaustive-enumeration]
  certificate: 幅83 REST6 level 17 掃引完走（leaves=2・生残2・2.42G nodes）+ 生残mask・生残集合の帰属再現（probe・node数まで一致）+ REST16 16法再検査 + 11050円2窓の直接列挙一致 + R'≤1e6 実現スキャン（realizerは5525のみ）
  independent_check: probe の classifyOne node数（mask456=101,881・mask3119=156,184）・11050円の独立直接列挙（x∈[0,82]/[23,105] 34点・17行）・REST16再検査（16法全通過）・実現スキャン（1,964円・制御込み realizer 5525 のみ）・state_w83.json の生残チャンク位置一致
  note: "w=83 は K0797 会計（g0≥2形・w≤84）の範囲内だが、witness が既知のため level 17 全滅は P≤32 を与えない（K0804の限界どおり）。本項の価値は (i) 掃引機の生存検出感度の正制御（w≤82全滅の信頼性の実証的裏付け）・(ii) 復活点の実測確定・(iii) w=83 の level 17 実現可能パターンがちょうど2件でいずれも11050円の両端窓であるという孤立性（witness の certificate-理論的な剛性: 2パターンは同一円の中心対称な2窓に対応し、独立した2つのwitness族ではない）"
relations:
- type: depends_on
  target: K0804
  note: 掃引機（width_sweep.mjs）と w≤82 全滅の境界。本項はその正制御完了
- type: depends_on
  target: K0785
  note: 11050円 witness（P(83)≥34・34点最小幅83）が生残予測の源
- type: depends_on
  target: K0791
  note: 34点最小幅83（復活点の右端の理論的裏付け）
- type: supports
  target: K0785
  note: level 17 復活点を理論値 (82,83] から実測でちょうど w=83 に確定・witness パターンの掃引機内での完全特定
artifacts:
- path: research/experiments/width83-positive-control-20261114/scripts/width83_survivor_probe.mjs
  role: verifier
  note: 生存mask・生残17行集合の帰属ログ付きプローブ（width_sweep.mjs と同一アルゴリズム）
- path: research/experiments/width83-positive-control-20261114/scripts/width83_realizability_scan.ts
  role: verifier
  note: REST16再検査 + 11050円2窓の直接検証 + R'≤1e6 実現スキャン
- path: research/experiments/width83-positive-control-20261114/output/width83_positive_control.json
  role: data
  note: 完走走査・帰属・REST16・実現・スキャンの全記録
- path: research/experiments/width69-84-sweep-20261114/output/state_w83.json
  role: data
  note: w=83完走状態（2.4M capプロトコル・2,420,302,072 nodes・leaves=2・生残2・capEsc 72）
- path: research/log/2026-11-14-width83-positive-control.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・有限全称）

1. **w=83 の level 17 REST6 生残パターンはちょうど2件**:
   - P₁ = {0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82}（maximal mask 3119 内）
   - P₂ = {0,5,7,19,27,32,40,52,54,59,63,70,73,76,77,81,82}（maximal mask 456 内）
   - 他の全 maximal mask（3,298件）は leaves=0・生残0。
2. **両パターンとも REST16 を通過**（16法全てで共通証明書非空）→ phase 2 でも死なない。
3. **両パターンとも 11050 円で実現**:
   - 窓 x∈[0,82]: 34点・17行 = P₁（行集合は完全一致）
   - 窓 x∈[23,105]: 34点・17行 = P₂（行集合は完全一致）
   - ⟹ **certificate-phantom 0件**（REST6 ⊇ REST16 ⊇ 実現可能 の差分は w=83・level 17 では空）
4. **level 17 の復活点は実測でちょうど w=83**（K0804: w≤82 全滅 + 本項: w=83 生残2件・実現可能）。

## 正制御としての意義

- K0785 の witness 予測（w=83 で level 17 が死なない）を機械検出側でちょうど再現:
  掃引機の**生存検出感度が実証**された。w=49..82 の全滅掃引（K0790..K0804）は
  「生残が出た時に検出できる」ことが実機で裏付けられたことになる。
- 2つの生残パターンは**同一円の中心対称な2窓**に対応（独立した witness 族ではない）:
  11050円の 34点を含む83幅窓は x∈[0,82] と x∈[23,105] の2つだけであり、
  これが掃引機の生残の全容と厳密に一致する。

## 構造観察

- witness の孤立性: w=83 で生残するのは witness 円の行パターンのみ
  （R'≤1e6・prod(e+1)≥9 の全1,964円・3実現形のスキャンで realizer は R'=5525 のみ）。
- P₁ と P₂ は行集合としては異なるが、11050円の行多重集合の2つの83連続行窓
  （doubled座標 [−105,59] と [−59,105]）に対応。窓幅83は witness の 34点帯の
  ちょうど最小幅であり、両端の窓だけが34点に達する（K0785 の per-window 計数と整合）。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- **P(83) の上界は open**（35点以上の円が幅83に収まる可能性は排除していない。
  level 18 掃引が必要）。P(83)≥34 のみ確定。
- w=84 の正制御は未実行（34点 witness は幅83..86で有効・K0785）。
  K0797 会計は w≤84 で有効。
- 実現スキャンの円の範囲は R'≤1e6・prod(e+1)≥9（r2≥36）に限定。
  より小さい r2 の円や R'>1e6 は掃引していない（ただし生残パターンの実現は
  11050円で直接的に確認済みのため、スキャンは孤立性の補助証拠）。
- 11×11 空盤・二石 root {49,60} は本項目と無関係に UNKNOWN のまま。
