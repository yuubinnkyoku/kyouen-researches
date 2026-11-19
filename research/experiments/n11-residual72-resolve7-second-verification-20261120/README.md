# n11-residual72-resolve7-second-verification-20261120

resolve7（K1072・残余72行のpost-fold witness再照合）出版正本の独立第二検証。
単一オーナー宣言ノート
`research/log/2026-11-20-n11-resolve7-second-verification-single-owner-note.md`
を先行出版した同一レーンの実行。branch/PRは作らずmainに直接出版。
fold10第二検証（receipt fold）・十七証明書三重検証と同じ
「出版済み正本のみからの独立再現」枠組み。

## 検証対象

- resolve7正本: `n11-residual72-postfold-witness-recheck-20261120/output/residual72-postfold-witness-recheck-20261120.json`
  SHA-256 `207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f`（27 gate）

## 何をしたか

resolve7が消費した5正本（resolve6/fold9/fold10/K1069掃引/sv17）に加え、resolve7が
消費しなかった3系統の出版記録をピンして、**4つの独立経路**で主要確定を再導出した。

- **route A（K1069分類の生probe記録からの再構成）**: 4-worker の生 probe 記録
  （`probes-w{0..3}.jsonl`98行・append-resume式・一意(root,ordering)対78）から
  dedup・agreement・両順序・cap・pilot_d6制御・terminal範囲を自前実装で検査し、
  分類を39/39再構成して sweep39 正本の classification と完全一致させた。
  nodes総計169,615,508・最大probe（`00000000010000809002000040000080`・14,249,420・
  andclose0・loss=false・terminal [13,17]）・平均（int除算）も再計算一致。
- **route B（39-root割当表の3ソース一致）**: 生probe記録の covered_rows・
  roots.json manifest・resolve6.witness_full の3ソースが同一の
  39 root×2行=78行1回被覆割当表を持つことを機械照合。roots.json の解剖
  （popcount 7・root==child|1<<bit・childが最小セットビット除去・bit一致・safe）も全rootで合格。
  witness root集合は dead_roots_39（39根）と互いに素。
- **route C（fold鎖の行算術・リンクごと）**: 78行→(fold9閉鎖4行 cost 76+64+79+80=299)→
  residual74→(fold10 target閉鎖2行 cost 66/73)→residual72 を、fold9/fold10各正本の
  residual listそのものでリンクごとに集合算術検証（resolve7の「78−6==72」とは別経路）。
  両foldのfrontier 7項目の前後差分（unique −4/−3・sum −299/−225・solved +4/+3・
  s6_needed −4/0・cost_needed −299/0・incidence −8/−8）を全検証し、
  fold9.frontier_after == fold10.frontier_before の鎖結合を確認。
  fold10の3行目（target外extra・cost 86）は78行計画外・residual74外も gate で確認。
- **route D（証明書幾何経路との一致）**: fold10第二検証正本
  （`a62d6d50…`・31 gate・証明書本体から56操作→7候補の幾何再導出を実行した別レーン記録）の
  candidates_touching_fold9_residual74 がfold10 target閉鎖2行と完全一致し、
  extra行も再導出候補に含まれることを確認。
- **resolve7正本自体の全フィールド照合（gate family r7-*・13 gate）**: rows78・
  witness 39 root順・fold9閉鎖4行・fold10 target 2行・extra 1行・residual72・
  post-retire割当（34×2+4×1・rows_per_root全照合・fold9行の割当root 4根）・
  K1069交差数値（WIN 1/REFUTED 38・供給ゼロ）・27 gate/pin宣言がすべて再計算値と一致。

追加の測定事実: 生probe記録 corpus には一意78対の他に**重複記録20行**（README組立時点の
観察は15行）が存在し、その全てが loss/nodes/capped/bit/child/terminalRange で
node-exact 一致する。append-resumeプロトコルと78/78再実行の記録と整合し、
run-to-run決定性の追加証拠になる一方、組立後の corpus 成長（15→20）は
観察記録として報告する（全行一致なので分類・合計に影響なし）。

## 結果

- **76 gateすべてPASS**（pin 12 + route A/B/C/D再導出51 + r7照合13）。
- resolve7の3つの確定（残余72行の出自78−4−2・retire後割当34×2+4×1で1回被覆維持・
  39-root計画からのdepth-10 witness供給ゼロ）は、resolve7が使わなかった経路でも
  すべて再現された。**resolve7 正本の全リスト・全数値は再計算値と完全一致**。
- 正本SHA-256 `4286100804d82376418066da89167c50017244f2c6f02b81ad76a07b45bd91d6`・
  2回実行+別cwd別プロセス（/tmp/r7vb）で byte-identical。
- 実行方法: stdlibのみ。`python3 scripts/resolve7_second_verification.py <input_dir> <out>`。
  input/ は正規名（resolve6.json/fold9.json/fold10.json/sweep39.json/sv17.json/
  probes-w{0..3}.jsonl/roots.json/resolve7.json/fold10second.json）。
  pins は機械内にSHA-256で固定（fail-closed）。worker記録・roots.json・fold10secondの
  pinは main@`ba5f9f4aad` 時点の出版状態から計算した snapshot pin。

## 解釈規約（他のn11項目と同一）

- REFUTED-D10 は LOSS 証明ではなく、fold・被覆は行の簿記。本第二検証は探索ゼロ・
  根の新規判定ゼロ・行の閉鎖ゼロ。供給ゼロは39-root計画というスコープの観察。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**

## 次の一手

1. 残余72行への候補供給は K1075（fresh-safe pool cache-join再構築・並走レーン）が
   出版済み。その正本に対する第二検証（同様の published-records-only 設計）が
   次の自然な価値ある作業候補。着手時は単一オーナー宣言ノートを先行すること。
2. add-two-stones 候補拡張・depth>10 コスト測定（K1038 stranded 構造の後続）は未着手。
