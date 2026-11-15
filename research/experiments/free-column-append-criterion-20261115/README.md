# free-column-append-criterion-20261115 — 自由列追加判定補題（K0853）の実装・検証

高速レーン 2026-11-15。(6,4) m=46 構成 witness に記録されていた
「js+py 2系統検証は bash 環境復旧後に実施予定」を完遂し、その過程で
各レーンが ad hoc に使ってきた「空列追加/シフトによる witness 帯延伸」を
**一般補題として定式化・機械検証**した。

## 補題（K0853・全称証明）

S を行 0..w−1 に含まれる有限石集合、q ≥ 2、max_x = max{x : (x,y) ∈ S} とする。

1. **安全性は幅非依存**: S に q 点共線/共円がなければ、同一石集合は
   任意の幅 m' > max_x の盤でも safe（禁止配置は石集合のみで決まる）。
2. **極大性判定**: 空点 c が *blocked* ⟺ c を通る直線または円で
   S の石を ≥ q−1 個含むものが存在（S が safe ならちょうど q−1）。
   blocked は (S, c) のみで決まり盤幅に依存しない。よって S が幅 m0 で
   safe+maximal なら、**自由列追加到達幅 R(S)**（max_x より右で最初に
   非blocked セルを含む列。なければ ∞）に対して
   **すべての幅 m0 ≤ m' ≤ R(S) で safe+maximal が保たれ、m' > R(S) では
   極大でない**。行石数は不変なので行欠損 witness は幅 m0..R(S) 全部の
   witness になる。

**証明**: (1) 禁止配置（q 石の共線/共円）は盤の幅に言及しない幾何的性質。
(2) 極大性の定義は「全空点が blocked」そのものであり、blocked の判定は
c を通る曲線と S の石のみに依存する（曲線は盤で切断されない）。
したがって旧列のブロック状態は幅によらず不変で、新列 max_x+1..m'−1 の
ブロック判定だけが追加される。□

系（実践的）: witness 帯延伸の際、ソルバを走らせる前に
R(S) を一度計算すれば、幅 m0+1..R(S) は**全て無料で witness 帯に加わる**。
R(S) の次の列が次の真の前線。

## 手法（scripts/append_criterion.py・独立実装）

- blocked判定は2つの候補族の完全列挙: (a) c を通る blocking 直線は
  石を ≥1 個含むので直線 (c, s) (s ∈ S) のみ、(b) blocking 円は
  ≥ q−1 ≥ 2...（q−1 ≥ 3 のとき）非共線3石で決まるので石三つ組の円のみ。
  すべて Fraction 演算・浮動小数点なし。
- 旧実装は円係数の連立一次方程式の右辺を −(f2−f1)/2 としていた
  （垂直二等分線の中点形式の /2 が中心 a=−D/2 と打ち消し合うことに
  気づかず）→ (6,4) m=46 witness のセル (40,0) で verify_witness.py
  と判定が食い違い発覚 → −(f2−f1) に修正して一致。
  **独立実装同士の不一致が片方のバグを発見した実例**として記録する。

## 結果（published 構成 witness 全部と一致・output/*.json）

| witness | safe | R(S) | 停止セル | published 記録 |
|---|---|---|---|---|
| (6,4) m=46 構成 witness（17石・maxx=39） | ✓ maxline=3/maxcirc=3 | **46** | (46,0) | 「free append は m=47 で停止・(46,0) uncovered」に一致 |
| (4,4) m=32 witness（11石・maxx=26） | ✓ | **33** | (33,2) | m=33 off=0 延伸の根拠・m=34 でシフトが必要な理由と一致 |
| (4,4) m=34 witness（= m=32 の +1 シフト） | ✓ | **34** | (34,2) | m=34 off=1 と一致・前線が m=35 である理由と一致 |

- (6,4) の同一17石集合は **幅 40..46 全て**で行欠損極大 witness
  （witness_widths [40,46]）。published の m=45→46 延伸はこの一般則の
  特殊例。1回の走査で 7 幅分の witness が確定する。
- 陰性対照 2 件: 石 (21,0) を (22,0)/(23,0) に移動 →
  (22,0) は unsafe（4石円を生成）・(23,0) は safe だが旧列 3 セル非ブロック
  （非極大）。いずれも witness_widths=[] として正しく棄却。
- 決定性: 同一入力の2回実行が byte-identical。

## (6,4) m=46 witness の js+py 2系統検証（保留項目の完遂）

K0833 の artifact note に「js+py 2系統検証は bash 環境復旧後に実施予定」
と記録されていた保留検証を実施した:

- js: sat.js verifyConfig(6,46,4) → ok（size 17・rows [2,3,3,3,3,3]・minRow 2）。
  同一石集合の (6,45,4)（m=45 ソース witness）も ok。
- py: verify_witness.py（Python Fraction・census 不使用）(6,46,4) → ok:true。
  (6,45,4) も ok:true。
- 陰性対照: 4石の行直線 [0,0],[1,0],[2,0],[3,0] が unsafe-line で棄却される
  ことを両系統で確認。
- 記録: `m46-js-py-verification-20261115.json`（構成レーンの output に新規追加）。

## files

- `scripts/append_criterion.py` — 補題判定器（独立実装・Fraction）。
- `output/criterion-*.json` — witness 3件・陰性対照2件の走査結果。
- `output/m46-js-py-verification-20261115.json` — js+py 検証記録
  （research/experiments/four-row-q4-q5-frontier-20261115/output/q4-w6-construct-m46/
  にも同一内容を配置）。

## 解釈境界

- 補題は全称だが、**R(S) の先の幅の witness 有無には何も言わない**
  （不在主張ではない）。前線は R(S)+1 から先もソルバ/構成の仕事のまま。
- シフト延伸は補題の平行移動版（平行移動で blocked 状態は随伴する）で
  本実装では別途走査する（(4,4) m=34 は +1 シフト集合として直接走査）。

## resume

- (4,5)/(4,4) 前線レーン: m=20/m=34 witness に append_criterion.py を
  走らせて R(S) を先に知ることができる（(4,4) m=34 は R=34 で停止済み・
  m=35 は新規探索が必要な理由が補題で確定）。
- 各 band-closure レーン: 新 witness を得るたびに R(S) を計算すれば
  無料延伸幅が即座にわかる。
