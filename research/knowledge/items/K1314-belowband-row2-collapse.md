---
id: K1314
title: "B-BB 下帯第2行崩壊: T-BB2（全 n≥3・全多重集合 X の下帯第2行 k=z+n−4 で E≤z+n−4→[E odd]・E=z+n−3→2・E≥z+n−2→1−[E odd]・例外セルは (1,1,1)@{0,1} のみ・n をまたぐ正しいマージ座標は (E,w)〔w:=E+z+n−5〕で多値セルは (−1,−3)→{0,1} と (−1,−2)→{1,2} のみ・L-2（n=2 plane 法の行 k=Z−2: 床は (a,Z)=(1,1) のみ 2・pair は Z≤g−2→[g even]/Z=g−1→2/Z≥g→[g odd]）・PB2（n=2 壁行 k=−2: g≤2→[g odd]/g=3→2/g≥4→[g even] で遠方場は偶奇反転）・L-BR2/L-0（基底補題）・系 A/B/C で K0832 3トークン過渡帯予想 A/B/C を解決〔U は open 継続〕・公刊 T-CSUM+T-DB+T-BB とのインターロックで全多重集合 n≥2 の k≥z+n−4 を完全確定・残余 open は k≤z+n−5 のみ (O-BBL3)・publish-then-execute・40,513 点公式監査 bad 0・4 走 byte-identical 4c2102c6・単一 R 強帰納 + 型付き子 D 座標 mex + 族 F1–F5 で閉じる.packet"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the BELOW-BAND ROW-2 collapse for ALL token multiplicities. Coordinates as K1285/K1308/K1311/K1313: H(R; X; z), S := sum(X), k := R-S, E := 2*max(X)-S. T-BB2 (universal, n>=3): for every n >= 3, z >= 0, descending multiset X of n tokens, on the SECOND ROW k := z+n-4: H = [E odd] if E <= z+n-4 (region 1), = 2 if E = z+n-3 (the 2-line), = 1-[E odd] if E >= z+n-2 (region 3, python parity, negative E included); the ONLY exception cells are X=(1,1,1) at z=0 (value 0) and z=1 (value 2), rejoining the general law at z>=2. With w := E+z+n-5 the value is a function of (E, w) ONLY, merged across ALL n >= 3: the frozen exploration WA observed EXACTLY two multivalue cells (E,w)=(-1,-3)->{0,1} and (-1,-2)->{1,2}, both second components supplied by the (1,1,1) exception cells. This answers K1313 SS5.2: within a single n the collapse coordinate is (E,z), but the correct ACROSS-n merge coordinate is (E,w), NOT (E,z). Regions 1 and 3 are infinite (E is unbounded below for n >= 3). MEANING: with the published tail T-CSUM (k >= z+n-1, K1312), the published boundary T-DB (k = z+n-2, K1311), the published top row T-BB (k = z+n-3, K1313) and this row, every n-mountain face (n >= 3) is closed for ALL k >= z+n-4, every multiset; the n=2 second row comes as L-2 (plane Z >= 1, row k = Z-2: beds 2 iff (a,Z)=(1,1) else 0; pairs (m+g,m), g>=1: Z <= g-2 -> [g even] / Z = g-1 -> 2 / Z >= g -> [g odd]) and PB2 (plane 0 wall row k=-2: g <= 2 -> [g odd] / g = 3 -> 2 / g >= 4 -> [g even], parity INVERTED relative to the L-2 far field — the first concrete instance of two different laws on the same k row at different planes), plus L-BR2 (n=1, row k=Z-3: R=0 -> 0; 2 iff (Z=x>=2) or (1,3) or (3,1); Z >= x+1 -> [x odd]; Z <= x-1 -> [x even]; a slice of the published K0832 single-token closed form) and L-0 (empty multiset H=0 for all R, z), so ALL n >= 2 are closed for k >= z+n-4 (n=2 top row published via T-BB's n=2 degeneration = the K1310 T-NCW constants). COROLLARIES: the K0832 3-token transient-band conjectures on the k=0 odd slice R=2x-1, X=(x,Y,W), Y>=W>=1 are RESOLVED — A (j=0): x=Y+W+z -> H=2 always (the T-BB2 2-line at E=z; (1,1,1) unreachable since x>=2); B (j=2): x=Y+W+z+2 -> H=2 always (the published T-DB 2-line Dlaw(E=z+2,p=z+1)=2); C (j=1): x=Y+W+z+1 -> H=2 iff z=0 (the published T-BB top-row law, u=2z); the band condition x < R=2x-1 < S+z+2 is verified in all three cases; the UNIFIED conjecture U (k >= 1 slices) lives on rows k <= z+n-5 and REMAINS OPEN (O-BBL3)."
  - "STRUCTURE (typed children, SINGLE strong induction on R across ALL faces): D := (z+n-4)-E (depth from the 2-line: region 1 iff D>=0, 2-line iff D=-1, region 3 iff D<=-2), rho := [E odd]. Typed child identities: every option of a second-row cell is EXACTLY one of (A-a) unique-top reduce x1>=2, x1>x2 -> child (n, z, same k, E-1) at (E-1, D+1); (A-b) non-top/tied reduce -> child (n, z, same k, E+1) at (E+1, D-1); (B) remove a value-1 heap -> child (n-1, plane z+1, SAME k, E+1) with FULLY DETERMINED typing: n-1=1 heir is an L-BR2 cell (row k=(z+1)-3), n-1=2 heir is ALWAYS an L-2 cell (plane z+1 >= 1, never PB2), n-1>=3 heir is a T-BB2 cell (z'+n'-4 = z+n-4, so the SAME D at D-1); (C) plane-down (z>=1) option value 1 XOR child, child (n, z-1, k-1, E) at (E, D-1) — the C-heir of an L-2 cell at Z=1 is the ONLY landing on a PB2 cell (the internal plane-0 interface of the second-row family). ALL children sit at budget R-1, so ONE strong induction over R across T-BB2 ∪ L-2 ∪ PB2 ∪ L-0 closes everything simultaneously (L-BR2 and the empty-multiset heirs known outside the induction domain by the published closed form and the mex{1}=0 induction). n=3 B-heirs are evaluated in L-2 (g, Z') coordinates (g := E+1, Z' := z+1; the E=-1 bed case included; n=3 cells with B present have E >= -1). Existence lemmas: (E1) (A-b OR B) always exists; (E2) tied top => E <= 2-n; (E3) non-exception parents of the (1,1,1)@{0,1} exception cells are finitely many (A-a: (2,1,1)@{0,1}; B: (1,1,1,1)@0; C: (1,1,1)@{1,2}); (E4) region-wise exclusion: tied at D=0 forces the single family F5 bed (a,a,1)@0, tied and x1=1 impossible at D in {-1,-2}. The generic 5-row D-coordinate mex table (D>=1 / D=0 / D=-1 / D=-2 / D<=-3, columns A-a, A-b, B(n>=4), B(n=3 via L-2 coordinates), C) closes the region algebra; the interface families F1 (1,1,1)@{0,1,2}, F2 (1,1,1,1)@0, F3 (2,1,1)@{0,1}, F4 (3,1,1)@0, F5 bed (a,a,1)@0 (a>=2) are direct computations. Bases at R=0: PB2 bed (1,1) terminal 0; L-2 has no R=0 cell; T-BB2 has no R<=1 cell (min R=2 at (1,1,1)@0). L-2 itself is proved by a 3-region (Z>=g / Z=g-1 / Z<=g-2) plus boundary algebra with the (1,1) bed exception and the PB2 interface edges; PB2 by the g<=4 small-case algebra plus the uniform all-options-equal-chi far field. Machine D5 rebuilds the typed children from the claim tables alone (published closed form for the B-heirs of n=1) and checks mex == claim == engine pointwise n=2..6, z<=8, S<=30 (4,509 pts)."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 7e597ba0 (K1314 vacancy verified by commit search, zero hits, no counter-declaration; observed HEAD 99577d5f with only orthogonal Part EC 11x11-lane commits; declaration-note sha256 37e71df6da00ac8ae47c292ef4cd38e84bae6269c7a1b1077b8dbe1168258d6), then kit parts A1 6a324217 (verify_k1314.py, sha256 94cef6434662acad602a472f57dc1d7021fafbd6bd6680773d9b2f7bedde280f, startup engine-sha gate pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92, embedded bytes identical to the K1138/K1282..K1313 chain), A2 3a8f0373 (kit README.md + standalone engine_block.py 582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0 identical to the K1282..K1313 kits + predry layout), B1 620265ee (frozen pre-declaration exploration: explore_k1314.py sha256 6e95ac4bd0e1f1ccadf55aa05a0ad21af0cf74003d67944ebb17676747316ff8 + explore_k1314.out sha256 197ca679c79a3b211072fc37118ef5a499baa4243ecfceb4839ee92661cad7f0; waves WA..WG all bad 0, ALL_WAVES_OK true), B2 eaa349c9 (4 predry runs byte-identical sha256 4c2102c689e3b7848fcb1708a4a8c0f865e81d31c1a2118e4d8cbd598bee1240, ~4.1 s/run; same cwd x2 PYTHONHASHSEED random/1 + isolated tree env -i x2 99/7), all pushes fetch-back byte-verified, THEN official 4 runs from the verified bytes at f62a02a3 (part 1: all rc=0, stdout byte-identical to the declared predry sha), tamper battery 15/15 exactly as pre-declared (part 2a-d: 80987915 / c617fb74 / fc1ab849 / 119638fe), detcheck.json verdict OFFICIAL-PASS + MANIFEST-sha256 (24 files, self-excluded) at b32413b3 (part 3), post-push fetch-back 25/25 byte-identical (FNV-1a 64 gate; 2 files retried after a transient rate limit). counts [1440, 2646, 2970, 928, 4509, 2338, 851, 7026, 542, 9538, 2145, 2912, 1968, 700] total 40,513 bad 0 (D1 T-BB2 census n=3 heaps<=8 z<=11 negative E incl. / D2 census n=4 + n=5 / D3 census n=6 + n=7 / D4 exception+interface families /(1^n) n=3..7 z<=40, (2,1,1) z<=40, (a,1,1), (a,a,1) a<=12 z<=30/ / D5 typed self-check n=2..6 z<=8 S<=30: children ONLY from claim tables, mex == claim == engine / D6 L-2 census pairs m<=11 g<=14 Z<=14 + beds a<=13 Z<=14 / D7 PB2 census a,b<=20 + L-BR2 census x<=29 Z<=19 with claim == engine == published closed form (577) + L-0 / D8 published anchors byte-faithful 7,026: K1313 T-BB (n=2..3) + K1311 T-DB boundary + K1312 T-CSUM tail + K0832 single-token closed-form replication sweep (3,900) / D9 cross-engine canonical vs ordered vs claim / D10 WA watershed reproduction: merge census 9,537 pts + multivalue check, EXACTLY (-1,-3)->{0,1} and (-1,-2)->{1,2} / D11 corollary A/B/C sweep, K0832 transient band k=0, Y<=10 z<=12 with band-condition asserts / D12 two-layer sweep (published top row T-BB + this row T-BB2, n=3..5) / D13 deep negative-E families a^n and (a+1,a^{n-1}) n=3..5 a<=8 z<=40 / D14 seed-1314 random multiset sweep n=2..7). Mutation battery 15/15 fail-closed exactly as pre-declared: --tamper-engine rc=2 (mutated sha 0ea47a80761d2b20bf414cd52b1535fba56829c3a4c232d1b2f5da3f81441882, same pin same mutation as K1311/K1313), ty 1440 / d2 2646 / d3 2970 / ex 928 / tt 4509 / l2 2338 / pb 851 / ps 7026 / ce 542 / wa 9538 / ab 2145 / db 2912 / zz 1968 / rs 700, all rc=1 with single-battery contamination arrays matching the declared counts."
  - "REACH and OPEN registrations (note SS5): with T-CSUM (K1312) + T-DB (K1311) + T-BB (K1313) + T-BB2 (this) + L-2/PB2 + the published n=1 closed form and the published n=2 top row (T-BB degeneration = K1310 T-NCW constants), every n-mountain face is determined for ALL k >= z+n-4, every multiset, every n >= 2; the below-band open shrinks to k <= z+n-5 (n=3: k <= z-2; n=2 plane side k <= Z-3). New open O-BBL3: the true law of that layer — whether the (E,w)-style merge penetrates deeper, the geometry of its 2-lines and flip regions; K0832 unified conjecture U (k >= 1 slices, k_row = E-1-2k <= z+n-5) is exactly this layer and stays open as the structural conjecture of O-BBL3. O-DB3 update: the B-heir typing is now FULLY determined at every level (n-1 = 1 -> L-BR2, 2 -> L-2, >= 3 -> T-BB2), so the third-row census (k = z+n-5) can be attacked bottom-up from the second-row values at plane z+1 (now known). The n=2 wall interface (PB2 vs L-2: the g=2 edge PB2(2)=0 vs L-2 formal value [g even]=1, g=3 value 2 vs [g odd], parity inversion for g >= 4) is the FIRST concrete instance of two DIFFERENT laws on the same k row at different planes; whether such plane splices recur deeper is an O-BBL3 observation target. Standard 11x11 empty board, two-stone roots, S2, classes 1/2/4 UNKNOWN at all times; verdicts unconsumed; the 40,513 census points are machine consistency checks and NOT a replacement for the hand proofs."
relations:
- type: resolves
  target: K1313
  note: "K1313 が open 登録した O-BBL2（下帯 k≤z+n−4）のうち**第2行 k=z+n−4 を本項の T-BB2 が全称定理として解決**（n=2 側は L-2/PB2 で全解消）。残る open は k≤z+n−5（O-BBL3 として新規登録）。K1313 §5.2 の問い「(E,z) 単一座標崩壊がどこまで貫くか」への回答: 同一 n 内では (E,z)、n をまたぐ正しいマージ座標は (E,w)（D10 で多値セル (−1,−3)→{0,1}・(−1,−2)→{1,2} を厳密特定）。"
- type: resolves
  target: K0832
  note: "3トークン過渡帯 k=0 奇数スライス R=2x−1 の予想 A/B/C を系として解決（A は T-BB2 の 2-line・B は公刊 T-DB の 2-line・C は公刊 T-BB に厳密帰着・帯条件 x<R<S+z+2 を検証・D11 で 2,145 点の有限照合）。統一予想 U（k≥1 スライス）は open のまま（O-BBL3 層に該当）。"
- type: depends_on
  target: K1313
  note: "頂行 k=z+n−3 の公刊 T-BB（系C の帰着先・D8 アンカー転写〔n=2..3〕・D12 頂行+第2行 2 層同時掃引の頂行側）。"
- type: depends_on
  target: K1311
  note: "境界行 k=z+n−2 の公刊 T-DB（系B の帰着先・D8 アンカー転写）。座標 E := 2x1−S の規約も K1311。"
- type: depends_on
  target: K1312
  note: "tail 行 k≥z+n−1 の公刊 T-CSUM（k≥z+n−4 領域確定のインターロック・D8 アンカー転写）。"
- type: depends_on
  target: K0832
  note: "L-BR2 は公刊単一トークン閉形式の R=x+Z−3 スライスとして直導（4 分枝・例外 (1,3),(3,1),(Z=x≥2)・R=0 込みで一致・D7 で claim==engine==公刊閉形式を 577 セル照合）。閉形式複製掃引 3,900 点も D8 に含む。"
- type: related
  target: K1282
  note: "engine block pin chain（埋込み bd5f22e4…・単体 582c93c1…）は K1282..K1313 kit と同一 bytes。"
artifacts:
- path: research/log/2026-11-25-belowband-row2-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 7e597ba0・単一 commit・sha256 37e71df6…）。§1 主張（T-BB2/L-2/PB2/L-BR2/L-0・typed 子恒等式・系 A–C・k≥z+n−4 完全確定の意味）・§2 手証明全文（2.1 型付き子の D 座標代数と存在補題 E1–E4・2.2 L-0・2.3 L-BR2 の公刊閉形式スライス直導・2.4 PB2 領域代数・2.5 L-2 領域代数〔3 領域+2 境界+床・PB2 インターフェース縁〕・2.6 T-BB2 generic 5 行 mex 表+族 F1–F5 直接計算・2.7 単一 R 強帰納の組み立て・2.8 系 A/B/C 導出・2.9 n=2 面と公刊則との接続）・§3 凍結探索 WA..WG（多値セル (−1,−3),(−1,−2) の特定・typed closure 5,007 等）・§4 機体宣言（14 電池 40,513 点・変異表 15 種・predry sha 4c2102c6…）・§4.5 主張の区別・§5 open 登録（O-BBL3/O-DB3/plane 0 vs plane ≥1 界面）・§6 honest 経緯（凍結前 engine ブロック provenance コメント省略による起動 sha ゲート fail の修正記録・草稿 w1..w6 の発見経緯・手計算 spot-check 約 25 点）。
- path: research/experiments/belowband-row2-20261125/
  role: machine
  note: 実験キット一式（出版 6a324217/3a8f0373/620265ee/eaa349c9・成果物 f62a02a3/80987915/c617fb74/fc1ab849/119638fe/b32413b3）: README.md・verify_k1314.py（sha 94cef643…・engine pin bd5f22e4… startup ゲート内蔵）・engine_block.py（582c93c1…・K1282..K1313 chain と同一 bytes）・explore_k1314.py/.out（6e95ac4b…/197ca679…・WA..WG 凍結正本）・predry 4 走（+.info・byte-identical 4c2102c6…）+ 公式監査成果物（output/official_run1-4.out+.info・tamper レコード 15・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 24 files・自己除外）。成果物 fetch-back 25/25 byte 一致（FNV-1a 64 照合・rate limit 2 件は再試行で解消）。
- path: research/log/2026-11-25-belowband-row2-collapse.md
  role: report
  note: 実行 log（chain 7e597ba0→6a324217→3a8f0373→620265ee→eaa349c9→f62a02a3→80987915/c617fb74/fc1ab849/119638fe→b32413b3・公式 4 走・変異電池 15 種実測表・主張区分の再掲・次課題 k=z+n−5 行 census・統一予想 U・plane 摺り合わせ観測）。

## 概要

公刊 tail (K1312)・境界行 (K1311)・頂行 (K1313) に続き、**下帯の第2行** k=z+n−4 を
全多重集合について全称確定した (K1138 エンジン座標):

- **T-BB2**: ∀ n≥3, z≥0, 降順多重集合 X, k := z+n−4 について
  **H = [E odd] (E≤z+n−4) / 2 (E=z+n−3) / 1−[E odd] (E≥z+n−2)**。
  例外セルは X=(1,1,1) の z=0→0・z=1→2 の 2 個のみ。値の n をまたぐ正しい
  マージ座標は **(E, w)**・w := E+z+n−5（多値セルは (−1,−3)→{0,1} と
  (−1,−2)→{1,2} のみ・いずれも例外セル由来・D10 で厳密特定）。
- **L-2 / PB2**: n=2 の第2行（plane Z≥1 の行 k=Z−2 と plane 0 壁行 k=−2）。
  PB2 の遠方場は L-2 に対して**偶奇反転**しており、同一 k 行でも plane が
  異なれば則が異なる最初の実例（内部インターフェース）。
- **L-BR2 / L-0**: 基底補題（公刊 K0832 閉形式の R=x+Z−3 スライス・空多重集合）。
- 手証明は型付き子 (A-a/A-b/B/C) の D 座標代数 + 存在補題 E1–E4 + generic 5 行
  mex 表 + 族 F1–F5 の直接計算 + **単一 R 強帰納**で完結（全子が予算 R−1 に着地
  するため、K1311 T-DB のような外側 n 帰納が不要）。B 承継の typing
  （n−1=1→L-BR2, 2→L-2, ≥3→T-BB2）が完全確定した。

系として **K0832 の 3トークン過渡帯予想 A/B/C**（k=0 奇数スライス・有限監査のみ
で支持されていた）を解決した（A は T-BB2 の 2-line、B は公刊 T-DB、C は公刊 T-BB
に厳密帰着）。**これで全多重集合 n≥2 の k≥z+n−4 が完全確定**。残余 open は
k≤z+n−5 のみ (O-BBL3)。統一予想 U は open 継続。

## 主張の区分 (過大主張の防止)

- 定理 (手証明が正本・宣言ノート §2): T-BB2・L-2・PB2・L-BR2・L-0。
- 系 (§2.8 で全称導出): K0832 予想 A/B/C。帯条件 x<R<S+z+2 は三者とも検証済み。
- 有限 witness 認証 (全称主張なし): D10 多値セル特定 (WA watershed)。
- census は証明ではない: 40,513 点は定理の実機照合 (bad 0)。D5 typed 検査
  (4,509 点) は帰納段 mex 計算の機械再現。D7/D8 は公刊閉形式・公刊アンカーの
  転写検査であり再主張ではない。
- 下帯 k≤z+n−5 (n≥3) / k≤Z−3 (n=2 plane 系) と統一予想 U は open のまま
  (O-BBL3 として新規登録・本項は不消費)。

## 公式監査 (publish-then-execute)

- 宣言 7e597ba0 (K1314 空き確認後・対抗宣言なし・note sha256 37e71df6…) →
  kit 6a324217/3a8f0373 (機体・engine_block) → 620265ee (explore 凍結) →
  eaa349c9 (predry 4 走 byte-identical 4c2102c6…) → 公式 4 走 f62a02a3
  (同一 cwd×2 PYTHONHASHSEED random/1 + 隔離 tree env -i×2 99/7) すべて
  rc=0・stdout byte-identical sha256 4c2102c6… (宣言・predry と同一)。
  約 4.1 秒/走。
- counts `[1440, 2646, 2970, 928, 4509, 2338, 851, 7026, 542, 9538, 2145,
  2912, 1968, 700]`・総計 40,513 点・bad 0・engine_gate PASS。
- 変異電池 15/15 検出・宣言どおり: engine rc=2 (0ea47a80…)・ty 1440・
  d2 2646・d3 2970・ex 928・tt 4509・l2 2338・pb 851・ps 7026・ce 542・
  wa 9538・ab 2145・db 2912・zz 1968・rs 700 (全 rc=1・単一電池汚染・
  bad 配列は宣言 counts と完全一致)。
- 成果物出版 b32413b3 (official_run1-4.out+.info・tamper レコード 15・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 24 files・自己除外)・
  fetch-back 25/25 byte 一致 (FNV-1a 64 照合)。
- インシデント (内容影響なし・note §6 に記録): 凍結前の explore 初版の engine
  ブロックが公刊 provenance コメント 6 行を欠く bytes で起動 sha ゲートに fail
  した。公刊 bytes に差し替えて再実行・全波完走後に凍結 (6e95ac4b… が正本)。
  値への影響なし。重大インシデントなし。

## 11×11・規約への接続

- verdict 不消費・11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN。
- 第2行の O(1) 即値則・B 承継 typing の完全確定が 11×11 giant レーンの枝刈りに
  効くかの採用判断は giant レーン側 (構造補題の接続は記録のみ)。

## 次課題 (単一オーナー候補)

1. **第3行 k=z+n−5 (n=3 では k=z−2)**: (E,w) 風マージ座標の貫徹有無を
   X2 型 census で最初に判定 (O-BBL3 の入口)。B 承継 typing が確定したので
   plane z+1 の第2行値 (本次既知) からボトムアップで攻められる。
2. **統一予想 U (K0832 k≥1 スライス)**: ちょうど O-BBL3 層に位置する構造予想。
3. **plane 摺り合わせの観測**: PB2/L-2 型界面 (同一 k 行・異なる plane で則が
   異なる) が下帯深層で再出現するか。
