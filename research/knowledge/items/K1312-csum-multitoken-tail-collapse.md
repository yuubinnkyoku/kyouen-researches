---
id: K1312
title: "C-SUM 多重トークン tail 崩壊: T-CSUM（全 n≥1・全多重集合 X の tail k≥z+n−1 で H(S+k;X;z)=S mod 2・値は総和 parity のみ・値 2 なし）・L-1（単一トークン tail k≥z で H=x mod 2・公刊 K0832 閉形式の 4 分枝スライス）・L-2（空位置 H(R;();z)=0・mex{1}=0 帰納）・C-SHARP（閾値は鋭い: n≥2 の境界行 k=z+n−2 に反則セル必在・公刊 K1311 T-DB から厳密に従う系）・K1308 O3/F1 の C-SUM census 予想を解決・K1311 T-DB とのインターロックで全多重集合 n≥2 の領域 k≥z+n−2 を完全確定・publish-then-execute・26,302 点公式監査 bad 0・4 走 byte-identical b22b9b02・外側 n・内側 R 強帰納 + typed 子 mex（全子が 1−c）で閉じる.packet"
kind: theorem
status: proved
topics: [grundy, residual-games]
aliases:
  - "THE PACKAGE: the TAIL-row collapse for ALL token multiplicities (the general-multiset complement of the published all-ones tail systems). Coordinates as K1285/K1308/K1311: H(R; X; z) with S := sum(X), k := R - S, tokens >= 1, value = mex of option set (K1138 published engine, ordered/canonical equal). T-CSUM (universal): for every n >= 1, every multiset X of n tokens, every z >= 0 and every k >= z+n-1: H(S+k; X; z) = S mod 2. The value depends on the TOTAL parity only (not on individual heap sizes), never takes the value 2, and the threshold is SHARP for every n >= 2 (C-SHARP, a rigorous corollary of the published K1311 T-DB boundary law D(E,k): the family X = (z+2n-1, 1^{n-1}) has E = z+n = k+2 on the boundary row k = z+n-2, D-value 1-[S odd]; the family X = (z+2n-2, 1^{n-1}) has E = k+1, D-value 2; both contradict the tail law, so the threshold cannot be lowered; n=1 sharp by the published L-SDB x=z instance value 2). SUBSUMPTIONS: n=2 tail row k=z+1 IS the published K1308 T-UH / T-DU' vertex; the published K0832 all-ones tail corollary (X = 1^n: R = n+k >= 2n+z-1 <-> k >= z+n-1, value [n odd]) is the X = 1^n instance. RESOLVES K1308 O3/F1: the C-SUM census conjecture (triples/mixed/quads boxes published there as OBSERVED, D8 boxes 2,364 pts) becomes a theorem; D7 re-transcribes the boxes byte-faithfully. INTERLOCK (recorded): with the published K1311 T-DB (boundary row k = z+n-2 for every multiset, single coordinate E = 2*max(X)-S) this theorem determines the WHOLE region k >= z+n-2 for every multiset and every n >= 2; n = 1 is fully determined by L-1 (all k >= z = z+n-1). The published tail systems of K0832 covered the all-ones family only; K1311 C2 therefore recorded the tail layer as 'published, connection only' — THIS PACKAGE supplies the general-multiset proof of that layer (a complement, not a correction)."
  - "STRUCTURE (typed children, DOUBLE induction: outer on n, inner STRONG on R at fixed n): Region(n) := {(R; X; z): |X| = n, k := R-S >= z+n-1}. Every option of a tail cell is EXACTLY one of (A) v>1 reduce: child (R-1; X with one v -> v-1; z): n unchanged, S' = S-1, k' = k >= z+n-1, child in Region(n) at R-1, inner IH value = S' mod 2 = 1-c; (B) v=1 remove: child (R-1; X\{v}; z+1) — n' = n-1, S' = S-1, k unchanged >= (z+1)+(n-1)-1 = z+n-1, child in Region(n-1), outer IH value = 1-c (the n'=0 heir is () with L-2 value 0 = 1-c since then X=(1), c=1; the n'=1 heir is the L-1 instance x mod 2 = S' mod 2); (C) z>=1 plane-down move, option value 1^H(R-1; X; z-1): k' = k-1, z' = z-1, threshold (z-1)+n-1 ⟺ k >= z+n-1 (the hypothesis itself), child in Region(n) at R-1, inner IH gives H = c, option value = 1-c. All option values equal 1-c and opts ≠ ∅ (a token option always exists since n >= 1), so opts = {1-c} uniformly, mex{1}=0 (c=0) and mex{0}=1 (c=1) give H = c. Base: n=1 is L-1 (four-branch slice of the published K0832 closed form; z=0 min(R,x)%2 = x%2 since R >= x; z=x branch both special conditions fail since R = x+k >= 2x; 1<=z<=x-1 branch m=q_odd(z) <= z < x <= x+z <= R kills both middle bands; z>=x+1 branch m=q_odd(x) <= x < x+z <= R kills the low band), plus L-2 empties by the mex{1}=0 induction. D5 machine-rebuilds the typed children from the claim tables alone (published closed form for the B-heirs of n=2) and checks mex == claim == engine AND set(children) == {1-claim} pointwise for n=2..5, z<=8, k in {z+n-1, z+n, z+n+1} (6,642 pts)."
  - "MACHINE (publish-then-execute, exact chain): single-owner declaration note published FIRST at 13e5f611 (K1312 vacancy verified by commit search, zero hits, no counter-declaration; K1311 slot had been taken earlier the same hour by the parallel lane 7653a639/e92542fd — verified content-complementary, no duplication), kit f74ead63 (13 files: README.md, verify_k1312.py, engine_block.py, explore_csum.py, explore_csum.out E6/E7/E8 frozen, predry/dryrun1-4 (+.info), 4 predry runs byte-identical sha256 b22b9b022461cc5b7e1927a180f92b37a7768f48ce2ace1ccb8a0e05d9404e3b, ~8.2 s/run), fetch-back 13/13 blob-sha equal to local git blob sha (byte-faithful), THEN official 4 runs from the verified bytes: same cwd x2 (PYTHONHASHSEED random/1) + isolated tree env -i x2 (PYTHONHASHSEED 99/7), all rc=0, stdout byte-identical to the declared predry sha, elapsed 8.1/8.2/8.1/8.3 s. Kit push hit one non-FF race against the parallel Part EB 11x11 lane (observed HEAD 6f280e0b) — refetched latest main and re-pushed cleanly (contents unaffected, recorded in the run log). verify_k1312.py sha256 eba59473aca206b95bb032547963f685a7c1dc21a8d058882f8c90f7ef628184 (28,407 B, embedded engine block startup sha gate pin bd5f22e4... K1138/K1282..K1311 chain identical embedded bytes; standalone engine_block.py 582c93... identical to the K1282..K1311 kits). counts [2184, 2310, 3024, 1748, 6642, 920, 8388, 616, 149, 32, 149, 140] total 26,302 bad 0 (D1 T-CSUM census n=3 z=0..12 tokens<=6 k=z+2..z+4 / D2 census n=4 z=0..9 k=z+3..z+5 + far n=3 stress z=15/18/21 / D3 census n=5 z=0..7 k=z+4..z+6 / D4 census n=6 z<=6 tokens<=4 + n=7 z<=5 tokens<=3 + far n=4 stress z=15/18 / D5 typed self-check n=2..5 z<=8: children built ONLY from the claim tables (T-CSUM + published single-token closed form), mex == claim == engine, uniformity set(children)=={1-claim} / D6 base lemmas: L-2 empties R<=19 x z<=9, L-1 vs BOTH engines x<=12 z<=9 k=z..z+2, n=1 engine-children uniformity / D7 published anchors byte-faithful: K1308 D8 C-SUM boxes 2,364 (triples 1344/mixed 840/quads 180, OBSERVED there, THEOREM instances here) + K1308 D1 T-UH tail box 5,760 + L-SB spot 264 = 8,388 / D8 cross-engine canonical vs ordered vs claim E9 boxes / D9 sharpness witnesses: the 149 frozen E6 boundary-row counters re-evaluated engine == recorded AND engine != [S odd] / D10 OBS tables E7 (11+9) + E8 pure family (12), NO claim / D11 T-DB interlock: all 149 witnesses satisfy the published D(E,k) with E = 2*max(X)-S at k=z+n-2 (149/149) / D12 sharp construction: C-SHARP 2 families n=2..11 x z=0..6, 140 pts). Mutation battery 13/13 fail-closed exactly as pre-declared: --tamper-engine rc=2 (mutated sha 0ea47a80...), c3 2,184 / c4 2,310 / c5 3,024 / c67 1,748 / ty 24,648 (every cell that uses T-CSUM as its expectation: D1..D4 9,266 + D5 6,642 + the csum share of D7 8,124 + D8 616) / lm 920 / ps 8,388 / ce 616 / sw 149 / ob 1 / db 149 / sc 140, all rc=1. Audit artifacts published at 69be721c (output/official_run1-4.out+.info, tamper records 13, detcheck.json verdict OFFICIAL-PASS, MANIFEST-sha256 50 rows). detcheck generation asserted the clean counts, engine sha, 4-run sha and all 12 mutation bad arrays against the declaration before writing."
  - "REACH and OPEN registrations (note SS5): with this package and K1311 T-DB, every n-mountain face (fixed token count n) has its k-axis COMPLETELY determined from the boundary row upwards (boundary row k = z+n-2 by K1311, tail k >= z+n-1 here), for every multiset and every n >= 2; n=1 fully by L-1. The ONLY undetermined layer for n >= 3 remains the below band k <= z+n-3 (O-BBL of K1311 — unchanged; this package does NOT consume it). E7 (boundary-row value distributions n=3 z=0..10 / n=4 z=0..8) and E8 (pure-family (a,...,a) non-monotone bad-count pattern: n3 63/117,0,0; n4 0,79/99,0,0; n5 49/72,0,63/72,0,0 across koff=0..n-1; tail row always 0) are registered as OBS with NO claim — candidate structure data for the below band. K0832 conjectures A (j=0) and C (j=1) stay open (undisturbed; conjecture B was resolved by K1311). K0832 general-n transient band z+2 <= k <= z+n-3 (the interior of the below band at general multiplicity) stays open. Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4 UNKNOWN at all times; verdicts unconsumed; the 26,302 census points are machine consistency checks and NOT a replacement for the hand proof (the proof lives in the declaration note SS2)."
relations:
- type: resolves
  target: K1308
  note: "K1308 に census 予想 O3/F1 として登録されていた C-SUM（多重トークン tail で H=S mod 2）を本項の T-CSUM が全称定理として解決。同紙 D8 の C-SUM 箱（triples/mixed/quads 2,364 点）を byte-faithful に D7 で再照合。"
- type: extends
  target: K1308
  note: "n=2 tail 行 k=z+1 は公刊 T-UH/T-DU′ 対角越えの被包（D7 で T-UH tail 箱 5,760 点を転写照合）。"
- type: extends
  target: K1311
  note: "K1311 C2 の 3 層フレームのうち tail 層を「公刊 all-ones 系・接続記録のみ」から一般多重集合の全称定理に上げた（K1311 を訂正するのでなく補完する）。インターロック: E6 の 149 境界反例全てが公刊 T-DB 則 D(E,k) に一致（本機体 D11・149/149）し、tail T-CSUM（k≥z+n−1）と境界 T-DB（k=z+n−2）で全多重集合 n≥2 の k≥z+n−2 が確定。"
- type: depends_on
  target: K0832
  note: "L-1 は公刊単一トークン閉形式の 4 分枝スライス（z=0 / z=x / 1≤z≤x−1 / z≥x+1）からの直接導出（D6 で両エンジン照合）。all-ones X=1^n では公刊 tail 系の閾値 R≥2n+z−1 ⟺ k≥z+n−1 と値 [n odd] が再現（被包整合）。単一トークン閉形式の実装も公刊転写。"
- type: related
  target: K1282
  note: "engine block pin chain（埋込み bd5f22e4…・単体 582c93c1…）は K1282..K1311 kit と同一 bytes。"
artifacts:
- path: research/log/2026-11-25-csum-multitoken-single-owner-note.md
  role: proof
  note: 単一オーナー宣言ノート（出版 13e5f611・K1312 空きを commit 検索で確認後単一 commit・fetch-back blob sha 一致）。§1 主張（T-CSUM/L-1/L-2/C-SHARP/インターロック/K1308 O3-F1/K1311 C2 補完）・§2 手証明全文（L-2 の mex{1}=0 帰納・L-1 の 4 分枝スライス・T-CSUM 二重帰納: 全子が Region 内で R−1、値 1−c、opts={1−c} 均一・C-SHARP 2 構成家族）・§3 宣言前探索 E6/E7/E8 凍結（149 witness・.out sha 4467429d… 再現一致）・§4 機体宣言（12 電池 counts 26,302・変異表 13 種・predry sha b22b9b02…）・§4.5 主張の区別・§5 open 登録（下帯 k≤z+n−3 は open 維持）・§6 honest 経緯（typed_kids 同値グループ置換バグ2件の宣言前機械検出修正・predry run3 seed 指定漏れの再実行記録）。
- path: research/experiments/csum-multitoken-20261125/
  role: machine
  note: 実験キット一式（出版 f74ead63・成果物 69be721c）: README.md・verify_k1312.py (sha eba59473…・engine pin bd5f22e4… startup ゲート内蔵)・engine_block.py (582c93c1…・K1282..K1311 chain と同一 bytes)・explore_csum.py/.out (ee40aaae…/4467429d…・E6 149 witness + E7/E8 OBS 正本)・predry/dryrun1-4 (+.info・byte-identical b22b9b02…) + 公式監査成果物（output/official_run1-4.out+.info・tamper レコード 13・detcheck.json OFFICIAL-PASS・MANIFEST-sha256 50 行）。fetch-back 13/13 + 成果物 36 ファイル出版。
- path: research/log/2026-11-25-csum-multitoken-tail.md
  role: report
  note: 実行 log（K1311 スロット並走取得の記録から K1312 回転・chain 13e5f611→f74ead63→69be721c・non-FF 競合 1 件の再 push 記録・fetch-back blob sha 照合・公式 4 走・変異電池 13 種実測表・主張区分の再掲・次課題下帯）。

## 概要

公刊 tail 系が all-ones 族のみを覆っていた残余ゲーム（K1138 エンジン・K0832 単一
トークン閉形式）について、**一般多重集合**の tail 則を全称確定した:

- **T-CSUM**: ∀ n≥1, 多重集合 X（各堆 ≥1）, S=sum(X), ∀ z≥0, ∀ k≥z+n−1:
  **H(S+k; X; z) = S mod 2**（§2 二重帰納・全子 1−c の型別 mex で閉じる）。
- **L-1/L-2**: 基底補題（公刊閉形式の 4 分枝スライス・空位置の mex{1}=0 帰納）。
- **C-SHARP**: 閾値は鋭い（公刊 K1311 T-DB から厳密に従う系・2 構成家族）。

K1308 の C-SUM census 予想（O3/F1）を解決し、K1311 T-DB とのインターロックで
**全多重集合・n≥2 の領域 k≥z+n−2 が完全確定**。n=1 は L-1 で全域確定。
all-ones では公刊 K0832 tail 系と閾値・値が一致（被包整合）。

## 主張の区分（過大主張の防止）

- 定理（手証明が正本・宣言ノート §2）: T-CSUM・L-1・L-2。系（公刊 T-DB から
  厳密に従う）: C-SHARP。
- 有限 witness 認証（全称主張なし）: D9/D11/D12。
- OBS（観察・無主張）: E7 境界行値分布・E8 純族非単調安定化パターン。
- census は証明ではない: 26,302 点は定理の実機照合（bad 0）。
- 下帯 k≤z+n−3（n≥3）は open のまま（K1311 O-BBL と同一 open。本項は不消費）。

## 公式監査（publish-then-execute）

- 宣言 13e5f611（K1312 空きを確認・対抗宣言なし）→ 機体 f74ead63（13 ファイル・
  kit push で Part EB レーンとの non-FF 競合 1 件、最新 main 再取得後に再 push）→
  fetch-back 13/13 blob sha 一致 → 公式 4 走（同一 cwd×2 PYTHONHASHSEED=random/1
  + 隔離 tree/env -i×2 99/7）すべて rc=0・stdout byte-identical sha256 b22b9b02…
  （宣言・predry と同一）。約 8.2 秒/走。
- counts `[2184, 2310, 3024, 1748, 6642, 920, 8388, 616, 149, 32, 149, 140]`・
  総計 26,302 点・bad 0・engine_gate PASS。D5 typed（申立+公刊閉形式のみで子構成・
  mex==申立==engine・均一性）・D7 公刊アンカー byte-faithful 転写・D11 T-DB
  インターロック 149/149・D12 構成家族 140 点。
- 変異電池 13/13 検出・宣言どおり: engine rc=2（0ea47a80…）・c3 2,184・c4 2,310・
  c5 3,024・c67 1,748・ty 24,648・lm 920・ps 8,388・ce 616・sw 149・ob 1・
  db 149・sc 140（全 rc=1・単一電池 bad）。
- 成果物出版 69be721c（official_run1-4.out+.info・tamper レコード 13・
  detcheck.json OFFICIAL-PASS・MANIFEST-sha256）。

## 11×11・規約への接続

- verdict 不消費・11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN。
- tail 行の O(1) 即値則が 11×11 枝刈りに効くかの採用判断は giant レーン側
  （構造補題の接続は記録のみ）。

## 次課題（単一オーナー候補）

1. **下帯 k≤z+n−3（n≥3）**: 唯一の未確定層（K1311 O-BBL と同一 open）。
   E7/E8 の OBS が下帯構造の入力データ。
2. **純族の下帯非単調パターンの全称説明**（E8: n5 koff2 で 63/72 に再上昇）。
3. **一般化**: r 人対戦版・d 次元版の tail collapse の成立可能性
   （本項は通常の mex 値・1 次元 budget のみ）。
