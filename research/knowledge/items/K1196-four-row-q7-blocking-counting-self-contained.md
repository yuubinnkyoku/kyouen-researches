---
id: K1196
title: 4×m・q=7の行欠損極大安全配置はm≤86、よってM_{4,7}=13はK0318非依存の第二certificateで閉じる（自己完結ブロッキング計数）
kind: proposition
status: proved
topics: [rectangles, variants, counting]
aliases: [four-row q7 blocking-counting certificate, M_{4,7} second certificate]
relations:
- type: supports
  target: K1182
  note: M_{4,7}=13の第二certificate（K0318非依存の閉包）。K1182のstatus proved・Mの値13は一切変更しない
- type: depends_on
  target: K1177
  note: 系のcertificate併合で使用する既刊正本: q=7 def 全幅掃引 13..85（sat2.js CNF・pinned kissat 4.0.4・rc=20・INDET 0）・m=12 不足極大 witness（下界）・m=13/16 capacity witness・records.jsonl 112レコード
- type: uses
  target: K1182
  note: m=86 genfast3 掃引 UNSAT（conflicts 5930・2回bit-exact）と m=87,88 UNSAT（5191/6072）の支持証拠。定理自体（m≤86）は掃引にもK0318にも依存しない
- type: related
  target: K0024
  note: 系のゲーム帰結 g(S)=(24−|S|) mod 2（空盤 second-player-win）の基盤はK1182と同一
artifacts:
- path: research/experiments/four-row-q7-blocking-counting-self-contained-20261121/README.md
  role: proof
  note: 証明本文（補題L1-L4・計数不等式・系・一般化備考・機械検証・解釈規約・sha256 68c05e0a…）
- path: research/experiments/four-row-q7-blocking-counting-self-contained-20261121/scripts/verify_blocking_counting_20261121.py
  role: verifier
  note: stdlibのみ・決定的・fail-closed検証機（49 gate・sha256 ee5d88e2…）
- path: research/experiments/four-row-q7-blocking-counting-self-contained-20261121/output/audit.json
  role: verifier
  note: 機械可読監査正本（49 gate明細・sha256 43618370…・4 battery byte-identical）
- path: research/experiments/four-row-q7-blocking-counting-self-contained-20261121/output/reproduction.log
  role: log
  note: battery・負/正の制御の実行記録
- path: research/log/2026-11-21-four-row-q7-blocking-counting-self-contained.md
  role: log
  note: セッションlog（宣言・battery・出版・実験事実）
solution:
  board: 4×m・q=7
  level: strong
  outcome: second-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: m≥13の全安全局面（K1182と同値・K0318非依存の閉包として再確定）
  conditions: q=7,w=4,m≥13
  verification: [mathematical-proof, machine-audit]
  certificate: 機械掃引[13,86]（K1177の13..85＋K1182のgenfast3 m=86）＋計数上界[87,∞)（本項の定理）＋m=12不足極大証人＋capacity存在（m=13/16 witness・同一石集合の幅単調性）
  independent_check: 49 gate検証機（幾何補題の格子全域整数演算テスト・計数不等式817²全数値列挙・掃引recordsのq7射影sha pin・m=12 witnessの全前提instantiation監査）・4 battery byte-identical・負の制御（tamperでGATE FAILED・監査未書込）・正の制御（append不変）
  note: g(S)=(24-|S|) mod 2（K0024飽和形式・K1182と同一）
---

# 4×m・q=7の行欠損極大安全配置はm≤86、よってM_{4,7}=13はK0318非依存の第二certificateで閉じる（自己完結ブロッキング計数）

K1182 の解釈規約に明示された自由課題「K0318 に依存しない自己完結的なブロッキング
計数証明（M の値を変えないが証明の独立性を高める）」の完成項目。主定理は
K0318・K1177・掃引のいずれにも依存しない独立の数学的証明であり、系で既刊掃引と
併合して K1182 の主張 M_{4,7}=13 を別の証明基盤から再確定する。
単一オーナー宣言ノート: commit `80ebdec39e7b349e2d3f2b6c66b652b3936f4e91`
（宣言時 main HEAD `497f4e176e82d979e65084900acc4ee7d3c72c0e`・2026-11-21T07:36Z）。

## 主定理（自己完結ブロッキング計数上界）

**定理.** w=4・q=7 の 4×m 盤（一般に 4 本の水平線上の点配置。整数格子性は使わない）
において、行欠損（ある行の石数 ≤ q−2 = 5）を伴う極大安全配置が存在するのは
m ≤ 86 のときに限る。したがって m ≥ 87 では全極大安全配置が満容量である。

**証明の骨子**（全文は実験 README・実験dir参照）: 欠損行 R の空格子点 p は
（L1: 行容量 6 ゆえ水平線は 6 石に届かず block できず、L2: 非水平直線は格子点 ≤ 4
ゆえ 7 点に届かないため）すべて真円の blocker 円で block される。割当円 C_i の
R 内割当点 e_i ∈ {1,2}・R 内石 u_i は L3（円×水平行交点 ≤ 2）より
e_i + u_i ≤ 2、blocker 定義より円上石数 ≥ 6 なので R 外石数 t_i ≥ 4 + e_i。
L4（相異なる 2 円の共有点 ≤ 2・円は非共線 3 点で一意）より、円上の R 外石の
非共線 3 点組は相異なる円間で非交差であり、R 外石は高々 3(q−1) = 18 個なので

Σ_i C(t_i, 3) ≤ C(18, 3) = 816、各円で C(t_i, 3) ≥ 10 e_i

ゆえ 10(m − r) = Σ 10 e_i ≤ 816 ⟹ m − r ≤ 81 ⟹ m ≤ r + 81 ≤ 86。∎

（同一円上の 3 格子点は非共線: 共線なら水平線だが L3 の交点 ≤ 2 と矛盾。
限界費用は type-1 = C(5,3) = 10・type-2 = C(6,3)/2 = 10 で等しい。
全数値列挙 max {a+2b : 10a+20b ≤ 816} = 81 は検証機 gate g05 で確認。）

## 系: M_{4,7} = 13 の第二certificate（K0318 非依存）

1. 機械掃引 [13,86]: K1177 の 13..85 全幅 UNSAT＋K1182 closure の m=86 UNSAT
   （genfast3・2 回 bit-exact）。m=87,88 の UNSAT はさらに先の支持証拠。
2. 計数上界 [87, ∞): 本定理（数学的証明・K0318 非依存）。
3. 下界: m=12 不足極大 witness（23 石・rows [6,6,5,6]・K1177）。
4. capacity 存在 m ≥ 13: m=13/16 SAT witness と同一石集合の幅単調性（K1182 で確立）。

1+2 で m ≥ 13 の全幅が def-UNSAT、3+4 で P(12) 不成立かつ capacity 存在となり、
**K0318 の一般上界 U_{4,7}=81 を使わず M_{4,7} = 13 が閉じる**。
ゲーム帰結 g(S) = (24 − |S|) mod 2（空盤 second-player-win）も K1182 と同一。

## 誠実な相対位置の記載

計数上界の閾値は独立に見ると m ≥ 87 であり、K0318 の解析上界 m ≥ 81 より
6 幅弱い（上界の品質は K0318 が上）。既刊掃引が 86（さらに 88）まで埋まっている
ため certificate としては十分。本項の独立価値は閉包が「有限掃引＋初等的な計数」の
2 部品のみで構成され、一般閾値定理への依存を除去した点にある。
**K1182 の status・数値は一切変更しない（第二 certificate の追加のみ）。**

## 一般化の備考 (w=4)

同じ計数は q ≥ 5 で通り、q=6 は m ≤ 117（K0318 の U_{4,6}=103 より弱い・参考値、
M_{4,6} = 16 or ∈ [35,103] は本項では閉じない）、q=8 は m ≤ 82
（K0077 で M_{4,8}=11 は既に閉鎖済み・参考値）。閾値が既刊掃引と噛み合うのは
q=7 のときに限る。

## 機械検証

`scripts/verify_blocking_counting_20261121.py`（stdlib のみ・決定的・fail-closed:
監査は全 gate 通過時のみ書込・1 実行約 1.0 秒）の 49 gate
（A 幾何補題 9 / B 計数 3 / C 掃引 certificate pin 7 / D m=12 witness 前提 15 /
E m=13 capacity 7 / F 組立 4）。battery 4 実行（同一 cwd 3 回＋隔離 copytree・
隔離 HOME/TMPDIR・env -i・PYTHONHASHSEED=random 1 回）すべて監査 byte-identical
（sha256 `4361837037034b632f79f2b6c9cef6f1ca3fc03a85d64e66b90acc810fefb277`）。
負の制御（m=12 witness byte 400 XOR 0x20 → rc=1・GATE FAILED g15_pin・監査未書込）・
正の制御（records.jsonl に無関係 1 行追記 → rc=0・監査 byte 同一・append 不変）を
実測済み。m=12 witness では定理の全前提が実データ上で成立することを検証機が
instantiation 監査している（Σ C(t,3) = 80 ≤ 816・10(m−r) = 70・割当円 7 個の
e/u/t 分類・3 つ組 registry 80 非交差直接確認）。

## 解釈規約

- 本項は K1182 の主張の第二 certificate であり、既存 verdict・records・witness の
  変更は一切しない。行は 1 行も閉じない（n11 の fold/coverage 簿記に無関係）。
  nodes 数・conflicts 数・solved 数を勝敗として読まない。REFUTED-D10 は LOSS 証明ではない。
- q=6 の M_{4,6} = 16 or ∈ [35,103] は本項では閉じない（参考値 m ≤ 117 のみ）。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**（固定幅レーンであり n11 の決着に影響しない。）
