# n11 第5次両計画更新: 206386 WIN の反映

基準: main `cf2e7734` ＋ 未コミットの先行実験
(adaptive系4件 / night-batch1 / night-batch2 / night-batch3 /
night-plan-update3 / night-plan-update4)。
本実験は既存実験・knowledge正本・生成物・共有solver論理・K0423・
既存出力・第1次〜第4次出力・batch1〜3出力・履歴を一切変更せず、
`research/experiments/n11-night-plan-update5-20261014/` に結果を分離保存する。
第4次出力 (`n11-night-plan-update4-20261014/output/`) は読み取り専用の基盤。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
UNKNOWNは証拠ではない。空盤 (11x11) はUNKNOWNのまま、全盤への飛躍は行わない。

## 反映した1件 (n11-night-batch3-20261014 の terminal-only receipt, trusted葉0)

| S5索引 | verdict | 探索nodes | DAG nodes / edges / 終局 | receipt | certificate SHA256 |
|---:|---|---:|---|---|---|
| 206386 | **WIN** | 11,024,416 | 1,592,383 / 2,384,095 / 223,354 | `nighta25m-206386-receipt.json` | `eb7d18a8…` |

`trusted_leaves=0`・`pruned_roundtrip_verified`・certificate SHA256 と terminal-DAG 実体の一致・
`probe_manifest` との結合を再検証した。node予算25Mの**新規run** (10M NODE_LIMIT run とは別run) によるSOLVED。
206386は本系列で4件目の新規独立WIN証拠 (1件目209644、2件目126017、3件目197665)。

## 二重比較表 (第4次更新と当初 K0423 の両基準)

| 指標 | 当初 (K0423) | 第2次 | 第3次 | 第4次 | 第5次 | Δ 第4次→第5次 | Δ 当初→第5次 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 上界 = 要求S5数 | 31,636 | 31,728 | 31,774 | 31,774 | **31,774** | 0 | +138 |
| 下界 = 整数dual (ceil) | 6,577 | 6,582 | 6,583 | 6,584 | **6,585** | +1 | +8 |
| 区間 | [6,577, 31,636] | [6,582, 31,728] | [6,583, 31,774] | [6,584, 31,774] | **[6,585, 31,774]** | — | — |
| 層別済み S5 (WIN+LOSS) | 2 (1+1) | 6 (2+4) | 10 (3+7) | 11 (4+7) | **12 (5+7)** | +1 | +10 |
| 除外 S4 クラス数 | 2 | 5 | 9 | 12 | **14** | +2 | +12 |
| 再選択した応答数 | 5 | 0 | 3 | 0 | **0** | 0 | −5 |
| free thirds | 122 | 122 | 122 | 122 | **122** | 0 | 0 |
| 完全S5境界を再検算した選択S4 | 349 | 350 | 351 | 351 | **351** | 0 | +2 |
| 第三手網羅 (root×third) | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | **19 × 2,261** | 0 | 0 |
| WIN側 使用可能証人pool (保存1,945) | 1,942 | 1,940 | 1,936 | 1,935 | **1,934** | −1 | −11 |
| WIN側 未閉鎖証人S5 | 1,944 | 1,846 | 1,749 | 1,748 | **1,747** | −1 | −197 |
| WIN側 closable 応手軌道 | 65 | 62 | 59 | 59 | **59** | 0 | −6 |
| WIN側 unclosable 応手軌道 | [] | [1, 2, 101] | [1, 2, 4, 15, 79, 101] | [1, 2, 4, 15, 79, 101] | **[1, 2, 4, 15, 79, 101]** | 0 | +6件 |
| WIN側 and-width (chosen fourths) | 7,519 | 7,165 | 6,812 | 6,812 | **6,812** | 0 | −707 |
| 新規閉鎖 第三手 / 軌道 | — | 0 / 0 | 0 / 0 | 0 / 0 | **0 / 0** | 0 | 0 |

第2次・第3次列は各回の出力ファイルから再取得して照合した (値は第4次README表と一致)。

## LOSS側 (§4)

- 新規LOSSは0件。要求unionに既知WIN・既知LOSSが残らないことを表明
  (`known_win_selected=0` / `known_loss_in_union=0`)。
- 206386 (WIN) を合法S5子として持つ、すなわち206386にLOSS/UNKNOWNを要求していた
  S4クラス `[5563, 5570, 5830, 5834]` を全cost集合から除外。
  うち `5570` は第4次で (197665 WIN)、`5830` は第3次で (126017 WIN) 既に除外済みのため、
  **新規除外は2件** (`5563` と `5834`)。除外計は 12件 → **14件**。
- 上記4クラスはいずれも第4次基準では選択されていない
  (5830 の3応答は第3次、5570 の該当応答は第4次で再選択済み) ため、
  **代替選択によるgreedy修復は空振りで、上界は 31,774 → 31,774 (Δ0)**。
  changed_choice_count=0。
- 19 root・全2,261 third手・351選択S4の完全境界を独立幾何から再検算し、
  既知WIN要求0件・既知LOSS混入0件を表明 (`verification.passed`)。
- batch と staged-forward (単一verdictの退化系) を同一凍結入力から再計算し、
  labels / candidates / obligations / choices / union の全sha一致を確認。

### ranking 照合 (n11-conflict-ranking-20261013 の ranking.tsv 当該行と反実仮想を独立幾何で再計算)

ranking.tsv 行 (`geometry_rank=18`):
`if_win_loss_choices_invalidated=3` / `if_win_new_free_win_branches=18` /
`if_win_greedy_loss_union=31685` / `if_win_greedy_delta=49` /
`if_loss_fixed_win_branches_uncovered=4`。ranking.json の該当フィールドと全一致をassert。

| 観点 | ranking (K0423基準) | 本実験 (第4次基準) | 判定 |
|---|---|---|---|
| WIN時 失効options | 4件 (`5563, 5570, 5830, 5834`) | 4件 (新規除外2件) | **一致** |
| WIN時 失効選択S4 | 3件 (`5830` の3応答) | 0件 (第3次で吸収済み) | 一致 (基準差を明記) |
| greedy Δ | +49 (K0423基準) | 0 (第4次基準) | 基準差を明記 |
| FREE化分岐数 (WIN側) | 18 | 18 (保存chosen thirdsから幾何再計算) | **一致** |
| LOSS時 証人欠落分岐 (唯一証人数) | 4 | 4 (幾何再計算) | **一致** |

ranking の greedy Δ・失効選択数は「K0423基準の反実仮想」であり、
第5次のΔ0は 126017 / 197665 / 206386 の同一除外options block を第3・第4次で吸収した結果である。

## 双対 (下界)

- 厳密 `Fraction`・全選択肢不等式 95,192件 (paid groups 869 / distinct 948 /
  options 34,435 / elements 962,457)、`--verify` で証明書を全再構成して一致確認。
- exact total `5069937 / 770` ≒ 6,584.3338 → ceil で **6,585**
  (第4次 `182500141 / 27720` ≒ 6,583.6992 から +1)。
- 上昇の機構: `5563` / `5834` の2options除去で in-play options 34,437 → 34,435、
  elements 962,458 → 962,457 となり、min-over-options の値がわずかに上がった。
  要素cost義務集合自体はWIN追加では縮まない (新規LOSSなし)。
- dual は候補集合と要素cost義務だけの関数であり、batch と退化staged の
  それらが同一 (上節) であるため、**両反射に同一証明書が成立**する。

## WIN側 (§5)

- 保存pool 1,945 から、層別済み12件のうち 558600 (pool外) を除く11 mask を除外 →
  使用可能 **1,934**。本轮の新規除外は1件 (206386)。
  新規証人の創作0件。すべての証人は保存pool内・cache非接触。
- 再最適化前の損傷: 被覆不能 branch **8** / S4クラス **8** / affected replies
  `[1, 2, 4, 15, 79, 101]` — 第4次から**変化なし**
  (206386 を唯一の保存証人とする被覆不能分岐は0件)。
  保存chosen thirds内で 206386 WIN により**18分岐がFREE化**
  (r=59, 60, 71 — ranking の if_win_newly_free_branches 18 と一致)。
- 再最適化後 (全65軌道 × 全119 third を幾何から再列挙):
  closable **59 (不变)**、unclosable **[1, 2, 4, 15, 79, 101] (不变)**、
  and-width **6,812 (不变)**、未閉鎖証人 **1,748 → 1,747 (−1)**。
  chosen third は全59軌道で第4次と同一。唯一の差分は r=59 の保存証人集合から
  **206386 自身 (mask `2362915438441499983872`) が resolved-WIN として除かれた1件**。
  FREE S4クラスは 24 → 26 (+2) だが、応手軌道単位の無料化・再閉鎖には至らず、
  新規閉鎖 (chosen thirdが全fourth無料) は第4次から/当初からとも **0件**。
- 全59軌道の cover を保存pool内で再検証し `verification.passed` (failures 0)。
  全 witness が cache済みキーでないこと、pool外不使用、dead/open fourthの整合を確認。
- 206386 WIN は block内 (157861, 181624 はUNKNOWNのまま) で軌道閉鎖に寄与せず。
  第4次申送りの予測「206386 は block 同様 (WIN時18分岐FREE・上界寄与なし)」は
  上界側 (Δ0)・WIN側 (18分岐FREE・軌道閉鎖なし) の両方で**的中**した。

## 独立証明の累積 (定義を明示して複数を併記)

`effect-measurement5.json` (`new_facts.cumulative_tallies`) を正とする。

| 定義 | 第4次まで | 第5次 (本轮後) |
|---|---:|---:|
| 本轮 | — | **1/1** (206386) |
| adaptive line の累積 (第1〜4次READMEの定義) | 9/9 | **10/10** |
| 計画層別 合計 (K0423パイロット込み) | 11/11 | **12/12** |
| 計画層別 **LOSSのみ** | 7/7 | **7/7** (不变) |
| 計画層別 WINのみ | 4/4 | **5/5** |
| conflict-closure系 (K0423を除く) | 12/12 | **13/13** |
| 独立receipt総数 (層別外 focus3 を含む) | 14/14 | **15/15** |

層別外のまま保持している3件 (115540 LOSS / 144193 LOSS / 144311 WIN) は
どの計画にも反映していない (本実験の指示範囲外)。

## 結果census

- 28 conflict候補のうち層別12件: WIN `[126017, 144095, 197665, 206386, 209644]` /
  LOSS `[558600, 126899, 121263, 145001, 137694, 143240, 220231]`。
- 未知18件 (層別外3件を含む)。`144019` / `144692` (UNKNOWN@10M) は扱い不变。
  206386 は UNKNOWN@10M から 25M 新規run で SOLVED(WIN) により層別済み。
- 空盤 (11×11) は UNKNOWN。全盤への飛躍は行っていない。
- 上界は「最適証明計画」ではなく greedy な楽観計画であり、root証明ではない。

## 保存パス

| 内容 | パス |
|---|---|
| 第5次 修復済み両計画 (batch反映・退化staged照合・ranking照合込み) | `output/repaired-joint-plan-update5.json` |
| 更新後 element-only dual (厳密Fraction・全選択肢不等式・`--verify`通過) | `output/updated-element-dual-update5.json` |
| WIN側 再解析 (ranking照合・pre-optimisation損傷込み) | `output/win-side-reanalysis5.json` |
| 効果測定 (二重基準・累積tally・census) | `output/effect-measurement5.json` |
| 実行ログ | `output/{plan-update5,dual,dual-verify,win-side,effects}-run.log` |
| スクリプト | `scripts/{update_loss_plan,update_dual,update_win_side,measure_effects}.py` |

第4次以前の出力 (`n11-night-plan-update4-20261014/`, `n11-night-batch3-20261014/`,
`n11-night-plan-update3-20261014/` 等) は読み取り専用で使用し、
一切書き換えていない (git status で未追跡のまま)。

## 次バッチへの申送り

- **上界が2回連続で動かなくなった**: 206386 も 126017 / 197665 と同一の
  4除外options block (`5563, 5570, 5830, 5834`) の3件目で、
  選択修復は第3・第4次で吸収済み。block内WINは最初の1件で上界が飽和する性質が
  3件で確認された。残る block内WIN 候補 (157861, 181624) も上界寄与は皆無と推定。
- **下界が +1 (6,584 → 6,585)**: 2options除去が min-over-options を押し上げた。
  要素dualは新規WINにほぼ反応しない (第3〜5次) が、options削減には反応する。
  下界をさらに動かすには group/第三手単位の制約追加が要る。
- **WIN側の unclosable が3回連続で救済されなかった**: 18分岐FREEは
  3件とも r=59/60/71 (closable軌道) に集中し、r=1/2/4/15/79/101 に寄与しない。
  r=4 ← 137694 / r=15 ← 143240 / r=79 ← 220231 の欠損は依然として、
  **当該応手分岐を直接FREE化する未知S5 WIN** を要する。
- **最有望の深掘り先**: 131631 (10Mでroot 99子中51子WIN・残48子、25M以上でのみ再開可)、
  162106 (2Mで11/99)。次いで 120370 (LOSS時14分岐欠落・free=20)、
  221294 (WIN時8選択影響・free=4)、block残2件の 181624 / 157861。
- **層別外3件 (115540 LOSS / 144193 LOSS / 144311 WIN) の扱いが未決** (第4次から継続):
  reply 0 / 46 が未知証人として依存しており、層別すると unclosable 化する可能性が高い。
- **UNKNOWN据え置き**: 144019 / 144692 はUNKNOWN@10Mのまま (同一条件再探索禁止)。
- ディスク: receipt発行済み trace (`build/n11-night-*-traces/`) は削除可。

## 再現 (repo root)

```sh
uv run --locked python research/experiments/n11-night-plan-update5-20261014/scripts/update_loss_plan.py
uv run --locked python research/experiments/n11-night-plan-update5-20261014/scripts/update_dual.py
uv run --locked python research/experiments/n11-night-plan-update5-20261014/scripts/update_dual.py \
  --verify research/experiments/n11-night-plan-update5-20261014/output/updated-element-dual-update5.json
uv run --locked python research/experiments/n11-night-plan-update5-20261014/scripts/update_win_side.py
uv run --locked python research/experiments/n11-night-plan-update5-20261014/scripts/measure_effects.py
```

`update_win_side.py` の出力は `seconds` 以外はバイト一致 (再実行で確認済み)。
既存の check_trace 実体・solver論理は読み取り専用で使用し、raw solver labelは
solver-trustedのまま、証拠への昇格は terminal-only receipt のみが行う。UNKNOWNは昇格しない。
