# 2026-11-17 n11 class2-lane: fixB worker分割memo merge測定（cost73k・K0907修正エンジン×K0909構成）

## 概要

K0907で特定した証明書extractorの2欠陥（Uint32Array符号キーによる重複挿入＝bug A・死んだsentinel 255負境界＝bug B）を両方修正した測定専用エンジンfixBを、K0909の出版2-way worker分割merge構成（73/76境界・MS=1<<23・band内共有）で測定した。repo-verbatim extractorは出版決定性のためrepo上未修正のまま。測定のみで、新規WIN/LOSS verdict・証明書bytes変更・manifest行の開閉は一切ない。claimはdcfdcb25で先行取得済み（base 7153fe58）。並走セッションのverbatim 8-way測定（b8c76a4d/175048ff）・hybrid seed union測定（da276db1/e0c13af3）とは別軸で重複なし。

## エンジンと入力

- fixB = verbatim extractor blob `52bcaf50` + MS置換 + Int32Array memoキー比較（bug A修正） + sentinel-aware nowin/nolose更新（bug B修正） + 出版dump/seed export block。行レベル変更数はorchestratorが厳密アサート。
- 入力pin: worker driver `2a95d952`・legal `8e97082c`・manifest `0892aed0`。simはlight_sim_seed_73k.mjs（出版seed容量設計のものと同一）。
- アーム: (1) fixB band ms23単一プロセス22 bit・(2) 2-way workers（A: bits<=73 / B: bits>=76・freshプロセス・MS=1<<23・band内共有）・(3) dump重複キーcensus・(4) live bound distinct+merge・(5) merge seed MS=1<<24 seedrun 22 bit・(6) 未seed fixB band ms24・(7) 設計点 MS=1<<25 seedrun・(8) band表 vs merged表の集合比較。

## 測定結果

（測定JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/fixb-worker-split-memo-merge-73k-20261117.json`・全gate検証済み）

1. **fixB band ms23 単一プロセス（初のfixBバンド全体測定）**: 28,620,380 nodes・最終占有率 5,028,453・証明書22/22 byte同一。verbatim band ms23 121,186,659の0.2362・fixB fresh battery（K0907・28,290,025）の1.011。
2. **2-way workers**: A 11,662,998 + B 16,174,401 = **27,837,399 nodes**（fixB band23比0.9726・出版verbatim 2-way 119,962,147比**0.2321**・fixB fresh battery比0.9840）。workerAのper-bit nodes系列はfixB band23プレフィックスと完全一致（最終占有率3,159,518も一致）。証明書は11/11・11/11 byte同一。
3. **重複キーcensus**: 両worker・band23・両seedrun dump・band24 dumpのすべてでrecords == distinct（dup_keys=0・max_copies=1）。K0907 bug A機構（符号キー重複挿入）がバンド全体で消えていることを定量確認。live bound被覆率はnowin 11-12%・nolose 39-40%・win_and_lose=0・win_and_nowin_lt=0・all_unbound=0（band23: win 1,946,187・lose 501,195・nowin 597,074・nolose 1,983,997）。
4. **live bound merge**: shared 1,332,283・occupied_after **5,479,157**（出版verbatim 2-way merge 4,291,899の1.277倍）・内部衝突0・cross衝突0・merge決定的（seed md5 c5941251f3f123be50a785893911fdf9）。verbatimでは負境界が常に死哨255のためcross衝突が構造的に起こり得ず、K0909の衝突検出器はfault注入でしか実証されていなかった。fixBのmergeはliveなnowin/nolose境界を持つ表の自然mergeとしては初めてで、衝突検出器が初めて自然実動作し矛盾0だった。
5. **merge seed MS=1<<24 seedrun**: 7,947,885 nodes（未seed fixB band ms24 21,697,814の0.366）・seed失敗24,253件（0.443%）== sim予測と完全一致（own-cluster 2,068 + spill-over 22,185・max cluster 94・bases>=64は308・load 0.3251）。失敗率は出版seed容量設計のknee（S約4.1-4.2M keysで0.1% gate境界）の予測どおりで、MS=1<<24の0.1%事前gateは不成立（設計規則の検証例として記録）。record恒等式は閉包（present==inserted 5,454,904・missing==failed 24,253・値違反0）・証明書22/22 byte同一・seedrun dumpもrecords==distinct。
6. **設計点 MS=1<<25 seedrun**: **6,005,236 nodes**（未seed band24比0.2768・fixB fresh battery比0.2123・**出版verbatim最良構成8-way seedrun25 70,538,916比0.0852 = 11.7倍安い**）・seed失敗19件 == sim予測19（3.5e-6）・record恒等式閉包（present 5,479,138・missing==19・違反0）・証明書22/22 byte同一・最終占有率5,798,302（load 0.173）。design point gatesは全合格（design_point_ms25.gates_all_pass=true）。エンジンと構成を横断したこのバンドの測定済み最安band実行。
7. **merge非閉包（fixBでも存続）**: band表 vs merged表: shared 5,027,776・only_in_band 677・only_in_merged 451,381・共有キー値矛盾0（band_strictly_better_win_examples=0・merged_strictly_better_win_examples=0）。verbatimの262件非閉包と同様にfixBでもmerge表はband表のsupersetではなく、coordinatorはmerge表を近似として扱う必要がある。

## gates

- 全アームの証明書byte同一gate: True（band23/seedrun24/band24/seedrun25が22/22、workerA/Bが11/11）
- workerA per-bit == fixB band23プレフィックス・workerA bit0 == K0907 fixB battery anchor: True
- 重複キー0・内部衝突0・cross衝突0・merge決定的: True
- seed失敗 == sim予測（ms24・ms25両方）: True
- record恒等式（ms24・ms25両方）: 閉包・違反0
- band_vs_merged共有キー値矛盾0: True
- 不成立はMS=1<<24の事前gate「seed失敗率<0.1%」のみ（0.443%・出版knee設計の予測どおり。設計点ms25では全gate合格）

## 実験事実（環境と実装）

- 最初のpythonオーケストレータ実行は、bashが復帰する際のプロセスグループkillで死んだ。band23のnode子プロセスはstart_new_sessionで起動していたため生存し完走した。以後の長時間ジョブはsetsid nohupによる完全detachで起動し再発なし。
- 実装バグ2件を測定中に発見・修正した: (a) band23のdistinct表を途中工程で生成し忘れておりband_vs_merged比較が落ちた、(b) その比較処理の前提誤り。いずれも最終実行前に修正し、出版orchestratorは修正後の最終版。
- 全アーム合計のwall timeは約10分（band23 133s・workerA 62s・workerB 73s・seedrun24 101s・band24 125s・seedrun25 97s）。CPU並列は控えめで大規模中間dumpは測定後に削除した。

## 解釈ガード

測定のみ。新規WIN/LOSS verdict無し・manifest行は1行も閉じない・証明書bytes不変・repo-verbatim extractorはrepo上未修正のまま。fixBを本番extractorとして採用するかは別レーンの判断。WIN7-D10は個別7石rootのdepth-10内先手勝ちのみ・REFUTED-D10はLOSS証明ではない。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWN**。
