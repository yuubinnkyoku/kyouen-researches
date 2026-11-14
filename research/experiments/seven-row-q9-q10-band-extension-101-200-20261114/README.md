# seven-row-q9-q10-band-extension-101-200-20261114

継続レーン: K0820 の (7,9)/(7,10) witness-free 帯 24..100 / 19..100 を m=101 以降へ延長する。
`research/experiments/seven-row-q9-q10-bands-20261114/` の実験と同一の符号化・ソルバ
（genfast.js CNF — K0820 で sat2.js とバイト一致検証済み — + kissat 4.0.4 official binary）を使い、
def 単一節（∃行欠損極大）完全符号化インスタンスを各幅で解く。UNSAT ⟹ その幅に行欠損極大安全配置は存在しない。

## 手法（source 実験と同一・生成器のみ高速化）

- CNF: `scripts/genfast2.js`（m=119 以降。K0820 の `scripts/genfast.js` の整数キー高速版。
  (v,ρ) 正規化をgcdなしの正準整数キー (N480,RHO)=(480v, 921600ρ²) と typed-array open addressing に置換し、
  census・順序・dedup・CNF エンコーディングは sat2.js をそのまま再利用。
  **4サンプル（7×25 q8 --rowY=2 / 7×101 q9 / 7×110 q10 --lex / 8×26 q9）で genfast.js とバイト一致検証済み**
  — `scripts/controls_byteid.json` 参照。~10.7x 高速（m=101 で 21.4s → 2.0s）。q≥w+1 限定は不変。
  m=118 以前の record は genfast.js 生成（`"generator"` フィールドで区別））。
- ソルバ: kissat 4.0.4 official linux-amd64（未変更・200s cap）。
- 記録: 各幅ごとに `output/q{9,10}-band/records.jsonl` に JSONL、生ログは同 dir の `s7xMqQ_none.kissat.txt`。
  CNF は決定的に再生成可能なため保存しない（source 実験と同じ方針）。
- batch 実行: `scripts/batchband.sh`（コンテナの ~290s hard stop を避ける wall guard 付き・幅ごとに記録。

## 較正（instance identity）

- (7,100,10) def-none 再生成 CNF: kissat UNSAT **2,388 conflicts** — source q10-band record と bit-exact
  （vars 17615 / clauses 64064 / curves 193 も一致）。`output/controls/`。
- genfast2.js ↔ genfast.js CNF バイト一致 4 サンプル: `scripts/controls_byteid.json`
  （q8 --rowY / q9 / q10 --lex / w=8 をカバー）。

## このコミット時点の結果

- (7,9): m=101..184 全幅 **UNSAT**（m=101..118 は genfast.js、m=119..184 は genfast2.js 生成。
  conflicts 6.9k..27.5k・200s cap 内で全幅完走、INDET なし）。
- (7,10): m=101..110 全幅 **UNSAT**（conflicts 1.5k..3.7k・本レーン分）。
- 継続中（(7,9) m=185.. 以降は後続バッチで追記）。SAT 発見時は witness dual-verify を記録。

## スコープ

有限機検証（census 完全性と kissat 正確性まで）。各幅の UNSAT はその幅の非存在の完全証明（符号化完全性に依存）。
m の未掃引区間の持続性は主張しない。M_{7,9} ∈ {24} ∪ [185,613] / M_{7,10} ∈ {19} ∪ [111,587] が本コミット時点の帰結。
