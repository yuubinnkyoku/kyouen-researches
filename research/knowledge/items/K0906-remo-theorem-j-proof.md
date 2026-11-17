---
id: K0906
title: 定理Jの全称証明（ラベル閉包法）— sv/detはr ≥ max(M,2)で一定・fl={C_i mod r}（正準領域）・σ ≤ M−1・広域版(ii′)（E=第1飽和可能容量集合）・補題C1′（剛体形）と補題FLの成立域確定（e_j ≥ 1）
kind: proposition
status: proved
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [Theorem J universal proof, label closure method, Lemma C1 prime rigid form, Lemma FL domain boundary, Theorem J wide-domain refinement]
relations:
- type: proves
  target: K0902
  note: K0902が予想として定式化した定理J（sv/detはr ≥ Mで一定・fl={C_i mod r}）を全称証明。証明はラベル閉包法（L1 phase-1のr非依存性・L2 ファントム吸収カスケード・L3 ラベル閉包・L4 接着）で、K0902スケッチの未完点(a)(b)(c)をプレイライン分解なしで解消し、見逃されていた境界ケースr=C_Y=Mもファントム吸収で処理。K0902の条件付き閉包（cap≤10 rレーン）を無条件化
- type: depends_on
  target: K0902
  note: 定理Jの定式化・証明スケッチ・補題C1・r=13 committed列（packed記録をJ0-J4で読む）
- type: generalizes
  target: K0904
  note: K0904の全715キー有限検証「σ(key)≤M(key)−1」を定理J(iii)として全称化（任意k・任意r ≥ max(M,2)・広域版でも成立）。K0904の「onset at M」観察とも整合（r < max(M,2)は定理の範囲外）
- type: depends_on
  target: K0864
  note: 補題FL（fl={C_i mod r}・正準領域）の根における直接再導出（L4・到達可能性ステップは共有原子容量C_j−e_j<C_jまたはexcl_Y初手でe_j ≥ 1が本質的）とcommitted列での冗長アンカー（J2・79,315対違反0）
- type: extends
  target: K0864
  note: 補題FLの成立域を確定: {C_i mod r}形は正準領域（単一原子非空e_j ≥ 1）に限り、広い領域（C_i ≥ 1のみ）では反例atoms=(0,0,0,0,1,1,0)（sizes (1,1,2)）でE={1}⊊{1,1,2}・fl≠{C_i mod r}。精緻化形(ii′) fl(r)={c mod r : c∈E}（E=第1飽和可能枝容量集合・盤面のみで決まるr非依存）が広域の正しい形
- type: depends_on
  target: K0898
  note: r=12 committed列（packed記録・J0-J4で5列比較の相手側）
- type: depends_on
  target: K0897
  note: r=11 committed列（同上）
- type: depends_on
  target: K0895
  note: r=10 committed列（同上）
- type: depends_on
  target: K0893
  note: r=9 committed列（同上）
- type: depends_on
  target: K0862
  note: cap≤10正準領域15,863プロファイル・Burnside (84494,3478,125)・列挙機械（verbatim）
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりプロファイルの定理が実現盤面すべてに転写される
- type: depends_on
  target: K0859
  note: REMO規則の計数ゲーム（カスケード・maximal・next_active）が証明対象のゲーム
artifacts:
- path: research/experiments/remo-theorem-j-proof-20261117/report.md
  role: proof
  note: 定理J主張（正準領域(i)(ii)(iii)・広域版(i)(ii′)(iii)）・L1-L4証明・補題C1′（剛体形・e_j ≥ 1依存と反例）・補題FLの成立域（E集合と反例証人）・系1-4（cap≤10 rレーン無条件閉包・σ≤M−1全称化・cap≤12残4スイープ・r=M−1鋭さ2022/2041）・機械検証内容・限界・再現
- path: research/experiments/remo-theorem-j-proof-20261117/verify_theorem_j.py
  role: verifier
  note: 自己完結検証器（stdlibのみ・決定的・新規スイープなし・head+K0902機構verbatim+tailの二重assemble byte同一）。7機械チェック（B1/J0/J1/J2/J3/J4/SG）+live 9項目（L0/J5/J5b/J6/J7a/J7b/J8/J9/L9）・新規独立実装の第1イベントカスケードシミュレータ（LC1/LC2）と部分ゲームDFS（L3/L4接着）・約95秒・二重実行で監査byte同一
- path: research/experiments/remo-theorem-j-proof-20261117/output/theorem_j_audit.json
  role: audit
  note: 監査JSON（sha256 60544b07…・検証器自身のsha256・5列のpacked sha256込み）
evidence: 'verify_theorem_j.py全チェック合格（二重assemble byte同一・二重実行で監査JSON byte同一・約95秒）。機械チェック: B1 Burnside (84494,3478,125)→15,863。J0 5つのcommitted packed列 r=9..13（K0893/K0895/K0897/K0898/K0902）完全性（各15,863・添字連続・states>0）・sha256記録。J1 sv/detがr ≥ max(M,2)の全committed列で不変（適格71,987比較・違反0・σ違反0・M分布4,330/4,205/7,328）。J2 fl={C_i mod r}が5列×15,863=79,315対で違反0。J3 r > Mでfl不変（60,454対・違反0）。J4 K0902 ARITH集合等式の再導出（r13↔r10 fl差=maxC=10集合7,328・r13↔r9 fl差=maxC≥9集合11,533・r13↔r9 sv差=同一7,328集合・他sv差0）。SG 状態数非不変ガード（741,630 vs 666,030）。live: L0 cap≤7全域2,048判定 mask twin==committed r=13記録。J5 cap≤7×r三つ組 sv/det不変+FL+σ（6,144判定違反0）。J5b cap≤5 verbatim==mask twin（1,038判定）。J6 r=M−1鋭さ（2,022/2,041変化・witness記録）。J7a k=2正準全域56プロファイル・J7b k=4電池22プロファイル。J8 サイズ11/12アンカー14プロファイル×r∈{M,M+1,M+2}（42判定・r=13,14はcommitted列の外の新アンカー・N≤17）。J9 カスケードシミュレータ（独立実装）: プレイ9,684（正準・cap≤5全域346）+2,581（特別電池259・空単一原子k=2/k=3/k=4）でpost-cascade正規化結果の全r同一・正準プレイ剛体形（C1′）違反0・特別電池の剛体形違反91プレイ（すべてe_j=0起因・witness記録）・根fl再導出（正準{C_i mod r}・特別はE精緻化形でFL領域証人atoms (0,0,0,0,1,1,0) sizes (1,1,2) E={1}⊊{1,1,2}を自動検出）・特別電池259プロファイルでsv/detのr不変とσ≤M−1を直接検証（広域版(i)(iii)の有限確認）。L9 接着検証: シミュレータ+部分ゲームDFSの根値がmask twin・verbatimエンジンと全一致（cap≤4全域117+k=2電池56+k=4電池22=195対・3エンジン一致）。検証器は証明の文章を検証するものではなく、定理の有限予測の全面的再導出と証明中間対象の独立実装検証である。全称証明本体はreport.mdのL1-L4'
scope: 'REMO計数ゲーム（K0859規則・K0861定理E′の軌道簡約ゲーム）のk枝atomプロファイル（k ≥ 1任意・枝容量C_i ≥ 1・M=max C_i）とr ≥ 2人について: 正準領域（すべての単一原子が非空e_j ≥ 1・committed列と同一領域）で(i) sv/detはすべてのr ≥ max(M,2)で一定、(ii) fl(r)={C_i mod r}（ゆえにr > Mで一定値{C_i}）、(iii) 可能生存者ラベルσ ≤ M−1。広い領域（単一原子が空を許すC_i ≥ 1のみ）では(i)(iii)はそのまま成立し(ii)は精緻化形(ii′) fl(r)={c mod r : c∈E}（E=第1飽和可能枝容量集合・r非依存・正準領域でE={C_i}）になる。定理E′経由でプロファイルを実現する任意の盤面に全称的に及ぶ。状態数・順位・消滅順序のr不変性は主張しない。r < max(M,2)は範囲外'
---

# 定理Jの全称証明（ラベル閉包法）

## 命題（全称・proved）

K0902が予想として定式化した定理Jを、プレイライン分解を使わない
**ラベル閉包法**で全称証明する（k任意・正準領域）:

- **(i)** sv/det は r ≥ max(M,2) で一定。
- **(ii)** fl(r) = {C_i mod r}（補題FLと同じ値を根で直接再導出）。
  r > M では一定値 {C_i}。
- **(iii)** σ ≤ M−1。

**広域版（C_i ≥ 1のみ）**: (i)(iii) は修正なしで成立（証明は単一原子
の非空性を使わない）。(ii) は (ii′) fl(r) = {c mod r : c ∈ E}
（E = 第1飽和可能枝容量集合・盤面のみで決まる r 非依存・
E ⊆ {C_i}・正準領域で E = {C_i}）に置き換える。

証明構造: **L1**（第1イベントまでのプレイ木は盤面のみの関数で
r非依存・イベント深さは t = C_Y ≤ M ≤ r・着手者 P_0..P_{C_Y−1}
相異別・敗者は P_{C_Y mod r}・境界 r = C_Y = M は P_0）→
**L2**（ファントム吸収カスケード: 0石ラベルの除去は盤面を変え
ないので maximal が持続し、カスケードは例外なくファントム
C_Y..r−1 を喰い、石持ち除去列・盤面推移・|active| 推移
（C_Y−j）は全 r ≥ max(M,2) で同一 → post-cascade 正規化結果は
ラベル < C_Y の中だけで書かれ r 非依存）→ **L3**（ラベル閉包:
active ⊆ {0..a−1} の状態の遷移は next_active が不活性ラベルを
飛ばすことから r ≥ a で r 非依存 → 部分ゲーム値は r 非依存）→
**L4**（接着: sv = ∪プレイpost値・fl = {c mod r : c ∈ E}・正準領域
で E = {C_i}（他枝 j の先飽和は共有原子容量 C_j − e_j < C_j で
不可能・または excl_Y 初手が j を永久に maximal にできない）・
σ < C_Y ≤ M）。

## 成立域の確定（本項の新規知見）

1. **補題C1′（剛体形）**: 正準領域ではカスケードは必ず P_0 で
   停止し、post-cascade 状態は剛体形（C_Y=1→終端P_0・C_Y=2→
   終端P_1・C_Y≥3→各ラベル1..C_Y−1に1石・active={1..C_Y−1}・
   mover=P_1）。容量不等式は e_j ≥ 1 が本質的で、**広い領域では
   偽**（反例 atoms (0,1,1,1,0,0,1)・sizes (2,3,2)・プレイ
   (e2,s12,s123) で P_0 除去後に枝1が飽和しカスケードが継続。
   J9特別電池で剛体形違反91プレイを分離・正準9,684プレイは違反0）。
   定理Jの証明にはC1′不要（L2の弱い形で十分）。
2. **補題FLの成立域**: fl = {C_i mod r} の到達可能性ステップ
   （各枝を第1飽和枝として強制）は excl_Y 初手または共有原子
   容量 C_j − e_j < C_j を使い、**e_j ≥ 1 が本質的**。広い領域では
   反例 atoms (0,0,0,0,1,1,0)（sizes (1,1,2)）で合法初手（s13/s23）
   が即座に枝1・枝2（容量1）を飽和させ、枝3（容量2）は決して
   第1飽和枝になれない: E = {1} ⊊ {1,1,2}・fl ≠ {C_i mod r}。
   精緻化形 (ii′) が広域の正しい形。K0864・K0902の主張は
   committed列と同じ正準領域の内部なので影響を受けない。

## 系

1. **cap≤10 rレーンの無条件閉包**（K0902の条件付き閉包を確定）。
2. **σ ≤ M−1 の全称化**（K0904の715キー有限検証を定理J(iii)として
   回収・広域版でも成立）。
3. **cap≤12の残作業は4本の有限スイープ**（サイズ11,12×r=9・
   サイズ11,12×r=10・サイズ12×r=11・r ≥ Mアンカー1列。
   fl列は全rで純算術でスイープ不要）。J8電池（サイズ11/12・
   r最大14・N ≤ 17・14プロファイル×42判定）が最初の有限アンカー。
4. **境界の鋭さ**: r = M−1 では cap≤7 の M ≥ 3 プロファイル
   2,041個中2,022個で sv/det が変化（J6・witness記録）。
   下界 max(M,2) はこの領域ではほぼ最良。

## 根拠

- 全称証明本体: report.md の L1-L4（数学的文章証明・検証器は
  これを検証しない）。
- 検証器: 上記 evidence の7機械チェック+live 9項目全合格・
  二重assemble/二重実行 byte同一（監査 sha256 60544b07…）。
  証明の中間対象（第1イベント深さ・post-cascade正規化状態・
  根flの和集合）を新規独立実装のカスケードシミュレータと
  部分ゲームDFSで検証し、mask twin・verbatim engine（K0902
  機構verbatim）と3エンジン一致（195対）。
- committed列: r=9..13 の5列（15,863プロファイル each）上で
  定理の全有限予測を再導出（J1: 71,987適格比較違反0・J2: 79,315対
  FL違反0・J3: 60,454対・J4: ARITH集合等式・SG: 状態数非不変）。

## 限界

- ラベル（det/sv/fl）のみ。状態数・順位・消滅順序は r 不変でない
  （SGガード）。
- (ii) の {C_i mod r} 形は正準領域限定。広域は (ii′)。E = {C_i} となる
  e_j ≥ 1 以外の特徴づけは未解決（e_j = 0 でも E = {C_i} のプロファイル
  は特別電池中に多数ある）。
- r < max(M,2) は範囲外（系4の通り一般に変化）。
- サイズ11/12 × r=9..13 は J8 電池（N ≤ 17）でしか有限検証して
  いない（定理自体は全称的に覆う。残4スイープは系3）。
- 11×11空盤・二石root・クラスフロンティアは本項と無関係で
  UNKNOWNのまま。
