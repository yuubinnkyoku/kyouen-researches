# n11 第3次両計画更新: 137694/143240/220231 LOSS・126017 WIN の反映

基準: main `cf2e7734` ＋ 未コミットの先行4実験 (adaptive-plan-update / update2 / probe / verify / night-batch1)。
本実験は既存実験・knowledge正本・生成物・共有solver論理・K0423・
第1次/第2次出力・履歴を一切変更せず、
`research/experiments/n11-night-plan-update3-20261014/` に結果を分離保存する。

極性は [K0371](../../knowledge/items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md)
絶対準拠: S5=AND・後手手番。WIN(verdict=1)=全S6先手WIN、LOSS(verdict=2)=存在S6先手LOSS。
UNKNOWNは証拠ではない。空盤 (11x11) はUNKNOWNのまま、全盤への飛躍は行わない。

## 反映した4件 (n11-night-batch1-20261014 の terminal-only receipt, trusted葉0)

| S5索引 | verdict | 探索nodes | DAG nodes / edges / 終局 | receipt | certificate SHA256 |
|---:|---|---:|---|---|---|
| 137694 | LOSS | 3,550,700 | 636,353 / 953,685 / 85,872 | `night-a-137694-receipt.json` | `f6c845fb…` |
| 143240 | LOSS | 4,774,013 | 724,034 / 1,088,867 / 98,414 | `night-a-143240-receipt.json` | `8acbb2a2…` |
| 220231 | LOSS | 3,570,981 | 483,525 / 741,330 / 58,329 | `night-a-220231-receipt.json` | `f33ec92f…` |
| 126017 | **WIN** | 7,151,480 | 1,318,386 / 1,984,060 / 178,988 | `nightb10m-126017-receipt.json` | `29eb8689…` |

全4件で `trusted_leaves=0`・`pruned_roundtrip_verified`・
certificate SHA256 と terminal-DAG 実体の一致・`probe_manifest` との結合を再検証した。
126017 は本系列で2件目の新規独立WIN証拠 (1件目は209644)。

## 二重比較表 (第2次更新と当初 K0423 の両基準)

| 指標 | 当初 (K0423) | 第2次 | 第3次 | Δ 第2次→第3次 | Δ 当初→第3次 |
|---|---:|---:|---:|---:|---:|
| 上界 = 要求S5数 | 31,636 | 31,728 | **31,774** | +46 | +138 |
| 下界 = 整数dual (ceil) | 6,577 | 6,582 | **6,583** | +1 | +6 |
| 区間 | [6,577, 31,636] | [6,582, 31,728] | **[6,583, 31,774]** | — | — |
| 層別済み S5 (WIN+LOSS) | 2 (1+1) | 6 (2+4) | **10 (3+7)** | +4 | +8 |
| 除外 S4 クラス数 | 2 | 5 | **9** | +4 | +7 |
| 再選択した応答数 | 5 | 0 | **3** | +3 | −2 |
| free thirds | 122 | 122 | **122** | 0 | 0 |
| 完全S5境界を再検算した選択S4 | 349 | 350 | **351** | +1 | +2 |
| 第三手網羅 (root×third) | 19 × 2,261 | 19 × 2,261 | **19 × 2,261** | 0 | 0 |
| WIN側 使用可能証人pool (保存1,945) | 1,942 | 1,940 | **1,936** | −4 | −6 |
| WIN側 未閉鎖証人S5 | 1,944 | 1,846 | **1,749** | −97 | −195 |
| WIN側 closable 応手軌道 | 65 | 62 | **59** | −3 | −6 |
| WIN側 unclosable 応手軌道 | [] | [1, 2, 101] | **[1, 2, 4, 15, 79, 101]** | +3件 (4, 15, 79) | +6件 |
| WIN側 and-width (chosen fourths) | 7,519 | 7,165 | **6,812** | −353 | −707 |
| 新規閉鎖 第三手 / 軌道 | — | 0 / 0 | **0 / 0** | 0 | 0 |

## LOSS側 (§4)

- 3件 (137694, 143240, 220231) を既知LOSS子として全cost集合から除外。
  要求unionに既知LOSSが残らないことを表明 (`known_loss_in_union=0`)。
- 126017 (WIN) を未解決子に持つ4 S4クラス
  `[3569, 3570, 4050, 5830]` を除外集合へ追加 (第2次 `[3942, 5408, 5687, 5690, 13938]` → 計9件)。
  うち `5830` は第2次計画で選択済みだったため、3応答 (first=49, reply=60, third=59/61/71) を
  greedy で再選択 (`5830 → 4137, 4137, 2634`)。
- 再選択の追加コスト +106 が3件のLOSS除外効果を上回り、上界は **31,728 → 31,774 (+46)**。
  ranking の反実仮想値 (126017 WIN時 greedy Δ+49、K0423基準) とは基準が異なる。
- 19 root・全2,261 third手・351選択S4の完全境界を独立幾何から再検算し、
  既知WIN要求0件・既知LOSS混入0件を表明 (`verification.passed`)。

## 双対 (下界)

- 厳密 `Fraction`・全選択肢不等式 95,207件 (paid groups 869 / distinct 948 / elements 962,459)、
  `--verify` で証明書を全再構成して一致確認。
- exact total `182461931 / 27720` ≒ 6,582.32 → ceil で **6,583** (第2次 6,582 から +1)。
- dual は候補集合と要素cost義務だけの関数であり、一括反映と両段階反映でそれらが同一
  (下節) であるため、**3反映すべてに同一証明書が成立**する。

## 一括4件反映 vs 段階反映 の一致検査

同じ凍結入力から3通り (batch / staged-forward / staged-reverse) を再計算した。

| 検査 | batch | staged-forward | staged-reverse | 判定 |
|---|---|---|---|---|
| 確定ラベル (resolved verdicts) のsha | 同一 | 同一 | 同一 | **一致** |
| 合法候補 (除外集合+options) のsha | 同一 | 同一 | 同一 | **一致** |
| 証明義務 (cost+options+除外) のsha | 同一 | 同一 | 同一 | **一致** |
| greedy選択 (choices) のsha | 基準 | 同一 | 同一 | 一致 (小差なし) |
| 上界 union_size | 31,774 | 31,774 | 31,774 | **一致 (差分0)** |
| free thirds | 122 | 122 | 122 | 一致 |
| 幾何再検算 (2,261 third / 選択S4完全境界) | passed | passed | passed | 通過 |

順序差による上界のブレは今回0件だった (forward は WIN 追加前の選択を継承して最終段で再選択、
reverse は LOSS除外前のcostで再選択するが、同じ貪欲解に収束)。

## WIN側 (§5)

- 保存pool 1,945 から、層別済み10件のうち 558600 を除く9 mask を除外 → 使用可能 **1,936**。
  本轮の新規除外は4件 (137694, 143240, 220231, 126017)。
  新規証人の創作0件。
- 再最適化前の損傷: 被覆不能 branch **8** / S4クラス **8** / affected replies `[1, 2, 4, 15, 79, 101]`。
  内訳は第2次からの既存4件 (r=1,2,101) ＋ 本轮3件のLOSS証人除去による5件
  (r=4 ← 137694、r=15 ← 143240、r=79 ← 220231、うち1 branchは他証人で救済)。
  126017 の除去による損傷は0件 (当該4 branchは WIN子により FREE化)。
- 再最適化後 (全65軌道 × 全119 third を幾何から再列挙):
  closable **62 → 59**、unclosable `[1,2,101] → [1,2,4,15,79,101]`、
  and-width **7,165 → 6,812**、未閉鎖証人 **1,846 → 1,749 (−97)**。
  新閉鎖 (chosen thirdが全fourth無料) は第2次から/当初からとも **0件**。
  FREE S4クラスは 16 → 21 (126017 WIN の効果) だが、応手軌道単位の無料化には至らなかった。
- 全59軌道の cover を保存pool内で再検証し `verification.passed` (failures 0)。
  全 witness が cache済みキーでないこと、pool外不使用、dead/open fourthの整合を確認。

### ranking との照合 (n11-conflict-ranking-20261013 の反実仮想を独立幾何で再計算)

| S5 | verdict | ranking (K0423基準) | 本実験の再計算 | 判定 |
|---:|---|---|---|---|
| 126017 | WIN | 選択3 / FREE 18 branch / greedy Δ49 | 選択3 (S4=`5830`) / 除外options 4 / FREE 18 branch (r=59,60,71) | **一致** |
| 137694 | LOSS | FREE 2 / 証人欠落2 / Δ97 | branch 2 (r=4) / sole-witness 2 | **一致** |
| 143240 | LOSS | FREE 2 / 証人欠落2 / Δ83 | branch 2 (r=15) / sole-witness 2 | **一致** |
| 220231 | LOSS | FREE 2 / 証人欠落1 / Δ40 | branch 2 (r=79) / sole-witness 1 | **一致** |

ranking の greedy Δ は「単独WIN反実仮想」の値であり、本実験の上界Δ (+46) は
3 LOSS除外との合成結果なので直接比較しない。

## 独立証明の累積 (定義を明示して複数を併記)

「累積7/7」の母数が一意でないため、全定義を `effect-measurement3.json`
(`new_facts.cumulative_tallies`) に記録した。

| 定義 | 第2次まで | 第3次 (本轮後) |
|---|---:|---:|
| 本轮 | — | **4/4** (137694, 143240, 220231, 126017) |
| adaptive line の累積 (第1次/第2次READMEの定義) | 4/4 | **8/8** |
| 計画層別 合計 (K0423パイロット込み) | 6/6 | **10/10** |
| 計画層別 **LOSSのみ** | 4/4 | **7/7** |
| 計画層別 WINのみ | 2/2 | **3/3** |
| conflict-closure系 (K0423を除く) | 7/7 | **11/11** |
| 独立receipt総数 (層別外 focus3 を含む) | 9/9 | **13/13** |

層別外のまま保持している3件 (115540 LOSS / 144193 LOSS / 144311 WIN) は
どの計画にも反映していない (本実験の指示範囲外)。
並行実験 `n11-night-batch2-20261014` が取得した 197665 WIN receipt も
本実験の入力範囲外のため、上記の各tallyには含めていない。

## 結果census

- 28 conflict候補のうち層別10件: WIN `[126017, 144095, 209644]` / LOSS `[558600, 126899, 121263, 145001, 137694, 143240, 220231]`。
- 未知20件 (層別外3件を含む)。`144019` / `144692` (UNKNOWN@10M) / `197665` (UNKNOWN@10M) は扱い不变。
- 空盤 (11×11) は UNKNOWN。全盤への飛躍は行っていない。
- 上界は「最適証明計画」ではなく greedy な楽観計画であり、root証明ではない。

## 保存パス

| 内容 | パス |
|---|---|
| 第3次 修復済み両計画 (batch反映・batch_vs_staged・ranking照合込み) | `output/repaired-joint-plan-update3.json` |
| 更新後 element-only dual (厳密Fraction・全選択肢不等式) | `output/updated-element-dual-update3.json` |
| WIN側 再解析 (ranking照合・pre-optimisation損傷込み) | `output/win-side-reanalysis3.json` |
| 効果測定 (二重基準・累積tally・census) | `output/effect-measurement3.json` |
| 実行ログ | `output/{plan-update3,dual,dual-verify,win-side,effects}-run.log` |
| スクリプト | `scripts/{update_loss_plan,update_dual,update_win_side,measure_effects}.py` |

第2次以前の出力 (`n11-adaptive-plan-update2-20261013/`, `n11-s5-s6-quotient-20261013/` 等) は
読み取り専用で使用し、一切書き換えていない。

## 次バッチへの申送り

- **WIN側の unclosable が3件増えた (r=4, 15, 79)**: 137694 / 143240 / 220231 が
  保存証人pool内で当該応手の唯一の未知証人だった。全119 thirdを再列挙しても
  viability zero のため、**代替thirdの獲得には新規S5証明 (未知S5のWIN) が必要**。
  未着手候補 (120370, 143718, 157861, 181624, 221294 ほか9件) が候補。
- **層別外3件 (115540 LOSS / 144193 LOSS / 144311 WIN) の扱いが未決**。
  保存証人poolに両LOSS maskが残っており、現在のWIN側coverのうち
  reply 0 が 115540 (2 branch)、reply 46 が 144193 (2 branch) に
  **未知証人としてのみ依存している** (計4 branch)。focus receiptを層別すれば
  この4 branchは被覆不能になり、reply 0 / 46 も unclosable 化する可能性が高い。
  計画更新実験で focus3 を層別するかどうかの判断を先に要する。
- **上界が +46 増加した**: LOSS3件のcost除外効果を、126017 WINによる4 S4除外→
  3応答のgreedy再選択 (+106) が上回った。greedyが飽和している兆候であり、
  再選択を局所交換/全体最適化に置き換えれば上界を下げられる余地がある。
- **下界は 6,582 → 6,583 の +1 のみ**。要素dualは新規WIN/LOSSの追加に対して
  ほとんど動かない。下界を動かすには要素以外の制約 (group/第三手単位) の追加が要る。
- **UNKNOWN据え置き**: 144019 / 144692 はUNKNOWN@10Mのまま (同一条件再探索禁止)。
  197665 については並行実験 `n11-night-batch2-20261014` が25M予算拡張runで
  10,294,083 nodesでSOLVEDし **WIN の独立receipt** (`nighta25m-197665-receipt.json`,
  trusted_leaves=0・pruned roundtrip ✓) を取得済み。**本実験では未層別**
  (本実験の指示範囲は batch1 の4件のみ) のため、次回のplan-updateで反映対象になる。
  ranking上は 126017 と同一block (WIN時18分岐FREE・3選択invalidated) なので、
  反映時の挙動は本実験の126017と同型の見込み。
  batch2 の Task B では 206386 / 166171 / 142283 / 137043 の4件が2Mで UNKNOWN@NODE_LIMIT。
- 126017 と同型の「WIN時18分岐FREE」block (157861, 181624) は本件で3件中0件しか
  FREE化しなかった。block内の追加WIN (197665 など) が軌道単位の閉鎖に寄与するかは
  次回反映で確認を要する。

## 再現 (repo root)

```sh
uv run --locked python research/experiments/n11-night-plan-update3-20261014/scripts/update_loss_plan.py
uv run --locked python research/experiments/n11-night-plan-update3-20261014/scripts/update_dual.py
uv run --locked python research/experiments/n11-night-plan-update3-20261014/scripts/update_dual.py \
  --verify research/experiments/n11-night-plan-update3-20261014/output/updated-element-dual-update3.json
uv run --locked python research/experiments/n11-night-plan-update3-20261014/scripts/update_win_side.py
uv run --locked python research/experiments/n11-night-plan-update3-20261014/scripts/measure_effects.py
```

`update_win_side.py` の出力は `seconds` 以外はバイト一致 (再実行で確認済み)。
既存の check_trace 実体・solver論理は読み取り専用で使用し、raw solver labelは
solver-trustedのまま、証拠への昇格は terminal-only receipt のみが行う。UNKNOWNは昇格しない。
