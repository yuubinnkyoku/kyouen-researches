# n11 長期レーン: depth-11コスト測定パイロット標本拡張: 単一オーナー宣言ノート（2026-11-20）

depth-11コスト測定パイロット（commit 1a2021979b・宣言ec5b09c1）は2 root・4 probeで
倍率バンド +0.04%〜+2.2% を得たが、**標本が2 rootに限られる**ことが弱点として明示されている。
本レーンは同じ宣言規約の下で**K1069 REFUTED-D10分類の38根から決定論的規則
（sorted化した38根のindex {0, 12, 24, 36}）で4根を選び**、同一プロトコル（runner v17固定
blob c132cc64…・cap 30M・timeout 280s・両AND順序・pilot_d6制御・逐次）でdepth 10とdepth 11の
両方を測定し、倍率標本を拡張する。

- 対象: `00000000000000003800000008001220`（bit 5）・`00000000000000801202000000880100`（bit 8）・
  `00000000000000889042000080000000`（bit 31）・`00000010000000801202000000400400`（bit 10）。
  すべてK1069正本（SHA-256 22953ae1…）のclassificationでREFUTED-D10。
- depth-10側はREFUTED-D10分類との整合（両順序loss=false・uncapped）をgateとする。
  環境timeoutは「当該環境で未検証」、値不一致はfail-closed。
- depth-11側のコスト取得は追加の宣言を要さない（本宣言の範囲）が、**判定・分類・行の閉鎖は
  一切行わない**。depth-11でloss=falseが得られてもそれは行閉鎖でもREFUTED-D11分類でもない。
- 出力は `research/experiments/n11-depth11-cost-scaling-pilot-ext-20261120/`。
  assembleはK1069正本のパスを引数に取り、対象4根のmembershipとSHA-256 pin
  （22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc）を検証する。
- 36-root sweep本体は掃引オーナーレーン管轄のまま着手しない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
REFUTED-D10 は LOSS 証明ではない。**（確認時HEAD: 5548f6ac23）
