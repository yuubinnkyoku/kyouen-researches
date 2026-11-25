# 単一オーナー宣言: Part CT — batch-28 (class 5343) 最終残EXHAUSTED 1行 (aa050) の高budget (30M) 再probe着手 (2026-11-23)

**publish-then-execute規約に従い、本宣言の出版後にのみsolver実行を実行する。**
対抗宣言の機械確認: 宣言直前の最新main (observed HEAD `41e3c3d6`) に
EXHAUSTED残1行 (aa050) への高budget (30M) 再probe着手宣言は存在しない
(直前のPart CS完了log `23d09513` は「30M等の別条件は新宣言必要・ただし30M exhaustionは
~163s/pass (当時推定) で260s inner windowを2-passで超えるため単発invocation設計では回収不能、
将来はinner window延長かp1/p2分割step設計が必要」と明記・Part CR/K1275は非接触の別レーン・
Part CP (batch-30 drive-2・宣言 `7aaa0525`) およびPart CI (batch-29・checkpoint `a5a159d7`) は
outputs停滞観察中だがtakeover無音基準 (3.5h・Part CI U/Z/CG基準) 未満で非接触)。
単一オーナー規約により、本Partの実験dir・outputsへの他セッションの接触を要求しない
(停滞時はtakeover規約)。

## 対象と鍵集合 (機械抽出・手選定なし)

Part CS (25M再probe・完了log `research/log/2026-11-23-part-cs-b28exhausted-reprobe25m.md`)
によりbatch-28 EXHAUSTED残は4行→1行。対象はpublished Part CS audit
`n11-centralreply-c5343-b28exh-reprobe25m-audit-v1` (output/audit.json sha256
`c6622d575f8379383856510caad1bffb6bd05bf047ba54a1589f7e01090e3796`・commit-pinned
`37c52cfb` でfetch・maker G8ゲートとcmp byte一致) の still_exhausted_rows
= {aa050} のpinそのまま。aa050 (lo `1152921504640401408`・hi `4228`・legal `94`) の
published exhaustion条件は 15M (Part CN drive-5 raw `4b9cb07b`/`a6e1fde6`)・
20M (Part CQ raw `8a0cbbfb`/`b410dfaa`)・25M (Part CS raw `44a9239d`×2) の3条件
(いずれも2-pass node-exact・nodes=budget)。base cache (Part CO canonical
`854800f3…` 6,301行) にaa050は不在 (0/1 hits・maker G9で機械検証済み)。

## 条件

- **新condition budget 30,000,000** (published 15M・published CQ 20M・published CS 25M
  とは別条件)。derived runner `runbatch_b28aa050-30m.sh`
  (`3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4`)
  は published runbatch.sh (`f591f8c2…`) の **EXACTLY 1行diff**
  (`BUDGET=15000000` → `BUDGET=30000000`)・stop rules/完全性guard/p2-pass fresh-cold設計不変。
- **no-same-condition-re-search規約は無傷**: published 15M / CQ 20M / CS 25M exhaustion行も
  同一条件では再実行しない。
- 2-pass fresh-cold per key・determinism mismatchは即HARD-STOP (rc=42)。
- **30M回収設計 (事前登録)**: published 25M pass wall実測131sから30M単発pass推定~157s。
  260s inner windowに単発passは収まるがp1+p2 (~314s) は収まらないため、
  **cross-invocation p1/p2 resume** (published runnerのfile-existence + truncated-sidecar
  guard・Part CSでaa050自体に実働実証済み) で1-3 invocation/キーで回収する。
  inner timeout 260s / 外側290s構成 (Part CN/CS実績) 継使用。
- WINDOW-EXCEEDED規則 (事前登録・バックアップ): 同一passのTRUNCATED-RETRY 2回でそのキーは
  skipし honest unresolvedとして監査に記録 (silent dropなし)。この場合将来の別条件Part
  (inner window延長かchunked pass設計) に委ねる。
- WIN-CONTINUE (Part CE/CK/CN/CQ/CS先例): WIN行 (rc=45) でorchestrationは停止しない。
  EXHAUSTED行 (result 0) はhonest UNKNOWNとして継続。

## 事前登録 (プロトコル・事前に全部開示)

1. **A scaffold**: 実験dir `research/experiments/n11-centralreply-class5343-b28aa050-reprobe30m-20261123/`
   に kit 30 files (scripts 6 / input 5 / sources 10 / val-gate 8 / README) を出版。
   jsreplay.js `84585617…` (published byte-clone)・runbatch.sh `f591f8c2…` (参照用)・
   derived runner `3b5083b47c043f93bbe01a5f3335baba6be6d1d6929885f4ab5b28b1778cf7b4…`・maker `5b605215…` (G1-G9 fail-closed・byte-stable 2回一致
   `f0ae762f…`)・session step `854daf1e…`・audit `a3749094…` (schema
   `n11-centralreply-c5343-b28aa050-reprobe30m-audit-v1`)。maker生成registry
   (input/reprobe-keys.json `f0ae762f…`・targets 1 (aa050)・anchors 2 (aa036/aa004)) 含む。
2. **val-gate fresh 4** (宣言後): at2m×2 budget 2,000,000 (exhaustion nodes 2,000,000)・
   15m×2 budget 15,000,000 (nodes 3,651,923 / 5,040,200)・published baselinesと
   node-exact (f6/f7一致・f8 wall_s比較外)。
3. **anchors** (宣言後・derived runner 30M): aa036 → result 2 nodes 955,659 (PASS行のみ)・
   aa004 → result 1 nodes 15,616,012 (PASS + WIN-HALT rc=45)・published値とnode-exact必須。
   anchor基準sourcesはpublished CQ raw (maker G7 pin)。
4. **target 1キー** (宣言後): session step 1 invocation 1キー進行でaa050を2-pass fresh-cold
   (cross-invocation resume想定2 invocation: p1完走→p2 truncated→retry完走)。mismatch 0を
   要請。解決nodes期待値は事前宣言しない (EXHAUSTEDならnodes=30,000,000 2-pass一致)。
5. **audit** (宣言後): `audit_ct.py` 3回実行 stdout+audit.json byte-identical・
   tamper電池4件 (p2 nodes改変→p1/p2不一致 / result反転→status照合 / replay_done削除→
   truncated捕捉 / registry `reprobe_condition.budget` 改変→gate A捕捉 ※CQ教訓: 改変先
   フィールドはregistry schema機械確認の上指定) + clean control・各probe復元cmp。
6. **出版**: B outputs (status.log + raw + val-gate .ct-host.out + audit.json) → C README最終 +
   MANIFEST-sha256 → 完了log。push毎にobserved HEAD再取得 + commit-pinned fetch-back
   byte照合。**11×11未解決ならUNKNOWNと明記**・nodes数を勝敗として読まない。

## verdict不消費

WIN/LOSS行はprobe-level honest labelsのみ。canonical adoptionは別宣言adoption Part
(pinned fail-closed merger `90711961…`) 経由のみ・WIN行はscrutiny owner C++第二実装
gate `9193f5b6…` 待ち。本Partはいかなるadoption・closure・secured・root勝敗の主張もしない。
**標準11×11空盤・class 5343・全キーは現在もUNKNOWN。**
