# 2026-11-01：中央49・四石優先計算を単一の固定計画として配布

最新main、`AGENTS.md`、`research/knowledge/README.md`、K0023・K0329・K0417、現行2,277類の31証人被覆、Python監査器、関連する11月1日の研究記録を確認した。標準11×11空盤と二石 `{49,60}` はともに **UNKNOWN**。

## 問題

従来の `--worklist ID --focus-priority [--existing partial.csv]` は、4作業者が**それぞれ別の時点の報告ファイルを読んで**優先四石証人を選ぶ。計算中に `partial.csv` が増えると、作業者ごとに異なる四石証人が選ばれ、同じ94類に計算を集中するという調整器の意図が崩れる可能性があった。既存の担当分割は重複を防ぐが、選択対象の同一性は保証しない。

## 修正

`audit_central49_three_swap_worker_results_2277.py` に **`--focus-plan`** を追加。既存の報告を一度読み込んで検査し、優先四石証人を一度だけ選択し、4作業者の一覧を**一つのJSON**として出力する。各作業者はこの同一JSON内の `worklists[ID]` を使用し、個別に優先対象を再選択しない。

```sh
python3 research/experiments/n11-central-19-cover-20261031/audit_central49_three_swap_worker_results_2277.py --focus-plan > focus-plan.json
python3 research/experiments/n11-central-19-cover-20261031/audit_central49_three_swap_worker_results_2277.py --focus-plan --existing partial.csv > focus-plan-resume.json
```

- `selected_s4`、`worklists`（4配列）、`worker_loads`、作業一覧ごとのSHA-256、元の2,277類計画のSHA-256を同じ出力に固定。
- `--existing` の内容のSHA-256を計算前後で比較し、読み込み中の変更を拒否。再開時の入力の同一性を記録。
- 報告済みの五石局面は再配布せず、担当外・重複・WIN5報告は拒否。明示的な `--focus-s4` による固定選択も可能。
- 全て報告済みなら空の作業一覧を返すが、**四石LOSSの証明済みとは扱わない**。報告値を独立証明へ昇格しない。
- `--focus-plan` と `--worklist` の同時指定を拒否。

初期状態の集中対象は94類、4分割は **24/24/23/23**。計画全体の未判定五石局面は **2,277類**、既知LOSS5依存は314類、未証明四石証人は28類で変わらない。

## 検証

合成局面による自己試験に、同一時点の4作業者一覧・完了報告済みの非昇格・WIN5報告拒否・無効な四石証人拒否を追加。実際の2,277類計画に対するCIでは、単一JSONの94類が重複なく4分割され、`--focus-s4` による従来の4一覧と完全一致し、SHA-256が一致することを確認。合成のLOSS5報告1件を加えた再開では、固定した四石証人の残数が **94→93**、既報告の1類が消え、入力報告のSHA-256も一致することを検証した。

**独立監査CI成功**：https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/41241877096

実装 `75c794ce821a1febf175fc138f1b02e0f4659a7b`、CI追加・改修 `a8eae6761b8956569e4721b1dbddf0b6999f8721` / `7e9c97d9bf5b889dc85be52ca5bb7e0790de9023`。branch・PRは作成せずmainへ直接反映。

## 信頼境界と次の課題

**今回改善したのは並列計算の対象選択を固定する手順**であり、数学的な被覆費用や探索時間を減らしたわけではない。新規五石判定0件、四石LOSS証明0件、二石root閉鎖0件。報告の完全性だけで証明が完成したとはいえず、全子局面の判定には独立した再検証が必要。

今後は固定計画の94類に計算を集中し、判定済みの五石局面を証明書付きで回収する。**標準11×11空盤はUNKNOWN。**
