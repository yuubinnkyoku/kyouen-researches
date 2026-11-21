---
id: K1145
title: 生存者列最小周期がr=33..48で機械確定（小witness棄却・全1,548,272真約数・witness C≤39・フォールバック不使用） — K0925定理S32の定理S48拡張・等Qブロックwitnessストリーム同一観察（sha256ピン）
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases:
  - theorem S48 survivor minimal period r33to48
  - K0925 S32 extension small witness rejection
  - equal-Q block witness stream identity
  - bounded witness observation r2to48
relations:
  - type: depends_on
    target: K0925
    note: 直接の続編。定理W+（全称・全C）が正方向（Q(r)は生存者列の周期）を全称で与え、定理S32（r=2..32機械確定）が手法と正本データを提供。本項のS1検査はr=17..32の同実装再計算がK0925出版監査（SHA-256 b3733ed5…）のW5値と全項目一致することで健全性を固定する。
  - type: depends_on
    target: K0922
    note: 補題DIV（周期集合のgcd閉包・列汎用）により生存者列の真約数棄却から最小性が決まる。m(r)|Q(r)で各真約数をwitness 1個の棄却で十分。
  - type: depends_on
    target: K0919
    note: 定理PER（⟸方向）と素数冪補題がQ(r)=lcm(1..r)の周期条件系の基盤。
  - type: related
    target: K0926
    note: 小C側のS(C,r)=P(C)プラトー構造（E6U）があるが、witness判定のS(C+d,r)側のr非依存性（等Qブロック同一観察）はプラトー定理の直接の帰結ではない（観察として記録）。
artifacts:
  - path: research/experiments/remo-survivor-minimal-period-r33plus-20261120/report.md
    role: proof
    note: 定理S48の記録・掃引表（r 33..48・全1,548,272真約数）・等Qブロックwitnessストリーム同一観察・信頼境界
  - path: research/experiments/remo-survivor-minimal-period-r33plus-20261120/survivor_witness_r33plus.py
    role: verifier
    note: S0-S4の5機械検査。stdlibのみ・決定的・assemble二重実行byte一致必須・per-(check,r) checkpoint・--no-cache全再計算・--budgetシャード再開（シャード境界チェックポイント・チェインドchunk sha256でwitnessストリームを再開安全にpin）
  - path: research/experiments/remo-survivor-minimal-period-r33plus-20261120/output/audit.json
    role: data
    note: 監査JSON（32,790 bytes・SHA-256 0b5ae7eb…・5/5 ok・別cwd隔離再計算と本体でbyte同一）
  - path: research/experiments/remo-survivor-minimal-period-r33plus-20261120/output/published_run.txt
    role: data
    note: "隔離cwdの完走invocation標準出力（5チェックOK・STATUS: COMPLETE checks:5 all_ok:True）"
  - path: research/log/2026-11-20-remo-survivor-minimal-period-r33plus.md
    role: source
    note: 高速レーン研究ログ（単一オーナー宣言の確認・掃引・観察・2プロセス検証・出版）
---

## 定理S48（機械・r=33..48）

K0859定理Dの計数再帰E(C,r)（Δ=0一様盤）の生存者列について、
**生存者列の最小周期はr=33..48の全rでちょうどQ(r)=lcm(1..r)**。

K0925定理S32と同一手法: K0919定理PER・K0925定理W+（全称・全C・
Q(r)は生存者列の周期）とK0922補題DIV（最小周期m(r)|Q(r)）により、
各真約数dをwitness 1個（S(C+d,r)≠S(C,r)となる最小C、窓[1,150]・
フォールバック窓[151,1500]）で棄却すれば十分で[1,Q(r)]完全走査は
不要。**r=33..48の全1,548,272真約数（Q(48)=4.43e20の294,911個を
含む）がすべてwitness C≤150で棄却され、フォールバック窓は不使用**
（観測最大39=r=47/48・d=Q/47型でh*=1〔M_1失敗〕に一致・K0925の
「最大witnessのdはQ/m型」パターンを継承）。Q(48)の約数は素因数
分解（e_p=max{a:p^a≤r}）から列挙（試し割りは√Q≈2.1e10で不可能）、
r=2..20で試し割りと完全一致を機械検査（S0）。K0925 S32との合算で
**掃引済み範囲はr=2..48**。

## 機械チェック（5/5合格・監査SHA-256 0b5ae7eb…）

S0（約数列挙の試し割り一致r=2..20・解析的指数パターンr=33..48）/
S1（**K0925再現pin**: r=17..32の(proper・unwitnessed・wit_max_sv・
wit_argmax_over_Q・sv_C1_same)が本実装の再計算で出版監査値と完全
一致・W5意味論の同一性を固定）・S2（主掃引r=33..48・2,959,796回
シミュレーション・約1.9回/約数・チェインドsha256でwitnessストリー
ム"d w"を再開安全にpin）・S3（正方向アンカー: C∈[1,1500]+{Q-1,
Q+1,Q+5,2Q-1}のS(C+Q,r)==S(C,r)、24,064比較・不一致0・全称証明は
K0925定理W+）・S4（verbatim 1石配分再帰==閉形式双対==survivor_fast
の全(elim, survivor)ペア一致をr=33..48・C∈[1,150]で2,400組で新規
ピン。K0925 TWINはr=2..24を既にカバー）。assemble二重実行byte一致
必須・別cwd隔離フル再計算プロセスで監査byte同一・CIは新規監査を
git diff pin。

## 有限観察（主張は限定的）

1. **有界witness観察の延長**: wit_max_sv ≤ r−1がr=33..48全域で
   成立（最大39・r=47/48）。r=2..48合算でもwitness最大は39のまま。
   有界witness予想（生存者側の全称最小性を閉じる鍵）は引き続き
   証明なし。
2. **等Qブロックwitnessストリーム同一観察（新規・sha256ピン）**:
   lcm(1..r)が等しいr（等Qブロック{17,18}/{19..22}/{23,24}/{25,26}/
   {27,28}/{29,30}/{31}/{32..36}/{37..40}/{41,42}/{43..46}/{47,48}）
   の内部では**各真約数へのwitness値d→wのストリーム全体が同一**
   （監査のチェインドsha256が各rで同じ）。K0925出版データの
   ブロック内集計一致を「全witness判定のr不変性」まで精緻化した。
   witnessの地図はブロック内で(Q,d)の関数でありrの関数ではない。
   プラトー定理（K0926 E6U: C≤r−1でS(C,r)=P(C)）は小C側のみ説明し
   S(C+d,r)側のr不変性は未説明で、本項は観察の記録にとどめる
   （K0928 pot縮約構造からの説明が次課題）。

## 限界

- Δ=0一様盤（定理D域）限定。非一様盤には一切言及しない。
- 定理S48はr ≤ 48の機械確定。生存者側の全称（有界witness予想）は
  OPENのまま。r ≥ 49には言及しない。
- 11×11空盤・クラスフロンティアは無関係でUNKNOWNのまま。

## 採番記録

2026-11-20 10:22Zの単一オーナー宣言（research/log/2026-11-20-remo-
survivor-witness-r33plus-single-owner-note.md・「現時点のmain最大
番号を確認してから決める」条項）に従い、掃引開始時点のmain最大番号
K1142（n11 fold25レーン）を確認した上で仮採番K1143でitem/log/README
bullet/CI stepを出版したが、**並走y11 fittingレーンが15分先行して
同名異slugの項目 K1143-two-token-y11-parametric-closed-form-fit
（12:15:50Z・commit 27944a94）をmainに出版しており、K1144
（n11残余72二検証・12:18:26Z）も使用済みだった**ため、AGENTS.mdの
再採番規則（main既存の番号は変更しない・重複新規項目を再採番し参
照を更新）に従い本項目をK1145へ再採番した（旧path
items/K1143-remo-survivor-minimal-period-r33to48.mdは同修正コミッ
トで削除し、README bullet・CI step名・監査JSONのitem欄も同時更新。
数値内容・検査・監査の正本は再採番不変で、変更は識別子表記のみ）。

## 再現

`python3 research/experiments/remo-survivor-minimal-period-r33plus-20261120/survivor_witness_r33plus.py`
（新規計算約6分・checkpoint再利用で高速化・--no-cacheで全再計算）。
CI audit stepも同スクリプトで監査JSONをgit diff pinする。
