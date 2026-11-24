---
id: K1276
title: "min>=5 クリティカルストリップ z=8 スライス: H(m+9;X;8)=v(ΣX,8,m+9)（F8/G8/E8条件付き再帰梯子+D8非完全崩壊セル+C7/C8新完全崩壊セル+mex吸収底+m帰納の全称証明・K1268 予想 C1 バンド m=5 行の完走・z*(5)=9 の最終セル z=8 を確定）"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases:
  - "critical-strip z=8 slice for min>=5: for every m>=5 and every nonempty finite multiset X with min(X)=m, H(m+9;X;8)=v(sumX,8,m+9); this fixes the z=8 slice of the strip for all m>=5, and CLOSES the m=5 row of the K1268 Conjecture C1 band completely (the last band cell z=8, with z*(5)=9; the m=5 row is now fully determined for z in {0..8})"
  - "z-ladder lemma structure at z=8: Lemma F8 (F8(s)=H(10;{1}+Y;8) decomposition-independent, 1/0/1/0/1/0/1/0 at s=0/3..8/>=9: the F-cell oscillation sinks the 2-family to 0 again at z=8), Lemma G8 (G8(s)=H(11;{2}+Y;8) equals 0/1/0/1/0/1/2/1 at s=0/3..8/>=9; deviants vs the R2-form collapse v(s+2,8,11) exactly {(6,),(3,3)} DOWNWARD 0<2 and {(8,),(3,5),(4,4)} UPWARD 2>1: the first G-cell hosting both directions), Lemma E8 (E8(s)=H(12;{3}+Y;8) equals 1/0/1/0/1/0 at s=0/3..6/>=7; deviants {(6,),(3,3)} upward; the E-cell s=4 deviant disappears at z=8) with the CONDITIONAL recursion expectation {G8(s), 1^E7(s)} + ({v(s+2,8,11)}: some Y token >=4): the UNCONDITIONAL ghost breaks exactly at Y=(3,3) s=6 (observed set {0,3} vs ghost {0,2,3}); at z=7 the E7 ghost had coincided with the option value so the unconditional form passed only by luck, and Lemma D8 (first NON-collapsing floored rung: D8(s):=H(13;{4}+Y;8), Y tokens >=5, depends only on s with table {0:0, 6:2, else v(s+4,8,13)}; the SINGLE s=6 upward deviant D8(6)=2 != v(10,8,13)=1 breaks the full-collapse series D6 (K1274)/D7 (K1275); the floor >=5 is essential, loosened to tokens>=3 the decomposition dependence at s in {6,8} enters, and Y=(4,) i.e. (4,4)@R=13 is the below-floor counterexample)"
  - "new fully-collapsing cells proved here (extending the K1274 D6c census observation to the full floored decomposition family of 1,078 shapes each plus paper proof): Lemma C7 (C7(s):=H(13;{5}+Y;7), Y tokens >=6: FULL collapse C7(s)=v(s+5,7,13) for all s in {0}+{>=6}, the (i)/(ii) A-line confluence v(s+4,7,12)=D7(s) and the C-child 1^v(s+5,6,12) via the published T-Z6) and Lemma C8 (C8(s):=H(14;{5}+Y;8), Y tokens >=6: FULL collapse C8(s)=v(s+5,8,14); the C8 recursion REALIZES the D8 s=6 deviant 2 as a child value but the mex absorbs it at every s, the first observed in-recursion realization of a rung deviant inside a fully collapsing cell)"
  - "proof technique: K0832 case computation closes the F8/G8/E8/D8/C7/C8 cells from published z<=7 lemmas, with the E8 recursion being the first CONDITIONAL option-set expectation in the series (the ghost option v(s+2,8,11) exists only when some Y token >=4; pre-registered machine detection of the unconditional form's break at probe P12 before the declaration). The m=5 base H(14;X;8) is deviant ABSORPTION: A'-child v(S-1,8,13)=1, c'-child 1^v(S,7,13)=1, D8-cell a=m child D8(S-5)=1 (the single s=6 exception has value 2 which the parent mex absorbs), parent mex = 0 = v(S,8,14). The m>=6 step is option-set identity {v(S-1,8,m+8)} (a>m stair edge exactly, a=m the induction hypothesis C(m-1,8) at R=m+8=(m-1)+9) and 1^v(S,7,m+8) (published T-Z7), matching the single-token side exactly"
  - "boundary sharpness: min>=5 is necessary (m=4 z=8 is out of band since z*(4)=6; the 222-shape m=4 z=8 negative record separates at exactly TWO points, (4,4) parent 0 vs single 2 DOWNWARD and (4,6) parent 2 vs single 1 UPWARD -- a NEW upward witness co-occurring with the frontier witness at the same (m,z) cell for the first time), and the m=5 row roof is EXACTLY z=8 (the m=5 z=9 out-of-band record separates at exactly one point (5,6) parent 2 vs single 0 upward over all 222 shapes; the s=6 shape joins the front witness), so the C1 m=5 band z<z*(5)=9 is fully consumed"
relations:
- type: extends
  target: K1275
  note: "K1275 が全称証明した z=7 スライス（min>=5）に続き、z=8（min>=5）を証明する。証明は K1275 の出版 F7/G7/E7/D7 表・T-Z7（m>=5・C手子 1^v(ΣX,7,m+8)）を直接引用し、F8/G8/E8〔条件付き再帰〕D8/C7/C8 の 6 セル梯子で閉じる。K1275 audit の D6c z8_cells census（F8/G8/E8/D8/C8 表・D8 床付き deviant s=6・_STRIP 96/96）は本項の宣言前探査 P11 crosscheck で完全一致確認の上で主張に昇格した。E8 の条件付き期待式は K1275 では無条件式が偶然成立していた（E7 の ghost が 1^E6(s) と一致）ことの訂正を含む。engine は同一の出版 sha-gate 鎖（engine block 2,508B SHA-256 bd5f22e4…）から機械抽出、出版源は 7 つに拡大（8 方 byte 照合 + pin 照合）。"
- type: extends
  target: K1270
  note: "K1270 の低z banded（z∈{0,1}）・K1272（m=5 の z∈{2,3,4}）・K1273 T-Z5・K1274 T-Z6・K1275 T-Z7 との併せ技で m=5 行は z∈{0..8} 全確定となり C1 バンドの m=5 行が完走（残部ゼロ・z*(5)=9）。"
- type: related
  target: K1268
  note: "統合窓 sharpness から登録された予想 C1 の m=5 行を完走（バンド z<z*(5)=9 の全セル z∈{0..8} 確定）。z=8 ストリップ崩壊は全 m>=5 で全称証明され（m=4 は (4,4) 下向き・(4,6) 上向きの 2 点分離・m=5 z=9 帯外は (5,6) 上向きの 1 点分離で上確認認）、C1 の予想帯と整合。残部は m>=6 の z∈{9..z*(m)−1}。"
- type: depends_on
  target: K1264
  note: "階段定理（空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R)）。母体の a>m 子・F8/G8/E8/D8/C7/C8 セルの A手子評価に窓端ちょうどの等式として使用。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v・q_odd・中間枝 (R+z)%2。F8/G8/E8/D8/C7/C8 梯子の全場合計算と単一側選択肢集合の算出基盤。"
- type: related
  target: K1273
  note: "z=5 スライス（min>=4）の T-Z5 との対照。K1275 は底 m=5 が自明吸収型だったが、z=8 では D8 の s=6 deviant 2 が a=m 子に実在し、底は K1273 の z=5 m=4 底（deviant 吸収型）と同型の mex 吸収構造に戻る。底構造の分類（自明吸収 vs deviant 吸収）が z ごとに交替することが観測された。"
- type: related
  target: K1272
  note: "出版 Lemma F（F セル表）系の z=8 延長が F8。F セル値の振動系は z=5（s>=6→2）→z=6（s>=8→0）→z=7（s>=8→2）→z=8（s>=9→0）と周期 2 の振動が継続する観測点。"
- type: related
  target: K1271
  note: "min=1 行の窓端分離法則 S(t) と対照。z=8 では m=4 帯外分離が 2 点 ((4,4) 下向き・(4,6) 上向き) となり、前線 witness と同符号の第 2 witness が同一 (m,z) セルで初めて同居。"
artifacts:
- path: research/experiments/strip-z8-min5-20261124/report.md
  role: proof
  note: 機械監査の正本記録（D1-D9・D6c z=9 census・変異電池 B1-B14・決定性・provenance・誠実記録）。証明全文は宣言ノート §2 にあり本 report は証明そのものではない。C1 m=5 行完走・D8 非完全崩壊・C7/C8 新完全崩壊セル・E8 条件付き再帰を含む。
- path: research/experiments/strip-z8-min5-20261124/verify_strip_z8.py
  role: verifier
  note: "専用機体（SHA-256 cdc472198c905233215b2c717986b77c5194b0588cdfa2f50e37376f3e5ed3ad・audit/tamper 両モード・engine block は7出版源から sha-gate 機械抽出）。D1-D9 宣言 protocol（宣言総計 24,551点/44,135比較）・14変異電池 B1-B14。"
- path: research/experiments/strip-z8-min5-20261124/build_engine_from_published.py
  role: verifier
  note: "provenance sha-gate（出版 K1264・K1268・K1271・K1272・K1273・K1274・K1275 の7源から engine block を cut・8方 byte 照合（7源+本機体）+ pin bd5f22e4… 照合・PROVENANCE PASS・手転写ゼロ）。"
- path: research/experiments/strip-z8-min5-20261124/probe_strip_z8_predecl.py
  role: verifier
  note: "宣言前探査機体（SHA-256 ff86f5dcddaec89cedf30879f9022d8273aebcf2adcc57f604b83799c2fe8a3b・宣言ノート §6 P1-P12+crosscheck の再現・E8 無条件期待式の破れ検出（Y=(3,3) ちょうど1件）ブロック込み・engine は出版 K1264 機から sha-gate cut）。宣言前探査の全開示規約の一次資料。"
- path: research/experiments/strip-z8-min5-20261124/probe_z8_predecl.json
  role: data
  note: "宣言前探査出力（SHA-256 3fa0745321ab33135cf34d1737f66aa369186ee1082513a9228fa7baa79f362a・出版 K1275 audit の z8_cells/z8_strip census との完全一致（P11 match=True）・E8 無条件式不一致 1 件→条件付き式 bad 0（P12）を含む）。"
- path: research/experiments/strip-z8-min5-20261124/published_audit.json
  role: data
  note: "出版 K1275 audit.json の pin copy（SHA-256 30deb244b68fc425368916320997d143ad9ea22acfe639a348cb6624477dc044・P11 crosscheck の照合対象）。"
- path: research/experiments/strip-z8-min5-20261124/output/audit.json
  role: data
  note: "監査正本（SHA-256 84605d3b41eb54fa8663c24403dffb5ff36edd1faac7735df3c5d0cd6f885dc1・宣言総計 24,551点/44,135比較 bad 0 と完全一致・4実行 byte-identical・D6c census に z=9 次レーン観測（F9/G9/E9/D9/C9/B9 表・D9 床付き deviant s=6 下向き・C9 床付き deviant s=6 上向き・B9 床付きは崩壊観測で完全崩壊セル次ランク候補・z=9 strip m>=6 96/96・m=5 帯外 95/96・m=4 z=8 negative 2 点・m=5 z=9 帯外 1 点）を記録）。"
- path: research/log/2026-11-24-strip-z8-min5-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit f4dcf92e・sha256 b85b18c3…・F8/G8/E8〔条件付き〕D8/C7/C8 + T-Z8 の証明全文を機械実行前に先行開示・publish-then-execute・宣言前探査 P1-P12 の全開示・宣言総計 24,551点/44,135比較の事前登録）。
- path: research/log/2026-11-24-strip-z8-min5.md
  role: log
  note: run log（選定→探査→E8 条件付き再帰の発見→紙面証明→宣言→機体組立→公式監査→出版→fetch-back 検証・誠実記録）。
scope: >-
  残余ゲーム H(R;X;z)（K0832/K1138系再帰・K0832 単一トークン閉形式 v）について、
  すべての m>=5・min(X)=m を持つ空でない任意の有限多重集合 X（全形状・全アリティ）に
  対して H(m+9;X;8)=v(ΣX,8,m+9) が成立するという全称命題（proved・F8/G8/E8〔条件付き
  再帰〕D8/C7/C8 閉形式の K0832 場合計算 + 出版 z<=7 補題引用 + 底 m=5 の D8 s=6
  deviant mex 吸収 + 選択肢集合一致 + m に関する帰納）。同一証明に含まれる数学的部品として
  Lemma F8（F セル z=8 閉形式表・分解非依存・全称）、Lemma G8（z=8 の R2型セル閉形式・
  deviant は s∈{6,8} の {(6,),(3,3)} 下向き ∪ {(8,),(3,5),(4,4)} 上向き ちょうど・
  全称）、Lemma E8（z=8 の E セル閉形式・条件付き再帰期待式・deviant は s=6 の
  {(6,),(3,3)} ちょうど・全称）、Lemma D8（床付き D ランクセル H(13;{4}∪Y;8)・Y>=5 で
  s-only だが唯一の deviant s=6 上向き・完全崩壊系列 D6/D7 が z=8 で初めて破れる・全称）、
  Lemma C7（床付き C ランクセル H(13;{5}∪Y;7)・Y>=6 で完全崩壊 v(s+5,7,13)・全称・
  本項目で初の全称証明）、Lemma C8（床付き C ランクセル H(14;{5}∪Y;8)・Y>=6 で完全崩壊
  v(s+5,8,14)・D8 の deviant を mex が吸収・全称・本項目で初の全称証明）も主張に含む。
  K1268 予想 C1 の m=5 行は完走（z∈{0..8} 全確定・残部ゼロ）。m>=6 の
  z∈{9..z*(m)−1}、z=9 ストリップ・F9/G9/E9/D9/C9/B9 閉形式、s=6 deviant 構造線
  （{(6,),(3,3)} が G6/E7/G8/E8/D8/D9/C9 に跨出現）の一般則、完全崩壊ランク移行の
  一般則（D6/D7→C7/C8→B9?・B9 は census 崩壊観測のみで open）は open、
  11×11 盤面のいかなる勝敗も本項目の範囲外。
