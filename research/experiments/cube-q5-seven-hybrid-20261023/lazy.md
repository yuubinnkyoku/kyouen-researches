# 到達範囲を保つ探索継続

`lazy.cpp` は `graph.cpp` の別版。tree置換後のPN/DN再集計を、次回その局面へ
降下するときまで遅らせる。保持する値は正の有限な未確定作業量推定だけであり、
P/Nラベルの生成規則や証明書形式は変えていない。
置換のたびに全浅層の子をディスク参照してしまう待ち時間を除くための変更である。
既知3立方20根・中断再開・上限40のtree置換・層引継ぎの独立証明を確認した
（`regression-lazy.json`）。同じ7立方24終盤も全証明を独立検査した。

`focus_checkpoint.py` は別対象の未知treeを作業領域から外す。
選択根Rについて、いずれかの48変換gでg(R)を含むkeyだけを保持する。
包含の遺伝性により、そのようなkeyの全ての子も、正規化後にある像g'(R)を含む。
したがってRからの探索が参照しうる未知の子を除去しない。
確定候補の全行・全証人・累積counterはそのままコピーする。
元snapshotは保持し、新しい別ファイルへ出力する。

小盤面で二つの異なる根の未知treeを20件保存し、一つに絞ると10件になった。
絞る前後で、その根の再開後追加展開数・累積展開数・最終証明書が完全一致し、
独立検査も通った（`regression-focus.json`）。
大盤面では中心四石根の作業tree750,000件のうち、関連する66,269件を保持した。
元750,000件のsnapshotもprivateな `unfocused-stage4.hyb` に保存してある。
現在の根に到達不能な作業をRAMから外しただけで、旧対象の探索情報を失っていない。

`policy.cpp` は有限の補助試行。各偶数石局面で、その局面を保つ位数2の立方体変換に
よる応手だけを、終端応手・既知P証人に加えて試す。全ての相手手を処理できたとき
だけPを通常証明として記録し、失敗はUNKNOWNとする。
中心側5四石候補は29訪問で全てこの制限付き方式に失敗した。
これは当該局面のN判定でも、全ての対称性戦略を否定する証明でもない。
この補助試行から大盤面の新たな勝敗は採用していない。
`policy-small.jsonl`は終端応手追加前、`policy-small-terminal.jsonl`と
`policy-central.jsonl`は終端応手追加後の記録である。

`boundary.cpp` は探索を行わず、指定根の全合法子を48軌道にまとめて、基礎層と
任意の最新checkpointにある確定候補を数える。checkpointの追加表を線形走査するので
観測のたびに巨大な索引を作る必要はない。候補数は独立検査済み数と別に記録する。

```sh
g++ -O3 -std=c++17 -Wall -Wextra -Werror research/experiments/cube-q5-seven-hybrid-20261023/lazy.cpp -o /tmp/q7-lazy
python research/experiments/cube-q5-seven-hybrid-20261023/regression_layers.py /tmp/q7-lazy /tmp/q7-legacy /tmp/q7-verify-incremental
```
