---
id: K1182
title: 4×m・q=7の真の満容量安定化長はM_{4,7}=13
kind: proposition
status: proved
topics: [rectangles, variants, grundy]
aliases: []
relations:
- type: depends_on
  target: K0024
  note: q点版固定幅の十分長さ定理。飽和状況のゲーム値形式 g(S)=((q−1)w−|S|) mod 2・先手勝ちiffq偶数かつw奇数の判定規約が本項のゲーム帰結の基盤
- type: depends_on
  target: K0318
  note: 証明済み一般上界 U_{4,7}=81（curve-packing fixed-width 閾値・三つ組充填計数）。closure レーンが独立実装 u_recompute.js で全30エントリ一致を機械確認
- type: depends_on
  target: K1177
  note: 有限掃引。q=7 witness band {7..12} SAT・witness-free band {13..85} 全幅 UNSAT（INDET 0・records機械監査）と m=12 不足極大 witness（下界）
artifacts:
- path: research/experiments/four-row-q7-stabilization-closure-20261121/README.md
  role: proof
  note: closure 実験dir 報告書（根拠の分担・genfast3 較正・live 再検証・受理条件つき宣言note 同dir）
- path: research/experiments/four-row-q7-stabilization-closure-20261121/output/u_recompute.json
  role: verifier
  note: K0318 整数最適化の独立再実装の結果正本（entries_checked 30・mismatches 0・U_{4,6}=103/U_{4,7}=81 含む）
- path: research/experiments/four-row-q7-stabilization-closure-20261121/output/records_audit.json
  role: verifier
  note: K1177 records.jsonl 108レコードの機械監査（q=7両帯・q=6両帯の完全性・INDET 0）
- path: research/experiments/four-row-q7-stabilization-closure-20261121/output/records_audit_ext88.json
  role: data
  note: m=86..88 追記後 112レコード再監査
- path: research/experiments/four-row-q7-stabilization-closure-20261121/scripts/genfast3.js
  role: solver
  note: 弦対抽象円 census（six-row-q8-band-closure-22-370-20261114 出版と byte-identical・md5 12c2bd9c…、q≥w+2 完全性論で w=4 に適用・低帯較正で sat2.js 出版 CNF と byte 一致・conflicts bit-exact）
- path: research/experiments/four-row-q6-q7-frontier-20261121/output/records.jsonl
  role: data
  note: 112レコード正本（closure band extension 4追記・m=86..88 UNSAT と (4,86,7) lexH を含む）
- path: research/log/2026-11-21-four-row-q7-m47-closure.md
  role: log
  note: closure セッションログ
solution:
  board: 4×m・q=7
  level: strong
  outcome: second-player-win
  classification: [root, first-moves, all-safe-win-loss, all-safe-grundy]
  coverage: m≥13の全安全局面
  conditions: q=7,w=4,m≥13
  verification: [mathematical-proof, exhaustive-enumeration]
  certificate: m≥81の証明済み一般上界（K0318・U_{4,7}=81）＋帯[13,85]の完全有限排除（K1177）＋m=12不足極大証人
  independent_check: K0318最適化の独立再実装（30エントリ全一致）＋records機械監査＋genfast3によるm=86..88直接掃引・較正CNF byte一致・pinned kissat conflicts bit-exact（2回の独立実行）
  note: g(S)=(24-|S|) mod 2
---

# 4×m・q=7の真の満容量安定化長はM_{4,7}=13

安定化長は K1177 と同一の定式化: M_{4,7} = least m0 such that P(m) for all m >= m0、
P(m) ⟺「4×m の全極大安全配置が満容量 (q−1)·4 = 24 石」⟺（被覆論により）def-mode UNSAT ∧ capacity 配置の存在。

三つの根拠の分担:

1. **一般上界（全域・解析的）**: K0318 の証明済み curve-packing（三つ組充填）一般上界
   U_{4,7} = 81 により m >= 81 の全幅で def-mode UNSAT。closure レーンは K0318 の
   整数最適化を独立実装（u_recompute.js）して閾値 JSON の全 30 エントリ一致を
   機械確認した（U_{4,6}=103 も再現・mismatches 0）。
2. **有限排除（帯 [13,85]・機械的）**: K1177 の q=7 全幅完全掃引 13..85 がすべて
   UNSAT（kissat 4.0.4 pinned・rc=20・INDET 0・records 機械監査で帯の完全性を確認）。
3. **下界**: m=12 に行欠損極大安全配置が存在（K1177 witness: 23石・rows [6,6,5,6]・
   3系統検証 PASS）より P(12) は不成立。

1 と 2 を併合すると [13,85] の有限排除と [81,∞) の解析上界が全幅 m >= 13 を被覆し、
3 により M > 12 が言えるため **M_{4,7} = 13** が閉じる。K0077 で確立した
「解析的上界＋有限排除＋下界証人」パターンの w=4, q=7（q=w+3 境界側）適用であり、
K0077（q=2w 境界・M_{4,8}=11）と合わせて w=4 の真の安定化長は q=7,8 の両側で確定した。

capacity 配置の存在は m=13,16 の SAT 実在（24石・全行6・3系統 capacity 検証 PASS）と
同一石集合の幅単調性（広い盤でも安全・極大）により m >= 13 全幅で従う。

**壁の先の直接確認（支持証拠）**: sat2.js 全三つ組 census の符号化メモリ壁（m=86）の先を、
six-row-q8-band-closure 出版の genfast3.js（弦対抽象円 census・md5 12c2bd9c…・byte-identical・
q >= w+2 完全性論で w=4 q=7 に適用）で掃引し、m=86..88 の 3 幅すべて UNSAT
（conflicts 5930/5191/6072・2回の独立実行で bit-exact）、(4,86,7) def-mode の `--lex=H`
交差符号化も UNSAT（conflicts 3677）。低帯較正として (4,13,7)・(4,20,7)・(4,16,6)・(4,85,7) の
CNF が sat2.js 出版値と byte 一致（md5 80663be5/6f882012/3ce3a8fa/2f78307d）・
pinned kissat conflicts も bit-exact（5446/3359/1980648/3759）。閉包の論法自体は
K0318 が [81,∞) を担うためこれらに依存しない。

## ゲーム帰結（K0024 の飽和ゲーム値形式の適用）

m >= 13 では全極大安全配置が満容量 24 石（全行 6）であり、任意の安全局面 S は
どのプレイ列でもちょうど 24−|S| 手で極大（終局）に到達する。よって

**全 m >= 13・全安全局面 S について g(S) = (24 − |S|) mod 2**（K0024 の形式
g(S)=((q−1)w−|S|) mod 2 の q=7, w=4 場合）。特に空盤は g=0、すなわち
**second-player-win**（K0024 の判定規約「先手勝ち iff q 偶数かつ w 奇数」と整合:
q=7 は奇数）。

## 解釈規約

- 本項は m >= 13 の全幅を K0318 の証明済み定理で被覆するため、有限掃引 13..85 の
  「未掃引幅への無主張」制約（K1177 の解釈規約）を超えて M を全称確定する。
  有限掃引と解析上界の役割分担は実験 README 参照。
- q=6 は本項で閉じない。M_{4,6} = 16 or ∈ [30,103]（U_{4,6}=103・K0318）のまま。
  残る 74 幅の掃引か解析的排除で閉じられる。
- 標準 11×11 空盤・二石 root 等の未解決局面に本項は影響しない（固定幅レーン）。
- m=86..88 の直接掃引は支持証拠であり、K0318 に依存しない自己完結的な
  ブロッキング計数証明は引き続き自由課題（M の値を変えないが証明の独立性を高める）。
