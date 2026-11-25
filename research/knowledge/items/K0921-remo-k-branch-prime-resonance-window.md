---
id: K0921
title: 3枝REMO決定性の素数共鳴窓（定理PRW） — 全素数サイズ94キーは全r ≥ 2で一様決定的 ⟺ r < m または r ≥ M（共鳴窓[m,M−1]一様非決定・mixedなし・生存者は窓下P_0/アンカーP_1・exotic11の完全反鏡像・K0916休眠窓2形状とK0920傾斜状休眠系列の一般則）
kind: proposition
status: proved
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [prime resonance window, PRW, REMO prime-size window law]
relations:
- type: depends_on
  target: K0906
  note: 定理J(i)（全称）がr ≥ max(M,2)側の全称化エンジン。43キーはcommitted r=M≤7列・51キーはr=11 focus列のアンカー値を全r ≥ Mへ拡張
- type: depends_on
  target: K0916
  note: 定理PD（cap≤10分のr ≥ M側）と低r断片観察（休眠窓2形状{2,3,4}/{2,..,6}・欺瞞171キー）。本項は窓2形状がPRWのm=5/m=7のdet接頭辞であることを確定し全r法則へ統合
- type: depends_on
  target: K0920
  note: 定理PD12（prime-11分のr ≥ M側）・focus列r=10/r=11（本項の窓上端・アンカーのcommittedデータ源・sha256ピン）・傾斜状休眠系列90/273/273/704/704の出版ピン（P11Sで累積計数として完全再現）・J13アンカー
- type: depends_on
  target: K0861
  note: 定理E′（軌道簡約・全称）によりキーのverdictは実現盤面すべてに転写
- type: depends_on
  target: K0875
  note: cap≤12 Burnside計数(261749,7805,203)・47,595正準プロファイル・1,365キー・正準列挙機構（verbatimブロック）
- type: depends_on
  target: K0881
  note: committed cap≤12 r=2,7,8列（窓r < M側の有限被覆・K0882順序保存埋め込みによりcap≤10分も含む）
- type: depends_on
  target: K0876
  note: committed cap≤12 r=3..6列（同上）
- type: depends_on
  target: K0912
  note: committed cap≤12 r=9列（同上・mixed34キー再導出の源）とverbatim機構ブロック twin of record
- type: depends_on
  target: K0864
  note: 定理G′（一様決定キーの生存者=チェーン生存者・r=2..6全称保証）と補題FL（fl={C_i mod r}・全称）。本項の生存者P_0/P_1レベルはr ≥ 7で有限観察
artifacts:
- path: research/experiments/remo-k-branch-prime-resonance-window-20261117/report.md
  role: proof
  note: 定理PRWの主張と組立（定理J+PD/PD12+committed 8列+K0920 focus 2列・新規スイープなし）・94キー/m・Mセンサス・728セル全件検査（違反0・mixed 0）・生存者P_0/P_1・EXO反鏡像・COR・DORM・P11S・13機械チェック・限界・再現
- path: research/experiments/remo-k-branch-prime-resonance-window-20261117/verify_prime_resonance_window_20261117.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ・ネットワークなし・新規スイープなし。入力はsha256ピン留め10 committed packed列（8 cap≤12列+K0920 focus 2列）。機構はK0912 verbatimブロック。13機械チェック全合格・assemble二重実行・3回cold実行で監査byte同一。LIVEは独立Python mask twinが329レコード（全キーのチェーンr=2/m/M・prime-51のr=10窓上端チェーンとlightest・exotic11全12プロファイルのr=10/11）を再計算しverdict一致かつtwin状態数==engine states
- path: research/experiments/remo-k-branch-prime-resonance-window-20261117/output/prime_resonance_window_audit.json
  role: data
  note: 監査JSON（sha256 52073f67…・13チェック・(m,M)クラス表・94キー表・prime-11チェーンstates表・P11S系列込み）
scope: '極大安全集合がちょうど3個の点族（3枝合成族・正準領域・cap≤12）のREMOについて、全枝サイズが{2,3,5,7,11}でΔ≠0の94キー（43+51・1,664プロファイル）がrで一様決定的であることがすべてのr ≥ 2で r < m（m=min C_i）または r ≥ M（M=max C_i）と同値であること（共鳴窓[m,M−1]では一様非決定・全rでmixedなし）。r全称は定理J(i)（K0906全称証明）とr=Mアンカー列1本の組立で確定し、窓r < M側はcommitted列（r=2..9・prime-11はK0920 focus r=10）による完全有限検査（728セル・違反0）、定理E′経由で実現盤面に及ぶ。生存者精密化（detセルはすべてチェーン生存者・窓下P_0・アンカーP_1）はr=2..6のG′全称保証を超える部分が有限観察。EXO（exotic11反鏡像: det ⟺ r < M）・COR（r=9 mixed34キーに全素数キー0個）・DORM（休眠プレフィックスm=2/3/5/7で∅/{2}/{2,3,4}/{2,..,6}）・P11S（K0920傾斜状休眠系列=m昇順累積プロファイル計数）は有限観察。{2,3,5,7,11}の素数性が機構であることの主張・枝サイズ≥13への外挿・順位決定性・r > 11の独立スイープは含まない'
evidence: 'verify_prime_resonance_window_20261117.py全チェック合格（13/13・assemble二重実行+3回cold実行で監査JSON byte同一・sha256 52073f67…・所要約13秒）。PIN: 10列（8 committed + 2 K0920 focus）sha256一致。B: Burnside(261749,7805,203)→47,595・1,365キー。TAX: 94=43+51・m/Mセンサス{(2,3):4,(2,5):6,(2,7):8,(2,11):10,(3,5):6,(3,7):9,(3,11):12,(5,7):10,(5,11):15,(7,11):14}・1,664=393+1,271プロファイル・30多重集合計数ピン。FOC: focus 2列（1,619・同一添字集合）が51 prime-11キー全1,271プロファイルを被覆。PRW: 728セル（218+510）全件・法則違反0・mixed 0・det 266（窓下172+アンカー94）。SV: 266 detケースすべてチェーン生存者一致・窓下sv=P_0・アンカーsv=P_1（94キー一律）。FL: 使用全14,882レコード違反0。J: cap≤10分43キンのr∈[M,9] sv不変（1,365レコード・0不一致）。EXO: exotic11はr=2..10全域一様決定（生存者P_0）→r=11=Mで一様非決定（sv 0b11）の完全反鏡像。COR: r=9 mixedキー34個（生列再導出）に全素数キー0個。DORM: prime-11 det接頭辞はmだけで決まる。P11S: K0920傾斜状休眠系列{90,273,273,704,704,1271,…}がm≤r累積計数として完全再現。LIVE: 独立twinが329レコードでverdict一致かつtwin状態数==engine states（最大9,271状態）。r全称は定理Jへの依存で、窓側は完全有限検査'
---

# 3枝REMO決定性の素数共鳴窓（定理PRW・全r ≥ 2）

## 命題（定理PRW・rについて全称）

正準領域 cap≤12（47,595プロファイル・1,365キー）の3枝REMOに
ついて、枝サイズがすべて{2,3,5,7,11}でΔ≠0のキーはちょうど
**94個**（M ≤ 10が43個・M = 11が51個・1,664プロファイル）。
m = min C_i・M = max C_i とすると、**すべての r ≥ 2** で:

> K が r で一様決定的 ⟺ **r < m または r ≥ M**

すなわち共鳴窓 [m, M−1] では一様非決定で、**素数サイズキーは
どの r でも決してmixedにならない**。

生存者精密化（r=2..6はG′全称保証・それ以上は有限観察）:
detセルの生存者はすべてチェーン生存者で、窓の下（r < m）では
一様 P_0・アンカー（r ≥ M）では94キーすべて一様 P_1。

## 組立（新規スイープなし）

(1) 定理J(i)（K0906全称）により r ≥ max(M,2) 側は r=M アンカー
列1本で全r確定（43キーはcommitted r=M≤7列・51キーはK0920
r=11 focus列）。r ≥ M側の一様決定性は定理PD（K0916）・定理
PD12（K0920）と整合し本項は両方向を生列から独立再導出。
(2) 窓 r < M は728セル（218 + 510）の完全有限検査: r=2..9は
committed cap≤12列、prime-11の r=10 はK0920 focus列。
(3) 定理E′（K0861）で実現盤面に転写。γ独立性は全プロファイル
検査に含まれる。

## 新規の構造知見（有限観察）

- K0916の休眠窓2形状 {2,3,4}/{2,..,6} は **PRWの m=5/m=7 の
  det接頭辞**だと確定し、断片観察が一般則に吸収された。
- **P11S**: K0920の傾斜状休眠系列（非決定プロファイル
  90/273/273/704/704 of 1,271・r=7..10で1,271）は **m ≤ r な
  キーのプロファイル計数の累積和**（90→+183→+431→+567）に
  正確に一致。「family mixed（傾斜状）」はキーごとの一様
  状態の重ね合わせで、K0920の残課題「休眠系列の一般則」は
  PRWそのもの。
- **EXO（反鏡像）**: exotic11 (1,1,11)|0・(1,11,11)|0 は
  m=1 で、r=2..10 全域一様決定的（生存者P_0）→ r=11=M で
  一様非決定（sv 0b11）。**det ⟺ r < M** という素数キーの
  完全鏡像であり、共鳴窓法則はサイズ1枝で反転する（素数
  共鳴は低rの自明な帰結ではない）。
- **COR**: r=9境界のmixed34キー（生列再導出）に全素数サイズ
  キーは0個（mixedは合成サイズに局在）。

## 限界

- r全称は定理J（K0906）経由。サイズは≤12で有限。
- {2,3,5,7,11}は有限集合の記述で、**素数性が機構とは主張
  しない**（K0916/K0920と同一の注意）。窓 r < M 側は完全
  有限検査で、サイズ≥13への外挿はしない。
- 生存者 P_0/P_1 レベルの r ≥ 7 部分と r > 11 のmixedなしは
  組立（定理J+一様アンカー）であり独立スイープではない。
- 順位決定性は扱わない。11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class1/2/4はいずれもUNKNOWNのまま。

## 再現

`python3 verify_prime_resonance_window_20261117.py`
（自己完結・決定的・stdlibのみ・入力はsha256ピン留め10
committed列のみ・機構はK0912 verbatimブロック）。
13機械チェック全合格・assemble二重実行・3回cold実行で
監査JSON byte同一（sha256 52073f67…）。所要約13秒。
