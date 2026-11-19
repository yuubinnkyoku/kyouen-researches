# 2026-11-19 N11 cost-16: k=39第二実行 — record corpus 29,219件を独立に全再計算しlean検証35 checks all pass・marginal I-E level-6打ち切り構成の実測値を確定 — 標準11×11空盤はUNKNOWNのまま

k=39本計算script出版一式（script `84bda7514e`〔blob `ce52edc9…`・k38 anchored-rep patch `8bf8484c`〔blob `d532e09d…`〕経由〕）と、rank-39 preread（blob `6056bd83…`）を受けて、本短期レーンは k=38まではowner単一出版物であったrecord corpus（pair/triple/quad/quint/sextet + anchor/cross）を**独立第二実行で全再計算した**。本実行時点でownerの k=39 result JSON・record JSONL・logはいずれも未着地（main HEAD `26fc92d1`・K1031）であり、本記録はそれらの重複出版ではなく第二実行の実測値・corpus識別子・環境事実の出版である。**生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。標準11×11空盤はUNKNOWNのまま。二石root・S2・class1/2/4も全て未知。**

## 実行構成とcorpus識別子

- 入力は全てcommit-SHA-pinned raw CDN取得＋git blob sha1照合（aggregate `31bdefdb…`・k14..k38 result・k37/k38/k39 preread・k38 JSON `c45ea8d0…`）。candidate-root表のみローカル再生（blob `89b24065…`）。
- pair 38本は公式scriptのpairs/triples/quads budget mode（rc=0）、anchor 10本は公式anchor mode（rc=0）、triple 703 / quad 8,436 / quint 14,166 / sextet 5,852本は公式per-record計算pathをlane driverが再実行（prescanが b_only/disjoint の工作itemを抽出し、zero-class subsetは I-E に寄与しない事から計算対象外。resume可能なshard分割）。
- **canonical corpus**: 29,219 records・5,516,755 bytes・git blob sha1 `ec323a3132773d372b7de5adbb2be02566cd7ae6`・md5 `b8fc1e21…`。**as-run corpus**: 29,233行・5,519,169 bytes・blob `742aed95…`・md5 `25209c87…`（公式anchor/pairs-budget両modeを続けて走らせた結果、cross 14種が各modeで1回ずつappendされ28行になった。両コピーは値完全一致〔field mismatch 0・elapsed-time欄を除く〕。canonicalはfirst-occurrence順のdedup。cross行はI-E項に寄与せず、両corpusとも同一35 checks・同一値でPASS）。

## 検証（35 checks / 0 failures）

record census（pair 38 = 4 shared/34 disjoint〔sharedは行5・24の4 prior sharer idx {2,4,14,25} でpreread構造予測と一致、全て joint_A=0〕・triple 703 = 319 b_only/42 zero/342 disjoint・quad 8,436 = 4,398/3,029/1,009・quint 14,166 = 13,658 b_only/508 disjoint・sextet 5,852 = b_only only・anchor 10・cross 14・全recordが C(38,0..5) の rank-39 包含subsetで過不足なし）、preread一致（新quint/sextet census・sextet二重行hist {15:682, 18:3147, 19:2023}・rank-39 membership 119,883,868,794,265,826）、quint新b_only二重行hist {18:6562, 19:4267, 15:1561, 5:763, 24:179, …} のpreread一致、quint disjoint 508本の全 |union|=10・全 joint_A>0、b_only/disjoint quint・b_only sextetのsubset構造（種類列が層構造どおり）、I-E恒等式・bounds・単調性維持（kill・A_survive・B_survive全て k38→k39 非減少）を検証し**全PASS**。

## 実測値（marginal I-E 6次構成・独立第二実行値）

| level | S総和 | A項 | B項 |
|---|---|---|---|
| 2 (pair) | 177,719,762,480,252,278 | 134,048,048,821,617,775 | 43,671,713,658,634,503 |
| 3 (triple) | 81,323,301,076,158,782 | 59,828,162,703,113,978 | 21,495,138,373,044,804 |
| 4 (quad) | 11,792,614,387,000,557 | 8,178,733,671,816,696 | 3,613,880,715,183,861 |
| 5 (quint) | 371,572,113,381,822 | 195,547,521,346,740 | 176,024,592,035,082 |
| 6 (sextet) | 2,239,577,445,579 | **0** | 2,239,577,445,579 |

- marginal(39) = m39 − S2 + S3 − S4 + S5 − S6 = **12,064,125,539,108,016**（m39 = 119,883,868,794,265,826。m39比 10.063177%・k38の20.0545%からの急低下はrank-39がfresh行を持たず両root行が同時に初二重化する構造の帰結）。A型 9,621,593,393,447,259（79.75%）/ B型 2,442,532,145,660,757（20.25%）。
- kill(39) = kill(38) 2,719,931,616,763,264,020（pinned k38 result blobから再現）+ marginal = **2,731,995,742,302,372,036**（全cover 2,966,450,341,680,481,356 比 92.096460%）。A_survive 189,465,234,042,187,464（6.386934%）・B_survive 44,989,365,335,921,856（**1.516606%・過去最低更新**）。
- **史上初の level-5 disjoint quint 項**（S5_A = 195,547,521,346,740・508本全 |union|=10）と**史上初の level-6 項**（S6 = 2,239,577,445,579・全b_only・j6_A = 0）が非零で、kill系列はprereadが機械保証した6次打ち取り構成そのままに実測確定した。

## 環境と事故の記録

1. 第一実行はcorpus完成後に provider 503 による環境完全リセット（09:29Z）でcorpusを喪失。第二実行で全再計算し、pair (37,38) record（A=3,864,883,981,998,822・B=1,256,159,032,032,453）が両buildで完全一致、決定性を確認した上で全値を第二実行から出版した。
2. 公式finalize modeは本環境の3.2GB capを超えOOM kill（rc=137・C(39,6)規模のsextet census辞書構築中）。よって本レーンはlean検証（record合算＋恒等式）までとし、result JSON/records/finalizeの出版はowner環境に残る。
3. lane harnessの検証器bugを2点、出版前に修正した: (a) 公式pathのb_only quad recordにjoint_B欄が無い件をliteral B=0と誤読していたのを、finalize意味論（B側full計上）へ修正、(b) 二重行検出をunion単passからrows multiset再計算へ修正（union列は二重行を1回しか載せない）。いずれも修正後に全恒等式が成立。

## 付録: k=39新pair disjoint統計（第二実行corpusから機械計算・owner出版後に対照予定）

k=14..k=38表（k38 crosscheck log付録）の形式で k39行を本レーンcorpusから機械計算した（ownerのresult JSON `new_pair_joints` は未出版のため、公式pairs budget modeが生産したpair 38本が源）。

| k | pairs | shared | disjoint | min joint | median | max | mean | mean(e15) |
|---|---|---|---|---|---|---|---|---|
| 39 | 38 | 4 | 34 | 4,904,287,325,721,534 | 5,133,642,115,816,323 | 5,623,964,665,978,698 | 5,218,430,925,039,604 | 5.2184 |

k38比: mean −0.285%（5.2333e15 → 5.2184e15）。shared 4本は全て joint_A=0、総和 293,111,028,905,730（marginal(39)比2.4296%）。disjoint 34本の総和は 177,426,651,451,346,548（S2総和 177,719,762,480,252,278）。

## 引き継ぎ

ownerの k=39 result/record/log出版を検知した次回実行は、canonical corpus（blob `ec323a31…`）とのrecord-by-record比較と S2..S6・marginal・kill値比較を行い、一致すれば第二実行合意記録を、不一致なら即時の食い違い報告を作成する（k38 `ec62057f` 前例）。k39 crosscheck拡張・k39 preread独立検証（未出版）はその後。本記録は組み合わせ計数のみを扱い、いかなるverdict主張も含まない。

## 機械可読結果

[cost16-k39-second-execution-lean-verification-20261119.json](../experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-k39-second-execution-lean-verification-20261119.json)・schema `n11-cost16-k39-second-execution-lean-verification-20261119-v1`・source_main_commit `26fc92d1e9c73a2306fc36a139c054fba50f00db`。
