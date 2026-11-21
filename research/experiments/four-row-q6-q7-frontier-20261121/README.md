# Four-row (w=4) q=6 / q=7 frontier — 2026-11-21

w=4 の q=6・q=7 は repo 内で未着手だった（q=4,5 は four-six-row band-extension レーン、q=8 は解決済み M_{4,8}=11、q≥9 は trivial K0025）。本実験はこの 2 本を初期掃引した。

## 主張（有限機械証明として正確に）

安定化長 M_{4,q} := least m0 such that P(m) ∀ m ≥ m0、ただし P(m) ⟺ def-mode UNSAT（行欠損極大安全配置の非存在）∧ capacity 配置の存在。

- **(4,m,7)**: witness band m=7..12（各行 ≤6・最小行 5・3系統検証 PASS）、witness-free band **m=13..88**（sat2.js census 13..85 + genfast3 census 86..88、全幅完全 UNSAT）。capacity 配置 m=13 と m=16 で SAT（24石、全行 6、3系統 capacity 検証 PASS）。よって有限掃引のみからは **M_{4,7} = 13 または M_{4,7} ≥ 89**。さらに証明済み一般上界 M_{4,7} ≤ U_{4,7} = 81（K0318・三つ組充填定理）と組み合わせると帯 [13,85] の有限排除と [81,∞) の解析上界が全幅 m ≥ 13 を被覆し、**M_{4,7} = 13 が閉じる**（下界は m=12 witness。後続 closure レーン K1182・K0077/K0071 と同一の「解析上界＋有限排除＋下界証人」パターン）。
- **(4,m,6)**: witness band m=6..15（最小行 4）、witness-free band **m=16..29**（全幅完全 UNSAT、conflicts 1.4M〜3.7M）。capacity 配置 m=16 SAT（20石、全行 5、3系統 capacity 検証 PASS）。よって **M_{4,6} = 16 または M_{4,6} ≥ 30**。上界の引用値: U_{4,6} = 103（K0318 thresholds JSON・packing_U）⇒ M_{4,6} = 16 or ∈ [30,103]。
- 境界幅の交差エンコーディング確認: (4,16,6) と (4,13,7) の def-mode + `--lex=H`（シンボリック LE を lexLeader 制約付きで再符号化）が双方 UNSAT。符号化独立性の信頼性追加。closure レーンが (4,86,7) の `--lex=H` 交差符号化も UNSAT（conflicts 3677）で追加確認した。
- **band extension（同日追い込み、commit参照）**: q=7 を m=73..85（13幅・すべて UNSAT・conflicts 2.8k..5.6k・0.13..0.21s）、q=6 を m=28..29（2幅・ともに UNSAT・2.46M/2.45M conflicts・140s/幅）へ延伸。q=7 の m=86 は sat2.js census 符号化のメモリ壁（生成段階 OOM・INDET ではなく符号化資源上限）だった。q=6 m=30 以降は未掃引。
- **closure band extension（closure レーン・genfast3 移植、commit参照）**: sat2.js のメモリ壁の先 q=7 m=86..88（3幅）を genfast3.js 弦対抽象円 census（six-row-q8-band-closure レーンから byte-identical 移植・md5 12c2bd9c…、q ≥ w+2 の完全性論は K1134 レーンで確立済み）で掃引。すべて UNSAT（conflicts 5930/5191/6072・0.16..0.23s/幅・rc=20）。低帯較正として (4,13,7)・(4,20,7)・(4,16,6)・(4,85,7) の CNF が sat2.js 出版値と byte 一致（md5 80663be5/6f882012/3ce3a8fa/2f78307d）、pinned kissat の conflicts も bit-exact（5446/3359/1980648/3759）。詳細は closure 実験 dir（research/experiments/four-row-q7-stabilization-closure-20261121/）と K1182。

## 観察（予想として記録・未証明）

- q=7 の witness-free UNSAT は幅にほぼ非依存（conflicts ~1000-6300、0.04-0.23s）。局所障害（有限窓引数）によって全幅で成り立つ可能性があり、M_{4,7}=13 は K0318×K1177 の結合で確定したが、これを置き換える自己完結的なブロッキング計数証明は依然として有力な定式化候補として残る。
- q=6 の UNSAT は幅とともに困難化（conflicts h→3.7M、220s/幅）。同様の局所障害は確認されておらず、延伸は追加計算資源を要する。M_{4,6} は [30,103] の掃引か解析的排除で残り 74 幅を処理すれば U_{4,6}=103 と組み合わせて閉じる（q=6 は q ≥ w+2 = 6 を満たすため genfast3 census が符号化に使用できる）。

## 再現方法

```
KISSAT_BIN=<path-to-kissat-4.0.4> node runner.js sweep <q> <mStart> <mMax> <capSec> <budgetSec>
KISSAT_BIN=... node runner.js lexdef <q> <m> 0 <capSec>
KISSAT_BIN=... node runner.js cap <q> <m> <capSec>
```

- runner.js は records.jsonl append-only（tag 重複で skip）。
- m ≥ 86（q=7）の genfast3 生成は closure 実験 dir の scripts/genfast3.js（md5 12c2bd9c…・`SEVEN_SCRIPTS` 参照・core は本 dir sat2.js と同一 md5）。append_records.js（closure dir）が本 dir の records.jsonl 形式で 4 レコードを追記した。
- 検証系統: sat.js verifyConfig（JS、安全+極大）、verify_witness.py（Python、`--capacity` モード追加）、verify3.py（Python、全候補部分集合ベース、`--capacity` モード追加）。witness は 3 系統、capacity 配置は 3 系統 capacity セマンティクス（安全+極大+全行 q−1）で PASS を要求。
- 較正: pinned kissat で (6,16,6) 陽性対照を再現（CNF md5 `22dd41bae3f338713c8ed866b9a28f8e`、conflicts 46 bit-exact）。

## ファイル

- `scripts/sat.js` — K0810 core（census、verifyConfig）。md5 `0cc6021a4e523a0d7f4d5ea0f5f5d40c`
- `scripts/sat2.js` — def-mode/rowY/lex/totalizer エンコーダ。md5 `282ae832efa0080127c6c153e65e1c3c`
- `scripts/sat5.js` — capacity 符号化（core + 全行 ≥ q−1 unit）
- `scripts/verify3.py` — 第 3 検証器（census 非依存・全候補列挙）
- `scripts/verify_witness.py` — 第 2 検証器（`--capacity` モード付き）
- `scripts/runner.js` — sweep/lexdef/rowfixed/cap オーケストレータ
- `output/records.jsonl` — 112 インスタンス記録（初期掃引 93 + band extension 15 + closure band extension 4）
- `output/witnesses/*.json` — witness（q=6 10個、q=7 6個）と capacity 配置（4個）

## 次の作業（レジューム情報・closure extension 後）

- q=7: **M_{4,7}=13 で閉鎖**（K1182。この dir の有限掃引 13..88 は [13,85] の証拠と壁の先の直接確認を担い、[81,∞) は K0318 定理が担う）。残る自由課題は自己完結的ブロッキング計数証明（M の値を変えないが証明の独立性を高める）。
- q=6: m=30 以降の掃引（外挿 ~140-250s/幅・`NODE_OPTIONS=--max-old-space-size=2048` 必須化の見込み。q=6 は q ≥ w+2 なので genfast3 census で生成資源を削減できる可能性が高い）。witness-free band が m=103 まで伸びれば U_{4,6}=103 と組み合わせて M_{4,6}=16 が閉じる。

$$
M_{4,6} = 16 \text{ or } \in [30,103] \qquad M_{4,7} = 13 \text{ (closed)}
$$
