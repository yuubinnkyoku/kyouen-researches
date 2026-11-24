# Part CX 宣言: batch-28 (class 5343) Part CQ 20M再probe新解決WIN 残5行 (aa005/aa030/aa031/aa047/aa053) の第三実装交叉検証 + 本host pinned-replica 2-pass + Part CO出版物unadopted補強gate 着手 (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `1dcd7cc5`
(Part CW completion log訂正・2026-11-24T00:45:20Z・CWのEXHAUSTED残0行事実誤記
訂正 `cd29566a` (experiment README+MANIFEST) に続くlog訂正commit)。

## 対象と目的

Part CQ (`research/experiments/n11-centralreply-class5343-b28exhausted-reprobe-20261123/`)
で**20M条件で新しく解決された batch-28 (closure class 5343) の WIN 行のうち、
Part CW (`n11-centralreply-closure-b28cqwin2-thirdimpl-20261124`) が交叉検証した
aa004/aa035 を除く残り5行**:

- **aa005**: key (1171516445255794690, 0)・s5 124331・legal 89・result **1 (WIN)**・
  nodes 15,957,877 (published 2-pass node-exact)
- **aa030**: key (1243574039293722624, 0)・s5 199715・legal 90・result **1 (WIN)**・
  nodes 16,765,560 (published 2-pass node-exact)
- **aa031**: key (1459746821407506432, 0)・s5 199716・legal 92・result **1 (WIN)**・
  nodes 17,185,014 (published 2-pass node-exact)
- **aa047**: key (1152921504611041280, 4228)・s5 199732・legal 92・result **1 (WIN)**・
  nodes 16,230,465 (published 2-pass node-exact)
- **aa053**: key (1152921504606855168, 4228)・s5 199738・legal 95・result **1 (WIN)**・
  nodes 16,685,872 (published 2-pass node-exact)

に対し、pinned第三実装 `third_impl.js` `08ea958f…` (非df-pn AND/ORミニマックス)
による verdict-level 交叉検証 (各キー a/b 2-run determinism pair) と、本host
pinned-replica `jsreplay.js` `84585617…` 2-pass fresh-cold再現
(`run_replica_cx.sh`・budget 20M = published CQ reprobe条件) を行う。
併せて Part CO adoption出版物 (merged canonical cache `854800f3…` 6,301行 /
increment `bd5ef7d7…` 7行 / increments-manifest `b47e07ca…`) に対する
**unadopted補強機械gate** (audit_cx.py G6) を設ける。

**verdict不消費**: 5行はhonest labelのまま。本Partはいかなるadoption・解放・
閉鎖も行わない。採用は scrutiny owner C++第二実装 gate `9193f5b6…` を経て
別adoption Part (pinned fail-closed merger `90711961…` 経由) のみ。
閉鎖・被覆・secured・root勝敗の主張はしない。
**標準11×11空盤・19 central-reply roots・class 5343・全キー (batch-28 54キーを
含む) はUNKNOWNのまま**。nodes数・expansions数を勝敗として読まない。

## 単一オーナー・非接触の機械確認 (observed HEAD 1dcd7cc5)

- **Part CW 完結済み** (aa004/aa035・宣言 `ba08e1cf` → 完了log `8f03ed3d`)・
  誤記訂正2commit (`cd29566a`/`1dcd7cc5`) 出版済み。CW対象 (aa004/aa035) と
  CX対象5行は互いに排他 (CQ解決WIN 7行の分割)。
- **Part CV** (宣言 `a8592d9c`・batch-29 ckpt-1/3 LOSS 16行 ab001..ab016 の
  row-audit + replica + 第三実装交叉検験) — batch-29 / class 2251 の別レーン。
  **非接触** (対象キー・class・バッチが全く別)。
- 既存のbatch-28第三実装交叉検証は published rows.json対象一覧で機械確認:
  b28win (aa001/aa002) / b28drive2loss (aa003) / b28drive2win (aa006/aa007) /
  b28drive3win (aa008/aa009) / b28cqwin2 (aa004/aa035) の9行のみで、
  **aa005/aa030/aa031/aa047/aa053 は未カバー** (published rows.jsonの
  targets key_id一覧をfetch照合済み・CS/CT解決分 aa021/aa028/aa032/aa050も
  同様に未カバーで、それらは本Part対象外のまま次回候補)。
- 本宣言時点で batch-28 CQ-WIN 残5行の第三実装交叉検証を宣言した対抗レーン
  なし (observed HEAD `1dcd7cc5` のcommit列に該当宣言なし)。Part文字CXは
  main未使用 (commit列機械確認)。

## canonical chain に対する位置づけ (誠実開示)

Part CU C (`2c2487f7`) により canonical merged chain は **6,317行 `30ddad9d…`**
に更新済み (batch-29 LOSS 16行採用)。本Part (CX) はそれに**読みも書きも
しない**: G6のpin対象はPart CO時点のmerged canonical cache `854800f3…`
(6,301行) のcommit-pinned byte snapshotであり、「unchanged」pinは
「本Partがcanonical cacheに一切書き込まない」ことと「pinしたsnapshot bytesが
採用後も不変であること」を意味する。5対象のrowは (verdict不消費により)
どのcanonical cache snapshotにも存在しないはずであり、実行記録において
最新snapshot (Part CU C `30ddad9d…`) に対する補助的機械不在確認を追加で行い
記録する (pinned kit gateとは別の記録として)。Part CWの補助確認で
aa004/aa035キーのrowは0行と確認済み。

## Part CW kit (maker `8a9fe75e…` / audit `a7876a0a…`) からの宣言済み派生点

1. EXP/schema名: `n11-centralreply-closure-b28cqwin5-thirdimpl-20261124` /
   rows `…-input-v1` / audit `…-audit-v1`。
2. 対象: batch-28 CQ-WIN 2行 (aa004/aa035) → **残5行 (aa005/aa030/aa031/
   aa047/aa053・全てWIN)**。PIN_RAW 4件 → **10件** (5キー×p1/p2)。
   PIN_PUB_INPUT 2件 → 5件。EXPECT_S5/EXPECT_REPLICA等をpublished値に更新
   (aa005 124331/15,957,877・aa030 199715/16,765,560・aa031 199716/17,185,014・
   aa047 199732/16,230,465・aa053 199738/16,685,872 machine-extracted)。
   rows.jsonの `unadopted_loss_rows` は falseのまま (本PartにLOSS行なし)。
3. replica予算: 20M不変 (=published CQ reprobe条件)。`run_replica_cx.sh`
   `6d05701c…` はpublished CW runner `8c123b65…` の**ヘッダコメントdiffのみ**
   (機能body機械diff照合で完全一致・budget 20Mも不変)。
4. audit target-count gate 2→5・target-verdict-kinds [1,1]→[1,1,1,1,1]・
   val-gate host出力suffix `.cw-host.out`→`.cx-host.out`。G6 unadopted
   id-list gate (batch-28適合版) はCWと同一ロジック・対象のみ5行に拡大
   (5行ともexhausted_excluded_ids (CO-time 15M EXHAUSTED roster)・
   probed_ids/resolved_idsに正当存在し、adopted/win系id listに不在を要求)。
5. status-cq.log / README-cq / log-cq phrase battery・anchors k02a/l1a
   (9,106,337/4,991,527・7,660,602/3,951,175)・negatives ng1/ng2・val-gate 4定数
   (2M×2 exhaustion・3,651,923・5,040,200) はすべてCWから不変再利用。

## 事前実行済み (publish-then-executeの許容範囲: solver非実行)

- maker `make_inputs_cx.py` (sha256 `7abf48c5…`) ×2回実行 **byte-stable PASS**
  (rows.json `3a87c5b6…`・両回byte一致)。input CSV 9件はpublished (CQ/BF) と
  byte一致 (sha256直照合)。audit `audit_cx.py` (sha256 `87152e94…`) は
  構文検査済み (実行は solver outputs生成後)。
- maker tamper電池 **8/8検出** (scratch copy上・experiment bytes不変事後sha照合):
  T1 aa005 raw p1 nodes+1 / T2 aa030 status verdict反転 (1→2) / T3 README-cqの
  aa005 nodes文言反転 / T4 completion logのaa031 nodes文言反転 / T5 batch-keys
  aa031 s5_index+1 / T6 aa047 published-input legal反転 (92→93) / T7 increment
  (aa036 row) nodes+1 / T8 increments-manifest exhausted_excluded_ids から
  aa005除去 → 全てABORT (rc=1)。適用実効性は全tamperでassert済み
  (Part CM/CR/CWのefficacy-asserted設計踏襲)。clean control PASS
  (rows.json byte-identical)。
- sources 10 raw + 5 published-input CSVはCQ実験dirからcommit-pinned raw
  fetch (sha256 `39809a1d…`ほか10件・`404e59ee…`ほか5件)。

## 実行protocol (宣言後)

- D1 rules gate (pinned `verify_tbl.js` `c8c52528…`): quads/triples比較を
  `output/rules-gate.txt` に記録。
- D2 val-gate fresh 4 (本host・published baselines node-exact・wall_s比較外
  ・`.cx-host.out`)。
- D3 negatives ng1/ng2 GATE_FAIL設計どおり。
- D4 anchors k02a/l1a 各a/b (published値とnode-exact)。
- D5 replica aa005/aa030/aa031/aa047/aa053 各p1/p2 (budget 20M・inner timeout 260
  ・1キー1 invocation・pass分離を許容)。
- D6 targets 5キー各a/b第三実装 (cap 300M・wallcap 240・memo-power 22)。
- D7 audit `audit_cx.py` ×3 byte-identical + clean control + tamper電池
  (audit-side A1-A4)。
- D8 B outputs出版 → C README最終 + MANIFEST-sha256 → 完了log出版
  (各push前後に最新main再取得・fetch-back byte一致検証・競合時は無理押し
  せず記録して次回へ)。

長時間探索・driveは行わない (本Partは交叉検証と監査のみ・計算量は
replica 5キー×2pass (各~85-100s) + 第三実装 5キー×2run (各~55-65s) +
anchors 4 run 程度)。
