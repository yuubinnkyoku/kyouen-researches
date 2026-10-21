# 根全体128ノードのP/N予算を複数局面へ配る比較

K0499では広い閾値でも最初の難しい残余局面でquotaを使い切った。
通常df-pn専用の明示オプション`--residual-attempt-budget=N`を追加し、
1回のP/N呼出しに渡す予算を`min(N, root残量)`に制限する。
実使用数だけroot残量から差し引く。省略時は従来のroot残量全体を使う。

上限指定時は、同じroot内で同じcanonical boardを再試行しない。
この集合はdf-pnと内部native exact handoffで共有し、root開始時に消去する。
UNKNOWNを勝敗cacheへ書かない。確定P/Nの採用と元の手番への変換は従来通り。
SG shadow crosscheckはこの試行抑制やP/N quotaを使わない。

## 固定プロトコル

- 根全体quota128、合法手数の閾値18を固定する。
- 調整はK0499の深い9局面。OFF・従来方式・1回8・1回32、2万work、各3反復。
- 8/32の候補はUNKNOWN根数、局面ごとの展開数中央値合計、時間中央値合計、capの順で最小化。
- 確認用の安全な5石6局面はseed2026102202で調整前に生成し、調整用とのD4重複を除く。
- 選択をcommitした後、OFF・従来方式・選択候補を2万/10万workで各3反復。
- 既知終盤26局面を同じ3設定・2万workで各1回検査する。新しいholdoutや時間比較とは呼ばない。

各評価はfresh process/TT、memo=18、native exact handoffなし、wall guard30秒。
通常workはdf-pnフレーム反復とnative exact board nodeの合計であり、P/N quotaは別枠。
新しい深い根の勝敗が確定した場合は停止し、独立検証してから採用する。
残余評価の既定OFFと、cap省略時の挙動は維持する。

## 再現・監査

```sh
g++ -std=c++20 -O2 cpp/solvers/kyouen_dfpn_root.cpp -o /tmp/dfpn-attempt
python research/experiments/residual-attempt-allocation-20261022/study.py freeze
# frozen入力をcommit
python research/experiments/residual-attempt-allocation-20261022/study.py train
# training.json / selection.jsonをcommit
python research/experiments/residual-attempt-allocation-20261022/study.py confirm
python research/experiments/residual-attempt-allocation-20261022/study.py verify
python research/experiments/residual-attempt-allocation-20261022/cli_test.py --solver /tmp/dfpn-attempt
python -m unittest discover -s research/experiments/residual-attempt-allocation-20261022 -p 'test_*.py'
```

記録を上書きしない。新しい比較には新しいexperimentを作る。
CIで行うのは小盤回帰と記録の再検査だけで、この探索をpushで再実行しない。
