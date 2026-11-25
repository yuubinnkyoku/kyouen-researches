# 2026-11-16 p=2207 全量 DRAT 監査ドライバ実装とパイロット実行 (W31, omp)

W26 設計(`research/log/2026-11-12-p2207-full-audit-design-omp.md`)の実行フェーズの
第一段。再開可能な実行ドライバを実装し、未監査 d の先頭 5 点(d=2..6)を実際に
監査して drat-trim VERIFIED を確認した。全量実行はしていない(パイロットまで)。
数値はすべて保存済み JSON・ログからの転記。

## 0. 成果物

- ドライバ: `research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_2207.py`
  (実際の置き場所は W26 §2.3/§2.6 の指定どおり実験ディレクトリ配下)。
- 領収書(集約、drat-trim): `research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_trim_audit_full_2207_92f0aa9575ed519d.json`
- 1 d ごとの成果物: `.../output/p2207-drat-full/d<d>/` に
  `input.cnf.gz` / `proof.drat.gz` / `receipt.json` / `drat-trim.log` /(副チェック時)`drat-inc.log`。
- 進捗ログ(追記式): `.../output/p2207-drat-full/progress.log`
- 未決(UNKNOWN)記録: `.../output/p2207-drat-full/unknown.json`(パイロットでは未生成)。

## 1. 未監査 d の確定(実読による)

標本監査の領収書 `output/drat_audit_full_2207_34249932790a9e9d.json`(修正版チェッカー、
21 点)と `output/p2207_d_verdicts.json`(出所つき全 1103 d の verdict)を実読した。

- 全 1103 d、うち標本監査済み **21 点**: d = 1, 50, 100, 150, 200, 250, 289, 297, 300,
  312, 324, 400, 500, 550, 600, 700, 800, 900, 1000, 1100, 1103。
- 未監査 = `{1..1103} \ 標本21` = **1082 点**。出所(`p2207_d_verdicts.json` の `sources`)で
  内訳: `mp-phase-200k`(=d≤286 帯)が **277**、`cadical-log`(=d≥287 帯)が **802**、
  その他(`rechecked-20M`)は 0(すべて標本 21 点側)。W26 §1.4 の 280+802 と一致する
  (残差 3 は本パイロットの d=2,3,4 が 280 側から消化されたため。§4 参照)。
- 未監査 d を昇順に圧縮した範囲列(ドライバの `--ds` に渡す形):
  `2-49,51-99,101-149,151-199,201-249,251-288,290-296,298-299,301-311,313-323,325-399,401-499,501-549,551-599,601-699,701-799,801-899,901-999,1001-1099,1101-1102`

### 1.1 標本 21 点の実測(転記、drat-trim ではなく増分チェッカー版の領収書)

W6 標本は増分チェッカー(`drat_check_incremental.cpp`, SHA
`34249932790a9e9d...`)で監査済み。drat-trim 領収書ではない点に注意。
転記値: proof lines 合計 7,151,383(平均 340,542、中央値 397,402、最大 576,575)、
solve 合計 368.0 秒(平均 17.5、中央値 17.7、最大 37.3)、
check(増分)合計 9,637.1 秒(平均 458.9、中央値 296.6、最大 1,356.8)。
全 21 点 solver=UNSAT、rc=0、VERIFIED。

## 2. ドライバ `audit_full_2207.py` の仕様

W26 §2.1/§2.3/§2.6 の要件を実装する。

1 d あたり: `clauses_for_pair(2207, edges, d)` で CNF 生成(`p cnf 1103 31868`)→
DRAT 生成 → proof を gzip(mtime=0、`proof_sha256` と `proof_gz_sha256` を記録)→
**drat-trim 主チェッカー**で検証(`s VERIFIED` かつ exit=0 で VERIFIED)→
1 d ごとに領収書 JSON を原子的(`tmp` + `os.replace`)に書く。集約領収書も毎回原子的に
書き直す。判定は `verdict` / `checker` / `input_sha256` / `proof_sha256` /
`proof_gz_sha256` / `clauses` / `conflicts` / `conflict_budget` / `solve_seconds` /
`check_seconds` / `exit_code` / `checker_binary_sha256` を含む。

- **再開(スキップ)**: 再実行時 `verdict=="VERIFIED"` かつ `proof.drat.gz` の SHA が
  記録と一致する d はスキップ(実測: d=2..6 を再投入で `todo=0`、2 秒で `driver done`)。
- **進捗ログ**: `progress.log` へ 1 行追記(`d=... native=... reason=...`、
  `d=... verdict=...`)。判断根拠(native 切替理由)もここに残す。
- **SAT 即停止**: `solver_status=="SAT"` を検出したら receipt に `verdict:"SAT"` を書いて
  `SAT FOUND (counterexample to K0693)` をログし、exit code 3 で停止。K0693 の反例扱い。
- **native cadical 分岐**: 以下のいずれかで pysat 経路を捨て、native CaDiCaL
  (`cadical --binary=false -c <budget> input.cnf proof.drat`、proof をディスク直書き、
  RAM 非保持)へ切り替え、理由をログする。
  - `--native-ds` に指定された d(強制)。
  - `MemAvailable < --mem-avail-floor-mib`(既定 1536 MiB)。切替理由
    `MemAvailable=<n>MiB < floor=1536MiB` を progress.log に記録。
  - pysat が `MemoryError` を送出した場合。
- **衝突予算ラダー**: `--budgets`(既定 `5000000,20000000,100000000`)。UNKNOWN なら次の
  予算で再実行。全予算で決着しなければ `unknown.json` に記録し **領収書化しない**
  (W26 の「UNKNOWN は領収書化しない」に従う)。
- **副チェッカー(任意)**: `--cross-check-ds` の d にだけ増分チェッカーを追加実行し
  `cross_check` を記録(W26 の層化少数点方針)。全量適用は非現実的(§5)。
- **入力の固定**: `edges_2207.txt` は `$TEMP/p2207_drat/edges_2207.txt`、SHA
  `d1eb1385dce47715054f71ad4ffe7768dee44071eea5bbd0d5a4f8988e47c7f6` を起動時に検証。
  drat-trim バイナリ SHA `92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`
  も起動時に検証し、不一致なら exit 1。

### 2.1 使い方(パイロット相当)

```sh
cd ~/workspace/kyouen-omp/full
TEMP=$HOME/workspace/kyouen-omp/bin nice -n 10 uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_2207.py \
  --ds 2-6
```

### 2.2 全量実行の detached 起動(メインエージェント向け)

W26 の 40 分窓運用に合わせ、`--wall-budget` で区切り、外部から再起動する前提。
未監査範囲列(§1)を渡すだけで再開できる(済み d はスキップ)。

```sh
cd ~/workspace/kyouen-omp/full
DS='2-49,51-99,101-149,151-199,201-249,251-288,290-296,298-299,301-311,313-323,325-399,401-499,501-549,551-599,601-699,701-799,801-899,901-999,1001-1099,1101-1102'
nohup env TEMP=$HOME/workspace/kyouen-omp/bin nice -n 10 \
  uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_2207.py \
  --ds "$DS" --wall-budget 2400 \
  >> research/experiments/parabola-p2207-no-equality-witness-20261107/output/p2207-drat-full/driver.stdout.log 2>&1 &
echo $!  # PID; 再起動は同じコマンドを再実行するだけ(verified 済み d は自動スキップ)
```

- P=1 逐次。重い solve を同時に複数走らせない(`nice` 付き)。
- 再起動で失うのは最大 1 d 分(進行中 d は領収書が無いので再実行される)。
- exit code: 0=完走/窓到達、3=SAT(即時停止・要人間判断)、4=UNKNOWN 記録あり、1=前提不一致。

## 3. パイロット結果(d=2..6、実測転記)

`output/drat_trim_audit_full_2207_92f0aa9575ed519d.json` および `progress.log` より。

| d | solver | status | conflicts | budget | proof lines | proof bytes | solve (s) | check (s) | verdict |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| 2 | cadical-native | SOLVER_UNSAT | 119,751 | 5,000,000 | 464,466 | 29,007,199 | 21.71 | 23.31 | VERIFIED |
| 3 | cadical-native | SOLVER_UNSAT | 163,183 | 5,000,000 | 513,223 | 37,425,122 | 28.10 | 27.10 | VERIFIED |
| 4 | cadical-native | SOLVER_UNSAT | 147,781 | 5,000,000 | 467,922 | 31,273,267 | 19.40 | 17.40 | VERIFIED |
| 5 | cadical-native | SOLVER_UNSAT | 141,837 | 5,000,000 | 485,865 | 30,829,456 | 17.88 | 18.41 | VERIFIED |
| 6 | cadical-native | SOLVER_UNSAT | 37,085 | 5,000,000 | 258,404 | 11,849,731 | 4.58 | 4.91 | VERIFIED |

- 5 点すべて drat-trim `s VERIFIED`・exit=0・`proof.drat.gz` の再計算 SHA が記録と一致。
- check 合計 91.13 秒。solve 合計 91.7 秒。proof lines 合計 2,189,880。
- **全 5 点が native cadical 経路**。理由は progress.log に記録:
  `native=True reason=MemAvailable=537..658MiB < floor=1536MiB`。
  すなわちこの VM は同時期の他ワークフロー(§5)で常時 MemAvailable が floor 未満のため、
  実測では pysat(with_proof)経路は選ばれず、native 経路が既定になっている。
  pysat 経路と native 経路は W26 の両分岐として実装済みで、RAM に余裕が出れば
  pysat 経路が自動選択される。
- 副チェッカー(増分)はパイロットでは d=2 の former attempt(別プロセス)で 867.6 秒で
  VERIFIED を確認済み(集約領収書に取り込み済み。cross_check フィールド)。
  本パイロット本体(--cross-check-ds 無し)では増分チェッカーは走らせていない。
- d=2,3 は former attempt(同一 W31 セッションの初回試行)による記録。d=4 は初回試行が
  完走前に中断され残骸(`input.cnf`/`proof.drat`、receipt 無し)を残したため削除し、
  再実行して VERIFIED を得た(再開可能性の実地確認でもある)。

## 4. 残り d 数と所要見積

- 全 1103 d。標本監査済み 21 + 本パイロット済み 5 = **26 点監査済み**。
- 残り **1077 d**(= 1103 − 26)。出所内訳(`sources` 集計): d≤286 帯 275 + d≥287 帯 802。
  素の未監査 1082(275+802=1077 は d≤286 帯のパイロット 5 点 d=2..6 を除いた値に一致)。
- 見積(W26 §2.2 と同じ、標本 21 点の平均を残り 1077 に外挿):

| 量 | 標本平均 | ×1077 の見積 |
|---|---:|---:|
| solve 秒 | 17.5 | ≈ 5.2 時間 |
| drat-trim check 秒 | (標本は増分チェッカー) | — |
| 証明 lines | 340,542 | ≈ 367 M 行 |

- drat-trim 検証時間は W26 §2.2 の行/秒レート(W20 実測 8,584〜158,104 行/秒)を
  367 M 行に当てはめると **≈ 0.7〜11.9 時間**。
- よって全量は **solve ≈ 5 時間 + drat-trim 検証 ≈ 1〜12 時間**が見積もり。
  パイロット 5 点の drat-trim check は 1 d あたり 4.9〜27.1 秒と高速で、
  標本の増分チェッカー(4.9〜1,356.8 秒)より桁で速い。ただし d 依存の難易度
  (p=2647 の W 字型)により裾は伸び得る。

## 5. リスク・注意

- **RAM 逼迫**: 実測 MemAvailable が常時 1536 MiB 未満(377〜658 MiB を観測)。同時期に
  候補Aラダー W30(`cadical -c 10000000` 1 プロセス)と W29 設計(`ladder_drat.py`)が
  走っており、これが容量を占める。このため pysat(with_proof)経路は選ばれず
  native 経路が既定。W26 の「重いプロセス同時数 ≤ 2」を守る(P=1 逐次 + nice)。
  RAM が空けば pysat 経路へ自動復帰する。
- **UNKNOWN の残存**: 予算 5M で UNKNOWN になる d があり得る(d=289,297,312,324 は
  20M で決着した実績)。ラダーは既定で 5M→20M→100M を試み、それでも駄目なら
  `unknown.json` に落とす(領収書化しない)。
- **SAT が出た場合**: K0693 の反例。ドライバは即停止し exit 3・ログする。人間の判断が要る。
- **drat-trim レートの大きな幅**: 証明の質依存(W20 で 18 倍の開き)。§4 の検証見積は幅で読む。
- **外挿の限界**: 標本は d について一様配置だが難易度が一様とは限らない。標本 check 秒は
  0.0〜1,356.8 と既に裾が広い。
- **証明・CNF のディスク量**: テキスト DRAT は 1 行 ≈ 25〜30 B とすると 367 M 行 ≈ 9〜11 GB
  RAW(gzip 後 2〜3 GB)。`output/p2207-drat-full/d<d>/` に gzip 保存し、RAW は検証後破棄する。

## 6. 次手(本タスク外)

- §2.2 の detached コマンドで残り 1077 d を昇順に消化する。
- 完了後、全 d(標本 21 + 本監査 1082)の drat-trim VERIFIED 領収書が揃うことを条件に
  K0693 を `computed` へ昇格できる(W26 §4)。本タスクでは knowledge 項目を編集しない。

(完)
