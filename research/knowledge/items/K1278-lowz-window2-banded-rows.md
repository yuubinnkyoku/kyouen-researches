---
id: K1278
title: "低z banded 窓+2/窓+3 行の全称崩壊定理群: T_A (z=0 窓+2, 全 m>=2)・T_A3 (z=0 窓+3, 全 m>=3)・T_B (z=1 窓+2, 全 m>=3)（補題 Z1/Z0・K1270 低z banded の窓+1 から窓+2/z=0 窓+3 への拡張・K1268 予想 C1 の z∈{0,1} 帯を w=2〔z=1 は m>=3〕と w=3〔z=0 は m>=3〕へ拡張確定・3 定理 2 補題すべて全称）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "low-z banded window+2/window+3 rows (universal collapse): for every m>=2 and every nonempty finite multiset X with min(X)=m, H(m+2;X;0)=v(sumX,0,m+2) (Theorem T_A: the window+2 row at z=0, an exact +1 window extension of the K1270 z=0 row to ALL m>=2); for every m>=3, H(m+3;X;0)=v(sumX,0,m+3) (Theorem T_A3: the window+3 row at z=0); and for every m>=3, H(m+3;X;1)=v(sumX,1,m+3) (Theorem T_B: the window+2 row at z=1, an exact +1 window extension of the K1270 z=1 row from all m>=2 to all m>=3; the m=2 z=1 window+2 cell is a genuine SEPARATION BAND, 8 of 10 rows separating, not a collapse row)"
  - "simplicity structure of the proof (all lemma/theorem statements are universal and machine-audited after publication of the full proof in the declaration note): Lemma Z1 (|W|>=2 implies H(2;W;0)=0 for every finite multiset W -- at z=0, no C-move, every A-child H(1;W';0)=1 and every B-child H(1;W\\{1};1)=2, so 0 is the mex), Lemma Z0 (H(3;{1}cup Y';0)=2 for every Y'!=empty with min(Y')>=2 -- the B-child H(2;Y';1) takes value 1 via mex{2,0} and every A-child is a {1}cup Y'' shape with arity >=2 so Z1 gives 0, whence mex{1,0}=2; the empty case H(3;{1};0)=v(1,0,3)=1 is the single-token boundary). Theorems T_A/T_A3/T_B are proved by strong induction on sumX with option-set identity arguments: at z=0 with min>=2 only the A-move survives, and every A-child collapses to the SAME value a:=v(sumX-1,0,m+1)(T_A) or v(sumX-1,0,m+2)(T_A3) -- min-preserving children hit the K1270 z=0 row (and T_A(m) inside T_A3) exactly, min-dropping children hit the induction hypothesis with budget arithmetic (R=(m-1)+2 resp. (m-1)+3) -- so both sides have option set {a} and the mexes agree; T_B (z=1, min>=3 has no B-move) has parent options exactly {v(sumX-1,1,m+2), 1^v(sumX,0,m+2)} (min-preserving A-child = published K1270 z=1 row, min-dropping A-child = induction, C-child = 1 XOR T_A(m)) which COINCIDES with the single-token option set at z=1, R=m+3 verbatim. The bases are absorption arguments: T_A base m=2 (option set inside {1,2}, 0 absent, mex=0=v(sumX,0,4) for sumX>=4), T_A3 base m=3 (the min-drop child W contains a token >2 whose own A-child hits T_A(2) value 0, so 0 in options(W) and c!=0, parent options {1,c}, mex{1,c}=0=v(sumX,0,6)), T_B base m=3 (the min-drop child's C-child is 1^T_A(2)=1, so c!=1, parent options {0,c}, mex{0,c}=1=v(sumX,1,6))"
  - "boundary sharpness: the T_A3 m=2 exclusion is necessary -- m=2, z=0, window+3 (R=5) separates at 2-token witness (3,2) parent 2 vs single 1 and in fact ALL 10 grid rows separate (a full separation band); the T_B m=2 exclusion is necessary -- m=2, z=1, window+2 (R=5) separates at witness (2,3) parent 2 vs single 0 with 8 of 10 rows separating (the first band where collapse rows and separation rows MIX); min=1 rows are untouched: they separate at window+1 already (T1/K1267 at z=0, T2/K1269 at z=1). Complementarity table of the low-z band (rows m x windows w of collapse-determined territory): w=1: z=0 m>=2 and z=1 m>=2 (K1270); w=2: z=0 m>=2 (T_A) and z=1 m>=3 (T_B, with m=2 a separation band); w=3: z=0 m>=3 (T_A3, with m=2 a full separation band); w=4 (z=0) and w=3 (z=1): 225/225 points show ZERO separations for m=4..12 but stay OBSERVATION-ONLY (claimed open). The z>=2 territory (window+1 ladder K1272-K1277, K1268 C1 band z*(m), z>=10 strips) is entirely untouched"
  - "machine audit (declaration protocol D0-D8, official run AFTER publication of the declaration note, declared totals matching measured totals EXACTLY to the point): 39,148 points / 65,265 comparisons / bad 0 (D0 closed-form v x twin raw engines single-token anchor grid 26,117/52,234; D1 Z1 grid tokens 1..6, arities 1..4: 3,108; D2 Z0 grid Y' tokens 2..7, arity<=3 incl. empty case: 518; D3 T_A fixed m=2..14 + light m=15..25 + random 10-shape seeds 20261142: 1,170; D4 T_B m=3..14 + light + random seed 20261143: 1,100; D5 T_A3 m=3..14 + light + random seed 20261144: 1,100; D6 structural checks option-set identity / typed child values / base absorption both engines: 5,170; D7 published anchors 17 rows machine table identical to K1272-K1277: 51; D8 deep random seed 20261145 + large-token spikes: 814). Mutation battery M1-M8 all caught rc=0 (M1 Z0 constant 2->3: bad 516; M2 Z0 empty case ->0: bad 2; M3 Z1 constant 0->1: bad 3,096; M4 T_A window+2->+3: bad 46; M5 T_B threshold 3->2: bad 46; M6 T_A3 threshold 3->2: bad 46; M7 closed-form corruption (z=1,R=9): bad 16; M8 anchor row 0 flip: bad 2). Determinism: 4 runs byte-identical (same cwd x2 + isolated tree/env -i/other HOME/PYTHONHASHSEED=random), audit.json sha256 18f35044cef257d8ad6cecd4b9b58d9832aefb955b5ce8cfa339bc88329cfc57. Engine block 2,508B pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92 sha-gate machine-extracted against ELEVEN published sources (K1264 verifier 108fdd65..., K1268 0ab66665..., K1271 1ce7df23..., K1272 009184ef..., K1273 314e176b..., K1274 61cb0b60..., K1275 0c400f32..., K1276 cdc47219..., K1277 bf3c0c1c..., K1270 dda422f2... plus the present verifier): 11-way byte agreement, PROVENANCE PASS, zero manual transcription"
relations:
- type: extends
  target: K1270
  note: "K1270（低z banded window extension: z=0 行 H(m+1;X;0)=v(Σ,0,m+1) 全 m>=2・z=1 行 H(m+2;X;1)=v(Σ,1,m+2) 全 m>=2）が report の次課題として明記した「窓+2 の z=0 拡張」の解決。T_A は z=0 行の窓+1 から窓+2 への全 m での拡張・T_B は z=1 行の窓+1 から窓+2 への m>=3 での拡張（m=2 は 8/10 分離の本物の分離帯）。証明内で min保持子の評価に K1270 両行を直接引用する（T_A の (a) 場合・T_A3 の (a) 場合・T_B の (B) 場合）。機械監査の出版アンカー17行は K1270 機と同一表。"
- type: depends_on
  target: K0832
  note: "単一トークン残余閉形式 v(x,z,R)（全称）。全定理の右辺・単一側選択肢集合の算出・D0 の 26,117点/52,234比較単一アンカー grid・吸収底での主張値計算（v(Σ,0,4)=0・v(Σ,0,6)=0・v(Σ,1,6)=1）の基盤。"
- type: depends_on
  target: K1264
  note: "階段定理（空でない X・0<=R<=z+min(X) で H(R;X;z)=v(ΣX,z,R)）。本項の全行は窓+2/窓+3 で窓端（R=z+m+1）の外側にあり主張自体には非依存だが、engine provenance 鎖（K1264 検証器 108fdd65… → K1268 機 → … → 本機）と min保持子評価の窓端等式の由来として依存。"
- type: related
  target: K1268
  note: "統合窓 sharpness census の予想 C1（m>=2・z<z*(m) で窓+1 崩壊）の z∈{0,1} 帯を窓+2（z=1 は m>=3）・窓+3（z=0 は m>=3）へ拡張確定。z>=2 帯（K1272-K1277 の窓+1 梯子・z*(m) 前線）には一切非接触。低z 帯の相補表（w=1: K1270・w=2: T_A/T_B・w=3: T_A3）が C1 と整合する形で確定。"
- type: related
  target: K1267
  note: "min=1 行の窓+1 分離定理（T1: H(3;{1}^t;0)=0 vs v(t,0,3)=1）。本項の min>=2 床と対をなし、z=0 帯の窓+n 崩壊領域の min 側境界を与える。"
- type: related
  target: K1269
  note: "min=1 行の z=1 窓+1 分離定理（T2: H(3;{1}^t;1)=2 vs v(t,1,3)=0）。z=1 帯の min 側境界。T_B の床 m>=3 と T2 の窓+1 分離が同一低z 帯の相補を構成。"
- type: related
  target: K1271
  note: "min=1 行（{1}^t）の窓端全称法則（M-RC/M-DIAG/M-SEP）。本項は min>=2 側の窓+2/窓+3 を確定し、min=1 行の窓+2 一般則（open）との間の対称的残部を明示化した。D9 境界記録に m=1 z=0 窓+3 の観測（8 行中 3 分離）を残す。"
- type: related
  target: K1272
  note: "z∈{2,3,4} クリティカルストリップ（窓+1）梯子の開始点。z>=2 の窓+2 行（本項の残部 open）は K1272-K1277 の窓+1 梯子との整合が未着手で、ストリップレーンと本レーンの間の橋として open 登録（非接触規約は維持）。"
artifacts:
- path: research/experiments/lowz-window2-banded-20261124/report.md
  role: proof
  note: 機械監査の正本記録（D0-D8 表・変異電池 M1-M8・決定性・D9 境界記録・相補表・証明ポインタ）。証明の全文（Z1/Z0/T_A/T_A3/T_B）は宣言ノート §2 にあり本 report は証明そのものではない。
- path: research/experiments/lowz-window2-banded-20261124/verify_lowz_window2.py
  role: verifier
  note: "専用機体（30,272B・SHA-256 ea114de3ef0e7b6e965af5c43aa2939d95681604bb46a640e74c96dedebc5703・audit/tamper 両モード・engine block pin bd5f22e4…・宣言 protocol D0-D9・公式実行 rc=0・OVERALL PASS・39,148点/65,265比較 bad 0）。"
- path: research/experiments/lowz-window2-banded-20261124/build_engine_from_published.py
  role: verifier
  note: "provenance sha-gate（出版 10 ソース〔K1264 検証器・K1268/K1270/K1271/K1272/K1273/K1274/K1275/K1276/K1277 機〕+ 本機の 11 方 byte 照合・pin bd5f22e4… 照合・PROVENANCE PASS・手転写ゼロ・SHA-256 26b81a0bdc85c326dc9e741ff3a2745acbc29d8c5ee16445055970607c27b64f）。"
- path: research/experiments/lowz-window2-banded-20261124/probe_w2_predecl.py
  role: verifier
  note: "宣言前探査機体（7,199B・SHA-256 586c2246ae3561a2d1af296c388885c56a3520a83d152c6ce1914c1810a8940d・宣言ノート §6 P1-P9 の再現・キャップ付きメモ・engine pin 一致）。宣言前探査全開示規約の一次資料。"
- path: research/experiments/lowz-window2-banded-20261124/probe_w2_predecl_out.json
  role: data
  note: "宣言前探査出力（2,775B・SHA-256 3326e4d9509f2d628484e2668143efd3193c310242942bd9304cd5df4705315b・P1 Z1 3,108点・P2 Z0 518点・P3-P6 定形/乱数・P8/P9 窓+3 観測・全 bad 0）。"
- path: research/experiments/lowz-window2-banded-20261124/output/audit.json
  role: data
  note: "監査正本（5,434B・SHA-256 18f35044cef257d8ad6cecd4b9b58d9832aefb955b5ce8cfa339bc88329cfc57・宣言総計 39,148点/65,265比較 bad 0 と完全一致・meta.verifier_sha256 ea114de3…・4実行 byte-identical）。"
- path: research/log/2026-11-24-lowz-window2-banded-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（commit 4185ed7767694cb5db7957a4d76a3832bc03716f・sha256 14bdd4da6615d7a5d6c60aba088f0403e89c83be269bbdb360c68abe79dbb1f8・証明全文（Z1/Z0/T_A/T_A3/T_B）を機械実行前に先行開示・publish-then-execute・受入条件 4 事前登録）。
- path: research/log/2026-11-24-lowz-window2-banded.md
  role: log
  note: run log（選定→宣言前探査→宣言出版→機体組立→公式監査→出版→fetch-back byte 検証の全工程）。
scope: >-
  残余ゲーム H(R;X;z)（K1138 再帰・K0832 単一トークン閉形式 v）について、
  低z banded 帯の窓+2/窓+3 行の全称崩壊を確定する: 任意の空でない有限多重集合
  X に対して T_A（全 m>=2・min(X)=m: H(m+2;X;0)=v(ΣX,0,m+2)）・T_A3
  （全 m>=3: H(m+3;X;0)=v(ΣX,0,m+3)）・T_B（全 m>=3: H(m+3;X;1)=
  v(ΣX,1,m+3)）が成立する（proved・補題 Z1: |W|>=2 で H(2;W;0)=0・
  補題 Z0: min(Y')>=2・Y'≠∅ で H(3;{1}∪Y';0)=2〔Y'=∅ では v(1,0,3)=1〕は
  証明内で全称使用）。K1270（窓+1）が report で次課題と明記した「窓+2 の
  z=0 拡張」の解決であり、K1268 予想 C1 の z∈{0,1} 帯を w=2（z=1 は
  m>=3）・w=3（z=0 は m>=3）へ拡張確定する。同一証明の数学的部品として
  証明に現れる Z0 の B手子評価 mex{2,0}=1 と A手子の Z1 帰着・T_B の
  C手子と単一側選択肢集合の完全一致も主張に含む。境界の鋭さとして
  T_A3 の m=2 除外（witness (3,2)@z=0,R=5 親2 vs 単一1・10行全分離帯）・
  T_B の m=2 除外（witness (2,3)@z=1,R=5 親2 vs 単一0・10行中8分離の
  崩壊/分離混在帯）を伴う。D9 境界記録（判定外・主張しない）: m=1 z=0
  窓+3 は 8 行中 3 分離・窓+4 z=0（m=4..12）と窓+3 z=1（m=4..12）は
  各 225 点 0 分離の観測。残部 open: 窓+4 z=0 / 窓+3 z=1 の底分類
  （min落下子 W の budget 分類）・z>=2 の窓+2 行（K1272-K1277 の
  窓+1 梯子との整合）・min=1 行の窓+2 一般則・s_n・K_n 未確定値・4×m/q=8・
  3×m/q=5/q=4 は本項目の範囲外。z>=2 帯の窓+1 梯子（K1272-K1277）・
  z*(m) 前線（K1268）・z>=10 ストリップには一切非接触。標準 11×11 空盤・
  二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はどの時点でも
  UNKNOWN のまま。
