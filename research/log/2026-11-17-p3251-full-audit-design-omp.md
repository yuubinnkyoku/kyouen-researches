# 2026-11-17 p=3251 全量 DRAT 監査(1,541 d)の設計 (W38, omp)

本ログは設計のみを記述する。監査は実行していない。数値はすべて保存済み JSON・
ログ・本日実行の直接計測からの転記であり、外挿には [INFERENCE] を付す。
push はしない。

## 0. 対象と前提

- 目的: K0708(p=3251 では剰余放物線の等号 `A(p)=(p+3)/2` を達成する証人が無い、
  status `needs-review`)の信頼境界「UNSAT はソルバ主張」を、全 d の DRAT 監査で閉じる。
- K0334 により等号は「ある d について signed NAE3/4 と原点節の CNF が充足可能」と
  同値。監査対象は d=1..1625(h=(3251-1)/2=1625)の各 CNF の UNSAT 主張。
- 全 1625 d のソルバ側走査は済み: `parabola-equality-extension-2143-2500-20261107/
  output/deep_scan_3251.json`(衝突予算 20 万、UNSAT 1625・unknown 0・SAT 0、
  4,694 秒、`scan_mp.py` 4 並列)。

## 1. 未監査集合の正確な定義

### 1.1 既監査 84 件の同定

- 領収書: `research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_audit_full_3251_34249932790a9e9d.json`
  (修正版増分チェッカー `drat_check_incremental.cpp`、ソース SHA-256
  `34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b`)。
  実読: **84 レコード**、全レコード solver=UNSAT・checker_rc=0・VERIFIED。
- 84 d の内訳(実読): **d=1..20 の連続 20 点** + **計画標本
  d=26,51,76,...,1601(25 刻み 64 点)**。すなわち計画標本
  `d=1,26,...,1601`(65 点)は 65/65 完了、さらに標本外の d=2..20 が監査済み。
  K0708 の記述(70 d → 追記で 84 d、標本 65/65)と整合。
- 補助証拠: `research/experiments/parabola-audit-coverage-20261109/inventory.json`
  (commit `87e28af` 時点では 70 d / 未被覆標本 14 点と記録。HEAD の領収書は
  84 d まで追記済みで、上記の実読が現在の正である)。
- 注意: この 84 件は **増分チェッカー** による監査であり drat-trim ではない。
  p=2207 の W26/W31 と同じ扱い(標本は既監査と数え、主チェッカーは drat-trim)
  に従い、84 件は再監査せず残り 1,541 件を drat-trim で監査する。

### 1.2 残り 1,541 d

- 未監査 = `{1..1625} \ 既監査84` = **1,541 点**(実読で確認)。
- 昇順の範囲列(ドライバの `--ds` に渡す形):

```
21-25,27-50,52-75,77-100,102-125,127-150,152-175,177-200,202-225,227-250,252-275,277-300,302-325,327-350,352-375,377-400,402-425,427-450,452-475,477-500,502-525,527-550,552-575,577-600,602-625,627-650,652-675,677-700,702-725,727-750,752-775,777-800,802-825,827-850,852-875,877-900,902-925,927-950,952-975,977-1000,1002-1025,1027-1050,1052-1075,1077-1100,1102-1125,1127-1150,1152-1175,1177-1200,1202-1225,1227-1250,1252-1275,1277-1300,1302-1325,1327-1350,1352-1375,1377-1400,1402-1425,1427-1450,1452-1475,1477-1500,1502-1525,1527-1550,1552-1575,1577-1600,1602-1625
```

(検証済み: 上記 65 範囲の和集合はちょうど 1,541 点であり、既監査 84 d との
和集合が `{1..1625}` と完全一致することを本日スクリプトで確認した。)

## 2. p=2207 ドライバの流用可能性(実コード確認)

流用元: `research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_2207.py`
(W31 実装、再開可能・SAT 即停止・native 分岐・予算ラダー実装済み)。
実読の結果、変更箇所は以下に限られる:

| 箇所 | 現行(p=2207) | 変更後(p=3251) |
|---|---|---|
| `P = 2207`(49 行目) | 2207 | **3251** |
| `EDGES_SHA`(51 行目) | `d1eb1385...`(edges_2207.txt) | **edges_3251.txt の新規 SHA**(下記) |
| `FULL = OUT / "p2207-drat-full"` | p2207-drat-full | **`p3251-drat-full`** |
| `RECEIPTS = OUT / f"drat_trim_audit_full_{P}_..."` | drat_trim_audit_full_2207_* | **drat_trim_audit_full_3251_***(P 変数で自動) |
| `PROCEDURE` 辞書(64-80 行目) | p=2207 の手順記述 | p=3251 向けの記述(CNF ヘッダ等) |

- `H = (P - 1) // 2` は自動(1625)。`parse_ds`・`dimacs`・領収書の原子書き込み・
  `already_done`(VERIFIED + proof_gz SHA 一致でスキップ)・`solve_pysat`・
  `solve_native`(native cadical `--binary=false` ディスク直書き)・
  `check_drat_trim`・`cross_check_incremental`(ソース SHA 検証付き)・
  予算ラダー `--budgets 5000000,20000000,100000000`・`--wall-budget`・
  exit code 規約(0/1/3/4)はすべてそのまま流用可能。
- チェッカー・ソルバの固定もそのまま: drat-trim バイナリ
  `~/workspace/kyouen-omp/tasks/drat-trim-src/drat-trim`
  (SHA-256 `92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`)、
  native CaDiCaL `~/workspace/kyouen-omp/bin/cadical-src/build/cadical`、
  増分チェッカー `drat_check_incremental.cpp`(SHA `34249932...`、副チェック用)。

### 2.1 辺リストの固定(p=3251 ではまだ凍結ファイルが無い)

実測(本日、`forbidden_edges.exe 3251` を直接実行):

- edges 生成に **117.8 秒**、**1,379,766 辺**。
- `~/workspace/kyouen-omp/bin/kyouen-parabola/` には `edges_101/2207/2531/2647.txt`
  はあるが **`edges_3251.txt` は存在しない**。W26 は固定 edges ファイルと SHA
  検証を前提としているため、p=3251 では初回に
  `forbidden_edges.exe 3251 > edges_3251.txt` で生成・SHA-256 を記録し、
  `EDGES_SHA` として固定する(生成は決定的な単一バイナリ出力なので
  SHA 一致で再現検証できる。p=2207 で `p2207_drat/edges_2207.txt` と
  `kyouen-parabola/edges_2207.txt` が同一 SHA だった前例と同じ運用)。

### 2.2 CNF サイズの実測

本日 `clauses_for_pair(3251, edges, d)` を直接呼び出し:

- d=1: **`p cnf 1625 60266`**(変数 1,625・節 60,266)
- d=813: 節 60,266(d によらず同一の節数 [INFERENCE: d=1 と d=813 の 2 点
  でのみ確認。W26 の p=2207 も全 d で 31,868 と固定だったことからの類推も補強])

p=2207(31,868 節)の約 1.9 倍。1 d あたりの DIMACS は数 MB 級で RAM・ディスク
とも問題なし。

## 3. 計算量とディスクの見積もり(外挿、根拠明示)

### 3.1 既存 84 件サンプルの実測(領収書 JSON からの転記)

- solve 合計 609.9 秒(平均 **7.3 秒**、中央値 7.2、最大 28.5)
- 増分チェッカー check 合計 28,038.2 秒(平均 **333.8 秒**、中央値 337.0、最大 849.2)
- proof lines 合計 11,259,981(平均 **134,047**、中央値 146,881、最大 219,183)
- 84 点すべて solver=UNSAT・VERIFIED。d≥26 の 64 点だけでも平均はほぼ同じ
  (solve 7.6 秒、check 332.5 秒、lines 135,550)ため、標本の偏りは小さい。

### 3.2 残り 1,541 d への外挿 [INFERENCE]

| 量 | 84 点平均 | ×1,541 の見積 |
|---|---:|---:|
| solve 秒 | 7.3 | **≈ 3.1 時間** |
| proof lines | 134,047 | **≈ 206.6 M 行** |
| 増分チェッカー check 秒 | 333.8 | ≈ 142.9 時間(非現実的、下記) |

- 増分チェッカーの全量適用は ≈143 時間かかるため不可。**drat-trim を主チェッカー**
  とし、増分チェッカーは層化少数点(各 100 d 帯から数点)のクロスチェックに限定
  (W26 §2.2 と同じ設計判断)。
- drat-trim の check 時間は行/秒レートで見積もる。根拠となる実測レート:
  - W31 パイロット(p=2207、d=2..6、drat-trim 実測):
    19.9k / 18.9k / 26.9k / 26.4k / 52.6k 行/秒
  - W20(p=2647)の 3 クラス: 8.6k〜158.1k 行/秒
- 206.6 M 行 ÷ 上記レート → **≈ 0.4〜6.7 時間**(W31 レート 19k〜53k だけで
  縮めると ≈ 1.1〜3.0 時間)[INFERENCE: レートは証明の質に強く依存し 18 倍の
  開きが観測済みのため幅で読む。p=3251 は CNF が 1.9 倍大きく、84 点の
  lines/d は p=2207 標本(平均 340,542)より小さいため、難易度の裾が
  p=2207 より軽い可能性があるが保証はない]。
- 合計の中央的見積: **solve ≈ 3 時間 + drat-trim 検証 ≈ 1〜7 時間**。
  W31 パイロット並みに安定すれば 1 日の 40 分窓バッチで数日〜1 週間で完了する
  規模 [INFERENCE]。

### 3.3 ディスク

- テキスト DRAT 1 行 ≈ 25〜30 B(W26 と同じ仮定)→ 206.6 M 行 ≈
  **RAW 5〜6 GB、gzip 後 ≈ 1〜2 GB** [INFERENCE]。
  実測 `df -h`: `/home/hatch` は 150 GB 中 **109 GB 空き**(2026-11-17)。
  `output/p3251-drat-full/d<d>/` への gzip 保存は十分可能。RAW は検証後破棄。
- RAM: 84 点の最大 proof は 219,183 行(≈ 6 MB 級)で pysat の RAM 保持にも
  問題ないが、W31 と同様 `MemAvailable < 1536 MiB` で native cadical へ自動分岐
  する(実測 2026-11-17: MemAvailable 422 MiB、4 コア・7.9 GiB。現在も逼迫)。

## 4. 実行手順

### 4.1 バッチ分割と再起動耐性(W26/W31 踏襲)

- **1 d = 1 サブプロセス**。1 d 完了ごとに `receipt.json` を原子的(tmp +
  `os.replace`)に書き、集約領収書 `drat_trim_audit_full_3251_92f0aa9575ed519d.json`
  も毎回原子書き換え。再起動で失うのは最大 1 d 分。
- 再実行は同じ `--ds` を渡すだけ。`verdict=="VERIFIED"` かつ `proof.drat.gz` の
  SHA が記録と一致する d は自動スキップ(W31 で d=2..6 の再投入が `todo=0`・
  2 秒で完了した実績)。
- `--wall-budget 2400`(40 分窓)。84 点サンプルの最大 check(増分)は 849.2 秒、
  drat-trim は桁で速いため大半の d は solve+check 合計で窓に収まる
  [INFERENCE: 裾の重い d は窓を超え得るが、失うのはその 1 d の再実行のみ]。
- **P=1 逐次 + `nice -n 10`**。重い外部プロセス(cadical / drat-trim)の同時数は
  他ワークフロー(現行: p=2207 全量監査ドライバ、W30 ラダー等)と合わせ
  「最大 2」を維持。p=2207 全量監査と同時に走らせる場合はどちらかを優先し、
  競合時間帯は後回し(再開可能性により損失なし)。
- 起動コマンド(W31 §2.2 と同じ形、DS は §1.2 の範囲列):

```sh
cd ~/workspace/kyouen-omp/full
DS='21-25,27-50,...(§1.2 の範囲列)...,1602-1625'
nohup env TEMP=$HOME/workspace/kyouen-omp/bin nice -n 10 \
  uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_3251.py \
  --ds "$DS" --wall-budget 2400 \
  >> research/experiments/parabola-p2207-no-equality-witness-20261107/output/p3251-drat-full/driver.stdout.log 2>&1 &
echo $!  # 再起動は同一コマンド再実行のみ(verified 済み d は自動スキップ)
```

- exit code 規約(W31 と同じ): 0=完走/窓到達、3=**SAT(即時停止)**、
  4=UNKNOWN 記録あり、1=前提不一致(edges SHA・drat-trim SHA 不一致)。

### 4.2 SAT が出た場合の即時停止ルール

- ドライバは `solver_status=="SAT"` を検出したら receipt に `verdict:"SAT"` を
  書き、`SAT FOUND (counterexample to K0708)` をログし **exit 3 で即時停止**。
- これは単なる監査失敗ではなく **K0708 の反例**(等号達成の証人発見)であり、
  `deep_scan_3251.json` の全 1625 d UNSAT 主張(予算 20 万)との矛盾になる。
  人間の判断を要するため、以降の d は一切実行しない。停止時点の
  CNF・proof・receipt(`input.cnf.gz`・`proof.drat.gz`・`receipt.json`)が
  証人候補の検証材料になる。

### 4.3 UNKNOWN の扱い

- 予算ラダー `--budgets 5000000,20000000,100000000`。全予算で決着しない d は
  `unknown.json` に記録し **領収書化しない**(W26/W31 と同じ)。p=3251 は
  予算 20 万ですでに全 1625 d が UNSAT になっている実績があるため、5M 予算で
  UNKNOWN になる確率は低い [INFERENCE]。

## 5. 完了時に昇格できる知識項目と条件

- 対象: **K0708**(`research/knowledge/items/K0708-p3251-no-parabola-equality-witness.md`)
  を `needs-review` → `computed` へ昇格。
- 条件(すべて満たした場合のみ):
  1. 残り 1,541 d すべてについて drat-trim 領収書が `verdict=="VERIFIED"` で
     `input_sha256`・`proof_sha256`・`proof_gz_sha256` が再生成物と一致
     (`drat_trim_audit_full_3251_92f0aa9575ed519d.json` に重複なく 1,541 レコード)。
  2. 既存 84 件(増分チェッカー領収書)と合わせ 1625 d 全数が DRAT 検証済み
     であることを inventory 系の再集計で確認
     (`parabola-audit-coverage-20261109/inventory.py` 相当の被覆検査で
     `full_verified_coverage: true`)。
  3. `unknown.json` が空(または存在しない)。
- 昇格時の更新: K0708 の `status`・`evidence`・`artifacts`(drat-trim 集約領収書
  と driver を追加)を更新し、AGENTS.md の統合前確認
  (`uv run --locked python tools/knowledge/check.py`・`build.py`・
  `git diff --exit-code -- README.md research/knowledge/generated`)を実行する。
- K0101(全奇素数で等号)は既に K0706(p=2647 全数監査)で反証済みのため、
  K0708 の昇格は K0101 の status を変えない(supports relation の裏付けを
  強めるのみ)。K0706 と同じ「全数監査済み」クラスに 3251 が加わる。

## 6. 限界・リスク

- §3 の外挿は既監査 84 点(計画標本 + d=2..20)の平均に基づく。難易度が d に
  構造を持つ場合(p=2647 の W 字型)は平均外挿がずれ得る [INFERENCE]。
  ただしサンプルは 25 刻みで全域(d=26..1601)を一様に押さえている。
- 既監査 84 件は増分チェッカーのみで drat-trim を通していない。p=2207 の
  W26/W31 でも標本 21 点は同様の扱いであり、層化クロスチェックで主張を補強する。
  全 d を drat-trim で通すことが昇格条件ではない(84 点は K0707 修正版チェッカー
  による VERIFIED 領収書として既に有効)。
- drat-trim レートの 18 倍の開き(W20 実測)により検証時間見積は幅を持って読む。
- VM の RAM 逼迫(実測 MemAvailable 422 MiB)は W31 と同様に native cadical
  経路を既定にさせる。p=2207 全量監査が並走している場合、CPU・ディスク I/O
  競合で 40 分窓あたりの消化 d 数が落ちる。同時重いプロセス ≤ 2 を守る。

## 7. 結論

- 監査対象の全容: 全 1,625 d、既監査 84 点(増分チェッカー、領収書
  `drat_audit_full_3251_34249932790a9e9d.json`)、残り **1,541 d**(§1.2 の範囲列)。
- ドライバ: `audit_full_2207.py` をコピーし、`P=3251`・`EDGES_SHA`(新規
  edges_3251.txt)・出力ディレクトリ名・`PROCEDURE` を変更するだけで流用可能。
  edges_3251.txt は初回に `forbidden_edges.exe 3251` で生成・SHA 固定
  (1,379,766 辺、生成 117.8 秒の実測)。
- 見積: solve ≈ 3.1 時間、drat-trim 検証 ≈ 1〜7 時間(レート依存)、
  証明 gzip ≈ 1〜2 GB(空き 109 GB)。40 分窓の P=1 逐次バッチで数日規模
  [INFERENCE]。
- 完了後、1625 d 全数の DRAT 検証被覆が揃い次第 K0708 を `computed` へ昇格
  (§5 の条件)。

(完)
