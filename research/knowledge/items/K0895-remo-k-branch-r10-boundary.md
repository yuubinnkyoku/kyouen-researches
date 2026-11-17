---
id: K0895
title: 3枝REMO決定性のr=10境界 — 定理I r=10（非坍縮キーはr=9と完全同一の7族34個・新規0・STASIS: r=9→r=10で決定性分類が全プロファイル不動の列不動点・FATE56初の無事象列・剰余算術r=10初計数55/330/330）
kind: proposition
status: proved
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [three-branch REMO r=10 boundary]
relations:
- type: depends_on
  target: K0893
  note: r=9境界の次のstep。STASISチェックでK0893出版packed記録（15863レコード）とr=10記録のdeterminedフラグが全プロファイル一致（差0）・34キー境界集合・per-key分割・生存者構造の完全同一を直接検証
- type: depends_on
  target: K0864
  note: r依存境界のr=10拡張。補題FL（全称）のr=10冗長アンカー
- type: depends_on
  target: K0862
  note: 同一cap≤10領域（15863プロファイル・715キー・Burnside 15863）
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりプロファイルverdictは実現盤面すべてに移る
- type: depends_on
  target: K0859
  note: Δ=0プロファイル728個が定理D再帰のr=10列（検証器内verbatim計算・出版表84エントリはr=2..8で一致確認）
- type: depends_on
  target: K0872
  note: 剰余類計数のr=10初計数（単一55・二重330・三重330・純算術）。「非坍縮⇒2剰余」の初反例(6,8,9)×γ=0..3がr=10でも3剰余mixedとして存続
- type: depends_on
  target: K0874
  note: 失敗族状態行列52キーのr=10列。r=3..9出版失敗56キーのr=10運命（FATE56）を確定、4/10族8キーがr=10でも一様非決定（一度もmixedにならず）を確認
artifacts:
- path: research/experiments/remo-k-branch-cap10-r10-boundary-20261117/report.md
  role: proof
  note: 定理I r=10（r=9と完全同一の34キー）・STASIS（列不動点・差0）・FATE56（34存続/22一様非決定・初の無事象列）・剰余算術r=10初計数・FL10/G-prime10/D0アンカー・限界の説明
- path: research/experiments/remo-k-branch-cap10-r10-boundary-20261117/verify_remo_k_branch_cap10_r10_boundary.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ。11機械チェック全合格・assemble二重実行byte同一・2回目のcold実行でも監査JSON byte同一。live checks（cap≤7全域2048のverbatim==twin==JS・strideサンプル496・34 witness群+56 FATEキー158突合）
- path: research/experiments/remo-k-branch-cap10-r10-boundary-20261117/mask_engine_fast_r10.js
  role: solver
  note: K0893出版修正版エンジン（pack符号シフトのr一般化）のbyte同一コピー
- path: research/experiments/remo-k-branch-cap10-r10-boundary-20261117/pack_records_r10.py
  role: solver
  note: full→packed出版形式の決定的パッキングscript
- path: research/experiments/remo-k-branch-cap10-r10-boundary-20261117/output/js_cap10_r10.packed.jsonl
  role: data
  note: r=10完全スイープのpacked記録15863レコード（[i, sv_mask, fl_mask, states]・atomsは正準列挙のiの純関数・315,477 bytes・sha256 fa1e1a405523403611101f819aed5013b353fdf2a526d125e643b8364b072884）。FL違反0
- path: research/experiments/remo-k-branch-cap10-r10-boundary-20261117/output/remo_k_branch_cap10_r10_boundary_audit.json
  role: data
  note: 監査JSON（sha256 8b37525729eb869b2fe8eb383d10331d4249c91135b128ff08c88bd8ca022dfa）。検証器run()がcommitted fileとコールド再生成のbyte照合を行う
scope: '極大安全集合がちょうど3個の点族（3枝合成族）のREMOについて、枝サイズがすべて10以下の場合（K0862/K0864/K0866/K0893と同一の15863正規形プロファイル・715キー領域）に、r=10では決定性が(sizes,gamma)に坍縮しないキーがr=9境界と同一の(6,6,8),(6,8,8)×gamma=0..4・(8,8,9),(8,9,9)×gamma=0..5・(6,6,9),(6,8,9),(6,9,9)×gamma=0..3の7族34個ちょうどであること、34キーすべてで決定側生存者が一様P_5=チェーン値であること、非決定側可能生存者集合・per-key分割計数がr=9出版表と完全同一であること、r=9でmixedだった34キーすべてがr=10でもmixed存続しr=3..9出版失敗56キーのうち22キー（小枝族・4/8族・4/9族）がr=10でも一様非決定であること、K0893出版r=9 packed記録とr=10記録の全15863プロファイルでdeterminedフラグが一致すること、剰余類計数が55/330/330で単一剰余55キーが全等トリプルちょうどであること、mixed剰余対が{6,8},{6,9},{8,9},{6,8,9}であること、補題FL違反0・定理G-prime r=10拡張・Δ=0プロファイル728個の定理D一致を完全列挙により確定する（定理E-prime経由で任意の実現盤面に全称的に及ぶ）。枝サイズ11,12×r=9,10、r≥11、順位決定性、STASIS/FATE/活動窓/剰余レンズの一般則（r≥9で境界が定常という全称主張を含む）は含まない'
evidence: '定理I r=10は有限パラメータ領域の完全計算による証明: 15863正規形プロファイルをr=10で完全スイープ（予算スキップ0。JS maskエンジン mask_engine_fast_r10.js・K0893修正版のbyte同一コピー。packed記録15863レコードを出版し検証器がインデックス整合・atoms==正準列挙・形式を検証）、(sizes,gamma)キーごとの均一性を機械判定。34キーのr=9との完全一致・FATE56（34存続/22一様非決定）・剰余計数55/330/330・witness（det/ndet atoms）はすべて検証器のピン付き定数として再導入され監査出力に記録（sha256 8b37525729eb869b2fe8eb383d10331d4249c91135b128ff08c88bd8ca022dfa・assemble二重実行byte同一・別プロセス2回目のcold実行でも監査byte同一）。STASISはK0893出版r=9 packed記録（repo内commit済み・sha256 fa1e1a40…）とのdeterminedフラグ全プロファイル照合で差0を検証器が直接確認。live checkとしてcap≤7全域2048判定でverbatimエンジン==Python mask twin==committed JS記録（verdict・状態数）、stride 32層化サンプル496判定、34キーwitness群と56 FATEキーのチェーンをverbatim再実行（158判定をcommitted JS記録と突合）。スイープは環境リセットを挟んで2回生成され両実行の解析定数が完全一致（クロス環境決定性の非計画的確認）。補題FLはK0864で全称証明済み（r=10は冗長アンカー）。非坍縮キー列挙は有限範囲（C_i≤10・r=10）の完全計算であり、範囲外への全称昇格（r≥9で境界が定常等）はしない'
---

# 3枝REMO決定性のr=10境界

## 命題・範囲

K0893が「r≥10は未走査」と残した点を埋め、失敗族のr依存の観察を
さらに1列蓄積する。

- **定理I r=10（34キーちょうど・7族・r=9と完全同一）**: 非坍縮は
  r=9境界（K0893定理I）と同一の7族34個で、新規0・坍縮0・復活0:
  (6,6,8),(6,8,8)×γ=0..4・(8,8,9),(8,9,9)×γ=0..5・
  (6,6,9),(6,8,9),(6,9,9)×γ=0..3。34キーすべてで決定側生存者は
  一様P_5（=チェーン値・定理G′ r=10拡張・不一致0）。非決定側
  可能生存者集合は{3,4,5},{3,5},{3,5,7},{3,4,5,7},{3,4,5,6,7}内、
  per-key分割計数も34キーすべてでr=9出版表と完全同一。センサスは
  一様決定98・一様非決定583・mixed 34（キー数はr=9と同一）。
  max_states 514,830。Δ=0プロファイル728個は定理Dのr=10列に全一致。
  補題FL違反0（K0864全称証明の冗長アンカー）。
- **STASIS（列不動点・新種の観察）**: K0893出版のr=9 packed記録と
  r=10記録は全15,863プロファイルでdeterminedフラグが完全一致
  （差0）。mixed境界（キー集合・per-profile det/ndet分割・決定側
  生存者・非決定側可能生存者集合）はr=9→r=10で完全不変。
  r×サイズ格子で初めて2つの連続する列が同一の決定性分類を持つ
  （有限観察・一般則ではない）。ただし成果のラベルは固定ではない:
  生存者maskは7,328件・第1敗者maskは11,533件が列間で異なる。
- **FATE56（初の無事象列）**: r=9でmixedだった34キー（6/8族10・
  8/9族12・6/9族12）はr=10でもmixedのまま存続（2列連続存続）。
  r≤8失敗でr=9に坍縮済みの22キー（小枝族10・4/8族6・4/9族6）は
  r=10でも一様非決定（チェーンverdictも{1,5}/{3,5}で不変）。
  新規族0・復活0・一様決定化0: FATE系列で初めて「何も起こらない」
  列。活動窓は8/9族{3,4,5,9,10}・6/8族{8,9,10}・6/9族{9,10}に更新
  （小枝族{3}・4/8族{6}・4/9族{7}は不変・有限観察）。
- **剰余算術（r=10の新算術列）**: 715キーの剰余類計数は単一55・
  二重330・三重330（K0872出版はr=3..9まででr=10は本項が初計数・
  純算術）。単一剰余55キーは全等トリプルちょうど。r=9で単一剰余
  だった(1,1,10)|0・(1,10,10)|0（10≡1 mod 9）はr=10では10≡0のため
  二重剰余に移る。mixedキーの剰余対は{6,8},{6,9},{8,9}に加えて
  3剰余{6,8,9}（(6,8,9)×γ=0..3）を含み、K0893の
  「非坍縮⇒2剰余」初反例はr=10でも存続。
- **4/10族（K0874候補族）**: 8キーはr=10でも一様非決定
  （r=2..10で一度もmixedにならず・有限観察）。
- **FL10/G-prime10/D0**: 補題FL違反0。定理G′ r=10拡張: 一様決定98
  キーすべて生存者=チェーン（不一致0）。Δ=0プロファイル728個は
  定理Dのr=10列に一致。

## 限界

- 枝サイズ11,12×r=9,10は未走査（K0881のcap≤12拡張はr=7,8まで）。
- r≥11は未走査。順位決定性は本項で扱わない（検証器も順位フィールド
  を再導出しない）。
- STASISは2列の有限観察であり「r≥9で境界が定常」という全称主張
  ではない。
- FATE/活動窓/剰余レンズ/分割計数不変性は有限観察のまま。
- 11×11空盤・クラスフロンティアは本項と無関係でUNKNOWNのまま。

## 再現

`verify_remo_k_branch_cap10_r10_boundary.py`（自己完結・決定的・
Python 3.11+ stdlibのみ・ネットワークなし・K0893検証器の機械変換
[単独性assert付き置換]）。11機械チェック全合格・assemble同一入力
2回実行byte同一・別プロセス2回目のcold実行でも監査JSON byte同一
（sha256 8b37525729eb869b2fe8eb383d10331d4249c91135b128ff08c88bd8ca022dfa）。
live checks: cap≤7全域2,048判定のverbatim==Python mask twin==committed
JS記録（verdictと状態数）・stride 32層化サンプル496判定・34キーの
det/ndet/chain witnessと56 FATEキーのチェーンをverbatimエンジンで
再実行（158 witness判定をcommitted JS記録と突合）。監査JSONは
検証器run()がcommitted fileとのbyte照合を行う。K0893 r=9 packed
記録（../remo-k-branch-cap10-r9-boundary-20261117/）をSTASIS
チェックで読む（repo内commit済みファイル・ネットワーク不要）。
