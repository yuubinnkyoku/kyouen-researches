# Part EE 完了: wave F (reaudit) 実行・af034loss1 adoption の機械導出確定 (2026-11-25)

単一オーナー Part EE・publish-then-execute。Part EE 宣言 (wave A
`27517867`) で事前登録されていた reaudit (wave F) を実行・出版した。
wave E 完了log (`8d417049`) の表で「次回以降の実行」としていた行を
本 wave で完結させる。標準 11×11 空盤は **UNKNOWN のまま**。

push 前の最終レースガード: observed HEAD `1a8d8953` (06:04Z・並走
K0568/GP-census lane は別dirのみ)。実験dirの `reaudit/` は本 push まで
main 上に不存在・commit 検索でも他実行の wave F 着手なしを確認。

| push | 内容 | commit |
|---|---|---|
| F1 | reaudit 6 files (refresh fork + extractor + 3 outputs + decomp)・git blob sha1 6/6 事前計算値と一致・curl raw fetch-back byte 同一 | `dcdd86c1` |
| F2 | README 改訂 (reaudit 実行済みへ) + MANIFEST rev2 (14 entries) + 本完了log | `10fbf47e` |
| F3 | 補遺 (honest 訂正): README 候補節 + 本log追記・worklist×batch packets cross-join で top-10 残 unknown 81子が全て不消費WIN行と機械確定・候補提示を取り下げ | (本 commit) |

## 出版物 (全 sha は「ファイル計算 → placeholder 置換 → 64hex 検証」で注入・手打ち sha 事故ゼロ)

| file | bytes | sha256 | git blob sha1 |
|---|---|---|---|
| `reaudit/scripts/refresh_adoption_ee.py` | 24,876 | `01937f23…` | `12e92dfe…` |
| `scripts/compare_deltas_ee_adoption.py` | 60,628 | `7660b441…` | `a9e8a299…` |
| `reaudit/output/refresh-summary.json` | 32,765 | `6af660a1…` | `7503a560…` |
| `reaudit/output/closure-classes.csv` | 35,951 | `27e00b0d…` | `502bb25d…` |
| `reaudit/output/per-root-coverage.csv` | 588 | `6974299b…` | `5b0df4e4…` |
| `output/decomp-deltas-af034loss1-adoption.json` | 7,212 | `614bbda0…` | `d0efc1e1…` |

- refresh fork = EC `73186e63…` からの fork (変更: docstring + CACHE pin
  `fc3e4ac9…` 6,666行のみ)。extractor = EC `548068c6…` からの fork
  (af034loss1 manifest schema に全面適応・fail-closed gate 全維持)。
- probe-worklist (3,724,115B) は size policy により出版しない。
  regen pin `b4933810…` を MANIFEST rev2 ヘッダに記載。published
  refresh fork + cache pin から誰でも再生成して sha256 照合できる。
- BASE (EC) 側再検証: EC fork scratch 再実行で EC summary `936373e6…`・
  closure `0ae9749c…`・prc `06cd6561…`・worklist regen `36bc6c6c…`
  byte 同一・BASE cache `cecc1a0f…` 6,665行。
- clean-room: reaudit outputs 全削除 → refresh fork 再実行 → byte 同一
  → extractor 再実行 → decomp byte 同一 (`refresh_outputs_byte_identical:
  true`・`DECOMP OK`)。

## 機械導出の確定値 (wave E の予想を実証・extractor が全て fail-closed 検証)

- **class 34908**: unknown 7→6・class_rank 8→7・groups_served 5 static・
  base_known_loss_children 49→50 (adopted_own 1・56子中 s5 universe 56・
  non-s5 0)・**NOT freed・NOT excluded**。残 6子は全て不消費
  probe-level WIN {af029 (s5 900646), af047 (961976), af050 (962386),
  af053 (962470), af023 (810351), af048 (962172)} のまま
  (scrutiny owner C++ 第二実装 gate pin `9193f5b6…` 専権)。
- class 16371: 全面 byte-static (rank 4・unknown 2・groups 3・不消費WIN子
  {e042, e002} 残存)。class 20421: churn は class_rank のみ (7→8・
  unknown 6・groups 4 static・EE 採用 key は境界外)。
- closure表: 807行全面 static・left/entered 空・groups_served 減少 0・
  rank churn は 20421 のみ (fully_stable 805)。34908 を除く unknown
  変化 class はゼロ (extractor は 34908 を専権セクションで検証・
  変化 class が空であることを fail-closed で確認)。
- frozen update8: 完全 byte-static (採用 s5 930660 は凍結 baseline
  要求の外側・resolved 259 / remaining 31,600 / groups_free_now 131・
  newly_resolved []・win_hit_groups [])。
- metrics (bookkeeping・決して verdict ではない): joint greedy union
  36,509→36,508・worklist 64,415→64,414・known_universe 844→845・
  cache_in_universe 821→822・root0 greedy 3004→3003・root12
  2891→2890 (free/uncovered は全 root 同一)・root27 (known-loss
  baseline) 119/119・class_status excluded 390 / excluded_now 23 /
  free_now 39 / unknown 34,497 static・board free 39/39・reject {}。

## 次 probe 候補 (検討用・次 Part の宣言が最終選定)

worklist regen (`b4933810…`) の機械抽出: **class 5804 (rank 6・
unknown 4)** が frontier 首位候補、次いで **class 34269 (rank 9・
unknown 11)**・**class 5343 (rank 10・unknown 46)**。class 34908 の
残 6子は全て scrutiny gate 専権のため本 lane の次 probe 対象外。
rank 1-5 (23101/1849/2251: unknown 1・16371: unknown 2・16757:
unknown 3) の残子を含む最終選定は次 Part の宣言が過去 pool 状態と
突き合わせて行う。

## 解釈ガード

- **標準 11×11 空盤は UNKNOWN。19 central-reply root も全て UNKNOWN。
  二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 も全て UNKNOWN。**
- class 34908 は 6不消費WIN子が残るため unknown のまま (NOT freed・
  NOT excluded)。勝敗・被覆の数値主張は本dirのどこにもない。
- nodes は bookkeeping・pn/dn ではない。greedy union / worklist /
  coverage 表は全て bookkeeping。
- 60M 解決 af034 の verdict 1行のみを canonical cache が消費済み。
  以後同キーの再 probe は不要。

## wave F 補遺 (2026-11-25 同日・honest 訂正)

F2 出版後に worklist regen (`b4933810…`) と published closure-class
batch packets (41 dirs・batch input keys 1,717 unique s5 + 各 family の
status.log) を機械 cross-join した結果・本 log 上記「次 probe 候補」節
と README 候補節を下記のとおり訂正する (同一 commit)。

- **closure rank 1-10 の残 unknown 計 81子は全て過去 packet 済み
  (fresh 0)**: 23101 (1) / 1849 (1) / 2251 (1) / 16371 (2) / 16757 (3) /
  5804 (4) / 34908 (6) / 20421 (6) / 34269 (11) / 5343 (46)。
- **81子すべて probe-level WIN-labeled (unconsumed・scrutiny owner
  C++ 第二実装 gate `9193f5b6…` 待ち)**。5343 の 11 EXHAUSTED@15M 行
  (aa004/aa005/aa021/aa028/aa030/aa031/aa032/aa035/aa047/aa050/aa053)
  は Part CQ (20M: aa004/aa005/aa030/aa031/aa035/aa047/aa053 の 7 WIN
  解決) → Part CS (25M: aa021/aa028/aa032 の 3 WIN) → Part CT (30M:
  aa050 WIN・nodes 25,541,199) の budget ladder で解決済み (各完了log:
  `c584e078` / `23d09513` / `30af9f49`)。34269 の 11 残子は batch-30
  の WIN-HALT 行 (ac002/ac003/ac006/ac020/ac026/ac027/ac034/ac041/
  ac045/ac048/ac054)。5804 の 4 残子は batch-31 WIN 行 (ad024/ad028/
  ad043@30M (Part DI) /ad055)。rank 1-8 の残子 (q042/l028/ab028/
  e042/e002/b018/b032/b048/d002 系/af 系) は既刊 docs の不消費WIN明記
  に拠る。
- **訂正**: 「class 5804 (rank 6・unknown 4) を筆頭とする次 probe
  候補」は取り下げる。top-10 には fresh (未 probe) キーも
  still-EXHAUSTED 行も存在しない。closure frontier の「unknown」の
  実体は不消費 WIN 行であり・closure unknown_now の減少は scrutiny
  gate 通過 + WIN 採用 Part (pinned merger `90711961…` 経由) でしか
  起こらない。
- 本補遺時点の機械抽出では・fresh キーを持つ最上位 class は **rank 12
  class 30345 (unknown 50・fresh 49)** (以後 rank 20 class 30484
  (52 fresh) / rank 22 class 23964 (51) / rank 24 class 8811 (51))。
  ただし抽出の prior-packet 対象は closure-class batch 41 dirs 基準で
  あり・旧 night/terminal 系 batch は未照合。最終選定は次 Part の宣言が
  fail-closed maker で行う。
- 本補遺はスケジューリング bookkeeping の訂正であり・verdict・coverage
  の主張はない。11×11 空盤は **UNKNOWN のまま**。
