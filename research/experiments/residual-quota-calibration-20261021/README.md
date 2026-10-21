# 残余P/N quotaの調整と新規確認用局面 (2026-10-21)

## 測定前に固定する規則

調整はK0494の既存train26局面のみ。対照OFFと、quota128/512/2048 × legal閾値6/12の
6設定を3反復し、各局面の探索時間中央値を合計する。候補PNの選択は
UNKNOWN数、solve_us、quota、閾値の辞書式最小。OFFは対照として別に保持する。
選んだ候補をselection.jsonへ固定してcommitしてから、新しい確認用局面を測定する。
確認結果から再選択しない。既存holdout26を今回の新規確認と呼ばない。

新しい確認用局面は、測定前にseed2026102107の512回のランダム合法対局から生成する。
legal=6..18 × occupied parity=0/1の26層。trial順、同trial内は対局の時間順に、未充足層の
最初の局面を選ぶ。同一trialからは1局面のみ。K0495/496の全826局面とのD4重複を除く。
勝敗や時間を見て選別しない。独立subset-mexと独立幾何検査で期待値と合法点・残余辺族を検査する。

新しい確認用26局面ではOFFと固定候補を3反復比較する。既存の深い3局面にも同じ2設定を
外側5000 board nodesで各3反復適用する。1根全体でP/N quotaを共有し、枯渇は通常探索へ復帰。
入力・binary hash、raw出力、UNKNOWN数、board nodes、PN calls/aborts、初期化/探索時間を保存する。
各反復内の設定順は回転し、solver/memoは根ごとに新規、共有cacheなし。

採用判断は、既知局面の誤答ゼロ、UNKNOWN増加ゼロ、新規確認でOFFより探索時間が少なく、
深い3局面でもUNKNOWNが増えず探索時間がOFF以下、の全条件を満たすこと。
満たさなければ既定handoff OFFと既定Grundyを維持する。満たしても本コーパスでの観測とする。
深い局面が新たに確定したら測定を停止し、独立検証前にその勝敗を採用しない。

この実験は有限の固定局面比較。新たな未知盤の長時間探索を自動workflowに追加しない。
quotaとboard nodesは別の仕事量で、quotaはwall時間上限ではない。約0.5秒/根の初期化を
探索時間から分ける。性能の全入力への一般化や11×11空盤の解決は主張しない。

## 再現と検査

```sh
c++ -std=c++20 -O2 -Icpp/solvers research/experiments/residual-quota-calibration-20261021/sample.cpp -o /tmp/quota-sample
/tmp/quota-sample > /tmp/quota-candidates.json
python research/experiments/residual-quota-calibration-20261021/verify_outputs.py --geometry
python -m unittest discover -s research/experiments/residual-quota-calibration-20261021 -p test_protocol.py
```

candidate-pool.jsonは/tmp/quota-candidates.jsonとbyte単位で一致する固定seedの出力。
prepare.pyはこのpoolからfixtures、入力CSV、protocolを生成し、全新規局面を独立幾何とsubset-mexで確認する。
測定を新しく実行する場合は別のexperimentへ出力し、当時の保存結果を上書きしない。
初回は固定ファイルをcommitした後にcalibrate.pyの`--phase train`を実行し、
training-records.jsonとselection.jsonをcommitしてから`--phase confirm`を実行する。
両段階に`--solver /path/to/frozen-binary`が必要で、binaryのhashを検査する。
selection作成後の再調整、確認済み出力の再実行を拒否する。

verify_outputs.pyはD4非重複、層とtrialの選択、入力hash、独立subset-mex、
各replay行の局面・勝敗・予算・quota、局面ごとの中央値、調整データだけによる選択と採用条件を検査する。
`--geometry`ではさらに合法点と極小残余辺族を別実装の行列式から再計算する。
CIはこの固定資料の監査と9単体テストのみを実行し、時間測定や深い3局面の再探索は起動しない。

## 完了結果と採用範囲

調整ではquota128・gate6を選び、ac421eddでselectionと全調整結果をcommitした後に確認を開始した。
調整用26局面の探索時間はOFF 3.781 ms、候補2.932 ms。閾値6の3予算は全て同じ259 kernel callsで
枯渇ゼロだったため、この予算間の小さい時間差には測定揺らぎも含まれる。

新規26局面ではOFF 4.748 ms、候補3.761 ms（20.8%短縮）。両方UNKNOWNゼロ・全勝敗一致。
深い3局面ではOFF 30.432 ms、候補29.900 msでUNKNOWNは両方3。差は0.532 ms（1.7%）と小さく、
統計的な優位性を主張しない。候補のPN呼出しは各深いrootで128、合計384。うち1 rootが
handoff内でUNKNOWNを返し、残り2 rootもquotaがゼロになった後は通常探索へ戻った。

事前に定めた数値採用条件を全て満たしたので、このbounded exact replayの明示指定として
`--residual-exact-legal=6 --residual-evaluator=outcome --residual-outcome-budget=128`を採用する。
通常探索の既定handoff OFFと既定Grundyは変更しない。今回の確認は外側5000 nodesの固定根であり、
他のboard budget、全ての初期局面、通常df-pn探索全体の性能を検証したものではない。

調整546根評価、新規確認156根評価、深い局面18根評価、計720。完全な表はcomparison.md。
既知の全局面は全設定・反復で正答し、新たな深い勝敗確定は出なかった。
