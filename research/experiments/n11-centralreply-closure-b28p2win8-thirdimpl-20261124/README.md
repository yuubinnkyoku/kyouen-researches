# n11-centralreply-closure-b28p2win8-thirdimpl-20261124 (Part DF)

Part DF: batch-28 (closure class 5343) b28-win46 third-impl queue registry
(REVISION 3) P2パッケージ8行 (aa014/aa049/aa051/aa019/aa013/aa020/aa010/
aa040・drive-4/5 15M-probe solved WIN・全てUNCONSUMED honest labels) の
第三実装交叉検証 (publish-then-execute)。

- 宣言: `research/log/2026-11-24-part-df-b28p2win8-thirdimpl-declaration.md`
  (commit `59b6540f`・observed HEAD `aebb2201`・対抗宣言なし機械確認済み・
  maker gates PASS byte-stable ×2 + tamper 15/15事前実行済み)。
- 実行 (D1-D8) はtakeover (`255d43a4`・amendment `4afac03b`) により完了
  (下記「実行記録」)。本READMEが最終版。

## kit構成 (このA commit)

- `scripts/` 7: make_inputs_df.py (`a3c6e8e1…`・宣言済みDE maker適応・
  適応時のQREG_P2_TOTAL修正は宣言記載) / audit_df.py
  (`76934660…`・宣言済みDE audit `a57e220c…`適応・target 8キー・P2-package
  文言・PIN_RAW_DF 16 pin・`.df-host.out` suffix) / run_replica_df.sh
  (`73f09f38…`・published DE runner `3e4263cc…`のヘッダcommentのみ書換・
  body byte不変・budget 15M不変) / run_thirdimpl.sh (`a0b77d83…`・CW版
  byte-clone) / third_impl.js (`08ea958f…`) / verify_tbl.js (`c8c52528…`) /
  jsreplay.js (`84585617…`) — 下3つはpinned byte-clone。
- `sources/` 39: drive-4/5実験
  (`n11-centralreply-closure-class5343-batch28-drive{4,5}-20261123`) からの
  commit-pinned fetch (raw 16: 8キー×p1/p2・決定ドライブ側正本・
  aa010/aa013/aa014/aa019/aa020はdrive-4・aa040/aa049/aa051はdrive-5 /
  published-input 8・published-input-bf 4) + status-drive4.log `59817444…`
  (61行) + status-drive5.log `ca1e98cc…` (109行) + batch-keys-b28.json
  `af19208f…` + queue-registry.json (rev3) `334f6209…` + README-queue.md
  (rev3) `4b20c6a0…` + Part CO 7-LOSS adoption出版物 (merged canonical cache
  `854800f3…` 259,886B・6,301行 / increment `bd5ef7d7…` / increments-manifest
  `b47e07ca…`) + Part DB 37-LOSS re-adoption出版物 (merged canonical cache
  `04b0a239…` 262,326B・6,354行・現canonical chain head / increment
  `85bd4469…` / increments-manifest `1b51f30d…`)。
- `input/` 13: rows.json (`e184c50b…`・maker 2回実行byte-stable) + 8対象 +
  anchors k02a/l1a + negatives ng1/ng2 のinput CSV (publishedとbyte一致)。
- `val-gate/` 8: at2m×2 + first-15m/second-15m published baselines + inputs
  (CWから不変再利用・host出力は `.df-host.out` として生成)。

## 対象8行 (published・全てUNCONSUMED)

| key | key (lo,hi) | s5 | legal | verdict | nodes | 決定drive |
| --- | --- | --- | --- | --- | --- | --- |
| aa014 | 1171516445255811072,0 | 160350 | 88 | WIN | 7,263,370 | drive-4 |
| aa049 | 1152921504623624192,4228 | 199734 | 83 | WIN | 7,272,703 | drive-5 |
| aa051 | 1152921504673955840,4228 | 199736 | 87 | WIN | 7,662,388 | drive-5 |
| aa019 | 1171516445322903552,0 | 183025 | 86 | WIN | 7,967,030 | drive-4 |
| aa013 | 1171516445255802880,0 | 156182 | 87 | WIN | 8,317,071 | drive-4 |
| aa020 | 1171516453845729280,0 | 185891 | 90 | WIN | 8,432,253 | drive-4 |
| aa010 | 1171516445255794720,0 | 144019 | 86 | WIN | 8,882,182 | drive-4 |
| aa040 | 1152921504606846992,4228 | 199725 | 89 | WIN | 8,916,641 | drive-5 |

## 目標と主張の限定

- 8行の第三実装verdict一致と本host pinned-replica 2-pass node-exact再現は
  **three-implementation corroboration** (jsreplay runner×2系 + 第三実装) の
  証拠であり、採用ではない。verdict不消費: 対象8行はhonest labelのまま・
  adoptionは scrutiny owner C++第二実装 gate `9193f5b6…` を経て別adoption Part
  (pinned merger `90711961…` 経由) のみ。
- 閉鎖・被覆・secured・root勝敗の主張をしない。
- **標準11×11空盤・19 central-reply roots・class 5343・全キー (対象8キー含む) は
  この時点でUNKNOWN**。nodes数・expansions数・ttHits数を勝敗や距離として
  読まない。

## 実行記録 (D1-D8, 2026-11-24, takeover実行)

- takeover: 原宣言 `59b6540f` (05:01:52Z) からscaffold検証log `4db1ffcb`
  (05:15:35Z) 後 3.5h停滞 → takeover宣言 `255d43a4` (08:23:34Z) + 時刻逸脱の
  amendment `4afac03b` (takeover宣言が earliest_takeover 08:31:52Z の約8分前に
  出た時計読み違え。D1-D9の実開始は08:31:52Z経過後・対抗/原オーナー出版なしを
  再確認済み)。kit復元: published scaffold 68ファイルをcommit-pinned raw fetchで
  復元し宣言ノート45 pin群を照合 44/45一致。唯一の不一致は宣言ノートの
  `run_replica_df.sh` pin転写誤り (出版bytes `73f09f38…` / blob `00384666` が
  正本・宣言ノート側の誤記と判定)。
- B wave (outputs出版): commit `46473d3e`・fetch-back byte検証 48/48。
- D1 rules-gate PASS: quads 95,670 一致・triples 195,044 mismatches 0。
- D2 val-gate fresh 4/4 node-exact (wall_s以外): first-15m result 2 nodes
  3,651,923 / second-15m result 2 nodes 5,040,200 / at2m 2行 budget-exhausted
  (result 0・nodes 2,000,000) ・出力は `.df-host.out` 4本。
- D3 negatives PASS (期待fail-closed): ng1 GATE_FAIL "legal count mismatch:
  derived=87 declared=88" / ng2 GATE_FAIL "stone count mismatch: bits=5
  declared=6" (rc=1)。
- D4 anchors a/b det-pair PASS: k02a result 1・expansions 9,106,337・ttHits
  4,991,527 / l1a result 2・expansions 7,660,202・ttHits 3,951,175
  (published pin完全一致)。
- D5 replica 8キー×2-pass fresh-cold (budget 15M): 16/16 rc=0・det-pair 8/8・
  published raw (PIN_RAW_DF 16) と node-exact 16/16 (pinned nodes合計
  64,713,638)。`run_replica_df.sh` の invocation-level exit 1 は script末尾
  `[ "$RC" -ne 0 ] && exit` idiom由来の benign (各pass rc=0・audit gates全PASS)。
- D6 third-impl targets 8キー×2-run (a/b): det-pair 8/8・verdict agreement
  8/8 (全WIN result 1・expect_third: 1 と一致)。第三実装expansions (pass-one
  合計 76,220,056) は実装依存のため pinned nodes との直接比較はしない。
- D7 audit ×3: `ALL 323 GATES PASS; verdict agreements 8/8 (WIN=8 LOSS=0);
  inconclusive=0`・stdout 3回 byte-identical (`96e59f21…`)・
  audit-summary.json `ffe227b3…`。
- D8 tamper battery 4/4捕捉・復帰green: T1 replica aa014 p1/p2 nodes+1 →
  `replica-aa014-verdict-vs-published` gate FAIL / T2 target aa010.a result
  1→2 → `target-aa010-det-pair` gate FAIL / T3 anchor k02a.a expansions
  9,106,337→9,106,336 → `anchor-k02a-a-expansions` gate FAIL / T4 rows.json
  aa040 replica_nodes +1 → `replica-aa040-verdict-vs-published` gate FAIL。
  各改竄 byte-exact復元 (rows.jsonはpin `e184c50b…` と事後照合)・復帰後
  green再実行 PASS。
- verdict不消費: 対象8行は honest WIN labels のまま。**標準11×11空盤・19
  central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 (54キーすべて・P2の8キー含む) は本Partの前後を通じてすべて
  UNKNOWNのまま。**
