# 削除を捨てたRUP追加列の監査

既存のサイズ1323証明を、SATの再実行なしで別の証拠形式として検査する。
現在の幾何学的結論は [K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md) に置く。
前回のDRAT検査と変数衝突の履歴は `../parabola-size1323-drat-20261109/` に保持する。

## なぜ削除を無視できるか

この検査器はRATを一切使わない。元CNFと、それまでRUPで確認した追加節を全て保持する。
各追加節Cについて、その否定を仮定したunit propagationが矛盾することを検査する。
従って各追加節は保持中の節の論理的帰結であり、帰納的に元CNFの帰結でもある。
空節まで通ったときだけ `RUP_VERIFIED` とする。

入力の削除行は構文検査後に無視する。これは元のDRAT列の削除意味論を検査する方法ではなく、
削除を消した追加列そのものがRUP反駁であることを検査する方法である。
元CNFが充足可能なら、正しいRUP節を何個加えても空節は導けない。
RATは論理的帰結を保証しないため、RUPで通らなかった節をRATへfallbackしてはならない。
K0707の古い代入を保持するDRAT検査器とは異なり、この列では代入の前提となる節を削除していない。

`rup_check.cpp` の伝播部分はK0707修正版のソースからコピーした。
RAT・削除処理を除き、宣言範囲・終端0・節数を調べるparserを追加した。
入力はheaderと各節をそれぞれ一行に置く制限形式であり、一般の全DIMACS構文には対応しない。
重複literalは取り除く。最初のprototypeでは重複literalにより正しいRUPを拒否したが、
`output/prototype-duplicate-literal-failure.json` の例で再現し、parserの正規化で修正した。
これは偽受理ではない。修正版は独立なPythonの毎回初期化するUPと516件で一致し、
受理例は全割当列挙でもUNSAT。K0707の偽証明4件は全て拒否した。
これは有限回帰であり、コンパイラや実装全体の形式証明ではない。

## 入力への写像の別検査

`encoding_audit.py` はCardEncもSATソルバも呼ばず、保存CNFの全節を独立したschemaと比較する。
one-hot、点変数の同値、辺の回避節に加え、一般kのstaggered sequential counterを比較した。
補助変数の名前だけは実節から復元し、選択変数・他counterとの範囲の分離、
全名前が相異なること、全節のmultiset一致を検査する。

AtMost(k)の補助変数S[i,j]は「入力の最初のi+1個で真がj個以上」を表すと解釈できる。
存在する範囲は `1<=j<=k, j-1<=i<=n-k+j-2`。
節は入力から第1段への含意、同じjでのprefixの単調性、入力と前段から次段への含意、
最後の段からのoverflow禁止である。
重みk以下の任意の入力についてこの閾値で全補助変数を与えれば各節が満たされる。
Equals(k)は正入力のAtMost(k)と負入力のAtMost(n-k)の組であり、重みkの全入力を拡張できる。
この拡張可能性こそ、幾何の安全集合をCNFのモデルへ写すために必要な向きである。
特に112のNONE=2について、両counterの全節も比較した。

全53886提供辺も既存のgeneric整数行列式検査器で再検査した。
全禁止辺を列挙したという仮定は不要であり、一部の真の禁止辺だけでもUNSATなら上界を与える。

## 再現

```sh
uv run --locked python research/experiments/parabola-monotone-rup-20261109/regression.py --output FRESH-regression.json
uv run --locked python research/experiments/parabola-monotone-rup-20261109/encoding_audit.py --output FRESH-encoding-audit.json
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-monotone-rup-20261109/audit.py --shape 112 --timeout 900 --output FRESH-audit112.json
```

出力先には既存ファイルを指定できない。監査は入力を修正版から再生成し、保存入力とbyte比較する。
証明はstreamで展開してhash・行数を調べ、検査器のソースとbinaryのhashをreceiptへ保存する。
112の元証明は107MBのgzipとしてローカルにのみ保持されている。
その所在と圧縮・展開後hashは前実験の `output/shape-112/proof-manifest.json` にある。
Gitだけの別checkoutでは112の生証明を復元するか再生成する必要がある。
receiptは監査の記録であり、生証明自体の配布を代替しない。
