---
id: K1163
title: 生存者列最小周期の最大真約数帰約LEMMA RED（全称証明付き）とr=49..150 maxdiv掃引による定理S150機械確定（全2,602対のwitness C≤150棄却・等Qブロック同一性のmaxdiv粒度拡張・棄却ベクトル不成立の負の観察）
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases:
  - theorem S150 survivor minimal period r2to150
  - LEMMA RED maximal proper divisor reduction
  - maxdiv sweep r49to150
  - equal-Q block minimal-witness map identity at maxdiv granularity
  - reject-vector non-identity negative observation
relations:
  - type: depends_on
    target: K0925
    note: 定理W+（全称・全C・正方向＝Q(r)は生存者列の周期）が閉包の正方向を担い、定理S32（r=2..32）が出版正本データ・手法を提供。C3は本実装の再計算でK0925監査のper-r witness最大値（r=2..32）をピンする。
  - type: depends_on
    target: K0922
    note: 補題DIV（周期集合は最小周期の正倍数集合・m|Q(r)）がLEMMA REDの前提。K0922監査M5のd=Q/p w_sv表（r=10..16）もC3で再現ピン。
  - type: depends_on
    target: K0919
    note: 定理PER（⟸方向）と素数冪補題がQ(r)=lcm(1..r)周期条件系の基盤。
  - type: depends_on
    target: K0859
    note: 定理Dの一様盤計数再帰E(C,r)と生存者列C→S(C,r)の定義（TWIN＝逐語1石配分再帰==閉形式双対==survivor_fast）。
  - type: extends
    target: K1145
    note: 定理S48（r=33..48・全1,548,272真約数掃引）の続編。LEMMA REDで検査を最大真約数π(r)個に落とし、掃引範囲をr=150まで拡張（定理S32+S48+本項でr=2..150）。等Qブロック同一観察をmaxdiv粒度・r≤150に精緻化。
artifacts:
  - path: research/experiments/remo-survivor-maxdiv-r49plus-20261120/report.md
    role: proof
    note: LEMMA REDの全称証明・定理S150・掃引表・コスト崩壊の定量・4観察・信頼境界・採番訂正記録
  - path: research/experiments/remo-survivor-maxdiv-r49plus-20261120/verify_survivor_maxdiv_r49plus.py
    role: verifier
    note: C0-C7の8機械検査。stdlibのみ・決定的・assemble二重実行byte一致必須・per-r checkpoint・--no-cache全再計算
  - path: research/experiments/remo-survivor-maxdiv-r49plus-20261120/output/audit.json
    role: data
    note: 監査JSON（51,077 bytes・SHA-256 d916f0a2…・8/8 ok・--no-cache隔離2重再計算+PYTHONHASHSEED=randomでbyte一致）
  - path: research/experiments/remo-survivor-maxdiv-r49plus-20261120/output/maxdiv_witness_table.txt
    role: data
    note: r=2..150のper-(r,p) witness表（9,148 bytes・SHA-256 cdf890c1…・監査内ピン）
  - path: research/experiments/remo-survivor-maxdiv-r49plus-20261120/output/published_run.txt
    role: data
    note: 出版fresh run標準出力（8チェックOK・checks:8 ok:8 all_ok:True・elapsed:110.8s）
  - path: research/log/2026-11-20-remo-survivor-maxdiv-r49plus.md
    role: source
    note: 高速レーン研究ログ（宣言確認・再採番・プローブ数値記録・出版）
  - path: research/log/2026-11-20-remo-survivor-maxdiv-r49plus-single-owner-note.md
    role: source
    note: 単一オーナー宣言ノート（commit 97b741b8・訂正f4af3e1b・採番繰下げ訂正を追記）
---

## LEMMA RED（全称・証明つき）

r≥2、Q(r)=lcm(1..r)、生存者列f(C)=S(C,r)について、K0925定理W+
（全称・全C: Q(r)はfの周期）とK0922補題DIV（fの周期集合は最小
周期mの正倍数全体・m|Q(r)）より:

**m = Q(r) ⟺ すべての素数p≤rについて最大真約数Q(r)/pはfの周期でない**
（= witness Cが1個ありS(C+Q/p,r)≠S(C,r)）。

証明（report.mdに掲載）: m<Q(r)ならQ(r)/mの任意の素因数pを取る
（Qの素因数はすべて≤r）とQ(r)/pはmの倍数で周期。逆にQ(r)/pが
周期ならm|Q(r)/pでm≤Q(r)/p<Q(r)。被覆事実「任意の真約数dは
ある最大真約数Q/pを割り切る」は一行で（dの補素因数qを取る）、
C0がr=2..36・全146,121真約数で機械アンカー。検査数は
d(Q(r))−1からπ(r)個へ崩壊: r=48で294,911→15、r=100で
660,602,879→25、r=128で96,636,764,159→31、r=150で
1,546,188,226,559→35。

## 定理S150（機械・r=2..150）

**生存者列の最小周期はr=2..150の全rでちょうどQ(r)**。r=2..48は
出版済み全真約数掃引（K0925 S32+K1145 S48）、r=49..150はC4が
全2,602 (r,p)対の最大真約数を窓[1,150]で棄却（フォールバック
[151,1500]不使用・fail-closed・全部witness≤r−1・全局最大124は
ブロック{131..136}）し、W+とDIV+REDで確定。掃引動力学は出版
closed-form survivor_fast（C2 TWIN・900組がr=49..150グリッドで
逐語再帰と一致）、必要性方向は全称補題であってr≥49の約数毎
全数走査ではない（信頼境界はK1145と同一構成）。

## 機械チェック（8/8合格・監査SHA-256 d916f0a2…）

C0（被覆アンカーr=2..36）・C1（独立再実装の全真約数掃引
W5形式との判定・witness一致・r=2..24でmaxdiv掃引が第二コード
パス）・C2（TWIN 900組）・C3（K0922 M5 d=Q/p表の再現
r=10..16・K0925/K1145出版per-r witness最大値との比較で
**例外r∈{19,20,21,22,27,28}では全真約数側最大値が最大真約数側
より真に大きい＝witness最大の約数は最大ですらない**ことを機械
記録）・C4（主掃引・ヒストグラム・argmax(h*,クラス)付き）・
C5（正周期アンカー540比較・S(C+Q,r)==S(C,r)）・C6（等Qブロック
p→最小witnessマップ同一性・40/40複数メンバーブロックで完全一致
・隣接対照47組全不一致）・C7（棄却ベクトルレベルの非同一性の
負の観察）。assemble二重実行byte一致必須・--no-cache隔離
（別cwd/別HOME/PYTHONHASHSEED=random）2回の全再計算で
audit.json・表ともbyte一致。採番訂正（K1162→K1163）後の
--no-cache全再計算8/8合格112.2sでitem欄以外byte一致をdiff確認。

## 有限観察（主張は限定的・r≤150）

1. **有界witness観察のmaxdiv断片**: 2,602/2,602対でwitness≤r−1
   （ウィンドウ形式はK0926 E6UプラトーでC≤rのS(C,r)=P(C)に帰着）。
   生存者側の全称必要性（有界witness予想）は証明なし・OPEN。
2. **等Qブロック同一性の拡張**（K1145観察2のmaxdiv粒度・r≤150化）:
   2..150の40個の複数メンバーブロックすべてで(p→最小witness)マップ
   完全一致（{89..96}24素数・{113..120}30・{131..136}32・
   {139..148}34を含む）。隣接対照は全不一致。E側位相構造
   （K1154 V6: E側h*マップはブロック非不変）では説明不能。
3. **h*=1 argmaxパターンはr≤48の人工物**: r=49..150では102r中
   6r（{71,73,97,103,131,139}＝ブロック先頭素数そのもの）のみ
   h*=1で、他はh*≥2（例: r=113..120はp=107のh*=7..14）。
   K1145の「witness最大のdはQ/p型でh*=1」は範囲の人工物。
4. **棄却ベクトル不成立（負の精緻化）**: 同一ブロック内でも
   完全棄却ベクトル（C∈[1,60]）は素数ごとに一致しない
   （{17,18}p=3でC=12・{37..40}p=13でC=27/p=19でC=20・
   {113,120}p=13でC=27/p=19でC=44。{89,90}は窓内一致・
   p依存）。最小witnessレベルが正しい不変量。値レベル同一性も
   不成立: 同一ブロックの生存者列はブロック先頭r′のプラトー窓
   [1,r′]の直後r′+1から相違（{17,18}のC=18・{37,40}のC=38・
   {89,90}のC=90・{113,120}のC=114・{131,136}のC=132・
   {139,148}のC=140・{49,52}のC=50・{29,30}のC=30・
   機械probe・研究logに記録）。

## 限界

- Δ=0一様盤（定理D域）限定。非一様盤には言及しない。
- 定理S150はr≤150の機械確定。r≥151には言及しない。r≥49の
  非最大約数のwitnessは掃引していない（最大真約数帰約により
  不要な一方、全真約数側の直接データはr=48まで）。
- 有界witness予想（生存者側全称必要性）はOPENのまま。本項の
  witness≤r−1は観察。
- 11×11空盤・二石root・クラス分類はすべてUNKNOWNのまま。

## 採番記録

2026-11-20T17:18Zの単一オーナー宣言（research/log/2026-11-20-
remo-survivor-maxdiv-r49plus-single-owner-note.md・commit 97b741b8・
「対照itemのK番号はpush直前に3点確認」条項）に従い、宣言時点で
仮にK1162とした検証器を完成させたが、**並走y12 universalレーンが
17:31Z（commits 60622f35/258cd7b0/1093e075）にK1162
（two-token-y12-universal-verifier-part1）を出版した**ため、
AGENTS.md再採番規則（main既存の番号は変更しない・重複新規項目を
再採番し参照を更新）に従い**K1163へ再採番**した。検証器のitem埋め
込み欄を更新し--no-cache全再計算（checks:8 ok:8 all_ok:True・
112.2s）で監査を再生成、数値内容はitem欄1行を除き旧監査とbyte一致
（diff機械確認・witness表は不変）。README bullet・研究log・宣言ノート
訂正も同時更新。

## 再現

`python3 research/experiments/remo-survivor-maxdiv-r49plus-20261120/verify_survivor_maxdiv_r49plus.py`
（checkpoint再利用で高速・--no-cacheで全再計算約110s・
assemble二重実行byte一致assert）。
