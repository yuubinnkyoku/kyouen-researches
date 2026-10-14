# n11 第4次両計画更新: 197665 WIN の反映

基準: main `cf2e7734` ＋ 未コミットの先行実験
(adaptive系4件 / night-batch1 / night-batch2 / night-plan-update3)。
本実験は既存実験・knowledge正本・生成物・共有solver論理・K0423・
第1次/第2次/第3次出力・batch2出力・履歴を一切変更せず、
`research/experiments/n11-night-plan-update4-20261014/` に結果を分離保存する。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
UNKNOWNは証拠ではない。空盤 (11x11) はUNKNOWNのまま、全盤への飛躍は行わない。

## 反映した1件 (n11-night-batch2-20261014 の terminal-only receipt, trusted葉0)

| S5索引 | verdict | 探索nodes | DAG nodes / edges / 終局 | receipt | certificate SHA256 |
|---:|---|---:|---|---|---|
| 197665 | **WIN** | 10,294,083 | 1,624,418 / 2,433,495 / 227,142 | `nighta25m-197665-receipt.json` | `9b50b654…` |

`trusted_leaves=0`・`pruned_roundtrip_verified`・certificate SHA256 と terminal-DAG 実体の一致・
`probe_manifest` との結合を再検証した。node予算25Mの**新規run**によるSOLVED
(10M run の NODE_LIMIT とは別run; 同一条件再探索ではない)。
197665は本系列で3件目の新規独立WIN証拠 (1件目209644、2件目126017)。

## 二重比較表 (第3次更新と当初 K0423 の両基準)

| 指標 | 当初 (K0423) | 第2次 | 第3次 | 第4次 | Δ 第3次→第4次 | Δ 当初→第4次 |
|---|---:|---:|---:|---:|---:|---:|
| 上界 = 要求S5数 | 31,636 | 31,728 | 31,774 | **31,774** | 0 | +138 |
| 下界 = 整数dual (ceil) | 6,577 | 6,582 | 6,583 | **6,584** | +1 | +7 |
| 区間 | [6,577, 31,636] | [6,582, 31,728] | [6,583, 31,774] | **[6,584, 31,774]** | — | — |
| 層別済み S5 (WIN+LOSS) | 2 (1+1) | 6 (2+4) | 10 (3+7) | **11 (4+7)** | +1 | +9 |
| 除外 S4 クラス数 | 2 | 5 | 9 | **12** | +3 | +10 |
| 再選択した応答数 | 5 | 0 | 3 | **0** | −3 | −5 |
| free thirds | 122 | 122 | 122 | **122** | 0 | 0 |
| 完全S5境界を再検算した選択S4 | 349 | 350 | 351 | **351** | 0 | +2 |
| 第三手網羅 (root×third) | 19 × 2,261 | 19 × 2,261 | 19 × 2,261 | **19 × 2,261** | 0 | 0 |
| WIN側 使用可能証人pool (保存1,945) | 1,942 | 1,940 | 1,936 | **1,935** | −1 | −7 |
| WIN側 未閉鎖証人S5 | 1,944 | 1,846 | 1,749 | **1,748** | −1 | −196 |
| WIN側 closable 応手軌道 | 65 | 62 | 59 | **59** | 0 | −6 |
| WIN側 unclosable 応手軌道 | [] | [1, 2, 101] | [1, 2, 4, 15, 79, 101] | **[1, 2, 4, 15, 79, 101]** | 0 | +6件 |
| WIN側 and-width (chosen fourths) | 7,519 | 7,165 | 6,812 | **6,812** | 0 | −707 |
| 新規閉鎖 第三手 / 軌道 | — | 0 / 0 | 0 / 0 | **0 / 0** | 0 | 0 |

## LOSS側 (§4)

- 新規LOSSは0件。要求unionに既知WIN・既知LOSSが残らないことを表明
  (`known_win_selected=0` / `known_loss_in_union=0`)。
- 197665 (WIN) を未解決子に持つ S4クラス
  `[5266, 5267, 5570, 5830]` を全cost集合から除外。
  うち `5830` は第3次で既に除外済み (126017 WIN) のため、
  **新規除外は3件** (第3次9件 → 計12件)。
- 126017 と 197665 は同一の4除外optionsを共有するblockであり、
  第3次が 5830 の3応答 (first=49, reply=60, third=59/61/71) を
  すでに再選択済みだったため、**第4次基準での失効選択は0件**。
  greedy再選択は空振りで、上界は **31,774 → 31,774 (Δ0)**。
- 19 root・全2,261 third手・351選択S4の完全境界を独立幾何から再検算し、
  既知WIN要求0件・既知LOSS混入0件を表明 (`verification.passed`)。
- batch と staged-forward (単一verdictの退化系) を同一凍結入力から再計算し、
  labels / candidates / obligations / choices / union の全sha一致を確認。

### ranking との照合 (n11-conflict-ranking-20261013 の反実仮想を独立幾何で再計算)

| 観点 | ranking (K0423基準) | 本実験 (第3次基準) | 判定 |
|---|---|---|---|
| WIN時 失効options | 4件 (`5266, 5267, 5570, 5830`) | 4件 (新規除外3件) | **一致** |
| WIN時 失効選択S4 | `[5830]` (3応答) | 0件 (第3次で吸収済み) | 一致 (基準差を明記) |
| greedy Δ | +49 (K0423基準) | 0 (第3次基準) | 基準差を明記 |
| FREE化分岐数 (WIN側) | 18 | 18 | **一致** |
| LOSS時 証人欠落分岐 | 4 | 4 | **一致** |

ranking の greedy Δ・失効選択数は「K0423基準の反実仮想」であり、
第4次のΔ0は126017/197665共有blockを第3次で吸収した結果である。

## 双対 (下界)

- 厳密 `Fraction`・全選択肢不等式 95,198件 (paid groups 869 / distinct 948 /
  options 34,437 / elements 962,458)、`--verify` で証明書を全再構成して一致確認。
- exact total `182500141 / 27720` ≒ 6,583.70 → ceil で **6,584**
  (第3次 6,583 から +1)。
- 上昇の機構: 3件のoptions除去により各paid groupの選択肢が減り、
  min-over-options の値がわずかに上がった。要素cost義務集合自体は
  WIN追加では縮まないが、**197665自身がin-play optionsから消え**
  elements 962,459 → 962,458 となった。
- dual は候補集合と要素cost義務だけの関数であり、batch と退化staged の
  それらが同一 (上節) であるため、**両反射に同一証明書が成立**する。

## WIN側 (§5)

- 保存pool 1,945 から、層別済み11件のうち 558600 を除く10 mask を除外 →
  使用可能 **1,935**。本轮の新規除外は1件 (197665)。
  新規証人の創作0件。
- 再最適化前の損傷: 被覆不能 branch **8** / S4クラス **8** / affected replies
  `[1, 2, 4, 15, 79, 101]` — 第3次から**変化なし**
  (197665はWINのため除去ではなく分岐をFREE化し、 LOSS由来の欠損は埋まらない)。
  保存chosen thirds内で 197665 WIN により**18分岐がFREE化**
  (r=59, 60, 71 — ranking の if_win_newly_free_branches 18 と一致)。
- 再最適化後 (全65軌道 × 全119 third を幾何から再列挙):
  closable **59 (不变)**、unclosable **[1, 2, 4, 15, 79, 101] (不变)**、
  and-width **6,812 (不变)**、未閉鎖証人 **1,749 → 1,748 (−1)**。
  FREE S4クラスは 21 → 24 (+3) だが、応手軌道単位の無料化・再閉鎖には至らず、
  新規閉鎖 (chosen thirdが全fourth無料) は第3次から/当初からとも **0件**。
  証人数減の内訳: r=59 の chosen third (third=60) が 197665 証人1件を
  FREE化分岐として不要化した1件のみ。
- 全59軌道の cover を保存pool内で再検証し `verification.passed` (failures 0)。
  全 witness が cache済みキーでないこと、pool外不使用、dead/open fourthの整合を確認。
- 197665 WIN は block内 (157861, 181624 はUNKNOWNのまま) で軌道閉鎖に寄与せず。
  第3次申送りの予測「126017と同型の挙動」は上界側で的中 (Δ0)、
  WIN側も18分岐FREEで一致したが、r=4/15/79 の代替third獲得には
  当該応手の分岐を直接FREE化する未知S5 WIN が必要である点も確認された。

## 独立証明の累積 (定義を明示して複数を併記)

`effect-measurement4.json` (`new_facts.cumulative_tallies`) を正とする。

| 定義 | 第3次まで | 第4次 (本轮後) |
|---|---:|---:|
| 本轮 | — | **1/1** (197665) |
| adaptive line の累積 (第1〜3次READMEの定義) | 8/8 | **9/9** |
| 計画層別 合計 (K0423パイロット込み) | 10/10 | **11/11** |
| 計画層別 **LOSSのみ** | 7/7 | **7/7** (不变) |
| 計画層別 WINのみ | 3/3 | **4/4** |
| conflict-closure系 (K0423を除く) | 11/11 | **12/12** |
| 独立receipt総数 (層別外 focus3 を含む) | 13/13 | **14/14** |

層別外のまま保持している3件 (115540 LOSS / 144193 LOSS / 144311 WIN) は
どの計画にも反映していない (本実験の指示範囲外)。

## 結果census

- 28 conflict候補のうち層別11件: WIN `[126017, 144095, 197665, 209644]` /
  LOSS `[558600, 126899, 121263, 145001, 137694, 143240, 220231]`。
- 未知19件 (層別外3件を含む)。`144019` / `144692` (UNKNOWN@10M) は扱い不变。
  197665 は UNKNOWN@10M から 25M新規runで SOLVED(WIN) により層別済み。
- 空盤 (11×11) は UNKNOWN。全盤への飛躍は行っていない。
- 上界は「最適証明計画」ではなく greedy な楽観計画であり、root証明ではない。

## 保存パス

| 内容 | パス |
|---|---|
| 第4次 修復済み両計画 (batch反映・退化staged照合・ranking照合込み) | `output/repaired-joint-plan-update4.json` |
| 更新後 element-only dual (厳密Fraction・全選択肢不等式・`--verify`通過) | `output/updated-element-dual-update4.json` |
| WIN側 再解析 (ranking照合・pre-optimisation損傷込み) | `output/win-side-reanalysis4.json` |
| 効果測定 (二重基準・累積tally・census) | `output/effect-measurement4.json` |
| 実行ログ | `output/{plan-update4,dual,dual-verify,win-side,effects}-run.log` |
| スクリプト | `scripts/{update_loss_plan,update_dual,update_win_side,measure_effects}.py` |

第3次以前の出力 (`n11-night-plan-update3-20261014/`, `n11-night-batch2-20261014/`,
`n11-adaptive-plan-update2-20261013/` 等) は読み取り専用で使用し、
一切書き換えていない (git status で未追跡のまま)。

## 次バッチへの申送り

- **上界が動かなくなった**: 197665 WIN は126017と同一blockのため、
  第3次で既に選択修復まで吸収済み。単独WIN (Δ49の反実仮想) と
  合成後の実効Δ0の差は、greedy計画がblock内の最初のWINで飽和することを示す。
  以降のblock内WIN (157861, 181624) も上界寄与は皆無と推定される。
- **下界が +1 (6,583 → 6,584)**: options 3件除去が min-over-options を押し上げた。
  要素dualは新規WINにほぼ反応しない (第3次からの傾向) が、
  options削減には反応する。下界をさらに動かすには group/第三手単位の制約追加が要る。
- **WIN側の unclosable が救済されなかった**: 197665 の18分岐FREEは
  r=59/60/71 (closable軌道) に集中し、r=4/15/79 に寄与せず。
  r=4 ← 137694 / r=15 ← 143240 / r=79 ← 220231 の欠損は依然として、
  **当該応手分岐を直接FREE化する未知S5 WIN** を要する。
  未着手候補 (120370, 143718, 157861, 181624, 221294 ほか) が候補。
- **最有望の深掘り先**: 206386 (10Mでroot 88子中82子WIN・残6子、
  「残り僅か」型、block同様のWIN時18分岐FREE)。
  166171 / 142283 (2Mで22/91・24/92)、137043 三兄弟は20〜30M級。
- **層別外3件 (115540 LOSS / 144193 LOSS / 144311 WIN) の扱いが未決**:
  現在のWIN側coverのうち reply 0 が115540 (2 branch)、reply 46 が144193 (2 branch) に
  未知証人としてのみ依存。層別すると reply 0 / 46 が unclosable 化する可能性が高い。
  計画更新実験で focus3 を層別するかどうかの判断を先に要する。
- **UNKNOWN据え置き**: 144019 / 144692 はUNKNOWN@10Mのまま (同一条件再探索禁止)。
  206386 の残6子は個別予算集中または25M拡張が別runとして可能。

## 再現 (repo root)

```sh
uv run --locked python research/experiments/n11-night-plan-update4-20261014/scripts/update_loss_plan.py
uv run --locked python research/experiments/n11-night-plan-update4-20261014/scripts/update_dual.py
uv run --locked python research/experiments/n11-night-plan-update4-20261014/scripts/update_dual.py \
  --verify research/experiments/n11-night-plan-update4-20261014/output/updated-element-dual-update4.json
uv run --locked python research/experiments/n11-night-plan-update4-20261014/scripts/update_win_side.py
uv run --locked python research/experiments/n11-night-plan-update4-20261014/scripts/measure_effects.py
```

`update_win_side.py` の出力は `seconds` 以外はバイト一致 (再実行で確認済み)。
既存の check_trace 実体・solver論理は読み取り専用で使用し、raw solver labelは
solver-trustedのまま、証拠への昇格は terminal-only receipt のみが行う。UNKNOWNは昇格しない。
