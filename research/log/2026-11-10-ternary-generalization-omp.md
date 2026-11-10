# 候補A(三値・固定d)の任意 d 一般化: 調査と検証 (W16)

対象: `research/experiments/parabola-ternary-selection-20261109/`
作業: 2026-11-10。git commit / push なし。既存ファイルは無変更(`ternary.py` は読み取りのみ)。
新規作成: `ternary_general.py`(同ディレクトリ)、本ログ、検証出力ディレクトリ。

## 1. 基礎CNFは何を表しているか

`parabola-cnf-deletion-distance-20261109/output/rc2-p2647-d1323-20261108T184724Z.cnf`
- ヘッダ `p cnf 1323 53886`(1,323変数、53,886節)。SHA-256 `0f09fc6e…2ff0b3`(既存 README と一致)。
- 変数の意味: 変数 `t` は点 `t`(1≤t≤1322)。点 0 と点 1323 は現れない。
  実際に `d=1323` とその相方 `p-d=1324` を全節走査しても一度も出現しない。
- 節の意味: 禁止四点(4×4整数行列式が 0 = パラメータ和が mod p で 0)の各 edge について、
  「その edge の点のうち、要求側に選ばれた点が少なくとも1つは存在しない」を表す。
  p=2647 の禁止四点は全部で 928,389 個(`forbidden_edges.cpp` の列挙、W16 で再生成)。
- edge は「どの4点が禁止か」であり、d とは独立。ただし `clauses_for_pair(p, edges, double=d)` は
  各 edge の要求リテラル集合を作るとき `t == 0` または `min(t, p-t) == d` の点を **捨てる**
  (`parabola_half_bound.py` 28–43行)。つまり保存CNFは **d=1323 でフィルタ済み**の産物。

### 結論(1): 保存CNFは d=1323 専用
節の意味は d に依存して「pair d の2点が固定で常に選択される」前提を織り込んでいる。
別の d では (i) pair d に触れる edge を落とす集合が変わり、(ii) 逆に d=1323 で落とした
pair 1323 のリテラルを復元しなければならない。後者は保存CNFからは復元できない
(節に pair 1323 の符号情報が残っていない)。よって保存ファイル単体は d≠1323 に使えない。

## 2. encode() の d 依存

`ternary.py` の `encode(p, d, original)`:
- `free = [1..h] \ {d}`(h=(p-1)/2=1323)。変数 `i, h+i, 2h+i`(1≤i≤1323, i≠d)を low/high/empty に割当。
- 元節のリテラル変換 `+v → -v`、`-v → -(h+v)`。v=d は元節に現れないので、この式は任意の v で壊れない
  (`-h + (-v) = -(h+v)`、v=h=1323 でも `-2646` = high 変数で正しい)。
- 各 free pair に one-hot の 4 節(少なくとも1つ、および pairwise の排他)を追加。
- 空対カウント制約 `atmost(empty_vars, h+2-target)` を seqcounter で追加。

d への実依存は (a) 基礎CNFの節集合、(b) 変数番号の集合( d の pair だけ変数が存在しない)、
(c) 空対変数の集合、の3点。いずれも `d` を引数化すれば足りる。変換式そのものは d 非依存。

## 3. 一般化の方式(採用)

基礎CNFを保存ファイルから読むのをやめ、**d 非依存の edge リストから再生成**する。
- edge リスト: `parabola-hplus1-drat-20261109/input/verified_edges.txt.gz`
  gz SHA-256 `bb1c0201192863b560a8687b570cdbab0f0a7d51c40d71fcd4a03c0f9ccbdae0`、
  展開後 SHA-256 `4e17fe105f191f781192466d0775a59d3c341b16b267ebe372ba279911f67a72`
  (既存 `init.json` の `edge_input_sha256` と一致)。
- 中身は 53,886 edge。全 928,389 個から「同一 pair の2点を含む(trapezoid)」を除いたもの。
  trapezoid は free pair の one-hot(各 pair 高々1点)の下で全選択不能なので冗長。
  このため kept リストは d 非依存に十分(`clauses_for_pair` の出力は d=1323 の保存CNFと一致)。
- 生成手順: `clauses_for_pair(p, edges, d)` → 各節内を `(abs, sign)` 順にソート → 節を辞書順ソート。
  d=1323 でこれが保存ファイルと **バイト一致**することを確認済み(下節)。

(以下、検証結果を追記)

## 4. 検証結果(すべて実測)

### 4.1 基礎CNFの再生成が d=1323 でバイト一致

`clauses_for_pair(2647, kept_edges, 1323)` を「節内を (abs, lit) 順、節を辞書順」に正規化したものは、
保存CNF 53,886 節と **節順・内容ともに完全一致**(Python で比較、差分 0)。よって
`ternary_general.py --d 1323` の `base_cnf_sha256` = `0f09fc6e…2ff0b3`(既存 README と一致)。

生成された CNF(展開後 1,551,984 バイト)は、既存 `output/target1322-budget3000000/input.cnf.gz` と
**gz バイト列まで一致**。`encoded_cnf_sha256` = `8cbd404a…b9f48a`、
`variables`=7,926、`clauses`=68,404。

### 4.2 d=1323, target=1322, budget=100k の再現

`output/generalization-check-d1323-target1322-budget100000/`(今回の実行):
- READY d=1323 target=1322 clauses=68404 variables=7926
- status **UNKNOWN**、solve **54.317 s**(このマシン、1コア、同時実行なし)
- 統計: conflicts 100001 / decisions 217401 / propagations 50404659 / restarts 4854

既存実績(`output/target1322-budget100000/result.json`):UNKNOWN、14.336 s、
統計は **conflicts 100001 / decisions 217401 / propagations 50404659 / restarts 4854 — 完全一致**。
節数・変数・CNF SHA・決定数・伝播数がすべて同一なので、探索は同一。壁時計だけが 3.8 倍遅い
(既存記録は D:/ 上の別環境、本実行は Linux の `uv run`。CPU 差であって入力差ではない)。
→ **d=1323 では現行 `ternary.py` と同一のCNF・同一探索**。オーダーは秒(十秒台)で一致。

### 4.3 d=300 での生成と実行

- `--d 300 --target 1322 --budget 100000`:生成可。CNF は base 53,886 節(保存CNFと同じ節数)・
  encoded 68,404 節 / 7,926 変数。base SHA `fb76aa1c…d6c59`、encoded SHA `2e3b213e…bd4a4e`。
- 結果 **SOLVER_UNSAT**、solve **1.811 s**、conflicts 1,808(予算 100k 未満 = 打ち切りではなく完全な反駁)。
- 独立確認:同一 `input.cnf.gz` を Glucose4 と Minisat22 に投入し、両方 `False`(UNSAT)。予算依存なし。
- `--d 300 --target 1293 --budget 100000`:142,992 節 / 45,249 変数(d=1323 target1293 と同サイズ)、
  **UNKNOWN** 90.207 s。→ 任意 d でも通常のラダー実行が回ることを確認。

**d=300 target=1322 の UNSAT の解釈**:この三値固定 d 部分族に「±300 を含む 1322 点安全集合」が
存在しない、という意味。全 Q_2647 の UNSAT ではない。また現行同様、DRAT 監査前の
`SOLVER_UNSAT` であり receipt としては未監査。d=1323 のときは 100k で UNKNOWN だったので、
**この族の難易度は d に強く依存する**ことが初めて実測された(次節の注意参照)。

### 4.4 edge リストの d 非依存性(独立検査)

- 全 928,389 edge の再列挙(`forbidden_edges.cpp`、W16 で再実行・2m11s)と kept 53,886 の比較:
  kept ⊆ full、差分 874,503 はすべて「同一 pair の2点を含む」edge(trapezoid)。
- 小さな素数 p=5,7,11,13,17 の全 d・全三値割当(合計 19,392 割当)で、
  `clauses_for_pair(full)` と `clauses_for_pair(kept)` の評価が全一致(不一致 0)。
- `ternary_general.base_clauses/encode` の出力と、整数幾何による
  「全選択四点に行列式0が無い」判定を同じ 19,392 割当で照合し、不一致 0。
→ trapezoid 除去は任意 d で健全。kept リストは d 非依存に使える。

## 5. 元の回帰テスト

`regression.py` は `HERE/"regression.json"` に書き込むため、repo を変更しないよう
`/tmp/w16/regression_w16.py` に複製して HERE と出力先だけ差し替えて実行した(repo側は無変更)。
結果は保存済み `regression.json` と全項目一致:総割当 19,392、cardinality 444 ケース、
invalid one-hot REJECTED、1296 点証人 PASS、target1300 UNKNOWN。所要 4.7 s。

## 6. 一般化版の使い方

```
uv run --locked --with python-sat==1.9.dev21 \
  python research/experiments/parabola-ternary-selection-20261109/ternary_general.py \
  --d <d> --target <target> --budget <conflicts> \
  --output research/experiments/parabola-ternary-selection-20261109/output/<name>
```

- `--d` 省略時は 1323(現行と同じ)。有効範囲 1 ≤ d ≤ 1323。
- `--target` の有効範囲 3 ≤ target ≤ 1325(h+2)。`empty_bound = 1325 - target`。
- `--output` は既存ディレクトリだと失敗する(`exist_ok=False`)。常に新しい名前を指定する。
- 出力: `init.json`(`d`, `target`, `base_cnf_sha256`, `encoded_cnf_sha256`, `edge_cache_*_sha256`,
  worker 自身の SHA を含む)、`input.cnf.gz`、`result.json`
  (`status` は `SAT` / `SOLVER_UNSAT` / `UNKNOWN`、`solve_seconds`、`statistics`)。
  SAT 時のみ `model.json` と `candidate.txt`。
- d=1323 では `base_cnf_sha256` が `0f09fc6e…` になることを内部 assert で強制している
  (edge キャッシュかエンコーダが変われば即失敗する)。

ラダー実行例(層化19 d、予算を上げる場合は同じ d・target で `--budget` だけ変える):

```
for d in 188 194 602 622 703 717 820 1003 1258 1300 1322; do
  uv run --locked --with python-sat==1.9.dev21 \
    python research/experiments/parabola-ternary-selection-20261109/ternary_general.py \
    --d "$d" --target 1322 --budget 100000 \
    --output "research/experiments/parabola-ternary-selection-20261109/output/d${d}-target1322-budget100000"
done
```
(d=300 は 100k で UNSAT 済みなので再実行しない。層化19 d の完全なリストは
`research/log/2026-11-10-a2647-113-hardcore-attack-plan-omp.md` §次手1 に従う。)
出力ディレクトリの命名は `d<d>-target<target>-budget<budget>` を推奨(既存の `target…` 名は d が
固定前提だったため、d を含めないと衝突する)。

## 7. 注意(実測から言えること)

1. **保存CNFは d=1323 専用**。`ternary_general.py` は保存CNFを読まず、必ず edge キャッシュから再生成する。
   `ternary.py` を任意 d に使う改造は不可(復元できない情報がある)。
2. **d=300 の UNSAT は receipt ではない**。DRAT を取るなら Cadical の proof tracing を有効にした実行が要る
   (本タスクでは未実施)。`SOLVER_UNSAT` のまま記録する。
3. 難易度は d に強く依存する。d=1323 は 100k で UNKNOWN(1.8k 万伝播規模)、d=300 は 1,808 conflicts で UNSAT。
   ラダーの 19 d を「同じコスト」で外挿しない。d ごとに実測が必要。
4. 位相ヒント:現行 `phases()` は pair が complete(両方 chosen)のとき low と high を同時に正にする。
   d=1323 では complete な pair は d 自身だけで、その変数は存在しないため無害。一般 d では
   1292 点 warm が pair 1323 を complete で含むため矛盾ヒントになる。`ternary_general.phases` は
   その場合 low のみ正に倒す。d=1323 では現行と **完全に同一の位相リスト**(3,966 リテラル)になることを確認済み。
5. 三値版の UNSAT は「0 と pair d を固定した部分族」の UNSAT であり、全 Q_2647 には拡張されない
   (既存 README と同じ制限)。

## 8. 再現コマンド(今回の検証そのもの)

```
python research/experiments/parabola-ternary-selection-20261109/ternary_general.py \
  --d 1323 --target 1322 --budget 100000 --output output/generalization-check-d1323-target1322-budget100000
python research/experiments/parabola-ternary-selection-20261109/ternary_general.py \
  --d 300 --target 1322 --budget 100000 --output output/generalization-check-d300-target1322-budget100000
python research/experiments/parabola-ternary-selection-20261109/ternary_general.py \
  --d 300 --target 1293 --budget 100000 --output output/generalization-check-d300-target1293-budget100000
```

(完)

## 9. 追加検査(W16 内、上記の後)

### 9.1 CLI ガード
- `--d 1400`(>h)と `--target 2000`(>h+2)は `ValueError: invalid target, budget or d` で停止。
- 既存 `--output` を指定すると `FileExistsError`。既存出力を上書きしない。
- 有効域: `1 ≤ d ≤ 1323`、`3 ≤ target ≤ 1325`、`budget ≥ 1`。

### 9.2 SAT 経路(モデル→候補変換)の検査
p=17 の全 d・全 target で 64 件の SAT ケースを解き、`parameters()` の再構成、
`size == h+2-empties`、`{d, p-d} ⊆ 候補`、全節充足、整数幾何での安全性を確認。全件一致。
(p=2647 では d≠1323 の SAT 例がまだ無いため、小さい p で経路を検証した。)

### 9.3 複数 d の 100k 掃引(途中経過、target=1322)
| d | status | solve | conflicts |
|---:|---|---:|---:|
| 188 | UNKNOWN | 35.80 s | 100,003 |
| 194 | UNKNOWN | 42.60 s | 100,001 |
| 300 | SOLVER_UNSAT | 1.70 s | 2,795 |
| 602 | UNKNOWN | 41.52 s | 100,000 |

d=300 は 1.8k conflicts で UNSAT、d=188/194/602 は 100k を使い切って UNKNOWN。同じ target でも
d により難易度が2桁以上違う。ラダーでは d ごとに実測が必要。
