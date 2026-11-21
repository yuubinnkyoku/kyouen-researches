# 入力 pin（本実験が使用した出版正本・HEAD e9e3bea57fe67e252520a389192ee4a3c888de1d 固定）

| repo path | sha256 | 用途 |
|---|---|---|
| `research/experiments/fixed-width/scripts/q34_support_exclusion.cpp` | `6960331d30e5cf…`（全文 sha256: 6960331d30e5cfa23e1ab5f695b9e5192b5e22d1b79ff3e69ac234383a75e141） | 移植原本（K0351 エンジン） |
| `research/experiments/fixed-width/output/q34_exact_threshold.json` | `e08c4abaee25…`（全文: e08c4abaee256b2f3f2a53ab36f8502568bd9328691a22e06ba1ab25558959e4） | bit-exact 比較正本（m=24..68 出版ケース値） |
| `research/experiments/fixed-width/output/q34_audit.json` | `3c5c9596cb16…` | m=23 witness 両系の座標比較正本 |
| `research/experiments/fixed-width/scripts/q34_deficient_witness_audit.py` | `2571cf0614d7…` | 出版 witness 検証器の新環境再実行 |
| `research/experiments/fixed-width/scripts/q34_independent_recheck.py` | `e970005b9f65…` | 独立再検証（3述語）の新環境再実行 |
| `research/experiments/three-row-q4-enumeration-20261121/scripts/witness_check.py` | `4259d15192c1…` | witness 第三系統検証（整数行列式） |

検証済みの等価性: 上記4ファイル（cpp・threshold.json・audit.json・両 py）とも、本レーン作業コピーが `e9e3bea5` の raw pinned URL からの取得 byte と sha256 完全一致。

- engine 原本は C++（`unsigned __int128`）。本環境に C++ コンパイラが無いため、Node.js 移植による再生とした（文対文・sha256 `a11e0091d5c3…`）。
- `witness_check.py` は m28 レーンの pin scripts（`enumeration-20261121/scripts/`）由来で、出版 md5 群（wsearch34.js `526cf1c3`・sat.js `0cc6021a`・dx34.js `b02235a9`）と同じ列挙閉包実験のスクリプト群に属する。
