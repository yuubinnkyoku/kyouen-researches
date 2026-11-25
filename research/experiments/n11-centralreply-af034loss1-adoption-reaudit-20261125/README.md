# n11-centralreply-af034loss1-adoption-reaudit-20261125 (Part EE)

Part EE (2026-11-25): Part ED af034 60M re-probe packet
(class 34908 の batch-33 EXHAUSTED 最後残キー af034; 予算条件 ladder
15M (b33) EXHAUSTED → 30M (Part EA) EXHAUSTED → 60M (Part ED)
resolved exact LOSS) の **fresh LOSS行 1行のみ (af034)** を canonical
exact-S5 chain cache に採用 (loss-only adoption) した接続coreと、
その reaudit (wave F) の出版物である。**probe-level WIN行は本
Part では 1行も対象外** (class 34908 の 6不消費WIN子 {af029, af047,
af050, af053, af023, af048} は引き続き scrutiny owner C++ 第二実装 gate pin
`9193f5b6…` 専権・全て不消費のまま)。

**11x11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
本dirのどの行も root verdict を主張しない。nodes は bookkeeping。**

## 構成 (接続core: waves A〜E 出版済み・reaudit: wave F 出版済み)

- `scripts/make_increments_ee_adoption.py` maker (sha
  `772c3c45e5d306089aa83fe05dea59571609ebb380ae56b7af20587acd156c5f`)
  - BASE = Part EC canonical cache `cecc1a0f…` 6,665行 (WIN 158 /
    LOSS 6,507) pin・pinned merger `90711961…` pin・quarantine pin
  - ED kit
    `research/experiments/n11-centralreply-closure-class34908-af034-reprobe60m-20261125/`
    (MANIFEST rev2 `1dfe02ca…` 36 files) file-by-file sha検証・
    jsreplay `84585617…`/60M runner `b0c5f714…`/ED status `26a97e02…`
    (5行)/audit_ed `5473eafb…` (58 gates) pin・input csv 4行 pin
    (af034 `a4bff566…`・af001 `b2ef3588…`・af029 `b5500b8d…`・
    af039 `e51a3c9d…`)
  - 採用キーの two-pass fresh-cold raw 再検証 (node-exact @60M:
    af034 32,012,059 = 採用 == packet全体・p1 176 s / p2 180 s)・
    base不在・quarantine不在 (fresh-increment gate)・
    15M/30M EXHAUSTED source raws pin (ladder: b33-status
    `1f663fc8…` 66行 pair + ea-status `db7c7017…` 13行 pair +
    exh30m raws `9ecfdc77…`/`3978990d…`)・anchors af001/af039 は
    BASE canonical行 verbatim 再現・af029 は BASE不在 (不消費WIN)
  - tamper battery: 3/3 ABORT fail-closed (T1 maker pin改変 / T2 raw
    verdict bit 反転 / T3 status nodes改変・いずれも出力なし)
- `scripts/s5_union_merge.py` pinned merger byte-clone (sha `90711961…`・
  selftest PASS・3回merge同一sha)
- `output/increment-af034loss1-20261125.cache` (sha `cc9c4746…`・1行
  `s5verdict,1152921504607911937,68719476736,5,2,32012059`・1,597B)
- `output/increments-manifest.json` (sha `0ad3469e…`・schema
  af034loss1-increments-manifest-v1・pool af034loss1のみ・
  full_packet_eq_loss_only=true・win_scenario_exists=false・
  adopted_table_digest `aab6262a…`)
- `output/merge-audit-run{1,2,3}.json` (3回とも sha `05381cea…`・
  unique 6,666・WIN 158 / LOSS 6,508・dup_elided 0)
- `output/merged-exact-s5-chain-plus-af034loss1-20261125.cache`
  (sha `fc3e4ac9…`・**6,666行・WIN 158 / LOSS 6,508**・277,578B)

merged cache名は短縮形式 (従来の BASE名+`-plus-…` 命名は 260B超で
merger `.tmp` 書き出しが filesystem 255B 制限に抵触するため・実測
Errno 36)。完全な BASE (EC) cache名 (243B) とsha `cecc1a0f…` は
maker・merge-audit・宣言が保持する。検証性は sha照合で完全に保たれる。

## reaudit (wave F・実行・出版済み・2026-11-25)

Part EE 宣言 (wave A) で事前登録された wave F を実行・出版した。
clean-room 検証: reaudit outputs を全削除 → refresh fork 再実行 →
byte同一 → extractor 再実行 → decomp byte同一。BASE (EC) 側は EC
refresh fork `73186e63…` を scratch 再実行で再検証 (EC summary
`936373e6…`・closure `0ae9749c…`・prc `06cd6561…`・worklist regen
`36bc6c6c…`・BASE cache `cecc1a0f…` 6,665行・byte同一)。

- `reaudit/scripts/refresh_adoption_ee.py` (sha256 `01937f23…`): EC
  refresh fork からの fork。変更は docstring + CACHE pin
  (`fc3e4ac9…` 6,666行へ) のみ
- `scripts/compare_deltas_ee_adoption.py` (sha256 `7660b441…`): EC
  extractor `548068c6…` の fork。af034loss1 manifest schema
  (row_counts.prior_adopted_loss_rows_base・batch
  whole_packet_nodes 32,012,059・origin_budget_15m 15,000,000・
  source_budget_30m 30,000,000・kit_integrity EA 61 + ED 36 file
  pins) に全面適応・fail-closed gate 全維持
- `reaudit/output/refresh-summary.json` (sha256 `6af660a1…`)
- `reaudit/output/closure-classes.csv` (sha256 `27e00b0d…`・807行)
- `reaudit/output/per-root-coverage.csv` (sha256 `6974299b…`)
- `reaudit/output/probe-worklist.csv` は**出版しない** (3,724,115B・
  size policy)。regen pin sha256 `b4933810…` を MANIFEST ヘッダに
  記載する (published refresh fork + cache pin `fc3e4ac9…` から
  誰でも再生成して sha256 照合できる・本 wave の clean-room 再実行で
  byte同一を確認済み)
- `output/decomp-deltas-af034loss1-adoption.json` (sha256
  `614bbda0…`・schema af034loss1-adoption-decomp-deltas-v1)

### wave F 機械導出の確定値 (wave E の予想を実証・全て extractor が fail-closed 検証)

- **class 34908**: unknown 7→6・rank 8→7・groups_served 5 static・
  base_known_loss_children 49→50 (adopted_own 1)・**NOT freed・NOT
  excluded**。残 6子は全て不消費 probe-level WIN {af029 (s5
  900646), af047 (961976), af050 (962386), af053 (962470), af023
  (810351), af048 (962172)}。scrutiny owner C++ 第二実装 gate pin
  `9193f5b6…` 専権のまま
- class 16371: 全面 byte-static (rank 4・unknown 2・groups 3・不消費
  WIN子 {e042, e002} 残存)
- class 20421: churn は class_rank のみ (7→8)。unknown 6・groups 4
  static・EE 採用 key は同class境界外 (frontier-cost bookkeeping)
- closure表: 807行全面 static。left/entered 空・unknown 変化 class
  は 34908 以外ゼロ・rank churn は 20421 のみ (fully_stable 805。
  extractor は 34908 を専権セクションで検証)
- frozen update8: 完全 byte-static (採用 s5 930660 は凍結 baseline
  要求の外側・resolved 259 / remaining 31,600 / groups_free_now
  131・newly_resolved []・win_hit_groups [])
- metrics (bookkeeping・決して verdict ではない): joint greedy union
  36,509→36,508・worklist 64,415→64,414・known_universe 844→845・
  cache_in_universe 821→822・root0 greedy 3004→3003・root12 greedy
  2891→2890 (free/uncovered は全 root 同一)・root27 119/119
- class_status: excluded 390 / excluded_now 23 / free_now 39 /
  unknown 34,497 (before/after 同一・static)・board 検証 free
  候補 39/39・reject 0

### 次 probe 候補 (2026-11-25 補遺で訂正)

worklist regen (`b4933810…`) と published closure-class batch packets
(41 dirs・batch input keys 1,717 unique s5 + 各 family status.log) を
機械 cross-join した結果: **closure rank 1-10 の全 class (23101/1849/
2251/16371/16757/5804/34908/20421/34269/5343) の残 unknown 計 81子は
全て過去 packet 済み (fresh 0) かつ全て probe-level WIN-labeled
(unconsumed・scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 待ち)**。
class 5343 の 11 EXHAUSTED@15M 行も Part CQ (20M: 7 WIN) → Part CS
(25M: 3 WIN) → Part CT (30M: aa050 WIN) の budget ladder で解決済み。
34269 の 11 残子は batch-30 WIN-HALT 行・5804 の 4 残子は batch-31 WIN
行 (ad024/ad028/ad043@30M (Part DI)/ad055)。よって本 README 初版の
「class 5804 を筆頭とする次 probe 候補」提示は取り下げる (top-10 には
fresh・still-EXHAUSTED とも存在しない)。

次 Part の実行可能選択肢: (a) scrutiny gate 通過後の WIN 行採用 Part
(C++ 環境専権)・(b) fresh キーを持つ最上位 class からの新規 batch
probe。機械抽出基準では fresh 最上位は rank 12 class 30345 (unknown
50・fresh 49) (以後 rank 20 class 30484 (52 fresh)・rank 22 class
23964 (51) が続く)。抽出は closure-class batch 41 dirs 基準で・旧
night/terminal 系 batch は未照合。最終選定は次 Part の宣言が
fail-closed maker で行う (本dirは候補抽出結果のみを出版)。

## 解釈ガード

- af034 は 15M / 30M では EXHAUSTED (honest UNKNOWN)、60M で初めて
  exact LOSS に解決 (各 rung は個別宣言済み Part・同一条件の再
  re-probe は行っていない)
- probe-level WIN行は本 Part では 1行も消費しない。既存の不消費WIN
  (b36 {d008, d009, d021, d026, d029}・b37 e042・b4 e002・
  af023 / af048 / af029 / af047 / af050 / af053) も引き続き全て
  不消費
- loss-only adoption は class を free化も excluded化もしない
  (class 34908 は 6不消費WIN子が残るため unknown のまま・reaudit
  の機械導出で確定)
- nodes は bookkeeping・pn/dn ではない・solved数は勝敗ではない
- closure表・worklist・greedy union・候補 class の列挙はいずれも
  bookkeeping であり、verdict・coverage 主張ではない
- **11×11 は UNKNOWN のまま。root verdict・coverage claim は本dirの
  どこにも無い**
