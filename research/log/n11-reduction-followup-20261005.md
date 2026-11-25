# 2026-10-05 交換可能残局classの有限kernelと速度gate

開始時main: `f76cb65cb5d6843e80a5359efa9c37473a80fbbd`。
AGENTS、knowledge正本、現在のopen questions、直近commit、K0108/K0194/K0300/
K0329/K0336とn11 residual-twins proof/codeを読んだ。

M5,7の閾値、n11のcacheを使うcover、残局一般構造を比較し、既存双子定理を
全交換可能classへ広げる構造を選択。新しい空盤df-pnは実行しない。

全R内の全二点交換を保存するclass Xには、内部辺の容量、または混合辺の
最大X交差数に応じた誘導点削除kernelがあることを証明した。
rank4ではclass高々4点、内部cliqueは1点。4点必要の具体反例も得た。
容量の(i,T)商DAGと深さ付き偶奇の辞書式帰納で全称性を証明。
別担当がcleanupを使わないcount-subset表現で独立数学監査した。

少数の直結した危険な強化を反証した。
Pだけのclosed-neighbor一致は三点辺で壊れる。自己同型の一軌道は全置換classではない。
rank4でclass全てを3点以下へ誘導削除することも反証される。

全7020小clutter、X6点/外部2・3点/rank4の全122+5097交換不変clutterを
別占有subset DPで検査。独立count-subset mexでも同族と720広rank族が一致した。
さらに孤立点2個のmisère補助mex周期を証明し、同じkernelがmisère h/P/Nも
保存することへ一般化した。misèreで成分xorは使わない。

n11の200本greedyから826 late snapshotsを保存。253で縮み、188で内部容量classを
縮める。mixed depth≥2の非内部class削除は0。最大初期削除7点。
|L|≤14の727 snapshotsの通常値とmisère補助mexを独立検査。
通常memo合計17324→10477（kernel）、9341（kernel+既知成分xor）。
安価な全incidence hash検出では10572/9398。

一回の小規模Python測定ではbaseline約0.24秒、kernel+成分約0.55秒、
hash+成分約0.46秒で、速度gate未達。R生成コストも除外されている。
したがって共有df-pnへの常時kernel検出は導入せず、証明とprototypeを保存する。
状態数節約と速度改善を混同しない。実geometry証人を二つ独立監査したうち、
連結Rと極小三点辺を持つ例はg=4、memo36→17（成分も併用すると14）。

今後は実exact handoffで全R生成を含む費用を測定し、まず容量1 hash検出を
有効にする条件を決める。未知classが同一kernelになる場合のcache共有も
候補だが、実探索への効果は未検証。11×11空盤は引き続きUNKNOWN。

現在の結論はknowledge項目、再現資産は
`research/experiments/n11-reduction-followup-20261005/` に保持する。
