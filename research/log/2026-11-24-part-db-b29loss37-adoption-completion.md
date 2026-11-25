# Part DB 完了: batch-29 (class 2251) 残37 LOSS行 (ab017..ab027+ab029..ab054) の canonical adoption + reaudit — class 2251 canonical unknown 38→1・残る1行は未消費WIN ab028 (2026-11-24)

実験dir `research/experiments/n11-centralreply-class2251-loss37-adoption-reaudit-20261124/`
(16 files: scripts 4 + output 9 + reaudit 3 + README + MANIFEST-sha256.txt)。
宣言 `research/log/2026-11-24-part-db-b29loss37-adoption-declaration.md`
(commit `3bf90f67`・git blob `6ec9ad49…`・observed HEAD `cca29581`
02:31Z時点で対抗adoption宣言なし機械確認) → 公式rerun (scratch
tree) → 出版 A scripts 4 (`feb725c3`・fetch-back 4/4 byte一致) →
B increment+manifest+merge-audit×3 (`c56f0706`・5/5) → C canonical
merged cache 262,326B (`951f7bcb`・byte一致) → D reaudit 3出力+decomp
(`728bc400`・4/4) → E README+MANIFEST-sha256 (`d5ed5dc0`・2/2・
public 16 file着地確認済み)。

**verdict不消費 (zero-WIN-consumed adoption)**: WIN行 ab028
(result 1・nodes 3,167,121・s5 93815) は incrementにもcanonical
cacheにも書き込まず未消費のまま (採用はscrutiny owner C++
第二実装 gate `9193f5b6…` 専権・three-implementation corroboration
はPart CZ `68751f…75` で成立済み)。**class 2251 は freeにも
excludedにもならず status unknown のまま**。

## 対象

- published Part CI takeover drive-2 evidence (kit MANIFEST
  `7c124233…` 71 files・drive-2 完了log `141c80ca`) のうち、Part CU
  採用済み16行 (ab001..ab016) とWIN行 ab028 を除く **37 fresh LOSS行**
  (2-pass fresh-cold node-exact・budget 15M・nodes合計
  **159,325,566/pass**)。
- BASE = Part CU canonical 6,317行 `30ddad9d…` → ADOPTED-CANONICAL
  = **6,354行 (WIN 158 / LOSS 6,196)・sha256 `04b0a239…`** (pinned
  fail-closed union merger `90711961…` 経由・WIN/LOSS conflict即abort)。
- 採用37行のkey・nodes・s5・legal・membershipは宣言ノートの37行表の
  とおり (manifest `1b51f30d…`・increment `85bd4469…` で機械保存)。

## 公式rerun (宣言後・scratch tree・全出力が宣言pinとbyte一致)

- **maker ×4**: increment `85bd4469…` + manifest `1b51f30d…` 全run
  byte一致 (kit MANIFEST 71/71・post-scaffold val-gate 8 file・raw
  108 file 54キー2-pass再検証・status.log 55行 CU drive-1 prefix16
  append-only gate `6b877344…`・ab028 WIN pin・BASE-unknown 38 =
  54−16 = 採用37+残1 チェック等全gate PASS)。
- **merger selftest PASS + merge ×3**: merged cache `04b0a239…`
  ×3 byte一致・merge-audit `2d7b4998…` ×3 同一byte。
- **refresh ×3 (~58s/run) + 隔離 (別tree・env -i・PYTHONHASHSEED=random)**:
  refresh-summary `1fc531d3…`・closure-classes `b37425d7…`・
  per-root-coverage `8f69d5bb…`・probe-worklist `4ecb9a0a…` 全run byte一致。
- **extractor ×4 + 隔離**: decomp `83536046…` (schema
  `n11-b29loss37-adoption-decomp-deltas-v1`) 全run byte一致・全gate
  PASS (契機行: class 2251 unknown 38→1・rank 4→3・status unknown)。
- 宣言前施行済み: tamper battery 15/15 (14 tamper案全rc=1捕捉+control
  rc=0)・pin群の機械照合 (ヘッダー17 sha定数+drive-1 prefix+VAL_GATES
  20 fileを実測と照合)。

## 採用効果 (機械観測・bookkeepingを勝敗として読まない)

- **class 2251: canonical unknown_now 38→1 (closure rank 4→3)。残る
  unknown 1行 = s5 93815 = 未消費ab028**。scenario statusはunknown
  のまま (free_now 38→38・excluded_now flip空・newly free空)。
- status counts両側不変: excluded 390 / excluded_now 23 / free_now 38
  / unknown 34,498。
- holder union 107 (2251 own 37・他106 class各1)。closure unknown減は
  2251 (38→1)・2257 (97→96)・2299 (98→97)・5535 (56→55)・8583 (59→58)
  ・9001 (60→59)・11779 (60→59) のみ・全UNKNOWNのまま。closure table
  808/808。churn stable-unknown 126 {excluded_now 2, unknown 124}。
  tie交換 left {1035 (rank 486, unknown 98)} / entered {2261
  (rank 460, unknown 97)} (group 15/39 anchor再選択bookkeeping)。
  anchors 23101 (1,1)・1849 (2,1) 不変・16757 unknown 29不変
  (rank 3→4・2251のunknown 1に追い抜かれ)。
- update8不変: resolved 141 / remaining 31,718・newly resolved空
  (採用37 s5 indexは要件集合と交差なし)。
- probe worklist 64,809→64,765 (net −44)。class 2251 serving 38→1
  (残り1行はちょうど未消費ab028: closure (37,81)・membership 3)。
  採用37キーはscenario worklistに0行残存。serving deltas: 1035
  (98→0)・2261 (0→97)・2257/2299/5535/8583/9001/11779 各−1。
- joint greedy union 35,691→36,903 (**+1,212・非monotoneな
  frozen greedy schedulerのbookkeeping**・per-root free/uncovered
  thirdsは全root不変・per-root roots summary不変 (root 27 = 119/119)・
  greedy movers root 14 (4,439→4,540, +101)・16 (−1)・37 (−96)・
  38 (−2)・49 (−1)。
- batch-29はprobe levelでfully probed: 54/54 (LOSS 53 = CU16+本37・
  WIN 1 unconsumed・EXHAUSTED 0)。

## 誠実記録・運用知見 (今回new)

1. **Part文字の並走衝突回避**: 計画時のPart DAは並走セッションが
   02:22Zに取得済み (`88ffdc92`・b29d2loss15第三実装交叉検証・読取
   専権レーン)。当レーンは**DA→DBに改名**して宣言 (対抗adoption宣言
   は直近25 commit機械走査で不存在を確認)。DA宣言自体が「canonical
   採用はpinned merger `90711961…` 経由の別adoption Part専権」と明記
   しており、本Part DBがまさにその役を担う補完関係。
2. **sha手転写タイポ2件を機械照合で捕捉**: extractorのVAL_GATES
   ブロックへpinshaを手転写した際2件のshaタイポが混入。宣言前の
   「ヘッダーsha定数+20 file実測照合」で検出・修正。**sha転写は
   必ず機械経由**の規約を再実証。
3. **merge-auditは入力path引数の字面を記録する**: 公式rerunで絶対
   path引数でmergeを呼ぶとaudit bytesが宣言pin (`2d7b4998…`) から
   ずれる (`f01b8626…`・差分はaudit JSON内のfile path fieldのみ・
   実質内容はpath正規化で完全一致)。**宣言時と同一の相対path引数
   (`root/...`) で呼び直すとbyte一致**。教訓: path埋め込み型auditの
   rerunは起動引数の字面まで再現する。
4. **1 bash invocation = 1 wave厳守** + 長時間waveは独立invocation
   (Part CPの環境reset事故の再来なし)。
5. refresh (~58s/run)・extractor (~4s/run) は変換処理のみ・NPU・
   外部リソース不使用・書込みは実験dir内のみ。
6. 出版push本文はsandbox内 `file_system.read_file` (行offset
   pagination・chunk連結・ASCII検証+byte数ゲート) で機械読込。
   262,326Bのmerged cacheもchunked再構成+fetch-back cmpでbyte完全一致。

## 並走 (非接触)

Part DA (batch-29 b29d2loss15第三実装・`88ffdc92`・読取専権で本Partと
補完)・Part CZ (ab028 corroboration・完了)・Part CP (batch-30 drive-3
宣言 `6edbcf58`)・Part CY drive-2 (batch-31・`21fef631`)・K1277
(高速レーン z=9 strip・02:35-02:37ZにA/B/C出版)。本Partの出版中に
観測した並走commitは全てパス非接触・pushは全てfast-forward成功・
fetch-back検証済み。

## これにより確定したこと・していないこと

- 確定: batch-29の37 fresh LOSS行がcanonical chainに採用され
  (CU含む計53 LOSS行)、**class 2251のcanonical serving unknown が
  38→1 に落ちたこと** (bookkeepingとして正確に記録)。
- 未確定: ab028のcanonical adoption (scrutiny owner C++ gate経由の
  別Part)・class 2251のclosure・secured coverage・root勝敗・
  batch-29のどのキーの最終verdictも本レーンでは確定させない
  (probe-level labelのcanonical採用は「当該キーのLOSS行がcacheに
  ある」ことのみを意味する)。
- **標準11×11空盤・19 central-reply roots・class 2251・batch-29全キー
  (ab028を含む)・batch-30/31キーはどの時点でも UNKNOWN**。
  nodes数・worklist行数・greedy union sizeを勝敗や距離として読まない。
