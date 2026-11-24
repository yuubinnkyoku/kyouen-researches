# Part DB 宣言: batch-29 (class 2251) 残37 LOSS行 (ab017..ab054 except ab028) の canonical adoption + reaudit deltas (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `cca29581`
(Part CP batch-30 drive-3 session script出版・2026-11-24T02:29:06Z)。
Part文字は直前の別セッションが「Part DA」(`88ffdc92`・b29d2loss15
第三実装交叉検証レーン) を取得済みのため、**DA→DBに改名**して宣言する
(対象作業は同一ではないが文字の衝突回避)。

## 対象と目的

published batch-29 kit
(`research/experiments/n11-centralreply-closure-class2251-batch29-20261123/`・
MANIFEST `7c124233…` 71 files・Part CI drive-2 完了log commit `141cf80c`:
batch-29 全54キー probe-complete LOSS 53 / WIN 1 (ab028) / EXHAUSTED 0)
のうち、Part CU (`2c2487f7`) で採用済みの16行 (ab001..ab016) と
WIN行 ab028 (Part CZ `68751fd7` で three-implementation corroboration
成立・verdict不消費) を除く **37 fresh LOSS行** を、CU先例の
pinned fail-closed union merger `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
(byte-clone・selftest PASS) で canonical merged cache に採用
(merge) する:

- BASE = Part CU canonical 6,317行 `30ddad9dc0add7e21698e864b5c202b8e6ebd3e396c4eb6156a85ff2d34005c4`
- ADOPTED-CANONICAL = BASE + 37行 = 6,354行 (WIN 158 / LOSS 6,196) `04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556`

37行 (合計 nodes **159,325,566/pass** = 2-pass node-exact):

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

(全行 kit raw p1/p2 byte一致 (2-pass node-exact)・status.log
`b49322d9ed8cd63e9bba20e10acd52b89849b408d19496931d5545b5ec99a6a0`
55行中の drive-2 PASS行 (budget 15000000, result 2, nodes) と一致。
status.log先頭16行は CU drive-1 prefix `6b877344…` と byte一致
(append-only chain gate)。)

**WIN行 ab028 は採用しない**: raw 2-pass node-exact (result 1,
nodes 3,167,121, key (1297036830121656320, 131074), s5 93815, legal 80,
membership 3) だが、increment・merge後cache・いかなるcanonical cacheにも
書き込まず **verdict不消費** (WIN行採用は引き続き scrutiny owner C++
第二実装 gate `9193f5b6…` 専権・Part CZ corroboration 済み)。
よって **class 2251 は freeにもexcludedにもならない**: BASE-unknown
38子 = 37採用 + 残1 = ab028 の s5 93815 のみで、status は unknown
のまま (unknown_now 38→1, closure rank 4→3)。
**閉鎖・被覆・secured・root勝敗の主張はしない。**
**標準11×11空盤・19 central-reply roots・class 2251・batch-29全キー
(batch-29 54キー・ab028を含む) はUNKNOWNのまま**。nodes数を勝敗として
読まない。

## 単一オーナー・非接触の機械確認 (observed HEAD cca29581)

- **Part DA** (`88ffdc92` 宣言・scaffold `267fec1a`/`9e0d71be`/`c5ccfbd3`:
  b29d2loss15 third-impl交叉検証): **読みのみ**の交叉検証レーンで
  「採用 (canonical cache merge) は CU先例の pinned fail-closed merger
  `90711961…` を経由する別adoption Part専権」と宣言済み。本Part DBが
  そのadoption Partに相当する。対象15キー (ab017..ab027+ab029..ab032) は
  本Partの37行に含まれるが、向こうはverdict不消費の読み専権レーンのため
  **書き込み衝突なし** (実験dirも `n11-centralreply-closure-b29d2loss15-thirdimpl-20261124`
  で完全に別)。本Partのmergeは相手のG6 unadopted gateのpin対象
  (CU出版物 `30ddad9d…` snapshot) を変更しない。
- **Part CP** (batch-30 class 34269・drive-3宣言 `6edbcf58`): 別バッチ・別
  class・別dir。**非接触**。
- **Part CY** (batch-31 class 5804・drive-2宣言 `21fef631`): 別バッチ・別
  class。**非接触**。
- observed HEAD `cca29581` 時点で直近25 commitを機械走査し、
  **37 LOSS行 (or 任意部分) のcanonical adoption を宣言した対抗レーンなし**
  (CU以来の adoption Part は本宣言のみ)。

## BASE 再現手続 (検証者用・publish済み出版物のみから)

BASE (Part CU reaudit outputs) は repo 揃いで fetch 可能:
`research/experiments/n11-centralreply-class2251-loss16-adoption-reaudit-20261123/`
配下 `reaudit/output/` の refresh-summary.json `b60d71a2…`・
closure-classes.csv `3019d37f…`・per-root-coverage.csv `61dbd39a…` と
`output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-20261123.cache`
`30ddad9d…`。
**probe-worklist.csv (64,809行) は体積のため repo 外**: CU出版の
`reaudit/scripts/refresh_adoption_b29loss16_adoption.py` (commit-pinned)
を当該実験tree上で実行し BASE worklist を
`…loss16…/reaudit/output/probe-worklist.csv` として再生成すれば
sha `0d7474e1adfbdbc8db438605e3e36310c1d8e656ab8c92899183f29b870a830a931c`
に byte一致 (本Partの準備作業で検証済み)。

## 事前宣言pin (全て本宣言前に機械計算・採用は宣言後に実行)

- maker `scripts/make_increments_b29loss37.py` `1e1aed907e3a75c5c2e87213198fcb5fe213462466cb5f92415944b839d53716` (×4 byte-stable)
- increment `output/increment-b29loss37-20261124.cache` `85bd44693edfd862a7cf74fc10414978fcf248dcef684a821b487f9757b443cc` (37行)
- manifest `output/increments-manifest.json` `1b51f30dabed6f4df435a3a034e1b5b9c2f405c75ebdcd918c0e256f2812d25a` (schema `b29loss37-increments-manifest-v1`)
- merger `scripts/s5_union_merge.py` `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a` (CU byte-clone・selftest PASS)
- merged cache `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-20261124.cache` `04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556` (6,354行)
- merge-audit ×3 `2d7b4998cfd5e6dbe99b716921b9f42e1ff4e680f545c676188b2b3f404ba40b` (全run同一byte)
- refresh `reaudit/scripts/refresh_adoption_b29loss37.py` `46d1bf3ad3d72e717d50773ca4241fad89ae585f1670d81249f41cdcfceec00c`
- refresh outputs (×3 + 隔離実行 byte一致):
  refresh-summary.json `1fc531d32fcd8817ec2b4bcfafea2b2c40fecde409c62347da3d7e7e1d601148`・
  closure-classes.csv `b37425d7686efc5446bd5e0dca9feac0413284e23f4e16e32cf8c5abc4d05bfb`・
  per-root-coverage.csv `8f69d5bbfbcace73985a66c2167b2b4f5e177a22f2bf427c71a7e466a93326bd`・
  probe-worklist.csv `4ecb9a0ac2d1c9282f54f1a554fd17088b5a47b93936e5c96d783cec91483599`
- extractor `scripts/compare_deltas_b29loss37_adoption.py` `be257558fea300391405717d20a327745e46d8563f4659ff96379d66e51a77a2`
- decomp `output/decomp-deltas-b29loss37-adoption.json` `8353604613533d6b6dca8e22d539a30cb8a725b280529fa330c9974cbfa693e0`
  (schema `n11-b29loss37-adoption-decomp-deltas-v1`・×4+隔離 byte一致)
- kit pins: batch-keys `330c0b9f…`・status.log `b49322d9…` (55行 = PASS 54 + WIN-HALT 1・drive-1 prefix `6b877344…`)・MANIFEST `7c124233…` (71 files・全file-by-file再検証)・val-gate 4パターン×4host (published-baseline/batch29/takeover/d2) 全replay byte一致 (node-exact)
- tamper battery 15/15 (14 tamper案全rc=1捕捉 + 無改変control rc=0)

## 宣言済み機械観測 (extractor gate・事前登録)

- status transitions 全安定 {excluded→excluded 390, excluded_now→excluded_now 23, free_now→free_now 38, unknown→unknown 34498}。excluded_now flips 空・newly free 空・free_now 38→38 (zero-WIN-consumed adoption)。
- class 2251: BASE-unknown 38 = batch s5 54 − CU既採用16 (chain continuity gate) = 採用37 + 残1; 残1 = [93815] = 未消費ab028; scenario status unknown (free_nowにもexcluded_nowにもならない)。
- holders (union 107): 2251 own 37・他106 classは各1。closure unknown_now変化は 2251 (38→1, rank 4→3) のみ、他は 2257 (97→96)・2299 (98→97)・5535 (56→55)・8583 (59→58)・9001 (60→59)・11779 (60→59) (全てUNKNOWNのまま)。churn stable-unknown 126 {excluded_now: 2, unknown: 124}・holder churnなし。closure table 808/808、left {1035 (rank 486, unknown 98)} / entered {2261 (rank 460, unknown 97)} (group 15/39 anchor候補再選択bookkeeping)。anchors: 23101 (1,1) 不変・1849 (2,1) 不変・16757 unknown 29不変でrank 3→4 (2251がunknown 1で追い抜き)。
- update8: resolved 141 / remaining 31,718 両側不変・newly resolved 空 (採用s5はupdate8要件外・機械確認)。
- worklist 64,809→64,765 (net −44)。class 2251 serving 38→1 (残る1行はまさに未消費ab028: s5 93815, class_unknown_now 1, closure (37,81), membership 3)。採用37キーはscenario worklistに0行残存。serving deltas: 1035 (98→0)・2261 (0→97)・2251 (38→1)・2257/2299/5535/8583/9001/11779 各−1。ab028はworklistに両側2行 (serving 2251 + 14338) を維持 (schedule bookkeepingのみ)。
- joint greedy union **35,691→36,903 (+1,212)** (NON-monotone・frozen greedy schedulerのbookkeeping・per-root free/uncovered thirdsは全root不変・被覆後退ではない)。per-root greedy movers: root 14 (4,439→4,540, **+101**)・16 (−1)・37 (−96)・38 (−2)・49 (−1) (root 14の+101も同じく計画サイズbookkeeping・free third 8→8)。roots summary 不変 (root 27 = 119/119)。
- per-root coverage (prc csv) free/uncovered: 全19 root両側不変。

## 実行計画 (宣言後・publish-then-execute)

1. 公式rerun (scratch tree含む): maker×4 → merger selftest+merge×3 → refresh regen ×3+隔離 → extractor×4+隔離。全出力が上記宣言pinとbyte一致すること。
2. 出版 A: scripts 4 (maker/merger/extractor/refresh)。B: increment+manifest+merge-audit×3。C: merged cache (262,326 bytes)。D: reaudit 3出力+decomp (probe-worklist.csvは体積のため出版しない・refresh regen手続本文に明記)。E: 実験README+MANIFEST-sha256 (repo内fileのshaのみ)。
3. fetch-back検証: commit-pinned raw URL + sha256sum。出版後に list_commits で着地確認。
4. 完了log + Knowledge更新。

verdict不消費・11×11 UNKNOWN担保不変。
