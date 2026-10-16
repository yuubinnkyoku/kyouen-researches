# 剰余放物線の等号A(p)=(p+3)/2：521..2000への有限拡張

2026-10-16。K0097/K0101の有限等号範囲を509から2000へ広げる計算記録。

## 背景

`proof.md`（research/experiments/frontier-geometry-2026-10-05）で一般上界 `A(p) <= (p+3)/2` が
証明され、等号集合は `{0} ∪ {d,p-d} ∪ (各対{i,p-i}から一方)` の形に限られることが示された
（完全対補題・NAE/原点分解、K0334）。等号 `A(p)=(p+3)/2` は「ある `d` について
signed NAE3/4 と原点節のCNFが充足可能」と同値。

既存記録は 5..509 の全奇素数と 509,1009 で等号を確認していたが、**509<p<1009 の奇素数は未記録**
だった（README末尾の「251..1009の全素数に関する記録ではない」）。本実験はその穴を埋め、さらに
2000まで延長する。

## 方法

- 禁止四点組（共円四元）は `forbidden_edges.cpp`（既存、`frontier-geometry-2026-10-05`）で
  整数行列式により厳密列挙。Vandermonde条件から共円四点は `sum≡0 mod p` を満たすため過不足ない。
- 各素数 `p`、`h=(p-1)/2` について `d=h` を最初に試し、UNSATなら `d=h-1,h-2,...` と降順に
  `clauses_for_pair(p,edges,d)`（既存 `structural-lemmas-2026-10-02/checks/parabola_half_bound.py`）を
  CNF化し、cadical（WSL）で求解。SATモデルから証人を構成。
- 候補のdごとの還元は厳密（全等号集合がこの形をとる）なので、全dのUNSATが反例となる。本実験では
  反例は出ず、対象全素数でSAT。

## 結果

**521..1999 の全206素数で等号証人を構成。** 既存の 5..509 と合わせ、**5..2000 の全奇素数で
等号が成立**する（記録済みの509,1009も含む）。

- 200素数は `d=h`。6素数は `d!=h`：1087,1091,1367,1523,1847 が `d=h-1`、1861が `d=h-66`。
- `p=1999` で禁止四点は522,014（最大）。
- 証人一覧: `output/witnesses_521_2000.json`（p, double_pair, parameters, size=h+2）。
  各証人は生成辺集合 `edges` のいかなる四点組も含まないことを構成時に照合。

## 独立検証

生成・求解とは別実装 `verify_witnesses.cpp --modular-filter`（既存、generic 4×4 Leibniz行列式。
探索の3×3とは別経路）で全証人を検査：`output/parabola-equality-audit.txt`（`p n covered checked`）。
出口コード0、206行。

- 検査対象は `sum≡0 mod p` を満たす四点のみ（それ以外は整数行列式が自動的に非零）。総被覆四点
  2,196,275,194,090、直接整数行列式 **1,385,691,858**、共円0件。
- `p=1009` の監査値（covered 2699163390, checked 2711706）は `proof.md` の記録と一致。

## 再現

```sh
g++ -O3 -std=c++17 research/experiments/frontier-geometry-2026-10-05/forbidden_edges.cpp   -o /tmp/forbidden_edges
g++ -O3 -std=c++17 research/experiments/frontier-geometry-2026-10-05/verify_witnesses.cpp   -o /tmp/verify_witnesses
# 証人の構成（python-sat不要。CNFはDIMACSでWSL cadicalに渡す）
python research/experiments/parabola-equality-extension-20261016/scripts/probe_parabola.py \
  --generator /tmp/forbidden_edges --start 521 --end 2000 --max-doubles 0 \
  --out output/probe.json        # max-doubles 0 は全dを試す
# 独立検証
python research/experiments/parabola-equality-extension-20261016/scripts/verify_saved_witnesses.py \
  output/witnesses_521_2000.json /tmp/verify_witnesses
```

## 注意

これは **5..2000の有限存在証明**であり、全奇素数での等号（K0101）の証明ではない。250を超える
全素数の充足可能性も、反例素数も未確定。上限や全盤K_pの既知下界とは別の問い。被覆数は
全奇素数中で最大とは限らない。
