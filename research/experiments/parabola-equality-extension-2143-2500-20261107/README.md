# 剰余放物線の等号証人：2003..2477 の保存と独立検証（2026-11-07）

## 背景

`Q_p = {(t, t^2 mod p)}` 上の安全集合（共円四点を含まない部分集合）の最大を `A(p)` とする。
奇素数 `p` で `A(p) <= (p+3)/2` は証明済み（K0097）。等号 `A(p) = (p+3)/2` は p ごとの有限問題で、
等号集合は完全対構造 `{0, d, p-d} ∪ (各対 {i, p-i} の一方)` を取る（K0334 の完全対補題）。

- `parabola-equality-extension-20261016` が 5..2000 の全奇素数で証人を保存した。
- `K0101` の 2026-10-17 記録は 2003..2143 を独立検査したと述べるが、証人は本 repo に保存されていなかった。

本実験は 2003..2477 の証人を保存し、生成とは独立な検証器で全件を監査する。

## 方法

1. `research/experiments/frontier-geometry-2026-10-05/forbidden_edges.cpp` で `Q_p` の禁止四点を
   `__int128` の整数行列式で厳密列挙する（Vandermonde 条件 `sum ≡ 0 mod p` で候補を絞る）。
2. `research/experiments/structural-lemmas-2026-10-02/checks/parabola_half_bound.py` の
   `clauses_for_pair(p, edges, d)` で signed NAE3/4 と原点節の CNF を作る。
3. `d = h = (p-1)/2` から降順に cadical（WSL の `/usr/bin/cadical`、呼び出しごとに `timeout`）で求解し、
   SAT モデルから `{0, d, p-d} ∪ 各対の一方` を構成する。その d で SAT なら等号証人。
4. 独立検証は `research/experiments/frontier-geometry-2026-10-05/verify_witnesses.cpp --modular-filter`。
   探索側の 3×3 行列式を使わず、generic 4×4 Leibniz 展開で、選択した三点と
   `sum ≡ 0` から決まる唯一の第四点の全組合せを検査する。

駆動は `probe_driver.py`（ファイル経由 IO。ジョブ実行環境で pipe を残さない）、監査は `verify_saved_witnesses.py`。

## 結果

- 2003..2477 の奇素数 **64 個のうち 62 個**で等号証人を構成し、`output/witnesses_2143_2500.json` に保存した
  （各 `size = h+2`、構成時に生成辺集合との照合済み）。
- `d != h` の例外: **2027, 2399, 2477 は d = h-1**。他の 59 素数は d = h。
- 証人が得られなかった素数: **2207**（d = h..h-120 の 121 個を試行、120 UNSAT・1 タイムアウト）と
  **2351**（d = h..h-5 を試行、大半が 45-240 秒でタイムアウト）。
  これは**予算内の探索失敗であり、等号不成立の証拠ではない**。
- 独立検証: 全 62 証人について `parabola-equality-audit.txt` に `p n covered checked` を出力（出口 0）。
  対象四点は総計 **4,201,666,014,750** 組、`sum ≡ 0 mod p` を満たす候補 **1,852,639,759** 組に直接整数行列式を適用し、共円 0 件。
- 連続範囲: 既存の 5..2000（穴なし）と合わせ、**5..2203 の全奇素数で等号証人が存在**する
  （2207 が最初の未発見素数）。2213..2477 も 2207, 2351 を除いて証人あり。

## 再現

```sh
g++ -O3 -std=c++17 research/experiments/frontier-geometry-2026-10-05/forbidden_edges.cpp  -o /tmp/forbidden_edges
g++ -O3 -std=c++17 research/experiments/frontier-geometry-2026-10-05/verify_witnesses.cpp -o /tmp/verify_witnesses
cd research/experiments/parabola-equality-extension-2143-2500-20261107
python probe_driver.py --generator /tmp/forbidden_edges --start 2003 --end 2477 --max-doubles 5 --timeout 45 \
       --out output/witnesses_2143_2500.json
python verify_saved_witnesses.py output/witnesses_2143_2500.json /tmp/verify_witnesses \
       output/parabola-equality-audit.txt
python summarize.py
```

既存の `output/witnesses_2143_2500.json` がある場合は、未処理の素数だけを追加する（再開可能）。

## 限界

- 2207, 2351 は未解決（より強い SAT 予算・別ソルバが必要）。穴なし等号は 5..2203 まで。
- 全奇素数での等号（K0101）は依然未解決。本実験は有限証人の範囲を広げるだけである。
- 監査は証人の安全性を検査する。証人の非存在・`d` の一意性は主張しない。
