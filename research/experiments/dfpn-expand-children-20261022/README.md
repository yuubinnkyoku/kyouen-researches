# 展開リストの所有権を同じフレームへ引き継ぐ

前回の`--frame-children-cache`は再訪時の再構築を避けるが、expand直後の初回構築は重複していた。
`--frame-children-expand-reuse`はexpandが新規に確保したGenのunique_ptrをそのフレームだけへ移す。
親子のリストを共有せず、フレームが破棄されれば解放する。この指定はframe cacheも有効にする。

expandのTT acquireによる追い出しやnative exactによる更新があり得るため、
初回利用時にも子のpn/dn/stを局面キーから再読出しする。
`--frame-children-audit`を併用すると初回を含む各refreshをfresh-listと照合する。
`frame_expand_uses`は移譲したリストを実際に初回再利用した数で、rootごとにresetする。
途中のexact handoffで解決した場合など、移譲後に一度も使わないリストはこの数に含めない。

## 事前固定の比較

- 旧深い3局面、新規安全5石6局面、既知終盤26局面。
- seed2026102204。新規6局面は直前2比較の既存深い局面とD4重複を除く。
- OFF・前回cache・今回expand reuseの3方式、各3反復。
- 深い根は2万/10万work、終盤は2万work、memo18、wall guard30秒、fresh process/TT。
- native exact・残余評価はOFF。新しい深い勝敗が出たら停止し、独立検証してから採用する。
- 旧3根を各2,000 workでexpand+fresh-list監査し、時間比較から分離する。
- 全3方式の勝敗・停止理由・探索量一致と、cache builds = expand builds + 初回再利用数を検査する。
- パラメータ調整は行わず、source/binary hashと入力をcommitしてから計測する。既定は全てOFF。

前回experimentの純粋な検査関数をimportlibで読み込み、そのhashも固定する。
旧ファイルを変更せず、新しい記録はこのexperimentに保持する。

```sh
g++ -std=c++20 -O2 cpp/solvers/kyouen_dfpn_root.cpp -o /tmp/dfpn-expand
python research/experiments/dfpn-expand-children-20261022/study.py freeze
# 入力をcommit
python research/experiments/dfpn-expand-children-20261022/study.py run
python research/experiments/dfpn-expand-children-20261022/study.py verify
python research/experiments/dfpn-expand-children-20261022/cli_test.py --solver /tmp/dfpn-expand
```

記録を上書きせず、CIで実行するのは小盤回帰と記録の再検査だけとする。

固定結果は`comparison.md`、現行の採用範囲は
[K0501の追加検証](../../knowledge/items/K0501-dfpn-frame-child-geometry-reuse.md#初回展開リストの所有権移譲による追加検証)を参照。
