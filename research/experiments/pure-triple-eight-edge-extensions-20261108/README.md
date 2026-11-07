# 七辺高値核への一辺追加

七辺完全表から通常値が指定値以上の核を選び、三点辺を一つ追加する。
既存点から0..3点を選び、残りを新しい専有点とし、さらに自由点0/1を許す。
選んだ核からの拡張は尽くすが、八辺族全体の完全列挙ではない。
cell占有数と別subsetによる通常値・終局1補助値を全根比較する。

```sh
uv run --locked python research/experiments/pure-triple-eight-edge-extensions-20261108/audit.py
```

不発見は八辺全族の上界や不存在証明に使用しない。
