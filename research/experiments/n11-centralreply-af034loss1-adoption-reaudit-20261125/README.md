# n11-centralreply-af034loss1-adoption-reaudit-20261125 (Part EE)

Part EE (2026-11-25): Part ED af034 60M re-probe packet
(class 34908 の batch-33 EXHAUSTED 最後残キー af034; 予算条件 ladder
15M (b33) EXHAUSTED → 30M (Part EA) EXHAUSTED → 60M (Part ED)
resolved exact LOSS) の **fresh LOSS行 1行のみ (af034)** を canonical
exact-S5 chain cache に採用 (loss-only adoption) した接続coreの
出版物である。**probe-level WIN行は本 Part では 1行も対象外**
(class 34908 の 6不消費WIN子 {af029, af047, af050, af053, af023,
af048} は引き続き scrutiny owner C++ 第二実装 gate pin
`9193f5b6…` 専権・全て不消費のまま)。

**11x11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
本dirのどの行も root verdict を主張しない。nodes は bookkeeping。**

## 構成 (接続core・wave B/C まで出版済み)

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

## reaudit (wave F・事前登録・未実行)

接続coreの出版に先立ち、reaudit (refresh fork
`reaudit/scripts/refresh_adoption_ee.py` = EC `73186e63…` の fork・
CACHE pin `fc3e4ac9…` のみ変更 + delta extractor
`scripts/compare_deltas_ee_adoption.py` = EC extractor `548068c6…`
の fork) と reaudit outputs (refresh-summary / closure-classes /
per-root-coverage / worklist regen pin検証 / decomp-deltas) は
** Part EE 宣言 (2026-11-25) の wave F として事前登録済みで、本
commit 時点では未実行・未出版** である。よって本 README の時点では
class 34908 の unknown 子数変化 (予想 7→6)・closure表・coverage の
機械導出はまだ行われておらず、このdirの出版物は verdict 1行の
canonical化までを主張する。

## 解釈ガード

- af034 は 15M / 30M では EXHAUSTED (honest UNKNOWN)、60M で初めて
  exact LOSS に解決 (各 rung は個別宣言済み Part・同一条件の再
  re-probe は行っていない)
- probe-level WIN行は本 Part では 1行も消費しない。既存の不消費WIN
  (b36 {d008, d009, d021, d026, d029}・b37 e042・b4 e002・
  af023 / af048 / af029 / af047 / af050 / af053) も引き続き全て
  不消費
- loss-only adoption は class を free化も excluded化もしない
  (class 34908 は 6不消費WIN子が残るため unknown のまま)
- nodes は bookkeeping・pn/dn ではない・solved数は勝敗ではない
- 11×11 は UNKNOWN のまま。root verdict・coverage claim は本dirの
  どこにも無い
