# 11×11 reply27：最有力S4の残り86 S5から20件をdirect exact LOSSと判定（2026-10-11）

標準共円ゲーム、11×11、二石root `{60,27}`。今回の開始時`main`は `1c2c010762e2e781ce04ed7d00e8592fc114776e`。既存のK0355と [前回10 S5 LOSS実験](../n11-reply27-ten-loss-20261011/README.md) を踏まえて、まだ未確定だった第三手 `{100,108}` の被覆を前進させる。

## 実験条件と選定

最優先S4 class：`(1297036692683752448,0)`、第三手coverage `{100,108,110,120}`、完全canonical S5子106件。開始時 **LOSS20 / WIN0 / UNKNOWN86**。

`shared-s5-tasks.csv`からこのS4に属する未確定S5を抽出し、合法手数の少ない**単一生存S4所属10件**、別の生存S4にも属する**共有10件**を選択した（選択順序・条件は `output/selection.json`）。先に幾何エンジン`independent.Board`で石数5・D4 canonical・合法手数を照合し、10組の2局面ずつを独立した入力CSVに固定した。

**cold exact replay**は前回実験と同一のsolver binary SHA256 `2878dc74ab1228c1bba6b13140dcd8f65f457f9813ae98d801a1709c77497ee5`を使用。元ソースの基準はmain `f33693cdd8be54738cedea8fc141553209c9a669`。当時のビルドは `g++ -O3 -std=c++20 -DNDEBUG cpp/solvers/kyouen_dfpn_root.cpp`。追加の証明DAG capture、cache preload、cross-query TTは使わず、1行ずつ冷たい状態で厳密判定した。

```sh
.local/reply27-next/dfpn --n=11 --memo=22 --only=5 \
  --exact-order=count --exact-replay=output/raw/target-00.csv \
  --exact-replay-budget=15000000 --csv=output/raw/probe-00.csv
```

`target-00.csv`・`probe-00.csv` は例示した相対パス。全10組は`target-00.csv`〜`target-09.csv`と`probe-00.csv`〜`probe-09.csv`として本experimentの `output/raw/`に保存してある。

## 新しい20件のexact verdict

| Batch | 単一生存S4所属：S5合法手数 / 直接判定nodes | 共有生存S4所属：S5合法手数 / 直接判定nodes |
|---|---:|---:|
| 00 | 93 / 5,461,211 LOSS | 96 / 4,133,815 LOSS |
| 01 | 93 / 3,182,164 LOSS | 96 / 6,137,538 LOSS |
| 02 | 93 / 2,973,580 LOSS | 96 / 2,745,800 LOSS |
| 03 | 94 / 3,823,653 LOSS | 97 / 3,638,190 LOSS |
| 04 | 94 / 3,504,651 LOSS | 97 / 4,292,117 LOSS |
| 05 | 94 / 4,597,825 LOSS | 97 / 4,352,577 LOSS |
| 06 | 94 / 3,353,183 LOSS | 97 / 5,975,893 LOSS |
| 07 | 94 / 4,720,547 LOSS | 97 / 2,691,082 LOSS |
| 08 | 95 / 3,964,389 LOSS | 97 / 5,002,748 LOSS |
| 09 | 96 / 2,996,288 LOSS | 97 / 4,259,034 LOSS |

- **直接exact LOSS20件、WIN0件、UNKNOWN0件**。いずれも15M nodesに到達せず確定。
- 完了したsolver rawの計算量合計は **81,806,285 nodes**。今回の20件では2M予備探索やtimeout再試行は行っていない。
- 合法なcanonical S4→S5完全子境界と、既存exact cacheの矛盾0件を確認した。

## 更新後の厳密境界

| 指標 | Before | After |
|---|---:|---:|
| exact S5 cache | 5,765 | **5,785** |
| S5 WIN / LOSS | 159 / 5,606 | **159 / 5,626** |
| 対象S4 106子の LOSS / WIN / UNKNOWN | 20 / 0 / 86 | **40 / 0 / 66** |
| 全3,384 S4の LOSS / WIN / UNKNOWN | 31 / 274 / 3,079 | 31 / 274 / 3,079 |
| 第三手被覆 | 117/119 | 117/119 |
| 未確定第三手 | `{100,108}` | `{100,108}` |

対象S4はなおUNKNOWN。必要な追加LOSS class最小数1と有理LP双対値1も不変。

`analyze.py` による更新rankでは本S4が引き続き1位で、未解決S5 66件のうち共有生存S4に属するものは45件。全61件の関連UNKNOWN S4の比較において、このS4の未確定子数は最小。liveなUNKNOWN S5 keyは4,505件（1親2,692 / 2親1,813）。履歴cost proxyは約374,787,214 nodesだが、完了するまでの上限や所要時間の予測ではない。

## 独立監査・再現性・証明信頼境界

`scripts/audit.py` がsolverと独立した`independent.Board`で、20 canonical局面の石数・合法手数・S4親子合法遷移・完全106子境界を再検算。rawの位置・予算・solver verdict・節点数を相互照合、隔離対象を拒否したcacheのみをmergeし、さらに全3,384 S4を再計算して全候補第三手の被覆を確認する。

`tests/test_audit.py` は完全再監査、AND/OR勝敗極性、偽造WIN行、行欠落、合法手数改ざん、占有bitmask改ざんの計6件。raw原本には手を触れず、一時複製のみに改ざんを注入してfail closedを検査した。

```sh
python3 research/experiments/n11-reply27-20more-20261011/scripts/audit.py
python3 -m unittest discover -s research/experiments/n11-reply27-20more-20261011/tests -v
python3 research/experiments/n11-two-target-design-20261010/scripts/analyze.py \
  --cache research/experiments/n11-reply27-20more-20261011/output/merged-exact-s5.cache \
  --out research/experiments/n11-reply27-20more-20261011/output/new-ranking
```

監査receiptおよびrawのSHA-256は `output/audit.json`、完全cacheは `output/merged-exact-s5.cache`、正確な20対象と全S4 rankingは `output/selection.json` および `output/new-ranking/` に固定した。

**重要な境界**：新規20件はraw solverによるdirect exact LOSSであり、独立整数幾何はその上位境界と再現データを検証している。終局までのterminal-only proof DAGはこの20根に対して生成・検証していない。11×11空盤および二石rootの勝敗は引き続きUNKNOWN。
