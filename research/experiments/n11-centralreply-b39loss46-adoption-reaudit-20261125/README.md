# n11-centralreply-b39loss46-adoption-reaudit-20261125 (Part EI)

Part EI (2026-11-25): Part EH batch-39 probe (closure class **30484**
rank-20 fresh-frontier・50 fresh targets・178-file kit MANIFEST
`52b69c04…`・two-pass fresh-cold node-exact @15M/order 0 MISMATCH 0) の
**honest-label exact-LOSS 46行 (aj001..aj050 から aj030/aj039 EXHAUSTED
除外・aj049/aj050 probe-level WIN 除外の46行)** を canonical exact-S5
chain cache に採用 (loss-only adoption) した接続coreと、その reaudit
の出版物である。**probe-level WIN行は本 Part では 1行も消費しない**
(scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 専権)。EXHAUSTED
2行 (aj030/aj039) は honest UNKNOWN のまま (同一条件での再 re-probe
禁止)。batch-38 の claim-reserved dual-class 2キー {ai044, ai048} は
pair level で採用対象外 (Part EF in-flight single-owner・本 Part は
一切触れていない)。

**11x11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
本dirのどの行も root verdict を主張しない。nodes は bookkeeping。**

## 構成 (publish-then-execute: waves 1a/1b/1c + 2 出版済み)

- `scripts/make_increments_ei_adoption.py` maker (sha256 `ff96435a…`)
  - BASE = Part EE canonical cache `fc3e4ac9…` 6,666行 (WIN 158 /
    LOSS 6,508) pin・pinned merger `90711961…` pin・quarantine `81d23160…`
    pin
  - batch-39 kit file-by-file byte検証 (178 files vs kit MANIFEST
    `52b69c04…`)・status.log 54行 pin `08d70bb7…`・batch-audit
    `5a2b67cb…` pin (honest-label 46/2/2/0・MISMATCH 0)・
    batch-keys `5e25b550…` pin (50 targets・claim-reserved 除外記録)
  - 100 raws (two-pass p1/p2) sha pin 再検証 (fresh-cold node-exact
    @15M・whole-packet nodes/pass 177,032,132・採用46行合計
    140,162,086)・status 54行 honest history 再構築照合・
    46採用キーの BASE 不在・quarantine 不在・prior-probe-universe
    不在 (fresh gates)・input csv 46行 byte pin
  - 採用表 digest `a7ef2336…`・emitted increment sha
    `a2b24baa…` の emit時 fail-closed pin
- `scripts/s5_union_merge.py` pinned merger byte-clone (sha
  `90711961…`・selftest PASS・本 Part で 3回 merge 同一sha)
- `output/increment-b39loss46-20261125.cache` (sha256 `a2b24baa…`・
  46行・3,310B)
- `output/increments-manifest.json` (sha256 `6ae4058b…`・schema
  b39loss46-increments-manifest-v1・pool b39loss46 のみ・
  full_packet_eq_loss_only=false・win_scenario_exists=true・
  不消費WIN/EXH/reserved の明示行)
- `output/merge-audit-run{1,2,3}.json` (3回とも sha `387010c5…`・
  unique 6,712・WIN 158 / LOSS 6,554・dup_elided 0)
- `output/merged-exact-s5-chain-plus-b39loss46-20261125.cache`
  (sha256 `73482be0…`・**6,712行・WIN 158 / LOSS 6,554**・279,805B)

## reaudit (wave 2・実行・出版済み・2026-11-25)

publish-then-execute 通り、wave 1 (1a maker+merger / 1b refresh /
1c extractor) 出版**後**に、main の tarball を clean fetch した
環境で全成果物を再生成し、宣言済み pin と byte 照合した (本
セッションでは 1a→1c push 完了後に実行環境が一度リセットされた
ため、再生成は完全な post-publication clean-room 実行になった)。
全出力 byte 同一。extractor は BASE側も in-situ に再実行して
検証した (EE refresh `01937f23…` scratch rerun + EI refresh
`1bcf1972…` scratch rerun・ともに byte-identical)。

- `reaudit/scripts/refresh_adoption_ei.py` (sha256 `1bcf1972…`):
  EE refresh fork。変更は docstring + CACHE pin (`73482be0…`
  6,712行へ) のみ。Board(11) 整数幾何の fail-closed child
  verification (free候補 39/39 verified・reject 0)
- `scripts/compare_deltas_ei_adoption.py` (sha256 `5433c4c2…`): EE
  extractor の全面適応 fork。class-30484 54-child / class-30118
  56-child Board 境界を Board(11).children で再生成し独立検証・
  fail-closed gate 全維持
- `reaudit/output/refresh-summary.json` (sha256 `414314eb…`)
- `reaudit/output/closure-classes.csv` (sha256 `e12bf328…`・807行)
- `reaudit/output/per-root-coverage.csv` (sha256 `2525f306…`)
- `reaudit/output/probe-worklist.csv` は**出版しない**
  (3,721,259B・size policy)。regen pin sha256 `98529a8d…` を
  MANIFEST ヘッダに記載 (published refresh fork + cache pin
  `73482be0…` から誰でも再生成可能・本 wave の clean-room 再実行で
  byte 同一確認済み)
- `output/decomp-deltas-b39loss46-adoption.json` (sha256
  `6b8b3e7d…`・schema b39loss46-adoption-decomp-deltas-v1)

### 機械導出の確定値 (extractor fail-closed 検証・全て bookkeeping)

- **class 30484**: unknown **52→6** (採用46)・rank **20→9**・
  groups_served 4 static・**NOT freed・NOT excluded**・残 6子 = 2
  EXHAUSTED honest UNKNOWN {aj030, aj039} + 2 不消費 probe-level WIN
  {aj049 (nodes 4,998,452), aj050 (1,871,594)} + 2 claim-reserved
  {ai044, ai048} (Part EF)。children_total_raw 54 (base known-loss
  2・receipt 0・non-s5 0)
- **class 30118**: secondary dual-class owner・unknown **54→52**
  (own adopted 2)・rank 39→21・groups_served 4 static
- class 16371 / 20421 / 34908: 全面 byte-static (採用キーは各
  Board 境界の外・left/entered 交換なし)
- closure表: 807行・fully_stable 776・rank churn 29行 (churn は
  rank 列のみ・unknown 実減は 30484/30118 のみ)・left/entered 空
- frozen update8: 完全 byte-static (採用46 s5 index は全て凍結
  baseline 要求の外側・resolved 259 / remaining 31,600 /
  groups_free_now 131・newly_resolved []・win_hit_groups [])
- class_status: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 (before/after 同一・static)・board 検証 free 候補
  39/39・reject 0
- metrics (bookkeeping・決して verdict ではない): joint greedy
  union 36,508→36,505 (unique_groups 2,115 static)・worklist
  64,414→64,366・known_universe 845→891・cache_in_universe
  822→868・root0 greedy 3,003→3,001 (free 7/7・uncovered
  112/112)・root24 greedy 2,827→2,782 (free 12/12・uncovered
  107/107)・root27 119/119・free/uncovered は全 root で同一
  (何も free 化していない)

### class 30484 の残 6子の扱い

次の実行可能選択肢: (a) scrutiny gate 通過後の WIN 行採用 Part
(C++ 環境専権・aj049/aj050)・(b) EXHAUSTED 2行の異条件 budget
ladder (同一15M条件の再 probe は禁止・事前宣言で段を設ける)・
(c) その他 fresh キーを持つ最上位 class からの新規 batch probe。
claim-reserved {ai044, ai048} は Part EF が単独完結するまで本
Part からは触れない。最終選定は次 Part の宣言が fail-closed
maker で行う。

## 解釈ガード

- 採用46行はすべて fresh (BASE 不在・prior-probe-universe 不在・
  quarantine 不在)・two-pass fresh-cold node-exact @15M の honest
  label のみ
- probe-level WIN行 (aj049/aj050) は本 Part では 1行も消費しない。
  b39 以外の既存不消費WIN も引き続き全て不消費
- EXHAUSTED 行 (aj030/aj039) は honest UNKNOWN・同一条件 (15M)
  での再 probe は行わない
- loss-only adoption は class を free化も excluded化もしない
  (class 30484 は残6子のため unknown のまま・reaudit の機械導出で
  確定)
- nodes は bookkeeping・pn/dn ではない・solved数は勝敗ではない
- closure表・worklist・greedy union・候補列挙はいずれも
  bookkeeping であり verdict・coverage 主張ではない
- **11×11 は UNKNOWN のまま。root verdict・coverage claim は本dir
  のどこにも無い**
