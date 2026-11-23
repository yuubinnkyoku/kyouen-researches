---
id: K1274
title: "min>=5 クリティカルストリップ z=6 スライス: H(m+7;X;6)=v(ΣX,6,m+7)（F6/G6/E6/D6 有限z梯子+D6完全崩壊セル+mex自明吸収+m帰納の全称証明・m=5 行の z=6 を確定しストリップ z=6 を全 m>=5 で解決）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=6 slice for min>=5: for every m>=5 and every nonempty finite multiset X with min(X)=m, H(m+7;X;6)=v(sumX,6,m+7); this fixes the z=6 slice of the strip for all m>=5, and resolves the (m=5,z=6) cell of the K1268 Conjecture C1 band (remaining for m=5: z in {7,8} with z*(5)=9)"
  - "z-ladder lemma structure at z=6: Lemma F6 (F6(s)=H(8;{1}+Y;6) is decomposition-independent and equals 1/0/1/0/1/0/0 at s=0/3..7/>=8; extends the published Lemma F/F5 tables to z=6), Lemma G6 (G6(s)=H(9;{2}+Y;6) equals 0/1/0/1/2/1 at s=0/3/4/5/6/>=7; the R2-form collapse v(s+2,6,9) breaks exactly at s in {4,6}, deviant set {(4,),(6,),(3,3)}; first ladder cell with TWO deviant sums), Lemma E6 (E6(s)=H(10;{3}+Y;6) equals 1/0/1/0/0 at s=0/3/4/5/>=6; deviant exactly Y=(4,)) and the NEW floored rank Lemma D6 (D6(s):=H(11;{4}+Y;6) with Y tokens >=5 satisfies the FULL collapse D6(s)=v(s+4,6,11) for every s, zero deviants, zero decomposition dependence: the first fully-collapsing rank cell in the ladder; the floor >=5 is essential, Y=(4,) i.e. the published frontier witness (4,4)@R=11 (parent 2 vs single 1) is the counterexample below the floor)"
  - "proof technique: K0832 case computation closes the F6/G6/E6/D6 cells from published z<=5 lemmas (F6's C-child uses the published F5 table; G6's A-on-2 child is the F6 cell; G6's C-child uses G5; E6's A-on-3 child is the G6 cell; E6's C-child is the published E5; D6's A-on-4 child is the E6 cell; D6's C-hand children all have value exactly 1 via the published T-Z5 at z=5). The m=5 base H(12;X;6) is trivial absorption: every A-hand child value is 1 so the mex is 0 = the single-token side (first base of this type; contrast K1273's deviant-absorbing m=4 base), and the m>=6 step is option-set identity: {v(sum-1,6,m+6)} from both A-children (a>m stair edge exactly, a=m the induction hypothesis C(m-1,6)) and 1^v(sum,5,m+6) from the C-child (published T-Z5), matching the single-token side exactly"
  - "boundary sharpness: min>=5 is necessary (m=4 is out of band at z=6 since z*(4)=6; the published frontier witness (4,4)@R=11 separates parent 2 vs single 1, machine-reproduced as the ONLY separation in the 222-shape m=4 z=6 negative record); the D6 floor >=5 is necessary and coincides with the strip boundary (the same witness (4,4) breaks the D6 collapse), so the bedrock cell and the strip are cut by the same frontier"
relations:
- type: extends
  target: K1273
  note: "K1273 が全称証明した z=5 スライス（min>=4）に続き、z=6（min>=5）を証明する。証明は K1273 の出版 Lemma F5/G/E 表・T-Z5（m>=4・C手子 1^v(ΣX,5,m+6)）を直接引用し、F6/G6/E6/D6 の 4 セル梯子（z=5 の F5/G/E に D ランクの床付きセルを加えた構成）で閉じる。engine は同一の出版 sha-gate 鎖（engine block 2,508B SHA-256 bd5f22e4…）から機械抽出で、出版源は 5 つに拡大（K1264・K1268・K1271・K1272・K1273 機の 6 方 byte 照合）。"
- type: extends
  target: K1270
  note: "K1270 の低z banded（z∈{0,1}）との併せ技で m=5 行は z∈{0..6} が確定（残部 z∈{7,8}・z*(5)=9）。"
- type: related
  target: K1268
  note: "統合窓 sharpness から登録された予想 C1（m>=2・z<z*(m)・R=z+m+1 の全 X 崩壊）の (m=5,z=6) セルを確定。z=6 ストリップ崩壊は全 m>=5 で全称証明され（m=4 は witness (4,4) の 1 点のみの分離）、C1 の予想帯と整合。残部は m=5 の z∈{7,8} と m>=6 の z∈{7..z*(m)−1}。"
- type: depends_on
  target: K1264
  note: "階段定理（空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R)）。母体の a>m 子・F6/G6/E6/D6 セルの A手子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。F6/G6/E6/D6 梯子の全場合計算と単一側選択肢集合の算出基盤。"
- type: related
  target: K1271
  note: "min=1 行の窓端分離法則 S(t) と対照。F6 セル H(8;{1}∪Y;6) は出版 Lemma F の z=6 延長で、min=1 行と min>=2 行の接続点。z=6 では F セルの値は 1 系に留まる（2 系への遷移は z=7 の F7 で観測・census 記録のみ）。"
- type: related
  target: K1267
  note: "境界の鋭さ: min=1 では窓+1 の z=0 が T1 で分離するため min(X)=m>=5 の仮定系の外側。"
- type: related
  target: K1269
  note: "境界の鋭さ: min=1 では窓+1 の z=1 が T2 で分離する。"
artifacts:
- path: research/experiments/strip-z6-min5-20261123/report.md
  role: proof
  note: 機械監査の正本記録（D1-D9・D6c census・変異電池・決定性・provenance・誠実記録）。証明全文は宣言ノート §2 にあり本 report は証明そのものではない。
- path: research/experiments/strip-z6-min5-20261123/verify_strip_z6.py
  role: verifier
  note: "専用機体（SHA-256 61cb0b60b9012320e2146f4b49566a3b6fc5cee4cfb42c8911db9dc5321cb134・audit/tamper 両モード・engine block は5出版源から sha-gate 機械抽出）。D1-D9 宣言 protocol（宣言総計 13,577点/28,833比較）・12変異電池 B1-B12。"
- path: research/experiments/strip-z6-min5-20261123/build_engine_from_published.py
  role: verifier
  note: "provenance sha-gate（出版 K1264 検証器 108fdd65…・出版 K1268 機 0ab66665…・出版 K1271 機 1ce7df23…・出版 K1272 機 009184ef…・出版 K1273 機 314e176b… の5源から engine block を cut・6方 byte 照合 + pin bd5f22e4… 照合・PROVENANCE PASS・手転写ゼロ）。"
- path: research/experiments/strip-z6-min5-20261123/output/audit.json
  role: data
  note: "監査正本（SHA-256 d63fa24d9927db6d071bfb994b299714b76aaf8e7ccff5bc12ea163eb8e71499・宣言総計 13,577点/28,833比較 bad 0 と完全一致・4実行 byte-identical・D6c census に z=7 次レーン観測（F7/G7/E7 s-only 表・G7 deviant {(6,),(3,3)}・E7 deviant {(4,),(6,),(3,3)}・D7(Y>=5)・C7(Y>=6) は床付きで完全崩壊・z=7 strip m∈{5..10} 96/96 崩壊・m=4 z=6 negative は (4,4) の1点のみ分離）を記録）。"
- path: research/log/2026-11-23-strip-z6-min5-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 7018151・F6/G6/E6/D6 + T-Z6 の証明全文を機械実行前に先行開示・publish-then-execute・宣言前探査の全開示を含む。宣言 commit メッセージの「28,830」は誤植・正しくは 28,833〔28,833比較〕）。
- path: research/log/2026-11-23-strip-z6-min5.md
  role: log
  note: run log（選定→探査→紙面証明→宣言→機体組立→公式監査→出版→fetch-back 検証・誠実記録）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰・K0832 単一トークン閉形式 v）について、
  すべての m>=5・min(X)=m を持つ空でない任意の有限多重集合 X（全形状・全アリティ）に
  対して H(m+7;X;6)=v(ΣX,6,m+7) が成立するという全称命題（proved・F6/G6/E6/D6 閉形式の
  K0832 場合計算 + 出版 z<=5 補題引用 + 底 m=5 自明吸収 + 選択肢集合一致 + m に関する
  帰納）。同一証明に含まれる数学的部品として Lemma F6（F セル z=6 閉形式表・分解非依存・
  全称）、Lemma G6（z=6 の R2型セル閉形式・deviant は s∈{4,6} の
  {(4,),(6,),(3,3)} ちょうど・全称）、Lemma E6（z=6 の E セル閉形式・deviant は
  Y=(4,) ちょうど・全称）、Lemma D6（床付き D ランクセル H(11;{4}∪Y;6)・Y>=5 で
  完全崩壊 D6(s)=v(s+4,6,11)・床 <5 では witness (4,4) が反例・全称）も主張に含む。
  m=5 の z∈{7,8}（z*(5)=9）、m>=6 の z∈{7..z*(m)−1}（上位スライス）、z=7 次レーンの
  F7/G7/E7/D7/C7 閉形式（census 記録のみで open）、11×11 盤面のいかなる勝敗も
  本項目の範囲外。
