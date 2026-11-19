# 2026-11-19 N11 cost-16 crosscheck: k=37対応拡張 — 259 checks版のbyte-identical再現を実証・k37拡張は28新規check込み287 checks all pass・二重実行+network mode byte-identical・record 10,546件の独立再分類とI-E恒等式（total/A/B）3系統厳密成立・rank-37 preread層10の機械再導出とk36主計算JSONとの3系統閉結合・k=14..k=37 disjoint pair統計全表を機械計算（付録）

k=36 crosscheck 259 checks版（commit `f688d65727fd114f6dee58b925e7489ca716caf7`・script blob `4d3036ef…`）と k=37本計算出版一式（script+log+patch `8423c9716d08e19eee259bd43bdbf2f946a79e2f`〔script blob `f30cde0f…`・変換patch blob `5842f345…`〕・result JSON `a4a7ce31325b28a76165a7cdcafedbcb35d73a36`〔blob `03084d81674e829015561351be799c8a757e7c7e`〕・record JSONL `9ff089ce3e9caf36cefc1469f417bb8dcb73543e`〔blob `b5bf20215ef5578be1ebd605716473e21445296f`・10,546 records〕・rank-37 preread script `900f68c3`/result `983210038579c6bab350d6efb452d81c3d954a39`〔blob `b98ed685e772eacbd28dc3100e9813e81c27040a`・34 checks〕・preread独立bit-mask検証 `958057fb8b49d6429dc8a298d3d671b57e124f7`〔33 checks〕・base64 padding erratum `059db03e`）を受けて、crosscheck scriptの k=37対応拡張（record層11段目 + preread層10 + closure 2件 + census拡張4）を main上の259 checks版からの機械変換で行った。**生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。標準11×11空盤はUNKNOWNのまま。**

## 前段: 259 checks版の復元と再現

1. **base取得**: main HEAD `dfe8e6cc`（S5 cache merge regression対抗コミット・並走の新規crosscheckなしをlist_commitsで確認）から、259 checks版script（127,314B・blob `4d3036ef…`・出版値と一致）と、PINS全件（k13..k37 result・k31pre..k37pre・aggregate `31bdefdb…`）+ JSONL_K26..K37 の計45ファイルをraw CDN取得し、**全45 pinned git blob sha1をこのレーンで独立照合（全一致・BAD 0件）**。k37 result `03084d81`・JSONL `b5bf2021`・k37pre `b98ed685` を含む。
2. **base再現**: 改変前の259 checks版を `--local`（pinned入力sha1検証込み）で実行し、**259 checks / 0 failures・出版済みk36 crosscheck結果JSON（58,942B・sha256 `bbc059eb…`）とbyte-identical**（cmp一致・13.5s）。変換前にbaseの健全性と出力決定性をまず確定した（k34末尾切断・k35 trailing newline・k37 preread base64 paddingの輸送事故を含む輸送リスク管理の標準手順）。

## k=37拡張（259 checks → 287 checks all pass・28新規check）

機械変換は anchored-rep方式の変換script `patch_cc_k37.py`（blobは出版本文参照・全20 repに単一出現count assertion・base sha256 `4d3036ef…` 固定・不一致は即時abort・probe/stale-literal audit込み）で適用。主な変更: PINSにk37（`03084d81…`）・k37pre（`b98ed685…`）追加、`JSONL_K37` 定数追加（blob `b5bf2021…`・**anchor4はk36 record層のdisjoint quads (4,13,25,35)/(4,16,25,35) に再錨付け** — 出版k37 JSONLのanchor4 recordから機械読み取りで確定）、値層の参照JSONをk37 resultに切替（K=37・kill系列k1..37）、quint census loop・prev-layer恒等式・sextet census loopへの37追加（docstring layer 10追加・fetch note更新）、record層loopへ (37, JSONL_K37, 2) 追加、preread層10（rank37 + rank-35/rank-36回帰block）新設、closure 2件のk37版追加、reportのschema/出力名/source_main_commit差し替え（`dfe8e6cc877b132c52f766af790cf31735fba409`）。

1. **値層（k37参照・範囲拡張15件改名）**: grand-total恒等・単調性・marginal chain k2..k37（出版 `survival.marginal` の `k37_minus_k36` = 23,865,474,772,969,886・`m37` = 119,973,409,932,394,637 と照合）・A/B kill分割恒等・reproduce anchors（`reproduce_k1_36`）・cross-publication系列一致 k13..k37 が全てk37点まで通る。kill(37) = 2,695,878,169,280,951,470（90.8789%）・A_survive 7.3544%・B_survive 1.7667%（**過去最低更新・verdictとは無関係**）。
2. **構造層（+4 check）**: quint census C(37,5)=435,897 = 20,156 b_only / 415,741 zero / 0 disjoint の独立再導入（二重行hist {15:3124, 16:616, 18:10260, 19:6156}・`quints_zero_synth_count` 56,183 = C(36,4) − 2,722）・prev-layer恒等（20,156 = 17,434 + 2,722・quint era継続）・sextet C(37,6)=2,324,784 all zero（I-E quint打ち切り・seventh order不要の機械保証をk37まで延長）・行8の初二重化（triple/quad層のみ・行7(rank-33)・行9(rank-34)と同じ単一sharer二重行定型の3例目）の構造再導入込み。
3. **record層k=37（+11 check）**: k37 JSONL（blob `b5bf2021…`）の 10,546 records 全件を独立分類器で再分類: kind計数（pair 36 + triple 630 + quad 7,140 + quint 2,722 + anchor2 4 + anchor3 2 + anchor4 4 + cross 8 = 10,546）・anchor/cross全match・anchor4両lineage一致（(4,13,25,35)/(4,16,25,35) 再錨付け・union rows再導出込み）・新layer組合せ完全性（triple 630 = C(36,2)・quad 7,140 = C(36,3)）・新b_only quint集合一致（2,722）・quad record census一致（2,394/4,589/157）・**I-E marginal恒等式（total/A/B 3本）**: m37 − Σ新j2(127,178,575,523,319,924) + Σ新j3(33,135,080,298,103,617) − Σ新j4(2,084,446,736,890,569) + Σ新j5B(20,006,802,682,125) = 23,865,474,772,969,886 = kill(37) − kill(36)（A型 18,933,557,461,780,451・B型 4,931,917,311,189,435）が record joints のみから厳密成立。**record JSONLから恒等式を取り直す第5系統検証のk37版**。
4. **preread層10（+11 check）**: rank-37 preread（blob `b98ed685…`・純Python正確整数・check_count 34・独立bit-mask第二系統検証 `958057fb`〔33 checks・erratum `059db03e`〕）を機械再導出: root (8,19)・行8 prior hits {[23]}（top-36内単一sharer = rank-24根 (8,18)・**行8の二重行化はtriple層8 record・quad層11 record・quint層0で初めて発生**・行7/rank-33・行9/rank-34と同じ単一sharer二重行定型の3例目）・行19 hits [0,2,3,8,9,10,15,29,32,33,35]（11-sharer hub・rank-36根に加えrank-37自身の行19メンバーシップもsharer・行21/22のfresh row seriesに続く「zero prior sharer」なし）・membership/A/B = 119,973,409,932,394,637 / 91,996,175,553,485,330 / 27,977,234,378,909,307（A+B==M成立）・新層census 4種（pair 12 shared / 24 disjoint・triple 397/100/133・quad 2,394/4,589/157・quint 2,722/56,183/0）・新層二重行hist 3種（triple 19:246 > 18:120・quad 19:1214 > 18:870・quint 19:1269 > 18:1043 で**行19がtriple/quad/quint全層で行18を逆転**〔quint逆転はrank-36の僅差 18:1200 vs 19:1195 から初めて〕）・b_only quint 4-subset profile {3/2/0: 2,722}・disjoint quad 157本全union=8・**累積1,520 = 機械再導出1,363（C(36,4)全走査）+ 157（ハードコード定数なし）**・full triples C(37,3)=7,770 {4,758/1,420/1,592}・full quints C(37,5)=435,897・sextet all zero・rank-35/rank-36両回帰block（`regression_block_ok` helper流用）・**3系統閉結合: preread内蔵rank-36回帰blockを出版済みk36 result JSON structureとfield-by-field直接照合**・k37 result JSON側 preread_match.* 5 check存在/PASS・rank37_root正確整数一致。
5. **closure 2件（k37版・+2 check）**: `k37preread_embedded_rank35_rank36_blocks_match_prior_prereads`（k37 preread内蔵回帰欄を先行preread出版〔rank35→k35pre・rank36→k36pre〕とschema正規化比較）・`k37json_preread_structure_matches_published_result`（rank-37 preread全構造欄をk37本計算出版JSONのstructure欄と直接照合）。k34/k35/k36版6 closure checkはそのまま維持。

## 実行と検証

- 実行: `--local` mode（pinned入力全件・sha1照合）で **287 checks / 0 failures**・rc=0。**二回実行 byte-identical + network mode（jsdelivr/raw fetch）でも byte-identical**（三重回帰: local×2 = network）。result JSON 65,829B・blob `858a4597ece4c6af9a43b829d7a78442d98a567a`・sha256 `04c4e0968956f24570fe6bafb93e55f379c626650fe4a6ba84d182e8a505fd52`。実行時間: local 約16.4s/回・network 24.2s（sextet C(37,6)=232万件を含む独立再分類込み・純Python・1プロセス・CPU並列なし）。
- 拡張script: 144,524 bytes・blob `3e1e9cbcd3c6b0e8f66dce9ab4ebebe2272da2e7`・sha256 `eda88d670ac3947e52de873f905619385940990a5ef2436f66b3cece16c1048f`・`py_compile` PASS。変換patch（`patch_cc_k37.py`・10,546-record層への拡張を含む全20 anchored-repを同梱）も同時出版（crosscheck変換patch出版の3例目）。
- 計算量: quint ΣC(26..37,5) ≈ 2.53M・sextet ΣC(29..37,6) ≈ 11.06M・record層 10,546件・preread層10のrank-35/36回帰block機関再導入込み。
- 機械可読結果: [cost16-k37-crosscheck-20261119.json](../experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-k37-crosscheck-20261119.json)・schema `n11-cost16-k37-crosscheck-20261119-v1`・source_main_commit `dfe8e6cc877b132c52f766af790cf31735fba409`。

## 付録: 新pair disjoint partner統計の全表（k=14..k=37・出版result JSONの `new_pair_joints` から機械計算）

各rankの新pair（rank-N rootとtop-(N-1)の各pair）のうち `shared_row=false`（disjoint partner）のjoint値統計。前回k36表（k=14..k=36）と本表のk=14..k=36行は全点機械一致（本レーンの独立再計算による相互検証）。要点: (a) **平均jointはrankの構成（新rootの行がhub帯のどの位置か・fresh row・単一sharer hubの有無）に依存し定数帯ではない**、(b) **k36が5.1195e15でシリーズ最低、k37は5.2645e15へ+2.8%回復**（min 4.5658e15→4.9267e15・median 5.1345e15→5.1524e15も回復）が、旧帯5.28〜5.30e15には届かず「帯」仮説は引き続き棄却のまま分布で記録する運用を維持、(c) 時代平均は k14..18: 5.6659e15 → k19..25: 5.3583e15 → k26..37: 5.2755e15 に収束傾向。

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

（`new_pair_joints` は各rankのresult JSONのvalues欄にrank単位で記録されており、本表は出版JSONからのみ機械計算。k13以前はpair jointsのrank単位values欄がないため対象外。k37のshared 12本は全てjoint_A=0で総和830,172,312,501,741〔marginal比3.478%〕・disjoint 24本の総和は126,348,403,210,818,183。shared pairはjoint=0または「新rootの行との共有行」を持ち、本表のjoint統計からは除外。）

## 運用メモ

1. **着地検証手順の遵守**: 本出版もpush後にcommit SHAピンraw CDN再fetch・blob/sha256照合・`py_compile` を実施する（k34/k35/k37-preの輸送事故の教訓）。
2. anchor4の再錨付け先はk37 JSONLのanchor4 recordから機械読み取りで確定した（(4,13,25,35)/(4,16,25,35)。**前rank record層の実disjoint quadsから選ばれる運用は不変**・行19 hub帯のrank根の組成に由来）。
3. 値層のk37参照切替に伴い、チェック名の範囲部分（`k16_k37_reproduce_anchors_all_pass` 等15件）は改名される。result JSONのcheck名集合はk36版の上位互換（範囲拡張を除き同一）。
4. k37 result JSONに `preread_match.*` 5 check・`rank37_root` の正確整数欄があることは本crosscheckの層10で機械保証された（finalize 52 checksの出版側内部検証に対する独立系統）。

## 次段（次回レーン候補）

- **rank-38 preread**（k37 preread script〔37,612B・blob `d0155d4f…`・commit `900f68c3`〕からの機械変換。**着手前に必ず最新mainでk38 preread出版有無を確認〔毎時並走〕**。変換時は `check_count==34` assertを新しいcountに更新する必要がある。rank-38前期事実はpinned aggregate（top50 blob `31bdefdb…`）から機械算出してから変換repに載せる）。
- k38本計算はk38 preread出版後に着手（k37 script〔blob `f30cde0f…`〕からの機械変換。PINS向けにk37 result `03084d81` / k37 preread `b98ed685` / k36→k37回帰層は本拡張の層10パターンで流用可能）。
- 11×11空盤・二石root・S2・class 1/2/4 は一切本crosscheckの対象外（下記参照）。

## 11×11 状態（interpretation guard）

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。本crosscheckの全checkはcover-plan組合せ数とその構造の検証であり、verdictを一切生成しない。kill(37) 90.88%・B_survive 1.77%台も「ban回避代替計画の組合せ論的飽和」の度量であって、探索進展や勝敗の尺度ではない。付録のdisjoint pair統計も同様に組合せ構造の記述である。
