# 2026-11-18 N11 検証側: 5最安cover target joint分析へのcost-16 parent拡張（blossom exact辺coverによる全31 subset厳密決定）

## 背景

セッション開始時のmainは `b10b397cd25e065f197683eeb3a3f86149e8f422`（amendments反映済み）。既刊の joint parent cover sharing 分析（`joint_parent_cover_sharing_20261118.py`・blob `f1a4783292897a6e9128dc1a5718617a33b119a1`・published `joint-parent-cover-sharing-20261118.json`）は4最安parent（個別exact最小cover cost 6/9/12/15・合計42）の15 subsetを「lb=ceil(r/maxspan)+greedy matching witness（60 restarts）」で扱い、4-way joint 41（benefit 1）を確定していた。cost-16 parent（`00000000000000003800000008001000`・31行・個別cost 16・published cost table で exact）は未統合だった。

## 手法: exact辺cover決定（greedy witness探索の置き換え）

cover table・phase-1列挙のいずれのsubset universeでも、各候補rootの被覆行数は高々2（span ≤ 2）。このとき**最小coverサイズは r − m**（r=対象行数、m=pair graph（行を頂点、あるrootがちょうど2行をcoverするとき辺）の最大matching）として厳密に決まる。下界は任意coverの2-rootから取り出せるmatchingによるcharging、達成は最大matchingの各辺にwitness root 1個＋ unmatched各行に被覆root 1個でsize r−mのwitness（機械検証）。greedy restart witnessと異なり、witnessがlbに届かない場合も最大matchingで厳密値が確定する。

最大matchingはself-containedなblossom（一般グラフ・e-maxx流）で計算し、決定的乱数（seed 20261118）の小グラフ3,000件をbrute forceと照合してin-script検証（0不一致）。runway: 列挙JSONL（6,337行・blob `89b24065d0588b0891395c9283e3a5b3d5551595`・published enumerate scriptから決定的再生成・published joint outputのbyte-exact再現に使用したものと同一）を再利用。

## 結果（31 subset全て exact・91 checks all PASS・二重実行byte-identical）

- **5-way joint（5最安parent全体）: 112行（11+18+23+29+31・互いに素確認）、lb=56、最大matching=56、exact最小cover=56**。個別合計58に対し**benefit 2**（58→56）。112行のperfect matchingが存在し、witness 56 rootを機械検証済み。
- cost-16単体: 16・exact・benefit 0（published cost tableと一致）。
- cost-16を含む新規pair/triple/quad: {c6,c16}=21/22（benefit 1）・{c9,c16}=25/25（**benefit 0**・cross-parent root 0でshare不可）・{c12,c16}=27/28（1）・{c15,c16}=30/31（1）・{c12,c15,c16}=47/49（**benefit 2**）・{c9,c12,c15,c16}=51/52（1）・{c6,c9,c12,c15,c16}=56/58（2）など。benefit 2は {c12,c15,c16} と5-wayの2組。
- 既刊15 subset（4 parentの全組み合わせ）は本方式で**全てpublished witness sizeと一致**（0不一致・published「exact」主張の独立確認）。
- cross-parent rootの分布: cost-16と {c15:10, c6:6, c12:9} 個（c9とは0・{c9,c16} benefit 0と整合）。

## 解釈境界

有限の簿記・組合せ計算のみ。cover意味論（root=行の1石D4正準形拡張候補）は各rootがcertificateとして妥当であることを前提とした計画計数であり、WIN/REFUTEDの主張ではない。REFUTED-D10とSTERILEはLOSS証明ではない。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。

## 成果物

- script: `joint_parent_cover_sharing_cost16_20261118.py`（blossom内蔵・pinned inputs 6種）
- output: `joint-parent-cover-sharing-cost16-20261118.json`（31 subset・91 checks all PASS）
