# 2026-10-28 高速レーン：奇数中心・偶数星型のGrundy遷移

- 最新mainの `AGENTS.md`、`research/knowledge/README.md`、生成された未解決一覧、および既存の私有葉ゼロ3頂点の無限反例族を確認。
- 既存の「3本の二点型が各2個」という均一な星を、中心私有葉任意の正奇数、各枝の二点型任意の正偶数、追加クリーク頂点の私有葉任意の正偶数へ拡張。
- 枝数pと追加頂点数mについて、全称閉形式 g=1 (p=m=0), g=3 (p<=2かつp+m>=1), g=2 (p>=3) を初手全分類と数学的帰納法で証明。星次数3がこの族での鋭い境界。
- `research/experiments/game-structure/odd-center-even-star-sharp-transition-20261028/` に証明READMEと名前付き頂点の独立mex検証器を保存。局所実行で非均一129件・追加均一6件が全一致、最大57,044再帰状態。
- 証拠水準は数学的全称証明＋限定された有限独立照合。整数格子共円ゲームでの実現可能性は未主張。
- 全体CIとknowledge再生成の実行環境がないため、正本への昇格は保留。次は複数中心の偶数二点型星や星以外の二点型を混ぜたときの分類。

関連： [証明](../experiments/game-structure/odd-center-even-star-sharp-transition-20261028/README.md) ／ [検証器](../experiments/game-structure/odd-center-even-star-sharp-transition-20261028/verify_named.py)。
