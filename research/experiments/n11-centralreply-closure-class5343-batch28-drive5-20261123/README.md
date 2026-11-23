# batch-28 drive-5 (WIN-CONTINUE): 残23キー aa032..aa054 完走 — batch-28 全54キー probed、EXHAUSTED含む誠実記録 (Part CN, 2026-11-23)

Part CN (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-23-part-cn-batch28-drive5-declaration.md`・commit `11f2b668…`)。
batch-28 (class 5343・54キー・Part CK drive-4終了時点: probed 31 = aa001..aa031 +
fileless 23キー aa032..aa054) のpublished kitをbyte-clone継続し、残り23キー
(s5_index 199717..199739・batch内最高s5帯) をpinned runnerで2-pass fresh-cold
probeする drive-5 (WIN-CONTINUE事前登録) の実験dir。**verdict不消費**。
閉鎖・被覆・secured・root勝敗の主張はしない。

## kit (published batch-28 drive-4 dir `85d26a2c` 時点のbyte-clone・148ファイル中148ファイルfetch-back byte同一の正本から構築)

- scripts byte-pins (一字不改): runbatch.sh `f591f8c2…` (stop rules: WIN rc=45 /
  MISMATCH rc=42 / p1/p2 fail rc=43/44・budget 15M・truncated passはevidenceでなく
  fresh-cold retry・`# replay_done`なしのpassは再実行)・jsreplay.js `84585617…`・
  row_audit_batch28.py `656cac31…`・row_audit_batch28_win_halt.py `96867282…`・
  make_batch28_keys.py `d1ffe72f…`・drive_batch28.sh `08dc059c…`・runwave.sh
  `8efd78c2…` + session-local drive5_local_step.sh `e2ceb7fa…` (drive-4の
  `ea0db83e…` と同一設計・差分は2箇所のみ: kit pathとworker timeout 285→260s
  (本host外側shell上限290sに対しinner timeout先発火で正常returnさせ、外側
  timeoutによる環境リセットがevidenceを巻き戻す事故構造を排除・宣言§3開示))。
- input 55 files (batch-keys.json `af19208f…`・published pinsそのまま・54キー変更なし)。
- output seeds: published drive-4 status.log (61行・sha `59817444…`) + published
  raw outs aa001..aa031 (68 files・truncated sidecars 6つ含む・published pins)。
  **drive-1..4のcompleted行 (aa001..aa031) は再probeしていない**。
- val-gate: published 12 files (at2m×2 budget 2M・15m×2 budget 15M・input CSV +
  published baselines + `.cd2-host.out`) + 本host fresh `.ck-host.out` 4 files
  (宣言後に再実行)。

## 実行記録 (宣言protocol・逐次)

1. val-gate fresh再実行 4/4 本host node-exact (宣言後に実施・wall_s比較外):
   at2m×2 nodes 2,000,000 (result 0)・first-15m 3,651,923 (result 2)・
   second-15m 5,040,200 (result 2)。wall 9/9/17/25s (published 8/9/17/25s)。
2. drive-5反復 13 worker-invocation (18:41〜19:24Z・2 worker・timeout 260):
   **aa032..aa054の23キー完走 (ALL-DONE)**。内訳:
   - **WIN 17** (result 1・2-pass node-exact・honest WIN label):
     aa033 3,347,117 / aa034 14,097,048 / aa037 14,239,714 / aa038 4,911,996 /
     aa039 11,349,776 / aa040 8,916,641 / aa041 10,283,599 / aa042 5,800,791 /
     aa043 12,069,965 / aa044 9,219,778 / aa045 12,371,943 / aa046 2,185,149 /
     aa048 10,553,343 / aa049 7,272,703 / aa051 7,662,388 / aa052 8,976,982 /
     aa054 13,227,570 nodes。
   - **LOSS 1** (result 2・採用候補のみ): aa036 955,659 nodes。
   - **EXHAUSTED 5** (result 0・budget 15M nodes 15,000,000・honest UNKNOWN・
     same-condition再probeなし): aa032 / aa035 / aa047 / aa050 / aa053。
   - aa034/aa035は初回invocationでp1完走 (WIN 14,097,048 nodes wall 150s /
     EXHAUSTED 15M wall 166s) 直後のp2がtimeout窓でtruncated (sidecars 2 files・
     runnerがrename) → 次invocationのcompleteness guardがp2のみfresh-cold再実行し
     完走 (P2-TRUNCATED-RETRY bookkeeping 2行)。MISMATCH 0・P1/P2 fail 0
     (batchキーに対しては)。
3. **batch-28全体の完走状態**: probed 54 = **WIN 35・LOSS 8 (aa003採用済み +
   aa015/aa017/aa018/aa023/aa024/aa029/aa036 採用候補のみ)・EXHAUSTED 11・
   fragment 0・fileless 0・mismatch 0**。54キーすべてが2-pass node-exact。

## 誠実記録 (incidents・宣言からの派生はすべて開示)

1. **session-local scriptのALL-DONE状態空キーバグ (発現1回・影響なし)**:
   drive5_local_step.sh (および同型のpublished drive-4 `ea0db83e…`) の残余キー
   計算は `print("\\n".join(rem))` で `rem=[]` のとき単一の空行を出力する。
   全54キー完了直後の14番目のinvocationで `runbatch.sh ""` (空キー) が呼ばれ、
   status.logにkey idを含まないjunk行 `P1-FAIL ` が1行追記され、
   `output/raw/.p1.out` (node ENOENT stack trace) が生成された。**いかなる
   batchキーにも触れておらず**、aaNNN形式の108 pass fileはすべて無傷 (sha256
   検証済み)。junk行と `.p1.out` は削除せずそのまま出版する (append-only log
   規約)。監査はjunk行を非verdict行として無視する (両監査とも `l.split()[1] ==
   kid` 形式照合のみ)。本バグの修正版scriptの出版は次drive以降の課題
   (batch-28は完走したため再発なし・宣言時に「timeout 260sは宣言済み」だが
   本バグは宣言時に認識できていなかった)。
2. **win-halt変種の適用外 (設計どおり)**: 全54キーcompleted状態では
   `row_audit_batch28_win_halt.py` (`96867282…`) は「batch fully completed
   with no fragment/fileless key」でGATE FAILEDする (設計どおり・実行して記録)。
3. **full監査の最小派生 full-v2**: published full audit `656cac31…` はWIN行の
   status.log照合を単行 (`… aaNNN WIN-HALT` に nodes を含む) 想定で行うため、
   batch-28の2行ペイロード (PASS行+裸WIN-HALT行) で「aa001: status.log node
   count mismatch」にGATE FAILする (**drive-4 README記載済みの既知設計**・batch-26
   Part BT確認済み)。Part CB先例 (winhalt版の単一ゲート修正派生の出版) と同型に、
   **EXACTLY 1 gate だけ**修正した最小派生 `scripts/row_audit_batch28_full_v2.py`
   (`1f4b3ce9…`): WIN行照合の「PASS行 (fields込み) + WIN-HALT行」の両方要求に
   変更 (winhalt版の実績あるhas_pass/has_halt対と同一logic)・他の全gateは
   byte-identical・docstringに全文開示・schemaは
   `…rowaudit-full-v2` を明記。B outputs commitでKitと共に出版。

## 状態 (row-audit full-v2・機械導出)

- row-audit(full-v2) PASS **x3 byte-identical** (json SHA-256 `00c32383…`):
  probed 54 = **WIN 35・LOSS 8・EXHAUSTED 11・mismatch 0** (loss_rows aa003/
  aa015/aa017/aa018/aa023/aa024/aa029/aa036・win_rows 35行・exhausted 11行)。
- tamper battery 4/4検出 (実効性assertモデル・実験dir正本に直接適用+復元cmp):
  T1 status.log aa036 LOSS nodes 955659→955999 → `aa036: status.log node count
  mismatch`・T2 raw aa033 p2 result 1→2 → `aa033: p1/p2 row mismatch`・T3 raw
  aa040 p1 `# replay_done`行削除 → `aa040.p1.out: missing # replay_done
  (truncated fragment)`・T4 raw aa046 p2 quads 95670→95671 → `aa046: forbidden
  quadruples header mismatch`。各probe後に復元をcmp検証、battery後のclean
  control runは実行3回目とbyte-identical。
- 宣言の期待どおり54キー完走 (ALL-DONE・fileless 0)。

## 解釈ガード

- nodes数・wall秒数を勝敗として読まない。WIN行 (drive-5の17行を含む35行) は
  honest labels only (unconsumed closure WIN候補・route statementのみ・採用判断は
  scrutiny owner C++第二実装 gate `9193f5b6` のまま・本レーンは代行しない)。
  LOSS行 (aa015/aa017/aa018/aa023/aa024/aa029/aa036の7行・aa003は採用済み) は
  adoption候補のみ (canonical cacheへの反映は別adoption宣言・pinned fail-closed
  merger `90711961…` 経由のみ)。EXHAUSTED 11行はhonest UNKNOWN
  (same-condition再probeなし・予算引き上げは別宣言条件)。EXHAUSTED行が8→
  11に増えたことはclass 5343の閉包を何も意味しない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・EXHAUSTED行を
  含む) は本実験の前後を通じてUNKNOWNのまま。** canonical cache (Part CH merged
  6,294行 `3124461b…`) への書込は一切ない。closure table不変 (adoption Partを
  通らない限り)。被覆・secured・root勝敗の主張はしない。
