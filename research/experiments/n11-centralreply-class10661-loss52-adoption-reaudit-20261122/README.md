# n11 central-reply batch-17 (class 10661) 52-LOSS canonical adoption reaudit (Part AV, 2026-11-22)

単一オーナーとして、Part AV宣言 (note Part AV amendment, commit `340abef3`,
observed HEAD-before-push `4741a92f`) を、takeover基準時刻 (~23:00Z・AYレーンと
共有) を過ぎても本実験dirがmainに現れなかったことを受けて**takeover**
(note Part AV takeover amendment, commit `d3ef2dc6`, observed
HEAD-before-push `432664f7`; scopeは宣言`340abef3`から不変・所有権移転のみ)
した本hostが実行した、batch-17 (class 10661) の52 LOSS行をcanonical
exact-S5 verdict cacheへ計上する採用・再監査実験。

Part AU (batch-17 完走: 52探査キー全部が2-pass node-exactで解決、
52 LOSS / **WIN 0** / 枯損 0 / 不一致 0・clean全LOSSバッチ5個目)
の直接後続。Part AP (batch-16) / Part AS (batch-14) と同一の採用形式だが、
**full == loss**: batch-17にはWIN行も枯損行も1行も存在しないため
(「不在のgate」として機械検証)、採用パケットがそのまま完全解決パケット
であることがmanifest上機械表明される (すべて機械表明・機械検査):

1. increments maker (`scripts/make_increments_batch17.py` = published
   Part AS maker `b6094f0b...` のbatch-17 adapt・宣言文言どおり
   row-audit 52行一致gateを新規搭載) をpublished batch-17 raws
   (publication commit `ffc09de1` + hygiene `4741a92f`) から再実行し、
   52 LOSS行 increment (sha256
   `afcdad5b9fa864d076e6998c12dc4ff1fdf69c110a2cf1495af2b3a96c3c4d52`,
   manifest sha256 `e1d430a4...`, schema `batch17-loss52-increments-manifest-v1`)
   を導出。3回実行・byte一致。gates: 3-way (p1/p2/status.log) node-exact +
   `# replay_done` 完了ガード、batch-keys (sha256 `db762175...`)
   legal/(lo,hi) 照合、published row-audit.json (sha256 `c19e768f...`)
   52行一致 (result 2・budget 15M・node_exact・nodes==pass2_nodes==raw・
   legal/(lo,hi)/s5_index/probe_order) + 全体像 (class 10661・batch 17・
   probed 52・results loss 52 / win 0 / exhausted 0 / mismatch 0・
   two_pass_node_exact 52・総ノード196,536,452/pass・host-event断片5件
   verdict行なし・fresh-cold再実行)、status.logの実行記録
   「EXECUTION-COMPLETE: 52/52 probed = 52 LOSS」に基づくWIN不在・
   枯損不在・dated stop行不在gate、52キーのBASE cache不在 (0 hits)・
   quarantine 0。
2. sha-pinned fail-closed union merger (`90711961...`, byte-copy pin,
   selftest PASS) で採用前canonical cache 6,120行 (`be9cb24e...`,
   Part AS正本) にincrementをmergeし、**canonical cache 6,172行**
   (WIN 158 / LOSS 6,014, conflict 0, duplicates 0, sha256
   `a554081156e2c2f940ecf2cc3c7af082dde6b760d6019e0a5113c4ddd5e12a3a`,
   253,898 bytes) を新path
   `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-20261122.cache`
   に出版 (本repoの次のcanonical exact-S5 verdict cache)。merge 3回実行・
   byte一致・merge-audit 3回byte一致 (sha256 `faf504ab...`)。
   merge後のBASE 6,120行cacheはbyte不変を再検証。
3. Part AS refresh機 (`5992738d...`) のadapt (docstring文言 + canonical
   cache path + cache sha期待値 = cache自体から機械抽出した
   `a5540811...` の3ハンク) = `reaudit/scripts/refresh_adoption_10661.py`
   を2回直列実行 (~62-66s/回)。4出力ともrun間byte一致:
   refresh-summary `a0043c76...`, closure-classes `e60c1088...`,
   per-root-coverage `4c7ec5d7...`, probe-worklist `667dc815...`
   (3.7MB, Part AH/AO/AP/AS先例どおり不出版・sha記録のみ)。
4. delta extractor `scripts/compare_deltas_batch17_adoption.py` (Part AS版
   `9e885ae0...` のbatch-17 adapt: 52キー全件の独立2-pass raw再検証
   (makerを信用しない第二の行検証)・WIN不在gate・full==loss機械表明・
   scenario closure/prcのsha pin追加・class 10661のfree化を要求する
   方向のgate反転・closure表churnは記録量に格下げ) を3回実行・
   byte一致 (sha256 `7d93613b...`)・全gate PASS。

## 結果: class 10661が37番目のBoard検証free classになる (閉包ではなく分類の前進)

- canonical分類: excluded 390 / excluded_now 23 / **free_now 36 → 37** /
  unknown **34,500 → 34,499**。遷移台帳 (機械gate): unknown->free_now 1
  (class 10661のみ)・free_now->free_now 36・unknown->unknown 34,499・
  excluded/excluded_now 不変。excluded_now flip 0 (zero-WIN採用では
  flipは起きえない: gate)・新規free == 計算期待 == {10661} (二方向gate)。
- **class 10661**: BASE-unknown費用子52個がbatch-17キー集合と機械一致し
  (gate)・increment52行で**全て**解決・scenario-unknown 52 → **0**。
  Board fail-closed child verification (子境界の独立整数幾何再生成・
  全子がcache上exact LOSS) にPASSし、**37番目のBoard検証free class**
  になる。closure候補表から退出 (退出6クラス = 10661 + 台帳churn 5:
  5844, 7581, 8826, 9039, 10010 / 新規5: 6372, 7577, 9317, 9330, 10008・
  churnはbest-option選択の簿記で被覆意味なし)。class 23101は
  unknown 11のままrank 1 (本採用は非接触)。
- per-root被覆: **root 24 (central) のfree 10 → 12 / uncovered 109 → 107**
  (新規free third 2個 = third 30・90・class 10661がoption)。他18 rootの
  free/uncovered列は不変 (root 27 baseline 119/119不変)。root 24の
  individual greedy 2,785 → 2,778。
- update8: resolved 79 → **80** (新規 s5 272756・increment内・LOSS・gate)、
  remaining 31,780 → 31,779、groups_free_now 127不変・lost [] (gate)。
- 簿記量 (schedule quantities・勝敗ではない): joint greedy 36,726 →
  **35,645** (−1,081)・probe worklist 64,941 → **64,888** (−53)・
  closure候補表 809 → 808行。

## verdict消費の範囲とguards

- 本実験で消費したverdictはbatch-17の52 LOSS行のみ (fail-closed merger
  経由・zero-WIN完全パケット採用)。batch-17にWIN行は存在しない
  (不在gate・manifest `win_scenario_exists: false`)。
- **17 unconsumed closure WIN (b018/d002/e002/f017/g018/j033/h045/z003/
  n005/n006/p002/p003/r001/r002/q042 + AY v001/v002) は不接触・不変**。
  WIN行の採用は引き続きscrutiny ownerのC++第二実装ゲート
  (`cpp/solvers/kyouen_dfpn_root.cpp` pin `9193f5b6...`) 待ち。
- fail-closed改ざんテスト8種全捕捉・復元byte一致: maker (raw 2-pass
  ノード改ざん / row-audit sha pin / status.log PASS行不整合) および
  extractor (increment sha pin / manifest row_counts gate / scenario
  cache sha pin / batch-keys sha pin)。入力ミラー (batch-17 177ファイル・
  Part AS 15ファイル) はテスト後全file sha再検証 0 bad。
- **標準11×11空盤・19 central-reply roots・class 10661以外の全class・
  未知の全S5子は本Partのどの時点でもUNKNOWNのまま。本実験の確定は
  canonical cache上の分類 (class 10661のfree化とroot 24の第三手2個
  free化) のみ。nodes数・worklist数・greedy数を勝敗として読まない。**

## ファイル

- `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-plus-batch16loss52-plus-batch14loss41-plus-batch17loss52-20261122.cache`
  — 新canonical verdict cache (6,172行・単一コミット出版)。
- `output/increment-batch17-loss52-20261122.cache` — 採用52 LOSS行
  increment (新bytes、本场で出版)。
- `output/increments-manifest.json` — 採用manifest
  (`batch17-loss52-increments-manifest-v1`, full==loss機械表明)。
- `output/merge-audit-run1.json` / `run2.json` / `run3.json` —
  canonical merge監査 (3回byte一致, sha256 `faf504ab...`)。
- `output/decomp-deltas-batch17-adoption.json` — 採用deltaの全gate機械証明
  (sha256 `7d93613b...`)。
- `reaudit/output/{refresh-summary.json, closure-classes.csv, per-root-coverage.csv}`
  — 採用後refresh正本 (summary sha256 `a0043c76...`・2回byte一致)。
- `reaudit/scripts/refresh_adoption_10661.py` — refresh機 (adapt版,
  sha256 `1b49cc07...`)。
- `scripts/{make_increments_batch17.py, s5_union_merge.py,
  compare_deltas_batch17_adoption.py}` — 本実験の機材 (mergerは
  published bytesのbyte-copy pin, maker/extractorはadapt版)。
- 不出版 (sha記録のみ): probe-worklist.csv (3.7MB, `667dc815...`) は
  Part AH/AO/AP/AS先例どおり不出版。実行log群 (merge-run*.log,
  reaudit runlogs, extractor実行log) は採用dir内部の作業記録
  (MANIFEST対象外)。
