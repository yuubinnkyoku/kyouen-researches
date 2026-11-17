---
id: K0902
title: 3枝REMO決定性のr=13不動列＋定理J（予想）— 5列連続決定性分類不動点（r=9..13）・3列連続全ラベル不動点（r=11..13）・ARITH（FL wraparound集合等式: r13↔r10差=maxC=10集合7,328・r13↔r9差=maxC≥9集合11,533）・r=14/17スポット一致（L5）・補題C1（カスケード停止・証明付き）・定理Jはsv/detがr≥Mで一定という未証明の予想として定式化
kind: proposition
status: computed
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [three-branch REMO r=13 invariance column, Theorem J]
relations:
- type: depends_on
  target: K0898
  note: r=12境界の次の列。STASIS5チェックでK0898出版packed記録（15863レコード）とr=13記録のdeterminedフラグ・生存者mask・第1敗者maskが全プロファイル一致（0/0/0差分・全ラベル不動点のr=12↔r=13継続）・34キー境界集合・per-key分割・生存者構造の完全同一を直接検証
- type: depends_on
  target: K0897
  note: r=11境界。r=11 packed記録もSTASIS5で読み5列detフラグ一致とr=11↔r=13全ラベル一致（0/0/0）を検証
- type: depends_on
  target: K0895
  note: r=10境界。ARITHチェックでr=10 packed記録の第1敗者ラベル差集合がmaxC=10プロファイル集合と正確に一致（7,328件・集合等式）するのを検証
- type: depends_on
  target: K0893
  note: r=9境界。ARITHチェックでr=9 packed記録の第1敗者ラベル差集合がmaxC≥9プロファイル集合と正確に一致（11,533件・集合等式）するのを検証
- type: depends_on
  target: K0864
  note: 補題FL（全称証明済み）のr=13冗長アンカー+ARITH列間交差検証（fl={C_i mod r}のwraparound予測が3つのcommitted列で集合等式として成立）
- type: depends_on
  target: K0862
  note: 同一cap≤10領域（15863プロファイル・715キー・Burnside 15863）
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりプロファイルverdictは実現盤面すべてに移る
- type: depends_on
  target: K0859
  note: Δ=0プロファイル728個が定理D再帰のr=13列（検証器内verbatim計算・出版表84エントリはr=2..8で一致確認）
- type: depends_on
  target: K0872
  note: 剰余類計数のr=13初計数（単一55・二重330・三重330・純算術・分割はr=10..r=12と同一）。r=13>最大枝サイズ10のためwraparound無し・cap≤10領域の剰余計数は自明化。「非坍縮⇒2剰余」初反例(6,8,9)×γ=0..3がr=13でも3剰余mixedとして5列目も存続
- type: depends_on
  target: K0874
  note: 失敗族状態行列52キーのr=13列。r=3..10出版失敗56キーのr=13運命（FATE56）を確定、34キーのmixed存続と22キーの一様非決定（4列連続無事象）を確認
artifacts:
- path: research/experiments/remo-k-branch-cap10-r13-invariance-20261117/report.md
  role: proof
  note: r=13列（34キー5列連続同一・センサス不変・max_states 741,630）・STASIS5（5列分類不動点+3列全ラベル不動点）・ARITH（FL wraparound集合等式）・定理J（予想）の定式化と証明スケッチ・補題C1（カスケード停止・証明付き）・SG過大主張ガード・限界の説明
- path: research/experiments/remo-k-branch-cap10-r13-invariance-20261117/verify_remo_k_branch_cap10_r13_invariance.py
  role: verifier
  note: 自己完結検証器（stdlibのみ・決定的・13機械チェック+live L1-L5・二重実行byte同一）。K0898検証器の機械変換+Python mask twinのflat bytes再符号化（意味保存・L1/L2でlive再検証）+新規L5（r=14/17層化496判定×2）
- path: research/experiments/remo-k-branch-cap10-r13-invariance-20261117/output/js_cap10_r13.packed.jsonl
  role: data
  note: r=13完全スイープpacked記録（15863レコード・[i, sv_mask, fl_mask, states]形式）
- path: research/experiments/remo-k-branch-cap10-r13-invariance-20261117/output/remo_k_branch_cap10_r13_invariance_audit.json
  role: audit
  note: 監査JSON（13機械チェック・検証器run()がbyte照合）
---

# 3枝REMO決定性のr=13不動列＋定理J（予想）

## 命題（有限・computed）

cap≤10領域（正準形15,863プロファイル・715キー）のr=13列は:

1. **mixedキー=7族34個**（r=9/r=10/r=11/r=12と完全同一・5列連続）。
   34キーすべて決定側生存者P_5、非決定側可能生存者集合・per-key
   分割計数も完全同一。センサス98/583/34不変。Δ=0（728プロファイル）
   は定理D r=13列に全一致。FL違反0。
2. **全ラベル不動点の継続**: r=12・r=11の両committed列とr=13列が
   全プロファイルでdet/生存者mask/第1敗者mask一致（0/0/0・両比較）。
   5列連続（r=9..13）決定性分類不変・3列連続（r=11..13）全ラベル
   不動点。段階的収束: det→r=9、生存者mask→r=10、第1敗者mask→r=11
   で固定。
3. **ARITH**: r=13↔r=10第1敗者ラベル差集合=maxC=10集合（7,328件）、
   r=13↔r=9差=maxC≥9集合（11,533件）、生存者ラベルのr=13↔r=9差
   も同一のmaxC=10集合（7,328件）ちょうど、の3集合等式（補題FLの
   wraparound算術の列間交差検証・新種・生存者maskのr=9→10収束は
   第1敗者のr=10→11収束と同じ7,328プロファイルに局在）。
4. **max_states 741,630**（≠r=12の666,030）: 状態数はr不変でない
   （SGガード・列不変性はラベルのみが対象）。
5. **FATE56**: r=9..12でmixedの34キーはr=13でもmixed存続、22キーは
   一様非決定のまま（4列連続無事象）。剰余計数55/330/330（r=10..12
   と同一・純算術）。

## 定理J（予想・未証明）

枝サイズC_1..C_k・M=max C_iに対し、(i) svとdetはすべてのr ≥ Mで一定、
(ii) fl={C_i mod r}（補題FL・K0864全称証明済み）ゆえr > Mで一定。
M ≤ 10 < 13のcap≤10領域では、r=13列=r=12列（本項で完全検証）・
r=14/17層化サンプル496判定×2一致（L5）が予想の有限検証。**予想が
正しければcap≤10領域のrレーンは閉じる**（r ≥ 13の全列=r=12列・
r ≥ 14スイープ不要）。本項はこの閉包を条件付きでのみ主張する。

補題C1（カスケード停止・証明付き）: star[Y]内の局面では単一原子の
非空性（C_j ≥ 1+共有石）より他枝jは飽和できず、枝Y飽和後のカスケード
は0石敗者の連鎖の後に必ず石持ち敗者P_0で停止し、P_0の除去後に飽和
枝は存在しない。これが定理J証明スケッチの第一段（report.md）。

## 対象範囲

- 有限部分はcap≤10・r=13の完全列挙（定理E′で実現盤面一般に適用）。
- 定理Jはk枝一般・r ≥ M一般を量化するが**未証明**（スケッチのみ）。
- 枝サイズ11,12×r=9..13は未走査のまま（定理Jは全称適用を志向するが
  アンカー列なし）。
- 順位・消滅順序のr不変性は主張しない（順序はr不変でない）。

## 根拠

- 完全スイープ: committed JS mask engine（K0898エンジンのbyte同一
  コピー）で15,863プロファイルをr=13で完全計算（予算スキップ0）。
- 自己完結検証器: 13機械チェック全合格+live L1-L5・二重実行byte
  同一（監査JSONのcommitted file byte照合込み）。
- 独立検証: Python mask twin（compact再符号化・意味保存）がverbatim
  engineとcommitted JS記録の双方に全一致（cap≤7全域+層化サンプル）。

## 限界

- 定理J未証明。条件付き閉包。無条件確定はr=9..13の5列+r=14/17の
  スポットまで。
- STASIS5/ARITH/FATEは有限観察。一般則は定理Jが証明されるまで予想。
- 11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4は
  本項と無関係でUNKNOWNのまま。
