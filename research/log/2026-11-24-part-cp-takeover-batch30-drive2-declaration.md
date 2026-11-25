# Part CP takeover 宣言 (2026-11-24): batch-30 (closure class 34269) drive-2 (WIN-CONTINUE・残50キー ac005..ac054) — 中断Part CP drive-2のtakeover (publish-then-execute)

単一オーナー: n11中央応答レーン (長期レーン本セッション・takeover)。takeover対象:
Part CP drive-2 宣言 commit `7aaa0525` (2026-11-23T21:56:11Z出版・note
`research/log/2026-11-23-part-cp-batch30-class34269-drive2-declaration.md`)。
observed HEAD: `4d70d1d142341399e44bdb27110c10269d78f07e` (本宣言push直前の最新main)。

## 0. takeover正当化 (宣告session消失判定・Part U / Part Z / Part CG / Part CI takeoverと同一基準)

- Part CP drive-2宣言 (`7aaa0525` 21:56:11Z) 以降 **3時間30分以上** (本宣言push直前 2026-11-24T01:2xZ時点)、
  batch-30系commit (outputs・status update・session script出版・完了log) はmainに存在しない
  (batch-30実験dir `research/experiments/n11-centralreply-closure-class34269-batch30-20261123/`
  への commits は最後が B `05a5ac94` 21:53:36Z で停止・以降pushなし・最新main commit列で機械確認)。
- 同一時間帯に Part CO/CU (batch-29 16-LOSS adoption)・Part CV・Part CW・Part CX・K1276宣言・
  Part CI takeover drive-2 (batch-29・`ec9c7191` 01:26Z) など他レーンの出版が継続しており、
  batch-30系の成果のみ3時間30分以上無音。batch-30 drive-2継続宣言・takeover宣言・
  所有権の再主張は存在しない (最新main commit列機械grep確認)。
- よって Part U (batch-8) / Part Z (batch-11) / Part CG / Part CI takeover と同一基準で
  **宣告session消失**と判定し、本セッションがPart CP drive-2をtakeoverする。
  原drive-2所有sessionが後に復帰して本takeoverより先にdrive-2結果を出版した場合は
  その出版物を正本として扱う (先着出版が正本・重複実行はliteratureとして残す)。
  本takeoverは原drive-1宣言 (`189a2e8e`)・drive-2宣言 (`7aaa0525`) のgoal・stop rules・
  検証gateの意味論を変更しない (WIN-CONTINUEは`7aaa0525`事前登録の設計そのもの)。

## 1. 継承 (原CP kitの全pinを本hostで再検証済み・read-only fair開示)

- **kit byte-pin再検査**: batch-30 scaffold (`281d58e6`) 所収の
  jsreplay.js `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df` /
  runbatch.sh `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84` /
  make_batch30_keys.py `61fab4f7…` / drive1_local_step.sh (v2) `e7b627a8…` /
  batch-keys.json `79fbd1664f4ad66ea62d9c8a8aa5aaff5d16bcdaa397895119ce4d8f47961232`
  を最新main commit-pinned raw fetchし sha256 完全一致。
  MANIFEST-sha256.txt 72エントリ中、host再生成対象4 sidecarを除く全エントリ
  (input 55件・scripts 4件・val-gate入力4件+baseline 4件・README) をfetch検証し
  **fail=0・missing=0**。
- **drive-1 outputs (`05a5ac94`) 9件pin照合**: status.log `43fcad17…`・
  raw 8件 (ac001.p1 `1bef2dc2…` … ac004.p2 `ed39eb75…`) がdrive-1完了log pin表と完全一致。
  全8 passに `# replay_done` あり・p1/p2のbudget/result/nodes完全一致 (node-exact)
  ・done-set機械再導出 (v2 regex) = ac001..ac004 → **残50キー ac005..ac054** を確定。
- **solver実行は宣言後にのみ実施** (事前はfetch・sha検証・runner source review・
  上記done-set/pass file検査のみ・開示済み)。
- 原drive-2宣言 (`7aaa0525`) の事前登録session script `drive2_local_step.sh`
  (`95c3f15b…`) は **出版されていない** (B' commitが存在せず継承不能のため正本再構成不能)。
  本hostがpublished v2 `e7b627a8…` から最小delta (WIN-HALT wave論理3箇所の除去のみ・
  機能bodyは機械diffで同等) で再作成し、**sha256
  `466f475fc16c810882100a4c2291787cb77da7b6a74a18c2a646a14ef5d899c9`** を本宣言で事前登録する
  (A' commitでkitに同梱出版)。

## 2. 継承するstop rules (runbatch.sh byte-clone内蔵・不変)

budget 15M・2-pass fresh-cold・MISMATCH rc=42 hard-stop・p1/p2 fail rc=43/44・
`# replay_done`のないpassファイルはTRUNCATED-RETRY (evidenceでない・次invocationで
fresh-cold再実行)・EXHAUSTED (result 0) はhonest UNKNOWN (same-condition再probeなし・継続)・
WIN rc=45 (runbatch内蔵の意味論のまま・`7aaa0525` WIN-CONTINUE設計ではorchestration層が次waveへ継続)。
WIN行・LOSS行はともにhonest label (verdict不消費)。

## 3. 本takeoverの追加事前登録

1. **takeover-host val-gate fresh 4** (`7aaa0525`§2どおり・本host fresh実行):
   sanctioned 4キー = at2m×2 (budget 2M)・first-15m・second-15m (budget 15M)。
   sidecar suffix **`.d2t-host.out`**: 4/4 件published baselines
   (`6e902ab1…`/`eeafe3ac…`/`8035fe54…`/`91dffdec…`) とnode-exact比較
   (budget/result/nodes・wall_s比較外)。不一致ならhard-stop。
2. **drive-2実行**: 残50キーをac005からbatch-keys.json固定順 (s5昇順) に
   1 invocationあたり最大2キー×2 worker並列 (timeout 260 wrapper・外側290s) でprobe。
   50キーで約25 invocationを見積もる。truncated passはrunnerのreplay_done guardが
   次invocationで回収。誠実打ち切り時は成果分のみhonest出版・未probeキーはfileless
   UNPROBEDのまま次回driveに委ねる (`7aaa0525`の打ち切り規約)。
3. **出版**: (A') drive2_local_step.sh + val-gate 4 sidecar → (B) raw pass outs +
   status.log (append-only) → (C) README追記 + MANIFEST-sha256更新 → (D) 完了log。
   各push前に最新main再取得・push後fetch-back byte一致検証・競合時は無理押しせず
   記録して次回へ。row-auditは別セッションで実施予定 (原CP drive-1完了logどおり)。
4. 結果非予告: probeの成否・勝敗混在は宣言しない。EXHAUSTEDも出る可能性を事前登録する。

## 4. UNKNOWN担保 (原CP宣言・drive-2宣言と同一)

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて)・class 2251
(batch-29全キーを含む)・class 34269 (本batch-30の54キーすべて・EXHAUSTED行を含む)・
class 34948 は本driveの実行・出版のどの時点でもUNKNOWNのまま。**
nodes数・wall秒数を勝敗として読まない。WIN採用は scrutiny owner C++第二実装 gate
`9193f5b6…` 通過後の別adoption Part (pinned fail-closed merger `90711961…` 経由) のみ
(本レーンは代行しない)。閉鎖・被覆・secured・root勝敗の主張はしない。

## 5. 不接触

- **Part CI takeover drive-2** (batch-29 class 2251 残38キー・宣言 `ec9c7191`
  2026-11-24T01:26:07Z・並走所有) のdir・outputs・進行は非接触。
- **Part CX** (batch-28 CQ-WIN残5行 aa005/aa030/aa031/aa047/aa053第三実装・
  宣言 `1300c10d`・並走所有) 非接触。
- K1276 fast lane (z=8スライス・宣言 `f4dcf92e`・A `685cce3a`) 非接触。
- Part CU canonical merged chain (6,317行 `30ddad9d…`) はread-only不変
  (本driveはcanonical cacheへ一切書き込まない)。
- batch 1..29各published dir (不変)・BASE caches (`3124461b…`・`854800f3…`) read-only不変。
- batch-28 WIN行scrutiny (C++ `9193f5b6…` 専権)・EXHAUSTED行の高budget再probe
  (別宣言条件)・19root計画・fast lane・finite-field lane・inversive lane。
