# 11×11 reply27：次候補S4への新規direct exact S5 LOSS 3件（2026-10-11）

開始時のmain：`f33693cdd8be54738cedea8fc141553209c9a669`。標準11×11の2石root `{60,27}` を対象とする。

## 目的と実施内容

前回の全S6 WIN伝播によって有力S4 `(1188950301626859520,536870912)` がWINになった。残る第三手は `{100,108}` で、両方を覆う次の最小UNKNOWN S5数のclass `(1297036692683752448,0)` の完全106 S5子境界を追った。開始時はLOSS 7、WIN 0、UNKNOWN 99。

既存の`output/merged-exact-s5.cache`、全S4・S5合法幾何、およびmainの他担当の最新結果を確認。canonicalかつ未登録の、legal84の単親候補、legal92・94の共有親候補を選定した。

| 新規canonical S5 | legal | 2M budget（cold） | 15M budget（cold） |
|---|---:|---|---|
| `(10412322338480590849,0)` | 84 | UNKNOWN 2,000,000 nodes | **LOSS 5,416,337 nodes** |
| `(1297036692750861312,0)` | 92 | UNKNOWN 2,000,000 nodes | **LOSS 5,026,776 nodes** |
| `(1301540292311122944,0)` | 94 | UNKNOWN 2,000,000 nodes | **LOSS 3,454,253 nodes** |

exact判定の15M再試行合計13,897,366 nodes。2Mの全3試行も含む累計19,897,366 nodes。3つともraw solver direct exact LOSS、WINは0。ソルバーの変更・共有TT・saved S5 cacheの読み込みは行わない冷たい独立root replay。使用ソルバーは新main `f33693c` の`cpp/solvers/kyouen_dfpn_root.cpp` から `g++ -O3 -std=c++20 -DNDEBUG` で構築、`--memo=22 --n=11 --exact-order=count`。

## 幾何監査・更新後frontier

`scripts/audit.py` はsolverから独立した整数幾何 `independent.Board` で、3局面それぞれの合法手数・canonical・五石・対象S4親子関係・完全106子境界・rawの正しい予算と出力形式を検査。旧cache 5,752 exact rowsとverdict conflict 0で整合し、隔離keyをcacheへ入れない。結果の3 S5 LOSSのみ追加した。

| 指標 | 最終状態 |
|---|---:|
| exact S5 cache | **5,755**（WIN159 / LOSS5,596） |
| 対象S4 106子境界 | **LOSS10 / WIN0 / UNKNOWN96** |
| 全3384 S4 class | LOSS31 / WIN274 / UNKNOWN3079 |
| 第三手被覆 | 117/119 |
| 未被覆 | `{100,108}` |
| 有理LP双対・必要追加LOSS class最小値 | 1 |

対象S4はUNKNOWNのまま。rank更新では引き続き第1位（未確定子数96）。参考の履歴打切りproxyは約531,448,656 nodesだが、完成までの計算量の上界でも予測時間でもない。さらに低legal候補を探索する際、既存raw履歴の再監査と他エージェント重複防止を優先。

## 再現

```sh
python3 research/experiments/n11-reply27-next-candidate-20261011/scripts/audit.py
python3 research/experiments/n11-two-target-design-20261010/scripts/analyze.py \
  --cache research/experiments/n11-reply27-next-candidate-20261011/output/merged-exact-s5.cache \
  --out research/experiments/n11-reply27-next-candidate-20261011/output/new-ranking
```

raw入力・2M・15M出力は`output/raw/`、SHA-256つき監査受領票は`output/audit.json`、最新candidate frontierは`output/new-ranking/`に保管。

**証拠の限界**：S5 LOSSは直接raw solver-trusted exact判定であり、それぞれ終局までの独立なterminal-only proof DAGはまだ生成していない。11×11空盤および `{60,27}` の勝敗もUNKNOWNのまま。
