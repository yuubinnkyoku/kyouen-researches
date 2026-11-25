# Part EE 宣言: af034loss1 (af034 60M解決 1 LOSS行) の canonical adoption - 接続core (2026-11-25)

単一オーナー宣言。observed HEAD `67b87d26` (K1315 workflow revision・
2026-11-25T05:32:12Z)。Part文字は「EE」を採用 (af034loss1 の
commit message 機械走査 total_count=0。ram名・実験dirとも未使用)。
本宣言は EE の最初の出版物 (wave A)。

## 対象と目的

Part ED は class 34908 の batch-33 EXHAUSTED 残キー af034
(lo/hi 1152921504607911937 / 68719476736・s5 930660・legal 95・
membership_class_count 4) を、事前宣言済み予算条件 **60,000,000**
(出版済み30M EXHAUSTED 条件からの budget-condition upgrade) で
re-probe し (kit `research/experiments/n11-centralreply-closure-class34908-af034-reprobe60m-20261125/`・
36 files MANIFEST rev2 `1dfe02ca…`)、**fresh exact LOSS (result=2, nodes
32,012,059, two-pass fresh-cold node-exact, p1 176 s / p2 180 s)** に
解決した (status.log 5行 honest history・audit_ed.json 58/58 gates PASS・
val-gate 4/4・anchors af001/af029/af039 3/3・verdict は ED 時点では
不消費)。よって Part EE として、この **fresh LOSS行 1行のみ** を
pinned fail-closed union merger (CU byte-clone pin `9071196100…`・
selftest PASS・merge-audit 3回同一sha) で canonical merged cache に
採用する。予算条件の推移は honestly な ladder 15M (b33 EXHAUSTED) →
30M (Part EA EXHAUSTED) → 60M (Part ED resolved exact LOSS) であり、
各 rung は個別の宣言済み Part である (同一条件の再 re-probe は
行っていない)。probe-level WIN行は本 Part では 1行も対象外
(class 34908 の 6不消費WIN子 {af029, af047, af050, af053, af023, af048}
は引き続き scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 専権・
全て不消費のまま)。

- BASE = Part EC canonical merged cache・6,665行 sha256
  `cecc1a0fae126d98d8e5f23e041657b86e4d7128f80cc1182f4f9830ed1e8626`
  (WIN 158 / LOSS 6,507・EC 出版byteを改変せずそのまま pin)
- ADOPTED-CANONICAL = BASE + 1行 = 6,666行 (WIN 158 / LOSS 6,508)
  merged cache名 = **`merged-exact-s5-chain-plus-af034loss1-20261125.cache`**
  sha256 `fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f`
  (277,578 bytes)

命名に関する注意 (正直な記録): 従来の chain 命名 (BASE名 + `-plus-…`)
を踏襲すると260バイトを超え、merger 内部の `.tmp` 付き書き出しパスが
255バイトの filesystem component-name 制限を超えて fail する (Errno 36・
実測)。EE merged cache名は短縮形式 `merged-exact-s5-chain-plus-af034loss1-20261125.cache`
(46 bytes) とし、完全な BASE (EC) cache名とshaは maker・merge-audit・
本宣言・README が byte-pin で保持する。検証性は名前而非pin (sha照合) で
完全に保たれる。

1採用行:

| key | lo / hi | legal | s5 | result | nodes @60M |
|---|---|---|---|---|---|
| af034 | 1152921504607911937 / 68719476736 | 95 | 930660 | 2 (LOSS) | 32,012,059 |

本 Part の packet は ED kit の probing packet と同一 (1キーのみ・
loss-only)。**full packet == 採用行** (probe-level WIN行ゼロ・
still-EXHAUSTED行ゼロ・win_scenario_exists=false・
full_packet_eq_loss_only=true)。nodes は bookkeeping であり勝敗主張ではない。

## class 境界 (期待値; reaudit refresh + extractor が fail-closed 機械導出)

- class 34908: EC 時点で unknown 子 7 (6不消費WIN {af029 s5 900646,
  af047 961976, af050 962386, af053 962470, af023 810351, af048 962172}
  + 1 still-EXHAUSTED af034 s5 930660)。af034 の 60M exact-LOSS 解決により
  **unknown 子は 7→6 予想** (残る6子は全て不消費WIN)。**class 34908 は
  free化も excluded化もされず unknown のまま** (win行は1行も消費しない)
- class 16371 / class 20421: 本 Part の行は一本も境界内に存在しない
  予想 (closure行 byte-static)
- preaudit の機械導出・byte照合は reaudit (wave F) が担う。本宣言では
  勝敗・coverage の主張を一切しない

**11×11 空盤は UNKNOWN のまま**。nodes は bookkeeping。WIN行は
scrutiny gate を満たさない限り一切消費しない。

## 接続core の実績 (本宣言時点で local 完了・ wave B 以降で出版)

本 Part は EC の構成を fork する。maker・merger・outputs は宣言の
出版に先立ち検証環境で生成・selftest・tamper battery 完了済みであり、
出版 waved の byte-pin は下記の実測値である (ex-post である点を
正直に記録する; publish-then-execute の趣旨である「条件・pin の
事前固定」は全 byte-pin が本宣言で固定されることで担保される)。

- maker `scripts/make_increments_ee_adoption.py` sha256
  `772c3c45e5d306089aa83fe05dea59571609ebb380ae56b7af20587acd156c5f`
  (EC maker `a6a416ed…` の fork・497行相当): ED kit 36 files
  file-by-file sha検証 + af034 two-pass fresh-cold raw 再検証
  (node-exact) + anchor 3キー (af001/af039 BASE verbatim 再現・
  af029 BASE不在) + 15M/30M EXHAUSTED source raws と両status の
  honest ladder pin + BASE不在・quarantine 不在 (fresh-increment
  gate) + 全ピン fail-closed
- merger byte-clone `scripts/s5_union_merge.py` sha256
  `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`
  (EC出版byteと完全一致): selftest PASS (positive dedupe+sort・
  cross-file conflict reject・within-file conflict reject・malformed
  row reject・double-run determinism)
- increment `output/increment-af034loss1-20261125.cache` (1,597 bytes)
  sha256 `cc9c474627ec8f6fc98c0ebeb7600707021e8cd598b3be6799d39c104289e162`
  (1行: `s5verdict,1152921504607911937,68719476736,5,2,32012059`・
  header comment と合わせた byte-pin)
- manifest `output/increments-manifest.json` (5,290 bytes) sha256
  `0ad3469ede4bfbddaee21d12dbab97f7e0babdbe5cbaba8cc7a6f2f41d0d22c9`
  (schema `af034loss1-increments-manifest-v1`・pool af034loss1のみ・
  adopted_table_digest_sha256 `aab6262a8cba4ecba4d82ccb197bb08c8a50dddb72931044a17b65f2f0ecf8dc`・
  full_packet_eq_loss_only=true・win_scenario_exists=false)
- merged cache `output/merged-exact-s5-chain-plus-af034loss1-20261125.cache`
  (277,578 bytes) sha256
  `fc3e4ac9052447158202f09d5efe05468dba32fe95ec90beaaa0a0de9d2c020f`
- merge-audit 3回とも同一 sha256
  `05381cea4c65fcbcaf46d77fbdf3b1d307c41f6abeef0cc9636954e29f5cbcfd`
  (`merge-audit-run1.json` / `run2.json` / `run3.json` 各1,658 bytes・
  unique 6,666・dup_elided 0・WIN(1) 158・LOSS(2) 6,508・
  nodes_field_mismatches_recorded [])

### tamper battery (fail-closed 検証済み)

- T1 maker pin改変 (`ADOPTED_INCREMENT_SHA` を壊す) → ABORT rc=1
  出力なし
- T2 raw verdict改変 (`af034.p1.out` result 2→1) → ABORT rc=1
  (kit file sha drift で即時検出) 出力なし
- T3 status nodes改変 (`af034 PASS 60000000,2,32012060`) → ABORT rc=1
  (status.log sha drift で即時検出) 出力なし

いずれも改変なしの再実行は increment・manifest・merged・audit の
全byteを再現 (double-run determinism 確認済み)。

## wave 計画 (EE、publish順)

- wave A: 本宣言
- wave B: kit 2 scripts (maker fork + merger byte-clone) 出版 +
  fetch-back blob sha照合
- wave C: outputs 5 files (increment・increments-manifest・merged cache
  (277,578B)・merge-audit-run1-3) 出版 + fetch-back 照合
- wave D: EE README.md + MANIFEST-sha256 出版
- wave E: Part EE 接続core 完了log (adoption 完了・reaudit pending
  を明記)
- **wave F (reaudit・事前登録)**: refresh fork
  (`reaudit/scripts/refresh_adoption_ee.py`・EC `73186e63…` の fork・
  CACHE path・CACHE pin `fc3e4ac9…` のみ変更) + delta extractor
  (`scripts/compare_deltas_ee_adoption.py`・EC extractor
  `548068c6…` の fork) + ED kit pins (36 files・MANIFEST rev2
  `1dfe02ca…`・status 5行 `26a97e02…`・audit_ed `5473eafb…`・
  60M runner `b0c5f714…`・jsreplay `84585617…`・exh30m raws
  `9ecfdc77…`/`3978990d…`)・closure-classes (class 34908 unknown
  7→6 の機械導出)・per-root-coverage・worklist regen pin
  (`36bc6c6c…` 再検証)・refresh-summary・decomp-deltas の再実行・
  byte-pin・出版。**実行時間の制約により本 run では wave F を実行
  せず、次回以降の実行に回す** (正直な分割)

## ED (出版済み) pin 一覧 (EE の依存 byte)

- ED kit MANIFEST rev2 `1dfe02ca…` (36 files: kit 21 + outputs 15)
- af034 raw `63860f94341477e7…` (p1) / `eb64725fa72a2ca6…` (p2)・
  exh30m source raws `9ecfdc77…` / `3978990d…`
- ED status.log `26a97e02…` (5行)・audit_ed.json `5473eafb…`
  (58/58 gates PASS・verdict_consumed=false)
- input csv: af034 `a4bff566…`・af001 `b2ef3588…`・af029 `b5500b8d…`・
  af039 `e51a3c9d…`
- b33-status `1f663fc8…` (66行・af034 15M EXH pair)・
  ea-status `db7c7017…` (13行・af034 30M EXH pair)
- 60M runner `b0c5f714…`・jsreplay `84585617…`
- ED 完了log (wave E・`a094f29f`) 他 ED 出版物は ED MANIFEST rev2 に準拠

## 制約・誠実性

- 11×11 空盤: **UNKNOWN** (不变)
- 本 Part は verdict 1行の消費のみを行う。class 境界・coverage の
  数値更新は reaudit (wave F) の機械導出を待つ
- nodes は bookkeeping・pn/dn ではない・solved数は勝敗ではない
- EXHAUSTED は honest UNKNOWN であり、より高い予算の re-probe には
  新規宣言が必要 (af034 は 60M で解決済み・以後同キーの re-probe 不要)
- hourly 並走があるため、各 wave の push前に最新 main を取り直し、
  競合時は無理せず次回へ回す
