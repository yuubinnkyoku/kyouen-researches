# 2026-11-21 n11 residual72 worker-partition 精密閉包・UB witness セッションlog

## 判断の経緯

- 本実行は長期レーン（標準11×11決着）として、まず最新main（開始時HEAD `fe945df2`→13:42Z時点で
  `3ceba86b`）・AGENTS.md・実験dir一覧を確認した。掃引オーナーレーン・reply27 S5 probeレーン・
  seven-row/three-row q4レーン・36root membershipレーンが並走中であり、いずれにも着手しない。
- worker partition candidateレーン（`f7466198`）は「one-swap local optimum, not a global
  optimum」、exact-class-membershipレーン（`432db238`）は「クラス計数のみで割当最適値なし」を
  明示的に残しており、割当目的関数の大域最適値・下界は両レーンの後続の未着手測定ギャップである。
  一次素材はすべて出版済み（census・candidate・multi-root-classes・exactclass）で掃引オーナー
  レーンと完全に独立。このギャップを埋める測定を本レーンの対象とした。
- 単一オーナー宣言 `459621ab`（13:50Z・宣言時直前HEAD `3ceba86b`）を出版してから実験dirを出版した。
  計算・検証は同一sandbox内で宣言前に完了していた（宣言ノートの透明性節に明記）。

## 実施内容

全モード、入力5点をSHA-256 pin（census `94fdb0c6…`・partcand `09b394b8…`・mr10 `5fec87af…`・
mr09 `68aa7df1…`・exactclass `37ea472e…`）で検証してから実行。目的関数は
class10 = 多重所属10石クラスの (worker span − 1) 総和、pair10 = 横断root対の共有クラス重み付き総和、
cross9 = 9石層の同class型目的（全多重所属9石クラスが2-root）。

1. **精密閉包（決定論anneal UB → UB未満全列挙のDFS B&B。閉包時のみ大域最適を主張）**:
   - W=2: class10大域最適 **732**（1,931 nodes・100s）・pair10大域最適 **737**（1,955 nodes）。
   - W=3: class10大域最適 **908**（301,671 nodes・0.1-0.2s）・pair10大域最適 **913**（308,146 nodes）。
2. **非閉包の正直言報（UB witnessのみ主張・大域最適性は主張しない）**:
   - W=4: class10 UB **1937**（501,219,328 nodes・170sで閉じず）・pair10 UB **1939**（686,817,280 nodes）。
     同一分割がcross9 **47**も同時達成（super-witness。d4 spread 10.7893% > 8% でT2非適合）。
   - W=6: class10 UB **2558** / pair10 UB **2562**（同一分割・cross9 62・90sで閉じず）。
   - 9石層: cross9 UB **47**（316,669,952 nodes・150sで閉じず・w4 witnessとは別分割でも47。
     47-witnessの一意性なしを再確認）。
3. **1-swap証明書（出版candidateを中心とした全数列挙）**:
   T1（バランスのみ）486 feasible / 3 improving / best 13↔19 → 1937(class)・1939(pair)。
   T2（+8% d4 cap）222 / 0 / 1998・2000 = 出版one_swap_checkの完全再現。
4. **大型anneal**: t1class/t1pair 1,500 restarts × 60,000 iters で1937/1939を破れず。
   t2class/t2pair 2,500 restarts × 60,000 iters（各1.5億iters）でも1998/2000を破れず。
   **T1・T2大域最適性はUNKNOWNのまま。**
5. **独立Python検証器（JS実装と一切コード共有なし・fail-closed・全142 gate PASS）**:
   入力pin・構造（mr10 2-root 5,420+3-root 5類・mr09 133）・出版candidate統計の全再現
   （class/pair/within/cross/loads/spreads/比較%/one_swap_check 222/0/2000）・
   exactclass partition_stats全再現（within定義はsplit triple同一worker対を含む
   Σ max(0, m_w − 1) で1241に一致）・全witness再計算・閉包表記整合・
   same-partition事実（W∈{2,3,4,6}でclass witness == pair witness）・super-witness三同時達成・
   候補比gap −61/−61/−2・T2非適合。

## 実装・運用の記録（失敗を含む）

- 本セッションは実行中に3度のsandbox環境リセット（240s bash timeoutが引き金）と3度のコンテキスト
  圧縮を経験した。成果物生成のたびにknowledge kitへ即退避する運用に切り替えたことで損失ゼロ。
  それ以前の実装で存在した「42M nodesでx9/1937/1939を閉じる強LB」の再現は断念し、
  W=4/x9/W=6は「UB witness + 非閉包の正直記録」として出版する方針を維持した。
- B&B実装で見つけ全runで維持した修正: (a) swap-Δの第三グループ寄与は0、(b) triple状態はSetでなく
  slot配列（同じworkerに2メンバーが戻るときのunwind破壊を防ぐ）、(c) class目的是のtriple増分を
  assign時に加算し葉でscratch assertsと一致。JSのconst gsスコープbugはruntimeで即検出・修正済み。
- **heavy-first順序**（pair重み行和降順）でw3classが324M → 326k nodes（約1000倍）に短縮し閉包に到達。
  ただしx9ではindex順・dynamic順も非閉包で、順序だけでは解けない。閉包には強LBが別途必要。
- 出版前のpath適合: script 3点をrepo相対path（入力は3レーンの出版JSON）へ改修。このとき
  (i) solvew側`pins_verified`出力がrepo pathになり出版物（logical名）と不一致するのを論理名に固定、
  (ii) 検証器の`os.path.exists`3箇所のうち1箇所（正条件側）の置き漏れで142→140 gateに落ちるのを
  検出・修正。改修版3点のsanity: oneswapT2class出力byte-identical、w2class全再現
  （時間欄以外完全一致・1,931 nodes）、検証器142 gate PASSかつ結果JSONがkit正本とbyte-identical。
- B&B系の実測参考値: w4class B&Bは約2.9M nodes/s（170s・501M nodes）。
  anneal seed: x9=305093817、w*class=3735928559+W、w*pair=781605401+W、t1class/t1pair/
  t2class/t2pairは固定（search.js参照）。iters 60,000固定。

## 出版物

- part0 宣言: `459621ab`（fetch-back byte一致）
- part1 実験dir: `92d28217`（README・scripts 3点・output 19 JSON・23ファイル単一コミット。
  fetch-back 23/23 byte一致）
- part2 本log・part3 `research/experiments/n11-search-methods/README.md` への参照行1行追加。

## 解釈とレジューム

- W∈{2,3}の4つの大域最適値（732/737/908/913）はbalanced割当全体に対する厳密値である。
  W=4/6・9石層の1937/1939/2558/2562/47は**UB witnessのみ**であり大域最適値ではない。
  T2（8% cap）下での大域最適性もUNKNOWN（candidate 1998/2000がone-swap / 大型annealで破れていない
  だけ）。super-witness（1937/1939/47の三同時達成）はT2非適合なのでsweep割当の根拠にはならない。
  実測TT hitがない段階であり、sweep割当変更の提案は引き続き行わない。
- 幾何的クラス重複は表命中率ではない。nodes数・目的関数値・solved数を勝敗として読まない。
- 次回レジューム: (a) w4/x9/w6閉包には強LB（例: unassigned-root間の相互作用を含む下界・
  LP緩和・tabu/大近傍探索）が必要。42M nodes閉包の再現が期待できる場合、B&BのLB強化が最短経路。
  (b) 9石層・8石層の同種閉包（8石層はroot間共有0なので自明）・W他値の掃引は安価に拡張可能。
  (c) 掃引オーナーが実測TT hit/表再利用計数を出版した時点で、本測定の幾何値との3層対照
  （pairwise proxy・クラス計数・実測hit）が高価値。
- **REFUTED-D10はLOSS証明ではない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 verdictsはすべてUNKNOWNのまま。**


## 事後追加（addendum・2026-11-21T14:1xZ出版）

part3出版後、実行時間が残っていたため9石層のclosure samplerを拡張した。

- `worker_partition_bnb_closure_20261121.mjs` に `x9w{N}` モードを追加（mode名からWを一般化・
  seedは305093817+W・x9のW=4固定と排他的な新モードで既存結果に非干渉）。
- **W=2の9石層cut大域最適 17**（1,198 nodes・100s・閉包）・**W=3の大域最適 22**
  （157,346 nodes・閉包）を確定。両モード2回再実行で時間欄以外byte-identical。
- **構造的発見**: x9w2 witnessはw2class/w2pairのclosure witnessと完全同一の分割。
  つまりW=2では**1つのbalanced分割がclass10最適732・pair10最適737・cross9最適17の
  3層大域最適を同時に達成**する。W=3では10石層のclosure witness自身もcross9 22
  （=大域最適）を達成しており、さらに別分割（x9w3 witness）も22に到達することから
  9石層22の最適分割は非一意（x9の47と同様の非一意性だが、こちらは値が大域最適確定済み）。
- 検証器に20 gate追加（x9w2/x9w3のwitness再計算・閉包表記・same-partition性
  （w2classと同一）・w3class witnessとの非同一・10石層witnessの9石層最適値の同時達成）。
  **ALL 162 GATES PASS**。`experiment_summary_20261121.json` をv2へ更新
  （proven_global_optimaにx9_w2_cross9=17・x9_w3_cross9=22、gates_total 162、
  structural_findings_addendum節を追加）。
- 依然として**W=4/6・x9(W=4)・T1・T2の大域最適性はすべてUNKNOWN**。
  標準11×11空盤・二石root・S2・class 1/2/4 verdictsはすべてUNKNOWNのまま。


## 事後追加2（addendum 2・2026-11-21T14:4xZ出版）

- 出版済みUB witnessの1-swap全近傍（各486 swap）を独立測定。
  **super-witness（1937/1939/47）はclass10・pair10・cross9の3目的すべてでstrict 1-swap局所最適**
  （最良隣接1962/1966/48・すべてのbalanced swapが厳密に悪化）。9石層x9 witness（別分割・47）も
  cross9について非厳密な1-swap局所最適（最良隣接47・改善0）。
- `scripts/oneswap_witness_neighborhood_20261121.py`（独立測定機・入力3点pin・
  witness読込cross-check・`/tmp/det`隔離環境でbyte-identical再現）を追加し、
  検証器に5 gate（3目的の厳密局所最適・x9 witnessの改善0・成果物JSON整合）を追加。
  **ALL 167 GATES PASS**。summary v3化。
- この測定は局所最適性の証明のみで、**W=4/6・x9(W=4)・T1/T2の大域最適性はすべてUNKNOWNのまま**。
  標準11×11空盤・二石root・S2・class 1/2/4 verdictsはすべてUNKNOWNのまま。
