---
id: K1254
title: "一般Xマージ法則 GX-M の観測と frontier reduction 補題 FR-X（多重度非依存・境界行 z=σ の有限パリティ条件 F±X への検証削減）"
kind: lemma
status: proved
topics: [grundy, residual-games]
aliases: 3トークン以上の残余ゲームマージ法則初観測、frontier reduction、F±X 前沿条件、BSL R* 公式、low-R 一般X縮約
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン全称閉形式 single_token/single_token_val（監査の閉形式側・FR-X の κ=1 基底・Lemma 0 平坦性の算術恒等）
- type: depends_on
  target: K1138
  note: 出版生エンジン H_ordered/H_canonical の逐語転写系列（y18全称機 part2 SHA-256 8ddd0c2f… からブロック抽出・engine ブロック SHA e5abe053… を scripts/check_blocks.py で照合）
- type: extends
  target: K1242
  note: bibliography 的母体は出版 cand17/cand18 ブロック（K1240/K1242 proved）: E5 成分が証明済み閉形式自身の境界行 BSL/F± 一致（9,266 セル）を機械確認し、y<=19 の証明済み族では F± が族閉形式の帰結であることを傍証
- type: related
  target: K1243
  note: 2トークンマージ法則 z>=S+1（= merge corollary x<=z-(y+1)）はプッシュ直前時点で y=1..20 全称確定（y=20 は K1249 全称機で完結・最新main再取得で確認）。本項は (a) F±(x,y) が成り立つときの全 y への構造的拡張経路（FR-X）と (b) y=21..30 の130族の新規独立 DP 証拠（M2D/M2・出版閉形式に依存しない）を与える
- type: related
  target: K1247
  note: 3トークンx11スケルトンレーンへの接続: GX-M・F±X の 3トークン観測、3トークン境界行の tail onset が σ+1..σ+4 にばらつくことの観測（公式未確定・follow-up 課題）
- type: related
  target: K1246
  note: y=20 族全称は K1249 として出版済み（プッシュ直前の最新main再取得で確認）。FR-X は境界行 F± 検査のみで y=20 マージ corollary を被覆する独立経路を与え、K1249 との相互整合傍証となる。y=21 以降の族全称レーンにも同じ経路が開かれている
artifacts:
- path: research/experiments/generalx-merge-frontier-reduction-20261123/report.md
  role: proof
  note: FR-X 定理の証明（σ 強帰納 + z↑ R↑・k>=1 層は選択肢集合の完全一致で無条件・k=0 前沿のみ mex 比較に帰着・Lemma 1 の27ケース表・F±X への簡約・出版 tail による R'>=2σ+1 の自動被覆・有限性の注意）と全観測法則の正確な宣言
- path: research/experiments/generalx-merge-frontier-reduction-20261123/audit_frontier.py
  role: verifier
  note: 正本監査機 9 成分（CX/XB/M2/M2D/G3/G4/L4/E5/C8）・fail-closed tamper 電池 6 変種同梱・出版転写ブロック3種収録（check_blocks PASS）・SHA-256 6c275bfe…
- path: research/experiments/generalx-merge-frontier-reduction-20261123/output/audit.json
  role: data
  note: 監査正本・overall_bad 0・総照合点 5,737,883・SHA-256 206ab3ac…・3実行 byte-identical（同一cwd+隔離tree+PYTHONHASHSEED=random+サンドボックスフルリセット後の全再構築再実行・リセット前後で byte 一致）
- path: research/experiments/generalx-merge-frontier-reduction-20261123/output/published_run.txt
  role: data
  note: 実行記録（pinned walls・tamper 6/6 detected・検出器バグ自捕捉の正直記録〔comp_m2d top-level bad 欠落を T2/T3 の TAMPER-MISSED が暴き出版前修正〕・C8 規則初稿の誤りをスモークが捕捉・リセット後の再生成が正本）
- path: research/experiments/generalx-merge-frontier-reduction-20261123/scripts/check_blocks.py
  role: verifier
  note: audit_frontier.py 内転写ブロックの SHA-256 固定値照合（engine e5abe053…/cand17 44f1ce4e…/cand18 caf13e80…）・PASS
- path: research/log/2026-11-23-generalx-merge-frontier-reduction-single-owner-note.md
  role: log
  note: 実行前単一オーナー宣言（commit efe21bd3・observed HEAD cf3fbe4a・予想点数は出版前に機械算出・対抗宣言 grep clean・K1254 仮採番）
- path: research/log/2026-11-23-generalx-merge-frontier-reduction.md
  role: log
  note: 実行記録（選定・経緯・誠実記録・出版記録・次段階）
---

## 定理（proved・条件つき補題）

**Theorem FR-X（frontier reduction）**。𝓜 をトークン簡約で閉じた多重集合のクラスとする。各 X ∈ 𝓜（κ(X) ≥ 2）について境界行 b_X(R') = H(R'; X; σ(X)) が前沿条件

- σ 偶数（F+）: b_X(奇数 R' ≤ σ-1) ≠ 1、b_X(偶数 R' ≤ σ) = 0、[σ+1, 2σ] で b_X ≠ 1
- σ 奇数（F-）: b_X(奇数 R' ≤ σ-2) ≠ 1、b_X(偶数 R' ≤ σ-1) = 0、[σ, 2σ] で b_X ≠ 0

を満たすならば、全 X ∈ 𝓜・全 z ≥ σ(X)+1・全 R ≥ 0 で H(R; X; z) = ST(σ, R)（マージ法則）が成立する。F±X は X ごとに有限（≈2σ+1 点）で、R' ≥ 2σ+1 は出版 tail 定理（一般X全称）で自動成立。k = z-(σ+1) ≥ 1 の層は選択肢集合が単一トークン側と完全一致するため無条件にマージ法則を満たし、唯一の障害は前沿 k = 0 の mex 比較 mex({φ₁, 1^b}) vs mex({φ₁, 1^s})（φ₁ = ST(σ-1, R-1)・s = 出版単一トークン境界閉形式）であり、27ケース mex 表（t=0: [b]==[s] の代替不是 [b==0]==[s==0]、t≠0: [b==1]==[s==1]・全ケース機械検証）で F±X に完全簡約される。

帰納構造: σ 強帰納（トークン子・消費子は σ-1 に落ち外側帰納被覆）+ 内側 z 昇順（z子のみ z 減少）+ R 昇順（全子 R-1）。基底は κ=1（出版単一トークン平坦性 Lemma 0・K0832閉形式の算術恒等）。

**効率帰結**: マージ領域の検証が境界行のパリティ有限検査に削減される。族追加ごとの全領域検証器（~700万点/族）が不要になる道が開け、y=20 全称（K1249 出版）とは独立に y=21 以降の族全称レーンのマージ corollary への別経路を与える。

## 観測された法則（observed・有限監査・全称主張なし）

1. **GX-M**: 3トークン（σ≤12 全列挙）・4トークン（σ≤10 全）・5トークン（σ≤8 全）+ストレッチ96族、z∈{σ+1,σ+2}、5,080点 bad 0。**3トークン以上のマージ法則は初観測**（他レーンは明示的に範囲外としてきた）。
2. **F±X**: 3/4/5トークン境界行 65族 1,237点 violation 0（FR-X の仮定の観測的支持）。
3. **BSL**: 2トークン境界行の R* = x+2y+1+(x mod 2) 公式。R < R* で出版単一トークン境界閉形式と一致（21,060点）、R ≥ R*-1 で tail（10,140点。出版 tail onset 2S+1 より最大 x 早期）、最初の乖離は R* ちょうど（390族中389族・(1,1) は R* > 2σ-1 で乖離窓が存在しない特例）、乖離は窓 [R*, 2σ] に局限（390/390）。y=1..30 × x=y..y+12（DP・124,800照合）+ y∈{20,22,24,26,28,30}×x∈{y,y+2} の生三点照合12族 + 証明済み cand17/cand18 での 9,266 セル一致（y≤19 では族閉形式の帰結）。
4. **2トークンマージ大掃引**: y=1..30、z∈{S+1,S+2}、63,180点 bad 0。y=21..30 の130族が新規証拠（y=20 は出版 K1249 全称と独立な DP 経路による再照合として機能）。
5. **low-R 一般X縮約**: R ≤ z+1 で H(R;X;z) = single_token(σ,z,R)、57族 5,984点 bad 0（出版 κ=2 低R縮約の一般X拡張観測）。
6. **F±（2トークン）**: 29,640点 violation 0。

## 機械的証拠の水準

- 出版生エンジン H_ordered/H_canonical + 出版閉形式 single_token/single_token_val + 証明済み cand17/cand18 を @@TRANSCRIPTION で逐語使用（SHA 照合 PASS）。新規 DP 列エンジンは 6族全セル 5,567,472 点で生エンジンと一致（CX）。
- 総照合点 5,737,883、全成分 bad 0、audit.json 3実行 byte-identical（同一 cwd、隔離 tree + PYTHONHASHSEED=random、サンドボックスフルリセット後の出版 bytes からの全再構築再実行）。
- fail-closed tamper 電池 6/6 検出（単一トークン閉形式反転・R* シフト・F 条件書換・DP ビット反転・single_token R オフバイワン・GX 単一側 σ-1）。
- 有限監査は有限観察の機械的証拠であり、GX-M/BSL/F±X/low-R の全称化は F±X の全多重集合での証明（境界行の内部 k≤-1 層依存・未解決）を要する。

## 正直な限界

- FR-X は十分条件の補題であり F±X 自体の全称証明を含まない（F±X の導出には内部層構造が必要で、本レーンは有限監査 + y≤19 での帰結傍証に留まる）。FR-X の必要性は主張しない。
- 3トークン境界行の tail onset は σ+1..σ+4 にばらつき、_formula 未確定（follow-up）。
- 標準11×11空盤・二石root・S2・class 1/2/4 はすべて UNKNOWN のまま。固定幅・q点版安定化長は範囲外。

詳細は[実験 README](../experiments/generalx-merge-frontier-reduction-20261123/README.md)・[定理と証明](../experiments/generalx-merge-frontier-reduction-20261123/report.md)・[監査JSON](../experiments/generalx-merge-frontier-reduction-20261123/output/audit.json)・[実行記録](../log/2026-11-23-generalx-merge-frontier-reduction.md)・[宣言ノート](../log/2026-11-23-generalx-merge-frontier-reduction-single-owner-note.md)。（2026-11-23）
