# 2026-11-17 Knowledge integrity赤化の完全診断と修復

## 観測

Knowledge integrity workflowは2026-11-16T13:33Z以降少なくとも386 run連続で失敗していた。失敗stepは `uv run --locked python tools/knowledge/check.py`（run 43986345711、head 2007c607）。2026-11-17T00:29Z以降は全ワークフローrunがqueuedのまま開始されていない（runner側の環境障害の疑い。ここからは修復不能、記録のみ）。

## 診断方法

check.py（load_items・validate・layout_errors）を正確に移植した単独検査器で、mainスナップショット（codeload tarball、2026-11-17T01:14Z時点、39,220ファイル）全体を検査した。front matterはYAMLサブセット解析器（複数行plainスカラー・複数行quotedスカラー・`>-`折り畳み・flow list・同一インデントsequence対応）で解釈し、867個の整形式項目すべてが解析可能なことを確認したうえで、validateの全規則とlayout_errors（全4137個の.md相対リンク、全3018個の.py構文とSOURCE_PATH、321個のworkflowのworking-directory、frozen_links.json、legacy dir不在）を再現した。artifact path 5,295件は全て実在（raw CDN全件200・404ゼロ）。generated viewsがK0875で停滞しており14項目分（K0876-K0892）古いことも判明した。

移植検査器の忠実性は、K0875までのコーパスで再生成したviewsがmainの現行viewsと、view生成後に項目編集されたことによる差分（K0873のstatus更新、K0636向けrelation note追加、K0783へのartifact追加、K0797/K0800のsolution note更新）以外でbyte一致することで確認した。

## 見つかったcheck.pyエラー（8件）

1. `research/knowledge/items/K0879-two-token-z6-y3-boundary.md`: front matterの閉じ`---`が存在しない（missing front matter）
2. `research/knowledge/items/K0885-two-token-z6-y6-boundary.md`: 閉じ`---`がEOF末尾にあり直後の改行がないため区切り正規表現に不一致（missing front matter）。本文が出版時に欠落していた
3. `K0880`: relation target K0879がunknown（1の帰結）
4. `K0887`: relation target K0885がunknown（2の帰結）
5. `K0880`本文の `../experiments/vertical-fiber-two-token-z6-y4-boundary-20261117/report.md` はdepth不足でbroken local link
6. `cost64h_sweep_audit_20261116.py`: docstring・メタデータ中の `scripts/legal_candidates.py` がrepo root基準のSOURCE_PATH検査でmissing（実験相対表記を実装がrepo絶対と解釈）
7. `preregister_cost76d_77e_fold_20261116.py`: 同様に `scripts/fold_projection_head1450_tool_20261116.py`
8. `update_claim72d_v2_20261117.py`: 同様に `scripts/audit_cost72d_raw_batches_20261117.py`

最初の失敗（13:33Z）はcost64h aux出版群（13:30-13:35Z）と時刻が一致する。6-8は兄弟scriptを実験相対の `scripts/...` で参照した文字列で、実体はいずれも同experimentの `scripts/` 内に存在する。

## 修復（最小限の外科的修正）

- K0879: 本文直前に閉じ`---`を挿入しfront matterを確定。本文は無修正
- K0885: 閉じ`---`に改行を付与し、front matterのevidence・artifact noteに記載された事実のみで構成した本文（概要・参照・限界）を追加。数学的主張の新規生成なし
- K0880: report.mdへのリンクdepthを `../../experiments/` に修正
- 3 script: 参照文字列を実在するrepo相対完全パスに書き換え（意味は不変、該当scriptは同experimentのscripts/配下）
- generated views 6ファイルとREADMEの解決状況ブロックを870項目全てから再生成

## 修復の検証

- 修復後スナップショットでcheck.py相当（load+validate+layout_errors移植）がエラー0・警告0
- 修正対象外の867項目はpush直前の最新mainとgit blob sha完全一致（views再生成の入力が正しいことの確認）
- K0879/K0885/K0880と3 scriptは、push直前にCDNから再取得した最新実ファイルへ同じpatchを適用した結果と一致
- READMEとgenerated 6ファイルはpush直前のmainと同一（views停滞の裏付け）

## 限界・未検証

- 本修復で解消するのはcheck.py stepとbuild+views diff stepの失敗要因。workflow内の各verify.py・audit.jsonの `git diff --exit-code` stepはrunner復旧後に別途確認が必要
- K0885の本文はfront matter由来の要約であり、完全な署名表・証明はreport.mdを参照する構造
- runner停止（00:29Z以降queued）は外部的要因で、こちらからは修復不能
- 11x11空盤の勝敗は本件と無関係にUNKNOWNのまま
