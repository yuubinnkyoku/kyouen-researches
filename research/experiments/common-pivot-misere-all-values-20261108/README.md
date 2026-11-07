# 共通pivot族のmisère無界性を相互再帰で証明する

二種類のコグラフG_m^aを構成し、h=a、低h制限ゲームの通常値t=mを全mで実現する。
K0694の変換から二点辺付き共通pivot族で全非負hが実現し、K0696の予想を証明へ進める。
純三点だけでも通常値0/1を固定して全h≥4を実現する。

```sh
uv run --locked python research/experiments/common-pivot-misere-all-values-20261108/verify.py
uv run --locked python research/experiments/common-pivot-misere-all-values-20261108/dag_audit.py
uv run --locked python research/experiments/common-pivot-misere-all-values-20261108/verify_geometry.py
```

無限族は[相互帰納の証明](proof.md)による。有限監査のみを無界性の根拠にはしない。
hには直和xor則を使わず、性質Rの下で制限通常ゲームtへxorを適用する。
独立な文字通りのoption-DAG実装もm=0..64の両側130根、4,363ゲーム局面で一致した。
指数サイズのグラフを直接展開した計算とは区別する。
