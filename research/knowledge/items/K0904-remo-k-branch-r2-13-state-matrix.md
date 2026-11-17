---
id: K0904
title: 3枝REMO決定性の全状態行列r=2..13（715キー×12列・committed列のみで合成）と定理J有限検証 — σ(key)≤M(key)−1全キー成立・34境界キーはonset正確にr=M・復活2帯キーは(8,8,9),(8,9,9)×γ=0..5の12キーちょうど・出版境界12列完全再導出
kind: verification
status: verified
topics: [variants, multiplayer, verification]
aliases: [three-branch REMO state matrix, sigma stabilization bound, Theorem J finite verification]
relations:
- type: depends_on
  target: K0902
  note: 定理J (i)（sv/detはr ≥ Mで一定・予想）の定式化とr=13列。本項はC4/C5で各キー自身の閾値r=Mからの全キー・全プロファイル有限検証（違反0）を行い、出版済みr=11..13全ラベル不動点がr ≥ M不動点の特別な場合であることを確定
- type: depends_on
  target: K0898
  note: r=12列（packed記録を本項の行列合成で読む・sha256ピン照合）
- type: depends_on
  target: K0897
  note: r=11列（同上）
- type: depends_on
  target: K0895
  note: r=10列（同上）
- type: depends_on
  target: K0893
  note: r=9列（同上）
- type: depends_on
  target: K0876
  note: cap≤12のr=3..6列（47,595レコード・cap≤10への全単射制限で本項のr=3..6列として使用）
- type: depends_on
  target: K0869
  note: r=8列（cap≤12列経由）とr=8出版境界10キーの再導出
- type: depends_on
  target: K0866
  note: r=7列（cap≤12列経由）とr=7出版境界6キーの再導出
- type: depends_on
  target: K0864
  note: r=2,4,5,6列（cap≤12列経由）と出版境界・一様決定計数・補題FLの再導出
- type: depends_on
  target: K0862
  note: r=3出版境界22キー（定理H）の再導出と列挙機械（verbatim）
- type: supports
  target: K0874
  note: 失敗族状態行列の拡張。r=2..8×52キーからr=2..13×全715キーへ。mixed和集合44（r=2..8・K0874出版値と同一）と56（r=2..13）、復活2帯構造のper-key特徴づけ
artifacts:
- path: research/experiments/remo-k-branch-cap10-r2-13-matrix-20261117/report.md
  role: proof
  note: 主結果（出版境界12列完全再導出・定理J有限検証σ≤M−1違反0・34キーonset正確にr=M・復活12キー2帯）・per-rデータ表・限界とSGガード・再現手順
- path: research/experiments/remo-k-branch-cap10-r2-13-matrix-20261117/scripts/verify_remo_k_branch_cap10_r2_13_matrix.py
  role: verifier
  note: 自己完結検証器（stdlibのみ・決定的・新規スイープなし・13 committed列をsha256ピンで読み列挙はverbatim・8機械チェック・二重実行で監査byte同一）
- path: research/experiments/remo-k-branch-cap10-r2-13-matrix-20261117/output/remo_k_branch_cap10_r2_13_matrix_audit.json
  role: data
  note: 監査JSON（8機械チェック・all_ok=true・sha256 51c9e080…）
- path: research/experiments/remo-k-branch-cap10-r2-13-matrix-20261117/output/matrix_r2_13.jsonl
  role: data
  note: 715キー×12列状態行列（key/M/cls/σ/混合帯/最終生存者集約・sha256 8b2f759e…）
evidence: '検証器verify_remo_k_branch_cap10_r2_13_matrix.pyの8機械チェック全合格（2回実行で監査JSON・行列ともbyte同一・all_ok=true）。C1: 13 committed列sha256ピン一致・index完全・states>0。C2: cap12→cap10写像が15,863プロファイルに全単射。C3: r=2..13全12列のmixedキー集合が出版境界と完全一致（0/22/12/12/6/6/10/34×5・センサス98/583/34・max_states r12=666,030・r13=741,630・mixed決定側生存者P_2/P_3/P_5ピン一致・r=4..8可能生存者境界内・mixed和集合44と56）。C4: 715キーすべてで分類がr ∈ [M,13]で不変・違反0。C5: 15,863プロファイルすべてで生存者maskがr ∈ [M,13]で不変・違反0（detフラグ不変を含む・r=9..13の5列det不動点とr=11..13全ラベル不動点を各キー閾値まで拡張）。C6: 補題FL包含が13列全レコードで違反0・mixedキーの第1敗者剰余unionがK0872出版対と一致（r=3..8）。C7: σ(key)≤M(key)−1が715キーで成立・r=13でmixedの34キーはすべてσ=M−1で最終mixedレジームが正確にr=Mで開始・2帯キーは(8,8,9),(8,9,9)×γ=0..5の12キーちゝど。C8: 行列成果物715レコード・監査二重assemble byte同一。観察はr=2..13・cap≤10・k=3の有限全称であり定理J（全r ≥ M・任意k）の証明ではない'
---

# 3枝REMO決定性の全状態行列r=2..13と定理J有限検証

committed された13列のpacked記録（r=2..8はcap≤12列のcap≤10全単射
制限・r=9..13はcap≤10列）だけから、715キー×12列の決定性分類行列
を全合成した。新規スイープなし・検証器は2回実行でbyte同一。

## 主結果

1. **出版境界12列の完全再導出**: r=2..13の全列でmixedキー集合が
   K0864/K0862/K0866/K0869/K0893..K0902の出版値と完全一致し、
   mixed和集合はr=2..8で44キー（K0874）・r=2..13で56キー。
   mixedキーの決定側生存者（P_1→P_2→P_3→P_5のr系列）と
   r=4..8の可能生存者境界も出版ピンと一致。10項目以上の
   cross-item整合監査を兼ねる。

2. **定理J (i)の全キー有限検証（違反0）**: 715キーすべてで分類が
   r ∈ [M,13]で不変（C4）、15,863プロファイルすべてで生存者maskが
   r ∈ [M,13]で不変（C5）。出版済み「r=11..13全ラベル不動点」は
   「r ≥ M不動点」の特別な場合であり、全キーで生存者ラベルは
   r=M時点からすでに定常。

3. **σ ≤ M−1とonsetの鋭さ**: σ(key)（最後の分類遷移位置）は
   715キーすべてでM−1以下。r=13でmixedの34キーはすべて
   σ=M−1で、最終mixedレジームは正確にr=Mで開始する
   （onset at M・Mより早くも遅くもない）。

4. **復活構造の特徴づけ**: 2つの不連続mixed帯を持つキーは
   (8,8,9),(8,9,9)×γ=0..5の12キーちょうど（mixed [3,5]→一様 [6,8]→
   mixed [9,13]）。K0893の復活のper-key形。他の44 mixed経験キーは
   すべて単一連続帯。

5. **データ**: per-rセンサス（一様決定245/…/98・mixed
   0/22/12/12/6/6/10/34×5）・max_states完全系列
   （2,625…666,030・741,630）・一様決定キーのチェーン生存者系列を
   監査JSONに全件記録。行列成果物は
   output/matrix_r2_13.jsonl（715レコード）。

## 限界

- 本項はr=2..13・cap≤10・k=3の有限検証であり、定理J（すべての
  r ≥ M・任意k・未証明）を証明しない。r ≥ 14はK0902のlive L5
  スポットチェック以外未観測。
- 枝サイズ11,12×r=9..13・cap≥13・k≠3は対象外。状態数はr非不変
  （max_statesは単調増加・SGガード）。
- 観察（σ≤M−1・onset at M・復活12キー）は有限全称であり、
  「観察」として記録する。定理J証明はK0902のスケッチのまま残る。
