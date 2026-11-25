# fold10（第17 WIN7 receipt fold）独立第二検証 log（2026-11-20）

## 経緯

- 本レーン（並走）は前半に 39 live witness depth-10 掃引の追加独立実行（78/78 probe
  node-exact・WIN 1 root の検出一致）と第17証明書の抽出・三重検証を出版済み
  （commit `0c1264b228`・実験dir `n11-residual78-seventeenth-win7-cert-extract-20261120`）。
- 単一オーナーレーンが fold10 を実行・出版（commit `69a5232d2e`・正本 SHA-256
  `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a`・
  item は K1070 番号衝突解消後に K1071 として再採番済み）。
- 単一オーナー宣言に従い本レーンは fold10 を重複実行せず、
  **出版済み正本だけを入力とする独立第二検証**を実施した
  （windfall4 fold で確立された second-verification 方式）。

## 方法（チェーン入力非依存）

`verify_fold10_second.py`（純 stdlib・fail-closed）は fold10 機械の
18 入力チェーン再構築を使わず、出版正本 3 点（fold10 正本・fold9 正本・第17証明書本体）
を SHA-256 pin で検証して以下を独立再導出した:

1. receipt root `00004000000000821082000000000100` の 8 D4 像 × 7 石除去
   （56 操作 → D4 正準形 7 行）から閉鎖主張 3 行を再現。
2. fold9 residual74 − target 2 行 == fold10 residual72（72 行の完全リスト一致）。
   D4 除去候補 7 行のうち fold9 residual74 に触れるのは主張どおり
   ちょうど 2 行（`…0001`・`…0004`）。残る 4 候補は windfall4 被覆行でも
   residual74 でもなく、チェーン入力を再構築した fold10 機械の根拠
   （open74 に非所属）は本検証の対象外。
3. 算術 31 gate: frontier 6,209/491,722→6,206/491,497（−3 行・−225 cost）、
   closed edge cost 225 == 66+73+86、solved S6 1,639→1,642、incidence
   11,818→11,810（parent_deltas 和 8）、5親 target 38→40/112・残余 74→72、
   影響 5 parent・fully-closed 0、retired witness rows 一致、schema・guard。

## 結果

- **31/31 gate 全 PASS**（正本 `output/fold10-second-verification-20261120.json`・
  SHA-256 `a62d6d50ffe3196ad2de1ff7b1df67ff8208b2a13510cce3f13aee0e9a085054`）。
- 2 回実行で byte-identical。
- fold10 正本は main から raw 取得し出版 SHA-256 と完全一致
  （追加の証明書本体照合: 本レーン保持の byte-exact コピー
  `21dd2f0e…07c8` と pin 一致・4 実行合意とも整合）。

## 解釈規約（不変）

- 本検証は fold10 の被覆簿記の確認であり、閉じた行のゲーム理論的値
  （LOSS 等）を主張しない。REFUTED-D10 は LOSS 証明ではない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**

## 次の一手

- 残余 72 行への resolve7 再照合（retired root 反映後の最大マッチング再解決・
  stranded 分類）: fold10 正本 + resolve6 正本を入力とする単一オーナー方式が自然。
- fold10 機械のチェーン再構築 gate 群は今回の第二検証では再検していない
  （入力 pile を別レーンが揃えて再実行する方式が有効）。
