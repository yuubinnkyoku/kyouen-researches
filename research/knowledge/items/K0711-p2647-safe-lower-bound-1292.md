---
id: K0711
title: 剰余放物線Q_2647の最大安全サイズは1303以上1322以下
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
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/candidate.txt
  role: certificate
  note: 現在の下界を与えるソート済み1303パラメータ。点は(t,t² mod 2647)
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/geometry.json
  role: data
  note: generic 4×4整数行列式で45241569候補を検査、禁止四点0件。入力・ソースhash付き
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/model.json
  role: certificate
  note: 117652節を満たす保存モデル。空対22、1303点を選択
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/input.cnf.gz
  role: data
  note: 空対22以下を要求して実際に解いた三値CNF
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/extensions.txt
  role: certificate
  note: 1303点証人への各未選択点1344個について、追加を阻む禁止四点の証人
- path: research/experiments/parabola-1296-warm-start-20261109/extend.cpp
  role: solver
  note: 必要合同式と整数行列式により各未選択点の禁止四点証人を生成
- path: research/experiments/parabola-1296-warm-start-20261109/verify_extensions.py
  role: verifier
  note: 全未選択点の被覆と禁止四点を独立3×3整数行列式で検査
- path: research/experiments/parabola-1296-warm-start-20261109/test_extensions.py
  role: verifier
  note: 証人の欠落・改変を拒否する回帰
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/one-deletion-blockers.txt
  role: certificate
  note: 各未選択点の一削除後に許され得る削除点を絞る禁止四点群
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1303-seed1302-budget300000/two-add-blockers.txt
  role: certificate
  note: 残る12210組の二点追加をそれぞれ阻む禁止四点
- path: research/experiments/parabola-1296-warm-start-20261109/two_add.cpp
  role: solver
  note: 一削除後の単点追加に関する障害四点群の生成
- path: research/experiments/parabola-1296-warm-start-20261109/try_swap.cpp
  role: solver
  note: 一削除後の候補二点組に対する障害四点の生成
- path: research/experiments/parabola-1296-warm-start-20261109/verify_two_add.py
  role: verifier
  note: 障害四点群、削除候補の包含関係、候補二点組の全被覆を整数行列式で検査
- path: research/experiments/parabola-1296-warm-start-20261109/test_two_add.py
  role: verifier
  note: 点・二点組の障害証人の欠落と改変を拒否する回帰
- path: research/experiments/parabola-1296-warm-start-20261109/probe_local_swap.py
  role: solver
  note: 固定対と既存証人からの削除数を制限した三値SAT符号化
- path: research/experiments/parabola-1296-warm-start-20261109/audit_local_cnf.py
  role: verifier
  note: 局所CNFの再生成と符号付き削除数制約の小規模全数照合
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete2-budget300000/input.cnf.gz
  role: data
  note: 固定対・削除高々2点・1304点以上の保存CNF
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete2-budget300000/local-proof.drat.gz
  role: certificate
  note: 固定対・削除高々2点の部分問題のUNSAT証明
- path: research/experiments/parabola-1296-warm-start-20261109/check_local_proof.py
  role: verifier
  note: 二つのDRAT検査器と打切り証明の拒否を再現
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete2-budget300000/proof-check.json
  role: data
  note: 二方式の証明受理・打切り拒否と検査器ソースhash
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete3-budget300000/input.cnf.gz
  role: data
  note: 固定対・削除高々3点・1304点以上の保存CNF
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete3-budget300000/local-proof.drat.gz
  role: certificate
  note: 固定対・削除高々3点の部分問題のUNSAT証明
- path: research/experiments/parabola-1296-warm-start-20261109/check_local_incremental.py
  role: verifier
  note: 修正版増分検査器による証明受理と打切り拒否を再現
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete3-budget300000/incremental-check.json
  role: data
  note: 3点削除の証明検査結果と入力・検査器のhash
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete4-budget300000/input.cnf.gz
  role: data
  note: 固定対・削除高々4点・1304点以上の保存CNF
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete4-budget300000/local-proof.drat.gz
  role: certificate
  note: 固定対・削除高々4点の部分問題のUNSAT証明
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete4-budget300000/incremental-check.json
  role: data
  note: 4点削除の証明検査結果と入力・検査器のhash
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete5-budget1m/input.cnf.gz
  role: data
  note: 固定対・削除高々5点・1304点以上の保存CNF
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete5-budget1m/local-proof.drat.gz
  role: certificate
  note: 固定対・削除高々5点の部分問題のUNSAT証明
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1304-seed1303-delete5-budget1m/drat-trim-check.json
  role: data
  note: DRAT-trimによる証明受理・打切り拒否と入力・検査器のhash
- path: research/experiments/parabola-1296-warm-start-20261109/check_drat_trim.py
  role: verifier
  note: 固定版DRAT-trimのコンパイル、入力と証明のhash照合、証明受理と打切り拒否の再現
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1302-seed1301-budget1m/candidate.txt
  role: certificate
  note: 先行する1302点証人。新たなSAT探索のphaseとしても使用
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1302-seed1301-budget1m/geometry.json
  role: data
  note: generic 4×4整数行列式で45104559候補を検査、禁止四点0件。入力・ソースhash付き
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1302-seed1301-budget1m/model.json
  role: certificate
  note: 120204節を満たす保存モデル。空対23、1302点を選択
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1302-seed1301-budget1m/input.cnf.gz
  role: data
  note: 空対23以下を要求して実際に解いた三値CNF
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1301-seed1300-budget300000/candidate.txt
  role: certificate
  note: 先行する1301点証人。新たなSAT探索のphaseとしても使用
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1301-seed1300-budget300000/geometry.json
  role: data
  note: generic 4×4整数行列式で44964434候補を検査、禁止四点0件。入力・ソースhash付き
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1301-seed1300-budget300000/model.json
  role: certificate
  note: 122752節を満たす保存モデル。空対24、1301点を選択
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1301-seed1300-budget300000/input.cnf.gz
  role: data
  note: 空対24以下を要求して実際に解いた三値CNF
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1300-seed1299-budget300000/candidate.txt
  role: certificate
  note: 先行する1300点証人。新たなSAT探索のphaseとしても使用
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1300-seed1299-budget300000/geometry.json
  role: data
  note: generic 4×4整数行列式で44826944候補を検査、禁止四点0件。入力・ソースhash付き
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1300-seed1299-budget300000/model.json
  role: certificate
  note: 125296節を満たす保存モデル。空対25、1300点を選択
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1300-seed1299-budget300000/input.cnf.gz
  role: data
  note: 空対25以下を要求して実際に解いた三値CNF
- path: research/experiments/parabola-1296-warm-start-20261109/probe_from_witness.py
  role: solver
  note: 指定された既存証人をphaseとして与える固定d三値SAT探索
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1299-seed1298-budget300000/candidate.txt
  role: certificate
  note: 先行する1299点証人。新たなSAT探索のphaseとしても使用
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1299-seed1298-budget300000/geometry.json
  role: data
  note: generic 4×4整数行列式で44688249候補を検査、禁止四点0件。入力・ソースhash付き
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1299-seed1298-budget300000/model.json
  role: certificate
  note: 127836節を満たす保存モデル。空対26、1299点を選択
- path: research/experiments/parabola-1296-warm-start-20261109/output/target1299-seed1298-budget300000/input.cnf.gz
  role: data
  note: 空対26以下を要求して実際に解いた三値CNF
- path: research/experiments/parabola-1296-warm-start-20261109/probe_1298.py
  role: solver
  note: 監査済み1298点証人をphaseとして与える固定d三値SAT探索
- path: research/experiments/parabola-1296-warm-start-20261109/output/control-target1296/candidate.txt
  role: certificate
  note: 先行する1298点証人。新たなSAT探索のphaseとしても使用
- path: research/experiments/parabola-1296-warm-start-20261109/output/control-target1296/geometry.json
  role: data
  note: generic 4×4整数行列式で44554130候補を検査、禁止四点0件。入力・ソースhash付き
- path: research/experiments/parabola-1296-warm-start-20261109/output/control-target1296/model.json
  role: certificate
  note: 135432節を満たす保存モデル。空対27、1298点を選択
- path: research/experiments/parabola-1296-warm-start-20261109/output/control-target1296/input.cnf.gz
  role: data
  note: 空対29以下を要求して実際に解いた三値CNF
- path: research/experiments/parabola-1296-warm-start-20261109/probe.py
  role: solver
  note: 監査済み1296点証人をphaseとして与える固定d三値SAT探索
- path: research/experiments/parabola-1296-warm-start-20261109/verify.py
  role: verifier
  note: 保存モデルの全節・点選択と独立幾何receiptのhashを検査
- path: research/experiments/parabola-1296-warm-start-20261109/test_verify.py
  role: verifier
  note: 候補・モデル・worker hashの改変を拒否する回帰
- path: research/experiments/parabola-1296-warm-start-20261109/README.md
  role: source
  note: 既存証人からのphase指定、各試行と独立検査の再現範囲
- path: research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/candidate.txt
  role: certificate
  note: 先行する1296点証人。新たなSAT探索のphaseとしても使用
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
  note: 小規模完全照合、既存1292点の適合性、先行1296点モデルの全節充足確認
scope: Q_2647={(t,t² mod 2647):0<=t<2647}の標準q=4安全集合。有限存在証人による下界1303と、形状クラス判定による上界1322。正確値や他素数への一般化は主張しない。
evidence: 1303点証人を保存し、全119554191575選択四点を必要合同式と45241569回の直接整数4×4行列式で検査して禁止四点0件。各未選択点と一削除後の候補二点組すべてへの障害四点証人を独立検査。上界はK0706の全d監査（A<=1324）と、サイズ1324・1323の全形状クラスのUNSAT（A<=1322）から従う。
---

## 命題と構成

**1303 <= A(2647) <= 1322**。正確な最大値は未確定。

保存CNF（p=2647,d=1323、1323変数・53886節）へ局所探索を100万flip、seed=20261109で行い、
元CNFの41節に違反する割当を得た。Pythonでも元の全節を直接評価して41違反と一致した。
対応する1325点の等号テンプレートから、違反節の支持を被覆する33点を除き、初回1292点証人を構成した。
41は当該CNFの節削除距離の上界であり、最適値とは主張しない。

その後、[K0712](K0712-parabola-empty-pair-ternary-sat-reduction.md) の低側・高側・空対の符号化で、
原点と完全対d=1323を固定し、空対32以下（1293点以上）を要求した。
CaDiCaLは11.233秒でSATを返し、空対29・1296点を選択した。
保存した142992節を再生成してhashを照合し、保存モデルが全節を満たすことと点選択を直接検査した。
初回1292点証人はphase指定に使ったが、新しい集合が初回集合を包含するとは主張しない。

さらに既存の1296点証人をphaseに使い、空対29以下（1296点以上）を要求した別の三値SAT試行で、空対27・**1298点**を得た。保存した135432節と全モデルを別スクリプトで読み直し、全節充足と選択点・空対を照合した。phaseは探索順の指定であり、1298点集合が1296点集合を包含するという主張ではない。

この1298点証人をphaseに使い、空対26以下（1299点以上）を要求すると、空対26・**1299点**を得た。保存した127836節・モデル・選択点を別スクリプトで照合した。この集合が1298点集合を包含するとは主張しない。

さらに1299点証人をphaseに使い、空対25以下（1300点以上）を要求すると、空対25・**1300点**を得た。保存した125296節・モデル・選択点を別スクリプトで照合した。この集合が先行証人を包含するとは主張しない。

同様に1300点証人をphaseに使い、空対24以下（1301点以上）を要求して、空対24・**1301点**を得た。保存した122752節・モデル・選択点を別スクリプトで照合した。

1301点証人をphaseに使い空対23以下を要求した30万衝突の試行はUNKNOWNだった。同じphaseで100万衝突に増やした別試行では642734衝突でSATとなり、空対23・**1302点**を得た。保存した120204節・モデル・選択点を別スクリプトで照合した。

さらに1302点証人をphaseに使い空対22以下を要求すると、224843衝突でSATとなり、空対22・**1303点**を得た。保存した117652節・モデル・選択点を別スクリプトで照合した。

この1303点集合は**包含について極大**である。未選択1344点それぞれに対し、その点と選択済みの3点からなる禁止四点を明示し、全点の被覆と各四点の整数行列式ゼロを独立な3×3計算で確認した。これは1点も追加できないという意味であり、1303点が最大とは主張しない。

さらにこの同じ集合は、**選択済みの1点を削除して未選択の2点を追加する操作でも改善できない**。未選択点ごとの禁止四点群から、どの1点を削除しても追加できない点1221個を証明し、残る点について許され得る削除点を絞る。その結果生じる候補二点組12210組のそれぞれに、削除されない既存2点との禁止四点を保存した。独立検査器が各障害の整数行列式、未選択点の網羅、削除点集合の包含、全候補二点組の被覆を確認した。これは指定された局所操作の排除であり、複数点を削除する改善や別の1304点集合の不存在を意味しない。

さらに原点と完全対 `d=1323` を維持し、他の各対から高々一側を選ぶ範囲では、この証人から**高々2点の削除で1304点以上へ改善することもできない**。直接投影に基づく三値符号化と削除数制約を加えた33886変数・121584節のCNFはUNSAT。保存した24030行のDRATを、修正版増分検査器と毎回代入を再構築する別実装の両方が受理し、打切り証明を拒否した。CNFは再生成して一致し、符号付き削除数制約は小規模1008ケースで全数照合した。これは固定対・二点削除以内という条件付きの計算機援用証明であり、固定対を壊す改善や全1304点集合の不存在は示さない。

同じ条件で削除を**高々3点**まで許した35181変数・124172節のCNFについても、再生成した入力が保存されたCNFと一致し、修正版増分検査器が266831行の証明を受理、打切り証明を拒否した。こちらの別実装による検査は未完了。結論は固定対を維持する局所改善に限り、一般の1304点集合の不存在を意味しない。

さらに**高々4点**を削除する場合も、再生成された36474変数・126756節のCNFについて、修正版増分検査器が381164行の証明を受理し、打切り証明を拒否した。削除数制約は小規模1248ケースで照合した。別実装での4点削除証明の検査は未実施であり、この結論も固定対の下での局所的なものである。

同じ固定対の条件で**高々5点**を削除する場合も、再生成した37765変数・129336節のCNFと1256894行の証明を保存した。DRAT-trimが証明を受理し、先頭100行だけの打切り証明を拒否した。削除数制約は小規模1472ケースで照合した。固定対を壊す改善や、一般の1304点集合の不存在は示さない。

## 下界の独立検査

現在の1303点証人のパラメータの範囲・ソート・重複を検査し、座標を整数として再計算した。
探索とは別の検証器で、全119554191575選択四点を対象に必要合同式で候補を絞り、
45241569候補にgeneric 4×4 Leibniz行列式を適用して0件だった。生出力は
`2647 1303 119554191575 45241569`、終了コード0。先行する1296・1298・1299・1300・1301・1302点証人も独立幾何検査済みである。

合同式フィルタの完全性は、行列式をmod pへ落とすとVandermonde積とパラメータ和の積になることによる。
異なる四パラメータで前者は非零だから、整数行列式0なら和は0 mod p。
各選択三点から唯一の第四パラメータを復元し、それが最大点のときだけ調べるので漏れ・重複がない。
検査器はCNF・モデル・edge cacheを使わない。したがって下界証人の安全性は、
局所探索やCNF符号化の正しさとは独立に確認される。

## 上界と限界

上界1324はK0706の全1323 dのUNSAT証明の修正版DRAT監査と等号還元から従う。
1303点集合の最大性や空対22の最小性は未確定。1300点以上を求める旧試行は60秒でUNKNOWNだったが、
その後の今回の別phase指定で1300点の存在を確認した。
旧commit `666a778c` の「A(2647)<=1103」はp=2207の数値との混同で、その後 `48f916ca` で訂正された。
[訂正後の形状ログ](../../log/2026-11-09-p2647-no-size-h1-set-corrected.md) の上界1323はソルバ主張であり、
本項で独立監査済みとして採用した上界は1324。単一CNFのDRAT監査による強化は今後の課題である。
なお本項の上界1322（サイズ1323の形状クラス判定）もソルバ主張に基づく。当初その機械可読な記録は
(1,1,2) のみで、残り3クラスはログ表だけだったが、2026-11-09 に全4クラスを再実行して
receipts を再生成し、節数が旧ログ表と全件一致した
（[receipts再生成ログ](../../log/2026-11-09-a2647-size1323-receipts-regenerated.md)）。
1322についてのDRAT監査も今後の課題である。
本項は有限計算の証人検査であり、Lean形式証明ではない。
小集合96例の全四点検査・合同式フィルタ・Python整数行列式の一致は回帰であり、
一般的健全性の証明と区別する。
