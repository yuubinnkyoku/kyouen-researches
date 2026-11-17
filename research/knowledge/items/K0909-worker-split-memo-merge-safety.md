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

## 解釈ガード

測定・検証のみ。新規WIN/LOSS verdict無し・manifest行は1行も閉じない・証明書bytes不変。
repo-verbatim extractorはrepo上未修正のまま（出版決定性チェーン）。WIN7-D10は個別7石rootの
深さ10以内の先手勝ちのみを証明し、REFUTED-D10はLOSS証明ではない。
11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はいずれもUNKNOWN。
