# n11-residual72-36witness-sweep-prep-independent-audit-20261120

36 fresh-witness depth-10掃引（`n11-residual72-36witness-depth10-sweep-20261120`・掃引オーナー宣言済み・実行中）に向けて2026-11-19T22:14:15Zに出版された**準備コミット `53b07ebe1647b2c966af098897290df243ba0d19`** の成果物一式を、publication-firstで独立監査した結果。単一オーナー宣言ノートは `research/log/2026-11-20-n11-36witness-sweep-prep-independent-audit-single-owner-note.md`（commit 18ec5f76）。

**目的**: 掃引オーナー環境で72 probe（最大72×280秒）が完走した後に `assemble.py` のgateが入力ピンの食い違いで失敗し、計算が流失するリスクを、実行前に独立機械で排除すること。出版済みレコードのみを入力とし、新規の探索・掃引・判定・証明書抽出・receipt fold・行の閉鎖は一切行っていない。

## 入力の固定（すべて出版済み）

- K1075候補供給正本 `research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json`（SHA-256 `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`）
- prepコミット 53b07ebe16 の `roots.json`（SHA-256 `3904041ea40c4e7c419d437046358eac7b91d169782e8d64abac0c9b044f160f`）・`residual72.json`（SHA-256 `78e3ee7a8092dbca23fa3bf41491fdc666ba73a2e62c23f3da7570430bf28f9b`）・`runner_v17.ts`（git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）・`prepare_roots.py`・`driver.py`・`assemble.py`
- repo原本 runner v17 `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/class4_child1_runner_v17.ts`

## 結果（40/40 gate PASS）

正本: `output/sweep-prep-independent-audit-20261120.json`（SHA-256 `e89fbe72ff8f8713cdc0d9cfedd37886e0a43d9750e5337109af269e3c622d6c`）

1. **独立再導出がbyte-exact**: 本レーンが独自に書いたD4実装（手計算で検証した4個のunit self-test込み。角対・中心・L字・回転合成）により、K1075正本の `witness_full`・`residual_row_hex` から36根（root・child・bit・rows・safe）と72行を再導出し、出版済み `roots.json`・`residual72.json` を `json.dumps(indent=1)+"\n"` で直列化した結果が**出版bytesと完全一致**（gate `byteequal-roots-json`・`byteequal-residual72-json`）。
2. **exact 1-coverの独立再確認**: 36根×2行の72被覆が残余72行と集合等価で、全行ちょうど1回、`row_demand` 72行と一致、両替えなし。D4削除軌道は36根すべてが7要素（衝突なし、`orbit_sizes {7:36}`）。
3. **assemble.py 3ピンの活性証明**: `roots.json` SHA（3904041e…）・`residual72.json` SHA（78e3ee7a…）・runner git blob（c132cc64…）がいずれも実在ファイルと一致 → 掃引完走後のgate群は入力側で落ちない。
4. **runner v17固定コピーの同一byte**: prepコピーとrepo原本がbyte-identical、自前計算git blob SHA-1がピンと一致。
5. **driver.py静的整合**: `roots[W::4]`分割が36根を9×4で非交差完全分割、(root, ordering) 72キーの一意性、cap 30M均一・timeout 280秒、resume述語がassembleのok-record述語と同一、argvフラグ集合がrunner側解析器と過不足一致、`andclose` 適用閾値 d≥8 で depth 10 の両モードが有効、interpretation guard（cappedは無証拠・REFUTED-D10非LOSS）が両機械に存在。
6. **runner interface 実行smoke test（cap 2000で非判定）**: `node --experimental-strip-types` で実際に起動し、pilot_d6制御が `{pilot_d6, loss=false, nodes=3402, capped=false}` に厳密一致、両順序でcapped micro-probe（nodes=2001・capped=true・loss=false）が確定的、1行制御+1行結果のJSONL形式がdriverの解析と整合。capped結果はどの方向の証拠でもない。

3回実行（同一cwd 2回+別cwd別プロセス1回・再生成含む）で正本byte-identical。

## 再現手順

```sh
python3 scripts/audit_sweep_prep_20261120.py   # repo-root相対で入力を解決、全pin fail-closed
```

出力は `output/sweep-prep-independent-audit-20261120.json`。`--no-smoke` でnode実行smokeのみ省略（残りの39 gateは不変）。

## 解釈境界

- 本監査は掃引の入力整合・機械整合の確認であり、**掃引結果には踏み込まない**。60のgateは全てprep時点の静的・幾何・ピン照合である。
- smoke testのcapped結果は証拠ではない。REFUTED-D10はLOSS証明ではなく、WIN7-D10は証明書抽出候補に過ぎない。
- 標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4 は **UNKNOWNのまま**。
