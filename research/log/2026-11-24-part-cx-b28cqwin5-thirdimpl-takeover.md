# Part CX takeover宣言: batch-28 (class 5343) Part CQ 20M再probe新解決WIN残5行 (aa005/aa030/aa031/aa047/aa053) の第三実装交叉検証 — 原宣言 `1300c10d` からのtakeover (2026-11-24)

単一オーナーtakeover宣言・publish-then-execute。

## takeover事由の機械確認 (takeover規約: 宣言から3.5h ⇒ earliest_takeover 2026-11-24T04:19:31Z 以降 かつ 停滞時)

- 原Part CX宣言: `1300c10d` (2026-11-24T00:49:31Z・research/log/2026-11-24-part-cx-b28cqwin5-thirdimpl-declaration.md)。
- cx実験dir (`research/experiments/n11-centralreply-closure-b28cqwin5-thirdimpl-20261124/`) への
  最後 (かつ唯一) のcommitは **scaffold A `3185a672` (2026-11-24T00:50:16Z)**。以降3.5h超、
  本takeover宣言時点まで:
  - 同dirにoutput/無し (D5/D6相当の成果物は一件も出版されていない・commit列機械確認)。
  - research/logにCXのB/C出版物・完了log・進捗log無し (commit列機械確認)。
  - CX関連の追加commit無し (cx実験dir pathに対するlist_commits機械確認・上記1件のみ)。
- 対抗takeover宣言なし (本宣言直前 2026-11-24T04:20Z 時点の最新main commit列で機械確認)。
- 観測 HEAD-before-push: **`10b8e96d`** (z11 predecl exploration・2026-11-24T04:00:20Z)。
  本takeover宣言のpush前に取得した最新main HEADであり、取得時点以降にCXへの進捗commit・
  対抗宣言は観測していない。
- 本宣言push時刻は earliest_takeover (2026-11-24T04:19:31Z) を過ぎている。

## 継承 (原宣言の全pin・protocol・stop rulesをbyte不変で継承)

- 原宣言の対象・protocol D1-D8・stop rules・主張の限定をすべてそのまま継承する。
  本takeoverは実行主体の交代のみで、宣言内容・kit・pinsに変更を加えない。
- kit (scaffold A `3185a672`・出版済み) からの復元を実施済み: 全52ファイル取得
  (commit `3185a672` pinのraw URL・fetch全成功) し、sha256照合でpin一致を確認:
  rows.json `3a87c5b6…`・make_inputs_cx.py `7abf48c5…`・audit_cx.py `87152e94…`・
  run_replica_cx.sh `6d05701c…`・third_impl.js `08ea958f…`・verify_tbl.js `c8c52528…`・
  jsreplay.js `84585617…` — 全byte一致。maker ×2 実行 green・stdout byte-identical・
  rows.json byte-stable も復元直後 (takeover時刻前) に確認済み。
- 対象5行 (原宣言と同一): aa005 (1171516445255794690, 0) nodes 15,957,877 / aa030
  (1243574039293722624, 0) 16,765,560 / aa031 (1459746821407506432, 0) 17,185,014 /
  aa047 (1152921504611041280, 4228) 16,230,465 / aa053 (1152921504606855168, 4228)
  16,685,872。全て published CQ 20M 2-pass node-exact WIN行・verdict不消費。

## 実行protocol (原宣言D1-D8をそのまま実施)

- D1 rules gate → `output/rules-gate.txt`。
- D2 val-gate fresh 4 (`.cx-host.out`・published baselinesとwall_s以外node-exact)。
- D3 negatives ng1/ng2 GATE_FAIL設計どおり (auditの読み先は tag "a"側2ファイル)。
- D4 anchors k02a/l1a 各a/b (9,106,337/4,991,527・7,660,202/3,951,175 pin一致)。
- D5 replica aa005/aa030/aa031/aa047/aa053 各p1/p2 (budget 20M・inner timeout 260・
  1キー1 invocation・pass分離許容)。
- D6 targets 5キー各a/b第三実装 (cap 300M・wallcap 240・memo-power 22)。
- D7 audit `audit_cx.py` (G6 CO出版物unadopted補強gate込み) ×3 byte-identical +
  tamper電池 (audit-side A1-A4)。
- D8 B outputs出版 → C README最終 + MANIFEST-sha256 → 完了log出版
  (各push前後に最新main再取得・fetch-back byte一致検証・競合時は無理押しせず記録して次回へ)。
- 補助確認 (原宣言どおり): 実行記録において現canonical chain head (Part DB merged cache
  `04b0a239…` 6,354行・DB manifest) に対象5キーrowが存在しないことを機械不在確認して記録する。
- いずれかのgateでGATE FAIL/MISMATCH → 停止・誠実記録・verdict不消費のまま出版。

## 主張の限定 (原宣言と同一)

- **verdict不消費**: 5行はhonest WIN labelsのまま。本takeover Partはいかなるadoption・
  解放・閉鎖も行わない。閉鎖・被覆・secured・root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・10968・23964・class 5343 (54キーすべて・対象5キー含む) は本Partの前後を
  通じてすべてUNKNOWNのまま。** nodes数・expansions数・ttHits数を勝敗や距離として読まない。
