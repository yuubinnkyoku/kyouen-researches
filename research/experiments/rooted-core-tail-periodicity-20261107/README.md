# 固定核＋長道の周期証明

2026-11-07の一次資料。現在の命題はK0682を参照。

* `engine.py`: 任意の固定残余核に対する正確な有限状態・長道mex再帰。
* `verify.py`: 5点以下の全6337ラベル付き核・513根付き型の周期証明書と直接subset監査。
* `proof.md`: 有限窓からの全称帰納と全5点核への適用。
* `output/audit.json`: 決定的な整数証明書。1型1行で必要な全prefixを保存。
* `probe_five.py`, `output/five_vertex_probe.json`: 証明前の有界探索一次資料。計時を含む診断であり証明書ではない。

```sh
uv run --locked python research/experiments/rooted-core-tail-periodicity-20261107/verify.py
```

標準ライブラリのみ。周期検出だけでは証明とせず、全核状態が有限窓条件を満たすことを確認する。
6点以上の任意核で周期34が成立するという全称命題は未証明。
