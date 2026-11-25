# df-pnフレーム内の子局面幾何の再利用

通常df-pnは同じフレームの再集計で`gen_into`を呼び、盤面変換・追加禁止手・canonical key・
対称な子の重複除去を再計算していた。`--frame-children-cache`指定時は、フレームが所有する
最初の子リストを保持し、再集計では子の証明数・勝敗だけをTTから読み直す。
TTのslot番号は保存しない。追い出された項目は従来と同じterminal/OPEN初期値へ戻す。
子の順序、手、元の向きの盤面、合法手数、root-child診断の更新は維持する。
`expand()`の一時リストと各フレームのリストは引き続き別の所有物である。

`--frame-children-audit`はcacheを有効化し、各refreshの直後に新規リストを作って、
子の順序、全8向きの盤面、合法手、canonical key、証明数、勝敗、診断用初期値まで照合する。
監査は時間比較から分離する。既定は従来方式のまま。

## 事前固定した比較

- 既存の深い9局面、新規の安全な5石6局面、既知終盤26局面。
- 新規局面はseed2026102203で作り、K0500の調整・確認15局面とD4重複を除く。
- OFF/cacheの2設定、深い局面は2万/10万work、終盤は2万work、各3反復。
- 各評価はfresh process/TT、memo=18、wall guard30秒、native exact・残余評価はOFF。
- パラメータ選択は行わず、入力とbinary/source hashをcommitしてから計測する。
- 勝敗・停止理由・訪問数・展開数は設定間で完全一致を要求する。
  OFFのgeometry build数 = cacheのbuild数 + refresh数も検査する。
- 旧9局面の先頭3件は2,000 workで別途fresh-list監査する。時間比較には含めない。
- 新たな深い勝敗が出たら停止し、独立検証してから採用する。

`geometry_builds`は全`gen_into`呼出し数（expandやnative exactからの呼出しも含む）。
`geometry_moves`は幾何を計算した合法手候補数で、対称な重複の除去前に数える。
`child_refreshes`は再利用したリスト数、`child_audits`はfresh-list照合数。いずれもroot開始時にresetする。
通常workはdf-pnフレーム反復とnative exact board nodesの合計で、生成回数とは別である。

## 再現

```sh
g++ -std=c++20 -O2 cpp/solvers/kyouen_dfpn_root.cpp -o /tmp/dfpn-frame
python research/experiments/dfpn-frame-children-20261022/study.py freeze
# 固定入力をcommit
python research/experiments/dfpn-frame-children-20261022/study.py run
python research/experiments/dfpn-frame-children-20261022/study.py verify
python research/experiments/dfpn-frame-children-20261022/cli_test.py --solver /tmp/dfpn-frame
python -m unittest discover -s research/experiments/dfpn-frame-children-20261022 -p 'test_*.py'
```

記録を上書きしない。CIでは小盤回帰と記録の再検査だけを行い、この探索はpushで再実行しない。

固定比較の全表は`comparison.md`、現行の採用範囲は
[K0501](../../knowledge/items/K0501-dfpn-frame-child-geometry-reuse.md)を参照。
