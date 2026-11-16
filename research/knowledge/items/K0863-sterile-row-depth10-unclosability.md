---
id: K0863
title: STERILE行depth-10閉鎖不能性定理 — 全合法候補がREFUTED-D10・0 cappedのS6行（STERILE）は自出行・cross-coverを問わずどのWIN7-D10 receipt rootにもcoverされない（位置レベル補題「X covers R ⟺ canon(X) ∈ 自出行候補のD4正準形集合」とD4判定不変性による）、best coverable class-2 S5の3行65k/70j/74hの完全route枯渇（自出行65/70/74・cross 390/420/444経路すべてがown candidateのREFUTED-D10へ(σ,t) witness付きで写像）、70j erratumの「STERILE行もcross-coverで閉鎖され得る」は過大訂正（引用先例は未sweep行かつ70g childは8 WIN7-D10の非STERILE行）
kind: proposition
status: proved
topics: [certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0783
  note: n11 S2{59,60} milestone-5のMS5 S6 manifest・S7 edge cost・WIN7-D10 receipt/cover機構（foldのmarginal閉鎖・D4正準化covers）の定義を継承し、その体系内の不可能性を証明する
artifacts:
- path: research/experiments/n11-class2-lane-sterile-unclosability-20261116/report.md
  role: proof
  note: 定理・補題・証明（trust境界の明示）・完全route map（65k 455/70j 490/74h 518経路）・先例再解釈（70f bit-84→70g childは非STERILE・V4c WIN-WIN一致、75e bit-10→未sweep行）・bit-92第7削除canonのfold記録整合性・64c bits 111/119のout-of-sample予測的中
- path: research/experiments/n11-class2-lane-sterile-unclosability-20261116/verify_sterile_unclosability_20261116.py
  role: verifier
  note: stdlibのみ・Bareiss整数行列式・独立D4正準化/covers/合法性実装。V0候補リストbit-exact再現（7件+70g）・V1 canon陽性対照（ROOT_D4・bit-92 7削除canon・bit-6/bit-84/bit-10 covers）・V2出版route map 17子完全再現・V2s掃済6経路witness（REFUTED-REFUTED一致）・V3最近5 WIN roots非cover・V4先例整合+WIN-WIN一致（bit-84↔own bit 29）・V5完全近傍route枯渇（689/636/689近傍）・V6決定論。全合格・新プロセス2回実行バイト同一
- path: research/experiments/n11-class2-lane-sterile-unclosability-20261116/output/audit.json
  role: data
  note: 監査記録152,619 bytes・sha256 6221d1aef67ab93dfb412269927af67c5c859830a89083304f6139c923e03ab6。3行の完全route map（(child, bit, own_t, σ)全リスト）とverdict一致集計（REFUTED-REFUTED 6・WIN-WIN 1・矛盾0）を含む
- path: research/experiments/n11-class2-lane-sterile-unclosability-20261116/verify_theorem_application_bit109_20261116.py
  role: verifier
  note: 定理の初適用（69a bit 109 theorem-derived REFUTED-D10・並走commit e3c5117c）の第三者独立検証。stdlibのみ・D4正準形同一性（69a bit109≡65k bit75≡74h bit97）・cover両行所属・両自前行sweep完了記録とraw bit行（488,221/282,846 nodes・loss=false・capped=false・[13,17]・andclose true）・69a合法候補69件独立再列挙。全check PASS
- path: research/experiments/n11-class2-lane-sterile-unclosability-20261116/output/theorem-application-bit109-verification-20261116.json
  role: data
  note: 検証出力。2回実行でbyte-identical（md5 d72feaac795c9bc1bd72812f1a4b5683）。A1-A5全合格・failures空
- path: research/experiments/n11-class2-lane-sterile-unclosability-20261116/theorem_applicability_scan_20261116.py
  role: verifier
  note: 定理の正準形verdict転送機構を汎用化した適用可能性スキャン。s2-5960実験dirの全出版per-bit verdict（raw batch 1,064ファイル・sweep記録77・sweep監査29・claim 109）から8,964個の7石root verdict（REFUTED-D10 8,305・WIN7-D10 659・capped-unknown 0）をD4正準形で索引化し、全レーン候補rootへfixpoint転送・corpus全体の同位置verdict矛盾検出を行う。stdlibのみ・決定論的（2回実行byte-identical）
- path: research/experiments/n11-class2-lane-sterile-unclosability-20261116/output/theorem-applicability-scan-20261116.json
  role: data
  note: スキャン出力227,648 bytes・sha256 57a0584f0b81…。115個の新theorem-derived REFUTED-D10（69a bits 55/65/109・76c 15/76候補ほか）・同位置1,782組のcross-sweep一致（矛盾0）・STERILE行35行census・入力1,279ファイルのsha256 manifest込み。全8 check合格
scope: 'n11 S2{59,60}のdepth-10 WIN7-D10 receipt/cover体系（MS5 S6 manifestの6石行・D4正準化covers・foldのmarginal閉鎖）に限る。行RがSTERILE（Rの全合法候補root R+tの出版verdictがREFUTED-D10・capped 0）のとき、任意のWIN7-D10 receipt root X（安全な7石位置）についてX covers Rでないことを、位置レベル補題（X covers R ⟺ canon(X) ∈ {canon(R+t): t∈legal_candidates(R)}・D4等長変換が安全性を保存することによる）とゲーム規則のD4不変性から証明する。前提はengine depth-10 verdictの健全性とD4不変性のみで、当レーンの全出版verdictと同一のtrust境界（前提が破れれば2 sweep間のverdict矛盾として検出可能）。機械検証は完全route枯渇を3 STERILE行の全canonical一石置換近傍（689/636/689軌道・出版解析と一致）にわたって(σ, own bit) witness付きで確認し、cost≤70出版route map（17子24経路）と掃済6経路（60c bit119・62b bits21/109・64c bits111/119+65k bit119）を厳密な部分集合として含む。depth>10の証拠・ capped候補のある行・receipt機構以外の閉鎖手段・engine健全性そのものの証明は含まない。STERILE行のゲーム理論的値（LOSS/WIN）には一切言及しない'
evidence: '定理はreport.mdの補題（位置レベルの同値・Bareiss det4安全性とD4等長変換）とD4ゲーム木同型性による矛盾論法。機械検証は独立stdlib実装（候補列挙・D4正準化・covers・完全route列挙）で、V0-V5全合格・V6決定論（新プロセス2回バイト同一・audit sha256 6221d1ae…）。実証: (a) 出版route map 17子のcovers・候補数をbit-exact再現、(b) 掃済6 cross-cover経路が全てown candidateのREFUTED-D10へ写像（REFUTED-REFUTED一致6件）、(c) 最近5 WIN receipt roots（75e bits 6/10/11/37・60c bit 92）は3 STERILE行をcoverしない、(d) 先例70f bit-84のcover先70g childは自乗sweep8 WIN7-D10（非STERILE）でV4c WIN-WIN一致（canon(bit84 root)=canon(70g child+bit29)）、75e bit-10のcover先は未sweep行（いずれもerratum引用で、定理と無矛盾）、(e) 完全route map 455/490/518経路すべてのown candidate tが出版REFUTED-D10リストに含まれる、(f) 定理のout-of-sample予測（64c bits 111/119はREFUTED-D10）が並走sweep完了（64/64 REFUTED・v15+v16一致）で的中。verdict一致は計8件・矛盾0'
---

# STERILE行depth-10閉鎖不能性定理

## 命題・範囲

n11 S2{59,60}レーンのdepth-10 receipt体系（WIN7-D10 receiptがその7削除正準形でmanifest行を閉じる機構）について、
自乗sweepがSTERILE（全合法候補REFUTED-D10・0 capped）の6石行Rは、**どのWIN7-D10 receipt rootにもcoverされない**
ことを証明する。自出行・cross-coverを問わない。

## 補題と証明

- **補題（位置レベル・engine不使用）**: X covers R ⟺ canon(X) ∈ {canon(R+t) : t ∈ legal_candidates(R)}。
  X covers R ⟺ ∃s: canon(X−s)=canon(R) ⟺ ∃σ∈D4, t: X=σ(R+t)。receipt rootは安全で、D4等長変換は
  安全性（concyclic/collinear 4点組の不在）を保存するので、R+tは安全、tは合法候補。
- **定理**: WIN7-D10 receipt XがSTERILE行Rをcoverすれば、補題よりX=σ(R+t)（tは合法候補）。
  STERILE性よりverdict(R+t)=REFUTED-D10。規則のD4不変性よりゲーム木は同型でverdict(X)=REFUTED-D10、
  WIN7-D10 receiptと矛盾。∎
- **前提（trust境界）**: engine depth-10 verdictの健全性・D4不変性。当レーンの全出版verdictと同一前提であり、
  破れた場合は2 sweep間のverdict矛盾として即検出可能（定理は強い否定的予測として運用できる）。

## 実証と機械検証

- 3 STERILE行（65k/70j/74h・best coverable class-2 S5 `00000000000000801202000000200000`の3行/209）の
  canonical一石置換近傍は689/636/689軌道（出版neighbor analysisと一致）。
  完全route mapは自出行65/70/74＋cross 390/420/444経路で、**全経路**がown candidate bit t（出版REFUTED-D10）
  の(σ, t) witness付きで表示される（verifierが全件生成・検証）。
- 出版cost≤70 route map（17子・24経路）と掃済6経路（60c bit 119・62b bits 21/109・64c bits 111/119/119→65k）は
  完全mapの厳密な部分集合で、掃済経路のverdictはREFUTED-REFUTED一致（6件・矛盾0）。
- 最近5 WIN receipt roots（75e bits 6/10/11/37・60c bit 92）はいずれも3 STERILE行をcoverしない。
- 先例照合: 70j claim erratumがcross-cover先例として挙げた (a) 70f bit-84のcover先70g childは自乗sweep
  **8 WIN7-D10**（bits 9/20/29/34/62/70/76/119）の非STERILE行で、canon(70f bit-84 root)=canon(70g child+bit 29)
  の**WIN-WIN一致**が2独立sweep間で成立（D4 verdict転送の正の対照）、(b) 75e bit-10のcover先は2 parentの未sweep行。
  いずれもSTERILE行ではないため定理と無矛盾で、「STERILE行もcross-coverで閉鎖され得る」というerratumの
  訂正文言は過大だった（未sweep行・WIN有り行にのみ当てはまる）。
- out-of-sample予測の的中: 定理は並走64c sweep着地前にbits 111/119（70j・65kをcoverする唯一根）の
  REFUTED-D10を予測し、sweep完了（64/64 REFUTED・0 capped・v15+v16一致）で的中。

## 帰結

- best coverable class-2 S5（3行/209）は**depth-10 receipt体系では証明的に閉鎖不能**（coverable rankingから
  depth>10証拠待ちカテゴリへ移すべき）。隣接childのsweep価値自体は他parent需要・自身の閉鎖目的で残るが、
  STERILE行の閉鎖という目的には一切寄与しない。
- 今後どのsweepがSTERILE行をcoverするWIN7-D10を見つけても、それはverdict矛盾（engine不健全性の証拠）であり
  WIN/LOSS conflictとして直ちに調査対象になる。

## 限界

STERILEはLOSS証明ではない。本定理は閉鎖手段の不可能性のみを言い、行のゲーム理論的値には言及しない。
11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。

## 追記: 定理の初適用と第三者検証（2026-11-16）

並走の長期レーンが本定理をcost-69a候補bit 109へ適用し、sweep体系で初のtheorem-derived verdict（REFUTED-D10）を記録した（commit e3c5117c・class2-lane-cost69a-inflight-20261116.json）。bit 109のroot `00002000000000801222000000800000` はD4正準形 `00000000020008801202000000200000` において65k行のown bit 75・74h行のown bit 97と同一位置であり、両行の自前列sweep（65/65・74/74全件REFUTED-D10・0 WIN7-D10・0 capped）からD4判定不変性でverdictが移る。同時にcover補題の正方向により、このrootは65k・74h両STERILE行のcover集合に属し、bit 109でのWIN7-D10は両行を1 receiptで同時に閉鎖する唯一残存のcost≤70単一root機会だったが、定理により不可能と確定した（69aのengine候補は68個に減算され、batch 8がbit 109を実行する場合は一致検査として保持）。

この適用を第三者として独立検証した: `verify_theorem_application_bit109_20261116.py`（stdlibのみ・D4正準化・合法候補再列挙・cover集合・両sweep記録とraw bit行・69a候補69件の独立再列挙）全check PASS、出力JSONは2回実行でbyte-identical。これはK0863のout-of-sample予測（64c bits 111/119の的中に続き2件目の的中）であり、定理がsweep計算量を構造的に削減した初の記録である。STERILE行3行（65k/70j/74h）はopenのまま（STERILEはLOSS証明ではない）。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWN。

## 追記: 正準形verdict cache化とcorpus全体適用（2026-11-16）

定理の転送機構（canon一致ならばverdict一致）を、単一のbit 109適用からs2-5960レーンの全出版per-bit verdictへ汎用化した（`theorem_applicability_scan_20261116.py`）。raw batch 1,064ファイル・sweep記録・sweep監査・claim 109件から、**8,964個の7石root verdict**（REFUTED-D10 8,305・WIN7-D10 659・capped-unknown 0）をD4正準形で索引化し、全レーンの候補rootへfixpoint（2反復で収束）まで転送した:

- **115個の新theorem-derived REFUTED-D10**（engine未実行候補への転送）: 69a（in-flight）はbits 55/65/109が事前確定しengine候補は66個に減算。bit 55は64c（STERILE行）own bit 103との正準形同一（64cのcover候補でもあり定理の直接適用）、bit 65は2行のengine REFUTED根との二重由来の純粋verdict転送、bit 109は既述の65k/74h二重cover。76c（in-flight）は15/76候補が事前確定（例: bit 102 ≡ 77e bit 22・1,391,763 nodes投下済みの既出版REFUTED-D10行と同一位置）。
- **corpus全体の同位置verdict矛盾検出**: 独立sweep群の間で同じ正準形位置が1,782組存在し、**矛盾0**（engine vs engine・engine vs transferとも）。定理の「強い否定的予測」が破れた場合はこの検出が最初に赤になる。
- **STERILE行census**: 完全sweep済みかつ全候補REFUTED-D10・0 cappedの6石行は**35行**（65k/70j/74h/64cのほか62b・70d・73f・74f・class-4 S5 `00000000020000003800000080000000`の82b/84/87など）。
- 決定論的（2回実行byte-identical）・入力1,279ファイルのsha256 manifest込み・trust境界は既存sweepと同一（engine depth-10 verdict健全性+D4不変性）。

転送は個別7石rootのverdictのみを定め、行の閉鎖・receipt被覆・ゲーム理論的値には一切言及しない。STERILE行・open行の値はそのまま。11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
