# 2026-11-20 n11: resolve7（K1072）出版正本の独立第二検証（76 gate全PASS・resolve7全フィールド再現）

## 経緯

前回実行（続行11）のレジュームどおり、K1069継続レーンが残していた

1. K1072（resolve7: 残余72行のpost-fold witness再照合・published-records only）
2. K1075（残余72行fresh-safe pool cache-join候補供給再構築）

の出版を回収した。両レーンとも単一オーナー宣言ノートを先行しており、当レーンは
これらの実行そのものには着手しない。代わりに、レジュームが挙げていた
「resolve7/cache-join成果が出版された時の第二検証」のうち resolve7 分を実行した。
単一オーナー宣言ノート
（`research/log/2026-11-20-n11-resolve7-second-verification-single-owner-note.md`）
を先行出版して着手権を確定してから機械を書いた。

## 実行内容（実験: `research/experiments/n11-residual72-resolve7-second-verification-20261120/`）

resolve7の5入力（resolve6 `e85d4bfb…`・fold9 `24db2352…`・fold10 `bed7d331…`・
K1069掃引 `22953ae1…`・sv17 `c1073bae…`）と同一のSHA pinに加え、resolve7が
消費しなかった

- 生4-worker probe記録 `probes-w{0..3}.jsonl`（snapshot pin・main@`ba5f9f4aad`）
- 39-root manifest `roots.json`
- fold10第二検証正本 `a62d6d50…`（証明書幾何再導出）
- 検証対象の resolve7 正本 `207f4094…` 自身

を入力とし、**4つの独立経路**で再導出した: (A) K1069分類39/39の生probe再構成
（dedup/agreement/両順序/cap/pilot/terminal各gate・nodes総計・最大probe・平均の再計算）、
(B) 39-root割当表の3ソース一致（probe covered_rows/roots.json/resolve6 witness_full・
解剖gate・dead根との非交差）、(C) fold鎖78→74→72のリンクごとの集合算術と
frontier7項目の全差分検査・fold9.after==fold10.before鎖結合・extra行の計画外確認、
(D) fold10第二検証正本との閉鎖3行一致。さらにr7-*の13 gateでresolve7正本の
全リスト・数値フィールド（rows78・witness順・閉鎖行・residual72・34×2+4×1割当・
fold9行割当root 4根・K1069交差・27gate/pin宣言）を再計算値と照合した。

## 結果

- **76 gateすべてPASS**（pin 12 + 再導出51 + r7照合13）。
- resolve7の3確定（出自78−4−2・retire後割当の1回被覆維持・depth-10 witness供給ゼロ）は
  resolve7が使わなかった経路でも全て再現。resolve7正本の全フィールドが再計算値と完全一致。
- 出力正本 SHA-256 `4286100804d82376418066da89167c50017244f2c6f02b81ad76a07b45bd91d6`・
  2回実行+別cwd別プロセスで byte-identical。
- 追加の測定事実: 生probe corpusは一意78対＋**重複記録20行**（実験README組立時点の
  観察は15行・append-resumeプロトコルと78/78再実行と整合した組立後の成長）で、
  20行全てがnode-exact一致。run-to-run決定性の追加証拠（分類・合計への影響なし）。

## 落ち穂・運用

- K1069掃引のsummary値（total_nodes・avg int除算・max_probe多field）まで正本から
  再現できる: assemble.py を読み込まずraw記録のみで再構成した点が第一機械との差異。
- fold9閉鎖4行のcost個別値（76/64/79/80・計299）とfold10の3行（66/73/86・計225）を
  記録に残した（第二検証で個別costを初めて全件確認）。
- GitHub API unauthenticatedは rate limit 渋滞したため、着地確認は
  get_file_contentsのblob SHA読み取り＋ローカル `sha1("blob <len>\0"+bytes)` で実施。

## 未解決のまま（解釈規約不変）

本第二検証は探索ゼロ・根の新規判定ゼロ・行の閉鎖ゼロ。REFUTED-D10はLOSS証明ではない。
供給ゼロは39-root計画スコープの観察。**標準11×11空盤・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

1. K1075（候補供給cache-join再構築）正本の第二検証が次の自然な作業候補
   （同様のpublished-records-only設計・単一オーナー宣言先行）。
2. 候補供給側の掃引・phase-2以降はK1075レーンの宣言を確認してから。
3. add-two-stones拡張・depth>10コスト測定は未着手。
