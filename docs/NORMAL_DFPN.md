# 通常df-pnの有限探索と子局面再利用

共有実装は`cpp/solvers/kyouen_dfpn_root.cpp`。repo rootから実行する。
現在の検証範囲と速度の根拠は[K0501](../research/knowledge/items/K0501-dfpn-frame-child-geometry-reuse.md)、
終盤P/N設定の根拠は[K0497](../research/knowledge/items/K0497-small-residual-quota-prospective-confirmation.md)と
[K0498](../research/knowledge/items/K0498-normal-dfpn-bounded-residual-handoff.md)を参照する。

## ビルドと小盤確認

```sh
g++ -std=c++20 -O2 -DNDEBUG cpp/solvers/kyouen_dfpn_root.cpp -o /tmp/kyouen-dfpn
/tmp/kyouen-dfpn --n=4 --empty --memo=12 --node-budget=20000 --budget=5 \
  --frame-children-expand-reuse \
  --log=/tmp/dfpn-n4-fast.log --csv=/tmp/dfpn-n4-fast.csv
```

4×4空盤の既知結果は元先手LOSS。ログとCSVは追記されるので、試行ごとに別名を使う。
省略時のフレーム再利用・残余評価・native exact handoffはいずれもOFF。

## 通常探索で使う指定

| 目的 | 追加する指定 |
|---|---|
| 展開直後と再訪時の幾何再構築を省く | `--frame-children-expand-reuse` |
| 再訪時だけ再利用する旧方式との比較 | `--frame-children-cache` |
| 再利用した各リストを作り直して照合 | 上記に`--frame-children-audit`を追加 |
| 終盤のbounded P/N評価 | `--residual-exact-legal=6 --residual-evaluator=outcome --residual-outcome-budget=128` |

初回移譲の指定は再訪時の再利用も有効にする。監査は追加計算を行うので、時間比較では外す。
残余P/Nとの併用も検証したが、各最適化の短縮率を足したり掛けたりできるという意味ではない。

次は保存済みの既知11×11終盤を使う、有限な実行例である。

```sh
/tmp/kyouen-dfpn --n=11 --memo=18 \
  --roots-csv=research/experiments/dfpn-expand-children-20261022/roots/late-0.csv \
  --node-budget=100000 --budget=30 --exact-legal=0 \
  --frame-children-expand-reuse \
  --residual-exact-legal=6 --residual-evaluator=outcome --residual-outcome-budget=128 \
  --log=/tmp/dfpn-n11-late-fast.log --csv=/tmp/dfpn-n11-late-fast.csv
```

独自入力の`--roots-csv`は次の形式で、親の点番号列と最後の1手を与える。
以下は**4×4用**。点番号は`y*N+x`なので、盤面サイズを変えてそのまま転用しない。

```csv
canonical_parent,move
"0,1,2,4",9
```

## native exactとの併用

動作確認用の小さいhandoff設定は以下。根とその子の合法手数が8以下になったら、
1回8 native board nodes、retry設定2でexact handoffを試す。
retry情報はTT項目に保持するので、追い出しをまたぐ根全体の厳密な呼出し回数上限ではない。
これは深い11×11探索に対する閾値・予算の性能推奨ではない。

```text
--exact-legal=8 --exact-budget=8 --exact-retries=2 --exact-publish=all
```

| `--exact-publish` | exactの途中確定結果の扱い |
|---|---|
| `all`（既定） | 通常のPnTTへ保存する |
| `root` | 呼出しごとのlocal cacheを使い、handoff根が確定したらPnTTへ反映する |
| `separate` | solver内で持続する別のexact cacheを使い、handoff根が確定したらPnTTへ反映する |

3方式ともフレーム再利用・SG終盤評価・P/N終盤評価との併用を小盤回帰で照合した。
`--residual-attempt-budget=8`でP/Nを分配する方式も回帰対象だが、深い探索の一般推奨設定にはしていない。
フレーム再利用はP/Nと併用できる。SG成分用の`--residual-share-gate`はoutcome evaluatorとの併用を拒否する。

## 予算と結果の読み方

CSVの`# dfpn_root`行を使う。

| 項目 | 意味 |
|---|---|
| `result=0/1/2` | UNKNOWN / 固定した元先手WIN / 固定した元先手LOSS |
| `reason` | `DONE`、`NODE_BUDGET`、`TIME_BUDGET`等の停止理由 |
| `nodes` | df-pnフレーム反復`visited`とnative exact board nodes`exact_nodes`の合計 |
| `pn_nodes` / `pn_remaining` | 根全体で共有する、別枠のP/N kernel使用数と残量 |
| `geometry_builds` / `child_refreshes` | 子リスト構築数と、幾何を再利用してboundsを読み直した数 |
| `frame_expand_uses` | 展開から移譲したリストを実際に初回利用した数 |

偶数石では元先手、奇数石では元後手が次の手番。`result`を「次の手番の勝敗」と読み替えない。
UNKNOWNや予算切れをLOSSとして保存しない。`--node-budget=0`は通常探索の仕事量を許可しない。
PnTTやseparate exact cacheは同じsolver内の複数根で再利用するが、P/N quota・試行抑制・幾何計数は根ごとにresetする。

`--budget`は探索側のwall guardで、solver初期化を含むprocess全体の時間上限ではない。
外側からprocess全体も制限したい場合は、別途実行環境側のtimeoutを使う。
監査で追加したfresh-list構築も`geometry_builds`に入る。

## 独立検証と回帰

CSVの勝敗行は独立検査済み証明書ではない。
proof DAGの取得は既存のexact replay経路を使い、フレーム再利用の3オプションは付けない。
これらは`--exact-replay`、quant、cover、coord等との混用を拒否する。
証明書と信頼境界は[CERTIFICATE_FORMAT](CERTIFICATE_FORMAT.md)と[PROOF_STATUS](PROOF_STATUS.md)を参照する。

小盤回帰を実行する場合はassertを有効にしたままビルドする。

```sh
g++ -std=c++20 -O2 cpp/tests/test_kyouen_frame_children.cpp -o /tmp/test-frame-children
/tmp/test-frame-children
python research/experiments/dfpn-combined-options-20261022/study.py verify
```

上のverifyは保存した既知局面の記録を再検査する。深い未知盤の探索を再実行しない。
