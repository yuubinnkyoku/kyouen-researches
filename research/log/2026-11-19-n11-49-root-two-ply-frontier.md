# 2026-11-19 n11: exact two-ply frontier and cross-root D4 sharing for the 49-root residual cover

開始時のmainは b2c52eb93fcc9f5f48791fc37829aee9cf8e504a。最新AGENTS.md、research/knowledge/README.md、K0001/K0002/K0023、K0863/K0865/K0868、49-root residual witness、既存のcache非所属・一手mobility監査を確認した。対象は残97行の最小49-root候補（2行被覆48本・1行singleton 1本）。

K0001/K0868の整数det4規約を使用。BigIntの三項余因子展開と六項Leibniz展開を28,553個の3点組×121点（3,454,913件/方式）で照合し、49本の一手候補集合も既存mobility bit集合と49/49一致した。

- 8石子: 2,985局面。合法応手数28〜73、終局子0。
- 順序付き二手目: 146,118。
- 9石の異なる局面: 73,059。
- 各root内のD4重複: 0。
- 49本横断のD4正準類: 72,756。共有重複303（0.4147%）、213 root pair。共有類は全て2 rootだけに属し、3 root以上の共有は0。

最大共有はroot 00000000000000801202020001001000（S6行00000000000000801202020000001000/00000000000000801202020001000000）とroot 00000000010000809002000040100000（S6行00000000010000809002000000100000/00000000010000809002000040000000）の47類。それぞれのfrontierは1,061類と1,707類、和集合2,721類。47共有状態の正準hexは結果JSONに保存した。

最小一手分岐47のroot 00000000000000821082000010800000 は二手先でも最小881局面（順序付き1,762手）。次点は49手・957局面。小probe候補は維持するが、分岐数は実DFPN費用ではない。9石層の共有cache利得は浅層で約0.415%に留まり、深い層の共有率は未測定。

再現スクリプト research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/scripts/audit_49_root_two_ply_frontier_20261119.mjs と結果JSON research/experiments/n11-head1410-residual-cover-after-receipt-fold-20261119/output/49-root-two-ply-frontier-20261119.json を追加。mobility/residual、K0001、K0868はGit blob SHAで固定。今回の計算は接続JavaScript実行環境で行い、公開スクリプト自体はrepo checkout上で未実行。未知盤の長時間workflowはAGENTS.mdに従い起動していない。

新しいWIN/LOSS verdict、WIN7-D10証明書、receiptはない。8石子に終局がないことは即時勝ち手がないだけで、49 rootのLOSSを意味しない。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWNのまま。
