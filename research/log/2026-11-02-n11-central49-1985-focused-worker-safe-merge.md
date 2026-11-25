# 2026-11-02：1,985七石条件付き計画の単一六石集中配布と安全な作業報告統合

最新mainの `AGENTS.md`、knowledge README、K0023、K0634、1,985類への三証人交換証明書、独立検証器、既存の1,984類向け作業者報告統合器を確認した。既存の1,984類計画はその後の反証で失効しており、その仕事一覧を新計画へ転用しない。

`focus_s7_worker_1985.py` を追加。既存 `verify_central49_three_swap_chain.py` の独立4×4整数幾何で、1,985七石正準類・2,989合法辺・46六石証人・最終選択集合SHA-256 `f72c587537cbe2239b0f077545dfd14628298d2fe6d7c6b80ac7345ff46b6026` を再検査してから、**選択六石一類だけ**の合法七石子を4作業者に重複なく均等配分する。

初期候補は「他の選択六石と共有されない七石子が最少→合法七石子総数が最少→六石正準鍵の辞書順」で選ぶ。これは幾何学的な再利用性の指標であって、実探索時間の短縮を証明しない。六石鍵を明示した場合も、選択46類への所属を検査する。

生成する計画には出典証明書のSHA-256、選択集合のSHA-256、集中六石、七石全鍵、作業者別の仕事一覧とSHA-256、`UNKNOWN` 極性を保存する。後から計画を読み込む際には出典から**再生成して完全一致**を検査する。旧1,984類計画の汎用報告検査関数だけを再利用し、旧仕事一覧・旧所有者は一切使わない。

作業者報告は `s7workerreport,worker,key,original_first,WIN|LOSS|UNKNOWN,unverified` に限定。担当外、重複、WIN/LOSS衝突、入力ファイルの読取中改変を拒否し、UNKNOWNを判定として保存しない。元先手WIN7の報告が一つでもあれば `REPLAN_REQUIRED` として停止する。統合結果は既存ファイルを上書きせず、同一ディレクトリの一時ファイルからハードリンクで原子的に新規作成する。**統合結果は独立終局証明ではなく、勝敗cacheにも自動反映しない。**

再現例：

```sh
python3 research/experiments/n11-central-19-cover-20261031/focus_s7_worker_1985.py --self-test
python3 research/experiments/n11-central-19-cover-20261031/focus_s7_worker_1985.py --plan-out /tmp/n11-1985-focus.json
python3 research/experiments/n11-central-19-cover-20261031/focus_s7_worker_1985.py --audit-plan /tmp/n11-1985-focus.json --worklist 0
```

専用短時間CI `.github/workflows/n11-central49-1985-focus.yml` を追加。計画の再構築、4分割、合成LOSS7報告の安全統合、極性改変の拒否を検査する。**この記録時点では専用CIの完了を未確認**。長時間探索は起動していない。

新規の六石LOSS・四石LOSS・二石root閉鎖は0件。1,985類は条件付き証明義務であり、証明済みの七石LOSS数ではない。標準11×11空盤の勝敗は**UNKNOWN**。
