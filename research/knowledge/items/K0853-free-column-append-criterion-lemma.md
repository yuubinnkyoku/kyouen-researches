---
id: K0853
title: "自由列追加判定補題: 石集合の安全性は幅非依存・極大性は新列のブロック条件と同値・到達幅 R(S) まで witness 帯が無料延伸される"
kind: proposition
status: proved
topics: [geometry, rectangles]
aliases: []
scope: "任意の行数 w・点数 q ≥ 2・行 0..w-1 の有限石集合 S。S が幅 m0 で safe+maximal なら、同一石集合は max_x(S) より右で最初の非ブロックセルを含む列 R(S)（なければ無限）までの全幅 m0 ≤ m' ≤ R(S) で safe+maximal であり、m' > R(S) では極大でない。行石数は不変なので行欠損 witness はこの全区間の witness。R(S) より先の witness 有無には何も言わない。"
evidence: "全称数学的証明: (1) 禁止配置（q 石の共線/共円）は石集合のみで決まり盤幅に依存しない。(2) 空点 c の blocked 判定（c を通る曲線が S の石をちょうど q-1 個含む）は (S,c) のみで決まり、旧列のブロック状態は幅不変。極大性の定義とこの幅不変性から到達幅 R(S) の主張が従う。独立 Fraction 実装（scripts/append_criterion.py）が published 構成 witness 3件を全て機械再現: (6,4) m=46 witness は R=46・停止 (46,0)（published 記録と一致）・同一17石が幅40..46 の witness、(4,4) m=32 witness は R=33・停止 (33,2)、(4,4) m=34（+1シフト）は R=34・停止 (34,2)。陰性対照2件（石移動 → unsafe/非極大）正検出・2回実行 byte-identical。"
relations:
- type: verifies
  target: K0833
  note: "(6,4) m=46 構成 witness の純TS検証に続き js+py 2系統検証を完遂（保留項目の解消）。(4,4) m=33/34 構成延伸・(6,4) m=45→46 延伸とその停止幅が補題で統一的に説明される。"
- type: depends_on
  target: K0026
  note: 極大性の定義（全空点で石を置くと禁止配置が生じること）
artifacts:
- path: research/experiments/free-column-append-criterion-20261115/README.md
  role: proof
  note: "補題の定式化・証明・3 witness 一致表・陰性対照・(6,4) m=46 js+py 検証完遂の記録。"
- path: research/experiments/free-column-append-criterion-20261115/scripts/append_criterion.py
  role: verifier
  note: "独立 Fraction 実装。blocking 直線は (c,s) 族・blocking 円は石三つ組族の完全列挙。初版の円係数右辺 -(f2-f1)/2 バグを verify_witness.py との不一致で発見・修正（/2 は中点形式と中心 a=-D/2 で打ち消し合う）。"
- path: research/experiments/free-column-append-criterion-20261115/output/criterion-6x4-m46-witness.json
  role: data
  note: "(6,4) m=46 witness: R=46・停止 (46,0)・witness_widths [40,46]・2回実行 byte-identical。"
- path: research/experiments/free-column-append-criterion-20261115/output/criterion-4x4-m32-witness.json
  role: data
  note: "(4,4) m=32 witness: R=33・停止 (33,2)。m=33 off=0 延伸の根拠と m=34 でシフトが必要な理由。"
- path: research/experiments/free-column-append-criterion-20261115/output/criterion-4x4-m34-witness.json
  role: data
  note: "(4,4) m=34 witness (+1 シフト): R=34・停止 (34,2)。前線が m=35 である理由。"
- path: research/experiments/free-column-append-criterion-20261115/output/criterion-6x4-m46-neg1.json
  role: data
  note: "陰性対照1: 石 (21,0)→(22,0) で 4石円生成（unsafe 検出）。"
- path: research/experiments/free-column-append-criterion-20261115/output/criterion-6x4-m46-neg2.json
  role: data
  note: "陰性対照2: 石 (21,0)→(23,0) で safe だが旧列3セル非ブロック（非極大検出）。"
- path: research/experiments/free-column-append-criterion-20261115/output/m46-js-py-verification-20261115.json
  role: data
  note: "(6,4) m=46 witness の js (sat.js verifyConfig) + py (verify_witness.py Fraction) 両系統 PASS・(6,45,4) 同一石も PASS・4石行直線の陰性対照棄却。K0833 の保留検証を完遂。"
- path: research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w6-construct-m46/verify-js-py-20261115.json
  role: data
  note: "構成レーンの output に置いた同一検証記録（保留検証の完遂を現場でも確認可能にするための新規ファイル・既存 records.jsonl は不変）。"
- path: research/log/2026-11-15-free-column-append-criterion.md
  role: log
  note: "定式化の動機・円係数バグの発見経緯・3 witness 一致・各 band レーンへの適用指針。"
---

## 補題（全称・証明済み）

w, q ≥ 2 とし、S は行座標が 0..w−1 に入る有限の石集合、
max_x = max{x : (x,y) ∈ S} とする。幅 m の盤 B(m) = {0..m−1}×{0..w−1}。

**定義**: 空点 c（c ∉ S）が *blocked* であるとは、c を通る直線または円で
S の石を q−1 個以上含むものが存在すること（S が safe なら
全曲線の石数 ≤ q−1 なので「ちょうど q−1」と同値）。
**到達幅** R(S) = max_x より右で非 blocked セルを含む最初の列
（存在しなければ ∞）。

1. **安全性は幅非依存**: S が safe なら同一石集合は任意の幅 m' > max_x で safe。
2. **極大性判定**: S が幅 m0 (> max_x) で safe+maximal なら、
   すべての m0 ≤ m' ≤ R(S) で safe+maximal、
   すべての m' > R(S) で maximal ではない。

**証明**:
(1) 禁止配置は「q 石が共線または共円」という石集合だけの性質で、
盤の幅は（石の位置が m' 内に収まる限り）関与しない。
(2) 極大性とは「B(m') の全空点が blocked」こと。blocked は
「c を通る曲線 ∩ S が q−1 石以上」という (S, c) のみの関数で、
曲線は盤で切断されないため盤幅に依存しない。よって列 0..max_x
（旧列）の blocked 状態はどの幅でも同じで、幅 m' の判定は新列
max_x+1..m'−1 の blocked のみに依存する。R(S) の定義より、
m' ≤ R(S) なら新列は全て blocked、m' > R(S) なら列 R(S) に
非 blocked セル（追加しても安全な点）があり極大性が壊れる。□

**系（witness 帯の無料延伸）**: 行欠損極大 witness S（幅 m0）に対し
R(S) ≥ m0+1 なら、幅 m0..R(S) の全てが同一石集合で witness。
行石数は幅によらず不変なので欠損性も保存される。
R(S)+1 が次の真の前線であり、それを超える延伸は
新しい石配置（シフト・surgery・SAT）を必要とする。

## 機械検証（published 構成 witness との完全一致）

独立実装 `append_criterion.py`（純 Python Fraction・候補族完全列挙:
blocking 直線は (c, s) 族、blocking 円は石三つ組族）:

- (6,4) m=46 構成 witness（17石・rows [2,3,3,3,3,3]・maxx=39）:
  safe（maxline=3・maxcirc=3）・R=46・停止セル (46,0)。
  published 記録「free append は m=47 で停止・(46,0) uncovered」と一致。
  **同一17石が幅 40..46 の 7 幅すべてで witness**（witness_widths [40,46]）。
- (4,4) m=32 witness（11石・maxx=26）: R=33・停止 (33,2)。
  m=33 off=0 延伸の根拠・m=34 でシフトが必要な理由を補題が説明。
- (4,4) m=34 witness（m=32 の +1 シフト・maxx=27）: R=34・停止 (34,2)。
  前線 m=35 が真の前線である理由と一致。
- 陰性対照: 石 (21,0)→(22,0) は unsafe（4石円）・(23,0) は
  safe だが旧列 3 セル非ブロック（非極大）。いずれも正しく棄却。
- 決定性: 同一入力 2 回実行 byte-identical。

## (6,4) m=46 witness の js+py 検証完遂（K0833 保留項目の解消）

K0833 の (6,4) m=46 構成 witness は純TS 第3系統のみで検証済みで、
js+py 2系統検証が bash 環境復旧待ちだった。本項目で完遂:

- js: sat.js verifyConfig(6,46,4) ok（size 17・minRow 2）。
  同一石の (6,45,4)（ソース witness）も ok。
- py: verify_witness.py (6,46,4) ok:true・(6,45,4) ok:true。
- 陰性対照（4石の行直線）は両系統で unsafe-line 棄却。

**4系統検証**（純TS/BigInt・js・py・criterion）で
witness 帯 m=6..46・M_{6,4} ∈ [47, 1113] が確定している。

## 限界

- R(S) を超える幅の witness 有無には一切言及しない（不在主張ではない）。
- シフト延伸は平行移動で blocked 状態が随伴する同型（別インスタンスとして走査）。
- 補題自体は自明に近いが、これまで per-instance 全盤走査で実施していた
  延伸可否判定を「石集合に対する1回の列走査」に縮約し、
  停止セルの位置まで予測する点が新しい。
