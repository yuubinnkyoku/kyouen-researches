# Part DY 単一オーナー宣言 (2026-11-25): batch-37 — closure class 16371 (rank 10) clean 47キー probe (publish-then-execute)

単一オーナー: n11中央応答 長期レーン (本セッション・Part DV/DW と同一レーンの別hourly実行・Part DX と直交)。
対抗宣言なし: push直前に最新mainを再取得し (observed HEAD `46e02d0e` =
Part DX batch-36 inc3・2026-11-24T23:59:08Z)、機械grepで batch-37 / Part DY /
class 16371 の新規probeを主張するcommit・宣言・実験dirがないことを確認してから
着手する (search_commits: "Part DY" total_count=0・"batch-37" 0・"batch37" 0・
"class 16371" を含むcommitは2026-11-22のbatch-4 (e002 WIN-HALT) と
e002 if-adopted analysis の歴史2件のみで以後の追加probeなし)。

## 1. レジューム経緯と選定根拠

Part DV (batch-35 probe) と Part DW (b35loss26 canonical adoption・canonical
chain 6,573行 `23d40e36…` WIN 158 / LOSS 6,415) は先行hourly実行で完走済み。
直前の並走hourly実行が Part DX (batch-36・closure class 20421 rank 9・
clean 45キー {d005..d049}) を宣言・kit出版・inc1-3出版まで進行中であり、
本実行はそれと**衝突しない別クラス**を対象とする。

Part DX 宣言が確定させた選定基準 (clean子を持つ最上位クラス) を本実行も
継承する。最新closure表 (Part DW reaudit出版・`b7241eb0…`・807行) で
rank 1..8 のunknownは全てhonest label取得済み (未採用WIN or EXHAUSTED)・
rank 9 class 20421のclean 45キーは Part DX が所有中。よって**新規batchとして
probe可能な最上位はrank 10 class 16371** (`[1153202979851993088, 16]`・
unknown_now 49) である。本宣言前探査で機械確定した内訳:

- **2キー probed honest-label・未消費 (batch-4 2026-11-22)**: e001 PASS LOSS
  `15000000,2,882800` (canonical chain未採用のまま)・e002 PASS WIN
  `15000000,1,14112632` + WIN-HALT (scrutiny owner C++ gate待ち)。
  batch-4は e002 で事前登録WIN-HALT停止し、以後の補完probeなし。
- **1キー canonical chain採用済み (dual-class)**: e022 (s5 546606) は
  batch-14 class 23101 packet の q007 として 2026-11-22 に PASS LOSS
  `15000000,2,1494975` 判定済みで **canonical cache に採用行が存在**
  (`s5verdict,1153202979868770304,16,5,2,1494975`・本宣言前探査で機械照合)。
  よって class 16371 の unknown 49 には含まれず worklist にも不在。
- **47キー clean (一度もverdict取得なし)**: batch-4 packet 50キーのうち
  {e003..e050} \ {e022}。49 == 2 (probed honest) + 47 (clean) と機械整合。

## 2. 宣言前探査 (read-only・本宣言前に実施・全開示・solver未実行)

1. **本環境でのrefresh原実行 byte再現 (Part DX宣言前探査と同一手法)**:
   Part DW 出版のrefresh fork `refresh_adoption_b35loss26.py` (`4aaabcd5…`) と
   全pinned入力 (graph `54f9c364…` / update8 `b658290a…` / independent.py
   `954d3a10…` / policy `78655e94…` / quarantine `81d23160…` / merged cache
   `23d40e36…`) を本セッション環境に再fetchして原実行したところ
   **4出力すべて出版bytesとsha256完全一致**: probe-worklist.csv regen pin
   `86767be9…` 一致・closure-classes.csv `b7241eb0…` 一致・
   refresh-summary.json `5fe3e5ab…` 一致・per-root-coverage.csv
   `f1abcd85…` 一致。本環境が Part DW reaudit を byte-exact に再現する
   ことが機械確定した。
2. canonical cache `23d40e36…` (6,573 s5verdict行) をpair-level parse:
   class 16371 の 49 unknown (47 clean + 2 probed) のexact (lo,hi) pairは
   **cacheに0件** (採用済み WIN/LOSS conflictなし)。e022 (=q007) 行は
   存在・result 2・nodes 1494975 (採用済みLOSS・maker G4bでゲート固定)。
3. **全published packetのverdict掃引 (今回 new・batch37固有)**: 本レーンが
   収集した closure系batch packet (batch-1..35・batch-14 residual・
   batch-28 drive2-5含む全status.log) をstatus-basedで機械掃引し、
   47 cleanキーの(lo,hi,s5_index)にverdict (PASS/EXHAUSTED/WIN) を与えた
   commitは**0件**を確認。e042 は batch-13 (class 16930) packet に p028
   として宣言のみ存在 (verdict行なし)・e022 は batch-14 q007 として
   verdict取得済み (上記どおり採用済み・除外)。batch-36 (Part DX・所有中)
   のキーはclass 20421由来で本batchと集合交差ゼロ (mask・worklist双方で確認)。
4. worklist regen (上記1のbyte一致出力) からclass 16371の49行を抽出
   (probe_order 126..174 連続・全行serving_class 16371・
   class_unknown_now 49): batch-4 packet 50キーからe022を除いた49キーと
   (lo, hi, legal, s5_index, membership_class_count) **全字段一致・
   mismatch 0**。抽出物を本kitのsourceとして出版する
   (worklist-class16371-extract.csv sha256
   `da8130274f0dcbeb57ed7994f0a7f210f7c04c641b0f2ebb24b22956e94ffdbc`・
   49 data rows)。probe-worklist.csv本体 (~4MB) はPart DW/DX同様
   体積で非出版・regen pin `86767be9…` で再現を担保し、
   後続adoption Partのextractorが両方向をfail-closed検証する。
5. closure-classes `b7241eb0…`: rank 10 = class 16371・unknown_now 49・
   first_group_first 26・first_group_third 50・groups_served 3。
6. quarantine registry `81d23160…`: active 2エントリ。47 cleanキーの
   exact pairはいずれもactive quarantine keyと不一致 (machine check)。
7. 本宣言時点で本セッションは solver (jsreplay) を一度も実行していない。
   maker (make_batch37_keys.py) は宣言前に3回実行して全gates PASS・
   3回byte-identical (inputs + batch-keys-b37.json 全48ファイル sha一貫)。
   tamper battery **10/10 fail-closed + control PASS**
   (T1 pin drift〔cache byte〕/ T2 packet field drift〔pin層〕/
   T2b 同 + re-pin〔G2意味層: e001 lo drift検出〕/ T3 status drift〔pin層〕/
   T3b 同 + re-pin〔G2意味層: e001 nodes drift検出〕/
   T4 target pair cache命中 + re-pin〔G4〕/
   T5 quarantine命中 (e003 pair active化) + re-pin〔G5〕/
   T6 closure rank drift (rank 10→class 16399) + re-pin〔G3〕/
   T7 worklist extract legal drift + re-pin〔G6〕/
   T8 adopted e022 cache行 nodes drift + re-pin〔G4b〕・全ABORT・
   変異適用を各stepでassert・battery後にcontrol rc=0)。

## 3. スコープ・手法

実験dir: `research/experiments/n11-centralreply-closure-class16371-batch37-20261125/`。

- 手法: pinned runner `runbatch.sh` (sha256 `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
  ・batch-33/34/35/36 kitとbyte-clone) + pinned replica `jsreplay.js`
  (sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  ・byte-clone)。2-pass fresh-cold replay・budget 15,000,000・
  1 solver / 1 row / 1 process・drive順 = worklist probe_order
  (= packet順 e003..e050 から e022 を除いた47キー) で逐次実行
  (本環境は2-core・並列2 solverまで)。
- val-gate (宣言後にfresh実行・published baseline 4 moleculeと
  node-exact一致が必須): batch-36 kit出版の4行
  `at2m-s5-1152921504606851072-536870946` (budget 2,000,000・result 0・nodes 2,000,000) ・
  `at2m-s5-1188950301626860544-536870912` (2,000,000・0・2,000,000) ・
  `first-15m-s5-1152921504606851072-536870946` (15,000,000・2・3,651,923) ・
  `second-15m-s5-1188950301626860544-536870912` (15,000,000・2・5,040,200)。
  input.csv・published-baseline.outはbatch-36 kitからbyte-clone出版。
- maker `make_batch37_keys.py` (本kit新規・sha256 `2c2c8c3a2d38f39a2742ab28c61c2c36989bfc94a43ed14ac0a0c0f9ff24a32d`):
  fail-closed gates
  - G1: sources sha pins (7ファイル: batch-4 batch-keys `70b8a4c8…` /
    batch-4 status `63c2d969…` / refresh-summary `5fe3e5ab…` /
    closure-classes `b7241eb0…` / canonical cache `23d40e36…` /
    quarantine `81d23160…` / worklist extract `da813027…`)
  - G2: batch-4 packet integrity (50キー e001..e050・status 2 PASS行
    = e001 LOSS result 2 + e002 WIN result 1 + e002 WIN-HALT 1行・
    budget/nodes pin照合・clean == {e003..e050}\{e022} == 47キー)
  - G3: closure-classes rank 10 == class 16371 かつ unknown_now == 49 で
    49 == 2 (probed honest-label) + 47 (clean) と一致・mask照合
  - G4: 49キー (47 clean + 2 probed) のexact (lo,hi) pairが
    canonical cacheに不在 (same-lo コンテキスト計数はreportのみ・採用しない)。
    **G4b (batch-37固有): 採用済みdual-class行 e022 (=batch-14 q007) が
    cacheに result 2 / nodes 1494975 で存在することをゲート固定**
    (e022はtargetから除外・worklist不在もG6でゲート)
  - G5: 47 cleanキーがquarantine activeでない
  - G6: worklist extract 49行 = probe_order 126..174連続・全字段がpacket key
    と一致・e022 pairがextractに不在
    (legalはjsreplay実行時にも独立再導出され mismatchで hard-fail)
- **停止規則 (事前登録)**:
  1. determinism mismatch → runner HARD-STOP (rc=42)、以後のキー着手不可。
  2. WIN (result 1) → pre-registered honest WIN-HALT marker行 (rc=45 per-key) ・
     **drive-level WIN-CONTINUE**: 残り全キーを継続 (batch-35/36実績と同一運用・
     全47キーをhonest labelする)。WIN行のverdictは一切不消費
     (scrutiny owner C++第二実装 gate `9193f5b6…` 通過後のみ採用可・
     本実行環境にC++コンパイラなし・Part G/DU/DXと同一の既知障害)。
  3. EXHAUSTED (result 0) → honest UNKNOWN (PASS行+EXHAUSTED行)・
     同一条件 (15M) の再探索は行わない。高budget再probeは別宣言・
     新runner sha (BUDGET変更) が必須。
  4. timeout・環境resetでTRUNCATEDになったpass fileはverdictでない・
     runnerの `# replay_done` guardでfresh再実行 (truncated passは
     完走 EXHAUSTED行の no-re-search規則に触れない)。
- 出版: raw 8キーごとのincrement wave (Part DS ④(a)の教訓・sandbox reset
  耐性)・status.log・batch-audit・README・MANIFEST-sha256・完了log。
  本batch単独ではverdictを1行も消費しない。adoptionは別Part
  (pinned merger `90711961…` 専権・WIN行はscrutiny owner C++ gate待ち)。
  なお batch-4 の未消費e001 LOSS行はpublished raw由来のため将来の
  adoption Partがincrement化しうるが、本batchのスコープ外 (本宣言は
  探索のみを所有する)。

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 16371を含む全クラスは全時点でUNKNOWNのまま
(nodes数はbookkeepingであり勝敗・距離ではない)・閉鎖・被覆・
secured coverage・root勝敗の主張は一切しない。**

## 4. 本体の工程 (publish-then-execute)

wave A: 本宣言出版 → kit scripts 3 (jsreplay/runbatch/maker) +
sources 7 (batch4-packet 2 + refresh-summary + closure-classes +
canonical cache + quarantine + worklist extract 1) →
input 48 (47 clean-key csv + batch-keys-b37.json) →
val-gate 8 (4 molecule × input/published-baseline byte-clone) 出版 →
kit fetch-back byte検証 (全files sha照合) →
val-gate 4 molecule fresh実行 (published baseline と (budget,result,nodes)
node-exact一致が必須・不一致なら即中止) →
e003..e050 (e022除く) 逐次drive (2-pass fresh-cold @15M) →
raw increment waves出版 (8キーごと) → status.log・batch-audit.json出版 →
README + MANIFEST-sha256 出版 → Part DY完了log 出版。
