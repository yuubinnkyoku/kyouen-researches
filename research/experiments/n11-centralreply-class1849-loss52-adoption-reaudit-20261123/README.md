# n11 central-reply batch-26 (class 1849) 52-LOSS canonical adoption reaudit (Part BU, 2026-11-23)

単一オーナーとして本hostが実行した、batch-26 (class 1849; Part BQ drive-1 +
Part BT residual) の52 LOSS行を canonical exact-S5 verdict cache へ計上する
採用・再監査実験。Part BU declaration は note Part BU amendment として実行前に
出版済み (publication commit `b299f42`、observed HEAD-before-push
`4ccf1630`)。

**full == loss ではない**ことが本実験の核心である: batch-26 の resolved
packet は53キー (honest label: WIN 1 (l028) + LOSS 52、row-audit full-v2
`cb4158d9…`・53 rows / mismatches 0・2-pass node-exact・pass総nodes
208,202,177) だが、採用するのは52 LOSS行のみ。l028 WIN (s5 index 81011,
2-pass node-exact result 1, 4,893,014 nodes, Part BS 第三実装交叉検証込み
4系統裏付け) は本採取では**不採用** (unadopted_win_ids == ["l028"]、
batch-14residual q042 / Part AS 先例と同一取り扱い)。l028 は28
unconsumed closure WIN候補の一員のまま Reader/Writer とも非接触で残り、
採用判断は scrutiny owner C++ 第二実装 gate (pin `9193f5b6…`) が通過した
後の別法律に依る。したがって**class 1849 は本採用では閉じない**
(unknown_now 53→1、残る1個は l028 のみ)。閉鎖・被覆・root勝敗の主張は
本READMEでは一切しない (すべて機械表明・機械検査):

1. increments maker (`scripts/make_increments_batch26.py`, sha256
   `838a5c840af7627e87bee655c4da641c391c1bf79a87a908b1cd6eefabbfe23b`,
   published Part BI maker `04bde073…` の batch-26 adapt) を published
   batch-26 kit 204ファイル (MANIFEST `af6da4ce…`・row-audit
   `cb4158d9…`・batch-keys `f1ea43ae…`) から実行し、52 LOSS行
   increment (sha256
   `19f6306e6c15e11e4eb3ead4c7cd1189f24210a927dcf0a153c3fe5c26733217`,
   manifest sha256 `5db2410b…`, schema `batch26-loss52-increments-manifest-v1`)
   を導出。4回実行・byte一致 (1回は fetch-back した published script
   bytes からの再実行)。gates: 3-way (p1/p2/row-audit) raw独立再検証
   (node-exact・`# replay_done`・result 2・budget 15M・stones 5・
   legal/(lo,hi) 照合)、l028 WIN行のraw再検証でincrement不採用
   (unadopted_win_ids == ["l028"])、full_packet_eq_loss_only false /
   win_scenario_exists true、52キーのBASE cache不在・quarantine 0。
2. sha-pinned fail-closed union merger (`scripts/s5_union_merge.py`
   sha256 `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`,
   byte-copy pin, WIN/LOSS conflict検出時の出力拒否gate込み・selftest PASS)
   で採用前 canonical cache 6,235行 (sha256
   `f6649fe36425f9a4e959b058392746b73e655cda0fcfa223befafd8905d67d26`,
   Part BI 採用正本・read-only不変) に increment を mergeし、**canonical
   cache 6,287行** (WIN 158 / LOSS 6,129, conflict 0, duplicates 0,
   sha256
   `e32a2e442e77799ea36194f675baeb2424f3410a1d3e681b4c4fbb389f66fe93`,
   259,260 bytes) を新path
   `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-plus-batch14residualloss10-plus-batch20loss53-plus-batch26loss52-20261123.cache`
   に出力。4回実行、merge-audit run1/run2/run3 byte一致 (3ファイルとも
   sha256 `faf6439ba8be23b530c17c93ebab1b69d3c6a3685df0c22346f5ec3810e80143`)。
   BASE行はbyte不変・採用行は追加のみ。
3. refresh (`reaudit/scripts/refresh_adoption_1849.py`, sha256
   `cf67ace759b7a23b8b0807cdd5649f0951b4cbda312f8dbdec427a7b11552c4a`,
   published Part BC refresh `2f77a8bb…` byte-copy の batch-26 adapt・
   cache sha期待値はcache本体から機械抽出・Board `954d3a10…` / policy
   `78655e94…` / quarantine `81d23160…`) で採用後の class status /
   free境界 / per-root coverage を graph + update8 + 新cache から再計算。
   gates: class_status_counts は BASE と同一 (free_now 38 /
   excluded_now 23 / unknown 34,498 すべて不変)、Board fail-closed
   free-candidate 子境界検証 (board_verified_free 38・rejected 0)、
   class 1849 の unknown_now 53→1 で残るunknownは l028 (s5 81011) のみである
   ことの機械検証。出力: `reaudit/output/refresh-summary.json` (sha256
   `51d6bf0dd6a7d73cc2824a692cf6b086849e5f7945509b9e72c6177ce7599101`,
   worklist_total 64,754・joint greedy_union_size 38,301) /
   `reaudit/output/closure-classes.csv` (sha256
   `e54a0eb831da6ade5cb5c35281713225d50039eb42c7254c50d25ddefd28cd50`,
   807 rows: class 1849 は class_rank 2 / unknown_now 1 / first_group
   (36,40) / groups_served 2。rank 1 は class 23101 unknown_now 1 のまま) /
   `reaudit/output/per-root-coverage.csv` (sha256
   `c1cb1bf52594eb810fe17cb6e9af0fdfc2791f39f0bb7551aa30c8c608a312fd`,
   known-loss-baseline + 19 central roots・全行BASE一致で改善のみ)。
   5回実行・byte一致。
4. delta extractor (`scripts/compare_deltas_batch26_adoption.py`, sha256
   `39606c48683c9d9c21a6593b78aae27ef805449c4589095bbdbe99639c9576f5`,
   published Part BI版 `92d83671…` の adapt) が BASE reaudit 3出力
   (Part BI: refresh-summary `d9d18fc2…` / closure-classes `d57a7609…` /
   per-root-coverage `bc409e63…`) と採用後3出力の差分を機械検査して
   `output/decomp-deltas-batch26-adoption.json` (sha256
   `33a540c392aec39e87f16e19eedb986338d8eac5b16dafd716275cb22b7fe986`,
   schema `n11-batch26-adoption-decomp-deltas-v1`) を生成。再計算gate:
   class statuses・known-universe counts・per-root free coverage を
   graph + update8 + cache から再計算し BASE/採用後両出力と一致を確認後
   にdeltaを出す。delta: verdict flips 空 / newly-free class 0 /
   newly_free_thirds 空 / class 1849 の BASE-unknown 53子 ==
   batch-26 key集合で52行解決・leftover == [81011] == l028 /
   closure候補表 ranking churn: class 1849 rank 24→2、worklist
   best-option churn のみ (left [5213, 18933], entered [1349, 1906],
   各churned classのstatusは不変) / metrics: joint_greedy_union_size
   38,415→38,301 (delta -114)・probe_worklist_total 64,808→64,754
   (delta -54)・unknown_classes 34,498 不変・update8 newly_resolved 0。
   4回実行・byte一致 (1回は published script bytes からの再実行)。
5. 防御: tamper battery **14/14 PASS** (maker 5種・refresh 2種・
   extractor 4種の改竄入力を全検出+復元byte一致・検出後 kit 204/204
   再検証、control 3件は正しく非検出) に加え、出版後に fetch-back した
   published script bytes 4/4 から全pipeline (maker → merger → refresh →
   extractor) を再実行し、全出力が出版前と byte 一致
   (maker 4回目 / merger 4回目 / refresh 5回目 / extractor 4回目)。

本採用がcanonical上で変化させるのは「batch-26 の52 LOSS行が canonical
cache 上 LOSS と計上された」ことのみである。l028 を含む class 1849 は
1個のunknown費用子 (s5 81011) を残したまま **UNKNOWN** のまま残る
(28 unconsumed closure WIN候補の消費は本Partではゼロ)。

**UNKNOWN担保**: 標準11x11空盤・19 central-reply roots・二石root {59,60}・
S2 {59,60}・class 1/2/4・class 1849 (53キーすべて、l028・52 LOSS行を含む)
は、本実験のどの時点でも **UNKNOWN** のままである。nodes数・worklist数・
greedy union size 等のscheduling quantities (簿記量) を勝敗・距離として
読んではならない。

ファイル (explicit enumeration。MANIFEST-sha256.txt 参照):
`scripts/` 3ファイル (maker / merger byte-copy / extractor)、
`reaudit/scripts/refresh_adoption_1849.py`、`output/` 7ファイル
(increment・increments-manifest・merge-audit×3・decomp-deltas・merged
canonical cache)、`reaudit/output/` 3ファイル (refresh-summary・
closure-classes・per-root-coverage)。`reaudit/output/probe-worklist.csv`
(sha256 `9ae1ca50fa23d7d292314a2e42c8f85732c94d271a854f8154127caef6b103c4`・
sha記録のみ) と `reaudit/scripts/preflight_refresh_12457.py`、runlogs は
意図的に本dirから出さない (Part AU/BC 慣例: no globs, no recursion)。

不接触: batch-27 (Part BR・並走) の drive outputs、batch 1..25 各dir・
各residual packet・fast lane (y18..y21)・inversive-arc lane・finite-field
lane・既存reaudit dirs、BASE canonical cache `f6649fe3…` (read-only不変)
のいずれにも書き込んでいない。

Part BU publication series (このREADMEが最終成果物): `b299f42` (declaration
note amendment) → `33f942a` (A: 実験コード4ファイル) → `694c816` (B1:
increment + manifest + merge-audit×3) → `8dc3bd64` (B2: decomp-deltas +
reaudit 3出力) → `8f3e487` (C: merged canonical cache 259,260 bytes) →
本commit (D: README + MANIFEST-sha256.txt)。各commitとも fetch-back
byte検証済み。
