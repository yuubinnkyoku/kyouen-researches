# 2026-11-17 n11 class2-lane: hybrid seed union measurement claim (cost73k)

## 目的

本logは着手宣言（claim）である。前セッションが出版したhybrid seed union設計
（DESIGN_DERIVED_NOT_MEASURED・設計JSON blob `8ec64f21b60b378595a749fc941f2232e0db5c21`・
設計log `research/log/2026-11-17-n11-class2-lane-hybrid-seed-union-design-73k.md`）が
次の実測として明示した4段階を、本セッション（長期レーン）が実行する。

## 計画

設計JSONのnext_measurementと同じ4段階に、sim予測（light_sim_seed_73k.mjs・MS=1<<25）を
事前gateとして加える。入力は全てpin付きblob（boundary測定JSON `b97c9334`・boundary
orchestrator `5ac1e3c0`・seed容量設計orchestrator `50b60247`・extractor `52bcaf50`・
manifest `0892aed0`・legal `8e97082c`）からraw CDNで再構築し、出版値（FINAL4 seed md5
`35ccec0e…`・2-way seed md5 `e7c2c17e…`・workers合計ノード数）の再現を工程ごとのgateとする。

## 状態

- base_head: `9b7a0a1d9e61124a61f7eb8bfa32467de43d5a53`
- batches_run: 0（この時点では一切の測定を実行していない）
- 進展・失敗は測定完了時に測定JSONとlogで出版する

## 解釈ガード

claimの時点では測定値なし。新規WIN/LOSS verdictなし・証明書bytes不変・manifest行の閉鎖なし。
標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWNのまま。
