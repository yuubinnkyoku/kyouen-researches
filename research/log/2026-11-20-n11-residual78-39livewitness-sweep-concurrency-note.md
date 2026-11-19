# n11 残余78行 39 live witness depth-10掃引の並走調整ノート（2026-11-20）

K1066（windfall4証明書抽出・三重独立検証）の出版直後に、resolve6（K1063）の
witness_fullが宣言した「39 live witnessのdepth-10両順序掃引」を本実行が
単一オーナーとして担当することを宣言する（k38レーンの並走調整ノート方式の踏襲）。

## 本レーンが実行するもの

- 対象: resolve6正本（SHA-256 e85d4bfb867a193f2b3cdb23ecfe15679359c9f337fcd97eb5c62473b90c281a）
  `witness_full` の39 root（全7石・D4正準形・全safe・covered rowsの和集合==残余78行）。
- runner v17（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59）・depth 10・cap 30M・
  両AND順序（andclose 1/0）・pilot_d6制御行（3,402 nodes・loss=false要求）・
  生整数hex child（child = root − 最小セットビット・canon_hex被せ禁止・K1046事故規約継承）。
- 出力正本は `research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/`
  に置く。実験dir名にK番号は含まない。

## 他レーンへのお願い

- 同一の39 root掃引の並行実行・重複出版は行わないこと。
- windfall4の4証明書のreceipt fold（fold9・4行の閉鎖計上）はwindfall4レーンが
  引き続き担当する想定（本ノートはfold9を主張するものではない）。
- 判定結果がWINのrootは証明書抽出候補として記録する（抽出・独立検証は別工程）。
  REFUTED-D10はLOSS証明ではなく、行のゲーム理論的値には一切言及しない。

## 解釈規約

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて
UNKNOWNのまま。** 本掃引の結果は行の被覆簿記と候補供給の観察であって、
勝敗確定ではない。
