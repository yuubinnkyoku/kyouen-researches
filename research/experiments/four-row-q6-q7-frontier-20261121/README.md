# Four-row (w=4) q=6 / q=7 frontier — 2026-11-21

w=4 の q=6・q=7 は repo 内で未着手だった（q=4,5 は four-six-row band-extension レーン、q=8 は解決済み M_{4,8}=11、q≥9 は trivial K0025）。本実験はこの 2 本を初期掃引した。

## 主張（有限機械証明として正確に）

安定化長 M_{4,q} := least m0 such that P(m) ∀ m ≥ m0、ただし P(m) ⟺ def-mode UNSAT（行欠損極大安全配置の非存在）∧ capacity 配置の存在。

- **(4,m,7)**: witness band m=7..12（各行 ≤6・最小行 5・3系統検証 PASS）、witness-free band **m=13..85**（全幅完全 UNSAT）。capacity 配置 m=13 と m=16 で SAT（24石、全行 6、3系統 capacity 検証 PASS）。capacity の m 単調性（同じ石集合はより広い盤でも安全・極大）と合わせ、**M_{4,7} = 13 または M_{4,7} ≥ 86**。
- **(4,m,6)**: witness band m=6..15（最小行 4）、witness-free band **m=16..29**（全幅完全 UNSAT、conflicts 1.4M〜3.7M）。capacity 配置 m=16 SAT（20石、全行 5、3系統 capacity 検証 PASS）。よって **M_{4,6} = 16 または M_{4,6} ≥ 30**。上界の引用値: U_{4,6} = 103（K0318 thresholds JSON・packing_U）。
- 境界幅の交差エンコーディング確認: (4,16,6) と (4,13,7) の def-mode + `--lex=H`（シンボリック LE を lexLeader 制約付きで再符号化）が双方 UNSAT。符号化独立性の信頼性追加。
- **band extension（同日追い込み、commit参照）**: q=7 を m=73..85（13幅・すべて UNSAT・conflicts 2.8k..5.6k・0.13..0.21s）、q=6 を m=28..29（2幅・ともに UNSAT・2.46M/2.45M conflicts・140s/幅）へ延伸。q=7 の m=86 は sat2.js census 符号化のメモリ壁（生成段階 OOM・INDET ではなく符号化資源上限。kissat 判定は得られていない）。q=6 m=30 以降は未掃引。

## 観察（予想として記録・未証明）

- q=7 の witness-free UNSAT は幅にほぼ非依存（conflicts ~1000-3000、0.04-0.13s）。局所障害（有限窓引数）によって全幅で成り立つ可能性があり、**M_{4,7}=13 は全称予想**として指定可能。ブロッキング計数（欠損行の空マスすべてを塞ぐには q−1=6 石を含む直線・円が必要で、石数 ≤23 の制約下で m≥13 では不足する、という類の計数）が証明候補。
- q=6 の UNSAT は幅とともに困難化（conflicts h→3.7M、220s/幅）。同様の局所障害は確認されておらず、延伸は追加計算資源を要する。

## 再現方法

```
KISSAT_BIN=<path-to-kissat-4.0.4> node runner.js sweep <q> <mStart> <mMax> <capSec> <budgetSec>
KISSAT_BIN=... node runner.js lexdef <q> <m> 0 <capSec>
KISSAT_BIN=... node runner.js cap <q> <m> <capSec>
```

- runner.js は records.jsonl append-only（tag 重複で skip）。
- 検証系統: sat.js verifyConfig（JS、安全+極大）、verify_witness.py（Python、`--capacity` モード追加）、verify3.py（Python、全候補部分集合ベース、`--capacity` モード追加）。witness は 3 系統、capacity 配置は 3 系統 capacity セマンティクス（安全+極大+全行 q−1）で PASS を要求。
- 較正: pinned kissat で (6,16,6) 陽性対照を再現（CNF md5 `22dd41bae3f338713c8ed866b9a28f8e`、conflicts 46 bit-exact）。

## ファイル

- `scripts/sat.js` — K0810 core（census、verifyConfig）。md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`
- `scripts/sat2.js` — def-mode/rowY/lex/totalizer エンコーダ。md5 `282ae832efa0080127c6c153e65e1c3c`
- `scripts/sat5.js` — capacity 符号化（core + 全行 ≥ q−1 unit）
- `scripts/verify3.py` — 第 3 検証器（census 非依存・全候補列挙）
- `scripts/verify_witness.py` — 第 2 検証器（`--capacity` モード付き）
- `scripts/runner.js` — sweep/lexdef/rowfixed/cap オーケストレータ
- `output/records.jsonl` — 108 インスタンス記録（初期掃引 93 + band extension 15）
- `output/witnesses/*.json` — witness（q=6 10個、q=7 6個）と capacity 配置（4個）

## 次の作業（レジューム情報・band extension 後）

- q=6: m=30 以降の掃引（外挿 ~140-200s/幅・`NODE_OPTIONS=--max-old-space-size=2048` 必須化の見込み）。witness-free band がさらに伸びれば主張の m ≥ 30 部分を改善。
- q=7: m=86 は sat2.js の全三つ組 census が生成段階でメモリ上限に到達（kissat 判定なし・INDET ではない）。 Six-row lane の genfast3.js 型の弦対抽象円 census（q ≥ w+2 で完全性論つき・K1134 レーンで確立済み）を w=4 q=7 に移植すれば突破可能。
- 予想 M_{4,7}=13 の全称証明（ブロッキング計数の定式化）は継続課題。当面は延伸掃引で支持を積む。

$$
M_{4,6} = 16 \text{ or } \ge 30 \qquad M_{4,7} = 13 \text{ or } \ge 86
$$
