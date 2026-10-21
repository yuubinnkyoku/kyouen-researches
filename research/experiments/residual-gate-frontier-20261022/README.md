# 通常df-pnの残余切替閾値と未発火の診断

K0498の深い3局面で残余呼出しが0だった理由を調べる。
実装の`--residual-profile`指定時に限り、未解決stage-0 frameの合法手数ヒストグラムを出力する。
解決済みTT frameは除外し、未解決frameの再訪は数える。ユニーク局面数ではない。
同一solverで複数rootを処理した場合も、出力はrootごとの差分である。

## 事前に固定する範囲

- 調整: K0498の深い3局面、通常work上限20,000、3反復。
- 設定: OFFと閾値6/12/18/24/32/48/64、各根のP/N quota128。
- 診断: 同じ3局面をOFF・profile ON・100,000 workで各1回。時間比較とは分離する。
- 候補選択: 閾値12以上からUNKNOWN根数、局面ごとの探索時間中央値合計、閾値の順で最小化。
- 確認: seed20261022で独立に生成した安全な5石6局面。旧3局面とD4同値を除外。
  選択をcommitした後、OFF・閾値6・選択候補を20,000/100,000 workで各3反復。
- 正しさ: 以前の既知終盤26局面を同3設定・20,000 workで各1回。新しいholdoutとは呼ばない。

各評価はfresh process/TT、native exact handoffはOFF、memo=18、wall guard30秒。
P/N quotaは通常workとは別枠。quota切れはUNKNOWNとして通常探索へ復帰する。
通常workはdf-pnフレーム反復とnative exact board nodeの合計であり、展開数とは異なる。
新たな深い勝敗が確定した場合は停止し、独立検証を済ませてから採用する。
既定の残余評価はOFFを維持する。長時間探索workflowは追加しない。

## 再現

記録済みファイルを上書きしない。新しい比較は別experimentで行う。

```sh
g++ -std=c++20 -O2 cpp/solvers/kyouen_dfpn_root.cpp -o /tmp/dfpn-gate-profile
python research/experiments/residual-gate-frontier-20261022/study.py freeze
# protocol.json / fixtures.json / rootsをcommit
python research/experiments/residual-gate-frontier-20261022/study.py train
# training.json / selection.jsonをcommit
python research/experiments/residual-gate-frontier-20261022/study.py confirm
python research/experiments/residual-gate-frontier-20261022/study.py verify
python -m unittest discover -s research/experiments/residual-gate-frontier-20261022 -p 'test_*.py'
```

CIでは記録の再検査と小さい回帰だけを実行し、この研究探索は再実行しない。
