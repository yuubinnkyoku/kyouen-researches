---
id: K1272
title: "クリティカルストリップ拡張 (z∈{2,3,4}・min(X)=m>=3): H(z+m+1;X;z)=v(ΣX,z,z+m+1)（F/R2/D 有限z梯子+選択肢集合一致+m帰納の全称証明・K1270 と併せ K1268 予想C1 の m=3 行を完全解決）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip banded window extension: for every m>=3, every z in {2,3,4} and every nonempty finite multiset X with min(X)=m, H(z+m+1;X;z)=v(sumX,z,z+m+1); together with K1270 (z in {0,1}, min>=2) this resolves the entire C1 band z<z*(3)=5 for m=3, i.e. the complete m=3 row of K1268 Conjecture C1, for all shapes and all arities"
  - "z-ladder lemma structure: Lemma U (H(2;{1}+Y;0)=0 for every nonempty Y with min(Y)>=2, and 1 for Y=()), Lemma F (the F-cell value F(s,z)=H(z+2;{1}+Y;z) is independent of the decomposition of s into 1..4 tokens >=3 and follows the z-indexed closed table for z in {1,2,3,4}), Lemma R2 (H(z+3;{2}+Y;z)=v(s+2,z,z+3) for z in {0,1,2,3}; z in {0,1} is K1270, z in {2,3} is new), Lemma D (D(s)=H(7;{2}+Y;4) is 0/1/2/1 at s=0/3/4/>=5; the z=4 collapse fails exactly at Y=(4,), D(4)=2 != v(6,4,7)=1, an arithmetic consequence of the closed forms)"
  - "proof technique: finite z-ladder + option-set identity + induction on m. The F/R2/D cells are closed by direct case computation from the K0832 single-token closed form; in the T-B parent (z+m+1;X;z) every a>m child hits the K1264 stair window edge exactly (budget z+m=z+min), every a=m child lands in an F/R2/D cell (m=3) or the induction hypothesis C(m-1,z) (m>=4), and the C-child lands in the K1270 z=1 slice (z=2) or the already-proved C(m,z-1); the resulting option set {v(sum-1,z,z+m), 1^v(sum,z-1,z+m)} coincides with the single-token side and both mexes are equal"
  - "boundary sharpness: z<=4 is optimal for m=3 (the frontier z*(3)=5 separates at the published K1268 witness (4,3)@R*=9, parent 2 vs single 0); the naive m=2 extension beyond the band is false (frontier z*(2)=2, witness (2,2)@z=2, parent 2 vs single 1); min=1 separates at window+1 via T1/K1267 (z=0) and T2/K1269 (z=1)"
relations:
- type: extends
  target: K1270
  note: "K1270 が全称証明した低zスライス (z=0,1) の banded 拡張をクリティカルストリップ z∈{2,3,4} まで拡張する。m>=3 では両者を併せ z∈{0..4}=バンド z<z*(3)=5 全域が確定し K1268 予想C1 の m=3 行が完全解決される。証明の C手評価は K1270 の z=1 スライスを直接引用する。エンジンは K1264→統合窓→K1271 と同一の出版 sha-gate 鎖（engine block 2,508B SHA-256 bd5f22e4…）から機械抽出。"
- type: depends_on
  target: K1264
  note: "階段定理（空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R)）。T-B 証明の a>m 子（K1268 窓端等式）・Fセルの A手子・R2 の A手子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。F/R2/D 梯子の全場合計算と単一側選択肢集合の算出基盤。"
- type: related
  target: K1268
  note: "統合窓 sharpness から登録された予想 C1（m>=2・z<z*(m)・R=z+m+1 の全 X 崩壊）の m=3 行を K1270 と併せて完全解決。前線 witness (4,3)@R*=9 との整合で T-B の z<=4 の最適性を確認。m>=4 行・上位帯 z>=5 は open のまま。"
- type: related
  target: K1271
  note: "min=1 行 ({1}^t) の窓端分離法則 S(t) と対照。F セル H(z+2;{1}∪Y;z) は混合 arming（1トークン+大きなY）が初めて閉形式に落ちた点で、min=1 行と min>=2 行の窓構造を接続する境界セル。"
- type: related
  target: K1267
  note: "境界の鋭さ: min=1 では窓+1 の z=0 が T1 で分離するため min>=2 系の仮定は鋭い（本項目は m>=3 を要求する）。"
- type: related
  target: K1269
  note: "境界の鋭さ: min=1 では窓+1 の z=1 が T2 で分離する。T-B の帰納で K1270 の z=1 スライスを引用する点でも接続。"
artifacts:
- path: research/experiments/min3-banded-strip-z2z4-20261123/report.md
  role: proof
  note: 機械監査の正本記録（D1-D7+census・変異電池・決定性・provenance・誠実記録）。証明全文は宣言ノート §2 にあり本 report は証明そのものではない。
- path: research/experiments/min3-banded-strip-z2z4-20261123/verify_min3_banded_strip.py
  role: verifier
  note: "専用機体（SHA-256 009184eff1accbaa82cdea9eea5e81253252e6d3681e893b1fd30506d6acad9c・audit/tamper 両モード・engine block は3出版源から sha-gate 機械抽出）。D1-D7 宣言 protocol・12変異電池 B1-B12。"
- path: research/experiments/min3-banded-strip-z2z4-20261123/build_engine_from_published.py
  role: verifier
  note: "provenance sha-gate（出版 K1264 検証器 108fdd65…・出版統合窓機 0ab66665…・出版 K1271 機 1ce7df23… の3源から engine block を cut・3方 byte 照合 + pin bd5f22e4… 照合・PROVENANCE PASS・手転写ゼロ）。"
- path: research/experiments/min3-banded-strip-z2z4-20261123/output/audit.json
  role: data
  note: "監査正本（SHA-256 c199946ad562fb7b20f20272a261a58d31cbebc61b7b6caba4c4335c83094af9・宣言総計 21,565点/64,730比較 bad 0 と完全一致・4実行 byte-identical）。"
- path: research/log/2026-11-23-min3-banded-strip-z2z4-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 4be51cb6・U/F/R2/D + T-B の証明全文を機械実行前に先行開示・publish-then-execute・宣言前探査の全開示を含む）。
- path: research/log/2026-11-23-min3-banded-strip-z2z4.md
  role: log
  note: run log（探査→宣言→機体組立→監査→出版→fetch-back 検証・誠実記録）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰・K0832 単一トークン閉形式 v）について、
  すべての m>=3・z∈{2,3,4}・min(X)=m を持つ空でない任意の有限多重集合 X（全形状・
  全アリティ）に対して H(z+m+1;X;z)=v(ΣX,z,z+m+1) が成立するという全称命題
  （proved・F/R2/D 有限z梯子+選択肢集合一致+mに関する帰納）。同一証明に含まれる
  数学的部品として Lemma U（H(2;{1}∪Y;0)）、Lemma F（F セル閉形式表・分解非依存）、
  Lemma R2（z∈{0..3}）、Lemma D（z=4・D(4)=2 の deviant は Y=(4,) ちょうど）も
  主張に含む。m>=2 の z=2 前線（K1270 出版 witness で T-B の外延ではない）、
  m>=4 の上位帯 z>=5（E3(z) 梯子の z=5 延長が未解決）、m=2 行の z>=2 前線以遠、
  min=1 行・窓+2 以上の一般保証は範囲外。D6c census の z=5・m∈{4..7} 崩壊観測
  （grid 上 384/384・反例不在）は観測記録であり本 item の主張ではない。
  標準11×11の空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 5343 は
  範囲外かつ UNKNOWN のまま。nodes 数・wall 秒数を勝敗として読まない。
---

## 命題・範囲

残余ゲーム H(R;X;z) について:

1. **Lemma U**: Y を空でない多重集合（トークンすべて >=2）とすると
   H(2;{1}∪Y;0)=0。また H(2;{1};0)=1。
2. **Lemma F**: s∈{0}∪{3,4,...} に対し F(s,z):=H(z+2;{1}∪Y;z)
   （Y は ΣY=s・トークン>=3・s>0 なら Y≠∅）は Y の分解に依らず
   z∈{1,2,3,4} で閉形式表に一致する:
   F(s,1)=1 (s=0) / 2 (s>=3)。
   F(s,2)=1 (s=0) / 0 (s>=3)。
   F(s,3)=1 (s=0) / 0 (s=3) / 2 (s>=4)。
   F(s,4)=1 (s=0) / 0 (s=3) / 1 (s=4) / 0 (s>=5)。
3. **Lemma R2**: H(z+3;{2}∪Y;z)=v(s+2,z,z+3)（s:=ΣY）が z∈{0,1,2,3}。
   z∈{0,1} は K1270・z∈{2,3} が本項目の新規部分。
4. **Lemma D**: D(s):=H(7;{2}∪Y;4) は D(0)=0・D(3)=1・D(4)=2・D(s>=5)=1。
   z=4 では崩壊は丁度 Y=(4,) で破れる（D(4)=2 ≠ v(6,4,7)=1・D式からの算術帰結）。
5. **Theorem T-B（主定理）**: すべての m>=3・z∈{2,3,4}・min(X)=m の空でない
   任意の有限多重集合 X に対して H(z+m+1;X;z)=v(ΣX,z,z+m+1)。
   K1270（z∈{0,1}）と併せ m>=3 では z∈{0..4} で窓+1 崩壊が全形状・全アリティで
   成立し、m=3 ではバンド z<z*(3)=5 全域が確定して **K1268 予想 C1 の m=3 行が
   完全解決**される（m>=4 の上位帯 z*(m)-1>=5 は open のまま）。

境界の鋭さ: m=3 は (4,3)@z=5・R*=9（親2 vs 単一0・K1268 前線 witness）で分離し
z<=4 は最適。m=2 への素朴拡張は偽（(2,2)@z=2・親2 vs 単一1・K1270 出版 anchor）。
min=1 は T1/K1267・T2/K1269 により窓+1 で分離。

## 現在の根拠と限界

全称性の証明は選択肢集合一致型（K1270 の手法の z 方向拡張）: 単一側の選択肢
集合 {v(Σ−1,z,z+m), 1^v(Σ,z−1,z+m)} に対し、親側の各手が a>m 子は《stair》
（K1264）窓端ちょうどの等式、a=m 子は F/R2/D セルまたは帰納仮定 C(m−1,z)、
C手は K1270 の z=1 スライスまたは C(m,z−1) に落ち、値集合が完全一致して両 mex
が等しい。帰納は m=3 を底に（まず R2 で z=2,3、次に D で z=4）、m>=4 は
m と z の有限樹状帰納で確定する。証明全文は宣言ノート（commit 4be51cb6）§2 に
機械実行前に先行開示した（publish-then-execute）。

機械監査（宣言 protocol D1-D7・事前登録値と完全一致・ドリフトなし）:
宣言総計 21,565点 / 64,730比較 / bad 0（D1 U掃引 495 / D2 F 全分解 14,628 /
D3 R2+D+deviant集合 1,650 / D4 T-B grid m∈{3..8}×222形状 3,996 /
D5 固定seed乱数深部 360 / D6a 出版アンカー17 / D6b 本項アンカー23 /
D7 選択肢集合検査 396）。変異電池 B1-B12 は 12/12 捕捉・隔離env込み4実行で
audit.json byte-identical（SHA-256 c199946a…）・機体と出版実験dirは
fetch-back byte 一致。engine block は出版 K1264 検証器・出版統合窓機・出版
K1271 機の3源から sha-gate（sha256 全一致）で機械抽出（PROVENANCE PASS）。
有限機械監査は証明そのものではない。

限界・open: m>=4 の帯上端 z>=5（E3(z) 梯子の z=5 延長が必要。D6c census は
grid 上 384/384 崩壊・反例不在を観測として記録するが証明しない）、D セルの
z>=5 での deviant 構造、F/R2/D 梯子の m=2 行以遠への一般化、閉形式の窓+2 以上の
拡張、min=1 行との統合分類。標準 11×11 空盤・二石 root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4・class 5343 はどの時点でも UNKNOWN のまま。
