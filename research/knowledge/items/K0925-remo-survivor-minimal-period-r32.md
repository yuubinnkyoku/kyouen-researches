---
id: K0925
title: 生存者列最小周期がr=2..32で機械確定（小witness棄却・全72,397真約数・witness C≤150・観測最大28） — 定理Wの全C強化（elim列は全Cがwitness）・h*(Q/p)算術・有界witness観察（wit_max_sv ≤ r−1）
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: [theorem S32 survivor minimal period r32, small witness rejection, theorem W all-C strengthening, hstar Q/p arithmetic, bounded witness observation]
relations:
- type: depends_on
  target: K0924
  note: 定理W（C=1版）と系MPV（elim列の全称最小周期）が本項の前提。本項は同一の均一オフセット帰納のC非依存性を明示して全C版（定理W+）へ強化し、W1/W2のC=1棄却はK0924 M1/M2の相互検証
- type: depends_on
  target: K0922
  note: 補題DIV（周期集合のgcd閉包・列汎用）により生存者列の真約数棄却から最小性が確定。r≤16のwit_maxとd=Q/pの[w_elim,w_sv]表が本項W5と完全一致
- type: depends_on
  target: K0919
  note: 定理PER（⟸方向）と条件lcm=Q(r)の素数冪補題が定理W+の前提。W0/W3が機械アンカー
- type: depends_on
  target: K0859
  note: 定理Dの計数再帰（Δ=0一様盤・全称）が本定理の対象。verbatim再帰はTWINの照合対象
artifacts:
- path: research/experiments/remo-uniform-witness-theorem-20261117/report.md
  role: proof
  note: 定理W+（全C強化のメモ証明）と定理S32（小witness棄却）・h*算術の記録・8機械チェックの定義
- path: research/experiments/remo-uniform-witness-theorem-20261117/verify_remo_uniform_witness_theorem.py
  role: verifier
  note: W0-W6+TWIN（決定的・stdlibのみ・新規スイープなし・per-(check,r) checkpointでresumable・--no-cacheで全再計算）
- path: research/experiments/remo-uniform-witness-theorem-20261117/output/remo_uniform_witness_theorem_audit.json
  role: data
  note: 監査JSON（sha256 b3733ed5…・24,959 bytes・assemble二重実行と2回の別プロセス実行（うち1回--no-cache全再計算）でbyte同一）
---

## 定理W+（全称・全C）と定理S32（機械・r=2..32）

K0859定理Dの計数再帰 E(C,r)（Δ=0一様盤・K0919定理PERの対象
と同一）について:

1. **定理W+（全称・全C・証明つき）**: すべての r ≥ 2, C ≥ 1,
   d ≥ 1 で elim(E(C+d,r)) = elim(E(C,r)) ⟺ Q(r) | d。K0924
   定理W（C=1版）の全C強化: 均一オフセット帰納（条件
   M_1: r|d、M_h: k_h(k_h+1)|d・lcmはちょうどQ(r)・最初の失敗
   h* の前で両runはフェーズロックし一様整数オフセット
   D_h = d/(k_h+1)・ℓ差 X_1=d, X_h=d/(k_h+1)、h* で敗者添字が
   X_{h*} mod k_{h*} ≠ 0 だけずれる）の帰納ステップは**Cを一切
   参照しない**ため、Q(r) ∤ d なら差は**すべてのC ≥ 1**で同じ
   位置 h* に生じる。elim列では全Cがwitness。
2. **系1（全称・K0924系MPVと一致・独立再導出）**: elim列の最小
   周期は全 r ≥ 2 でちょうど Q(r)・周期=Q(r)の倍数全体。ペア列
   も同様。W1/W2/W3は K0924 M1/M2 の r ≤ 24 部分を独立に再現
   （相互検証）。
3. **定理S32（機械・r=2..32・生存者列の拡張）**: 生存者列の
   最小周期は r=2..32 の全rでちょうど Q(r)。K0922補題DIV
   （最小周期はQ(r)の約数）により**各真約数を1つのwitness Cで
   棄却すれば十分**で[1,Q(r)]完全走査は不要。全真約数72,397個
   （Q(32)≈1.44e14の18,431個を含む）がすべて witness C ≤ 150
   で棄却（観測最大28=r=29・フォールバック窓[151,1500]不使用）。
   K0924が「r≥17の生存者列最小性は窓走査が必要で未到達」と
   残した部分を手法転換で解決。r ≤ 16 は K0922 出版監査と
   完全一致。
4. **h* の算術（d=Q/p）**: k(k+1)|Q が常に成立するため
   h*(Q/p) = 1（v_p(r)=v_p(Q)のとき）以外は
   r+1−max{k≤r−1: v_p(k(k+1))=v_p(Q)} と閉形式で決まる
   （r=2..24の全(p,r)で機械確認・不一致0）。

## 有限観察（主張は限定的）

- **有界witness観察（r≤32）**: wit_max_sv ≤ r−1 が r=2..32
  全域で成立（1,1,2,3,3,3,6,6,6,10,10,9,9,9,8,12,12,9,9,9,9,
  8,8,20,20,18,18,28,28,27,25）。witness最大のdは r=23
  （d=32760=Q/163438）を除きすべて Q/m 型で h*=1（M_1失敗）に
  集中。「witnessが常に有界（たとえばC≤r−1）なら生存者側の
  全称最小性も補題DIVで閉じる」を有界witness予想として記録
  （証明なし）。
- **C=1が生存者witnessにならない真約数**は多数（r=32で
  18,431個中9,146個・監査JSON記録）。elim列（全Cがwitness）
  との対照。

## 機械チェック（8/8合格）

W0（Q(r)ピン・条件lcm恒等式 r=2..32）/ W1（C=1・全真約数9,813
ペア・r=2..24・最初の差=h*完全一致・K0924 M1/M2相互検証）/
W2（d∈[1,300]全数・6,665非倍数ペア）/ W3（全C強化48,858
ペア+PERアンカー）/ W4（帰納データ全段検査3,801ペア・違反0・
フェーズ痕跡の直接比較）/ W5（定理S32・生存者r=2..32・K0922
出版ピン完全一致）/ W6（h*算術・不一致0）/ TWIN（verbatim==
閉形式双子4,692ペア）。監査JSONは assemble二重実行・2回の
別プロセス実行（うち1回--no-cache全再計算）でbyte同一
（sha256 b3733ed5…）。

## 限界

- Δ=0一様盤（定理D域）限定。非一様盤には一切言及しない。
- 定理S32は r ≤ 32 の機械確定。生存者側の全称は OPEN
  （有界witness予想が残課題）。
- 11×11空盤・クラスフロンティアは無関係でUNKNOWNのまま。
- K0922のP(C)素数予想には本項から新しい光を当てていない
  （別課題）。

## 再現

`python3 verify_remo_uniform_witness_theorem.py`（checkpoint
利用で高速・`--no-cache`で全再計算約2-4分・stdlibのみ・決定的）。
2回実行で監査JSON byte同一を確認。
