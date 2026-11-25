# Knowledge corpus integrity修復 2026-11-21（クラスA/B/C一括実行の機材とcensus）

## これは何か

`research/log/2026-11-21-knowledge-corpus-integrity-repair-single-owner.md`
（単一オーナー宣言）が実施した修復の再現機材と、修復前後の全数census
（main items 1,179ファイル）の正本である。

- 修復対象と基準commit: main codeload tarball（2026-11-21T08:45Z頃取得・
  3,395,570,577 bytes・items 1,179ファイル）。
- 修復内容: クラスA 32ファイル引用符wrap・クラスB 9ファイルfence再構築
  （K1088は `summary`→`evidence` renameを含む）・K1059のハードラップ3箇所
  （artifact path 2・block scalar本文 1）のjoin・クラスC後着4itemの再採番
  （K1198-K1201）とrelation/README付け替え3+2箇所。
- 実験の入力・出力の変更: なし（知識項目のロード可能性のみを変える修復で、
  数学的計算や探索は一切行わない）。11×11の勝敗はUNKNOWNのまま。

## 検査器（scripts/）

本sandboxはpip/uvによるPyYAML導入禁止のため、公式
`uv run --locked python tools/knowledge/check.py` の代わりに、check.py
（load_items + validate + tree file存在照合）を忠実移植した
PyYAML-free機を使う。greenコーパス誤検出ゼロ（2026-11-20校正済み
scanner `scan_frontmatter.py` と全ロードエラー件数・ファイル集合が一致）。

- `yamlmin.py`: PyYAML代替の忠実YAMLサブセット解釈器。plain/quoted
  scalar（複数行含む）・flow list・block seq/map・`>`/`|` block scalar対応。
  fail-closed: 想定外の構造は load error。
- `census_v3.py`: load+validateの全数census。`python3 census_v3.py <mirror_root>`
  （mirror_root は `research/knowledge/items/` と `VOCABULARY.yaml` と
  `tree_manifest.txt` [repo相対パス一覧] を含む）。検査器と同一 directory設置で実行。
- `repair.py`: 後述の追跡ループ修復機。`repair_targets.json` に対象
  ファイル名一覧。`repaired/` に修復済みファイルを出力する。
- `scan_frontmatter.py`: 2026-11-20インベントリ用の校正済み静的scanner（参照用）。

## 修復アルゴリズム（repair.py）

追跡ループ: censusと同一loaderでロードを試み、最初のエラー1件に
対して1つの最小修正を適用し、再ロードする（最大200周）。

- `plain scalar contains ": "`（key/seq item）: 該当scalarの開始行から
  終端までを特定し、二重引用符でwrap（`\`→`\\`、`"`→`\"` エスケープのみ。
  複数行scalarは開始行に開き引用符・終端行に閉じ引用符）。
- `missing front matter`:
  - 先頭fence欠落（1行目が `id:`/`title:`）: `---` を先頭に付与。
  - `summary:` があって `evidence:` がない: field名rename（K1088のみ）。
  - 閉じfence欠落: col-0 Markdown見出し（`## `）直前の空行群の前に
    fenceを挿入し、無ければEOFに付与。
- `orphan mapping`: 前行が `- path:` のpath断片、またはblock scalar
  内容行のcol-0断片（出版時ハードラップ）なら前行にjoin。
- 保全検証: 修復前後でスペース・引用符・backslash・`---`行を
  除去した正規化テキストのbyte一致（K1088のrename5文字を除く全41ファイルで確認）。

## census正本（output/）

| ファイル | 状態 | load errors | validate errors |
|---|---|---|---|
| `census-before-20261121.json` | 修復前main | 41 | 533 |
| `census-after-ab.json` | A/B修復後 | 0 | 513 |
| `census-after-abc.json` | A/B/C修復後（再採番含む） | 0 | 509 |

`validate errors` の残り509件はクラスE（schema・語彙負債:
remo系の別schema `relations: - depends_on: [K...]`・`date:`/`tags:`
未知field・`kind: experiment/theorem`・`role: document/record/...`
語彙外・`type: related/connects/...` 語彙外など）とクラスF
（実在しないartifact path 4件）であり、schemaガバナンス判断要のため
本修復では手つかず（宣言ノートの「残務」参照）。

`repair-report.json`: 41ファイルそれぞれに適用された修正の種別と位置の全記録。

## 再現手順

```
# 1) 最新mainをcodeload tarballで取得し items/VOCABULARY/README と
#    全ファイル一覧（tree_manifest.txt 相当）を <mirror>/ に展開
# 2) python3 census_v3.py <mirror>            # 修復前census
# 3) repair_targets.json（censusのload_errors由来）に対し
#    python3 repair.py                        # repaired/ に修复済みを出力
# 4) repaired/ を <mirror2>/ に反映して census 再実行
# 5) クラスCは宣言ノート表の再採番を適用後、census 再実行
```

uv環境では最終的に公式確認 `uv run --locked python tools/knowledge/check.py`
・unittest・`build.py`（generated views再生成）・`git diff --exit-code`
を実行すること（本sandboxでは実行不可・宣言ノートに明記）。

## 文責と解釈規約

- 本修復は知識インフラの整合性回復であり、いかなる盤面・クラスの
  勝敗確定もしない。REFUTED-D10はLOSS証明ではなく、foldは行被覆の簿記。
- 標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。
