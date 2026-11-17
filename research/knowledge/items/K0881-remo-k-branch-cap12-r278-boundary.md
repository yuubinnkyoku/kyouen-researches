---
id: K0881
title: 3枝REMO決定性のr=2,7,8サイズ境界cap≤12拡張（非坍縮キーは出版cap≤10境界のまま・r=2列は補題FL閉形式で全プロファイルに錨付け）
kind: computation
status: computed
topics: [multiplayer, variants, strategy-length]
aliases: [three-branch REMO cap12 r278 size boundary]
relations:
- type: depends_on
  target: K0861
  note: 定理E′（atomプロファイルへの軌道簡約・全称）でプロファイル判定が盤に転送される
- type: depends_on
  target: K0862
  note: エンジン系譜（領域計数ゲーム・プロファイル列挙・Burnside機構・定理D再帰）
- type: depends_on
  target: K0864
  note: 定理I（cap≤10のr依存境界）・補題FL（全称・証明つき）のr=2閉形式・出版r=2..6サブセンサス
- type: depends_on
  target: K0866
  note: r=7境界（6キー・分割計数・witness・生存者P_3）のcap≤12拡張対象
- type: depends_on
  target: K0869
  note: r=8境界（10キー・分割計数・witness・生存者P_5）のcap≤12拡張対象とecho dormancy
- type: depends_on
  target: K0872
  note: 第1敗者剰余レンズ（出版失敗剰余対 r=7:{2,4}, 8:{0,6}）
- type: depends_on
  target: K0874
  note: 52キー状態行列のr=2,7,8列156セル（監査sha256ピン付きでsibling実験から再現）
- type: depends_on
  target: K0875
  note: 定理H12（r=3・cap≤12）・正準形47,595プロファイル列挙・D_10⊂D_11⊂D_12
- type: depends_on
  target: K0876
  note: 定理I12（r=4,5,6・cap≤12）・実験形式・maskエンジンの直接の親
- type: extends
  target: K0866
  note: r=7のサイズ境界をcap≤10からcap≤12へ拡張し非坍縮キー集合の不変を確定
- type: extends
  target: K0869
  note: r=8のサイズ境界をcap≤10からcap≤12へ拡張し非坍縮キー集合の不変を確定
- type: extends
  target: K0864
  note: r=2のcap≤10サブセンサスと生存者集合レベルの完全坍縮をcap≤12全域へ拡張（補題FL閉形式の帰結として決定論的）
- type: verifies
  target: K0866
  note: 出版r=7境界（キー集合・分割計数・witness・決定生存者一様P_3・剰余対）をcommitted records上で再現
- type: verifies
  target: K0869
  note: 出版r=8境界（キー集合・分割計数・witness・決定生存者一様P_5・剰余対・echo dormancy）をcommitted records上で再現
- type: verifies
  target: K0874
  note: 52キー状態行列のr=2,7,8列156セル（坍縮フラグ・生存者集合多様性・決定計数・chain判定・第1敗者剰余）をcommitted recordsのcap≤10部分列から完全再現
artifacts:
- path: research/experiments/remo-k-branch-cap12-r278-boundary-20261116/report.md
  role: data
  note: 定理I278主張・r=2閉形式錨付け・センサス表・剰余レンズ・アンカー・限界
- path: research/experiments/remo-k-branch-cap12-r278-boundary-20261116/verify_remo_k_branch_cap12_r278_boundary.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ。29機械チェック全合格・assemble二重実行byte同一・run()はcommitted監査JSONとコールド再生成のbyte照合を行う。live checks（cap≤7全域2048×3rのverbatim==mask twin==JS三重照合・層化サンプルstride 24/48/48・K0866/K0869全witnessとecho/pre-echoのverbatim再実行）
- path: research/experiments/remo-k-branch-cap12-r278-boundary-20261116/mask_engine_fast.js
  role: solver
  note: r=2,7,8の決定的maskエンジン（K0876実験dirと同一bytes・savedCol退避バグ修正済み系譜）・正準形プロファイル列挙は検証器内蔵のdirect_constrained(12)で再現
- path: research/experiments/remo-k-branch-cap12-r278-boundary-20261116/pack_records.py
  role: solver
  note: full形式レコード→packed出版形式の決定的packer
- path: research/experiments/remo-k-branch-cap12-r278-boundary-20261116/output/js_cap12_r2.packed.jsonl
  role: data
  note: r=2決定的sweepレコード47,595件・packed形式[i,sv_mask,fl_mask,states]（sha256 1fd9dbf4cb6699c26bab7f6b34a900f5877d3408603a02a2dd121ca71ef8e951・環境リセット挟み独立再生成でbyte-identical）
- path: research/experiments/remo-k-branch-cap12-r278-boundary-20261116/output/js_cap12_r7.packed.jsonl
  role: data
  note: r=7決定的sweepレコード47,595件・packed形式（sha256 50eb7c1ba41825dcbf726258cb2c6878a324d58bb17a708cb587d9d2b3b79c78）
- path: research/experiments/remo-k-branch-cap12-r278-boundary-20261116/output/js_cap12_r8.packed.jsonl
  role: data
  note: r=8決定的sweepレコード47,595件・packed形式（sha256 0a884b490e28c281166754c1e82aaa73f7515580dea05b4ce023e8a1f079e8dc）
- path: research/experiments/remo-k-branch-cap12-r278-boundary-20261116/output/remo_k_branch_cap12_r278_boundary_audit.json
  role: data
  note: 29機械チェック・r=2,7,8センサス・分割・剰余レンズ・アンカーの全記録（sha256 121dde1fd8abdcb8a3f7fcf05a7009dedf45db9891094e5cb921fd2a341a1319・meta.dateは2026-11-16固定・実行環境フルリセットを挟いた独立4回生成でbyte-identical）
scope: "3枝REMO、r=2,7,8、枝サイズ≤12（正準形47,595プロファイル・1,365キー）の有限完全列挙。r=7,8列は定理Jのr ≥ max(M,2)成立域の外側（M=11,12キー）を直接決める列。r=9..12×枝サイズ11,12・枝サイズ≥13・順位決定性は含まない。r=2の閉形式はK0864補題FL（全称証明済み）の帰結として決定論的だが、r=7,8の本結果は有限完全列挙であり全称特徴づけではない。"
evidence: "決定的JavaScript maskエンジンで生成したコミット済みsweepレコード（47,595件×3r・packed出版形式・sha256照合・環境リセットを挟いた独立再生成でbyte-identical）を、単一検証器（stdlibのみ・決定的・assemble二重実行byte同一・29 machine checks全合格）が照合する: レコードsha256・件数・インデックス完全性・atom列挙一致・予算スキップ0・Burnsideと直接列挙の軌道数一致（15,863/28,065/47,595）。出版定数は埋込み定数として全て再現する: K0866/K0869のr=7,8境界キー・分割計数・witness・決定生存者一様P_3/P_5・剰余対{2,4}/{0,6}、K0864のr=2閉形式とサブセンサス245/470、K0872剰余レンズ、K0874の52キー行列156セル（sibling実験監査sha256 6e68a86fピンで照合）、K0859定理D表84エントリ。live checksとしてcap≤7全域2,048プロファイル×3r=6,144判定でverbatimエンジン==Python mask twin==committed JS記録（verdict・状態数）、cap≤12層化サンプル（stride 24/48/48）、K0866 r=7・K0869 r=8の全witnessとchain生存者のverbatim再実行、r=2 echo dormancy（K0869失敗族10キー278プロファイルの全件再実行で一様決定P_1）とpre-echo（K0866族8チェーンの一様非決定）を三重照合する。監査JSON（sha256 121dde1fd8abdcb8a3f7fcf05a7009dedf45db9891094e5cb921fd2a341a1319）は実行環境フルリセットを挟いた独立4回の生成でbyte-identical（2026-11-16に3回・本backfill出版時に1回）。"
---

## 主張

**定理I278（cap≤12・r=7,8・有限完全）**: 3枝点族で全枝サイズC_i≤12・任意γのとき（正準形47,595プロファイル・1,365キー・予算スキップ0）、生存者決定性が(sorted sizes, γ)に坍縮しないキーは**出版cap≤10境界と完全同一**である: r=7は(4,4,9),(4,9,9)×γ=0..2の**6個ちょうど**（K0866定理I r=7）、r=8は(6,6,8),(6,8,8)×γ=0..4の**10個ちょうど**（K0869定理I r=8）。サイズ境界10→12で新規キーは0個。

付随する確定事実:

- サイズ11枝を含む363キー・サイズ12枝を含む364キー（和集合650・K0875/K0876と同じ新キー集合）に**mixedは0個**（新キーはr=7,8とも一様決定45個・残り605個一様非決定。r=2では203個一様決定・447個一様非決定）。新キーがmixedになることはr=2..8の全7列でない（K0875/K0876に続き確定）。
- キーセンサス（一様決定/一様非決定/mixed・1,365キー）: r=7: 143/1216/6、r=8: 143/1212/10。max_statesはr=7: 862,150・r=8: 1,436,710。cap≤10部分のサブセンサスは出版値と完全一致（一様決定98/98・2剰余キー362/347）。
- 失敗キーの構造はcap≤10と完全不変: 決定側生存者はr=7で一様P_3・r=8で一様P_5、per-key分割計数はK0866/K0869出版表と完全一致、剰余対はr=7: {2,4}・r=8: {0,6}でK0872出版対と同一、r=3小枝族10キー・4/8族ミラー6キーはr=7,8とも全域一様非決定（K0874のr=7,8列と整合）。
- 剰余レンズ拡張: 新2剰余キーはr=7で609個・r=8で613個で全て坍縮。r=7では出版失敗対{2,4}を持つ新キー30個も全て一様非決定（アウトオブサンプル署名検査・mixed 0）、r=8では出版失敗対{0,6}を持つ新キーは0個。
- 補題FL（可能第1敗者=={C_i mod r}・K0864全称証明）はr=7,8×全47,595プロファイルで違反0（冗長アンカー）。Δ=0プロファイル1,512個（サイズ11/12枝を含む784個を含む）は全て定理D値で決定的。定理G′生存者レベルは一様決定キー143/143×2rで不一致0（うち45個は11/12枝を含む新キー・新キー不一致0）。定理D再帰はK0859出版(C,r)表84エントリと完全一致。
- K0874の52キー状態行列のr=2,7,8列156セル（坍縮フラグ・生存者集合多様性・決定計数・chain判定・第1敗者剰余）はcommitted recordsのcap≤10部分列から完全再現（sibling実験の監査sha256 6e68a86f…ピンで照合）。

## r=2列（補題FL閉形式のcap≤12全プロファイル錨付け）

r=2では生存者集合は第1敗者の補集合なので、K0864補題FL（全称・任意k/r）は閉形式を与える: 全C_iが剰余p (mod 2)で一致すればあらゆるプレイで第1敗者P_p・生存者P_{1-p}でDETERMINED、mixed parityなら第1敗者{P_0,P_1}・生存者集合{P_0,P_1}でNON-determined（γ・atom配分は無関係）。本検証器はこの帰結をcommitted records上で全域錨付けする:

- センサスは**一様決定448キー・一様非決定917キー・mixed 0・2剰余キー=917個ちょうど**（閉形式の直接帰結・max_states 6,526）。cap≤10部分はK0864出版サブセンサス（決定245・非決定470・失敗0）と完全一致。
- K0869のr=8失敗族（(6,6,8),(6,8,8)×γ=0..4）はr=2では一様決定（chain生存者P_1・生存者不一致0・10キー278プロファイルの全件verbatim再実行でecho dormancyを確認）。K0866のr=7失敗族（(4,4,9),(4,9,9)×γ=0..3）はr=2では一様非決定（pre-echo・γ=3まで含む8チェーン全てn_det=0）。
- 全1,365キー×cap≤12全域でプロファイルごとの可能生存者集合==chainプロファイルの集合（K0862のcap≤7 r=2完全坍縮・K0864のcap≤10拡張に続き、この水準の坍縮がcap≤12でも崩れないことを記録。閉形式の系として決定論的）。

## 限界

r=2,7,8のみで、**r=9..12×枝サイズ11,12のセルは本項では未走査**（r=9はK0912で確定済み・残る確定スイープはサイズ11,12×r=10・サイズ12×r=11・r ≥ Mアンカー1列）。枝サイズ≥13は未走査で「r=7,8の失敗キーがサイズ4+9/6+8枝を含む」はサイズ≤12でのみ確定。**順位決定性は再導入していない**（maskエンジンのレコードは生存者・第1敗者・決定性のみを再現しorder列を再現しない）。r=2閉形式はK0864補題FLの帰結として全称だが、r=7,8の本結果は有限完全列挙であり全称特徴づけではない（定理J（K0906）はr ≥ max(M,2)の plateau を全称証明するが、M=11,12キーのr=7,8列は成立域の外側で本項の直接計算による）。非坍縮キーの構造的特徴づけ（なぜサイズ4+9/6+8か）は未解決のまま（列挙である）。11×11空盤はUNKNOWNのまま。
