# 三平行線q6・17候補改善案の監査

旧証明の全称帰着を[audit.md](audit.md)で点検し、Python/C++の全有限部分を再実行する。
E13の6,173,662有理候補、3族各544記号候補、AP5005候補を含む。
結果・旧ソースSHA256は `audit.json`。旧experimentは変更しない。

```sh
uv run --locked python research/experiments/q6-seventeen-audit-20261024/run.py --cxx g++
```

Windowsで必要なら `--cxx C:/msys64/ucrt64/bin/g++.exe`。
数十秒から数分の有限監査で、未知盤の長時間探索ではない。
結論は17候補十分・全終局15石・全安全局面の偶奇Grundy値。最小性は未主張。
E≥13という条件を外すと一点四円の明示反例があることも厳密確認する。
