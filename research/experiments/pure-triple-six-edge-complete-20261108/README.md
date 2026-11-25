# 純三点六辺の全核を生成する完全計算

既知の全五辺核445型へ新しい三点辺を追加し、辺所属次数profileと辺置換で完全同型を除く。
生成された全型の辺ラベル付きorbit総数を、独立な多変数母関数と集合分割のMobius反転で確認する。
ゲーム値は所属cell占有数mexと別C++個別占有subset DPを比較する。

```sh
uv run --locked python research/experiments/pure-triple-six-edge-complete-20261108/audit.py
```

計算は完了し、全4,279型が別subsetの通常値と一致した。核gは6以下、
任意自由点込みでg≤7。全六辺以下4,806核の両自由点偶奇も検査し、補助値h≤7が鋭い。
g6核は八点三型・九点六型・十点一型の全十型。

`misere.py`でPythonと別subsetの両値、`export_misere.py`で新しいC++cellとsubsetを全根照合する。
`verify_generation.py`はEDGE_COUNT一般化後の全署名・辺安定化群位数の回帰、
`catalog.py`は高値全十型の抽出。詳細は[証明](proof.md)とK0687/K0691を参照。
hは終局1の補助mexで、xorを仮定せず自由点二個周期を証明して使用する。
