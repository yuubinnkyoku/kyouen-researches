---
id: K0941
kind: proposition
status: proved
title: 合成NのV(m)/U(m)完全決定（LADDER-ONLY・死の二分法・E-game閉包・ラベル合成）と全m値の純算術化
aliases: []
relations:
  - depends_on: [K0928, K0934, K0935, K0937, K0939]
  - connects: [K0929, K0931, K0933, K0936, K0922, K0919, K0943]
artifacts:
  - research/experiments/remo-composite-values-20261118/report.md
  - research/experiments/remo-composite-values-20261118/sievegen_core.py
  - research/experiments/remo-composite-values-20261118/composite_core.py
  - research/experiments/remo-composite-values-20261118/composite_verify.py
  - research/experiments/remo-composite-values-20261118/audit_build.py
  - research/experiments/remo-composite-values-20261118/output/composite_values_audit.json
date: 2026-11-18
tags: [remo, uniform-board, counting-recursion, composite, ladder, endgame, josephus, machine-evidence]
---

## 主張（K0939の残課題「合成Nの値そのもの」を閉じる。全定理が紙上全称証明）

### 定理A（LADDER-ONLY・全称）

奇合成N（N=2m+1+s・s=0がV・s=1がU）の監視は、ladder regimeを生存して
t=0エンドゲームに入ることができない。したがって（K0937死亡合同式により）
監視は**ladder stretch spf(N)−1で必ず死に**、それ以前のstretchでは死なない。
証明: stretch 2..w−1の生存はNが3..wのどの数でも割れないことを意味し、
Nの素因数はすべて≥w+1（N奇）。N合成なのでN≥spf(N)²≥(w+1)²。
一方ENTRY-LOC（K0939・素数性不使用）のfamily範囲では
N=w(n+1)+h+s≤w²+2w<(w+1)²（V: h≤w・U: h≤w−1）。矛盾。

### 定理B（死の二分法と死後状態・全称）

死亡合同式 a=r+1（K0937）より **V死は必ずbreaking死**（a=h→r=h−1・
保持w+1 hot）・**U死は必ずblock死**（a=h+1→r=h・保持w cold）。
LAD-GEN（K0934）のdeal構造から:

- **V**: breakingのdeal [n−h−w, n−h−2] はtail [n−h, n−1] に触れないので
  残存全員が保持w+1となり、死後状態は一様 **Z(w+1, n−t)**
  （pot w+1・人数n−t・フレームはn−h+1から）。
- **U（非崩壊）**: block死後も同一stretchのbreaking位相が走り
  （bl=w−r（r≥1）またはw+1（r=h=0・t≥2））、その直後は
  **E(w+1; n−t−1−w, w)**（[w+1]^α+[w+2]^w・pot w+1・フレームbl+1から）。
- **U（崩壊 (t,h,r)=(1,0,0)）**: collapse位相（q=1・敗者位置0）を挟んで
  **Z(w+2, w−1)**（フレームは位置1から）。

### 定理C（E-game閉包と生存者位置σ・全称）

任意のE状態 E(P;α,β)（k=α+β・holdings [P]^α+[P+1]^β・pot P・ptr先頭）は
1フェーズ後もE形式を保つ: r<α→E(P+q; α−r−1, β+r)・
r≥α→E(P+q+1; β+2α−r−1, r−α)（K0939 END-INVの帰納段と同一の
状態局所計算・family入口という仮定を除去）。一様状態は
Z(M,K)→1フェーズ→E(M+q; K−1−r, r)（q,r=M div/mod K）。
最終生存者の入口フレーム位置は**逆合成再帰**
σ_旧=(r+1+σ_新) mod k（基底 k=1 で σ=0）、
σ_Z(M,K)=(r+1+σ_E(M+q, K−1−r, r)) mod K。
σの閉形式は現在知らない（Josephus型の有限算術再帰そのものが決定結果・O(k)）。

### 定理D（ラベル合成）と系COMPOSITE-VALUES（全称）

死亡stretch開始フレームの「フレーム位置→元ラベル」写像は:
Vはフェーズ1後の LS[i]=(i+2) mod m（長さm−1）・Uは LS[i]=i（長さm）、
生存した各stretchでLAD-GEN除去集合 { j(w′+1)−1: j≤J′ }∪{bl′} を除去して
bl′+1から再フレームする操作を反復し、死亡stretchで定理Bの除去を適用して
死後フレーム（ラベル列）が得られる。よって

**合成Nの V(m)/U(m) = frame[σ] は純算術で完全決定される。**
SIEVE-PRIME（K0939・素数N: V=0/U=m−1）と合わせて**全m≥1のV/U値が
純算術決定**となり、K0928定理RED経由で **P(C)（全C≥2）も純算術決定**。

## 機械的証拠（composite_verify.py・audit_build.py）

sievegen_core.pyはK0937 committed版のbyte同一コピー
（sha256 a69f916c86ed02d5eeed3d5494bbb0f44f652d0d1e4714c50bbc68bef1843499）。
7チェック全合格:

- **PIN**: K0929コミット表のsha256・形式・P(1..40)ピン照合。
- **DEATH**: 合成m≤8,000両側12,277ゲーム: tracker status全died・
  死亡stretch w=spf(N)−1・V: r=h−1・保持w+1・U: r=h・保持w。違反0
  （定理A系・定理B二分法の全範囲アンカー）。
- **FULLREPRO**: 全m≤8,000両側16,000値: 純算術predict（合成は本項・
  素数はSIEVE-PRIME）がコミットU/V表と完全一致（0不一致）。
  **コミット済み全値が純算術から再構成**された。
- **STRUCT**: 合成m≤1,500両側2,141ゲーム: リテラル位置エンジンの
  死後境界ptr円ラベル列==合成フレーム・holdings/pot==定理Bの死後状態
  （Z/E形式・値・順序）・最終生存者==frame[σ]。0失敗
  （定理B/C/Dの構造アンカー・保持記録はdeal前時点の実装どおり）。
- **EGAME**: 一般E状態（P∈{3,7,12,25,60,120}・k≤50・全α）と一様状態
  （M∈{2,3,5,9,20,47}・K≤50）計8,238状態: リテラル状態エンジンの
  生存者==σ_E/σ_Z。0失敗（定理Cをfamily・死後状態の外の一般状態でアンカー）。
- **ENGINE**: m≤600両側1,200ゲーム: 新鮮python engine play_fullの
  生存者ラベル==predict（素数・合成の全mで値レベル一致。
  K0939が監視生死のみ検証していたのを強化）。
- **P2OBS**（当時は観察・K0943で全称証明へ昇格）: U崩壊死(t,h,r)=(1,0,0)⟺N=spf(N)²
  （29例↔29例の全単射）・V側N=p²の死亡stretch状態は常に(n,t,r,h)=(p,1,0,1)
  （m≤8,000・違反0）。K0943の系P2が両方向を全称証明（m≤30,000・52↔52で機械確認）。

audit_build.pyはrun_checksを1回in-process実行し、さらに
composite_verify.py（内部でrun_checksを2回実行してin-process決定性を検証）
を2回cold実行してbyte同一を確認し、output/composite_values_audit.jsonを書く
（監査sha256 97e854f7311ac24784fa7165a1a4dba55fca6727569af07e88b281e0f2558961）。

## 範囲と限界

- 一様盤・ゼロリセット・K0928定理RED経由の設定のみ。非一様盤・11×11空盤・
  二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4には一切言及しない
  （**UNKNOWN不変**）。
- σ_E/σ_Zの閉形式は主張しない（再帰が決定結果）。
  σ_Z(3,K)（K偶数・K≤4,000）の値1位置は豊富（4,8,12,28,40,52,72,…）で
  単純な倍数構造には乗らない。
  → K0945でONE-CHAR全称特徴付け（σ_Z(3,K)=1 ⟺ σ_E(3;K mod 4, 3⌊K/4⌋)=K mod 4+1）・
  A2-NEVER（K≡2 (mod 4)は全称的に値1を取らない）・fold分解（RUN-3/FOLD）・FAST算法が出版された。
- P2OBSはK0943（STATE-CF・DS-CF・P2）で全称証明済み（h-walk記述は不要だった）。
- 定理B/C/Dの紙上証明はK0934（LAD-GEN）・K0939（ENTRY-LOC・END-INV遷移）・
  K0937（死亡合同式・INV-TRACK）の出版済み証明に依存する。機械アンカーは
  この依存構造込みで16,000値再構成+2,141ゲーム構造照合+8,238状態照合を
  0失敗で裏付ける。
- `uv run check/build`・unittestは本環境にcloneとuvがないため未実施
  （K0937/K0939と同じ扱い）。generated/とroot READMEは未編集。
