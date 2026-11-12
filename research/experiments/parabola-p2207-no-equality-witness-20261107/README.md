# 剰余放物線の等号不達成（p=2207, 2531）と DRAT 監査

`Q_p = {(t, t² mod p) : 0 <= t < p}` の安全集合（共円・共線四点を含まない部分集合）の最大を `A(p)` とすると、
K0097 は上界 `A(p) <= (p+3)/2` を証明し、5..2203 の全奇素数で等号証人が知られていた。
本実験は **p=2207 と p=2531 では等号 `A(p)=(p+3)/2` が成立しない**ことを示す（K0693, K0702）。

- 根拠の骨格: サイズ `h+2`（`h=(p-1)/2`）の安全集合は `0` ＋一つの完全対 `{d,p-d}` ＋他の各対の一側に限られ、
  K0334 が等号を「ある `d` について signed NAE3/4 と原点節の CNF が充足可能」と全奇素数で同値に還元している。
  したがって `d = 1..h` の全 `d` で CNF が UNSAT なら等号は不成立。
- p=2207（h=1103）: 全 1103 d が UNSAT（うち 4 件は 30 秒制限タイムアウトのため衝突予算 2000 万で再判定）。
- p=2531（h=1265）: 全 1265 d が UNSAT（衝突予算 20 万、unknown 0）。
- 実装の全数照合: p=5..23 で `Q_p` の全安全集合を列挙し、完全対 d の集合と CNF の SAT/UNSAT が
  7 素数すべてで一致（p=23 は安全集合 8,064 個、brute_d = cnf_d = {1,...,11}）。
- 独立検算: 同じ実装は隣接 63 素数（2003..2477）で SAT 側の証人を作り、探索と独立な generic 4×4
  Leibniz 検証器で共円 0 件を確認している。

## DRAT 監査（ソルバ主張を独立検証する）

- `drat_check.cpp`: 素朴な RUP/RAT チェッカー（毎回ゼロから伝播）。
- `drat_check_incremental.cpp`: 決定レベル・trail・バックトラックを使う増分チェッカー。
  11 MB（145,134 行）の証明を約 100 秒で検証できることを確認済み。
- `verify_drat_sample.py`: 1 件分のパイプライン（CNF 生成 → pysat CaDiCaL の DRAT → チェッカー）。
- `audit_all_d.py`: 素数ごとの全 d 監査ドライバ（再開可能、`output/drat_audit_full_<p>.json`）。
- 進捗:
  - p=2207: 標本 21 d（1, 50, 100, 150, 200, 250, 289, 297, 300, 312, 324, 400, 500, 550, 600,
    700, 800, 900, 1000, 1100, 1103）が **21/21 VERIFIED**（証明 16〜576,575 行）。
  - p=2531: 旧検証器での「1265/1265」は K0707 の健全性不具合により独立証拠に採用しない。
    修正版検証器（削除時に代入を失効）で**再監査中**（1 件 1〜450 秒、全数で 8〜13 時間）。
  - p=2647: **修正版検証器で 1323/1323 VERIFIED（完了）**。証明 22〜29,212 行、検査 0.5〜43 秒/件。
    これにより p=2647 の等号不達成は有限計算として完全に証明された（K0706、status computed）。
  - p=3251: 修正版検証器で全 1625 d の監査を実行中。

## 1104 石（次サイズ）の探索

サイズ `h+1` の集合は `x + c - e = 1`（`x`=0 を含む、`c`=完全対数、`e`=空対数）から 3 形ある。

- `scan_shape_b.py`: 形状 (a) `(1,0,0)` と (b) `(0,1,0)` を既存エンコーダで走査。
  (a) は UNSAT、(b) は全 d で UNSAT。
- `search_1104_shape_c.py`: 形状 (c) `(1,1,1)` を単一 CNF（各対 {BOTH,NONE,LOW,HIGH}、BOTH=1, NONE=1）で探索。
  台形辺を冗長として削除する（p=2207 で 607,753 節 → 52,819 節、8,822 変数）。
  `--write-cnf` で DIMACS を書き出せる（外部ソルバ用）。判定状況:

  | p | h+1 | 形状 (c) の判定 | 備考 |
  |---|---|---|---|
  | 2207 | 1104 | **SAT**（5,328.5 秒） | 完全対 307・空対 1078。独立幾何監査は K0722 |
  | 2647 | 1324 | UNSAT（8.2 秒） | 形状 (a)(b) も UNSAT → `A(2647) <= 1323` |
  | 2531 | 1266 | 未決（797 秒 / 200 万衝突、継続中） | 形状 (a)(b) は UNSAT |
  | 3251 | 1626 | **UNSAT**（cadical 既定設定、約 35 分） | 形状 (a)(b) も UNSAT → `A(3251) <= 1625` |

  形状 (c) は p=2207 で充足可能、p=2647 と p=3251 で不可能なので、2531/3251 の未決を
  「UNSAT の兆候」とも「SAT 寄り」とも決めつけられない（2647 は 8 秒で UNSAT、2207 は 89 分で SAT）。
- `scan_shape_c_census.py`: 奇素数 5..401 の 77 個で形状 (c) を判定し、**77/77 SAT**（UNSAT 0）。
  形状 (c) の UNSAT は珍しく、いま分かっている例は 2647 と 3251 だけ（2531 は未決）。
- 対称性の注意: パラメータの単元倍 `t↦at` は安全性を保たない（K0774）。完全対を `{1,p−1}` に
  正規化する対称性破りはできない。反射 `t↦p−t`（完全対の数え上げの根拠）だけが使える。
- `maxsat_probe.py`: 各辺節に緩和変数を足し「違反 k 節以内」を問う。p=2207, d=h では k=1（3.2 秒）も
  k=2（77.7 秒）も UNSAT で、**3 節以上**を違反しないと充足できない。
- `scan_maxsat_k1.py`: 全 d の k=1 走査（d によっては 1 件 10 分以上かかり、47 分で完走せず中断）。

## 負の結果

- `search_equality_single.py`: 等号を 1 個の SAT インスタンスで判定する単一クエリ符号化。
  変数あたり約 4.4 節でランダム 4-SAT のしきい値付近に入り、証人が存在する p=2503 でも 10 分以上未決。
  d 固定の CNF（密度約 29）の方が易しく、単一クエリ化は採用しない。

## 形状 (c) の証明書パイプライン

- `search_1104_shape_c.py <p> --write-cnf OUT.cnf`: 形状 (c) の CNF を書き出す（再生成可能）。
- `certify_shape_c_unsat.py --p <p> --proof P.drat`: CNF を再生成して hash を突き合わせ、
  `drat_check_incremental.cpp` で DRAT を検査し、receipt（CNF/proof/checker の hash）を書く。
- `scan_shape_c_census.py --start 5 --end 401`: 小さい素数の形状 (c) 国勢調査（77/77 SAT）。
- `drat_check_fast.cpp`: 検証器の高速版（K0780）。既存4証明書で旧版と同一判定のまま 3〜11 倍速い。
  `validate_fast_checker.py` が4証明書の再検査と負の対照2件をまとめて実行する。

```sh
g++ -O2 -std=c++17 drat_check_fast.cpp -o drat_fast
uv run --locked --with python-sat python search_1104_shape_c.py 3251 --write-cnf a3251_1626.cnf
uv run --locked --with python-sat python certify_shape_c_unsat.py --p 3251 --proof a3251.drat
uv run --locked python validate_fast_checker.py --checker ./drat_fast
```

## 再現

```sh
g++ -O2 -std=c++17 drat_check_incremental.cpp -o drat_inc
uv run --locked --with python-sat python validate_reduction.py            # p<=23 の全数照合
uv run --locked --with python-sat python build_inventory.py 2207          # p=2207 の判定表
uv run --locked --with python-sat python audit_all_d.py --p 2531 --workers 12   # 全 d 監査（再開可能）
```

## 限界

- p=2207 の DRAT 監査は標本 21/1103、p=2531 は 400 件超/1265 で継続中。残りはソルバ主張のまま。
- 両素数とも「全 d UNSAT」は cadical の主張であり、全数証明が揃うまで status は `needs-review`。
- `A(2531)` の正確な値は未確定（上界は h+1。形状 (c) が未決なので h+1 か h 以下かが残る）。
  `A(2207) = 1104 = h+1` は K0722 で確定済み。`A(3251) <= 1625` は K0775（証明書は作成中）。
- 不達成素数の分布・特徴づけは K0101 の問いとして残る。
