# 5×m・q=7の後続frontier

[証明](proof.md)では、同和弦の三本鎖分解と反転後のMelchior不等式を組み合わせて
既存上界200を158へ改善する。下界19は既存の独立検査済みm18証人を使う。

- `scripts/verify_packing.py`: 証明の有限成分と実blockerの独立監査。
- `output/packing-audit.json`: 座標集合・整数最適化・小盤監査の結果。
- `scripts/maximal_probe.py`: 外部行にも極大性を要求する bounded SAT probe。
- `output/maximal-probe.json`: SAT実験。UNKNOWNおよび未監査UNSATを上界証明に使わない。

現在の結論は `research/knowledge/items/K0332-width-five-q7-stabilization-bounds.md` が正本。
