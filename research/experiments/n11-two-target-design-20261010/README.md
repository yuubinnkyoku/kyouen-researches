# 11×11 reply27: 残る第三手100・108の対称性と共有探索

2026-10-10。対象は標準通常版の二石局面 `{60,27}` のみ。開始時の `main` は `1739ddf2f9a5ec411ad5aeb0a2d8f9259951597c`。並行担当が開始後に3 S5 LOSSをmainへ追加したため、最終統合時は `4a9ea150faca7f49a94b453eebfb87d2c22b57b7` を土台にして衝突なしで再計算した。この実験の根拠を超えて空盤勝敗を主張しない。

## 第一の結論：2-class分離案は幾何的に成立しない

盤面番号は `11r+c`。縦軸反射 `f(11r+c)=11r+(10-c)` は石60=(5,5)と27=(2,5)をそれぞれ固定し、100=(9,1)を108=(9,9)へ移す。反射は四点共円・四点共線の禁止条件と合法手・終局条件・勝敗を保つ。このため二つの第三手は**同じ勝敗**である。

`{60,27}` を含むS4 classはD4正規化した二手目集合の同値類である。あるclassの表現の一つが第三手100を含めば、反射した表現は108を含み、**同じclass**に属する。したがって「100のみを覆うclass」「108のみを覆うclass」は存在しない。全3,384 classの保存済み独立整数幾何を再集計すると、両方を覆う115 classのみが該当し、基準cacheでは53 WIN・62 UNKNOWN・0 LOSSであった。必要追加LOSS class数1と有理双対1はこの構造と整合する。

これは「1-class戦略が常に探索費用最小」という主張ではない。classを複数保留し、早期棄却・証拠共有を使った**探索順序**を最適化する余地はある。しかし2-classに分離して別々の第三手を覆う利益はない。1つのS4 LOSS classが決定すれば両方一度に覆える。

## 再計算可能な全候補・探索順位

`scripts/analyze.py` はK0372で独立監査した `n11-strategy-redesign-20261010/output/geometry.json.gz`（全3,384 classの全S5境界）を読み、K0371隔離済みcacheと結合する。既存の `history.json` と legal手数10刻みの15M打切り費用を使った**計算量の参考指標**も出す。候補ごとの `WIN/LOSS/UNKNOWN`、未知数、legal範囲、履歴node、S5共有数と順位は `output/post-probe/candidate-classes.csv` 全115行に記録する。

実験開始時exact S5 cache: 5,738行（WIN158 / LOSS5,580 / conflict0）。並行担当による3件追加後の統合基準cacheは5,741行（WIN158 / LOSS5,583）。S4はともにLOSS31 / WIN272 / UNKNOWN3,081、被覆117/119。

| 比較 | 1 class + 順次probe（A） | 第三手ごと2 class（B） | 共有S5優先 + 1-class着地（C） |
|---|---|---|---|
| 証明の論理 | 少なくとも1 class全S5 LOSS | 分離した対象が存在しない | 最終的に1 class全S5 LOSS |
| 開始候補 | `1188950301626859520:536870912`, 開始98→最終93 UNKNOWN | 100専用0 / 108専用0 | 生存62 classを同時管理 |
| 開始S5重複 | class単独で0 | 定義不能 | 生存62 class: UNKNOWN延べ6,469 / distinct4,580 |
| S5共有の内訳 | 他生存classとも重なるのは当初60/98 | 定義不能 | 1親2,691、2親1,889（未知S5） |
| 実測nodes | この研究で単独方式を新規実行せず | 不適用 | 2M打切り2本 + 15M再試行2本＝12,692,123 |
| exact新規判定 | 比較試行なし | 不適用 | S5 LOSS 2、WIN0、S4新LOSS0 |
| 被覆増 | 未実験 | 不適用 | 0、117/119 |
| 全証明予測 | 完了費用は不明 | 分離案は不可 | 完了費用は不明。参考指標を下表に示す |

Cの2 probeは**実験開始時点で新規の対象**。公平なA対Cの統制実験ではないため、実測の高速化を主張しない。正しいexact cacheを共有するAも、すでに得られた同じS5判定を当然再利用できる。新探索の優位性は未確認である。

15M打切り参考費用は、過去に従来のrankingが選んだS5子のlegal帯別平均nodesを未知子へ加算したもの。未解決時の右打切りと選択バイアスがあり、証明費用の上界でも期待値でもない。

| post-probe順位 | S4 class | UNKNOWN / LOSS | 参考費用（nodes） |
|---|---|---:|---:|
| 未知数1位・費用1位 | `1188950301626859520:536870912` | 93 / 16 | 530,074,017 |
| 費用2位 | `1297036692683752448:0` | 99 / 7 | 546,960,118 |
| 費用3位 | `1297036830122704896:0` | 100 / 7 | 549,330,121 |

参考値の差は小さい。順位だけではどのclassが実際にLOSSになるか判定できない。候補間の共有局面を活用しつつ、早期S5 WINにより速やかに棄却する運用を推奨する。

## 独立S6境界を使った共有調査

`scripts/s6_overlap.py` はK0372の独立 `Board` で上位5 classの未知S5全子（S6）を再生成する。S6遷移延べ48,561、各class内の重複を除いたS6集合を足すと26,126、5 class間でまとめると25,274 distinct、**異なるclass間で852件の重複**（各class集合の延べ約3.3%）だった。一方、各class内ではS6 childの延べ9,367に対し5,342 uniqueなど、重複が約44%ある。class間の共有より、1 class内のS6を重複なく処理する工夫にも価値がある。

古い `history.json` 内のexact S6との交差は66 WIN・0 LOSS（この対象集合について）。履歴の後の回収分を含む完全なS6監査ではないため、現時点で「S6 LOSS witnessがない」と結論してはならない。またS6 LOSSを作るときにS7 LOSSを1子だけ見ても不十分であり、**全合法S7子のLOSS**が必要。S5 LOSSにはS6 LOSS1個で十分。既存の独立DAG検査とは別に保持する。

## 少数の新しいdirect exact probe

現mainで未解決、履歴上同budget以上のUNKNOWNがない共有S5を2つ選んだ。solver sourceは `cpp/solvers/kyouen_dfpn_root.cpp` SHA-256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`。Intel Core i5-9400T / Debian g++ 14.2.0、binary SHA-256 `98aadf580119ea3fb89be77fa161defded6feb87f5cb2f30b0503e35a4163c01`。Linux g++ `-O3 -std=c++20 -DNDEBUG`、`--n=11 --memo=22 --only=5 --exact-order=count`、1 workerでの保存raw。

| S5 canonical key | legal | 2M | 15M | 15M消費nodes | 生存S4への寄与 |
|---|---:|---|---|---:|---|
| `1152921504606851072:536870946` | 98 | UNKNOWN | **LOSS** | 3,651,923 | 2 classでUNKNOWN子が1減る |
| `1188950301626860544:536870912` | 99 | UNKNOWN | **LOSS** | 5,040,200 | 2 classでUNKNOWN子が1減る |

exact決着分8,692,123 nodes、2Mの打切り再試行を含む総数12,692,123 nodes。2つのS5は同じ基準cacheからcold replayした。保存rawには2MのUNKNOWNも残したが、cacheへは入れない。

`scripts/verify_and_merge.py` は保存rawの11列を検査し、独立整数幾何 `independent.Board(11)` でS5安全性・canonical・合法手数・S4親の完全合法境界所属を検査。隔離規則によるcache読み込み拒否も行い、衝突なしで並列担当3件を含む基準cache5,741行から5,743行へ統合した。これらの独立検査はsolverの**最終勝敗を終局まで再証明したものではない**。従って「solver-trusted exact」と記す。

統合後cache: WIN158 / LOSS5,585 / conflict0、S4 LOSS31 / WIN272 / UNKNOWN3,081、被覆117/119、残り100と108、最小追加LOSS class1、有理双対1。新たなS4 LOSS/WINはゼロ。

## 再現手順

必要物はPython 3.11以上の標準ライブラリ・同repoの既存独立整数幾何。新しい外部依存はない。

```sh
python3 research/experiments/n11-two-target-design-20261010/scripts/verify_and_merge.py
python3 research/experiments/n11-two-target-design-20261010/scripts/analyze.py --cache research/experiments/n11-two-target-design-20261010/output/merged-exact-s5.cache --out research/experiments/n11-two-target-design-20261010/output/post-probe
python3 research/experiments/n11-two-target-design-20261010/scripts/s6_overlap.py
```

初期snapshotでの参考計算は `analyze.py` に引数なしで実行。原始rawと入力、stdout logは `output/raw/` に保管し、`output/probe-audit.json` にそれぞれSHA-256を記録した。solver binary自体はコミットせず、その再コンパイル元SHAを残す。

## 次の探索担当者向け（定型実験）

1. 最新 `main` と作業treeを確認し、他担当の同じS5/S6探索が進行中でないことを確認する。基準cacheは必ず更新された正本を選び、隔離対象を排除する。旧履歴上の2M/15M UNKNOWNとexactを再点検する。
2. 継続対象は `(1188950301626859520,536870912)`（現時点93 UNKNOWN、16 LOSS）。共同探索を優先する場合の未着手共有S5の一例は `(1188950301626859520,536870944)`、legal98。これは他の生存S4 `(1297036692683751424,131072)` とも共有する。既存計画の単独child `(3494793310840553472,536870912)`（legal88）は比較候補として残すが、他エージェントが探索中なら絶対に重複実行しない。候補のprioritized一覧は `output/post-probe/shared-s5-tasks.csv`。
3. まず1 worker・2M nodesのcold exact replayを実施。UNKNOWNの場合はrawとS6/S7交差、過去の同budget以上のUNKNOWNを再点検してから、同じsolver/設定の15Mへ上げる。新しいbudget=0 projectionや未完UNKNOWNをexactに使わない。
4. **S5 WINが1つでも確定すれば、その局面を合法子に持つ全S4 classをWINとして棄却**し、当該classのcompletionを中止。S5 LOSSは全子条件を満たした証明ではなく1個の確定結果としてのみ加算する。
5. 15MでもUNKNOWNなら、S6を全合法生成し、まず保存exact S6とreverse parentを照合する。新S6 LOSS witnessが必要なら、S6の**全S7 LOSS**を示す探索・境界検証が必要。探索見積もりが高い場合はそのtargetを保留して別候補を試す。大量completionへ一気に移らない。
6. raw input/output/log・binary/source SHA・geometry audit・cache merge receipt・全3384 S4再分類・119第三手被覆と整数最小被覆および有理双対を保存。新classが完了するまで `{60,27}` や空盤の勝敗を更新しない。push直前に `main` の移動を検査し、branch/PRは作らない。

全証明を最短で完成する探索戦略はまだ確定できていない。とくに、WINの発見確率とS6 LOSS証明費用を未選択局面へ外挿する際の選択バイアスは未解決である。

## 統合時の既存リンク修正

新規K項目を追加してknowledgeを再生成した際、既存のK0355にGit管理されていないv5 artifact inventoryへの参照が存在していたためcheckが失敗した。GitHub履歴で当該v5のコミットを確認できず、同系列のv6を保持したうえで、K0355の**存在しないv5 artifactリンク3行のみ**を削除した。一次資料やv6のハッシュ・実験データを捏造・書換えしていない。

## 並列担当との統合記録

本作業中に別担当が同じS4 classのlegal88/89のS5 3局面をexact LOSSとし、main commit `4a9ea150faca7f49a94b453eebfb87d2c22b57b7` に反映した。うち `3494793310840553472:536870912` は本研究で再探索を避ける比較用候補として挙げていた局面に当たり、こちらで起動せず再利用できた。この3件と新規2件は互いに異なる正規化S5であり、併合cacheにverdict conflictはない。
