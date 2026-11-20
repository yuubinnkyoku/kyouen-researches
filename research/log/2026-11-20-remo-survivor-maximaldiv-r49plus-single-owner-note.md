# 単一オーナー宣言: REMO 生存者列最小周期の最大真約数縮約による r=49..160 機械拡張（高速レーン）

- 宣言時刻: 2026-11-20T17:2xZ 級（push後にcommit時刻で確定）・高速レーン・単一オーナー。
- 本ノートは次段階の着手権を宣言する（先行出版）。他レーンが同範囲へ着手する場合は本ノート以降の出版を避け、
  別範囲（r>160・全称証明・E列側など）に回すこと。

## 着手範囲（本レーンが出版するもの）

1. **系MAX（Corollary MAX・全称・証明つき・新規）**: K0922補題DIV（周期集合=最小周期m(r)の正の倍数全体・m(r)|Q(r)）と
   K0919定理PER（Q(r)は周期）から、「任意の列（生存者列を含む）の最小周期がちょうどQ(r) ⟺ すべての最大真約数
   Q(r)/p（pはr以下の素数）がその列の周期でない」ことを導く。証明: m<Q かつ m|Q なら Q/m>1 の素因子 p について
   m | Q/p（pの存在: p|Qでp≤r）、Q/pはmの正の倍数ゆえ周期となり棄却と矛盾。
2. **定理SM160（機械確定・r=49..160・新規）**: 上記縮約のもと、各rの全最大真約数Q(r)/p（p≤r素数・計約2,800対）を
   K0925/K1145と同一のwitness意味論（最小昇順・窓[1,150]・フォールバック[151,1500]・検証器は出版survivor_fast
   （閉形式双対・verbatim per-stone再帰と twin pin））で棄却し、生存者列の最小周期がr=49..160の全rでちょうどQ(r)
   であることを機械確定する。K0925（r≤32）・K1145（r≤48）との合算で掃引済み範囲は r=2..160。
   全真約数掃引（τ(Q(160))≈10^11で実行不可能）に代わり最大真約数π(r)個の棄却で足りる本縮約が範囲拡張を可能にした
   （r=49..48帯ではK1145が全1,548,272真約数を掃引済み・妥当性の再現pinを行う）。
3. **再現pin**: K1145出版監査（pinned commit d345c645）の r=33・r=48 全掃引集計（proper/unwitnessed/wit_max_sv/
   wit_argmax_over_Q/sv_C1_same/n_sims/hist 含む）と chunk-chained stream_sha256 を本検証器の再実装で完全一致
   （必要なら一部）させる。K0925 W5 pins（r=17..32・5集計値）も同型の意味論固定に使う。
4. **観察の拡張（有限観察として明確に区別）**: (a) 有界witness観察 wit_max_sv ≤ r−1 のr≤160での継続判定、
   (b) 等Qブロック内の最大真約数witnessストリーム同一性（K1145観察）のr≤160での継続・破れの記録
   （8要素ブロック[89..96]・[113..120]・10要素ブロック[139..148]を含む）、(c) 各(r,p)のE側第一逸脱位相h*(Q/p,r)
   （K1154 V3/V6系譜）とwitnessの対比データ。
5. 正方向アンカー（S(C+Q(r),r)==S(C,r)、C∈窓+錨）、小rでの全称的周期集合の総当たりアンカー（r≤12）、
   twin アンカー、assemble二重実行byte一致。

## 出版計画

- 実験dir: research/experiments/remo-survivor-maximal-divisor-r49plus-20261120/（README + 検証器 + output/audit.json）
- knowledge item: 仮採番 K1162-remo-survivor-minimal-period-maximaldiv-r49to160（push直前に3点確認で再確認）
- 研究log + knowledge README末尾bullet + knowledge.yml CI step 1行追加。

## 範囲外（主張しない・着手しない）

- 生存者側の全称最小性（有界witness予想の証明）は本項では閉じない。OPENのまま。
- Δ≠0非一様盤には一切言及しない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は無関係で
  UNKNOWNのまま。fold26 receipt fold・round-5 refsolve・WIN8-D10証明書抽出・y12 universal audit・K0928 pot縮約は
  他レーン宣言済みで着手しない。

（宣言時のHEAD: d345c64594）
