# 7行 q=4/5/6 witness 前線のSAT再確認と負記録 — M_{7,4} ≥ 36 の多系統強化

Date: 2026-11-15
Lane: 高速レーン ((7,9)帯閉包 2026-11-14/15 の後続バッチ)
Experiment: research/experiments/seven-row-q4-q6-witness-frontier-20261115/ (main push済み)

## 概要

w=7 の q≤6 帯について、sat2.js 完全符号化 + kissat 4.0.4 による witness 前線の
再確認と負記録を実施した。主結果は **(7,4) m=22..27 の SAT 再確認（4系統検証へ昇格）**
と、それに伴う **CSV下界の整合修正 (7,4) 22..1929 → 36..1929** である。

## 結果

1. **(7,4) m=22..27: 全幅 SAT・0 conflicts・2系統検証 PASS。**
   - m=22: 18石 witness、行構造 [3,3,3,3,3,2,1] — K0827 構成的 free extension と一致。
   - m=23..27: 20石、[3,3,3,3,3,3,2] — K0827 config CA と同一行構造。
   - 検証は sat.js verifyConfig (js) + Python Fraction (py) の2系統で PASS。
     既存の tsVerify (構成的延伸) と合わせ、**m=22..27 は4系統検証済み**
     (kissat SAT + jsVerify + pyVerify + tsVerify)。
   - m=28..35 は引き続き構成的延伸 (tsVerify のみ)。SAT側の再検証は pending。
2. **前線負記録（いずれも不在主張ではない）**:
   - (7,5) 7×32: 200s kissat INDET, 329,844 conflicts。
   - (7,6) 7×27: 200s kissat INDET, 744,027 conflicts。
3. **sat2.js census 壁**: 7×28 (q=4) の全三つ組 census 生成が node heap 2560MB で
   OOM (rc 137)。SAT による (7,4) 帯の直接延長は m=28 で停止。
   m ≥ 28 の SAT 探索には **q ≤ w 版メモリ有界 census** の開発が必要
   （実験 README に技術メモとして記載済み）。
4. **較正**: (7,5) m=23 の再実行 (1,200 conflicts) が公開 record と bit-exact。
   符号化・ソルバ挙動の再現性を確認。

## 知識反映

- K0827 (research/knowledge/items/K0827-...md): m=22..27 の再検証ステータス更新
  （pending → 4系統検証済み）+ records.jsonl artifact 追記 + 追記セクション。
- results/fixed-width/mwq_stabilization.csv: **(7,4) 行の下界整合修正**。
  K0827 の構成的延伸により下界は既に ≥36 だったが、CSV は
  `22..1929 / frontier 7x22` のまま stale だった → `36..1929 / frontier 7x36` へ修正。
  あわせて (7,5)/(7,6) 行に INDET 負記録を注記。
- results/fixed-width/README.md: 前線記述の更新
  （前線 7×22 → 7×36、(7,4)=36..1929、q5/q6 の INDET 負記録）。

## 位置づけ（w=7 の残る open band）

- (7,4): M ∈ [36, 1929] — 下界36（構成的+SAT 4系統検証）、上界 T_7=1929 (K0068/K0318)。
- (7,5): M ∈ [32, 1142]
- (7,6): M ∈ [27, 862]
- (7,7): M ∈ [27, 708]
- (7,8): M ∈ [25, 651] — q=w+1 で genfast3 不適用、前線 7×25 は長期レーン向き。
- (7,9): **M = 24 exact（今回の帯閉包 m=201..612 完走で決着）**。
- (7,10): M = 19 exact（並走レーンが genfast3 再利用で達成、K0820追記4）。

次の高速レーン候補: (5,7) m=22..157 掃引（要 class-split、長期寄り）、
q≤w メモリ有界 census の開発（7×28+ q4 SAT 探索の鍵）。
