---
id: K1313
title: "B-BB 下帯頂行崩壊: T-BB（全 n≥2・全多重集合 X の下帯頂行 k=z+n−3 で u:=E+z+n−4 として u≥1→[E odd]・u=0→2・u≤−1→1−[E odd]・値は座標 (E,z) のみで単一座標崩壊・E は n≥3 で下に非有界なので 2 の線 E+z=4−n と flip 領域 E+z≤3−n は無限半直線・n=2 は 6 例外セルに縮退し公刊 K1310 T-NCW-B bed 定数と T-NCW-P g*≤0 極を系として再現・K1311 O-BBL の頂行層を解決し tail T-CSUM (K1312)・境界 T-DB (K1311) とのインターロックで全多重集合 n≥2 の k≥z+n−3 を完全確定・残余 open は k≤z+n−4 のみに縮小・publish-then-execute・28,024 点公式監査 bad 0・4 走 byte-identical a634658c・単一 R 強帰納 + typed 子 6 区域 mex（U1/U2/H/I1/I2）で閉じる.packet"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the BELOW-BAND TOP-ROW collapse for ALL token multiplicities. Coordinates as K1285/K1308/K1311: H(R; X; z), S := sum(X), k := R-S, E := 2*max(X)-S (K1311 convention). T-BB (universal): for every n >= 2, z >= 0, descending multiset X, on the row k := z+n-3 (>= -1; for n=2, z=0 this is the wall row k=-1): with u := E+z+n-4, H(S+k; X; z) = [E odd] if u >= 1, = 2 if u = 0, = 1-[E odd] if u <= -1 (python parity, E negative included). The value depends on the coordinate pair (E, z) ONLY — the below-band counterpart of the published K1311 boundary collapse T-DB. E is UNBOUNDED BELOW for n >= 3 (X=(a,..,a): E=-a), so the 2-line E+z = 4-n and the flip region E+z <= 3-n are infinite half-lines; for n = 2 the constraint E >= 0 truncates them to six exceptional cells, REPRODUCING the published K1310 T-NCW-B bed constants (edge (a,a): z>=3 -> 0, z=2 -> 2, z=1 -> 1) and the T-NCW-P g*<=0 pole ([g odd] on the non-congruent window row k=z-1, z>=2) as corollaries. RESOLVES the top layer of O-BBL registered in K1311 (SS5)/K1312 (SS5): with the published tail law T-CSUM (k >= z+n-1, K1312), the published boundary law T-DB (k = z+n-2, K1311) and this row, every n-mountain face (n >= 2, every multiset) is closed for ALL k >= z+n-3; the only remaining open layer per n >= 3 is k <= z+n-4 (O-BBL2). The K1311 OBS-BBL frozen watershed observation (naive mismatch counts (80,80,68)->(80,0,0) on the triples k=z row) is fully reproduced (machine D9, exact frozen table) and explained: the naive comparisons miss exactly the transient/flip cells, T-BB matches the engine with bad 0 on that whole domain."
  - "STRUCTURE (typed children, SINGLE strong induction on R across ALL faces): L-BR1 (base lemma, a slice of the published K0832 single-token closed form): for all x >= 1, Z >= 1: v(x, Z, x+Z-2) = PB1(x,Z), t := x+Z-3: t >= 1 -> [x odd] / t = 0 -> 2 / t <= -1 -> 1-[x odd]; used for the B-heirs of n=2 (single tokens at plane z+1, row k=Z-2). Typed child identities: every option of a row cell is EXACTLY one of (A-a) unique-top reduce -> (n, z, k, E-1), child u-1; (A-b) tied-top/tail reduce -> (n, z, k, E+1), child u+1; (B) 1-heap removal -> (n-1, plane z+1, SAME k, E+1), child u+1 (n-1=1 heirs by L-BR1, whose t = u+1 reproduces exactly the same u-algebra); (C) z>=1 plane-down, option value 1 XOR PB(n, E, z-1), child u-1. ALL children sit at budget R-1, so a single strong induction over R across all row cells of all n-faces closes the theorem (unlike K1311 T-DB which needed the outer n-induction). Existence lemma: (i) (A-b OR B) always exists; (ii) tied => E <= 2-n; (iii) E >= 3-n => unique top & A-a exists. Region mex algebra with rho := [E odd] (6 regions): U1 (u>=2) all option values 1-rho -> mex = rho; U2 (u=1) opts superset {1-rho} subset {2,1-rho,3} -> mex = rho; H (u=0) opts subset {rho, 1-rho} = {0,1}, nonempty by (i) -> mex = 2; I1 (u=-1) opts = {2, rho} (2 always present by (i); rho by C if z>=1 else by (iii) at z=0 where E=3-n) -> mex = 1-rho; I2 (u<=-2) all option values rho -> mex = 1-rho. Base R=1: the single cell (n=2, X=(1,1), z=0, k=-1): PB(2,0,0) = 1 = engine mex{0}. Machine D5 rebuilds the typed children from the claim tables alone (published closed form for the B-heirs of n=2) and checks mex == claim == engine pointwise, n=2..6, z<=8, 4,509 pts."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST (K1313 vacancy verified by commit search, zero hits, no counter-declaration; observed HEAD 8440276e all orthogonal Part EA 11x11 lane commits): NOTE — the first declaration commit 0c8f5873 pushed an unfilled 8-byte placeholder instead of the note body (single-owner assembly mistake, caught by the kit fetch-back byte check in the same pass); the full note was republished verbatim with honest-history additions (final commit 66916e87). Kit ab9e4f05 (13 files: README.md, verify_k1313.py, engine_block.py, explore_k1313.py/.out X1..X10 frozen, predry/predry_random+predry_1+dryrun_99+dryrun_7 (+.info), 4 predry runs byte-identical sha256 a634658cd7baa418b2474e4793700aca2b8d7b8e2b652d7be312a31b89c4b78e, ~3.3 s/run), fetch-back 13/13 byte-identical, THEN official 4 runs from the verified bytes: same cwd x2 (PYTHONHASHSEED random/1) + isolated tree env -i x2 (PYTHONHASHSEED 99/7), all rc=0, stdout byte-identical to the declared predry sha. verify_k1313.py sha256 9fd5535d2637ea3697991812bbfcb73927d15e3eefc99072b2846020fff9786d (startup engine-sha gate pin bd5f22e4... K1138/K1282..K1312 chain identical embedded bytes; standalone engine_block.py 582c93c1... identical to the K1282..K1312 kits). counts [1440, 2646, 2970, 1768, 4509, 4200, 3742, 542, 7, 1968, 3532, 700] total 28,024 bad 0 (D1 T-BB census n=3 heaps<=8 z<=11 neg-E incl. / D2 census n=4+n=5 / D3 census n=6+n=7 / D4 n=2 census incl. wall row (z=0,k=-1) / D5 typed self-check n=2..6 z<=8 S<=30: children ONLY from claim tables, mex == claim == engine / D6 L-BR1 x<=20 Z<=15 vs closed form + both engines, plus single-token closed-form replication sweep / D7 published anchors byte-faithful: T-DB boundary 1458 + T-NCW-B beds 54 + T-NCW-P 1320 + K1312 tail 910 / D8 cross-engine / D9 OBS-BBL frozen table 7 rows exact reproduction + PB bad 0 same domain / D10 deep-negE families a^n,(a+1,a^{n-1}) n=3..5 a<=8 z<=40 / D11 T-DB adjacency two-layer sweep / D12 seed-1313 random multiset sweep n=2..7). Mutation battery 13/13 fail-closed exactly as pre-declared: --tamper-engine rc=2 (mutated sha 0ea47a80...), ty [1440,2646,2970,...], h2 [98,...], in [286,...], wl [1766->1768 at D4], tt 4509, lm 4200, ps 3742, ce 542, ob 1, db 1766, zz 1968, rs 700, all rc=1. Audit artifacts published at afeccb95 (output/official_run1-4.out+.info, tamper records 13, detcheck.json verdict OFFICIAL-PASS, MANIFEST-sha256 22 rows), post-push fetch-back 23/23 byte-identical. detcheck generation asserted the clean counts, engine sha, 4-run sha and all 12 mutation bad arrays against the declaration before writing."
  - "REACH and OPEN registrations (note SS5): with T-CSUM (K1312) + T-DB (K1311) + T-BB (this), every n-mountain face is determined for ALL k >= z+n-3, every multiset, every n >= 2 (n=1 by the published K0832 closed form). New open O-BBL2: the below band k <= z+n-4 — its true law, whether the (E,z) single-coordinate collapse penetrates further down, the geometry of its 2-lines and flip regions, and the connection to the tail side. O-DB2 update: B-children of below-band cells land on the TOP ROW of the (n-1)-face at plane z+1 (same k), now known by T-BB, so the below band can be attacked bottom-up from plane z+1 values. K0832 conjectures A (j=0) and C (j=1) live in the below band; the n=3 top row (k=z) is exactly the K0832 transient-band row J, conjecture-C consistency check flagged for the next lane run; the remaining row for A is k=z-1. OBS-BBL watershed is now fully explained at its top layer; observation interest moves to k=z-1 (n=3) and below. Standard 11x11 empty board, two-stone roots, S2, classes 1/2/4 UNKNOWN at all times; verdicts unconsumed; the 28,024 census points are machine consistency checks and NOT a replacement for the hand proofs."
relations:
- type: resolves
  target: K1311
  note: "K1311/K1312 が open 登録した O-BBL (下帯 k≤z+n−3) のうち頂行層 k=z+n−3 を本項の T-BB が全称定理として解決。残る open は k≤z+n−4 (O-BBL2 として新規登録)。K1311 OBS-BBL 凍結 watershed 観測 (80,80,68)→(80,0,0) は D9 で表ごと完全再現され、T-BB で説明完了。"
- type: depends_on
  target: K0832
  note: "L-BR1 は公刊単一トークン閉形式の R=x+Z−2 スライスとして直導 (4 分枝すべて例外セル ((1,2),(2,1),(1,1)) 込みで一致)。n=2 の B 系承継子の評価に使用。閉形式実装も公刊転写 (D6 で複製掃引 3,900 点)。"
- type: extends
  target: K1310
  note: "n=2 への縮退として公刊 T-NCW-B bed 定数 (合同縁 (a,a): z≥3→0・z=2→2・z=1→1) と T-NCW-P の g*≤0 極 (非合同行 k=z−1, z≥2 で [g odd]) を系として再現 (D7 で転写照合 54+1320 点)。壁行 (z=0, k=−1) は K1303 band の下の行として新規に閉じた。"
- type: related
  target: K1312
  note: "tail T-CSUM (k≥z+n−1) と境界 T-DB (K1311) と本項 T-BB (k=z+n−3) のインターロックで全多重集合 n≥2 の k≥z+n−3 が完全確定。D7 で K1312 tail 行 [S mod 2] を転写照合 (910 点)。"
- type: related
  target: K1282
  note: "engine block pin chain (埋込み bd5f22e4…・単体 582c93c1…) は K1282..K1312 kit と同一 bytes。"
artifacts:
- path: research/log/2026-11-25-belowband-toprow-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート (出版 chain 0c8f5873→881d8b42→66916e87・K1313 空きを commit 検索で確認後単一 commit・fetch-back byte 一致 sha256 137a9711…)。§1 主張 (T-BB/L-BR1/typed 子)・§2 手証明全文 (2.1 L-BR1 スライス・2.2 typed 子の u-座標代数・存在補題・2.3 六区域 mex U1/U2/H/I1/I2・2.4 単一 R 強帰納・2.5 n=2 縮退と公刊系)・§3 凍結探索 X1..X10・§4 機体宣言 (12 電池 28,024 点・変異表 13 種・predry sha a634658c…)・§4.5 主張の区別・§5 open 登録 (O-BBL2・O-DB2 接続更新・K0832 conjecture A/C 照合課題)・§6 honest 経緯 (D12 減量前 OOM・宣言プレースホルダ出版インシデントの記録含む)。
- path: research/experiments/belowband-toprow-20261125/
  role: machine
  note: 実験キット一式 (出版 ab9e4f05・成果物 afeccb95): README.md・verify_k1313.py (sha 9fd5535d…・engine pin bd5f22e4… startup ゲート内蔵)・engine_block.py (582c93c1…・K1282..K1312 chain と同一 bytes)・explore_k1313.py/.out (d4d727a8…/5ce1ec3a…・X1..X10 凍結正本)・predry 4 走 (+.info・byte-identical a634658c…) + 公式監査成果物 (output/official_run1-4.out+.info・tamper レコード 13・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 22 行)。fetch-back kit 13/13 + 成果物 23/23 byte 一致。
- path: research/log/2026-11-25-belowband-toprow-collapse.md
  role: report
  note: 実行 log (chain 0c8f5873→881d8b42→66916e87→ab9e4f05→afeccb95・プレースホルダ出版インシデントと修復の記録・fetch-back 照合・公式 4 走・変異電池 13 種実測表・主張区分の再掲・次課題下帯深層)。

## 概要

公刊 tail 系 (K1312)・境界行 (K1311) に続き、**下帯の頂行** k=z+n−3 を全多重集合・
全 n≥2 について全称確定した (K1138 エンジン座標):

- **T-BB**: ∀ n≥2, z≥0, 降順多重集合 X, k := z+n−3, u := E+z+n−4 として
  **H = [E odd] (u≥1) / 2 (u=0) / 1−[E odd] (u≤−1)**。値は座標 (E,z) のみ
  (単一座標崩壊)。n≥3 では E が下に非有界なので、値 2 の線 E+z=4−n と flip
  領域 E+z≤3−n は**無限半直線**。
- **L-BR1**: 基底補題 (公刊 K0832 閉形式のスライス)。
- 手証明は型付き子 (A-a/A-b/B/C) の 6 区域 mex 代数 + **単一 R 強帰納**で完結
  (全子が R−1 に落ちるため、K1311 のような外側 n 帰納が不要)。

n=2 への縮退で公刊 K1310 の bed 定数・g*≤0 極を系として再現し、n=2 の壁行
(z=0, k=−1) を新規に閉じた。**これで全多重集合 n≥2 の k≥z+n−3 が完全確定**
(tail K1312 + 境界 K1311 + 頂行 本次)。残余 open は k≤z+n−4 のみ (O-BBL2)。

## 主張の区分 (過大主張の防止)

- 定理 (手証明が正本・宣言ノート §2): T-BB・L-BR1。
- 系 (T-BB の n=2 インスタンス): K1310 T-NCW-B/P 再現・壁行の値。
- 有限 witness 認証 (全称主張なし): D9 OBS-BBL 凍結表再現・D7 公刊アンカー転写。
- census は証明ではない: 28,024 点は定理の実機照合 (bad 0)。D5 typed 検査
  (4,509 点) は帰納段の mex 計算の機械再現。
- 下帯 k≤z+n−4 (n≥3) は open のまま (O-BBL2 として新規登録・本項は不消費)。

## 公式監査 (publish-then-execute)

- 宣言 (K1313 空き確認後) → 機体 kit ab9e4f05 (13 ファイル) → fetch-back 13/13
  byte 一致 → 公式 4 走 (同一 cwd×2 PYTHONHASHSEED random/1 + 隔離 tree env -i×2
  99/7) すべて rc=0・stdout byte-identical sha256 a634658c… (宣言 predry と同一)。
  約 3.3 秒/走。
- counts `[1440, 2646, 2970, 1768, 4509, 4200, 3742, 542, 7, 1968, 3532, 700]`・
  総計 28,024 点・bad 0・engine_gate PASS。
- 変異電池 13/13 検出・宣言どおり: engine rc=2 (0ea47a80…)・ty 7056 (D1+D2+D3)・
  h2 98・in 286・wl 1768・tt 4509・lm 4200・ps 3742・ce 542・ob 1・db 1766・
  zz 1968・rs 700 (全 rc=1・単一電池 bad)。
- 成果物出版 afeccb95 (official_run1-4.out+.info・tamper レコード 13・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 22 行)・fetch-back 23/23 一致。
- インシデント (修復済み・note §6 に記録): 宣言コミット 0c8f5873 で宣言本文の
  埋め込みに失敗し 8 バイトのプレースホルダが出版された。fetch-back 照合で
  即時検出し、本文全文を verbatim 再出版 (66916e87)。定理の内容・監査には影響なし。

## 11×11・規約への接続

- verdict 不消費・11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN。
- 頂行の O(1) 即値則・型付き子の構造 (B 承継が (n−1) 面頂行に着地) が 11×11
  giant レーンの枝刈りに効くかの採用判断は giant レーン側 (構造補題の接続は
  記録のみ)。

## 次課題 (単一オーナー候補)

1. **k=z+n−4 行 (n=3 では k=z−1)**: (E,z) 単一座標崩壊の有無を X2 型 census
   で最初に判定 (O-BBL2 の入口)。
2. **O-DB2 のボトムアップ工具**: plane z+1 の (n−1) 面頂行値 (T-BB 既知) から
   下帯深層を typed 解析。
3. **K0832 conjecture A/C の照合**: n=3 頂行 k=z が今回閉じたため、conjecture
   C (j=1) の主張値との一致確認が高優先。
