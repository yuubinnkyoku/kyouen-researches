# 保存1302点集合の包含極大性

命題・対象は[K0720](../../knowledge/items/K0720-p2647-saved-1302-witness-inclusion-maximal.md)を参照する。
保存1302点の安全性の独立幾何receiptへhashを結び付け、未選択1345点すべてへの単点追加不能を検査した。

`output/initial/blockers.txt` の先頭は `2647 1345`、各行は `追加t q0 q1 q2 q3`。
四点はtと既存集合の3点からなり、相異なるソート済みの四点で整数4×4行列式が0となる。
未選択点を重複なく完全に被覆するため、指定集合は包含極大である。

`audit.py` は以前の1300点用ドライバを1302点の入力と行数に適用した版で、source hashも記録する。
CNFは阻止候補の生成だけに用いる。
既存の `parabola-maximal-1300-20261109/verify_blockers.cpp` を再ビルドし、CNFを読まない検査を行った。
正例1345行を受理し、欠落・余分データ・異なるp・追加点重複・既選択点・未ソート四点・非禁止四点の7制御を拒否した。

```sh
uv run --locked python research/experiments/parabola-maximal-1302-20261109/audit.py --output FRESH-maximality-audit
```

出力先は毎回新しくし、過去の証拠を上書きしない。
これは保存集合への単点追加不能であり、最大サイズや交換不能ではない。
1303点要求の4点以下除去のUNKNOWNは、別experimentの予算付き探索記録として区別する。
