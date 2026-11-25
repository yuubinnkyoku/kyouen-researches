# 11×11：19残存初手の共同S5証明計画の上下界（2026-10-12）

基準は分離worktreeの `origin/main`（`480f78be`）。同一 `.git` で他エージェントが作業中のため、ローカル `main` へのpullは行わず `D:\wk-krr` で作業した。

## 判断

- 中央応手（`f=60`）固定のLOSS側片側評価に絞り、大規模solver探索なしで有限の組合せ最適化＋既存cache証拠だけにした。
- 2261 third手が948種に重なることを確認し、重複統合が最適値を変えない証明スケッチを `Instance` のdocstringに残して共同問題を869有料群に縮小した。
- 上界 heuristic（4種greedy×16 start＋再選択＋縮小）と5種の下界（per-group-min、threshold、element-only双対、grouped双対、LP緩和双対）を実装した。
- 結果：共同 上界31,546／下界6,573、個別合計63,118、削減50.02%。最安は初手49（2,055）。
- `verify_plans.py` で全2,261 third手・全34,948到達S4を独立再計算し失敗0。検証器自体の初版バグ（WIN除外クラス数の扱い）は修正済み。
- `optimize_s5_selection.py` の初版バグ（最終refineが最良解でなく最終start解に適用）も修正済み。旧数値（例：49番3,299→正2,055）は破棄した。

## 失敗・遅延

- フルラン初回は40分timeoutで中断した。原因は (1) greedy内側loopの規模見積もり不足（34,449選択肢×869群）、(2) `dual_value` 内の全要素表明（962,525×869の二次loop）、(3) `refine` の64 pass。対策は重複除去・表明削除（`LB <= UB` 表明に置換）・pass削減・pool反転・進捗logである。
- 作業途中のsmoke出力（`individual-smoke.*`、`joint-smoke.*`）と `__pycache__` は削除した。

## 引き継ぎ

- 未実施：`--extra-replies` による非中央応手の個別最適値比較、初手WIN証明側の費用分析（課題4相当）、下界と上界の差の縮小（分枝限定なし）。
- K0417（computed）を作成し、`tools/knowledge/check.py`・単体試験・`build.py` の通過後に `git push origin HEAD:main` で反映する。
