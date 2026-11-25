# 2026-11-18 remo smooth-hit DEEP-CAP（高速レーン・K0960）

## 経緯

- K0958レジューム(i)(ii)として、(a) CENSUS-STRIPのt>60帯完全化、(b) 構造補題の
  全称昇格を予定して開始。
- セッション序盤にt≥40集団の因数分解形（K0958: N=2·449·487²など）から
  「奇素数の2べき梯子が窓を跨ぐ」構造に気づき、紙上でODDCAP→MIN3→DEEP-CAPを
  証明（case A/B）。その後、全ペア積への窓回避（PAIR-MIN）がtop pair境界の
  最大1/3の強化であることを特定し、機械検証に追加した。
- CENSUS-STRIP2: census_full2000.py（素数Y列挙最適化・checkpoint再開型）で
  135素数133秒。t≤60帯7,441行はK0958出版hits_strip.jsonと完全一致。
- audit_build.pyを書き直後の初回実行で破損検出（旧版のmixed int/strキーで
  sort_keysが落ちるのみ・数学的検査は全通過済み）→修正→完了。
  初回実行時のengineフェーズ147秒（890+278件・0失敗）。

## 本日の成果

1. **THEOREM DEEP-CAP（全称証明）**: smoothヒット（素数M≥5・main regime・t≥2）は
   t < max(√M, ((M−1)²+4)/(4M))、特にM≥17でt < M/4。SEAM（K0956）のsmooth側
   4倍改良。補題ODDCAP（p ≤ (M−1)/2^a）・MIN3（Ω(odd)≥3）・系K3-A
   （kodd=3は全てcase A）・系PAIR-MIN（k₀ < min{pᵢpⱼ ≥ M}・top pair境界の強化）。
2. **CENSUS-STRIP2（決定的完全列挙）**: 1000<M≤2000全t・8,277 smoothヒット
   （t>60帯836件・max t=427@1789・N最大比0.1844）。
3. **全数機械検証**: deep hit 5,982件（strip2 4,844 + 出版M≤1000 1,138）で
   6述語0違反（N独立再因数分解）・engine錨890+278件0失敗・同値性M=1009/1783/1999・
   YSQR新帯・決定性（census冷再実行135 ckpt byte同一・audit冷二重実行byte同一）。
4. **構造**: t>60帯全件kodd=3・3奇素数ともM/2近傍（p₁最小149）・ODDCAP飽和2件・
   PAIR-MIN近接max 0.9973・case B 3/5,982（全t≤3）・2集団構造の算術的説明
   （窓回避の全ペア積制約）をK0958 OPENに提示。

## 判断メモ

- DEEP-CAPはsmooth専用でbranch型初回ヒット（93.8%）に適用されないためF(M)には
  影響しない。K0956/K0959のF表と整合。
- hits_strip2.jsonは単一ファイル完全版として出版したが、K0958のhits_strip.jsonは
  そのまま正本扱い（行完全一致・重複管理しない）。
- push時のHEADは08a0d111（n11レーンが進行中）。実験dir・item・log・README bulletは
  すべて新規パス+K0958最小更新のため競合リスクは低い。push前に再取得。

## 次課題

- (i) t≥40集団の「kodd=3ちょうど」条件の定量化（PAIR-MIN近接分布の理論）。
- (ii) K0959 EV増幅の定量モデル化。
- (iii) K0959 F_t/ln²M bucket medianのM>2000延伸（F計算が重い・要注意）。
- (iv) M>2000のcensus延伸（sieve-walk・約2.5倍/倍帯のコスト）。
