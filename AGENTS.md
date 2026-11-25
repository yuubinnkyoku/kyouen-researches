# AGENTS.md

このrepoで作業するエージェント向けの運用規約です。
詳細なschema・語彙は `research/knowledge/SCHEMA.md` と `research/knowledge/VOCABULARY.yaml`、各領域の説明は対応するREADMEを参照してください。

## 作業前

- 最新の `main` を確認してから作業する。
- 原則として `main` に直接反映する。branch / PR は指示がある場合だけ使う。
- 古いREADME・log・archiveの記述より、現在の `research/knowledge/items/` を優先する。

## 置き場所

- `research/knowledge/items/`: 現在の知識の唯一の正本
- `research/experiments/`: 再現コード・入力・出力・監査
- `research/log/`: 発見順・判断・失敗・引き継ぎ
- `research/archive/`: 旧仮説帳・旧計画・歴史資料
- `docs/`: 現在有効な読者向け説明
- `results/`: 横断的なmachine-readable結果
- `cpp/`, `scripts/`, `rust/`, `Kyouen/`: 共有実装・検証器・形式化

現在の結論を複数の場所で並行管理しない。experiment / log / archive は当時の一次資料として保持し、現在のstatusに合わせて書き換えない。

## Knowledge item

新しい知識は `research/knowledge/items/Knnnn-content-slug.md` に置く。
項目の形式、status、relation、artifactは `research/knowledge/SCHEMA.md` に従う。

- 同じ命題のstatusや証拠の更新は、原則として同じK項目を更新する。
- 条件や量化範囲が変わり別の主張になった場合は、新しいK項目を検討する。
- 実験1回につき1 Kを作らない。後から独立して参照したい知識単位で分ける。
- 有限計算・観測・独立検証・数学的証明を混同しない。

### K番号

作業中の新規K番号は仮番号として扱う。複数作業で重複してもよい。
統合時にmain上の番号と衝突する新規項目を再採番し、その項目を参照する新規relationやMarkdown参照も更新する。
mainに既に存在するK番号は変更しない。

## Generated files

`research/knowledge/generated/` とroot `README.md` の生成領域は派生物であり、直接編集しない。

複数の変更を統合するときは、

1. 正本側をmergeする
2. K番号の衝突を解消する
3. 生成物を再生成する

の順に行う。generated側の競合を手作業で統合しない。

```sh
uv run --locked python tools/knowledge/build.py
```

## 並行作業

- 巨大な共有Markdownへ結果を集約しない。
- 新しい知識は独立したK項目、新しい研究記録は独立したlog、新しい実験は独立したexperimentとして追加する。
- 同じ既存K項目を複数作業が変更した場合は、統合時に内容を確認してmergeする。
- 作業割り当ては人または親エージェント側で管理し、repo内に独自のtask管理を増やさない。

## Workflow

未知盤の長時間探索・probe・sweepを通常pushで不用意に起動しない。
長時間探索系workflowは、明示的な指示がない限り手動起動のままにする。
リファクタリングや文書変更だけを理由に未解決探索を再実行しない。

## 統合前の確認

knowledgeまたはresearch構造を変更した場合は、統合後に少なくとも次を実行する。

```sh
uv sync --locked
uv run --locked python tools/knowledge/check.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
uv run --locked python tools/knowledge/build.py
git diff --exit-code -- README.md research/knowledge/generated
```

コード・verifier・Lean等を変更した場合は、変更範囲に応じた既存回帰も実行する。

## 構造変更

現在のSSOT構造を前提に作業する。
`night-research/` や `research/verification/` など旧taxonomyを復活させない。
新たな大規模リファクタリングは、不都合が実際に確認された場合だけ行う。
