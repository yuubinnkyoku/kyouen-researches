---
id: K0898
title: 3枝REMO決定性のr=12境界 — 定理I r=12（非坍縮キーはr=9/r=10/r=11と完全同一の7族34個・新規0・STASIS4: 4列連続決定性分類不動点＋全ラベル不動点（r=11↔r=12でdetフラグ・生存者mask・第1敗者mask全て差0・新種）・FATE56 3列連続無事象・剰余算術r=12初計数55/330/330（分割はr=10/r=11と同一））
kind: proposition
status: proved
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [three-branch REMO r=12 boundary]
relations:
- type: depends_on
  target: K0897
  note: r=11境界の次のstep。STASIS4チェックでK0897出版packed記録（15863レコード）とr=12記録のdeterminedフラグ・生存者mask・第1敗者maskが全プロファイル一致（0/0/0差分・全ラベル不動点）・34キー境界集合・per-key分割・生存者構造の完全同一を直接検証
- type: depends_on
  target: K0895
  note: r=10境界。r=10 packed記録もSTASIS4で読み4列detフラグ一致（差0）を検証
- type: depends_on
  target: K0893
  note: r=9境界。r=9 packed記録もSTASIS4で読み4連続列（r=9..12）のdeterminedフラグ一致（差0）を検証
- type: depends_on
  target: K0864
  note: r依存境界のr=12拡張。補題FL（全称）のr=12冗長アンカー
- type: depends_on
  target: K0862
  note: 同一cap≤10領域（15863プロファイル・715キー・Burnside 15863）
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりプロファイルverdictは実現盤面すべてに移る
- type: depends_on
  target: K0859
  note: Δ=0プロファイル728個が定理D再帰のr=12列（検証器内verbatim計算・出版表84エントリはr=2..8で一致確認）
- type: depends_on
  target: K0872
  note: 剰余類計数のr=12初計数（単一55・二重330・三重330・純算術・分割はr=10/r=11と同一）。r=12>最大枝サイズ10のためwraparound無し・単一剰余キーは全等トリプルちょうど（一般にr>最大枝サイズなら分割不変は純算術の帰結でr≥13でも演繹可能・cap≤10領域の剰余計数は以後自明化）。「非坍縮⇒2剰余」の初反例(6,8,9)×γ=0..3がr=12でも3剰余mixedとして4列目も存続
- type: depends_on
  target: K0874
  note: 失敗族状態行列52キーのr=12列。r=3..10出版失敗56キーのr=12運命（FATE56）を確定、4/10族8キーがr=12でも一様非決定（一度もmixedにならず）を確認
artifacts:
- path: research/experiments/remo-k-branch-cap10-r12-boundary-20261117/report.md
  role: proof
  note: 定理I r=12（r=9/r=10/r=11と完全同一の34キー）・STASIS4（4列detフラグ不動点＋全ラベル不動点・段階的ラベル収束の説明）・FATE56（34存続/22一様非決定・3列連続無事象）・剰余算術r=12初計数・FL12/G-prime12/D0アンカー・限界の説明
- path: research/experiments/remo-k-branch-cap10-r12-boundary-20261117/verify_remo_k_branch_cap10_r12_boundary.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ。11機械チェック全合格・2回実行で監査JSON byte同一。live checks（cap≤7全域2048のverbatim==twin==JS・strideサンプル496・34 witness群+56 FATEキー158突合）
- path: research/experiments/remo-k-branch-cap10-r12-boundary-20261117/mask_engine_fast_r12.js
  role: solver
  note: K0893出版修正版エンジン（pack符号シフトのr一般化・K0895/K0897版と同一バイナリ・CLI引数でr指定）のbyte同一コピー
- path: research/experiments/remo-k-branch-cap10-r12-boundary-20261117/pack_records_r12.py
  role: solver
  note: full→packed出版形式の決定的パッキングscript
- path: research/experiments/remo-k-branch-cap10-r12-boundary-20261117/output/js_cap10_r12.packed.jsonl
  role: data
  note: r=12完全スイープのpacked記録15863レコード（[i, sv_mask, fl_mask, states]・atomsは正準列挙のiの純関数・326,021 bytes・sha256 0835a06fe3a2cc812b5434ef0d56146f72b2b019b144ed62544d437472c05274）。FL違反0
- path: research/experiments/remo-k-branch-cap10-r12-boundary-20261117/output/remo_k_branch_cap10_r12_boundary_audit.json
  role: data
  note: 監査JSON（sha256 249ec902ba56bee625a87b939655ad23c989d0c47bc54649e6de7314d717cea4）。検証器run()がcommitted fileとコールド再生成のbyte照合を行う
scope: '極大安全集合がちょうど3個の点族（3枝合成族）のREMOについて、枝サイズがすべて10以下の場合（K0862/K0864/K0866/K0893/K0895/K0897と同一の15863正規形プロファイル・715キー領域）に、r=12では決定性が(sizes,gamma)に坍縮しないキーがr=9/r=10/r=11境界と同一の(6,6,8),(6,8,8)×gamma=0..4・(8,8,9),(8,9,9)×gamma=0..5・(6,6,9),(6,8,9),(6,9,9)×gamma=0..3の7族34個ちょうどであること、34キーすべてで決定側生存者が一様P_5=チェーン値であること、非決定側可能生存者集合・per-key分割計数がr=11出版表と完全同一であること、r=9..11でmixedだった34キーすべてがr=12でもmixed存続しr=3..10出版失敗56キーのうち22キー（小枝族・4/8族・4/9族）がr=12でも一様非決定（チェーンverdict・チェーン生存者ラベルも不変）であること、K0897出版r=11 packed記録とr=12記録が全15863プロファイルでdeterminedフラグ・生存者mask・第1敗者maskの3つすべてで一致（0/0/0差分・全ラベル不動点）し、K0895出版r=10 packed記録およびK0893出版r=9 packed記録ともdeterminedフラグが全プロファイル一致すること（4列連続の決定性分類不動点）、剰余類計数が55/330/330でr=10/r=11と同一分割・単一剰余55キーが全等トリプルちょうどであること、mixed剰余対が{6,8},{6,9},{8,9},{6,8,9}であること、補題FL違反0・定理G-prime r=12拡張・Δ=0プロファイル728個の定理D一致を完全列挙により確定する（定理E-prime経由で任意の実現盤面に全称的に及ぶ）。枝サイズ11,12×r=9..12、r≥13、順位決定性、STASIS/FATE/活動窓の一般則（r≥9で境界が定常という全称主張を含む・全ラベル不動点のr≥13での継続）は含まない'
evidence: '定理I r=12は有限パラメータ領域の完全計算による証明: 15863正規形プロファイルをr=12で完全スイープ（予算スキップ0・476秒・max_states 666,030。JS maskエンジン mask_engine_fast_r12.js・K0893修正版のbyte同一コピー。packed記録15863レコードを出版し検証器がインデックス整合・atoms==正準列挙・形式を検証）、(sizes,gamma)キーごとの均一性を機械判定。34キーのr=9/r=10/r=11との完全一致・FATE56（34存続/22一様非決定）・剰余計数55/330/330・witness（det/ndet atoms）はすべて検証器のピン付き定数として再導入され監査出力に記録（sha256 249ec902ba56bee625a87b939655ad23c989d0c47bc54649e6de7314d717cea4・2回実行byte同一）。STASIS4はK0897出版r=11 packed記録（repo内commit済み・sha256 08324c19…）とのdeterminedフラグ・生存者mask・第1敗者mask全プロファイル照合で0/0/0差分、K0895 r=10 packed記録（fa1e1a40…）およびK0893 r=9 packed記録（a2bb16bc…）とのdeterminedフラグ照合で差0を検証器が直接確認。live checkとしてcap≤7全域2048判定でverbatimエンジン==Python mask twin==committed JS記録（verdict・状態数）、stride 32層化サンプル496判定、34キーwitness群と56 FATEキーのチェーンをverbatim再実行（158判定をcommitted JS記録と突合）。補題FLはK0864で全称証明済み（r=12は冗長アンカー）。非坍縮キー列挙は有限範囲（C_i≤10・r=12）の完全計算であり、範囲外への全称昇格（r≥9で境界が定常等）はしない'
---

# 3枝REMO決定性のr=12境界

## 命題・範囲

K0897が「r≥12は未走査」と残した点を埋め、失敗族のr依存の観察を
さらに1列蓄積する。

- **定理I r=12（34キーちょうど・7族・r=9/r=10/r=11と完全同一）**:
  非坍縮はr=9（K0893）・r=10（K0895）・r=11（K0897）境界と同一の
  7族34個で、新規0・坍縮0・復活0（4列連続同一）:
  (6,6,8),(6,8,8)×γ=0..4・(8,8,9),(8,9,9)×γ=0..5・
  (6,6,9),(6,8,9),(6,9,9)×γ=0..3。34キーすべてで決定側生存者は
  一様P_5（=チェーン値・定理G′ r=12拡張・不一致0）。非決定側
  可能生存者集合は{3,4,5},{3,5},{3,5,7},{3,4,5,7},{3,4,5,6,7}内、
  per-key分割計数も34キーすべてでr=11出版表と完全同一。センサスは
  一様決定98・一様非決定583・mixed 34（キー数はr=9..11と同一）。
  max_states 666,030。Δ=0プロファイル728個は定理Dのr=12列に全一致。
  補題FL違反0（K0864全称証明の冗長アンカー）。
- **STASIS4（4列不動点＋全ラベル不動点・新種の観察）**: K0897
  出版のr=11 packed記録とr=12記録は全15,863プロファイルで
  determinedフラグ・生存者mask・**第1敗者maskの3つ全てが完全一致
  （0/0/0差分）**。r=10↔r=11では7,328件動いていた第1敗者ラベルが
  r=11↔r=12で初めて固定された**全ラベル不動点**で、K0897の生存者
  mask不動点より真に強い（生存者ラベルはr=10→r=11で、第1敗者
  ラベルはr=11→r=12で固定という段階的収束）。K0895 r=10・K0893
  r=9記録を含めると4連続列（r=9,10,11,12）で決定性分類が完全不変
  （有限観察・一般則ではない）。
- **FATE56（3列連続無事象）**: r=9..11でmixedだった34キー（6/8族10・
  8/9族12・6/9族12）はr=12でもmixedのまま存続（4列連続存続）。
  r≤8失敗でr=9に坍縮済みの22キー（小枝族10・4/8族6・4/9族6）は
  r=12でも一様非決定（チェーンverdictもチェーン生存者ラベルも
  r=10/r=11と不変）。新規族0・復活0・一様決定化0: FATE系列で3列
  連続の「何も起こらない」列。活動窓はr=10値のまま（有限観察）。
- **剰余算術（r=12の新算術列）**: 715キーの剰余類計数は単一55・
  二重330・三重330でr=10/r=11と完全同一の分割（本項が初計数・
  純算術）。r=12は最大枝サイズ10を超えるためmodular wraparoundが
  存在せず、単一剰余キーは全等トリプルちょうど。一般にr>最大枝
  サイズなら剰余類計数はサイズ列の線形構造のみで決まるため、
  r≥13でもこの分割は不変（純算術の帰結・cap≤10領域の剰余計数は
  以後自明化）。mixedキーの剰余対は{6,8},{6,9},{8,9}と3剰余
  {6,8,9}（(6,8,9)×γ=0..3）で、K0893の「非坍縮⇒2剰余」初反例は
  4列目も存続。
- **4/10族（K0874候補族）**: 8キーはr=12でも一様非決定
  （r=2..12で一度もmixedにならず・有限観察）。
- **FL12/G-prime12/D0**: 補題FL違反0。定理G′ r=12拡張: 一様決定98
  キーすべて生存者=チェーン（不一致0）。Δ=0プロファイル728個は
  定理Dのr=12列に一致。

## 限界

- 枝サイズ11,12×r=9..12は未走査（K0881のcap≤12拡張はr=7,8まで）。
- r≥13は未走査。順位決定性は本項で扱わない（検証器も順位フィールド
  を再導出しない）。
- STASIS4は4列の有限観察であり「r≥9で境界が定常」という全称主張
  ではない。全ラベル不動点はr=11↔r=12の1組の観察であり、r≥13での
  継続は保証しない。
- FATE/活動窓/分割計数不変性は有限観察のまま。
- 11×11空盤・クラスフロンティアは本項と無関係でUNKNOWNのまま。

## 再現

`verify_remo_k_branch_cap10_r12_boundary.py`（自己完結・決定的・
Python 3.11+ stdlibのみ・ネットワークなし・K0897検証器の機械変換
[単独性assert付き置換]）。11機械チェック全合格・2回実行で監査
JSON byte同一（sha256 249ec902ba56bee625a87b939655ad23c989d0c47bc54649e6de7314d717cea4）。
live checks: cap≤7全域2,048判定のverbatim==Python mask twin==committed
JS記録（verdictと状態数）・stride 32層化サンプル496判定・34キーの
det/ndet/chain witnessと56 FATEキーのチェーンをverbatimエンジンで
再実行（158 witness判定をcommitted JS記録と突合）。監査JSONは
検証器run()がcommitted fileとのbyte照合を行う。K0897 r=11 packed
記録（../remo-k-branch-cap10-r11-boundary-20261117/）・K0895 r=10
packed記録（../remo-k-branch-cap10-r10-boundary-20261117/）・
K0893 r=9 packed記録（../remo-k-branch-cap10-r9-boundary-20261117/）
をSTASIS4チェックで読む（repo内commit済みファイル・ネットワーク不要）。
