# n11 adaptive plan update: S5 126899 LOSS / 144095 WIN の両証明計画への反映

基準: 最新main・clean基盤＋未コミット2実験（adaptive-probe / adaptive-verify）。
本実験は既存実験・knowledge正本・生成物・共有solver論理を一切変更せず、
`research/experiments/n11-adaptive-plan-update-20261013/` に結果を分離保存する。

## 入力として固定した確定結果

いずれも `n11-adaptive-verify-20261013/output/pilot-{receipt,terminal-dag.json.gz}`
の trusted葉0・pruned roundtrip済み独立終局検証receiptに依存する。

| S5索引 | 元先手結果 | solver探索nodes | receipt |
|---:|---|---:|---|
| 126899 | LOSS (verdict=2) | 3,184,967 | `pilot-126899-receipt.json` |
| 144095 | WIN (verdict=1) | 4,152,553 | `pilot-144095-receipt.json` |

K0423の558600 (LOSS)・209644 (WIN) も同一のtrusted葉0 receiptから取り込む。
既存の K0423パイロット、focus/next既存出力、履歴は上書きしない。

## 手順 (§4準拠、推定補完なし)

1. **現行入力の読み取り**: `n11-s5-s6-quotient-20261013/output/repaired-joint-plan.json`
   (上界31,636)・`updated-element-dual.json` (下界6,577)、
   `n11-conflict-ranking-20261013/output/ranking.json` (28候補の影響表)、
   `n11-proof-cost-comparison-20261012/output/win-side-analysis.json` +
   `win-witness-masks.json` (証人1,945・AND幅7,519)。
2. **LOSS側更新** (`scripts/update_loss_plan.py`): 144095 WINにより当該S5を
   全子LOSSとして要求するS4候補を除外し、`repair_plan.py`と同じ
   決定的greedyで選択修復。126899 LOSSは既知LOSS子として全費用集合から除外。
   19 root・全2,261 third手・350選択S4を幾何から再検算し、既知WIN子なし・
   全要求境界一致・未確定要求31,730を確認。
3. **WIN側更新** (`scripts/update_win_side.py`): 144095 WINを子に持つS4は
   FREE確定、126899 LOSSは死(S4死=資産)。126899・144095・209644をWIN証人
   候補から除外し、保存1,945集合の範囲で全65応手軌道×119 thirdを再被覆
   (`win_side.py`・`win_witness_masks.py`流用、新規証人の創作なし)。
4. **双対下界の再計算** (`scripts/update_dual.py`): `updated_dual.py`流用・
   厳密Fraction・全選択肢不等式95,218件・`--verify`通過。
5. **空盤全体のWIN/LOSSへの飛躍は禁止**。UNKNOWN (144692・144019) の扱いは
   変更しない。

## 結果

### 上下界

| | 前 | 後 | 変化 |
|---|---:|---:|---:|
| 上界 (選択S5要求のunion) | 31,636 | 31,730 | +94 |
| 下界 (厳密element-only双対のceil) | 6,577 | 6,583 | +6 |
| 区間 | [6,577, 31,636] | [6,583, 31,730] | — |

上界は144095 WINで失効した4選択 (すべて旧S4=13938) の再選択で増加。
126899 LOSSで56件が要求から除かれ、150件が追加され純増94。
下界は除外S4増と126899費用除去の純効果で+6。

### WIN側 (初手49)

- 未閉鎖証人数: 1,944 → **1,910** (−34)。保存1,945から209644(WIN)・
  144095(WIN)・126899(LOSS)の3件を除外し、被覆再最適化後の実使用証人数。
- 被覆不能: 応手軌道 **r=2 が不能** (保存証人集合の範囲では119 third全てに
  証人不在のfourthが1つ以上残る。best third t=8 は dead 0・被覆不能 fourth 1)。
  これは独立に全119 thirdを再走査して確認済み。新規証人は創作していない。
- AND幅: 7,519 → 7,401 (r=2の118 fourthが落ちた)。
- 応手軌道: closable 65 → 64、unclosable [2]。
- 新規閉鎖 (第四手が全て144095 WINで無料化されたthird): 0件。144095 WINは
  全whole-thirdを無料化せず、個別fourthのFREE化にとどまった。

### 勝敗census (28衝突候補)

- WIN: 144095, 209644 (2件) / LOSS: 126899, 558600 (2件)
- UNKNOWN: 26件 (144692・144019を含む、扱い不変)
- 独立証明成功: 2/2 (126899・144095ともtrusted葉0 receipt)
- 11×11空盤はUNKNOWNのまま。空盤全体への飛躍は行っていない。

## 保存パス

| 内容 | パス |
|---|---|
| LOSS修復plan | `output/repaired-joint-plan-update.json` |
| 厳密双対証拠 | `output/updated-element-dual-update.json` |
| WIN側再解析 | `output/win-side-reanalysis.json` |
| 効果測定 | `output/effect-measurement.json` |
| WIN側走行log | `output/win-side-run.log` |

## 再現 (repo root)

```sh
python research/experiments/n11-adaptive-plan-update-20261013/scripts/update_loss_plan.py
python research/experiments/n11-adaptive-plan-update-20261013/scripts/update_dual.py
python research/experiments/n11-adaptive-plan-update-20261013/scripts/update_dual.py \
  --verify research/experiments/n11-adaptive-plan-update-20261013/output/updated-element-dual-update.json
python research/experiments/n11-adaptive-plan-update-20261013/scripts/update_win_side.py
python research/experiments/n11-adaptive-plan-update-20261013/scripts/measure_effects.py
```

`update_dual.py --verify` は証拠を再構成して全選択肢不等式を再検査する。
`update_win_side.py` は被覆を独立幾何から再走査し、失敗があれば非0終了する。
具体的DAGのLean内形式検査を意味しない。LOSS planは楽観計画のまま;
WIN側証人は保存集合内の楽観frontierであり、各証人S5自身の全sixths WIN閉鎖は
未証明。境界と勝敗の確定を混同しない。
