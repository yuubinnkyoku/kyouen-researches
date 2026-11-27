# 2026-11-27 高速レーン: 6頂点グラフ核全型（純二点辺clutter全体）の全長34周期認証

自実行・単一オーナー。本sessionはユーザーPC到達不可（GitHub API 出版のみ・sandbox
upgraded・Python 3.12）。K0684系列の次の空白「二点辺を含む核の完全族」を攻めた。

## 選定

未解決リストとK0684の現状から、証明済み完全族（≤5点全型・6点純三点辺全型・
7点純三点辺≤5本）の外で、計算量が本sessionで完走できる唯一の完全族として
**6頂点のグラフ核（純二点辺clutter）全体**を選んだ。raw 2^15 = 32768 件は
二点辺同士が包含を持たないため全件がclutterであり、根付き同型は544型
（Burnside・canonical列挙の二重導出）。閉包は663状態（新規544 + K0682既知119）
で、新規状態は初期型そのもの（着手は必ず点数を減らすため中間状態が生じない）。
同日の並走レーン（n11 ninth-cost adoption・six-row q7 6x23・seven-row q4 w70・
(4,24,5)/(4,5) m24 class-split・z24-min19）とは全く disjoint。

## 実行と結果

- 公式 solve（`solve_graph.py`: pinned engine + K0682表再利用・7点kit
  `solve_core.py` の構造適応）: **544型全てについて L>=500 で34周期、
  jointly_certified=true、必要値1069、prefix上Grundy最大22**。
  純三点辺6点全型（最大29）より低く、稠密核（K6まで）を含む族でも
  Grundy値は押し上げられない（観測）。
- **最小最終周期は全544型でちょうど34**（窓500..1069上で1/2/17への短縮なし）。
  開始分布は71値（最小46・最頻値50・最悪500は2状態
  (6,[3,5,6,9,17,24,34,40]) / (6,[3,5,6,9,10,17,20,34,36])）。

## 検証

1. 独立第二実装（`verify_independent.py`）: engine/K0682表不使用の全再帰で
   閉包663状態を0..1069で全再計算 → 544レコード全値一致・窓一致・PASS・2走byte同一。
2. 原始第三実装（`verify_direct.py`）: 層化標本76状態×L=0..8=684比較を、
   canonical/remap/道表/再帰式なしのラベル付き直接ゲーム木で全一致。
3. 群論（`verify_enum.py`）: E1 canonical列挙544 = E2 Burnside 544 =
   E3 orbit-stabilizer Σ120/|Aut|=32768。
4. tamper電池（`verify_tamper.py`）: control PASS、T1値改変/T2 phantom/T3
   certified反転/T4窓主張改変が全部 fail-closed（rc≠0・verdict FAIL）。
5. 外部錨: 出版済み7点純三点辺≤5本監査の閉包に現れた純二点辺状態のうち
   n=6 の102状態が本公式auditと全prefix 0..1069 で完全一致
   （`output/crosscheck_seven_point.json`）。

## 正直開示

- (a) 環境reset 1回（tamper電池を1本のbashで5走しようとして300s超過）。
  workspace は消滅し、公式solve・独立検証・全電池を reset 後に最初から再実行
  した（pre-reset と post-reset で audit byte 同一を確認済み）。以後、
  長時間コマンドは分割し、作業treeは knowledge mount `_six-graph-kit/` に置いた。
- (b) 独立検証器の初版は path list を [0] で初期化したまま per-length 追加する
  index shift bug があり、自身の全値比較が fail-closed して検出・修正した。
  公式 audit は無影響（公式 solver は検証済み solve_core の path 構成の clone）。
- (c) official run は宣言より後（post-hoc）。単一実装起点の実験だが、
  上記5軸の検証で裏付けた。publish-then-execute の対抗probe形式は
  本レーンでは採用していないことを明記する。
- (d) K0684 の更新（artifacts追記・evidence追記・本文末尾に2026-11-27節）は
  items 正本のみで行い、generated の再生成は本sandboxにrepo checkoutが
  ないため実行していない（tools/knowledge/build.py は要 full checkout。
  本追記は SCHEMA 上 artifacts/evidence/本文追記のみで generated 側の
  素材は変えない）。次回の統合側で再生成を前提とする。

## 接続

- 次の完全族候補: 6点・二点辺+三点辺混在の「高々2総辺」族（2点辺を含む
  ≤2総辺の全clutter、raw約570件・閉包は7点監査の混在状態の一部と交差）は
  さらに軽量。7点グラフ核は raw 2^21 = 2M 件で根付き型数万・数時間級
  （別session向け）。二点辺混在の一般全称証明・反例は K0684 のまま OPEN。
- 標準11×11空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費・nodes は bookkeeping。
