# seven-row-q5-m38-class-split-20261120

高速レーン。**IN FLIGHT claim (2026-11-20 19:0xZ) — (7,5) 前線 7×38 class {0} class-split SAT・実行中 (cap 10800s)**

## Claim

- 着手時点の境界: (7,5) witness 帯 m=5..37 (m=37 は winC surgery 構成 27 石
  rows [3,4,4,4,4,4,4]・seven-row-q5-m37-surgery-20261115)・
  **M_{7,5} ∈ [38, 1142]** (上界 K0318 substitution U=1142)・前線 7×38。
- 本レーンは **前線 7×38 の class {0} class-split SAT** を着手する
  (sat3.js --class=0・row 0 は ≤3 石・row 1..6 は exactly 4 石・単一欠損型。
  V-mirror で row 6 欠損型と同値)。
- ツール pin: sat3.js md5 d03f908ea99ba819caee2a6fbb471c1b (m30 dir と同一 blob)・
  kissat 4.0.4 md5 3a5eba830aa6008a604fcc9bbe99a325 (rel-4.0.4 asset)。
  CNF (7,38,5) class {0}: vars 288,546 / clauses 1,007,507 / md5 b050817dff84083cbffc0d68aaca4e62。
- **SAT ⟹ witness 帯 m=5..38 延伸・M_{7,5} ∈ [39, 1142]**。
  UNSAT ⟹ class {0} (row 0/6 欠損型) では 7×38 に単一欠損 witness なし
  (**7×38 全体の不在主張ではない**: ミラー非自明クラス {1},{2},{3}・
  深欠損型・3 編集以上 surgery・別 seed が残る)。
- m=38 の既存負記録: winC 種の **2 編集 surgery 完全列挙 0 witness**
  (six-case・seven-row-q5-m38-surgery-negative-20261115・局所負)・
  free-column extension は cell (37,0) 未遮断 (one-stone-short)。
- depth 較正: (7,5) 直接 SAT は rowY=0 分割 m=32 129,923 / m=33 655,159 conflicts
  (seven-row-q5-q6-frontier-row-split / seven-row-q5-q8-sat-frontier)。
  class-split としては q=6 で m=29 3,074,703 / m=30 2,670,296 conflicts (K0827)。
  **(7,5) m=38 の直接 SAT は初評価** (過去 record なし・cap 内決着は保証外)。

## 手法・運用

- 生成は決定的 (同一引数 → 同一 md5)。cap 内完了なら conflicts は bit-exact 再現可能。
- SAT 時の witness は 3 系統検証 (sat.js verifyConfig・verify_witness.py Python
  Fraction・verify_witness_det.js 純整数 4×4 行列式) + 負対照 (1 石除去摂動の
  非極大検出) を要求する。sat3.js decode は >65k 変数で overflow するため
  モデル復号は parse_model.py (独立 Python パーサ) で実施。
- records.jsonl に 1 インスタンス 1 record 増分追記・resumable (m32 dir の
  run_one.sh と同一構造)。

## Not claimed

- 7×38 全体の不在 (class {0} の UNSAT は不在主張ではない)・7×39 以降、
  (7,q≠5) 家族、Grundy 値、(7,4) 幅60 はいずれも本 dir の対象外。

## files

- `run_one.sh` — 単一インスタンス runner (m32 dir と同一構造・KS path 環境差し替え済み)。
- `scripts/` — sat.js/sat2.js/sat3.js/verify_witness.py/verify_witness_det.js
  (m30 dir pin と同一 blob)・parse_model.py (m31 dir pin と同一 blob c1cef8f8…)。
- 結果は本 dir の records.jsonl・output/ と K0827 へ追記して反映する。
