# Grundy frontierの有限境界調査とq=7上界の独立監査

2026-10-05。一次実験資料であり、現行の結論はknowledge項目を参照する。
今回このディレクトリのceiling調査から新しいknowledge項目は作らない。

- [有限調査・切替理由](reports/ceiling-boundary-investigation.md)
- [完全有限集計](output/census.json)
- [別生成法・直接安全集合mexによる照合](output/independent-audit.json)
- [q=7上界と一般弦energyの独立数学監査](reports/q57-independent-review.md)
- [別コードによるpacking算術receipt](output/packing-independent-audit.json)

再現手順:

```sh
c++ -std=c++17 -O3 -Wall -Wextra -pedantic \
  research/experiments/grundy-frontier-followup-20261005/scripts/ceiling_census.cpp \
  -o /tmp/ceiling_census
/tmp/ceiling_census 6 0
/tmp/ceiling_census 6 1
python research/experiments/grundy-frontier-followup-20261005/scripts/check_census.py
python research/experiments/grundy-frontier-followup-20261005/scripts/check_packing_independent.py
```

mode 0は全単点が合法なn頂点複体、mode 1はn点上の空でない下方閉複体Dを
`simplex([n]) ∪ ({b}*D)`へ変換したn+1頂点ゲーム。両方とも通常プレイの一点追加。
stdoutはJSON。保存したcensusはn=1..6・両modeの12集計をrows配列に結合したもの。
別生成法による全件独立照合はn≤5で、n=6は全保存証人の直接照合だけを行う。
正方形盤の状態を列挙しておらず、標準盤の無界命題への反例ではない。
