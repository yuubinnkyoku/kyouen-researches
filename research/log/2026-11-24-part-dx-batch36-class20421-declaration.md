# Part DX 単一オーナー宣言 (2026-11-24): batch-36 — closure class 20421 (rank 9) clean 45キー probe (publish-then-execute)

単一オーナー: n11中央応答 長期レーン (本セッション・Part DV/DW 完了直後の後継)。
対抗宣言なし: push直前に最新mainを再取得し (observed HEAD `2c12d88c`
= K1309 fast-lane README bullet・2026-11-24T23:13:39Z)、最近コミットを
機械grepして batch-36 / Part DX / class 20421 probe を主張するcommit・
宣言・実験dirがないことを確認してから着手する
(search_commits: "Part DX" total_count=0・"batch-36" 0・"batch36" 0。
"class 20421" を含むcommitは2026-11-22のbatch-3関係3件のみで
以後の追加probeなし)。

## 1. レジューム経緯と選定根拠

Part DV (batch-35 probe・宣言 `63028eea`・完了log `8548e231` 部位) と
Part DW (b35loss26 canonical adoption・宣言 `ddd144a8` 部位・完了log
`295b9505`) が本レーン先行実行で完走した。canonical chain は
6,573行 `23d40e36…` (WIN 158 / LOSS 6,415)・class 16757 は
unknown 29→3 (b018/b032/b048 不消費WIN・NOT freed / NOT excluded)。

最新closure表 (Part DW reaudit出版・`b7241eb0…`・807行) のrank上位は
本宣言時点で以下であり、rank 1..8 のunknownは**全て
honest label取得済み (未採用WIN または EXHAUSTED・いずれも
scrutiny owner C++ gate 待ちか高budget再probe待ち) のchildren**で、
honest-label-free (clean) なchildは存在しない:

- rank 1: class 23101 unknown 1 = ag001 WIN (batch-34・DU-b第三実装一致・不消費)
- rank 2: class 1849 unknown 1 = ag002 WIN (batch-34・同上・不消費)
- rank 3: class 2251 unknown 1 = ab028 WIN (batch-29・Part CZ corroboration済み・不消費)
- rank 4: class 16757 unknown 3 = b018/b032/b048 WIN (batch-1/batch-35・不消費)
- rank 5: class 5804 unknown 4 = 未採用WIN 4 (ad024/ad028/ad043/ad055)
- rank 6: class 34908 unknown 9 = 未採用WIN 4 + EXHAUSTED 5 (Part DQ-DS)
- rank 7: class 34269 unknown 11 = 未採用WIN 11 (Part CP drive-1等)
- rank 8: class 5343 unknown 46 = 未採用WIN 46 (batch-28・b28win46第三実装queue registry)
- **rank 9: class 20421 (`[1155173304420536320, 131072]`) unknown 49**
  = 深刻な格差なし・**clean 45キー (d005..d049)** + probed honest-label 4
  (d001 LOSS ・d002 WIN ・d003 LOSS ・d004 LOSS・いずれもbatch-3
  2026-11-22の2-pass node-exactで、canonical chain未採用)

よって **probe可能な (honest labelをまだ持たない) unknown children を
持つ最上位クラスはrank 9 class 20421であり、そのclean 45キーを
batch-36とする**。45キーはpublished batch-3 packet
(`research/experiments/n11-centralreply-closure-class20421-batch-20261122/`・
49キー d001..d049) のうちstatus.log 4 PASS行 (d001/d002/d003/d004)
を除いた集合 {d005..d049} と正確に一致 (手転写ゼロ・ makerが機械照合・
G2)。Part DV と同一の選定規準 (clean子を持つ最上位クラス) である。

## 2. 宣言前探査 (read-only・本宣言前に実施・全開示・solver未実行)

1. **本環境でのrefresh原実行 byte再現 (今回 new)**: Part DW 出版の
   refresh fork `refresh_adoption_b35loss26.py` (`4aaabcd5…`) と全pinned入力
   (graph `54f9c364…` / update8 `b658290a…` / independent.py `954d3a10…` /
   policy `78655e94…` / quarantine `81d23160…` / merged cache `23d40e36…`) を
   本セッション環境に再 fetch して原実行したところ、
   **4出力すべて出版bytesとsha256完全一致**: probe-worklist.csv
   regen pin `86767be9…` 一致・closure-classes.csv `b7241eb0…` 一致・
   refresh-summary.json `5fe3e5ab…` 一照合・per-root-coverage.csv
   `f1abcd85…` 一致。本環境が Part DW reaudit を byte-exact に
   再現することが機械確定した。
2. canonical cache `23d40e36…` (6,573 unique s5verdict行) をpair-level parse:
   batch-3 packet 49キーのexact (lo,hi) は **cacheに 0件** (採用済み WIN/LOSS
   conflictなし)。d002 WINも不在 (不消費どおり)。closure表unknown_now 49 =
   4 (probed honest-label・未採用) + 45 (clean) と機械整合する。
3. worklist regen (上記1のbyte一致出力) からclass 20421の49行を抽出
   (probe_order 77..125 連続・全行serving_class 20421・
   class_unknown_now 49): batch-3 packet 49キーと
   (lo, hi, legal, s5_index, membership_class_count) **全字段一致・
   mismatch 0**。抽出物を本kitのsourceとして出版する
   (worklist-class20421-extract.csv sha256
   `2e6102be49eb997b833f68dea99151924c353f3d771b6574ff881c1321c55c99`・
   49 data rows)。probe-worklist.csv本体 (~4MB) はPart DW同様
   体積で非出版・regen pin `86767be9…` で再現を担保し、
   後続adoption Partのextractorが両方向 (regen byte一致・extract行一致) を
   fail-closed検証する。
4. closure-classes `b7241eb0…`: rank 9 = class 20421・unknown_now 49・
   first_group_first 12・first_group_third 51・groups_served 4。
5. quarantine registry `81d23160…`: active 2エントリ。49キーのexact pairは
   いずれもactive quarantine keyと不一致 (machine check)。
6. 本宣言時点で本セッションは solver (jsreplay) を一度も実行していない。
   maker (make_batch36_keys.py) は宣言前に3回実行して全gates PASS・
   3回byte-identical (batch-keys-b36.json `d5918203…`)・tamper battery
   9/9 fail-closed + control PASS (T1 pin drift / T2 packet field drift
   [pin層] / T2b 同 + re-pin [G2意味層] / T3 status drift [pin層] /
   T3b 同 + re-pin [G2意味層] / T4 cache hit + re-pin [G4] /
   T5 quarantine hit + re-pin [G5] / T6 closure rank drift + re-pin [G3] /
   T7 worklist extract drift + re-pin [G6]・全ABORT・変異適用を各stepでassert)。

## 3. スコープ・手法

実験dir: `research/experiments/n11-centralreply-closure-class20421-batch36-20261124/`。

- 手法: pinned runner `runbatch.sh` (sha256 `f591f8c2b67326e53873f8ea70f8d04d18423e7c8ef8359838cbafe8264f3b84`
  ・batch-33/34/35 kitとbyte-clone) + pinned replica `jsreplay.js`
  (sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  ・byte-clone)。2-pass fresh-cold replay・budget 15,000,000・
  1 solver / 1 row / 1 process・drive順 = worklist probe_order
  (= packet順 d005..d049) で逐次実行。
- val-gate (宣言後にfresh実行・published baseline 4 moleculeと
  node-exact一致が必須): batch-35 kit出版の4行
  `at2m-s5-1152921504606851072-536870946` (budget 2,000,000・result 0・nodes 2,000,000) ・
  `at2m-s5-1188950301626860544-536870912` (2,000,000・0・2,000,000) ・
  `first-15m-s5-1152921504606851072-536870946` (15,000,000・2・3,651,923) ・
  `second-15m-s5-1188950301626860544-536870912` (15,000,000・2・5,040,200)。
  input.csv・published-baseline.outは同kitからbyte-clone出版。
- maker `make_batch36_keys.py` (本kit新規・sha256 `c71a4877da4a99b04656edeee45960a0f886cd599ae0b94192d02264fb2ef7c0`):
  fail-closed gates
  - G1: sources sha pins (7ファイル: batch-3 batch-keys `ad05073a…` /
    batch-3 status `7877f4a0…` / refresh-summary `5fe3e5ab…` /
    closure-classes `b7241eb0…` / canonical cache `23d40e36…` /
    quarantine `81d23160…` / worklist extract `2e6102be…`)
  - G2: batch-3 packet integrity (49キー d001..d049・status 4 PASS行
    = d001/d003/d004 LOSS result 2 + d002 WIN result 1 + d002 WIN-HALT
    1行・budget/nodes pin照合・clean == {d005..d049})
  - G3: closure-classes rank 9 == class 20421 かつ unknown_now == 49 で
    49 == 4 (probed honest-label) + 45 (clean) と一致
  - G4: 49キー (45 clean + 4 probed) のexact (lo,hi) pairがcanonical cacheに不在
    (same-lo コンテキスト計数はreportのみ・採用しない)
  - G5: 45 cleanキーがquarantine activeでない
  - G6: worklist extract 49行 = probe_order 77..125連続・全字段がpacket keyと一致
    (legalはjsreplay実行時にも独立再導出され mismatchで hard-fail)
- **停止規則 (事前登録)**:
  1. determinism mismatch → runner HARD-STOP (rc=42)、以後のキー着手不可。
  2. WIN (result 1) → pre-registered honest WIN-HALT marker行 (rc=45 per-key) ・
     **drive-level WIN-CONTINUE**: 残り全キーを継続 (batch-35実績と同一運用・
     全45キーをhonest labelする)。WIN行のverdictは一切不消費
     (scrutiny owner C++第二実装 gate `9193f5b6…` 通過後のみ採用可・
     本実行環境にC++コンパイラなし)。
  3. EXHAUSTED (result 0) → honest UNKNOWN (PASS行+EXHAUSTED行)・
     同一条件 (15M) の再探索は行わない。高budget再probeは別宣言・
     新runner sha (BUDGET変更) が必須。
  4. timeout・環境resetでTRUNCATEDになったpass fileはverdictでない・
     runnerの `# replay_done` guardでfresh再実行 (truncated passは
     完走 EXHAUSTED行の no-re-search規則に触れない)。
- 出版: raw 8キーごとのincrement wave (Part DS ④(a)の教訓・sandbox reset
  耐性)・status.log・batch-audit・README・MANIFEST-sha256・完了log。
  本batch単独ではverdictを1行も消費しない。adoptionは別Part。

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 20421を含む全クラスは全時点でUNKNOWNのまま
(nodes数はbookkeepingであり勝敗・距離ではない)・閉鎖・被覆・
secured coverage・root勝敗の主張は一切しない。**

## 4. 本体の工程 (publish-then-execute)

wave A: 本宣言 + kit scripts 3 + val-gate inputs/baselines 8 + sources 7
(extract含む) + input 46 (45 csv + batch-keys-b36.json) 出版 →
kit fetch-back byte検証 (全files sha照合) →
val-gate 4 molecule fresh実行 (published baseline と (budget,result,nodes)
node-exact一致が必須・不一致なら即中止) →
d005..d049逐次drive (2-pass fresh-cold @15M) →
raw increment waves出版 → status.log・batch-audit.json出版 →
README + MANIFEST-sha256 出版 → Part DX完了log 出版。
