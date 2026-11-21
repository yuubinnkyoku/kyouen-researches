# 7行 q=4 witness band 60plus レーン: 実行成果（2026-11-21 高速レーン）

- 宣言: `research/log/2026-11-21-seven-row-q4-band-m60-single-owner.md`（11:35Z・宣言時 HEAD `e0d072fb`）。
- 成果物: `research/experiments/seven-row-q4-witness-band-60plus-20261121/`。
- publish:
  - part1 `5d22f006`: scripts（enum_two.js・verify_witnesses.py）+ 較正 + 幅60 witness 4件 + 2系統検証（fetch-back md5 照合 MATCH）。
  - part2 `b0a663a6`: 幅61..67 チェーン成果（frontier/stats/witness 各幅）+ チェーン代表検証 7件（fetch-back 抽査 MATCH）。
  - part3（本 commit）: 第三系 verify_third.py + third_verify.json + README 追記 + K0827 反映 + knowledge README 反映 + 本ログ。

## 結果（下界更新）

1. **7×60 witness 4件を発見**（w60_a..d）: A57（7×57 witness・2026-11-15 two-swap レーンの
   既発見だが 7×60 近傍は未調査だった seed）の fresh 2-for-2 近傍完全列挙で
   95,722 safe 候補のうち 4件が安全かつ行欠損極大。
2. **チェーンで幅61..67 の全幅に witness**（2-for-2 fresh・frontier cap 10・max-x 貪欲）:
   新規 61:49 / 62:29 / 63:72 / 64:18 / 65:41 / 66:38 / 67:2 件。
3. **M_{7,4} ∈ [68, 1929]**（従来 [60, 1929]）。上界は K0068 の 1929 が不変。
4. 幅68 は最終 frontier 2件の近傍で 0件（局所負記録のみ・不在主張なし）。

## 検証

- 列挙器 `enum_two.js`: pinned `audit_two_swap.cpp` 出版計数に完全一致較正
  （base53@57 1,436,643/60,921/2 + witness 2件の石配置一致、base53@60 1,599,648/83,225/0、
  foundB@60 1,599,648/110,748/0）。
- witness 13件（アンカー A57/B59・幅60 4件・幅61..67 代表 7件）:
  (b) 正規化整数直線/円方程式 Python 検証器 PASS、(c) 第三系（素朴 4×4 行列式総当たり）PASS。
  浮動小数点不使用。3系統一致。

## 環境メモ（次回実行用）

- 今回の実行は途中 2 回、bash 300s 超過で実行環境リセットにより作業ファイルを喪失し、
  そのたびに seed pool・スクリプトを再構成した（列挙器は較正で計数再現を確認）。
  **中間成果は小刻みに main へ publish して永続化する運用が有効**（part1..part3 方式）。
- チェーンの endpoint（幅68）は frontier cap 10 の貪欲に依存。cap・選別基準を
  変えれば 68+ 到達の可能性が残る（幅68 witness 探索が次の実行可能課題）。
- 実行時間の目安: 1近傍列挙につき 2〜4 秒（幅60前後）、1幅あたり cap 10 で 10〜36 秒。
