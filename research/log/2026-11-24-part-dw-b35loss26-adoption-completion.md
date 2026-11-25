# Part DW 完了: batch-35 (class 16757) 26-LOSS canonical adoption 完了log (2026-11-24)

単一オーナー Part DW。宣言
`research/log/2026-11-24-part-dw-b35loss26-adoption-declaration.md`
(observed HEAD `4d2d506a` = K1307(仮) REMO lane commit・2026-11-24T22:03:42Z
時点)。commit message 機械走査で「b35loss26」「Part DW」とも
total_count=0 で宣言時点で未使用の Part 文字。**11×11 空盤は UNKNOWN の
まま** (本 Part で消費した verdict は26 exact LOSS行のみ・2 WIN行 (b032/
b048) と batch-1 WIN b018 は不消費・class 16757 は free化せず)。

## 出版物と pin (全て本セッションの実行で byte 生成・fetch-back sha256照合済み)

実験dir `research/experiments/n11-centralreply-class16757-b35loss26-adoption-reaudit-20261124/`
(MANIFEST self-sha `013835e2…`・14エントリ):

- scripts/make_increments_b35loss26.py `57d276d4…` (commit `fe8a7f3e`)
  (maker・kit MANIFEST 109 file sha検証・28行2-pass fresh-cold再検証
  (`# replay_done` both passes)・status 30行 honest-history照合・
  raw/batch-keys (legal,lo,hi,s5,mcc) 照合・raw inventory 56 primary +
  sidecar 0・val-gate 4 molecule x 2 host node-exact・採用26キーの
  BASE 6,547行/quarantine `81d23160…` 不在・不採用2キーの BASE 不在・
  採用 per-pass nodes 67,593,391・全28 nodes 73,757,659・3x byte-identical)
- scripts/s5_union_merge.py `90711961…` (commit `4c675e2a`・pinned merger
  byte-clone・selftest PASS・変更なし)
- scripts/compare_deltas_b35loss26_adoption.py `d20750fb…` (commit
  `fb2d9e29`・extractor・20 artifact pin・kit 109検証・両 refresh script
  scratch 再実行 byte一致・Board 49子境界再生成・全 delta pin照合)
- reaudit/scripts/refresh_adoption_b35loss26.py `4aaabcd5…` (commit
  `488ca027`・DT `5533b3f9…` の fork・docstring と CACHE pin `23d40e36…`
  のみ変更・graph/board/policy/quarantine pin不変)
- output/increment-b35loss26-20261124.cache `10cb8589…` (26行・commit
  `d6a13bc2`)
- output/increments-manifest.json `e925cf0c…` (commit `32c8b9a1`・schema
  b35loss26-increments-manifest-v1・mixed-packet構造: `full_packet_eq_loss_only
  =false`・`win_scenario_exists=true`・unadopted WIN b032/b048・EXHAUSTED 0・
  status 30行 pin・kit manifest pin・val-gate multi-host node-exact)
- output/merge-audit-run{1,2,3}.json 3回とも `a2548c1a…`
  (commits `b9675a6f`/`ad46f056`/`c498b8e3`)
- output/merged-exact-s5-chain-plus-...-plus-b35loss26-20261124.cache
  `23d40e36…` (6,573行・WIN 158 / LOSS 6,415・merge-audit×3同一sha・
  commit `521e9368`)
- output/decomp-deltas-b35loss26-adoption.json `d952a6cb…` (commit
  `b962f152`・schema b35loss26-adoption-decomp-deltas-v1)
- reaudit/output/refresh-summary.json `5fe3e5ab…` (commit `6e057ad0`)
- reaudit/output/closure-classes.csv `b7241eb0…` (commit `6f8a5062`・
  807行・class 16757行 = rank 4 / unknown 3 / groups 5)
- reaudit/output/per-root-coverage.csv `f1abcd85…` (commit `83b90ea1`・
  root 27 119/119)
- probe-worklist.csv は体積で非出版・regen pin `86767be9…`
- README.md `1f6c2868…` (commit `10e5377f`)・MANIFEST-sha256.txt
  `013835e2…` (commit `97eb9326`・14エントリ fetch-back 14/14照合)

## 実行の経過 (publish-then-execute・単一host逐次)

1. wave A: 宣言を出版 (observed HEAD `4d2d506a`・racing guard 走査
   「b35loss26」0件・「Part DW」0件)。同時に Part DV 完了log
   (`8548e231` 部位) を出版。
2. wave B: scripts 4を出版 (merger byte-clone `90711961…` 含む)。
3. wave C: maker実行 (kit 109/109 sha検証 → increment/manifest 生成) →
   merger ×3 (6,573行・audit同一sha) → increment/manifest/audit/merged
   cache出版。
4. wave D: refresh fork実行 (reaudit 3出力 + worklist regen) →
   extractor実行 (両 refresh script scratch再実行 byte一致・decomp
   deltas生成・DECOMP OK changed=2 rank_churn=28 gs_dec=0 stable=776) →
   reaudit 3出力・decomp deltas・README・MANIFEST-sha256出版。
5. wave E: 本完了log 出版。

## 検証の要点 (extractor fail-closed 全 gate PASS)

- canonial relation: SCEN == BASE 6,547行 + 26 increment rows verbatim
  (他は不変・WIN 158 / LOSS 6,415)
- class 16757 (Board 49子境界): unknown 29→3 (b018/b032/b048 不消費WIN
  残存)・rank 7→4・groups_served 5 static・**NOT freed / NOT excluded**
- closure table 807行キープ (left 0 / entered 0)・rank churn 28行・
  unknown変化 micro-class 2件 (30118 55→54 own 1・30484 54→52 own 2・
  Board own-membership検証)・stable 776行
- update8: resolved 188→214 (+26 = 採用26 s5全てが baseline requirement
  内)・remaining 31,671→31,645・groups_free_now 131 static・win_hit []
- class_status_counts 完全 static (excluded 390 / excluded_now 23 /
  free_now 39 / unknown 34,497)・board_verified 39/39
- per-root: free/uncovered thirds 全 root 不変・root 27 119/119。
  individual greedy は root 48/36/0 で減少し root 24 で増加 (2778→2829・
  re-selection bookkeeping)。per-root remaining は root 36 (-78) /
  48 (-52) のみ減少
- joint greedy 36,849→36,943 (+94 bookkeeping)・worklist 64,564→64,535
- tamper battery T1-T4 (kit raw tamper / status tamper / batch-keys
  tamper / merged verdict flip 2→1): 全て ABORT (fail-closed)・復帰後
  kit 109/109 再検証・merged cache merger再実行で byte一致

## 次の作業

- closure表 rank上位は class 23101 (unknown 1)・1849 (1)・2251 (1)・
  16757 (3・不消費WIN×3)・5804 (4)・34908 (9)・34269 (11)・5343 (46)。
  EXHAUSTED残は 34908×5・5804 ad043 (30M WIN化済み) の高budget再probe
  とWIN行交叉検証 (DU-b流第三実装・scrutiny C++ gate は実行可環境が前提)
  を別Partで着手する。
