---
id: K1154
title: 一様盤REMO計数再帰・全記録Eの周期の完全特徴付け（定理PNE・必要性方向の全称証明）— Tが周期 ⟺ Q(r)|T（全r ≥ 2・最小周期はちょうどQ(r)・万能witness C=1・第一逸脱位相h*(T,r)はC非依存）— K0919 OPEN「r ≥ 10の最小性・必要性方向」を解決
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: [REMO full-record period characterization, theorem PNE, first-failing-phase witness, universal E-side witness C=1]
relations:
- type: depends_on
  target: K0919
  note: 定理PER（十分性・全称）と補題Q（保存条件系のlcmがちょうどlcm(1..r)）が基盤。本項は同じ均一オフセット帰納法の鏡像（保存補題INS・逸脱補題MIS）で必要性方向を全称証明し、K0919の明示的OPEN「r ≥ 10の最小性と必要性方向（周期は必ずQ(r)の倍数）」を閉じる。肯定側アンカーは本項検証器V2がr ≤ 13で再固定
- type: depends_on
  target: K0859
  note: 定理Dの計数再帰（Δ=0一様盤）が対象オブジェクト。V1がK0859 verbatim per-stoneブロック==閉形式双子（3,540組）を再固定
- type: related
  target: K0922
  note: 補題DIV（周期集合のgcd閉包・最小周期は任意の周期の約数）により、V4の全真約数棄却掃引（r ≤ 28・witness C=1）は本項の全称証明に依存しない機械的最小性アンカーとして読める
- type: related
  target: K0925
  note: 生存者列側の機械的最小性（定理S32・r=2..32）。本項の全称必要性は全記録E（敗者全列＋生存者）側のみ。生存者列単独の必要性（有界witness予想）は本項では閉じない
- type: related
  target: K1145
  note: 生存者列側の機械的最小性（定理S48・r=33..48・全1,548,272真約数・witness ≤ 39・窓[1,150]）と本項の万能witness C=1（探索窓不要・全r・全非周期T）の対比。等Qブロック内の生存者witnessストリーム同一性（観察）に対し、E側の第一逸脱位相h*マップはブロック非不変（V6）で、生存者側観察はE側フェーズ構造から自動的には導けないことを機械的に明示
artifacts:
- path: research/experiments/remo-uniform-period-characterization-20261120/report.md
  role: proof
  note: 定理PNEと強形の全称証明（補題INS/MIS・閉形式D_h=T/k_{h-1}・X_h=T/k_{h-1}）・監査数値（h*表・真約数掃引23,249）・生存者側との厳密な分離・限界記述
- path: research/experiments/remo-uniform-period-characterization-20261120/verify_period_necessity.py
  role: verifier
  note: V0-V6の7機械検査: 補題Qアンカー・verbatim==閉形式双子・十分性アンカー・最大真約数棄却r ≤ 48・全真約数掃引r ≤ 28・フェーズ級強形1,450トレース違反0・等Qブロック対比。自己完結・stdlibのみ・決定的・入力ファイルなし・監査を2回in-process生成してbyte一致・所要約3.3秒
- path: research/experiments/remo-uniform-period-characterization-20261120/output/audit.json
  role: data
  note: 監査JSON（14,284 bytes・SHA-256 77d9df88…・7/7 ok・最大真約数ごとのh*表とrごとの真約数掃引内訳を出版）
- path: research/log/2026-11-20-remo-full-record-period-characterization.md
  role: source
  note: 高速レーン研究ログ（宣言→数値整合→検証器構築→出版の記録・K1153→K1154再採番記録・次課題）
scope: 'K0859定理Dの計数再帰E(C,r)（Δ=0一様盤・終端サイズC・r人）の全記録（敗者全列と生存者）について、すべてのr ≥ 2とT ≥ 1で「TがE(・,r)の周期（すべてのC ≥ 1でE(C+T,r)=E(C,r)）⟺ Q(r)=lcm(1..r) | T」が成立（全称証明。十分性はK0919定理PER・必要性は第一逸脱位相witness帰納法の鏡像）。系として最小周期はすべてのr ≥ 2でちょうどQ(r)（K0919の明示的OPEN「r ≥ 10の最小性と必要性方向」を解決）し、周期はちょうどQ(r)の正の倍数。強形: Q(r)∤TならすべてのC ≥ 1でE(C+T,r)≠E(C,r)で、敗者列の第1〜h*-1項は一致し第h*項が最初の不一致（h*(T,r)=保存条件列M_1: r|T・M_h: k_{h-1}k_h|Tの最初の破れで、Cに非依存）。とくにC=1がE側の万能witness。生存者列単独の必要性（K0925/K1145の機械確定r ≤ 48・有界witness予想）は本項では閉じない: フェーズh*の除去ラベル不一致は生存者不一致を含意しない。Δ≠0非一様盤には一切言及しない。等Qブロック内でE側h*マップがブロック非不変であること（{17,18}{41,42}{47,48}）は有限観察（V6）で、生存者側witnessストリーム同一性（K1145観察）の説明は次課題。順位の安定性は扱わない。11×11空盤・クラスフロンティアは本項と無関係でUNKNOWNのまま'
evidence: 'verify_period_necessity.py全チェック合格（7/7・監査二重生成byte一致・コールドラン間byte一致・SHA-256 77d9df88…・CIはaudit.jsonをgit diff pin）。V0: 補題Qアンカー（lcm(r,k(k+1))==Q(r)がr=2..48・M条件合致⟺Q|Tがr=2..32の1,314決定的T探針）。V1: K0859 verbatim per-stone再帰==閉形式双子（r=2..12・C∈[1,30]全数・3,540組）。V2: 十分性アンカー（r=2..13・E(C+Q)=E(C)がC∈[1,25]・E(C+2Q)=E(C)がC∈[1,5]・Q|r!）。V3: 各r=2..48の最大真約数Q(r)/p（p≤r素数）がすべての探針C∈[1,8]+巨大C 3点（2^30+1・2^30+7・10^12+3）で棄却され第一不一致が常にh*(T,r)（4,477組・h*表出版・例: r=10でQ/2→h*=3・Q/5→h*=1、r=48でQ/2→17）。V4: r=2..28のQ(r)全真約数23,249個がwitness C=1で棄却・第一不一致==h*（全称証明に依存しない機械最小性アンカー・K0919 E3のr ≤ 9をDIV引数でr ≤ 28へ拡張）。V5: フェーズ級強形（r=2..20の最大真約数+LCG非周期T・C∈[1,10]の1,450トレース・違反0: h < h*で活性リスト/turn/li/除去ラベル同一・counts offset==D_h=T/k_{h-1}厳密・ell差==X_h=T/k_{h-1}（X_1=T）・k_h|X_h、フェーズh*で活性リスト/turn同一のままliと除去ラベルが不一致でli差 mod k_h == X mod k_h ≠ 0）。V6: 等Qブロック対比（{17,18}は共通素数7個全て・{41,42}は13個全てでh*マップがブロック内で相違する等の有限観察）。定理PNE本体は全称証明で機械チェックは独立検証アンカー。V6と巨大C探針は有限アンカー'
---

# 一様盤REMO計数再帰・全記録Eの周期の完全特徴付け（全称・必要性方向を含む）

## 命題（定理PNE・全称）

K0859定理Dの計数再帰 E(C,r) = (敗者全列, 生存者)（一様盤・終端サイズC・
r人）について、Q(r) := lcm(1,2,…,r) とおくと、**すべての r ≥ 2 と
すべての T ≥ 1** に対し:

> **T が E(·,r) の周期 ⟺ Q(r) | T**

が成立（全称証明）。とくに**最小周期はすべての r ≥ 2 でちょうど Q(r)**
で、周期はちょうど Q(r) の正の倍数。**K0919 の OPEN「r ≥ 10 の最小性と
必要性方向（周期は必ず Q(r) の倍数）」を解決する。**

**強形**。Q(r) ∤ T なら**すべての C ≥ 1 で** E(C+T,r) ≠ E(C,r)。しかも
敗者列の第1〜h*−1項は一致し、**第h*項でちょうど最初の不一致**が生じる。
h* = h*(T,r) は保存条件列（M_1: k_1 = r | T、M_h: k_{h−1}·k_h | T、
h ≥ 2）の最初の破れの番号で、T と r のみで決まり C に非依存。
**C = 1 が E 側の万能witness**（棄却に探索窓が一切不要）。これは生存者側の
「witness ≤ r−1・窓[1,150]」（K0925/K1145）との顕著な対比をなす。

## 証明（必要性方向・K0919帰納法の鏡像）

盤 C と C+T を並走させ、フェーズh開始時の状態 σ_h（in-sync: 順序つき
活性リスト・turn が同一で、全活性者の石数差が一様 D_h）を置く（σ_1 は
自明・D_1 = 0）。活性者数 k_h = r, r−1, …, 2、配分石数の差
X_h = T − k_h·D_h。

- **補題INS（保存）**: σ_h かつ k_h | X_h なら、貧富パターンt・敗者
  オフセット li・除去ラベル・除去後turnがすべて同一で、σ_{h+1} が
  D_{h+1} = D_h + X_h/k_h = T/k_h で成立（K0919定理PERの帰納法そのもの）。
- **補題MIS（逸脱）**: σ_h かつ k_h ∤ X_h なら、活性リストが同一ゆえ
  li′ − li ≡ X_h mod k_h ≠ 0 により**除去ラベルが両盤で相異**。

閉形式は σ接頭辞上で D_h = T/k_{h−1}・X_h = T/k_{h−1}（X_1 = T）で、
保存条件の列は M_1: r | T、M_h: k_{h−1}·k_h | T となり、全体の成立は
ちょうど Q(r) | T（K0919補題Q）。

Q(r) ∤ T のとき h* を最初の破れとすると、INSをフェーズ1〜h*−1に適用して
σ_{h*}、MISがフェーズh*の除去ラベル不一致を与える。**議論はCに
一切依存しない**ので全C ≥ 1で E(C+T) ≠ E(C)。十分性（定理PER）と
合わせて特徴付けと最小周期 = Q(r) が全rで確定する。

## 機械アンカー（7/7合格・SHA-256 77d9df88…）

V0 補題Q（r ≤ 48・1,314探針）→ V1 verbatim==閉形式双子（3,540組）→
V2 十分性（r ≤ 13）→ V3 最大真約数棄却（r ≤ 48・全探針Cで
第一不一致==h*・h*表出版）→ V4 **全真約数掃引 r ≤ 28・23,249個が
witness C=1 で棄却**（全称証明に依存しない機械最小性アンカー・
DIV引数でE3の r ≤ 9 を r ≤ 28 へ拡張）→ V5 **フェーズ級強形
1,450トレース違反0**（証明で使う全恒等式を位相ごとに照合）→
V6 等Qブロック対比（E側h*マップはブロック非不変・有限観察）。

数値例: r=10 の最大真約数 h*: Q/2→3, Q/3→2, Q/5→1, Q/7→4。
r=48: Q/2→17, Q/3→22, Q/5→24, …, Q/47→2。

## 生存者側との厳密な分離

本定理は**全記録E（敗者全列＋生存者）**の主張。生存者列単独の必要性
（K0925/K1145の機械確定 r ≤ 48・有界witness予想）は**閉じない**:
フェーズh*の除去ラベル不一致は生存者不一致を含意しない（h*以降は
ラベルの異なる同サイズ部分ゲームの比較になりσ構造は保存されない）。
またK1145の等Qブロック内生存者witnessストリーム同一性（観察）に対し、
E側h*マップはブロック内で相違する（V6）ため、生存者側観察はE側
フェーズ構造から自動的には導けない。両観察の統一説明は次課題。

## 限界

- Δ=0一様盤（定理D域）のみ。Δ≠0の非一様盤には一切言及しない。
- 生存者列側の全称必要性・有界witness予想はOPENのまま。
- V6と巨大C探針は有限アンカー。全称主張はreport内の証明による。
- 11×11空盤・クラスフロンティアは無関係でUNKNOWNのまま。

## 採番記録

単一オーナー宣言（e5d6e02f・2026-11-20T14:50:48Z）時点では仮番号
K1152を予定していたが、y12 two-token fitting レーンがK1152を
14:51:50Zに出版。K1153に上げてpart1を準備したところ、part1 pushの
競合non-fast-forwardの間に n11 residual23 レーンが「[K1153 part1]」
を14:56:39Zに出版したため、AGENTS.mdの後者优先規則により本項を
K1154へ再採番した（part1実験dirの監査・reportはK1154名で生成し
直し、fetch-back・CIパリティ（別環境での監査再生成byte一致）を
検証済み）。

## 再現

`python3 research/experiments/remo-uniform-period-characterization-20261120/verify_period_necessity.py`
（所要約3.3秒・2回のin-process監査生成でbyte一致・コールドラン間で
byte一致・CI stepが `output/audit.json` を git diff pin）。
