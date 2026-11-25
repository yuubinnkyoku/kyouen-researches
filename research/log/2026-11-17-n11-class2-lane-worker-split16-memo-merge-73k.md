# 2026-11-17 n11 class2-lane: 16-way worker分割 memo merge測定（cost73k・K0909 resume item・worker数の限界測定）

## 経緯

K0909のresume item「16-way拡張（損失0.0073%のままunionがさらに増えるか・worker数の限界測定）」を実施した。
計算前にclaim JSON（`class2-lane-worker-split16-merge-73k-claim-20261117.json`）をcommit `c3d9c918`で先行取得した
（batches_run 0・base_head `fb9aeb7d`。並走のfixB 8-way claim `7dca832c`・cost78c掃引claim・census v11とは非重複）。
入力は全てpin付きblobで再構築し検証した: extractor `52bcaf50`（repo-verbatim・K0907の2欠陥を含むまま）・
driver `2a95d952`・legal `8e97082c`・manifest `0892aed0`・worker_memo_merge `fe2c5411`・証明書41 part files（19 split×2+3 whole）。

## 設計

- 分割: 出版band ms23 per-bitノード数に対する連続DP min-max 16分割（min-max群重量 11,857,737 = bit95単独）。
  V1=[0]・V2=[7,11]・V3=[15]・V4=[35,39]・V5=[41,44]・V6=[58,62]・V7=[73]・V8=[76]・V9=[87]・V10=[89]・
  V11=[94]・V12=[95]・V13=[97,98]・V14=[103]・V15=[105,112]・V16=[117]。
  10個の単独bit worker＋6個の2-bit worker（22 bitの完全順序分割・gate確認）。
- 各workerはfresh process・MS=1<<23・band内共有（per-bit clearRows・per-bit snapshotで出版証明書とbyte比較）→KYOENWM1全slot dump。
- offline merge: per-worker外部sort+stream dedup（内部衝突計数）→16-way heapq merge-join（incidence histogram・cross衝突・
  sorted KYOENWM2 seed16）→軽量simulator（`light_sim_seed_73k.mjs`・出版seed容量設計で二重anchor検証済み）でMS=1<<24/25/26掃引。
- seedrun: MS=1<<25設計点（fsync強化dump・cap 200・drop_caches・不要worker dump削除）でseed16から全22 bit band実行。

## 結果（測定JSON `worker-split16-memo-merge-73k-20261117.json`・15/15 gate合格）

1. **worker合計 108,802,603 nodes**（band ms23 121,186,659の0.8978・出版2-way 119,962,147の0.9070・
   nb4 112,741,501の0.9651・境界4-way 111,953,183の0.9719・**8-way 110,639,931の0.9834〔−1.7%〕**）。
   2→4→8→16の単調改善は継続するが、**fresh ms23電池108,499,241の1.0028倍（+0.28%）に到達**し、
   分割によるworker計算の削減はfresh床にほぼ収束した。証明書22/22 byte同一（10×1＋6×2）。
2. **V1 band23プレフィックス一致**（bit0 4,303,203 nodes・最終占有率710,449==BAND23_OCC[0]）。
   他15 workerの先頭bit（7,15,35,41,58,73,76,87,89,94,95,97,103,105,117）は全て出版fresh per-bit anchorと完全一致（gate）。
   先頭bit fresh/carried比は13/15が1未満（0.7474–0.9937）・bit95はちょうど1.0（memo-state-invariant）で、唯一の逆行はbit41の+5.6%
   （8-wayの逆行bit39〔+3.6%〕と併せ、fresh anchorがband-carriedを上回るbitは39/41に局在し、逆行ペナルティはN非依存のbit特有現象と特定）。
3. **2-bit workerの第2bitはfresh値の±1.3%内**（bit11 +0.37%・bit39 +1.01%・bit44 +0.16%・bit98 −0.47%・bit112 +1.31%。
   例外はbit62の+12.8%〔worker内carry 1,998,613 vs fresh 1,771,346〕だがband-carried 2,241,220比では−10.8%）。
   2-bit worker内のcross-bit memo再利用はほぼ効かず、N-way分割の利得の本体は「高負荷単一テーブルの後半bit汚染回避」である
   （band-carriedがfreshより高コストなbitでworker内carryが両者の中間に落ちる観察と整合）。
4. **16-way heapq merge**: distinct合計8,375,088（records 20,072,127・dup_keys 1,346,833はverbatim符号キー重複のまま）・
   **occupied_after 5,404,082**（出版2-way seed比+25.9%・nb4比+8.4%・8-way比+3.1%でunion増大は逓減継続:
   2→4 +16.2%・4→8 +5.2%・8→16 +3.1%）・shared 2,137,777・
   incidence {1:3,266,305, 2:1,493,134, 3:486,611, 4:130,721, 5:24,296, 6:2,794, 7:214, **8:7**, 9..16:0}
   （incidence 8のキーが初出現・全16 worker同時memo化キーは存在せず）・内部衝突0・cross衝突0・merge決定的
   （2回実行でbyte同一）・seed16 md5 `9a29784dae371569a6a012ba68ab4886`。
5. **sim MS掃引（seed16・5,404,082 keys）**: 1<<24→70,175失敗（1.2986%・load 0.3179・own-cluster 17,872+spill-over 52,303・
   最大cluster 161 keys・8-way seed系knee曲線〔4.29M→1,448・4.99M→16,137・5.24M→39,409〕に16-way seedの第4点5.40M→70,175を追加し超線形性を確認）・
   1<<25→2,285（0.0423%・load 0.1610・own 714+spill 1,571・8-way 383の約6倍・<0.1% gateは2.4倍余裕で合格）・
   **1<<26→8失敗（8-way seedは1<<26で0だったため、seedサイズがkneeを超えると1<<26でもclean容量を失うことを初実測）**
   （1<<26の失敗はspill-overのみ・bases>=64は0）。
6. **MS=1<<25 seedrun**: seeded 5,404,082 / inserted 5,401,797 / **failed 2,285 == sim予測2,285**・証明書22/22 byte同一・
   record恒等式閉包（present 5,401,797・missing==2,285・値違反0）・**68,006,820 nodes**
   （8-way seedrun25 70,538,916の0.9641〔−3.6%〕・並走hybrid 72,761,010の0.9347・nb4 seedrun25 72,745,351の0.9349）・
   最終占有率14,004,499（load 0.4174）・bit95は11,857,737 nodesで6度目の完全不変確認。
   **大きいunion seedほどband実行が安いという濃度とコストの関係はN=16でも成立し、このバンドのverbatim軸での
   測定済み最安band構成を更新した**。
7. **worker数の限界（本測定のまとめ）**: N=16で(a) worker計算コストはfresh床+0.28%に収束し分割の計算利得はほぼ枯渇、
   (b) unionの増大は+3.1%に逓減しband実行の削減も−3.6%に逓減、(c) 一方でseed挿入失敗率はMS=1<<25設計点で
   超線形に増加し（28→383→2,285）1<<26のclean容量は既に喪失（8失敗）。よってこのバンド（22 bit・union ~5.4M keys）では
   **N=16がMS=1<<25設計点で実用的な最終段階**に近く、それを超える細分割（N=22完全fresh化等）は
   seed容量設計の再設計（MS=1<<26での播種は本実行環境では不可〔typed arrays 1.34GB〕のためseed truncationか
   0.1% gateの再設定）を要する。coordinatorのworker数選択はseed負荷とkneeの距離で評価すべきという
   出版設計規則の適用範囲がN=16まで拡張された。

## gates（15/15合格）

split_exact_partition / workerV1_per_bit_equals_band23_prefix / workerV1_total / workerV1_final_occupied /
first_bit_fresh_anchors（15/15）/ bit95_memo_state_invariant / internal_conflicts_zero（16 workers）/
cross_conflicts_zero / merge_deterministic / worker_byte_identical（10×1+6×2=22）/ seedrun_byte_identical（22/22）/
seedrun_seed_failed_equals_sim25 / seed_failure_rate_below_0.1pct / record_identity_no_violations /
record_identity_missing_equals_seed_failed。

## 実行・実装の事実

- 事前smoke test: bit39単独worker（fresh 2,037,105 nodes・証明書byte同一・占有率412,510）で全経路
  （variant生成・driver・plan構築・legal・証明書byte比較）を確認してから本番起動。
- 本番は全工程detached（setsid+nohup）で実行し約16分で完走（worker段階・sort/distinct/merge/sim・seedrun25+record恒等式）。
  全stepはworkdirのstate.jsonからresume可能。
- **実装バグ1件（出版前に修正済み）**: 8-way版orchestratorからの機械変換で測定JSONのmerge section keyが
  `merge8`のまま残っていた（gate・値には無影響・schema文字列は正しくsplit16）。keyを`merge16`へ修正して
  resumable再実行し、run1とrun2でmerge sectionの値を含む全数値が完全一致したことを確認した上でrun2を出版した。
- 環境負荷: workerは逐次実行（MS=1<<23・cap 350・各~30s）・seedrun25はcap 200＋fsync強化dump＋drop_caches
  （出版8-way測定と同一処方）でOOM無し。中間ファイルはseedrun前に削除。

## 解釈ガード

測定のみ。新規WIN/LOSS verdict無し・manifest行は1行も閉じない・証明書bytes不変・repo-verbatim extractorはrepo上未修正
（出版決定性チェーン）。WIN7-D10は個別7石rootのdepth-10内先手勝ちのみを証明し、REFUTED-D10はLOSS証明ではない。
11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はいずれもUNKNOWNのまま。

## レジューム

- (i) fixB 8-way worker分割は並走claim `7dca832c`中のため着手禁止（出版後の交差比較が次候補）。
- (ii) cost78c掃引は並走claim中・census/coordinatorループは並走管理のため着手禁止。
- (iii) 本測定でN-way系列（2/4/8/16）のverbatim軸は一段落。次候補はcoordinator候補選択に基づく証明書積み上げ設計の測定、
  またはseed16を用いた後続バンド（73l等）へのseed適用可能性の設計測定。
- (iv) 11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はいずれもUNKNOWN。
