# 2026-11-06 n11 focus_s6（00000000000000203808000000000040）の全62子局面を確定

2091 条件付き計画（K0670 系）の focus S6 `00000000000000203808000000000040` が持つ
未検証 S7 子 62 件（`n11-central-19-cover-20261031/output/focus2154_plan.json` の
`unverified_s7`）について、全件の確定戦略を生成し独立監査した。

## 生成
- 生成器: `research/experiments/n11-central-19-cover-20261031/generate_five_terminal_loss7.cpp`
  （デフォルトは `original_first_LOSS7`；`original_first_WIN7` 引数で反転）
- 実行: 8並列、90s/件上限、`/mnt/d/kyouen-focus-certs/` に `*.cert` / `*.win7.cert`
- 結果: 35 件 LOSS7 生成、27 件 WIN7 生成、重複 0、未解決 0
- 生成時ログ: `C:\Users\yuubi\AppData\Local\Temp\opencode\run_focus62.log`
  （実行結果 `results.json` は cert と同所）

## 独立監査
- 監査器: `research/experiments/n11-central-19-cover-20261031/verify_five_terminal_loss7.py`
  （生成器と独立の 4x4 Bareiss 整数行列式で全応答を再計算）
- 62 件すべて PASS、fails 0
- 検証記録: `/mnt/d/kyouen-focus-certs/verified.json`（loss 35 / win 27 / fails 0）

## 帰結（確定事実）
- WIN7 子が 27 件存在する ⇒ focus_s6 の手番（先手）には確定の勝ち手がある。
  したがって focus_s6 は terminal 策略レベルで先手勝ちと確定する。
  （27手すべて個別戦略が独立監査済み）
- LOSS7 子 35 件も確定したが、勝ち手の存在により focus_s6 の勝敗は決まる。
- K0670 等の条件付き計画の outcomes は変更しない（従来どおり UNKNOWN）。
  focus_s6 単独の確定情報として記録する。
