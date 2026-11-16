# 2026-11-16：STERILE行depth-10閉鎖不能性定理確定 — 全合法候補REFUTED-D10のS6行（65k/70j/74h）はどのWIN7-D10 receipt rootにもcoverされない（位置レベル補題+D4不変性・完全route枯渇455/490/518経路を機械検証）・70j erratumのcross-cover文言の過大訂正・head 1410不変

開始時main: `909b7690`（cost-64c sweep着地・64/64 REFUTED・STERILE）。

## 実施内容

### 1. 定理本体（証明・trust境界はlane全verdictと同一）

**定理**: STERILE行（全合法候補rootがREFUTED-D10・0 cappedの6石行R）は、自出行・cross-coverを問わず、どのWIN7-D10 receipt rootにもcoverされない。

- **補題（位置レベル・engine不使用）**: X covers R ⟺ canon(X) ∈ {canon(R+t) : t ∈ legal_candidates(R)}（X=σ(R+t)の存在同値。receipt rootは安全で、D4等長変換は安全性を保存）。
- **証明**: XがRをcoverすれば補題よりX=σ(R+t)。STERILE性よりverdict(R+t)=REFUTED-D10、ゲーム規則のD4不変性よりゲーム木同型でverdict(X)=REFUTED-D10 → WIN7-D10 receiptと矛盾。∎
- 前提はengine depth-10 verdictの健全性・D4不変性のみで、当レーンの全出版verdictと同一trust境界。前提が破れれば2 sweep間のverdict矛盾として検出可能。

### 2. 完全route map — 近傍sweepでの閉鎖は原理的不可能

best coverable class-2 S5 `00000000000000801202000000200000`（3行/209・全行STERILE）の3行65k/70j/74hについて、canonical一石置換近傍（689/636/689軌道・出版neighbor analysisと一致）の全近傍childから自出行・cross-coverの全経路（65k 65+390=455・70j 70+420=490・74h 74+444=518）を列挙し、**全経路がown candidate bit tの(σ, t) witness付きで表示される**ことをverifierが全件検証（V5）。全経路のown candidateは出版verdictリストのREFUTED-D10に含まれるため、近傍sweepをどれだけ回しても3 STERILE行の閉鎖は原理的に起こらない。

### 3. 機械検証 `verify_sterile_unclosability_20261116.py`（stdlibのみ・約6秒・V0-V6全合格）

- V0: 7件+70gの候補リストbit-exact再現。V1: canon陽性対照（ROOT_D4・bit-92第7削除canon・bit-6/bit-84/bit-10 covers）。V2: 出版cost≤70 route map 17子完全再現（24経路）。V2s: 掃済6経路witness（60c bit 119・62b bits 21/109・64c bits 111/119+65k bit 119）全てown candidateのREFUTED-D10へ写像・REFUTED-REFUTED一致6件。V3: 最近5 WIN receipt roots（75e bits 6/10/11/37・60c bit 92）は3行をcoverしない。V4: 先例整合。V4c: 70f bit-84 rootと70g child+bit 29のWIN-WIN一致（canon同一・2独立sweep間のD4 verdict転送の正の対照）。V5: 完全近傍route枯渇。V6: 決定論（新プロセス2回バイト同一・audit sha256 6221d1ae…）。
- verdict一致は計8件（REFUTED-REFUTED 6・WIN-WIN 1）・**矛盾0**。

### 4. 70j erratum訂正の訂正

70j claim erratumの「STERILE行も他childのWIN7 receiptのmarginal経由で閉鎖され得る」は**過大訂正**。引用先例 (a) 70f bit-84のcover先は70g child自乗sweep **8 WIN7-D10**（bits 9/20/29/34/62/70/76/119）の非STERILE行（V4c WIN-WIN一致）、(b) 75e bit-10のcover先は未sweep行。いずれもSTERILE行ではなく定理と無矛盾。cross-cover閉鎖は「未sweep行・WIN有り行」にのみ可能。

### 5. out-of-sample予測の的中・継続予測

定理は並走64c sweep着地前（claim d5d3d532時点）に「bits 111/119（70j・65kをcoverする唯一根）はREFUTED-D10」と予測し、sweep完了（64/64 REFUTED・0 capped・v15+v16一致）で的中。定理は今後のsweepに対する強い否定的予測として運用できる（STERILE行をcoverするWIN7-D10が出たらverdict矛盾・WIN/LOSS conflict調査対象）。**継続予測**: 並走のcost-69a IN FLIGHT claim（0379929e・bit 109が65k/74h両行をcoverする唯一残存dual-root）に対し、定理はbit 109根のREFUTED-D10を予測する（完全route mapの74h cross経路 bit 109は74h own candidateのREFUTED-D10へ写像済み・V5で全件検証）。

### 6. 副産物 — 60c fold bit-92記録の第7削除canon

60c bit-92のmarginal 6件に加え、第7削除canon `00000000000000801212200000000000`（stones [45,49,52,57,60,71]）が存在。fold意味論（marg=covers−s_1407・covers=7/marginal=6）から1407時点で既coverと強制される（head簿記は無影響・記録整合性の観察としてauditに保存）。

## 構造的事実・帰結

- best coverable class-2 S5（3行/209）は**depth-10 receipt体系では証明的に閉鎖不能**（coverable rankingからdepth>10証拠待ちカテゴリへ移すべき）。隣接childのsweep価値は他parent需要・自身の閉鎖目的で残るが、STERILE行閉鎖の目的には一切寄与しない。
- solved 1410はmanifest被覆の簿記。REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。

## 次の状況

- canonical head **1410**不変。76c/76d/77e foldは並走claim済みで着手禁止（着地時は1410とのreconciliationが必要だが、本定理はbaseline独立の位置レベル解析なので影響なし）。
- **11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま**。本定理は閉鎖手段の不可能性のみを言い、行のゲーム理論的値には一切言及しない。
