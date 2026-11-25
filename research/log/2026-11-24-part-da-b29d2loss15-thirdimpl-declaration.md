# Part DA 宣言: batch-29 (class 2251) Part CI takeover drive-2 ckpt-2/3 LOSS 15行 (ab017..ab027 + ab029..ab032) の第三実装交叉検証 + 本host pinned-replica 2-pass + Part CU出版物unadopted補強gate 着手 (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `7ff09bb8`
(Part CY drive-2 incident amendment・2026-11-24T02:20:27Z。直前は Part CZ
完了log `68751fd7`: batch-29 drive-2 WIN行 ab028 three-implementation
corroboration 成立・2026-11-24T02:13:18Z)。

## 対象と目的

Part CI takeover drive-2
(`research/experiments/n11-centralreply-closure-class2251-batch29-20261123/`・
完了log commit `141cf80c`: batch-29 全54キー probe-complete LOSS 53 / WIN 1
(ab028) / EXHAUSTED 0) で **15M fresh-cold 2-pass条件で解決した batch-29
(closure class 2251) の drive-2 ckpt-2/3 LOSS 15行**:

| key | lo / hi | legal | s5 | membership | result | nodes |
|---|---|---|---|---|---|---|
| ab017 | 1155314076402843648 / 0 | 93 | 78838 | 4 | 2 (LOSS) | 3,366,331 |
| ab018 | 1299429230118961152 / 0 | 83 | 84223 | 4 | 2 (LOSS) | 6,998,686 |
| ab019 | 1155314316921012224 / 0 | 88 | 86005 | 3 | 2 (LOSS) | 2,623,573 |
| ab020 | 1155331634229149696 / 0 | 85 | 87025 | 4 | 2 (LOSS) | 3,020,397 |
| ab021 | 1155349226415194112 / 0 | 89 | 89372 | 4 | 2 (LOSS) | 3,748,592 |
| ab022 | 1155384410787282944 / 0 | 79 | 91588 | 4 | 2 (LOSS) | 4,620,753 |
| ab023 | 1155876991996526592 / 0 | 86 | 93761 | 3 | 2 (LOSS) | 8,695,465 |
| ab024 | 1155314042043105280 / 32 | 90 | 93811 | 4 | 2 (LOSS) | 4,131,850 |
| ab025 | 1155314042043105280 / 64 | 93 | 93812 | 4 | 2 (LOSS) | 3,832,650 |
| ab026 | 5908722848549044224 / 131072 | 86 | 93813 | 3 | 2 (LOSS) | 1,835,150 |
| ab027 | 1297036830121656832 / 131072 | 101 | 93814 | 4 | 2 (LOSS) | 4,364,868 |
| ab029 | 1155314042043105280 / 16 | 97 | 93816 | 4 | 2 (LOSS) | 2,583,183 |
| ab030 | 1191342839062069248 / 0 | 88 | 93817 | 4 | 2 (LOSS) | 7,694,235 |
| ab031 | 1227371636081033216 / 0 | 94 | 93818 | 4 | 2 (LOSS) | 2,973,520 |
| ab032 | 1443544418194817024 / 0 | 93 | 93819 | 4 | 2 (LOSS) | 3,320,290 |

(全行 status-b29.log `b49322d9…` PASS行 (budget 15000000, result 2,
nodes) とcross-check済み。ab029/ab031 はraw p1/p2 byte同一 (wall同秒・
正当)。WIN行 ab028 は**対象外**: Part CZ `68751fd7` で成立済み。)

これら15行に対し、pinned第三実装 `third_impl.js` `08ea958f…` (非df-pn
AND/ORミニマックス) による verdict-level 交叉検証 (各キー a/b 2-run
determinism pair) と、本host pinned-replica `jsreplay.js` `84585617…`
2-pass fresh-cold再現 (`run_replica_da.sh` `f0b4c6f0…`・budget **15M** =
published batch-29 drive-2 probe条件・CZ runner `cb909064…` の文言のみ
DA化) を行う。併せて Part CU adoption出版物 (merged canonical cache
`30ddad9d…` 6,317行 = CO base `854800f3…` 6,301行 + 採用16行 /
increment `bab011e3…` 16行 / increments-manifest `f9f58ee1…`) に対する
**unadopted補強機械gate** (audit_da.py G6) を設ける。

**verdict不消費**: 15行はhonest labelのまま。本Partはいかなるadoption・
解放・閉鎖も行わない。採用 (canonical cache merge) は CU先例の
pinned fail-closed merger `90711961…` を経由する別adoption Part専権。
WIN行 ab028 の採用は引き続き scrutiny owner C++第二実装 gate
`9193f5b6…` 経由。
閉鎖・被覆・secured・root勝敗の主張はしない。
**標準11×11空盤・central-reply roots・class 2251・全キー (batch-29
54キーを含む) はUNKNOWNのまま**。nodes数・expansions数を勝敗として
読まない。

## 単一オーナー・非接触の機械確認 (observed HEAD 7ff09bb8)

- **Part CP takeover** (batch-30 class 34269 drive-2・宣言 `21fef631`
  時点のscaffold言及と進行中 checkpoint `dd660ce7` ac005..ac021) —
  別バッチ・別class。**非接触**。
- **Part CY** (batch-31 class 5804 drive-2宣言 `21fef631`・drive-2
  val-gate `68f80a85`・incident amendment `7ff09bb8`) — 別バッチ・別
  class。**非接触**。
- **Part CX** (宣言 `1300c10d`・batch-28 CQ 20M再probe新解決WIN 5行) —
  同種作業だが対象はbatch-28のみ。**非接触** (対象キー・class完全に別)。
- **Part CZ** (宣言 `4c741798`・完了 `68751fd7`): batch-29 drive-2 **WIN
  1行 ab028 のみ**。**本Part対象の15 LOSS行は未カバー**。
- **Part CV** (宣言 `a8592d9c`・完了 `3b6ad066`): batch-29 **drive-1**
  ckpt-1/3 LOSS 16行 ab001..ab016 のみ。**drive-2 15行は未カバー**
  (published Part CV rows.json対象一覧で機械確認済み)。
- 本宣言時点 (observed HEAD `7ff09bb8`) で drive-2 ckpt-2/3 LOSS 15行の
  第三実装交叉検証を宣言した対抗レーンなし (直近15 commit機械走査)。
- 対象15キーは全て Part CU increments-manifest 上 fileless UNPROBED
  (batches[0].fileless_unprobed_ids 38キーroster内・kit maker/audit双方
  で機械gate済み) であり、採用 (adoption) 作業対象でもない。

## canonical chain に対する位置づけ (誠実開示)

Part CU C (`2c2487f7`) により canonical merged chain は 6,317行
`30ddad9d…` (batch-29 drive-1 LOSS 16行採用済み) が最新で CZ以降も
不変 (Part CZは読みのみで書き込みなし・本Partも同じ)。本Part (DA) の
G6 pin対象はこの `30ddad9d…` snapshotそのものであり、**読みのみ**で
一切書き込まない。15行のrowは (verdict不消費により) このcacheにも
Part CO base `854800f3…` にも存在しないことがkit gate (maker・audit
双方) で機械検証される。15 LOSS行の今後の採用は CU先例の別adoption
Part 専権 (cache 6,317行→6,332行相当のmerge・`90711961…` merger)。

## Part CZ (maker `782e8937…` / audit `3c95e32f…` / runner `cb909064…`) からの宣言済み派生点

1. EXP/schema名: `n11-centralreply-closure-b29d2loss15-thirdimpl-20261124` /
   rows `…-thirdimpl-input-v1` / audit `…-thirdimpl-audit-v1`。
2. 対象: CZのWIN 1行 (ab028) → **drive-2 ckpt-2/3 LOSS 15行**。
   rows.jsonの `unadopted_win_rows` false / `unadopted_loss_rows` true。
3. TARGETS 15・EXPECT_RESULT全件 2・EXPECT_REPLICA (=published nodes)
   15件 (makerがsources/raw 30 file (p1/p2) から機械導出・status-b29.log
   PASS行とcross-check)。
4. status-b29.log battery: WIN-HALT key == **exactly ab028** (CZでは
   WIN-HALT key == TARGETSだったのを分離)。各target PASS行 ==
   published drive-2 LOSS行 (15000000, 2, nodes pin)。ab028のPASS行
   (15000000, 1, 3167121) は**唯一の宣言済みresult-1例外**として
   node-pin gate化 (単なるexemptではなくpublished WIN行として緻密pin)。
5. G6 unadopted id-list gate: 対象15キー全員が adopted/win/probed系
   id list全不在・fileless_unprobed_ids (38キー) 在籍・merged cache
   (6,317行) に同key row不在 — CZと同一設計を15キーに拡張。
6. val-gate host出力suffix: `.cz-host.out` → `.da-host.out` (D2でfresh
   再生成。A kitにはpublished baselines+inputのみ同梱)。
7. PIN_RAW_DA 30ピン (15キー×p1/p2・published drive-2 raw fetch済み・
   batch-29 MANIFEST pin全件一致検証済みの published-input 15件の
   byte一致もmaker gate済み)。
8. rows.json pin: `8b212fd4d6193ea806b455a41d967f6270348ed57c3e513554374270ad1a9ffc`。

## 事前実行済み (publish-then-executeの許容範囲: solver非実行)

- maker `make_inputs_da.py` `2cfe8d32…` ×2回実行 **byte-stable PASS**
  (rows.json `8b212fd4…`・input CSV 19件 = targets 15 + anchors 2 +
  negatives 2。targets/anchors/negativesのCSVはpublished
  (drive-2正本出力 / Part BF) とbyte一致maker gate済み)。
- 誠実記録 (maker生成過程の重要修正): CZ makerからの流用生成スクリプト
  は EXPECT_* 辞書置換regexが複行dict前提 (`\n\}`) で単行dictに不適合
  だったため、単行・複行両対応の `re.search` + assert に修正してから
  36,023 byte版を確定 (最終sha `2cfe8d32…`)。ステータスbatteryも
  「非target drive-2行は全てresult 2」gateがab028 (published WIN行)
  で不当ABORTする設計欠陥を、WIN行node-pin例外gate化して修正。
- maker tamper電池 **9/9検出** (scratch copy上・experiment bytes不変・
  efficacy-asserted・各tamper後にclean control PASS): T1 raw nodes+1
  (ab017.p1・sha pin先発火) / T2 status-b29.log verdict反転 (ab021
  2→1) / T3b README改変 (主張句にバイト変化・sha pin先発火) /
  T4 completion log nodes+1 / T5 CU increment adopted row nodes改変 /
  T6 manifest fileless roster ab020除去 / T7 merged cache偽採用row
  追加 (ab030) / T8 非target drive-2行 verdict反転 (ab054) / T9
  batch-keys s5_index改変 (ab019) → 全てABORT。
  誠実記録: T3初回は改竄文言が実ファイルの改行をまたいだためreplaceが
  no-op (改竄未適用) で「検出されず」であり、実在句での byte変化を
  与え直してsha pin先発火検出を確認 (maker gate自体は有効)。
- audit `audit_da.py` `ca24423d…` は**合成データkit上**でスモークテスト
  済み (第三実装target行は合成プレースホルダ): **全429 gate PASS ×3回
  byte-identical** + audit-side tamper電池 **7/7 fail-closed検出**
  (A1 third verdict反転〔det-pair先発火〕/ A2 replica p2 nodes改変 /
  A3 rows.json改変〔rows-json-pin先発火〕/ A4 raw pin改変 (ab030.p1) /
  A5 manifest ab020をloss_idsへ追加〔shared sha-pin先発火〕/ A6 val-gate
  host nodes drift / A7 malformed third行〔present gate fail-closed〕)。
  全tamper後にclean control PASS。合成kitは実験dirとは別のローカル
  scratchで実施・実験bytes不変・第三実装solver未実行。
- 誠実開示: スモークの一環として published val-gate 4入力の本host
  pinned-replay (jsreplay.js) を宣言前に4回実行した (全て published
  baseline node-exact: 2M×2 result 0 / 15M×2 result 2 nodes
  3,651,923・5,040,200 — Part CY drive-2 val-gate `68f80a85` と同値の
  再現)。これらはreplay再現であり新規探索ではない。**D2では改めて
  fresh 4 runを `.da-host.out` として実行する** (smoke kitのhost出力は
  廃棄・実験dirに持ち込まない)。

## 実行protocol (宣言後)

- D1 rules gate (pinned `verify_tbl.js` `c8c52528…`): quads/triples比較を
  `output/rules-gate.txt` に記録 (期待: replica quads 95670 mine quads
  95670・mismatches 0)。
- D2 val-gate fresh 4 (本host・published baselines node-exact・wall_s
  比較外・出力は `.da-host.out`)。
- D3 negatives ng1/ng2 GATE_FAIL設計どおり (legal+1 / stones 6)。
- D4 anchors k02a/l1a 各a/b (published値とnode-exact: k02a WIN
  expansions 9,106,337・ttHits 4,991,527 / l1a LOSS expansions
  7,660,602・ttHits 3,951,175)。
- D5 replica 15キー×p1/p2 (budget 15M・inner timeout 260・determinism
  fields p1==p2・published raw fields node-exact)。
- D6 targets 15キー×a/b第三実装 (cap 300M・wallcap 240・memo-power 22・
  verbatim入力CSV stringキー)。wallcap到達時は **WALL-INCONCLUSIVE**
  として誠実記録し勝敗とは読まない (audit G5設計どおり)。
- D7 audit `audit_da.py` ×3 byte-identical (schema
  `n11-centralreply-closure-b29d2loss15-thirdimpl-audit-v1`) +
  audit-summary.json出版。
- D8 B outputs出版 → C README最終 + MANIFEST-sha256 → 完了log出版
  (各push前後に最新main再取得・fetch-back byte一致検証・競合時は無理押し
  せず記録して次回へ)。

長時間探索・driveは行わない (本Partは交叉検証と監査のみ・計算量は
replica 15キー×2pass (nodes 1.8M-8.7M・~1-30s/pass想定) + 第三実装
15キー×2run (bounded by cap/wallcap) + anchors 4 run 程度)。
