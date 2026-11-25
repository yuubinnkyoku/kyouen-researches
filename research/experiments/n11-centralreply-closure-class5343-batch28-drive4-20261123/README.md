# batch-28 drive-4 (WIN-CONTINUE): fileless 45 keys aa010..aa054 — 22 keys probed, honest session cut, 23 fileless (Part CK, 2026-11-23)

Part CK (publish-then-execute・単一オーナー・宣言
`research/log/2026-11-23-part-ck-batch28-drive4-declaration.md`・commit `ad269701…`)。
batch-28 (class 5343・54キー・Part CJ drive-3終了時点: completed aa001..aa009 + fileless
45キー aa010..aa054) のpublished kitをbyte-clone継続し、残り45キーをpinned replicaで
2-pass fresh-cold probeする drive-4 (WIN-CONTINUE事前登録) の実験dir。
**verdict不消費**。閉鎖・被覆・secured・root勝敗の主張はしない。

## kit (published batch-28 drive-3 dirのbyte-clone・105ファイルfetch-back 104/104+MANIFEST byte同一の正本から構築・drive-3 session-local scriptとdrive-3 host val-gate 4 filesは除外)

- scripts byte-pin再利用 (一切変更なし): runbatch.sh `f591f8c2…` (pre-registered stop
  rules: WIN rc=45 / MISMATCH rc=42 / p1/p2 fail rc=43/44・budget 15M・TRUNCATED passは
  evidenceでなくfresh-cold retry・`# replay_done`なしのpassは再実行)・jsreplay.js
  `84585617…`・drive_batch28.sh `08dc059c…`・row_audit_batch28.py `656cac31…`・
  row_audit_batch28_win_halt.py `96867282…`・make_batch28_keys.py `d1ffe72f…`・
  runwave.sh `8efd78c2…`。
- scripts/drive4_local_step.sh `ea0db83e…`: session-local orchestration記録 (pinned kit
  の一部ではない・Part CD/CJと同型の実行tree path差のみ・solver/runner/stop rulesは
  byte-identical・反復每に未完キー最大2個を `timeout 285` でpinned runbatch.shへ直接
  渡す。**WIN-CONTINUE: rc=45を観測しても次反復へ進むのは本orchestration層のみ**
  (宣言§1・runner内蔵stop rules不変)。
- input 55 files (54 CSV + batch-keys.json `af19208f…`・published pinsそのまま)。
- output seeds: published drive-3 status.log (21行・Part CJ B pin) + published raw outs
  aa001..aa009 (22 files・drive-2 truncated sidecars 4つ含む・published pins)。
  **drive-1/2/3のcompleted行 (aa001..aa009) は再probeしていない**。
- val-gate: published 12 files (sanctioned 4キー: at2m×2 budget 2M・15m×2 budget 15M・
  input CSV + published baselines + Part CD `.cd2-host.out`) + 本host fresh
  `.ck-host.out` 4 files (Part CK宣言後に再実行・4/4 node-exact・wall_s比較外)。

## 実行記録 (宣言protocol・逐次)

1. val-gate fresh再実行 4/4 本host node-exact (宣言ad269701後)。
2. wave反復 8 invocation (17:44〜18:18Z・2 worker・timeout 285): **aa010..aa031の
  22キー完走**。内訳 **WIN 12 (aa010 8,882,182 / aa011 12,424,953 / aa012 4,994,213 /
  aa013 8,317,071 / aa014 7,263,370 / aa016 2,621,847 / aa019 7,967,030 / aa020
  8,432,253 / aa022 14,044,375 / aa025 3,056,950 / aa026 11,019,409 / aa027 4,860,191
  nodes・いずれもresult 1・2-pass node-exact)・LOSS 6 (aa015 6,152,494 / aa017
  11,446,358 / aa018 214,968 / aa023 5,000,770 / aa024 5,003,631 / aa029 10,010,789
  nodes・いずれもresult 2・採用候補のみ)・EXHAUSTED 4 (aa021/aa028/aa030/aa031・
  budget 15M nodes 15,000,000・honest UNKNOWN)**。
   - aa030/aa031は初回invocationでp1完走 (EXHAUSTED 15M・wall 157/159s) 直後のp2が
     timeout窓でtruncated (sidecars 2 files・runnerがrename) → 次invocationの
     completeness guardがp2のみfresh-cold再実行し完走 (P2-TRUNCATED-RETRY bookkeeping
     2行)。MISMATCH 0・P1/P2 fail 0。
3. **誠実なsession時間制約打ち切り**: 18:18:30Z時点で残23キー (aa032..aa054) は
   fileless UNPROBEDのまま終了 (宣言§1 (c))。将来drive-5+で継続可能。

## 状態 (row-audit-winhalt・機械導出)

- row-audit(winhalt) PASS (pinned `96867282…` x3 byte同一・json SHA-256 `dcf078aa…`):
  **probed 31 (aa001..aa031) = WIN 18・LOSS 7 (aa003 + aa015/017/018/023/024/029)・
  EXHAUSTED 6 (aa004, aa005, aa021, aa028, aa030, aa031)・fragment 0・fileless 23・
  mismatch 0**。
- full-variant `row_audit_batch28.py` (`656cac31…`) は宣言§3どおり併走: GATE FAILED
  「aa001: status.log node count mismatch」(WIN行の2行ペイロード (PASS+WIN-HALT) を
  単行想定で照合する既知設計・batch-26 Part BTで確認済みの性質。部分終了+WIN行が
  ある本状態ではwinhalt版が適用され、full版のfailは適用外の正常挙動として記録)。
- tamper battery 4/4検出 (scratch copy上・実効性assert込み: T1 win行aa010 p1 result
  反転 1→2 → p1/p2 row mismatch gate・T2 status.log aa010 WIN nodes +1 → WIN-HALT
  record incomplete gate・T3 status.log aa015 LOSS nodes +1 → node count mismatch
  gate・T4 raw aa015 legal 89→90 (p1/p2両方) → published packet legal不一致gate)。
  battery後の実験dir全ファイルsha256不変を検証。
- 出力変更なしに宣言の期待簿記 (probed 9+22=31) と一致。

## 解釈ガード

- nodes数・wall秒数を勝敗として読まない。WIN行 (drive-4の12行を含む) はhonest
  labels only (unconsumed closure WIN候補36..47番目に相当・route statementのみ・
  採用は別adoption Part (pinned merger `90711961…`) 経由のみ)。LOSS行 (drive-4の
  aa015/aa017/aa018/aa023/aa024/aa029の6行・aa003は採用済み) はadoption候補のみ
  (canonical cacheへの反映は別adoption宣言のみ)。EXHAUSTED行はhonest UNKNOWN
  (same-condition再probeなし)。scrutiny owner C++第二実装 gate `9193f5b6` は継続。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて) は本実験の前後を
  通じてUNKNOWNのまま。** canonical cache (Part CH merged 6,294行 `3124461b…`) への
  書込は一切ない。closure table不変 (adoption Partを通らない限り)。
