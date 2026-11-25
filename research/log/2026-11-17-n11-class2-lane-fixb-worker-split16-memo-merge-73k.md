# 2026-11-17 n11 class2-lane: fixB 16-way worker分割memo merge測定（cost73k・K0907修正エンジン×K0909 16-way構成）

## 概要
出版済みのfixB 2-way（追記5）・fixB 8-way（追記7）測定を、出版verbatim 16-way測定（追記6）に対応する16-worker構成に拡張した（claim 273fb094・並走cost75f/cost78c等とは別軸）。fixBでのworker数曲線（2→8→16）を完成させ、(a) workerコストの単調増加への転換、(b) unionのN=8飽和、(c) seedrun利得の枯渇とseed失敗の増加、の3点を定量した。測定のみで勝敗変更なし。

## エンジンと入力
- engine: fixB（K0907監査済み両バグ修正の測定専用variant・repo-verbatim extractor blob `52bcaf50` はrepo上未修正）。出版fixB 8-wayオーケストレータ `measure_worker_split8_fixb_memo_merge_73k_20261117.py` を変換し、blob-pin済みパイプライン（fixB 2-wayモジュールをimportlib読み込み）を再利用。新規実装は16-way GROUPS定数とseed名のみ。
- 分割: fixB band ms23 per-bitノード数の連続DP min-max 16分割。min-max値 **2,900,183 = bit 117単独**（構造的下界そのもの・10単独bit worker＋6個2-bit worker）。V1 = [0]（band23プレフィックスアンカー）。
- manifest blob `0892aed0`・legal blob `8e97082c`・worker driver blob `2a95d952`。実行MSはworkers/band23が1<<23・seedrunが1<<25。全工程 `setsid nohup` detach・state.json resume・worker逐次実行（控えめCPU）。

## 測定結果
1. **16 workers**: 合計 **28,281,063 nodes**（v1 1,277,392 / v2 1,591,792 / v3 865,968 / v4 2,032,584 / v5 2,018,925 / v6 1,919,972 / v7 1,862,433 / v8 2,822,481 / v9 1,708,980 / v10 989,258 / v11 1,097,336 / v12 1,415,400 / v13 2,702,545 / v14 1,679,848 / v15 2,411,237 / v16 1,884,912）。fixB band23 28,620,380比0.9881・fixB 2-way 27,837,399比1.0159・**fixB 8-way 27,878,487比1.0144（+1.4%）**・verbatim 16-way 108,802,603比0.2599・**fixB fresh battery 28,290,025の0.9997**。fixBでは細分割のworkerコストが2→8→16で単調増加に転じ、fresh床に収束する（band23比は2-way 0.9726 → 8-way 0.9741 → 16-way 0.9881）。V1はper-bit・占有率ともband23プレフィックス（bit 0: 1,277,392 nodes・372,070 slots）と完全一致、他15 workerの先頭bitはfixB fresh battery anchorと完全一致（15/15）、全worker証明書byte同一（22/22）。
2. **重複キーcensus**: 16 dumpすべてでrecords == distinct（dup_keys 0・max_copies 1）。
3. **live bound 16-way merge**: shared 2,369,039・occupied_after **5,794,358**（fixB 8-way 5,773,620の**+0.36%でunionはN=8でほぼ飽和**・2-way 5,479,157比+5.75%・verbatim 16-way 5,404,082比1.0722）・incidence {1:3,425,319, 2:1,654,929, 3:540,872, 4:143,585, 5:26,303, 6:3,100, 7:241, **8:9**, 9..16:0}（incidence 8はfixBで初出現〔9 key〕・全16 worker同時memo化キーは存在しない）・内部/cross衝突0・決定的（2回実行でmd5同一）。
4. **sim MS掃引（5,794,358 keys）**: 1<<24→164,898失敗（2.8458%・load 0.3355）・1<<25→14,354（**0.2477%**・load 0.1723）・1<<26→177（3.1e-5・load 0.0863）。
5. **設計点 MS=1<<25 seedrun**: **5,197,507 nodes**・seed失敗14,354 == sim予測完全一致・record恒等式閉包（present 5,780,004 == inserted・missing == failed・違反0）・証明書22/22 byte同一・最終占有率5,857,373。fixB 8-way seedrun25 5,235,505比**0.9927（−0.7%）でseed充実の利得はほぼ枯渇**・fixB 2-way 6,005,236比0.8655・**verbatim 16-way seedrun25 68,006,820比0.0764 = 13.1倍安い**でエンジン・分割構成横断の測定済み最安band実行（追記7の記録を更新）。sim==engine完全一致は5.79M-key seed領域まで拡張。失敗率0.2477%での0.1%事前gate不成立は出版knee設計どおり（正しい設計点はMS=1<<26・sim予測177失敗・engineはcgroup内で1<<26不可のためsimが担う）。失敗は性能のみで健全性に無影響。
6. **band表 vs 16-way merged表**: shared 5,028,439・only_in_band **14**（2-way 677 → 8-way 48 → **16-way 14**でband表の0.00028%まで縮小）・only_in_merged 765,919・共有キー値矛盾0。merge表はband表のsupersetではないという結論（追記4・5・7）はN=16でも修正されないが、unionはband表の実質完全被覆に漸近する。

## gates
14/15合格。不成立は `seed25_failure_rate_below_0.1pct`（0.2477% > 0.1%）のみで、出版knee設計（MS=1<<25の0.1%境界はS≈4.1-4.2M keys・5.79M keysは境界を大きく超過）の予測どおり。検証gate（v1プレフィックス・先頭bit anchor・census・内部/cross衝突0・決定性・sim==engine・record恒等式・証明書byte同一・band比較矛盾0・workers sanity）は全て合格。

## 実験事実（環境と実装）
単一セッションで全アーム完走（起動から測定JSON書き出しまで約13分・band23単一プロセス約3分・16 worker逐次・merge/sim掃引/seedrun/passes残り）。実行環境リセットは今回事象なし。state.json resumeで全段階再開可能。orchestratorは出版8-wayオーケストレータの変換で、py_compile・ASCII純度検証済み・実装バグなし。

## 解釈ガード
測定のみ・新規WIN/LOSS verdict無し・manifest行は1行も閉じない・証明書bytes不変・repo-verbatim extractorはrepo上未修正・fixB本番採用は別レーン判断・WIN7-D10は個別7石rootのdepth-10内先手勝ちのみ・REFUTED-D10はLOSS証明ではない・**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWN**。
