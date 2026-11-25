# n11 残余72行 36 fresh witness depth-10掃引の単一オーナー宣言ノート（2026-11-20）

K1075（残余72行のfull cache join候補供給再構築・正本SHA-256
49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa）の出版に
先立ち宣言済みだった「fresh-safe poolの候補供給データ出版（計画自体の掃引
着手は別途宣言）」の後段として、K1075の `witness_full` が特定した
**36 fresh witness root（phase-2 join後も未判定・全7石・D4正準形・全safe・
最大matching 36で残余72行を1回被覆・stranded 0）のdepth-10両順序掃引**を
本レーンが単一オーナーとして実行することを宣言する（K1069 39live掃引の
並走調整ノート方式の踏襲）。

## 本レーンが実行するもの

- 対象: K1075正本（49b6f85f…）`witness_full` の36 root（全7石・D4正準形・
  covered rowsの和集合==残余72行・1回被覆・36 pair・singleton割当なし）。
  roots.jsonはK1075正本のwitness_fullから機械生成し、popcount==7・
  child|1<<bit==root（child=root−最小セットビット・生整数hex・canon_hex
  被せ禁止・K1046事故規約継承）をgateする。
- runner v17（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59・本レーンで
  raw取得しgit blob SHA-1再計算一致を確認済み）・depth 10・cap 30M均一・
  両AND順序（andclose 1/0）・pilot_d6制御行（3,402 nodes・loss=false要求・
  runner内fail-closed）。
- 出力正本は `research/experiments/n11-residual72-36witness-depth10-sweep-20261120/`
  に置く。実験dir名にK番号は含まない。72 probe（36 root × 2順序）を
  4 worker分割（roots[W::4]・1 workerあたり最大約4並列相当の控えめた並列度）・
  probe単位280s timeout・append/resume式記録で実行する。

## 他レーンへのお願い

- K1075 witness 36 rootの同一掃引の並行実行・重複出版は行わないこと。
- 判定結果がWINのrootは証明書抽出候補として記録する（抽出・独立二重検証・
  receipt foldは別工程・別途宣言）。REFUTED-D10はLOSS証明ではなく、行の
  ゲーム理論的値には一切言及しない。
- 掃引の結果、どの行も閉じない（閉鎖計上は証明書fold後）。

## 解釈規約

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて
UNKNOWNのまま。** 本掃引の結果は行の被覆簿記と候補供給の観察であって、
勝敗確定ではない。
