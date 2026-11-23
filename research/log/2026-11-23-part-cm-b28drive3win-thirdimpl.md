# Part CM 完了log (2026-11-23): batch-28 (class 5343) drive-3 WIN-HALT行 aa008/aa009 第三実装交叉検証 — three-implementation corroboration 成立・drive-3 WIN行の最初の独立セッション再現を記録 (verdict不消費・11×11 UNKNOWN担保不変)

Part CM (宣言 `research/log/2026-11-23-part-cm-b28drive3win-thirdimpl-declaration.md`
commit `27217816`・publish-then-execute・単一オーナー) の実行・出版が完結した。
対象はPart CJ drive-3で出版されたWIN-HALT行2件 (unconsumed closure WIN候補34/35番目):

- aa008: key (1171516445255794704,0)・s5 140489・membership 4・legal 85・result 1 (WIN)・nodes 5,270,340
- aa009: key (1747977197559218176,0)・s5 142299・membership 4・legal 91・result 1 (WIN)・nodes 7,319,605

Part採番はCMで確定 (CKは並走のdrive-4、CLは本レーン先段のaa003)。並走が18:01に
Part CG takeover宣言 (aa006/aa007) `d5e9acc2` を出版したがaa008/aa009とは無関係で
干渉なし。

## 結果 (route statementのみ・勝敗の新規主張なし)

1. **第三実装 (非df-pn AND/OR minimax `third_impl.js` `08ea958f…`) verdict一致
   2/2**: aa008 = result 1 (WIN)・expansions 6,247,727・ttHits 3,349,810 (wall
   16.76/16.84s)・aa009 = result 1 (WIN)・expansions 8,663,677・ttHits 4,539,319
   (23.52/23.38s)。両キーともa/b determinism pair PASS・cap 300M・wallcap 240・
   WALL-INCONCLUSIVE 0・DIVERGENCE 0。**以上でaa008/aa009は published df-pn
   replica 2-pass (Part CJ) + 本host pinned-replica 2-pass + 第三実装 minimax
   2-run のthree-implementation corroborationを得た (6実行すべて result 1)。**
2. **本host pinned-replica 2-pass fresh-cold node-exact**: aa008 nodes
   **5,270,340** (both passes・wall 24/25s vs published 51/52s)・aa009 nodes
   **7,319,605** (wall 35/36s vs published 76/50s)。**drive-3 WIN行2件の最初の
   独立セッション再現** (Part CJ実行hostの単一環境出版物に対する第二実行環境で
   の再現・実行hostの物理的相違までは主張しない)。
3. 補助gate: rules gate PASS (quads 95,670・triples 195,044・mismatches 0・
   0.82s)・val-gate this-host 4/4 node-exact (`.cm-host.out` 4ファイル・published
   baselineと一致)・negatives 2/2 GATE_FAIL設計どおり・anchors 4/4 published値再現
   (k02a 1/9,106,337/4,991,527・l1a 2/7,660,602/3,951,175・a/b determinism PASS)・
   **audit `3f9a29fa…` ALL 101 GATES PASS 3回byte一致** (audit-run1..3.txt sha
   `2754d27c…`・audit-summary sha `dcee79ed…`)・verdict agreements 2/2 (WIN=2)・
   maker tamper 8/8検出 (T1 raw nodes+1 / T2 row-audit probed 9→10 / T3 README文言 /
   T4 status verdict反転 / T5 published-input legal / T6 BF anchor lo+1 / T7
   batch-keys s5_index / T8 merged-cache aa003 row)・audit tamper 4/4検出
   (gate名特定) + clean control PASS (実験dir bytes不変)。

## 出版コミット (全てcommit-pinned raw fetch-back byte照合)

- 宣言: `27217816`。
- A scaffold: `3dc7ec07` (38 files)。
- B outputs: `3ac117fc` (27 files)。
- C README + MANIFEST-sha256 (66 files pinned): `3de57a61` (MANIFEST `651a27dc…`)。
- **C-fix (後段参照)**: `889f6f72`。fetch-back検証は65/66→修復後66/66 byte一致。
- 実験dir: `research/experiments/n11-centralreply-closure-b28drive3win-thirdimpl-20261123/`。
- published kitはpublished bytesのみで `audit_cm.py` を再実行可能 (全入力・
  出力・sources・val-gate baselines同梱・script pins fail-closed)。

## 誠実記録 (宣言に対する逸脱・事故・開示)

1. **merged cache truncated事故 (fetch-back機械検出→C-fix修復)**: A commit
   `3dc7ec07` で `sources/canonical-cache-ch-merged-b28loss1.cache` が
   63,997/259,574バイトに切断されて混入した。原因はsandbox read_fileの単発読み込み
   上限 (~9KB) を超えるファイルをpush_filesに単発で渡したこと。fetch-back検証
   (commit-pinned raw + sha256sum) が65/66中1件の不一致として即機械検出 (検証工程
   M1が作動した実例)。→ C-fix `889f6f72`: read_fileのoffset/limitページング
   (150行×42ページ) で259,574バイトをsandbox内に正確に再組立て (assert: len
   259574・newline 6,295・s5verdict rows 6,294・header/末尾row一致・全ASCII) →
   既存blobのGit blob sha (sha1 `41c7850a…`) を切断bytesから自前計算して
   create_or_update_fileで全文再push → fetch-back 66/66 byte一致・sha256
   `3124461b…` (MANIFEST pin) 一致。**教訓: 単発read上限超のファイルはページング
   再組立て+fetch-back検証を必須とする (次回以降のkit作成規約に反映)。**
   なおconnectorのget_file_contentsはblob shaを返さない構造のため、更新用shaは
   `blob <size>\0` + bytes のsha1自己計算で確定した。
2. **G6 gate設計段階の事前修正**: 採用row byte同一性gateはmanifestのraw文字列
   scanではなくid-list構造検査として設計 ("(aa008..aa054)"のような注記文言を
   id listと誤ABORTしない機械区別)。宣言前に確定済み。
3. **宣言protocol順の補足**: status.logの機械生成はevidence確定後の最後に置く
   (Part CLと同様の体裁。判定には無影響)。
4. **宣言前read-only探査 (maker 4回)**: 宣言文に開示済みの範囲内で実施、逸脱なし。

## 意味と消費規則

- 本Partはverdict不消費: WIN行 (aa008/aa009を含む全6 WIN行
  aa001/aa002/aa006/aa007/aa008/aa009) の採用判断は引き続き scrutiny owner
  C++第二実装 gate pin `9193f5b6…` 待ち。本Partの新規採用・解放・閉包は一切ない。
- canonical cache 6,294行 `3124461b…` はread-only不変 (C-fixはバイト完全修復であり
  内容変更ではない・MANIFEST pin不変)。aa004/aa005 (EXHAUSTED 2行) はhonest
  UNKNOWN。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa008/aa009を
  含む) はどの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数・wall秒数を
  勝敗として読まない。被覆・secured・root勝敗の主張はしない。WIN/LOSS採用は別
  adoption Part (pinned fail-closed merger `90711961…` 経由) のみ。

## レジューム (着手前に必ず最新main再取得・hourly並走注意)

Part CM完結 (C-fix含む)。次回の最有力候補:

1. **Part CG takeover (aa006/aa007 thirdimpl・宣言 `d5e9acc2`) のoutputs出版
   状況確認** (長時間停滞時はtakeover規約に従い対抗/takeover宣言の有無を最新main
   で確認してから判断)。
2. **drive-4 (Part CK・aa010..aa054 WIN-CONTINUE) の追い越し判定** (WIN行の追加
   出版有無・verdict agreement待ちキーの確定。追い越す場合はWIN行第三実装交叉
   検証をCM形式で継続)。
3. **batch-29 (Part CI・ab001..ab054) outputs確認** (WIN/LOSS/EXHAUSTED分行の
   集計と第三実装検証・LOSS行adoptionの準備)。
4. scrutiny owner C++第二実装 gate `9193f5b6…` 待ちは不変 (WIN行6行の採用判断は
   このgateが開くまで保留)。
