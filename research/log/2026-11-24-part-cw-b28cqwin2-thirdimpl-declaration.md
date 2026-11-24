# Part CW 宣言: batch-28 (class 5343) Part CQ 20M再probe新解決WIN 2行 (aa004/aa035) の第三実装交叉検証 + 本host pinned-replica 2-pass + Part CO出版物unadopted補強gate 着手 (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `f6635144`
(Part CU D: batch-29 16-LOSS adoption reaudit outputs・2026-11-24T00:24:08Z過ぎ・
CU C `2c2487f7` で canonical merged 6,317行 `30ddad9d…` 出版済み)。

## 対象と目的

Part CQ (`research/experiments/n11-centralreply-class5343-b28exhausted-reprobe-20261123/`)
で**20M条件で新しく解決された batch-28 (closure class 5343) の WIN 2行**:

- **aa004**: key (1171516445255794689, 0)・s5 118693・legal 91・result **1 (WIN)**・
  nodes 15,616,012 (published 2-pass node-exact)
- **aa035**: key (1152921504606846978, 4228)・s5 199720・legal 96・result **1 (WIN)**・
  nodes 15,424,243 (published 2-pass node-exact)

に対し、pinned第三実装 `third_impl.js` `08ea958f…` (非df-pn AND/ORミニマックス)
による verdict-level 交叉検証 (各キー a/b 2-run determinism pair) と、本host
pinned-replica `jsreplay.js` `84585617…` 2-pass fresh-cold再現
(`run_replica_cw.sh`・budget 20M = published CQ reprobe条件) を行う。
併せて Part CO adoption出版物 (merged canonical cache `854800f3…` 6,301行 /
increment `bd5ef7d7…` 7行 / increments-manifest `b47e07ca…`) に対する
**unadopted補強機械gate** (audit_cw.py G6) を設ける。

**verdict不消費**: 2行はhonest labelのまま。本Partはいかなるadoption・解放・
閉鎖も行わない。採用は scrutiny owner C++第二実装 gate `9193f5b6…` を経て
別adoption Part (pinned fail-closed merger `90711961…` 経由) のみ。
閉鎖・被覆・secured・root勝敗の主張はしない。
**標準11×11空盤・19 central-reply roots・class 5343・全キー (batch-28 54キーを
含む) はUNKNOWNのまま**。nodes数・expansions数を勝敗として読まない。

## 単一オーナー・非接触の機械確認 (observed HEAD 2c2487f7)

- **Part CU** (宣言 `d8276573`・batch-29 class 2251 の16-LOSS canonical adoption・
  A `b8ece461` / B `24111596` / C `2c2487f7` / D `f6635144` 進行中) — batch-29
  LOSS 16行の採用とcanonical chain更新 (最新 merged 6,317行 `30ddad9d…`) を担う
  別レーン。
  **非接触**: 対象キー (batch-28 aa004/aa035)・class (5343 vs 2251)・バッチ
  (28 vs 29) が全く別で、CUのadoptionはbatch-29 LOSS行のみを扱う。
- **Part CV** (宣言 `a8592d9c`・batch-29 ckpt-1/3 LOSS 16行 ab001..ab016 の
  row-audit + replica + 第三実装交叉検証・A `3a78cd3e`) — 同じくbatch-29 LOSS
  別レーン。**非接触** (対象キー・class完全に別)。
- 既存のbatch-28第三実装交叉検証は aa001/aa002 (b28win) / aa003 (drive2loss) /
  aa006/aa007 (drive2win) / aa008/aa009 (drive3win) の7行のみで、**aa004/aa035
  は未カバー** (published experimentsのrows.json対象一覧で機械確認済み)。
- 本宣言時点で batch-28 CQ-WIN 2行の第三実装交叉検証を宣言した対抗レーンなし。

## canonical chain に対する位置づけ (誠実開示)

Part CU C (`2c2487f7`・00:23:54Z) により canonical merged chain は **6,317行
`30ddad9d…`** に更新済み (batch-29 LOSS 16行採用)。CU D (`f6635144`) はその
reaudit outputs出版。本Part (CW) はそれに**読みも書きも
しない**: G6のpin対象はPart CO時点のmerged canonical cache `854800f3…`
(6,301行) のcommit-pinned byte snapshotであり、「unchanged」pinは
「本Partがcanonical cacheに一切書き込まない」ことと「pinしたsnapshot bytesが
採用後も不変であること」を意味する (Part CUの正当な更新とは独立)。aa004/aa035
のrowは (verdict不消費により) どのcanonical cache snapshotにも存在しないはず
であり、実行記録において最新snapshot (Part CU C `30ddad9d…`) に対する
補助的機械不在確認を追加で行い記録する (pinned kit gateとは別の記録として)。

## Part CR (audit `2ab974c3…` / maker `364a217f…`) からの宣言済み派生点

1. EXP/schema名: `n11-centralreply-closure-b28cqwin2-thirdimpl-20261124` /
   rows `…-thirdimpl-input-v1` / audit `…-thirdimpl-audit-v1`。
2. 対象: batch-30 drive-1 4行 (2 WIN + 2 LOSS) → batch-28 CQ-WIN 2行 (両方WIN)。
   rows.jsonの `unadopted_loss_rows` は true → **false** (本PartにLOSS行なし)。
3. replica予算: 15M → **20M** (published CQ reprobe条件・`run_replica_cw.sh`
   `8c123b65…` はpublished CR runner `7980b2fb…` の機能diff予算1行のみの派生)。
4. G6 unadopted id-list gate の batch-28 適合 (最重要派生): aa004/aa035は
   batch-28メンバのため manifestの probed_ids/resolved_ids に正当に存在し、
   また CO時点では15M EXHAUSTEDだったため exhausted_excluded_ids (11行) に
   存在する。CRの「あらゆるid listに不在」gateを「**adopted/win系id list
   (loss_ids/win_ids/unadopted_win_ids/unadopted_win_rows/adopted_loss_ids/
   already_adopted_ids/fragment_ids) に不在** かつ **exhausted_excluded_ids
   (top-level + batch block) と probed_ids/resolved_ids に存在**」に置換。
   併せて新規のcross-artifact整合gate: CQ status PASS roster (13キー) から
   anchors {aa036, aa046} を除いた11キーが manifest exhausted_excluded_ids
   と完全一致することを機械検査。merged cache内「対象row不在」「同key衝突row
   ゼロ」gateはCRと同一。
5. CQ completion log はsha pin表を持たないため、CRのpin表機械解析gateを
   **phrase battery + raw bytes直接pin (PIN_RAW 4件)** に置換 (宣言済み)。

## 事前実行済み (publish-then-executeの許容範囲: solver非実行)

- maker `make_inputs_cw.py` ×2回実行 **byte-stable PASS** (rows.json
  `4a69c73f…`)。input CSV 6件はpublished (CQ/BF) とbyte一致。
- maker tamper電池 8/8検出 (scratch copy上・実験dir bytes不変): T1 raw nodes+1 /
  T2 status verdict反転 / T3 README文言反転 / T4 completion log nodes+1 /
  T5 batch-keys s5_index+1 / T6 published-input legal反転 / T7 increment nodes+1 /
  T8 manifest exhausted roster からaa004除去 → 全てABORT。
  誠実記録: 初回のT3/T5はsedパターン不適合で無効果 (makerが正常PASS) したため、
  適用実効性をassertした sed/python で再実行し検出を確認 (Part CM/CRの
  efficacy-asserted設計踏襲)。clean control PASS (rows.json byte-identical)。

## 実行protocol (宣言後)

- D1 rules gate (pinned `verify_tbl.js` `c8c52528…`): quads/triples比較を
  `output/rules-gate.txt` に記録。
- D2 val-gate fresh 4 (本host・published baselines node-exact・wall_s比較外)。
- D3 negatives ng1/ng2 GATE_FAIL設計どおり。
- D4 anchors k02a/l1a 各a/b (published値とnode-exact)。
- D5 replica aa004/aa035 各p1/p2 (budget 20M・inner timeout 260)。
- D6 targets aa004/aa035 各a/b第三実装 (cap 300M・wallcap 240・memo-power 22)。
- D7 audit `audit_cw.py` ×3 byte-identical + clean control + tamper電池
  (audit-side A1-A4)。
- D8 B outputs出版 → C README最終 + MANIFEST-sha256 → 完了log出版
  (各push前後に最新main再取得・fetch-back byte一致検証・競合時は無理押し
  せず記録して次回へ)。

長時間探索・driveは行わない (本Partは交叉検証と監査のみ・計算量は
replica 2キー×2pass (各~90s) + 第三実装 2キー×2run + anchors 4 run 程度)。
