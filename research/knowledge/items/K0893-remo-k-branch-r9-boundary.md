---
id: K0893
title: 3枝REMO決定性のr=9境界 — 定理I r=9（非坍縮キーは7族34個・6/8族の存続と8/9族の復活によるFATEパターンの破れ・初の3剰余mixed族(6,8,9)・新3族のr=2..8完全休眠とr=9覚醒）・JS maskエンジンpacked符号のr≥9非単射欠陥の修正（出版済みr≤8成果は無影響）
kind: proposition
status: proved
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [three-branch REMO r=9 boundary]
relations:
- type: depends_on
  target: K0864
  note: r依存境界のr=9拡張。補題FL（全称）のr=9冗長アンカー。エンジン欠陥はFL違反6378件として検出（K0864のFLが検出器として機能）
- type: depends_on
  target: K0862
  note: 同一cap≤10領域（15863プロファイル・715キー・Burnside 15863）。r=3小枝族を含む44前失敗キーのr=9運命（FATE44）を確定
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりプロファイルverdictは実現盤面すべてに移る
- type: depends_on
  target: K0859
  note: Δ=0プロファイル728個が定理D再帰のr=9列（検証器内verbatim計算・出版表84エントリはr=2..8で一致確認）
- type: depends_on
  target: K0866
  note: r=7境界の次のstep。4/9族のr=9一様非決定坍縮を確定
- type: depends_on
  target: K0869
  note: r=8境界の次のstep。6/8族のr=9存続（分割計数はr=8と完全同一）とFATE44の破れを確定
- type: depends_on
  target: K0872
  note: r=9算術前置き57/336/322完全一致。「非坍縮キーは全て2剰余」観察がr=9で初反例（(6,8,9)×γ=0..3の3剰余{0,6,8}）
- type: depends_on
  target: K0874
  note: 失敗族状態行列52キーのr=9列。44キーの運命をFATE44として再計算し、4/10族8キーがr=9でも一様非決定（一度もmixedにならず）を確認
artifacts:
- path: research/experiments/remo-k-branch-cap10-r9-boundary-20261117/report.md
  role: proof
  note: 定理I r=9（7族34キー・分割計数・生存者構造）・FATE44（22存続/22坍縮・初の族復活）・ECHO9（新族のr=2..8完全休眠）・剰余レンズ初反例・FL9/G′9/D0アンカー・エンジン欠陥修正の説明・限界
- path: research/experiments/remo-k-branch-cap10-r9-boundary-20261117/verify_remo_k_branch_cap10_r9_boundary.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ。11機械チェック全合格・assemble二重実行byte同一。live checks（cap≤7全域2048のverbatim==twin==JS・stride 32サンプル496・34 witness群+44 FATEチェーンverbatim再実行・146判定のJS突合）。CIコールド実行約7分
- path: research/experiments/remo-k-branch-cap10-r9-boundary-20261117/mask_engine_fast_r9.js
  role: solver
  note: K0876/K0881出版エンジンのpack符号8ビットシフトをrに一般化した修正版（r≥9でP_8第1敗者ビットがP_0生存者ビットと衝突する非単射欠陥を修正）。r≤8では復号ビット同一・K0881出版packedレコードとの回帰照合 r=2全47595件+r=7 6300件+r=8 3300件で不一致0
- path: research/experiments/remo-k-branch-cap10-r9-boundary-20261117/pack_records_r9.py
  role: solver
  note: full→packed出版形式の決定的パッキングscript
- path: research/experiments/remo-k-branch-cap10-r9-boundary-20261117/output/js_cap10_r9.packed.jsonl
  role: data
  note: r=9完全スイープのpacked記録15,863レコード（[i, sv_mask, fl_mask, states]・atomsは正準列挙のiの純関数）。修正版エンジンで生成・FL違反0
- path: research/experiments/remo-k-branch-cap10-r9-boundary-20261117/output/remo_k_branch_cap10_r9_boundary_audit.json
  role: data
  note: 監査JSON（sha256 f407faee7280a95d5674128fa4ba7c9fced8923d710a657eb16cfac0bae289d8）。検証器run()がcommitted fileとコールド再生成のbyte照合を行う
scope: '極大安全集合がちょうど3個の点族（3枝合成族）のREMOについて、枝サイズがすべて10以下の場合（K0862/K0864/K0866/K0869と同一の15863正規形プロファイル・715キー領域）に、r=9では決定性が(sizes,γ)に坍縮しないキーが(6,6,8),(6,8,8)×γ=0..4と(8,8,9),(8,9,9)×γ=0..5と(6,6,9),(6,8,9),(6,9,9)×γ=0..3の7族34個ちょうどであること、34キーすべてで決定側生存者が一様P_5=チェーン値であること、非決定側可能生存者集合が{3,4,5},{3,5},{3,5,7},{3,4,5,7},{3,4,5,6,7}内であること、r=3..8の全44出版失敗キーのうち22キー（6/8族・8/9族の全キー）がr=9でもmixedのまま存続し22キーが一様非決定へ坍縮すること、新3族12キー573プロファイルがr=2..8の全値で一様非決定かつチェーン非決定（完全休眠）であること、(6,8,9)×γ=0..3が初の3剰余mixed族であること、剰余類計数57/336/322がK0872出版前置きに一致すること、補題FL違反0・定理G′ r=9拡張・Δ=0プロファイル728個の定理D一致を完全列挙により確定する（定理E′経由で任意の実現盤面に全称的に及ぶ）。枝サイズ11,12×r=9、r≥10、順位決定性、FATE/ECHO/活動窓/剰余レンズの一般則は含まない'
evidence: '定理I r=9は有限パラメータ領域の完全計算による証明: 15863正規形プロファイルをr=9で完全スイープ（予算スキップ0。JS maskエンジン mask_engine_fast_r9.js・packed記録15,863レコードを出版、検証器がインデックス整合・atoms==正準列挙・形式を検証）し、(sizes,γ)キーごとの均一性を機械判定。34キーの分割計数・チェーン値・witness（det/ndet atoms）・44 FATEキーの運命・新族12キーのr=2..8完全休眠（573プロファイル×7r+84チェーン実行）はすべて検証器のピン付き定数として再導入され監査出力に記録（sha256 f407faee7280a95d5674128fa4ba7c9fced8923d710a657eb16cfac0bae289d8・assemble二重実行byte同一）。live checkとしてcap≤7全域2048判定でverbatimエンジン==Python mask twin==committed JS記録（verdict・状態数）、stride 32層化サンプル496判定、34キーwitness群と44 FATEチェーンのverbatim再実行（146判定をcommitted JS記録と突合）。エンジン欠陥: K0876/K0881のpacked符号 out=(svm<<8)|flm は固定8ビットシフトでr≥9で非単射（初回r=9スイープでFL違反6378件として検出）。修正版はシフトをrに一般化し、r≤8では復号がビット同一であることをK0881出版packedレコードとの回帰照合（r=2全47595・r=7 6300・r=8 3300件・(sv,fl,states)不一致0）で確認。出版済みr≤8成果は全て無影響。補題FLはK0864で全称証明済み（r=9は冗長アンカー）。非坍縮キー列挙は有限範囲（C_i≤10・r=9）の完全計算であり、範囲外への全称昇格はしない'
---

# 3枝REMO決定性のr=9境界

## 命題・範囲

K0869が「r≥9は未走査」と残した点を埋め、失敗族のr依存の観察を
さらに1段蓄積する。

- **定理I r=9（34キーちょうど・7族）**: 非坍縮は
  (6,6,8),(6,8,8)×γ=0..4・(8,8,9),(8,9,9)×γ=0..5・
  (6,6,9),(6,8,9),(6,9,9)×γ=0..3 の7族34個ちょうど。
  34キーすべてで決定側生存者は一様P_5（=チェーン値）。
  非決定側可能生存者集合は{3,4,5},{3,5},{3,5,7},{3,4,5,7},
  {3,4,5,6,7}内。センサスは一様決定98（r=7,8と同数）・
  一様非決定583・mixed 34・max_states 363,630。
- **FATE44の破れ（初の族復活・初の次r存続）**: r=3..8の出版失敗
  44キーのうち、r=8失敗族(6,6,8)/(6,8,8)はr=9でもmixedのまま存続
  （分割計数はr=8と完全同一）、r=3,4,5失敗族(8,8,9)/(8,9,9)は
  r=6,7,8の一様非決定を経てr=9で復活。r≤8で観察された
  「失敗族は次のr以降一様非決定へ坍縮」が一般則でないことを確定。
  残る22キー（小枝族10・4/8族6・4/9族6）は従来パターンどおり
  一様非決定へ坍縮。活動窓は8/9族{3,4,5,9}・6/8族{8,9}に更新。
- **ECHO9（新族の完全休眠）**: 新3族12キー573プロファイルは
  r=2..8の全値で一様非決定かつチェーン非決定でr=9に初覚醒。
  6/8族（r=2でチェーン決定）・8/9族（r=3,4,5でチェーン決定）と
  覚醒の形状が異なる（有限観察）。
- **剰余レンズの初反例**: (6,8,9)×γ=0..3は初の3剰余{0,6,8}
  mixed族。K0872の「非坍縮⇒2剰余」観察がr=9で初反例。
  剰余類計数57/336/322は出版前置きと完全一致。
  単一剰余57キーは55全等トリプル+(1,1,10)|0・(1,10,10)|0。
- **4/10族（K0874候補族）**: 8キーはr=9でも一様非決定
  （r=2..9で一度もmixedにならず・有限観察）。
- **FL9/G′9/D0**: 補題FL違反0（K0864全称証明の冗長アンカー）。
  定理G′ r=9拡張: 一様決定98キーすべて生存者=チェーン（不一致0）。
  Δ=0プロファイル728個は定理Dのr=9列に一致。

## エンジン欠陥の修正

K0876/K0881出版JS maskエンジンのpacked符号 `out=(svm<<8)|flm` は
固定8ビットシフトでr≥9では非単射: P_8の第1敗者ビット(1<<8)が
P_0の生存者ビット位置と衝突する。初回r=9スイープでFL違反6378件と
して検出。修正版 `mask_engine_fast_r9.js` はシフトをrに一般化。
r≤8では復号がビット同一（flm<2^r≤2^8とsvm<<8の占有ビットが互いに
素）で、K0881出版packedレコードとの回帰照合
（r=2全47,595・r=7 6,300・r=8 3,300件）で(sv,fl,states)不一致0を
確認。**出版済みの全r≤8成果は無影響**。

## 限界

- 枝サイズ11,12×r=9は未走査（K0881のcap≤12拡張はr=7,8まで）。
- r≥10は未走査。順位決定性は本項で扱わない。
- FATE/ECHO/活動窓/剰余レンズ/分割計数不変性は有限観察であり
  一般則へ昇格しない。
- 11×11空盤・クラスフロンティアは本項と無関係でUNKNOWNのまま。

## 再現

`verify_remo_k_branch_cap10_r9_boundary.py`（自己完結・決定的・
stdlibのみ）。11機械チェック全合格・assemble二重実行byte同一
（監査JSON sha256 f407faee7280a95d5674128fa4ba7c9fced8923d710a657eb16cfac0bae289d8）。
live checks: cap≤7全域2048判定のverbatim==twin==JS突合・
stride 32サンプル496・34 witness群+44 FATEチェーンのverbatim再実行
（146判定をcommitted JS記録と突合）。CIコールド実行約7分。
