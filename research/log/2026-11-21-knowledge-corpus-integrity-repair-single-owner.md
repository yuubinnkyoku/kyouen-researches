# 2026-11-21 Knowledge corpus integrity修復の単一オーナー宣言（クラスA/B/C一括実行）

## 宣言

- 本ノートを出版するレーン（knowledge corpus integrity修復レーン）は、
  `research/log/2026-11-20-knowledge-integrity-inventory.md` が列挙した
  クラスA（plain scalar 内 ASCII ": "）・クラスB（front matter未閉鎖）・
  クラスC（id重複=後着再採番）の**修復実行の単一オーナーを宣言する**。
  並走レーンはこの修復を重複して実施しないこと（K1067再採番ノートと同一手続き）。
- これは11-20インベントリの「各所有レーンが自itemを修正することが望ましい」との
  運用を、修復専用レーンが一括で肩代わりするものである。各itemの数学的主張・
  実験結果・artifacts・文面は一切変更しない。変更はロード可能性と番号衝突の
  解消のみ（引用符付与・fence挿入・id再採番・参照付け替え）。
- 修復対象は2026-11-21T08:45Z頃のmain codeload tarball全数検査
  （3,395,570,577 bytes・items 1,179ファイル）で確定した:
  - クラスA 32ファイル（load error: plain scalar contains ": "）
  - クラスB 9ファイル（load error: missing front matter。
    先頭fence欠落4 = K1190-K1193、閉じfence欠落5 = K1046/K1057/K1059/K1088/K1148）
  - クラスC 4組（duplicate id: K0936/K0974/K0975/K1149）
  - 副次的発見: K1059のartifact path 2箇所とfront matter本文1行が
    出版時にハードラップされており、`.mjs`監査機参照が2行に分断されていた
    （断片joinで復元。パスはtree全体と照合）。
- 変更方式（全て最小差分・意味保存）:
  - A: 該当plain scalarを二重引用符でwrap（`\`→`\\`・`"`→`\"` エスケープ。
    ASCII ": "は保持）。複数行scalar・seq item（aliases等）も同様。
  - B: 先頭`---`付与（4ファイル）・閉じ`---`挿入（5ファイル。K1059は本文
    「## 追記」直前、他4件はEOF）・K1088のみschema外field `summary:` を
    正規field `evidence:` へrename（内容不変）。
  - C: 後着4itemを空き番号へ再採番（下記）。参照relationのtarget付け替えは
    target意味論を指す側の文面で判定した。
- **11×11の勝敗は本作業の対象外であり一切変更しない**。標準11×11空盤・
  二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて**UNKNOWNのまま**。
  REFUTED-D10はLOSS証明ではない。nodes数・solved数・win8証明書の存在を勝敗と
  読まない（規約は各itemの「解釈規約」sectionのまま）。

## クラスC再採番の詳細（後着をK1198-K1201へ）

空き番号確認（三点検査: item 404・README/text言及0・repo全ファイル名に存在しない）を
2026-11-21の最新main tarballで実施済み。初回出版時刻はGitHub path別commit履歴
（全commits取得・最古 commit date）で確定した:

| 後着item（再採番先） | 後着初回出版 | 先着item（番号不変） | 先着初回出版 |
|---|---|---|---|
| K0936-two-token-z6-y25-boundary → **K1198** | 11-17T20:22:53Z | K0936-remo-sieve7-uv-mod210 | 11-17T20:09:58Z |
| K0974-p2207-full-drat-audit → **K1199** | 11-19T01:21:24Z | K0974-two-token-z6-y-ge4-full-grundy | 11-18T16:32:52Z |
| K0975-p3251-full-drat-audit → **K1200** | 11-19T01:21:24Z | K0975-two-token-z6-uniform-independent-verification | 11-18T16:55:09Z |
| K1149-six-row-q5-q6-deficient-witness-band-extension → **K1201** | 11-20T14:31:45Z | K1149-n11-replace9-sweep-reexec-second-verification | 11-20T14:30:20Z |

relation target付け替え（target意味論は指す側のrelation noteで判定）:

- K0938-two-token-z6-y26-boundary: depends_on K0936→**K1198**
  （note「z=6,y=25全Grundy公式」= 後着two-token切片を指す）
- K0693-p2207-no-parabola-equality-witness: depends_on K0974→**K1199**
  （note「全1,103 d のDRAT監査」= p2207 drat-auditを指す）
- K0708-p3251-no-parabola-equality-witness: depends_on K0975→**K1200**
  （note「全1,625 d のDRAT監査」= p3251 drat-auditを指す）
- 付け替え不要（先着を指す）: K0975-two-token-z6-uniform からK0974へのverifies
  （note「K0974式（レポート逐語実装）」= y≥4全Grundy公式を指す）、
  K0976-two-token-z7-y-ge4-conjecture からK0974へのdepends_on（同左）、
  K1159からK1149へのverifies（replace9掃引第二検証を指す）。

knowledge README（手書き管理領域）の付け替え2箇所:
行43「y=25は[K0936](items/K0936-two-token-z6-y25-boundary.md)」→
「[K1198](items/K1198-two-token-z6-y25-boundary.md)」、行332 bullet
「（[K1149](items/K1149-six-row-q5-q6-deficient-witness-band-extension.md)）」→
「（[K1201](items/K1201-six-row-q5-q6-deficient-witness-band-extension.md)）」。
p2207/p3251両itemのREADME bullet・表示idは存在しない（generation観点の確認済み）。

## 実行環境とその限界（ 重要: 公式検査との関係）

- 本レーンのsandboxは **pip/uvによるPyYAML導入が禁止** されているため、
  公式 `uv run --locked python tools/knowledge/check.py` を実行できない。
  代替として、check.py（load_items + validate + tree全体とのartifact照合）を
  忠実移植した PyYAML-free 検査器 `census_v3.py`（YAMLサブセット解釈器
  `yamlmin.py` 付き）を使用した。チェックには
  `research/experiments/knowledge-corpus-integrity-repair-20261121/` に
  検査器・census before/afterを公開する（2026-11-17修復logと同じ手法。
  2026-11-17実績では、同種の移植検査器がviews再生成のbyte一致で裏付けられた）。
- よって「公式check.pyがgreenになった」ことの確認は**完了していない**。
  uv環境を持つ所有者（人間またはレーン）による
  `uv run --locked python tools/knowledge/check.py` → unittest → build.py →
  `git diff --exit-code` の実行・確認が残務（下記「残務」を参照）。

## 結果（2026-11-21のmain全数census）

| 指標 | 修復前（main） | A/B修復後 | A/B/C修復後 |
|---|---|---|---|
| load errors | 41（A32+B9） | **0** | **0** |
| validate errors | 533 | 513 | **509** |
| duplicate id | 4 | 4 | **0** |
| unknown relation target | 107 | **0** | **0** |
| warnings | 15 | 19 | 19 |

- 修復前の41ロードエラーのファイル集合と11-20インベントリのA/BClass列挙の
  差分: 該当リスト掲載の8ファイル（K1063/K1069/K1070/K1071/K1072/K1075/
  K1151/K1153/K1155の一部）はインベントリ後に他レーンが修復済みであった
  （本レーンのcensusでは既にエラーなし。新規出版のK1196が同じAパターンで
  追加されていたため総数は41で同数）。
- **残るvalidate errors 509件はクラスE（schema・語彙の別系負債）と
  クラスF（実在しないartifact path参照4件）であり、本修復の対象外**。
  クラスE内訳の主要項: `artifact must be a mapping` 115、
  `unknown artifact role` 100、`unknown relation type: related` 62、
  `invalid relation mapping` 36（`relations: - depends_on: [K...]` 形式）、
  `invalid kind: experiment/theorem` 31、`unknown fields: date/tags` 50、
  topics不正 59、`unknown topic: frontier-bookkeeping` 16。
  これらはVOCABULARY.yaml拡張か項目書き換えかの**schemaガバナンス判断を要する**
  ため、別議として次回以降に提起する（本修復とは分離して記録する）。
- クラスD（generated views停滞・root README解決状況ブロック停滞）も
  「残る赤」である（build.py再生成にはuv環境が必要）。

## 残務（次回以降・他レーン歓迎）

1. uv環境での公式確認: `uv run --locked python tools/knowledge/check.py`
   （load 0・クラスE残留の予想エラー数）、unittest、`build.py`
   （クラスD解消）、`git diff --exit-code`。
2. クラスEのschemaガバナンス判断: VOCABULARY.yaml拡張（1行差分・全項目編集不要）
   vs 該当項目（ remo系・機械生成系を中心に~130項目超）の書き換え。
3. クラスF: `n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/scripts/`、
   `n11-residual72-verdict-sweeps-reexec-third-verification-20261120/fresh-runs/`、
   `n11-win8-receipt-source-record-census-20261121/scripts/win8_receipt_source_record_census.py`、
   `three-row-q4-frontier-20261121/output/wit_3x23_outer_4.witness.json`
   の実在確認（パスtypoか未出版かを目視で判定）。

## 変更対象外の明記

- 41ファイルの本文（fence再構築でbodyが空になった場合を含め）の文面・
  数値・主張は1文字も変更していない（引用符・fence・id・参照付け替えのみ。
  41ファイル全件でスペース・引用符・backslash・fence行を除去した正規化
  比較が byte一致、K1088のみ `summary`→`evidence` の5文字変更＝意図的rename）。
- 削除する4旧itemファイル（K0936/K0974/K0975/K1149後着）はgit履歴に保持される。
- log・experiment是一次資料（11-17修復log・11-20インベントリを含む）は書き換えない。
