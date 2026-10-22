---
id: K0501
title: df-pnのフレーム内子局面を再利用すると固定した新規6局面で探索量を変えず約29–35%短縮した
kind: computation
status: observed
topics: [search-methods, verification, statistics]
aliases: []
relations:
- type: depends_on
  target: K0498
  note: 通常df-pnのroot計数と共有work上限を用いた同一仕事量の比較
artifacts:
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: フレーム所有の不変子局面、TT bounds再読出し、fresh-list監査、root計数
- path: cpp/tests/test_kyouen_frame_children.cpp
  role: verifier
  note: 独立幾何と直接部分集合DP、全安全4×4局面、TT追い出し、両tie順序、hybrid exactと診断の一致
- path: research/experiments/dfpn-frame-children-20261022/cli_test.py
  role: verifier
  note: CLI、既定OFF、監査、root reset、0 work上限、不正modeの拒否
- path: research/experiments/dfpn-frame-children-20261022/protocol.json
  role: manifest
  note: 事前固定入力・source/binary hash、予算、3反復、同一仕事量規則
- path: research/experiments/dfpn-frame-children-20261022/fixtures.json
  role: data
  note: 再利用の深い9局面、新規6局面、既知終盤26局面
- path: research/experiments/dfpn-frame-children-20261022/records.json
  role: data
  note: 全336根評価の結果・仕事量・生成数・再利用数・時間とraw参照
- path: research/experiments/dfpn-frame-children-20261022/audits.json
  role: data
  note: 時間比較とは別の3根・計2995リストのfresh-list監査
- path: research/experiments/dfpn-frame-children-20261022/comparison.md
  role: data
  note: 局面ごとの中央値合計による全比較表
- path: research/experiments/dfpn-frame-children-20261022/study.py
  role: verifier
  note: 独立幾何による入力再生成、全raw行、全組合せ、A/B仕事量と生成数の厳密照合、再集計
- path: research/experiments/dfpn-frame-children-20261022/test_study.py
  role: verifier
  note: 誤局面、新規勝敗、監査の時間比較混入、仕事量・生成数のずれ等を拒否する9テスト
---

## 方式と不変条件

通常df-pnは、同じフレームの再集計のたびに子の盤面変換、合法手、canonical key、
対称な子の重複除去を行っていた。これらはそのフレームの盤面が同じ限り不変である。
以下の明示指定で、最初に構築したフレーム所有の子リストを再利用する。

```text
--frame-children-cache
```

子の証明数・勝敗は再集計ごとに局面キーからTTを引き直す。
TT slot番号は保持せず、追い出された場合は従来と同じterminal/OPEN初期値に戻す。
子の順序、手、元の向きの全8盤面、合法手数、root-child診断の更新を維持する。
既存のフレーム所有heap bufferを使い、`expand()`の一時bufferとは共有しない。
フレームが破棄されればリストも破棄する。rootをまたぐ幾何cacheは作らない。

`--frame-children-audit`は再利用を有効化し、各refresh直後に従来方式で新しいリストを構築して
子の順序、全8盤面、合法手、key、count、move、pn/dn/st、診断用初期値を比較する。
監査は時間比較から分離した。オプションは通常df-pn専用で、standalone exact replay等との混用は拒否する。

## 正しさと仕事量の監査

独立した整数行列式で4×4盤の禁止4点集合を列挙し、占有部分集合の直接P/N DPを計算した。
全安全5,811局面についてfresh solver/TTの従来方式とcache+auditを比較し、
独立勝敗と、設定間のpn/dn、訪問数、展開数、exact nodesが全て一致した。
このとき計38,006回のrefreshでfresh-list監査を通過した。

さらにmemo=5/12、tie順序asc/desc、native exact併用の有無の8設定を比較し、
予算切れを含めてpn/dn、仕事量、追い出し数、root-child診断が一致した。
追い出しイベントは合計4,194件だった。rootを変えた再利用も確認した。
同じC++回帰は通常・UBSanの両方で通過した。
CLIでは既定OFF、同じ根の解決済みTT再利用時の計数reset、0 work上限、監査と不正modeを検査した。
既存の通常探索・P/N評価・独立proof DAG回帰も通過した。

## 固定比較

再利用の深い9局面、新規の安全な5石6局面、既知終盤26局面を使った。
新規6局面はseed2026102203で生成し、K0500の調整・確認15局面とのD4重複を除いた。
手法のパラメータ選択は行わず、入力とsource/binary hashをcommitしてから計測した。
各評価はfresh process/TT、memo=18、wall guard30秒、残余評価・native exactなし、各3反復。
以下は各局面の探索時間中央値の合計で、solver初期化は含まない。

| 対象 | work上限 | 従来 | cache | 変化 |
|---|---:|---:|---:|---:|
| 再利用9局面 | 20,000 | 2077.811 ms | 1491.117 ms | −28.2% |
| 再利用9局面 | 100,000 | 9269.068 ms | 6966.678 ms | −24.8% |
| 新規6局面 | 20,000 | 1486.324 ms | 1061.362 ms | −28.6% |
| 新規6局面 | 100,000 | 6954.096 ms | 4514.078 ms | −35.1% |
| 既知終盤26局面 | 20,000 | 13.305 ms | 9.799 ms | −26.4% |

全336評価をOFF/cacheで対にし、勝敗・停止理由・通常work・訪問数・展開数・exact nodesの完全一致を要求した。
全て一致し、`OFF geometry_builds = cache geometry_builds + child_refreshes`も全対で成立した。
新規6局面の10万workではリスト構築が887,014→587,026回、
幾何を計算する手候補は18,315,642回減った。
再利用したリストは299,988回であり、減った構築回数と一致する。

深い15根は全予算・設定・反復でUNKNOWN、既知終盤の全156評価は既知勝敗と一致した。
watchdogは0件。別途、旧3根を各2,000 workで計測し、計2,995回のrefreshを
全てfresh-list監査した。この3評価は時間表に含めない。
入力、全raw行、全組合せ、監査の分離と集計を再検査するverifierと9テストをCIに追加した。
CIではこの深い比較を再実行しない。

## 採用範囲と限界

通常df-pnの明示オプションとして利用できる。既定はOFFを維持する。
今回確認したのは同じ探索仕事量を速く処理できることと、限定した監査範囲の正しさであり、
深い根の新しい勝敗確定や必要探索量の減少ではない。
既存9局面と終盤26局面は過去に露出した標本で、新しいholdoutとは呼ばない。
時間は単一hostでの観測であり、全局面・他host・wall-time上限下で同じ短縮率になるとは主張しない。
