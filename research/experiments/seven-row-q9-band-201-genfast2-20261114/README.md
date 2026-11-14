# seven-row-q9-band-201-genfast2-20261114

継続レーン: K0820 (7,9) witness-free 帯 24..200（m=101..200 は `seven-row-q9-q10-band-extension-101-200-20261114`）を m=201 以降へ延長する目的で開始した。作業中に並走レーンが **genfast3.js による帯閉鎖 201..612**（`seven-row-q9-band-extension-201-612-20261114`・IN FLIGHT claim・commit d06d8015・O(C(w,2)·m²·w) 弦対census）を開始したため、本実験は **m=201..237 の独立 genfast2 記録**として役割を確定し、掃引は 237 で停止した（重複掃引の回避）。

## 手法（101-200 レーンと同一）

- CNF: `scripts/genfast2.js`（整数キー (N480,RHO) 高速版。sat2.js との CNF バイト一致は元レーンの controls_byteid.json で 4 サンプル検証済み・census/順序/dedup/符号化は sat2.js を verbatim 再利用）
- ソルバ: kissat 4.0.4 official linux-amd64（未変更・200s cap）
- 実行: `scripts/leanband.sh`（1幅ごとに JSONL record + kissat 生ログ + meta・CNFは決定的再生成可能なため保存しない）+ `scripts/batchband.sh`（wall guard 付き連続実行・GUARD_STOP で幅単位永続）
- 較正（instance identity）: (7,9) m=200 再生成 → vars 34592 / clauses 125765 / curves 393 / **UNSAT 24,369 conflicts** — 元レーンの record と bit-exact（`output/controls/`）。

## このコミット時点の結果

- **m=201..237 全幅 UNSAT**（37幅・conflicts 14,082..28,265 の範囲・200s cap 内で全幅完走・INDET なし・生成はすべて genfast2）。
- 帰結（本実験単独）: witness-free 帯は **{24..237}** を含む → **M_{7,9} ∈ {24} ∪ [238,613]**（上界 613 は K0318 substitution）。
- **役割**: genfast3 閉鎖レーン（201..612）の幅 201..237 に対する**独立実装交叉検証**。genfast2 ↔ genfast3 は対照サンプル（7×101/110lex/150/200 他 13 サンプル・controls_genfast3.json）で CNF バイト一致が検証済みのため、閉鎖レーンの records.jsonl の conflicts が本実験の37幅と全幅一致すれば、新生成器の大規模掃引での正しさの独立傍証になる（不一致があれば早期に検出できる）。

## スコープ

有限機検証（census 完全性と kissat 正確性まで）。各幅の UNSAT はその幅の行欠損極大安全配置の非存在の完全証明（符号化完全性に依存）。未掃引区間（m ≥ 238）の持続性は主張しない。
