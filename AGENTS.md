# AGENTS.md

このファイルは、このリポジトリで作業する人間・LLMエージェント向けの運用規約です。
数学的なschemaの詳細は `research/knowledge/SCHEMA.md` と `research/knowledge/VOCABULARY.yaml` を正本とします。
この文書では、複数エージェントが並行して研究・整理・検証するときに、どこへ何を書き、何を正本とし、どう統合するかを定めます。

## 1. 基本原則

研究情報を次の役割に分離します。

- `research/knowledge/items/`: **現在の知識の唯一の正本**
- `research/experiments/`: **再現可能な実験・入力・出力・監査**
- `research/log/`: **発見順・判断・失敗・引き継ぎなど研究の時系列**
- `research/archive/`: **旧仮説帳・旧計画・supersededなまとめ・歴史的監査**
- `docs/`: **現在有効なreader向け説明**
- `results/`: **公開・横断集計のmachine-readable output**
- `cpp/`, `scripts/`, `rust/`, `Kyouen/`: **共有実装・検証器・形式化**

同じ数学的結論を複数の場所で「現在の結論」として並行管理しないでください。
experiment・log・archive・docsに記述があっても、現在のstatus・量化範囲・検証境界はknowledge itemを正本とします。

## 2. Knowledge itemの扱い

新しい定理、仮説、反例、計算結果、検証結果、定義、方式、未解決問題など、現在の研究状態として残す価値があるものは
`research/knowledge/items/Knnnn-content-slug.md`
として登録します。

### K番号

- mainに存在するK番号は永久IDとして扱い、意味の都合で付け替えません。
- 作業branch上で新規に付けるK番号は**仮番号**です。
- 複数branchで同じ新規K番号を使っていても構いません。
- 統合時にmainの既存番号と衝突する新規項目だけ再採番します。
- 再採番時は、ファイル名、front matterの`id`、新規項目間の`relations.target`、Markdown中のK参照をまとめて更新します。
- branch内だけで使った仮K番号をaliasとして残す必要はありません。
- 既存main項目のK番号は再採番しません。

### 状態更新と新規項目

- **同じ命題のstatusや証拠が更新された場合は、同じK項目を更新**します。
- 条件や量化範囲が変わり、数学的に別の主張になった修正版は新しいK項目にします。
- 別の主張が旧主張を置き換える場合だけ`supersedes`を使います。
- 「支持実験が増えた」「statusが変わった」という履歴だけのためにK項目を大量追加しないでください。
- 研究の状態変化の履歴は`research/log/`とGit履歴に残します。

### relation

relationは`SCHEMA.md`の向きで一方向だけ記述します。逆リンクは生成器に任せます。

特に次を混同しないでください。

- `depends_on`: 論理的・数学的に必要な前提
- `supports`: 有限計算・標本などによる支持。証明ではない
- `proves`: 記載した量化範囲全体を証明
- `refutes`: 反例・不可能性証明による否定
- `verifies`: 独立検査・形式検証
- `generalizes`: より一般の命題から特殊な命題への関係
- `supersedes`: 異なる現行知識による旧知識の置換

有限計算を無界命題の`proved`へ昇格させないでください。
「計算済み」「独立検査済み」「Leanで一般的健全性を証明済み」「具体的巨大証明書をLean核内で検査済み」は別の状態です。

## 3. Generated files

`research/knowledge/generated/` と root `README.md` の生成領域は**派生物**です。
現在知識の正本ではありません。

- generated fileを手で編集しないでください。
- 通常の研究作業では、まずknowledge itemsなどの正本を編集します。
- 複数branchを統合するときは、**K番号の衝突解消と正本側のmergeを先に行い、その後で一度だけ再生成**します。
- generated側でmerge conflictが起きた場合、内容を手作業で統合するのではなく、正本の競合を解決してから再生成してください。
- branch単体でCIを通す必要がある場合は、最後の派生ステップとして生成物を更新して構いません。
- 複数branchのgenerated差分をそのまま足し合わせる必要はありません。

再生成:

```sh
uv run --locked python tools/knowledge/build.py
```

生成後は次が無差分になることを確認します。

```sh
git diff --exit-code -- README.md research/knowledge/generated
```

## 4. Research log

`research/log/` は「現在何が真か」ではなく、**どう研究が進んだか**を残す場所です。

新しいログでは、可能な限りファイル名に日付と内容を含めてください。

例:

```text
2026-10-04-n11-dfpn-investigation.md
2026-10-04-fixed-width-q5-followup.md
```

`Round 42` や `Cycle 17` のような番号だけを新しいログの主識別子にしないでください。
既存のRound/Cycle資料は歴史資料としてそのまま参照できます。

新しいログには、関連するK項目やexperimentへのリンクを可能な範囲で含めます。
ただし、K項目のstatusをlog側でも並行更新する運用にはしません。

ログに残す典型例:

- 何を調べようとしたか
- 何を試したか
- 失敗した方法と理由
- 判断が変わった理由
- 発見の順序
- 次に検討すべき点
- 関連K項目・experiment

## 5. Experiments

`research/experiments/` は再現可能性のための場所です。

- 実験固有のscript、入力、raw output、監査、preregistration、reportは実験単位の近くに置きます。
- 複数実験で共有するsolver・verifier・libraryをexperiment配下へ複製しません。共有物は`cpp/`, `scripts/`, `rust/`などに置きます。
- 実験reportの当時の結論を、現在のknowledge statusとして並行更新しません。
- 新しい複雑な実験は、可能なら実験ディレクトリに`manifest.yaml`を置き、最低限次を記録してください。

```yaml
title: ...
date: YYYY-MM-DD
related:
  - K....
commit: <40-character commit SHA>
programs:
  - ...
inputs:
  - ...
outputs:
  - ...
command: ...
```

既存実験には複数形式のmanifestがあるため、過去資料を無理に一括変換する必要はありません。
この規則は新規実験から徐々に適用します。

## 6. Artifacts

K項目の`artifacts`は、その知識を支える実ファイルへの参照です。

- repo内に実在するファイルだけを指定します。
- ディレクトリ全体、絶対path、外部URLはartifactにしません。
- `role`と有用な`note`を必ず付けます。
- 特定時点のコードや結果に依存する重要な証拠では、可能なら完全40桁のcommit SHAを記録します。
- 大量の実験ファイルを一つのK項目に列挙するより、manifestや代表reportへまとめて参照する方を優先します。

## 7. Archiveと旧資料

archiveや旧logにあるSUPPORTED、REFUTED、OPENなどのラベルを、そのまま現在のstatusとして採用しないでください。

- 旧資料は当時の一次資料・provenanceです。
- 現在の結論は対応するK項目を確認してください。
- 旧path文字列がhash receiptや移行記録に残ることはありますが、current executable pathとして復活させません。
- `night-research/` と `research/verification/` は再作成しません。

## 8. Docs

`docs/` は初見の読者向けの現在有効な説明です。

- 一回限りの実験report、preregistration、raw auditを置きません。
- 数学的な現在状態を詳しく重複記載するより、対応するK項目へリンクします。
- ルール、再現手順、証明方式、certificate形式、関連研究など、長く有効な説明を置きます。

## 9. 複数エージェントでの並行作業

並列作業の調整は、人間または親エージェントが行う前提です。
repo内に独自のタスク予約システムを増やす必要はありません。

並行性を保つため、次を優先します。

- 巨大な共有Markdownへ追記を集約せず、新しい知識は独立したK itemへ分ける
- 新しい研究ログも独立ファイルにする
- 新しい実験も独立ディレクトリにする
- generated fileは正本として共同編集しない
- 同じ既存K項目を複数エージェントが同時編集する場合だけ、統合時に意味を確認してmergeする
- 研究ブランチの履歴そのものを研究記録にしない。必要な経緯はlogへ残す

## 10. Workflowと長時間計算

未知盤の長時間探索・probe・sweepを通常pushで不用意に起動しないでください。
探索系workflowは、明示的に継続運用すると決めた回帰検査を除き、原則として`workflow_dispatch`など手動起動を使います。

リファクタリング、文書整理、path変更だけで未解決探索を再実行しないでください。

## 11. Merge前の確認

knowledgeやresearch構造に触れた場合、統合担当はK番号衝突を解消した後に少なくとも次を実行します。

```sh
uv sync --locked
uv run --locked python tools/knowledge/check.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
uv run --locked python tools/knowledge/build.py
git diff --exit-code -- README.md research/knowledge/generated
```

コードや形式化も変更した場合は、変更範囲に応じて既存のCMake、Rust、Lean、certificate回帰も実行します。

検査器が通ることは、数学的結論そのものの正しさを保証しません。
新しい主張については、本文に対象範囲、根拠、検証境界、既知の限界を明示してください。

## 12. 迷ったときの判断基準

- 「現在、何が分かっている？」→ `research/knowledge/items/`
- 「なぜそう分かった？」→ K itemのrelations / artifactsから辿る
- 「どう再現する？」→ `research/experiments/`
- 「研究がどう進んだ？」→ `research/log/`
- 「昔は何と言っていた？」→ `research/archive/`
- 「初見の人へどう説明する？」→ `docs/`

分類に迷った場合は、同じ情報を複数場所で正本化するのではなく、最も適切な一か所を正本にして他からリンクしてください。
