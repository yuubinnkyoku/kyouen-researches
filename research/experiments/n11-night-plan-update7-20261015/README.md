# n11 第7次両計画更新: 162106 WIN とS6 LOSS 3件の反映

基準: main `f621b1ca`（S6/S8終局証明パッケージの独立検証push済み）。
本実験は既存実験・knowledge正本・生成物・共有solver論理・K0423・
既存出力・第1次〜第6次出力・batch1〜5出力・履歴を一切変更せず、
`research/experiments/n11-night-plan-update7-20261015/` に結果を分離保存する。
第6次出力 (`n11-night-plan-update6-20261014/output/`) は読み取り専用の基盤。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
UNKNOWNは証拠ではない。空盤 (11x11) はUNKNOWNのまま、全盤への飛躍は行わない。

## 反映した2事実

### 1. 162106 WIN (n11-night-batch5-20261014 の terminal-only receipt, trusted葉0)

| S5索引 | verdict | 探索nodes | DAG nodes / edges / 終局 | receipt | certificate SHA256 |
|---:|---|---:|---|---|---|
| 162106 | **WIN** | 18,141,378 | 2,372,823 / 3,500,917 / 352,077 | `nighta25m-162106-receipt.json` | `d996a682…` |

`trusted_leaves=0`・`pruned_roundtrip_verified`・certificate SHA256とterminal-DAG実体の一致・
`probe_manifest` との結合を再検証した。`nighta25m-162106-python-comparison.json`
(verdict / nodes / edges / terminal_nodes / trusted_leaves) がreceiptと全一致すること、
`check_trace.cpp` の実体SHA (`0f890cb4…`) がreceiptの `checker_source_sha256` と一致することをassertした。
node予算25Mの**新規run** (10M NODE_LIMIT runとは別run) によるSOLVED。
162106は本系列で6件目の新規独立WIN証拠 (既存: 209644, 126017, 197665, 206386, 131631)。

層別14件のうち `checker_source_sha256` を持つ12件（K0423 pilot 2件は別schema）と
層別外native focus 3件を含む**同一checker source SHA256** (`0f890cb4…`) を再確認した。

### 2. S6 LOSS終局証明由来の3 S5 LOSS verdict

`n11-s6-terminal-loss-20261015` の六石LOSS `00000000040004001004000004010000` 終局証明
(K0426で独立検証済み: 29 S8証人・483終局S10葉・1,028,621状態・certificate SHA `cb2e73c2…`) は
6個のS5 LOSS親を与える。本実験は親集合を独立幾何から再構成し、
うち3個が凍結第6次計画の選択S4クラス `16397` の8第三手群に現れることを再計算で確認した:

| index | S5 mask | 由来 |
|---:|---|---|
| 381840 | `00000000000000401100400040000000` | S6終局証明(certificate)から導出 |
| 402066 | `00000000040000011004000004000000` | 同上 |
| 550881 | `00000000040004001004000004000000` | 同上 |

per-index receiptは存在しない (1証明書→3verdict)。S4選択を固定したまま
要素cost義務から3件を除去し、要求S5和集合が31,774 → **31,771** (−3) となる。
「将来の計画改訂時は要再監査」に従い、親集合・計画関連3件の一致・既解決集合との非交差を
script内でassertした (`assert (parents & baseline_required) == set(s6_loss)`)。

## 二重比較表 (第6次更新と当初 K0423 の両基準)

| 指標 | 当初 (K0423) | 第2次 | 第3次 | 第4次 | 第5次 | 第6次 | 第7次 | Δ 第6次→第7次 | Δ 当初→第7次 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 上界 = 要求S5数 | 31,636 | 31,728 | 31,774 | 31,774 | 31,774 | 31,774 | **31,771** | −3 | +135 |
| 下界 = 整数dual (ceil) | 6,577 | 6,582 | 6,583 | 6,584 | 6,585 | 6,585 | **6,585** | 0 | +8 |
| 区間 | [6,577, 31,636] | [6,582, 31,728] | [6,583, 31,774] | [6,584, 31,774] | [6,585, 31,774] | [6,585, 31,774] | **[6,585, 31,771]** | — | — |
| 層別済み S5 (WIN+LOSS) | 2 (1+1) | 6 (2+4) | 10 (3+7) | 11 (4+7) | 12 (5+7) | 13 (6+7) | **17 (7+10)** | +4 | +15 |
| 除外 S4 クラス数 | 2 | 5 | 9 | 12 | 14 | 17 | **20** | +3 | +18 |
| 再選択した応答数 | 5 | 0 | 3 | 0 | 0 | 0 | **0** | 0 | −5 |
| free thirds | 122 | 122 | 122 | 122 | 122 | 122 | **122** | 0 | 0 |
| 完全S5境界を再検算した選択S4 | 349 | 350 | 351 | 351 | 351 | 351 | **351** | 0 | +2 |
| 第三手網羅 (root×third) | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | **19 × 2,261** | 0 | 0 |
| WIN側 使用可能証人pool (保存1,945) | 1,942 | 1,940 | 1,936 | 1,935 | 1,934 | 1,933 | **1,932** | −1 | −10 |
| WIN側 未閉鎖証人S5 | 1,944 | 1,846 | 1,749 | 1,748 | 1,747 | 1,746 | **1,745** | −1 | −199 |
| WIN側 closable 応手軌道 | 65 | 62 | 59 | 59 | 59 | 59 | **59** | 0 | −6 |
| WIN側 unclosable 応手軌道 | [] | [1, 2, 101] | [1, 2, 4, 15, 79, 101] | [1, 2, 4, 15, 79, 101] | [1, 2, 4, 15, 79, 101] | [1, 2, 4, 15, 79, 101] | **[1, 2, 4, 15, 79, 101]** | 0 | +6件 |
| WIN側 and-width (chosen fourths) | 7,519 | 7,165 | 6,812 | 6,812 | 6,812 | 6,812 | **6,812** | 0 | −707 |
| 新規閉鎖 第三手 / 軌道 | — | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | **0 / 0** | 0 | 0 |

## LOSS側 (§4)

- **162106 WIN**: 162106を合法S5子として持つS4クラス `[4327, 4328, 5056, 5830]` を
  全cost集合から除外。`5830` は第3次 (126017 WIN) で既に除外済みのため**新規除外は3件**
  (`4327`, `4328`, `5056`)。除外計は 17件 → **20件**。
  4クラスはいずれも第6次基準で選択されておらず (`4327`/`4328`/`5056` は過去に選択なし、
  `5830` の3応答は第3次で再選択済み)、**greedy修復は空振りで上界不変** (changed_choice_count=0)。
- **S6 LOSS 3件**: `cost[s]` から `381840 / 402066 / 550881` を除去
  (`known_loss_removed_from_cost`)。選択応答は全て維持され、要求S5和集合は
  **31,774 → 31,771 (−3)**。
- 19 root・全2,261 third手・351選択S4の完全境界を独立幾何から再検算し、
  既知WIN要求0件・既知LOSS混入0件を表明 (`verification.passed`)。
- batch と staged-forward (反映順 `(162106, 381840, 402066, 550881)`) を同一凍結入力から
  再計算し、labels / candidates / obligations / choices / union の全sha一致を確認。
- free thirds 122・完全S5境界351 は第6次から不変。

### ranking 照合 (n11-conflict-ranking-20261013 の ranking.tsv 当該行と反実仮想を独立幾何で再計算)

ranking.tsv 行 (`geometry_rank=25`):
`if_win_loss_choices_invalidated=3` / `if_win_new_free_win_branches=18` /
`if_win_greedy_loss_union=31685` / `if_win_greedy_delta=49` /
`if_loss_fixed_win_branches_uncovered=4`。ranking.json の該当フィールドと全一致をassert。

| 観点 | ranking (K0423基準) | 本実験 (第6次基準) | 判定 |
|---|---|---|---|
| WIN時 失効options | 4件 (`4327, 4328, 5056, 5830`) | 4件 (新規除外3件・`5830` は既存除外) | **一致** |
| WIN時 失効選択S4 | 1クラス (`5830` の3応答 49/60/59, 49/60/61, 49/60/71) | 0件 (第3次で吸収済み) | 一致 (基準差を明記) |
| greedy Δ | +49 (K0423基準) | 0 (第6次基準) | 基準差を明記 |
| FREE化分岐数 (WIN側) | 18 | 18 (保存chosen thirdsから幾何再計算) | **一致** |
| LOSS時 証人欠落分岐 (唯一証人数) | 4 | 4 (幾何再計算) | **一致** |

## 双対 (下界)

- 厳密 `Fraction`・全選択肢不等式 95,176件 (paid groups 869 / distinct 948 /
  options 34,429 / elements 962,452)、`--verify` で証明書を全再構成して一致確認。
- exact total `9126455 / 1386` ≒ 6,584.7439 → ceil で **6,585**
  (第6次 `182532671 / 27720` ≒ 6,584.8727 から exact は −0.1288、ceilは不変)。
- 動いた機構: options 34,432 → 34,429、elements 962,456 → 962,452。
  162106の3options除去 (`4327/4328/5056`) はどの群のmin alphaも押し上げず、
  S6 LOSS 3要素のcost除去が各選択肢の重み和を下げた。
- dual は候補集合と要素cost義務だけの関数であり、batch と staged の
  それらが同一 (上節) であるため、**両反射に同一証明書が成立**する。

## WIN側 (§5)

- 保存pool 1,945 から、層別済み14件のうち 558600 (pool外) を除く13 mask を除外 →
  使用可能 **1,932**。本轮の新規除外は1件 (162106, mask `4035788216077402112`)。
  S6 LOSS 3件のmaskは保存pool外のためpool縮小には寄与しない (cache登録のみ)。
  新規証人の創作0件。すべての証人は保存pool内・cache非接触。
- 再最適化前の損傷: 被覆不能 branch **8** / S4クラス **8** / affected replies
  `[1, 2, 4, 15, 79, 101]` — 第6次から**変化なし**。
  保存chosen thirds内で 162106 WIN により**18分岐がFREE化**
  (r=59, 60, 71 — ranking の if_win_newly_free_branches 18 と一致)。
  うち第6次時点ですでにFREEだった分岐を除いた**純増は12分岐**。
- 再最適化後 (全65軌道 × 全119 third を幾何から再列挙、dead fourthを含むthirdは
  反証されるため除外):
  closable **59 (不変)**、unclosable **[1, 2, 4, 15, 79, 101] (不変)**、
  and-width **6,812 (不変)**、未閉鎖証人 **1,746 → 1,745 (−1)**。
  chosen third は全59軌道で第6次と同一。唯一のcover差分は r=59 の
  witness_count **25 → 24** (保存証人集合から 162106 自身が resolved-WIN として
  除かれた1件)。
- S4区分: FREE 30 → 33 (+3)、OPEN 9,488 → 9,485 (−3)、DEAD 0。
  FREE化の+3は `4327/4328/5056` (162106をWIN子に持つクラス) が除外対象になったのと整合。
  新規閉鎖 (chosen thirdが全fourth無料) は第6次から/当初からとも **0件**。
- 全59軌道の cover を保存pool内で再検証し `verification.passed` (failures 0)。
  dead fourth によるthird失格 (`dead_disqualified_thirds`) も0。
- 162106 WIN は block内 (157861, 181624 はUNKNOWNのまま) で軌道閉鎖に寄与せず。
  第6次申送りの「block内WINは上界寄与皆無」予想は本件でも成立した。

## 独立証明の累積 (定義を明示して複数を併記)

`effect-measurement7.json` (`new_facts.cumulative_tallies`) を正とする。

| 定義 | 第6次まで | 第7次 (本轮後) |
|---|---:|---:|
| 本轮 | — | **1/1** (162106) |
| adaptive line の累積 (第1〜6次READMEの定義) | 11/11 | **12/12** |
| 計画層別 合計 (K0423パイロット込み) | 13/13 | **17/17** (receipt-backed 14 + certificate-derived 3) |
| 計画層別 **LOSSのみ** | 7/7 | **10/10** (7 receipt + 3 derived) |
| 計画層別 WINのみ | 6/6 | **7/7** |
| conflict-closure系 (K0423を除く) | 14/14 | **15/15** |
| 独立receipt総数 (層別外 focus3 を含む) | 16/16 | **17/17** |
| certificate-derived verdict (別枠) | — | **1証明書 / 3 verdict** |

層別外のまま保持している3件 (115540 LOSS / 144193 LOSS / 144311 WIN) は
どの計画にも反映していない (本実験の指示範囲外)。

## 結果census

- 28 conflict候補のうち層別17件: WIN `[126017, 131631, 144095, 162106, 197665, 206386, 209644]` /
  LOSS `[558600, 121263, 126899, 137694, 143240, 145001, 220231, 381840, 402066, 550881]`。
- 未知16件 (層別外3件を含む)。162106 は rank-25 候補のまま 25M 新規run で SOLVED(WIN)。
  `144019` / `144692` (UNKNOWN@10M) は扱い不変。
- 空盤 (11×11) は UNKNOWN。全盤への飛躍は行っていない。
- 上界は「最適証明計画」ではなく greedy な楽観計画であり、root証明ではない。

## 保存パス

| 内容 | パス |
|---|---|
| 第7次 修復済み両計画 (batch反映・staged照合・ranking照合・S6親再監査込み) | `output/repaired-joint-plan-update7.json` |
| 更新後 element-only dual (厳密Fraction・全選択肢不等式・`--verify`通過) | `output/updated-element-dual-update7.json` |
| WIN側 再解析 (ranking照合・pre-optimisation損傷・cover差分込み) | `output/win-side-reanalysis7.json` |
| 効果測定 (二重基準・累積tally・census) | `output/effect-measurement7.json` |
| 実行ログ | `output/{plan-update7,dual,dual-verify,win-side,effects}-run.log` |
| スクリプト | `scripts/{update_loss_plan,update_dual,update_win_side,measure_effects}.py` |

第6次以前の出力 (`n11-night-plan-update6-20261014/`, `n11-night-batch5-20261014/` 等) は
読み取り専用で使用し、一切書き換えていない。

## 次バッチへの申送り

- **上界が3回連続不変の後に動いた (31,774 → 31,771)**: 動因はWIN追加ではなく
  **S6 LOSS終局証明の要素cost削減**。162106 (block内4件目のWIN) は予想どおり
  上界寄与なし。certificate-derived LOSSが選択S4の子に直接当たる場合に
  上界が縮むという**新しい経路**が開いた。
- **下界はceil不変 (6,585)、exactは微減 (−0.1288)**: LOSS要素除去は各選択肢の重み和を
  下げる方向。ceilを動かすにはやはりgroup/第三手単位の制約追加が要る。
- block系残り候補 157861 (`4232/4233/4652/5830`)、181624 (`4807/4808/5132/5830`)、
  120370 (`3460/3469/5830/5839`) は引き続き**上界寄与皆無と推定**。
- **最有望の深掘り先**: 221294 (WIN時 失効選択8件・free=4・Δ+111、`5830` 非依存)。
  unclosable `[1, 2, 4, 15, 79, 101]` の救済は依然として**当該応手分岐を直接FREE化する
  未知S5 WIN** を要する (r=4 ← 137694 / r=15 ← 143240 / r=79 ← 220231 の欠損)。
- **層別外3件 (115540 LOSS / 144193 LOSS / 144311 WIN) の扱いが未決** (第4次から継続):
  reply 0 / 46 が未知証人として依存しており、層別すると unclosable 化する可能性が高い。
- **UNKNOWN据え置き**: 144019 / 144692 はUNKNOWN@10Mのまま (同一条件再探索禁止)。
- サイズ注意: night-batch5の162106 trace DAG (64.8MB)・131631 pruned DAG (57MB) は
  push済みだが、今後のtrace追加はLFS/分割を検討。

## 再現 (repo root)

```sh
uv run --locked python research/experiments/n11-night-plan-update7-20261015/scripts/update_loss_plan.py
uv run --locked python research/experiments/n11-night-plan-update7-20261015/scripts/update_dual.py
uv run --locked python research/experiments/n11-night-plan-update7-20261015/scripts/update_dual.py \
  --verify research/experiments/n11-night-plan-update7-20261015/output/updated-element-dual-update7.json
uv run --locked python research/experiments/n11-night-plan-update7-20261015/scripts/update_win_side.py
uv run --locked python research/experiments/n11-night-plan-update7-20261015/scripts/measure_effects.py
```

`output/*-run.log` は上記5コマンドの実行ログ (2026-10-16未明のクリーン再実行)。
`update_win_side.py` の出力は `seconds` 以外はバイト一致 (再実行で確認済み)。
既存の check_trace 実体・solver論理は読み取り専用で使用し、raw solver labelは
solver-trustedのまま、証拠への昇格は terminal-only receipt と検証済みcertificateのみが行う。
UNKNOWNは昇格しない。
