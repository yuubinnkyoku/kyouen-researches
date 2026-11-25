---
id: K1275
title: "min>=5 クリティカルストリップ z=7 スライス: H(m+8;X;7)=v(ΣX,7,m+8)（F7/G7/E7/D7 有限z梯子+D7完全崩壊セル+mex自明吸収+m帰納の全称証明・m=5 行の z=7 を確定しストリップ z=7 を全 m>=5 で解決・C1 バンド m=5 行の残部を z=8 の1セルに）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=7 slice for min>=5: for every m>=5 and every nonempty finite multiset X with min(X)=m, H(m+8;X;7)=v(sumX,7,m+8); this fixes the z=7 slice of the strip for all m>=5, and resolves the (m=5,z=7) cell of the K1268 Conjecture C1 band (remaining for m=5: z=8 only, exactly one cell, with z*(5)=9)"
  - "z-ladder lemma structure at z=7: Lemma F7 (F7(s)=H(9;{1}+Y;7) is decomposition-independent and equals 1/0/1/0/1/0/2 at s=0/3..7/>=8; the F-cell 2-family RETURNS at z=7, F5>=6->2, F6>=8->0, F7>=8->2: z=6 merely sank the oscillation), Lemma G7 (G7(s)=H(10;{2}+Y;7) equals 0/1/0/1/0/1/1 at s=0/3..7/>=8; the R2-form collapse v(s+2,7,10) breaks exactly at s=6, deviant set {(6,),(3,3)} DOWNWARD 0<1: a direction reversal of G6's upward s=6 deviant, and G6's second deviant s=4 disappears at z=7), Lemma E7 (E7(s)=H(11;{3}+Y;7) equals 1/0/1/0/2/0 at s=0/3/4/5/6/>=7; deviant set {(4,),(6,),(3,3)}: s=4 reverses to downward 1<2 and s=6 is a new upward 2>0) and the floored rank Lemma D7 (D7(s):=H(12;{4}+Y;7) with Y tokens >=5 satisfies the FULL collapse D7(s)=v(s+4,7,12) for every s in {0}+{>=5}, zero deviants, zero decomposition dependence: the SECOND fully-collapsing rank cell after D6; the floor >=5 is essential, Y=(4,) i.e. the (4,4)@R=12 frontier witness (parent 0 vs single 1, DOWNWARD) is the counterexample below the floor)"
  - "proof technique: K0832 case computation closes the F7/G7/E7/D7 cells from published z<=6 lemmas (F7's C-child uses the published F6 table; G7's A-on-2 child is the F7 cell; G7's C-child uses G6; E7's A-on-3 child is the G7 cell; E7's C-child is the published E6; D7's A-on-4 child is the E7 cell; D7's C-hand children all have value exactly 1 via the published T-Z6 at z=6). The m=5 base H(13;X;7) is trivial absorption: every A-hand child value is 1 so the mex is 0 = the single-token side, closed THROUGH the D7 collapse alone (the K1274 residual note conjectured a C7 full-collapse cell would be needed; C7 is NOT needed, the a=5 child lands in D7 and C7 remains a census-record-only cell). The m>=6 step is option-set identity: {v(sum-1,7,m+7)} from both A-children (a>m stair edge exactly, a=m the induction hypothesis C(m-1,7)) and 1^v(sum,6,m+7) from the C-child (published T-Z6), matching the single-token side exactly"
  - "boundary sharpness: min>=5 is necessary (m=4 is out of band at z=7 since z*(4)=6; the frontier witness (4,4)@R=12 separates parent 0 vs single 1, machine-reproduced as the ONLY separation in the 222-shape m=4 z=7 negative record; this is the FIRST OBSERVED DIRECTION REVERSAL of the frontier witness, z=6 was upward 2 vs 1, z=7 is downward 0 vs 1); the D7 floor >=5 is necessary and coincides with the strip boundary (the same witness Y=(4,) breaks the D7 collapse), so the bedrock cell and the strip are cut by the same frontier at the same position value"
relations:
- type: extends
  target: K1274
  note: "K1274 が全称証明した z=6 スライス（min>=5）に続き、z=7（min>=5）を証明する。証明は K1274 の出版 F6/G6/E6/D6 表・T-Z6（m>=5・C手子 1^v(ΣX,6,m+7)）を直接引用し、F7/G7/E7/D7 の 4 セル梯子で閉じる。K1274 run log §6 残務の「z=7 証明には C7 の完全崩壊が必要」という予想を、底 m=5 の a=5 子が D7 セル（Y=X\\{5} は床 >=5 を自動的に満たす）に落ちる構成で解消した（C7 は不要）。engine は同一の出版 sha-gate 鎖（engine block 2,508B SHA-256 bd5f22e4…）から機械抽出、出版源は 6 つに拡大（6 方 byte 照合 + pin 照合）。"
- type: extends
  target: K1270
  note: "K1270 の低z banded（z∈{0,1}）・K1272（m=5 の z∈{2,3,4}）・K1273 T-Z5・K1274 T-Z6 との併せ技で m=5 行は z∈{0..7} が確定（残部 z=8 ちょうど1セル・z*(5)=9）。"
- type: related
  target: K1268
  note: "統合窓 sharpness から登録された予想 C1（m>=2・z<z*(m)・R=z+m+1 の全 X 崩壊）の (m=5,z=7) セルを確定。z=7 ストリップ崩壊は全 m>=5 で全称証明され（m=4 は witness (4,4) の 1 点のみの分離・下向き）、C1 の予想帯と整合。残部は m=5 の z=8 のみと m>=6 の z∈{8..z*(m)−1}。"
- type: depends_on
  target: K1264
  note: "階段定理（空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R)）。母体の a>m 子・F7/G7/E7/D7 セルの A手子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。F7/G7/E7/D7 梯子の全場合計算と単一側選択肢集合の算出基盤。"
- type: related
  target: K1273
  note: "z=5 スライス（min>=4）の T-Z5 構成との対照。m=5 底の自明吸収構造（全 A手子値 1 → mex=0）が z=5 の m=4 底（deviant 吸収型）と z=6 の m=5 底（自明吸収型）に続き z=7 の m=5 底でも成立し、底構造の z 超え安定を示した。"
- type: related
  target: K1272
  note: "出版 Lemma F（F セル表）の z=7 延長が F7。F セル値の 2 系が z=6 で一旦 0 に沈み z=7 で再来する振動（F5>=6→2・F6>=8→0・F7>=8→2）は min=1 窓端構造の低 z 振動の高 z 側の観測点。"
- type: related
  target: K1271
  note: "min=1 行の窓端分離法則 S(t) と対照。z=7 では前線 witness (4,4) の分離方向が下向き（親 0 vs 単一 1）に反転する初例（z=6 は上向き 2 vs 1）。"
- type: related
  target: K1267
  note: "境界の鋭さ: min=1 では窓+1 の z=0 が T1 で分離するため min(X)=m>=5 の仮定系の外側。"
- type: related
  target: K1269
  note: "境界の鋭さ: min=1 では窓+1 の z=1 が T2 で分離する。"
artifacts:
- path: research/experiments/strip-z7-min5-20261123/report.md
  role: proof
  note: 機械監査の正本記録（D1-D9・D6c census・変異電池・決定性・provenance・誠実記録）。証明全文は宣言ノート §2 にあり本 report は証明そのものではない。C1 m=5 行の残部 z=8 1セル化・前線 witness 方向反転の初例を含む。
- path: research/experiments/strip-z7-min5-20261123/verify_strip_z7.py
  role: verifier
  note: "専用機体（SHA-256 0c400f32e78b7a8848a6bdaa40a2f29ff73fe1b0f667abb187b961508f53a1c9・audit/tamper 両モード・engine block は6出版源から sha-gate 機械抽出）。D1-D9 宣言 protocol（宣言総計 13,578点/28,836比較）・12変異電池 B1-B12。"
- path: research/experiments/strip-z7-min5-20261123/build_engine_from_published.py
  role: verifier
  note: "provenance sha-gate（出版 K1264・K1268・K1271・K1272・K1273・K1274 の6源から engine block を cut・7方 byte 照合（6源+本機体）+ pin bd5f22e4… 照合・PROVENANCE PASS・手転写ゼロ）。"
- path: research/experiments/strip-z7-min5-20261123/probe_strip_z7_predecl.py
  role: verifier
  note: "宣言前探査機体（SHA-256 42a3311955422bd3175dd414ca84374444ca3a127e65a5d077c22eed16bd5e52・宣言ノート §6 P1-P11 の再現・engine は出版 K1274 機から sha-gate cut）。宣言前探査の全開示規約の一次資料。"
- path: research/experiments/strip-z7-min5-20261123/output/audit.json
  role: data
  note: "監査正本（SHA-256 30deb244b68fc425368916320997d143ad9ea22acfe639a348cb6624477dc044・宣言総計 13,578点/28,836比較 bad 0 と完全一致・4実行 byte-identical・D6c census に z=8 次レーン観測（F8/G8/E8/D8/C8 表・D8 は床付きでも deviant s=6 が1つ出現し D6/D7 の完全崩壊系列が初めて破れる・z=8 strip m∈{5..10} 96/96 崩壊・m=4 z=7 negative は (4,4) の1点のみ分離・下向き）を記録）。"
- path: research/experiments/strip-z7-min5-20261123/output/probe_predecl.json
  role: data
  note: 宣言前探査出力（SHA-256 b86ea675453708079ce09f1d8ed5b10758f178f6223724454ac64899023c91bc・出版 K1274 機の z7_cells/z7_strip census との完全一致含む）。
- path: research/log/2026-11-23-strip-z7-min5-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 4e8229fd・sha256 f36195a7…・F7/G7/E7/D7 + T-Z7 の証明全文を機械実行前に先行開示・publish-then-execute・宣言前探査の全開示を含む・宣言総計 13,578点/28,836比較の事前登録）。
- path: research/log/2026-11-23-strip-z7-min5.md
  role: log
  note: run log（選定→探査→紙面証明→宣言→機体組立→公式監査→出版→fetch-back 検証・誠実記録）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰・K0832 単一トークン閉形式 v）について、
  すべての m>=5・min(X)=m を持つ空でない任意の有限多重集合 X（全形状・全アリティ）に
  対して H(m+8;X;7)=v(ΣX,7,m+8) が成立するという全称命題（proved・F7/G7/E7/D7 閉形式の
  K0832 場合計算 + 出版 z<=6 補題引用 + 底 m=5 自明吸収（D7 完全崩壊経由・C7 は不要）
  + 選択肢集合一致 + m に関する帰納）。同一証明に含まれる数学的部品として Lemma F7
  （F セル z=7 閉形式表・分解非依存・s>=8 で 2 系再来・全称）、Lemma G7（z=7 の
  R2型セル閉形式・deviant は s=6 の {(6,),(3,3)} ちょうど・下向き 0<1・方向反転・全称）、
  Lemma E7（z=7 の E セル閉形式・deviant は s∈{4,6} の
  {(4,),(6,),(3,3)} ちょうど・全称）、Lemma D7（床付き D ランクセル
  H(12;{4}∪Y;7)・Y>=5 で完全崩壊 D7(s)=v(s+4,7,12)・床 <5 では witness (4,4) が反例・
  完全崩壊セル2例目・全称）も主張に含む。m=5 バンドの残部は z=8 ちょうど1セル
  （z*(5)=9・D8 には床付きでも deviant s=6 がある census 記録のみで open）、
  m>=6 の z∈{8..z*(m)−1}（上位スライス）、s=6 deviant 構造線（{(6,),(3,3)} が
  G6/E7/G8/E8/D8 に跨出現）の一般則は open、11×11 盤面のいかなる勝敗も本項目の
  範囲外。
