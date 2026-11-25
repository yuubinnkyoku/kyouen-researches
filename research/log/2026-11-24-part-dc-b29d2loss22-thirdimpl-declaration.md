# Part DC 宣言: batch-29 (class 2251) Part CI takeover drive-2 ckpt-3/3 LOSS 22行 (ab033..ab054) の第三実装交叉検証 + 本host pinned-replica 2-pass + Part CU出版物unadopted補強gate + Part DB出版物canonical事後補強gate (G6b) 着手 (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `d2d60645`
(Part DD drive-2 log CU→DB waypoint chain audit complete・2026-11-24T02:48:13Z。
直前は Part DD outputs `d4564f98` 02:47:31Z・`c2572cb5`・宣言直後A `048b69c5`
(n11 canonical S5 chain integrity independent TS re-audit PASS・read-only)。
push直前再取得でHEAD更新)。

## 対象と目的

Part CI takeover drive-2
(`research/experiments/n11-centralreply-closure-class2251-batch29-20261123/`・
完了log: batch-29 全54キー probe-complete LOSS 53 / WIN 1 (ab028) /
EXHAUSTED 0) で **15M fresh-cold 2-pass条件で解決した batch-29
(closure class 2251) の drive-2 ckpt-3/3 LOSS 22行**:

| key | lo / hi | legal | s5 | membership | result | nodes |
|---|---|---|---|---|---|---|
| ab033 | 1155314042043105280 / 4 | 99 | 93820 | 4 | 2 (LOSS) | 5,737,514 |
| ab034 | 1155314042043105280 / 16384 | 94 | 93821 | 4 | 2 (LOSS) | 2,421,190 |
| ab035 | 1155314042043105280 / 32768 | 97 | 93822 | 4 | 2 (LOSS) | 3,712,073 |
| ab036 | 1297036830121656320 / 131073 | 84 | 93823 | 2 | 2 (LOSS) | 5,512,708 |
| ab037 | 1297036830121657344 / 131072 | 96 | 93824 | 4 | 2 (LOSS) | 3,582,387 |
| ab038 | 1297036830121656576 / 131072 | 100 | 93825 | 4 | 2 (LOSS) | 7,949,979 |
| ab039 | 1155314042043105280 / 65536 | 87 | 93826 | 4 | 2 (LOSS) | 3,343,978 |
| ab040 | 1297045626214678528 / 131072 | 96 | 93827 | 4 | 2 (LOSS) | 3,796,441 |
| ab041 | 1315051228631138304 / 131072 | 99 | 93828 | 4 | 2 (LOSS) | 4,746,725 |
| ab042 | 1155314042043105280 / 131072 | 84 | 93829 | 4 | 2 (LOSS) | 1,926,643 |
| ab043 | 1155314042043105280 / 8 | 84 | 93830 | 4 | 2 (LOSS) | 3,003,611 |
| ab044 | 1297036831195398144 / 131072 | 95 | 93831 | 4 | 2 (LOSS) | 4,719,146 |
| ab045 | 1297039029144911872 / 131072 | 87 | 93832 | 4 | 2 (LOSS) | 3,978,891 |
| ab046 | 1301540429749026816 / 131072 | 94 | 93833 | 4 | 2 (LOSS) | 4,979,936 |
| ab047 | 1297036832269139968 / 131072 | 90 | 93834 | 4 | 2 (LOSS) | 5,604,561 |
| ab048 | 1297041228168167424 / 131072 | 96 | 93835 | 4 | 2 (LOSS) | 3,457,154 |
| ab049 | 1155314042043105280 / 8192 | 88 | 93836 | 4 | 2 (LOSS) | 4,332,757 |
| ab050 | 1306044029376397312 / 131072 | 98 | 93837 | 4 | 2 (LOSS) | 4,127,068 |
| ab051 | 1297036834416623616 / 131072 | 101 | 93838 | 4 | 2 (LOSS) | 6,906,311 |
| ab052 | 1297036830122180608 / 131072 | 95 | 93839 | 4 | 2 (LOSS) | 5,830,122 |
| ab053 | 1297036830122704896 / 131072 | 95 | 93840 | 4 | 2 (LOSS) | 2,832,769 |
| ab054 | 1297036830123753472 / 131072 | 95 | 93841 | 4 | 2 (LOSS) | 3,014,059 |

(全行 status-b29.log `b49322d9…` PASS行 (budget 15000000, result 2, nodes)
とcross-check済み・合計 95,516,023 nodes/pass。raw p1/p2 44 fileは
batch-29 MANIFEST pin全件一致検証済みのpublished正本とbyte一致maker gate
済み。WIN行 ab028 は**対象外**: Part CZ `68751fd7` で成立済み。drive-1
16行は**対象外**: Part CV `3b6ad066` で成立済み。ckpt-2/3 15行は**対象外**:
Part DA で成立済み。)

これら22行に対し、pinned第三実装 `third_impl.js` `08ea958f…` (非df-pn
AND/ORミニマックス) による verdict-level 交叉検証 (各キー a/b 2-run
determinism pair) と、本host pinned-replica `jsreplay.js` `84585617…`
2-pass fresh-cold再現 (`run_replica_dc.sh` `8ddf1ef4…`・budget **15M** =
published batch-29 drive-2 probe条件・CW runner `8c123b65…` と同じ条件で
文言のみDC化) を行う。

**verdict不消費**: 本Partはいかなるadoption・解放・閉鎖も行わない。
**誠実開示 (DB完了時刻との前後関係)**: 本Partのkit設計中 (CU snapshot
6,317行 `30ddad9d…` 時点のunadopted gate設計として着手) に、Part DB
(batch-29 drive-2 残37 LOSS行 canonical adoption・完了 `10a79660`
2026-11-24T02:40:07Z・increment 37行 `85bd4469…`・post-adoption
canonical merged cache 6,354行 `04b0a239…` = CU 6,317 + 37) が出版され、
対象22行はCU snapshot時点では未採用だったが (G6: CU merged cache
`30ddad9d…` に同key row不在をkit gateで機械検証)、**取材時点の現行
canonical chainには採用済み**となった。この事実を受けて本Partは
**G6b (post-DB canonical corroboration) を追加設計した**: 22行のtarget
rowが DB increment `85bd4469…` (37行) と DB post-adoption merged cache
`04b0a239…` (6,354行) の双方に (result 2, published nodes) で
**byte同一に存在**することをmaker・audit双方の機械gate化した
(cache sha pin + 行数gate + 22キー×2資产の行byte一致gate)。G6bは
**新しいverdictの主張でもcoverage/class statusの主張でもない**
(独立機械交叉照合)。本Partは读みのみで一切書き込まず、adoptionは
Part DBが完了済み・WIN行 ab028 の採用は引き続き scrutiny owner C++第二実装
gate `9193f5b6…` 経由。
閉鎖・被覆・secured・root勝敗の主張はしない。
**標準11×11空盤・central-reply roots・class 2251・全キー (batch-29
54キーを含む) はUNKNOWNのまま**。nodes数・expansions数を勝敗として
読まない。

## 単一オーナー・非接触の機械確認 (observed HEAD d2d60645)

- **Part DA** (宣言 `88ffdc92`・完了): batch-29 drive-2 **ckpt-2/3 LOSS
  15行** (ab017..ab027+ab029..ab032) のみ。**本Part対象22行は未カバー**。
- **Part DB** (宣言 `3bf90f67`・完了 `10a79660`): batch-29 37 LOSS行の
  canonical **adoption** (書き込み側)。本Partは読みのみの交叉検証であり
  書き込み競合なし。
- **Part DD** (宣言→完了 `d4564f98`): canonical chain integrity の独立TS
  re-audit (CU→DB waypoint)・read-only。本Partの第三実装交叉検証とは
  別物・非接触。
- **Part CZ** (宣言 `4c741798`・完了 `68751fd7`): drive-2 **WIN 1行
  ab028** のみ。
- **Part CV** (宣言 `a8592d9c`・完了 `3b6ad066`): batch-29 **drive-1**
  ckpt-1/3 LOSS 16行 ab001..ab016 のみ。
- **Part CX** (宣言 `1300c10d`): batch-28 (class 5343) のみ。別バッチ・
  別class。**非接触**。
- **Part CP takeover** (batch-30 class 34269)、**Part CY** (batch-31
  class 5804)、**高速レーン K1276/K1277** (クリティカルストリップ
  z=8/z=9スライス) — いずれも別バッチ・別class・別主题。**非接触**。
- 本宣言時点 (observed HEAD `d2d60645`) で drive-2 ckpt-3/3 LOSS 22行の
  第三実装交叉検証を宣言した対抗レーンなし (直近40 commit機械走査・
  experiments dir一覧でも `…b29d2loss22-thirdimpl…` は不在を機械確認)。
- 対象22キーは Part CU increments-manifest 上 fileless UNPROBED
  (batches[0].fileless_unprobed_ids 38キーroster内・kit maker/audit双方
  で機械gate済み)。Part DB後に published increments-manifest は本Partが
  読む CU版 `f9f58ee1…` の位置づけのまま (CU snapshot)。

## canonical chain に対する位置づけ (誠実開示)

現行 canonical merged chain は Part DB C (`951f7bcb`) により 6,354行
`04b0a239…` (WIN 158 / LOSS 6,196・CU 6,317行 `30ddad9d…` + drive-2
37 LOSS行採用)。本Partはこのcacheに**読みのみ**で書き込まない。
G6 pin対象は CU snapshot `30ddad9d…` (22行不在gate・歴史的unadopted
位置づけ) と、DB出版物 `85bd4469…` + `04b0a239…` (22行byte存在gate・
G6b) の双方。class 2251 の canonical unknown は DB後に 38→1 (残1行は
未消費WIN ab028) だが、これは Part DB完了log `10a79660` の記載であり、
本Partはこの状況を**追認も変化もさせない** (第三bridge実装による
verdict一致の独立証拠追加のみ)。

## Part DA (maker `2cfe8d32…` / audit `ca24423d…` / runner `f0b4c6f0…`) からの宣言済み派生点

1. EXP/schema名: `n11-centralreply-closure-b29d2loss22-thirdimpl-20261124` /
   rows `…-thirdimpl-input-v1` / audit `…-thirdimpl-audit-v1`
   (schema名はDAと同じ正文・行数違い。rows.json `schema` field
   `n11-centralreply-closure-b29d2loss22-thirdimpl-input-v1` で機械固定)。
2. 対象: DAの15行 (ckpt-2/3) → **ckpt-3/3 LOSS 22行** ab033..ab054。
   rows.jsonの `unadopted_win_rows` false・`unadopted_loss_rows` true・
   `consumed_into_canonical_cache` false (CU snapshot文脈)。
3. TARGETS 22・EXPECT_RESULT全件 2・EXPECT_REPLICA (=published nodes)
   22件・合計 95,516,023 nodes/pass (makerがsources/raw 44 file (p1/p2)
   から機械導出・status-b29.log PASS行とcross-check)。
4. status-b29.log battery: WIN-HALT key == **exactly ab028**。各target
   PASS行 == published drive-2 LOSS行 (15000000, 2, nodes pin)。ab028の
   PASS行 (15000000, 1, 3167121) は**唯一の宣言済みresult-1例外**として
   node-pin gate化 (DAと同一設計)。
5. G6 unadopted id-list gate: 対象22キー全員が adopted/win/probed系
   id list全不在・fileless_unprobed_ids (38キー) 在籍・CU merged cache
   (6,317行) に同key row不在 — DAと同一設計を22キーに拡張。
   **G6b (本Part追加)**: DB increment `85bd4469…` (s5verdict 37行) と
   DB merged cache `04b0a239…` (s5verdict 6,354行) の行数gateと、
   各target行 `s5verdict,{lo},{hi},5,2,{published nodes}` が両資产で
   byte一意存在maker ABORT gate + audit gate (maker 3 gate種・
   audit 48 gate)。
6. val-gate host出力suffix: `.da-host.out` → `.dc-host.out` (D2でfresh
   再生成。A kitにはpublished baselines+inputのみ同梱)。
7. PIN_RAW_DC 44ピン (22キー×p1/p2・published drive-2 raw fetch済み・
   batch-29 MANIFEST pin全件一致検証済みの published-input 22件の
   byte一致もmaker gate済み) + anchors/negatives published正本4件
   (k02a/l1a/ng1/ng2)。
8. rows.json pin: `64bc4b78711dbe1e3798116a670d669bcdd71865768bf9a0998bd50550dc13b6`
   (G6b追加後の改訂版。改訂前 `bb0efa0a…` は廃棄・未出版)。

## 事前実行済み (publish-then-executeの許容範囲: solver非実行)

- maker `make_inputs_dc.py` `94dfd45f…` ×2回実行 **byte-stable PASS**
  (全体tree hash 2回一致・rows.json `64bc4b78…`・input CSV 26件 =
  targets 22 + anchors 2 + negatives 2。targets/anchors/negativesのCSVは
  published (drive-2正本出力 / Part BF) とbyte一致maker gate済み)。
- 誠実記録 (G6b追加改訂): Part DB完了 (02:38-44Z) を受け、CU時点設計の
  kitに G6b投下 (maker: DB出版物sha pin 2件 + increment 37行/merged
  6,354行の行数ABORT + 22 target行のbyte一意存在ABORT / audit: 同内容の
  gate化 48 gate / rows.json sources に DB adoption出典記載) し、
  rows.jsonを再生成して audit pinを再埋込 → 最終sha `64bc4b78…`。
- maker tamper電池 **14/14検出** (scratch copy上・experiment bytes不変
  ・efficacy-asserted): T1 raw nodes+1 (ab033.p1・sha pin先発火) /
  T2 status-b29.log verdict反転 (ab042) / T3 README-b29 byte改変 /
  T4 status ab033 nodes+1 / T5 CU increment adopted行nodes改変
  (4265342→4265343) / T6 manifest fileless roster ab050除去 /
  T7 CU merged cache偽採用row追加 (ab054) / T8 非target drive-2行
  verdict反転 (ab019) / T9 batch-keys s5_index改変 (ab041) /
  **T10 (G6b) DB increment ab033行nodes改変** /
  **T11 (G6b) DB merged cache ab054 target行削除** /
  **T12 (G6b) DB increment 37→36行truncation** → 全てABORT・
  clean control PASS・battery後にexperiment bytes unchanged確認。
  誠実記録: T5の初回sed文言 (3366331) はCU incrementに実在せずno-op
  だったため、実在値 `4265342→4265343` にやり直して検出。T12の初回は
  `bash -c` 内 `"$d"` が外壳展开で空script化しno-opだったため、
  `\$d` escape修正後に削除適用を確認して検出。いずれも
  「改竄が適用されて初めて意味するbattery」であり、gate自体の有効性は
  T10-T12の適用済み検出で担保。
- audit `audit_dc.py` `e60630ac…` は**合成データkit上**でスモークテスト
  済み (第三実装target行は合成プレースホルダ・replica行はsources/raw
  のcopy): **全652 gate PASS ×3回 byte-identical** (DA版604 gate +
  G6b 48 gate: pin 2 + 行数 2 + 22行×2資产行一致 44) +
  audit-side tamper電池 **10/10 fail-closed検出** (A1 third verdict
  反転〔det-pair先発火〕/ A2 replica p2 nodes改変 / A3 rows.json改変
  〔rows-json-pin先発火〕/ A4 raw pin改変 (ab051.p1) / A5 manifest
  ab042をloss_idsへ追加 / A6 val-gate host nodes drift / A7 malformed
  third行 / **A8 (G6b) DB increment行改変〔db-pin-increment-shared先発火〕** /
  **A9 (G6b) DB merged cache truncation〔db-pin-merged-shared先発火〕**)。
  全tamper後にclean control PASS。
  誠実記録: A8の初回sedはreplica出力形式 (`,15000000,2,…`) を期待した
  文言でDB increment行形式 (`s5verdict,lo,hi,5,result,nodes`) に不一致の
  no-opだったため、行形式に合わせて検出。
- 合成kitは実験dirとは別のローカルscratchで実施・実験bytes不変・
  第三実装solver・replica solverとも宣言前未実行 (smokeの合成replica行は
  published rawのcopyであり新規探索でない)。

## 実行protocol (宣言後)

- D1 rules gate (pinned `verify_tbl.js` `c8c52528…`): quads/triples比較を
  `output/rules-gate.txt` に記録 (期待: replica quads 95670 mine quads
  95670・mismatches 0)。jsreplay pin `84585617…` (本host byte-clone
  照合済み)。
- D2 val-gate fresh 4 (本host・published baselines node-exact・出力は
  `.dc-host.out`)。
- D3 negatives ng1/ng2 GATE_FAIL設計どおり (legal+1 / stones 6)。
- D4 anchors k02a/l1a 各a/b (published値とnode-exact: k02a WIN
  expansions 9,106,337・ttHits 4,991,527 / l1a LOSS expansions
  7,660,602・ttHits 3,951,175)。
- D5 replica 22キー×p1/p2 (budget 15M・inner timeout 260・determinism
  fields p1==p2・published raw fields node-exact・resumable step wave
  (1 wave ≤300s・complete判定 replay_done))。
- D6 targets 22キー×a/b第三実装 (cap 300M・wallcap 240・verbatim入力CSV
  stringキー)。wallcap到達時は **WALL-INCONCLUSIVE** として誠実記録し
  勝敗とは読まない (audit G5設計どおり)。
- D7 audit `audit_dc.py` ×3 byte-identical (schema
  `n11-centralreply-closure-b29d2loss22-thirdimpl-audit-v1`・652 gate) +
  audit-summary.json出版。
- D8 B outputs出版 → C README最終 + MANIFEST-sha256 → 完了log出版
  (各push前後に最新main再取得・fetch-back byte一致検証・競合時は無理押し
  せず記録して次回へ)。

長時間探索・driveは行わない (本Partは交叉検証と監査のみ・計算量は
replica 22キー×2pass (合計 191,032,046 nodes replay・~1-60s/pass想定) +
第三実装 22キー×2run (bounded by cap/wallcap) + anchors 4 run 程度)。
