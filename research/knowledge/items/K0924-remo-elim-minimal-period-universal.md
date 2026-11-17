---
id: K0924
title: 定理W（elim(1+d,r)=elim(1,r) ⟺ Q(r)|d・全称証明）と系MPV（敗者全列の最小周期=Q(r)・全r≥2全称）— K0922 witness C=1の全称化・witness機械検証はr=40まで拡張（真約数293,573個全棄却）
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: [theorem W witness C=1, corollary MPV elimination column universal minimal period, uniform offset cascade]
relations:
- type: depends_on
  target: K0919
  note: 定理PER（Q(r)周期の全称証明）・素数冪補題（lcm({r}∪{k(k+1)})=Q(r)）が定理Wの両方向の前提
- type: depends_on
  target: K0922
  note: 補題DIV（周期集合のgcd閉包）の列形式が系MPVの前提。定理WはK0922のwitness C=1有限観察（r≤16）の全称化
- type: depends_on
  target: K0859
  note: 定理Dの計数再帰（Δ=0一様盤・全称）が本定理の対象
artifacts:
- path: research/experiments/remo-elim-minimal-universal-20261117/report.md
  role: proof
  note: 定理W（均一オフセット帰納によるフェーズごとの敗者一致条件カスケード）と系MPVの全証明・9機械チェックの定義
- path: research/experiments/remo-elim-minimal-universal-20261117/verify_remo_elim_minimal_universal.py
  role: verifier
  note: M0-M8（決定的・stdlibのみ・per-r checkpointでresumable・--no-cacheで全再計算約3分）
- path: research/experiments/remo-elim-minimal-universal-20261117/output/remo_elim_minimal_universal_audit.json
  role: data
  note: 監査JSON（sha256 394e2cf0…・11,730 bytes・3回実行でbyte同一・M6生存者列C=1失敗リスト全件）
---

## 定理W（全称・証明つき）と系MPV（全称・証明つき）

K0859定理Dの計数再帰 E(C,r)（Δ=0一様盤）の敗者全列
elim(C,r) について:

1. **定理W**: すべての r ≥ 2 と d ≥ 1 に対して
   **elim(1+d, r) = elim(1, r) ⟺ Q(r) | d**。証明は E(1+d) と
   E(1) の均一オフセット比較帰納: フェーズ1の敗者一致 ⟺ r|d、
   そのとき一様オフセット D_2 = d/r。以降、フェーズh（h≥2）で
   「一様オフセット D_h = d/(r−h+2) のもとで 敗者一致 ⟺
   (r−h+2)(r−h+1) | d」がカスケードし、全フェーズ一致には
   r|d かつ k(k+1)|d（k=2..r−1）が必要。K0919のlcm恒等式で
   Q(r)|d が閉じる。逆方向はK0919定理PER。
2. **系MPV**: **敗者全列のC方向最小周期はすべての r ≥ 2 で
   ちょうど Q(r) = lcm(1..r)**。K0922定理MP（機械・r≤16）の
   うち敗者全列分を全称定理へ昇格。証明は定理W + K0922補題DIV
   の列形式（gcd閉包・Bezout上向き適用）: m_e | Q(r) が真約数
   ならC=1で棄却されて矛盾。
3. **発散位置の構造**: elim(1+d) と elim(1) の最初の発散フェーズは
   r∤d→フェーズ1 / r|d→最小のh≥2で(r−h+2)(r−h+1)∤d と
   正確に予測できる（真約数の「深さ」=約数条件の最初の破れ）。

## 機械検証（9/9合格・監査JSON sha256 394e2cf0…）

M1 witness C=1 elim列 r=2..16（真約数1,181個全棄却・K0922の
独立再現）・M2 r=17..40への直接拡張（真約数292,392個全棄却・
各dは評価2回の直接比較で窓走査不要・r=40でQ≈5.34e15）・
M3/M3b 最初の発散フェーズ予測118,486件不一致0・M4 同値性
7,503件違反0・M0 lcm恒等式39件・M5 周期アンカー39件・
M6 生存者列C=1失敗リスト（r=2..16全件）・M8 第1敗者閉形式
elim(C,r)[0]=C%r全評価表明。

## 限界

- Δ=0一様盤・敗者全列限定。非一様盤には言及しない。
- **生存者全列の最小周期はK0922の機械結果（r≤16）のまま**。
  全称性はOPEN（C=1は生存者列witnessにならないdが存在・M6記録。
  r≥17の生存者列最小性は窓走査が必要で未到達）。
- 形式的証明（Lean等）には未展開。機械検証は証明ステップの
  数值的整合性の独立確認。
- P(C)素数予想（K0922）は予想のまま。11×11空盤・クラス
  フロンティアは無関係でUNKNOWNのまま。

## 再現

`python3 verify_remo_elim_minimal_universal.py`（checkpoint利用・
`--no-cache`で全再計算約3分・stdlibのみ・決定的）。3回実行
（--no-cache含む）で監査JSON byte同一を確認済み。
