# 2026-11-19 n11 長期レーン: 残余86行のadd-one-stone候補拡張と43-witness掃引・第9〜第12 WIN7-D10証明書・4-receipt fold・resolve5

## 経緯

- 前回実行（K1046出版）で117-rootプールはdepth-10完全判定済み（109 REFUTED + 8 WIN）。
  残余86行（5親target 26/112）はプール内候補では全行strandedであったため、
  今回は86行各行に1石追加した新規7石root候補の全体censusから再開した。
- 採用規約は K1046 の教訓を継承: probe driverは(child,bit)分解に生のmaxbit childのみを使う
  （canon_hex被せ事故の再発防止）。

## 今回の成果（K1057 itemとして出版）

1. **86行census（expand86.py）**: universe 8,663（D4重複除去後）。内訳 in_pool 98・
   known_refuted 7・known_win 0・fresh 8,558（safe 5,142 / unsafe 3,416）。
   既知(WIN receipt 8 root)は86行を0行しか被覆しない。
   multi-cover（3行以上を被覆するfresh-safe root）は0本で、pair候補のみ
   （pair edge 835）。maximum matching **43** が86/86行を完全pair被覆し、
   witness 43 rootを決定した（greedy set-coverなら46本が必要）。
   二回実行はbyte-identical（census JSON SHA-256 6fe87d61…）。
2. **43-root witness掃引（sweep43）**: runner v17・depth 10・cap 30M・両AND順序・
   pilot_d6（3,402 nodes）86 probe全件合格。**WIN 4 / REFUTED 39 / CAPPED 0・順序矛盾0**。
   総nodes 173,165,148。raw生76 probe記録を出版。
3. **第9〜第12 WIN7-D10証明書**: WIN 4 rootから証明書を抽出。
   - 第9  `00000000000000801202000001040200`（72合法手・3,765,226 nodes・84,928行。
     正本は3,069,801 bytesのためgzip+base64の `.n11.gz.b64`（561,188 bytes）として出版。
     `base64 -d <file>.gz.b64 | gunzip > <file>.n11` で復元、SHA-256 503ff9da…と一致）
   - 第10 `00000000000000821082040200000000`（56合法手・2,536,415 nodes・45,450行）
   - 第11 `00000000000000821092200000000000`（47合法手・702,661 nodes・24,375行）
   - 第12 `00000000001020003800000048000000`（51合法手・834,730 nodes・26,756行）
   4枚とも BigInt 3×3余因子展開＋4×4 Bareissの二重独立検証（全subroot PASS・
   union差分0・cross-method状態流量一致・終局石数[13,17]・fbt_drops 0）。
   .n11テキスト正本を出版（SHA-256はMANIFEST参照）。
4. **4-receipt fold**: 閉鎖9 S6行（8 target行＋第10のextra 1行）、
   closed_edge_cost 667。frontier 6,222/492,688 → **6,213/492,021**、
   solved S6 1,626→**1,635**、parent incidence 11,848→11,826、
   5親target **26→34/112（残余78行）**、fully-closed parent 0。
   verdict universe（明示pinned source結合）は340/164→379/168、矛盾0。
5. **resolve5**: 第12fold後の残余78行について再解決。universe 7,969
   （in_pool 93・known_refuted 46・fresh 7,830: safe 4,728）。
   39本のREFUTED witnessは全て78行universe内、4本のWIN witnessは閉鎖済み行のみを
   被覆していたため不在（この整合性をgateで明示検証）。
   既知WINは78行を0行被覆、multi-cover 0本、pair edge 706・maximum matching **39**が
   78/78行を完全被覆、**stranded 0**（greedyなら42本）。
   39 witnessは次回depth-10掃引の条件付き計画であり証明書ではない。

## 構造観察

- census-43掃引は「43 pair witness → 4 WIN（8行閉鎖）+ 39 REFUTED」となったが、
  fold後にmatchを組み直すと残余78行がちょうど39 pairで完全被覆された
  （deflation 43→39）。REFUTED witnessの担っていた行は全てfresh代替pairで
  再結合できたことになり、このレーンの候補供給構造は現時点で枯渇していない。

## 解釈規約（既存レーンと同一）

- REFUTED-D10はLOSS証明ではない。foldは行被覆の簿記であり行のゲーム理論的値には
  一切言及しない。witness群は条件付き計画。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手（次回実行・着手前に必ず最新mainを取り直す）

1. **39-witness掃引**（resolve5の計画実行）: 39 root × 両順序 = 78 probe。
   WINが出れば証明書抽出→fold→残余の再解決（deeper expansion・depth>10は
   stranded行が出てから）。
2. fold後に残る行群がstrandedになった場合のみ、add-two-stones拡張または
   depth>10探索コストの測定に進む。
3. 並走レーンとの重複確認: sweep43の43 rootとresolve5の39 witnessは
   117-rootプール外の新規rootのため、既存の118root系掃引（probe_driver18系）と
   重複しない。
