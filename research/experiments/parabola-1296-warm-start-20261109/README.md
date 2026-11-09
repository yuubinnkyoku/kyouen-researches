# 既存証人を初期値にした Q_2647 の安全集合（2026-11-09）

基準 main `a90f6992` の K0711/K0712 と直接投影CNFを使用。原点と完全対 `d=1323` を固定し、他の対から低側・高側・空対を選択する。旧実験の1296点証人と、その後得た各証人を次のCaDiCaL195試行のphase（探索順）に使う。点を固定するassumptionではないため、後の集合が前の集合を含むとは限らない。

| 初期値 | 目標点数 | 空対上限 | 衝突予算 | 結果 |
|---:|---:|---:|---:|---|
| 1296 | 1296 | 29 | 100,000 | SAT、1298点（空対27） |
| 1296 | 1299 | 26 | 200,000 | UNKNOWN |
| 1298 | 1299 | 26 | 300,000 | SAT、1299点（空対26） |
| 1299 | 1300 | 25 | 300,000 | SAT、1300点（空対25） |
| 1300 | 1301 | 24 | 300,000 | SAT、1301点（空対24） |
| 1301 | 1302 | 23 | 300,000 | UNKNOWN |
| 1301 | 1302 | 23 | 1,000,000 | SAT、1302点（空対23） |
| 1302 | 1303 | 22 | 300,000 | SAT、1303点（空対22） |
| 1303 | 1304 | 21 | 300,000 | UNKNOWN |
| 1303 | 1304 | 21 | 1,000,000 | UNKNOWN |
| 1302 | 1304 | 21 | 300,000 | UNKNOWN |

UNKNOWNはSATでもUNSATでもなく、不存在・最適性を意味しない。各出力の `init.json` / `result.json` は実行時点の状態とハッシュを保存する。solverの `geometry: UNCHECKED` はソルバ直後の記録であり、その後に同じ候補を別の幾何検査器へ渡した結果を `geometry.json` として保持する。

## 1303点証人の独立検査

対象: `output/target1303-seed1302-budget300000/`。

- 保存された **117,652節**と全モデルを別スクリプトで読み直し、全節充足、三値選択、空対22、点数1303、出力座標との対応を検査。
- CNFや探索コードを使わないgeneric 4×4整数行列式検査器が、全 `C(1303,4)=119554191575` 四点を必要合同式で被覆し、**45,241,569** 候補の直接行列式検査で禁止四点0件。入力と検証器のhashは `geometry.json` に記録。
- 1298・1299・1300・1301・1302点の候補も同じ手順でそれぞれ独立幾何検査済み。
- `test_verify.py` は候補点、モデル、worker hashの改変を拒否する。
- 証人の未選択1344点すべてに、選択済み3点との禁止四点を与える `extensions.txt` を保存。独立な3×3整数行列式で各証人と全点の被覆を照合した。したがってこの集合は **包含極大**。最大点数であることは意味しない。
- さらに各未選択点に複数の障害四点を与え、1221点はどの既存1点を削除しても追加不能と確認。残る候補について一削除で許され得る二点組 **12,210組**すべてに、削除されない既存2点との障害四点を保存した。独立検査器が全点と全組の被覆・行列式を照合したため、この証人は **一削除二追加でも改善できない**。複数削除や別集合には及ばない。
- 固定された原点・完全対を維持し、他の各対から高々一側を選ぶ場合、**既存1303点から高々2点を削除して1304点以上にすることも不可能**。削除数制約を追加した33,886変数・121,584節のCNFについて、24,030行のDRATを保存。修正版増分検査器と毎回代入を再構築する別検査器がともに受理し、打切り証明を拒否した。CNFの再生成と小規模1,008ケースの符号付き削除数制約の全数照合も実施。固定対を壊す場合やより多くの削除には適用できない。

よって **A(2647)≥1303**。上界1322は別の形状クラスのソルバ判定に依存し、DRAT独立監査は未完。正確値や他素数への一般化は主張しない。

## 再現

```sh
uv run --locked python research/experiments/parabola-1296-warm-start-20261109/verify.py research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000
uv run --locked python research/experiments/parabola-1296-warm-start-20261109/test_verify.py
uv run --locked python research/experiments/parabola-1296-warm-start-20261109/verify_extensions.py research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/candidate.txt research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/extensions.txt
uv run --locked python research/experiments/parabola-1296-warm-start-20261109/test_extensions.py
uv run --locked python research/experiments/parabola-1296-warm-start-20261109/verify_two_add.py research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/candidate.txt research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/one-deletion-blockers.txt research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/two-add-blockers.txt
uv run --locked python research/experiments/parabola-1296-warm-start-20261109/test_two_add.py
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-1296-warm-start-20261109/audit_local_cnf.py
uv run --locked python research/experiments/parabola-1296-warm-start-20261109/check_local_proof.py
uv run --locked python research/experiments/parabola-1296-warm-start-20261109/audit_slice.py
uv run --locked python research/experiments/parabola-local-repair-20261109/verify.py --audit research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/candidate.txt --receipt /tmp/q2647-1303-geometry.json
```

`probe.py` と `probe_1298.py` は最初の二実行の固定source snapshot、`probe_from_witness.py` は次の実行以降の汎用worker。実行ごとにworker・符号化・初期値・CNFのハッシュを記録し、既存出力先を上書きしない。探索を再実行する場合は必ず新しい `--output` を指定する。

## 1322点の固定対スライス

別に、K0712の符号化で `d=1323`、空対3以下（1322点以上）を調べた。100,000衝突（10.61秒）、1,000,000衝突（120.17秒）の両試行は **UNKNOWN**。実際のCNFは **7,926変数・68,404節**で、両試行の展開後SHA-256は同じ `8cbd404a7e01bcc3ea0d32fe770d105c38b6c8ee241c018cf8a070a0dcb9f48a`。結果とCNFは `../parabola-ternary-selection-20261109/output/target1322-d1323-20261109/` と `../parabola-ternary-selection-20261109/output/target1322-d1323-1m-20261109/` にある。いずれも固定対の一部分であり、全体の上界を改善しない。
