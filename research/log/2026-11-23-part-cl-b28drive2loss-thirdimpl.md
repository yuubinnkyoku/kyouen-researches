# Part CL 完了log (2026-11-23): batch-28 (class 5343) drive-2 LOSS行 aa003 第三実装交叉検証 —canonical cache最新採用rowのthree-implementation corroboration 成立・aa003の最初の独立セッション再現を記録 (verdict不消費・11×11 UNKNOWN担保不変)

Part CL (宣言 `research/log/2026-11-23-part-cl-b28drive2loss-thirdimpl-declaration.md`
commit `7a184e92`・publish-then-execute・単一オーナー) の実行・出版が完結した。

## 結果 (route statementのみ・勝敗の新規主張なし)

1. **第三実装 (非df-pn AND/OR minimax `third_impl.js` `08ea958f…`) verdict一致
   1/1**: aa003 = published replica verdict (result 2 = LOSS行) と一致 (clean・
   a/b determinism PASS・expansions 4,715,593・ttHits 2,592,846・wall 13.65/13.43s・
   cap 300M・wallcap 240・WALL-INCONCLUSIVE 0・DIVERGENCE 0・exp/nodes比 1.158)。
2. **本host pinned-replica 2-pass fresh-cold node-exact**: result 2・nodes
   **4,070,373** (both passes・wall 19/19s vs published 51/49s)。
   **aa003 (Part CHでcanonical cache 6,294行 `3124461b…` に採用済みの最新row)
   の最初の独立セッション再現** (Part CD実行hostの単一環境出版物に対する第二
   実行環境での再現・実行hostの物理的相違までは主張しない)。
3. **採用row byte同一性 G6 gate群 (新設)**: 検証対象rowが
   `s5verdict,1152921504741064704,4228,5,2,4070373` としてmerged canonical
   cache (6,294行中ちょうど1回・同key競合rowゼロ)・increment `dc857bfd…`
   (単一row)・increments-manifest `017c7c30…` (loss_ids=[aa003]・base 6,293・
   absent-hits 0・quarantine 0・merger `90711961…`) の3ソースでbyte同一である
   ことを機械gate。**以上で採用rowは published df-pn replica 2-pass + 本host
   pinned-replica 2-pass + 第三実装 minimax 2-run のthree-implementation
   corroborationを得た**。
4. 補助gate: rules gate PASS (quads 95,670・triples 195,044・mismatches 0)・
   val-gate this-host 4/4 node-exact (at2m exhaustion 2,000,000×2・15m
   3,651,923 / 5,040,200)・negatives 2/2 GATE_FAIL・anchors 4/4 published値再現
   (k02a 9,106,337/4,991,527・l1a 7,660,602/3,951,175・det-pair PASS)・
   **audit `edf0ae7c…` ALL 68 GATES PASS 3回byte一致** (audit-summary sha
   `297e7a7f…`)・maker tamper 8/8検出・audit tamper 4/4検出 + clean control PASS
   (実験dir bytes不変)・maker 4回byte一致 (CL-SCAFFOLD)。

## 出版コミット (全てcommit-pinned raw fetch-back byte照合)

- 宣言: `7a184e92` (10,843B・blob `c256073d`)。
- A scaffold: `943b7bbe` (34 files・fetch-back 34/34 byte一致)。
- B outputs: `66614e85` (23 files・fetch-back 23/23 byte一致)。
- C README + MANIFEST-sha256 (58 files pinned): `bf4d72e3` (fetch-back 58/58
  byte一致・MANIFEST自体もbyte一致)。
- 実験dir: `research/experiments/n11-centralreply-closure-b28drive2loss-thirdimpl-20261123/`。
- published kitはpublished bytesのみで `audit_ck.py` を再実行可能 (全入力・
  出力・sources・val-gate baselines同梱・script pins fail-closed)。

## 誠実記録 (宣言に対する逸脱・事故・開示)

1. **pin転写ドリフト1件 (宣言前・自Conventionで解消)**: maker初稿でstatus-cd.log
   のpin定数を手打ちした際に転置を混入 → maker自身のfail-closed sha gateが即ABORT
   (fail-closed設計の作動実例) → 以降は「ローカル実shaを計算し、published
   MANIFEST文字列を機械grepして両者が一致した値のみをsedで機械置換」に切り替え、
   maker/audit両方の全pinを機械値で確定。手転写shaの危険性を再確認 (Part CH E2
   と同型の事故を本番化前の段階で捕捉)。
2. **val-gate初回4本の体裁不整合**: jsreplayはquads header行をstderrに出す
   ため、stdoutのみの取得ではpublished baseline体裁 (stdout+stderr統合) と
   不整合になる。体裁を合わせて再実行し全4本 node-exact・初回ファイルは破棄
   (最終実行のみ出版)。宣言protocolに対する実行上の補足 (判定には無影響)。
3. **status.log機械生成時の文言不整合1件**: PROTOCOL行を出力ファイルから機械
   生成する際、[4] anchors行の組版ミスを検出 → 修正して確定 (evidenceファイル
   は無関係・機械検出)。
4. **audit tamper T1の補助sed no-op**: T1に含めた `s/Pin_THIRD/…` はマッチしない
   no-opだったが、有効tamper (PIN_THIRD末尾反転) の適用実効性assertが通り検出は
   成立。no-op正直開示 (Part BT/BV系の前例と同じ取り扱い)。
5. **Part採番の相剋と即時回避**: 本レーンは当初「Part CK」を採番して宣言を執筆
   したが、push直前の最新main再取得で並走が「Part CK = batch-28 drive-4
   (aa010..aa054)」を宣言済みであることを検知 → 本レーンは**Part CL**に改番
   (drive-4はaa008/aa009 WIN-HALTを受けてWIN-CONTINUE事前登録と正当な継続)。
   宣言文の非接触記述もdrive-3/4の新状況へ更新してから出版。

## 意味と消費規則

- 本Partはverdict不消費: aa003の採用は先行のPart CHが完了済みであり、本Partの
  新規採用・解放・閉鎖は一切ない。canonical cache 6,294行 `3124461b…` は
  read-only不変。
- WIN行 (aa001/aa002/aa006/aa007/aa008/aa009) の採用判断は引き続き scrutiny
  owner C++第二実装 gate pin `9193f5b6…` 待ち。aa006/aa007の第三実装検証は
  Part CG宣言済み (outputsは本log時点で未出版)。EXHAUSTED 2行 (aa004/aa005) は
  honest UNKNOWN。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa003を含む) は
  どの時点でもUNKNOWNのまま。** nodes数・expansions数・ttHits数・wall秒数を勝敗と
  して読まない。被覆・secured・root勝敗の主張はしない。WIN/LOSS採用は別adoption
  Part (pinned fail-closed merger `90711961…` 経由) のみ。

## レジューム (着手前に必ず最新main再取得・hourly並走注意)

Part CL完結。次回の最有力候補:

1. **Part CG (aa006/aa007 thirdimpl) のoutputs出版状況確認** (宣言 `38770f4f`
   は17:32以降もoutputs未出版。長時間停滞時はtakeover規約に従い最新mainで
   対抗/takeover宣言の有無を確認してから判断)。
2. **drive-3 WIN行 (aa008/aa009) の第三実装交叉検証** (Part CG形式の拡張。
   aa008 s5/nodes 5,270,340・aa009 7,319,605・Part CK drive-4の進捗と
   WIN-CONTINUEによる追加WIN行の出版状況を見てから着手)。
3. **batch-29 (Part CI) probeのoutputs確認** (ab001..ab054・宣言 `efd2d488`・
   outputsが出ればWIN/LOSS/EXHAUSTED分行の集計と第三実装検証・LOSS行adoption
   (別adoption Part・merger `90711961…` 経由) の準備)。
4. aa004/aa005 EXHAUSTED行の再probe条件设计 (予算引き上げは新しい宣言条件に
   なるため、batch-28 lane ownerとの整合確認を要する)。
