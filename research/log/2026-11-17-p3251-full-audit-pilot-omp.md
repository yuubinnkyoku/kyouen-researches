# 2026-11-17 p=3251 全量DRAT監査ドライバの実装とパイロット (W41, omp)

W38 設計(`research/log/2026-11-17-p3251-full-audit-design-omp.md`)どおりに p=2207 の
ドライバを p=3251 用へ適応し、新規ドライバ `audit_full_3251.py` を置いた。未監査集合を
領収書の実読から再確定し、その先頭 3 点(d=21,22,23)を実際に監査して drat-trim
VERIFIED を確認した。全量実行はしていない。数値はすべて実ファイル・実測からの転記で、
外挿には [INFERENCE] を付す。push はしていない。

## 0. 成果物

- ドライバ(新規): `research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_3251.py`
  (p=2207 の `audit_full_2207.py` は未変更。`git status` で 2207 側ドライバに差分なしを確認)
- 固定入力: `$HOME/workspace/kyouen-omp/bin/p3251_drat/edges_3251.txt`
  (SHA-256 `11c8966a75615b3cd92b719cae55c2babfc0920e5adceedd35f5c88538d6fd0f`、
  1,379,766 辺 / 25,759,407 B)。元ファイルは `bin/kyouen-parabola/edges_3251.txt`
  (同一 SHA を `sha256sum` で確認、コピーして凍結)。
- 集約領収書(drat-trim、パイロット分): `output/drat_trim_audit_full_3251_92f0aa9575ed519d.json`
  (現在 3 レコード。drat-trim バイナリ SHA を名前に含むため既存の増分チェッカー領収書
  `drat_audit_full_3251_34249932790a9e9d.json` と衝突しない)。
- 1 d 単位: `output/p3251-drat-full/d<d>/` に `input.cnf.gz` / `proof.drat.gz` /
  `receipt.json` / `drat-trim.log`。`output/p3251-drat-full/progress.log` は追記式。
  `unknown.json` は未生成(UNKNOWN 0)。

## 1. ドライバの変更箇所(2207 版との差分、すべて実装済み)

`audit_full_2207.py` をコピーして以下だけを変えた。ロジック(solve 分岐・予算ラダー・
再開判定・原子書き込み・exit code)は無変更。

1. docstring: p=3251・`clauses_for_pair(3251, edges, d)`・出力先 `p3251-drat-full`・
   使用例 `--ds 21-25` に更新。
2. `P = 2207` → **`P = 3251`**。`H = (P - 1) // 2` は自動で 1625。
3. `EDGES_SHA` → **`11c8966a75615b3cd92b719cae55c2babfc0920e5adceedd35f5c88538d6fd0f`**
   (W38 §2.1 の「初回生成・SHA 固定」を、既に存在した `edges_3251.txt` の実測 SHA で実施)。
4. `FULL = OUT / "p2207-drat-full"` → **`OUT / "p3251-drat-full"`**。
   `RECEIPTS = OUT / f"drat_trim_audit_full_{P}_{CHECKER_BIN_SHA[:16]}.json"` は P 依存で自動。
5. `PROCEDURE["target"]` / `["cnf"]` → K0708・残り 1,541 d・edges 3251 の記述
   (1,379,766 辺、`p cnf 1625 60266`)。`SAT FOUND` のログ文字列も K0708 に。
6. edges パス → `$TEMP/p3251_drat/edges_3251.txt`。
7. 集約領収書のキー `ccadical_solver_used_for` → `cadical_solver_used_for`(2207 版の
   綴り間違いの修正。値は同じ)。

不変: drat-trim バイナリ固定(SHA `92f0aa95...`、起動時検証・不一致で exit 1)、
`--budgets 5000000,20000000,100000000`、`--wall-budget`、`--mem-avail-floor-mib 1536`、
native CaDiCaL `--binary=false` 直書き、増分チェッカー副チェック(ソース SHA `34249932...`
検証付き)、`already_done`(VERIFIED + `proof.drat.gz` SHA 一致でスキップ)、
exit code 0/3/4/1。

## 2. 未監査集合の確定(実読)

領収書 `output/drat_audit_full_3251_34249932790a9e9d.json` を読んだ実測:

- `p=3251`, `h=1625`, `checker_source_sha256=34249932...`(増分チェッカー)、
  **records 84**。全 84 レコードが `verified=true` / `checker_rc=0` /
  `checker_out="VERIFIED"` / `solver="UNSAT"`。
- d の集合(昇順、実読): 1..20 の連続 20 点 + 26,51,76,...,1601(25 刻み 64 点)。
  計画標本 `d=1,26,...,1601` は 65/65、加えて標本外の d=2..20。W38 §1.1 と一致。
- 注: 84 件は drat-trim ではなく**増分チェッカー**の領収書。本ドライバの集約領収書
  (drat-trim)とは別ファイル・別 `checker` で、同一 d を二重計上しない。
- `research/experiments/parabola-audit-coverage-20261109/inventory.json` は
  commit `87e28af` 時点の snapshot(70 d)であり、現在の HEAD の 84 d とはずれる。
  本ログの 84 d は上記領収書の実読を正とする(W38 と同じ判断)。

未監査 = `{1..1625} \ 既監査84` = **1,541 点**。スクリプトで再計算し、
範囲列の和集合がちょうど 1,541 点、既監査 84 との和集合が `{1..1625}` と一致することを確認した。
`--ds` に渡す範囲列(W38 §1.2 と同一。65 範囲):

```
21-25,27-50,52-75,77-100,102-125,127-150,152-175,177-200,202-225,227-250,252-275,277-300,302-325,327-350,352-375,377-400,402-425,427-450,452-475,477-500,502-525,527-550,552-575,577-600,602-625,627-650,652-675,677-700,702-725,727-750,752-775,777-800,802-825,827-850,852-875,877-900,902-925,927-950,952-975,977-1000,1002-1025,1027-1050,1052-1075,1077-1100,1102-1125,1127-1150,1152-1175,1177-1200,1202-1225,1227-1250,1252-1275,1277-1300,1302-1325,1327-1350,1352-1375,1377-1400,1402-1425,1427-1450,1452-1475,1477-1500,1502-1525,1527-1550,1552-1575,1577-1600,1602-1625
```

## 3. 限定パイロット(実測)

未監査の最小 d 3 点。コマンド:

```sh
cd ~/workspace/kyouen-omp/full
TEMP=$HOME/workspace/kyouen-omp/bin nice -n 10 \
  uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_3251.py \
  --ds 21-23
```

| d | solver | status | conflicts | budget | proof lines | proof bytes | gz bytes | solve (s) | check (s) | verdict |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 21 | cadical-native | SOLVER_UNSAT | 21,277 | 5,000,000 | 300,332 | 11,142,308 | 2,164,640 | 2.26 | 2.96 | VERIFIED |
| 22 | cadical-native | SOLVER_UNSAT | 23,020 | 5,000,000 | 352,930 | 12,468,769 | 2,324,310 | 2.78 | 4.67 | VERIFIED |
| 23 | cadical-native | SOLVER_UNSAT | 5,941 | 5,000,000 | 331,374 | 9,603,252 | 1,745,990 | 0.83 | 1.56 | VERIFIED |

- 3 点すべて `s VERIFIED`・drat-trim exit=0。ドライバ本当の総壁時計は **50.0 秒**
  (CNF 生成込み。1 d あたり約 16.7 秒)。
- 全 3 点が native CaDiCaL 経路。progress.log の理由は
  `MemAvailable=371/488/365MiB < floor=1536MiB`(W31 と同じく RAM 逼迫で既定が native)。
- `proof.drat.gz` の再計算 SHA-256 が receipt の `proof_gz_sha256` と一致することを
  3 点で確認。`unknown.json` は生成されていない。
- CNF ヘッダ実測: `p cnf 1625 60266`(W38 §2.2 の d=1 実測と一致)。
- **再開性の実地確認**: 同じ `--ds 21-23` を再投入して `todo=0` / `driver done` /
  2.8 秒(全スキップ)。
- `check_seconds` の行/秒レート: 101k / 76k / 212k 行/秒。W38 が引用した
  W20 の幅 8.6k〜158k 行/秒の上側に近い。

## 4. W38 見積との整合判定 [INFERENCE]

パイロット 3 点の平均を残り 1,541 点へ外挿する。

| 量 | パイロット平均 | ×1,541 の見積 | W38 見積 | 判定 |
|---|---:|---:|---:|---|
| solve 秒 | 1.96 | ≈ 0.8 h | ≈ 3.1 h | 見積より速い(整合) |
| proof lines | 328,212 | ≈ 505.8 M 行 | ≈ 206.6 M 行 | **2.4 倍多い**(下記) |
| drat-trim check 秒 | 3.06 | ≈ 1.3 h(77k 行/秒なら ≈ 1.8 h) | ≈ 1〜7 h | 整合(下端寄り) |
| proof gz 合計 | 2.08 MB/d | ≈ 3.2 GB | ≈ 1〜2 GB | **上振れ** |
| proof RAW 合計 | 11.07 MB/d | ≈ 17 GB(検証後破棄) | ≈ 5〜6 GB | 上振れ(空き 109 GB で収容可) |
| 総壁時計(CNF 生成込み) | 16.7 s/d | ≈ 7.1 h | — | solve+check 合計より大 |

- **solve は W38 見積より速い**。W38 の 84 点平均 7.3 s は増分チェッカー時代の
  solve 記録で、ドライバの native CaDiCaL 実測は 1〜3 s 台。予算 5M で
  conflicts は 6k〜23k と小さく、UNKNOWN も出ていない。
- **proof lines は 84 点平均より 2.4 倍多い**。理由は難易度の d 依存で、
  d=21..23 は 84 点の近傍(d=20: 40,058 行、d=26: 174,853 行)より重い側に当たった
  [INFERENCE: 3 点のみで、標本の周辺 d は 4〜17 万行なので、パイロットの
  30〜35 万行は小 d 帯の局所的な重さと読むのが自然]。したがって §3 の
  lines/gz/check の外挿は**上側の bound** であり、W38 の 206.6 M 行 /
  1〜2 GB を棄却するものではない。両論併記で幅を持たせる:
  検証 ≈ **1.3〜3.0 h**、gzip 保存 ≈ **1〜3.2 GB**、RAW 一時 ≈ **6〜17 GB**。
- 時間の支配項は solve でも check でもなく **d あたりの固定費(CNF 生成・gzip・
  子プロセス起動)**。実測 16.7 s/d × 1,541 ≈ 7.1 時間が実効の下限になる。
  40 分窓(`--wall-budget 2400`)なら 1 窓あたり約 140 d、1,541 d で
  **約 11 窓**。1 日 1〜2 窓なら 1 週間規模 [INFERENCE]。

## 5. 全量実行の起動手順

### 5.1 バッチ分割と再起動耐性

- **1 d = 1 サブプロセス**。d 完了ごとに `receipt.json` を原子的(`tmp` + `os.replace`)に
  書き、集約領収書も毎回原子的に書き直す。再起動で失うのは最大 1 d。
- 再起動 = 同一コマンドの再実行のみ。`verdict=="VERIFIED"` かつ `proof.drat.gz` の SHA が
  記録と一致する d は自動スキップ(§3 で実地確認: `todo=0`)。
- `--wall-budget 2400`(40 分窓)で区切り、外部から再起動する。`P=1` 逐次 + `nice -n 10`、
  重い外部プロセス同時数 ≤ 2 を維持(p=2207 全量監査と並走させる場合はどちらかを待たせる)。

```sh
cd ~/workspace/kyouen-omp/full
DS='21-25,27-50,...,1602-1625'   # §2 の 65 範囲
nohup env TEMP=$HOME/workspace/kyouen-omp/bin nice -n 10 \
  uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_3251.py \
  --ds "$DS" --wall-budget 2400 \
  >> research/experiments/parabola-p2207-no-equality-witness-20261107/output/p3251-drat-full/driver.stdout.log 2>&1 &
echo $!
```

- exit code: 0=完走/窓到達、**3=SAT(即時停止)**、4=UNKNOWN 記録あり、1=前提不一致
  (edges SHA・drat-trim SHA 不一致)。

### 5.2 SAT が出た場合の即時停止ルール

`solver_status=="SAT"` を検出したら receipt に `verdict:"SAT"` を書き、
`SAT FOUND (counterexample to K0708)` をログして **exit 3 で即時停止**する。
以降の d は一切実行しない。これは監査失敗ではなく **K0708 の反例**(`A(3251)=(p+3)/2`
を達成する証人)であり、`deep_scan_3251.json` の全 1625 d UNSAT 主張(衝突予算 20 万)と
矛盾する。停止時点の `input.cnf.gz`・`proof.drat.gz`・`receipt.json` が検証材料。
人間の判断を要するため自動続行しない。

### 5.3 UNKNOWN

予算ラダー 5M→20M→100M。全予算で決着しない d は `unknown.json` に記録し
**領収書化しない**(W26/W31 と同じ)。現在 UNKNOWN 0。`unknown.json` が非空のままなら
§6 の条件 3 を満たさず昇格できない。

## 6. K0708 の `computed` 昇格条件

すべて満たした場合のみ、`research/knowledge/items/K0708-p3251-no-parabola-equality-witness.md`
を `needs-review` → `computed` に更新する。

1. 残り 1,541 d すべてに drat-trim 領収書があり `verdict=="VERIFIED"`、かつ
   `input_sha256`・`proof_sha256`・`proof_gz_sha256` が再生成物と一致する。
   集約領収書 `drat_trim_audit_full_3251_92f0aa9575ed519d.json` に重複なく
   **1,541 レコード**(重複 d なしをスクリプトで検査)。
2. 既存 84 件(増分チェッカー領収書)と合わせ **1,625 d 全数**が DRAT 検証済みであることを
   被覆検査で確認(`full_verified_coverage: true` 相当。`inventory.py` の `classify` は
   単一領収書しか見ないため、2 領収書を d 集合の和として突き合わせる集計を別途行う)。
3. `unknown.json` が空(または存在しない)。
4. 昇格時の更新: K0708 の `status`・`evidence`・`artifacts`(drat-trim 集約領収書と
   `audit_full_3251.py` を追加)を更新し、AGENTS.md の統合前確認
   (`uv sync --locked` / `tools/knowledge/check.py` / unittest / `build.py` /
   `git diff --exit-code -- README.md research/knowledge/generated`)を実行する。

本タスクでは knowledge 項目を編集していない(K0708 は `needs-review` のまま)。
K0101 の status は K0706 で既に反証済みのため、K0708 の昇格で変わらない
(supports relation の裏付けが強まるのみ)。

## 7. 限界・リスク

- パイロットは 3 点(d=21..23)、しかも小 d 帯に偏る。proof lines が 84 点平均の
  2.4 倍だったことは難易度の d 依存を示す。§4 の外挿は上側 bound として読む。
- native CaDiCaL 経路が実測の既定(RAM 逼迫)。pysat `with_proof` 経路は実測未使用で、
  分岐は W31 実装のまま。RAM が空けば自動で切り替わる。
- drat-trim レートは証明の質依存(W38 の 18 倍の開き)。パイロット 3 点は上側レート。
- 増分チェッカーは全量適用しない(143 h 見積、W38 §3.2)。層化少数点のクロスチェック
  (`--cross-check-ds`)に限定する。
- RAW proof は検証後削除する運用(集約領収書は gzip のみを SHA 固定)。

## 8. 結論

- 新規ドライバ `audit_full_3251.py` を置いた。変更は 7 箇所(P・EDGES_SHA・出力ディレクトリ・
  docstring・PROCEDURE・edges パス・キー綴り)のみ。p=2207 側は未変更。
- 未監査集合は実読で **1,541 d**(全 1,625 − 既監査 84、84 は増分チェッカー領収書で
  すべて VERIFIED)。`--ds` 範囲列(65 範囲)を確定し、和集合一致を検証した。
- パイロット d=21,22,23 はすべて drat-trim **VERIFIED**(solve 0.8〜2.8 s、
  check 1.6〜4.7 s、lines 30〜35 万)。再投入で `todo=0` の再開性も確認。
- W38 の solve ≈ 3.1 h はパイロット実測(≈ 0.8 h 外挿)と整合し、上回る速度。
  検証は ≈ 1.3〜3.0 h、gzip ≈ 1〜3.2 GB、RAW 一時 ≈ 6〜17 GB。実効支配項は
  d あたり固定費で総壁時計 ≈ 7.1 h(40 分窓で約 11 窓)。
- 全量起動手順・SAT 即時停止(exit 3)・UNKNOWN 非領収書化・K0708 昇格条件 4 点を
  §5/§6 に固定した。全量は未実行。

（完）
