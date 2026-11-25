# 2026-11-18 n11 head-1476 S5 parent再分類とclass-2 11行の候補被覆

## 背景

最新mainは `aa3af62b6394699d42fe08a62bc8c5032717545a`。AGENTS.md、knowledge README、K0863/K0865/K0868、head-1410 worklist、head-1410 census、head-1410→1476の10 fold ledgerを確認して再開した。

直近の全fold台帳監査は、cost76cのparent Bエントリが77e行を二重計上していることを検出した。これはparent単位の記述誤りで、大域head算術には影響しない。本再計算では誤記されたBのafter値を使わず、ledgerが確定した大域66行の閉鎖集合と、独立に再導出したD4 parent-child関係だけを使う。

## head-1476の全174 parent再分類

従来の5-subset canon indexとは別に、各5石parentのD4像8個を直接作り、6石worklist行への包含を全174×6,438組で判定した。head-1410時点で、174 parentすべてについて行数・edge cost・STERILE行hex集合がK0865 censusと完全一致した。その後、10 foldの大域閉鎖66行を差し引いた。

- head-1410: 6,438行 / cost 509,109 / parent incidence 12,274 / STERILE incidence 91
- head-1476: 6,372行 / cost 504,389 / parent incidence 12,143 / STERILE incidence 91 / effective incidence 12,052
- parent分類: head-1410は all-STERILE 3・partial 57・no-STERILE 114、head-1476は **all-STERILE 4・partial 56・no-STERILE 114**
- 66閉鎖行と35 STERILE行の交差は0。K0863の定理に反するSTERILE行のreceipt閉鎖は起きていない。

新たに全残行STERILEへ移ったparentは `00000000000000801202000040000000`（class 2）。head-1410では5行/cost364中2行/cost135がSTERILEだったが、head-1476では残る2行が両方STERILEになった。したがってD10 WIN7 receipt体系ではこのparentも閉鎖不能。ただしLOSSではない。

head-1476の全STERILE parentは次の4件。

- class 2: `00000000000000801202000040000000` — 2行 / cost 135
- class 2: `00000000000000801202000000200000` — 3行 / cost 209
- class 3: `00000000000000809082000000000000` — 10行 / cost 698
- class 4: `00000000020000003800000080000000` — 18行 / cost 1460

## 次のclass-2候補を11行へ縮小

D10 receiptで閉鎖不能な行を除いたclass-2 parentを、残存する自前候補costで再順位付けした最上位は `00000000000000403800000008000000`。

- head-1410: 24行 / cost 1,704
- head-1476: **11行 / cost 806**
- STERILE行: 0
- 11行の全806候補は既存cache・D4転送後もOPEN（WIN 0 / REFUTED 0 / transferred REFUTED 0 / open 806）

11行それぞれの候補をBigInt det4で再列挙し、worklist edge costと11/11一致した。候補806件を7石rootのD4正準形にまとめると757 root class。内訳は単独行をcoverする708 root、2行をcoverする49 rootで、3行以上をcoverするrootは0。

よって11行を覆うroot数の下界はceil(11/2)=6であり、実際に6 rootの被覆が存在する。**最小6 root coverは337,020通り**（singleton/perfect-matching計数5,250を用いて独立計数）。一例の辞書順最小cover:

1. `0000000000000040380000000800000a` → `00000000000000403800000008000008`
2. `00000000000000403800000008004020` → `00000000000000403800000008000020` / `00000000000000403800000008004000`
3. `00000000000000403800000408200000` → `00000000000000403800000008200000` / `00000000000000403800000408000000`
4. `00000000000000c09002000200001000` → `00000000000000c09002000000001000` / `00000000000000c09002000200000000`
5. `00000000010000809003000000000001` → `00000000000000801206000000000400` / `00000000000000c09002000000400000`
6. `00000000020001003810000008000000` → `00000000000000403800400008000000` / `00000000000000c09002000000002000`

この6本がすべてWIN7-D10証明書を得れば11行すべてを閉じられる、という幾何学的な候補計画である。現時点では6本とも未探索であり、証明書でもreceiptでもない。REFUTED-D10はLOSSを意味しない。

## 候補会計

worklist全体では9行/cost635が既存receipt予約（category `win_receipt_scheduled`）であり、status列は0のまま予約枠として扱われる。残り6,429行では own candidate cost と WIN + REFUTED + transferred REFUTED + open の和が一致する。全体statusは WIN 4・REFUTED 2,777・transferred REFUTED 18・open 505,675。予約9行を通常のopen候補と混ぜない。

## 再現・成果物

同じ入力blob pinで2回再計算し、JSON全体がbyte-identical、745/745 checks PASS。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/recompute_head1476_parent_census_and_class2_cover_20261118.mjs`
- result: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/head1476-parent-census-and-class2-cover-20261118.json`

この環境ではrepo checkout上のNode実行はできないため、計算本体は利用可能なJavaScript実行環境で実行した。公開したmjsは同じ入力blob SHAを検査して再現するための標準Nodeスクリプトであり、checkout上での実行済みとは主張しない。

## 解釈境界・次の作業

新しい7石verdict・certificate・foldはない。次の作業は、この11行に対する337,020通りの最小coverから、既存coordinatorの測定済み費用情報で探索順を決め、選んだrootだけを探索すること。今回の6本例を固定の最適順とみなさない。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。
