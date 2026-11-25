# Part DA takeover 完了log: batch-29 (class 2251) drive-2 ckpt-2/3 LOSS 15行 第三実装交叉検証 — three-implementation corroboration 15/15 (LOSS)・audit ALL 429 GATES PASS ×3 byte-identical・verdict不消費・11×11 UNKNOWN担保不変 (2026-11-24)

## 実行の経緯 (takeover)

- 原宣言 `88ffdc92` (2026-11-24T02:22:43Z)・scaffold A 3 commit (`267fec1a` /
  `9e0d71be` / `c5ccfbd3`・02:23:28Z 完了) の後、原宣言sessionはD1-D8に
  着手しないまま 3.5h 超停滞。
- takeover宣言 `f2b36862` (2026-11-24・earliest_takeover 05:52:43Z 通過後・
  observed HEAD `9abe5e66`・直近12 commit 機械走査で対抗宣言/本dir新commit
  なしを確認): `research/log/2026-11-24-part-da-takeover-b29d2loss15-thirdimpl.md`。
- kit復元 (takeover宣言前に実施・solver実行なし): published scaffold 3
  commitから92ファイル raw fetch・pin照合 (script 7点 + rows.json + sources
  6点=全sha一致)・input/published-input byte一致 15/15+4/4・knowledge
  lane-kit jsreplay `84585617…` 一致。
- takeover は原宣言対象・protocol・pinを一切変更せず継承 (Part CX先例
  `c48aa56b` と同一規約)。

## 実行結果 (D1-D8 全green)

- **D1** rules gate: verify_tbl.js — replica quads 95,670 / mine quads
  95,670・triples checked 195,044・mismatches 0 (`output/rules-gate.txt`
  sha256 `88c0b78b…`)。
- **D2** val-gate fresh 4/4 node-exact (`.da-host.out`): 2M×2 result 0
  (budget-exhausted・nodes 2,000,000) / 15M×2 result 2 nodes 3,651,923 /
  5,040,200 — published baselines と wall_s 以外全field一致。
- **D3** negatives 2/2 fail-closed: ng1 "legal count mismatch: derived=87
  declared=88" / ng2 "stone count mismatch: bits=5 declared=6"。
- **D4** anchors 4/4 published pin と node-exact: k02a a/b WIN expansions
  9,106,337・ttHits 4,991,527 / l1a a/b LOSS expansions 7,660,602・ttHits
  3,951,175 (det-pair a==b・~22-26s/run)。
- **D5** pinned-replica 30/30 pass (15キー×p1/p2・budget 15M): 全pass rc=0
  (runner終端のrc=1は宣言・DC知見どおり `[ rc -ne 0 ] && exit` の偽評価
  によるbenign quirk・成否はstatus.log行で判定)・p1==p2 determinism
  (全determinism field一致)・published drive-2 raw と全行 node-exact
  (result 2・nodes 1,835,150〜8,695,465・15/15)。
- **D6** 第三実装 30/30 run clean (15キー×a/b・cap 300M・wallcap 240・
  memo-power 22): 全run rc=0 clean・det-pair a==b・pass-one expansions
  合計 **73,293,629** (最小 ab026 2,075,693〜最大 ab023 10,104,496)・
  **verdict 15/15 = result 2 で published drive-2 LOSS 行と完全一致 =
  three-implementation corroboration 15/15**・WALL-INCONCLUSIVE 0。
- **D7** audit (audit_da.py `ca24423d…`) ×3 byte-identical: 同一cwd
  PYTHONHASHSEED=random / 1 + 隔離tree `env -i` PYTHONHASHSEED=99 —
  **ALL 429 GATES PASS ×3** (stdout sha256
  `5cef05e33d2690657245d17b1975635b0fd603a559972561ad3d3860480070f6`・
  audit-summary.json `9d21022a…`・両run同sha)・verdict agreements 15/15
  (WIN=0 LOSS=15)・G6 unadopted補強 15キー全員機械担保 (merged cache
  `30ddad9d…` 6,317行にrow不在・no-key-row・CU manifest
  fileless_unprobed_ids (38キー) 在籍・adopted/win/probed系id list全不在)。
- **D8** 出版: B1 `fd7024a4` (output 32: status.log 66行 + rules-gate +
  replica 30) → B2 `33d746ca` (targets 30 + anchors 4 + negative 2) →
  B3 `4ba20863` (audit-summary + audit-run1-3) → B4 `77eecd66` (val-gate
  host 4) → C `93e85406` (README + MANIFEST-sha256 **169 files・fetch-back
  sha256 全件一致 80+89/169・fail 0**) → 本完了log。
  pushは全てfast-forward成功・競合なし (各push直前に最新main再取得・
  observed HEAD記載)。
- local記録の補足 (誠実開示・出版データには影響なし): (a) D5 runner の
  外側rc=1は benign quirk (上記)。(b) D3確認時の `tail -4 file1 file2`
  複数file文法が本環境のtailで invalid context 扱いになったが、
  status.log行とaudit gate (文言一致検証) で二重確認済み。(c) D7 run3は
  隔離tree (cp -a 実験dir全体) で実施・run3のstdoutを main treeへ
  byte-copyし sha 同一確認 (`5cef05e3…` 3走同一)。

## 意味 (verdict不消費 の範囲内で)

batch-29 (closure class 2251) 54キーの第三実装交叉検証は本完了で全行成立:
drive-1 ckpt-1/3 16行 (ab001..ab016・Part CV `3b6ad066`) + drive-2 WIN 1行
(ab028・Part CZ `68751fd7`) + **drive-2 ckpt-2/3 15行 (本Part DA takeover)**
+ drive-2 ckpt-3/3 22行 (ab033..ab054・Part DC `488f61f4`)。ただし:
- 本結果は制御された再実行・交叉検証の記録であり、**verdict は不消費**
  (15行はhonest labelのまま・adoption/解放/閉鎖/被覆/root勝敗の主張を
  しない)。
- LOSS 15行の canonical 採用は CU先例の pinned merger `90711961…` 経由の
  別adoption Part 専権。WIN ab028 は scrutiny owner C++ gate
  `9193f5b6…` 通過後のみ採用可。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・class 2251 (batch-29 54キーすべて) は全時点で
  UNKNOWNのまま。nodes数・expansions数・ttHits数を勝敗や距離として
  読まない。**

## 並走状況 (本Part完了時点・非接触確認)

Part DF (batch-28 P2・aa*キー・最終観測 `4db1ffcb`) / Part DG (batch-28 P3・
aa*キー・最終観測 B outputs `9abe5e66`) / queue registry (batch-28 WIN46) /
K1282 fast lane (`33cb9306` 完了) はいずれも対象キー・実験dir完全分離。
batch-30 drive-3 (ac030..ac054)・batch-31 drive-2 (ad029..ad055) は本Partでは
非接触 (別宣言の対象外)。

## レジューム (着手前に必ず最新main再取得・hourly並走注意)

次回候補: (a) **batch-29 全54キーの位置づけ確認 (機械確認済み)**: LOSS 53行は
CU (drive-1 16行) + **Part DB (37行・完了log `10a79660` 2026-11-24T02:40:07Z
= DA原宣言 02:22:43Z の後に着地)** で canonical 採用済み (post-adoption
merged cache `04b0a239…` 6,354行)。本Part対象15行は DB採用37行に含まれ、
本takeoverの third-impl corroboration は **DB採用行の事後強化** (DBは
drive-2 published 出力ベース・DA原宣言は CU snapshot `30ddad9d…`
(6,317行) を G6 pin しており矛盾なく両立・原宣言の「採用は別adoption Part
専権」の文言どおり DB が採用を担当した)。class 2251 の残る canonical
unknown は WIN ab028 1行のみ (scrutiny owner C++ gate `9193f5b6…` 通過待ち
・採用は別adoption Part 専権)。(b) **batch-28 queue registry P4パッケージ
(CS/CT解決4行 aa032/aa028/aa021/aa050 + 5行・est≈373.8M) の第三実装交叉検証**
(別単一オーナー宣言・cross-invocation step設計・DF (P2)/DG (P3) が同時進行中
のため対抗宣言チェック必須)、(c) batch-30 drive-3 (ac030..ac054) /
batch-31 drive-2 (ad029..ad055) の別単一オーナー宣言。5343・2251・5804・
34269 等全class・root・空盤は全時点UNKNOWNのまま。
