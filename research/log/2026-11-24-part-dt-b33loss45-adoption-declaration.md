# Part DT 宣言: batch-33 (closure class 34908) 45 LOSS行 (probe-complete・mixed packet) の canonical adoption + reaudit deltas (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `ff3e99c1`
(W_24 s-spectrum lane・2026-11-24T19:07:16Z)。
Part文字は「DT」を採用 (直近 main の commit message 機械走査で
「b33loss45」は total_count=0、「Part DT」も total_count=0。本宣言は
DT の最初の出版物)。

## 対象と目的

Part DQ/DR/DS drive-1+2+3 batch-33 (closure class 34908) は probe-complete
で、published kit の全54キーが honest two-pass fresh-cold label
(budget 15M・status.log 66行 = 54 PASS verdict行 {45 LOSS, 4 WIN,
5 EXHAUSTED} + 4 WIN-HALT marker + 5 EXHAUSTED marker + 3 resolved
P2-TRUNCATED-RETRY marker・MISMATCH 0) を持つ。**mixed packet から
45行の fresh LOSS行のみを** pinned fail-closed union merger
`907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac46a74606a`
(CU byte-clone・selftest PASS) で canonical merged cache に採用 (merge)
する:

- BASE = Part DP canonical merged cache・6,502行 sha256
  `1ded9a083feabc095dd998c92002b47efc05b8666adf030501bcffc2873a9dd6`
  (WIN 158 / LOSS 6,344・DP 出版byteを改変せずそのまま pin)
- ADOPTED-CANONICAL = BASE + 45行 = 6,547行 (WIN 158 / LOSS 6,389)
  merged cache名 = DP cache名 + `-plus-b33loss45`:
  `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-20261124.cache`
  sha256 `973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b`
  (6,547行・271,884 bytes)

45採用行 (合計 nodes **281,411,183/pass** = 2-pass fresh-cold node-exact、
全行 decisive budget 15,000,000・published batch-33 kit raws):

| key | lo / hi | legal | s5 | membership | result | nodes @15M |
|---|---|---|---|---|---|---|
| af001 | 1152921504742113281 / 68719476736 | 91 | 1176 | 2 | 2 (LOSS) | 2,952,432 |
| af002 | 10376293541462671361 / 68719476736 | 93 | 38614 | 3 | 2 (LOSS) | 10,550,283 |
| af004 | 1152921779485802497 / 68719476736 | 96 | 225112 | 4 | 2 (LOSS) | 3,318,813 |
| af005 | 5764607523035283457 / 68719476736 | 98 | 259539 | 4 | 2 (LOSS) | 5,078,821 |
| af006 | 1152921504607961089 / 68719476736 | 98 | 325164 | 3 | 2 (LOSS) | 5,970,933 |
| af007 | 1152921504607895553 / 68719476737 | 99 | 356884 | 3 | 2 (LOSS) | 7,700,082 |
| af008 | 1152921504607895585 / 68719476736 | 91 | 415399 | 4 | 2 (LOSS) | 14,364,852 |
| af009 | 1152921504607895553 / 68719476738 | 93 | 442092 | 4 | 2 (LOSS) | 3,618,250 |
| af010 | 1153202979584606209 / 68719476736 | 84 | 494504 | 2 | 2 (LOSS) | 5,558,617 |
| af011 | 1152921504607895553 / 68719476992 | 84 | 544291 | 2 | 2 (LOSS) | 9,514,618 |
| af012 | 1152921642046849025 / 68719476736 | 91 | 564062 | 4 | 2 (LOSS) | 9,240,870 |
| af013 | 1152922054363709441 / 68719476736 | 94 | 597227 | 4 | 2 (LOSS) | 6,573,273 |
| af014 | 1155173304421580801 / 68719476736 | 98 | 605532 | 4 | 2 (LOSS) | 9,869,039 |
| af015 | 1152921504607895553 / 68719477248 | 96 | 625618 | 4 | 2 (LOSS) | 5,884,486 |
| af016 | 1152921504675004417 / 68719476736 | 97 | 682541 | 4 | 2 (LOSS) | 5,920,144 |
| af017 | 1152921504876331009 / 68719476736 | 93 | 709725 | 4 | 2 (LOSS) | 6,520,712 |
| af018 | 1157425104235266049 / 68719476736 | 93 | 716543 | 4 | 2 (LOSS) | 4,504,991 |
| af019 | 1152921504607895553 / 68719477760 | 100 | 732262 | 4 | 2 (LOSS) | 4,140,443 |
| af020 | 1152921504607928321 / 68719476736 | 96 | 772553 | 4 | 2 (LOSS) | 6,989,622 |
| af021 | 1152921504608026625 / 68719476736 | 96 | 794839 | 4 | 2 (LOSS) | 5,619,693 |
| af022 | 1161928703862636545 / 68719476736 | 95 | 800281 | 4 | 2 (LOSS) | 4,329,388 |
| af024 | 1152921504607895569 / 68719476736 | 87 | 839602 | 4 | 2 (LOSS) | 6,089,162 |
| af025 | 1152921504607895617 / 68719476736 | 97 | 854635 | 4 | 2 (LOSS) | 2,894,174 |
| af026 | 1170935903117377537 / 68719476736 | 100 | 858969 | 4 | 2 (LOSS) | 4,299,814 |
| af027 | 1152921504607895553 / 68719480832 | 90 | 866321 | 4 | 2 (LOSS) | 2,601,444 |
| af028 | 1152921573327372289 / 68719476736 | 86 | 887040 | 2 | 2 (LOSS) | 3,569,293 |
| af030 | 1152921504641449985 / 68719476736 | 101 | 904339 | 4 | 2 (LOSS) | 4,462,892 |
| af031 | 1152921505144766465 / 68719476736 | 97 | 913616 | 4 | 2 (LOSS) | 4,165,016 |
| af032 | 1152923703631151105 / 68719476736 | 97 | 916477 | 4 | 2 (LOSS) | 5,132,691 |
| af033 | 1152921504607895553 / 68721573888 | 101 | 921203 | 4 | 2 (LOSS) | 11,737,990 |
| af035 | 1152921504608157697 / 68719476736 | 97 | 937328 | 4 | 2 (LOSS) | 6,690,990 |
| af036 | 1152925902654406657 / 68719476736 | 93 | 939215 | 4 | 2 (LOSS) | 3,982,739 |
| af037 | 1152921504607895553 / 68723671040 | 97 | 941383 | 4 | 2 (LOSS) | 10,047,387 |
| af038 | 1152921504607895561 / 68719476736 | 98 | 946835 | 4 | 2 (LOSS) | 8,731,665 |
| af040 | 1152930300700917761 / 68719476736 | 94 | 951758 | 4 | 2 (LOSS) | 5,576,569 |
| af041 | 1152921504607895553 / 68727865344 | 101 | 953035 | 4 | 2 (LOSS) | 7,100,779 |
| af042 | 1152921504607903745 / 68719476736 | 86 | 958529 | 3 | 2 (LOSS) | 10,487,546 |
| af043 | 1152921504608419841 / 68719476736 | 97 | 960072 | 4 | 2 (LOSS) | 6,467,873 |
| af044 | 1152921506755379201 / 68719476736 | 95 | 960568 | 4 | 2 (LOSS) | 11,691,718 |
| af045 | 1152921504607895553 / 77309411328 | 91 | 960786 | 3 | 2 (LOSS) | 3,895,802 |
| af046 | 1152921504607895557 / 68719476736 | 99 | 961459 | 4 | 2 (LOSS) | 5,382,774 |
| af049 | 1152921504607895553 / 85899345920 | 99 | 962233 | 4 | 2 (LOSS) | 4,811,237 |
| af051 | 1152921504609992705 / 68719476736 | 96 | 962410 | 4 | 2 (LOSS) | 5,475,786 |
| af052 | 1152921504606852096 / 17626545782784 | 90 | 962450 | 4 | 2 (LOSS) | 3,611,892 |
| af054 | 1152921504606852096 / 87960930222080 | 88 | 962471 | 2 | 2 (LOSS) | 4,283,588 |

注: 上表の lo/hi は整数表記であり、公式 pin は maker の ADOPTED_KEYS
(key tuple) と kit raws/batch-keys が byte 照合する。全54キーの総 nodes
は 383,609,606 (drive-3 README 記載と一致)。

**verdict 不消費の 9行** (本 Part では一切採用しない・BASE にも入れない):

| key | lo / hi | legal | s5 | label | nodes @15M |
|---|---|---|---|---|---|
| af003 | 3458764513821589505 / 68719476736 | 93 | 153030 | EXHAUSTED (honest UNKNOWN) | 15,000,000 |
| af023 | 1152921504607895553 / 68719478784 | 94 | 810351 | EXHAUSTED (honest UNKNOWN) | 15,000,000 |
| af029 | 1152921504607895553 / 68720525312 | 86 | 900646 | WIN (WIN-HALT marker) | 4,862,485 |
| af034 | 1152921504607911937 / 68719476736 | 95 | 930660 | EXHAUSTED (honest UNKNOWN) | 15,000,000 |
| af039 | 1152921504607895681 / 68719476736 | 89 | 950512 | EXHAUSTED (honest UNKNOWN) | 15,000,000 |
| af047 | 1152921504607895809 / 68719476736 | 84 | 961976 | WIN (WIN-HALT marker) | 9,841,975 |
| af048 | 1152921508902862849 / 68719476736 | 87 | 962172 | EXHAUSTED (honest UNKNOWN) | 15,000,000 |
| af050 | 1152921504607899649 / 68719476736 | 94 | 962386 | WIN (WIN-HALT marker) | 7,311,834 |
| af053 | 1152921504606852096 / 17660905521152 | 90 | 962470 | WIN (WIN-HALT marker) | 5,182,129 |

4 WIN行は scrutiny-owner C++ 第二実装 gate (pin `9193f5b6…`) 通過後に
別 adoption Part でのみ採用可能。5 EXHAUSTED行は honest UNKNOWN
(高budget再probeは別宣言条件)。したがって increments-manifest は
`full_packet_eq_loss_only=false`・`win_scenario_exists=true` で class 34908
は本 Part では **free化も excluded化もしない**。

## 入力証拠 (全て published bytes・宣言前に本セッションでfile-by-file検証)

- batch-33 kit: `research/experiments/n11-centralreply-closure-class34908-batch33-20261124/`
  MANIFEST sha256 `f2603e3a12d291579f02b81b7c388b5c952b90125df53756c91812368f16dbcb`
  (manifest 186行・file 186/186 sha一致を本セッションで取得検証・
  MANIFEST自体は kit root に出版されており manifest は自身を含まない)
- drive status.log: `1f663fc802c03b27c2e39d6130cf6c1392d62dd99b5847d6af477cd823a94b52`
  (66行 = 54 PASS verdict行 {4 WIN-HALT行・5 EXHAUSTED行・3 P2-TRUNCATED-RETRY行
  は marker}・first=`2026-11-24T17:04:25Z af001 PASS 15000000,2,2952432`・
  final=`2026-11-24T18:41:47Z af054 PASS 15000000,2,4283588`・行ごとに
  raw pair と (15M, result, nodes) 一致を maker が検証)
- batch-keys: `8a863381454fcfec3cb190db7130ce6801accf56170ee3a1b944402491fecbaa`
  (schema n11-centralreply-closure-class34908-batch33-input-v1・class 34908・
  budget 15M・54キー・kit選択時点 rank 36・runner_up 11490・
  published_base_canonical_rows 6,502 の frozen snapshot・
  groups_served_full [(0,20),(0,100),(12,10),(12,110)]・
  class_mask ["1152921504607895553","68719476736"])
- jsreplay.js: `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
  (pinned solver image・過去の kit と同一byte)
- val-gate: 4 molecule × 2 host (published-baseline + b33-host)
  全て node-exact
  (at2m-s5-1152921504606851072-536870946=(2000000,0,2000000)・
  at2m-s5-1188950301626860544-536870912=(2000000,0,2000000)・
  first-15m=(15000000,2,3651923)・second-15m=(15000000,2,5040200))
- raw inventory: 108 primary pair (54×{p1,p2}) + 3 pinned truncated-retry
  sidecar (af008/af039/af048 各 `# replay_done` guard なし・retry artifact
  であり verdict行ではない)
- 採用45キーは BASE (6,502行)・quarantine registry
  `81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9`
  の双方に不在 (fresh-increment gate・機械確認済)。不採用9キーも
  BASE に不在・採用集合と衝突しない (機械確認済)。

## 単一オーナー・非接触の機械確認 (observed HEAD ff3e99c1)

- **Part DQ/DR/DS** (batch-33 drive実行 lane・完了 commit `72877473a`):
  本 Part の入力証拠は読み込み専用。非接触。
- **Part DP** (b32loss54 adoption): BASE を提供・非接触 (DP出版物の
  byte は変更しない)。
- **K-items / W_24 lanes** (K1301, W_24 s-spectrum等): 別 asset 体系・非接触。
- **batch-33 (class 34908) adoption**: observed HEAD 時点で未宣言
  (b32loss45/b33loss45 採用主張なし・実験dir
  `n11-centralreply-class34908-b33loss45-adoption-reaudit-20261124` 未存在)。
  もし本宣言以降・wave C (merged cache出版) より先に他レーンが同 adoptionを
  出版した場合は即時停止し BASE 再計画の上で次回へ引き継ぐ (racing guard)。

## 事前宣言する期待機械観測 (本セッションの dry-run で一度生成済み・
## 出版後に独立 rerun で byte 再現を検証する)

全て reaudit refresh (Board による子検証 fail-closed) と decomp delta
extractor (両 refresh script の byte-verbatim 再実行) から得た機械観測:

- **class 34908 (56子 = 2 BASE既知LOSS s5 {955954, 958114} + 54 batch key)
  は unknown のまま**: 45採用で unknown children 54→9 (残り9 = 4 unconsumed
  WIN + 5 EXHAUSTED)。free_now 39→39・unknown 34,497→34,497・
  excluded_now 23→23・excluded 390→390、Board 検証 39/39 (rejected 0)。
  **class 34908 は free化しない。free_now・coverage は Board-derived な
  scheduling bookkeeping であり、root 勝敗でも coverage 主張でもない。**
- closure 表: 807→807行 (left=[]・entered=[]・行数不変)、
  完全 stable 775行・rank churn のみ 30行・class 34908行は
  rank 36→5・unknown_now 54→9・groups_served_count 4→5 のみ変化
  (45行の delta は Board 子境界上の own採用 45 と一致)、
  class 34269 は groups_served_count 5→4 (rank 5→6・unknown不変) の
  純 scheduling churn。unknown_now 変化クラスは class 34908 以外なし。
- per-root coverage: free/uncovered thirds は全rootで不変 (classが
  freeでないため)。individual greedy union は root 0 (3,054→3,009)・
  root 1 (6,353→6,352)・root 12 (2,986→2,984)・root 13 (6,175→6,174) のみ
  減少 (再選択 churn)。root 27 は 119/119 不変。unique_groups 2,115→2,115。
  joint greedy union は 36,968→36,849 (**減少**: class-34908 の frontier
  cost が 54→9 に低下する再選択 bookkeeping)。worklist 64,609→64,564
  (-45)。per-root remainingは root 0 (-3) と root 12 (-2) のみ減少。
- update8: resolved 187→188 (新規 s5 {962471}・採用45内)、
  remaining 31,672→31,671、groups_free_now 131 静止、
  known_universe 681→726・cache_rows_in_universe 658→703
  (cache_rows 6,502→6,547・verdicts WIN 158 / LOSS 6,344→6,389)。
- **閉鎖・被覆・secured・root勝敗の主張は一切しない。標準11×11空盤・
  19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・5343・5804・34269・34908 (WIN 4行/EXHAUSTED 5行を含む
  全54キー) は全時点で UNKNOWN。nodes数を勝敗として読まない。**

## 実行計画 (宣言後・publish-then-execute)

実験dir: `research/experiments/n11-centralreply-class34908-b33loss45-adoption-reaudit-20261124/`

1. wave B: scripts 4 = maker `make_increments_b33loss45.py`
   (sha256 `561dc1cce76da2ebf1e5d4346fb2fc222302f2eb403da6d0fc0d25ad1d6a49ea`・
   kit MANIFEST 186 file・54行2-pass・status 66行honest-history照合・
   WIN/EXHAUSTED marker照合・BASE/quarantine 不在・val-gate node-exact・
   raw inventory 108+3 の fail-closed gates)・merger `s5_union_merge.py`
   (byte-clone `90711961…`)・extractor
   `compare_deltas_b33loss45_adoption.py`
   (sha256 `70219793880c7e2797eb8f6df3a56870584b3eb4e4f8d5ee1ca8e98d2a74a598`)・
   refresh fork `reaudit/scripts/refresh_adoption_b33loss45.py`
   (DP `41bf706f…` の fork・sha256
   `5533b3f908cff069c6d86c5b96f32c6f978fda6b7ec5e8d32a3302a344363dee`・
   CACHE=merged cache `973bcd19…`・graph/update8/board/policy/quarantine
   pin不変)。
2. wave C: increment `increment-b33loss45-20261124.cache`
   (sha256 `255d54f5757ea19d00894e1f5483ab030634ca979a9fa6ed66390eda0ad3f155`・
   45行) + `increments-manifest.json`
   (sha256 `4b0a9f0fc08dc88d9ecc7807dad3ee503c59f9cbc9a233a2b3ddb72f5bcd1c70`・
   schema b33loss45-increments-manifest-v1・mixed-packet構造はPart DN式:
   `full_packet_eq_loss_only=false`・`win_scenario_exists=true`・
   `unadopted_win_ids`・`exhausted_excluded_ids`・status_log全行pin) +
   merge-audit-run1/2/3
   (3回とも sha256 `13c9739517d1f36f112de09c1a52009a4d6f68e37566fd3fe4dd61465711379b`)
   + merged cache (sha256 `973bcd19…`・6,547行・271,884 bytes)。
3. wave D: reaudit 3出力 (refresh-summary.json
   `38fc4e193cf08cf4efb7830a8bad3d2245bc732380f44c4ee2913e05d5644732`・
   closure-classes.csv
   `6cc33dd731c5d2237291552a91c3f7d60947bba875867fcab10394b533f1a68d`・
   per-root-coverage.csv
   `c5a2721d60c641ead369d10184e477cd5156ba7d02561c31dcd77b7b81b6f504`
   probe-worklist.csv は体積で非出版・regen pin
   `5881d7b3b51ef0ce780abaadaf7043c1fbcd3b258b9a261cadd2c539fb35ba61`)
   + decomp deltas
   (`output/decomp-deltas-b33loss45-adoption.json` sha256
   `a87c1ebdfdbe2170ea5ed0176f7fcf11b3257554dab202f65aee4a9eea4b331f`)
   + README + MANIFEST-sha256。
4. wave E: 完了log (tamper battery 記録含む)。
5. tamper battery (sandbox stage - T1〜T8) を maker/merger/refresh に施行し
   rc=1 捕捉と復旧後 sanity rc=0 を記録する (本セッションの dry-run で
   8項目全て fail-closed ABORT・復旧後再現を確認済み・完了logに記録)。

本 Part の計算実行は全て単一host・逐次 (4並列目安以内)。大規模中間fileの
作成なし (probe-worklist regen ~4.4MB・repo外)。

verdict不消費の残務 = 4 WIN行 (scrutiny-owner C++ gate `9193f5b6…` 待ち)
+ 5 EXHAUSTED行 (高budget再probeは別宣言条件)・11×11 UNKNOWN担保不変。
