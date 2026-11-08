---
id: K0711
title: 剰余放物線Q_2647の最大安全サイズは1296以上1322以下
kind: proposition
status: computed
topics: [maximum-safe, geometry, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共線・共円四点を含まない安全集合
- type: depends_on
  target: K0706
  note: 全1323 dの修正版DRAT監査による上界A(2647)<=1324
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
  note: サイズ1323の4形状クラスすべてUNSATの記録（上界1322の根拠）
- path: research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_b_single_2647.json
  role: data
  note: サイズ1324の形状(b)がUNSAT（形状(a),(c)は別記録）
- path: research/log/2026-11-09-p2647-near-miss-and-size-1323.md
  role: source
  note: 形状クラス判定の方法と結果
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
scope: Q_2647={(t,t² mod 2647):0<=t<2647}の標準q=4安全集合。有限存在証人による下界1296と、形状クラス判定による上界1322。正確値や他素数への一般化は主張しない。
evidence: 1296点証人を保存し、全117002820060選択四点を必要合同式と44277012回の直接整数4×4行列式で検査して禁止四点0件。上界はK0706の全d監査（A<=1324）と、サイズ1324・1323の全形状クラスのUNSAT（A<=1322）から従う。
---

## 命題と構成

**1296 <= A(2647) <= 1322**。正確な最大値は未確定。

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

## 上界と限界

上界1324はK0706の全1323 dのUNSAT証明の修正版DRAT監査と等号還元から従う。
1296点集合の最大性や空対29の最小性は未確定。1300点以上を求める別試行は60秒でUNKNOWNであり、
1300点の不存在を意味しない。
旧commit `666a778c` の「A(2647)<=1103」はp=2207の数値との混同で、その後 `48f916ca` で訂正された。
[訂正後の形状ログ](../../log/2026-11-09-p2647-no-size-h1-set-corrected.md) の上界1323はソルバ主張であり、
本項で独立監査済みとして採用した上界は1324。単一CNFのDRAT監査による強化は今後の課題である。
本項は有限計算の証人検査であり、Lean形式証明ではない。
小集合96例の全四点検査・合同式フィルタ・Python整数行列式の一致は回帰であり、
一般的健全性の証明と区別する。
