# 3×3×4・3×3×5・3×3×6・3×3×7 共面4点禁止版の強解決（2026-10-27）

K0529 が容量（全mの最大・最小極大石数）を証明し 3×3×3 を強解決した家族について、3×3×4・3×3×5・3×3×6・3×3×7 の全局面強解決を二方式の独立計算で完了させた実験（ディレクトリ名は開始時点の対象 m=4 に由来する）。

- `verify.py` — Python。Leibniz 4×4行列式、安全集合の昇順全生成、階層mex。旧実験（coplanar-3x3xm-q4-20261024）の verify.py の拡張で、m≤6 に対応。
- `independent.cpp` — C++。外積行列式、空盤DFS＋メモ化。旧 independent.cpp のマスクを uint32_t から uint64_t へ一般化し m≤7 に対応。点順序は verify.py と意図的に異なる。
- `enum2.cpp` — C++。m=7 の第二方式。Leibniz 行列式・ボトムアップ全生成・上位層からのmex。
- `orbits.py` — 最大層（K石）の配置を箱対称群 D4×Z2（位数16）で軌道分割する第三の確認。
- `results.md` — 回帰照合（m=1〜3 は K0529 公表値と完全一致）と m=4,5,6,7 の全集計。
- `cpp_m4.txt` 〜 `cpp_m7.txt` / `enum2_m6.txt` / `enum2_m7.txt` / `py_m4.json` 〜 `py_m6.json` / `orbits_m4.json` 〜 `orbits_m7.json` — 実行出力の保存。

範囲は有限計算の完了であり、m≥8 の Grundy や全称命題は含まない。
