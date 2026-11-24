# 2026-11-24 Part DD drive-2: CU→DB waypoint の正準S5 chain 拡張監査（読み取り専用）完了

対象: drive-1 (commit 048b69c5) で確立した独立TS監査を、Part DB (batch-29 37 LOSS canonical adoption) の landing に
よって新たに出版された waypoint DB（6,354行, sha256 04b0a23987a9...）へ1区間拡張したもの。単一オーナー、読み取り専用、
計算レーン（Part DA/CY/CP/CX等）への干渉なし。observed HEAD c2572cb5 時点で実行。

## 結果: ALL GATES PASS

1. CU (6,317行, 30ddad9d...) が DB (6,354行, 04b0a239...) の strict subset（subset 不一致 0、欠落キー 0）。
2. DB−CU の delta 37キーは increment-b29loss37-20261124（37キー）と完全一致（キー集合・verdict・per-key nodes、
   base 内既存キー 0）。27行ではなく37行の採用分が正しく反映。
3. delta の 37行はすべて LOSS。WIN 計数は 158 のまま不变で、probe-level WIN ab028 はどこにも消費されず cache 外の
   まま（zero-WIN-consumed adoption の出版主張と独立に整合確認）。
4. increment の nodes 総和 159,325,566 == manifest の total_nodes_pass_one。
5. DB merged cache の sha256 は DB MANIFEST-sha256.txt の登録値・知見pin (04b0a239...) と一致、DB manifest の
   base_cache_sha256 は CU pin (30ddad9d...) と一致、merger pin 90711961... 確認。
6. 検疫 2 キーは DB にも不在。git-blob チャネル整合（再計算 == 報告、全6取得ファイル）・ASCII-only 確認。

## 出版 (全 fetch-back byte 一致)

- commit d4564f98: research/experiments/n11-centralreply-chain-integrity-tsaudit-20261124/ に
  scripts/audit_chain_integrity_drive2.ts (15,082B, sha256 91a75d3b...)・output/audit-report-drive2.json (4,236B, f22912dc...)・
  output/audit-summary-drive2.txt (1,329B, 3b91d9b6...)・README.md 更新 (4,809B, ca3fe977...)・MANIFEST-sha256-drive2.txt (468B)。
  drive-1 の4ファイルは不変（MANIFEST-sha256.txt の pin が依然有効）。
- push 直後に5ファイル全件再取得し sha256 をローカル再計算と照合、byte 一致を確認。本 log も同様に fetch-back 検証する。

## 観察（非阻塞・記録のみ）

- increment-b29loss37 のヘッダーコメントには「(Part DA, 2026-11-24)」と書かれているが、採用 Part は DB へ改名済み
  （knowledge 記録のとおり DA→DB 改名エピソード）。verdict・キー・pin はすべて正しく、単なるコメント内の旧称。

## Interpretation Guard

本監査は chain-trust の強化のみを主張する。勝敗の前進・verdict 消費・class status 変更は一切ない。正規11×11空盤、
19個の central-reply root、二石root、S2、class 2251 はすべて UNKNOWN のまま。batch-29 の全54キー（WIN ab028 を含む）
も verdict としては UNKNOWN のまま。nodes は bookkeeping であり勝敗でも距離でもない。

## 次の拡張点

次の adoption waypoint（例: batch-30/31 の採用）が出版されれば DB→(新waypoint) の同一手順での検証を追加する。
