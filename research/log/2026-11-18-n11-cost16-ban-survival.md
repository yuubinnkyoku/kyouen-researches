# 2026-11-18 N11 31行cost-16 parent ban生存曲線 k=4/k=8 厳密再計算（per-d slice resume設計）

## 成果

31行cost-16 parent `00000000000000003800000008001000` について、membership上位k本のpair rootをbanしたときの最小cover総数を厳密再計算し、**生存曲線のk=4点・k=8点を新規に確定**した（前回出版のtop-10 jointで確定済みだったk=1/k=2点と合わせて5点 series化）。top-8は全てpair root・全425 pair typeがmultiplicity 1のため、banはそのままpair type削除に対応する。

- script: `cost16_ban_survival_20261118.py`（point / assemble の2 mode・per-d slice resume-safe JSONL）
- output: `output/cost16-ban-survival-20261118.json`（5,925 bytes・timing欄なし・二重実行byte-identical・sha256 `21d332637e79661c…`）・`output/cost16-ban-survival-20261118.jsonl`（66 slice record + summary・計算log）

## 生存曲線（全最小cover 2,966,450,341,680,481,356 に対する厳密値）

| k | 生存最小cover総数 | kill | kill share | A成分 | B成分 | 由来 |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 2,966,450,341,680,481,356 | 0 | 0% | 2,305,787,291,293,934,388 | 660,663,050,386,546,968 | 出版A16+B16 |
| 1 | 2,830,067,742,535,007,691 | 136,382,599,145,473,665 | 4.5975% | - | - | total−m1（厳密） |
| 2 | 2,704,376,702,109,131,038 | 262,073,639,571,350,318 | 8.8346% | - | - | 包含排除（出版joint12） |
| 4 | **2,453,842,390,618,094,434** | 512,607,951,062,386,922 | **17.2802%** | 1,912,189,176,067,079,977 | 541,653,214,551,014,457 | **本次再計算** |
| 8 | **2,001,925,712,552,127,087** | 964,524,629,128,354,269 | **32.5144%** | 1,564,239,038,548,375,836 | 437,686,674,003,751,251 | **本次再計算** |

ban対象（k=8まで）: (15,19) / (16,18) / (5,19) / (0,19) / (18,24) / (1,18) / (18,30) / (4,18)（出版aggregateのmembership降順）。

## 構造的観察

1. **killの非加法性の定量**: exact kill / naive membership和は k=1: 1.0000 → k=2: 0.9789 → k=4: 0.9676 → k=8: 0.9169 と単調減少。k=8で上位8本のmembership総和1,051,902,765,110,629,572（全coverの35.46%）に対し、実際のkillは964,524,629,128,354,269（32.51%）で、**overlapが8.3%分を二重計上**。根あたりの限界killは root1: 4.60% → roots2-4: 約4.22%/本 → roots5-8: 約3.81%/本 と緩やかに逓減。
2. **A/B成分の非対称な生存**: A型cover（15 pair + 1 singleton）の全coverに占める割合は baseline 77.71% → k=4: 77.93% → k=8: 78.13% と単調増加。上位membership根のbanはpair密度の高いB型coverを相対的に強く刈る。全banがpair rootであることと整合（singleton rootはbanされておらずA型の経路が残る）。
3. **対称性によるslice一致**: k=4・k=8とも d=2 と d=3 の B_d が完全一致（k=4: 19,508,265,303,094,853・k=8: 15,998,135,690,856,567・memo状態数も一致）。parent内部の行2/3の対称性と整合する独立兆候。

## 方法・検証

- 公式（出版odd-r framework・r=31, k=16）: A_k = Σ_s w1[s]·pm'(V∖{s})、B_k = Σ_d Σ_{a<b∈N'(d)} w'(d,a)w'(d,b)·pm'(V∖{d,a,b})。全最小coverはA型（15 disjoint pair + 1 singleton）かB型（16 pair・二重被覆行ちょうど1つ）のいずれかなので A_k+B_k がban回避最小coverの厳密数。pm'はban済みedge_wに対するPmLazy（出版moduleからimport・実装はphase A/B/groups runnerと同一lineage）。
- **per-d slice resume設計**: A phase 1回（共用memo・31 singleton錨・3.52M状態・約36秒）+ B slice 31本（各slice独立fresh memo・約3.52M状態・約35秒・2 slice/invocation・予算75秒）。pm値はmemo履歴非依存（出版groups runで実証済み）のため、slice独立memoの和は共用memo runと同一の厳密整数を与える。1 k点あたり約19分。
- **assemble 7 checks全PASS**: k=0 split（出版A16+B16）・k=1/k=2の生存値が出版top-10 joint出力のk1_killed/k2_killedと厳密一致・slice完備性（31/31 + A）・単調非増加・union bound（total_k ≥ total0 − Σ上位k membership）。k=0..8の5点は全て厳密減少。
- **決定論性の追加実測（環境リセットをまたいで）**: 計算中に実行環境がリセットされワークスペースが消失したが、出版pin群から入力を再取得・候補JSONLを同梱scriptで再生成（6,337行・parent構造は31行/2,333候補/1,908 root/425 pair type mult 1として再検証）して計算を最初からやり直したところ、**消失前のA₄・B_d0と再計算値が完全一致**（A₄=1,912,189,176,067,079,977・B_d0=15,677,424,859,815,108）。assemble出力は二重実行でbyte-identical。以降の運用として、各invocation後にknowledge scratchへJSONLをsnapshotし損失ゼロで継続した。
- 入力pin: cover表 `4e4a911d…`・phase-B groups aggregate `31bdefdb…`・top-10 joint出力 `df52b55a…`（sha256 `b84e5c3c…`）をbyte-exact検証。
- **並走laneのdirect-mode B_d表（commit `08a0d111`出版）の着地検証も本セッションで実施**: 出版JSONL 31 recordのΣ contrib == B16 == 660,663,050,386,546,968 が厳密一致、かつ全31行のper-d contribが出版phase-total出力の b_slices と完全一致（2計算mode間の独立交叉検証）。

## 並走k=1..10曲線との交叉検証（2独立手法の完全一致）

出版直後のmain確認で、並走laneが包含排除の構造的崩壊（top-10全rootがハブ行18/19を含む → disjoint triple不在・全210 4-subset構造的不能 → kill(k)=Σm−Σj2+Σj3で完結）による生存曲線k=1..10厳密決定（commit `a59881a2`・出力 `cost16-survival-k10-20261118.json`・独立MyPm counter）を07:00に出版済み、さらにsingleton行ban拡張（`c98cb51d`）を07:04に出版済みであることが判明した。**本計算（ban下での全再計算・per-d slice・PmLazy）と並走（包含排除・joint再結合・MyPm）は手法として完全に独立しており、kill(4) = 512,607,951,062,386,922 と kill(8) = 964,524,629,128,354,269 が両者で厳密一致**した。これは並走のI-E打ち切り機構（quad以上の項が構造的にゼロという主張を含む）が、2点で独立な全再計算により確認されたことを意味する。逆に並走曲線は本logのk=4/k=8点を包含しており、31行cost-16 parentの生存曲線k=0..10は2独立手法で確定済みとなった。

## 解釈上の注意

生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもWIN/REFUTED verdictでもない。membership上位banで残ったcover計画の存在は、それらの根の証明上の役割には何も含意しない。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。
