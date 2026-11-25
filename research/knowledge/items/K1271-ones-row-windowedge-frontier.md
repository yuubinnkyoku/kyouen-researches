---
id: K1271
title: "{1}^t 行の窓端分離の全称法則: 行閉形式 A_j(k,z)（M-RC）と分離集合 S(t) の完全特徴付け（M-SEP）— K1268 E5 疎パターン課題の全称解決"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "ones-row window-edge closed form (M-RC, universal): for j>=0, k>=0, z>=max(1,2j-1) with R=z+2-2j>=1, A_j(k,z):=H(z+2-2j;{1}^k;z) satisfies k odd (k>=1): 2 iff z odd and z<=k+2j-2 / 1 iff z>=k+2j-1 / 0 otherwise; k even (k>=0): 2 iff z odd and z<=k+2j-3 / 0 otherwise; proved by strong induction on the budget R (children B: A_{j+1}(k-1,z+1) and C: A_j(k,z-1), both R-1) with a 4-way mex case split on (k parity, z parity); with d:=R-z the B-move shifts d to d-2 and the C-move keeps d, so from the window edge (j=0, d=2) only even d appear; bases R=0 (0), R=1 (H(1;{1}^k;z>=1)=2), plus the z=1/j=0 C-child min(2,k) mod 2 boundary"
  - "diagonal (M-DIAG, j=0): H(z+2;{1}^t;z)=1 for t=1, 0 for t=2, 2 iff z odd z<=t-3 for even t>=4, and for odd t>=3: 2 iff z odd z<=t-2 / 1 iff z>=t-1 / 0 otherwise (mechanically audited j=0..7, k<=44, full z-range, 26,190 states, bad 0)"
  - "separation law (M-SEP, unified window W(z,1)=max(z+1,2), edge R*=W+1: z>=1 -> R*=z+2, z=0 -> R*=3): {1}^t separates from the single token (t) exactly at: t=1: nowhere (row is a single token itself); t=2: nowhere (K1265 total collapse row S(2)=empty); even t>=4: S(t)={0} ∪ {z odd: 1<=z<=t-3}; odd t>=3: S(t)={0} ∪ {z odd: 1<=z<=t-2} ∪ {t-1,t}; separating values: z=0 parent 0 vs single 1 (T1 = K1267), odd z in the staircase parent 2 vs single 0 (T2 generalized from (z,R)=(1,3) to the whole odd staircase), for odd t also {t-1}: parent 1 vs single 0 and {t}: parent 1 vs single 2; resolves in full the K1268 open lane 'E5 sparse pattern general law' (observed t=3: {0..3}, t=5: {0,1,3,4,5}, t=7: {0,1,3,5,6,7} are exactly S(3), S(5), S(7); even-t odd staircase included); machine audit of the declared protocol 31,079 points / 93,210 comparisons / bad 0, separating points 546 = pre-declared arithmetic value, fail-closed tamper battery 10/10 caught, 4 runs byte-identical"
relations:
- type: depends_on
  target: K0832
  note: 単一トークン閉形式 v(t,z,R)（M-SEP の対側・z=0 の R*=3 条款 v(t,0,3)=1）。機体エンジンは K0832/K1138系の出版再帰定義に由来。
- type: depends_on
  target: K1264
  note: 機体エンジン block（2,508B・SHA-256 bd5f22e4…）は出版 K1264 検証器（108fdd65…）と出版 K1268 機（0ab66665…）から build_engine_from_published.py（d99361a3…）が三方 byte 照合で機械抽出（PROVENANCE PASS・手転写ゼロ）。
- type: extends
  target: K1267
  note: T1（(z,R)=(0,3)・全 t>=3 の親0 vs 単一1 分離）は S(t) の z=0 要素として従う。D4 アンカーで t=3..12 再照合。
- type: extends
  target: K1265
  note: {1,1} 行（t=2）の全 R 崩壊が S(2)=∅ として再証明。D4 アンカーで z<=12・R<=8 を両エンジン再照合。
- type: extends
  target: K1268
  note: 未解決課題「E5 {1}^t 行の疎パターンの一般則」の全称解決（証明付き）。E5 観測 t=3..8・z<=24 は S(t) の t<=8 切片。分離 sweep D3（t<=44・z<=54・分離546点）で出版観測と bad 0。
- type: related
  target: K1269
  note: T2 の (z,R)=(1,3) 分離（全 t>=3・親2 vs 単一0）は本項 M-SEP の z=1 要素（t 偶数>=4 は 1<=t−3、t 奇数>=3 は 1<=t−2 で常に z=1 ∈ S(t)）。本項は全 z を含む行法則として独立に導出・K1269 は同事実の単点昇格（並走出版 5fa9ce83）。両者で {1}^t の z∈{0,1} が全 t で確定。
- type: related
  target: K1270
  note: min(X)>=2 の低z banded 拡張（z∈{0,1} で窓+1 まで全形状崩壊）と本項（min=1 の全 z 行法則）は min の値で分割された相補な全称結果。K1270 が指摘するとおり min=1 は banded 拡張の境界であり、その境界行の全 z 構造が本項。両者の併合分類表は resume 課題（run log 記載）。
artifacts:
- path: research/log/2026-11-23-ones-row-frontier-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（commit 55e6b109・先行出版・M-RC/M-DIAG/M-SEP 証明全文開示・protocol D1-D4 事前登録・宣言点数・照合数・分離546の算術予想値・宣言前探査の全開示）。
- path: research/experiments/ones-row-windowedge-frontier-20261123/report.md
  role: proof
  note: 実験正本（主張・証明要旨・監査全数値・決定性・誠実記録4点・min>=2 banded との関係）。
- path: research/experiments/ones-row-windowedge-frontier-20261123/verify_ones_row_frontier.py
  role: verifier
  note: 監査機体（SHA-256 1ce7df23…・D1 A-family 26,190点 / D2 対角+z=0列 2,244点 / D3 分離sweep 2,420点 / D4 出版アンカー 225点・fail-closed・変異電池10種）。
- path: research/experiments/ones-row-windowedge-frontier-20261123/output/audit.json
  role: data
  note: 監査正本（SHA-256 fb35211a…・総93,210照合 bad 0・分離546・隔離env込み4実行 byte-identical）。
- path: research/experiments/ones-row-windowedge-frontier-20261123/build_engine_from_published.py
  role: verifier
  note: プロビナンスゲート（SHA-256 d99361a3…・K1264/K1268 両機からの engine block 三方照合抽出）。
- path: research/log/2026-11-23-ones-row-frontier.md
  role: log
  note: run log（T2 回避→E5 レーン選定の経緯・宣言→実行→出版の全記録・M1 no-op 差替えの開示・resume 課題）。
scope: >-
  {1}^t 行（min(X)=1・アリティ t の残余ゲーム H(R;{1}^t;z)）の窓端全状態族
  A_j(k,z)（j>=0・R=z+2−2j）の値の全称閉形式（M-RC）と、統合窓 W(z,1)=
  max(z+1,2) の窓端 R*=W+1 における単一トークンからの分離集合 S(t) の完全
  特徴付け（M-SEP）。全称性は紙面の強帰納（予算 R 減少・mex 場合分け4通り・
  d=R−z は窓端から偶数値しか取らないことによる閉包）による。機械監査
  31,079点・93,210照合・bad 0（有限域の独立検証）は全称性の根拠ではない
  （AGENTS.md 区分・証明は宣言ノート全文開示）。d 奇数の状態（窓端から
  到達不能）の値・min>=2 側の全形状（banded 拡張レーン所管）・アリティ>=3
  の一般X・固定幅・q点版・r人対戦・d次元は範囲外。標準11×11の空盤・
  二石root・S2 {59,60}・class 1/2/4 はどの時点でも UNKNOWN のまま。
---

## 命題・範囲

M-RC: j>=0・k>=0・z>=max(1, 2j−1)（R=z+2−2j>=1）で A_j(k,z):=H(z+2−2j;{1}^k;z) は
k 奇数（k>=1）なら 2 ⟺ z 奇数 かつ z<=k+2j−2 / 1 ⟺ z>=k+2j−1 / 0 その他、
k 偶数（k>=0 を含む）なら 2 ⟺ z 奇数 かつ z<=k+2j−3 / 0 その他。

M-SEP: 統合窓端 R*=W(z,1)+1（z>=1 は z+2・z=0 は 3）で {1}^t が単一トークンから
分離するのは t=1 なし・t=2 なし・t 偶数>=4 は S(t)={0}∪{z 奇数: 1<=z<=t−3}・
t 奇数>=3 は S(t)={0}∪{z 奇数: 1<=z<=t−2}∪{t−1,t} ちょうど。

分離値: z=0 親0 vs 単一1（T1）・z 奇数は親2 vs 単一0（T2 の全 z への拡張）・
奇数 t の {t−1} は親1 vs 単一0・{t} は親1 vs 単一2。

## 現在の根拠と限界

全称性は強帰納（予算 R について・子は B手 A_{j+1}(k−1,z+1) と C手 A_j(k,z−1) の
みで双方 R−1・d=R−z は B手で −2・C手で不変なため窓端 j=0 の d=2 から偶数 d に
閉じる）。基底 R=0（0）・R=1（2/0）・境界 z=1/j=0 の C子 min(2,k) mod 2。
場合分け (1) k奇・z偶 / (2) k奇・z奇 / (3) k偶・z奇 / (4) k偶・z偶 の4通りで
mex が CFG 目標値と一致（閾値の偶奇により中間の空の場合は消える）。証明は
宣言ノート（commit 55e6b109）で全文開示。M-DIAG は M-RC の j=0 系、M-SEP は
M-DIAG と K0832 単一閉形式の命題的な合わせ。

機械監査（宣言 protocol D1-D4・事前登録値と完全一致・ドリフトなし）:
31,079点 / 93,210照合 / bad 0・分離点 546=宣言算術値・電池10種全捕捉・
隔離env込み4実行 byte-identical。有限機械監査は証明そのものではない。

限界・open: A_j 族の d 奇数状態（窓端から到達不能・到達可能性込みの拡張）、
min>=2 側の banded window 拡張（K1270・並走出版 5fa9ce83）との
統合、t=1/z>=1 の崩壊行と t=2 行の windowedge 外構造、アリティ>=3・一般Xへの
S(t) 型法則の一般化、固定幅・q点版・r人対戦・d次元版。T2 点 (z,R)=(1,3) の
独立昇格 K1269（同出版）は本項の z=1 切片に含まれる（related・機体は非接触）。標準11×11・二石root・S2 {59,60}・
class 1/2/4 は常に UNKNOWN のまま。
