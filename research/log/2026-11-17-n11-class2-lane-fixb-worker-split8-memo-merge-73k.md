# 2026-11-17 n11 class2-lane: fixB 8-way worker分割memo merge測定（cost73k・K0907修正エンジン×K0909 8-way構成）

## 概要

fixB worker分割merge測定（追記5・d3060c8e/2ead47be）を、出版verbatim 8-way構成（b8c76a4d/175048ff）と同じ8-worker構成に拡張した。22 band bitをfixB band ms23 per-bitノード数のDP min-max（min-max値4,168,242）で連続8分割し、V1=fixB band23プレフィックスアンカー、他7 workerはfreshプロセス・MS=1<<23・band内共有で測定。repo-verbatim extractorはrepo上未修正のまま。測定のみで、新規WIN/LOSS verdict・証明書bytes変更・manifest行の開閉は一切ない。claimは7dca832cで先行取得済み（base 2ead47be）。並走セッションのverbatim 16-way claim（74b96a55）・cost78c claim（fb9aeb7d）とは別軸で重複なし。

## エンジンと入力

- fixB = verbatim extractor blob `52bcaf50` + MS置換 + Int32Array memoキー比較（bug A修正） + sentinel-aware nowin/nolose更新（bug B修正） + 出版dump/seed export block。行レベル変更数は2-way出版orchestrator（`measure_worker_split_fixb_memo_merge_73k_20261117.py`）のアサートをそのまま再利用。
- オーケストレータ `measure_worker_split8_fixb_memo_merge_73k_20261117.py` は出版fixB 2-wayモジュールをimportlibで読み込み、workdirを新dir `fixb_worker_split8_merge_73k_work/` に差し替えて全関数（エンジン生成・アサート・dump解析・distinct・merge・sim・seedrun・record恒等式・band比較）を再利用する。新規実装は8-way merge-join（nway_merge）とDP min-max 8分割のGROUPS定数のみ。入力pin: worker driver `2a95d952`・legal `8e97082c`・manifest `0892aed0`。simはlight_sim_seed_73k.mjs。
- 8分割: V1=[0,7,11]（band23プレフィックス）・V2=[15,35,39,41]・V3=[44,58,62,73]・V4=[76,87]・V5=[89,94]・V6=[95,97,98]・V7=[103,105,112]・V8=[117]。
- アーム: (1) fixB band ms23単一プロセス22 bit（band表比較の基準表生成）・(2) 8 fixB workers（freshプロセス・MS=1<<23・band内共有・per-bit nodes・KYOENWM1 dump・証明書byte gate・先頭bit anchor）・(3) dump重複キーcensus・(4) live bound 8-way merge（衝突検出・incidence・決定性2回実行）・(5) sim MS掃引 1<<24/1<<25/1<<26・(6) 設計点 MS=1<<25 seedrun 22 bit・record恒等式・(7) band表 vs 8-way merged表の集合比較。

## 測定結果

（測定JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/fixb-worker-split8-memo-merge-73k-20261117.json`・全gate検証済み）

1. **8-way workers**: v1 3,679,556 + v2 4,572,322 + v3 4,612,979 + v4 2,844,107 + v5 2,126,338 + v6 4,090,605 + v7 4,067,668 + v8 1,884,912 = **27,878,487 nodes**（fixB band23 28,620,380比0.9741・**fixB 2-way 27,837,399比1.0015**・出版verbatim 8-way 110,639,931比0.2520）。**fixBでは8-wayのworker利得が消滅する**（verbatimでは8-wayは2-way比0.9223で利得あり）。K0907 bug A/Bが後半bit汚染を介した「分割による汚染分離」利得の主因だったことの裏付け。V1はper-bit・最終占有率1,097,055ともにband23プレフィックスと完全一致、V2〜V8の先頭bitはfixB fresh battery anchorと完全一致。証明書は全workerでbyte同一（3/3・4/4・4/4・2/2・2/2・3/3・3/3・1/1）。
2. **重複キーcensus**: 8 worker dumpすべてでrecords == distinct（dup_keys=0・max_copies=1）。live bound被覆はnowin 11-12%・nolose 39-40%・win_and_lose=0・win_and_nowin_lt=0・all_unbound=0。
3. **live bound 8-way merge**: shared 2,270,338・occupied_after **5,773,620**（fixB 2-way merge 5,479,157の1.0537倍・出版verbatim 8-way merge 5,243,408の1.1011倍）・incidence {1: 3,503,282, 2: 1,672,101, 3: 493,437, 4: 95,044, 5: 9,342, 6: 409, 7: 5, 8: 0}（**incidence 8は0**: 全8 workerに現れるキーは存在しない）・内部衝突0・cross衝突0・merge決定的（2回実行でmd5同一）。
4. **sim MS掃引**（8-way merged seed 5,773,620 keys）: 1<<24 → 151,445失敗（2.623%・load 0.3351）・1<<25 → 10,842失敗（0.1878%・load 0.1717）・1<<26 → 92失敗（1.59e-5・load 0.0860）。
5. **設計点 MS=1<<25 seedrun**: **5,235,505 nodes**（seed 5,773,620 keys中挿入成功5,762,778・失敗10,842 == sim予測と完全一致）・record恒等式閉包（present 5,762,778 == inserted・missing == failed 10,842・値違反0）・証明書22/22 byte同一・最終占有率5,853,231（seedrun dumpもrecords == distinct・dup 0）。fixB 2-way seedrun25 6,005,236比**0.872**・出版verbatim最良8-way seedrun25 70,538,916比**0.0742 = 13.5倍安い**・未seed fixB band ms24 21,697,814比0.2413で、**エンジンと分割構成を横断したこのバンドの測定済み最安band実行**（fixB 2-wayの記録からさらに更新）。seed失敗率0.1878%はMS=1<<25の0.1%事前gateを超過（不成立はこのgateのみ）。5.77M keysは出版knee設計のMS=1<<25の0.1%境界（負荷<=~0.15設計線）を超えており、正しい設計点はMS=1<<26（load 0.086・sim予測92失敗）で、engineはこのcgroupで1<<26を確保できないためsimが担う（出版済みseed容量設計の記述どおり、gateは固定失敗率でなくseed負荷とkneeの距離で評価する）。失敗は性能のみで健全性に無影響。
6. **band表 vs 8-way merged表**: shared 5,028,405・only_in_band **48**（fixB 2-wayの677から48へ縮小・band表5,028,453 keysの0.00095%）・only_in_merged 745,215（2-wayの451,381の1.65倍）・共有キー値矛盾0（band_strictly_better_win_examples=0・merged_strictly_better_win_examples=0）。8-way unionはband表を実質的に覆い、かつ745,215 keysのband表外領域を追加する。merge表はband表のsupersetではないためcoordinatorはmerge表を近似として扱う必要があるという結論（追記5・追記4と整合）。

## gates

- 全worker証明書byte同一（計22 bit・全worker）、V1 per-bit/占有率 == band23プレフィックス、V2〜V8先頭bit == fixB fresh battery anchor: すべてTrue
- 全dump records == distinct（dup 0）・内部衝突0・cross衝突0・merge決定的: True
- seed失敗 == sim予測（10,842）: True
- record恒等式: 閉包（present == inserted・missing == failed・違反0）: True
- seedrun25証明書22/22 byte同一: True
- band_vs_merged8共有キー値矛盾0: True
- workers_total sanity: True
- 不成立はMS=1<<25の事前gate「seed失敗率<0.1%」のみ（0.1878%・出版knee設計の予測どおりで、5.77M-key seedではMS=1<<26が設計点）

## 実験事実（環境と実装）

- **同一セッション内の2回の完全実行（環境リセットを跨ぐ決定性の実証）**: 1回目は8 worker・merge・sim掃引・設計点seedrun25・record恒等式・band比較まで完走し全gateを検証したが、出版push直前に実行環境がリセットされ、workdir・測定JSON・orchestrator script・出版編集済みファイルがすべて失われた（重要証拠を再現不能なローカル状態に置かない運用原則により、数値はstate poll記録から、成果物は再実行から復旧）。入力をrepoから再取得し（extractor `52bcaf50`・driver `2a95d952`・legal `8e97082c`・manifest `0892aed0`の4 blob pinがすべてbyte同一であることを再検証）、2回目を完全実行した。workers合計・merge occupied_after/incidence・sim失敗数・seedrun25 nodes・seed失敗数・record恒等式・band_vs_merged8の全数値が1回目の記録と完全一致した。出版されたscript・測定JSONは2回目の実行によるもの。
- 全ジョブはsetsid nohupによる完全detachで起動（fixB 2-wayセッションで確立したプロセスグループkill対策）。状態はstate.jsonにcheckpointされ、pollは進行logのtailで行った。8 workerは逐次実行（控えめなCPU使用）。band23 arm（比較基準表生成用）を含む全アームのworker段階のwall timeは合計約5分、sort・merge・sim・恒等式・比較を含む全体は約20分。
- orchestratorは出版fixB 2-wayモジュールをimportlibで読み込みworkdirのみ差し替えて全アーム関数を再利用したため、fixBエンジン生成・アサート・dump解析・distinct・sim・seedrun・record恒等式・band比較の各実装は2-way出版物と同一コード。新規実装はnway_merge（8-way merge-join・incidence histogram・live bound cross衝突検出）とGROUPS/BAND23定数のみ。

## 解釈ガード

測定のみ。新規WIN/LOSS verdict無し・manifest行は1行も閉じない・証明書bytes不変・repo-verbatim extractorはrepo上未修正のまま。fixBを本番extractorとして採用するかは別レーンの判断。WIN7-D10は個別7石rootのdepth-10内先手勝ちのみ・REFUTED-D10はLOSS証明ではない。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWN**。
