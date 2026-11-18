# 2026-11-18 N11 cost-16 parent（00000000000000003800000008001000・31行）最小coverのA型総数・singleton membership厳密解析

## 成果

cover表で4番目に安い（runner-upの次の）対象 parent `00000000000000003800000008001000`（31 open non-STERILE行・cost 16 exact・2,333候補・1,908 root = 425 pair type（すべてmultiplicity 1）+ 1,483 singleton）について、**A型最小cover総数と全1,483 singleton rootのmembershipを厳密に決定**した。31行は本プロジェクトで厳密計算した最大のparentである。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/cost16_parent_membership_20261118.py`（2段階出力設計: phase A出力をphase B前に書き切る）
- output: 同dir `output/cost16-a-phase-20261118.json`（blob `fe4b4b55`）
- 12 checks all PASS。phase Aは4回の実行すべてが完走し、総数・memo状態数・全数値が完全一致（singleton位相34.6〜36.1秒/回）、outputはbyte-identical（blob sha一致）を確認。

## 主要数値

1. **A型総数 = 2,305,787,291,293,934,388（約2.3e18）**: 15 disjoint pair + 1 singleton 型の最小cover計画数。**29行runner-upの全最小cover総数（4.59e16）の約50倍**で、行数2行増で総数が約50倍に跳ね上がった。ただし**A型は総数の下限成分であって総数ではない**（B型 = 16 pair・1行二重被覆型は未計算・下記参照）。
2. **全1,483 singleton rootのmembership確定**（= pm(V∖s)・行s上のrootはすべて同値）。min 1,415,501,771,326,047 / max 1,798,095,446,108,235（Aの0.078%）で、行ごとのpm値は27%以内に収まる極めて平坦な分布。恒等式 Σ(singleton membership) == A が厳密に成立（A型coverはsingletonをちょうど1本含む）。
3. 構造: witness 16本（15 pair + 1 singleton）全行被覆・bottleneck行18（cover options 64）・行2/3/13がpair degree 30のハブ。
4. **anchored状態空間の行数非依存性の実測**: 31行parentの最初の30行anchored木は1,346,254状態（11.9秒）で、29行runner-upのsingleton位相の全union（1,346,267状態）とほぼ一致（差13状態）。到達可能状態空間は行数でなく候補構造（両parentは同じfold族の近縁行集合）で決まることを示す実測で、全174 parentの計算費用予測に使える。

## 検証

- 実装検証: 出版済み29行runner-up output（blob `05f54eb5`）の**全1,505 singleton membershipを同一実装が完全再現（0不一致）**。
- cover表（blob `4e4a911d`）との整合: 行数31・候補2,333・root 1,908・span histogram・cost 16 exact・witness構造をすべて機械照合。
- phase A二重実行 byte-identical（総数・memo状態数3,524,561・全数値一致）。

## phase B（pair membership・B型総数）の実験的事実

pair-membership位相（425 root×約5,700 pm呼び出しの28行木）は**4回の実行すべて、開始後数十秒で原因不明のSIGKILL相当で kill**された（tracebackなし・コンテナRAM 3.2GB上限のOOM-killが最有力）。29行parent（26行木・memo 920万状態）は完走できたが、31行の28行木では一時的なDFS収集バッファ（seen/orderで各木の状態数分）が効き、メモリ上限を超える。**次回は収集をchunk分割して一時バッファを上限する設計**（またはより大きいホスト）が必要。B型総数・pair membership・top-50/jointは未確定のまま次回課題。

## 解釈上の注意

A型総数は代替最小cover計画の組合せ数であって探索コストでもverdictでもない。本分析はcover計画の組合せ論のみを主張する。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
