---
id: K0923
title: 欺瞞族(1,1,p)|0のパイル帰着とspf法則（補題R1-R4） — 可能生存者集合は3パイル決定パスで全称計算可能・sv={P_0} ⟺ r < spf(p)（p ≤ 100機械・4,851列違反0）で欺瞞窓[2,p−1]一様決定 ⟺ p素数・K0921 EXO反鏡像の機構解明
kind: proposition
status: proved
topics: [multiplayer, variants]
aliases: [deceptive pile mechanism, spf law, pile reduction]
relations:
- type: depends_on
  target: K0859
  note: REMO規則（巡回・maximal直面で着手前敗退・敗者石除去）の定式化。補題R1-R4の証明はこの規則にのみ依存
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）のアトム/スター領域表現。プロファイル(1,1,0,p,0,0,0)はキー(1,1,p)|0の正準形で、決定性・可能生存者は実現盤面すべてに転写
- type: depends_on
  target: K0912
  note: engine交差検証の相手バイナリ（pin mask_engine_fast2.js sha256 b904760e…）。88列で(det,sv)完全一致
- type: generalizes
  target: K0920
  note: exotic11 (1,1,11)|0の低r一様決定観察とr=M反転を(1,1,p)|0全般のspf法則（p ≤ 100機械+全称帰着）へ統合
- type: supports
  target: K0921
  note: EXO（exotic11反鏡像: det ⟺ r < M）はspf(p)=p=Mの場合として本項の法則で説明される
artifacts:
- path: research/experiments/remo-k-branch-deceptive-pile-mechanism-20261117/report.md
  role: proof
  note: 補題R1-R4のメモ証明（占有単一性・即勝ボタン・強制ストレッチ・決定パス）とspf法則・単一ストレッチ構造の機械観察・engine交差88列・限界・再現
- path: research/experiments/remo-k-branch-deceptive-pile-mechanism-20261117/pile_sim.py
  role: source
  note: 3パイルゲームシミュレータ本体（決定パスの厳密実装・検証器内蔵版と同一コード）
- path: research/experiments/remo-k-branch-deceptive-pile-mechanism-20261117/verify_deceptive_pile_mechanism_20261117.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ・ネットワークなし。engine交差88列はピン済みK0912 engine実行系列をPython reprでインライン。5機械チェック全合格・assemble二重実行byte同一
- path: research/experiments/remo-k-branch-deceptive-pile-mechanism-20261117/output/deceptive_pile_mechanism_law.json
  role: data
  note: 監査JSON（sha256 8134c6b4…・5チェック・24素数表・4,851列spfスイープ・741列単一ストレッチ・合成数sv例）
scope: '3枝REMOのキー(1,1,p)|γ=0（プロファイル(1,1,0,p,0,0,0)・3つの単独アトム1・1・p）について2層の主張を区別する。(i) 補題R1-R4は全称（全p ≥ 1・全r ≥ 2・メモ証明付き）で、可能生存者集合svが3パイルゲームの決定パス（決定点=盤面空位置の着手者全体∪端末生存者・有限で循環なし）で正確に計算できることを確定する。(ii) spf法則（sv={P_0} ⟺ r < spf(p)、spf(p)はpの最小素因数）はp=3..100×r=2..p−1の4,851列の完全機械掃引で違反0・したがって欺瞞窓[2,p−1]で一様決定 ⟺ pが素数（24素数ちょうど・全決定列で生存者一様P_0・合成数の決定列はちょうど[2,spf(p))）、単一ストレッチ構造（決定点は開始点1個のみ・端末生存者==P_0 ⟺ r < spf(p)）はp ≤ 40の741列、素数のr=pとr=p+1はsv={0,1}は24素数全て、は有限機械観察。spf法則・単一ストレッチ性のp > 100は予想（spf予想）として全称主張しない。(1,p,p)|0側（重なりアトムを含む17プロファイル）・γ > 0の(1,1,p)型・順位決定性は範囲外。定理E′経由で実現盤面に及ぶ'
evidence: 'verify_deceptive_pile_mechanism_20261117.py 5チェック全合格（assemble二重実行byte同一・監査sha256 8134c6b4…・所要2〜3分・環境リセット後の再実行でもAUDIT PASSEDと出版JSON byte同一を確認済み）。ENGINE_CROSS_88: シミュレータがピン済みK0912 engine（sha256 b904760e…）の(det,sv)を(1,1,11)/(1,1,13)/(1,1,17)の全窓40列と合成数{4,6,8,9,10,15,21,25}の48列で完全再現・不一致0（engine列はp13/p17プローブ出版logと同一実行系列）。SPF_LAW_P100: 4,851列違反0。DECEPTIVE_WINDOW_IS_PRIMES: 窓全域一様決定なpは24素数{3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97}ちょうど。SINGLE_STRETCH_P40: 741列違反0。PRIME_R_GE_P_SV01: 24素数×2列でsv={0,1}・合成数はsv={0,T}でT奇数（例(1,1,4)|0 r=4は{0,3}）。engineの実用範囲はr ≲ 18（再帰深さ）で、シミュレータ広域掃引（r ≤ 101）はengine範囲を超える外挿である点をreport.mdに明記。R1-R4からシミュレータまでは証明済みで、spf法則はシミュレータ出力への有限観察'
---

# 欺瞞族(1,1,p)|0のパイル帰着とspf法則

## 命題（2層構造）

**全称層（補題R1-R4・メモ証明）**: キー(1,1,p)|0の正準形は
3つの単独アトム（a=star1専属容量1・b=star2専属容量1・
c=star3専属容量p）で、可能生存者集合は次の決定パス計算で
正確に得られる（全p ≥ 1・全r ≥ 2）:

- **R1（占有単一性）** 到達可能な全位置で占有アトム集合は
  ∅/{a}/{b}/{c} のいずれか。
- **R2（即勝ボタン）** 盤面空・|active| ≥ 2の位置でa（またはb）
  を開けた着手者が生存者。star1/2は即完成し、maximal巡回敗退
  （各敗退は盤面を変えない）で開けた本人だけが残る。
- **R3（強制ストレッチ）** occ={c}ではcount==pで着手者敗退
  （自分の石m個が除去されcountはm減る・m=0なら除去なし）、
  0 < count < pでは唯一の合法手はcへの石置き。
- **R4（決定パス）** sv = {各決定点（occ=∅）の着手者} ∪
  {端末生存者}。パスは開始点から「a/bを開ける（その着手者が
  生存者で終了）かcを開ける（一意の強制区間→次の決定点または
  端末）」の2択列で、activeは真に減少するため有限・循環なし。

**機械層（有限観察）**:

- **spf法則**: 2 ≤ r ≤ p−1で sv={P_0} ⟺ r < spf(p)
  （pの最小素因数）。p=3..100 × r=2..p−1 の4,851列で違反0。
  帰結として**欺瞞窓[2,p−1]で一様決定 ⟺ pが素数**
  （24素数ちょうど・全決定列で生存者は一様P_0）。
  合成数の決定列はちょうど[2,spf(p))
  （例: (1,1,9)|0はr=2のみ決定・(1,1,25)|0はr=2,3,4決定）。
- **単一ストレッチ構造**: p=3..40の741列で決定点は常に開始点
  1個のみ（第1強制ストレッチがゲームを終わらせる）で、
  端末生存者==P_0 ⟺ r < spf(p)。違反0。
- **r ≥ p**: sv={0,T(p,r)}で、素数pでは24素数全てT=1
  （r=pとr=p+1の両列）。

## 機構とK0921 EXOの統合

欺瞞族(1,1,p)|0の「低rでは頑健に一様決定に見えてr=Mで反転する」
観察（K0920 exotic11・p13/p17プローブ出版log）の機構:
決定パスの決定点が1個しかないため、決定性は「第1強制
ストレッチの巡回算術が端末をP_0にするか」の一点問題に帰着し、
その算術がr = spf(p)で初めて崩れる。K0921のEXO
（exotic11反鏡像: det ⟺ r < M）は spf(11)=11=M の特別場合
として本法則に吸収される（素数pでは一般にspf(p)=p=M）。
素数性はこの族の(1,1,p)|0側では spf(p)=p という形で
機構に現れる。

## 限界

- spf法則・単一ストレッチ性はp ≤ 100 / p ≤ 40の有限機械観察。
  **p > 100は予想（spf予想）**。全称証明には単一ストレッチ性の
  証明とcストレッチの巡回算術の閉形式が必要。
- engine交差検証は88列（engine実用範囲 r ≲ 18）。シミュレータの
  広域掃引（r ≤ 101）はengine範囲を超える外挿（R1-R4帰着の
  正当性により意味は保たれるがengine独立再現ではない）。
- **(1,p,p)|0側（b2∩b3重なりアトムを含む17プロファイル）は
  本項では未解決**。欺瞞族の完全な機構特徴づけには残る。
- γ > 0の(1,1,p)型キー・順位決定性には言及しない。
- 11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class1/2/4はいずれもUNKNOWNのまま。

## 再現

```sh
cd research/experiments/remo-k-branch-deceptive-pile-mechanism-20261117
python3 verify_deceptive_pile_mechanism_20261117.py
# -> AUDIT PASSED (5 checks) + audit byte-identical（所要2〜3分）
```
