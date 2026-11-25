---
id: K0912
title: 3枝REMO決定性のサイズ境界cap≤12×r=9 — 定理I9のサイズ拡張（mixed 34キーはK0893境界と完全同一・650新キーにmixed 0・新45決定キーの剰余類構造）・定理Jのcap≤12 r=9機械アンカー（K0906系3の残4スイープの第1本）
kind: proposition
status: proved
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [three-branch REMO cap12 r=9 boundary]
relations:
- type: depends_on
  target: K0893
  note: r=9 cap≤10境界（34キー・7族）のサイズ拡張。D_10部分列15,863位置のr=9記録がK0893出版packed列とbyte一致・mixed 34キー・per-key分割・決定側生存者一様P_5・cap≤10サブセンサス98/583/34が完全同一
- type: depends_on
  target: K0906
  note: 定理J（全称・r ≥ max(M,2)でsv/det不変）のcap≤12 r=9機械アンカー。M≤8キーでdet/svがr=8列（K0881出版）と完全一致・det差分876はすべてM=9・M=9一様決定キーは(9,9,9)×γ=0..8（Δ=0族）ちょうど。K0906系3「残4スイープ」の第1本目
- type: depends_on
  target: K0875
  note: cap≤12正準領域（47,595プロファイル・1,365キー・Burnside 261749/7805/203）とD_10順序保存埋め込み（K0882性質）
- type: depends_on
  target: K0876
  note: r=2..8 cap≤12 committed列（定理Jアンカー・ECHO表r=2..8の相手側）とエンジン機構（mask_engine_fast2.jsはK0893修正版のメモ表現のみ相違）
- type: depends_on
  target: K0864
  note: 補題FL（全称）のr=9・cap≤12冗長アンカー（全47,595プロファイル違反0）
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりプロファイルverdictは実現盤面すべてに移る
- type: depends_on
  target: K0859
  note: Δ=0プロファイル1,512個（うち784個は11/12枝を含む）が定理D再帰のr=9列・定理D再帰は出版表84エントリと一致
- type: depends_on
  target: K0900
  note: STASIS系列監査再現性欠陥の教訓を反映した出版設計（committed記録はpacked単一ソース・atomsはiの純関数・full形式はコミットせず・fresh checkoutでの監査byte再現性を最初から組み込み）
artifacts:
- path: research/experiments/remo-k-branch-cap12-r9-boundary-20261117/report.md
  role: proof
  note: 定理I9サイズ拡張（34キー同一・新キー650個の内訳）・新45決定キーの剰余類構造・定理J cap≤12 r=9アンカー・Δ=0・ECHO・FL・限界・再現の説明
- path: research/experiments/remo-k-branch-cap12-r9-boundary-20261117/verify_remo_k_branch_cap12_r9_boundary.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ・packed単一ソース。13機械チェック全合格・assemble二重実行byte同一・2回目cold実行で「audit byte-identical」。live checks（cap≤7全域2,048のverbatim==twin==JS・D_10 stride-32層化432・新キー層化450・34 mixedキーwitness 102判定のJS突合）。CIコールド実行約7分
- path: research/experiments/remo-k-branch-cap12-r9-boundary-20261117/mask_engine_fast2.js
  role: solver
  note: K0893修正版JS maskエンジン（r一般化シフト）のbyte arena + open addressingメモ実装（ゲーム論理・再帰順序・予算意味論・レコード形式はverbatim同一・メモ表現のみ相違）
- path: research/experiments/remo-k-branch-cap12-r9-boundary-20261117/output/js_cap12_r9.packed.jsonl
  role: data
  note: r=9 cap≤12完全スイープのpacked記録47,595レコード（[i, sv_mask, fl_mask, states]・atomsは正準列挙のiの純関数）。sha256 02e771cd…・975,488 bytes。独立2プロセス（添字0..24,447と23,798..47,594・オーバーラップ650レコードbyte一致）のマージで生成・実行環境リセット後も再マージでbyte再現
- path: research/experiments/remo-k-branch-cap12-r9-boundary-20261117/output/remo_k_branch_cap12_r9_boundary_audit.json
  role: data
  note: 監査JSON（sha256 8c87d104…）。検証器run()がcommitted fileとのbyte照合を行う（fresh checkout再現可能）
scope: '極大安全集合がちょうど3個の点族（3枝合成族）のREMOについて、枝サイズがすべて12以下の場合（K0875/K0876と同一の47,595正準プロファイル・1,365キー領域）に、r=9では決定性が(sizes,γ)に坍縮しないキーがK0893 cap≤10境界の7族34個と完全同一であること（サイズ11/12を含む650新キー・31,732プロファイルのうちmixedは0・新キーは一様決定45/一様非決定605）、新45一様決定キーが(1,1,11)|0・(1,11,11)|0・(10,10,12)×γ=0..9・(10,12,12)×γ=0..9・(11,11,11)×γ=0..10・(12,12,12)×γ=0..11ちょうどで第1敗者剰余類が{1,2},{1,3},{2},{3}のみであること、M=max C_i≤8の全キーでr=9のdet/svがr=8列と完全一致しr8→r9のdet差分876がすべてM=9プロファイルでM=9一様決定キーが(9,9,9)×γ=0..8（Δ=0族）ちょうどであること（定理Jのcap≤12機械アンカー・証明はK0906）、Δ=0プロファイル1,512個が定理Dのr=9生存者で決定であること、一様決定143キーすべての決定プロファイルがチェーン生存者を持つこと、34 mixedキーのr=2..9決定性履歴がサイズ拡張で不変であること、補題FL違反0を完全列挙により確定する（定理E′経由で任意の実現盤面に全称的に及ぶ）。枝サイズ≥13・r≥10・順位決定性・新キー構造の一般則は含まない'
evidence: '有限パラメータ領域の完全計算による確定: 47,595正準プロファイルをr=9で完全スイープ（予算スキップ0・独立2プロセスでオーバーラップ650レコードbyte一致を確認しマージ・実行環境リセット後も両セグメントの再マージでpacked sha256 02e771cd…がbyte再現）。JS maskエンジン mask_engine_fast2.js（K0893修正版とゲーム論理・再帰順序・予算意味論・レコード形式verbatim同一・メモ表現のみ相違）でpacked記録47,595レコードを出版（atomsはiの純関数で packing は損失なし・検証器がpacked→レコード復元とbyte往復を検証）。committed記録はpacked単一ソースとしfull形式はコミットしない（K0900で発見した監査再現性欠陥の予防・fresh checkoutで検証器run()の監査byte照合が通る設計）。13機械チェック全合格（Burnside×3+包含・packed整合+engine sha・K0893 D_10列byte一致・FL違反0・センサス+mixed同一+分割+チェーン・新キーセンサス+G′+剰余+45キー・定理J+Δ0・ECHO・定理D表84）・assemble二重実行byte同一・2回目cold実行で「OK: audit byte-identical」（監査sha256 8c87d104…）。live check: cap≤7全域2,048判定でverbatim==Python mask twin==committed JS記録・D_10位置stride-32層化432判定・新キー(11/12枝)stride-37層化450判定・34 mixedキーのchain/min-det/min-ndet witness 102判定をverbatimエンジンで再実行しcommitted記録と突合。定理JはK0906の全称証明に依存し本項のr=9列は機械アンカーであって証明ではない。新キー構造・ECHO・167キーのチェーン和集合一致は有限観察であり全称昇格しない'
---

# 3枝REMO決定性のサイズ境界（枝サイズ≤12）×r=9

## 命題・範囲

K0906系3「cap≤12の残4スイープ」の第1本。K0893が「枝サイズ11,12×r=9は
未走査」と残したセルを埋め、定理I系譜のr=9列をcap≤12全域で確定する。

- **定理I9サイズ拡張（mixed 34キーちょうど・サイズ不変）**: 非坍縮
  キーはK0893 cap≤10境界の7族34個と**完全同一**。(1,1,11)|0や
  (12,12,12)×γ=0..11といったサイズ11/12を含む650新キー
  （11枝363・12枝364・31,732プロファイル）のうち**mixedは0**で、
  新キーは一様決定45 / 一様非決定605に二分。34キーのper-key分割・
  決定側生存者一様P_5・34チェーンプロファイル全決定・cap≤10
  サブセンサス98/583/34はK0893出版値と同一。D_10部分列15,863位置の
  r=9記録はK0893出版packed列とbyte一致（max_states 363,630）。
- **新45一様決定キーの剰余類構造（有限観察）**: (1,1,11)|0,
  (1,11,11)|0, (10,10,12)×γ=0..9, (10,12,12)×γ=0..9,
  (11,11,11)×γ=0..10, (12,12,12)×γ=0..11 ちょうど。第1敗者剰余類は
  {1,2},{1,3},{2},{3}のみ（11≡2・12≡3 mod 9）。605一様非決定の
  うち167は可能生存者集合==チェーン生存者の和集合（観察）。
- **定理J cap≤12 r=9アンカー（K0906全称定理の機械アンカー）**:
  M = max C_i ≤ 8の全キーでr=9のdet/svはr=8列（K0881出版）と完全
  一致（0/0）・M ≤ 7ではflも一致。r8→r9のdet差分876はすべてM=9
  プロファイル（34キー族がr ≥ max(M,2)閾値を跨ぐ分）・M=9一様決定
  キーはΔ=0族(9,9,9)×γ=0..8ちょうど。sv-mask差分38,070。
- **Δ=0（定理D）**: 一様サイズ1,512プロファイル（うち784は11/12枝
  を含む）はすべて定理Dのr=9生存者で決定・定理D再帰はK0859出版表
  （84エントリ）に一致。
- **G′ r=9**: 一様決定143キーすべての決定プロファイルがチェーン
  生存者を持ち不一致0（45新キーを含む）。
- **ECHO r=2..9**: 34 mixedキーの決定性履歴はサイズ拡張で一切不変
  （6/8族{8,9}・8/9族{3,4,5,9}・6/9三族r=9初覚醒）。
- **補題FL（K0864全称・冗長アンカー）**: 全47,595プロファイルで
  第1敗者 == {C_i mod 9}・違反0。

センサス: 1,365キー = 143 / 1,188 / 34。max_states 2,331,310
（i=31964・(12,12,12)|γ=3）・状態総数3,889,246,676。

## スイープと出版形式

独立2プロセス（添字0..24,447と23,798..47,594・オーバーラップ650
レコードは(sv,fl,states)三つ組byte一致）でスイープしマージ。
実行環境のリセットを1回挟んだが両セグメントが保全され、再マージで
packed列（sha256 02e771cd…・975,488 bytes）がbyte再現した。
committed記録は**packed単一ソース**としfull形式はコミットしない
（atomsは正準列挙のiの純関数なので劣化なし・K0900で発見した
STASIS系列監査再現性欠陥の予防）。検証器はpackedからレコードを
復元しbyte往復を検証する。

## 限界

- 枝サイズ≥13・r≥10は本項の範囲外（K0906系3の残るアンカー列）。
- 定理Jは全称定理（K0906）であり、本項のr=9列はそのcap≤12機械
  アンカーであって証明ではない。
- 順位決定性は本項で扱わない（検証器も順位フィールドを再導出
  しない）。
- 新キー構造・ECHO・チェーン和集合一致はすべて有限観察であり、
  一般則・全称定理へは昇格しない。
- 11×11空盤・クラスフロンティアは本項と無関係でUNKNOWNのまま。

## 再現

`verify_remo_k_branch_cap12_r9_boundary.py`（自己完結・決定的・
Python 3.11+ stdlibのみ・ネットワークなし）。13機械チェック全合格・
assemble二重実行byte同一・2回目cold実行で「OK: audit
byte-identical」（監査JSON sha256 8c87d104…）。live checks:
cap≤7全域2,048判定のverbatim==twin==JS突合・D_10 stride-32層化
432判定・新キー層化450判定・34 mixedキーwitness 102判定のverbatim
再実行とJS突合。CIコールド実行約7分。
