---
id: K0961
title: smoothヒットのSQUEEZE構造（TWO-ZONE・EFFECTIVE-WINDOW・SQUEEZE-3・CHAR-3・K4-A・K4-CAP）とphantom観測
kind: proposition
status: proved
topics: [residual-games, statistics, verification]
aliases: [TWO-ZONE, CO-FACTOR, EFFECTIVE-WINDOW, PAIR-MIN+, SQUEEZE-3, CHAR-3, K4-A, K4-CAP]
relations:
  - type: depends_on
    target: K0960
    note: ODDCAP・MIN3・DEEP-CAP・PAIR-MIN・K3-Aを前提・一般化し、出版hits_strip2/deep_bandを行入力に再利用
  - type: depends_on
    target: K0958
    note: 出版hits_full（M≤1000全t・2,609行）とpinned census_walk/sieve_flags/window_blockedを再利用
  - type: depends_on
    target: K0956
    note: 中核恒等式N=(M+1)k₀+2M−κ・HIT-ARITH（[Y ok]限定の精密化）・SPLIT/EXCLUSIVE
  - type: depends_on
    target: K0949
    note: PARITY（a=v₂(N)≥1）をK4二分法・K4-Aで使用
  - type: generalizes
    target: K0960
    note: ODDCAP→TWO-ZONE（奇素数から全奇約数へ）・PAIR-MIN→PAIR-MIN+（(1+2/(M−1))倍拡張窓）・DEEP-CAP→K4-CAP（γ行でM/4の9倍）・K3-A→K4-A（kodd=3から4へ）
artifacts:
  - path: research/experiments/remo-smooth-squeeze-20261118/report.md
    role: proof
    note: TWO-ZONE/CO-FACTOR/EFFECTIVE-WINDOW/SQUEEZE-3/CHAR-3/K4-A/K4-CAPの全称証明と機械検証の正本
  - path: research/experiments/remo-smooth-squeeze-20261118/squeeze_audit.py
    role: verifier
    note: 24述語全数検証・prime-Y walk 34素数・composite-Y walk 33素数・engine錨の統合監査（決定的・冷再実行byte同一）
  - path: research/experiments/remo-smooth-squeeze-20261118/smooth_core.py
    role: verifier
    note: K0958ピン（sha256 928c54ca…一致）
  - path: research/experiments/remo-smooth-squeeze-20261118/prehit_core.py
    role: verifier
    note: K0956ピン（sha256 bf8ed817…一致）
  - path: research/experiments/remo-smooth-squeeze-20261118/composite_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 3990d67f…一致）・engine錨のsigma_Z
  - path: research/experiments/remo-smooth-squeeze-20261118/sievegen_core.py
    role: verifier
    note: K0950/K0956ピン（sha256 a69f916c…一致）
  - path: research/experiments/remo-smooth-squeeze-20261118/branch_density_core.py
    role: verifier
    note: K0954/K0956ピン（sha256 34b4ff15…一致）
  - path: research/experiments/remo-smooth-squeeze-20261118/output/squeeze_audit.json
    role: data
    note: 24述語0違反・walk/composite/engine集計・k4分岐・squeeze統計（sha256 5fca78b9…・冷再実行byte同一）
  - path: research/log/2026-11-18-remo-smooth-squeeze.md
    role: log
    note: 発見順・機械結果の要約・次課題
date: 2026-11-18
---

## 命題・範囲

記法はK0956/K0958/K0960と同一（M素数・main regime K=(M+1)t+κ・0≤κ≤M−2・
(t,κ)≠(1,0)・Y=K+1・k₀=Mt+κ−1・N=MY−1・窓=[M,k₀]・a=v₂(N)・kodd=Ω(N/2^a)・
中核恒等式 N=(M+1)k₀+2M−κ）。対象はsmoothヒット（Nが(M−1)-smooth∧窓空）。
X̄ := (M+1)k₀/(M−1)。

- **TWO-ZONE（全称・t≥2）**: Nの奇約数qは 2^a·q ≤ M−1 または q > k₀
  （中間帯禁止）。奇素数に限ればK0960 ODDCAPを回収し、複奇約数ではzone 2が実在
  （梯子2^i q (i≤a) の窓回避・K0960梯子論法の奇約数への一般化）。
- **CO-FACTOR（全称・regime恒等式）**: d ≤ M−1なる約数は N/d > X̄
  （N > (M+1)k₀ からの一行証明・窓空不要）。
- **EFFECTIVE-WINDOW（全称・t≥1）**: 約数は拡張窓 [M, X̄) に不存在
  （スリバー幅 ≈ 2t+2）。証明はd∈スリバーの余因子eが [k₀+1, Y−1] に落ち、
  d = N/e ≤ M+1 かつ d ≥ M+1 で d=M, M+1 とも Nの約数でない矛盾。
  **作業メモの条件 k₀ ≥ 2M−κ は不要**（t≥1で閉じる・auditは条件外3,833行でも
  スリバー約数0件を確認）。系PAIR-MIN+: K0960 PAIR-MINを
  min{pᵢpⱼ ≥ M} ≥ X̄ に(1+2/(M−1))倍強化。
- **SQUEEZE-3（全称・kodd=3∧compliant）**: p₁p₂ > X̄・
  t·M·(M+1) ≤ (M−1)p₁p₂−1（floor到達26/899行・argmax ρ=0.99725@M=1997,t=121）・
  p₁p₂ ≥ Y+1 ≥ M+3・深部cap t·M·(M+1)·2^{2a} ≤ (M−1)³−2^{2a}
  （K0960 DEEP-CAP case Aを(M−1)/(M+1)因子分厳密化）。
- **CHAR-3（特徴付け）**: compliant（2^a p₃ ≤ M−1）だけで窓が必ず空
  （約数の全列挙: 2^i・2^i p_j ≤ M−1、ペア・トリプル積 ≥ p₁p₂ ≥ Y+1 > k₀・
  窓検査不要・Y素数性不要・合成Y域でも成立 511/511）。t≥2では逆に
  ODDCAPからcompliantが自動。まとめ: t≥2・[Y ok]で「kodd=3ヒット ⟺ compliant」。
  t=1では⟸のみ成立し非compliantヒット1,111件が実在（梯子のt≥2が本質）。
- **K4-A（全称・t≥2）**: kodd=4ヒットは全てcase A（top pair ≥ M）。
  case Bなら N=(2^a p₁p₂)(p₃p₄) ≤ (M−1)² < 2M²+2M+1 ≤ N。t=1ではcase B 22件。
- **K4交叉対二分法（全称）**: (p₂p₃,p₁p₄)も(p₁p₃,p₂p₄)も両方≥M不可
  （N=2^a(交叉対積)(交叉対積) > 2k₀² vs N ≤ (M+2)k₀+1）。
- **K4-CAP（全称）**: case Aは3分岐。(α) p₂p₃<M≤p₁p₄:
  t < √M/2^a + 1/M（鋭形 t < ((M−1)^{3/2}/2^{3a/2}+1)/M）。
  (β) p₂p₃<M∧p₁p₄<M: **t < 1 で常に空**（N ≤ (M−1)²/2^a・メモのt ≤ 2^a−1から強化）。
  (γ) p₂p₃≥M: p₁p₂,p₁p₃,p₁p₄ < M の3重TWO-ZONEから
  Mt ≤ ⌊(M−1)/2^a⌋²（weak）・κ≥1で t·2^{2a}p₁² ≤ M−2（sharp）。
  まとめ: kodd=4 ⟹ t < max(√M/2+1/M, (M−2)/12)（無条件）/
  max(√M/2+1/M, (M−2)/36)（κ≥1・センサスγ全413行がκ≥1）。
  DEEP-CAP M/4のγ行側9倍厳密化。実測: α 139・β 0・γ 413（max t=37@1619・
  N=2·3·229·263·269・sharp bound 44）・B 0・a最大2。
- **予想（有限検証のみ・未証明）**: kodd=4 ⟹ t < √M（552行0違反・γの理論上界
  (M−2)/36が√Mを超えるM>1296域が真価とされたが**K0965で反証**
  （最初の反例 M=2221・t=54・M≤10⁴で932反例・全てγ枝κ≥1））。
  kodd ≥ 5 ⟹ t ≤ 3（0違反・kodd=5部分はK0963で反証・kodd≥6部分は
  K0963/K0965の掃引帯内で支持のまま未解決）。

## 現在の根拠と限界

- 上記定理は紙上全称証明（report.md正本）。機械は有限アンカー: 出版smoothヒット
  10,886行（K0958 hits_full 2,609 + K0960 hits_strip2 8,277・M≤2000全t）で
  N独立再因数分解の24述語全数検査・**0違反**（identity/parity/smooth/exclusive/
  twozone/effwindow/squeeze 5種/k4 8種/char3/deepband照合/予想錨2種）。
  t=1のTWO-ZONE違反8,209件は定理範囲外（梯子はt≥2）。
- engine錨: ヒット474件σ_Z=1・窓阻止40件σ_Z≠1・phantom 25件σ_Z≠1（0失敗）。
  prime-Y walk 34素数は出版ヒット集合と完全一致（mismatch 0）・
  CHAR-3 iff完全一致（t≥2 compliant 137件全窓空・非compliant窓空0）。
  composite-Y walk（M≤149・全Y）: compliant 511件の窓非空0（自己阻止の合成域成立）。
- **HIT-ARITH適用範囲の精密化（K0956の読みの修正）**: 窓空 ⟺ σ_Z=1は
  [Y ok]（Y素数∨Y=M²）クラス限定。composite-Yでは窓空かつσ_Z≠1の
  **phantom**が実在（676件 = dead 610 + live 66・engine錨25/25）。
  hitの正しい定義はσ_Z(M,K)=1。素数Y域のphantomはdead排除（T5系:
  Y素数∧Y≥M+2 ⟹ gcd(κ+1,M+1)=1）で存在しない。
- 構造観察（有限）: t>60帯899行は全件kodd=3・v₂≥2例外3行（1901 t=65・1987 t=71/84）。
  max t per kodd: 3→427@1789・4→37@1619・5→3@1097・6→2@757・7-9→1。
- OPEN: (i) γ分岐のDiophantine scarcity（**K0965で解消: scarcityは偽・
  t=235@M=9857まで到達しγ sharp上界の86%飽和**）・予想2件の全称化
  （(i)はK0965で反証・(ii)のkodd=5部分はK0963で反証・kodd≥6部分は未解決）。
  (ii) κ=0のγ行のM>2000での有無（**K0965: 15行実在**・γ 9/α 6・全てt<√M）。
  (iii) PAIR-MIN+近接分布の理論（K0960 OPEN(i)継続）。(iv) M>2000延伸
  （**K0965でkodd=4/5/6はM≤10⁴まで完了**）。(v) t=1非compliant集団1,111行の構造。
- branch型ヒット・F(M)には不適用（初回ヒット93.8%はbranch型・K0956不変）。
  11×11空盤に言及しない。uv check/buildは本環境にcloneとuvがなく未実施
  （歴代remo項目と同じ扱い）。generated/とroot READMEは未編集。
