# 2026-10-30: N11第27回の独立検証CI偽陽性を修正

最新main、AGENTS.md、knowledge正本、9〜27回の証明書・研究記録を確認した。第27回の独立検証CI [40889814358](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40889814358) は成功表示だったが、ジョブログを再監査すると Node 検証器 `verify_compact.js` の `for(let n=9;n<=26;n++{` が構文エラーを起こし、Node検証は**実行されていなかった**。シェルの `node ... | tee ...` に `pipefail` がないため、後段の `tee` が成功してジョブ全体が緑になっていた。Python独立検証は当時成功していたが、NodeとPythonの両成功と解釈するのは誤り。

- [構文修正](https://github.com/yuubinnkyoku/kyouen-researches/commit/e5378c70b8b8304779be92aa102e1f5a83e273d2) で `for(...){` に修正。
- [独立検証CI修正](https://github.com/yuubinnkyoku/kyouen-researches/commit/6a1adba0d96064c408a152c843f52d9342ecc657) で Node/Python 両ステップに `set -o pipefail` を追加。検証器変更も起動条件に含めた。
- 修正後の[独立検証CI 40899341173](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40899341173) は**成功**。Node は `verified=true`、9石LOSS 1類、最小終局1類、163再帰状態を報告。Pythonも同じLOSSと163再帰状態を報告。Nodeの偽証人・範囲外添字拒否を含む負例試験が通過。
- 第27回証明を再利用する[第28回再計画](../experiments/n11-s9-post-round27-replan-20261030/replan.js)をmainに実装し、検証CI [40899217821](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40899217821) を起動。結果未確定。
- 限定候補在庫が枯渇する前に、固定14根計画の未証明8石37類から**全合法9石子**を列挙する[構造監査](../experiments/n11-s8-complete-child-audit-20261030/audit.js)を実装。検証CI [40899226812](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/40899226812) は結果未確定。選択候補だけを数えた結果と、全合法子の分類を混同しない。

証明限定8石WIN 5,859類、固定14根計画の未証明辺37本、新規二石root閉鎖0件。**標準11×11空盤はUNKNOWN**。
