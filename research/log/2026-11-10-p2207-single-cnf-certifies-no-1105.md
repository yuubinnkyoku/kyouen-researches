# 2026-11-10 p=2207 の 1105 石不存在を単一 DRAT 証明で確定（A(2207)=1104）

## 結果

- サイズ h+2 = 1105 の安全集合が存在しないことを、**単一の CNF と単一の DRAT 証明**で示した。
- サイズ h+2 の集合は `x + c - e = 2` からクラス `(x,c,e) = (1,1,0)` のみ（K0097 の上界証明の完全対構造）。
  すなわち「0 ＋一つの完全対 ＋各他の対一側」で、K0334 の等号集合と同じ形。
- 符号化（`search_shape_class.py` の 4 値クラス版）:
  - 各対を {BOTH, NONE, LOW, HIGH} の 4 値（exactly-one）、BOTH はちょうど 1、NONE は 0。
  - 点の選択を補助変数 `a_t <=> side_t or BOTH` で表し、全禁止四点（原点を含む辺も）を節にする。
  - 7,720 変数・50,616 節（うち辺由来 31,868）。
- 求解: CaDiCaL が **UNSAT（28.6 秒）**、DRAT 証明は **497,179 行**。
- 検証: 修正版（削除時に代入を失効させる）`drat_check_incremental.cpp` で **VERIFIED（875 秒）**。

## 意味

- K0722 の独立幾何監査済み下界 **1104 点**と合わせて **A(2207) = 1104**。
  上界 `(p+3)/2 = 1105` は 1 だけ達成されない。
- 従来の「全 1103 d の UNSAT」を前提にした上界とは独立に、**単一の証明**で上界が確定した。
  d ごとの CNF の全数監査は不要になり、p=2207 の上界は 1 本の証明で完結する。

## 保存物

- `output/cert-2207-1105/a2207_1105.cnf`（1.1 MB）: 符号化した CNF そのもの。
- `output/cert-2207-1105/a2207_1105.drat.gz`（9.6 MB）: DRAT 証明（解凍後 48 MB、
  SHA-256 は `F0CE140DB899E4C9009FCED1BC38AA753315D71BD8EB9F1498DB0C74AD77A7EA`）。
- `output/shape_class_2207_1105.json`: 求解の記録（変数・節数・時間）。

## 再現

```sh
# 符号化して解き、証明を保存して検査する（search_shape_class.build を使用）
python - <<'PY'
import sys; sys.path.insert(0, "../parabola-equality-extension-2143-2500-20261107")
from probe_driver import run_gen
from search_shape_class import build
clauses, nv, kept = build(2207, run_gen("forbidden_edges.exe", 2207), 1, 1, 0)
# Cadical195(with_proof=True) で解き、get_proof() を .drat として保存し、
# drat_check_incremental.cpp で検査する
PY
```

## 次の一手

- 同じ単一 CNF の手法を p=2531 / 3251 / 2647 にも適用し、上界を 1 証明ずつ確定する
  （形状クラスは素数ごとにサイズが違うので、`size = h+2` で自動列挙できる）。
- 有効な証明の保存形式（現在は gzip した DRAT）を、repo の他の証明と揃えるか検討する。
