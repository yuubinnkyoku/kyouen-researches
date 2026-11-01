# 2026-11-01：中央49の優先94類を合法第六手の総数で厳密平準化

最新main（開始時 `3206a601`）、`AGENTS.md`、knowledge README、K0023、中央49の2,208類計画・固定S5 cache・直近の作業者報告分離を確認した。標準11×11空盤と二石局面 `{49,60}` は **UNKNOWN**。

## 観測と改善

現行31証人被覆の優先四石クラス `00000000000000003800800000000000`（石47,59,60,61）の合法五石子は相異なるD4正準クラスで94類。固定S5 cache（フィルタ後5,851類）との一致は0類で、94類すべてが未判定である。

各五石クラスについて、**盤上の合法な生の第六手の個数**を整数3×3行列式（共円・共線四点の禁止）から全数計算した。各クラスの第六手数は68〜92、94類の合計は **7,890辺**。

| 指標 | 既存の均等件数割当 | 今回の平準化 |
| --- | ---: | ---: |
| 作業者ごとの五石局面数 | 24 / 24 / 23 / 23 | 24 / 24 / 23 / 23 |
| 合法第六手数の合計 | 2,021 / 1,998 / 1,909 / 1,962 | **1,973 / 1,972 / 1,972 / 1,973** |
| 最大の合法第六手数 | 2,021 | **1,973** |
| 最大負荷の減少 | — | **48辺（約2.38%）** |

4作業者の合法第六手数の合計は7,890なので、どの割当でも最大負荷は少なくとも `ceil(7890/4)=1973`。今回の具体的割当はこの下界を達成するため、**この94類を対象とした合法第六手数の最大値最小化は厳密最適**。最適化時にはSciPy/HiGHSの0/1整数計画を使ったが、保存済みの割当と最適性の検証には最適化器を必要としない。

## 再現と証拠の境界

- `research/experiments/n11-central-19-cover-20261031/focus_s6_balanced_94.json`：正準鍵の昇順94類に対する4作業者の割当を94文字で固定。
- `research/experiments/n11-central-19-cover-20261031/verify_focus_s6_balanced_94.py`：独立の整数幾何から94類・第六手数・4分割・下界達成を再計算し、改変した割当を拒否する。
- `audit_central49_post_three_three_swap_worker_results_2208.py` に `--focus-plan --balance-s6` を追加。既存の標準分割は変更せず、任意選択した平準化計画についても同じ凍結計画照合・担当外報告拒否・安全な未検証結果統合・中断再開を利用できる。凍結計画には平準化証明書のSHA-256を記録する。

実行例：

```sh
python3 research/experiments/n11-central-19-cover-20261031/verify_focus_s6_balanced_94.py
python3 research/experiments/n11-central-19-cover-20261031/audit_central49_post_three_three_swap_worker_results_2208.py --focus-plan --balance-s6 > balanced-plan.json
# balanced-plan.json の worklists[0..3] をそれぞれ担当作業者に渡す
```

`--audit-focus-plan balanced-plan.json --worker 0 worker0.csv --merged-out merged.csv` で結果を受領する。再開時は `--existing merged.csv --focus-plan --balance-s6` とする。結果は `s5workerreport` 形式の未検証報告であり、厳密cacheには自動昇格しない。

**重要：合法第六手数は探索時間の実測ではない。** 分岐後の探索難度・cache hit・共有TT・通信費用を反映せず、実行時間が2.38%短縮すると主張しない。新規S5判定0、S4 LOSS証明0、二石root閉鎖0。未判定S5は2,208類、優先94類、未証明S4は28類で不変。標準11×11空盤は **UNKNOWN**。

専用CIは `.github/workflows/n11-central49-post-three-three-swap-2208.yml` に追加した。結果は別途確認する。

## 独立監査CI確定

[GitHub Actions #41271942982](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/41271942982) はコミット `a51bb7ac7e687e4afbd4cc2ae71ecbfa439fcfd6` で **success**。従来の三証人置換全数監査・2,208類の独立再構築・旧形式の凍結計画回帰に加え、94類の合法第六手の全数再計算、最適平準化、平準化計画の担当外報告拒否・改変拒否・結果統合・中断再開をすべて検査した。勝敗証明ではなく計算配分の厳密監査である。
