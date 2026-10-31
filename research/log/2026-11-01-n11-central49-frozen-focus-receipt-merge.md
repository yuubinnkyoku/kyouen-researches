# 2026-11-01：中央49・凍結した四石集中計画に対する五石結果の厳格監査と安全な統合

開始時に最新 `main`、`AGENTS.md`、`research/knowledge/README.md`、K0023・K0329・K0417、中央49の2,277類被覆、直近の四石集中計画と研究記録を確認。標準11×11空盤と二石 `{49,60}` はともに **UNKNOWN**。

## 発見した安全性の隙間

前回の `--focus-plan` は四石証人1類の94個の未判定五石子を、24/24/23/23個に固定して配布できた。しかし従来の一般監査 `--worker ID CSV` は、全2,277類の担当集合に属する結果を受け付けるため、**凍結した94類の外にある五石局面**の報告でも正常な結果として統合できた。これは誤った勝敗を確定する欠陥ではないが、coordinatorが指定した四石証人に計算を集中させたかを後から検査できない。

## 修正

`audit_central49_three_swap_worker_results_2277.py` に `--audit-focus-plan PLAN.json` と `--merged-out NEW.csv` を追加。

```sh
python3 research/experiments/n11-central-19-cover-20261031/audit_central49_three_swap_worker_results_2277.py --focus-plan > focus-plan.json
python3 research/experiments/n11-central-19-cover-20261031/audit_central49_three_swap_worker_results_2277.py \
  --audit-focus-plan focus-plan.json --worker 0 worker0.csv --worker 1 worker1.csv \
  --merged-out merged-next.csv
# 再開した凍結計画の場合は、生成時と同一の --existing partial.csv を必ず指定する。
```

- 元の2,277類被覆・既知判定・幾何学的被覆を再構築し、凍結JSONが再構築した計画と**全項目一致**することを確認。既存報告のSHA-256が計画生成時と一致しなければ停止。
- 各作業者の報告は、その作業者に割り当てられた**凍結一覧内の局面だけ**を受理。2,277類に属していても凍結一覧外なら拒否。
- 従来の厳格な六列CSV監査を再利用し、担当違い・不正形式・同一ファイル内の重複・WIN/LOSS衝突を拒否。UNKNOWNは判定として統合しない。WIN5報告があれば `REPLAN_REQUIRED` として統合を停止。
- 読み込み前後の既存報告と作業者ファイルのSHA-256を照合し、処理中の変更を拒否。
- 統合結果は**新規ファイルだけ**に、同一ディレクトリ内の一時ファイルからハードリンクで原子的に公開。入力・既存出力を上書きしない。統合CSVの探索節点数欄は、元の計算量を保存できないため**0（不明）**とし、架空の節点数を記録しない。
- 結果の証拠段階は `WORKER_REPORTED_NOT_INDEPENDENTLY_REPLAYED`。全行が報告済みでも四石LOSS証明とは扱わない。

## 検証

専用CIに実際の2,277類計画からの94類凍結一覧を使う回帰を追加。合成LOSS5報告1件を統合し、残数94→93、出力行の整合性を検査。担当違い、WIN5、同一キーのWIN/LOSS衝突、改ざんした凍結JSON、全2,277類には含まれるが凍結94類の外にあるキー、既存出力の上書きをそれぞれ拒否することを確認。従来の三証人置換全数監査・幾何学的被覆・既知WIN除外・中断再開の回帰も成功。

**独立監査CI成功**：https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/41246575707

実装：`7e31d0c20c485b4f788ed51cb4f62920682d9fd8`、後続の改修・CI：`4764eb6d21b7398477af93569535f8d4be39c218` まで。branch・PRを作らずmainへ直接反映。

## 証拠の境界と残件

今回確定したのは**凍結した集中計画と回収結果の整合性を機械的に検査し、安全に統合できること**。実際の五石局面の新規判定0件、四石LOSS証明0件、二石root閉鎖0件。保存済みLOSS5依存314類、未判定S5 **2,277類**、未証明S4 **28類**は不変。CIの94→93は合成報告による試験であり、実際の証明進展ではない。

次の計算では、同一の凍結JSONを4作業者へ配り、結果をこの監査で統合した後、五石判定を**独立再探索または証明書の検証**で確定させる。標準11×11空盤は引き続き **UNKNOWN**。
