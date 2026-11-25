---
id: K1311
title: "境界帯全多重度崩壊: T-DB（全 n≥2 の境界行 k=z+n−2 が公刊 Z-DIAG 3 分岐則へ単一座標崩壊: H(S+k;X;z)=D(E,k)・E:=x1−Σ_{i≥2}x_i・値 2 は超対角 E=k+1 直線上のみ・n=2 は公刊 Z-DIAG/T-DU′ の被包再証明）・L-SDB（単一トークン境界行 v(x,z,x+z−1)=D(x,z−1)・K0832 閉形式から 3 枝スライス直導）・C1（K0832 予想 B を E=z+2 部分族として全称回収）・C2（n 山面 k 軸 3 層フレーム: tail〔公刊・接続記録のみ〕/ 境界行〔本項〕/ 下帯〔n=2 公刊確定済み・n≥3 は O-BBL open〕）・C3 all-ones 整合・C4 n=2 公刊の独立帰納・publish-then-execute・12,409 点公式監査 bad 0・4 走 byte-identical・外側 n・内側 R の二重帰納 + typed mex 区域代数 R-I..R-V で閉じる全多重度 packet"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the boundary-row collapse for ALL token multiplicities. Coordinates as K1285/K1308: H(R; X; z) with S := sum(X), k := R - S, X sorted descending (x1 >= ... >= xn >= 1); excess coordinate E := x1 - (x2 + ... + xn) = 2x1 - S (as low as 2-n on all-ones). D is the published K1308 Z-DIAG 3-branch law D(g,p) = [g odd] (g <= p) / 2 (g = p+1) / [g even] (g >= p+2), evaluated with python parity for g <= 0. T-DB (universal): for all n >= 2, z >= 0, descending multisets X, on the BOUNDARY row k := z+n-2 (>= 0): H(S+k; X; z) = D(E, k). The value depends on the single coordinate E ONLY (not on x2..xn individually); value 2 lies EXACTLY on the superdiagonal line E = k+1. Instances: n=2 IS the published Z-DIAG vertex row k=z with beds g=0 -> D(0,z)=0 = published T-DU' (subsumption re-proof, C4); n=3 fixes the TOP row k=z+1 of the K0832 triple transient band and PROVES K0832 conjecture B (kappa=0 slice, j=2 family R=2x-1, value 2) as the exact subfamily E=z+2 of the boundary row (C1: band condition x < R < S+z+2 always holds at R=S+z+1); n >= 4 rows are new territory. L-SDB (base, derived from the published K0832 closed form): for all x >= 1, z >= 1: v(x, z, x+z-1) = D(x, z-1) (single-token boundary row k=z-1; three-branch slice z=x / 1<=z<=x-1 / z>=x+1 of the closed form). C2: with the published K0832 Lemma P tail regime (k >= z+n-1 -> H = S mod 2, recorded as a CONNECTION ONLY, machine D7 transcription, no re-claim) and the published n=2 below-band closure (K1303 band + K1309 congruent + K1310 non-congruent windows), each n-mountain face k-axis reads as a 3-layer frame: tail / boundary row (this package) / below band k <= z+n-3 — the ONLY undetermined layer per n >= 3 is the below band (O-BBL). C3: the all-ones boundary values D(2-n, k) agree with the published K0832 U-family boundary instances (D10). Conjectures A (j=0) and C (j=1) of K0832 live BELOW the boundary row (k=z-1, k=z rows of the below band) and stay OPEN (O-BBL register, witness data OBS-BBL frozen table)."
  - "STRUCTURE (typed children, DOUBLE induction: outer on n, inner STRONG on R at fixed n): every option of a boundary cell (n >= 2, k >= 1) is EXACTLY one of (A-a) unique-top A-move x1 >= 2, x1 > x2 -> (n, same k, E-1) since max(X') = x1-1 survives re-sorting; (A-b) tied-top or any tail heap A-move -> (n, same k, E+1) (the other copy becomes the new max); (B) 1-heap removal -> (n-1, plane z+1, SAME k, E+1) since k_child = (z+1)+(n-1)-2 = k (n-1 = 1 heirs are single tokens at their own boundary = L-SDB, and in the n=2 case the L-SDB value D(x1, z) coincides with D(E+1, k) because E = x1-1, k = z; n-1 >= 2 heirs covered by the OUTER induction with unbounded budget); (C) z >= 1 -> (n, plane z-1, k-1, SAME E), option value 1 XOR D(E, k-1). Existence lemma: (i) for n >= 2 an (A-b) or (B) option ALWAYS exists, so a D(E+1, k) option is always present; (ii) E >= 1 forces (A-a) existence (x1 = (S+E)/2 >= 1+(n-1) >= 2, tied top would force E <= 0); (iii) for E <= 0 (A-a) presence is indeterminate but harmless: the region algebra only needs 'if present then value 1-c side'. Region mex algebra (k >= 1, c := D(E,k)): R-I E <= k-1 -> opts subset {1-c} with 1-c present -> mex = [E odd] = c (all-ones included); R-II E = k -> (A-a) present, opts {1-c, 2, (3: C-value 1^D(k,k-1)=1^2} -> mex = [k odd] = c; R-III E = k+1 -> forced (A-a) gives D(k,k) = t := [k odd], (A-b/B) gives D(k+2,k) = 1-t, (C) gives 1^t -> opts {t, 1-t} = {0,1} -> mex = 2 = c; R-IV E = k+2 -> (A-a) gives 2, (A-b/B) gives [k odd] = 1-c -> mex = [k even] = c; R-V E >= k+3 -> all option values 1-c -> mex = [E even] = c. All regions close pointwise; (C)-absence at z=0, k >= 1 (n >= 3) harmless in R-I..R-V. k=0 base cells (only (z=0, n=2) exists for k=0) are outside the typed analysis, published Z-DIAG z=0 + T-DU' z=0. Well-foundedness: every typed child has budget R-1 < R except (B)'s n-1 child which is covered by the outer induction (budget unbounded). Honest history (note SS6): two pre-declaration implementation bugs (ascending-tuple E mismeasurement giving 11+1 FALSE mismatches on n=4..7; tied-top mistyping in early typed options) were fixed BEFORE freeze and are recorded in the declaration note; frozen explore_db.py is the corrected original."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 7653a639 (observed HEADs: 6247d6a5 at work start via tarball, 04c132fd Part EA at declaration push — the 10 racing commits were all orthogonal Part DZ/EA 11x11 canonical-cache adoptions with no knowledge changes; K1311 vacancy verified by commit search, no counter-declaration), kit e92542fd (13 files: README.md, verify_k1311.py, engine_block.py, explore_db.py, explore_db.out X1..X5 frozen, predry/dryrun1-4 (+.info), 4 runs byte-identical sha256 811d7ae3390ef43c94cc24f3ae5d77c32de179bc9336d468be49201997d44bdb, ~2.2 s/run python 3.12), fetch-back 14/14 byte-identical (declaration note + kit; every sha256 matched the declared pins incl. predry x4), THEN official 4 runs from the verified bytes: same cwd x2 (PYTHONHASHSEED random/1) + isolated tree env -i x2 (PYTHONHASHSEED 99/7), all rc=0, stdout byte-identical to the declared predry sha. verify_k1311.py sha256 4b5b81de90a8c45da69d36d1903ed543f40212c1394afb999c16d22ff1f20b9b (19,093 B, embedded engine block startup sha gate pin bd5f22e4... K1138/K1282..K1310 chain identical embedded bytes; standalone engine_block.py 582c93c1... identical to the K1282..K1310 kits). counts [240, 1628, 1353, 2303, 1659, 861, 1390, 1200, 747, 521, 7, 500] total 12,409 bad 0 (D1 L-SDB census x<=20 z=1..12 / D2 n=2 boundary anchor pairs+beds k=z, z=0..10, a<=8, g<=20, S<=28 / D3 triple boundary census k=z+1 z=0..10 S<=16 full sweep / D4 n=4..7 census z=0..6 heaps<=8 S<=16..13 / D5 typed self-check n=2..5 z<=6 heaps<=6 S<=15: children built ONLY from the claim tables D + L-SDB, mex == claim == engine 1,659 / D6 cross-engine canonical vs ordered vs claim n=2..4 z<=6 S<=13 / D7 tail rows k=z+n-1, z+n published-regime transcription n=2..4 z<=4 / D8 far stress seeds 1311/1312/1313: triples z7..14, quads z7..12, n=5..7 z7..9 / D9 K0832 conjecture-B 2-set EQUALITY (value 2 iff E=z+2) triples z=0..8 S<=14 / D10 all-ones n=2..14 x z=0..10 + near-all-ones (x,1^{n-1}) n=3..8 x=2..8 z=0..8 vs D(2-n,k)/D(x-n+1,k) / D11 OBS-BBL frozen below-row table z=1..7 reproduction / D12 random multiset sweep seed 1314 n=2..6 z=0..7 500 pts). Mutation battery 13/13 fail-closed exactly as pre-declared: --tamper-engine rc=2 (mutated sha 0ea47a80...), np1 [D1] 228 / np2 [D2] 1,540 / np3 [D3] 1,297 / np4 [D4] 2,295 / ty [D5 claim flip] 1,659 / ce [D6] 838 / tl [D7] 1,390 / fs [D8] 1,199 / kb [D9 2-location reversal] 747 / ao [D10] 512 / ob [D11 frozen-table mutation] 7 / rs [D12] 490, all rc=1. Audit artifacts published at 5cf2c639 (output/audit_run1-4.out+.info, tamper 13 record files, detcheck.json verdict OFFICIAL-PASS, MANIFEST-sha256 34 entries, README/MANIFEST self-excluded per K1309 convention); post-push fetch-back verified all 34 MANIFEST rows byte-identical. detcheck generation asserted clean counts, battery names, engine sha, 4-run sha and all 13 mutation bad arrays before writing."
  - "REACH and OPEN registrations (note SS5): with this package every n-mountain face (fixed token count n) has its k-axis organized as tail / boundary / below-band, and the ONLY undetermined layer for n >= 3 is the below band k <= z+n-3 (O-BBL open; n=2 below-band fully closed by K1303 band + K1309 congruent window + K1310 non-congruent window). K0832 conjecture B is resolved as the exact E=z+2 subfamily (machine D9: 2-set equality, 747 pts); conjectures A (j=0) and C (j=1) live in the below band and stay OPEN. OBS-BBL frozen observation (D11, NO claim): triple rows k=z (ONE below the boundary), z=1..7, heaps<=8, S<=15, 80 cells/z; mismatch counts against the two naive laws D(E,z-1)/D(E,z) read (80,80,68) -> (80,56,47) -> (80,31,25) -> (80,16,12) -> (80,6,4) -> (80,2,1) -> (80,0,0), collapsing with growing z inside the finite window — a candidate watershed phenomenon recorded as witness data for the open below band. O-DB2 open: whether the inner two rows of the region algebra (E = k-1, k; the C-value transition 3 = 1^2) can be read in reverse (B-move n-1 children landing on the boundary row of plane z+1) to type the below band. Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 UNKNOWN at all times; verdicts unconsumed; the 12,409 census points are machine consistency checks and NOT a replacement for the hand proofs."
relations:
- type: extends
  target: K1308
  note: "境界行 k=z+n−2 を n=2 で読むと公刊 Z-DIAG 対角行 k=z・床は T-DU′（被包再証明 = C4）。本項は Z-DIAG 3 分岐則 D を「2 山面の境界行」として全多重度 n≥2 に単一座標 E で一般化（値 2 の超対角線 E=k+1 は g=z+1 の一般化）。機体 D2 が n=2 アンカー 1,628 点。"
- type: depends_on
  target: K0832
  note: "L-SDB は公刊単一トークン閉形式の 3 枝スライス（z=x / 1≤z≤x−1 / z≥x+1）からの直接導出（機体 D1・X3 三方照合）。C1 により予想 B（κ=0・j=2 族の値 2）を E=z+2 境界部分族として全称証明（D9 両含意 747 点・予想 A/C は下帯で open のまま）。tail 行 k≥z+n−1 の H=S mod 2 は Lemma P 系の接続記録のみ（D7 転写照合・再主張なし）。all-ones 整合（C3）は公刊 U 族との照合（D10）。"
- type: related
  target: K1282
  note: "engine block pin chain（埋込み bd5f22e4…・単体 582c93c1…）は K1282..K1310 kit と同一 bytes。"
- type: related
  target: K1309
  note: "C2 接続: n=2 の下帯 k≤z−1 は公刊（K1303 帯域+K1309 合同窓+K1310 非合同窓）で確定済み。よって 2 山面の k 軸は 3 層すべて確定（K1310 C5 と本項 C2 の合致）。"
- type: related
  target: K1310
  note: "C2 接続の相手側: n≥3 では下帯 k≤z+n−3 が open（O-BBL）。本項の typed mex 区域代数が 2 山面 packet（単一 R 強帰納・C-descent 非合同性保存）と同じ形で下帯 typed 化に使えるかは O-DB2 として open 登録。"
- type: resolves
  target: K0832
  note: "予想 B（κ=0 スライス R=2x−1・j=2 族の値 2）を境界行 E=z+2 部分族として全称回収（宣言ノート C1・帯条件 x<R<S+z+2 は R=S+z+1 で常に成立）。予想 A（j=0）・C（j=1）は境界行の下に生息し本項では確定しない（O-BBL 登録・open）。"
artifacts:
- path: research/log/2026-11-25-boundary-band-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 7653a639・着手時 HEAD 6247d6a5〔tarball〕・宣言 push 時観測 HEAD 04c132fd〔Part EA 直交〕・K1311 空き確認後に単一 commit・fetch-back byte 一致 sha256 9ccea925…）。§1 主張（T-DB/L-SDB/C1–C4）・§2 手証明全文（2.1 L-SDB 3 枝スライス・2.2 二重帰納 typed mex: 子型 (A-a)/(A-b)/(B)/(C)・存在補題・区域代数 R-I..R-V・透明性注記）・§3 宣言前探索 X1–X5 凍結（X1 (z,j) 列一様 861/861・X2 n=4..7 bad 0・X3 160+963+63・X4 960+1,390・X5 typed 597/597）・§4 機体宣言（12 電池 counts・総計 12,409・変異表 13 種・predry sha 811d7ae3…）・§4.5 主張の区別・§5 open 登録（O-BBL/O-DB2・OBS-BBL 凍結表）・§6 honest 経緯（昇順タプル E 誤計測 2 件の宣言前修正）。
- path: research/experiments/boundary-band-20261125/
  role: machine
  note: 実験キット一式（出版 e92542fd・成果物 5cf2c639）: README.md・verify_k1311.py (sha 4b5b81de…・engine pin bd5f22e4… startup ゲート内蔵)・engine_block.py (582c93c1…・K1282..K1310 chain と同一 bytes)・explore_db.py/.out (5747cb9a…/6b48b840…・X1..X5 凍結正本)・predry/dryrun1-4 (+.info・byte-identical 811d7ae3…) + 公式監査成果物（output/audit_run1-4.out+.info・tamper レコード 13・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries）。fetch-back 14/14 + MANIFEST 34 行全照合。
- path: research/log/2026-11-25-boundary-band-collapse.md
  role: report
  note: 実行 log（出版 chain 7653a639→e92542fd→成果物 5cf2c639 の記録・fetch-back byte 照合・公式 4 走・変異電池 13 種の実測表・受入判定・§4.5 の主張区分の再掲・次課題 O-BBL/O-DB2）。

## 概要

K1308 Z-DIAG（ペア対角行）を「2 山面の境界行」と読み直し、**全多重度 n≥2 の境界行
k=z+n−2** が公刊 3 分岐則に**単一座標で崩壊**することを全称確定した:

- **T-DB**: H(S+k; X; z) = D(E, k)。値は E:=x1−Σ_{i≥2}x_i のみで決まり、
  x2..xn の個別値に非依存。値 2 は超対角 E=k+1 の直線上ちょうど。
- **L-SDB**: v(x,z,x+z−1)=D(x,z−1)（単一トークン境界行・帰納 base・
  K0832 閉形式から 3 枝スライスで直導）。

n=2 インスタンスは公刊 Z-DIAG/T-DU′ そのもの（被包再証明・C4）。n=3 インスタンスは
K0832 過渡帯の頂行 k=z+1 を全確定し、**予想 B を E=z+2 部分族として全称証明**（C1）。
n≥4 は新領域。公刊 tail 系（k≥z+n−1→H=S mod 2・K0832 Lemma P 系）と合わせ、
n 山面の k 軸は tail／境界行／下帯の **3 層フレーム** に整理され、n≥3 で未確定なのは
下帯 k≤z+n−3 のみ（O-BBL open・OBS-BBL 凍結表を証人データとして登録）。

## 主張の区分（過大主張の防止）

- 定理（全称証明・宣言ノート §2 に証明全文）: T-DB・L-SDB。
- 導出補題（published からの直接導出）: C1・C2〔tail は接続記録のみ〕・C3・C4。
- census は証明ではない: 12,409 点は定理・手表 typed mex の実機照合（bad 0）であり、
  定理の全称性は手証明によって成立する。
- D11 OBS-BBL 凍結表は観測登録（法則主張なし）。下帯は open のまま。
- 予想 A（j=0）・C（j=1）は下帯に生息し本項では確定しない。

## 公式監査（publish-then-execute）

- 宣言 7653a639（着手時 HEAD 6247d6a5・push 時観測 HEAD 04c132fd〔Part DZ/EA
  並走は 11×11 canonical cache 採用系列で knowledge 変更なし・直交〕・K1311 空きを
  commit 検索で確認・対抗宣言なし）→ 機体 e92542fd（13 ファイル）→
  fetch-back byte 一致（宣言ノート+kit 14 ファイル・全 sha256 が宣言 pin と一致）→
  公式 4 走（同一 cwd×2 PYTHONHASHSEED=random/1 + 隔離 tree/env -i×2 99/7）
  すべて rc=0・stdout byte-identical sha256 811d7ae3…（宣言・predry と同一）。
  約 2.2 秒/走。
- counts `[240, 1628, 1353, 2303, 1659, 861, 1390, 1200, 747, 521, 7, 500]`・
  総計 12,409 点・bad 0・engine_gate PASS。D5 typed（申立+L-SDB 表のみで子構成・
  mex == 申立 == engine 三点一致）・D9 予想 B interface（値 2 ⇔ E=z+2 の両含意）・
  D10 all-ones 公刊 U 族整合・D11 OBS-BBL 凍結表 7 行再現。
- 変異電池 13/13 検出・宣言どおり: engine rc=2（0ea47a80…）・np1 228・np2 1,540・
  np3 1,297・np4 2,295・ty 1,659・ce 838・tl 1,390・fs 1,199・kb 747・ao 512・
  ob 7・rs 490（全 rc=1・per-battery bad 配列も宣言どおり単一電池）。
- 成果物出版 5cf2c639（audit_run1-4.out+.info・tamper レコード 13・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256 34 entries）→ fetch-back MANIFEST
  全 34 行照合一致。

## 11×11・規約への接続

- verdict 不消費・11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 は全時点 UNKNOWN。
- census 12,409 点は定理の実機照合であって証明の代替ではない。
- 境界行の O(1) 即値則が 11×11 枝刈りに効くかの採用判断は giant レーン
  オーナー側（構造補題の接続は記録のみ）。

## 次課題（単一オーナー候補）

1. **O-BBL**: n≥3 の下帯 k≤z+n−3 の真の法則。OBS-BBL 凍結表（triples k=z 行・
   z=1..7・naive 不一致計数の z 増大で消える観測）が入力データ。
   K0832 予想 A（j=0）・C（j=1）の生息地。
2. **O-DB2**: 区域 mex の内側 2 行（E=k−1, k）の (C) 値遷移 3=1^2 の逆読み
   （B 手 n−1 子が境界行 z+1 に落ちる構造）で下帯を typed 化できるか。
3. **一般化**: r 人対戦版・d 次元版の境界行collapse の成立可能性
   （本項は通常の mex 値・1 次元 budget のみ）。
