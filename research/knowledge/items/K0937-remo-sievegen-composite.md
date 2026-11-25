---
id: K0937
title: "SIEVE構造の全称完結: 不変量INV-TRACK・合成数側死亡定理SIEVE-COMPOSITE-GEN（全spf）・双子法則の全称化"
kind: proposition
status: proved
topics: [variants, multiplayer, strategy-length]
aliases: []
relations:
- type: depends_on
  target: K0928
- type: depends_on
  target: K0931
- type: depends_on
  target: K0933
- type: depends_on
  target: K0934
- type: depends_on
  target: K0935
- type: depends_on
  target: K0936
- type: related
  target: K0919
- type: related
  target: K0929
artifacts:
- path: research/experiments/remo-sievegen-composite-20261118/report.md
  role: proof
  note: "INV-TRACK（監視距離不変量）・死亡合同式・t=1へのWATCH-MAP拡張と限界特定・SIEVE-COMPOSITE-GEN・双子法則のmod 210制限除去の全称証明レポート"
- path: research/experiments/remo-sievegen-composite-20261118/sievegen_core.py
  role: solver
  note: "track_gen/play_full等の共有コア（K0934-K0936検証器からverbatim・以降の実験群でpinned byte同一コピーとして参照される）"
- path: research/experiments/remo-sievegen-composite-20261118/sievegen_verify.py
  role: verifier
  note: "12チェックの機械アンカー（全前提を検証）"
- path: research/experiments/remo-sievegen-composite-20261118/audit_build.py
  role: verifier
  note: "監査アセンブラ（2回in-process実行一致・2回コールド実行でbyte同一）"
- path: research/experiments/remo-sievegen-composite-20261118/output/sievegen_audit.json
  role: data
  note: "監査正本（file sha256 5281e92e…・12チェック表）"
date: 2026-11-18
tags: [remo, uniform-board, counting-recursion, ladder, stretch, watched-tracking, sieve, invariant, twin-laws, machine-evidence]
---

## 主張（すべてK0928のpot力学上。合成数側は本項で全称証明・素数側はK0939で全称証明）

### 定理INV-TRACK（不変量・全称）

V(m)（監視ラベル0・N=2m+1）・U(m)（監視ラベルm−1・N=2m+3）について、
監視が生存する限りの**すべての**stretch-w開始状態（w≥2・t=n//(w+1)≥1・
ladder regime）はF(w,h;n)で表され、監視距離aは

- V: **a = h**（h≥1）、U: **a = h+1**

を満たす。石数T = wn+h+wは毎stretch不変で、基礎状態はV: F(2,1;m−1)・a=1
（T=N）、U: F(2,0;m)・a=1（T=N−1）。帰納段はWATCH-MAPの事例別純代数
（INV条件下ではfront逆ケースa≤r<hとback逆ケースa>r≥hが発生しない）。

### 定理（死亡合同式・全称）

INV条件下で、stretch-wで監視が死む ⟺ a = r+1 ⟺ **(w+1) | N**。
（T恒等式とINVから T ≡ h−a (mod w+1)、V: T=N・a=h、U: T=N−1・a=h+1。）
K0935 (e)の死亡判定はt≥2に限るが、本項はt=1も含み、かつt=1では(e)は
一般に偽（反例 (w,h,n,a)=(5,0,8,5): breaking敗者w−rとしてa≠r+1でhot死）な
ことを特定。正しいt≥1全域の判定は排出集合判定（元位置がblock j(w+1)−1
(j≤J) またはbreaking敗者）。INV条件下ではt=1でも死亡 ⟺ a=r+1
（V: r=h−1 / U: r=h）が復元される（危険ケースは2r=h−1<h resp. 2r=h≤r
で代数的に不可能）。

### 定理SIEVE-COMPOSITE-GEN（合成数側・全spf・全称）

N=2m+sが合成数なら監視は**stretch spf(N)−1で死亡**する:

- V: breaking敗者としてのhot死・保持spf(N)・死亡フェーズ=t=n//(w+1)
  （stretch最終フェーズ）。
- U: block-t敗者としてのcold死・保持spf(N)−1・死亡フェーズ=t
  （t=1・r=h=0すなわちN=(w+1)²のcollapse stretchでもblock-1として
  保持w・フェーズ1）。

stretch 2..spf(N)−2では一切死亡しない。REGIME補題: 合成N（spf p）では
stretch 2..p−1のすべてでt≥1かつゲーム終了前にladder regimeが保たれる
（n≤w仮定がT下界p²−1と矛盾; n2=1は(w,t)=(2,1)の場合のみでN=9は
stretch-2で死亡済み）。これによりK0936の系SIEVE-COMPOSITE（spf∈{3,5,7}）
は**全spfへ拡張**され、spf≥11に依存する残りmod 210類を含む合成数側が
閉じた。

### 系TWIN-COMP-GEN（双子法則の全称化）

- すべての奇数合成C≥9: P(C)≠1。すべての偶数C≥2かつC+1合成: P(C)≠C−1。
- K0936の57+57類制限を除去。類内素数インスタンスの有限ピン
  （P(3)=P(5)=P(7)=1・P(2)=1・P(4)=3・P(6)=5）と合わせ、
  「P(C)=1 ⟹ C素数」「P(C)=C−1 ⟹ C+1素数」はmod類制限なしの全称定理。

### 定理（素数側ladder部分）と定理SIEVE-PRIME（K0939で証明済み）

N素数なら監視は**すべてのt≥1 stretchを生存する**（死亡⟺(w+1)|Nだが
t≥1 stretchではw+1=NがT恒等式と矛盾）。素数ゲームは必ずt=0 endgame
（n≤w）に入るため、残るOPENは**t=0エンドゲームが監視を殺さないこと**
（= survivor）に正確に特定された。出版時は予想SIEVE-PRIMEとして明示し、
m≤2600両側の新鮮engineで全素数ゲーム（deathなし・survivor==監視）を
機械確認済みだったが、**K0939で全称証明された**（エンドゲームは
END-INV・ENTRY-LOCの下で約数篩END-SIEVEで、family状態上で監視生存⟺
N素数。N素数ならV(m)=0・U(m)=m−1）。これにより逆方向（C素数⟹
P(C)=1）を含む双子法則LAW1/LAW2の完全iffが全称定理化した
（K0929・K0939参照）。

## t=1レジームのWATCH-MAP拡張（実装ギャップの解消）

K0935のwatchmapはn≥2w+2（t≥2）に制限されていた。本項はt=1（w+1≤n≤2w+1）
でもcensus F(w+1,h2;n2)が成立し、**INV関連距離a∈{h,h+1}では同一のa2公式**
が成立することを位置計算で証明し、全t=1グリッド（w≤11・1,075 INV関連+
6,075全窓）でミニエンジン照合。非INV窓ケースのa2はt=1で崩れる
（270偏差を観測記録: front式は幾何変化・back式はn2超過）。定理が使うのは
INV関連のみで、INV到達可能性の論証と合わせて全称性は紙上証明による。

## 機械的証拠（sievegen_core.py・sievegen_verify.py・audit_build.py）

12チェック全合格: PIN・REDRECON（7,998比較0不一致）・T1MAP（t=1: INV関連
1,075・全窓6,075・collapse 75・0失敗）・T2REG（t≥2で拡張watchmap==出版
watchmap 3,258）・DEATHFAST（O(1)排出判定==LAD-GEN elim意味 5,115・0失敗）
・**INVGEN（m≤200,000両側・400,000ゲーム・36,818,347 stretch entryで
INV・T恒等式・合成死亡則0失敗。死亡332,283・endgame exit 67,717・
最大死亡stretch 630=spf 631・631²=398,161）**・FRESHPIN（m≤2,600・5,200・
コミット表一致）・CANON（tracker全stretch entry==engine・t=1含む86,615・
0失敗）・TRK（死亡pot・保持・フェーズまで照合5,200・0失敗）・
SIEVEOBSGEN（engine版spf則・合成3,819ゲーム・0失敗）・SV7REG（K0936回帰:
domain 684対・stretch-5無死・stretch-6⟺7|N・0失敗）・TWINCOMP（コミットP表
C≤8000: 合成2,993+2,993・0違反・素数側観測1,006+1,006）。audit_build.pyは
2回in-process実行一致・2回cold実行でbyte同一（output/sievegen_audit.json・
file sha256
5281e92e221ffd589b56dc712e2ad76308d12c51c792496d2216ee3657c761d2）。
拡大: K0936の機械範囲（m≤700・stretch≤6）からトラッカー法則は
m≤200,000（N≤400,003・stretch≤630）へ、engineアンカーはm≤2,600
（N≤5,203・死亡stretch≤70）へ。全称性は紙上証明による。

## 範囲と限界

- 一様盤・ゼロリセット・K0859再帰（K0928定理RED経由）のみ。非一様盤・
  11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4は一切
  言及しない（**UNKNOWN不変**）。
- 素数側は本項出版時点では**予想**（SIEVE-PRIME）だったが、**K0939で
  全称証明済み**（エンドゲームEND-SIEVE理論）。「C素数⟹P(C)=1」は定理。
- t=1の非INV窓ケースのa2公式は主張しない（観測270偏差を記録）。
- t=1ではK0935 (e)のa=r+1判定は一般に偽（上記反例）。本項の死亡判定は
  (e)に依存しない排出集合判定。
- K0936のdeath_infoはcollapse stretchのblock-1死亡に対しheld=w+2を返す
  実装特性がある（engine真理はheld=w）。K0936のtrack()はw≥6で打ち切る
  ためpublished結果に影響しない。本項のdeath_fastはengine真理に合わせ
  （TRKで照合済み）。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （前項の高速レーン項目と同じ扱い）。generated/とroot READMEは未編集。
