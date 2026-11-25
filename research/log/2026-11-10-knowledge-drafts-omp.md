# 2026-11-10 本日分の研究結果の knowledge 項目ドラフト (W22)

対象: 2026-11-10 の W11/W12/W14/W15/W16/W17/W18/W19 と全 d 掃引完走の結果。
成果物は本 log 1件のみ。knowledge 項目ファイルは編集していない。commit / push なし。

## 0. 前提と読み方

- 本 log は**ドラフト**であり、K 番号はすべて仮番号(AGENTS.md: 作業中の新規 K 番号は仮番号)。
  統合時に main 上の番号と衝突したら再採番し、参照側も更新する。
- 数値はすべて原典 JSON / log の実読値。原典 log と JSON が食い違う箇所は §6 に列挙し、
  ドラフトの主張文には**より弱い方**を採る。
- status は `research/knowledge/VOCABULARY.yaml` の `status_by_kind` に適合させた。
  `computation/computed`, `proposition/proved`, `verification/verified`, `question/open` のみ使用。
- 新規番号は K0713..K0720(仮)。K0713..K0719 は本日分の実質、K0720 は任意(残存ギャップの記録)。

## 1. 読んだファイルと、既存項目の有無の確認

読んだ原典:

- `research/log/2026-11-10-a2647-113-full-sweep-100k-result.md`(掃引完走)
- `research/log/2026-11-10-a2647-113-easy-d-hypotheses-omp.md`(W9/H4 の提起)
- `research/log/2026-11-10-a2647-113-artifact-test-omp.md`(W11 逆順・fresh-each)
- `research/log/2026-11-10-a2647-113-candidate-b-proof-omp.md`(W10 候補B証明、前提(1)-(4))
- `research/log/2026-11-10-k0334-identity-verification-omp.md`(W12 同一性と生成器完全性)
- `research/log/2026-11-10-cardenc-verification-omp.md`(W15)
- `research/log/2026-11-10-ternary-generalization-omp.md`(W16)
- `research/log/2026-11-10-a2647-113-tail-unsat-verification-omp.md`(W17)
- `research/log/2026-11-10-a2647-113-tail-cross-solver-omp.md`(W18 + W19 追補)
- `research/log/2026-11-10-a2647-113-cross-solver-omp.md`(W14)

読んだ生データ(すべて git tracked。`git ls-files --error-unmatch` で確認済み):

- `research/experiments/parabola-p2207-no-equality-witness-20261107/output/w7-assump-2647-1322-full100k.json`
- 同 `output/w11-artifact-reverse.json`, `output/w11-artifact-fresh.json`
- 同 `output/w14-cross-solver.json`, `output/w18-tail-cross-solver.json`, `output/w19-1316-cross-rest.json`
- 同 `output/w17-tail-fresh.json`, `output/w15-cardenc-verify.json`
- 同 `search_shape_class.py`, `search_shape_class_assump.py`, `cardenc_verify.py`,
  `reverse_order_probe.py`, `tail_fresh_probe.py`, `cross_solver_probe.py`
- `research/experiments/parabola-ternary-selection-20261109/ternary.py`, `ternary_general.py`
- 同 `output/generalization-check-d1323-target1322-budget100000/{init,result}.json`
- 同 `output/generalization-check-d300-target1322-budget100000/{init,result}.json`
- 同 `output/generalization-check-d300-target1293-budget100000/{init,result}.json`
- `research/experiments/frontier-geometry-2026-10-05/forbidden_edges.cpp`, `proof.md`

読んだ既存項目: K0097, K0101, K0334, K0693, K0706, K0711, K0712, K0671(verification の書式見本)。

既存項目の有無:

- **候補B(assumption 掃引)を扱う項目は存在しない**。`grep -rln "候補B\|candidate B\|形状クラス"`
  でヒットするのは K0328(無関係な maximal-fault-tolerance)と K0711 のみ。
- 掃引 JSON を参照する項目も無い(`grep -rln "assumption\|w7-assump"` で 0 件)。
- したがって §3 の新規案(掃引・候補B・行列式同値・列挙完全性・CardEnc・独立性・三元一般化)は
  いずれも重複作成ではない。

## 2. 数値の再検証(実読)

### 2.1 掃引 JSON(`w7-assump-2647-1322-full100k.json`)

- `records` は 1,323 件、d は 1..1323 を連続・重複なしで被覆。
- 判定内訳(`sat=false, unknown=false` を UNSAT と数える): **UNSAT 67 / UNKNOWN 1,256 / SAT 0**。
- `seconds` 合計 **56,620.73 秒**。メタ: p=2647, h=1323, size=1322, budget=100000, ds_spec="1..1323",
  edges=928389, classes `{"1,1,3": {vars:17180, clauses:90891, kept_edges:53886}}`。
- UNSAT の d(全 67): 1, 32, 95, 116, 125, 158, 221, 231, 266, 284, 300, 345, 346, 347, 389, 410,
  448, 461, 473, 478, 536, 551, 567, 599, 656, 662, 725, 788, 851,
  1279, 1280, ..., 1316(38 連続)。
- 序盤 29 件(d≤851)の `seconds` 合計 **137.472 秒**。
- 中盤 d=852..1278 は **427 件すべて UNKNOWN**。
- 尾部 d=1279..1316(38 件)の `seconds` 合計 **8.333 秒**。
- 末尾 d=1317..1323 は **7 件すべて UNKNOWN**(181.3, 165.3, 167.4, 207.3, 103.0, 116.5, 164.1 秒)。

原典 log の表(67/1,256/0、137.5 秒、8.333 秒、427 件)と一致。

### 2.2 W11/W17/W14/W18/W19

- W11 逆順(8 件): d=1322 UNKNOWN 34.493, 1000 UNKNOWN 32.196, 851 UNSAT 13.203, 500 UNKNOWN 39.381,
  478 UNSAT 1.375, 300 UNSAT 0.228, 100 UNKNOWN 47.277, 1 UNSAT 0.238。
- W11 fresh-each(4 件): 851/478/300/1 すべて UNSAT(17.569 / 1.062 / 0.532 / 0.986 秒)。
- W17 fresh-each(8 件): 1280 UNSAT 661 conflicts、1290 UNSAT 946、1300 UNSAT 693、1310 UNSAT 565、
  1316 UNSAT 33,464 conflicts(20.853 秒)、1317 UNKNOWN 100,004 conflicts、1322 UNKNOWN 100,003、
  1200 UNKNOWN 100,000。`unit_conflict` は全件 false。**W17 のレコードには `verdict`/`solver`
  キーが存在しない**(キーは `budget,conflicts,d,decisions,propagations,sat,seconds,total_seconds,
  unit_conflict,unknown,wall_timeout`)。`w7-assump-…full100k.json` も
  `class,d,sat,unknown,seconds,budget` のみ。W14/W18/W19 は `verdict` を持つ。本 log は
  `sat`/`unknown` から判定を読み、原典表と突合済み。
- W14(54 レコード、records 上のソルバ 14 種。JSON ヘッダの `solvers` は 7 名のみで
  最終バッチの設定を反映しており、実データとは一致しない):
  d=1/300/478 は 13 種 UNSAT(Cadical195 含む)+ MapleChrono timeout
  ⇒ **Cadical を除いて 12 種**。d=851 は 7 種試行中 4 種 UNSAT
  (Cadical195 53.498, Ergo 54.280, MinisatGH 54.601, Kissat404 90.487)、
  Glucose4 / Minisat22 / Maplesat は 120 秒 timeout。d=100 は 5 種すべて UNKNOWN か timeout。
  **注意**: W14 の timeout には 90 秒のもの(d=1, d=300 の MapleChrono)があり、これは
  `device_timeout=120` ではなく `deadline=620`・`jobs=3` の残余打ち切り。したがって
  この 1 件の timeout は「MapleChrono がこの問題を解けない」証拠ではなく、
  打ち切り時刻の違いである(原典 §注意)。
- W18(47 レコード): d=1280 と 1300 は各 14 レコードで **UNSAT 13 / timeout 1(MapleChrono)**。
  d=1316 は **5 レコード(5 UNSAT)** のみ。d=1317 は **14/14 timeout**(壁時計 120 秒、
  conflict 予算 100k 未到達)。合計 UNSAT 31 / timeout 16。
- W19(9 レコード): d=1316 の残り 9 種で UNSAT 4(Maplesat, Glucose3, Gluecard3, Gluecard4)、
  timeout 5(MapleCM, MapleChrono, Glucose4, Glucose42, Mergesat3)。
  ⇒ d=1316 の 14 種合計は **UNSAT 9 / timeout 5**(UNKNOWN 0)。
- 表記の不整合(W18 原典): 結論 1 は「Cadical195 を除く 13 種」と書くが、直後に列挙する
  名前は 12 個(Glucose3/4/42, Gluecard3/4, Minisat22/GH, Maplesat, MapleCM, Mergesat3,
  Ergo, Kissat404)。JSON 実読では 13 UNSAT に Cadical195 が含まれるので、
  **正しい言い方は「14 種中 13 種 UNSAT、Cadical を除いて 12 種」**。§6 に記録。

### 2.3 W15(`w15-cardenc-verify.json`)

- `total_cases` 473、`total_assignments` 1,588,640、`total_mismatches` 0、`seconds` 314.01、
  `incomplete` は空、`joint_complete` true、`nmax` 12、`joint_nmax` 7。
- variants: contiguous / strided / chained(各 90 ケース、98,304 割当)、joint(203 ケース、1,293,728 割当)。
- レコードは `x['aux_alias_main']` と `x['lit_above_nv']` を持ち、全 473 ケースで 0。
- **`negative_control` キーは存在しない**(トップレベルキーは
  `script, pysat_encoding, verified_encoder, method, nmax, joint_nmax, joint_complete,
  variants, scope_note, total_cases, total_assignments, total_mismatches, incomplete, seconds, records`)。
  W15 §3.3 のとおり、ハーネスの検出力の証拠は保存物に無い。

### 2.4 W16(三元一般化)

- `generalization-check-d1323-target1322-budget100000/result.json`: d=1323, target=1322,
  status UNKNOWN, solve 54.317 秒, conflicts 100001 / decisions 217401 / propagations 50404659 /
  restarts 4854、base_clauses 53886、variables 7926、clauses 68404 — 既存実績と統計完全一致。
- `generalization-check-d300-target1322-budget100000/result.json`: status **SOLVER_UNSAT**,
  solve **1.811 秒**, conflicts **1,808**, decisions 8224。Glucose4 と Minisat22 で
  `False`(UNSAT)を独立確認(原典)。
- `generalization-check-d300-target1293-budget100000/result.json`: status UNKNOWN,
  solve 90.207 秒, conflicts 100000, variables 45249, clauses 142992。
- 原典 §4.1 の gz バイト一致・`encoded_cnf_sha256 = 8cbd404a…`、§4.4 の 19,392 割当 0 不一致、
  §5 の regression 全項目一致(19,392 割当・444 cardinality ケース)。
- 原典 §9.3 の表は d=300 を「1.70 s / 2,795 conflicts」とするが、
  `generalization-check-d300-target1322-budget100000/result.json` の実値は
  **1.811 s / 1,808 conflicts / 8,224 decisions / 1,644,604 propagations / 87 restarts**。
  `2,795` を持つ JSON は output 配下に無い(`grep` のヒットはモデル内の変数番号)。
  §9.3 の行は**別実行の値**とみられる。§6 に記録。引用は §4.3 の JSON 実値で行う。
- §9.3 の d=188/194/602(100k、UNKNOWN)には **結果 JSON が保存されていない**
  (`output/ladder-d{188,194,602}-target1322-budget100000/` は空。残るのは 300 万予算版の
  `result.json` と `.partial-*` のみ)。したがって 35.80 / 42.60 / 41.52 秒は原典 log の
  記載のみで、artifact からの再現ができない。**K0719 の主張文にはこの 3 点を入れない**。

### 2.5 実行中(本 log の結論には使わない): W20 サイズ1322 の全形状クラス DRAT

作業中に `research/experiments/parabola-p2207-no-equality-witness-20261107/output/w20-drat-1322/` が
生成され、`w20_drat_1322.py --class 0,1,2` が走っている(未追跡ファイル、未 commit)。
サイズ1322 の許容クラスは `e = x + c + 1` より (0,0,1),(0,1,2),(1,0,2),(1,1,3) の 4 つ。

現時点の観測(**途中経過。完了扱いしない**):

| クラス | 状態 |
|---|---|
| (0,0,1) | `solver.json`: SOLVER_UNSAT(1.319 秒、1,996 conflicts、proof 22,379 行)。`audit.json`: `steps=9732 rup=9732 rat=0 deletions=5756 empty=1 ok=1` `VERIFIED`(8.110 秒、`verified: true`) |
| (1,0,2) | `solver.json`: SOLVER_UNSAT(15.096 秒、24,595 conflicts、proof 790,206 行)。**audit 未出力**(進行中) |
| (0,1,2) | 求解中(init.json と input.cnf.gz のみ) |
| (1,1,3) | 未開始 |

- (0,0,1) は c=0 かつ e=1 で、クラス CNF が BOTH 変数を全否定するため **assumption を使わない
  単体 UNSAT** であり、DRAT 監査が通った最初の「サイズ1322 の非三値クラス」である。
  ただし 1 クラスのみで、サイズ1322 の全4クラス監査ではない。
- **副産物の照合(K0716 に効く)**: `solver.json` の `kept_edges` は x=0 の (0,0,1) で
  **53,882**、x=1 の (1,0,2) で **53,886**。差がちょうど 4 で、`build()` が
  `0 in q and x == 0` で捨てる辺の数と一致する。W12 3.3 の「残余 53,886 辺のうち
  0 を含むもの 4」の独立確認になる(CardEnc を経ない `build()` 単体の値なので、
  基数符号化に依存しない)。ただし作業中の値なので確定扱いは保留。
- この作業は本 log の §3〜§6 の主張(掃引の地図、A の範囲)を**変えない**。
  K0720 の「assumption-UNSAT を DRAT へ落とす手続き」に対する部分的な実例が出つつある、
  という位置づけだけを記録する。
- 完了後に別 log で報告されるべき事項であり、本 log は数値を確定値として扱わない。

## 3. 新規項目ドラフト

### 案1: K0713(仮) 全 d 掃引の完走地図

- **対象**: 新規 K0713
- **kind / status**: `computation` / `computed`(明示された有限範囲の完了計算。命題ではない)
- **title**: p=2647 サイズ1322 形状クラス (1,1,3) の 100k/d 全 d 掃引は 67 UNSAT・1,256 UNKNOWN・0 SAT で完走した
- **主張文**:
  「p=2647、size=1322、形状クラス (x,c,e)=(1,1,3)(クラス CNF 17,180 変数 / 90,891 節、
  kept_edges 53,886)を単一 Cadical195 インスタンスに載せ、完全対の仮定 `B_d` を assumption として
  d=1..1323 を昇順に 1 d あたり conflict 予算 100,000 で解く掃引が完走した。記録は 1,323 件で
  d=1..1323 を連続・重複なしで被覆し、判定は UNSAT 67・UNKNOWN 1,256・SAT 0、累計
  56,620.73 秒。UNSAT は序盤の散発 29 件(d≤851、合計 137.472 秒)と尾部の連続 38 件
  (d=1279..1316、合計 8.333 秒、うち 1279..1313 は各 0.057 秒以下、1314..1316 は 2.057/1.368/4.319 秒)
  からなり、中盤 d=852..1278 の 427 件はすべて UNKNOWN、末尾 d=1317..1323 の 7 件も
  UNKNOWN(103.0〜207.3 秒)である。」
- **限界(本文に必ず書く)**:
  - これは「100k 予算で決まる d の地図」であり、**クラス (1,1,3) の判定ではない**。
    1,256 件の UNKNOWN は UNSAT でも SAT でもない。
  - UNSAT は assumption 方式のソルバ主張で、単体の DRAT receipt ではない(W10 第2部)。
  - 尾部の即 UNSAT は、掃引だけでは「d 固有」か「学習節の蓄積」かを分離できない
    (分離は W17 が行う。→ K0718)。
  - 掃引の単一インスタンス昇順実行であるため `seconds` は履歴込みの値で、
    独立再解の時間ではない(W14 §5 の指摘)。
  - **A(2647) の範囲を動かさない**: 1296 ≤ A ≤ 1322(ソルバ主張)、DRAT 監査済み上界は 1324 のまま。
- **relation**: `depends_on: K0712`(固定原点・一完全対の還元の上でのクラス符号化)、
  `supports: K0714`(候補B分割の適用記録)、`supports: K0718`(独立性検証の対象データ)。
- **artifacts**:
  - `research/experiments/parabola-p2207-no-equality-witness-20261107/output/w7-assump-2647-1322-full100k.json` / `data` / 「1,323 レコード、67 UNSAT・1,256 UNKNOWN・0 SAT、予算 100k/d」
  - `…/search_shape_class_assump.py` / `solver` / 「1 インスタンス + assumption B_d の掃引器」
  - `.../search_shape_class.py` / `solver` / 「クラス (1,1,3) の CNF 構築(build)」
  - `research/log/2026-11-10-a2647-113-full-sweep-100k-result.md` / `log` / 「完走時刻・区間構造・留保」
- **根拠ログ**: `2026-11-10-a2647-113-full-sweep-100k-result.md`(本文)、
  `2026-11-10-a2647-113-tail-unsat-verification-omp.md` §1(区間の統計)

### 案2: K0714(仮) 候補B(assumption 掃引)の分割正当性

- **対象**: 新規 K0714
- **kind / status**: `proposition` / `proved`
- **title**: 形状クラスCNFのモデル集合は完全対の仮定 B_d で互いに素に分割され、全 d の UNSAT はクラス UNSAT と同値
- **主張文**:
  「c=1 のクラス CNF は `#B = 1` と両立禁止節 `[-B_i,-B_j]` を持ち、任意のモデルで真となる
  B 変数はちょうど 1 つ存在する。したがってモデル集合は `M_d = {M ⊨ CNF : B_d}` により
  `M_1,…,M_h` へ互いに素に分割され、`CNF = ⋁_d (CNF ∧ B_d)`。よって決定的な
  (UNKNOWN を返さない)ソルバ呼び出しの下で、`すべての d∈{1..h} で CNF ∧ B_d が UNSAT`
  ⇔ `CNF が UNSAT`。健全性は assumption が一時的な単位節追加にすぎないことから従い、
  SAT 側の主張は復号した点集合を生成済み全 928,389 辺と直接照合する自己検証を持つ
  (符号化の健全性に依存しない)。c=0 では分割が空になり、掃引は `assumptions=[]` の
  1 クエリ = クラスCNF そのもの。UNKNOWN が 1 つでも残る d 範囲については何も主張しない。」
- **status 根拠**: 論理(暗号化定義からの導出)であり、前提(1)(3) は K0716/K0717 で
  証明・範囲限定検証済みになった。**前提(4)(ソルバ健全性)は論理命題の一部ではない**ため
  `proved` を妨げないが、**応用(掃引の UNSAT からクラス UNSAT を出す段)は依然
  assumption-UNSAT に依存する**。この切り分けを本文に明記する。
- **関係/帰属の注意**:
  - W10 §1.3 冒頭の「⇔」は偽(和0 の四点は禁止四点より真に多い。p=17 で 140 対 30、
    p=43 で 2870 対 239)。**本項では ⇒ としてのみ述べる**(W12 4.2 注記2)。
  - 前提(2)の「K0334 の同一性」という帰属は不正確(W12 1.2: K0334 本文に行列式の因数分解は
    無い)。本項は K0715/K0716 を根拠にし、K0334 の同一性には言及しない。
- **relation**: `depends_on: K0712`(固定原点・一完全対の還元)、`depends_on: K0716`(辺リスト完全性)、
  `depends_on: K0715`(捨て規則(ii) の和条件)、`depends_on: K0717`(基数符号化、範囲限定)、
  `depends_on: K0720`(前提(4) の未解決ギャップ)。
- **artifacts**:
  - `research/log/2026-11-10-a2647-113-candidate-b-proof-omp.md` / `proof` /
    「第1部の分割・健全性・完全性の証明と §1.7 の前提一覧」
  - `…/search_shape_class_assump.py` / `solver` /
    「assumption 掃引の実装(SAT 側は復号点を全 928,389 辺と照合)」
  - `…/search_shape_class.py` / `solver` /
    「`#B = c` の cardinality 制約と対ごと exactly-one の本体」
  - `…/output/w7-assump-2647-1322-full100k.json` / `data` / 「分割の適用記録(1,323 d)」。
- **根拠ログ**: `2026-11-10-a2647-113-candidate-b-proof-omp.md` 第1部。
- **注意**: 本項は W10 の log を proof artifact にしてよいか、が論点。W10 は log であって
  形式証明ではないので、`role: proof` は「証明の記述」の意。Lean 形式化ではない旨を本文に書く。

### 案3: K0715(仮) 剰余放物線の四点行列式の因数分解と共円判定

- **対象**: 新規 K0715
- **kind / status**: `proposition` / `proved`
- **title**: 剰余放物線の四点行列式は −(パラメータ和)×Vandermonde 積に合同で、det=0 は共円・共線と同値
- **主張文**:
  「`Q_p={(t,t² mod p)}` の相異なる四点 `q={t_1,…,t_4} ⊂ {0,…,p−1}` について:
  (i) 共円・共線判定の 4×4 巡回行列式 `D_cyc = det[x_k²+y_k², x_k, y_k, 1]` は、第4点で
  平行移動した 3×3 形 `D_enc = det[Δx_k, Δy_k, Δn_k]`(k=1..3、`forbidden_edges.cpp:7-16` の `det()`)
  に可換環上の恒等式として一致する(補題A)。
  (ii) パラメータ行列式 `D = det[t_i^{d_j}]`、`(d_1..d_4)=(0,1,2,4)` について、Z[t_1..t_4] 上で
  `D = (Σt_i)·V`、`V = ∏_{i<j}(t_j−t_i)`(定理B、整数多項式の恒等式)。
  (iii) したがって mod p で `D_cyc(q) ≡ −(Σt_i)·V (mod p)`(系C)。
  `D_cyc=0 ⟺ 四点が同一円または同一直線上`(系A1、整数)であり、`V ≢ 0 (mod p)` なので
  `D_cyc≡0 ⟹ Σt ≡ 0 (mod p)`(系C1)。**逆は偽**(p=17 で和0 の四点 140 組に対し禁止四点 30 組、
  p=43 で 2870 対 239)。系として、完全対を含む禁止四点は二完全対(系D、一般証明)、
  二完全対は必ず禁止で台形辺の総数は `C(h,2)`(系E。逆向きは p=17/29/43 の全対で
  「禁否でない」0 件)、完全対を含まない辺は {0,a,b,c} 型に限られ第四点が一意(系F)。」
- **status 根拠**: 補題A と定理B は可換環上の基本変形と Z[t] の UFD 性のみを使う全称証明。
  §3 の有限体全数検査(p=17,29,43,97 の全四点で系C 違反 0、p=17/29/43 の全対で系E 逆 0 件)と
  p=2647 の会計(928,389 = C(1323,2)=874,503 + 53,886、0 を含む辺 4)は独立実装による確認。
- **relation**: `supports: K0334`(K0334 文3 の t³ 係数ルートとは独立な第2証明を与え、
  等号分解の前提を裏づける)、`supports: K0714`(捨て規則の和条件)、`depends_on: K0334` は付けない
  (K0334 に依存しない)。逆に K0334 から `supports` を受ける形が自然か要検討。
- **artifacts**: `research/experiments/frontier-geometry-2026-10-05/forbidden_edges.cpp` / `verifier` /
  「det() の 3×3 実装(補題A の対象)」、`research/experiments/frontier-geometry-2026-10-05/proof.md` /
  `proof` / 「K0334 側の全称証明(本項とは独立ルート)」、
  `research/log/2026-11-10-k0334-identity-verification-omp.md` / `log` / 「定理B・系C/D/E/F と
  p=2647 の会計」。
- **限界**: 証明スクリプト `/tmp/k0334/check3.py`, `check101.py`, `crosscheck_edges.py` は
  repo 外で、artifact にできない。再現には repo 内実装(`forbidden_edges.cpp`)との突合のみ可能。
  p=503 の突合は原典でも未回収。
- **矛盾**: なし。K0334 の status(proved)は変更不要(W12 §4.1)。

### 案4: K0716(仮) 禁止四点の構造と生成器の列挙完全性

- **対象**: 新規 K0716
- **kind / status**: `proposition` / `proved`(W10 前提(1) の格上げ)
- **title**: 剰余放物線の禁止四点の列挙アルゴリズムは健全・完全・重複なしで、辺リストは過不足がない
- **主張文**:
  「`forbidden_edges.cpp` は `i<j<k` を全走査し `l = (−(i+j+k)) mod p` を取って `l>k` かつ
  `det({i,j,k,l})=0` の行だけを出力する。この出力集合は全禁止四点集合に一致する:
  (i) 健全性は出力条件 `det==0` と K0715 の同値性から、(ii) 完全性は禁止四点なら
  `Σt≡0` より `t_4 ≡ −(t_1+t_2+t_3)` で `l` の計算値が `t_4` に一致し `l>k` を満たすことから、
  (iii) 重複なしは他の三つ組から得られる `l` が常に `k` より小さいことから、(iv) 計算の完全性は
  `__int128_t` 評価と入力検査 `p<=100000` から。よって p=2647 の 928,389 辺は過不足なく、
  うち台形辺 `C(1323,2)=874,503`、残余 53,886(0 を含む辺 4)で、W10 の `kept_edges=53,886` と一致する。」
- **status 根拠**: 列挙アルゴリズムの論理は W12 4.3 で閉じる。**残るのは実行の真正性**
  (走らせたバイナリがソースと同一か、`edges2647.txt` の行数記録の真正性、p=2647 の独立再列挙を
  していないことの3点)。これは数学的欠落ではなく信頼境界なので本文に明記し、status は `proved`。
- **relation**: `depends_on: K0715`(系C1 の必要方向と第四点の一意性)、`supports: K0714`(前提(1))。
- **artifacts**: `research/experiments/frontier-geometry-2026-10-05/forbidden_edges.cpp` / `verifier` /
  「列挙本体(i<j<k と l の一意化)」、`research/log/2026-11-10-k0334-identity-verification-omp.md` /
  `log` / 「4.3 の 1-4 と p=2647 実走の会計」。
- **矛盾**: なし。ただし W12 が「W10 前提(1) は証明済みへ格上げできる」と言うとき、
  **証明されるのはアルゴリズムの論理であって実行記録ではない**。本項の本文でこの区別を保持する。

### 案5: K0717(仮) pysat seqcounter `equals` の小規模全件検証

- **対象**: 新規 K0717
- **kind / status**: `verification` / `verified`(**範囲限定を本文と scope に明記**)
- **title**: pysat の seqcounter による CardEnc.equals は build と同一の呼び出し形で小規模全件「ちょうど bound 個」を満たす
- **主張文**:
  「`search_shape_class.build()` と同一の呼び出し形(`CardEnc.equals(..., encoding=EncType.seqcounter)`、
  `top_id` 連鎖、`aux = card_n.nv`)のもとで、pysat 1.9.dev21 の `equals` は
  単体 `n<=12`・連鎖 `n<=7` の**全主割当**について「CNF が補助変数へ拡張可能 ⟺ 主変数上で
  ちょうど bound 個」を満たした(473 ケース、1,588,640 割当、**不一致 0**、SAT 側 46,414 件と
  UNSAT 側 1,542,226 件の両方向で一致)。補助変数が主変数以下に落ちる件数 `aux_alias_main` と
  `.nv` を超えるリテラル `lit_above_nv` はいずれも全 473 ケースで 0。対象は `equals`+`seqcounter` のみ。」
- **status 根拠/限界**:
  - 有限個の全件照合であり、**一般 n の証明ではない**。実用は `h=1323` で、検証済み `n=12` からの
    外挿は「同じコード経路が一様に動く」という仮定に立つ([INFERENCE])。
  - **負の対照(検出力)の証拠が保存 JSON に無い**(`negative_control` キー不在)。したがって
    「0 件」は符号化の正しさの証拠であっても、ハーネスが誤りを検出できることの証拠を欠く。
    厳格に読むなら `needs-review` も選び得るが、**照合の真値は主割当の列挙から独立に計算されており、
    2系統の完全判定器で両方向一致している**ため、本ドラフトは `verified` + 明示的な限界記述を採る。
    統合時の判断材料として両案を併記する。
  - 前提(4)(ソルバ健全性)には触れない。
- **relation**: `supports: K0714`(前提(3) の範囲限定格上げ)。K0712 との関係は**付けない**
  (K0712 の regression は 444 cardinality ケースで、本項の 473 ケースとは別ハーネス。
  包含関係は未確認)。
- **artifacts**: `…/cardenc_verify.py` / `verifier` / 「全主割当の拡張可能性を DPLL で判定する
  照合器」、`…/output/w15-cardenc-verify.json` / `data` / 「473 ケース・1,588,640 割当・
  不一致 0・構造不変量 0(negative_control は未保存)」、
  `…/search_shape_class.py` / `solver` / 「照合対象の build() 呼び出し形(:50-53)」。
- **根拠ログ**: `2026-11-10-cardenc-verification-omp.md` 第2部・§3.1・§3.3・§3.4。

### 案6: K0718(仮) 易 UNSAT の履歴非依存性とソルバ横断再現

- **対象**: 新規 K0718
- **kind / status**: `verification` / `verified`(**d ごとの範囲を明記**)
- **title**: 候補B の易 UNSAT は学習節の履歴に依存せず、ソルバ横断でも d に応じた範囲で再現する
- **主張文**:
  「p=2647・size=1322・クラス (1,1,3) の候補B において、
  (a) **履歴非依存**: 履歴ゼロの新規 Cadical195(fresh-each)で再解すると、
  掃引で UNSAT だった 9 点(d=1,300,478,851 / 1280,1290,1300,1310,1316)はすべて UNSAT、
  掃引で UNKNOWN だった 3 点(1317,1322,1200)は UNKNOWN で、conflict 予算 100k を使い切る。
  別途、単一インスタンスを降順 `[1322,1000,851,500,478,300,100,1]` で回す shared-reverse でも
  UNSAT は 1/300/478/851、UNKNOWN は 100/500/1000/1322 で記録と一致する
  (この mode は「履歴を逆から積む」検査であり、履歴ゼロの検査ではない)。
  `unit_conflict` は全点 false で、「即 UNSAT」は伝播閉包ではなく 565〜33,464 conflicts の
  探索による(1280-1310 は 10³ 級、1316 は 3.3×10⁴)。
  (b) **ソルバ横断**: d=1/300/478 は 14 種中 13 種が UNSAT(Cadical195 を除いて 12 種、
  MapleChrono のみ timeout)。d=1280/1300 は 14 種中 13 種 UNSAT(除く 1 種は MapleChrono)。
  d=1316 は 14 種中 **9 種 UNSAT / 5 種 timeout**(240 秒壁時計、予算未到達)。d=851 は
  試行 7 種中 4 種 UNSAT。d=1317 は 14/14 が timeout(120 秒、予算未到達)。
  d=100 は 5 種すべて UNKNOWN か timeout。」
- **status 根拠/限界**:
  - 全モードが**同一のクラス CNF**(候補B、`w14-cnf-cache.pkl` / `search_shape_class.build(2647, edges, 1, 1, 3)`)、
    同一の conflict 予算(100k)。ただし**壁時計 cap は d ごとに違う**(W14 は 120 秒、
    W18 は 1280/1300/1317 が 120 秒・1316 が 240 秒、W19 は 1316 が 240 秒)。
    したがって排除できたのは「学習節の履歴依存」と「Cadical195 固有性(d に応じた範囲で)」であり、
    **符号化の同一性と外部バイナリの未検証は残る**。
  - 「ソルバ非依存」は d について一様でない(1316 は 9/14、851 は 4/7)。本項は**数表を伴う
    範囲限定の主張**として書く。タスク指示の要約「残る留保は同一符号化のみ」は d=1/300/478
    については正確だが、851/1316 には当てはまらない。§6 に記録。
  - W18 の timeout は壁時計打ち切りで、UNSAT と数えない。W17 の UNKNOWN は conflict 予算切れ。
    この2種を混同しない。
- **relation**: `verifies: K0714`(候補B 分割の適用)、`depends_on: K0713`(掃引記録)、
  `depends_on: K0717`(同一符号化の基数制約)。
- **artifacts**:
  - `…/reverse_order_probe.py` / `verifier` / 「逆順と fresh-each の再解器」
  - `…/output/w11-artifact-reverse.json`(8 レコード) / `data` / 「逆順 8 点の判定」
  - `…/output/w11-artifact-fresh.json`(4 レコード) / `data` / 「履歴ゼロ 4 点の判定」
  - `…/tail_fresh_probe.py` / `verifier` / 「尾部 fresh-each と unit_conflict/統計の計測」
  - `…/output/w17-tail-fresh.json`(8 レコード) / `data` / 「尾部 5 点 UNSAT・境界 3 点 UNKNOWN」
  - `…/cross_solver_probe.py` / `verifier` / 「交差ソルバ実行器」
  - `…/output/w14-cross-solver.json`(54) / `data` / 「d=1/100/300/478/851 のソルバ表」
  - `…/output/w18-tail-cross-solver.json`(47) / `data` / 「d=1280/1300/1316/1317」
  - `…/output/w19-1316-cross-rest.json`(9) / `data` / 「d=1316 の残り 9 種」
- **根拠ログ**: `2026-11-10-a2647-113-artifact-test-omp.md`(W11)、
  `2026-11-10-a2647-113-tail-unsat-verification-omp.md`(W17)、
  `2026-11-10-a2647-113-cross-solver-omp.md`(W14)、
  `2026-11-10-a2647-113-tail-cross-solver-omp.md`(W18 + W19)。
- **分割の是非**: 「履歴非依存」と「ソルバ横断」は証拠集合が別なので 2 項目に割る案もある。
  AGENTS の「1 実験 1 K を作らない」に照らし、本ドラフトは**1 項目 + 明示的な per-d 表**を推す。

### 案7: K0719(仮) ternary 符号化の任意 d 一般化と実装検証

- **対象**: 新規 K0719
- **kind / status**: `verification` / `verified`
- **title**: ternary 符号化の d 一般化実装は d=1323 で現行と同一の CNF・同一探索を再現し、任意 d で節生成が健全
- **主張文**:
  「`ternary_general.py` は d を引数化して固定完全対 d の三値符号化を生成する。
  (i) d=1323・target=1322 では、生成した base 節集合は**節内を (abs,lit) 順・節を辞書順に
  正規化した後で**保存 CNF の 53,886 節と一致し(base SHA `0f09fc6e…2ff0b3`)、
  生成 CNF(7,926 変数 / 68,404 節)は既存 `input.cnf.gz` と **gz バイト列まで一致**
  (`encoded_cnf_sha256 = 8cbd404a…b9f48a`)。100k 予算の探索統計は既存実績と完全一致
  (conflicts 100,001 / decisions 217,401 / propagations 50,404,659 / restarts 4,854、UNKNOWN)。
  (ii) `edge` リストの d 非依存性は、p=5,7,11,13,17 の全 d・全三値割当 19,392 件で
  `clauses_for_pair(full)` と `clauses_for_pair(kept)` の評価、および整数幾何の禁止四点判定が
  全一致(不一致 0)。kept ⊆ full で、差分 874,503 はすべて同一 pair の2点を含む台形辺。
  (iii) d=300 では 19,392 割当の照合に加え、target=1322 が **SOLVER_UNSAT**
  (1.811 秒、conflicts 1,808、予算未満 = 打ち切りでない反駁。Glucose4 と Minisat22 で独立に UNSAT)、
  target=1293 が UNKNOWN(90.207 秒、142,992 節 / 45,249 変数)。SAT 経路は p=17 の全 d・全 target
  64 件でモデル再構成と整数幾何安全性を確認。CLI は d∈[1,1323]、target∈[3,1325] を検証し、
  既存出力を上書きしない。既存 regression(19,392 割当・444 cardinality ケース)も全項目一致。」
- **status 根拠/限界**:
  - これは**実装の検証**であり、符号化の数学的正当性は K0712 の全称証明が担う。
  - d=300/target=1322 の UNSAT は「±300 を含む 1322 点安全集合が存在しない」であって、
    Q_2647 全体の UNSAT ではない。かつ DRAT 監査前の `SOLVER_UNSAT`。
  - 難易度の d 依存(1323 は UNKNOWN、300 は 1.8k conflicts)は実測事実で、機構の説明ではない。
- **relation**: `verifies: K0712`、`generalizes: K0712`(空対 0 の等号集合から任意 d へ)、
  `supports: K0713`(候補A/三元系の一般化が次の測定の前提になる)。
- **artifacts**: `research/experiments/parabola-ternary-selection-20261109/ternary_general.py` /
  `solver` / 「d を引数化した三値符号化の生成器」、
  `…/output/generalization-check-d1323-target1322-budget100000/{init,result}.json` / `data` /
  「base 53,886 節一致・統計完全一致・UNKNOWN」、
  `…/generalization-check-d300-target1322-budget100000/{init,result}.json` / `data` /
  「SOLVER_UNSAT 1.811 s / 1,808 conflicts」、
  `…/generalization-check-d300-target1293-budget100000/{init,result}.json` / `data` /
  「UNKNOWN 90.207 s / 142,992 節」。
- **根拠ログ**: `2026-11-10-ternary-generalization-omp.md` §4・§5・§9。
- **注意**: 原典 §9.3 の d=300「1.70 s / 2,795 conflicts」は §4.3 の JSON 実値
  (1.811 s / 1,808 conflicts)と食い違う。**本項の主張文は JSON 実値を引用**する。

### 案8(任意): K0720(仮) assumption-UNSAT の監査可能性ギャップ

- **対象**: 新規 K0720
- **kind / status**: `question` / `open`
- **title**: 候補B の assumption-UNSAT を単体の DRAT 証明へ落とす手続きは未取得である
- **主張文(問いの形)**:
  「`solve_limited(assumptions=[B_d])` の UNSAT は `${CNF ∧ B_d}` の UNSAT を意味するが、
  現行の掃引記録は assumption を単位節として書き出していないため、単体の DRAT 証明に対応しない。
  d 固定 CNF(または B_d を加えた CNF)を書き出して DRAT を取り、修正版検証器
  (K0707 の削除時代入失効)で検査する手続きを、(1,1,3) の 1,256 UNKNOWN を増やさずに
  適用できるか。候補A 方式と候補B 方式の費用対効果は未測定。」
- **status 根拠**: W10 §1.7 前提(4)・§2.1 が「未取得」と明記。W22 時点で新しい計算は無い。
- **relation**: `depends_on: K0714`(前提(4) の所在)、`depends_on: K0706`(DRAT 監査の実施例)。
- **artifacts**: `research/log/2026-11-10-a2647-113-candidate-b-proof-omp.md` / `log` /
  「第2部の証明書計画(候補A: d 固定 CNF + DRAT)」、
  `research/log/2026-11-10-a2647-113-hardcore-attack-plan-omp.md` / `log` /
  「候補A 予算ラダーの計画」。
- **任意とした理由**: 本日分の「確定した結果」ではない。ただし (1,1,3) の未決着と
  候補B の監査可能性を結びつける唯一の項目なので、掃引完走を受けて作る価値がある。

## 4. 既存項目の更新案

### 更新案1: K0706「現在の範囲」の上界表記(要整理。ただし矛盾ではない)

- **対象**: 既存 K0706
- **現状**: 本文「限界」節に「現在の範囲は1296<=A(2647)<=1324」とある(根拠は K0711 の
  1296 点証人 + K0706 自身の DRAT 全件監査による ≤1324)。
- **問題**: `1296<=A<=1324` は**真だが最良でない**。K0711 は 1322 上界を持つ
  (サイズ1323 の全4形状クラス UNSAT、ソルバ主張)。K0706 の文は「現在の範囲」と
  書く以上、最良既知の上下界を示すべきで、DRAT 監査済み上界と最良既知上界を
  区別せず 1324 だけ書くのは読み手を誤らせる。**論理的矛盾ではない**(1322 ⇒ 1324)。
- **更新案(主張の強さは変えない)**:
  「現在の最良の範囲は **1296 ≤ A(2647) ≤ 1322**(上界 1322 はサイズ1323 の全4形状クラス
  UNSAT・サイズ1324 の形状 (b) UNSAT による**ソルバ主張**)。**DRAT 監査済みの上界は 1324**
  (全1323 d の receipts、1323/1323 VERIFIED)で、1322 側は DRAT 監査前。」
- **status**: `computed` のまま変更なし(監査済みの主張は A≤1324 のまま)。
- **根拠**: K0711 の scope/evidence、`2026-11-09-a2647-size1323-receipts-regenerated.md`。
- **注意**: 本 log は knowledge を編集しない。統合時に本文1文の置換として実施する(§6 にも記載)。

### 更新案2: K0711 への artifact 追加(主張は不変)

- **対象**: 既存 K0711
- **案**: `w7-assump-2647-1322-full100k.json` を `data` として追加し、note を
  「サイズ1322・クラス (1,1,3) の 100k/d 掃引(67 UNSAT / 1,256 UNKNOWN / 0 SAT)。
  **上界・下界の根拠ではなく**、クラスが未決着であることの記録」とする。
- **更新しないもの**: title、scope、evidence、status(`computed`)。掃引は範囲を動かさない。
- **理由**: 掃引を K0711 に混ぜると「上界の根拠」と誤読される危険があるため、
  note で明示的に非根拠と書く。あるいは K0713 のみに置き、K0711 に artifact を足さない選択も可
  (本ドラフトは**追加しない方**を推す。K0713 から `supports` を張るだけで足りる)。
- **推奨**: 追加しない。関係のみ(逆方向の参照は生成側が張る)。

### 更新案3: K0712 への artifact 追加と実装上の注記(主張は不変)

- **対象**: 既存 K0712
- **案**:
  - artifact 追加: `research/experiments/parabola-ternary-selection-20261109/ternary_general.py` /
    `solver` / 「d を引数化した同符号化の生成器(保存 CNF は d=1323 専用なので必ず再生成する)」。
  - 本文「実装検査と使用範囲」に 1 文追加:
    「保存 CNF(`target1322-budget3000000/input.cnf.gz`)は **d=1323 でフィルタ済み**の産物であり、
    別 d では `clauses_for_pair` による再生成が必要。一般 d の生成器と d=1323 での
    バイト一致は 2026-11-10 に検証済み(K0719)。」
- **status**: `proved` のまま変更なし。scope も変更なし。
- **根拠**: W16 §3・§4.1、`ternary_general.py`。

### 更新案4: K0334 への言及(変更不要)

- **対象**: 既存 K0334
- **判断**: **status 変更なし、本文への同一性の追記も不要**(W12 §4.1)。
  K0334 文3 の t³ 係数による議論は (P5) として独立に成立しており、行列式の因数分解は
  新規項目 K0715 側に置く。K0334 と K0715 は `supports`(K0715 → K0334)で結ぶのが適切。
- **付随する文書作業**: W10 §1.7 前提(2) の「K0334 の同一性」という帰属は不正確。
  W10 は log(一次資料)なので書き換えない。統合時に W10 を引用する側が
  「K0715 で証明した合同式」と読み替える。§6 に記録。

## 5. 前提(1)-(4) の現状対応表(W10 §1.7)

| 前提 | 内容 | 本日分の結果 | 対応する草案項目 | 扱い |
|---|---|---|---|---|
| (1) | 辺リストの完全性(生成器の過不足なし) | 列挙アルゴリズムの論理が閉じた。残るのはバイナリ/記録の真正性 | K0716 | 証明済み → `proved` |
| (2) | 台形辺捨ての和条件(行列式 = Vandermonde積 × 和) | 因数分解と det=0 同値性を証明。p=17/29/43/97 全数 + p=2647 会計 | K0715 | 証明済み → `proved` |
| (3) | pysat `CardEnc.equals`(seqcounter)の健全性・完全性 | 単体 n<=12・連鎖 n<=7 の全主割当で不一致 0。一般 n は未証明 | K0717 | 範囲限定で `verified` |
| (4) | CaDiCaL の UNSAT 報告と assumption semantics | 未解決。DRAT 化の手続き未取得 | K0720(任意) | `open` |

これにより W10 第1部の定理は、**符号化側の前提が (3) の外挿のみ**、**ソルバ側の前提が (4)** という形に整理される。
「(1)(2) が証明で閉じた」というタスク要約はこの意味で正確。

## 6. 矛盾・要訂正・留保の一覧(統合時に必ず確認)

1. **W18 結論1 の数え方**: 「Cadical195 を除く 13 種」と書くが列挙は 12 名。
   JSON 実読では d=1280/1300 の UNSAT は 13 件(Cadical 含む)、timeout 1 件。
   正しくは「14 種中 13 種 UNSAT、Cadical を除いて 12 種」。**K0718 の主張文は後者**。
2. **W16 §9.3 の d=300 数値**: 「1.70 s / 2,795 conflicts」に対し §4.3 の
   `generalization-check-d300-target1322-budget100000/result.json` は
   「1.811 s / 1,808 conflicts」。2,795 を持つ JSON は output 配下に無く、
   `ladder-d300-*` ディレクトリも存在しない(§9.3 の掃引は d=188/194/602 の
   `ladder-*` と同系列だが `ladder-d300` の結果は保存されていない)。
   **K0719 は §4.3 の JSON 実値を引用**。
3. **W15 の負の対照**: 原典 §2.3 は「JSON に記録」とするが、保存 JSON に
   `negative_control` キーは無い(原典 §3.3 が自ら訂正済み)。**K0717 は「証拠なし」と明記**。
4. **K0706 本文の上限 1324 vs K0711 の 1322**: §4 更新案1。K0706 の status は変えず、
   本文の「現在の範囲」だけを 1322(ソルバ主張)+ 1324(DRAT 監査済み)に整理する。
5. **W10 §1.3 の「⇔」**: 和0 の四点 ⊋ 禁止四点(反例: p=17 で 140 対 30、p=43 で 2870 対 239)。
   **K0714 は ⇒ としてのみ述べ、⇔ を書かない**。W10 本文は log なので書き換えない。
6. **W10 §1.7 前提(2) の帰属**: 「K0334 の同一性」は K0334 本文に無い。K0715 に独立項目として置く。
7. **タスク要約の「残る留保は同一符号化のみ」**: d=1/300/478 については正確だが、
   d=851 は 7 種中 4 種、d=1316 は 14 種中 9 種しか UNSAT でない。また外部バイナリ
   (DIMACS 経由)は未実施。**K0718 は per-d 表を伴う範囲限定の主張**にする。
8. **掃引 JSON の `seconds` は履歴込み**: 独立再解の時間ではない(K0713 の限界に明記)。
   例: d=1316 は掃引 4.319 秒 / fresh-each 20.853 秒 / W18 Cadical195 49.214 秒。
9. **掃引の 1,256 UNKNOWN は「未決着」**: クラス (1,1,3) も A(2647) の範囲も動かない。
   1296 ≤ A ≤ 1322(ソルバ主張)、DRAT 監査済み上界 1324 のまま。
10. **p=503 の会計突合が未回収**(W12 §4.5 ギャップ1)。K0715/K0716 の本文に
    「会計は p=17, 29, 43, 97, 101, 2647 で一致、p=503 は未回収」と書く。

## 7. 再採番と統合の手順(AGENTS 準拠)

1. main の最新 K 番号を確認し、K0713..K0720(仮)と衝突する新規項目を機械的に再採番する。
2. 再採番した項目を参照する `relations.target` と Markdown リンクを同時に更新する。
3. `uv sync --locked` / `check.py` / `unittest` / `build.py` /
   `git diff --exit-code -- README.md research/knowledge/generated` を実行する。
4. 生成物(generated, root README)は手で編集しない。

## 8. 未実施(本 log の範囲外)

- knowledge 項目ファイルの作成・編集(指示により禁止)。
- 新しい計算(掃引の再実行、DRAT 取得、CardEnc の負の対照再実行、p=503 の突合)。
- 原典 log の訂正(W10/W16/W18 は一次資料として保持)。

(完)
