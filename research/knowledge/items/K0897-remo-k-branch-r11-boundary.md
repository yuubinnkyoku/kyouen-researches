---
id: K0897
title: 3枝REMO決定性のr=11境界 — 定理I r=11（非坍縮キーはr=9/r=10と完全同一の7族34個・新規0・STASIS3：3列連続決定性分類不動点＋生存者mask全列不動点（r=10↔r=11で差0・新種）・FATE56 2列連続無事象・剰余算術r=11初計数55/330/330（分割はr=10と同一））
kind: proposition
status: proved
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [three-branch REMO r=11 boundary]
relations:
- type: depends_on
  target: K0895
  note: r=10境界の次のstep。STASIS3チェックでK0895出版packed記録（15863レコード）とr=11記録のdeterminedフラグが全プロファイル一致（差0）に加え生存者maskも全プロファイル一致（差0・全列ラベル不動点）・34キー境界集合・per-key分割・生存者構造の完全同一を直接検証
- type: depends_on
  target: K0893
  note: r=9境界。r=9 packed記録もSTASIS3で読み、3連続列（r=9,10,11）のdeterminedフラグ一致（差0）を検証
- type: depends_on
  target: K0864
  note: r依存境界のr=11拡張。補題FL（全称）のr=11冗長アンカー
- type: depends_on
  target: K0862
  note: 同一cap≤10領域（15863プロファイル・715キー・Burnside 15863）
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりプロファイルverdictは実現盤面すべてに移る
- type: depends_on
  target: K0859
  note: Δ=0プロファイル728個が定理D再帰のr=11列（検証器内verbatim計算・出版表84エントリはr=2..8で一致確認）
- type: depends_on
  target: K0872
  note: 剰余類計数のr=11初計数（単一55・二重330・三重330・純算術・分割はr=10と同一）。r=11>最大枝サイズ10のためwraparound無し・単一剰余キーは全等トリプルちょうど。「非坍縮⇒2剰余」の初反例(6,8,9)×γ=0..3がr=11でも3剰余mixedとして存続
- type: depends_on
  target: K0874
  note: 失敗族状態行列52キーのr=11列。r=3..10出版失敗56キーのr=11運命（FATE56）を確定、4/10族8キーがr=11でも一様非決定（一度もmixedにならず）を確認
artifacts:
- path: research/experiments/remo-k-branch-cap10-r11-boundary-20261117/report.md
  role: proof
  note: 定理I r=11（r=9/r=10と完全同一の34キー）・STASIS3（3列detフラグ不動点＋生存者mask不動点・第1敗者mask 7,328差のpin）・FATE56（34存続/22一様非決定・2列連続無事象）・剰余算術r=11初計数・FL11/G-prime11/D0アンカー・限界の説明
- path: research/experiments/remo-k-branch-cap10-r11-boundary-20261117/verify_remo_k_branch_cap10_r11_boundary.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ。11機械チェック全合格・2回実行で監査JSON byte同一。live checks（cap≤7全域2048のverbatim==twin==JS・strideサンプル496・34 witness群+56 FATEキー158突合）
- path: research/experiments/remo-k-branch-cap10-r11-boundary-20261117/mask_engine_fast_r11.js
  role: solver
  note: K0893出版修正版エンジン（pack符号シフトのr一般化・K0895版と同一バイナリ・CLI引数でr指定）のbyte同一コピー
- path: research/experiments/remo-k-branch-cap10-r11-boundary-20261117/pack_records_r11.py
  role: solver
  note: full→packed出版形式の決定的パッキングscript
- path: research/experiments/remo-k-branch-cap10-r11-boundary-20261117/output/js_cap10_r11.packed.jsonl
  role: data
  note: r=11完全スイープのpacked記録15863レコード（[i, sv_mask, fl_mask, states]・atomsは正準列挙のiの純関数・325,479 bytes・sha256 08324c19e8837041d8128423f26d88100b1ba7963fea1b86e3f90052b10664f0）。FL違反0
- path: research/experiments/remo-k-branch-cap10-r11-boundary-20261117/output/remo_k_branch_cap10_r11_boundary_audit.json
  role: data
  note: 監査JSON（sha256 a437de751047de99b5c466ca87f7c0ad9abfd31da82108d954b08423c048cb5d）。検証器run()がcommitted fileとコールド再生成のbyte照合を行う
scope: '極大安全集合がちょうど3個の点族（3枝合成族）のREMOについて、枝サイズがすべて10以下の場合（K0862/K0864/K0866/K0893/K0895と同一の15863正規形プロファイル・715キー領域）に、r=11では決定性が(sizes,gamma)に坍縮しないキーがr=9/r=10境界と同一の(6,6,8),(6,8,8)×gamma=0..4・(8,8,9),(8,9,9)×gamma=0..5・(6,6,9),(6,8,9),(6,9,9)×gamma=0..3の7族34個ちょうどであること、34キーすべてで決定側生存者が一様P_5=チェーン値であること、非決定側可能生存者集合・per-key分割計数がr=10出版表と完全同一であること、r=9/r=10でmixedだった34キーすべてがr=11でもmixed存続しr=3..10出版失敗56キーのうち22キー（小枝族・4/8族・4/9族）がr=11でも一様非決定（チェーンverdict・チェーン生存者ラベルも不変）であること、K0895出版r=10 packed記録とr=11記録が全15863プロファイルでdeterminedフラグおよび生存者maskの両方で一致（差0）し、K0893出版r=9 packed記録ともdeterminedフラグが全プロファイル一致すること（3列連続の決定性分類不動点）、剰余類計数が55/330/330でr=10と同一分割・単一剰余55キーが全等トリプルちょうどであること、mixed剰余対が{6,8},{6,9},{8,9},{6,8,9}であること、補題FL違反0・定理G-prime r=11拡張・Δ=0プロファイル728個の定理D一致を完全列挙により確定する（定理E-prime経由で任意の実現盤面に全称的に及ぶ）。枝サイズ11,12×r=9,10,11、r≥12、順位決定性、STASIS/FATE/活動窓/剰余レンズの一般則（r≥9で境界が定常という全称主張を含む・生存者mask不動点のr≥12での継続）は含まない'
evidence: '定理I r=11は有限パラメータ領域の完全計算による証明: 15863正規形プロファイルをr=11で完全スイープ（予算スキップ0・441秒・max_states 590,430。JS maskエンジン mask_engine_fast_r11.js・K0893修正版のbyte同一コピー。packed記録15863レコードを出版し検証器がインデックス整合・atoms==正準列挙・形式を検証）、(sizes,gamma)キーごとの均一性を機械判定。34キーのr=9/r=10との完全一致・FATE56（34存続/22一様非決定）・剰余計数55/330/330・witness（det/ndet atoms）はすべて検証器のピン付き定数として再導入され監査出力に記録（sha256 a437de751047de99b5c466ca87f7c0ad9abfd31da82108d954b08423c048cb5d・2回実行byte同一）。STASIS3はK0895出版r=10 packed記録（repo内commit済み・sha256 fa1e1a40…）とのdeterminedフラグ・生存者mask全プロファイル照合で差0、K0893 r=9 packed記録（a2bb16bc…）とのdeterminedフラグ照合で差0、第1敗者mask 7,328差分のpinを検証器が直接確認。live checkとしてcap≤7全域2048判定でverbatimエンジン==Python mask twin==committed JS記録（verdict・状態数）、stride 32層化サンプル496判定、34キーwitness群と56 FATEキーのチェーンをverbatim再実行（158判定をcommitted JS記録と突合）。補題FLはK0864で全称証明済み（r=11は冗長アンカー）。非坍縮キー列挙は有限範囲（C_i≤10・r=11）の完全計算であり、範囲外への全称昇格（r≥9で境界が定常等）はしない'
---

# 3枝REMO決定性のr=11境界

## 命題・範囲

K0895が「r≥11は未走査」と残した点を埋め、失敗族のr依存の観察を
さらに1列蓄積する。

- **定理I r=11（34キーちょうど・7族・r=9/r=10と完全同一）**:
  非坍縮はr=9境界（K0893）・r=10境界（K0895）と同一の7族34個で、
  新規0・坍縮0・復活0: (6,6,8),(6,8,8)×γ=0..4・
  (8,8,9),(8,9,9)×γ=0..5・(6,6,9),(6,8,9),(6,9,9)×γ=0..3。
  34キーすべてで決定側生存者は一様P_5（=チェーン値・定理G′ r=11
  拡張・不一致0）。非決定側可能生存者集合は
  {3,4,5},{3,5},{3,5,7},{3,4,5,7},{3,4,5,6,7}内、per-key分割計数も
  34キーすべてでr=10出版表と完全同一。センサスは一様決定98・
  一様非決定583・mixed 34（キー数はr=9/r=10と同一）。max_states
  590,430。Δ=0プロファイル728個は定理Dのr=11列に全一致。補題FL
  違反0（K0864全称証明の冗長アンカー）。
- **STASIS3（3列不動点＋生存者mask不動点・新種の観察）**: K0895
  出版のr=10 packed記録とr=11記録は全15,863プロファイルで
  determinedフラグが完全一致（差0）に加え**生存者maskも完全一致
  （差0）**。r=9→r=10では成立しなかった全列ラベル不動点（決定性
  分類のみならず生存者ラベルまで固定）で、K0895のdetフラグ不動点
  より真に強い。K0893のr=9記録を含めると3連続列（r=9,10,11）で
  決定性分類が完全不変（有限観察・一般則ではない）。第1敗者mask
  はr=10↔r=11で7,328件異なる（ラベル固定は生存者のみ）。
- **FATE56（2列連続無事象）**: r=9/r=10でmixedだった34キー（6/8
  族10・8/9族12・6/9族12）はr=11でもmixedのまま存続（3列連続
  存続）。r≤8失敗でr=9に坍縮済みの22キー（小枝族10・4/8族6・
  4/9族6）はr=11でも一様非決定（チェーンverdictもチェーン生存者
  ラベルもr=10と不変）。新規族0・復活0・一様決定化0: FATE系列で
  2列連続の「何も起こらない」列。活動窓はr=10値のまま
  （8/9族{3,4,5,9,10}・6/8族{8,9,10}・6/9族{9,10}・小枝族{3}・
  4/8族{6}・4/9族{7}・有限観察）。
- **剰余算術（r=11の新算術列）**: 715キーの剰余類計数は単一55・
  二重330・三重330でr=10と完全同一の分割（本項が初計数・純算術）。
  r=11は最大枝サイズ10を超えるためmodular wraparoundが存在せず、
  単一剰余キーは全等トリプルちょうど。一般にr>最大枝サイズなら
  剰余類計数はサイズ列の線形構造のみで決まるため、r≥12でもこの
  分割は不変（純算術の帰結）。mixedキーの剰余対は{6,8},{6,9},
  {8,9}と3剰余{6,8,9}（(6,8,9)×γ=0..3）で、K0893の
  「非坍縮⇒2剰余」初反例はr=11でも3列目の存続。
- **4/10族（K0874候補族）**: 8キーはr=11でも一様非決定
  （r=2..11で一度もmixedにならず・有限観察）。
- **FL11/G-prime11/D0**: 補題FL違反0。定理G′ r=11拡張: 一様決定98
  キーすべて生存者=チェーン（不一致0）。Δ=0プロファイル728個は
  定理Dのr=11列に一致。

## 限界

- 枝サイズ11,12×r=9,10,11は未走査（K0881のcap≤12拡張はr=7,8まで）。
- r≥12は未走査。順位決定性は本項で扱わない（検証器も順位フィールド
  を再導出しない）。
- STASIS3は3列の有限観察であり「r≥9で境界が定常」という全称主張
  ではない。生存者mask不動点もr=10↔r=11の1組の観察であり、
  r≥12での継続は保証しない。
- FATE/活動窓/分割計数不変性は有限観察のまま。
- 11×11空盤・クラスフロンティアは本項と無関係でUNKNOWNのまま。

## 再現

`verify_remo_k_branch_cap10_r11_boundary.py`（自己完結・決定的・
Python 3.11+ stdlibのみ・ネットワークなし・K0895検証器の機械変換
[単独性assert付き置換]）。11機械チェック全合格・2回実行で監査
JSON byte同一
（sha256 a437de751047de99b5c466ca87f7c0ad9abfd31da82108d954b08423c048cb5d）。
live checks: cap≤7全域2,048判定のverbatim==Python mask twin==committed
JS記録（verdictと状態数）・stride 32層化サンプル496判定・34キーの
det/ndet/chain witnessと56 FATEキーのチェーンをverbatimエンジンで
再実行（158 witness判定をcommitted JS記録と突合）。監査JSONは
検証器run()がcommitted fileとのbyte照合を行う。K0895 r=10 packed
記録（../remo-k-branch-cap10-r10-boundary-20261117/）とK0893 r=9
packed記録（../remo-k-branch-cap10-r9-boundary-20261117/）を
STASIS3チェックで読む（repo内commit済みファイル・ネットワーク不要）。
