# Part DL 宣言: batch-31 (closure class 5804) 51 LOSS行 (ad001..ad054 except {ad024, ad028, ad043, ad055}) の canonical adoption + reaudit deltas (2026-11-24)

単一オーナー宣言・publish-then-execute。observed HEAD `890e6186`
(Part DK A scaffold・2026-11-24T08:12:48Z)。
Part文字は「Part DK」が 2026-11-24T08:11:41Z (`e411045b`・batch-30 ac013
25M high-budget再probe宣言) に別レーンへ取得されたため、本レーンは
**DK→DLに改名** して宣言する (Part DB宣言のDA→DB改名先例と同一の
衝突回避手続。対象作業は同一ではない。本セッションは元々「DK」で
成果物を作成していたが、DKの実効取得を list_commits で機械確認した
後、全成果物・script docstringを Part DL に改名し、公式隔離rerunで
全pinを再検証した上で本宣言する)。

## 対象と目的

published batch-31 kit
(`research/experiments/n11-centralreply-closure-class5804-batch31-20261124/`・
MANIFEST `3481019545cc1ed6d86765130ea895915e5b18865dfd6ed29d673fdff2d98b9a`
194 files・Part CY drive-1/drive-2 takeover + Part DI reprobe で batch-31
全55キー probe-complete: **LOSS 51 / WIN 4 / EXHAUSTED 0**) のうち、
**51 fresh LOSS行** を CU先例の pinned fail-closed union merger
`907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
(byte-clone・selftest PASS) で canonical merged cache に採用 (merge) する:

- BASE = Part DB canonical 6,354行 `04b0a23987a97518e276ea5ff966496facab22f93628cd5fbc682a04c3650556`
- ADOPTED-CANONICAL = BASE + 51行 = 6,405行 (WIN 158 / LOSS 6,247) `60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84`

51行 (合計 nodes **237,596,711/pass** = 2-pass fresh-cold node-exact):

| key | lo / hi | legal | s5 | membership | result | nodes |
|---|---|---|---|---|---|---|
| ad001 | 6053400849273585664 / 0 | 92 | 97381 | 3 | 2 (LOSS) | 5,609,720 |
| ad002 | 6052837899320164352 / 128 | 94 | 102238 | 3 | 2 (LOSS) | 4,555,434 |
| ad003 | 6053400849139367937 / 0 | 96 | 119474 | 4 | 2 (LOSS) | 5,940,995 |
| ad004 | 6053400849139367938 / 0 | 97 | 125125 | 4 | 2 (LOSS) | 3,434,932 |
| ad005 | 6053400849139367940 / 0 | 94 | 130687 | 4 | 2 (LOSS) | 3,420,177 |
| ad006 | 6053400849139367944 / 0 | 96 | 136105 | 4 | 2 (LOSS) | 7,296,844 |
| ad007 | 6053400849139367952 / 0 | 100 | 141315 | 4 | 2 (LOSS) | 7,840,993 |
| ad008 | 6053400849139367968 / 0 | 94 | 144458 | 3 | 2 (LOSS) | 2,362,665 |
| ad009 | 6053400849139369984 / 0 | 100 | 148458 | 4 | 2 (LOSS) | 2,479,959 |
| ad010 | 6053400849139372032 / 0 | 89 | 152721 | 4 | 2 (LOSS) | 12,273,095 |
| ad011 | 6053400849139376128 / 0 | 94 | 156973 | 4 | 2 (LOSS) | 2,914,995 |
| ad012 | 6053400849139384320 / 0 | 92 | 161166 | 4 | 2 (LOSS) | 5,968,986 |
| ad013 | 6053400849139400704 / 0 | 97 | 165259 | 4 | 2 (LOSS) | 5,270,933 |
| ad014 | 6053400849143562240 / 0 | 97 | 170887 | 4 | 2 (LOSS) | 3,337,929 |
| ad015 | 6053400849147756544 / 0 | 96 | 174498 | 4 | 2 (LOSS) | 4,271,124 |
| ad016 | 6053400849156145152 / 0 | 90 | 177679 | 4 | 2 (LOSS) | 3,479,933 |
| ad017 | 6053400849172922368 / 0 | 89 | 180752 | 4 | 2 (LOSS) | 2,805,657 |
| ad018 | 6053400849206476800 / 0 | 82 | 183816 | 4 | 2 (LOSS) | 7,948,923 |
| ad019 | 6053400857729302528 / 0 | 100 | 186724 | 4 | 2 (LOSS) | 6,567,285 |
| ad020 | 6053400866319237120 / 0 | 97 | 189532 | 4 | 2 (LOSS) | 4,663,738 |
| ad021 | 6053400883499106304 / 0 | 95 | 192176 | 4 | 2 (LOSS) | 4,826,218 |
| ad022 | 6053400917858844672 / 0 | 89 | 194523 | 4 | 2 (LOSS) | 3,183,609 |
| ad023 | 6053400986578321408 / 0 | 96 | 196763 | 4 | 2 (LOSS) | 2,795,664 |
| ad025 | 6053418441325412352 / 0 | 93 | 199913 | 4 | 2 (LOSS) | 2,750,868 |
| ad026 | 6053436033511456768 / 0 | 99 | 201807 | 4 | 2 (LOSS) | 3,940,244 |
| ad027 | 6053471217883545600 / 0 | 84 | 203738 | 3 | 2 (LOSS) | 1,624,906 |
| ad029 | 6053400849139367936 / 4 | 100 | 211491 | 4 | 2 (LOSS) | 2,936,438 |
| ad030 | 6052837907775881216 / 128 | 100 | 211529 | 4 | 2 (LOSS) | 3,146,845 |
| ad031 | 6052837899190140928 / 128 | 98 | 211582 | 4 | 2 (LOSS) | 5,946,707 |
| ad032 | 6052837899185948672 / 128 | 95 | 211655 | 4 | 2 (LOSS) | 11,268,913 |
| ad033 | 6052837899185946625 / 128 | 99 | 211693 | 4 | 2 (LOSS) | 5,883,887 |
| ad034 | 6053400849139367936 / 8 | 98 | 211744 | 4 | 2 (LOSS) | 4,885,748 |
| ad035 | 6052837916365815808 / 128 | 90 | 211788 | 4 | 2 (LOSS) | 3,582,819 |
| ad036 | 6052837899194335232 / 128 | 87 | 211830 | 4 | 2 (LOSS) | 1,675,597 |
| ad037 | 6052837899185950720 / 128 | 94 | 211891 | 4 | 2 (LOSS) | 5,417,573 |
| ad038 | 6052837899185946626 / 128 | 101 | 211921 | 4 | 2 (LOSS) | 4,503,724 |
| ad039 | 6053400849139367936 / 16 | 92 | 211965 | 4 | 2 (LOSS) | 4,962,308 |
| ad040 | 6052837933545684992 / 128 | 89 | 211996 | 4 | 2 (LOSS) | 1,723,362 |
| ad041 | 6052837899202723840 / 128 | 84 | 212031 | 4 | 2 (LOSS) | 2,168,706 |
| ad042 | 6052837899185954816 / 128 | 99 | 212087 | 4 | 2 (LOSS) | 3,179,879 |
| ad044 | 6053400849139367936 / 32 | 91 | 212160 | 4 | 2 (LOSS) | 2,251,201 |
| ad045 | 6052837967905423360 / 128 | 89 | 212175 | 4 | 2 (LOSS) | 7,781,306 |
| ad046 | 6052837899185963008 / 128 | 92 | 212243 | 4 | 2 (LOSS) | 3,560,629 |
| ad047 | 6052837898185946632 / 128 | 94 | 212273 | 4 | 2 (LOSS) | 11,064,379 |
| ad048 | 6053400849139367936 / 64 | 86 | 212307 | 4 | 2 (LOSS) | 10,316,369 |
| ad049 | 6052838036624900096 / 128 | 92 | 212340 | 4 | 2 (LOSS) | 3,146,801 |
| ad050 | 6052837899253055488 / 128 | 91 | 212372 | 4 | 2 (LOSS) | 1,897,590 |
| ad051 | 6052837899185979392 / 128 | 100 | 212404 | 4 | 2 (LOSS) | 3,580,351 |
| ad052 | 6052837899185946640 / 128 | 101 | 212432 | 4 | 2 (LOSS) | 5,410,550 |
| ad053 | 6052837899185946656 / 128 | 92 | 212464 | 3 | 2 (LOSS) | 4,094,246 |
| ad054 | 6052838174063853568 / 128 | 86 | 212512 | 3 | 2 (LOSS) | 1,644,957 |

(全行 kit raw p1/p2 byte一致 (2-pass fresh-cold node-exact)・status.log
`c69c2fec9d07e50dca6763fdb97acb5a05798b7852a1ab45be8e7a7a7889dd5b`
59行 = 55 PASS + WIN-HALT 3 + EXHAUSTED 1 (pinned ad043) と maker
G-gates で逐行検証。採用51キーは BASE (6,354行)・quarantine ともに不在
(base_cache_absent_hits_for_emitted 0・quarantine_hits 0)。raw台帳は
ad001..ad055 x {p1,p2} の計110 file (fragment/truncated sidecar なし)。)

**WIN 4行 (ad024/ad028/ad043/ad055) は採用しない** (verdict不消費・
WIN行採用は引き続き scrutiny owner C++ 第二実装 gate `9193f5b6…` 専権):

- ad024: s5 198576・result 1・nodes 4,360,661 (budget 15M)
- ad028: s5 207094・result 1・nodes 12,803,283 (budget 15M)
- ad043: s5 212115・result 1・nodes 18,247,029 (Part DI 30M再probe (kit MANIFEST `31ac5acd…` 40 files)・p1==p2 node-exact・同キーの published 15M EXHAUSTED行は DI kit内 exh15m clones と byte一致で supersede 鎖を maker が検証・anchors ad054/ad055 val-gate node-exact)
- ad055: s5 212536・result 1・nodes 3,364,655 (budget 15M)

よって **class 5804 は freeにもexcludedにもならない**: BASE-unknown
55子 = 51採用 + 残4 = 上記未消費WIN 4の s5 {198576, 207094, 212115,
212536} のみ。scenario status は unknown のまま (unknown_now 55→4)。
**閉鎖・被覆・secured・root勝敗の主張はしない。**
**標準11×11空盤・19 central-reply roots・class 5804・batch-31全キー
(WIN 4行を含む) はUNKNOWNのまま**。nodes数を勝敗として読まない。

(update8巨視: 採用51行のうち丁度1行 s5 148458 (ad009) がupdate8要件行:
resolved 141→142・remaining 31,718→31,717。)

## 単一オーナー・非接触の機械確認 (observed HEAD 890e6186)

- **Part DK** (宣言 `e411045b`・2026-11-24T08:11:41Z・scaffold `890e6186`:
  batch-30 ac013 25M再probe): 別class・別バッチ・別dir。verdict不消費の
  再probe専権レーン。**非接触** (本Partの入力・出版先と一切共通なし)。
- **batch-30 (class 34269) adoption**: Part DJ完了log (`41c9ede4`・5/6キー
  解決) と DK宣言の後も、observed HEAD時点で**未宣言**(直近30 commitを
  機械走査し、batch-30 or その他の batch行 canonical adoption 主張なし:
  DB以来の adoption Part は本宣言のみ)。もし batch-30 adoptionレーンが
  新しいcanonical headを本Partのmerge wave (C) より先に出版した場合は
  本Partは即時停止し、BASE再計画の上で次回実行に引き継ぐ (racing guard)。
- 実験dir
  `research/experiments/n11-centralreply-class5804-b31loss51-adoption-reaudit-20261124`
  は observed HEAD時点で remote に未存在 (get_file_contents 404機械確認
  予定・出版は A-E wave)。
- K1283-K1285 理論出版 (pair-slices等)・Part CT/CU/CZ/DB先例出版物:
  読み込み専用。非接触。

## BASE 再現手続 (検証者用・publish済み出版物のみから)

BASE (Part DB出版物) は repo 揃いで fetch 可能:
`research/experiments/n11-centralreply-class2251-loss37-adoption-reaudit-20261124/`
配下 `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-20261124.cache`
`04b0a239…` (6,354行) と `reaudit/output/` の
refresh-summary.json `1fc531d32fcd8817ec2b4bcfafea2b2c40fecde409c62347da3d7e7e1d601148`・
closure-classes.csv `b37425d7686efc5446bd5e0dca9feac0413284e23f4e16e32cf8c5abc4d05bfb`・
per-root-coverage.csv `8f69d5bbfbcace73985a66c2167b2b4f5e177a22f2bf427c71a7e466a93326bd`。
**probe-worklist.csv (64,765行) は体積のため repo外**: DB出版の
`reaudit/scripts/refresh_adoption_b29loss37.py` を DB実験tree上で実行して
BASE worklist を再生成すれば (当該実験dirの `reaudit/output/probe-worklist.csv`)
sha `4ecb9a0ac2d1c9282f54f1a554fd17088b5a47b93936e5c96d783cec91483599`
に byte一致 (本Partの準備作業で検証済み)。

## 事前宣言pin (全て本宣言前に機械計算・公式隔離rerunで再現検証済み)

- maker `scripts/make_increments_b31loss51.py` `65f5eec6e5f0ae710a7e4ef2096e308fd71990561921696d63fc90e5f27a7aaa`
  (0.3s・fail-closed G-gates: batch-31 kit MANIFEST 194 files 逐file検証・
  DI reprobe kit 40 files・5-host val-gate 20 files node-exact・55キー
  2-pass raw 110 files・status.log 59行逐行・ad043 supersede鎖
  (15M exhaustion raw byte-equal DI exh15m clones・DI 30M WIN nodes
  18,247,029)・BASE/quarantine 不在検証)
- increment `output/increment-b31loss51-20261124.cache` `87ffb450a32b7409682e27efc258b5ed514d32dbc4c5a2b983d3846031403d67`
  (51行 = header 42 + s5verdict 51・rows sorted by (lo,hi))
- manifest `output/increments-manifest.json` `ad6c4e2336d71b951769e6c280b18988db0ba4acde2340a2b386f1d0f41d5d12`
  (schema `b31loss51-increments-manifest-v1`・row_counts
  {probed 55, adopted 51, prior_adopted 0, wins 4, exhausted 0, fragments 0,
  fileless 0}・ad043_supersede block・base_cache_prior_adoption_confirmed 0・
  quarantine_hits 0)
- merger `scripts/s5_union_merge.py` `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
  (CU byte-clone・selftest PASS: positive dedupe+sort・WIN/LOSS conflict
  reject・malformed reject・determinism)
- merged cache `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-20261124.cache`
  `60222707dd13902103fc8f7ef11c8487ec1be531ad0711e23e50c32154e30b84`
  (6,405行・264,619 bytes・WIN 158 / LOSS 6,247)
- merge-audit ×3 `ed3577c464d89b3539d422d72f62d8e69e91f1736f0a12b994ce5db316adae7c`
  (全run同一byte・audit JSON内 path は実験dir相対)
- refresh `reaudit/scripts/refresh_adoption_b31loss51.py` `a6ed4b7eb280d9f21a9591c6d02c11293ed25918afbba115248b3d750ad44d52`
  (Part DB refreshの port・CACHE=merged cache 60222707・~59s/run)
- refresh outputs (×3 + env -i + 隔離実行で全て byte一致):
  refresh-summary.json `fea0b0d4473b34447556f3a3e8b9ecc7c57c59221b18c4bb58222e0149b2e4bc`・
  closure-classes.csv `50841fa47676be8af145f1f8f751b0d96f75e94417990418cbe1d2a52bd4d389`・
  per-root-coverage.csv `136e308a332c8ab6fe877f3ef3a3b361770931285d91a0d12a59a6dd9707b487`・
  probe-worklist.csv `006ccd78d061c22838b3cee7701a91649d35abf3c8d56cecbb05931b604846d5`
  (regen・repo外)
- extractor `scripts/compare_deltas_b31loss51_adoption.py` `83825eb590106e66c747d35e084d3c602f5f4ef94224f0c973f0ddaa2d66a323`
  (54 pin-gates)
- decomp `output/decomp-deltas-b31loss51-adoption.json` `1d55167920a8988daceb622424787b3deef227f379ded4e1b5ee96a0aac5fa7f`
  (×3+隔離 byte一致)
- kit pins: batch-keys `d058fddc862c5f62b387eea7c7ac5b78f2c5063661371b388e5078772af4ff0e`・
  batch-31 status.log `c69c2fec…` (59行)・b31 kit MANIFEST `3481019545cc…`
  (194 files)・DI kit MANIFEST `31ac5acd…` (40 files)・DI status
  `f681a3c4…`・jsreplay `84585617…`
- tamper battery 6/6 (rc=1捕捉 + 無改変control rc=0):
  T1 kit raw tamper→maker kit-hash drift abort・T2 status.log tamper→
  abort・T3 kit file欠落→abort・T4 BASE cache tamper→merger入力hash
  gate abort・T5 WIN-conflict increment注入→merger "WIN/LOSS conflict"
  reject (出力file 生成なし)・T6 scenario cache tamper→extractor sha
  drift abort

本Partの計算実行は全て単一host・逐次 (4並列目安以内・実際は1-2 procs)。
大規模中間fileの作成なし (probe-worklist.csv regen 3.7MB のみ・repo外)。

## 宣言済み機械観測 (extractor 54 pin-gates・事前登録)

- status transitions 全安定 {excluded→excluded 390, excluded_now→
  excluded_now 23, free_now→free_now 38, unknown→unknown 34,498}。
  excluded_now flips 空・new_free 空 (zero-WIN-consumed adoption)。
  採用51行は全て unknown→unknown (class status不変)。
- class 5804: BASE-unknown 55 = 採用51 + 残4; 残4 = 未消費WIN 4のs5
  {198576, 207094, 212115, 212536}。scenario status unknown のまま
  (unknown_now 55→4)。
- closure変化は3行のみ: 5804 (38,55)→(4,4)・8730 (60,56)→(30,54)・
  8811 (50,55)→(38,54)。churn 54 (excluded_now 4 / unknown 50)・
  closure left/entered 空。holder union 126 (5804 own 51・8730 2・8811 2・
  他21 class各2)。
- update8: resolved 141→142 (+1: s5 148458 = ad009)・remaining
  31,718→31,717。
- worklist 64,765→64,711 (net −54)。class 5804 serving 55→4 (残る4行は
  未消費WIN 4のs5そのもの)。未消費WIN 4キーのworklist行は維持
  (ad024はserving classes {5804, 8811}、他3キーは{5804}のみ:
  schedule bookkeepingのみ)。
- joint greedy union **36,903→36,854 (net −49)**。PRG/IG movers
  {4: −1, 5: −2, 13: −1, 25: −1, 38: −50, 49: −105} (frozen greedy
  schedulerのbookkeeping)。per-root greedy free third は全20 root不変
  (root 27 = 119/119)。
- per-root coverage (prc csv) free/uncovered: 全root両側不変
  (被覆後退なし)。

## 実行計画 (宣言後・publish-then-execute)

1. 宣言後の公式隔離rerun (clean copy: maker→merger selftest+merge×3→
   refresh regen→extractor) で全出力が上記pinに byte一致すること。
2. 出版 A: scripts 4 (maker/merger/refresh/extractor)。B: increment +
   manifest + merge-audit×3。C: merged cache (264,619 bytes)。D: reaudit
   3出力 + decomp (probe-worklist.csvは体積のため出版しない・regen手続は
   BASE 再現手続節の通り)。E: 実験README + MANIFEST-sha256 (repo内実験dir
   fileのshaのみ)。各waveの直前に list_commits racing guard。
3. fetch-back検証: 各fileを get_file_contents (sha照合)。出版後に
   list_commits で着地確認。
4. 完了log + Knowledge更新。

verdict不消費・11×11 UNKNOWN担保不変。
