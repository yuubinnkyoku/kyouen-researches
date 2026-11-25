# 2026-11-19 N11 cost-16 crosscheck: k=38対応拡張 — 287 checks版のbyte-identical再現を実証・k38拡張は28新規check込み315 checks all pass・二重実行+network mode byte-identical・record 11,359件の独立再分類とI-E恒等式（total/A/B）3系統厳密成立・rank-38 preread層11の機械再導出とk37主計算JSONとの3系統閉結合・k=14..k=38 disjoint pair統計全表を機械計算（付録）

k=37 crosscheck 287 checks版（script commit `cb5714d33ca8`・result `fe8abfadeb73`〔blob `858a4597…`〕・patch `c430f75e929d`・log `3cc3a8da7073`）と k=38本計算出版一式（単一オーナー出版: publication script `9d1b0a6a4c83` + patch `aa3f78a28840`・result JSON `78b6f1bd81`〔blob `c45ea8d0a11f009343c0736f6b98b5e4d06e8d4e`〕・record JSONL `b4ed53b2e1`〔blob `e8f9a8c9065bad3906a121f9bc816be6d299fb23`・11,359 records〕・log `cbade9c5ef`・第二実行合意記録 `ec62057f4f81`・rank-38 preread script `7d35406cf28e` / result `75fabfd01842`〔blob `3fa8297990d8e9880f386a0cfa075e3a95f226fd`・34 checks〕・preread独立bit-mask検証 `126614cc4819`/`f37ddd047ee7`/`e9a8a2330dbd`〔48-check audit〕・検証log `5e0ef79575ac`・k38レーン並走調整ノート `112a32470578`）を受けて、crosscheck scriptの k=38対応拡張（record層12段目 + preread層11 + closure 2件 + census拡張4）を main上の287 checks版からの機械変換で行った。**生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。標準11×11空盤はUNKNOWNのまま。**

## 前段: 287 checks版の復元と再現

1. **base取得**: main HEAD `2878e9e0`（高速レーンのz16 y1出版・並走の新規crosscheckなしをlist_commitsで確認）から、287 checks版script（144,524B・blob `3e1e9cbcd3c6b0e8f66dce9ab4ebebe2272da2e7`・sha256 `eda88d67…`・出版値と一致）と、PINS全件（k13..k38 result・k31pre..k38pre・aggregate `31bdefdb…`）+ JSONL_K26..K38 の計48ファイルをraw CDN取得し、**全pinned git blob sha1をこのレーンで独立照合（全一致・BAD 0件）**。k38 result `c45ea8d0`・JSONL `e8f9a8c9`・k38pre `3fa82979` を含む。
2. **base再現**: 改変前の287 checks版を `--local`（pinned入力sha1検証込み）で実行し、**287 checks / 0 failures・出版済みk37 crosscheck結果JSON（65,829B・blob `858a4597…`）とbyte-identical**（cmp一致・約17s）。変換前にbaseの健全性と出力決定性をまず確定した（輸送事故リスク管理の標準手順）。

## k=38拡張（287 checks → 315 checks all pass・28新規check）

機械変換は anchored-rep方式の変換script `patch_cc_k38.py`（blob `76d0f4d9…`・全19 repに単一出現count assertion・base sha256 `eda88d67…` 固定・不一致は即時abort・probe/stale-literal audit込み）で適用。主な変更: PINSにk38（`c45ea8d0…`）・k38pre（`3fa82979…`）追加、`JSONL_K38` 定数追加（blob `e8f9a8c9…`・**anchor4はk37 record層のdisjoint quads (4,13,25,36)/(4,16,25,36) に再錨付け** — 出版k38 JSONLのanchor4 recordから機械読み取りで確定）、値層の参照JSONをk38 resultに切替（K=38・kill系列k1..38）、quint census loop・prev-layer恒等式・sextet census loopへの38追加（docstring layer 11追加・fetch note更新）、record層loopへ (38, JSONL_K38, 2) 追加、preread層11（rank38 + rank-36/rank-37回帰block）新設、closure 2件のk38版追加、reportのschema/出力名/source_main_commit差し替え（`2878e9e02b33059ab0d192f893b9598587ec92cd`）。

1. **値層（k38参照・範囲拡張15件改名）**: grand-total恒等・単調性・marginal chain k2..k38（出版 `survival.marginal` の `k38_minus_k37` = 24,053,447,482,312,550・`m38` = 119,940,649,042,609,991 と照合）・A/B kill分割恒等・reproduce anchors（`reproduce_k1_37`）・cross-publication系列一致 k13..k38 が全てk38点まで通る。kill(38) = 2,719,931,616,763,264,020（91.6898%）・A_survive 6.7113%・B_survive 1.5989%（**過去最低更新・verdictとは無関係**）。marginal(38) = 24,053,447,482,312,550（m38比20.0545%）。
2. **構造層（+4 check）**: quint census C(38,5)=501,942 = 23,024 b_only / 478,918 zero / 0 disjoint の独立再導入（二重行hist {15:3,463, 16:687, 18:11,303, 19:7,571}・`quints_zero_synth_count` 63,177 = C(37,4) − 2,868）・prev-layer恒等（23,024 = 20,156 + 2,868・478,918 = 415,741 + 63,177・quint era継続）・sextet C(38,6)=2,760,681 all zero（I-E quint打ち切り・seventh order不要の機械保証をk38まで延長）・行29の初二重化（triple/quad層のみ・行7(rank-33)・行9(rank-34)・行8(rank-37)と同じ単一sharer二重行定型の4例目）の構造再導入込み。
3. **record層k=38（+11 check）**: k38 JSONL（blob `e8f9a8c9…`）の 11,359 records 全件を独立分類器で再分類: kind計数（pair 37 + triple 666 + quad 7,770 + quint 2,868 + anchor2 4 + anchor3 2 + anchor4 4 + cross 8 = 11,359）・anchor/cross全match・anchor4両lineage一致（(4,13,25,36)/(4,16,25,36) 再錨付け・union rows再導出込み）・新layer組合せ完全性（triple 666 = C(37,2)・quad 7,770 = C(37,3)）・新b_only quint集合一致（2,868）・quad record census一致（2,519/5,094/157）・**I-E marginal恒等式（total/A/B 3本）**: m38 − Σ新j2(126,500,505,218,444,094) + Σ新j3(32,607,007,742,615,406) − Σ新j4(2,013,833,852,645,949) + Σ新j5(20,129,768,177,196) = 24,053,447,482,312,550 = kill(38) − kill(37)（A型 19,076,687,088,172,916・B型 4,976,760,394,139,634）が record joints のみから厳密成立。**record JSONLから恒等式を取り直す第5系統検証のk38版**（単一オーナー出版entity + 第二実行合意記録 + k38 result finalize 52 checks + 本crosscheckで4系統目まで独立に一致）。
4. **preread層11（+11 check）**: rank-38 preread（blob `3fa82979…`・純Python正確整数・check_count 34・独立bit-mask第二系統検証 `e9a8a233`〔48 checks〕）を機械再導出: root (19,29)・行29 prior hits {[19]}（top-37内単一sharer = rank-20根 (18,29)・**行29の二重行化はtriple層8 record・quad層11 record・quint層0**・**4例目の単一sharer二重行定型で、root両行とも二重行化する史上初のrank**）・行19 hits [0,2,3,8,9,10,15,29,32,33,35,36]（12-sharer hub・rank-38自身の行19メンバーシップもsharerに加算）・membership/A/B = 119,940,649,042,609,991 / 91,876,760,891,572,775 / 28,063,888,151,037,216（A+B==M成立）・新層census 4種（pair 13 shared / 24 disjoint〔**shared数はシリーズ最多**〕・triple 420/113/133・quad 2,519/5,094/157・quint 2,868/63,177/0）・新層二重行hist 3種（triple 19:269 > 18:120・quad 19:1,339 > 18:870・quint 19:1,415 > 18:1,043 で**行19がtriple/quad/quint全層で行18を逆転する3世代連続**に到達）・b_only quint 4-subset profile {3/2/0: 2,868}・disjoint quad 157本全union=8・**累積1,677 = 機械再導出1,520（C(37,4)全走査）+ 157（ハードコード定数なし）**・full triples C(38,3)=8,436 {5,178/1,533/1,725}・full quints C(38,5)=501,942・sextet all zero・rank-36/rank-37両回帰block（`regression_block_ok` helper流用）・**3系統閉結合: preread内蔵rank-37回帰blockを出版済みk37 result JSON structureとfield-by-field直接照合**・k38 result JSON側 preread_match.* 5 check存在/PASS・rank38_root正確整数一致。
5. **closure 2件（k38版・+2 check）**: `k38preread_embedded_rank36_rank37_blocks_match_prior_prereads`（k38 preread内蔵回帰欄を先行preread出版〔rank36→k36pre・rank37→k37pre〕とschema正規化比較）・`k38json_preread_structure_matches_published_result`（rank-38 preread全構造欄をk38本計算出版JSONのstructure欄と直接照合）。k34..k37版8 closure checkはそのまま維持。

## 実行と検証

- 実行: `--local` mode（pinned入力全件・sha1照合）で **315 checks / 0 failures**・rc=0。**二回実行 byte-identical + network mode（jsdelivr/raw fetch）でも byte-identical**（三重回帰: local×2 = network）。result JSON 72,744B・blob `16cd6914ef5138bb827f2fa279674f22706a4dca`・sha256 `559ed8e6…`。実行時間: local 約20.6s/回・network 27.7s（sextet C(38,6)=276万件を含む独立再分類込み・純Python・1プロセス・CPU並列なし）。
- 拡張script: 162,303 bytes・blob `55d9e7c886a36bca1332887abe7da1ed2db82e89`・sha256 `c5546f28…`・`py_compile` PASS。変換patch（`patch_cc_k38.py`・11,359-record層への拡張を含む全19 anchored-repを同梱）も同時出版（crosscheck変換patch出版の4例目）。baseは清浄状態からの再適用でbyte再現済み。
- 計算量: quint ΣC(26..38,5) ≈ 3.03M・sextet ΣC(29..38,6) ≈ 13.82M・record層 11,359件・preread層11のrank-36/37回帰block機械再導入込み。
- 機械可読結果: [cost16-k38-crosscheck-20261119.json](../experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-k38-crosscheck-20261119.json)・schema `n11-cost16-k38-crosscheck-20261119-v1`・source_main_commit `2878e9e02b33059ab0d192f893b9598587ec92cd`。

## 付録: 新pair disjoint partner統計の全表（k=14..k=38・出版result JSONの `new_pair_joints` から機械計算）

各rankの新pair（rank-N rootとtop-(N-1)の各pair）のうち `shared_row=false`（disjoint partner）のjoint値統計。前回k37表（k=14..k=37）と本表のk=14..k=37行は全点機械一致（本レーンの独立再計算による相互検証・旧CSVは環境リセットで喪失したため全行を出版JSONから再生成した）。要点: (a) **平均jointはrankの構成（新rootの行がhub帯のどの位置か・fresh row・単一sharer hubの有無）に依存し定数帯ではない**、(b) **k38は5.2333e15でk37の5.2645e15から−0.6%**（min 4.9264e15・median 5.1472e15 も微減）で、旧帯5.28〜5.30e15には届かず「帯」仮説は引き続き棄却のまま分布で記録する運用を維持、(c) 時代平均は k14..18: 5.6659e15 → k19..25: 5.3583e15 → k26..38: 5.2729e15 に収束傾向、(d) **k38のshared 13本は全てjoint_A=0**（Σ 900,428,663,021,754 = marginal(38)比3.7434%）で**shared数はシリーズ最多**。

| k | pairs | shared | disjoint | min joint | median | max | mean | mean(e15) |
|---|---|---|---|---|---|---|---|---|
| 14 | 13 | 2 | 11 | 5,347,054,724,145,252 | 5,391,934,909,056,891 | 5,884,308,345,994,752 | 5,551,405,341,173,875 | 5.5514 |
| 15 | 14 | 3 | 11 | 5,386,207,957,208,478 | 5,615,581,361,559,726 | 5,859,279,647,997,483 | 5,650,692,838,069,557 | 5.6507 |
| 16 | 15 | 7 | 8 | 5,360,592,596,427,726 | 5,620,092,070,953,768 | 5,868,544,794,159,441 | 5,662,311,923,595,167 | 5.6623 |
| 17 | 16 | 5 | 11 | 5,564,706,794,487,768 | 5,620,836,359,106,003 | 6,069,249,969,873,702 | 5,722,129,624,866,517 | 5.7221 |
| 18 | 17 | 6 | 11 | 5,367,174,804,045,744 | 5,814,284,572,299,138 | 6,069,249,969,873,702 | 5,742,946,875,441,907 | 5.7429 |
| 19 | 18 | 7 | 11 | 5,139,738,498,369,648 | 5,391,024,078,824,310 | 5,638,937,949,371,472 | 5,403,927,831,674,773 | 5.4039 |
| 20 | 19 | 8 | 11 | 5,121,097,547,473,080 | 5,378,381,730,864,174 | 5,617,605,754,176,816 | 5,390,133,202,074,937 | 5.3901 |
| 21 | 20 | 9 | 11 | 5,138,768,568,140,046 | 5,394,240,765,702,534 | 5,620,799,612,638,860 | 5,413,170,826,062,727 | 5.4132 |
| 22 | 21 | 10 | 11 | 5,134,659,339,597,828 | 5,376,277,275,079,026 | 5,631,889,800,560,352 | 5,395,255,806,231,745 | 5.3953 |
| 23 | 22 | 5 | 17 | 4,944,097,643,675,484 | 5,371,379,380,000,506 | 5,644,886,245,836,516 | 5,274,723,208,086,718 | 5.2747 |
| 24 | 23 | 11 | 12 | 4,948,687,706,837,748 | 5,384,840,174,609,115 | 5,626,215,437,592,552 | 5,374,215,406,965,750 | 5.3742 |
| 25 | 24 | 12 | 12 | 4,939,809,653,860,653 | 5,343,079,473,636,492 | 5,388,596,351,672,925 | 5,256,582,731,584,931 | 5.2566 |
| 26 | 25 | 2 | 23 | 4,903,765,746,269,784 | 5,353,293,438,318,477 | 5,629,249,003,732,014 | 5,258,251,176,633,078 | 5.2583 |
| 27 | 26 | 13 | 13 | 4,937,052,096,763,182 | 5,367,752,471,659,116 | 5,612,847,628,081,542 | 5,345,036,264,256,389 | 5.3450 |
| 28 | 27 | 14 | 13 | 4,937,597,902,824,558 | 5,341,895,282,877,666 | 5,601,452,278,508,196 | 5,338,907,012,407,896 | 5.3389 |
| 29 | 28 | 4 | 24 | 4,900,908,038,491,569 | 5,160,940,200,617,043 | 5,643,273,501,996,042 | 5,274,230,823,256,752 | 5.2742 |
| 30 | 29 | 8 | 21 | 4,937,641,205,345,811 | 5,169,813,919,834,722 | 5,634,977,608,780,092 | 5,284,157,738,834,411 | 5.2842 |
| 31 | 30 | 15 | 15 | 4,928,665,644,035,646 | 5,333,009,948,523,438 | 5,592,057,922,741,860 | 5,317,312,138,795,487 | 5.3173 |
| 32 | 31 | 7 | 24 | 4,932,676,743,030,444 | 5,252,843,931,524,148 | 5,627,213,519,869,485 | 5,287,654,966,095,152 | 5.2877 |
| 33 | 32 | 9 | 23 | 4,931,370,896,961,645 | 5,158,785,651,596,994 | 5,627,525,779,051,341 | 5,282,128,458,074,969 | 5.2821 |
| 34 | 33 | 10 | 23 | 4,931,470,140,914,826 | 5,158,923,781,753,914 | 5,627,928,287,020,101 | 5,265,168,495,950,508 | 5.2652 |
| 35 | 34 | 16 | 18 | 4,742,105,445,803,346 | 5,313,173,646,508,824 | 5,585,272,601,523,870 | 5,268,626,691,322,206 | 5.2686 |
| 36 | 35 | 10 | 25 | 4,565,761,899,546,747 | 5,134,512,098,763,630 | 5,613,850,580,116,431 | 5,119,517,838,390,175 | 5.1195 |
| 37 | 36 | 12 | 24 | 4,926,721,102,810,461 | 5,152,444,978,763,760 | 5,632,447,468,101,189 | 5,264,516,800,450,758 | 5.2645 |
| 38 | 37 | 13 | 24 | 4,926,398,972,373,516 | 5,147,160,528,776,736 | 5,617,605,754,176,816 | 5,233,336,523,142,598 | 5.2333 |

（`new_pair_joints` は各rankのresult JSONのvalues欄にrank単位で記録されており、本表は出版JSONからのみ機械計算。k13以前はpair jointsのrank単位values欄がないため対象外。k38のshared 13本は全てjoint_A=0で総和900,428,663,021,754〔marginal(38)比3.7434%〕・disjoint 24本の総和は125,600,076,555,422,340。shared pairはjoint=0または「新rootの行との共有行」を持ち、本表のjoint統計からは除外。）

## 運用メモ

1. **着地検証手順の遵守**: 本出版もpush後にcommit SHAピンraw CDN再fetch・blob/sha256照合・`py_compile` を実施する（k34/k35/k37-preの輸送事故の教訓）。
2. anchor4の再錨付け先はk38 JSONLのanchor4 recordから機械読み取りで確定した（(4,13,25,36)/(4,16,25,36)。**前rank record層の実disjoint quadsから選ばれる運用は不変**・行19 hub帯のrank根の組成に由来）。
3. 値層のk38参照切替に伴い、チェック名の範囲部分（`marginal_chain_k14_k38` 等15件）は改名される。result JSONのcheck名集合はk37版の上位互換（範囲拡張を除き同一）。
4. k38 result JSONに `preread_match.*` 5 check・`rank38_root` の正確整数欄があることは本crosscheckの層11で機械保証された（finalize 52 checksの出版側内部検証に対する独立系統）。

## 次段（次回レーン候補）

- **k=39本計算**（rank-39 preread出版一式〔script `92305f5ad310`・result `848727f192e3`〔blob `6056bd83…`・35 checks〕・patch `ed9891962d13`・log `8c50c037e9f1`〕のload/assert chainに接続。**finalize I-Eはlevel-5 disjoint項（j5_A）とlevel-6 b_only項（j6_B）を含む6次構成〔level-6打ち切り〕に拡張必須**・sextet層は史上初の非ゼロb_only 5,852本でpm実計算が必要。**着手前に必ず最新mainでk39本計算script出版有無を確認〔毎時並走〕・単一オーナー出版規約を踏襲**）。
- k39本計算出版後の crosscheck k=39拡張は本拡張の層11パターンの流用に加え、**初のdisjoint quint層（508本・全union 10）と初のb_only sextet record層の機械再導出**が必要（record層のkind計数・新b_only quint集合比較オプションの拡張が本スクリプトの次の変換課題）。
- 11×11空盤・二石root・S2・class 1/2/4 は一切本crosscheckの対象外（下記参照）。

## 11×11 状態（interpretation guard）

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。本crosscheckの全checkはcover-plan組合せ数とその構造の検証であり、verdictを一切生成しない。kill(38) 91.69%・B_survive 1.60%台も「ban回避代替計画の組合せ論的飽和」の度量であって、探索進展や勝敗の尺度ではない。付録のdisjoint pair統計も同様に組合せ構造の記述である。
