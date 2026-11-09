---
id: K0711
title: 剰余放物線Q_2647の独立監査済み範囲は1296以上1323以下
kind: proposition
status: computed
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線・共円四点を含まない安全集合
- type: supports
  target: K0706
  note: 従来の全d監査による1324より強い、3形状DRAT監査の上界1323
- type: depends_on
  target: K0097
  note: 安全集合は完全対を高々一つしか含まず、h+1点を3形状に分類できる
- type: depends_on
  target: K0334
  note: 整数共円行列式が0なら四パラメータ和が0 mod pとなる必要条件
artifacts:
- path: research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/candidate.txt
  role: certificate
  note: 現在の下界を与えるソート済み1296パラメータ。点は(t,t² mod 2647)
- path: research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/geometry.json
  role: data
  note: generic 4×4整数行列式で44277012候補を検査、禁止四点0件。入力・ソースhash付き
- path: research/experiments/parabola-local-repair-20261109/verify_subset.cpp
  role: verifier
  note: 探索・CNF・edge cacheを読まない独立整数幾何検査器
- path: research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/model.json
  role: certificate
  note: 初回1292点構成に用いた固定d=1323の41違反割当。最適性は未主張
- path: research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/assessment.json
  role: data
  note: 元53886節の直接評価41違反、1325点から33点除去した1292点候補
- path: research/experiments/parabola-local-repair-20261109/walk_initial.cpp
  role: solver
  note: 実際の100万flip・seed20261109の局所探索ソース
- path: research/experiments/parabola-local-repair-20261109/verify.py
  role: verifier
  note: 小規模比較回帰と明示的な証人監査の再現ドライバ
- path: research/experiments/parabola-local-repair-20261109/regression.json
  role: data
  note: 4玩具CNF、96小集合の2モード比較、7不正入力制御とhash照合
- path: research/experiments/parabola-local-repair-20261109/README.md
  role: source
  note: 初回1292点構成、再現手順と信頼境界
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_class_2647_1323.json
  role: data
  note: 旧4形状UNSAT記録。000/101はK0713の変数衝突があり、幾何上界の根拠への採用を保留
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_b_single_2647.json
  role: data
  note: サイズ1324の形状(b)がUNSAT（形状(a),(c)は別記録）
- path: research/log/2026-11-09-p2647-near-miss-and-size-1323.md
  role: source
  note: 形状クラス判定の方法と結果
- path: research/log/2026-11-09-a2647-size1323-receipts-regenerated.md
  role: source
  note: サイズ1323の4形状クラスのreceipts再生成（全UNSAT、節数は旧ログ表と全件一致）
- path: research/experiments/parabola-local-repair-20261109/output/walk-1000000-seed20261109/candidate.txt
  role: certificate
  note: 初回1292点証人。新しいSAT探索のphaseの起点としても保持
- path: research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/input.cnf.gz
  role: data
  note: 低側・高側・空対と空対32以下を符号化した142992節の実入力
- path: research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/model.json
  role: certificate
  note: 全142992節を満たす保存モデル。空対29、1296点を選択
- path: research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/result.json
  role: data
  note: 1293点以上を要求したSAT試行が1296点を返した記録。幾何検査は別artifact
- path: research/experiments/parabola-ternary-selection-20261109/ternary.py
  role: solver
  note: 直接投影節を点選択制約へ変換し、空対数を制限する探索器
- path: research/experiments/parabola-ternary-selection-20261109/regression.py
  role: verifier
  note: 19392三値割当・444 cardinalityケースと保存CNF・モデル・幾何receiptの再評価
- path: research/experiments/parabola-ternary-selection-20261109/regression.json
  role: data
  note: 小規模完全照合、既存1292点の適合性、現在の1296点モデルの全節充足確認
- path: research/experiments/parabola-hplus1-drat-20261109/input/verified_edges.txt.gz
  role: data
  note: 上界に使う53886禁止四点の部分集合。全件を独立整数行列式で検査
- path: research/experiments/parabola-hplus1-drat-20261109/input/geometry.json
  role: data
  note: 全提供辺の健全性を検査したreceipt。辺集合の完全性は上界に不要
- path: research/experiments/parabola-hplus1-drat-20261109/verify_edges.cpp
  role: verifier
  note: 探索generatorを使わないgeneric整数4×4の禁止四点検査
- path: research/experiments/parabola-hplus1-drat-20261109/output/shape-a/audit.json
  role: data
  note: 形状(1,0,0)の1324点不存在CNFのDRAT受理記録
- path: research/experiments/parabola-hplus1-drat-20261109/output/shape-b/audit.json
  role: data
  note: 形状(0,1,0)の1324点不存在CNFのDRAT受理記録
- path: research/experiments/parabola-hplus1-drat-20261109/output/shape-c/audit.json
  role: data
  note: 形状(1,1,1)の1324点不存在CNFのDRAT受理記録
- path: research/experiments/parabola-hplus1-drat-20261109/output/replay-20261109/summary.json
  role: data
  note: 後日の実DRAT再生も全3件VERIFIED。入力・証明・検査器sourceとbinaryのhash付き
- path: research/experiments/parabola-hplus1-drat-20261109/regression.py
  role: verifier
  note: 5917配置の幾何照合、全提供辺検査、全入力再生成と明示的counter節の別実装照合
- path: research/experiments/parabola-hplus1-drat-20261109/regression.json
  role: data
  note: 3形状の構造・小例・hash照合の実測結果。DRAT受理とは別の検査
- path: research/experiments/parabola-hplus1-drat-20261109/README.md
  role: source
  note: 保存された3入力・DRAT証明と再生方法、上界への論理と信頼境界
- path: research/experiments/parabola-size1323-drat-20261109/output/qualification-final.json
  role: data
  note: 修正版と同一の1323点入力3形状はDRAT受理、残る112は検査未完了。全4形状は未完了
- path: research/experiments/parabola-size1323-drat-20261109/output/shape-112/proof-manifest.json
  role: data
  note: ローカルに保持する2127240行の未検査生証明のhash。生証明はGit非収録で受理証拠ではない
- path: research/experiments/parabola-monotone-rup-20261109/encoding_audit.py
  role: verifier
  note: CardEncを呼ばず修正後4入力の全節を独立schemaとprefix閾値counterへ比較し、全提供辺を再検査
- path: research/experiments/parabola-monotone-rup-20261109/output/encoding-audit-reservation.json
  role: data
  note: 1323点の全4入力で全節schema一致。辺53886件の整数幾何も再検査成功。UNSAT検査とは別
- path: research/experiments/parabola-monotone-rup-20261109/README.md
  role: source
  note: 閾値counterによる安全集合からCNFモデルへの拡張可能性とRUP-only検査の論理
scope: Q_2647={(t,t² mod 2647):0<=t<2647}の標準q=4安全集合。独立検査済み下界1296と3形状DRAT監査の上界1323。旧1322根拠CNFの一部にK0713の変数衝突があり、修正版の全4形状監査は未完了。正確値や他素数への一般化は主張しない。
evidence: 下界は1296点の独立整数幾何検査。上界は1324点の全3形状の入力・DRAT証明を保存し、53886提供辺の整数幾何健全性と全3本の修正版DRAT受理を確認。実証明の再生も全件成功。
---

## 命題と構成

**独立監査済みの範囲は1296 <= A(2647) <= 1323**。正確な最大値は未確定。
ソルバ主張による上界1322は、下記の別の証拠レベルとして保持する。

保存CNF（p=2647,d=1323、1323変数・53886節）へ局所探索を100万flip、seed=20261109で行い、
元CNFの41節に違反する割当を得た。Pythonでも元の全節を直接評価して41違反と一致した。
対応する1325点の等号テンプレートから、違反節の支持を被覆する33点を除き、初回1292点証人を構成した。
41は当該CNFの節削除距離の上界であり、最適値とは主張しない。

その後、[K0712](K0712-parabola-empty-pair-ternary-sat-reduction.md) の低側・高側・空対の符号化で、
原点と完全対d=1323を固定し、空対32以下（1293点以上）を要求した。
CaDiCaLは11.233秒でSATを返し、空対29・1296点を選択した。
保存した142992節を再生成してhashを照合し、保存モデルが全節を満たすことと点選択を直接検査した。
初回1292点証人はphase指定に使ったが、新しい集合が初回集合を包含するとは主張しない。

## 下界の独立検査

証人のパラメータの範囲・ソート・重複を検査し、座標を整数として再計算した。
探索とは別の検証器で、全117002820060選択四点を対象に必要合同式で候補を絞り、
44277012候補にgeneric 4×4 Leibniz行列式を適用して0件だった。生出力は
`2647 1296 117002820060 44277012`、終了コード0。

合同式フィルタの完全性は、行列式をmod pへ落とすとVandermonde積とパラメータ和の積になることによる。
異なる四パラメータで前者は非零だから、整数行列式0なら和は0 mod p。
各選択三点から唯一の第四パラメータを復元し、それが最大点のときだけ調べるので漏れ・重複がない。
検査器はCNF・モデル・edge cacheを使わない。したがって下界証人の安全性は、
局所探索やCNF符号化の正しさとは独立に確認される。

## 上界1323の独立監査

h=1323とし、原点の有無x、完全対数c、空対数eで点数は `|S|=h+x+c-e`。
安全集合には完全対が高々一つなので、1324=h+1点なら次の3形状が全てを尽くす。

| 形状(x,c,e) | CNF変数 | 節 | 保存DRAT行数 | 独立検査 |
|---|---:|---:|---:|---|
| (1,0,0) | 7938 | 73731 | 19525 | VERIFIED |
| (0,1,0) | 9260 | 76370 | 56616 | VERIFIED |
| (1,1,1) | 10582 | 79017 | 126556 | VERIFIED |

各対のBOTH/NONE/LOW/HIGHをexactly-oneで表し、BOTH・NONEの個数を制限する。
点選択補助変数は側の選択またはBOTHと同値なので、任意の当該形状の集合を表せる。
Cardinalityの実節は、明示的なprefix OR鎖の別実装と全3入力で一致した。
各提供四点を整数行列式で検査して真の禁止四点と確認したため、任意の安全集合はその回避節を満たす。
辺を一部しか使わなくても、CNFは安全集合に対する緩和であり、UNSATによる排除は健全である。
辺集合の完全性を仮定しない。

全3本のDRATをK0707修正版ソース
`34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b` からビルドした検証器で受理した。
入力を再生成し、入力・保存証明をhash照合した。後日の実再生でも全3本を受理（合計66419 RUP、0 RAT）。
従って1324点安全集合は存在せず、より大きい安全集合の1324点部分集合も存在し得ないので上界1323となる。

## ソルバ上界1322と未確定事項

従来の上界1324はK0706の全1323 dのDRAT監査による。上記3形状監査はそれを1323へ強化する。
1296点集合の最大性や空対29の最小性は未確定。1300点以上を求める別試行は60秒でUNKNOWNであり、
1300点の不存在を意味しない。
旧commit `666a778c` の「A(2647)<=1103」はp=2207の数値との混同で、その後 `48f916ca` で訂正された。
[訂正後の形状ログ](../../log/2026-11-09-p2647-no-size-h1-set-corrected.md) の1323を今回DRAT独立監査した。
一方、上界1322（サイズ1323の形状クラス判定）の旧ソルバ記録は、
[K0713](K0713-shape-cnf-auxiliary-variable-aliasing.md) の変数衝突が000/101で見つかり、そのままでは根拠として使えない。
当初その機械可読な記録は
(1,1,2) のみで、残り3クラスはログ表だけだったが、2026-11-09 に全4クラスを再実行して
receipts を再生成し、節数が旧ログ表と全件一致した
（[receipts再生成ログ](../../log/2026-11-09-a2647-size1323-receipts-regenerated.md)）。
修正後入力へ結び付けた監査は000/011/101の3形状が完了し、112はUNSAT証明を保存したが検査未完了。
さらに全4入力の全節を、CardEncを使わない別実装のone-hot・点同値・辺回避・prefix閾値counterへ照合した。
112のNONE=2を含め、重みkの任意の入力がcounterのモデルへ拡張できる節schemaと一致した。
全53886提供辺の整数幾何も再検査した。この写像の検査と、残るUNSAT証明の検査完了は別である。
全4形状の独立監査が揃うまでは、1322を監査済み範囲へ混ぜない。
本項は有限計算の証人検査であり、Lean形式証明ではない。
小集合96例の全四点検査・合同式フィルタ・Python整数行列式の一致は回帰であり、
一般的健全性の証明と区別する。
