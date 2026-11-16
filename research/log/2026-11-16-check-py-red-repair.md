# 2026-11-16: check.py 連続失敗（run #21〜#50）の根絶 — stale 生成ビュー・presweepメタデータ・logリンクの一括修復

## 発見

refresh-generated-views.yml の run #21（2026-11-15 21:46Z・起点コミット 4c073bee）以降、
run #50まで全て step 42 `tools/knowledge/check.py` が失敗し続けていた。CIログ（API経由の
step要約）と、main HEADを38kファイル・ミラーして tools/knowledge の checked() を
ローカル再実行した結果、失敗は9件のlayoutエラーに集約された:

1. `scripts/next_target_presweep_head1435_20261116.py` L309 —
   `"path": "scripts/recompute_frontier_cost64d_receipts_20261116.py"` がrepoルートに存在せず
   layout checker の missing source/runner path。
2. `next_target_presweep_head1435_v2_20261116.py` L351（同一名の文字列）。
3. `next_target_presweep_head1438_20261116.py` L417（cost64f版）。
4. `next_target_presweep_head1441_20261116.py` L567（cost64g版・07:40以降の並走pushで追加）。
5-7. 生成ビュー index.md / artifacts.md / relations.md の
   `../items/K0869-p2647-size1322-three-class-drat-audit.md` へのbroken link
   （K0869 ID衝突修復でitemがK0871再採番されたが生成ビューが05:54Z（31dcedd2）のままstale）。
8-9. `research/log/2026-11-16-k0869-id-collision-repair.md` 内の、リテラル「...」付きで
   存在しないパス `K0869-p2647-...`・`K0871-p2647-...` へのmarkdownリンク2件
   （broken link — 修復ログ自身が新規エラーを発生させていた）。

構造的な根因: 両workflowとも `check.py` が `build.py` より先に走るため、
itemリネームを伴うpush後に生成ビューがstaleになると、check.pyが失敗して
build.pyが永久に実行されない（自己修復不能のデッドロック）。
06:00ZのK0869衝突修復は「CIのretryループが生成ビューを再生成する」と期待していたが、
この順序では再生成は決して起きない。

## 修復（本コミット）

1. **4 presweep script**: ピンrecord metadataの `"path"` をrepoルート相対の実在パス
   `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost64[d,f,g]_receipts_20261116.py`
   に修正した。実行系（`SCRIPTS / "..."` のPath結合）には影響しない metadata のみの修正。
2. **衝突修復log**: L29 の2リンクをmarkdownリンクからコードスパンに変更した
   （frozen_links.json は research/experiments 配下 .md のみ対応のため、logではコードスパンで記録）。
3. **生成ビューの再生成**: 現在の856 itemから index / aliases / relations / summary
   の4ビューを全量再生成したほか、artifacts.md は連携ツールの1コミット容量上限のために
   先頭1,200,045 bytes（artifactパス辞書順で `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-raw-batch6-20261115.jsonl` のセクション直前まで、9,787行）で
   切った版を公開した（切断位置はセクション境界"\n## ["で、リンク整合性は全量検証済み）。残り後半とK0875以降の追記は
   check.py 通過後に走る refresh-knowledge-generated.yml の build.py が全量を正規再生成して
   コミットするため、そこで正本に置き換わる。solutions.md と README.md の解決状況ブロックは
   内容が不変のため変更なし。
   PyYAMLが利用できないサンドボックスでは、tools/knowledge/common.py・layout.py・build.py を
   忠実に移植したローカル実装（mini-YAML parser込み）で生成した。
4. workflow末尾にtrigger commentを追加した。

## 生成内容の検証（byte-fidelity）

ビューの信頼性を担保するため、31dcedd2（05:54Z・生成ビューの最終更新コミット）時点の
851 itemを全件取得して同一パイプラインで再生成し、mainの生成ビュー6件と
ルートREADME.md 全てについてバイト完全一致を確認した（mini-YAML parser の
引用スカラー複行折り返し・` #` コメント終端・`key: #comment` の3件の差異を
この検証で検出・修正して一致に至った）。修復後の main HEAD 相当チェックは
855 item・0 error・0 warning。

## 残る既知の挙動

- refresh-knowledge-generated.yml run #176（63c5443a起点）はチェックアウト時点で
  staleビューを含むため、監査ステップ通過後も check.py で失敗する見込み
  （本コミット以降のrunでは通過する）。
- itemのリネーム・削除を伴うpushでは、生成ビューを同時pushしない限り
  このデッドロックが再発する。恒久対策としては workflow で check を build の後に
  走らせる、または check.py のみの軽量workflowをpushごとに先行実行することが有効。

## ツール

- `/home/user/ci-diag/check_local.py`（common.py/layout.py のローカル移植+mini-YAML）・
  `build_local.py`（build.pyの移植）・`gt_test.py`（31dcedd2 に対する回帰検証）は
  サンドボックス内のみの資材（repo外）。

## 完了確認（2026-11-16 09:23Z 正本landing）

- 切断版 artifacts.md（1,200,045 bytes・9,787行）を 7761ceea でpushした後、62031291 の
  trigger comment で再発火した refresh workflow の commit step が正本の全量
  artifacts.md を再生成・commitし、`docs: refresh generated knowledge views`
  （37b9a1ed・09:23:46Z）としてlandingした。同コミットの差分は +7,014行・削除0行で、
  切断版の9,787行が canonical 再生成の行完全prefixであることをCI側の git diff が機械確認した。
- run 7971（Knowledge integrity・7761ceea起点）は check.py・unittest・build.py が全て通過し、
  失敗は最終段階の `git diff --exit-code`（切断版と正本の差分検出）のみだった。
  すなわち check.py 自体は本修復で green に復帰済み。
- refresh run #53（refresh-generated-views.yml・62031291起点）は success。run #180
  （refresh-knowledge-generated.yml・同起点）は監査継続中で、commit step は最新mainで
  生成ビューがcurrentであることを確認して正常終了する見込み。
- GITHUB_TOKEN による push は後続workflowを発火しないため 37b9a1ed 自身には run が
  存在しない（check-runs total=0）。本コミット以降の main へのpushで Knowledge integrity が
  green になれば本修復は完全確認となる。
