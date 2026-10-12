# 履歴資料：極性誤りを含む旧WIN側出力（2026-10-12 監査で無効化）

この3件は旧 `win_side.py` / `win_witness_masks.py` が S5 LOSS子を持つS4を先手WIN（free）と扱う極性誤りで生成したもので、K0371（S4=OR：WIN ⟺ WIN子あり）と矛盾するため採用しない。

- `win-side-analysis.json`：旧65/65閉鎖可能・無料5・証人約1,739・AND幅7,503は誤り。証人はS5 WINでなくS5 LOSSを数えていた。
- `win-witness-masks.json`：旧証人1,739マスクはLOSS側frontierであり、WIN証人ではない。
- `pilot-candidates.json`：legal手数分布と最安10件は極性に依存せず有効。`dual_use` 16件（WIN証人と共同要求の両用）は誤り。新 `pilot-candidates.json` では重なりに極性衝突の意味を持たせて再計算する。

訂正済み出力（`output/win-side-analysis.json` schema v2、`output/win-witness-masks.json` schema v2）は修正後の `win_side.py` が共有モジュール `scripts/s4_win_polarity.py` を使って再生成したものである。新旧の数値対応は親READMEの監査記録を参照する。
