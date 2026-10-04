# 剰余多項式グラフ・NAE分解・証人回復

現在の結論はK0340/K0341とK0097/K0101を参照する。
`proof.md`は全称証明、JSONは有限監査記録または明示証人である。

検査はrootから実行する。Python標準ライブラリとC++17だけで保存済み全証拠を再検査できる。

```sh
python research/experiments/frontier-geometry-2026-10-05/verify_polynomial_curves.py
g++ -std=c++17 -O3 research/experiments/frontier-geometry-2026-10-05/verify_witnesses.cpp -o /tmp/frontier-parabola-verifier
python research/experiments/frontier-geometry-2026-10-05/verify_saved_witnesses.py --verifier /tmp/frontier-parabola-verifier
```

最初の検査は66多項式グラフの全直線・円カタログ、13素数p≤43の全362137四点組、
全double候補での既存CNFとNAE分解の同値、次数3/4の鋭さ証人を検査する。
第二の検査は131..251の全23素数の全94575425選択四点組をgeneric Leibniz整数行列式で直接検査する。
p=509,1009の診断証人は証明済み合同式フィルタにより全四点を覆い、3063918候補を直接整数検査する。

回復した証人を再探索するには既存pair-CNF/DPLLを再利用する。

```sh
g++ -std=c++17 -O3 research/experiments/frontier-geometry-2026-10-05/forbidden_edges.cpp -o /tmp/frontier-parabola-edges
python research/experiments/frontier-geometry-2026-10-05/recover_witnesses.py --generator /tmp/frontier-parabola-edges
```

`--generator`を省略すれば既存Pythonの候補列挙を使う。探索と全四点直接検査には数分かかる。
回復理由は、mainの131..251実験報告が参照していた証人JSONがGit管理されておらず、このcheckoutにもなかったため。
既存29素数の証人を再発見した成果として数えない。

大きい二素数の密度診断を再探索する場合だけ`python-sat==1.9.dev15`を別環境へ導入し、次を実行する。
通常の証拠検査にはこの依存は不要。

```sh
python research/experiments/frontier-geometry-2026-10-05/density_probe.py --generator /tmp/frontier-parabola-edges
```

密度やSATの処理速度は一般充足可能性の証明ではない。p=509,1009は明示された二素数だけであり、
251..1009の全素数に関する記録ではない。全奇素数のq=4等号問題K0101は未解決。
