# Part DF 完了: batch-28 (class 5343) b28-win46 queue registry P2パッケージ8行 第三実装交叉検証 (takeover) — 全工程green・323 gates PASS

- 2026-11-24T09:00Z (authoring time; commit timestampはGitHub側)
- 原宣言: `research/log/2026-11-24-part-df-b28p2win8-thirdimpl-declaration.md` (出版 `59b6540f`・2026-11-24T05:01:52Z・publish-then-execute)
- takeover宣言: `research/log/2026-11-24-part-df-b28p2win8-thirdimpl-takeover.md` (出版 `255d43a4`・08:23:34Z) + 時刻訂正amendment (出版 `4afac03b`・08:24:03Z)
- 実験dir: `research/experiments/n11-centralreply-closure-b28p2win8-thirdimpl-20261124/`
- 対象8行 (全て drive-4/5 15M-probe solved・UNCONSUMED honest WIN labels):
  aa014 [1171516445255811072,0] / aa049 [1152921504623624192,4228] /
  aa051 [1152921504673955840,4228] / aa019 [1171516445322903552,0] /
  aa013 [1171516445255802880,0] / aa020 [1171516453845729280,0] /
  aa010 [1171516445255794720,0] / aa040 [1152921504606846992,4228]

## ① honest記録: takeover時刻逸脱とamendment

- takeoverは earliest_takeover 08:31:52Z (原宣言05:01:52Z + 3.5h) を待たず
  **08:23:34Z に出版された** (時計読み違え)。amendment `4afac03b` (08:24:03Z) で
  「D1-D9の実開始は08:31:52Z経過後まで行わない・08:31:52Zまでに原オーナー出版・
  対抗takeoverがあれば今回のtakeoverを無効とする」と先行記録した。
- 08:32:37Zに最新mainを再取得し (a) 原オーナーによるDF scope出版物なし
  (DF実験dirはscaffold 3 commits `2245e85e`/`26fc5352`/`50b5b430` のみ・
  対抗takeoverなし) を機械確認した上でD1を開始した。以降の工程は規約上の
  takeover条件成立後である。
- kit復元: published scaffold 68ファイルをcommit-pinned raw fetchで復元し、
  原宣言ノートのpin群 45件を機械抽出照合し **44/45一致**。唯一の不一致は
  宣言ノートの `run_replica_df.sh` pin転写誤りと判定した (出版物側の
  bytes実測 sha256 `73f09f38b3f53b4ea1b695a557d9f9bc4bd44fb47e8adf97e965b27c469d4ec8`
  ・git-blob `00384666` がA1出版時のGitHub API記録と一致するため出版bytesが正本)。
  以降の工程は出版bytesのkitで実施。この判定誤りの場合はkit側G1 script pin gateが
  FAILする設計であり、audit 全gates PASSによりkitは出版正本とbyte一致が機械担保された。

## ② 実行 (D1-D8全green・takeover実行)

- D1 rules-gate PASS (rc=0): quads 95,670 一致・triples 195,044 mismatches 0
  (`output/rules-gate.txt`)。
- D2 val-gate fresh 4/4 node-exact (wall_s以外全字段一致): first-15m result 2・
  nodes 3,651,923 / second-15m result 2・nodes 5,040,200 / at2m 2行
  budget-exhausted (result 0・nodes 2,000,000)。host出力4本
  (`val-gate/*.df-host.out`)。
- D3 negatives PASS (期待fail-closed・rc=1): ng1 GATE_FAIL "legal count mismatch:
  derived=87 declared=88" ・ ng2 GATE_FAIL "stone count mismatch: bits=5
  declared=6"。
- D4 anchors a/b det-pair PASS: k02a result 1・expansions 9,106,337・ttHits
  4,991,527 / l1a result 2・expansions 7,660,202・ttHits 3,951,175。
  published pinと完全一致。
- D5 replica 8キー×2-pass fresh-cold (budget 15,000,000・inner timeout 260・
  1キー1 invocation): 16/16 rc=0・det-pair 8/8 (p1==p2)・published raw (PIN_RAW_DF
  16 pin) と **node-exact 16/16** — aa014 7,263,370 / aa049 7,272,703 /
  aa051 7,662,388 / aa019 7,967,030 / aa013 8,317,071 / aa020 8,432,253 /
  aa010 8,882,182 / aa040 8,916,641 (pinned合計 64,713,638・全て result=1)。
  `run_replica_df.sh` の invocation-level exit 1 はscript末尾
  `[ "$RC" -ne 0 ] && exit` idiom由来の benign (各pass rc=0・status.log記録どおり・
  audit gates全PASS・Part DGと同一挙動)。
- D6 third-impl targets 8キー×2-run (a/b): det-pair 8/8 (a==b)・verdict
  agreement **8/8** (全て third result=1 = published honest WIN。rows.json
  expect_third: 1 と一致)。第三実装expansions (pass-one合計 76,220,056) は
  実装依存のため pinned nodes との直接比較はしない (verdict一致のみ主張)。
- D7 audit `audit_df.py` ×3: **`ALL 323 GATES PASS; verdict agreements 8/8
  (WIN=8 LOSS=0); inconclusive=0`**・stdout 3回 byte-identical
  sha256 `96e59f21298ead3885896d842bf36a11518cb4b1e7816c1f8066a819481eda1e`
  (`output/audit-run{1,2,3}.txt`)・`output/audit-summary.json` 45,854B
  sha256 `ffe227b3acaa2bcdc56a9cde93632268de01681dee28e2f44e2d4ff7546c9e92`。
- D8 tamper battery 4/4捕捉・byte-exact復元・復帰green:
  - T1: `output/replica/aa014.p1.out`+`p2` nodes 7,263,370→7,263,371 (det-pairを
    greenに保つため両pass同時改竄) → `GATE FAILED: replica-aa014-verdict-vs-published
    this-host result=1 nodes=7263371 vs published result=1 nodes=7263370` (rc=1)。
  - T2: `output/targets/aa010.a.out` third行 result 1→2 → `GATE FAILED:
    target-aa010-det-pair a=(2,10450160,clean) b=(1,10450160,clean)` (rc=1)。
  - T3: `output/anchors/k02a.a.out` expansions 9,106,337→9,106,336 →
    `GATE FAILED: anchor-k02a-a-expansions exp=9106336 vs 9106337, ttH=4991527
    vs 4991527` (rc=1)。
  - T4: `input/rows.json` aa040 replica_nodes 8,916,641→8,916,642 →
    `GATE FAILED: replica-aa040-verdict-vs-published this-host result=1
    nodes=8916641 vs published result=1 nodes=8916642` (rc=1)。
  - 復元後 green再実行: `ALL 323 GATES PASS …` (rc=0)。rows.jsonは
    pin `e184c50bc62c39aee0dc13b80fa4caecb6aa943ecd4d89996084d8bfdfbb8e8a`
    と事後byte一致 (pristine backupとsha256同一)。

## ③ 出版 (D9) — fetch-back byte検証済み

- B wave `46473d3e`: outputs 48ファイル (status.log・replica 16・targets 16・
  anchors 4・negative 2・rules-gate.txt・audit-run1-3.txt・audit-summary.json・
  val-gate host 4)。commit-pinned raw fetch-back sha256照合 **48/48一致**。
- C wave `aab9790b`: README最終版 (7,097B・実行記録追加) + MANIFEST-sha256.txt
  (116行・実験名dir下の全出版物の sha256 path-sorted)。commit内blob sha1照合
  README `398d1176…` / MANIFEST `62d5f166…` で一致
  (MANIFESTはraw fetch-back sha256も一致・READMEのrawはCDNキャッシュ遅延のため
  commit内blob照合を正本とした)。
- queue registry rev4 bookkeeping (後続wave): `research/experiments/
  n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124/output/
  queue-registry.json` で P2 8行 thirdimpl open→done (completion=本完了log出版
  commit)・done_win 21→29・open_win 25→17・packages.P2 status done。純bookkeeping・
  verdict不消費。rev5 (追加候補): Part DG (P3・完了log `014a0361`・audit
  323 gates PASS `fd68c562…`・verdict agreement 8/8) 分の同様の反映。DG宣言が
  「DF側のP2反映更新と競合する可能性があるため…次回合流」と明記委任済みのため、
  rev4出版後のrev5として合流する。

## 主張の限定

- 本Partは交叉検証のみ。**verdict不消費**: 対象8行は honest WIN labels のまま・
  adoptionは scrutiny owner C++第二実装 gate `9193f5b6…` 通過後、pinned merger
  `90711961…` 経由の別adoption Part 専権。
- 閉鎖・被覆・secured・root勝敗の主張はしない。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 5343 (54キーすべて・P2の8キー含む) は本Partの前後を通じて
  すべてUNKNOWNのまま。** nodes数・expansions数・ttHits数を勝敗や距離として読まない。
