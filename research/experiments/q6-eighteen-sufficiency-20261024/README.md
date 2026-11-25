# 三平行線q6の18候補十分性：独立した全称代数監査

K0478のE14障害を、連続156有理式と固定4823四円組の完全排除で閉じる。
全終局15石・全安全局面g=(15−|S|) mod2。18の最小性は主張しない。
旧17候補改善案は証明の前提にしない。[全証明](proof.md)。

```sh
uv run --locked python research/experiments/q6-eighteen-sufficiency-20261024/run.py --cxx g++
```

Windowsでg++がPATHにない場合は `--cxx C:/msys64/ucrt64/bin/g++.exe`。
一時バイナリはOSの一時ディレクトリに置く。リポジトリの依存・lockを変更しない。

* `symbolic.py`: SymPy 1.14.0による証明書生成器。
* `symbolic-certificate.json`: 3族×52条件の有理式・因数分解・排除証拠。
* `check_symbolic.py`: SymPyを使わず全恒等式・全ケース・符号域を再計算する検査器。改変2種類を拒否。
* `fixed.py`, `fixed_independent.cpp`: 11,628混合候補と4823四円組を独立計算。
* `symbolic-audit.json`, `fixed-audit.json`, `audit.json`: 実行結果。

証明書を再生成する場合だけ次を使う。通常の検査にはSymPyは不要。

```sh
uv run --no-project --with sympy==1.14.0 python research/experiments/q6-eighteen-sufficiency-20261024/symbolic.py
```
