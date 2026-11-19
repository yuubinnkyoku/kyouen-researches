# n11-seventeenth-receipt-fold-second-verification-20261120

単一オーナーレーンが出版した fold10（第17 WIN7-D10 receipt fold・実験dir
`n11-seventeenth-win7-receipt-fold-20261120`・正本 SHA-256
`bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a`）に対する、
別レーンによる独立第二検証 (second verification)。

## 検証方法（チェーン入力に依存しない独立再導出）

`scripts/verify_fold10_second.py` は fold10 機械 `fold_seventeenth.py` の
18 入力チェーン再構築（worklist・ledger・tarball 等）を一切使わず、
出版正本 3 点のみを SHA-256 pin で検証して次を再導出する:

1. **被覆行の幾何再導出**: receipt root `00004000000000821082000000000100` の
   8 D4 像 × 7 石除去（56 操作）の D4 正準形集合（7 行に正準化）を独立実装で
   再導出し、閉鎖主張 3 行（5親 target 2 行 + target 外 extra 1 行）がすべて
   含まれることを確認。
2. **残余簿記の完全一致**: fold9 正本の residual74 から target 2 行を除いた
   72 行のリストが fold10 の `residual_row_hex_after` と完全一致（順序含む）。
   56 操作で得た 7 候補のうち fold9 residual74 に触れるものが主張どおり
   ちょうど 2 行（`00000000000000821082000000000001`・`00000000000000821082000000000004`）
   であることも確認（残る 4 候補は windfall4 被覆行でも fold9 residual74 でもない。
   fold10 以外の候補は open 集合の外にあるため fold10 機械では閉じられていない）。
3. **算術 gate**: frontier 6,209/491,722 → 6,206/491,497（row −3・cost −225）、
   closed edge cost 225 == 3 行 cost の和 (66+73+86)、solved S6 1,639→1,642、
   parent incidence 11,818→11,810（parent_deltas の rows_closed 総和 8 と一致）、
   影響 5 parent・fully-closed 0・rows_before/after 単調、5親 target 38→40/112、
   witness retired rows == target rows、schema・interpretation guard 等の計 31 gate。

## 結果

- **31/31 gate 全 PASS**（output/fold10-second-verification-20261120.json・
  SHA-256 `a62d6d50ffe3196ad2de1ff7b1df67ff8208b2a13510cce3f13aee0e9a085054`）。
- 決定論: 2 回実行で出力 byte-identical。
- 入力 pin: fold10 正本 `bed7d331…54ab908a`（main から raw 取得・出版値一致）・
  fold9 正本 `24db2352…17cdc2`・第17証明書本体 `21dd2f0e…07c8`・
  （resolve6 pin `e85d4bfb…c281a` は fold10 正本内の pin と照合）。

## 検証境界（通例どおり失敗閉鎖的明記）

- 本検証は fold10 機械自身のチェーン再構築 gate（12 blob SHA-1 pin 入力や
  base→…→ninth-twelfth の frontier 再現）を代替しない。それらは単一オーナー
  機械 `fold_seventeenth.py` の fail-closed gate が担う。
- extra 行 `00004000000000003800000100000020` が open74（6,209 行）に属していた
  ことはチェーン入力がないと本検証からは再導出できない（幾何候補であることと
  target 簿記外であることのみ独立確認）。
- fold は被覆の簿記であり、閉じた行のゲーム理論的値を主張しない。
  REFUTED-D10 は LOSS 証明ではない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**

## ファイル

- `scripts/verify_fold10_second.py`: 検証機（純 stdlib・決定的・fail-closed）
- `output/fold10-second-verification-20261120.json`: 31 gate の機械可読正本
  （候補 7 行の完全列挙・入力 SHA-256・unknown guard を含む）

## 次の一手

残余 72 行への resolve7 再照合（39-root witness 計画の当該 root retired 後の
最大マッチング再解決）は publish 済み fold10 正本を入力とする別レーンの
単一オーナー方式で進められる。本検証は fold10 の判定に何も変更しない。
