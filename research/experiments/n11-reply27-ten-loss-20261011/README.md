# 11×11 reply27: 最有力S4候補の未確定S5を10件追加解決（2026-10-11）

この実験は標準共円ゲームの2石根 `{60,27}` の完全境界を前進させる。開始時の最新版mainは `3db4b36cd647bf895c96f4484e0884d20b29e5d3`。他のエージェントによるS5 proof DAG bundleが同mainに存在するが、今回はそれとは**別の10局面**を独立に再探索した。

## 対象と選定

S4 `(1297036692683752448,0)`、第三手coverage `{100,108,110,120}`、完全なcanonical S5子106個のうち、既知LOSS10・WIN0・UNKNOWN96。前回の `research/experiments/n11-reply27-next-candidate-20261011` のcacheと候補表を正本の出発点として、未確定子の合法手数昇順6件と、別の生存S4にも属する子4件を選んだ。新規S5は全10件で、いずれもcache未登録だった。

各局面を同一binary・count-asc・`--memo=22`・cold別rootで200万node試行すると、すべてUNKNOWN。1,500万nodeの再探索では10件すべて**直接exact LOSS**になり、WIN0件だった。

| S5 canonical key | legal | 15M exact nodes | 他の生存S4と共有 |
|---|---:|---:|---|
| `(3602879701897446400,0)` | 89 | 2,742,740 | いいえ |
| `(5908722711111140352,0)` | 89 | 3,182,164 | いいえ |
| `(1297036692683760640,0)` | 90 | 14,122,712 | いいえ |
| `(1297036692683752480,0)` | 91 | 3,983,104 | いいえ |
| `(1297036761403229184,0)` | 92 | 6,522,725 | いいえ |
| `(1297036692683883520,0)` | 93 | 4,100,570 | いいえ |
| `(10376293541461626881,32)` | 95 | 3,777,766 | はい |
| `(1297036830122705920,0)` | 95 | 3,670,909 | はい |
| `(1297107061427930112,0)` | 95 | 7,147,572 | はい |
| `(10376293541461626881,65536)` | 96 | 3,074,874 | はい |

確定再探索nodes総計は **52,325,136**。予備探索10×2Mを含めた、**完了したraw行**の合計は **72,325,136 nodes**。

**中断の取り扱い**：最初に3局面まとめて実行した `group1b-15m.csv` は環境の約60秒の呼び出し制限に達した。その時点までに記録された1個の完全なLOSS行だけを採用し、後続の未記録2件を `single91-15m.csv`・`single92-15m.csv` で各1件ずつ別途再試行して両方LOSSを確認した。中断プロセスが最後に費やしたがraw行に残らなかった計算量は総計に含めない。UNKNOWN行をLOSSに昇格させていない。

## 独立幾何監査と全探索境界

`scripts/audit.py` により、solverから独立した整数幾何 `independent.Board` で各S5局面のcanonical性・占有石数5・合法手数・完全なS4/S5親子関係を検証した。隔離cache keyを拒否し、旧5,755件の既存exact S5との矛盾がないことを確かめ、10件のLOSSだけを合成した。

| 指標 | Before | After |
|---|---:|---:|
| exact S5キャッシュ | 5,755 | **5,765** |
| WIN / LOSS | 159 / 5,596 | **159 / 5,606** |
| 対象S4のS5 LOSS / WIN / UNKNOWN | 10 / 0 / 96 | **20 / 0 / 86** |
| 全3,384 S4：LOSS / WIN / UNKNOWN | 31 / 274 / 3,079 | 31 / 274 / 3,079 |
| 第三手被覆 | 117 / 119 | 117 / 119 |
| 未被覆 | `{100,108}` | `{100,108}` |

対象S4は今もUNKNOWN。最小追加LOSS class数は依然1、有理LP双対値も1。新たなliveな未確定S5は合計4,525 distinct、そのうちほかの未確定S4と共有される局面は1,823（2親）。

本実験の更新ランキングでは引き続き対象S4が未確定子数最小の首位（86個）。履歴legal-decileによる参考の15M打切り費用proxyは479,485,981 nodesに下がったが、これは最終判定までの予測量や上界ではない。

## 再現

```sh
python3 research/experiments/n11-reply27-ten-loss-20261011/scripts/audit.py
python3 -m unittest discover -s research/experiments/n11-reply27-ten-loss-20261011/tests -v
python3 research/experiments/n11-two-target-design-20261010/scripts/analyze.py \
  --cache research/experiments/n11-reply27-ten-loss-20261011/output/merged-exact-s5.cache \
  --out research/experiments/n11-reply27-ten-loss-20261011/output/new-ranking
```

- `output/raw/`：cold入力・2M UNKNOWN・15M exact LOSSの生CSV。中断されたgroup1bも完全行だけをそのまま保存。
- `output/audit.json`：全raw SHA-256、対象canonicalキーと親子監査、leaf trust区分、全3,384 classの最新境界。
- `output/merged-exact-s5.cache`：既存5,755＋新規10だけを追加した監査済みcache。
- `output/new-ranking/`：全115対象classと共有S5 taskの再集計。
- `tests/test_audit.py`：誤WIN挿入、合法手数改ざん、行重複、行欠落、AND/OR極性の回帰5件。

使用した実行binaryのSHA-256は `2878dc74ab1228c1bba6b13140dcd8f65f457f9813ae98d801a1709c77497ee5`、buildはmain `f33693c` の`cpp/solvers/kyouen_dfpn_root.cpp`から `g++ -O3 -std=c++20 -DNDEBUG`。実験中の最新mainには後から証明bundle capture実装が入っていたが、今回の探索は従来のcold exact replayで行った。

**証明の限界**：10件のS5 LOSSはsolverのdirect raw exact verdictである。上位の合法幾何とcache整合性は独立検証済みだが、10件それぞれの根から終局までのtrusted-leaf-zero DAGをまだ生成・検証したわけではない。11×11空盤と2石根 `{60,27}` の勝敗はなおUNKNOWN。
