# 11×11 reply27：S5の全S6子を独立分割してWINまで閉じた実験

対象：標準共円ゲーム11×11、二石root `{60,27}` のみ。開始時の最新mainは `581e72c277d05149b847d997c47a15bfc77a36c7`。今回の勝敗は**元の先手固定視点**で、探索solverが返した葉の勝敗を信頼し、その上位の合法境界とAND/OR伝播を独立検証したものである。terminal-only minimaxで90葉を再証明したものではない。

## 主結果：直接15M UNKNOWNだったS5を、全子S6 WINで証明

対象S5 `(1188950301626859520,603979776)` は、別担当の直接15,000,000-node exact replayでUNKNOWNになっていた。今回、既存の完全合法S6境界を独立整数幾何 `independent.Board` で再構築し、**90個**の異なるcanonical S6子を得た。

- 最初の3つ（legal=60,63,64）は2M budgetですべてdirect S6 WIN。
- legal帯別に選んだ15個は1M budgetですべてdirect S6 WIN。
- 残り72個を1M budgetで全件検査し、67 WIN / 5 UNKNOWN。
- 上限到達の5局面のみ15M budgetで再試行し、**5個ともdirect S6 WIN**。

したがって全90子がexact WIN、未確定S6は0。石数5のAND境界について `WIN iff 全S6子WIN` が成立し、対象S5は**WIN**。このS5を合法な子とする次の2つのS4 classは、石数4のOR則で **WIN** と確定した。

| S4 class | coverage | 新しい結果 |
|---|---|---|
| `(1188950301626859520,536870912)` | `{55,65,100,108}` | UNKNOWN → WIN |
| `(1188950301776805888,0)` | `{24,30,55,65}` | UNKNOWN → WIN |

検証済みraw S6試行の総計は **29,794,287 nodes**（最初の1M打切り5件とその15M再試行を両方含む）。直接S5の15M UNKNOWNと同程度の計算量ではないが、直接では不明だった局面について**確定値が得られた**ことが重要。この成果は「90子を1個ずつ、別々のfresh solverでexact判定し、上位で独立に全子条件を閉じる」方法の実用性を示す。

S6のWIN値は正しい極性を保つ。**S7 LOSSが一件見つかってもS6 LOSS/WINを導けない**。S6 LOSSには完全な全S7子LOSSが必要。今回のS6 WINは既存の修正済みsolverによるdirect raw exactであり、上位のS5 WINは独立な合法境界検査で導出した。

## S5二局面を対象とした記憶共有の比較

先行実験で有望とされた2件の共有S5（legal 95と96）について、同一bin・同一budget・同じ順序・単一workerで、2Mと15Mの**cold別root**／**shared TT**を比較した。結果は2件ともS5 LOSS、cold直接実行でも再確認した。

| S5 key | cold 15M探索nodes | shared TT探索nodes | 結果 |
|---|---:|---:|---|
| `(1152921504606851072,805306370)` | 5,925,730 | 5,925,730 | LOSS |
| `(1188950301626859520,671088640)` | 4,399,355 | 4,352,188 | LOSS |
| **合計** | **10,325,085** | **10,277,918** | 2 LOSS |

node削減率は **約0.46%**。この組に対する実測効果は小さく、一般の全探索への外挿はできない。rawではcoldとsharedで同じverdictを返した。2Mの各試行はすべてUNKNOWNで、正確な判定には加えて15M実行を要した。S5ベンチ全実行nodesは28,603,003（4M cold pilot + 4M shared pilot + 10,325,085 cold15M + 10,277,918 shared15M）。

## 最新の証明frontier

開始cacheは `current-exact-s5-after-probe-9-rebased-main.cache` の5,749 exact S5（WIN158 / LOSS5,591）。新規2件の直接S5 LOSSと1件のS6全子条件由来S5 WINを統合すると、

| 指標 | 結果 |
|---|---:|
| exact S5 total | **5,752** |
| S5 WIN / LOSS | **159 / 5,593** |
| verdict conflict | 0 |
| S4 LOSS / WIN / UNKNOWN | **31 / 274 / 3,079** |
| 第三手被覆 | 117/119 |
| 未被覆 | `{100,108}` |
| 最小追加LOSS class | 1 |
| 有理LP双対値 | 1 |

上位exact S5の全件がterminal-only独立証明書を持つわけではなく、既存cacheにはcache-only根拠がある。今回の新しいS6 90 exactの直接rawと上位境界の健全性とを区別する。

## 次に探索すべきclass

新cacheでの全115対象候補の更新は `output/new-ranking/candidate-classes.csv` にある。WIN54、UNKNOWN61、LOSS0。次のUNKNOWN最小／15M打切り参考費用最小は、

```
S4: (1297036692683752448,0)
S5 boundary: 106 children
known LOSS: 7
UNKNOWN: 99
WIN: 0
coverage: {100,108,110,120}
```

合法手数の少ないUNKNOWN S5：

- `(10412322338480590849,0)` legal84、現historyに高budget UNKNOWNなし（単class所属）
- `(1297036692750861312,0)` legal92、生存class `(1297036692750860288,0)` と共有（2親）
- `(1301540292311122944,0)` legal94、生存class `(1301540292311121920,0)` と共有（2親）

優先順は目的次第。低legalは早期WIN棄却の可能性を評価する候補、共有S5は他classへ同時寄与し得る候補。いずれも**順位は勝敗証明ではない**。開始前に最新main、raw、2M/15M UNKNOWN、S6/S7既存証拠、他担当targetを再確認する。同じ対象のsolverを重複実行しない。

過去履歴の15M打切り参考費用は、新最上位classで約546,960,118 nodes。これは条件付きの参考指標で、LOSS完成に必要な予測時間や上界ではない。

### 新たな探索順序の提案

直接S5を2M・15Mで段階探索し、依然UNKNOWNの局面を単に大budgetへ上げる前に、完全S6境界の合法手数分布・cache交差を計算する。その後S6を1Mなど小budgetで個別に解き、UNKNOWNだけ増額する。**S6 LOSSが1件ならS5 LOSS**、**全S6 WINならS5 WIN**である。後者が見つかったclassの残りS5を即時停止し、全3384 classの逆方向反映と119第三手被覆を再計算する。この方法が全局面に勝つことはまだ実証していないので、まずは保存rawの再生と少数対照実験で評価する。

## 実験再現と独立監査

`output/raw/` の21ファイルはbyte-preservingに保存しており、全SHA-256を `output/audit.json` に記録した。source hash `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`。solverはIntel i5-9400T、Debian g++14.2.0、`-O3 -std=c++20 -DNDEBUG`、`--n=11 --memo=22 --exact-order=count`、1 workerで実行。

```sh
python3 research/experiments/n11-s6-universal-closure-20261011/scripts/audit.py
python3 -m unittest discover -s research/experiments/n11-s6-universal-closure-20261011/tests -v
python3 research/experiments/n11-two-target-design-20261010/scripts/analyze.py \
  --cache research/experiments/n11-s6-universal-closure-20261011/output/merged-exact-s5.cache \
  --out research/experiments/n11-s6-universal-closure-20261011/output/new-ranking
```

`audit.py` は独立 `Board` で全90個のS6子の安全性・canonical・legal手数・完全列挙集合一致を照合し、全raw出力のverdict・budget・同一子への再試行を確認する。改ざんテストとしてS6 WIN値をLOSSに変える、rawの1子を落とす、極性を誤る変更を拒否する。UNKNOWNをexactとしてmergeしない。

**注意**：親S5/S4の論理境界は独立監査済みだが、90個のS6 raw WIN自体はsolver信頼の葉であり、全員のterminal-only minimax DAGは未生成。これはK0372の独立性区分に従う。
