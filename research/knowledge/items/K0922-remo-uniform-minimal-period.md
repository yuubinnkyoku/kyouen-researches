---
id: K0922
title: 一様盤REMO計数再帰の最小周期はr=2..16でちょうどlcm(1..r)（敗者全列・生存者両列・全真約数棄却） — 補題DIV（割り切り・全称証明）により必要性方向も同時に閉じる・witness C=1観察とP(C)=1⟺素数予想（C≤300・有限観察）
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: [minimal period lcm, theorem MP, lemma DIV period gcd closure, P(C) prime survivor conjecture]
relations:
- type: depends_on
  target: K0919
  note: 定理PER（Q(r)=lcm(1..r)周期の全称証明）とE3（r=2..9最小性）が本項の前提。M7はE3の独立再現・M3は定理PERのr=10..16機械アンカー・補題DIVは定理PERとの組合せで必要性⟺最小性を確定
- type: depends_on
  target: K0859
  note: 定理Dの計数再帰（Δ=0一様盤・全称）が本定理の対象。verbatim再帰はM2の照合対象
artifacts:
- path: research/experiments/remo-uniform-minimal-period-20261117/report.md
  role: proof
  note: 定理MP・補題DIV（Bezoutによるgcd閉包）・witness C=1観察・P(C)素数予想の記録と7機械チェックの定義
- path: research/experiments/remo-uniform-minimal-period-20261117/verify_remo_uniform_minimal_period.py
  role: verifier
  note: M1-M7（決定的・stdlibのみ・新規スイープなし・per-r checkpointでresumable・--no-cacheで全再計算）
- path: research/experiments/remo-uniform-minimal-period-20261117/output/remo_uniform_minimal_period_audit.json
  role: data
  note: 監査JSON（sha256 3c9ee621…・12,211 bytes・assemble二重実行と2回の別プロセス実行でbyte同一）
---

## 定理MP（機械・r=2..16・完全走査）と補題DIV（全称）

K0859定理Dの計数再帰 E(C,r)（Δ=0一様盤・K0919定理PERの対象と
同一）について:

1. **定理MP**: 敗者全列（elimination列）と生存者列の**それぞれ**の
   C方向最小周期は、r = 2..16 の全rで**ちょうど Q(r) = lcm(1..r)**
   （Q(10..16) = 2520, 27720, 27720, 360360, 360360, 360360,
   720720・真約数計1,049個を両列で全棄却・witness走査は
   [1, Q(r)] の完全窓）。r=10..16が新規範囲・r=2..9はK0919 E3の
   独立再現（M7・全132真約数で出版結果と完全一致）。
2. **補題DIV（全称・証明つき）**: E(·,r) の周期集合 Per(r) は
   最小周期 m(r) の正の倍数全体と一致し m(r) | Q(r)。証明は
   Bezout（g = a·T1 − b·T2・a,b ≥ 0・添字は全て ≥ 1 を保つ
   上向き適用）によるgcd閉包。とくに**必要性方向「周期はQ(r)の
   倍数に限る」は最小性と同値**であり、真約数棄却だけで両方向が
   決まる。r ≤ 16 では両方向とも閉じた。
3. **定理Jとの対比**: 一様盤計数再帰は「r方向に有界窓で安定化
   （K0906）・C方向に周期 Q(r) で反復、かずその周期は最小
   （本項・r ≤ 16）」。

## 有限観察（主張は限定的）

- **witness C=1（elim列・r=2..16）**: Q(r) のすべての真約数 d が
  C=1で棄却される（E(1+d,r) ≠ E(1,r)・E(1,r)の敗者列は
  (1,2,…,r−1)・生存者0）。r ∤ d なら第1敗者オフセット (1+d) mod r
  の差で即棄却・r | d の深い場合も含めて r ≤ 16 全域で成立。
  全rでの全称性はOPEN（証明課題・生存者列のwitnessは最大10）。
- **P(C) = 1 ⟺ C 素数（C ≤ 300・予想としてのみ提案）**:
  P(C) = S(C,C) は C ≤ 300 で「素数62個すべて P=1・合成数237個
  すべて P≠1・C=1はP=0」。機構は未解明・閉形式も全称性も主張
  しない。P(C) = C−1 となる C（61個・C ≤ 300）も監査JSONに
  記録（構造規則は未同定）。

## 機械チェック（7/7合格）

M1 Qピン/割り切り・M2 verbatim==双子（1,811ペア・r=10..16・
[1,200]全数+層化61点+大型アンカー8点）・M3 定理PERアンカー
（1,859,760ペア・全数）・M4 帰納データ検査（違反0）・M5 最小性
（真約数1,049個両列棄却）・M6 P(C)ピン40項一致+300項拡張・
M7 K0919 E3独立再現。監査JSONはassemble二重実行・2回の別
プロセス実行（うち1回--no-cache全再計算・環境リセット1回挟入）で
byte同一（sha256 3c9ee621…）。

## 限界

- Δ=0一様盤（定理D域）限定。非一様盤には一切言及しない。
- 最小性は r ≤ 16 の機械確定。r ≥ 17 は OPEN（Q(17) = 12,252,240
  で2Q窓は約2,450万評価・現行1GiB環境では窓分割またはストリー
  ミング設計が必要）。
- witness C=1・P(C)素数予想は有限観察であり全称主張しない。
- 順位（敗者順序の一部・full ranking）の周期性は別問題
  （elim全列の一致を検証しており帰納法自体は全順位一致を与える）。
- 11×11空盤・クラスフロンティアは無関係でUNKNOWNのまま。

## 再現

`python3 verify_remo_uniform_minimal_period.py`（checkpoint
利用で高速・`--no-cache`で全再計算約5-7分・stdlibのみ・
決定的）。2回実行で監査JSON byte同一を確認。
