---
id: K1315
title: "B-BB 下帯第3行 k=z+n−5 観測パケット: OBS-BBL3 クラス (n,j) 層化崩壊 census (生 (E,z) 層は非崩壊・多値セル {n=3:17, 4:21, 5:48, 6:61, 7:90}・(6,0),(6,1),(7,1)..(7,7) は完全崩壊・(7,0) 33 セルは m2=2/≥3 の 2-族衝突帯 w∈[−17,−15]) + 族アンカー 3 ピース則 (2 on w=A / [E even] 左 / [E odd] 右・n=4..8 全 5,779 単一 2 行で法則実違反 0) + アンカー表 η(n)=1,0,−5,−10,−15/−17 と n=8 j=0 の 4 族ラダー (c2≥2→−20 / c2=1→−22 / m2=3→−24 / m2≥4→−26) + 抑制・壁族 (z*:=A−E≤0 で右高原化・反例 0 行・n=3 壁得失点族 36 行・(2^4,1,1) 型の山消失 vs top≥3 の z*=0 ライン出現を V_LAW 定数に固定) + L-BR3 転写補題 (公刊 K0832 閉形式の行オフセット −4 スライス・格子上 grid-verified 924/924) + CONJ-BBL3 全称予想 (未証明・明示免負付き) — 観測パケットで定理なし・O-BBL3 は open のまま・publish-then-execute・1,307 点公式監査 bad 0・verify stdout sha 5990db75…・explore 2 走 (sandbox O1/O2) + Actions runner 走が全て byte-identical 558ed202….packet"
kind: observation-packet
status: published-observation
topics: [grundy, residual-games]
aliases:
  - "OBS-BBL3 (census observations on the frozen sweep, coordinates K1311/K1314: H(R;X;z), descending X, S:=sum(X), k:=R-S, E:=2x1-S; third below-band row k=z+n-5, merge coordinate w:=E+z (=K1314 w2 up to the constant n-5, same row => same value), auxiliaries j:=#1-heaps, m2:=smallest heap >=2, c2:=#2-heaps): (a) NEGATIVE observation: the raw (E,z) layer does NOT collapse on row 3; merging all instances within a single n yields multivalue cells n=3:17 / n=4:21 / n=5:48 / n=6:61 / n=7:90 (contrast: row 2 T-BB2 collapsed raw). (b) the correct layering is the CLASS (n,j): classes (6,0), (6,1), (7,1)..(7,7) have EXACTLY 0 multivalue cells in-sweep (full collapse); residue: (7,0) has 33 (the two-tail-family conflict band, all w in [-17,-15]), plus few at n<=5 and (6,2)/(6,4) (exception families / wall corrections, all enumerated in the frozen .out). (c) 3-PIECE LAW per tail-family: within a class the instances split into 1..4 tail-families, each with a constant anchor A (the 2-line position in w), and V(E,w)=2 on w=A / [E even] for w<A / [E odd] for w>A; across ALL classes and families of n=4..8 the measured single-2 rows (5,779 lines, incl. the 464 n=8 j=0/1/2 lines) show 0 real violations; law-conforming off-level outliers (rows whose family A deviates from the class-modal) are fully declared (n=4: 8 rows, n=5: 2 rows, .out off_level_ex). (d) ANCHOR TABLE and tail ladders: modal j=0 anchors eta(n): n=3:1, n=4:0, n=5:-5, n=6:-10, n=7:-15/-17 (2 families); A_{n,j} shape (n<=7): eta(n)+2j-2*[j>=n-3] with a flat spot at j=n-3 (n=4 j=1, n=5 j=2, n=6 j=3, n=7 j=4); the (7,0) split is m2=2 -> -15 vs m2>=3 -> -17 (confirmed invariant under the heap-cap change hi=8, 639+636 votes); n=8 j=0 is a 4-FAMILY LADDER c2>=2 -> -20 / c2=1 -> -22 / m2=3 -> -24 / m2>=4 -> -26, n=8 j=1 two families -18/-20, j=2 one -16. (e) SUPPRESSION (wall effect): rows with line position z*:=A-E <= 0 (i.e. E>=A) show no 2 in-window and read as the pure right plateau [E odd]; counterexamples (E<A with no 2) are 0 rows for n>=4; wall families: n=3 (t+3,t,1) and (t+2,t,2) absorb the z=0 cell into the right plateau (36 rows, declared); (2,2,2,2,1,1)-type hills vanish in-window while top>=3 analogues (3,3,2,2,1,1)/(4,4,1,1,1,1) show the line at z*=0, pinned by the frozen V_LAW constants."
  - "L-BR3 (GRID-VERIFIED transcription lemma, no new math): the n=1 slice of row 3 (k=z-4, R=x+z-4) satisfies H_canonical(x+z-4;(x,);z) == single_token(x,z,x+z-4) on all 924 reachable cells of the x<=30, z<=30 grid (wave WA; machine battery D1 reproduces 924/924). This is a machine cross-check of the published K0832 single-token closed form at row offset -4; the universal claim belongs to the published closed form, not to this packet."
  - "CONJ-BBL3 (conjecture, NOT proven, explicit disclaimer): for ALL instances and ALL n>=3 the row k=z+n-5 value follows the 3-piece law with a family anchor A(X) determined by (n, j, tail structure); the general rule for A (ladder geometry beyond the measured ladder shapes) is undetermined. Evidence is finite-sweep only. Feasibility sketch (registered in the note): the typed-children bottom-up of K1314 should adapt, since a row-3 cell's children land on row-2 values at plane z+1 (B-heir typing n-1=1 -> L-BR2, 2 -> L-2, >=3 -> T-BB2), suggesting a single-R strong induction. O-BBL3 REMAINS OPEN; unified conjecture U (K0832 k>=1 slices) remains open."
  - "MACHINE (publish-then-execute, exact chain): declaration note da3f6538 (sha256 6c6b056fc87d6fc5f9136794138ec616d85f3fb1810fd3b2e794d4496bb44f3c), kit 919b51bf (verify_k1315.py final sha256 de580d46d7d2d65b99ebfe122a7979b308cb52d7f7febfb3a072b9f38ad2f37676 after transcription repairs 3b833e3f + 9ae7d106, engine pin bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92 startup gate, engine_block.py 582c93c1... identical bytes to the K1282..K1314 chain), 12c402a2 (kit README.md d1c2f5a5... + frozen pre-declaration explore_k1315.py 29f7080ae59ff9852b62a8c2f6d4300b3db2c713dae90589c7d9e09eda37e195; waves WA/WB/WC/WD/WE+WF/WG), frozen output explore_k1315.out sha256 558ed202ebdd0d80b6159856a836842dd10e73807d37c6eb392437f1175032eb (82,348 bytes deterministic JSON) PUBLISHED BYTE-VERIFIED via GitHub Actions workflow (.github/workflows/k1315-publish-out.yml commits 8bef5e61 + 67b87d26; the runner regenerates from the published kit with PYTHONHASHSEED=1 python 3.12, gates on the frozen sha, and auto-commits only on gate pass; published commit 7954ae84: this is a THIRD-ENVIRONMENT byte-identity proof in addition to sandbox runs; first run passed the gate but lost the final push race to a concurrent lane commit, race-safe rebase revision succeeded). OFFICIAL RUNS from fetch-back-verified bytes: O1 explore cwd PYTHONHASHSEED=1 (144.9 s) and O2 explore isolated env -i PYTHONHASHSEED=1337 LC_ALL=C (146.5 s) both byte-identical to the published .out; O3 verify full (frozen .out staged next to the kit): rc 0, overall_bad 0, engine_gate PASS, counts [924, 289, 10, 10, 74] total 1,307 = declared, stdout sha256 5990db75696b0b7ec29fd81664fee82907167af234ee6bc1c689c50100ea1f13 byte-identical to the note-S4 declared predry sha (predry 2 runs cwd / PYTHONHASHSEED=12345 also byte-identical; all stdout seed-independent). Tamper battery 6/6 fail-closed exactly as declared: --tamper-engine rc 2 (engine_gate), --tamper=law|cells|xen|anchors|census all rc 1 with the declared single-battery contamination. detcheck.json OFFICIAL-PASS published b522c00e (fetch-back sha256 ceda40d7dd3955f70d510aa7ec18e6cdaca8b0826d3809bb295fe4a7d5ca4f12)."
relations:
- type: extends
  target: K1314
  note: "K1314 が open 登録した O-BBL3（下帯 k≤z+n−5）への最初の census パケット。第3行 k=z+n−5 の観測構造（クラス (n,j) 層化・族アンカー 3 ピース則・アンカー表・ラダー・壁族）を凍結格子で確定し、CONJ-BBL3 を構造予想として登録。K1314 の B 承継 typing（n−1=1→L-BR2, 2→L-2, ≥3→T-BB2）が証明方針の根拠。O-BBL3 自体は open のまま。"
- type: depends_on
  target: K1311
  note: "座標規約 E := 2x1−S・k := R−S の定義を共有。"
- type: related
  target: K0832
  note: "L-BR3 は公刊単一トークン閉形式の k=z−4 スライス転写（格子上 924/924 機械照合・新規数学内容なし）。統一予想 U（k≥1 スライス）は O-BBL3 層に該当し open 継続、CONJ-BBL3 がその構造予想の一部を具体化するかは次課題。"
- type: related
  target: K1138
  note: "engine block 転写 chain（pin bd5f22e4…・単体 582c93c1…）は K1282..K1314 kit と同一 bytes。"
artifacts:
- path: research/log/2026-11-25-belowband-row3-single-owner-note.md
  role: declaration
  note: 単一オーナー宣言ノート（出版 da3f6538・単一 commit・sha256 6c6b056fc87d6fc5f9136794138ec616d85f3fb1810fd3b2e794d4496bb44f3c）。§1 主張（L-BR3 転写・OBS-BBL3 (a)–(e)・CONJ-BBL3 免責付き予想）・§2 定義と規約（エンジン pin・掃引格子 n=3..8 の hi/zmax・マージ座標 w:=E+z・R<0 除外）・§3 凍結探索（explore_k1315.py 29f7080a… / .out 558ed202… 82,348 bytes・波 WA..WG・n=8 j=0/1/2 464 本・WG seed=1315 ランダム 150 本）・§4 機体宣言（verify_k1315.py de580d46…・5 電池 1,307 点・変異表 6 種・predry stdout sha 5990db75…・公式実行 O1/O2/O3 構成）・§4.5 主張の区別（定理なし・11×11 UNKNOWN・verdict 不消費）・§5 open 登録・次課題 1–5・§6 honest 経緯（手計算矛盾の解消・実行環境破棄インシデント・凍結 v1→v2）。
- path: research/experiments/belowband-row3-20261125/
  role: machine
  note: 実験キット一式（出版 919b51bf/12c402a2・内容修正 3b833e3f/9ae7d106・成果物出版 7954ae84 (Actions) / b522c00e）: README.md（d1c2f5a5…）・verify_k1315.py（de580d46…・engine pin bd5f22e4… startup ゲート・5 電池 1,307 点・tamper 6 種）・engine_block.py（582c93c1…）・explore_k1315.py/.out（29f7080a…/558ed202…・WA L-BR3 924 PASS・WB 生層非崩壊 census・WC クラス census・WD アンカー投票表・WE+WF 抑制・3 ピース適合・WG seed=1315 ランダム）・output/detcheck.json（OFFICIAL-PASS・predry/O1/O2/O3/tamper/kfetch-back 実測・honest notes・fetch-back sha ceda40d7…）。Actions workflow .github/workflows/k1315-publish-out.yml（8bef5e61/67b87d26・runner 再生成 sha ゲート出版）。
- path: research/log/2026-11-25-belowband-row3-collapse.md
  role: report
  note: 実行 log（chain da3f6538→919b51bf→12c402a2→3b833e3f→9ae7d106→8bef5e61→67b87d26→7954ae84→b522c00e→item/log commit・公式実行実測値・tamper 6 種実測・大ファイル転写の incidents と Actions 切替・D5 skip 構成の発見・次課題 CONJ-BBL3 証明）。

## 概要

下帯第2行 (K1314 T-BB2) に続き、**第3行 k=z+n−5** の構造を観測パケットとして確定し
出版した (K1138 エンジン座標)。本項は**定理を 1 つも含まない**観測パケットであり、
O-BBL3 は open のまま (CONJ-BBL3 は免責付きの構造予想として登録)。

- **OBS-BBL3 (a) 生層非崩壊**: 同一 n 内の (E,z) マージで多値セルが n=3:17 / 4:21 /
  5:48 / 6:61 / 7:90 個生じ、第2行のような生層崩壊は**起こらない** (negative
  observation・第3行の複雑性の実測)。
- **(b) クラス (n,j) 層化**: 正しい層化はクラス (n,j)。(6,0), (6,1), (7,1)–(7,7) は
  掃引域内で多値セル 0 (完全崩壊)。残余は (7,0) 33 セル (2-族衝突帯 w∈[−17,−15])
  と少数の例外族・壁補正分 (凍結 .out に全列挙)。
- **(c) 族アンカー 3 ピース則**: クラス内の族ごとに定数 A が決まり、
  V = 2 (w=A) / [E even] (w<A) / [E odd] (w>A)。n=4..8 の全 5,779 単一 2 行で
  **法則実違反 0** (off-level 外れ値は宣言済みリスト)。
- **(d) アンカー表とラダー**: η(n) = 1, 0, −5, −10, −15/−17 (n=7 は m2=2 か
  ≥3 かで完全分離・heap cap 不変)。n=8 j=0 は **4 族ラダー** (c2≥2→−20 /
  c2=1→−22 / m2=3→−24 / m2≥4→−26)。A_{n,j} shape は η+2j−2·[j≥n−3]
  (flat spot を 1 個含む)。
- **(e) 抑制・壁族**: z*:=A−E≤0 の行は 2 を持たず右高原化。反例 0 行 (n≥4)。
  n=3 の壁得失点族・(2^4,1,1) 型の山消失 vs top≥3 型の z*=0 ライン出現を V_LAW
  定数に固定。
- **L-BR3 (grid-verified)**: n=1 スライス (k=z−4) が公刊 K0832 閉形式の転写として
  格子上 924/924 で一致。
- **CONJ-BBL3 (予想)**: 全インスタンスで族アンカー 3 ピース則に従うという全称予想
  (未証明)。証明方針は K1314 の typed-children ボトムアップ強帰納。

## 機体と出版 (publish-then-execute)

- 宣言ノート da3f6538 → kit 919b51bf / 12c402a2 → 転写修正 3b833e3f / 9ae7d106
  (API contents fetch-back で 4 ファイル全 sha 一致を確認)。
- 凍結 .out (558ed202…, 82,348 bytes) は GitHub Actions workflow
  (8bef5e61 → 競合修正 67b87d26) で runner 再生成 sha ゲート出版 (7954ae84)。
  runner (ubuntu-latest python 3.12) での再生が byte 一致したことは、sandbox
  O1/O2 とは独立な**第 3 環境での再現性実証**。
- 公式実行 (fetch-back bytes から): O1 (PYTHONHASHSEED=1, 144.9s) / O2 (隔離 env,
  PYTHONHASHSEED=1337, 146.5s) が出版 .out と byte 一致。O3 (verify, .out 同梱
  構成) rc 0・overall_bad 0・counts 1,307 = 宣言・**stdout sha 5990db75… が宣言
  §4 predry sha と完全一致**。predry 2 走 byte-identical (seed 非依存)。
- tamper 6 種 (engine/law/cells/xen/anchors/census) が全て宣言どおり fail-closed
  (rc 2 / rc 1×5)。
- detcheck.json (OFFICIAL-PASS) 出版 b522c00e (fetch-back ceda40d7…)。

## 主張の区別 (定型)

L-BR3 は転写照合 (grid-verified)。OBS-BBL3 (a)–(e) は凍結掃引格子上の観測。
CONJ-BBL3 は予想。11×11 空盤・二石 root・S2・class 1/2/4 は全時点 UNKNOWN・
verdict 不消費。
