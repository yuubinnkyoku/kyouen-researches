# five-row-q5-m24-class-split-20261115

高速レーン。(5,5) 前線 5×24 の class-split 攻撃として着手し、
**m=24・m=25 に連続して witness が存在したため (5,5) witness 帯の自動延伸に拡張**した。

## 結果（2026-11-15 01:2x UTC 時点・バッチ1）

- **5×24 q=5 class {0}: SAT** — 698,570 conflicts / 75.65s（kissat 4.0.4・T=250s cap の 200s wall 以前に自力完了）。
  **19石・行構成 [3,4,4,4,4] の単一欠損極大安全配置（witness）**。
  js verifyConfig（census 系）と Python Fraction（verify_witness.py・census-free 厳密幾何）の
  **2系統検証とも PASS**。→ **M_{5,5} 下界 24 → 25**。
  witness: `output/witness_5x24_c0.json`（stones は `witness_5x24_c0_stones.json`）。
- **5×25 q=5 class {0}: SAT** — 35,972 conflicts / 8.14s。
  **19石・rows [3,4,4,4,4]**。2系統検証 PASS。→ **M_{5,5} 下界 25 → 26**。
  witness: `output/witness_5x25_c0.json`。
- m=24 class {1}: INDET（200s wall cap・1,155,708 conflicts / 124.24s process）— honest negative（不在主張ではない）。
  M 下界の観点では class {0} の SAT により問題自体は解決済み（m=24 に witness が存在する）。
- witness 探索前線は **5×26** へ移動（バッチ2以降・`scripts/extend55.sh` が自動延伸中:
  class {0} plain → krow k=0..2 → k=3 × minpos 0..⌊(m−1)/2⌋ の段階的分解で SAT を探す）。

## 境界の更新

| family | 着手前 | 現在 | 上界 |
|---|---|---|---|
| (5,5) | witness 帯 m=5..23・M ∈ [24, 336] | **witness 帯 m=5..25・M ∈ [26, 336]** | K0318 U=336 |

## 手法・較正

- 生成器: sat3.js（`five-row-q7-m22-class-split-20261114/scripts/` と同一・md5 d03f908ea99ba819caee2a6fbb471c1b）。
  sat2.js md5 282ae832efa0080127c6c153e65e1c3c・sat.js md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c（
  `four-six-row-q4-q5-band-extension-20261115` README 記載の sat.js md5 と一致・機械不変）。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325・不変）。
- class-split: 欠損行集合 D（行 y の石数 ≤ q−2=3・D 外の行はちょうど q−1=4）を正準 19 クラスに割る。
  鏡像正準化（行反転 i↔4−i）により、正準代表 D のインスタンスだけを掃けば全 orbit を被覆する
  （安全性・極大性・欠損性は行鏡像不変のため）。
- **較正1（エンドツーエンド bit-exact）**: 5×23 q=5 def-mode（sat2 --deficient --lex=H,V・有効 [H,V]）
  SAT **508,466 conflicts** — 前レーン（four-six-row-q4-q5-witness-search-20261114・2026-11-14T21:06:04Z）
  の 508,466/62.9s と conflicts bit-exact・vars/clauses 31309/109366 も完全一致。
- **較正2（陽性対照）**: 5×23 class {0} SAT 200,118 conflicts / 22.12s → decode →
  19石 rows [3,4,4,4,4] verifyConfig PASS — m=23 witness を端末間で再発見。
- 予備陰性（透明性）: 最初に --class="{0}" と波括弧付きで渡した際に class [null]（全行full強制）の
  無関係インスタンスが走った（破棄・記録には含めない）。同じバグ形式は sat3.js の引数仕様
  （--class=D は D=0,1 形式）を守れば生じない。

## スコープ

有限機械検証まで。各幅の SAT はその幅の欠損極大安全配置の存在証明（witness 有限証拠）。
INDET は cap 到達であり不在を意味しない。上界（K0318 substitution U=336）は不変。

## 関連

- K0833 / four-six-row-q4-q5-witness-search-20261114（m=5..23 witness 帯・m=24 def-OR 90s/699k INDET の出典）
- four-six-row-q4-q5-band-extension-20261115（sat3/sat.js/kissat の同一機・sat2 OOM 壁の超え方）
- K0821/K0834（class-split + k×minpos 分解プロトコル・5×21/22 q=7 の完全決着例）
- K0815（(5,6)/(6,5) 等の witness 帯延伸の前例）
