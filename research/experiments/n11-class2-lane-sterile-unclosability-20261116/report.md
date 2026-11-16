# STERILE行depth-10閉鎖不能性定理（n11 class-2 lane・2026-11-16）

対象: 11×11標準盤・S2 {59,60}の二石root証明優先レーン（MS5 S6 manifest・S7 edge cost・WIN7-D10 receipt/cover体系）。
開始時のcanonical head: 1410/174/6438/509109/4711/373023。本実験は解析・検証のみで、sweep・fold・claimは含まない（head不変）。

## 定理

**STERILE行depth-10閉鎖不能性**。6石のmanifest行Rの自乗sweepがSTERILE（全合法候補root R+tがREFUTED-D10・capped 0）なら、
どのWIN7-D10 receipt root XもRをcoverしない。自出行・cross-cover（他childのsweepによるmarginal閉鎖）を問わない。

## 証明

**補題（位置レベル・engine不使用）**。
X covers R ⟺ canon(X) ∈ {canon(R+t) : t ∈ legal_candidates(R)}。
証明: X covers R ⟺ あるs∈Xでcanon(X−s)=canon(R) ⟺ あるσ∈D4・cell tでX=σ(R+t)。
receipt root Xは安全（concyclic-free・sweepは安全なchildの合法候補bitで走る）で、D4等長変換は安全性を保存する。
ゆえにR+tは安全、すなわちtはRの合法候補である。∎

**定理本体**。WIN7-D10 receipt root XがSTERILE行Rをcoverすると仮定する。補題よりX=σ(R+t)（tはRの合法候補）。
STERILE性より自乗sweepの出版verdictはverdict(R+t)=REFUTED-D10。11×11盤の規則はD4等長変換で不変なので、
Xとσ⁻¹(X)=R+tのゲーム木は同型で、depth-10 verdictは一致する: verdict(X)=REFUTED-D10。
これはXがWIN7-D10 receipt rootであることと矛盾する。∎

**前提（trust境界）**: engineのdepth-10 verdictの健全性とD4不変性。これは当レーンの全出版verdict
（REFUTED-D10・WIN7-D10・STERILE記録のすべて）と同一のtrust境界であり、本定理はこの前提の下でのみ成り立つ。
前提が破れた場合（あるWIN7-D10 receipt rootが実際にはcover可能な位置である等）は2つのsweep間のverdict矛盾として
即座に検出可能であり、その意味で定理は「STERILE行をcoverするWIN7-D10 receiptは決して現れない」という
強い否定的予測として運用できる（下記out-of-sample予測の的中を参照）。

## 機械検証（verify_sterile_unclosability_20261116.py・stdlibのみ・Bareiss整数行列式・独立実装）

全チェック合格（V0–V5・V6決定論）。監査記録 `output/audit.json`（152,619 bytes・sha256 6221d1ae…・新プロセス2回実行バイト同一）。

- **V0 候補リスト再現**: 3 STERILE行（65k/70j/74h）と掃済child（75e/60c/62b/64c）の合法候補リストを
  独立Bareiss実装でbit-exact再現（65/70/74/75/60/62/64個）。70g child（cost-70g・11-15 fold対象）の候補数70も再現。
  埋め込み全位置の安全性（concyclic-free）を検証。
- **V1 canon/covers陽性対照**: bit-92 rootのD4正準形が出版ROOT_D4と一致。bit-92の7削除正準形が
  出版marginal 6件＋第7削除（del stone 5 → `00000000000000801212200000000000`）に一致。
  75e bit-6が75e childを、70f bit-84が70g childを、75e bit-10が出版marginal行をcoverすることを再現。
- **V2 出版route map完全再現**: 並走laneのneighbor analysis（commit d5d3d532）のcost≤70未sweep17子について、
  候補数とcovers（3 STERILE行へのbit）を独立実装で完全一致再現（24経路）。
- **V2s 掃済経路witness**: 60c bit 119→70j、62b bits 21/109→70j、64c bits 111/119→70j、64c bit 119→65kの
  6経路すべてに(σ, 自出行bit t)のwitnessを提示。tは全て-cover側行の合法候補かつREFUTED-D10、
  掃済側bitの出版verdictもREFUTED-D10（REFUTED-REFUTED一致6件・矛盾0）。
- **V3 最近のWIN roots非cover**: 75e bits 6/10/11/37と60c bit 92の5 receipt rootはいずれも
  3 STERILE行をcoverしない（定理の直接的な実例）。
- **V4 先例整合（erratum訂正の訂正）**: 70j claimのerratum（schema v3）は「STERILE行もcross-coverで閉鎖され得る」と
  訂正したが、その引用先例はいずれもSTERILE行ではない。
  - 70f bit-84のcross-coverが閉じた「cost-70g child」（`00000000000100809002000000000800`）の自乗sweepは
    **8 WIN7-D10**（bits 9/20/29/34/62/70/76/119）で非STERILE。
    さらに**V4c WIN-WIN一致**: canon(70f bit-84 root) == canon(70g child + bit 29)が厳密に成立し、
    2つの独立sweep（70f掃のbit-84と70g自乗掃のbit 29）が同一位置WIN7-D10で一致する。
    これは定理のD4 verdict転送前提の正の対照である（REFUTED-REFUTED 6件とあわせverdict一致8件・矛盾0）。
  - 75e bit-10のmarginalが閉じた行（`00000000000000801202000000000201`）は2 parentの未sweep行であった
    （閉鎖時点でSTERILEではない）。どちらの先例行も3 STERILE行とD4不同値。
  よって「STERILE行もcross-coverで閉鎖され得る」は過大訂正であり、正しくは
  **「未sweep行・WIN有り行はcross-coverで閉鎖され得るが、STERILE行は（自出行もcross-coverも）depth-10 receiptでは閉鎖されない」**。
- **V5 完全route枯渇**: 各STERILE行のcanonical一石置換近傍（65k 689・70j 636・74h 689軌道・出版解析と一致）に対し、
  **全近傍・全合法候補にわたる完全route map**を直接列挙で生成:
  65k 455経路（自出行65・cross 390・390子）、70j 490（70・420・389子）、74h 518（74・444・444子）。
  全経路が自出行候補bit tへ(σ, t) witness付きで写像され、tの出版verdictはREFUTED-D10。
  すなわち**どの子をどの順でsweepしても、STERILE行をcoverするWIN7-D10 receiptは原理的に発生しない**
  （cost≤70出版mapと掃済6経路はこの完全mapの厳密な部分集合）。

## 副産物の観察

- **bit-92 receiptの第7削除canon**: 60c foldのbit-92記録はmarginal 6件（manifest 3＋非manifest 3）を掲載するが、
  7削除の正準形は7個すべて相異なる。foldの意味論（marg = covers − s_1407・記録はcovers=7/marginal=6を出版）から、
  第7canon `00000000000000801212200000000000`（del stone 5・stones [45,49,52,57,60,71]）はhead 1407時点で
  既にcover済みだったことが出版記録のみから強制される（直近16 receiptではcoverされないため、より早期のreceiptによる）。
  head 1410の簿記は影響を受けない（記録整合性の観察として監査に保存。chain再実行による独立再導出は本実験の範囲外）。
- **out-of-sample予測の的中**: 本定理は並走laneの64c sweep（IN FLIGHT・claim d5d3d532）の着地前に
  「cover候補bits 111/119はREFUTED-D10になるはず」と予測した。sweep完了（commit 909b7690・64/64 REFUTED・0 capped・
  v15+v16がbits 111/119を含むアンカーで一致）により予測は的中した。

## 戦略的帰結（coordinatorへの反映事項）

1. **best coverable class-2 S5 `00000000000000801202000000200000`（3行/209）はdepth-10 receipt体系では閉鎖不能**。
   3行（65k/70j/74h）全てSTERILEなので、どの隣接childのsweepも（たとえWIN7-D10を産んでも）このS5の行を閉じない。
   このS5は「証明的にD10閉鎖不能」カテゴリへ分類し、coverable rankingから除外してdepth>10証拠待ちとすべき。
   （なお隣接child自体のsweep価値は消えない: 隣接子は他parentの行でもあり、自乗receiptによる
   他parent側の閉鎖・自身の閉鎖には従来どおり寄与する。STERILE行の閉鎖という目的に限り無駄になる。）
2. STERILE行の閉鎖に向けて残る道はdepth>10証拠のみ（例: REFUTED-D10の行に対するWIN7-D11+探索、
   またはdepth>10の全候補反証 — 探索爆発に注意）。
3. 今後のneighbor sweepでSTERILE行をcoverするbitがWIN7-D10として現れた場合は、定理より2 sweep間の
   verdict矛盾（engine不健全性の証拠）として直ちに調査対象になる（WIN/LOSS conflict検出の特殊形）。

## 限界・UNKNOWN明記

- 本定理はdepth-10 WIN7-receipt体系内の不可能性であり、STERILE行のゲーム理論的値には何も言わない。
  REFUTED-D10はLOSS証明ではなく、STERILEもLOSS証明ではない。
- **11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1・class 2・class 4はすべてUNKNOWNのまま。**
- solved 1410はmanifest被覆の簿記であり、勝敗確定とは無関係。

## 再現

```sh
python3 verify_sterile_unclosability_20261116.py   # stdlibのみ・約6秒・全チェック合格
```

ソース（すべてyuubinnkyoku/kyouen-researches main出版済み・監査JSONのSOURCESにcommit/pin付きで記録）:
neighbor analysis d5d3d532、64c sweep完了 909b7690、60c fold 05cc8bdb、
70j claim v3（erratum含む）、75e/70f/70g(11-15) fold records、各sweep audit。
