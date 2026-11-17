---
id: K0909
title: cost73kバンドのworker分割メモmergeは衝突0で安全・merge seed band実行はband ms24比80.2%
kind: verification
status: verified
topics: [certificates, verification, search-methods]
aliases: []
relations: []
artifacts:
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split_memo_merge_73k_20261117.py
    role: verifier
    note: オーケストレータ（worker実行・KYOENWM1 dump・sortベースmerge・衝突検出・KYOENWM2 seedrun・record恒等式ゲート・全gate判定）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split_memo_73k.ts
    role: source
    note: worker/seedrunドライバ（per-bit snapshot+clearRows・dumpMemo/seedMemo）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/worker-split-memo-merge-73k-20261117.json
    role: data
    note: 測定JSON（全gate合格・prior session値との差分記録入り）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split4_memo_merge_73k_20261117.py
    role: verifier
    note: 4-worker N-way拡張オーケストレータ（ノード数均衡4分割・heapq N-way merge-join・incidence histogram・merge seed band実行・全gate判定）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/fault_inject_worker_merge_conflicts_20261117.py
    role: verifier
    note: 衝突検出器のfault注入試験（streaming設計・合成破損の正確検出・誤検出0・sentinel吸収の実証・全gate判定）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/worker-split4-memo-merge-73k-20261117.json
    role: data
    note: 4-way測定JSON（13/14 gate合格・seed挿入失敗0.324%のgate超過を事実として記録・record恒等式は閉じている）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/fault-inject-worker-merge-conflicts-73k-20261117.json
    role: data
    note: fault注入試験JSON（7/7 gate合格・注入キーと検出サンプル完全一致・F5吸収はclean mergeと完全一致）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split4_boundary_memo_merge_73k_20261117.py
    role: verifier
    note: 境界保存4-way拡張オーケストレータ（W0..W3六pairwise+cascade merge・2-way worker同時再実行アンカー・FINAL4 vs 2-way seed鍵集合比較・FINAL4 seed seedrun）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/worker-split4-boundary-memo-merge-73k-20261117.json
    role: data
    note: 境界保存4-way測定JSON（2-way出版パイプラインのbyte完全再現・全工程2回実行でbyte同一・merge非閉包only_in_seed2 262を記録）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/light_sim_seed_73k.mjs
    role: verifier
    note: 軽量seed挿入simulator（verbatim mHash + 64-slot線形探査の占有率のみ・実seedキーでMS掃引・prefix knee・失敗attribution）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_seed_capacity_design_73k_20261117.py
    role: verifier
    note: seed容量設計オーケストレータ（pin付きblob再構築による4-way/2-way再現・sim二重anchor検証・design point MS=1<<25 band実行・16 gate判定）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/seed-capacity-design-73k-20261117.json
    role: data
    note: seed容量設計測定JSON（16/16 gate合格・engine seed失敗28==sim予測28・record恒等式閉包・MS=1<<25 band実行72,745,351 nodes=ms24 seedrun比0.9459）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_hybrid_seed_union_73k_20261117.py
    role: verifier
    note: ハイブリッドseed union測定オーケストレータ（pin付き再構築・262レコード再抽出・hybrid seed構築・sim・MS=1<<25 seedrun・record恒等式・全gate判定・run A・824行）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_hybrid_seed_union_73k_independent_20261117.py
    role: verifier
    note: 独立実装の同一測定オーケストレータ（run B・957行・境界seedrun24のin-run再現アンカー・prefix merge join+tail hash join方式のrecord恒等式）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/hybrid-seed-union-73k-20261117.json
    role: data
    note: run A測定JSON（全gate合格・262レコードmd5 1d97a0d2…・hybrid seed md5 d24198ea…・seedrun25 72,761,010 nodes）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/hybrid-seed-union-measurement-73k-20261117.json
    role: data
    note: run B測定JSON（59 gate合格・独立実装との全数値一致・record恒等式prefix/tail分割検査）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/hybrid-seed-union-independent-verification-73k-20261117.json
    role: verifier
    note: claimセッションの独立検証JSON（hash・tail byte同一・証明書22/22・record恒等式独自再実装・run間完全一致・3セッション実行履歴と環境リセット記録）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split8_memo_merge_73k_20261117.py
    role: verifier
    note: 8-worker分割測定オーケストレータ（連続DP min-max 8分割・先頭bit fresh anchor・8-way heapq merge・sim MS掃引・MS=1<<25 seedrun・record恒等式・全gate判定）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/worker-split8-memo-merge-73k-20261117.json
    role: data
    note: 8-way測定JSON（15/15 gate合格・worker合計110,639,931 nodes・merge 5,243,408 keys・seedrun25 70,538,916 nodes・seed失敗383==sim予測）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split_fixb_memo_merge_73k_20261117.py
    role: verifier
    note: fixB worker分割merge測定オーケストレータ（fixB band23・2 worker・live bound merge・seedrun24・設計点seedrun25・sim交差検証・record恒等式・全gate判定）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/fixb-worker-split-memo-merge-73k-20261117.json
    role: data
    note: fixB測定JSON（workers 27,837,399 nodes・dup_keys 0・merge衝突0・seed失敗==sim予測・設計点ms25 gates全合格）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split16_memo_merge_73k_20261117.py
    role: verifier
    note: 16-way worker分割測定オーケストレータ（連続DP min-max 16分割・10単独bit＋6個2-bit worker・16-way heapq merge・sim MS掃引・MS=1<<25 seedrun・record恒等式・全gate判定）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/worker-split16-memo-merge-73k-20261117.json
    role: data
    note: 16-way測定JSON（15/15 gate合格・worker合計108,802,603 nodes・merge 5,404,082 keys・seedrun25 68,006,820 nodes・seed失敗2,285==sim予測）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split8_fixb_memo_merge_73k_20261117.py
    role: verifier
    note: fixB 8-way worker分割merge測定オーケストレータ（band23 per-bit DP min-max 8分割・V1=band23プレフィックス・8-way merge-join・sim MS掃引・設計点ms25 seedrun・band表vs merged表比較・全gate判定）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/fixb-worker-split8-memo-merge-73k-20261117.json
    role: data
    note: fixB 8-way測定JSON（workers 27,878,487 nodes・merge 5,773,620 keys・衝突0・incidence 8は0・seed失敗10,842==sim予測・seedrun25 5,235,505 nodes・record恒等式閉包）
---

# K0909: worker分割メモmergeの安全性（cost73kバンド・verbatim engine）

## 主張（有限測定の検証）

cost-73kバンド（child `00000000000000801206000000000400`・22 WIN7-D10 root・manifest blob `0892aed0`）の
証明書抽出メモ（位置keyed・engine verbatim blob `52bcaf50`・K0907監査済みの2欠陥を含むまま）について:

1. **2 worker分割（73/76境目・各11 bit・band内共有・MS=1<<23）の実行**は
   合計119,962,147 nodesで、band ms23単一プロセス121,186,659の0.9899。
   worker A（bits 0..73）はband ms23プレフィックスとper-bit完全一致（48,482,011 nodes・
   最終占有率slot 5,263,320）。分割は85%負荷の単一テーブル後半bitの汚染を避けつつ
   worker内共有を保持するため、ms23単一プロセスよりむしろ1.0%有利。
2. **KYOENWM1全slot dump（A 5,263,320レコード/B 6,242,804レコード）のsortベースmerge**
   （win=min・lose=min・nowin=max・nolose=max・255=非bound結合）は
   distinct A 2,619,833 + B 2,554,155・cross共有882,089・merge後occupied_after 4,291,899。
   **内部衝突0・cross衝突0**（衝突定義は両側255非boundを考慮：win<255∧lose<255・
   win<255∧nowin<255∧nowin>=win・lose<255∧nolose<255∧nolose>=lose）。
   重複キー（符号キーバグによる重複挿入）は全てhigh-bitで最大64コピー。
   つまりworker間でメモ値は大域的に一貫しており、**worker cacheの安全merge
   （WIN/LOSS矛盾の即時検出）が出版engineの実測で裏付けられた**。
   merge自体は2回実行でbyte同一（決定的）。
3. **merge表（KYOENWM2・4,291,899レコード）をseedとしたMS=1<<24全22 bit band実行**は
   85,747,496 nodes（未seedのband ms24 106,861,135の80.2%・fresh ms23電池108,499,241の79.0%）・
   最終占有率slot 10,614,912（負荷率63.3%・merge後load設計どおり）。
   seed 4,291,899件中1,448件（0.034%）は64-slot探査窓飽和で挿入失敗
   （25.6%初期負荷でのverbatim hash clustering由来・性能のみで健全性無影響）。
   **証明書22/22 byte同一**。最終dumpのrecord恒等式ゲート：挿入成功4,290,451 keyは
   全て残存し結合値はseed値と同等以上（違反0）、欠損は挿入失敗1,448件ちょうど。
   bit95は11,857,737 nodesで全構成と一致（memo-state-invariant root・K0907と同じ観察）。
4. **4 worker分割（ノード数均衡・W1=band ms23プレフィックス・各worker MS=1<<23・band内共有）の
   N-way拡張**は合計112,741,501 nodes（2-wayの0.9399・band ms23の0.9303・
   W1 29,193,572/W2 30,417,638/W3 31,104,578/W4 22,025,713）で、W1はband ms23
   プレフィックスとper-bit完全一致（証明書7/7 byte同一・W2 6/6・W3 5/5・W4 4/4）。
   distinct W1 1,979,858/W2 1,793,658/W3 1,544,867/W4 1,565,935、
   sort済distinct表のheapq N-way merge-joinは
   **occupied_after 4,985,986（2-way比+694,087・+16.2%）・shared 1,592,504・
   incidence histogram {1:3,393,482, 2:1,306,914, 3:265,352, 4:20,238}・
   内部衝突0・cross衝突0・merge決定的**。unionが2-wayより大きいのは、細分割で
   worker負荷が下がりdump時点の64-slot窓飽和によるキー欠落が減ったためで、
   merge表はより完全になった（欠落は性能でなく完整性の問題であり、
   細分割はmerge seedの質を上げる）。
5. **4-way merge seed（4,985,986レコード・md5 7b098aeb…）でのMS=1<<24全22 bit band実行**は
   **76,903,818 nodes（2-way seedrun 85,747,496の0.8969・未seed band ms24 106,861,135の
   0.7197・fresh ms23 108,499,241の0.7088）**・最終占有率10,526,730（負荷62.7%）・
   **証明書22/22 byte同一**。seed挿入失敗は16,137件（0.324%・初期負荷29.7%・
   2-wayの0.034%比で約10倍：seedが大きいほどclustering窓飽和が非線形に増える）。
   事前gate「挿入失敗<0.1%」はこの値で不合格（13/14 gate合格）だが、record恒等式は
   閉じている（挿入成功4,969,849 key全て残存・値違反0・欠損は挿入失敗16,137件ちょうど）。
   bit95は11,857,737 nodesでどのseedでも不変（memo-state-invariant）。
6. **衝突検出器のfault注入実証（実データ）**: 自然衝突が0のため検出器自身は
   発火実績がなく未実証だった。実dump/distinct表のコピーに決定的な合成破損を注入した
   結果、検出は**ちょうど注入した矛盾に限り誤検出0**であることを実証した:
   F1（W2 raw dumpに既存win-boundキーの重複レコードをlose=3で追記）→sort+distinct
   pipelineがちょうど2件の内部win_and_lose・F2/F3（共有キーのcross lose/win注入）→
   N-way mergeがちょうど4件のcross win_and_lose・F4（incidence-1キーの単一レコードに
   nowin=winを注入）→ちょうど2件のwin_le_nowin、いずれも検出サンプルは注入キーと
   完全一致。F5（W3レコードにnowin=4/nolose=2を注入）は他workerの255 sentinelが
   max結合で吸収し発火せず、**fault merge後レコードはclean merge後レコードと完全一致**
   （正境界は保持され注入負境界は吸収）。fault mergeの構造計数
   （occupied_after 4,985,986・shared 1,592,504・incidence histogram）はclean mergeと
   完全一致し、破損が値のみを変えたことを確認。
   **merge時検出のキャッチメントは結合値の論理矛盾（両側が実境界のwin∧lose・
   win<=nowin・lose<=nolose）ちょうどと特徴づけられた**。単一workerの負境界が
   他workerの非bound sentinelに吸収されるのは仕様（論理矛盾でない）であり、
   検出不能性ではなく検出不要性である。

## 測定上の注意

- 前セッション（2026-11-17早く）の同一測定はスクリプトを環境リセットで喪失。
  本測定は新規実装による再構築で、worker合計119,962,147 nodesは前セッション記録値と
  完全一致したが、merge後occupied_afterは前セッション記録4,291,129に対し4,291,899
  （+770・0.018%）。前実装の詳細は失われているためこの差は実装差として記録する
  （本実装はoccupied_after = distinctA + distinctB - shared を厳密に計算）。
- 実装中に発見した自分のバグ3件（実験事実として記録）: (a) 結合関数のtuple index誤り、
  (b) dump header行がsortを通ってしまいrecord parserが落ちる、(c) chunk分割sortの
  `sort -m`に`-k2,5`を付け忘れslot順の「整列」ファイルができrecord恒等式ゲートが
  368万key「欠損」と誤検出（ゲートが実装バグを捉えた好例・修正後は欠損=挿入失敗1,448件ちょうど）。
  (d) 255 sentinelをbound扱いする衝突定義は誤り（verbatim engineの負境界は死んでおり
  nowin/noloseは常に255・衝突は起こり得ない）。
- 環境のサイレントなプロセスkill（推定）で630MB dumpの単発sortが2回中断されたため、
  chunk分割sort+resume方式に切り替えて完走。
- 4-way測定は2環境インスタンスにまたがって実行された（bash復帰時のプロセスグループkill 2回・
  環境フルリセット1回でW1〜W3完了分を喪失し再構築）。リセット前後でW1/W2/W3の
  ノード数・占有率は完全一致（クロス環境決定性の追加証拠）。再構築は全入力を
  raw CDNからpin検証付きで再取得。
- fault試験の初回実装（4 distinct表を全てメモリに載せる設計）は~1GiB cgroup制限で
  OOM kill 2回（tracebackなしの静寂死・dmesgのoom-killで確定）。streaming書き換え
  （heapq選択1pass・streaming表コピー・orchestratorのdistinct_pass/merge_pass_nway再利用）で
  数分で完走。長い単発工程はこの環境では脆く、resume可能な工程とメモリ定数設計が要る。
- F5シナリオの当初設計（W3レコードが完全unbound＝4値全て255のキー）は実表に存在せず
  （実表のレコードは必ずwinかloseの正境界を持つ）0/2で選択失敗。verbatim engineの
  nowin/noloseは常に255（K0907）なので、任意のW3レコードへの注入で吸収試験は
  常にwell-posedであり、この緩和版で実施した。

- 実行環境のフルリセット（bashのdefault timeout超過でblocking読み込みが発生）により作業treeを喪失し、
  seed容量設計測定はpin付きblob（orchestrator 50b60247・extractor 52bcaf50・manifest 0892aed0・legal 8e97082c）からの
  完全再構築として実行した。再構築後も全出版値（両merge seed md5を含む）が厳密に再現され、
  クロス環境決定性が再度確認された。
- MS=1<<25 seedrunは3回のOOM killで環境上限（~1.09 GiB cgroup・typed arraysだけで672MB）を特徴付けた:
  cap 500はdumpMemo 26%で死・cap 200は22 bit探索完走後にdumpMemo 61%で死（VmRSS 806MBで安定）・
  cap 150は~5.6GBの中間dumpがpage cacheに乗った状態でbit 15前に探索中に死（memory.peak=cgroup上限値ちょうど）。
  単離再現（672MB typed arrays + verbatim dumpMemo chunkループ・cap 200・678MB書き込み）は生存し、
  arrays+dumpループ単独ではkillを説明できない。完走版はcap 200で(a)不要中間ファイル5.1GBの削除とpage cache解放、
  (b) MS=1<<25 variantのみのdumpMemo fsync強化（32MiB毎+最終fsync・dump bytes不変・実測~36ms/32MiB）
  により840MB dumpをOOMなしで完走した。
- MS>=1<<26のengine全band実行は本環境のcgroupでは不可能（typed arraysが1.34GB/2.68GB）。
  MS掃引はsimulatorが担ぎ、MS=1<<24で2 anchor・design point MS=1<<25で1回のcross-validation済み。

## 解釈ガード

測定・検証のみ。新規WIN/LOSS verdict無し・manifest行は1行も閉じない・証明書bytes不変。
repo-verbatim extractorはrepo上未修正のまま（出版決定性チェーン）。WIN7-D10は個別7石rootの
深さ10以内の先手勝ちのみを証明し、REFUTED-D10はLOSS証明ではない。
11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はいずれもUNKNOWN。

## 境界保存4-way分割の独立測定（2026-11-17追記・測定のみ）

同じバンドを出版2-wayと同一のbit境界（39/41・73/76・97/98）で4 workerに分割
（W0=bits 0..39・W1=41..73・W2=76..97・W3=98..117・MS=1<<23・band内共有・
証明書byte同一gate）し、出版2-way（workerA/B）を同一orchestrator内で再実行して
**merged seed md5 `e7c2c17e7a91d8ea17f433f3bb482f29`・workers合計119,962,147 nodes・
per-bit nodes/occupancy系列を全て出版値とbyte同一で再現**した上で、
六pairwise+cascade merge・FINAL4 vs 2-way seed鍵集合比較・FINAL4 seedによる
MS=1<<24全22 bit band実行を測定（独立環境での測定・全工程2回実行で出力JSON byte同一・
`measure_worker_split4_boundary_memo_merge_73k_20261117.py`）:

1. **4-way worker合計111,953,183 nodes**（出版2-way比0.9332・band ms23比0.9238・
   並走のノード数均衡7/6/5/4分割112,741,501比も0.7%安い）。W0/W2は2-way接頭辞と
   per-bit完全一致。fresh再開のoccupancy-harmはper-bitで定量: W3後半5 bitは
   carried比−6,012,227 nodes（−17.8%・bit117単独で7,739,551 vs 10,008,242）。
   fresh workerの先頭bitのみ逆行（bit41 +5.6%: 直前bit群のmemoを失うため）。
2. **衝突0は境界保存4-wayでも完全**: W0..W3内部衝突0・六pairwise cross衝突0・
   cascade（M01 shared 472,945・M23 368,177・最終merge shared 1,137,932）も0。
   mergeは各段階2回実行でbyte同一。FINAL4 = 4,975,265 distinct keys
   （2-way seed比+15.9%）。並走測定の全重複量（衝突0・byte同一22/22・
   record恒等式閉包・seed失敗率0.1%超え）と独立に一致（交差検証成立）。
3. **merge非閉包の定量（本測定の固有成果）**: FINAL4 vs 2-way seedは
   共有4,291,637 key全て同等以上（違反0）だが、**only_in_seed2 = 262
   （0.0061%）**: より細かい分割のmerge表は2-way merge表の厳密supersetではない。
   verbatim memoの探索・挿入は経路依存で、unsplit workerがmemo化した位置の
   一部は分割側で到達も挿入もされない。unionが大きいこと（+683,628 net）と
   supersetでないことは両立し、「merge表はより完全」は濃度についてのみ成立。
   coordinatorはmerge表を近似として扱い、より粗い構成のcacheの代替にしてはならない。
   コストのみで健全性無影響（証明書22/22 byte同一・seedrunで再計算される）。
4. **FINAL4 seed seedrun 76,599,320 nodes**（出版2-way seedrun比0.8933・
   未seed band ms24比0.717・並走の76,903,818比0.4%安い）・最終占有率10,525,071
   （負荷62.7%）。seed挿入失敗14,657件（0.295%・並走の0.324%と独立に同じ
   0.1%予測gateを不成立化: 失敗率はseedサイズに対し超線形）。record恒等式は
   挿入成功4,960,608 key全残存・違反0・欠損は挿入失敗14,657件ちょうど。
5. **gates_all_pass=Falseは予測gate 2件のみ**（(a) superset予測・(b) seed失敗率
   <0.1%）で、健全性/正確性/再現/衝突0/決定性gateは全合格。両不成立は実測事実
   として記録し、gate定数の再設計（0.1%は大きいseedには不適切）を次回に残す。

勝敗変更なし・11×11はUNKNOWN。

## N-way merge seed容量設計（2026-11-17追記2・測定のみ・gate定数の再設計）

両4-way測定（ノード均衡・境界保存）が事前gate「seed挿入失敗<0.1%」を0.324%/0.295%で破った件の
gate定数再設計として、N-way merge seedの容量設計規則を確定した
（`measure_seed_capacity_design_73k_20261117.py`・軽量simulator `light_sim_seed_73k.mjs`・
測定JSON 16/16 gate合格・独立log `2026-11-17-n11-class2-lane-seed-capacity-design-73k.md`）:

1. **出版pipelineの完全再構築**: pin付きblobから4-way pipelineを再構築し、全出版値
   （workers W1 29,193,572/W2 30,417,638/W3 31,104,578/W4 22,025,713 nodes・distincts・
   merge occupied_after 4,985,986・seed md5 7b098aeb…・seedrun4 76,903,818 nodes・seed失敗16,137・
   record恒等式）をgate逐一致で再現。2-wayもworker A 48,482,011/B 71,480,136 nodes・
   distincts 2,619,833/2,554,155・生seed md5 1599c496…・出版header置換で出版md5 e7c2c17e…完全一致。
2. **軽量simulatorの二重anchor検証**: verbatim mHash（4語imul XOR）+64-slot線形探査の
   占有率のみを複製するsimulatorは、distinct-key seedではengineのkey-match分岐が非到達になるため
   厳密。MS=1<<24で両engine anchorに完全一致（4-way 16,137・2-way 1,448）。
3. **MS掃引**（4-way seed 4,985,986 keys）: 1<<24→16,137（0.324%・load 0.296）・
   **1<<25→28（0.00056%・load 0.149・0.1% gateを2桁の余裕で合格）**・1<<26→0。
   失敗機構はhash clustering: 最大base indexに109 distinct keys（>=64 keysのbaseが
   1,224,783中250）・own-cluster飽和2,278+spill-over 13,859。
4. **MS=1<<24でのseedサイズknee**（実キー・merge順のprefix実測）:
   S=1M/2M→0・3M→26・3.5M→256・4M→2,017・4.29M→5,969・4.5M→8,233・4.75M→11,410・4.99M→16,137。
   0.1% gate境界はS≈4.1-4.2M keys: 2-way（4.29M・0.034%）が合格し両4-way（~4.99M・~0.3%）が
   破った理由を定量的に説明する。gate定数は固定MSでの固定失敗率ではなくseed負荷（S/MS）と
   kneeの距離で設計すべき。
5. **design point MS=1<<25の全band engine実行**: seed 4,985,986中28件失敗==sim予測28（0.00056%<0.1%）・
   証明書22/22 byte同一・record恒等式閉包（present 4,985,958・missing==28・違反0）。
   **band計算も72,745,351 nodesで、MS=1<<24 seedrun（76,903,818）の0.9459**:
   MS=1<<24では探索中にも64-slot窓飽和が発生して~3.5M memoエントリを喪失し
   （最終占有率10,526,730=load 0.627 vs 1<<25の14,073,139=0.419）再展開の余分を払っていた。
   per-bitはbit 95を除き全て1<<25が安い（比率0.878-0.986）。bit 95は両MSで11,857,737 nodes
   （比率ちょうど1.0）でmemo-state-invariant rootの3度目の独立確認。
6. **設計規則**: N-way merge seedはMS=1<<25（初期負荷<=~0.15）に播種する。
   MS=1<<24はS<=~4.1M keysまでしか0.1% gateを許容せず、仮にseedが通ってもband実行が~5%高コスト。
   「失敗率<0.1% at MS=1<<24」ではなくseed負荷とkneeの距離でgateを評価する。

勝敗変更なし・11×11はUNKNOWN。

## hybrid seed union測定（2026-11-17追記3・測定のみ）

出版hybrid seed union設計（DESIGN_DERIVED_NOT_MEASURED・blob 8ec64f21）を実測へ転換した
（run A `measure_hybrid_seed_union_73k_20261117.py`・run B独立実装
`measure_hybrid_seed_union_73k_independent_20261117.py`・run A JSON
`hybrid-seed-union-73k-20261117.json`・run B JSON
`hybrid-seed-union-measurement-73k-20261117.json`・独立検証JSON
`hybrid-seed-union-independent-verification-73k-20261117.json`・log
`2026-11-17-n11-class2-lane-hybrid-seed-union-measurement-73k.md`）:

1. **262レコード再構成**: only-in-2way 262レコード（13,356 bytes・
   md5 1d97a0d2167506168faae5f3898ff952・sha256 8195de51…）を決定的再抽出
   （再抽出byte同一）。
2. **hybrid seed**: 境界保存FINAL4 seed（4,975,265 key・md5 35ccec0e…）の
   byte-prefixに262レコードを追記した4,975,527 key・253,874,013 bytes・
   単一KYOENWM2ヘッダー（md5 d24198ea37b31ffbd85ead4ba230560b・
   sha256 c4f76b07…・出版FINAL4 seedとbyte-prefix同一・FINAL4部分は
   キー厳密昇順・追記分ちょうど13,356 bytes）。初期負荷0.1482822597026825
   （MS=1<<25）は設計予測と最後の桁まで一致。
3. **sim予測**: MS=1<<24→14,657失敗（境界FINAL4 anchorと同一・設計上界
   14,919内・追記レコードは失敗を1件も増やさない）・MS=1<<25→20・
   MS=1<<26→0。
4. **MS=1<<25全band実行**: seeded 4,975,527 / inserted 4,975,507 /
   **failed 20 == sim予測**（0.00040%・<0.1% gateを2桁の余裕で合格）・
   **証明書22/22 byte同一**・**72,761,010 nodes**・最終占有率14,065,965
   （負荷0.419）。node-balanced seedrun25（72,745,351）比1.00022
   （262レコードの非閉包補償は測定済み最安seed比+0.022%）、境界FINAL4
   seedrun24（76,599,320）比0.9499、出版2-way seedrun24（85,747,496）比
   0.8485。bit95は11,857,737 nodesで再度完全不変（4度目の独立確認）。
5. **record恒等式**: present 4,975,507・missing==failed 20・値違反0で閉包。
   **連結seedの落とし穴（新規・実験事実）**: hybrid seedはFINAL4整列prefix+
   非整列262レコードtailの連結で、単一sort merge joinはtailを誤読して
   missing 282（=真の20+tail 262）を出す。run Aはseedレコードをsort後に
   外部mergeで修正（アーカイブ済みrun1 JSONは最終JSONとbyte同一・
   md5 9da5ccc8…）、run Bは当初からprefix merge join（present 4,975,245・
   missing 20）+tail hash join（present 262・missing 0）で設計。
   今後の連結seedのrecord恒等式gateは非整列tailを考慮すること。
6. **実行と検証の経緯**: 測定は2つの独立実装orchestrator（824行/957行）で
   2回独立に完走し全成果物がbyte同一（run Bは出版境界seedrun24もin-run
   anchorとして再現・76,599,320 nodes・14,657失敗・22/22 byte同一）。
   claim保持セッションの自runは6 worker全て出版値byte同一で完了後、
   sleep 300のpollingコマンドが環境の300秒上限に抵触して環境リセットで
   workspaceを喪失（実験事実として記録）。同セッションが事後検証として
   ファイルhash・tail byte同一・証明書22/22（分割出版証明書連結比較）・
   record恒等式の独自再実装（seed全件sort+streaming mergeで
   present 4,975,507・missing 20・違反0・missingリスト一致）・per-bit総和・
   run間完全一致を確認して本測定をclaimとして出版した。

勝敗変更なし・manifest行は閉じず・証明書bytes不変・11×11はUNKNOWN。

## 8-way worker分割の測定（2026-11-17追記4・測定のみ）

K0909 resume item（8-worker拡張・先頭bit逆行ペナルティの構造性・MS=1<<25設計点でのseed失敗再評価）を測定した
（`measure_worker_split8_memo_merge_73k_20261117.py`・測定JSON 15/15 gate合格・
独立log `2026-11-17-n11-class2-lane-worker-split8-memo-merge-73k.md`・
claim `worker-split8-memo-merge-measurement-claim-73k-20261117.json`・
計算前にclaimをb8c76a4dで先行取得・並走hybrid測定（1299412a/e0c13af3）とは別アイテムで重複なし）:

1. **分割設計**: band ms23のper-bitノード数に対する連続DP min-max分割で22 bitを8 worker化
   （V1=0,7,11・V2=15,35・V3=39,41,44,58・V4=62,73,76・V5=87,89,94・V6=95,97・V7=98,103,105・V8=112,117・各MS=1<<23・band内共有）。
   V1はband ms23プレフィックスとper-bit完全一致（12,253,371 nodes・最終占有率1,882,289==BAND23_OCC[11]）。
   他7 workerの先頭bit（15,39,62,87,95,98,112）は全て出版fresh per-bit anchorと完全一致（gate）。
2. **worker合計110,639,931 nodes**（band ms23 121,186,659の0.9130・出版2-way 119,962,147の0.9223・
   ノード均衡4-way 112,741,501の0.9814・境界保存4-way 111,953,183の0.9883）で、
   2→4→8の分割数拡大が全出版構成で単調に安いことを確認（改善は逓減: 2-way→nb4で−6.0%・nb4→8-wayで−1.9%）。
   証明書22/22 byte同一（V1..V8各3/2/4/3/3/2/3/2）。
3. **先頭bit逆行ペナルティはN=8では構造的でない**: 先頭bitのfresh/carriedノード比は
   V2 0.9937・V3 1.0362（唯一の逆行・bit39）・V4 0.7903・V5 0.8171・V6 1.0（bit95・memo-state-invariant）・
   V7 0.8788・V8 0.7731で、大半の先頭bitはband-carriedよりむしろ安い
   （fresh23合計がband23合計より小さいことと整合）。境界保存4-wayのbit41 +5.6%は普遍則ではない。
4. **8-way heapq merge-join**: distinct合計7,914,609・occupied_after **5,243,408**
   （出版2-way seed比+22.2%・nb4 seed比+5.2%・union増大は逓減: 2→4-way +16.2%・4→8-way +5.2%）・
   shared 1,980,110・incidence {1:3,263,298, 2:1,422,024, 3:441,397, 4:101,479, 5:14,142, 6:1,030, 7:38, 8:0}
   （全8 workerが同時にmemo化したキーは存在しない）・内部衝突0・cross衝突0・merge決定的（2回実行でbyte同一）・
   seed8 md5 `8d07cd7b82a3befc07cc775ea883e2e0`。
5. **sim MS掃引（seed8）**: 1<<24→39,409失敗（0.7516%・load 0.3102・失敗はown-cluster 7,019+spill-over 32,390・
   最大cluster 130 key・>=64-key base 563）でknee曲線の第3点
   4.29M→1,448・4.99M→16,137・5.24M→39,409を加え超線形性を確認。
   1<<25→383（0.0073%・load 0.1563で0.15設計線を僅かに超えるがkneeはMSと共に動き失敗率は2桁の余裕）・
   1<<26→0（load 0.0781・>=64-key baseなし）。
6. **MS=1<<25 seedrun（fsync強化dump・cap 200）**: seeded 5,243,408 / inserted 5,243,025 /
   **failed 383 == sim予測383**（0.0073%<0.1% gate）・証明書22/22 byte同一・
   record恒等式閉包（present 5,243,025・missing==383・値違反0）・**70,538,916 nodes**
   （nb4 seedrun25 72,745,351の0.9697・nb4 seedrun24 76,903,818の0.9172・
   並走出版hybrid seedrun25 72,761,010の0.9695）・最終占有率14,053,298（load 0.4188）・
   bit95は11,857,737 nodesで5度目の完全不変確認。大きい8-way union seedほどband実行が安いという
   濃度とコストの関係がN=8まで成立し、このバンドの測定済み最安band構成となった
   （sim==engine一致は設計較正点（4.99M）の1つ外側まで拡張）。

勝敗変更なし・manifest行は閉じず・証明書bytes不変・11×11はUNKNOWN。

## fixBエンジンでのworker分割memo merge測定（2026-11-17追記5・測定のみ）

K0907の両バグ修正エンジンfixB（測定専用variant・repo-verbatim extractorはrepo上未修正）をK0909の出版2-way構成（73/76境界・MS=1<<23・band内共有）で測定した（`measure_worker_split_fixb_memo_merge_73k_20261117.py`・測定JSON `fixb-worker-split-memo-merge-73k-20261117.json`・log `2026-11-17-n11-class2-lane-fixb-worker-split-memo-merge-73k.md`・claim dcfdcb25・並走8-way/hybrid測定とは別軸）:

1. **fixB band ms23単一プロセス（初のfixBバンド全体測定）**: 28,620,380 nodes・最終占有率5,028,453・証明書22/22 byte同一（verbatim band ms23 121,186,659の0.2362・fixB fresh battery 28,290,025の1.011）。
2. **2-way workers**: A 11,662,998 + B 16,174,401 = **27,837,399 nodes**（fixB band23比0.9726・**出版verbatim 2-way 119,962,147比0.2321**・fixB fresh battery比0.9840）。workerAはfixB band23プレフィックスとper-bit完全一致（占有率3,159,518も一致）。
3. **重複キーcensus**: 両worker・band23・両seedrun dump・band24 dumpのすべてでrecords == distinct（dup_keys=0・max_copies=1）で、K0907 bug A機構（符号キー重複挿入）のバンド全体での消滅を定量確認。live bound被覆はnowin 11-12%・nolose 39-40%・win_and_lose=0・all_unbound=0。
4. **live bound merge**: shared 1,332,283・occupied_after **5,479,157**（出版verbatim 2-way merge 4,291,899の1.277倍）・内部衝突0・cross衝突0・決定的（md5 c5941251…）。verbatimの負境界は常に死哨255でcross衝突が構造的に不可能だったため、**liveなnowin/nolose境界を持つ表の自然mergeとしては衝突検出器が初めて実動作し**矛盾0だった（追記のfault注入実証の自然対応物）。
5. **merge seed MS=1<<24 seedrun**: 7,947,885 nodes（未seed fixB band ms24 21,697,814の0.366）・seed失敗24,253件（0.443%）== sim予測と完全一致（own-cluster 2,068+spill-over 22,185・max cluster 94・bases>=64 308）。出版knee設計（MS=1<<24で0.1% gate境界はS約4.1-4.2M keys）どおりの超線形失敗で0.1%事前gateは不成立・record恒等式は閉包（present==inserted 5,454,904・missing==failed・違反0）・22/22 byte同一。
6. **設計点 MS=1<<25 seedrun**: **6,005,236 nodes**・seed失敗19件 == sim予測19（3.5e-6）・record恒等式閉包・22/22 byte同一・占有率5,798,302（load 0.173）・design gates全合格。未seed band24比0.2768・fixB fresh battery比0.2123・**出版verbatim最良の8-way seedrun25 70,538,916比0.0852（11.7倍）**で、エンジン軸を横断したこのバンドの測定済み最安band実行。
7. **merge非閉包はfixBでも存続**: band表 vs merged表でshared 5,027,776・only_in_band 677・only_in_merged 451,381・共有キー値矛盾0。coordinatorはmerge表を近似として扱うべきという結論（追記）は修正エンジンでも変わらない。

勝敗変更なし・manifest行は閉じず・証明書bytes不変・repo-verbatim extractorはrepo上未修正・fixBの本番採用は別レーン判断・11×11はUNKNOWN。

## 16-way worker分割の測定（2026-11-17追記6・測定のみ・worker数の限界測定）

K0909 resume item（16-way拡張: 0.0073%損失水準のままunionがさらに増えるか・worker数の限界）を測定した
（`measure_worker_split16_memo_merge_73k_20261117.py`・測定JSON 15/15 gate合格・
独立log `2026-11-17-n11-class2-lane-worker-split16-memo-merge-73k.md`・
claim `class2-lane-worker-split16-merge-73k-claim-20261117.json`・
計算前にclaimをc3d9c918で先行取得・並走fixB 8-way claim（7dca832c）・cost78c掃引claimとは非重複）:

1. **分割設計**: band ms23のper-bitノード数に対する連続DP min-max 16分割（min-max群重量 11,857,737 = bit95単独）で
   22 bitを16 worker化（10単独bit worker＋6個の2-bit worker: V1=[0]・V2=[7,11]・V3=[15]・V4=[35,39]・V5=[41,44]・
   V6=[58,62]・V7=[73]・V8=[76]・V9=[87]・V10=[89]・V11=[94]・V12=[95]・V13=[97,98]・V14=[103]・V15=[105,112]・V16=[117]・
   各MS=1<<23・band内共有）。V1はband ms23プレフィックスとper-bit完全一致（4,303,203 nodes・最終占有率710,449==BAND23_OCC[0]）。
   他15 workerの先頭bit（7,15,35,41,58,73,76,87,89,94,95,97,103,105,117）は全て出版fresh per-bit anchorと完全一致（gate）。
2. **worker合計108,802,603 nodes**（band ms23 121,186,659の0.8978・出版2-way 119,962,147の0.9070・
   nb4 112,741,501の0.9651・境界4-way 111,953,183の0.9719・**8-way 110,639,931の0.9834〔−1.7%〕**）で
   2→4→8→16の単調改善が継続するが、**fresh ms23電池108,499,241の1.0028倍（+0.28%）に到達**し、
   分割によるworker計算の削減はfresh床にほぼ収束した。証明書22/22 byte同一（10×1＋6×2）。
3. **先頭bit逆行の局在確定**: 先頭bit fresh/carried比は13/15が1未満（0.7474–0.9937）・bit95はちょうど1.0で、
   唯一の逆行はbit41の+5.6%。8-wayの逆行bit39（+3.6%）と併せ、fresh anchorがband-carriedを上回るbitは
   39/41に局在し、逆行ペナルティはN非依存のbit特有現象と特定された。
4. **2-bit workerの第2bitはfresh値の±1.3%内**（bit11 +0.37%・bit39 +1.01%・bit44 +0.16%・bit98 −0.47%・bit112 +1.31%。
   例外はbit62の+12.8%〔worker内carry 1,998,613 vs fresh 1,771,346〕だがband-carried 2,241,220比では−10.8%）。
   2-bit worker内のcross-bit memo再利用はほぼ効かず、**N-way分割の利得の本体は高負荷単一テーブルの後半bit汚染回避**である
   （band-carriedがfreshより高コストなbitでworker内carryが両者の中間に落ちる観察と整合）。
5. **16-way heapq merge-join**: distinct合計8,375,088（records 20,072,127・dup_keys 1,346,833はverbatim符号キー重複のまま）・
   **occupied_after 5,404,082**（出版2-way seed比+25.9%・nb4比+8.4%・境界4-way比+8.6%・8-way比+3.1%で
   union増大は逓減継続: 2→4-way +16.2%・4→8-way +5.2%・8→16-way +3.1%）・shared 2,137,777・
   incidence {1:3,266,305, 2:1,493,134, 3:486,611, 4:130,721, 5:24,296, 6:2,794, 7:214, **8:7**, 9..16:0}
   （incidence 8のキーが初出現〔7 key〕・全16 worker同時memo化キーは存在せず）・内部衝突0・cross衝突0・
   merge決定的（2回実行でbyte同一）・seed16 md5 `9a29784dae371569a6a012ba68ab4886`。
6. **sim MS掃引（seed16・5,404,082 keys）**: 1<<24→70,175失敗（1.2986%・load 0.3179・own-cluster 17,872+spill-over 52,303・
   最大cluster 161 keys・8-way seed系knee曲線〔4.29M→1,448・4.99M→16,137・5.24M→39,409〕に16-way seedの
   第4点5.40M→70,175を追加し超線形性を確認）・1<<25→2,285（0.0423%・load 0.1610・own 714+spill 1,571・
   8-way 383の約6倍・<0.1% gateは2.4倍余裕で合格）・**1<<26→8失敗（0ではない）**。
   8-way seedは1<<26で0失敗だったため、**seedサイズがkneeを超えると1<<26でもclean容量を失うことを初実測**した
   （失敗はspill-overのみ・>=64-key baseは0）。
7. **MS=1<<25 seedrun（fsync強化dump・cap 200）**: seeded 5,404,082 / inserted 5,401,797 /
   **failed 2,285 == sim予測2,285**・証明書22/22 byte同一・record恒等式閉包（present 5,401,797・missing==2,285・値違反0）・
   **68,006,820 nodes**（8-way seedrun25 70,538,916の0.9641〔−3.6%〕・並走hybrid 72,761,010の0.9347・
   nb4 seedrun25 72,745,351の0.9349）・最終占有率14,004,499（load 0.4174）・bit95は11,857,737 nodesで6度目の完全不変確認。
   **大きいunion seedほどband実行が安いという濃度とコストの関係はN=16でも成立し、
   このバンドのverbatim軸の測定済み最安band構成を更新した**。
8. **worker数の限界（本測定のまとめ）**: N=16で(a) worker計算コストはfresh床+0.28%に収束し分割の計算利得はほぼ枯渇、
   (b) unionの増大は+3.1%に逓減しband実行の削減も−3.6%に逓減、(c) 一方でseed挿入失敗率はMS=1<<25設計点で
   超線形に増加し（28→383→2,285）1<<26のclean容量は既に喪失（8失敗）。よってこのバンド（22 bit・union ~5.4M keys）では
   **N=16がMS=1<<25設計点で実用的な最終段階**に近く、それを超える細分割（N=22完全fresh化等）は
   seed容量設計の再設計（MS=1<<26のengine実行は本環境のcgroupでは不可〔typed arrays 1.34GB〕のため
   seed truncationかgateの再設定）を要する。「worker数はseed負荷とkneeの距離で評価する」という追記2の設計規則の
   適用範囲がN=16まで拡張された。

勝敗変更なし・manifest行は1行も閉じず・証明書bytes不変・repo-verbatim extractorはrepo上未修正・11×11はUNKNOWN。

## fixBエンジンでの8-way worker分割memo merge測定（2026-11-17追記7・測定のみ）

fixBでの2-way測定（追記5）を出版verbatim 8-way構成（追記4）に対応する8-worker構成に拡張した（`measure_worker_split8_fixb_memo_merge_73k_20261117.py`・測定JSON `fixb-worker-split8-memo-merge-73k-20261117.json`・log `2026-11-17-n11-class2-lane-fixb-worker-split8-memo-merge-73k.md`・claim 7dca832c）。22 band bitをfixB band ms23 per-bitノード数のDP min-max（min-max値4,168,242）で連続8分割し、V1=band23プレフィックスアンカー、他7 workerはfreshプロセス・MS=1<<23・band内共有。orchestratorは出版fixB 2-wayモジュールをimportlibで再利用し新規実装は8-way merge-joinのみ。並走verbatim 16-way・cost78c claimとは別軸:

1. **8-way workers**: 合計**27,878,487 nodes**（v1 3,679,556 + v2 4,572,322 + v3 4,612,979 + v4 2,844,107 + v5 2,126,338 + v6 4,090,605 + v7 4,067,668 + v8 1,884,912）。fixB band23比0.9741・**fixB 2-way 27,837,399比1.0015**・verbatim 8-way比0.2520。**fixBでは8-way細分割のworker利得が消滅する**（verbatimでは8-wayは2-way比0.9223で利得があった）。K0907 bug A/Bが後半bit汚染を介した分割利得の主因だったことを裏付ける。V1はper-bit・占有率ともband23プレフィックスと完全一致、V2〜V8先頭bitはfixB fresh battery anchorと完全一致、全worker証明書byte同一。
2. **重複キーcensus**: 8 dumpすべてでrecords == distinct（dup_keys=0・max_copies=1）。live bound被覆はnowin 11-12%・nolose 39-40%・win_and_lose=0・all_unbound=0。
3. **live bound 8-way merge**: shared 2,270,338・occupied_after **5,773,620**（fixB 2-way 5,479,157の1.0537倍）・incidence {1: 3,503,282, 2: 1,672,101, 3: 493,437, 4: 95,044, 5: 9,342, 6: 409, 7: 5, **8: 0**}（全8 worker共有キーは存在しない）・内部/cross衝突0・決定的（md5 aa1adb87…、2回実行で同一）。
4. **sim MS掃引**: 1<<24→151,445（2.623%・load 0.3351）・1<<25→10,842（0.1878%・load 0.1717）・1<<26→92（1.59e-5・load 0.0860）。
5. **設計点 MS=1<<25 seedrun**: **5,235,505 nodes**・seed失敗10,842 == sim予測完全一致・record恒等式閉包（present 5,762,778 == inserted・missing == failed・違反0）・証明書22/22 byte同一・占有率5,853,231。fixB 2-way seedrun25 6,005,236比**0.872**・**verbatim最良8-way seedrun25 70,538,916比0.0742 = 13.5倍安い**でエンジン・分割構成横断の測定済み最安band実行（追記5の記録を更新）。sim==engine完全一致は5.77M-key seed領域まで拡張。0.1%事前gate不成立（0.1878%）は出版knee設計のとおりで、正しい設計点はMS=1<<26（sim予測92失敗・engineはcgroup内で1<<26不可のためsimが担う、は出版済み記述どおり）。失敗は性能のみで健全性に無影響。
6. **band表 vs 8-way merged表**: shared 5,028,405・only_in_band **48**（2-wayの677から縮小・band表の0.00095%）・only_in_merged 745,215（2-wayの451,381の1.65倍）・共有キー値矛盾0。8-way unionはband表を実質覆いつつ745,215 keysの新規領域を加える。merge表はband表のsupersetではないという結論（追記4・5）はN=8でも修正されない。

**解釈**: fixBでは「worker合計は2-way比1.0015で増えないが、unionは+5.4%拡大しseedrun25は0.872に下がる」という非自明なトレードオフが成立する。細分割はworkerコスト削減ではなくseed充実（union拡大）の手段として機能し、seedrun段階で回収される。coordinator設計では、worker数の選択はseed容量とkneeの距離とセットで評価すべきである。

**再現実験の記録**: 本測定は同一セッション内で2回完全実行された。1回目は全gate検証まで完走した後、出版push直前の実行環境リセットでworkdir・成果物・出版編集を喪失した。入力をrepoのpin済み blobから再構築（extractor 52bcaf50・driver 2a95d952・legal 8e97082c・manifest 0892aed0すべてblob同一を再検証）して2回目を完全実行し、workers・merge・sim・seedrun25・record恒等式・band_vs_merged8の全数値が1回目の記録値と完全一致した。出版されたscript・JSONは2回目の実行によるものであり、同時に環境リセットを跨ぐ決定性の実証例となる（全アームの決定的実行・証明書byte同一・gate同一）。

勝敗変更なし・manifest行は閉じず・証明書bytes不変・repo-verbatim extractorはrepo上未修正・fixBの本番採用は別レーン判断・11×11はUNKNOWN。
