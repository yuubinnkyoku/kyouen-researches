# W18: 掃引尾部 UNSAT の交差ソルバ検証（p=2647, size=1322, 形状 (1,1,3), 候補B）

- 日付: 2026-11-10
- 対象: p=2647, size=1322, 形状クラス (x,c,e)=(1,1,3)、候補B（assumption `B_d`）、
  d ∈ {1280, 1300, 1316, 1317}
- 元の問い: W17 `research/log/2026-11-10-a2647-113-tail-unsat-verification-omp.md` §結論5
  「交差ソルバでの尾部確認は未実施（W14 は d∈{1,100,300,478,851} のみ）」。
  W17 は履歴（学習節）依存を排除したが、排除していないのは
  「この符号化＋Cadical195 の組合せに固有の易しさ」である。
- 本タスクの変数: **ソルバのみ**。符号化はW14/W17と同一（`w14-cnf-cache.pkl`）。
- 新規計算は行っていない。本ログは既存の結果 JSON の実読と、W14/W17 との対照のみ。

## 方法

### スクリプトと出力（W14 と同一の流儀）

- スクリプト: `research/experiments/parabola-p2207-no-equality-witness-20261107/cross_solver_probe.py`
  （W14 と同一ファイル。d とソルバ集合を差し替えて実行）
- 出力: `research/experiments/parabola-p2207-no-equality-witness-20261107/output/w18-tail-cross-solver.json`
  （47 レコード。掃引 JSON `w7-assump-2647-1322-full100k.json` へは書き込んでいない）
- 対象 d: 尾部内 {1280, 1300, 1316}、境界 {1317}。d=1317 は掃引・W17 ともに UNKNOWN の点。

### 符号化と予算・上限（JSON の実読値）

JSON のヘッダは次の値を記録している（`cross_solver_probe.py` の
`--device` / `--deadline` / `--jobs` / `--caps` に対応する値）:

| 項目 | 値 |
|---|---|
| p / size / class | 2647 / 1322 / [1,1,3] |
| budget（conflicts） | 100,000 |
| vars / clauses / kept_edges | 17,180 / 90,891 / 53,886 |
| build_seconds / build_source | 1.7 / `cached:output/w14-cnf-cache.pkl` |
| device_timeout | 240.0 秒 |
| caps | `1280:120,1300:120,1316:240,1317:120` |
| deadline（全体） | 2,400.0 秒 |
| jobs | 4 |
| solvers | 14 種 |

実効上限は W14 と同じく `min(device, cap(d), 残余deadline)`。したがって d=1280/1300/1317 は
120 秒、d=1316 のみ 240 秒が上限。1 クエリ = 1 サブプロセス、
`conf_budget(100000)` + `solve_limited(assumptions=[B_d])`。
**Kissat404 だけは assumption 非対応のため `setup: unit-B_d`（`B_d` を単位節で追加）**、
他の 13 種は `setup: assumption-B_d`。この差は W14 と同じ。

記録形式の差: `verdict: "unsat"` の行は `sat:false, unknown:false` と `seconds` /
`build_seconds` を持つ。`verdict: "timeout"` の行は `setup` / `sat` / `unknown` /
`build_seconds` を持たず、`seconds: 120.0` と
`reason: "wall cap 120s (conflict budget 100000 not reached)"` のみを持つ
（親側の壁時計でサブプロセスを打ち切った記録）。timeout は **UNSAT と数えない**。

### d ごとの試行数（実読で数えた値）

| d | レコード数 | 内訳 |
|---:|---:|---|
| 1280 | 14 | unsat 13 + timeout 1 |
| 1300 | 14 | unsat 13 + timeout 1 |
| 1316 | **5** | unsat 5 |
| 1317 | 14 | timeout 14 |
| 合計 | 47 | unsat 31 + timeout 16 |

**d=1316 は 5 ソルバ分しかレコードが無い**（14 − 5 = 9 種は未実行、記録なし）。
理由（残余 deadline 到達か別途停止か）は JSON から判別できない。したがって 1316 について
「14 種で UNSAT」とは書けない。

## 結果: d × ソルバ判定表（`w18-tail-cross-solver.json` の実読値のみ）

`timeout` は 120 秒の壁時計打ち切り（conflict 予算 100k 未到達）。
「—（未実行）」はレコードが存在しないもの。

| ソルバ | setup | d=1280 (p−2d=87) | d=1300 (47) | d=1316 (15) | d=1317 (13) |
|---|---|---|---|---|---|
| Cadical195（参照） | assumption | UNSAT 5.924s | UNSAT 4.016s | UNSAT 49.214s | timeout 120s |
| Ergo | assumption | UNSAT 5.346s | UNSAT 3.804s | UNSAT 25.011s | timeout 120s |
| MinisatGH | assumption | UNSAT 5.251s | UNSAT 3.177s | UNSAT 43.313s | timeout 120s |
| Minisat22 | assumption | UNSAT 5.934s | UNSAT 1.675s | UNSAT 120.779s | timeout 120s |
| Maplesat | assumption | UNSAT 5.098s | UNSAT 3.195s | —（未実行） | timeout 120s |
| MapleCM | assumption | UNSAT 8.612s | UNSAT 11.881s | —（未実行） | timeout 120s |
| MapleChrono | assumption | **timeout 120s** | **timeout 120s** | —（未実行） | timeout 120s |
| Glucose3 | assumption | UNSAT 7.594s | UNSAT 3.212s | —（未実行） | timeout 120s |
| Glucose4 | assumption | UNSAT 6.401s | UNSAT 3.504s | —（未実行） | timeout 120s |
| Glucose42 | assumption | UNSAT 7.383s | UNSAT 3.219s | —（未実行） | timeout 120s |
| Gluecard3 | assumption | UNSAT 4.401s | UNSAT 3.214s | —（未実行） | timeout 120s |
| Gluecard4 | assumption | UNSAT 4.096s | UNSAT 3.197s | —（未実行） | timeout 120s |
| Mergesat3 | assumption | UNSAT 2.226s | UNSAT 3.499s | —（未実行） | timeout 120s |
| Kissat404 | **unit** | UNSAT 13.402s | UNSAT 8.584s | UNSAT 116.508s | timeout 120s |

`build_seconds`（サブプロセス内の CNF bootstrap）は 0.103〜0.721 秒、
`seconds` は `solve_limited` 区間のみで、W14 の表と同様にプロセス起動・cache 読込を含まない。

読み取り:

- **d=1280 と 1300 は 13 種が UNSAT、timeout は MapleChrono の 1 種のみ。**
  この 2 点では UNSAT が極端に安く（1.675〜13.402 秒、1316 の 1/3 以下）、
  試したソルバの優劣にほとんど依らない。MapleChrono は W14 の d=1 でも 90 秒で
  時間切れしており（`w14-cross-solver.json`）、この 2 点の timeout を尾部の硬さの
  証拠には使わない。
- **d=1316 は 5/5 UNSAT だが、試行は 5 種のみ。** 費用は 25.011〜120.779 秒で、
  全ソルバが 1280/1300 の 4〜20 倍を要した（Minisat22 は cap 240 秒の半分 120.779 秒）。
  未実行 9 種があるため「14 種で UNSAT」とは書けない。
- **d=1317 は 14/14 が timeout。** しかも `reason` はすべて
  「100k conflicts 未到達のまま 120 秒の壁時計」であり、予算切れの UNKNOWN ではない。
  1316 と 1317 の間に、少なくとも「120 秒で 100k conflicts に届くか」を跨ぐ段差がある。

## W17（fresh-each, Cadical195）との対照

W17 は d ごとに履歴ゼロの新規 Cadical195 で解いた。W18 の Cadical195 行は
同じ 1 クエリ=1 新規インスタンスだが、jobs=4 の並列実行下で壁時計を測っている。

| d | W17 判定 | W17 seconds | W17 conflicts | W18 Cadical195 判定 | W18 seconds |
|---:|---|---:|---:|---|---:|
| 1280 | UNSAT | 0.104 | 661 | UNSAT | 5.924 |
| 1300 | UNSAT | 0.176 | 693 | UNSAT | 4.016 |
| 1316 | UNSAT | 20.853 | 33,464 | UNSAT | 49.214 |
| 1317 | UNKNOWN | 55.101 | 100,004 | timeout（120s, 予算未到達） | 120.0 |

- **判定は 4/4 で一致**（1280/1300/1316 = UNSAT、1317 = UNKNOWN）。
- 秒数は一致しない。W18 は d あたり 14 クエリを jobs=4 で走らせており、
  親が測る壁時計は CPU 共有の影響を受ける。加えて W17 の `seconds` は
  `solve_limited` 区間、W18 の timeout は親側の壁時計打ち切りである。
  したがって 1280 の 0.104 秒対 5.924 秒を「ソルバ差」として読まない。
- **1317 の質的な差は予算到達の有無**: W17 は 55.101 秒で 100,004 conflicts に到達して
  UNKNOWN（予算切れ）。W18 Cadical195 は 120 秒で 100k conflicts に達せず timeout。
  同じ d・同じソルバで、W18 の方が 1 クエリあたりの実効速度が低い
  （並列度とマシン負荷の差）[INFERENCE]。判定はどちらも UNKNOWN。

## 結論

1. **尾部内側（d=1280, 1300）の UNSAT はソルバ非依存の方向に確定した。**
   Cadical195 を除く 13 種（Glucose3/4/42、Gluecard3/4、Minisat22/GH、Maplesat、MapleCM、
   Mergesat3、Ergo、Kissat404）がそれぞれ独立に UNSAT。唯一の timeout は MapleChrono で、
   W14 の d=1 でも時間切れする既知の遅いソルバである。
   系譜は Glucose 系 5・Minisat 系 2・Maple 系 3・Mergesat3・Ergo・Kissat404 の
   6 系統（Cadical195 を加えて 7）であり、W14 の 12 種/7 系統と同じ構図。
   ただし Kissat404 は単位節方式で、厳密には同一入力形式ではない。
2. **d=1316 は「試した 5 種すべて UNSAT」までしか言えない。** 未実行 9 種
   （Maplesat, MapleCM, MapleChrono, Glucose3/4/42, Gluecard3/4, Mergesat3）がある。
   また 1316 は 5 種中 Minisat22 が 120.779 秒（cap 240 秒）と最も高価で、
   費用の面では 1280/1300 と同列に扱えない。
   1316 を「ソルバ非依存」と断定するには、残り 9 種（少なくとも Glucose/Maple 系の
   各 1 種）の実行が必要で、本ログの範囲では未実施。
3. **境界 d=1317 は全 14 種で UNKNOWN（wall cap、予算未到達）。**
   掃引（UNKNOWN）・W17 fresh Cadical195（UNKNOWN, 100,004 conflicts）と整合する。
   「1316 まで UNSAT / 1317 から UNKNOWN」という切れ目は、履歴を除いても、
   ソルバを替えても保たれた。したがって境界は履歴依存でも Cadical195 依存でもない。
   **ただし 1317 側は「UNKNOWN の一致」であって「SAT の一致」ではない**:
   1317 が充足可能であることは誰も示していない。
4. **同一符号化（候補B）の留保は残る。** W18 の変数はソルバのみで、クラス CNF は
   全クエリで `search_shape_class.build(2647, edges, 1, 1, 3)` の同一節集合
   （`output/w14-cnf-cache.pkl`、vars=17,180、clauses=90,891、kept_edges=53,886）である。
   排除できたのは「Cadical195 固有の易しさ」だけで、
   「この符号化（候補B・このクラス CNF 生成器）に固有の易しさ」は排除していない。
   また外部 binary（cadical/kissat/glucose/minisat 等）は PATH に無く（W14 で確認済み）、
   DIMACS 経由の完全に独立な実装での検証は依然として未実施。
5. **timeout の解釈。** W18 の 16 レコードの timeout はすべて
   「120 秒の壁時計打ち切り、100k conflicts 未到達」であり、conflict 予算による UNKNOWN
   とは別種である。d=1316 の Minisat22（120.779 秒）は cap 240 秒の下で完走しているので
   timeout ではない。MapleChrono は d=1280/1300/1317 の 3 点で timeout しており、
   尾部の判定には寄与していない（W14 の d=1 でも timeout している低速ソルバ）。

**要約**: 尾部 UNSAT のうち d=1280/1300 は 13 種・6 系統で再現し、ソルバ非依存の方向に
確定した。d=1316 は 5 種のみで、未実行 9 種が残るため断定しない。d=1317 は全 14 種で
UNKNOWN のまま境界が保たれた。残る制約は「符号化が候補B の同一節集合であること」と
「外部 binary による独立実装検証が未実施」である。

（完）

## 追補（W19）

- 日付: 2026-11-10
- 目的: W18 で未実行だった d=1316 の残り 9 ソルバを実行し、1316 の判定を 14 種で揃える。
- 新規計算は行っていない。以下の数値は既存 JSON の実読のみ。
- 入力: `output/w19-1316-cross-rest.json`（9 レコード）と
  `output/w18-tail-cross-solver.json`（d=1316 の 5 レコード）。
  両者が合わせて 14 ソルバ、**重複なし**（W19 の 9 種と W18 の 5 種は交わらない）。

### W19 の実行条件（JSON ヘッダの実読値）

| 項目 | 値 |
|---|---|
| p / size / class | 2647 / 1322 / [1,1,3] |
| budget（conflicts） | 100,000 |
| vars / clauses / kept_edges | 17,180 / 90,891 / 53,886 |
| build_seconds / build_source | 1.0 / `cached:.../w14-cnf-cache.pkl` |
| device_timeout | 240.0 秒 |
| caps | `1316:240` |
| deadline（全体） | 3,000.0 秒 |
| jobs | 2 |
| solvers（ヘッダ） | 8 種（MapleCM, MapleChrono, Glucose3, Glucose4, Glucose42, Gluecard3, Gluecard4, Mergesat3） |
| elapsed | 910.4 秒 |

注: ヘッダの `solvers` 配列は 8 種だが、`records` は 9 件あり **Maplesat がヘッダから漏れている**
（9 件のソルバ名は全て相異なる）。集計はヘッダではなく `records` の実読に従った。

`vars` / `clauses` / `kept_edges` が W18 と完全一致するので、**同一の CNF cache
（候補B、`search_shape_class.build(2647, edges, 1, 1, 3)`）** を使った入力であることは
JSON から確認できる。変動したのは並列度（W18: jobs=4 → W19: jobs=2）だけで、
1 クエリ = 1 サブプロセス、`conf_budget(100000)` + `solve_limited(assumptions=[B_d])` は同じ。
Kissat404 のみ `unit-B_d`（assumption 非対応）で、これは W19 の 9 種には含まれない。

### 結果: W19 の 9 ソルバ（d=1316, cap 240 秒）

| ソルバ | setup | 判定 | seconds | build_seconds |
|---|---|---|---:|---:|
| Maplesat | assumption-B_d | UNSAT | 224.885（cpu 81.191） | 0.101 |
| MapleCM | assumption-B_d | **timeout** | 240.0 | — |
| MapleChrono | assumption-B_d | **timeout** | 240.0 | — |
| Glucose3 | assumption-B_d | UNSAT | 189.793 | 0.107 |
| Glucose4 | assumption-B_d | **timeout** | 240.0 | — |
| Glucose42 | assumption-B_d | **timeout** | 240.0 | — |
| Gluecard3 | assumption-B_d | UNSAT | 182.216 | 0.217 |
| Gluecard4 | assumption-B_d | UNSAT | 221.463 | 0.099 |
| Mergesat3 | assumption-B_d | **timeout** | 240.0 | — |

timeout 5 種はいずれも `reason: "wall cap 240s (conflict budget 100000 not reached)"`、
つまり **conflict 予算 100k に到達しないまま親の壁時計で打ち切られた**記録であり、
予算切れの UNKNOWN ではない。UNSAT とは数えない。

Maplesat の `seconds`（224.885）が `cpu_seconds`（81.191）より大きいのは
jobs=2 の並列実行下の壁時計であるため。W18 の表（jobs=4）とは秒数を直接比較しない。

### d=1316 の最終集計（14 ソルバ, W18 5 + W19 9）

判定別:

| 判定 | 数 | ソルバ（seconds） |
|---|---:|---|
| UNSAT | **9** | Ergo 25.011, MinisatGH 43.313, Cadical195 49.214, Kissat404 116.508（unit）, Minisat22 120.779, Gluecard3 182.216, Glucose3 189.793, Gluecard4 221.463, Maplesat 224.885 |
| timeout（240s, 予算未到達） | **5** | MapleCM, MapleChrono, Glucose4, Glucose42, Mergesat3 |
| UNKNOWN（予算切れ） | 0 | — |
| SAT | 0 | — |

系統別（UNSAT / 試行）:

| 系統 | ソルバ | UNSAT | timeout |
|---|---|---:|---:|
| Cadical | Cadical195 | 1/1 | 0 |
| Kissat | Kissat404 | 1/1 | 0 |
| Minisat | Minisat22, MinisatGH | 2/2 | 0 |
| Ergo | Ergo | 1/1 | 0 |
| Maple | Maplesat, MapleCM, MapleChrono | 1/3 | 2 |
| Glucose 系 | Glucose3, Glucose4, Glucose42, Gluecard3, Gluecard4 | 3/5 | 2 |
| Mergesat | Mergesat3 | 0/1 | 1 |

**UNSAT を与えた系統は 6（Cadical, Kissat, Minisat, Ergo, Maple, Glucose 系）、
UNSAT 9 種。**

### 結論の更新

1. **d=1316 は「ソルバ非依存」とまだ言えない。** W18 時点の「5/5 UNSAT」は
   14 種に広げると **9/14 UNSAT・5 timeout** になった。UNSAT は
   6 系統・9 種で再現しており、SAT は 1 種も出ていないので**反証は無い**。
   しかし 5 種が 240 秒の壁時計で結論を出しておらず、
   「どのソルバでも解ける」ではなく「9 種では解け、5 種では 240 秒では解けなかった」
   が正確な記述である。したがって W18 結論 2 の「試した 5 種すべて UNSAT までしか
   言えない」は、「9 種で UNSAT、5 種は未決」に置き換わる。
   timeout 5 種のうち Glucose4 / Glucose42 / MapleCM / Mergesat3 は 1280/1300 では
   UNSAT を返していた（MapleChrono のみ 1280/1300 でも timeout）ので、
   1316 の硬さは特定ソルバの不得意だけでは説明できない。
2. **d=1280/1300 との非対称は timeout 数に現れる。**
   1280 と 1300 はそれぞれ 13 UNSAT + 1 timeout（MapleChrono のみ）、
   1316 は 9 UNSAT + 5 timeout。cap が 120 秒（1280/1300）対 240 秒（1316）と
   1316 の方が 2 倍緩いにもかかわらず timeout が 1 → 5 に増えており、
   しかも 1316 の timeout はすべて「240 秒で 100k conflicts 未到達」である。
   したがって **1316 は 1280/1300 と同格の「易しい尾部内側」ではなく、
   境界 1317 に近い硬い点**として扱うべきである。
   一方、UNSAT 側の費用も 25.011〜224.885 秒で、1280/1300 の 1.675〜13.402 秒の
   1 桁上にある（並列度が jobs=4 → 2 と違うため厳密比較は不可、方向のみ）。
3. **境界 d=1317 の扱いは変わらない。** 1316 が 9 種 UNSAT・5 種 timeout である以上、
   「1316 まで UNSAT / 1317 から UNKNOWN」の切れ目は 1317 側（14/14 timeout、
   予算未到達）で支えられており、1316 側の全数確定は未了。1317 が充足可能であることも
   依然として誰も示していない。
4. **「同一符号化」の留保は残る。** W19 も W18 と同じ `w14-cnf-cache.pkl`
   （vars=17,180 / clauses=90,891 / kept_edges=53,886）を使っており、
   排除できたのは「Cadical195 固有の易しさ」と「一部ソルバ固有の易しさ」だけである。
   「候補B・このクラス CNF 生成器に固有の易しさ」は排除していない。
   外部 binary（DIMACS 経由の独立実装）による検証も未実施のままである。
5. **timeout と UNKNOWN の区別は維持する。** 1316 の 5 timeout は
   conflict 予算 100k 未到達の壁時計打ち切りであり、W17 の d=1317
   （100,004 conflicts 到達後 UNKNOWN）とは別種。予算を上げれば判定が変わる可能性は
   否定できない [INFERENCE]。本追補はその検証を含まない。

**要約（W19 後）**: d=1316 の 14 ソルバ集計は **UNSAT 9 / timeout 5 / SAT 0**。
UNSAT は 6 系統で再現し反証は無いが、5 種が 240 秒で未決のため
「ソルバ非依存」とは断定しない。d=1280/1300（各 13 UNSAT + 1 timeout、cap 120 秒）と比べ、
1316 は cap を 2 倍にしても timeout が 5 種に増える硬い点である。
境界 1317（14/14 timeout）と「同一符号化（候補B）」の留保は変わらない。

（W19 完）
