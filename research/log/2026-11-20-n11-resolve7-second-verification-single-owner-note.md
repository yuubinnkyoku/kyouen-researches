# 単一オーナー宣言: resolve7（K1072）出版正本の独立第二検証

- 2026-11-20 06:35 JST（2026-11-19 21:35 UTC）。取り直した最新 main HEAD `e7e83353c0`
  （K1075 bullet 反映済み）に基づき宣言する。
- 当レーンは、residual 72 行の post-fold witness 再照合（resolve7・K1072・出版正本
  SHA-256 `207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f`・27 gate）の
  **独立第二検証**をこの実行で出版する。他レーンは同内容の第二検証を重複して出版しないこと。
  （fold10 第二検証・十七証明書三重検証と同じ「出版済み正本のみからの独立再現」枠組み。）

## やること・やらないこと

- 入力は出版済み正本のみ: resolve6 / fold9 / fold10 / K1069掃引 / sv17 の5正本（resolve7と同一の
  SHA-256 pin・fail-closed）に加え、resolve7 が消費していない生 4-worker probe 記録
  （probe-records-w{0..3}.jsonl）・39-root manifest（roots.json）・fold10 第二検証正本
  （`a62d6d50…`）をピンして消費する。
- 独立経路: (A) K1069分類の生probe記録からの再構成（dedup+agreement の自前実装・39/39照合・
  nodes総計/最大probe/平均の再計算）、(B) 39-root割当表の3ソース一致（probe covered_rows・
  roots.json・resolve6 witness_full）、(C) fold鎖の行算術（78→74→72 を各fold正本のresidual
  listごとに検証しつつ frontier 7項目の前後差分を全検証）、(D) fold10第二検証正本
  （証明書幾何再導出）との閉鎖3行一致。
- さらに resolve7 出版正本の全リスト・全数値フィールドを再計算値と照合する（gate family r7-*）。
- **探索は行わない。根は判定しない。行は閉じない。universe再構築もしない。**
  勝敗には一切言及しない。REFUTED-D10 は LOSS 証明ではない。
  標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。

## 管轄外（着手しない）

- 残余 72 行への候補供給（fresh-safe pool cache-join: K1075 出版済み）とその掃引・
  phase-2 以降の作業は宣言済みの並走レーンの管轄。
- add-two-stones 拡張・depth>10 コスト測定も本宣言の対象外。
