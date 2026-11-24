# 2026-11-24 Part DD: 正準S5 cache連鎖の独立TS監査（読み取り専用）完了

対象レーン: n11 central-reply 正準S5 cache連鎖（CH→CO→CU）の非オーナー独立検証。単一オーナー方式、読み取り専用、
計算レーン（Part DB/CY/CP/DA/CX、K1277）への干渉なし。

## 実施内容

sandboxed TypeScript に sha256/sha1 をスクラッチ実装し（FIPSテストベクトル + 3系統の公開pin一致で実装正当性を决定）、
GitHub contents API 経由で公開済み正準chain 3 waypoint を全行再解析・再検証した。Python 不要・native host 不要・
solver 再実行なし・verdict 消費なしの独立監査。

- CH (6,294行): merged-exact-s5-chain-...-plus-b28loss1-20261123.cache, sha256 3124461b...
- CO (6,301行): merged-...-plus-b28loss7-20261123.cache, sha256 854800f3...
- CU (6,317行): merged-...-plus-b29loss16-20261123.cache, sha256 30ddad9d...（出版時点の BASE）

## 結果: ALL GATES PASS

1. 3 waypoint の行レベル解析: 6,294 / 6,301 / 6,317 行、スキーマ厳密 (stones=5, verdict∈{1,2})、bad row 0、
   重複キー verdict conflict 0。verdict 計数は公開値と完全一致（CO: WIN 158 / LOSS 6,143、CU: WIN 158 / LOSS 6,159）。
2. CH ⊂ CO ⊂ CU が strict subset として成立（共有キーの verdict・nodes 全一致、欠落キー 0）。
3. CO−CH の delta は increment-b28loss7-20261123（7キー）と完全一致、CU−CO の delta は increment-b29loss16（16キー）と
   完全一致（キー集合・verdict・per-key nodes、base 内既存キー 0）。
4. b28loss1 increment（aa003）は CH 内に verdict/nodes 一致で存在。
5. increment nodes 総和は manifest と一致（b28loss7: 38,784,669、b29loss16: 57,463,971）。
6. 検疫中 2 キー（results/n11-s5-evidence-quarantine.json）は 3 waypoint すべてに不在。
7. 公開 pin 11 gate 全一致（CH/CO/CU の MANIFEST、increments-manifest 内部 base_cache_sha256・sha256.loss、merger pin 90711961...）。
8. チャネル整合: 再計算 git blob sha1 == connector 報告値（取得全10ファイル）、ASCII-only 確認済み。

## 出版

- 実験: research/experiments/n11-centralreply-chain-integrity-tsaudit-20261124/（commit 048b69c5）
  - scripts/audit_chain_integrity.ts (17,431B, git blob a4457437)
  - output/audit-report.json (8,055B, git blob 449fa00e) 機械生成レポート
  - output/audit-summary.txt (1,241B, git blob b347b436)
  - README.md (3,509B, git blob 129bfe39)
  - MANIFEST-sha256.txt (357B, git blob b9b579c4)
- fetch-back 検証: push 直後に5ファイル全件を再取得し sha256 をローカル Calc と照合、byte 一致を確認済み。
- 本 log は出版後に fetch-back + sha256 照合で検証する（結果を本 log の最後に追記する運用は次回実施）。

## Interpretation Guard

本監査は chain-trust の強化（BASE 成果物の独立・クロス言語・クロスチャネル検証）のみを主張する。勝敗の前進や verdict
消費は一切ない。正規11×11空盤、19個の central-reply root、二石root、S2 はすべて UNKNOWN のまま。nodes は bookkeeping
であり勝敗でも距離でもない。

## 次の拡張点

Part DB (batch-29 37LOSS) adoption landing 後に新 waypoint（6,354行想定）が出版されれば、CU→DB の subset/delta 検証を
同じ手順で追加する（audit_chain_integrity.ts の拡張、pin は DB manifest から機械取得）。
