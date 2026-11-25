---
id: K1216
title: (6,5) 6×31 witness — K0815 L2 6×30 witnessの純並進で下界更新 M_{6,5}∈[32,658]・単一石集合で幅26..31の6連続staircase・6×32 編集近傍の限定的陰性
kind: proposition
status: proved
topics: [rectangles, maximal-safe, variants]
aliases: []
relations:
- type: generalizes
  target: K0815
  note: 第6弾 L2 6×30 witness（第3同型類・rows 4,4,4,4,4,3）の x+1 純並進で witness 帯を 6×31 に延伸し M_{6,5}≥31 を ≥32 に更新。第5弾の「6×31 r≤5 探索 0件」はプール相対の限定陰性であり本結果と矛盾しない（L2 は第6弾で発見・純並進は未走査だった）
- type: depends_on
  target: K0853
  note: 自由列追加判定補題（安全性の幅非依存・blocked 性の (S,c) 局所性）が x+1 並進 witness の正しさと witness_widths staircase の根拠
- type: depends_on
  target: K0854
  note: 行直線ブロック命題（欠損行とブロック構造の帰結）
- type: depends_on
  target: K0806
  note: 上界（K0318 代入）は不変
artifacts:
- path: research/experiments/six-row-q5-m31-band-extension-20261122/w6x31q5_L2shift1.json
  role: source
  note: 6×31 q=5 witness 23石（rows 4,4,4,4,4,3・sha256 245adc6d…）・L2 6×30 witness の x+1 平行移動
- path: research/experiments/six-row-q5-m31-band-extension-20261122/scripts/surgery_gen.js
  role: source
  note: 整数正準曲線鍵検証器（--verify で safe+全盤 maximality+行欠損を判定・K1209 出版pinと byte 同一 dfc97506…）および bounded surgery engine
- path: research/experiments/six-row-q5-m31-band-extension-20261122/scripts/det_q_verify.py
  role: source
  note: 純 3×3/4×4 行列式ゼロ判定の第2系統検証器（det3/det4・safe+maximal_at_m）
- path: research/experiments/six-row-q5-m31-band-extension-20261122/scripts/append_criterion.py
  role: source
  note: 純 Python Fraction の free-append 判定器（出版 pin byte 一致 d08d8fb1…・old_uncovered/reach/witness_widths を出力）
- path: research/experiments/six-row-q5-m31-band-extension-20261122/scripts/surgery_deep.js
  role: source
  note: 6×32 frontier 用 bounded-edit engine（core verbatim + remKadd0/rKa1 完全クラス + rem3add2 targeted-complete・per-base checkpoint）
- path: research/experiments/six-row-q5-m31-band-extension-20261122/scripts/run_verify_suite.sh
  role: source
  note: 3系統検証+対照+陽性対照の決定的スイート（run A/B byte 一致）
- path: research/experiments/six-row-q5-m31-band-extension-20261122/output/verify-w6x31-three-systems.json
  role: data
  note: 3系統検証の統合機械記録（tamper 陰性対照・5同行制御・L2 陽性対照・決定性を含む）
- path: research/experiments/six-row-q5-m31-band-extension-20261122/output/translation-census-summary.json
  role: data
  note: 公開 m≤30 プール 15 iso-config の D4 像込み純並進 free-append census（maxw=50・band_top 31 は c009 のみ・reach≥32 皆無の限定観察）
- path: research/experiments/six-row-q5-m31-band-extension-20261122/output/w32-bounded-edit-negatives.json
  role: data
  note: 6×32 限定陰性（24 base×r0s/r1a1/r2a1/r3a1/r4a1 完全走査・t2 は c009@off3 のみ完走 17,233,201 候補・全 0 witness・UNDETERMINED 不変）
solution:
  board: 6×31（q=5）
  level: weak
  outcome: conditional
  classification: [root]
  coverage: 6×31 q=5 に行欠損極大安全witnessが存在（下界のみ更新）
  conditions: q点共円・共線禁止・標準整数格子・maxx=25 の同一石集合が幅26..31の各盤に埋め込み可能
  verification: [independent-enumeration]
  certificate: witness座標（3系統独立検証器がすべて safe+maximal PASS・tamper/5同行は全系統 FAIL・出版 L2 6×30 witness は同経路で WITNESS_OK 再現・2回実行 byte 一致）
  independent_check: 異なる数学的原理（整数正準曲線鍵・行列式ゼロ判定・Fraction 円方程式）による3系統の一致
  note: 下界更新のみ（M_{6,5}∈[32,658]・上界 T=658 は K0806 代入で不変・mwq_stabilization.csv は K1201 前例により不変）。t2 targeted-completeness の帰着（unblocked target の covering curve は必ず D(u) 上の add を持つ）は実験 README に明記。6×32 編集近傍陰性は公開プール配置相対の限定スコープであり不在主張ではない。衝突確認: K1216 は 2026-11-22T01:33Z HEAD `2b7b4db` 時点で未使用。
---

# (6,5) 6×31 witness の構成と下界更新（2026-11-22）

単一オーナー宣言 `bc11e28b`（research/log/2026-11-22-six-row-q5-m31-band-extension-single-owner-note.md・
宣言時HEAD `bcc39add`）の下、K0815 第6弾の L2 6×30 witness（conflicts 4,001,401・rows 4,4,4,4,4,3）を
x+1 に純並進した23石配置が 6×31 q=5 の行欠損極大安全witnessであることを3系統の独立検証で確定し、
**M_{6,5} ∈ [32,658]** とした（下界のみの更新・上界 T=658 不変・mwq_stabilization.csv は K1201 前例により不変）。

- **witness**: maxx=25・rows [4,4,4,4,4,3]・free_append_reach=31・first_unblocked [31,5]。
  同一石集合は witness_widths **[26,31]**、すなわち単一集合で幅26..31の6連続 staircase
  （(6,5) の単一集合最幅広記録。従来は L2 自身の幅域と c008 の [26,30]）。
- **検証**: (a) surgery_gen.js（整数正準曲線鍵）WITNESS_OK・(b) det_q_verify.py（det3/det4）safe+maximal_at_m
  （163空点全blocked）・(c) append_criterion.py（Fraction・出版pin byte一致）old_uncovered 0・の3系統で PASS。
  tamper対照2種は全系統 FAIL（1つは maxcirc 5 で unsafe を直接可視化）・5同行制御 FAIL・
  出版 L2 6×30 witness の陽性対照 WITNESS_OK・2回実行 byte 一致。
- **純並進census**: 公開 m≤30 プール（15 iso-config・D4像込み）の全 offset（maxw=50）で band top は
  c009（L2）の31のみ。複数の先行配置（c008 [26,30] 等）を含め reach≥32 の配置は皆無（限定観察・不在主張なし）。
- **6×32 frontier**: 165配置の unblocked census で unblocked≤3 の24 base を選び
  r0s/r1a1/r2a1/r3a1/r4a1（完全）を24 base 全てで、t2（rem3add2・targeted-complete）を
  c009@off3 で完走（D-set 74・9,731 pair×1,771 removals=17,233,201 候補）。すべて0 witness。
  **6×32 は UNDETERMINED**（編集近傍の限定陰性・k≤4R≤1A+3R2A 近傍外の witness を排除しない）。
  残り23 base の t2 は checkpoint で resume 可能。
- K0815 第5弾の「6×31 r≤5 探索 0件」との関係: 同探索は第5弾時点のプール（L2 未発見）相対であり、
  L2 発見後の純並進は未走査だった。本結果と矛盾しない。
- 標準 11×11 空盤・二石root・S2・class 1/2/4 は本レーン非接触で UNKNOWN のまま。
  checked/candidate 数は勝敗ではない。
