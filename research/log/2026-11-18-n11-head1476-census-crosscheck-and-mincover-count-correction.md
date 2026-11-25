# 2026-11-18 n11 head-1476 parent census・class-2 coverの検証側クロスチェックと最小被覆計数の修正

## 背景

最新main `3b307854171947aaedfcc83b5d3ea7217b92f84d`(着手時点)を確認し、AGENTS.md・knowledge README・K0863/K0865・head-1410 worklist・head-1410 census・head-1410→1476 fold ledgerから再開した。検証対象は並走の3コミット(`abaa3874` / `e652dd78` / `658597f0`)で出版された「head-1476 全174 S5 parent再分類とclass-2 candidate cover」。

## 第三実装による独立クロスチェック

検証器 `crosscheck_head1476_census_and_class2_cover_20261118.py` は、既存の2実装(parent側8像包含join・BigInt det4・singleton/matching計数)と手法が異なる第三実装として全数値を再導出した。

- parent-child D4 join は row 側から(各行の6つの5石subsetのD4正準形を parent 正準形と照合)。parent 側8像包含とは逆方向のjoin。
- 最小被覆計数は 2^11 counting DP と、完全マッチング全列挙(除外頂点11×945マッチング)による形状別分解の二通り。
- 出版JSONの全派生値(174 parent baseline・head-1476再分類・fully-sterile 4 parent・class-2 ranking top12・selected parentの11行・757 root全表・辞書順最小被覆・候補会計)をfield単位で照合。
- 入力は git blob pin(worklist `2fee1d07` / census `9c251da3` / ledger `e8785d50` / 出版JSON `8e870809`)。

結果: **978/978 checks all PASS・二重実行byte-identical**。

独立再現した主要数値:

- worklist 6,438行 / cost 509,109 / baseline incidence 12,274 / sterile incidence 91 / effective 12,183 / 分類 3+57+114
- 閉鎖66行: worklist内・cost総和 4,720(= 509,109−504,389)・open_parents列総和 131(= 12,274−12,143)・STERILE 35行との交差 0
- head-1476: 6,372行 / 504,389 / incidence 12,143 / sterile 91 / effective 12,052 / 分類 **4+56+114**
- 新規全残行STERILE parent は rank-1 parent `00000000000000801202000040000000`(2行/135)のみ、残る2行は両STERILE
- class-2 own-closable 最上位 `00000000000000403800000008000000`(head-1410 24行/1,704 → head-1476 11行/806・STERILE 0)
- 11行の det4 候補再列挙が worklist edge cost と 11/11一致・全候補OPEN(WIN 0 / REFUTED 0 / transferred 0 / open 806)
- 806候補 → 757 D4 root class・被覆ヒストグラム 708(1行)+49(2行)+0(3行以上)・最小被覆 6 root
- 辞書順最小被覆 6 root は出版記録と完全一致(root hex・cover_rows・occurrences (row,bit) 全照合)
- 候補会計: win_receipt_scheduled 9行/635(予約扱い)・非予約6,429行の恒等式・全体 WIN 4 / REFUTED 2,777 / transferred 18 / open 505,675

## 所見1: 最小被覆計数の過少(337,020 → 359,610)

出版記録は「最小6 root coverは337,020通り」(all_minimum_cover_sets)としているが、この計数(singleton×perfect-matching積)は**分割型**(5つの disjoint pair root + 1 singleton root)のみを数えている。最小被覆には**重なり型**(6つの pair root・ちょうど1行が二重被覆)も存在し、22,590通りある。最小6 root被覆の総数は **359,610**通り。

- 2^11 counting DP: 359,610
- 分割型の直接計算: 337,020(= 出版値と一致)
- 重なり型の直接計算: 22,590
- 三方向の一致で確定。重なり型の計数根拠: 6 root × 最大2行 = 12 ≥ 11 なので、6 pair root がちょうど1行だけ二重被覆する形があり得る。出版の計数は「最小被覆は必ず分割型」という暗黙仮定に依存していた。

重なり型最小被覆の具体例(行 `00000000000000403800000008000008` が二重被覆・6 root全てが2行被覆・union 11行):

  - `00000000000000403800000008000028`
  - `00000000000000403800000008004008`
  - `00000000000000403800000408200000`
  - `00000000000000c09002000200001000`
  - `00000000010000809003000000000001`
  - `00000000020001003810000008000000`

影響: 最小被覆サイズ 6・下界・辞書順最小cover・候補計画はすべて不変(全最小被覆がちょうど6 rootであることは変わらない)。純粋な計数ラベルの誤りであり、既存の出版mjs check名 `candidate.minimum_cover_count` も同様に分割型計数を総数として扱っている。

## 所見2: 出版mjsの再現性

出版mjs(git blob `da06826256ecf24650bd178653cd91117708be55`)を、pin済み入力3ファイルを再構成したcheckout上で2回cold実行した:

- 両run byte-identical・**735/735 checks all PASS**
- log主張の全headline数値(6,372/504,389・4/56/114・12,143/91/12,052・806/757/708+49/6・337,020・5,250)を再現
- ただし出版JSON本体はより前の745-check版(schema・check名が異なる実装)で生成されており、出版mjsではbyte再現できない。出版logの「745/745 checks」はこの未出版版を指す
- 出版JSONと出版mjsの間に実質的な数値の不一致は見つからなかった

## 成果物

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/crosscheck_head1476_census_and_class2_cover_20261118.py`
- result: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/crosscheck-head1476-parent-census-and-class2-cover-20261118.json`(二重実行byte-identical)

## 解釈境界

- engine実行なし・新規7石verdict/receipt fold/S5 closureなし。6 root被覆は将来のWIN7-D10証明書を仮定した幾何学的候補計画に過ぎない。
- REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。
- 標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。
