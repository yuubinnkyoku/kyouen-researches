# q8の同和弦上界と証明区間縮小

[証明](proof.md)は五行q8の無界末尾を101から始められることを示す。
既存M5,8=16の独立検査済み有限除外のうち、255件だけを使う証明に縮小できる。
旧一次資料は保存し、現在の結論はK0331に置く。

`scripts/reduce_manifest.py` は抽出対象CNFを全て再生成してhash照合し、
`output/reduced-manifest.json` を出力する。今回はSAT・DRATを再実行しない。
