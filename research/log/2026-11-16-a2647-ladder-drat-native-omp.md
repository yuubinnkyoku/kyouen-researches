# 2026-11-16: ネイティブCaDiCaLによるラダーDRAT領収書パス (W33, omp)

## 目的と前提

ラダー決着8件のうちDRAT監査済みは7件。残る d=820@20M は、pysat版
`ladder_drat.py`（`with_proof=True`、`get_proof()` で証明全体をRAMに載せる）で
2回試行し、いずれもVM再起動で殺された（15:35開始→16:10、17:17開始→20:12、
`solver.json` なし）。同スクリプトの3回目の試行が並走中。

本作業は、証明をディスクへストリームするネイティブCaDiCaL 3.0.1で同じ領収書を作る
ドライバを用意し、小さい段 d=1292@3M で end-to-end 検証すること。
**d=820@20M のネイティブ実行はしていない**（指示どおり。起動手順のみ §3）。

## §1 設計

### 1.1 ネイティブ呼び出し方法: なぜCLIでなくshimか

スタンドアロンの `cadical` バイナリは決定フェーズ（warm-start候補）を
**変数ごとに**設定できない。CLI にあるのは `--forcephase`（全変数を同一フェーズ）と
`-r <sol>`（competition出力形式の解を読む）だけで、pysat版が使う
`Solver::set_phases(tg.phases(...))` に相当する入口が無い。
`--forcephase` をかけると全変数が同一初期フェーズになり、warm-startの意味が消える。

そこで `native_solve.cpp`（新規, 117行）を用意し、ビルド済みの
`libcadical.a` に対して直接リンクする。呼ぶのは3つだけ:

- `Solver::trace_proof(path)` — `state()==CONFIGURING` の間だけ許されるので
  `read_dimacs` より先に呼ぶ。以降の証明はCaDiCaLの内部tracerが
  **1ステップずつファイルへ書く**。ドライバ側のRAMには載らない。
- `Solver::phase(lit)` — `phases.txt` の符号付きリテラルを順に適用。
- `Solver::limit("conflicts", budget)` — ラダーと同じ20M/3M等の衝突予算。

解決後は `close_proof_trace(true)` と `statistics()` を呼び、閉路時の
`DRAT <n> added clauses` / `DRAT <n> deleted clauses` / `DRAT <n> bytes` を
`run.log` に残す（領収書に証明ステップ数を記録するため）。

```
usage: native_solve <input.cnf> <proof> <conflict-budget>
                    [<phases>|-] [<result.json>|-] [<witness>|-]
```

`native-result.json` に `solver_version` / `variables` / `phase_hints` /
`solve_seconds` / `statistics{conflicts,decisions,propagations,ticks}` /
`max_rss_kb`（`getrusage(RUSAGE_SELF)`）を書く。終了コードはCaDiCaLの
10=SAT, 20=UNSAT, 0=UNKNOWN をそのまま返す。

shimは `output/native-solve` に1回だけビルドし（source より古い時のみ再ビルド）、
バイナリshaを領収書に記録する:

```
g++ -std=c++17 -O2 -DNDEBUG \
    -I.../cadical-src/src -I.../cadical-src/build \
    native_solve.cpp .../cadical-src/build/libcadical.a -o output/native-solve
```

### 1.2 ドライバ: `ladder_drat_native.py`（新規）

pysat版 `ladder_drat.py` の `build_cnf(d)` をそのままimportしてCNFを作り、
`ternary_general.phases(P, d, warm[2:])` で同じwarm-start phasesを作る。
既存ファイルは一切変更しない。

出力先は新規 `output/ladder-drat-native-d<D>-budget<B>/`:

| file | 内容 |
|---|---|
| `init.json` | CNF来歴・sha・参照したpysat領収書との一致判定 |
| `input.cnf.gz` | gzip(mtime=0) のDIMACS。ラダー資産とバイト同一 |
| `input.cnf` | 展開済みDIMACS（ソルバ入力、drat-trim入力） |
| `phases.txt` | 3966個の符号付きリテラル（3·1322変数ぶん） |
| `run.log` | ネイティブソルバのstdout/stderr全部 |
| `native-result.json` | shimの生出力 |
| `solver.json` | 領収書（pysat版の項目名を踏襲した上位集合） |
| `proof.drat` | バイナリDRAT（ネイティブがストリーム出力） |
| `proof.drat.gz` | 証明のgzip（mtime=0、検証後に保存） |
| `drat-trim.log` | 検証器のstdout |
| `audit-drat-trim.json` | pysat版と同形式の監査記録 |

`solver.json` の主要項目（pysat版との対応）:

- 共通: `p, d, target, empty_bound, conflict_budget, variables, clauses,
  base_clauses, encoded_cnf_sha256, worker_source_sha256, generator_source_sha256,
  solver_status, solver_exit_code, solve_seconds, statistics, scope`
- ソルバ同定: `solver="cadical-native"`, `solver_version="3.0.1"`,
  `solver_source_commit`（libcadicalのビルド元),
  `solver_binary_sha256`, `solver_shim_source_sha256`, `solver_shim_binary_sha256`
- 証明: `proof_format="binary-drat"`, `proof_bytes`, `proof_sha256`,
  `proof_steps{added,deleted,bytes}`, `proof_lines=null`
- 資源: `wall_seconds`（driver計測）, `max_rss_kb`
- 来歴: `phase_hints`, `input_cnf_gz_sha256` は `init.json` 側

`proof_lines` はpysat版のASCII行数に相当する値が無いため `null`、
代わりに `proof_steps` を置く。

`audit-drat-trim.json` は pysat版のキー構成
（`checker, returncode, stdout, stderr, seconds, timed_out, verified,
p, target_size, d, conflict_budget, checker_source*, checker_build,
checker_binary_sha256, input_sha256, proof_sha256, proof_lines, log`）を保ち、
`proof_gz_sha256`, `proof_bytes`, `proof_format`, `proof_steps`,
`not_verified`（MEMOUT/`s NOT VERIFIED` 行の抜粋）を追加する。

### 1.3 CNF同一性の照合方法

1. `build_cnf(d)` でDIMACSを再生成し `encoded_cnf_sha256` を計算。
2. 参照先（既定: `output/ladder-drat-d<D>-budget<B>/`）の `init.json` の
   `encoded_cnf_sha256` と比較。**不一致なら即停止**（偽の領収書を作らない）。
3. 生成した `input.cnf.gz` のgzバイトshaを参照領収書の `input.cnf.gz` と比較。
4. 既にステージ側に `input.cnf.gz` がある場合は、展開後のshaが再生成値と
   一致することを確認（改竄・破損の検出）。

実測（`--cnf-only`、solveなし）:

| d | budget | cnf_sha256 | init一致 | gzバイト一致 |
|---|---|---|---|---|
| 1292 | 3M | `f144e4dcf1a358b1…` | true | true |
| 820 | 20M | `1c2dece33115f9d0…` | true | true |

参照先が存在しない場合（例: `--budget 1`）は `cnf_sha_match: null` として
警告のみ出し、解決は続行する（新規段を許すため）。

### 1.4 再開可能性

ネイティブCaDiCaLにチェックポイント／再開機能は無い。VM再起動で殺された場合、
**その回の証明は先頭から無効で、最初からやり直し**。ドライバの挙動:

- `solver.json` が存在する段は solve をスキップ（idempotent）。
- `solver.json` が無い段は、`proof.drat` に前回の書けかけが残っていても
  上書き再実行する。`run.log` は切り詰め、`native-result.json` はshimが上書き。
  直前の実行が殺されていれば `native-result.json` が無いので、
  ドライバはログ末尾5行を添えて異常終了する（部分的な領収書を作らない）。
- 監査は `input_sha256` / `proof_sha256` / `proof_gz_sha256` /
  `checker_binary_sha256` が全て一致する既存 `audit-drat-trim.json` がある時だけ
  再利用する。`--recheck` で強制再検証。`--verify-only` は solve を伴わない。

検証済み挙動（d=1292@3M、スクラッチ出力先で実施）:

- 再実行 → `solver.json present -> skip solve` → `VERIFIED (saved audit)`。
- `solver.json` と audit を削除し `proof.drat` を5000バイトのノイズで置換
  （再起動で殺された状態の模擬）→ 再solveし、証明sha
  `bfd0c446a809db35…` に復帰、VERIFIED。
- `--budget 1` → exit 0 / status UNKNOWN / conflicts 2 / 検証はスキップ
  （UNSAT限定の領収書なので当然）。
- 同一入力で2回流すと `proof.drat` は**バイト同一**
  （`bfd0c446a809db3597650d980f46fb8b4475b73be47ed92681c826912dc9380e`、2回一致）。

### 1.5 検証のメモリに関する注意（重要）

drat-trimはパースした証明をRAMに保持する（`S->proof` はステップあたり
`long` 1個、`S->DB` は証明リテラルあたり `int` 1個）。したがって
**証明ファイルがディスクに収まっても検証が8GiBに収まるとは限らない**。

実測基準（pysat領収書、同一VMで検証成功済み）: d=1258 の証明はASCII 1.45GB、
リテラル 262,889,867個（63 lit/conflict）、検証 1,564秒。
d=820 は 13,294,778 conflicts なので、pysat比で約3.2倍、リテラル約8億、
`int` DBだけで約3.2GB＋ステップ配列＋作業領域 → **4〜6GB程度と推定 [INFERENCE]**。
現在の空きRAMは約1.1GB（`free -m`: total 7934, available 1104）なので、
検証段は他プロセスを止めた状態で単独実行する必要がある。

## §2 d=1292@3M での end-to-end 検証結果

出力: `output/ladder-drat-native-d1292-budget3000000/`。
コマンド:

```
uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-ternary-selection-20261109/ladder_drat_native.py \
  --d 1292 --budget 3000000
```

| 項目 | pysat版（既存） | ネイティブ版（新規） |
|---|---|---|
| `encoded_cnf_sha256` | `f144e4dc…37e8` | `f144e4dc…37e8`（一致） |
| `input.cnf.gz` バイトsha | `7ab347c0…1ca1` | `7ab347c0…1ca1`（一致） |
| `solver` | Cadical195 (pysat 1.9.dev21) | cadical-native 3.0.1 (libcadical `c6073042`) |
| `solver_status` | SOLVER_UNSAT | SOLVER_UNSAT（一致） |
| `conflicts` | 674 | 628 |
| `solve_seconds`（プロセス内） | 0.2573 | 0.1477（shim計測 0.1081） |
| 証明の表現 | ASCII 3,514行 / 52,300 B | binary 3,331 added + 161 deleted / 23,116 B |
| `proof_sha256` | （ASCII、別物） | `bfd0c446…380e` |
| drat-trim | `s VERIFIED`, 0.242 s | `s VERIFIED`, 0.211 s |
| `input_sha256`（監査） | `f144e4dc…37e8` | `f144e4dc…37e8`（一致） |

drat-trimログ（ネイティブ）:

```
c turning on binary mode checking
c parsing input formula with 7926 variables and 68404 clauses
c finished parsing, read 23116 bytes from proof file
c detected empty clause; start verification via backward checking
c 1191 of 68404 clauses in core
c 522 of 3332 lemmas in core using 26107 resolution steps
c 0 RAT lemmas in core; 137 redundant literals in core lemmas
s VERIFIED
```

一致した点: CNF（sha・gzバイト同一）、verdict（UNSAT）、独立検証の成否。
不一致（差に理由がある点）: 衝突数 674→628 と証明バイト数。これは
**ソルバ実装が異なる**ため当然で、証明の内容はソルバ依存。ラダーの
d=1292 決着は「そのCNFがUNSAT」であり、証明はどちらも
drat-trimが `s VERIFIED` を出しているので主張は同一。
warm-start phasesは両者で同一（3·1322=3966個、`phase_hints=3966`）。

証明ストリーミングの確認: ネイティブ実行の `max_rss_kb=69,884`（約68MiB）。
d=1292規模では区別がつかないが、W30の(1,1,3) 10M段では
conflicts 10,000,001・証明2,747,386,981B でRSS 56MB の実績があり、
proofサイズがRSSに比例しないことを示している。

## §3 d=820@20M ネイティブ実行の起動手順（メインエージェント用）

**実行しない**（今回はドライバ完成とd=1292検証まで）。起動する場合:

```sh
cd ~/workspace/kyouen-omp/full
# ソルブ（証明をストリーム、solver.json が出たら完走）
uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-ternary-selection-20261109/ladder_drat_native.py \
  --d 820 --budget 20000000 --solve-only
# 検証（他プロセスを止め、RAMを空けてから）
uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-ternary-selection-20261109/ladder_drat_native.py \
  --d 820 --budget 20000000 --verify-only
```

1コマンドで両方やるなら `--solve-only` を外す（solve → gzip → drat-trim）。

- 入力同一性は確認済み（§1.3）: `cnf_sha256=1c2dece33115f9d0…`、
  `output/ladder-drat-d820-budget20000000/` の `init.json` と一致、
  `input.cnf.gz` もバイト一致。
- **推定所要時間 [INFERENCE]**: pysatの実測 13,294,778 conflicts / 3,813 s
  （= 3,486 conflicts/秒）。ネイティブはW30 (1,1,3) 10M段で
  10,000,001 conflicts / 3,586 s（= 2,788 conflicts/秒、real 4,856 s）。
  この2点から **4,500〜4,800秒（1.3時間程度）**。pysat版の3,813秒より遅い側に
  出る可能性がある（ネイティブは証明を常時ディスクへ書くため）。
- **推定証明サイズ [INFERENCE]**: W30実測 275 B/conflict。13.29M conflicts
  → **約3.6GB**（終盤ほど1ステップが長いので 3.5〜4.5GB と見る）。
  ディスク空き 115GB なので余裕。
- **再起動リスク**: 再起動間隔は当日2〜4時間。1.3時間のソルブは窓に収まる見込みが
  高いが、保証はない。殺されたら証明は最初から（§1.4）。pysat版が2時間55分で
  終わらなかったのはRAM上の証明バッファと`get_proof()`のコピーが原因で、
  ネイティブにはその区間が無い。
- **検証リスク**: §1.5のとおり、drat-trimは約4〜6GBを要求すると推定。
  8GiB（実空き1.1GiB）では OOM しうる。OOM時は `drat-trim.log` に
  `c MEMOUT: ...` が残り、`audit-drat-trim.json` は `verified=false`,
  `not_verified` にその行が入る（証明とソルブ領収書は無傷なので、
  RAMの大きいホストで `--verify-only` を再実行すればよい）。
  検証だけは pysat版と違い**実行時間も長い**（d=1258で1,564秒、
  d=820はその約3.2倍 → 1.2〜1.5時間 [INFERENCE]）。

## 成果物

- ドライバ: `research/experiments/parabola-ternary-selection-20261109/ladder_drat_native.py`
  - SHA-256 `6215ebb9a6abdd6b0a19215acabed650f7577bf7bd57e37ea8a8a92fb5e36423`
- shim: `research/experiments/parabola-ternary-selection-20261109/native_solve.cpp`
  - SHA-256 `5d3fc38ec92435032bd24ee0c068cc486bc2b898a3a9fab465aeda916dfa67c7`
  - ビルド済み `output/native-solve` SHA-256
    `e5afb8d5b47c161be312dca0258e57b265ee08cbbce647e06ba27afa7ac874e0`
- 検証済み領収書: `output/ladder-drat-native-d1292-budget3000000/`
  （`solver.json` / `audit-drat-trim.json` とも `verified=true`）
- 既存ファイル・既存出力ディレクトリは無変更（`git status` で新規のみ）。
  ただし pysat版 d=820@20Mの3回目試行が並走中で `output/ladder-drat-d820-budget20000000/`
  に触れているが、本作業は参照のみ（読み取り）。
- `output/native-solve`（1.7MBのビルド済みshim）と `input.cnf`（非圧縮DIMACS,
  1.5MB）は派生物。領収書にはそれぞれのshaを記録済みなので、追跡するかは
  統合側の判断に委ねる（本作業では未追跡のまま）。
- pushなし、knowledge項目の編集なし。

(完)
