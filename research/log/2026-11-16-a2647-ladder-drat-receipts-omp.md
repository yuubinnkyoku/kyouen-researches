# 2026-11-16: 候補Aラダー決着8 d の DRAT 領収書化 (W28, omp)

## 目的

候補Aラダー（`research/log/2026-11-13-a2647-candidate-a-ladder-result-omp.md`）で
SOLVER_UNSAT と決着した 8 d は、solver の主張のみで DRAT 証明が保存されておらず
領収書が無かった。各 d を決着した段と同一の入力・予算で、DRAT 証明を出力する
Cadical195（python-sat 1.9.dev21）で再実行し、drat-trim で独立検証して領収書を作る。

決着8件（d / 決着段 / conflicts / solve_seconds）:
1292 / 3M / 674 / 0.1、977 / 3M / 417,436 / 61.4、1040 / 3M / 447,601 / 63.1、
914 / 3M / 628,202 / 92.5、622 / 3M / 1,796,375 / 371.2、
1258 / 10M / 4,176,372 / 887.5、1266 / 10M / 3,945,161 / 819.2、
820 / 20M / 13,294,778 / 3,813.1。

## 方法

再実行スクリプト: `research/experiments/parabola-ternary-selection-20261109/ladder_drat.py`
（SHA-256 `1b44a77af639cda431305b0778726051b5459dccea66df8d4adf2d072aa4f213`）。
これは CNF 構築を `ternary_general.py`
（SHA-256 `8875004ef41e4f8570e59efaad842081d7bef33f248cd5ec08f98191de9bfb46`）から
import し、ラダーと同一の target=1322 / empty_bound=3 / 予算 / warm-start phases で
Cadical195 を `with_proof=True` で走らせ、証明を `proof.drat.gz`（gzip, mtime=0）に、
検証を drat-trim で `audit-drat-trim.json` に記録する。W20 の方式と同一。

- 検証器: drat-trim（https://github.com/marijnheule/drat-trim、commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`、`gcc drat-trim.c -std=c99 -O2 -o drat-trim`）。
  バイナリは `~/workspace/kyouen-omp/tasks/drat-trim-src/drat-trim`、
  SHA-256 `92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a`（実行時に照合）。
- 出力は新規ディレクトリ
  `research/experiments/parabola-ternary-selection-20261109/output/ladder-drat-d<D>-budget<B>/`
  （既存ラダーの `ladder-d<D>-target1322-budget<B>/` は上書きしない）。
- 実行は逐次（P=1）。`TEMP=$HOME/workspace/kyouen-omp/bin`。

入力同一性: 再実行の `input.cnf.gz` は、元ラダーの `input.cnf.gz` と
**バイト単位で一致**することを 4 d（1292, 977, 1040, 914）で確認済み
（`encoded_cnf_sha256` も init.json 間で一致）。

生成の再現性: 決着段の conflicts が元ラダーと完全一致（下表の conf 列 vs 背景の値）。

## 結果: drat-trim VERIFIED の 4 d（すべて SOLVER_UNSAT）

| d | 段 | conflicts | solve_seconds | 証明行数 | drat-trim verdict | check_seconds | 証明 SHA-256 |
|---|---|---|---|---|---|---|---|
| 1292 | 3M | 674 | 0.26 | 3,514 | VERIFIED | 0.24 | 95dafdaa…c529538 |
| 977 | 3M | 417,436 | 126.34 | 1,056,572 | VERIFIED | 144.59 | ef1219df…57ef86e |
| 1040 | 3M | 447,601 | 101.22 | 1,069,706 | VERIFIED | 223.53 | f79aa378…dc49836 |
| 914 | 3M | 628,202 | 119.83 | 1,408,769 | VERIFIED | 212.29 | 926f4e03…c9f4707 |

## 進行中: d=622（solve 完了、drat-trim 検証中）

- solver: SOLVER_UNSAT、565.94 秒、conflicts **1,796,375**（元ラダーと完全一致）、
  証明 3,801,225 行、501,762,222 バイト、SHA-256 `f15b5e44e577df7989c59151a7fdd33bb7f8886c8034b6b73f2113e3a7a7aa38`
  （`ladder-drat-d622-budget3000000/solver.json` より）。
- 本ログ作成時点では drat-trim 検証が進行中（`audit-drat-trim.json` 未生成）。
  検証はドライバ（`/tmp/w28-driver.sh`）が継続しており、完了時に
  `audit-drat-trim.json` / `drat-trim.log` が同ディレクトリに生成される。

全数値は各 `ladder-drat-d<D>-budget<B>/solver.json` および
`audit-drat-trim.json` からの転記。証明 SHA-256・行数は gzip 解凍後の実バイトから
再計算して JSON と一致することを確認済み。checker_binary_sha256 は各 audit で
`92f0aa95…` に一致。

drat-trim の内訳（各 `drat-trim.log` より）:

- d=1292: 1,210/68,404 clauses in core、555/3,376 lemmas in core、26,057 resolution
  steps、0 RAT lemmas。
- d=977: 26,143/68,404 clauses in core、337,272/511,993 lemmas in core、
  186,346,639 resolution steps、0 RAT lemmas。
- d=1040: 26,846/68,404 clauses in core、352,079/522,504 lemmas in core、
  195,071,879 resolution steps、0 RAT lemmas。
- d=914: 29,012/68,404 clauses in core、504,259/702,976 lemmas in core、
  219,362,158 resolution steps、0 RAT lemmas。

領収書ファイル（各 d ディレクトリ内）: init.json / input.cnf.gz / solver.json /
proof.drat.gz / audit-drat-trim.json / drat-trim.log。
証明・CNF はバイナリのため push 対象外。SHA-256 は各 JSON に記録されており
バイト単位で再生成可能。

## 未完了（本タスクの時間枠内では未達）

逐次ドライバ（軽い順）は 1292, 977, 1040, 914 の 4 d の領収書を完成させ、
622 は solve を完了（conflicts は元ラダーと一致）して drat-trim 検証中、
1258 / 1266 / 820 は未着手の段階で本セッションの時間枠を迎えた。
以下は本ログ作成時点で `audit-drat-trim.json` が未生成の分:

| d | 段 | 状態 |
|---|---|---|
| 622 | 3M | solve 完了（UNSAT、領収書は検証中）、上記 |
| 1258 | 10M | 未着手 |
| 1266 | 10M | 未着手 |
| 820 | 20M | 未着手 |

未完了分の想定所要（元ラダーの solve_seconds と DRAT ロギングの上乗せ、および
本タスクの実測 4 d でのロギング倍率から）: 622 は数百分、1258 / 1266 は
約 0.5〜1 時間規模、820 は元 solve 3,813 秒＋検証で 1 時間超の見込み。
重い順の 820 は単独でも 1 時間を超えるため、本タスクの枠では 4〜5 d が上限。

## 再実行手順（未完了分の続行用）

```sh
cd ~/workspace/kyouen-omp/full
export TEMP=$HOME/workspace/kyouen-omp/bin
uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-ternary-selection-20261109/ladder_drat.py \
    --d <D> --budget <B>
```

`<D> <B>` は 622 3000000 / 1258 10000000 / 1266 10000000 / 820 20000000。
スクリプトは `solver.json` が既にあれば solve をスキップし、`audit-drat-trim.json` が
検証済みなら検証もスキップする（`--recheck` で再検証）。逐次実行すること
（同時に重い solve を複数走らせない）。出力は
`output/ladder-drat-d<D>-budget<B>/` に生成される。

## 注意点

- 本ログの 4 d の領収書は、入力 CNF が元ラダーとバイト一致し、conflicts も
  元ラダーと完全一致する。したがってラダーのこれら 4 d の SOLVER_UNSAT 主張は
  DRAT 監査済みとなった。
- 未完了の 4 d（622, 1258, 1266, 820）の領収書は本ログ作成時点では存在しない。
- 本ログの数値はすべて保存された JSON・ログからの転記であり、推定は未完了分の
  所要時間見込みにのみ付す。

（完）
