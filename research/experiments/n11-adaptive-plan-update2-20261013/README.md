# n11 adaptive plan update 2: S5 121263 LOSS / 145001 LOSS の両証明計画への反映

基準: 最新main・clean基盤＋未コミット3実験（adaptive-verify / adaptive-probe / adaptive-plan-update）。
本実験は既存実験・knowledge正本・生成物・共有solver論理・K0423パイロット・
第1次更新の出力を一切変更せず、`research/experiments/n11-adaptive-plan-update2-20261013/`
に結果を分離保存する。

## 入力として固定した確定結果

いずれも `n11-adaptive-probe-20261013/output/adaptive-{index}-{receipt,terminal-dag.json.gz}`
の trusted葉0・pruned roundtrip済み・manifest trace一致の独立終局検証receiptに依存する。

| S5索引 | 元先手結果 | solver探索nodes | receipt |
|---:|---|---:|---|
| 121263 | LOSS (verdict=2) | 4,687,601 | `adaptive-121263-receipt.json` |
| 145001 | LOSS (verdict=2) | 4,202,236 | `adaptive-145001-receipt.json` |

基盤（第1次更新の出力、上書きしない）:
`n11-adaptive-plan-update-20261013/output/repaired-joint-plan-update.json` (上界31,730)・
`updated-element-dual-update.json` (下界6,583)・
`win-side-reanalysis.json` (証人1,910・r=2不能)・
`effect-measurement.json`。

## 手順 (§4のS5 LOSS側、推定補完なし)

1. **LOSS側更新** (`scripts/update_loss_plan.py`): 121263・145001を既知LOSS子として
   全費用集合から除外。WIN側の判定集合は前回同様 {209644, 144095} なので除外S4集合は
   変わらず再選択は0件。19 root・全2,261 third手・350選択S4の完全境界を幾何から再検算し、
   既知WIN要求0件・要求union内の既知LOSS 0件を表明。
2. **WIN側更新** (`scripts/update_win_side.py`): 保存1,945証人poolから
   209644(WIN)・144095(WIN)・126899(LOSS)・121263(LOSS)・145001(LOSS) の5件を除外
   (allowed 1,942→1,940)し、他の保存証人だけで全65応手軌道×119 thirdの第四手境界を再被覆。
   新規証人の創作は禁止（保存pool内のみ）。
3. **双対下界の再計算** (`scripts/update_dual.py`): 厳密Fraction・
   全選択肢不等式95,218件・`--verify` 通過。
4. **空盤WIN/LOSSへの飛躍は禁止**。UNKNOWN (144692・144019) の扱いは変更しない。

## 結果

### 上下界（第1次から / 当初から の二重比較）

| | 当初 (K0423) | 第1次 | 第2次 (本) | 第1次から | 当初から |
|---|---:|---:|---:|---:|---:|
| 上界 (選択S5要求のunion) | 31,636 | 31,730 | **31,728** | −2 | +92 |
| 下界 (厳密element-only双対のceil) | 6,577 | 6,583 | **6,582** | −1 | +5 |
| 区間 | [6,577, 31,636] | [6,583, 31,730] | **[6,582, 31,728]** | — | — |

厳密双対値: 36,490,451 / 5,544 = 6,581.9716… → ceil 6,582。
上界は121263 (選択S4=12359)・145001 (選択S4=14743) の2件が要求集合から除かれた純減。
再選択0件・除外S4追加0件・free thirds 122→122。

### WIN側 (初手49)

| | 当初 | 第1次 | 第2次 (本) |
|---|---:|---:|---:|
| 未閉鎖証人数 | 1,944 | 1,910 | **1,846** |
| allowed証人pool | 1,945 | 1,942 | **1,940** |
| closable応手軌道 | 65 | 64 | **62** |
| AND幅 (fourth) | 7,519 | 7,401 | **7,165** |
| unclosable応手軌道 | [] | [2] | **[1, 2, 101]** |

- **r=2不能: 継続かつ拡大**。保存pool内で第四手境界を覆えない応手軌道が
  1件 (r=2) から3件 (r=1, r=2, r=101) に増えた。これは再最適化前の損傷計測
  (被覆不能S4 4件・被覆不能branch 4件・affected replies [1, 2, 101]) と一致し、
  121263・145001の証人除外が直接の原因。解消はしていない。
- 証人数は 1,910 → 1,846 (第1次から −64、当初から −98)。unclosable軌道が
  証人ゼロになったことでunionから落ちた分が主因。
- 新規閉鎖: 第三手 **0件**・応手軌道 **0件**（第1次から / 当初から の両基準とも0）。
  121263・145001はWINではなくLOSSのため、fourthのFREE化は発生しない。
- 新規証人の創作 0件。全62軌道のcoverを保存pool内で再検証し `verification.passed`。

### 勝敗census (28衝突候補)

- WIN: 144095, 209644 (2件) / LOSS: 121263, 126899, 145001, 558600 (4件)
- UNKNOWN: 24件 (144692・144019を含む、扱い不変)
- 独立証明成功: 本轮 2/2、累積 **4/4** (126899・144095・121263・145001)。
  K0423パイロットreceipt (558600・209644) を含めれば 6/6。
- 11×11空盤はUNKNOWNのまま。空盤全体への飛躍は行っていない。

## 保存パス

| 内容 | パス |
|---|---|
| LOSS修復plan | `output/repaired-joint-plan-update2.json` |
| 厳密双対証拠 | `output/updated-element-dual-update2.json` |
| WIN側再解析 | `output/win-side-reanalysis2.json` |
| 効果測定 | `output/effect-measurement2.json` |
| WIN側走行log | `output/win-side-run.log` |

## 再現 (repo root)

```sh
python research/experiments/n11-adaptive-plan-update2-20261013/scripts/update_loss_plan.py
python research/experiments/n11-adaptive-plan-update2-20261013/scripts/update_dual.py
python research/experiments/n11-adaptive-plan-update2-20261013/scripts/update_dual.py \
  --verify research/experiments/n11-adaptive-plan-update2-20261013/output/updated-element-dual-update2.json
python research/experiments/n11-adaptive-plan-update2-20261013/scripts/update_win_side.py
python research/experiments/n11-adaptive-plan-update2-20261013/scripts/measure_effects.py
```

`update_dual.py --verify` は証拠を再構成して全選択肢不等式を再検査する。
`update_win_side.py` は被覆を独立幾何から再走査し、失敗があれば非0終了する。
具体的DAGのLean内形式検査を意味しない。LOSS planは楽観計画のまま;
WIN側証人は保存集合内の楽観frontierであり、各証人S5自身の全sixths WIN閉鎖は
未証明。境界と勝敗の確定を混同しない。
