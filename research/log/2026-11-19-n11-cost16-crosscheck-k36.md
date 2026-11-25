# 2026-11-19 N11 cost-16 crosscheck: k=36対応拡張 — 231 checks版のbyte-identical再現を belong手順で実証・k36拡張は28新規check込み259 checks all pass・二重実行byte-identical・record 10,028件の独立再分類とI-E恒等式（total/A/B）3系統厳密成立・rank-36 preread層9の機械再導出とk35主計算JSONとの3系統閉結合・k=14..k=36 disjoint pair統計全表を機械計算（付録）

k=35 crosscheck 231 checks版（commit `a956245bfdca40a41b3145d291eedbd202d1259e`・script blob `a2df5648038ea9b3cecfce6d52ca5f1f9f01e764`）と k=36本計算出版一式（script+log+patch `48dc73e6`・輸送erratum `21bf2cd2`〔正確blob復元 script `d1e93a9f`・patch `00867996`〕・result JSON `6fcea02c`〔blob `b7a78e79bdc82c8097222ef2fd057e6b1a4b9350`〕・record JSONL `0e96cde4`〔blob `7ba84693d302d2bc76851163fd3eb6a6fa7b0caa`・10,028 records〕・rank-36 preread `67985e92c9`〔blob `760aa396361cc7d2ea8bc371f4dd673d962f07fe`〕・Proxmox再現log `fc46f01e`）を受けて、crosscheck scriptの k=36対応拡張（record層10段目 + preread層9 + closure 2件）を main上の231 checks版からの機械変換で行った。**生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。標準11×11空盤はUNKNOWNのまま。**

## 前段: 231 checks版の復元と再現

1. **base取得**: main HEAD `b1484ddd`（K1010帳簿コミット・並走の新規出版なしをlist_commitsで確認）から、231 checks版script（109,615B・blob `a2df5648…`・出版値と一致）と、PINS全件（k13..k36 result・k31pre..k36pre・aggregate `31bdefdb…`）+ JSONL_K26..K36 の計42ファイルをraw CDN取得し、**全39 pinned blob sha1をこのレーンで独立照合（全一致・BAD 0件）**。k36 result `b7a78e79`・JSONL `7ba84693`・k36pre `760aa396` を含む。
2. **base再現**: 改変前の231 checks版を `--local`（pinned入力sha1検証込み）で実行し、**231 checks / 0 failures・出版済みk35 crosscheck結果JSON（45,185B・sha256 `f4de97df…`）とbyte-identical**（cmp一致）。前回の輸送破損事故（k34版末尾切断・k35版trailing newline）の教訓どおり、変換前にbaseの健全性と出力決定性をまず確定した。

## k=36拡張（231 checks → 259 checks all pass・28新規check）

機械変換は anchored-rep方式の変換script `patch_cc_k36.py`（28,540B・blob `a09e3831…`・全repに単一出現count assertion・不一致は即時abort・residual audit込み）で適用。主な変更: PINSにk36（`b7a78e79…`）・k36pre（`760aa396…`）追加、`JSONL_K36` 定数追加（blob `7ba84693…`・**anchor4はk35 record層のdisjoint quads (2,14,28,34)/(2,16,28,34) に再錨付け** — 出版k36 JSONLのanchor4 recordから機械読み取りで確定）、値層の参照JSONをk36 resultに切替（K=36・kill系列k1..36）、quint census loop・prev-layer恒等式・sextet census loopへの36追加、record層loopへ (36, JSONL_K36, 2) 追加、preread層9（rank36 + rank-34/rank-35回帰block）新設、closure 2件のk36版追加、reportのschema/出力名/source_main_commit差し替え（`b1484dddb9e410c23f024d6759305b13b98afe1a`）。

1. **値層（k36参照・範囲拡張15件改名）**: grand-total恒等・単調性・marginal chain k2..k36（出版 `survival.marginal` の `k36_minus_k35` = 22,931,496,078,632,577・`m36` = 120,046,727,515,486,665 と照合）・A/B kill分割恒等・reproduce anchors（`reproduce_k1_35`）・cross-publication系列一致 k13..k36 が全てk36点まで通る。kill(36) = 2,672,012,694,507,981,584（90.0744%）・A_survive 7.9926%・B_survive 1.9329%（過去最低・初の2%割れ・verdictとは無関係）。
2. **構造層（+4 check）**: quint census C(36,5)=376,992 = 17,434 b_only / 359,558 zero / 0 disjoint の独立再導入（二重行hist {15:2785, 16:545, 18:9217, 19:4887}・`quints_zero_synth_count` 49,525 = C(35,4) − 2,835）・prev-layer恒等（17,434 = 14,599 + 2,835）・sextet C(36,6)=1,947,792 all zero（I-E quint打ち切り**13世代連続**の機械保証・行22の初被覆〔fresh row〕はいかなる層でも二重行化しない構造事実の再導入込み）。
3. **record層k=36（+11 check）**: k36 JSONL（blob `7ba84693…`）の 10,028 records 全件を独立分類器で再分類: kind計数（pair 35 + triple 595 + quad 6,545 + quint 2,835 + anchor2 4 + anchor3 2 + anchor4 4 + cross 8 = 10,028）・anchor/cross全match・anchor4両lineage一致（(2,14,28,34)/(2,16,28,34) 再錨付け・union rows再導出込み）・新layer組合せ完全性（triple 595 = C(35,2)・quad 6,545 = C(35,3)）・新b_only quint集合一致（2,835）・quad record census一致（2,458/3,919/168）・**I-E marginal恒等式（total/A/B 3本）**: m36 − Σ新j2 + Σ新j3 − Σ新j4 + Σ新j5B = 22,931,496,078,632,577 = kill(36) − kill(35)（A型 18,174,993,772,658,979・B型 4,756,502,305,973,598）が record joints のみから厳密成立。**第5の独立系統としてrecord JSONLから恒等式を取り直した検証のk36版**。
4. **preread層9（+11 check）**: rank-36 preread（blob `760aa396…`・純Python正確整数・Proxmox再現 `fc46f01e`）を機械再導入: root (19,22)・行19 prior hits {[0,2,3,8,9,10,15,29,32,33]}（10 sharer hub・**rank-36 root自身が行19のsharer**）・行22 hits {[]}（zero prior sharers・初被覆・行21・行22のfresh row seriesはrank-36で中断）・membership/A/B = 120,046,727,515,486,665 / 92,003,630,985,566,871 / 28,043,096,529,919,794（A+B==M成立・Node丸めerratum不発生を純Python側から逆保証）・新層census 4種（pair 10 shared / 25 disjoint〔過去最大のdisjoint share〕・triple 391/63/141・quad 2,458/3,919/168・quint 2,835/49,525/0）・新層二重行hist 3種（triple 19:232 > 18:136・quad 19:1150 > 18:992 で**行19がtriple/quad両層で初めて行18を逆転**・quintは18:1200 vs 19:1195の僅差で行18維持）・b_only quint 4-subset profile {3/2/0: 2,835}・disjoint quad 168本全union=8・**累積1,363 = 機械再導出1,195（C(35,4)全走査）+ 168（ハードコード定数なし）**・full triples C(36,3)=7,140・full quints C(36,5)=376,992・sextet all zero・rank-34/rank-35両回帰block（`regression_block_ok` helper流用）・**3系統閉結合: preread内蔵rank-35回帰blockを出版済みk35 result JSON structureとfield-by-field直接照合**・k36 result JSON側 preread_match.* 5 check存在/PASS・rank36_root正確整数一致。
5. **closure 2件（k36版・+2 check）**: `k36preread_embedded_rank34_rank35_blocks_match_prior_prereads`（k36 preread内蔵回帰欄を先行preread出版〔rank34→k34pre・rank35→k35pre〕とschema正規化比較）・`k36json_preread_structure_matches_published_result`（rank-36 preread全構造欄をk36本計算出版JSONのstructure欄と直接照合）。k34/k35版4 closure checkはそのまま維持。

## 実行と検証

- 実行: `--local` mode（pinned入力全件・sha1照合）で **259 checks / 0 failures**・rc=0。**二回実行 byte-identical**（result JSON 58,942B・blob `a96d7a1ad434c49070cf72676d059756d312d56b`・sha256 `bbc059ebcd959027b16c3efb72cce63b2867a35850782a9b29cc7d54f4c5e353`）。約13.5s/回（sextet C(36,6)=1.95M件の独立再分類込み・純Python・1プロセス・CPU並列なし）。
- 拡張script: 127,314 bytes・blob `7dc47183e267c388817b333691c10e7755297ab6`・sha256 `4d3036eff58ef30c9be9739e2e8a3e18cabbed5c14235e69b2c6900d7d4c6734`・`py_compile` PASS。変換patch（`patch_cc_k36.py`）も同時出版（k36本計算の `patch_k36.py` に続く変換patch出版の2例目）。
- 計算量: quint ΣC(26..36,5) ≈ 2.10M・sextet ΣC(29..36,6) ≈ 7.67M・record層 10,028件・preread層9のrank-34/35回帰block機関再導入込み。
- 機械可読結果: [cost16-k36-crosscheck-20261119.json](../experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-k36-crosscheck-20261119.json)・schema `n11-cost16-k36-crosscheck-20261119-v1`・source_main_commit `b1484dddb9e410c23f024d6759305b13b98afe1a`。

## 付録: 新pair disjoint partner統計の全表（k=14..k=36・出版result JSONの `new_pair_joints` から機械計算）

各rankの新pair（rank-N rootとtop-(N-1)の各pair）のうち `shared_row=false`（disjoint partner）のjoint値统计。サイエンスとしての要点: (a) **平均jointはrankの構成（新rootの行がhub帯のどの位置か・fresh row・単一sharerHubの有無）に依存し定数帯ではない**（k35 logの観察のk36版確定・下表でk36がシリーズ最低）、(b) k36のmin 4.5658e15は全シリーズ最小、(c) 時代平均は k14..18: 5.6659e15 → k19..25: 5.3583e15 → k26..36: 5.2765e15（26..35のみなら5.2868e15）に収束傾向。

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

（`new_pair_joints` は j35以降のresult JSONのvalues欄にrank単位で記録されており、本表は出版JSONからのみ機械計算。k13以前はpair jointsのrank単位values欄がないため対象外。shared pairはjoint=0または非ゼロだが「新rootの行との共有行」を持ち、本表のjoint統計からは除外。）

## 運用メモ

1. **着地検証手順の遵守**: 本出版もpush後にcommit SHAピンraw CDN再fetch・blob/sha256照合・`py_compile` を実施する（k34/k35の輸送事故3件の教訓）。
2. anchor4の再錨付け先はk36 JSONLのanchor4 recordから機械読み取りで確定した（(2,14,28,34)/(2,16,28,34)。k35 logの予告「(4,13,25,34)/(4,16,25,34)」系のパターン外・**前rank record層の実disjoint quadsから選ばれる運用は不変**）。
3. 値層のk36参照切替に伴い、チェック名の範囲部分（`k16_k36_reproduce_anchors_all_pass` 等15件）は改名される。result JSONのcheck名集合はk35版の上位互換（範囲拡張を除き同一）。

## 次段（次回レーン候補）

- **rank-37 preread**（k36 preread script〔blob `cc25c4f3…`〕からの機械変換。着手前に必ず最新mainでk37 preread出版有無を確認〔毎時並走〕。pinned aggregate由来のrank-37前期事実: root〔top50 index 36〕hex `00000000080000003800000108001000`・rows (8,19)・m37 = 119,973,409,932,394,637（A 91,996,175,553,485,330 / B 27,977,234,378,909,307・A+B==M確認済み）・fresh rowなし（行8はtop-36内単一sharer〔index 23〕・行19は11-sharer hub〔0,2,3,8,9,10,15,29,32,33,35〕でrank-36自身もsharer）・新pair census 12 shared / 24 disjoint予想）。
- k37本計算はk37 preread出版後に着手。着手前の出版有無確認を忘れないこと。
- PINSにk35 result `80a22ac7` / k36 result `b7a78e79` を使うrank-36/37回帰層は本拡張の層9パターンで直接流用可能。

## 11×11 状態（interpretation guard）

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。本crosscheckの全checkはcover-plan組合せ数とその構造の検証であり、verdictを一切生成しない。kill(36) 90.07%・B_survive 1.93%台も「ban回避代替計画の組合せ論的飽和」の度量であって、探索進展や勝敗の尺度ではない。付録のdisjoint pair統計も同様に組合せ構造の記述である。
