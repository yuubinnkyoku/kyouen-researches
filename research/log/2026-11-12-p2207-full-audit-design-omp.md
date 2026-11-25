# 2026-11-12 p=2207 全量 DRAT 監査(1,082 d)の設計 (W26, omp)

本ログは設計のみを記述する。監査は実行していない。数値はすべて保存済みの
JSON・ログからの転記であり、見積もりは見積もりと明記し外挿の根拠を付す。

## 0. 対象と前提

- 目的: K0693(p=2207 では剰余放物線の等号 `A(p)=(p+3)/2` を達成する証人が無い、
  status `needs-review`)の信頼境界「UNSAT はソルバ主張」を、全 d の DRAT 監査で閉じる。
- 等号は K0334 により「ある d について signed NAE3/4 と原点節の CNF が充足可能」と同値。
  監査対象は d=1..1103(h=1103)の各 CNF の UNSAT 主張。
- 現状の被覆: **21 / 1103**(後述)。残り **1,082 d**。K0693 は全数監査未完のため
  `needs-review` のまま(`research/knowledge/items/K0693-p2207-no-equality-witness.md`)。

## 1. W6 サンプル監査の全体像

### 1.1 記録の所在

- 標本監査の実行記録(残り 9 点): `research/log/2026-11-09-p2207-sample-reaudit-complete.md`
- 確定状態の集計: `research/log/2026-11-09-drat-reaudit-status-omp.md`
- 領収書 JSON(修正版チェッカー): `output/drat_audit_full_2207_34249932790a9e9d.json`
  (SHA-256 `0a77846a730cdc96d5818a8a8a4e76550815e15f9910496b9f58031b9987bd00`)
- 旧版チェッカーの領収書: `output/drat_audit_full.json`
  (SHA-256 `b8a62d3243519b205667a067a214938adfc101e6ea130edb75011ee4d3495c6d`)
- ドライバ: `research/experiments/parabola-p2207-no-equality-witness-20261107/audit_sequential.py`
  (SHA-256 `e0ec68fd43c2cbe90975f3cea6f023b4de137fc63a056eca0a4ff5553cd2f002`)、
  チェッカー: `drat_check_incremental.cpp`(SHA-256
  `34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b`、K0707 の修正版)。
- W6 の実行ログ: `~/workspace/kyouen-omp/tasks/W6-output.log`(9 点の逐次実行、
  全件 verified、check 秒合計 ≈ 1,687 秒)。
- W6 標本の一覧は 2 つの JSON で一致: d = 1, 50, 100, 150, 200, 250, 289, 297, 300,
  312, 324, 400, 500, 550, 600, 700, 800, 900, 1000, 1100, 1103 の **21 点**。

### 1.2 入力 CNF と証明の所在

- CNF 生成: `parabola_half_bound.clauses_for_pair(p=2207, edges, d)`。
  ソース上 `clauses_for_pair(p, edges, double)` の第 3 引数は `double`(対の番号)であり、
  各辺 `t` について `min(t, p-t)==double` を満たす点を要件から除外する
  (=その対を「どちらも選ばない」空対に固定する)。`build_inventory.py` は
  d=1..1103(=h)を列挙しており、本設計でも同じ d を監査単位とする。d=1 で
  **`p cnf 1103 31868`**(変数 h=1103、節 31,868)を確認。
- 辺入力: `~/workspace/kyouen-omp/bin/p2207_drat/edges_2207.txt` と
  `~/workspace/kyouen-omp/bin/kyouen-parabola/edges_2207.txt` は **同一**
  (639,621 行、SHA-256 `d1eb1385dce47715054f71ad4ffe7768dee44071eea5bbd0d5a4f8988e47c7f6`)。
  先頭行 `0 46 1080 1081`。
- **証明・CNF は保存されていない**: `audit_sequential.py` は各 d の検証後に
  `output/` の一時 CNF と `proof.drat` を `unlink` するため、標本 21 点の
  証明・CNF は残っていない。全量監査では証明・CNF を再生成する必要がある。
  (W20 の p=2647 クラス監査は `output/w20-drat-1322/class-*/input.cnf.gz` /
  `proof.drat.gz` として保存しており、p=2207 で流用できる保存形式の参照例。)

### 1.3 標本の実測値(修正版チェッカーの領収書 JSON より転記)

| d | proof lines | solve (s) | 増分チェッカー check (s) |
|---:|---:|---:|---:|
| 1 | 16 | 0.0 | 1.0 |
| 50 | 206,079 | 22.0 | 395.2 |
| 100 | 354,155 | 34.0 | 1,356.8 |
| 150 | 402,086 | 23.3 | 472.6 |
| 200 | 129,586 | 15.5 | 126.5 |
| 250 | 499,634 | 24.4 | 823.9 |
| 289 | 507,181 | 27.0 | 987.9 |
| 297 | 518,463 | 30.0 | 1,020.2 |
| 300 | 309,488 | 28.6 | 976.6 |
| 312 | 431,671 | 20.4 | 746.9 |
| 324 | 522,426 | 37.3 | 1,010.8 |
| 400 | 111,575 | 3.3 | 31.6 |
| 500 | 576,575 | 16.4 | 425.7 |
| 550 | 503,678 | 17.7 | 296.6 |
| 600 | 397,402 | 16.2 | 195.0 |
| 700 | 479,766 | 14.7 | 259.4 |
| 800 | 498,210 | 17.8 | 288.1 |
| 900 | 240,705 | 6.4 | 81.5 |
| 1000 | 248,333 | 7.1 | 78.4 |
| 1100 | 214,260 | 5.9 | 62.4 |
| 1103 | 94 | 0.0 | 0.0 |

集計(21 点): proof lines 合計 7,151,383(平均 340,542、中央値 397,402)、
solve 合計 368.0 秒(平均 17.5、中央値 17.7、最大 37.3)、
増分チェッカーの check 合計 9,637.1 秒(平均 459、中央値 296.6、最大 1,356.8)。
すべて solver=UNSAT、checker_rc=0、VERIFIED。衝突予算は既定 5,000,000。

旧版(`drat_audit_full.json`)は同一 21 d・同一 proof lines だが check 合計
28,797.7 秒(中央値 1,299.2)で、修正版は約 3 倍速い。標本の被覆数には加えない。

### 1.4 残り 1,082 d の内訳

`output/p2207_d_verdicts.json` の出所(`sources`)による分類(全 1103 d):

| 出所 | 全体 | うち標本 21 点を除いた残り |
|---|---:|---:|
| `mp-phase-200k`(d=1..286、200k 予算のマルチプロセス) | 286 | 280 |
| `cadical-log`(d=287..1103、cadical ログ判定) | 813 | 802 |
| `rechecked-20M`(d=289, 297, 312, 324、20M で再判定) | 4 | 0 |
| 合計 | 1,103 | **1,082** |

標本 21 点の配置: d≤286 に 6 点(1, 50, 100, 150, 200, 250)、d≥287 に 15 点。
残り 1,082 の内訳は上の表のとおり d≤286 が 280、d≥287 が 802。
d=1103 は標本に含まれる(残り側にはない)。

## 2. 全量監査の設計

### 2.1 手順(1 d あたり)

1. **CNF 生成**: `clauses_for_pair(2207, edges, d)` を d ごとに呼ぶ。
   辺は `edges_2207.txt`(SHA-256 `d1eb1385...`)を固定使用。DIMACS ヘッダは
   `p cnf 1103 <節数>`、節は決定的に再現可能。
2. **証明生成**(主経路 = pysat Cadical195): `Cadical195(bootstrap_with=clauses,
   with_proof=True).solve_limited()` を衝突予算付きで実行し、`get_proof()` の
   テキスト DRAT を `proof.drat.gz`(gzip, mtime=0)に保存。標本の証明は
   ≤ 576,575 行(数十 MB 級)で RAM に収まる(pysat の proof はリスト保持)。
   - 主経路の W20 での実績: `with_proof=True` のテキスト DRAT を drat-trim が
     そのまま VERIFIED した(後述)。
3. **検証**(主チェッカー = drat-trim): `drat-trim input.cnf proof.drat`
   (テキスト DRAT はオプション無し。バイナリ DRAT は `-i`)。
   ログの `s VERIFIED` と exit=0 の両方で VERIFIED と判定。
   - 検証器: `~/workspace/kyouen-omp/tasks/drat-trim-src/drat-trim`
     (https://github.com/marijnheule/drat-trim、commit
     `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`、`gcc drat-trim.c -std=c99 -O2`)。
     バイナリ SHA-256 `92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`。
   - 参考速度(W20、p=2647、テキスト DRAT、2026-11-12):
     (0,0,1) 22,379 行 → 0.425 秒、(1,0,2) 790,206 行 → 4.998 秒、
     (0,1,2) 2,143,709 行 → 249.726 秒。3 クラスすべて VERIFIED。
4. **副チェッカー(任意のクロスチェック)**: 修正版 `drat_check_incremental.cpp`
   (SHA-256 `34249932790a9e9d...`)でも検証し、両チェッカーの判定一致を記録。
5. **領収書**: 1 d ごとに原子的追記(既存 `audit_sequential.py` の
   `save()` = 一時ファイル + `os.replace` と同方式)。記録項目は
   d / solver_status / conflict_budget / conflicts / solve_seconds /
   proof_lines / proof_sha256 / input_sha256 / checker(名前・ソース SHA・
   バイナリ SHA)/ check_seconds / exit_code / verdict とする。
   - 領収書パス: 増分チェッカーは既存の `output/drat_audit_full_<p>_<sha16>.json`
     を踏襲。drat-trim 用は `output/drat_trim_audit_full_2207_<sha16>.json`
     を新設し、checker を混同しない(既存の drat_audit_full は増分チェッカーの
     領収書である)。
6. **証明・CNF の保存**: `output/p2207-drat-full/d<d>/` に
   `input.cnf.gz`(SHA 記録)・`proof.drat.gz`(SHA 記録)・`receipt.json` を置く。
   W20/W28 と同じくバイナリは push 対象外、SHA でバイト単位再生成可能とする。

### 2.2 総コストの見積もり(外挿、根拠明記)

標本 21 点の平均値を残り 1,082 d に外挿する(標本は d に対して一様配置、
ただし難易度は一様とは限らない。§3 の限界参照)。

| 量 | 標本平均 | ×1,082 の見積 |
|---|---:|---:|
| proof lines | 340,542 | **≈ 368.5 M 行** |
| solve 秒 | 17.5 | **≈ 5.3 時間** |
| 増分チェッカー check 秒 | 459 | **≈ 137.9 時間(≈ 5.7 日)** |

drat-trim の check 時間は、W20 の 3 クラスで観測した行/秒レートを標本の
proof lines に当てはめた範囲で見積もる(レートは証明の質により大きく異なる):

| 想定レート(行/秒) | 出所 | 368.5 M 行の見積 |
|---:|---|---:|
| 8,584 | W20 (0,1,2) の実測 | ≈ 11.9 時間 |
| 52,656 | W20 (0,0,1) の実測 | ≈ 1.9 時間 |
| 158,104 | W20 (1,0,2) の実測 | ≈ 0.7 時間 |

すなわち **solve ≈ 5 時間 + drat-trim 検証 ≈ 1〜12 時間**(レート依存)が
中央的な見積もり。増分チェッカーを副チェッカーとして全 d に走らせると
**さらに ≈ 138 時間**かかるため、副チェッカーの全量適用は非現実的。
設計判断: **drat-trim を主チェッカーとし、増分チェッカーは層化少数点
(例: 各 100 d 帯から数点)のクロスチェックに限定する**。これは W20 の
(0,1,2) が増分チェッカーでは 3,600 秒タイムアウトしたため drat-trim 単独
領収書となった前例、および W28 の流儀(drat-trim 主)とも整合する。

証明のバイト量: テキスト DRAT を 1 行 ≈ 25〜30 B と仮定すると
368.5 M 行 ≈ 9〜11 GB RAW(gzip 後 ≈ 1/5、2〜3 GB)。`/home/hatch` は
150 GB 中 120 GB 空き(実測)であり、gzip 保存は可能。RAW は検証後破棄する。

### 2.3 バッチ分割と再開可能性

- VM 再起動は約 2 時間おき、時に 40 分間隔。**1 バッチを 40 分窓に収める**のを
  安全側の目標とする。
- 標本の最大 check は 1,356.8 秒(≈ 22.6 分、d=100、増分チェッカー)。
  drat-trim はこれより速いため、**大半の d は solve+check 合計で 40 分窓に収まる**。
  ただし重い tail(proof lines の裾)は窓を超え得る。
- 設計: **1 d = 1 サブプロセス**で実行し、各 d 完了ごとに領収書を原子的追記する。
  再起動は最大 1 d 分の作業しか失わない(進行中の d は領収書が無いので再実行)。
  呼び出し側は d の昇順リストを渡し、**verified 済みの d はスキップ**(既存
  `audit_sequential.py` の `todo = [d for d in ds if saved.get(d, {}).get("verified")
  is not True]` と同じ再開機構)。
- 再起動後の再開手順は 1 コマンドで完結させる(残り d のリストを再度渡すだけ)。
  逐次実行を必須とし、同時に重い solve を複数走らせない(W28 の注意点と同じ)。
- 完了の判定: 領収書の `verdict=="VERIFIED"` かつ `input_sha256`・
  `proof_sha256` が再生成物と一致すること。

### 2.4 候補Aラダーとの CPU 競合の扱い

- マシンは 4 コア、RAM 7.9 GiB(実測 `MemTotal: 8124900 kB`)。
  2026-11-16 13:39 時点で `MemAvailable` ≈ 2.4 GB、load average ≈ 1.9。
- 同時期に走っている重い作業(2026-11-16 13:39 の `ps` 実測): 候補Aラダー
  W30(`ladder113_driver.sh` / native cadical、
  `cadical -c 10000000 ... proof.drat` が 1 プロセス)と
  W29 の SAT 側攻撃設計(`ladder_drat.py --d 1258 --budget 10000000`)。
  ラダーは solve(cadical)+drat-trim で約 2 コアを使う。
- 方針: **p=2207 全量監査は P=1 の逐次実行**とし、`nice` を付ける。
  重い外部プロセス(cadical / drat-trim / ladder_drat)の同時数を
  「ラダー + 監査 = 最大 2」に制限する。RAM は CNF が 31,868 節・
  証明が数十 MB 級のため per-d の追加消費は小さく、ラダーの
  ~1 GB RSS と共存可能。競合が激しい時間帯は監査を後回しにしてよい
  (再開可能性により損失は出ない)。
- ラダー完了(または停止)後に P を 2〜3 に上げてよいが、その場合も
  同時 solve 数は 1 を保つ(証明生成は単一プロセス、検証のみ並列化)。

## 3. 限界・リスク

- 外挿は標本 21 点(一様配置)の平均に基づく。難易度が d について構造を持つ場合
  (p=2647 では k=h−d に対し W 字型の難易度が観測されている)は平均外挿が
  ずれ得る。標本の check 秒は最小 0.0〜最大 1,356.8 と既に裾が広い。
- 標本は衝突予算 5,000,000 で solve した。d=289, 297, 312, 324 は shallow 走査で
  30 秒タイムアウトした後、20M 予算で 20.7〜31.6 秒で決着した実績があり、
  予算 5M では UNKNOWN に落ちる d が残りに存在し得る。その場合は予算ラダー
  (5M → 20M → 100M)で再実行する(UNKNOWN は領収書化しない)。
- もし証明生成が SAT を返したら K0693 の反例であり、単なる監査失敗ではない。
  その場合は即座に停止して記録する(全 1103 d の既存 verdict は UNSAT)。
- pysat の proof は RAM 保持のため、重い d で証明が巨大化すると RAM を圧迫する。
  その場合の代替は native cadical(`--binary=false` のテキスト、またはバイナリ
  出力 + drat-trim `-i`)に切り替え、RAM を消費せずディスクへ直接書く
  (W30 のラダードライバ `ladder113_driver.sh` がこの方式)。
- drat-trim のレートは証明の質に強く依存する(W20 の 3 クラスで 8.6k〜158k 行/秒、
  実に約 18 倍の開き)。したがって §2.2 の検証時間見積は幅を持って読むこと。

## 4. 結論

- 監査対象の全容: 全 1103 d、標本 21 点監査済み、残り 1,082 d
  (280 mp-phase + 802 cadical-log)。
- 手順: `clauses_for_pair` で CNF 生成 → pysat Cadical195(with_proof)で
  テキスト DRAT 生成・gzip 保存 → **drat-trim** で検証(主チェッカー)
  → 1 d ごとに原子的領収書追記。
- 見積: solve ≈ 5 時間、drat-trim 検証 ≈ 1〜12 時間(レート依存)。
  増分チェッカーは層化少数点のクロスチェックに限定。
- 競合: P=1 逐次 + nice、重いプロセス同時数 ≤ 2 でラダーと共存。
  1 バッチ 40 分窓、再起動で失うのは最大 1 d。
- 次手(実行フェーズ、本タスク外): 上記ドライバを実装し、
  d=1..1103 のうち未監査 d を昇順に消化。完了後 K0693 を
  `computed` へ昇格できる(全 d の drat-trim VERIFIED 領収書が揃うことを条件とする)。

(完)
