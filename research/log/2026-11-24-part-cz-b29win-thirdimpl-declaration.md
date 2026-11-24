# Part CZ 宣言: batch-29 (class 2251) Part CI takeover drive-2 WIN 1行 (ab028) の第三実装交叉検証 + 本host pinned-replica 2-pass + Part CU出版物unadopted補強gate 着手 (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `39f29652`
(Part CY B: batch-31 drive-1 outputs・2026-11-24T02:06:08Z。直前は
Part CI takeover drive-2 completion log `141cf80c`: batch-29 全54キー
probe-complete LOSS 53 / WIN 1 (ab028) / EXHAUSTED 0・2026-11-24T01:59:32Z)。

## 対象と目的

Part CI takeover drive-2
(`research/experiments/n11-centralreply-closure-class2251-batch29-20261123/`・
完了log commit `141cf80c`) で **15M fresh-cold 2-pass条件で解決した batch-29
(closure class 2251) の WIN 1行**:

- **ab028**: key (1297036830121656320, 131074)・s5 93815・legal 80・
  membership 3・result **1 (WIN)**・nodes 3,167,121 (published 2-pass
  node-exact・status.log 55行 = 54 PASS + 1 WIN-HALT のWIN-HALT対象キー)

に対し、pinned第三実装 `third_impl.js` `08ea958f…` (非df-pn AND/ORミニマックス)
による verdict-level 交叉検証 (a/b 2-run determinism pair) と、本host
pinned-replica `jsreplay.js` `84585617…` 2-pass fresh-cold再現
(`run_replica_cz.sh` `cb909064…`・budget **15M** = published batch-29 drive-2
probe条件・published CW runner `8c123b65…` の機能diff予算1行のみの派生) を
行う。併せて Part CU adoption出版物 (merged canonical cache `30ddad9d…`
6,317行 = CO base `854800f3…` 6,301行 + 採用16行 / increment `bab011e3…`
16行 / increments-manifest `f9f58ee1…`) に対する **unadopted補強機械gate**
(audit_cz.py G6) を設ける。

**verdict不消費**: ab028はhonest labelのまま。本Partはいかなるadoption・解放・
閉鎖も行わない。採用は scrutiny owner C++第二実装 gate `9193f5b6…` を経て
別adoption Part (pinned fail-closed merger `90711961…` 経由) のみ。
閉鎖・被覆・secured・root勝敗の主張はしない。
**標準11×11空盤・central-reply roots・class 2251・全キー (batch-29 54キーを
含む) はUNKNOWNのまま**。nodes数・expansions数を勝敗として読まない。

## 単一オーナー・非接触の機械確認 (observed HEAD 39f29652)

- **Part CP takeover** (宣言 `87e19b5a`・batch-30 class 34269 drive-2 WIN-CONTINUE
  残50キー ac005..ac054) — 別バッチ・別class。**非接触**。
- **Part CY** (宣言 `afc1bcc5`・batch-31 class 5804 55-key probe・A `6197f658` /
  B `3f77a007` / C `190820c7` / B outputs `39f29652` 進行中) — 別バッチ・別class。
  **非接触**。
- **Part CX** (宣言 `1300c10d` 00:49:31Z・batch-28 CQ 20M再probe新解決WIN
  残5行 aa005/aa030/aa031/aa047/aa053 の交叉検証) — 同種作業だが対象は
  batch-28のみ。**非接触** (対象キー・class完全に別)。
- batch-29の既存第三実装交叉検証は Part CV (宣言 `a8592d9c`・完了
  `3b6ad066`) のckpt-1/3 **LOSS 16行 ab001..ab016 のみ**で、**ab028
  (drive-2 WIN行) は未カバー** (published Part CV rows.json対象一覧で
  機械確認済み)。本宣言時点で ab028 の第三実装交叉検験を宣言した対抗
  レーンなし。
- 対象キー ab028 は Part CU increments-manifest 上 fileless UNPROBED
  (batches[0].fileless_unprobed_ids 38キーroster内・機械確認済み) であり、
  採用 (adoption) 作業対象でもない。

## canonical chain に対する位置づけ (誠実開示)

Part CU C (`2c2487f7`) により canonical merged chain は 6,317行 `30ddad9d…`
(batch-29 LOSS 16行採用済み) が最新。本Part (CZ) の G6 pin対象はこの
`30ddad9d…` snapshotそのものであり、**読みのみ**で一切書き込まない。
ab028のrowは (verdict不消費により) このcacheにも Part CO base `854800f3…`
にも存在しないことがkit gate (maker・audit両方) で機械検証される。
WIN行ab028が今後採用される場合は scrutiny owner C++ gate 経由の別Part専権。

## Part CW (audit `a7876a0a…` / maker `8a9fe75e…` / runner `8c123b65…`) からの宣言済み派生点

1. EXP/schema名: `n11-centralreply-closure-b29ab028win-thirdimpl-20261124` /
   rows `…-thirdimpl-input-v1` / audit `…-thirdimpl-audit-v1`。
2. 対象: batch-28 CQ-WIN 2行 (aa004/aa035) → **batch-29 drive-2 WIN 1行
   (ab028のみ)**。rows.jsonの `unadopted_win_rows` true /
   `unadopted_loss_rows` false (本PartにLOSS行なし・WIN行のみ)。
3. replica予算: 20M → **15M** (published batch-29 drive-2 probe条件)。
4. G6 unadopted id-list gate の batch-29/CU適合 (最重要派生): ab028は
   batch-29メンバでCU時点 fileless UNPROBED のため、CWの
   「exhausted_excluded_ids / probed_ids 系所属」gateを
   「**adopted/win/probed系id list (loss_ids / win_ids /
   unadopted_win_ids / unadopted_win_rows / batches adopted_loss_ids /
   already_adopted_ids / fragment_ids / probed_ids / resolved_ids) に不在**
   かつ **fileless_unprobed_ids (38キー) に存在**」に置換。manifestの
   status_log_sha256 prefix pin (`6b877344…`・16行) でCU出版物との
   byte連鎖も機械検証。merged cache内「対象row不在」「6,317行台」「同key
   衝突rowゼロ」gateはCWと同一。
5. CQ completion log はsha pin表を持たないため、CRのpin表機械解析gateを
   **phrase battery + raw bytes直接pin (PIN_RAW 2件: ab028 p1/p2)** に
   置換 (CWと同一設計・drive-2 completion log `46c461bd…` 適合)。

## 事前実行済み (publish-then-executeの許容範囲: solver非実行)

- maker `make_inputs_cz.py` `782e8937…` ×2回実行 **byte-stable PASS**
  (rows.json `d8c53d29…`)。input CSV 5件はpublished (drive-2正本出力 /
  Part BF) とbyte一致 (ab028 `1d0416af…`・k02a `b6174a3f…`・l1a
  `e13d2a6c…`・ng1 `8e64b9ad…`・ng2 `f19cd5a3…`)。
- maker tamper電池 **8/8検出** (scratch copy上・experiment bytes不変・
  efficacy-asserted): T1 raw nodes+1 / T2 status-b29.log ab028行verdict
  反転 / T3 README rank句改変 / T4 completion log nodes+1 / T5 batch-keys
  ab028 s5_index+1 / T6 published-input legal反転 / T7 increment nodes+1 /
  T8 manifest fileless roster ab028除去 → 全てABORT。
  誠実記録: T3は初回 (「LOSS 53」句置換) がassertで不適合検出により
  未適用だったため、実在句 (rank 35 class 2251) で再実行し検出を確認。
  clean control PASS (rows.json `d8c53d29…` byte-identical)。
- audit `audit_cz.py` `3c95e32f…` は**合成データkit上**でスモークテスト済み:
  全79 gate PASS ×3回 byte-identical + audit-side tamper電池 **10/10
  fail-closed検出** (T1 target verdict divergence / T2 replica pair
  divergence / T3 merged-cache改変 / T4 manifest fileless-roster除去
  〔size gate先発火も含む〕/ T4b roster内ab028 swap〔pin差し替え下で
  対象gate発火〕/ T5 malformed negative行 / T6 rules-gate mismatch /
  T7 val-gate node drift / T8 malformed target行 / T9 target行の
  GATE_FAIL 〔present gate fail-closed〕)。
  誠実記録: スモークテスト中に malformed third行でtracebackクラッシュする
  弱点を発見し、fail-closedの名前付きgateとして扱うよう修正済み
  (本宣言のsha `3c95e32f…` が修正後)。合成kitは実験dirとは別の
  ローカルscratchで実施・実験bytes不変・solver未実行。

## 実行protocol (宣言後)

- D1 rules gate (pinned `verify_tbl.js` `c8c52528…`): quads/triples比較を
  `output/rules-gate.txt` に記録 (期待: replica quads 95670 mine quads
  95670・mismatches 0)。
- D2 val-gate fresh 4 (本host・published baselines node-exact・wall_s
  比較外・出力は `.cz-host.out`)。
- D3 negatives ng1/ng2 GATE_FAIL設計どおり (legal+1 / stones 6)。
- D4 anchors k02a/l1a 各a/b (published値とnode-exact: k02a WIN
  expansions 9,106,337・ttHits 4,991,527 / l1a LOSS expansions
  7,660,602・ttHits 3,951,175)。
- D5 replica ab028 p1/p2 (budget 15M・inner timeout 260・determinism
  fields p1==p2・published raw fields node-exact)。
- D6 targets ab028 a/b第三実装 (cap 300M・wallcap 240・memo-power 22・
  verbatim入力CSV stringキー)。
- D7 audit `audit_cz.py` ×3 byte-identical (schema
  `n11-centralreply-closure-b29ab028win-thirdimpl-audit-v1`) +
  audit-summary.json出版。
- D8 B outputs出版 → C README最終 + MANIFEST-sha256 → 完了log出版
  (各push前後に最新main再取得・fetch-back byte一致検証・競合時は無理押し
  せず記録して次回へ)。

長時間探索・driveは行わない (本Partは交叉検証と監査のみ・計算量は
replica 1キー×2pass (~30-90s/pass) + 第三実装 1キー×2run (bounded by
cap/wallcap) + anchors 4 run 程度)。
