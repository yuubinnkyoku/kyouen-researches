# n11 第6次両計画更新: 131631 WIN の反映

基準: main `cf2e7734` ＋ 未コミットの先行実験
(adaptive系4件 / night-batch1〜4 / night-plan-update3〜5)。
本実験は既存実験・knowledge正本・生成物・共有solver論理・K0423・
既存出力・第1次〜第5次出力・batch1〜4出力・履歴を一切変更せず、
`research/experiments/n11-night-plan-update6-20261014/` に結果を分離保存する。
第5次出力 (`n11-night-plan-update5-20261014/output/`) は読み取り専用の基盤。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
UNKNOWNは証拠ではない。空盤 (11x11) はUNKNOWNのまま、全盤への飛躍は行わない。

## 反映した1件 (n11-night-batch4-20261014 の terminal-only receipt, trusted葉0)

| S5索引 | verdict | 探索nodes | DAG nodes / edges / 終局 | receipt | certificate SHA256 |
|---:|---|---:|---|---|---|
| 131631 | **WIN** | 22,709,147 | 2,815,975 / 4,139,862 / 429,845 | `nighta25m-131631-receipt.json` | `bbbc6c9b…` |

`trusted_leaves=0`・`pruned_roundtrip_verified`・certificate SHA256 と terminal-DAG 実体の一致・
`probe_manifest` との結合を再検証した。さらに night-batch4 の
`nighta25m-131631-python-comparison.json` (verdict / nodes / edges / terminal_nodes / trusted_leaves) が
receipt と全一致すること、`check_trace.cpp` の実体SHA (`0f890cb4…`) が receipt の
`checker_source_sha256` と一致することをassertした。
node予算25Mの**新規run** (10M NODE_LIMIT run とは別run) によるSOLVED。
131631は本系列で5件目の新規独立WIN証拠 (1件目209644、2件目126017、3件目197665、4件目206386)。
計画に層別した13件のreceiptは script内で全件 assertし
(`plan["shared_checker_source_sha256"]` = `0f890cb4…`)、
層別外の3件 (native focus 115540 / 144193 / 144311) を含む**全16件の独立receiptが
同一の checker source SHA256** (`research/experiments/n11-native-terminal-checker-20261013/
scripts/check_trace.cpp` の実体) を共有することを本轮で全数確認した。

## 二重比較表 (第5次更新と当初 K0423 の両基準)

| 指標 | 当初 (K0423) | 第2次 | 第3次 | 第4次 | 第5次 | 第6次 | Δ 第5次→第6次 | Δ 当初→第6次 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 上界 = 要求S5数 | 31,636 | 31,728 | 31,774 | 31,774 | 31,774 | **31,774** | 0 | +138 |
| 下界 = 整数dual (ceil) | 6,577 | 6,582 | 6,583 | 6,584 | 6,585 | **6,585** | 0 | +8 |
| 区間 | [6,577, 31,636] | [6,582, 31,728] | [6,583, 31,774] | [6,584, 31,774] | [6,585, 31,774] | **[6,585, 31,774]** | — | — |
| 層別済み S5 (WIN+LOSS) | 2 (1+1) | 6 (2+4) | 10 (3+7) | 11 (4+7) | 12 (5+7) | **13 (6+7)** | +1 | +11 |
| 除外 S4 クラス数 | 2 | 5 | 9 | 12 | 14 | **17** | +3 | +15 |
| 再選択した応答数 | 5 | 0 | 3 | 0 | 0 | **0** | 0 | −5 |
| free thirds | 122 | 122 | 122 | 122 | 122 | **122** | 0 | 0 |
| 完全S5境界を再検算した選択S4 | 349 | 350 | 351 | 351 | 351 | **351** | 0 | +2 |
| 第三手網羅 (root×third) | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | **19 × 2,261** | 0 | 0 |
| WIN側 使用可能証人pool (保存1,945) | 1,942 | 1,940 | 1,936 | 1,935 | 1,934 | **1,933** | −1 | −9 |
| WIN側 未閉鎖証人S5 | 1,944 | 1,846 | 1,749 | 1,748 | 1,747 | **1,746** | −1 | −198 |
| WIN側 closable 応手軌道 | 65 | 62 | 59 | 59 | 59 | **59** | 0 | −6 |
| WIN側 unclosable 応手軌道 | [] | [1, 2, 101] | [1, 2, 4, 15, 79, 101] | [1, 2, 4, 15, 79, 101] | [1, 2, 4, 15, 79, 101] | **[1, 2, 4, 15, 79, 101]** | 0 | +6件 |
| WIN側 and-width (chosen fourths) | 7,519 | 7,165 | 6,812 | 6,812 | 6,812 | **6,812** | 0 | −707 |
| 新規閉鎖 第三手 / 軌道 | — | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | **0 / 0** | 0 | 0 |

第2次〜第5次列は各回の出力ファイルから再取得して照合した
(値は第4次・第5次README表と一致)。

## LOSS側 (§4)

- 新規LOSSは0件。要求unionに既知WIN・既知LOSSが残らないことを表明
  (`known_win_selected=0` / `known_loss_in_union=0`)。
- 131631 (WIN) を合法S5子として持つ、すなわち131631にLOSS/UNKNOWNを要求していた
  S4クラス `[3678, 3679, 4564, 5830]` を全cost集合から除外。
  うち `5830` は第3次で (126017 WIN) 既に除外済みのため、**新規除外は3件**
  (`3678`, `3679`, `4564`)。除外計は 14件 → **17件**。
- 上記4クラスはいずれも第5次基準では選択されていない
  (`3678` / `3679` / `4564` はK0423基準から一度も選択されたことがなく、
  `5830` の3応答は第3次で再選択済み) ため、**代替選択によるgreedy修復は空振りで、
  上界は 31,774 → 31,774 (Δ0)**。changed_choice_count=0。
- 19 root・全2,261 third手・351選択S4の完全境界を独立幾何から再検算し、
  既知WIN要求0件・既知LOSS混入0件を表明 (`verification.passed`)。
- batch と staged-forward (単一verdictの退化系) を同一凍結入力から再計算し、
  labels / candidates / obligations / choices / union の全sha一致を確認。

### ranking 照合 (n11-conflict-ranking-20261013 の ranking.tsv 当該行と反実仮想を独立幾何で再計算)

ranking.tsv 行 (`geometry_rank=23`):
`if_win_loss_choices_invalidated=3` / `if_win_new_free_win_branches=18` /
`if_win_greedy_loss_union=31685` / `if_win_greedy_delta=49` /
`if_loss_fixed_win_branches_uncovered=4`。ranking.json の該当フィールドと全一致をassert。

| 観点 | ranking (K0423基準) | 本実験 (第5次基準) | 判定 |
|---|---|---|---|
| WIN時 失効options | 4件 (`3678, 3679, 4564, 5830`) | 4件 (新規除外3件・`5830` は既存除外) | **一致** |
| WIN時 失効選択S4 | 1クラス (`5830` の3応答) | 0件 (第3次で吸収済み) | 一致 (基準差を明記) |
| greedy Δ | +49 (K0423基準) | 0 (第5次基準) | 基準差を明記 |
| FREE化分岐数 (WIN側) | 18 | 18 (保存chosen thirdsから幾何再計算) | **一致** |
| LOSS時 証人欠落分岐 (唯一証人数) | 4 | 4 (幾何再計算) | **一致** |

ranking の greedy Δ・失効選択数は「K0423基準の反実仮想」であり、
第6次のΔ0は 126017 (第3次) が `5830` 上の3応答を再選択済みであることに加え、
`3678` / `3679` / `4564` がそもそも未選択クラスであるためである。
なお ranking の「LOSS時欠落4分岐」(r=59, third=60 の4分岐) は、
本轮では **131631 が当該分岐のWIN子になるのと同時に唯一証人から外れる**ため、
uncovered にならず (r=59 は引き続きclosable)、被覆不能分岐は第5次の8件のままである。

## 双対 (下界)

- 厳密 `Fraction`・全選択肢不等式 95,185件 (paid groups 869 / distinct 948 /
  options 34,432 / elements 962,456)、`--verify` で証明書を全再構成して一致確認。
- exact total `182532671 / 27720` ≒ 6,584.8727 → ceil で **6,585**
  (第5次 `5069937 / 770` ≒ 6,584.3338 から ceil は不変、exact値は +0.5389 上昇)。
- 動いた機構: `3678` / `3679` / `4564` の3options除去で in-play options 34,435 → 34,432、
  elements 962,457 → 962,456。要素cost義務集合自体はWIN追加では縮まない (新規LOSSなし)。
- dual は候補集合と要素cost義務だけの関数であり、batch と退化staged の
  それらが同一 (上節) であるため、**両反射に同一証明書が成立**する。

## WIN側 (§5)

- 保存pool 1,945 から、層別済み13件のうち 558600 (pool外) を除く12 mask を除外 →
  使用可能 **1,933**。本轮の新規除外は1件 (131631, mask `4035788216077385732`)。
  新規証人の創作0件。すべての証人は保存pool内・cache非接触。
- 再最適化前の損傷: 被覆不能 branch **8** / S4クラス **8** / affected replies
  `[1, 2, 4, 15, 79, 101]` — 第5次から**変化なし**
  (131631 を唯一の保存証人とする被覆不能分岐は0件)。
  保存chosen thirds内で 131631 WIN により**18分岐がFREE化**
  (r=59, 60, 71 — ranking の if_win_newly_free_branches 18 と一致)。
  うち第5次時点ですでにFREEだった分岐を除いた**純増は12分岐**
  (`freed_branches_by_new_win_only_in_stored_thirds`)。
- 再最適化後 (全65軌道 × 全119 third を幾何から再列挙):
  closable **59 (不变)**、unclosable **[1, 2, 4, 15, 79, 101] (不变)**、
  and-width **6,812 (不变)**、未閉鎖証人 **1,747 → 1,746 (−1)**。
  chosen third は全59軌道で第5次と同一。唯一の差分は r=59 の
  witness_count **26 → 25** (保存証人集合から 131631 自身が resolved-WIN として
  除かれた1件)。viable_thirds 6 → 6、chosen_fourths 117 → 117。
- S4区分: FREE 26 → 30 (+4)、OPEN 9,492 → 9,488 (−4)、DEAD 0。
  応手軌道単位の無料化・再閉鎖には至らず、新規閉鎖 (chosen thirdが全fourth無料) は
  第5次から/当初からとも **0件**。
- 全59軌道の cover を保存pool内で再検証し `verification.passed` (failures 0)。
  全 witness が cache済みキーでないこと、pool外不使用、dead/open fourthの整合を確認。
- 131631 WIN は block内 (157861, 181624 はUNKNOWNのまま) で軌道閉鎖に寄与せず。
  第5次申送りの推定「block内WINは最初の1件で上界が飽和する」は、
  `3678/3679/4564/5830` ブロックの**1件目**である本轮でも
  上界側 (Δ0)・WIN側 (18分岐FREE・軌道閉鎖なし) の両方で成立した。

## 独立証明の累積 (定義を明示して複数を併記)

`effect-measurement6.json` (`new_facts.cumulative_tallies`) を正とする。

| 定義 | 第5次まで | 第6次 (本轮後) |
|---|---:|---:|
| 本轮 | — | **1/1** (131631) |
| adaptive line の累積 (第1〜5次READMEの定義) | 10/10 | **11/11** |
| 計画層別 合計 (K0423パイロット込み) | 12/12 | **13/13** |
| 計画層別 **LOSSのみ** | 7/7 | **7/7** (不变) |
| 計画層別 WINのみ | 5/5 | **6/6** |
| conflict-closure系 (K0423を除く) | 13/13 | **14/14** |
| 独立receipt総数 (層別外 focus3 を含む) | 15/15 | **16/16** |

層別外のまま保持している3件 (115540 LOSS / 144193 LOSS / 144311 WIN) は
どの計画にも反映していない (本実験の指示範囲外)。

## 結果census

- 28 conflict候補のうち層別13件: WIN `[126017, 131631, 144095, 197665, 206386, 209644]` /
  LOSS `[558600, 126899, 121263, 145001, 137694, 143240, 220231]`。
- 未知17件 (層別外3件を含む)。`144019` / `144692` (UNKNOWN@10M) は扱い不变。
  131631 は UNKNOWN@10M から 25M 新規run で SOLVED(WIN) により層別済み。
- 空盤 (11×11) は UNKNOWN。全盤への飛躍は行っていない。
- 上界は「最適証明計画」ではなく greedy な楽観計画であり、root証明ではない。

## 保存パス

| 内容 | パス |
|---|---|
| 第6次 修復済み両計画 (batch反映・退化staged照合・ranking照合・checker SHA共通照合込み) | `output/repaired-joint-plan-update6.json` |
| 更新後 element-only dual (厳密Fraction・全選択肢不等式・`--verify`通過) | `output/updated-element-dual-update6.json` |
| WIN側 再解析 (ranking照合・pre-optimisation損傷・cover差分込み) | `output/win-side-reanalysis6.json` |
| 効果測定 (二重基準・累積tally・census) | `output/effect-measurement6.json` |
| 実行ログ | `output/{plan-update6,dual,dual-verify,win-side,effects}-run.log` |
| スクリプト | `scripts/{update_loss_plan,update_dual,update_win_side,measure_effects}.py` |

第5次以前の出力 (`n11-night-plan-update5-20261014/`, `n11-night-batch4-20261014/` 等) は
読み取り専用で使用し、一切書き換えていない (git status で未追跡のまま)。

## 次バッチへの申送り

- **上界が3回連続で動かなくなった (31,774)**: 131631 は
  `3678 / 3679 / 4564 / 5830` という**第2のoptions-blockの1件目**であり、
  それでも最初の1件で選択飽和した (`5830` は全block共有で第3次除外済み、
  残り3件は未選択クラス)。同型の残り候補は 162106 (`4327/4328/5056/5830`)、
  157861 (`4232/4233/4652/5830`)、181624 (`4807/4808/5132/5830`)、
  120370 (`3460/3469/5830/5839`) で、**上界寄与は皆無と推定**。
  上界を本当に動かすのは 221294 (WIN時 失効選択8件・free=4・Δ+111) のような
  block外候補。
- **下界は ceil 不変だが exact は +0.5389 上昇**: 3options除去が min-over-options を
  押し上げた。要素dualは新規WINにほぼ反応しない (第3〜6次) が、options削減には反応する。
  ceilをさらに動かすには group/第三手単位の制約追加が要る。
- **WIN側の unclosable が4回連続で救済されなかった**: 18分岐FREEは
  4件とも r=59/60/71 (closable軌道) に集中し、r=1/2/4/15/79/101 に寄与しない。
  r=4 ← 137694 / r=15 ← 143240 / r=79 ← 220231 の欠損は依然として、
  **当該応手分岐を直接FREE化する未知S5 WIN** を要する。
- **未閉鎖証人は 1,746**: r=59 のcoverは witness_count 26→25 に縮んだが
  chosen third は不変。r=59/60/71 は 131631 で既にFREE寄与済みのため、
  同一blockの残り候補 (162106 等) はここにも寄与しない可能性が高い。
- **最有望の深掘り先**: 221294 (WIN時8選択影響・free=4・失効optionsが `5830` 非依存)、
  次いで 120370 (LOSS時14分岐欠落・free=20)、162106 (2Mで11/99)、
  block残2件の 157861 / 181624。
- **層別外3件 (115540 LOSS / 144193 LOSS / 144311 WIN) の扱いが未決** (第4次から継続):
  reply 0 / 46 が未知証人として依存しており、層別すると unclosable 化する可能性が高い。
- **UNKNOWN据え置き**: 144019 / 144692 はUNKNOWN@10Mのまま (同一条件再探索禁止)。
- ディスク: receipt発行済み trace (`build/n11-night-*-traces/`) は削除可。

## 再現 (repo root)

```sh
uv run --locked python research/experiments/n11-night-plan-update6-20261014/scripts/update_loss_plan.py
uv run --locked python research/experiments/n11-night-plan-update6-20261014/scripts/update_dual.py
uv run --locked python research/experiments/n11-night-plan-update6-20261014/scripts/update_dual.py \
  --verify research/experiments/n11-night-plan-update6-20261014/output/updated-element-dual-update6.json
uv run --locked python research/experiments/n11-night-plan-update6-20261014/scripts/update_win_side.py
uv run --locked python research/experiments/n11-night-plan-update6-20261014/scripts/measure_effects.py
```

`update_win_side.py` の出力は `seconds` 以外はバイト一致 (再実行で確認済み)。
既存の check_trace 実体・solver論理は読み取り専用で使用し、raw solver labelは
solver-trustedのまま、証拠への昇格は terminal-only receipt のみが行う。UNKNOWNは昇格しない。
