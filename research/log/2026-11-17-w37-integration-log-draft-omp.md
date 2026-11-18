# W37: 次回 push 用の統合ログ草案とファイル一覧 (omp)

- 日付: 2026-11-17
- 作業dir: `~/workspace/kyouen-omp/full`
- 前回 push: 2026-11-16 の知識統合（K0869/K0870、リモート 31dcedd2）。
  本クローンの HEAD は `3b959959`（"knowledge: mirror K0869/K0870 integration from kb clone (local mirror of 0361ee0e)"）で、作業対象の成果はすべて未追跡（`git status --porcelain` の `??` のみ、変更ファイルなし）。
- 本作業は草案と一覧のみ。**push しない、commit しない。**
- 数値はすべて `git status --porcelain`・find/du・各ログ・各 JSON の実読。推測には [INFERENCE] を付ける。

---

## 1. 成果ごとの結論（統合ログ本文草案）

### 1.1 W24b: T5 部分スイープ設計（p=2207 / p=2531 の tail-UNSAT 一般化テスト設計）

log: `research/log/2026-11-12-t5-partial-sweep-design-omp.md`（ファイル名の日付 11-12 は設計起票時のもの。11-16 に先行する形で完成した設計）。

- 対象素数の選定として、p=2207（h=1,103、h−1=1,102 で CNF vars 14,320 / clauses 62,713 / kept edges 31,868、実測）と p=2531（h=1,265、size 1,264 で vars 16,426 / clauses 73,541 / kept edges 38,160、`t5_size_2531.py` で実測）を比較し、**第一対象を p=2207 に決定**した。
- パイロット実測: 単一インスタンス assumption 方式で d=735 は UNKNOWN 50.303 s（`t5-assump-2207-1102-d735.json` 実読）。tail d（d=1,103 / 1,097 等）は 47〜54 s 台で 100k 予算に対して UNKNOWN。
- 結論: 100k 予算では p=2207 の tail-UNSAT（size 1,102 の UNSAT）は決着せず、d=735 の fresh-each vs 単一インスタンスの判定差などが観測された段階。全量掃引の実行は未着手（設計と軽いパイロットのみ）。

### 1.2 W29b: SAT 側攻撃の設計（全段 UNKNOWN 11 d と (1,1,3)）

log: `research/log/2026-11-16-a2647-sat-side-attack-design-omp.md`。

- 候補Aラダー（45 件 = UNSAT 8 / UNKNOWN 37 / SAT 0）で 3M/10M/20M 全段 UNKNOWN の 11 d（147, 188, 194, 488, 602, 703, 717, 1003, 1103, 1166, 1229）を対象に、SAT 側（反例探索）攻撃の設計。S1（pair 状態空間の局所探索）→ candidate 変換 → 独立幾何検査の段階設計。
- 成果物は本 log 1 件のみ（repo 内の既存ファイルは無変更）。長時間 solver は未実行、符号化の健全性チェックのみ実施（VM 再現に数分）。
- 境界の明示: 探索で割当が「見つからなかった」ことは UNSAT の証明ではない。

### 1.3 W31: p=2207 全量 DRAT 監査ドライバ実装とパイロット

log: `research/log/2026-11-16-p2207-full-audit-pilot-omp.md`、ドライバ `research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_2207.py`（20 KB、SHA-256 先頭 `d232e70e43de`）。

- 再開可能（VERIFIED 済み d の SHA 一致でスキップ、実測 todo=0・2 秒で再投入完了）な全量監査ドライバを実装。SAT 即停止（K0693 反例扱い）・native CaDiCaL 切替分岐・進捗ログ・原子的領収書書き込みを備える。
- パイロット: 未監査 d の先頭 5 点（d=2..6）を監査し drat-trim VERIFIED を確認（集約領収書 `drat_trim_audit_full_2207_92f0aa9575ed519d.json`）。
- **監査はパイロット後も継続走行しており、本稿時点で d=2..264 のうち 258 点 VERIFIED**（下記 §4 参照）。これはパイロットの範囲を超えて進行中の一次資料として注記する。

### 1.4 W32: SAT 側パイロット S1（WalkSAT 型局所探索）

log: `research/log/2026-11-16-a2647-sat-side-pilot-omp.md`、探索器 `walksat.cpp`（SHA 先頭 `1a3036f0389b`…だが W32 log 記載と現在のファイル `636bea019906` が異なる → §5.6 参照）、driver `walksat_pilot.py`（SHA 先頭 `31209695ae18`、W32 log 記載と一致）。

- **結論: 違反 0 の割当は見つからなかった。** 11 d × 2 seed × 2 初期化 = 44 ラン各 10^6 flips すべてで、基数制約を満たす最良状態の不充足 base 節数は 20〜44 の範囲（`pilot-results.json` 44 レコード実読、solved=0、d 集合・seed 集合 W29 と一致）。
- candidate 変換 → 独立幾何検査の段には進んでいない。UNSAT の根拠ではない（W29 §3.4 の境界どおり）。
- 出力: `output/walksat-pilot-20261116/` に `pilot-results.json`（38 KB）、`eval-check.json`（21 KB、`all_ok` 等の符号化照合）、`problem-d147-sample.txt`（1.5 MB）。

### 1.5 W33: ネイティブ CaDiCaL によるラダー DRAT 領収書パス

log: `research/log/2026-11-16-a2647-ladder-drat-native-omp.md`、driver `ladder_drat_native.py`（20 KB、SHA 先頭 `6215ebb9a6ab`）、shim `native_solve.cpp`（117 行、SHA 先頭 `5d3fc38ec924`）。

- pysat 版 `ladder_drat.py` は証明全体を RAM に載せるため d=820@20M で 2 回とも VM 再起動に殺された。そこで `libcadical.a` に直接リンクする shim（`trace_proof` で 1 ステップずつディスクへストリーム）を用意した。
- 小さい段 d=1292@3M で end-to-end 検証: native solve（exit 20）→ drat-trim VERIFIED 0.205 秒（proof 23,116 bytes、追加 3,331 削除 161、`audit-drat-trim.json` 実読）。native 実行と drat-trim が同一入力を検査していることを別経路で照合済み（W33 log）。

### 1.6 W28 完了分①: d=1258 / d=1266 の pysat DRAT 領収書

`research/experiments/parabola-ternary-selection-20261109/output/ladder-drat-d1258-budget10000000/` と `ladder-drat-d1266-budget10000000/`。

- d=1258@10M: drat-trim VERIFIED、検証 1,564.130 秒（集約実測 `seconds` 1,564.2）、proof lines 8,666,047、core 337 万 / 総 lemma 434.9 万、resolution steps 1,284,608,603。
- d=1266@10M: drat-trim VERIFIED、検証 1,501.024 秒、proof lines 7,800,374、core 321.8 万 / 総 398.0 万、resolution steps 1,296,717,215。
- いずれも drat-trim binary SHA `92f0aa9575ed519d...`（commit `2e3b2dc0`）、input/proof の SHA256 を領収書に記録。

### 1.7 W28 完了分②: 8/8 達成 — d=820 の native 領収書（独立節）

**候補Aラダーの決着 8 段すべてが drat-trim VERIFIED で裏付けられた（8/8 達成、2026-11-17 検証完了）。** 最後の 1 段 d=820@20M は以下のとおり。

- ディレクトリ: `research/experiments/parabola-ternary-selection-20261109/output/ladder-drat-native-d820-budget20000000/`
- native solve: **4,820.636 秒**（`native-result.json`: cadical-native 3.0.1、exit 20、phase hints 3,966、conflicts 19,442,067、decisions 26,858,859、propagations 6,735,662,235、ticks 138,086,220,311、max RSS 98,272 KB）。
- drat-trim 検証: **8,204.407 秒で `s VERIFIED`**（集約 `seconds` 8,204.7）。proof 2,367,583,553 bytes（binary DRAT、追加 19,610,968 / 削除 19,564,515）、core 44,610 / 68,404 clauses、core lemma 12,992,212 / 19,610,969、resolution steps 5,299,520,466。checker binary SHA `92f0aa9575ed519d...`。
- **duplicate 照合**: `ladder-drat-d820-budget20000000/`（pysat 側宛先）に同じ `audit-drat-trim.json`・`drat-trim.log`・`solver.json` が置かれ、native 側の `audit-drat-trim.json` と JSON として完全一致（diff 実行で同一）。d=820 の領収書は native 実行・pysat 宛先の 2 ディレクトリに同じ内容で存在する。
- これにより候補Aラダーの決着 UNSAT 8 段がすべて DRAT 証明で machine-checkable になった（決着 8 d の一覧は W29 log 転記の UNSAT 8 件、本 log では転記しない）。A(2647) ≤ 1321 の根拠が強化された（残る全段 UNKNOWN 11 d の決着とは独立）。

### 1.8 経過中の成果（本 push 対象外だが同時期に存在、§5 参照）

W34（113 再設計）、W38〜W41（p=3251 全量監査設計・ドライバ）、p=2207 全量監査の継続走行中の d=2..264 成果（258 VERIFIED）。これらは W37 の push 対象から除外し、完成後に別バッチで push する。

---

## 2. リポジトリに置くべきファイル一覧（push 対象）

方針: **`.gz` の大きな証明ファイル・CNF ファイルは従来どおりローカル保持で push 対象外**（下記 §3 に列挙）。原則、log・コード・小さい JSON 領収書（KB 級）を push する。

### バッチ A: log 5 件（小、計約 100 KB）

| # | パス | 実測サイズ |
|---|---|---|
| 1 | research/log/2026-11-12-t5-partial-sweep-design-omp.md | 193 行 |
| 2 | research/log/2026-11-16-a2647-sat-side-attack-design-omp.md | 248 行 |
| 3 | research/log/2026-11-16-p2207-full-audit-pilot-omp.md | 175 行 |
| 4 | research/log/2026-11-16-a2647-sat-side-pilot-omp.md | 177 行 |
| 5 | research/log/2026-11-16-a2647-ladder-drat-native-omp.md | 266 行 |

### バッチ B: コード 6 件（小、計約 100 KB）

| # | パス | 実測サイズ | SHA-256 先頭 |
|---|---|---:|---|
| 6 | research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_2207.py | 20 KB | d232e70e43de |
| 7 | research/experiments/parabola-p2207-no-equality-witness-20261107/audit_full_3251.py | 20 KB | — (W38/W41 成果、§5.7 で扱い) |
| 8 | research/experiments/parabola-ternary-selection-20261109/walksat.cpp | 12 KB | 636bea019906 |
| 9 | research/experiments/parabola-ternary-selection-20261109/walksat_pilot.py | 12 KB | 31209695ae18 |
| 10 | research/experiments/parabola-ternary-selection-20261109/ladder_drat_native.py | 20 KB | 6215ebb9a6ab |
| 11 | research/experiments/parabola-ternary-selection-20261109/native_solve.cpp | 8 KB | 5d3fc38ec924 |

※ #7 `audit_full_3251.py` は W41 の成果物で W37 のスコープ外。§5.7 参照（除外推奨）。

### バッチ C: T5 出力 7 件（小、計約 56 KB）

`research/experiments/parabola-t5-partial-sweep-20261116/` 全体（実測 56 KB）:

| # | パス |
|---|---|
| 12 | …/t5_build_check.py |
| 13 | …/t5_size_2531.py |
| 14 | …/t5_pilot_p2207.py |
| 15 | …/t5_pilot_p2531.py |
| 16 | …/output/t5-pilot-2207-1102.json (8.5 KB) |
| 17 | …/output/t5-assump-2207-1102-d735.json (352 B) |
| 18 | …/output/t5-pilot-2207-1102-v2.json (840 B) |
| 19 | …/output/t5-pilot-2207-w24.json (13.5 KB) |

### バッチ D: W32 pilot 領収書 3 件（小、計約 1.5 MB — 1.5 MB 級は単独バッチ推奨）

`research/experiments/parabola-ternary-selection-20261109/output/walksat-pilot-20261116/`:

| # | パス | 実測サイズ |
|---|---|---:|
| 20 | …/pilot-results.json | 38 KB |
| 21 | …/eval-check.json | 21 KB |
| 22 | …/problem-d147-sample.txt | 1.5 MB ← 単独バッチ（§3） |

### バッチ E: W33 / W28 領収書（小 JSON のみ、.cnf/.drat/.gz は対象外）

`research/experiments/parabola-ternary-selection-20261109/output/` 配下:

| # | パス | 実測サイズ |
|---|---|---:|
| 23 | ladder-drat-native-d1292-budget3000000/audit-drat-trim.json | 1.5 KB |
| 24 | ladder-drat-native-d1292-budget3000000/native-result.json | 311 B |
| 25 | ladder-drat-native-d1292-budget3000000/solver.json | 1.4 KB |
| 26 | ladder-drat-native-d1292-budget3000000/init.json | 1.6 KB |
| 27 | ladder-drat-native-d1292-budget3000000/run.log | 2.4 KB |
| 28 | ladder-drat-native-d1292-budget3000000/drat-trim.log | 450 B |
| 29 | ladder-drat-native-d1292-budget3000000/phases.txt | 21 KB |
| 30 | ladder-drat-native-d820-budget20000000/audit-drat-trim.json | 1.5 KB |
| 31 | ladder-drat-native-d820-budget20000000/native-result.json | 333 B |
| 32 | ladder-drat-native-d820-budget20000000/solver.json | 1.4 KB |
| 33 | ladder-drat-native-d820-budget20000000/init.json | 1.6 KB |
| 34 | ladder-drat-native-d820-budget20000000/run.log | 3.2 KB |
| 35 | ladder-drat-native-d820-budget20000000/drat-trim.log | 478 B |
| 36 | ladder-drat-native-d820-budget20000000/phases.txt | 21 KB |
| 37 | ladder-drat-d1258-budget10000000/audit-drat-trim.json | 1.1 KB |
| 38 | ladder-drat-d1258-budget10000000/solver.json | 1.1 KB |
| 39 | ladder-drat-d1258-budget10000000/init.json | 750 B |
| 40 | ladder-drat-d1266-budget10000000/audit-drat-trim.json | 1.1 KB |
| 41 | ladder-drat-d1266-budget10000000/solver.json | 1.1 KB |
| 42 | ladder-drat-d1266-budget10000000/init.json | 750 B |
| 43 | ladder-drat-d820-budget20000000/audit-drat-trim.json | 1.5 KB（native 側と同一内容の duplicate、§5.5） |
| 44 | ladder-drat-d820-budget20000000/solver.json | 1.4 KB |
| 45 | ladder-drat-d820-budget20000000/init.json | 749 B |

※ E は 23 ファイル。30 ファイル未満に収まるよう #37-45（9 件）をバッチ E2 に分けてもよい。

### バッチ F: p=2207 全量監査パイロット領収書（W31 完了分のみ）

| # | パス | 実測サイズ |
|---|---|---:|
| 46 | research/experiments/parabola-p2207-no-equality-witness-20261107/output/drat_trim_audit_full_2207_92f0aa9575ed519d.json | 222,626 bytes（約 218 KB） |

※ W31 log がパイロット 5 点までを対象とするため、全量監査の集約領収書は 258 d 分まで進んだ状態を含む。push 対象に含めるか、W31 パイロット時点の 5 d 分の領収書として d=2..6 の receipt.json 5 件を含めるか、判断が必要（§5.4）。

---

## 3. push 対象外ファイル（ローカル保持）

`.gz` の大きい証明・CNF、および証明の生ファイル（.drat）は従来どおりローカル保持。

- `ladder-drat-native-d820-budget20000000/proof.drat`（2,367,583,553 bytes = 2.3 GB）、`proof.drat.gz`（1,323,763,304 bytes = 1.3 GB）、`input.cnf`（1,562,581 bytes）、`input.cnf.gz`（315,999 bytes）
- `ladder-drat-d820-budget20000000/proof.drat.gz`（1,323,763,304 bytes = 1.3 GB）、`input.cnf.gz`（315,999 bytes）
- `ladder-drat-d1258-budget10000000/proof.drat.gz`（311,347,450 bytes ≒ 311 MB）、`input.cnf.gz`（316,089 bytes）
- `ladder-drat-d1266-budget10000000/proof.drat.gz`（295,825,927 bytes ≒ 296 MB）、`input.cnf.gz`（315,648 bytes）
- `ladder-drat-native-d1292-budget3000000/proof.drat`（23,116 bytes）/ `proof.drat.gz`（9,204 bytes）: **小さいので対象外にする必然性はないが、一貫性の判断待ち**（§5.3）
- `ladder-d1292-target1322-budget3000000/input.cnf.gz` 等、`ladder-d<D>-target1322-budget<B>/` 配下の CNF（§5.2: 未分類の大量ディレクトリ）
- `p2207-drat-full/`（1.5 GB）: d=2..265 までの input.cnf.gz / proof.drat.gz / receipt.json / drat-trim.log 等が蓄積中。**push 対象から除外**（ただし receipt.json のみ軽量で、別途 push する判断は §5.4 に残る）
- `w14-cnf-cache.pkl`（15 MB）: W14 のキャッシュ。push 対象外が妥当と判断（§5.8）
- `w20-drat-1322/`、`w23-113-probe/` 配下の input.cnf.gz / proof.drat.gz 等: W20/W23 成果の .gz は従来方針どおり対象外
- `w19-1316-cadical-calib.json` / `w19-1316-cross-rest-jobs4-contended.json`: W19 成果（W37 スコープ外、§5.9）
- `w19_rest_probe.py`: W19 成果（同上）
- `ladder-d1292-target1322-budget3000000/input.cnf.gz` 等は§5.2参照
- `research/experiments/parabola-ternary-selection-20261109/output/target1322-budget20000000/init.json` / `input.cnf.gz`: W33 と混在する成果。`init.json` のみ小さいが、どの成果に紐づくか確認が要る（§5.10）
- `research/experiments/parabola-ternary-selection-20261109/output/native-solve`: ビルド済みバイナリ（実測の大きさ未確認、§5.10）。push 対象外（ビルド成果物）。
- 11-17 追加の log 4 件（2026-11-17-a2647-sat-side-deep-design-omp.md / 2026-11-17-a2647-113-100m-restartable-design-omp.md / 2026-11-17-p3251-full-audit-design-omp.md / 2026-11-17-w34-knowledge-update-draft-omp.md）は W37 スコープ外。§5.7 参照。

---

## 4. 実在確認メモ（git status / find 実読）

- `git status --porcelain`: すべて `??`（未追跡）。**変更（M）ファイルは 0 件**。
- p2207-drat-full 配下の d ディレクトリ数: 259（d=2..265 ただし d=50/100/150/200/250 を除く — gap 実測）。progress.log 実読で 258 verdict=VERIFIED 行、最終行は 2026-11-17T14:57:26Z d=264 VERIFIED（native 切替、solve 9.09 s / check 11.04 s）。**d=265 は実行中**（d=265 verdict 行は未確認、input.cnf.gz / proof.drat.gz / drat-trim.log のみ存在、receipt.json は 2026-11-17 14:58 時点で存在、verdict 行は progress.log にまだ無い [INFERENCE]）。
- 集約 `drat_trim_audit_full_2207_92f0aa9575ed519d.json`: records 258 件、すべて VERIFIED。check_seconds 総計 1,864 秒（≈31 分）、solve_seconds 総計 2,053.5 秒。d 範囲 2..264、ただし 50/100/150/200/250 欠（標本監査済みのためスキップ）。
- W32 pilot-results.json: 44 レコード。ds = {147, 188, 194, 488, 602, 703, 717, 1003, 1103, 1166, 1229}、kind = {warm, random}、base_violations_best 範囲 20..44、solved=0。
- eval-check.json: `ds`（11 d）、`seeds`=[1,2,3]、`random_states_per_seed`=3、`all_ok` キーを含む照合記録（詳細は §5.11 で要全文精査）。

---

## 5. 一覧と実在の食い違い・未確認点（隠さず列挙）

1. **W31 の成果物範囲が当初一覧と異なる**: W31 の log はパイロット 5 点（d=2..6）までを成果としているが、実際の `p2207-drat-full/` には d=2..265 までの領収書が蓄積している。これは W31 完了後に（別の作業継続として）全量監査が進行中であることを意味する。push 対象を W31 パイロット分に限定するか、進行中の領収書を含めるかは判断が必要。
2. **`ladder-d<D>-target1322-budget<B>/` ディレクトリ群が多数未追跡**: git status に `ladder-d1003-target1322-budget10000000.partial-074717/` 等の大量の `.partial-<HHMMSS>/` ディレクトリと `input.cnf.gz` が出ている。これらは候補Aラダー走行の途中成果。W37 のスコープ（W24b/W29b/W31/W32/W33/W28 完了分）には含まれていない。**W37 の一覧では対象外とするが、どの成果の一部として push するかは未整理**（候補Aラダー自体は前回 push 済み f8fd6578 の「solver claims only」コミットに対応する資産と思われる [INFERENCE]）。
3. **d1292 native の proof.drat.gz が 9 KB と小さい**: 対象外方針の根拠（.gz が大きい）が当てはまらない。一貫性のため .drat/.drat.gz/.cnf/.cnf.gz は原則対象外とするなら、d1292 の proof も対象外になる（現状の一覧では phases.txt 等の小ファイルのみ push 対象に含めた）。input.cnf（1.55 MB）が .cnf.gz（315 KB）と重複している点も整理要。
4. **`drat_trim_audit_full_2207_92f0aa9575ed519d.json`（W31 集約領収書）は成長中**: 実測 222,626 bytes（約 218 KB）。パイロット時点（5 d 分）から 258 d 分まで成長しており、push 時点の内容はドライバの進行に依存する。push 対象に含めるなら、その時点での records 数を再確認して commit メッセージに明記すること。d=2..6 の receipt.json 5 件をパイロット分として含める選択肢との判断が必要。
5. **d=820 の領収書が 2 箇所に重複**: `ladder-drat-native-d820-budget20000000/` と `ladder-drat-d820-budget20000000/` の `audit-drat-trim.json` が JSON として完全一致（diff 実行で確認）。pysat 宛先側には `proof.drat.gz`（1.3 GB）もあり、native 側証明のコピーと推定される [INFERENCE: 内容照合は SHA で未実施、領収書の proof_gz_sha256 が同一であることから同一証明と判断できる]。
6. **walksat.cpp の SHA が W32 log 記載と異なる**: log には `1a3036f0389b22103d22df15847e6968f1e444770a6a70c235eb075ae993e315` とあるが、現ファイルの SHA-256 は `636bea019906...`（先頭 12）。ファイルが log 記載後に更新された可能性がある [INFERENCE: 更新理由は未調査。push 前に W32 log 側の SHA を更新するか、更新の経緯を確認する必要がある]。
7. **W37 スコープ外の未追跡 log・コードが同時期に存在**: `2026-11-17-a2647-sat-side-deep-design-omp.md`、`2026-11-17-a2647-113-100m-restartable-design-omp.md`、`2026-11-17-p3251-full-audit-design-omp.md`、`2026-11-17-w34-knowledge-update-draft-omp.md`、`audit_full_3251.py`。これらは W34/W38/W41 等の別作業の成果物で、本 W37 の一覧には含めない。ただし `audit_full_3251.py` が W31 のドライバを流用した成果であるため、W37 push のバッチ B に含めるかどうかは判断が分かれる（現時点では除外）。
8. **w14-cnf-cache.pkl（15 MB）**: W14 の成果物。`git status` に出ているが W37 スコープ外。push 対象外（大きい・キャッシュ）。
9. **w19-1316-cadical-calib.json / w19-1316-cross-rest-jobs4-contended.json / w19_rest_probe.py**: W19 の成果物 [INFERENCE: log 名からの推定]。W37 スコープ外。push 対象から除外するが、W19 を push する作業が別にあるかは未確認。
10. **native-solve（バイナリ）**: `output/native-solve` は `native_solve.cpp` のビルド成果物（push 対象外が妥当）。`output/target1322-budget20000000/` については §5.12 参照。
11. **eval-check.json の `all_ok` は True を実読で確認済み**（ds 11 d、seeds [1,2,3]、random_states_per_seed 3）。
12. **target1322-budget20000000 は W33 log に記載あり**（grep で 4 件ヒット [INFERENCE: ヒット行の精読までは未実施]）。init.json のみ小さいため push 判断の余地あり。
13. **t5-assump-2207-1102-d735.json が W24 log では既存扱い**: W24 log はこのファイルを「既存 output の記録」として参照している。git status では未追跡なので、W24b より前の作業成果が未 push のまま残っている [INFERENCE: 元の作業 log は未確認]。push 対象に含める（バッチ C）。

---

## 6. push バッチ分割案

過去の教訓: 91 ファイル一括は tree 作成タイムアウトで失敗。約 30 ファイル単位が安全。数 MB 級は単独バッチ。

- **バッチ 1（log 5 件、約 100 KB）**: #1-5
- **バッチ 2（コード 5 件、約 100 KB）**: #6, 8-11（audit_full_3251.py 除外）
- **バッチ 3（T5 成果 8 件、約 60 KB）**: #12-19
- **バッチ 4（W32 pilot 領収書 2 件、約 60 KB）**: #20-21
- **バッチ 5（problem-d147-sample.txt 単独、1.5 MB）**: #22
- **バッチ 6（W33 d1292 領収書 7 件、約 28 KB）**: #23-29
- **バッチ 7（W28/W33 d820 領収書 16 件、約 52 KB）**: #30-45
- **バッチ 8（W31 集約領収書 1 件）**: #46 — §5.1/§5.4 の範囲判断が済んだ後で

各バッチは `git add <files> && git commit && git push` で分割実行する [INFERENCE: リモートの tree 作成タイムアウトはバッチごとの push サイズ依存と想定されるため、約 30 ファイル・約 1.5 MB を超えない分割とした]。

---

## 7. 次のアクション（push 実行時）

1. §5 の未確認点（特に walksat.cpp SHA 差、W31 集約領収書の範囲、d=820 duplicate の扱い）を解消する。
2. §6 のバッチ順に push する。
3. push 後、`uv run --locked python tools/knowledge/build.py` の再生成は不要（knowledge item の変更は W37 では無し）。ただし `git diff --exit-code -- README.md research/knowledge/generated` は統合前確認として実行する（AGENTS.md「統合前の確認」に従い、knowledge/research 構造を変更していないため最小限でよい [INFERENCE: log 追加のみなら build.py 実行の要否は README 生成物が log に依存しないため不要]）。

（完）
