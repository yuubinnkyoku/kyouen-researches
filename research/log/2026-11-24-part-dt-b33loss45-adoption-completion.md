# Part DT 完了: batch-33 (class 34908) 45-LOSS canonical adoption 完了log (2026-11-24)

単一オーナー Part DT。宣言
`research/log/2026-11-24-part-dt-b33loss45-adoption-declaration.md`
(observed HEAD `ff3e99c1` = W_24 s-spectrum lane commit・2026-11-24T19:07:16Z
時点)。commit message 機械走査で「b33loss45」「Part DT」とも total_count=0
で宣言時点で未使用の Part 文字。**11×11 空盤は UNKNOWN のまま**
(本 Part で消費した verdict は45 exact LOSS行のみ・4 WIN行と
5 EXHAUSTED行は不消費・class 34908 は free化せず)。

## 出版物と pin (全て本セッションの実行で byte 生成・sha 確定済み)

実験dir `research/experiments/n11-centralreply-class34908-b33loss45-adoption-reaudit-20261124/`:

- scripts/make_increments_b33loss45.py
  `561dc1cce76da2ebf1e5d4346fb2fc222302f2eb403da6d0fc0d25ad1d6a49ea`
  (maker・kit MANIFEST 186 file sha検証・54行2-pass fresh-cold再検証
  (`# replay_done` both passes)・status 66行 honest-history照合
  (first/final/marker 12行pin)・raw/batch-keys (legal,lo,hi,s5,mcc) 照合・
  raw inventory 108 primary + 3 truncated sidecar (sidecar は guard なし
  retry artifact)・val-gate 4 molecule × 2 host node-exact・
  採用45キーの BASE 6,502行/quarantine `81d23160…` 不在・
  不採用9キーの BASE 不在・採用 per-pass nodes 281,411,183・
  全54 nodes 383,609,606)
- scripts/s5_union_merge.py
  `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
  (pinned merger byte-clone・変更なし)
- scripts/compare_deltas_b33loss45_adoption.py
  `70219793880c7e2797eb8f6df3a56870584b3eb4e4f8d5ee1ca8e98d2a74a598`
  (extractor・BASE DP vs SCEN DT・20 artifact sha pin・kit 186検証・
  両 refresh script scratch 再実行 byte一致・Board 56子境界再生成・
  全 delta pin 照合)
- reaudit/scripts/refresh_adoption_b33loss45.py
  `5533b3f908cff069c6d86c5b96f32c6f978fda6b7ec5e8d32a3302a344363dee`
  (DP `41bf706f…` の fork・docstring と CACHE pin `973bcd19…` のみ変更・
  graph `54f9c364…`/update8 `b658290a…`/board `954d3a10…`/policy
  `78655e94…`/quarantine pin不変)
- output/increment-b33loss45-20261124.cache
  `255d54f5757ea19d00894e1f5483ab030634ca979a9fa6ed66390eda0ad3f155`
  (45行)
- output/increments-manifest.json
  `4b0a9f0fc08dc88d9ecc7807dad3ee503c59f9cbc9a233a2b3ddb72f5bcd1c70`
  (schema b33loss45-increments-manifest-v1・mixed-packet構造はPart DN式:
  `full_packet_eq_loss_only=false`・`win_scenario_exists=true`・
  `unadopted_win_ids` [af029,af047,af050,af053]・
  `exhausted_excluded_ids` [af003,af023,af034,af039,af048]・
  status_log 全66行 pin・kit manifest pin・val-gate multi-host node-exact)
- output/merge-audit-run{1,2,3}.json
  3回とも `13c9739517d1f36f112de09c1a52009a4d6f68e37566fd3fe4dd61465711379b`
- output/merged-exact-s5-chain-plus-...-plus-b33loss45-20261124.cache
  `973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b`
  (6,547行・271,884 bytes・WIN 158 / LOSS 6,389・merge-audit×3同一sha)
- output/decomp-deltas-b33loss45-adoption.json
  `a87c1ebdfdbe2170ea5ed0176f7fcf11b3257554dab202f65aee4a9eea4b331f`
  (schema b33loss45-adoption-decomp-deltas-v1・extractor出力)
- reaudit/output/refresh-summary.json
  `38fc4e193cf08cf4efb7830a8bad3d2245bc732380f44c4ee2913e05d5644732`
- reaudit/output/closure-classes.csv
  `6cc33dd731c5d2237291552a91c3f7d60947bba875867fcab10394b533f1a68d`
  (807行・class 34908行 = rank 5/unknown 9/groups 5)
- reaudit/output/per-root-coverage.csv
  `c5a2721d60c641ead369d10184e477cd5156ba7d02561c31dcd77b7b81b6f504`
- probe-worklist.csv は体積 (~4.4MB) で非出版・regen pin
  `5881d7b3b51ef0ce780abaadaf7043c1fbcd3b258b9a261cadd2c539fb35ba61`
- README.md (本dir)・MANIFEST-sha256.txt
  `1da89591c7ed95dfa0c603ec77718801e005d945123e897a6e71beab9ea66d3f`

## 実行の経過 (publish-then-execute・単一host逐次)

1. wave A: 宣言を出版 (observed HEAD `ff3e99c1`・racing guard 走査
   「b33loss45」0件・「Part DT」0件で未使用確認済み)。
2. wave B: scripts 4 を出版 (merger byte-clone `90711961…` 含む)。
3. wave C: maker 実行 (kit 186/186 sha検証から increment/manifest 生成) →
   merger ×3 (6,547行・audit同一sha) → increment/manifest/audit/merged
   cache 出版。
4. wave D: refresh fork 実行 (reaudit 3出力 + 非出版 worklist regen) →
   extractor 実行 (両 refresh script scratch 再実行・byte一致確認・
   decomp deltas 生成) → reaudit 3出力・decomp deltas・README・
   MANIFEST-sha256 出版。
5. wave E: 本完了log 出版。

実行途中の失敗 (正直な記録・全て本セッションで解決):
- sandbox環境リセット対応で過去の fetch 済み作業tree (kr2/job1) が
  残存しているうちに kit MANIFEST-sha256.txt だけ未fetch (kit 186 file
  はあった) → published kit MANIFEST (main 上に存在・sha `f2603e3a…` 一致)
  で補填して 186/186 再検証後に wave C 実行。
- maker の PRIMARY_RE regex 生成時エスケープ扱い (`\.p[12]\.out` の
  `p` 抜け) → kit raw primary inventory gate が ABORT。修正 (raw string
  template + precompiled regex) して全 gate 再通過。
- extractor の groups_served churn pin に unknown_now 静止値 [11,11] を
  追加 (class 34269 groups 5→4 rank 5→6・unknown不変) して再通過。
- Bash の cut delimiter 指定ミスで SANITY 判定文字列化け → sha再照合で
  全出力 byte 同一を確認。

## tamper battery (sandbox stage・8項目・全て fail-closed ABORT rc=1)

- T1 kit raw byte tamper (af001.p1.out) → maker ABORT
  "kit ... file sha drift" → 復旧後 rc=0・increment sha 再現。
- T2 status.log WIN-HALT marker改変 → maker ABORT (kit MANIFEST file-sha
  gate が status.log を捕捉)。
- T3 status.log 行追加 (af055) → 同 ABORT (file-sha gate で捕捉)。
- T4 BASE cache改変 → maker ABORT "base cache sha drift"。
- T5 val-gate file欠落 → maker ABORT "val-gate file missing"。
- T6 WIN-LOSS conflict 注入 (s5verdict 135268368:536870912 verdict 1) →
  merger rc=1 "GATE FAILED: WIN/LOSS conflict ... verdict 2 vs verdict 1"・
  出力fileなし。
- T7 merged (SCEN) cache改変 (verdict 2→1) → refresh fork ABORT
  "merged cache sha256 drift"。
- T8 quarantine 注入 (採用キーを active entry 化) → maker ABORT
  "quarantine registry sha drift" (registry sha gate が先に捕捉)・
  復旧後 quarantine sha `81d23160…` 一致。
- SANITY: battery 後 全入力復旧で maker rc=0・increment
  `255d54f5…`/manifest `4b0a9f0f…`/merged `973bcd19…` 再現、
  status.log `1f663fc8…` 一致。

## 機械観測の確定値 (extractor・refresh・宣言の期待と全て一致)

- cache: 6,502→6,547行 (relation: SCEN == BASE rows + 45 increment rows
  verbatim・verdicts WIN 158 / LOSS 6,344→6,389・
  cache_rows_in_universe 658→703・known_universe 681→726)。
- class 34908: Board 56子 (2 base-known LOSS s5 {955954, 958114} + 54 batch
  keys)・unknown children 54→9 (9 = 4 unconsumed WIN + 5 EXHAUSTED)・
  rank 36→5・groups_served 4→5・free_now 39→39・unknown 34,497→34,497・
  Board 検証 39/39 rejected 0。**free化せず excluded化せず**。
- closure表: 807→807行・left=[]・entered=[]・完全 stable 775・
  rank churn 30・unknown_now 変化クラス [] (34908 以外)・
  class 34269 groups_served_count 5→4 (rank 5→6・unknown 11→11).
- update8: resolved 187→188 (新規 {962471} ⊂ 採用45)・remaining
  31,672→31,671・groups_free_now 131 静止。
- metrics: joint greedy 36,968→36,849・worklist 64,609→64,564・
  unique_groups 2,115→2,115・per-root remaining {0: -3, 12: -2}・
  per-root free/uncovered thirds 全root不変・greedy減少は
  root 0 (3,054→3,009)/1 (6,353→6,352)/12 (2,986→2,984)/13
  (6,175→6,174)・root 27 119/119 不変。

## 制約・文言規約の確認

- verdict不消費: 4 WIN行 (af029/af047/af050/af053) は scrutiny-owner C++
  第二実装 gate (pin `9193f5b6…`) 通過後に別 adoption Part のみ採用可。
  5 EXHAUSTED行 (af003/af023/af034/af039/af048) は honest UNKNOWN。
- 被覆・secured・root勝敗の主張なし。free_now は Board-derived
  scheduling bookkeeping。nodes数は bookkeeping。
- 計算資源: 単一host逐次・4並列目安以内・大規模中間fileなし
  (probe-worklist regen ~4.4MB は repo外)。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4・5343・5804・34269・34908 (WIN 4行/EXHAUSTED
  5行を含む全54キー) は全時点で UNKNOWN。**

次回レジューム候補: closure表 rank上位の small-pocket (23101/1849/2251
unknown 1・5804 残4=未消費WIN 1) の batch 選定、class 11490 (unknown 55)
batch、EXHAUSTED 5行の高budget再probe宣言、WIN 4行 scrutiny gate。

## 出版補遺 (2026-11-24, wave E 出版時点)

本log出版時の走査で「b33loss45」「Part DT」commit とも total_count=0 (単一オーナー確認済み)。
本文中の observed HEAD `ff3e99c1` は成果物生成時点のもので、出版開始直前の HEAD は
他レーンのcommitが挟まり `4905228a` に進んでいた。出版対象は全て新規path (add-only)
のため競合なし。実出版は 6 commit に分割:

- wave A: 宣言log → `06bb4f62`
- kit 1/4: README + MANIFEST-sha256 + increment cache (45行) + increments-manifest + merge-audit run1-3 + decomp-deltas + per-root-coverage → `cfe49ee2`
- kit 2/4: scripts 4本 (maker / pinned merger / comparator / refresh fork) → `c4d1b902`
- kit 3/4: reaudit outputs 2 (refresh-summary + closure-classes) → `b6c76d1a`
- kit 4/4: 正準chain merged cache (6,547行+head行 / 271,884B, byte照合で271,884=271,884 PASS) → `f771d3cb`
- wave E: 本完了log (このcommit)

sandbox メモリ制約 (run_typescript 16MiB) のため 1回のpushを 18ファイル一括から
6分割に変更した。byte検証は全ファイル decoded=utf8=expected で一致、fetch-back
照合は次回実行で実施予定。11×11 は UNKNOWN のまま不変。
