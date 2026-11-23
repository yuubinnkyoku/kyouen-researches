# 単一オーナー宣言: Part CS — batch-28 (class 5343) remaining-EXHAUSTED 4行の高budget (25M) 再probe着手 (2026-11-23)

**publish-then-execute規約に従い、本宣言の出版後にのみsolver実行を実行する。**
対抗宣言の機械確認: 宣言直前の最新main (observed HEAD `fb1c540d`) に
EXHAUSTED残4行 (aa021/aa028/aa032/aa050) への高budget (25M) 再probe着手宣言は存在しない
(直前のPart CQ完了log `c584e078` は「higher-budget (25M等) 再probeは別宣言条件でopen」と
明記・Part CR/K1274/Part CI/Part CPは非接触の別レーン)。単一オーナー規約により、
本Partの実験dir・outputsへの他セッションの接触を要求しない (停滞時はtakeover規約)。

## 対象と鍵集合 (機械抽出・手選定なし)

Part CQ (20M再probe・完了log `research/log/2026-11-23-part-cq-b28exhausted-reprobe.md`)
によりbatch-28 EXHAUSTED残は11行→4行。対象はpublished Part CQ audit
`n11-centralreply-c5343-b28exh-reprobe20m-audit-v1` (output/audit.json sha256
`6227eb2cfeb14c31799d94f19436c07233d55c8301d8640ee266b8cc3a366692`・commit-pinned
`962348f9` でfetch・ローカルkit生成物とcmp byte一致) の still_exhausted_rows
= {aa021, aa028, aa032, aa050} のpinそのまま。base cache (Part CO canonical
`854800f3…` 6,301行) に4キーとも不在 (0/4 hits・maker G7で機械検証済み)。

## 条件

- **新condition budget 25,000,000** (published 15M・published Part CQ 20M とは別条件)。
  derived runner `runbatch_b28exh25m.sh` (`9048c3291d981d52c846bc177bb727f95827d88892c6fd44ae84c5a110b4ac1c`)
  は published runbatch.sh (`f591f8c2…`) の **EXACTLY 1行diff**
  (`BUDGET=15000000` → `BUDGET=25000000`)・stop rules/完全性guard/p2-pass fresh-cold設計不変。
- **no-same-condition-re-search規約は無傷**: published 15M exhaustion行も published CQ 20M
  exhaustion行も同一条件では再実行しない。
- 2-pass fresh-cold per key・determinism mismatchは即HARD-STOP (rc=42)。
- WINDOW-EXCEEDED規則 (事前登録): 同一passのTRUNCATED-RETRY 2回でそのキーはskipし
  honest unresolvedとして監査に記録 (silent dropなし)。260s inner window継使用
  (25M exhaustion推定~136s/pass・runnerのfile-existence resumeで1-3 invocation/キー)。
- WIN-CONTINUE (Part CE/CK/CN/CQ先例): WIN行 (rc=45) でorchestrationは停止しない。
  EXHAUSTED行 (result 0) はhonest UNKNOWNとして継続。

## 事前登録 (プロトコル・事前に全部開示)

1. **A scaffold**: 実験dir `research/experiments/n11-centralreply-class5343-b28exhausted-reprobe25m-20261123/`
   に kit 35 files (scripts 6 / input 8 / sources 12 / val-gate 8 / README) を出版。
   jsreplay.js `84585617…` (published byte-clone)・runbatch.sh `f591f8c2…` (参照用)・
   derived runner `9048c329…`・maker `d769540b…` (G1-G7 fail-closed・byte-stable)・
   session step `cbab0017…`・audit `9722ca42…` (schema
   `n11-centralreply-c5343-b28exh-reprobe25m-audit-v1`)。
2. **val-gate fresh 4** (宣言後): at2m×2 budget 2,000,000 (exhaustion nodes 2,000,000)・
   15m×2 budget 15,000,000 (nodes 3,651,923 / 5,040,200)・published baselinesと
   node-exact (f6/f7一致・f8 wall_s比較外)。
3. **anchors** (宣言後・derived runner 25M): aa036 → result 2 nodes 955,659 (PASS行のみ)・
   aa004 → result 1 nodes 15,616,012 (PASS + WIN-HALT rc=45)・published値とnode-exact必須。
   anchor基準sourcesはpublished CQ raw (maker G5 pin)。
4. **targets 4キー** (宣言後): session step 1 invocation 1キー進行で4キーまで。全キー2-pass
   fresh-cold・mismatch 0を要請。解決nodes期待値は事前宣言しない
   (EXHAUSTEDならnodes=25,000,000 2-pass一致)。
5. **audit** (宣言後): `audit_cs.py` 3回実行 stdout+audit.json byte-identical・
   tamper電池4件 (p2 nodes改変→p1/p2不一致 / result反転→status照合 / replay_done削除→
   truncated捕捉 / registry `reprobe_condition.budget` 改変→gate A捕捉 ※CQ教訓: 改変先
   フィールドはregistry schema機械確認の上指定) + clean control・各probe復元cmp。
6. **出版**: B outputs (status.log + raw + val-gate .cs-host.out + audit.json) → C README最終 +
   MANIFEST-sha256 → 完了log。push毎にobserved HEAD再取得 + commit-pinned fetch-back
   byte照合。**11×11未解決ならUNKNOWNと明記**・nodes数を勝敗として読まない。

## verdict不消費

WIN/LOSS行はprobe-level honest labelsのみ。canonical adoptionは別宣言adoption Part
(pinned fail-closed merger `90711961…`) 経由のみ・WIN行はscrutiny owner C++第二実装
gate `9193f5b6…` 待ち。本Partはいかなるadoption・closure・secured・root勝敗の主張もしない。
**標準11×11空盤・class 5343・全キーは現在もUNKNOWN。**
