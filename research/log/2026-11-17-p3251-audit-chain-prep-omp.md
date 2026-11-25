# 2026-11-17 p=3251 全量監査チェーンの投入準備 (W43, omp)

W41 のドライバ(`audit_full_3251.py`)とパイロット領収書を実読して再確認し、
p=2207 のチェーン(`w31-direct2207.sh`)を流用した p=3251 用チェーン
`tasks/w43-direct3251.sh` を書いた。**実行はしていない**。本実行は p=2207 監査が
batch 3 実行中のため投入しない。数値はすべて実ファイル・実測からの転記で、外挿には
[INFERENCE] を付す。push はしていない。

## 0. 成果物

- 新規: `/home/hatch/workspace/kyouen-omp/tasks/w43-direct3251.sh`(実行権あり、
  1,541 d のバッチチェーン。`tasks/` 配下、`w31-direct2207.sh` とは別名)
- 検証ログ: `tasks/w43-direct3251.log`(dry-run と guard の記録のみ)
- knowledge 項目・driver・実験出力は未変更。

## 1. パイロット再確認(実読)

### 1.1 集約領収書 = 3 レコード、すべて VERIFIED

`research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_trim_audit_full_3251_92f0aa9575ed519d.json`
(4,156 B、2026-11-17 14:58)を読んだ実測:

| d | verdict | solver_status | proof_lines | proof bytes | gz bytes | gz SHA 再計算一致 | solve | check |
|---:|---|---|---:|---:|---:|---|---:|---:|
| 21 | VERIFIED | SOLVER_UNSAT | 300,332 | 11,142,308 | 2,164,640 | true | 2.26 s | 2.96 s |
| 22 | VERIFIED | SOLVER_UNSAT | 352,930 | 12,468,769 | 2,324,310 | true | 2.78 s | 4.67 s |
| 23 | VERIFIED | SOLVER_UNSAT | 331,374 | 9,603,252 | 1,745,990 | true | 0.83 s | 1.56 s |

- トップレベル: `p=3251`、`h=1625`、`checker="drat-trim"`、
  `checker_binary_sha256=92f0aa95…aa7a`、`checker_source_sha256=d834b649…c2ee`、
  `cadical_solver_used_for="solve only (proofs are checked by drat-trim)"`。
- 各レコードの `proof_gz_sha256` を `d21/d22/d23` の実ファイルから `sha256sum` 相当で
  再計算し、3 点すべて一致を確認(スキップ判定 `already_done` の前件が成立している)。
- 各 d ディレクトリの中身: `input.cnf.gz`(416,542 B 前後)・`proof.drat.gz`・
  `receipt.json`・`drat-trim.log`。RAW の `proof.drat` / `input.cnf` は検査後
  `unlink` 済みで残っていない(ドライバ §audit_one の実装どおり)。

### 1.2 progress.log の実読

```
2026-11-17T14:57:19+0000 p=3251 h=1625 edges=1379766 requested=3 todo=3 ...
... d=21/22/23 verdict=VERIFIED ... native=True reason=MemAvailable=371/488/365MiB < floor=1536MiB
2026-11-17T14:58:05+0000 driver done
2026-11-17T15:00:17+0000 p=3251 ... requested=3 todo=0 ...     ← 再投入の全スキップ確認
2026-11-17T15:00:17+0000 driver done
```

第 2 回の `requested=3 todo=0` が「領収書 + gz SHA 一致でスキップ」の実地証拠。

### 1.3 ドライバ実装の再確認(コード実読)

- `audit_full_3251.py`: `P=3251`・`H=(P-1)//2=1625`・
  `EDGES_SHA=11c8966a75615b3cd92b719cae55c2babfc0920e5adceedd35f5c88538d6fd0f`・
  `FULL=OUT/"p3251-drat-full"`・`RECEIPTS=OUT/f"drat_trim_audit_full_{P}_{CHECKER_BIN_SHA[:16]}.json"`
  を実読で確認。`EDGES_SHA` は
  `$HOME/workspace/kyouen-omp/bin/p3251_drat/edges_3251.txt`(25,759,407 B /
  1,379,766 辺)の `sha256sum` 実測と一致。起動時に SHA 不一致なら exit 1。
- `parse_ds`(124-135 行): `,` 区切りの `a-b` を展開し `sorted(set(...))`。
  範囲の重複・順序に依存しない。
- `already_done`(169-173 行): `verdict=="VERIFIED"` **かつ** `proof.drat.gz` の
  SHA が `proof_gz_sha256` と一致した場合のみ True。片方でも欠ければ再実行。
- `main`(380-470 行): `todo = [d for d in ds if args.recheck or not already_done(...)]`、
  `--wall-budget` は d の間で判定、`outcome=="SAT"` で `return 3`、
  UNKNOWN があれば `return 4`、正常完走 `return 0`。

### 1.4 `--ds` 範囲列と 84 件スキップの整合(実計算)

- 84 レコードの実読集合: `d=1..20`(20 点)+ `d=26,51,76,...,1601`(25 刻み 64 点)= **84**。
- 範囲列(65 範囲)を展開: **和集合 1,541 点・重複 0**。
- `{1..1625} \ 84` との差集合は空、範囲列との共通部分も空。
  `1,541 + 84 = 1,625` で全数を被覆。**W38 §1.2 / W41 §2 の記述を独立に再現した。**
- したがって 84 件スキップは「範囲列が既監査 d を含まない」ことで自動的に成立し、
  加えて `already_done` の SHA 一致判定が二重の安全網になる。

## 2. チェーン script(tasks/w43-direct3251.sh)

`w31-direct2207.sh` の構造をそのまま使い、次を変更した。

| 項目 | w31-direct2207.sh | w43-direct3251.sh |
|---|---|---|
| driver | `audit_full_2207.py` | `audit_full_3251.py` |
| `DS` | p2207 の 1,082 点 | p3251 の 1,541 点(65 範囲) |
| 進捗ファイル | `p2207-drat-full/progress.log` | `p3251-drat-full/progress.log` |
| 直列ガード | なし | p=2207 の実行中/未完了なら **exit 5 で拒否** |
| 最大バッチ | 40 | **24** |
| 終了コード | 0/1/3/4 | 0/1/3/4/5/6/7(下記) |

### 2.1 終了条件

- **SAT 即時停止**: driver `rc=3`、または progress.log に `SAT FOUND` を検出 →
  `exit 3`。ループを抜けて以降のバッチを回さない。`rc==3` と `SAT FOUND` の二重判定は、
  receipt 書込後に OOM 等で driver が `exit 3` せず死んだ場合の取りこぼしを塞ぐため。
- **前提不一致**: driver `rc=1`(edges SHA / drat-trim SHA 不一致)→ `exit 1`。
- **UNKNOWN 検出**: `unknown.json` が非空 → `exit 7`。UNKNOWN は領収書化されないため
  放置すると `todo` が永久に 0 にならず、K0708 昇格条件 3 を満たせない。手動で
  予算を上げる必要があるので自動続行しない。
- **todo=0 で ALL DONE**: `todo=0` **かつ** `rc=0` **かつ** このバッチで progress.log が
  伸びた、の 3 条件同時成立でのみ `exit 0`。
  - 3 条件にした理由: パイロットの `todo=0` 行が progress.log に残っているため、
    「起動に失敗して 1 行も書かなかったバッチ」が直前の `todo=0` を読むと
    偽の ALL DONE になる。実際にスタブで再現し、修正前は誤判定、修正後は
    `rc=1`/stall 側に落ちることを確認した(§4)。
- **stall**: 直前バッチと `todo` が同一で、かつ (`rc!=0` または progress が伸びた)
  場合に 1 回計上。2 回で `exit 4`。progress が伸びたのに todo が減らない =
  `verdict=REJECTED` の d が居座っている状態で、放置しても永久に進まない。
- **上限到達**: 24 バッチで `todo>0` なら `exit 6`(再投入すれば再開)。

### 2.2 バッチ wall-budget と最大バッチ数

- `WALL=2400`(40 分窓)。p=2207 チェーンと同じ値で、重い外部プロセス同時数
  ≤ 2 の運用に合わせる。
- `MAX_BATCHES=24` の根拠:
  - パイロット実測 16.7 s/d(CNF 生成込み、50.0 s / 3 d)→ 1 窓 ≈ 143 d、
    1,541 d で **≈ 10.7 窓**。
  - 負荷下の実測(p=2207 batch 2: `todo` 952→847 の 105 d を 2,401 s)= **22.9 s/d**
    → 1 窓 ≈ 105 d、**≈ 14.7 窓**。
  - 24 は後者の ≈ 1.6 倍。`exit 6` は再投入で再開するので上限は安全側でよい。

## 3. ディスク所要(パイロット実測からの再計算)

パイロット 3 d の実ファイルサイズを平均し 1,541 d へ外挿 [INFERENCE]。

| 量 | 実測(3 d) | 平均/d | ×1,541 | 備考 |
|---|---:|---:|---:|---|
| `proof.drat.gz` | 6,234,940 B | 2.078 MB | **3.20 GB** | 恒久保存 |
| `input.cnf.gz` | 1,249,523 B | 0.417 MB | **0.64 GB** | 恒久保存 |
| 合計(保存分) | — | 2.495 MB | **3.84 GB** | receipt/log は無視できる |
| RAW `proof.drat` | 33,214,329 B | 11.07 MB | **17.1 GB** | 検証後 `unlink`、一時のみ |

- gz/RAW 比は実測 0.194 / 0.186 / 0.182(≈ 5.2 倍圧縮)。
- **W38 の「gzip 1〜2 GB」は下限側の見積**で、実測ベースでは **3.2 GB**
  (保存分合計 3.84 GB)。W38 の 1〜2 GB は 84 点の `proof_lines` 平均 134,047
  からの 206.6 M 行 → 25〜30 B/行 → 5〜6 GB RAW という経路で、パイロットの
  328,212 行/d(2.4 倍)を織り込んでいない。**3.84 GB を採用値**とする。
- `.pkl` 等の一時ファイルは別。現在 `output/` 全体は 4.4 GB
  (うち `p2207-drat-full` 1.6 GB)。
- `df -B1 /home/hatch` 実測: **空き 116.1 GB / 使用 44.6 GB / 150 GB**。
  p=2207 の残り(796 d、p=3251 と同程度の規模なら ≈ 1〜2 GB 追加)を入れても
  4 GB 級の追加は余裕で収まる。**ディスクは制約でない**。
- RAM は制約: パイロット時 `MemAvailable` は 365〜488 MiB で floor 1,536 MiB を
  下回り、3 点すべて native CaDiCaL 経路。p=2207 と並走させると二重に逼迫するため、
  §2.1 の直列ガードは RAM 防衛でもある。

## 4. チェーン script の検証(dry-run のみ、本実行なし)

- `bash -n` → 構文 OK。
- 実環境で `./w43-direct3251.sh` → **`rc=5`**:
  `REFUSING: audit_full_2207.py is still running`。実際に
  `pgrep -af 'audit_full_2207\.py'` で PID 15849/15864 が生きていることを確認。
  guard が期待どおり効いている。
- `DRY_RUN=1 ALLOW_CONCURRENT=1 ./w43-direct3251.sh` → `rc=0`。
  ログに `audit_full_3251.py --ds <65 範囲> --wall-budget 2400` の完全なコマンド行を
  記録。driver の `--help` も単体で `rc=0`(usage に `--ds/--budgets/--wall-budget/
  --native-ds/--mem-avail-floor-mib/--cross-check-ds/--recheck` を確認)。
- スタブ driver + 隔離ディレクトリで分岐を実測:

| ケース | 仕込み | 期待 | 実測 |
|---|---|---|---|
| A 陳腐な `todo=0` 行 + driver `rc=1` | 偽 ALL DONE を出さない | 1 | **1** |
| B 健全に `todo=0` + `rc=0` + progress 増 | 0 | 0 | **0** |
| C `todo=0` 行のみ、driver 失敗 | 1 | 1 | **1** |
| D `todo` 固定・progress 増(`REJECTED` 相当) | 2 回で stall → 4 | 4 | **4** |
| E 24 バッチ到達相当(`MAX_BATCHES=2` で代用) | 6 | 6 | **6** |
| F `unknown.json` 非空 | 7 | 7 | **7** |
| G `SAT FOUND` + driver `rc=3` | 3、バッチ 1 回で停止 | 3 | **3**(start 行 1 個) |

## 5. 投入手順(p=2207 完了待ち)

### 5.1 投入の合図となる条件

次の 3 つすべてが成立したときだけ投入する。script の guard が (1)(2) を機械判定する。

1. `pgrep -f 'audit_full_2207\.py'` が空。
2. `~/workspace/kyouen-omp/tasks/w31-direct2207.log` に
   `direct2207 ALL DONE` が現れる(w31 のチェーンが `exit 0` した証拠)。
3. p=2207 側の集約領収書が想定 d 数を満たしている(任意の最終確認)。

現時点(2026-11-17 15:11 UTC)の実測: p=2207 は **batch 3 実行中**、
領収書 286 レコード(d=292 まで)、`DS` 1,082 点に対する **残り 796 点**、
直近 batch 2 は 2,401 s で 105 d 消化。1 窓 ≈ 105 d なら **≈ 8 窓**残り
[INFERENCE: 難易度が d に依存するため幅を持つ]。

### 5.2 p=2207 の ALL DONE 確認方法

```sh
# 1. プロセスが消えたか
pgrep -af 'audit_full_2207\.py' || echo "no p2207 driver"

# 2. チェーンが ALL DONE を記録したか
grep 'ALL DONE' ~/workspace/kyouen-omp/tasks/w31-direct2207.log

# 3. todo が 0 か(最終 progress 行)
grep 'todo=' ~/workspace/kyouen-omp/full/research/experiments/parabola-p2207-no-equality-witness-20261107/output/p2207-drat-full/progress.log | tail -1

# 4. 領収書の d 集合が DS を覆ったか(実測 1,082 点)
python3 - <<'PY'
import json
OUT='/home/hatch/workspace/kyouen-omp/full/research/experiments/parabola-p2207-no-equality-witness-20261107/output/'
r=json.load(open(OUT+'drat_trim_audit_full_2207_92f0aa9575ed519d.json'))['records']
DS="2-49,51-99,101-149,151-199,201-249,251-288,290-296,298-299,301-311,313-323,325-399,401-499,501-549,551-599,601-699,701-799,801-899,901-999,1001-1099,1101-1102"
want=set()
for q in DS.split(','):
    a,b=q.split('-'); want.update(range(int(a),int(b)+1))
got={x['d'] for x in r if x['verdict']=='VERIFIED'}
print('receipts',len(r),'verified',len(got),'want',len(want),'missing',len(want-got))
PY
```

`missing 0` かつ `pgrep` 空かつ `ALL DONE` あり、で投入可。script は 1 と 2 を
自己判定するので、実務上は `nohup` で起動して `rc=5` でなければ投入成立。

### 5.3 投入コマンド

```sh
cd ~/workspace/kyouen-omp/tasks
nohup ./w43-direct3251.sh >> w43-direct3251.log 2>&1 &
echo $!          # 再投入 = 同じコマンドを再度 nohup(verified d は自動スキップ)
```

- `exit 6`(上限到達)や `exit 4`(stall)は**同一コマンド再実行で再開**。
  `exit 3`/`1`/`7` は再実行せず、ログを見て人間が判断する。
- 1 回目の起動で `rc=5` になるのは guard が働いた場合のみ。`ALLOW_CONCURRENT=1` は
  p=2207 の残余と意図的に並走させたい場合の非常口で、RAM 逼迫時は使わない。

## 6. チェーン完了時に揃う K0708 昇格の 4 条件

W41 §6 の 4 条件に対する、`w43-direct3251.sh` の `exit 0` 時点の到達点。

| # | 条件 | チェーン完了時に揃うか |
|---|---|---|
| 1 | 残り 1,541 d すべてに drat-trim 領収書があり `verdict=="VERIFIED"`、`input_sha256`・`proof_sha256`・`proof_gz_sha256` が再生成物と一致。集約領収書に重複なく 1,541 レコード | **揃う**。`todo=0` は「1,541 d すべてが `already_done` を通った」と同値で、その判定自体が `verdict=="VERIFIED"` かつ `proof_gz_sha256` の実 SHA 一致を要求する。`input_sha256`/`proof_sha256` は receipt 記録値で、RAW は削除済みのため**再生成による照合は別途必要**(下記の被覆スクリプトで行う) |
| 2 | 既存 84 件と合わせ 1,625 d 全数が DRAT 検証済み(`full_verified_coverage: true`) | **未検証のまま。完了直後に再集計が必要**。実測スクリプトで現在 `union 87 / 1625`(84 + pilot 3)を確認済み。完了時は `union == {1..1625}` になるはずだが、これは領収書を突き合わせないと確定しない |
| 3 | `unknown.json` が空(または存在しない) | **揃う**。非空ならチェーンが `exit 7` で止まるので、`exit 0` は空を意味する |
| 4 | K0708 の `status`・`evidence`・`artifacts` 更新 + AGENTS.md の統合前確認 | **チェーンの仕事ではない**。knowledge 編集と `check.py`/`build.py`/`git diff --exit-code -- README.md research/knowledge/generated` は完了後に人間/別作業で行う |

補足: 条件 2 の再集計は次の 1 コマンドで足りる(現時点の実測出力付き)。

```sh
python3 - <<'PY'
import json
OUT='/home/hatch/workspace/kyouen-omp/full/research/experiments/parabola-p2207-no-equality-witness-20261107/output/'
a=json.load(open(OUT+'drat_audit_full_3251_34249932790a9e9d.json'))['records']   # 84, incremental checker
b=json.load(open(OUT+'drat_trim_audit_full_3251_92f0aa9575ed519d.json'))['records']  # drat-trim
A={r['d'] for r in a if r.get('verified')}
B={r['d'] for r in b if r['verdict']=='VERIFIED'}
print('84-verified',len(A),'drat-trim-verified',len(B),'overlap',len(A&B),
      'union',len(A|B),'missing',len(set(range(1,1626))-A-B))
print('coverage_complete', (A|B)==set(range(1,1626)))
PY
# 現在: 84 84 0 87 1538 / False
# 完了時: 84 1541 0 1625 0 / True を期待
```

## 7. 限界・リスク

- §3 の外挿はパイロット 3 点(d=21..23、小 d 帯)の平均。proof サイズの d 依存が
  強ければ ±2 倍程度ずれ得る [INFERENCE]。ただし保存分 3.84 GB の 2 倍でも 8 GB 弱で、
  空き 116.1 GB に対して制約にならない。
- `MAX_BATCHES=24` は p=2207 実測レート(22.9 s/d)の 1.6 倍。d の難易度分布が
  p=2207 と違えば窓あたり消化数は変わる。`exit 6` は再投入で継続するので安全。
- 条件 1 の `input_sha256`/`proof_sha256` の再生成照合は、RAW proof を保存しない運用
  (W41 §7)のため完了直後にはできない。gz から展開して照合するか、gz SHA 一致を
  もって代用するかの判断が残る。本ログは「gz 一致は `already_done` が保証、
  RAW ハッシュは receipt 記録値のみ」と明示して残す。
- guard の `pgrep -f 'audit_full_2207\.py'` は文字列一致なので、無関係な
  `vim audit_full_2207.py` 等でも誤って `exit 5` になり得る。誤検知は安全側
  (起動しないだけ)なので許容する。

## 8. 結論

- パイロット 3 点は drat-trim VERIFIED、gz SHA 再計算一致、再投入で `todo=0` を
  実読で再確認した。`--ds` 範囲列は 1,541 点・重複 0・84 件と交差 0、
  全 1,625 d を被覆することを独立に再計算した。
- チェーン `tasks/w43-direct3251.sh` を新規作成した。p=2207 実行中は guard が
  `exit 5` で拒否(実環境で確認)。7 分岐すべてをスタブで実測し、期待終了コードと一致。
- ディスクはパイロット実測から **保存 3.84 GB / RAW 一時 17.1 GB**。W38 の
  1〜2 GB は下限見積で、実測ベースは 3.2 GB(gz のみ)。空き 116.1 GB で余裕。
- p=2207 は残り 796 d、直近 105 d / 40 分。`ALL DONE` を合図に `nohup` で投入する。
  完了時点で昇格条件 1・3 が揃い、2 は再集計、4 は knowledge 側の作業として残る。

(完)
