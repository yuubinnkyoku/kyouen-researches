---
id: K1273
title: "min>=4 クリティカルストリップ z=5 スライス: H(m+6;X;5)=v(ΣX,5,m+6)（F5/G/E 有限z梯子+mex吸収+m帰納の全称証明・K1268 予想C1 の m=4 行が完全解決）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=5 slice for min>=4: for every m>=4 and every nonempty finite multiset X with min(X)=m, H(m+6;X;5)=v(sumX,5,m+6); z=5 is the last in-band slice for m=4 (z*(4)=6), so together with K1270 (z in {0,1}) and K1272 (z in {2,3,4}) this resolves the complete m=4 row of K1268 Conjecture C1, for all shapes and all arities, and proves the strip z=5 for every m>=4"
  - "z-ladder lemma structure at z=5: Lemma F5 (F5(s)=H(7;{1}+Y;5) is independent of the decomposition and equals 1/0/1/0/2 at s=0/3/4/5/>=6; extends the published Lemma F table from z<=4 to z=5), Lemma G (G(s)=H(8;{2}+Y;5) equals 0/1/0/1 at s=0/3/4/>=5; the R2-form collapse v(s+2,5,8) fails exactly at Y=(4,) where G(4)=0 != v(6,5,8)=1, an arithmetic consequence, pointing opposite to the z=4 deviant D(4)=2>collapse), Lemma E (E(s)=H(9;{3}+Y;5) equals 1/0/2/0 at s=0/3/4/>=5; the deviant Y=(4,) cell E(4)=2 != v(7,5,9)=0 IS the published K1268 frontier witness (4,3)@R*=9, located for the first time inside a closed-form ladder)"
  - "proof technique: K0832 case computation closes the F5/G/E cells from published z<=4 lemmas (F5's C-child uses the published Lemma F z=4 table; G's A-on-2 child is the F5 cell; G's C-child uses the published Lemma D; E's A-on-3 child is the G cell; E's C-child is the published K1272 T-B at z=4). The m=4 base absorbs the E-cell deviant into mex (E(4)=2 never fills the missing 0, same absorption pattern as K1272's D(4)); the m>=5 step is option-set identity: {v(sum-1,5,m+5)} from both A-children (a>m stair edge exactly, a=m the induction hypothesis C(m-1,5)) and 1^v(sum,4,m+5) from the C-child (published T-B at z=4), matching the single-token side exactly"
  - "boundary sharpness: min>=4 is necessary (m=3 is out of band at z=5; the frontier witness (4,3)@R*=9 separates parent 2 vs single 0, and is exactly the Lemma E deviant cell); z<=5 is optimal for m=4 (z=6 is the frontier z*(4)=6, witness (4,4)@R=11 parent 2 vs single 1, machine-reproduced); the G-cell deviant at z=5 flips the direction of the z=4 deviant (0 below collapse vs 2 above)"
relations:
- type: extends
  target: K1272
  note: "K1272 が全称証明した z∈{2,3,4}（min>=3）に続き、m=4 のバンド上端 z=5 を新增証明する。証明は K1272 の出版 Lemma F（z=4 表）・Lemma D・Theorem T-B（z=4・m>=3）を直接引用し、F5/G/E セルの関数構造（（z+手ごとに閉じる再帰）は K1272 の R2/D 階梯を z=5 に延長したもの。エンジンは同一の出版 sha-gate 鎖（engine block 2,508B SHA-256 bd5f22e4…）から機械抽出（出版源は4つに拡大: K1264・K1268・K1271・K1272 機）。"
- type: extends
  target: K1270
  note: "K1270 の低z banded（z∈{0,1}・min>=2）との併せ技で m=4 行が全域 z∈{0..5} で確定する（z*(4)=6 を使い切る）。"
- type: related
  target: K1268
  note: "統合窓 sharpness から登録された予想 C1（m>=2・z<z*(m)・R=z+m+1 の全 X 崩壊）の m=4 行を完全解決し、m>=5 行の z=5 も確定（m>=5 の残部 z∈{6..z*(m)-1} は open）。前線 witness (4,3)@R*=9 が Lemma E の deviant セルそのものと同定されたことで、『バンド外の分離』と『バンド内の閉形式梯子』が単一の構造に統合された。"
- type: depends_on
  target: K1264
  note: "階段定理（空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R)）。母体の a>m 子・F5/G/E セルの A手子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。F5/G/E 梯子の全場合計算と単一側選択肢集合の算出基盤。"
- type: related
  target: K1271
  note: "min=1 行の窓端分離法則 S(t) と対照。F5 セル H(7;{1}∪Y;5) は混合 arming の閉形式延長（z<=4 の出版 Lemma F の z=5 延長）で、min=1 行と min>=2 行の接続点。z=5 で F セルの値は初めて 1 系から 2 系（s>=6 で 2）へ遷る。"
- type: related
  target: K1267
  note: "境界の鋭さ: min=1 では窓+1 の z=0 が T1 で分離するため min(X)=m>=4 の仮定系の外側。"
- type: related
  target: K1269
  note: "境界の鋭さ: min=1 では窓+1 の z=1 が T2 で分離する。"
artifacts:
- path: research/experiments/strip-z5-min4-20261123/report.md
  role: proof
  note: 機械監査の正本記録（D1-D7・D6c census・変異電池・決定性・provenance・誠実記録）。証明全文は宣言ノート §2 にあり本 report は証明そのものではない。
- path: research/experiments/strip-z5-min4-20261123/verify_strip_z5.py
  role: verifier
  note: "専用機体（SHA-256 314e176b4229486ff60672b63095397daa786fb1e4affe90ac20b5c060b724f4・audit/tamper 両モード・engine block は4出版源から sha-gate 機械抽出）。D1-D7 宣言 protocol（宣言総計 5,943点/17,865比較）・12変異電池 B1-B12。"
- path: research/experiments/strip-z5-min4-20261123/build_engine_from_published.py
  role: verifier
  note: "provenance sha-gate（出版 K1264 検証器 108fdd65…・出版 K1268 機 0ab66665…・出版 K1271 機 1ce7df23…・出版 K1272 機 009184ef… の4源から engine block を cut・5方 byte 照合 + pin bd5f22e4… 照合・PROVENANCE PASS・手転写ゼロ）。"
- path: research/experiments/strip-z5-min4-20261123/output/audit.json
  role: data
  note: "監査正本（SHA-256 d5cc8eb0d7f6d63ab0f598e197c84a7f5fa9f17f179dcdd6c0d33d65957a95a5・宣言総計 5,943点/17,865比較 bad 0 と完全一致・4実行 byte-identical・D6c census に z=6 次レーン観測（F6/G6/E6 s-only テーブル・G6 deviants s∈{4,6}・E6 deviant {4}・z=6 strip m∈{5..8} 96/96 崩壊・m=4 は (4,4) の1点のみ分離）を記録）。"
- path: research/log/2026-11-23-strip-z5-min4-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 352f73c2・F5/G/E + T-Z5 の証明全文を機械実行前に先行開示・publish-then-execute・宣言前探査の全開示を含む）。
- path: research/log/2026-11-23-strip-z5-min4.md
  role: log
  note: run log（選定→探査→紙面証明→宣言→機体組立→公式監査→出版→fetch-back 検証・誠実記録）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰・K0832 単一トークン閉形式 v）について、
  すべての m>=4・min(X)=m を持つ空でない任意の有限多重集合 X（全形状・全アリティ）に
  対して H(m+6;X;5)=v(ΣX,5,m+6) が成立するという全称命題（proved・F5/G/E 閉形式の
  K0832 場合計算 + 出版 z<=4 補題引用 + mex 吸収 + m に関する帰納）。同一証明に含まれる
  数学的部品として Lemma F5（F セル z=5 閉形式表・分解非依存・全称）、Lemma G（z=5 の
  R2型セル閉形式・deviant は Y=(4,) ちょうど・全称）、Lemma E（z=5 の E セル閉形式・
  deviant は Y=(4,) ちょうど・全称・当該セルは K1268 前線 witness (4,3)@R*=9 そのもの）
  も主張に含む。m>=5 の z∈{6..z*(m)-1}（上位スライス）、z=6 次レーンの F6/G6/E6 閉形式
  （census 記録のみで open）、11×11 盤面のいかなる勝敗も本項目の範囲外。
