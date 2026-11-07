# 共通pivotのmisère補助mex変換

通常版ではrank三以下の共通pivot族はg≤3だが、補助mex hには値4・5・6・7が現れる。
二点辺が一つある場合は、pivot着手後のh=0/1局面に制限した通常ゲームの値tと
合法点数の偶奇から厳密に計算できる。

- [全称変換の証明と適用範囲](proof.md)
- [h/t再帰と独立C++の比較](audit.py)、[C++原始subset DP](independent.cpp)
- [41662根の全一致](output/audit.json)
- [整数座標への移送検査](verify_geometry.py)、[座標と全共円四点組](output/geometry.json)
- [失敗した最初の式](failed-formula.md)、[当時の不一致記録](output/failed_formula.json)
- [縮小した十五点h6・十六点h7の別検査](audit_induced.py)、[達成例](output/induced_high_audit.json)

`search_forms.py`は自由一点・P3・C6（任意でPetersen）から和と完全joinを作る
有界探索。`search_restricted.cpp`は十四頂点の辺変更探索で、
seed20261108・試行上限100000で早期停止し、`output/restricted_mutations.json`を得た。
`minimize_high.py`はその全誘導部分グラフだけを調べる。
これらの不発見から上界や不存在を主張しない。

現在の正本はK0694。hは直和のSprague–Grundy不変量ではない。
