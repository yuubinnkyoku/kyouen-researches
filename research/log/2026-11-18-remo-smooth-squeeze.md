# 2026-11-18 remo smooth-hit SQUEEZE構造（高速レーン・K0961）

## 経緯

- K0960レジューム(i)(iii)として、(a) ODDCAP/PAIR-MINの構造精密化、(b) kodd≥4の
  t上界、(c) kodd=3の特徴付け、を予定して開始。
- 奇素数から全奇約数への梯子論法の一般化（TWO-ZONE）を紙上で確定後、
  N=(M+1)k₀+2M−κ恒等式から余因子評価（CO-FACTOR）・拡張窓空性（EFFECTIVE-WINDOW）を
  導出。EFFECTIVE-WINDOWは当初 k₀ ≥ 2M−κ の条件付きと考えていたが、証明を書き
  直すと d ≤ M+1+(M−κ−1)/(k₀+1) の評価だけで t≥1 全域で閉じることが判明
  （条件不要の強化・auditは旧条件付き+条件外観測の両方を記録）。
- kodd=3: compliance（2^a p₃ ≤ M−1）だけで全約数が「≤ M−1 か > k₀」に分類され
  窓が必ず空になること（CHAR-3⟸・窓検査不要）に気づき、双方向特徴付けを確定。
- kodd=4: case A判別（K4-A）・交叉対二分法・3分岐のt上界（K4-CAP）を紙上で導出。
  (β)分岐は「t ≤ 2^a−1」ではなく t < 1 で常に空であることも判明（強化）。
  (γ)の鋭い上界 t·2^{2a}p₁² ≤ M−2 は κ≥1 で証明され、センサスγ全413行がκ≥1。
- squeeze_audit.py（24述語・prime-Y walk 34素数・composite-Y walk 33素数・engine錨）
  を実装し、出版10,886行への全数検査・walk再走査で0違反・0失敗を確認。
  冷再実行で出力byte同一（決定性）。
- composite-Y walkで「窓空かつσ_Z≠1」のphantom候補676件（dead 610 + live 66）を
  観測し、K0956 HIT-ARITHの「窓空 ⟺ σ_Z=1」が[Y ok]クラス限定であることを
  engine錨で確定（読みの精密化・出版smoothヒット列は全て素数Y域なので無影響）。

## 本日の成果

1. **TWO-ZONE（全称・t≥2）**: 奇約数qは 2^a q ≤ M−1 か q > k₀ のみ
   （ODDCAPの全奇約数への一般化・zone 2の実在例 M=1997 337·719=242,303 > k₀）。
2. **EFFECTIVE-WINDOW（全称・t≥1・条件不要に強化）**: 約数は拡張窓
   [M, (M+1)k₀/(M−1)) に不存在。系PAIR-MIN+でK0960 PAIR-MINを
   (1+2/(M−1))倍強化。CO-FACTOR（余因子 > X̄）はregime恒等式の一行系。
3. **SQUEEZE-3（全称）**: kodd=3∧compliantで p₁p₂ > X̄・
   t ≤ ((M−1)p₁p₂−1)/(M(M+1))（floor到達26/899・argmax ρ=0.99725@1997）・
   p₁p₂ ≥ Y+1・深部cap t·M·(M+1)·2^{2a} ≤ (M−1)³−2^{2a}
   （DEEP-CAP case Aの(M−1)/(M+1)因子分厳密化）。
4. **CHAR-3（特徴付け）**: t≥2・[Y ok]で「kodd=3ヒット ⟺ compliant」。
   compliantだけで窓が必ず空（窓検査不要・合成Y域でも511/511）。
   t=1は⟸片方向のみ（非compliantヒット1,111行実在）。
5. **K4-A・K4-CAP（全称）**: kodd=4は全てcase Aで、3分岐
   α: t < ((M−1)^{3/2}/2^{3a/2}+1)/M・β: 空（t < 1・強化）・
   γ: κ≥1で t·2^{2a}p₁² ≤ M−2。まとめ t < max(√M/2+1/M, (M−2)/12)
   （κ≥1では(M−2)/36）。DEEP-CAP M/4のγ行側9倍。実測 α 139・β 0・γ 413・B 0。
6. **機械検証**: 24述語0違反（10,886行・N独立再因数分解）・engine錨
   474+40+25件0失敗・prime-Y walk 34素数が出版と完全一致・決定性（冷再実行byte同一）。
7. **phantom観測とHIT-ARITH適用範囲の確定**: composite-Y域の窓空非ヒット676件
   （engine錨25/25でσ_Z≠1）。hitの定義はσ_Z=1であり、窓空との同値は[Y ok]限定。
   素数Y域のphantom不存在（dead排除）は証明付き。

## 判断メモ

- 有限実験（予想2件・phantom集計・κ=0不在観測）と全称定理を明確に区別した。
  予想「kodd=4 ⟹ t < √M」「kodd ≥ 5 ⟹ t ≤ 3」は0違反だが未証明のまま
  （γの理論上界(M−2)/36が√Mを超えるM>1296域で有意義・次課題）。
- K0960のPAIR-MIN・DEEP-CAPはすべて本項の下位系として回収され、
  出版済み主張に後方互換（強化のみ・撤回なし）。
- push時のHEADはe9957932（並走n11レーン・seven-row-q6）。実験dir・item・log・
  README bulletはすべて新規パス+K0960 bullet直下挿入のため競合リスクは低い。
  push前に最新mainを再取得する。

## 次課題

- (i) γ分岐のDiophantine scarcity: p₂p₃ ≥ M ∧ ペア積がk₀付近に集中する合同構造
  （なぜγ行はt ≤ 37で(M−2)/36の理論上界に遠いのか）。
- (ii) 予想2件の全称化（kodd=4 → t < √M・kodd≥5 → t ≤ 3）。
- (iii) PAIR-MIN+/SQUEEZE-3のfloor到達分布の理論（K0960 OPEN(i)継続）。
- (iv) t=1非compliant集団1,111行の構造（梯子が切れるt=1固有の算術）。
- (v) M>2000延伸（sieve-walk・K0960と同じ方法で素直に可能）。
