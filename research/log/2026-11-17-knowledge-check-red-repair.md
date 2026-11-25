# 2026-11-17：check.py赤修復 — 引用符なしスカラー内のASCII ': '（6 item）と role: audit（3 item）を修正

開始時状況: 「Knowledge integrity」workflowが2026-11-17 02:58:39以降すべてfail（失敗stepは `uv run --locked python tools/knowledge/check.py`）。mainの全884 itemを実パースして原因を完全特定したところ、load error 6件とrole語彙error 3件はすべて本高速レーン系列のitemで、他877 itemは構造的に完全クリーンだった。

## 成果1：原因の完全特定（main全884 itemの実パース監査）

mainの全884 itemをダウンロードし、PyYAML（UniqueLoader相当の重複キー検査つき）でtools/knowledge/check.py の load/validate ロジックをローカル再現:

- **load error 6件**: 引用符なしYAMLスカラー内のASCII ': ' は `mapping values are not allowed here`（ScannerError）。該当は K0895 title（STASIS: r=9→r=10…・02:58の赤の起点）・K0897 title（STASIS3: ）・K0898 title（STASIS4: ）・K0900 notes 3箇所（修正(a)適用（…）: ・修正(a)適用: ×2）・K0902 title（FL wraparound集合等式: r13↔r10差…）・K0906 note（補題FLの成立域を確定: …と集合内壁記法 {c mod r : c∈E}）。
- **validate error 3件**: K0902/K0904/K0906 の監査JSON artifactの `role: audit` はVOCABULARY.yaml のartifact_roles語彙に存在しない（repo慣例は監査JSONにも role: data・K0860..K0905はすべてdata）。
- relation target不在・循環・kind/status語彙・必須キーは全884 itemで違反0。

## 成果2：修復と全item再検証

- 6 itemのスカラー内ASCII ': ' を全角'：'に置換（8箇所・意味変更なし）。K0906のscopeは単引用符付きでYAML上 safe なため保存し、非引用note側の同一数式のみ置換。
- K0902/K0904/K0906 の `role: audit` を `role: data` に修正。
- 修復後、main最新の884 item一式で load 0 error・validate 0 error を確認（artifact実在チェックのみrepo全体が必要なためローカル検証外）。

## 副次観察（修正せず記録のみ）

- K0797/K0800 の `solution.certificate` で値中の ' #' 以降がYAMLコメントとして黙って切り詰められている（load errorにならないデータ品質バグ・値は「全 (a,u) 全数走査による classMax = min_m max_{a,u}」で途切れる）。該当は別レーンの古いitemのため本項では編集せず、将来のmetadata正規化で直すべき観察として記録する。

## 反映

- 1コミットでmainに直接反映（branch/PRなし・repo方針どおり）: 7 item（K0895/K0897/K0898/K0900/K0902/K0904/K0906）+ workflow trigger comment + 本log。push前に最新mainを再取得し、対象7 itemとworkflowへの並走コミットがないことをファイルごとの最終touchコミット照合で確認済み。

## 次の課題

- 修復push後の「Knowledge integrity」再実行で、load errorに隠れていたlayout_errors（broken link等）が顕在化する可能性を監視する（CI queueは数時間遅延気味なため確認は次回実行に回す）。
- K0797/K0800のcertificate切り詰めをmetadata正規化の際に修正するか検討。
- K0902/K0906レジュームの「cap≤12残4スイープ」「広域版E集合の特徴づけ」は本修復の影響を受けず継続。
