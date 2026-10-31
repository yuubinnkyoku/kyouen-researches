# 2026-10-31：中央49のS5分割結果を独立再計算し、worker報告をfail-closed監査

開始時のmain `4247fcd5280de2e03d6a8ba8c741011de15c1cf8`、`AGENTS.md`、`research/knowledge/README.md`、K0023・K0329・K0415、中央19初手の実験README、中央49の31類証人・S5依存データ・分割器、既存の`dfpn_s5_merge.sh`と直近logを確認。標準11×11空盤は**UNKNOWN**。

## 実装

`research/experiments/n11-central-19-cover-20261031/audit_central49_worker_results.py` を追加。既存Node分割器と別のPython実装で、次を**保存済み証拠から再生成**する。

- 2つのS5 cacheのGit blob SHA-1、全5,853類の正準性・安全性・極性衝突を検査。
- 選択31個の四石証人の合法五石子を4点共円判定とD4対称性で再列挙し、既知LOSS4の全子のLOSSと未判定28類の子数を照合。
- 相異なる未判定S5 2,525類のSHA-256、元の4分割のworker別SHA-256を固定値と照合。91類優先の新しい分割（632/631/631/631）も独立構成。
- `--worker ID CSV` で部分結果を受け取る。正しい分割に属さない鍵、対象外の鍵、同一ファイルの重複、WIN/LOSS衝突、形式不正を拒否。`result=0`（未完）は判定数に含めず、既存の集約済みcacheに含まれていれば拒否する。
- `--existing CSV` は**この2,525類だけの過去の部分集約**に限る。全盤共通のcacheを指定してはならない。
- 四石証人別の未報告子数、報告WIN/LOSS数を出すが、workerが主張する勝敗を独立証明に昇格させない。証明済み扱いするには別途、各S5の厳密な再探索・証明書監査が必要。

これは**読取専用の事前監査**である。実際の書込み・排他制御・原子的な矛盾検査付き集約には既存`research/experiments/n11-search-methods/scripts/dfpn_s5_merge.sh`を使う。監査と集約の間に入力が変更されない運用が必要で、監査だけでは同時書込みの安全性は保証しない。

## 再現

```sh
python3 research/experiments/n11-central-19-cover-20261031/audit_central49_worker_results.py --self-test
python3 research/experiments/n11-central-19-cover-20261031/audit_central49_worker_results.py
python3 research/experiments/n11-central-19-cover-20261031/audit_central49_worker_results.py --worker 0 worker0.csv --worker 1 worker1.csv
```

手元の合成データによる正例・負例テストは`SELF_TEST_OK`。誤worker割当、対象外鍵、矛盾、同一ファイル重複、異常形式、未完の誤昇格を拒否する。専用CIに独立再列挙と負例テストを追加した。

未判定S5の新規厳密判定0件、四石LOSS新規証明0件、二石root追加閉鎖0件。**11×11空盤はUNKNOWN**。

## CI確認

2026-10-31の独立監査CI [41179459426](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/41179459426) は**成功**。Pythonの負例テストと、実データからの2,525類・91類優先分割の再生成、既存Node監査を含む全工程が成功した。変更後のCIが成功したことは監査実装の回帰確認であり、workerの未実行S5局面が新たにLOSS/WINと判定されたことを意味しない。
