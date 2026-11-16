---
id: K0876
title: 3枝REMO決定性のr=4,5,6サイズ境界cap≤12拡張（非坍縮キーは出版cap≤10境界のまま）
kind: computation
status: computed
topics: [multiplayer, variants, strategy-length]
aliases: [three-branch REMO cap12 r456 size boundary]
relations:
- type: depends_on
  target: K0861
  note: 定理E′（atomプロファイルへの軌道簡約・全称）でプロファイル判定が盤に転送される
- type: depends_on
  target: K0862
  note: エンジン系譜（領域計数ゲーム・プロファイル列挙・Burnside機構・定理D再帰）
- type: depends_on
  target: K0864
  note: 定理I（cap≤10のr=4,5,6非坍縮境界）・出版分割計数・出版witness・生存者ラベル
- type: depends_on
  target: K0872
  note: 第1敗者剰余レンズ（出版失敗剰余対 r=4:{0,1}, 5:{3,4}, 6:{2,4}）
- type: depends_on
  target: K0875
  note: 定理H12（r=3・cap≤12）・正準形47,595プロファイル列挙・audit JSON・r=3クロスアーティファクト
- type: extends
  target: K0864
  note: r=4,5,6のサイズ境界をcap≤10からcap≤12へ拡張し非坍縮キー集合の不変を確定
- type: extends
  target: K0875
  note: 定理H12の残課題「r≥4×枝サイズ11,12セル」をr=4,5,6で閉じる
- type: verifies
  target: K0864
  note: 出版cap≤10境界（キー集合・分割・生存者・ミラー交代）をcommitted records上で再現
artifacts:
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/report.md
  role: data
  note: 定理I12主張・センサス表・剰余レンズ・アンカー・savedColバグ修正記録・限界
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/verify_remo_k_branch_cap12_r456_boundary.py
  role: verifier
  note: committed records照合・Python twin live checks・出版定数埋込み・40機械チェック・assemble二重バイト同一
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/mask_engine_fast.js
  role: solver
  note: r=3..6の決定的maskエンジン（savedCol退避バグ修正済み）
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/resume_sweep.sh
  role: solver
  note: 実行環境制約下での分割再開スイープdriver
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/resume_check.py
  role: solver
  note: スイープ進捗・レコード整合の再開前検査
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/gen_profs.py
  role: solver
  note: 正準形47,595プロファイルの決定的生成
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r3.jsonl.gz
  role: data
  note: r=3決定的sweepレコード47,595件（K0875クロスアーティファクト照合済み）
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r4.jsonl.gz
  role: data
  note: r=4決定的sweepレコード47,595件
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r5.jsonl.gz
  role: data
  note: r=5決定的sweepレコード47,595件
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/output/js_cap12_r6.jsonl.gz
  role: data
  note: r=6決定的sweepレコード47,595件
- path: research/experiments/remo-k-branch-cap12-r456-boundary-20261116/output/remo_k_branch_cap12_r456_boundary_audit.json
  role: data
  note: 40機械チェック・r=3..6センサス・分割・剰余レンズ・アンカーの全記録
scope: "3枝REMO、r=4,5,6、枝サイズ≤12（正準形47,595プロファイル・1,365キー）の有限完全列挙。r=7,8×枝サイズ11,12の組合せと枝サイズ≥13は未走査。順位決定性は再導出していない。"
evidence: "決定的JavaScript maskエンジンで生成したコミット済みsweepレコード（47,595件×r・gzip -n・sha256照合）を、Python mask twinのlive checks（cap≤7全域8,192判定・層化サンプル5,952判定・全witness 104件の三重照合0不一致）と出版定数の機械再現（K0864境界・分割・生存者・K0875 audit・K0859定理D表・K0872剰余対）で検証する単一検証器（stdlibのみ・決定的・assemble二重バイト同一）による40 machine checks全合格。"
---

## 主張

**定理I12（cap≤12・r=4,5,6・有限完全）**: 3枝点族で全枝サイズC_i≤12・任意γのとき、生存者決定性が(sorted sizes, γ)に坍縮しないキーは**出版cap≤10境界（K0864定理I）と完全同一**である: r=4,5は(8,8,9),(8,9,9)×γ=0..5の12個、r=6は(4,4,8),(4,8,8)×γ=0..2の6個。サイズ境界10→12で新規キーは0個。

付随する確定事実:

- サイズ11枝を含む363キー・サイズ12枝を含む364キー（和集合650・新キー）に**mixedは0個**（r=3の定理H12と同じキー集合）。新キーは一様決定110個（r=3,4）/78個（r=5,6）と残り一様非決定。
- キーセンサス（一様決定/一様非決定/mixed・1,365キー）: r=4: 216/1137/12、r=5: 163/1190/12、r=6: 163/1196/6（r=3再掲: 232/1111/22）。max_states 100,240/241,132/506,254。
- 失敗キーの構造はcap≤10と完全不変: 決定側生存者はr=4,5で一様P_2・r=6で一様P_3、非決定側可能生存者集合はr=4: {(1,2,3)}、r=5: {(1,2,3),(1,2,3,4)}、r=6: {(2,3)}、8/9族のr=4,5分割計数はr=3出版表と同一、4/8族ミラーのr=6計数も出版と同一。
- r=3小枝族10キーはr=4,5,6の全域47,595プロファイルで一様非決定。4/8族ミラー6キーはr=4,5で全域一様非決定・r=6でmixed（出版交代の拡張）。
- 剰余レンズ拡張: 新2剰余キーはr=4: 576個・r=5: 592個・r=6: 605個で全て坍縮。r=4では出版失敗対{0,1}を持つ新キー60個（すべてサイズ12枝を含む15サイズ多重集合）も全て一様非決定、r=5,6では出版失敗対を持つ新キー0個。
- 補題FL（可能第1敗者=={C_i mod r}）はr=4,5,6×全プロファイルで違反0。Δ=0プロファイル1,512個（サイズ11,12枝を含む784個を含む）は全て定理D値で決定的。定理G′生存者レベルは一様決定キー232/216/163/163個すべてで不一致0。定理D再帰はK0859出版表84エントリと完全一致。r=3のcommitted recordsはK0875出版auditを正確に再現。

## 限界

r=4,5,6のみで、**r=7,8×枝サイズ11,12のセルは未走査**（K0866/K0869のr=7,8境界はcap≤10上限）。枝サイズ≥13は未走査で「サイズ8/9・6+8枝が失敗に必要」はサイズ≤12でのみ確定。**順位決定性は再導出していない**（maskエンジンのレコードは生存者・第1敗者・決定性のみを再現しorder列を再現しない）。非坍縮キーの構造的特徴づけは未解決で本項は列挙。11×11空盤はUNKNOWNのまま。
