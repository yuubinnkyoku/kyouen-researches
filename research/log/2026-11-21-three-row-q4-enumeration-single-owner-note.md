# 単一オーナー宣言: 3行 q=4 列挙閉包レーン（m=24..27・enumeration）

- 宣言日時: 2026-11-21T07:50Z
- 宣言時 HEAD: `a8e4b0a69bd8b2b8cab5a18ea3ab6c5d9f0e58bb`（main）
- レーン: `research/experiments/three-row-q4-enumeration-20261121/`（本宣言後に出版）
- 目的: 3×m・q=4 def-mode の m=25,26,27 を含む witness-free 判定を、
  SAT 符号化とは独立な**列挙閉包**（63プロファイル完全分割:
  family 9 = wsearch34.js 構造探索 / fast 13 = dx34.js circle-class 列挙 /
  lemma 41 = crossing-supply 補題の算術キル）で機械証明し、
  既出版の m=24 P(24)（行和63分割 + pinned kissat・frontier レーン）を
  独立第二方法で再証明・二重裏付けする。
- 先行宣言の不在確認: 宣言時点の main に m≥25 を掃引した出版物なし
  （q34 frontier レーンの最新出版 c1a2a333/0cebd5ea は「m≥25 は未掃引で
  一切主張なし」が明示済み・task (a) の m=25 分割掃引着手の宣言なし）。

## 受入条件

1. **実験dir**: scripts（wsearch34.js md5 `526cf1c3…`・dx34.js md5
   `b02235a9…`・sat.js md5 `0cc6021a…`〔frontier レーンと同一 pin〕・
   closure_check.py・crossval_summary.py・verify_witness.js・witness_check.py）
   と output（掃引・交差検証・閉包台帳）を出版し、README が再現手順を明示。
2. **主張の正確な言葉遣い**: witness-free 幅 {24,25,26,27}
   （P(24) は独立第二方法再証明・P(25),P(26),P(27) は本レーンの新規確定）。
   **M_{3,4} ∈ [24,69] は不変**（M は「P(m) for all m≥m0 の最小 m0」であり、
   P(25..27) は M=24 の必要条件の一部でしかなく、下界 24 は witness band 23
   終端由来・上界 69 は K0024 由来）。**m≥28 は未掃引で一切主張なし**。
   P の幅単調性は未証明のまま。
3. **検証チェーン（全機械・出版 byte のまま再実行可能）**:
   dx34 direct ≡ brute_3x{4..8}（プロファイル毎・def総数一致・fast≠direct 0・
   m=4..12）、wsearch34 ≡ brute family（m=4..8×Y∈{0,1,2}×a∈{0,1,2} の15通り
   全精確一致）、m=23 陽性対照（Y=0:2件・Y=1:4件・Y=2:2件・2系統検証 PASS・
   出版外側行 witness wit_3x23_outer_4 と石集合 byte-exact 再発見）、
   closure_check validate（補題キルが m=4..12 の全数列挙と矛盾 0）、
   crossval_summary.json の overall PASS。
4. **既有 K 項目の同一命題更新**: K1183（3行q=4 witness band）の item を
   更新（title・claims・artifacts・scope/evidence）し、knowledge README の
   K1183 bullet を更新。新規 K 番号は採番しない（K1196 は four-row q=7 レーン
   が 07:42Z に使用済みのため衝突回避も兼ねる）。
5. **並走への配慮**: 本レーン確定後、frontier レーン task (a)（m=25 分割
   kissat 掃引）は同一結論を独立方法で確認する位置づけに変わる（衝突ではなく
   交叉検証）。records.jsonl は frontier レーンの正本のまま本レーンでは
   触れない。push 競合・HEAD 不一致が生じた場合は本レーンの残partを次回実行へ
   繰り越す（無理に押し進めない）。

以上の条件で本レーンの出版を開始する。
