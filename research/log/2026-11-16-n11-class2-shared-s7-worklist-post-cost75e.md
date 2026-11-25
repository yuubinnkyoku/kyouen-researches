# 2026-11-16：cost-75e fold後の第二候補S5を5行/364へ更新し、354件の一意S7 worklistを再生成

作業開始時main: f0c9a005d797a6f496772ff8edb8a19782cf837b。直前のab9ecaeはK0832の生成ビュー更新のみ。f0c9のcost70j claimは別の最良class-2 S5を対象とし、この第二候補S5の5つのS6 mask・盤規則・cost75e foldには変更がない。AGENTS.md、knowledge README、K0023/K0105/K0783、cost75e fold出力、現在のtop-candidatesを確認した。

## cost-75eの確定進展

cost-75eの4つのWIN7-D10証明書（bits 6/10/11/37）が公開され、BigInt 3×3と整数Bareiss 4×4の独立検査で全234 sub-rootが通過。manifestは203,163行、7,352,075 bytes、62,175,955 extraction nodes。bit6は2分割＋receiptで全体bytesを再構成・検証した。

4 receiptをreconciled head 1405へfold：
- 1405/6443/509457/4713/373180 → **1407/6441/509300/4711/373023**
- 総marginal 19、うちin-manifest marginal 2
- cost75eのS6 child orbitはbit6 receiptでちょうど1回閉鎖
- bit10のin-manifest marginalは00000000000000801202000000000201。cost75e parent2とcost70g parent2にedge 82で重複していた行を1回だけ閉鎖
- 4 rootのdisjointness、raw batchからのsweep再導出、決定性再実行、v15 crosscheck、集合等式、逆順replay一致を確認

第二候補S5 00000000000000801202000040000000は **6行/439 → 5行/364**。cost75e parent2 00000000000000801202000000000200は67行/5473 → 65行/5316。最良class-2候補は別のS5（3行/209）。

WIN7証明書は個別7石rootの先手勝ち証明。REFUTED-D10はLOSS証明ではなく、manifestのsolved数もS5親や空盤の勝敗値ではない。

## 現在の5行から作った一意S7 worklist

残るS6子はcost64a/71d/76c/76d/77e、合法手数は64+71+76+76+77=364。cost75eの75候補はfold済みなので除外した。別のD4座標変換実装と整数lifted determinantで共通S5座標への整列、合法手、S7 root、第一応手を再生成した。

- 364候補出現 → **354個の異なるraw S7 root**（D4軌道も354）
- 重複root 10件。上位3件の合法第一応手数は73/72/72
- root重複除去で第一応手辺648本を除去（22,174 → 21,526）
- 異なる8石局面10,449個。全70四点部分集合731,430件を検査し、共円違反0
- root重複除去後の潜在再訪11,077件。実測TT hit・節点削減ではない
- 2つのS6群から到達する8石局面618個、3群から10個
- 2つの一意S7 rootから到達する8石局面9,821個、3 rootから628個

424件worklistはcost75e fold前の歴史的snapshot。現在の探索入力は354件版を使う。完全なworklist JSONはスクリプト出力から再生成できる。2回の実行はbyte-identicalで、圧縮出力SHA-256はdcface6695e6297e5596f987cc02bbe848b3fc640a3c9566bd8584cac80b7d04、展開JSON SHA-256はc064f3d45205f15bd4f7037bdb741d9d3df8e292a126613c7cbe6203d0d49c32。

## 次の判断

424→354は候補rootの一意化であり、探索節点が同率で減るという意味ではない。shared engineの実測はまだ行っていない。次は354件から重複rootを除いた固定小集合でfresh engine対shared engineを比較し、root別節点数・TT hit/store・占有率・挿入失敗・WIN/LOSS一致を測る。

cost76cのin-flight claimはhead 1407へrebaseが必要。cost76d/77eの並列claimもhead 1405固定なので、fold時には1407とのreconciliationとroot disjointness確認が必要。共有計算機の稼働サービスを避け、今回は長時間探索を起動していない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWN。** 1407はmanifest被覆数であり、11×11の勝敗決着ではない。

## Artifact
- research/experiments/n11-class2-shared-s6-child-overlap-20261116/audit_post_cost75e.py
- SHA-256: 59589079ca10111ce89038929dca2f683f570b8324db653ff2163d720df4e922
