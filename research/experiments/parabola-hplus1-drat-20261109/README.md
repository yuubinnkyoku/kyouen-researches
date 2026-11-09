# p=2647の1324点不存在: 3形状のDRAT監査

原点の有無x、完全対数c、空対数eにより、サイズh+1=1324の安全集合を3形状に分け、
各形状の単一CNFのUNSAT証明を保存・独立検査した。
現在の監査済み範囲と証拠レベルは [K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md) を参照する。
形状判定の単なるソルバ主張から、入力・証明を再検査可能な上界1323へ進める実験である。

| 形状 (x,c,e) | 変数 | 節 | DRAT行数 | 初回DRAT独立検査 |
|---|---:|---:|---:|---|
| a=(1,0,0) | 7938 | 73731 | 19525 | VERIFIED |
| b=(0,1,0) | 9260 | 76370 | 56616 | VERIFIED |
| c=(1,1,1) | 10582 | 79017 | 126556 | VERIFIED |

3本ともK0707修正版の検証器ソースSHA-256
`34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b` を使った。
初回は各4.1/41.9/75.2秒、後日の再生でも3本とも受理し、計66419 RUP・0 RATだった。

## 証拠の構成

- `input/verified_edges.txt.gz`: 実際に用いた53886四点。原cacheの928389四点から非台形部分を選択した。
- `input/geometry.json`: 全提供四点が実際に整数共円・共線行列式0であることの独立な受理記録。
- `verify_edges.cpp`: 探索generatorを使わず、既存generic 4×4 Leibniz行列式を直接適用する。
- `encoding.py`: 各対のBOTH/NONE/LOW/HIGH、個数制約、点選択補助変数をCNFにする。
- `output/shape-{a,b,c}/input.cnf.gz`: 3形状の実入力。
- `output/shape-{a,b,c}/proof.drat.gz`: 生DRAT証明（入力とともに展開後のhashを保存）。
- `output/shape-{a,b,c}/solver.json`: ソルバのUNSAT主張、入力・証明・ソースのhash。
- `output/shape-{a,b,c}/audit.json`: 初回の独立DRAT検査。ソースhashと実行binary hashを記録する。
- `output/replay-20261109/`: 後日の実際の再生結果。初回receiptは上書きしない。
- `regression.json`: 小例5917配置、入力再生成、明示的prefix counterの別実装との節集合一致、
  全提供四点の再検査と保存証拠のhash照合。

圧縮ファイルは生の入力・出力の全内容を保持する。原cacheの完全性を上界の根拠に仮定しない。

## 上界への論理

K0097により安全集合には完全対は高々一つ。点数は `|S|=h+x+c-e` なので、
1324=h+1点なら3形状が全てを尽くす。各対の状態と点選択を忠実に符号化した。
全ての提供四点は整数幾何で禁止四点と確認済みなので、任意の安全集合はそれらの回避節を満たす。
提供していない禁止四点があっても、このCNFは緩和であり、UNSATによる上界は損なわれない。
3形状すべてUNSATで1324点集合が存在しなければ、より大きい安全集合の1324点部分集合も存在し得ず、
A(2647)<=1323となる。CNFから返るSAT候補の安全性には別途の全幾何検査が必要。

prefix counterについては、値0なら全flagを偽にする単位節、値1なら全flagのORと高々一つの
prefix鎖を使う。正しい個数のflag選択からprefix ORを補助変数へ代入すれば全節を満たす。
この明示的な節構成が実際の3入力のcardinality部分と一致することを、生成ライブラリとは別に検査した。

## 再現

repo rootで、保存証拠を使う有限回帰（大きなDRATの再生はしない）:

```sh
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-hplus1-drat-20261109/regression.py
```

p=3,5,7,11,13,17で全5917の有効な3形状配置を調べ、CNFと独立整数幾何の判定が一致した。
実際の53886四点も毎回整数行列式で再検査し、非辺・重複・範囲外・欠損・余剰入力を拒否する。
3形状の入力をbyte単位で再生成し、保存入力・DRAT・初回receiptのhashを照合する。

保存DRATを実際に再生する場合は、新しい出力先を選ぶ:

```sh
uv run --locked python research/experiments/parabola-hplus1-drat-20261109/replay.py --output D:/tmp/hplus1-replay-new
```

このコマンドはソルバを再実行せず、検証器をソースから再ビルドし、新しいreceiptへ保存する。
最初の入力・証明生成用 `prepare.py` / `generate.py` / `audit.py` も保持するが、
同じ対象の計算を重複起動せず、既存の証明がある場合は再生を使う。

本結果は有限計算の証明検査で、Leanの形式証明ではない。検査器・コンパイラ等への依存は残る。
サイズ1323の4形状UNSATからの上界1322は別の未監査ソルバ記録で、この監査が覆う範囲ではない。
