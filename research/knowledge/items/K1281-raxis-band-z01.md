---
id: K1281
title: "低z R-axis 帯 (z∈{0,1}) の帯全域+対角崩壊と前線分類の条件付きパッケージ T-B0/T-B1（仮説 H1 = z0-δ2 arm-1 法則・H2 = z1-δ2 mixed 則は finite-census observed・定理は H1/H2 の含意として proved・宣言ノートに証明全文収録・91,020 点公式監査 bad 0・4 走 byte-identical）"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "conditional package for the low-z R-axis band z in {0,1} (notation: m=min(X)>=2, z0-plane band R in [m+1,2m], diagonal R=2m, frontier R=2m+1, delta-2 R=2m+2; z1-plane band R in [m+2,2m], same diagonal/frontier): HYPOTHESES (finite-census observed, universal status OPEN, not claimed universally): H1 = z0-delta-2 arm-1 law (for every m>=1 and every X with min(X)=m, mult(X,m)=1, |X|>=2: H(2m+2;X;0)=1; census D2 m=1..7, 18,060 mixed points bad 0); H2 = z1-delta-2 mixed law (for every m>=1 and every mixed X with min(X)=m, |X|>=2: H(2m+2;X;1)=min(sumX,2m+2)%2; census D1 m=1..8, 8,276 mixed points incl. 1-token shapes bad 0). THEOREMS (proved as IMPLICATIONS, full proofs in the single-owner note):
  T-B0: H1 ⟹ (i) full-band+diagonal collapse of the z0 plane: for every m>=2, every R in [m+1,2m], every X with min=m and |X|>=2: H(R;X;0)=v(sumX,0,R) — subsuming the published w<=3 rows (K1270 w=1, K1278 T_A w=2 / T_A3 w=3) and extending to ALL windows w in [4,m] plus the diagonal w=m; (ii) frontier classification for every m>=3 at R=2m+1: mixed -> 2 and allm (m^a) a>=2 -> 0.
  T-B1: T-B0 conclusion (i) + H2 ⟹ (i) full-band+diagonal collapse of the z1 plane: for every m>=2, every R in [m+2,2m]: H(R;X;1)=v(sumX,1,R) (subsuming K1270-z1 w=1 and K1278 T_B w=2, extending to w in [3,m-1] plus the z1 diagonal w=m-1); (ii) frontier classification for every m>=2 at R=2m+1: mixed -> 2, (m,m) -> 0, (m^a) a>=3 -> 2.
  Proof skeletons: A-child min rule (moving w=m ALWAYS drops the min to m-1 since m-1<m remains, even when mult(m)>=2 — used as the corrected case rule); z0 interior step = option-set identity {a} with a=v(sumX-1,0,R-1)=(R-1)%2 via within-row induction (min-preserving) + row-(m-1) strong induction (min-drop child lands inside the row-(m-1) band [m,2m-2]); z0 diagonal = mex{1,2}=0 (min-preserving child at 2m-1 by band, min-drop child at row-(m-1) FRONTIER=2m-1 -> 2 by Q(m-1)); z0 frontier = mex{0, 1}: min-preserving child at the row-m diagonal -> 0, min-drop child at row-(m-1) DELTA-2 -> 1 by H1 arm-1 (child always has mult(m-1)=1); z1 interior = option-set identity {R%2} (C-child 1 XOR v(sumX,0,R-1) by T-B0, A-min-preserving by within-row, A-min-drop by row-(m-1) z1-band); z1 diagonal = mex{0,2}=1=(2m+1)%2 (min-drop child at row-(m-1) z1-frontier -> 2); z1 frontier = mex{1,0}=2 / (m,m): mex{1}=0 / a>=3: mex{1,0}=2 (C-child 1 XOR z0-diag value 0, A-big child at z1-diag -> 1, A-min child at row-(m-1) z1-delta-2 by H2). Row-induction dance: z0: P(2),P(3) published bases then interior -> diagonal -> frontier per row (frontier of row m-1 feeds the diagonal of row m); z1: Q1(2) established directly via H2(m'=1), then P1 via Q1(m-1) and T-B0(i), Q1 via P1(diag)+H2."
  - "unconditional consequences recorded (all finite-census OBSERVED only, status open, not claimed): LAW-C full text for z0-delta-2 mixed shapes (H=1 iff mult(m)=1 or (max<=m+1 and mult(m+1)=1), else 0; allm: a=1->v(m,0,R), a=3->1, a in {2,4..}->0; census 18,116 comparisons); z1-delta-2 allm (a>=2 -> 0); z1-delta-3 (R=2m+3) mixed shapes never take value 0 (m=2..6); delta-4 (R=2m+4) mixed shapes never take value 2 (z in {0,1}, m=2..4); z0-delta-3 takes all values {0,1,2} (hist recorded); z=2 band probe: collapse holds for R<=2m-1 (m=2..6, bad 0) but fails at R=2m (band-edge shift, connects to the z>=2 lanes); m=2 z0-frontier row (R=5) classified on the finite grid (mixed->2, allm->0, consistent with the published K1278 D9 separation record, witness (3,2) parent 2 vs single 1). K1278's 225/225-point window+4 z0 observation (m=4..12, claim-free) is exactly the w=4 slice of T-B0(i) (R=m+4<=2m iff m>=4), upgrading to a conditional theorem under H1."
  - "machine audit (declaration protocol; single-owner note published FIRST at 9547af4e, machine frozen at 5930fafe, official runs AFTER publication; declared totals matching measured totals EXACTLY): 91,020 comparisons / bad 0, counts=[8,340; 18,116; 17,759; 23,660; 14,552; 1,250; 7,088; 255] = [D1 H2 census; D2 LAW-C census; D3 z0-frontier classification + FB0 identity + cval; D4 z1-frontier classification + typed inputs a1/cbase/sigma; D5 band+diagonal collapse census (m=2..7, theorem-conclusion direct check); D6 typed-child diagonal structural grid; D7 delta-3/4 observational batteries + z0-delta-3 hist; D8 published anchors (K1278 T_B/T_A3 witnesses, K1265, K1267, K1269, K1270)]. Determinism: 4 official runs byte-identical (same cwd x2 + isolated tree/HOME + env -i + PYTHONHASHSEED random/1), stdout sha256 c64639c24f2f226164466bbe430d7f5a640c09cbdc06d427c273f3a63489ad40 = declared expectation exactly. Mutation battery: --tamper-engine -> rc=2 (embedded sha gate prints the mismatch), --tamper=lawc -> rc=1 with D2 bad=5,873, --tamper=lawc-allm -> rc=1 with D2 bad=56, all exactly as pre-declared. Fetch-back: git blob sha of the published kit (cefe9072...) equals the locally computed blob of the executed bytes (PROVENANCE PASS); engine block 2,508B pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92 sha-gated in-kit every run."
relations:
- type: extends
  target: K1278
  note: "K1278（窓+2/窓+3 行の全称崩壊 T_A/T_A3/T_B）が claim-free として残した窓+4 z0 225/225 点観測・窓+3 z1 観測と「対角列・前線列の一般化」の着地。T-B0(i) は彼らの w∈{1,2,3} 行を含む形で帯全域 w∈[1,m] と対角 w=m を条件付きで確定し、T-B1(i) は z1 帯 w∈[1,m−1]（w∈{1,2} が K1270-z1/T_B）を確定。彼らの D9 分離観測（m=2 z0 窓+3 全分離・(3,2) 親 2 vs 単一 1・m=2 z1 窓+2 8/10 分離・(2,3) 親 2 vs 単一 0）は本項の前線分類の m 最小ケースに相当（z0 m=2 は定理外の有限照合行、z1 m=2 は T-B1(ii) に含む）。honest 記録: K1278 宣言ノートの T_A 場合 (a) ラベル（mult(m)>=2 で min 保持）は字義誤りだが同一子値経由で影響なし、本項で自前規則に再構成（詳細は宣言ノート §3）。"
- type: depends_on
  target: K1270
  note: "窓+1 両面行 H(m+1;X;0)=v(Σ,0,m+1)(全 m>=2)・H(m+2;X;1)=v(Σ,1,m+2)(全 m>=2) が帯帰納の底部（z0 行 w=1・z1 行 w=1 および min 落下子が行 m−1 の帯下端 m/(m+1) に当たる全箇所）。出版物アンカーは D8 で再照合。"
- type: depends_on
  target: K0832
  note: "単一トークン閉形式 v(x,z,R)。補助計算 A0 (x>R ⟹ v(x,0,R)=R%2)・A1 (x>R>=3, z=1 ⟹ v(x,1,R)=(R+1)%2) が崩壊値表示・選択肢集合一致判定の全基盤。"
- type: related
  target: K1268
  note: "統合 sharpness census の予想 C1（窓+1 崩壊帯 z<z*(m)）の低 z 側を、本項は窓全域〜対角・前線・δ=2 まで拡張（条件付き）。相補表: w=1: K1270・w=2/3: K1278・w∈[4,m]+対角+前線: 本項・δ>=3: open・z>=2: K1272-K1277 と z10/z11 ストリップ。"
- type: related
  target: K1265
  note: "min=1 の {1,1} 全 R 崩壊（D8 アンカー 7 行再照合）。本項の min>=2 座標系の min 側境界を構成する仮説 H2 は 1-トークン混在形状を含む（D1 m=1 census が z1 前線 m=2 の min 落下子 {1}∪Y を直接被覆）。"
- type: related
  target: K1267
  note: "min=1 z0 窓+1 分離 T1（{1}^t, t>=3 は H=0 vs v=1・t<=2 は v-collapse）。D8 アンカーで実値再照合（本項の z1-δ2 m=1 被覆と合わせ、仮説域と min=1 分離域の接続面。z0-δ2 m=1 の LAW-C 全文は t=1 崩壊行と張り付く）。"
- type: related
  target: K1269
  note: "min=1 z1 窓+1 分離 T2（t>=3 は H=2 vs v=0・t∈{1,2} は v-collapse・(1,1) は崩壊値 0）。D8 アンカー修正の根拠（旧メモでは (1,1) を z1 側分離と誤解 → 実 engine 再計算で修正・宣言ノート honest 記録 3）。"
- type: related
  target: K1271
  note: "min=1 行の窓端全称法則（M-RC/M-DIAG/M-SEP）。本項は min>=2 を帯全域で条件付き確定し、min=1 行の窓>=2 一般則（open）との間の対称的残部を維持。"
- type: related
  target: K1254
  note: "大型 z 側の merge 領域・FR-X。本項の低 z 帯構造（z∈{0,1}）と z 大域をつなぐのが z>=2 面と δ ラダーの open（z=2 帯プローブの帯端シフトはその最初の構造観測）。"
- type: related
  target: K1279
  note: "z=10 min>=7 スライス全称証明（ストリップレーン）。同種の R-axis 座標で高 z 側を確定。本項の z>=2 open の向こう側に位置し、本項仮説 H1/H2 が z∈{0,1} に限定されている限り非接触。"
- type: related
  target: K1280
  note: "z=11 min>=7 スライス全称証明（ストリップレーン・本項の宣言観測 HEAD の直前コミット群）。同上・非接触規約は維持。"
artifacts:
- path: research/log/2026-11-24-raxis-band-z01-single-owner-note.md
  role: proof
  note: 宣言ノート（単一オーナー宣言・主張区分・T-B0/T-B1 の証明全文・protocol・honest 記録）。証明の正本。
- path: research/experiments/raxis-band-z01-20261124/
  role: machine
  note: 実験キット一式（verify_raxis_band_z01.py・engine_block.py・exploration 12 ファイル・dryrun 3 本・公式 output: audit 4 走分・変異 3 本・detcheck.txt・MANIFEST-sha256）。
- path: research/log/2026-11-24-raxis-band-z01.md
  role: report
  note: 実行 log（宣言→機体→公式監査→出版の全記録・受入判定・次課題）。
---
