# 前段被覆を引き継ぐp2531の並列LRAT監査

現在の監査状態は[K0702](../../knowledge/items/K0702-p2531-no-parabola-equality-witness.md)を参照する。
凍結した以前のドライバを変更せず、`--prior` で前段manifestを渡せる再利用可能なドライバを追加した。
今回の対象は未被覆d=102..120,122..140の38件。d=121は既存監査済みなので対象に含めない。

各caseは独立processと独立一時ディレクトリを使い、異なるdを最大4並列で処理する。
入力・原証明・coreを他caseと共有せず、重複d・既被覆d・範囲外dは開始前に拒否する。
plan.jsonと各caseの結果を保存し、未完結の場合は `--collect-only` で既存結果から被覆を集計できる。
既存のcoverage.jsonは上書きしない。UNKNOWN・失敗・未完了は独立検査済み被覆へ加えない。

## 今回の結果

全38件でsolver UNSAT、DRAT-trim -U VERIFIED、空節処理修正版LRAT VERIFIEDを確認した。
さらに保存されたCNF・LRAT gzipを別の再生処理で展開し、全38件を実再生して受理した。
提供38160辺の整数幾何、全新入力の独立投影schema、原DRAT hash、前段manifestのhash連鎖も照合した。
7不正planとUNKNOWN・失敗・未完了・既存coverage上書きの合成制御は全て期待通りだった。

前段162 dと新38 dは重複なしで200/1265 d、未被覆1065 d。
内訳は修正版増分DRAT143 d、LRAT57 dであり、異なる検証器の履歴を同じsource hashへ混ぜない。
全数監査や検証器の一般健全性の形式証明、正確な最大サイズを主張しない。

採用CNF gzipとLRAT gzipはGit管理する。
原DRAT gzipとraw LRATは `output/batch102-140/d<d>/` にローカル保持してGitから除外する。
certificate manifestには採用証明のpath・hash、原DRATのpath・hashと保存範囲を記した。
原DRATがない別checkoutでも採用CNFとLRATだけで独立再生できる。

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-p2531-lrat-batches-20261110/audit.py --prior research/experiments/parabola-p2531-lrat-20261110/output/batch86-100/coverage.json --edges research/experiments/parabola-p2531-lrat-20261110/input/edges.txt --ds 102-120,122-140 --output FRESH-batch --workers 4 --budget 100000
uv run --locked python research/experiments/parabola-p2531-lrat-batches-20261110/verify_saved.py --saved research/experiments/parabola-p2531-lrat-batches-20261110/output/batch102-140 --output FRESH-verification.json --manifest FRESH-certificates.json --workers 4
uv run --locked python research/experiments/parabola-p2531-lrat-batches-20261110/regression.py --output FRESH-controller-regression.json
```

最初は証明生成からの再現、二つ目は保存証拠の照合と実再生で新しいSAT探索を使わない。
同じdを新しい研究上の被覆件数へ再計上しない。
