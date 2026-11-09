---
id: K0711
title: 剰余放物線Q_2647の独立監査済み範囲は1302以上1322以下
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
  note: 従来の全d監査による1324より強い、4形状RUP/LRAT監査の上界1322
- type: depends_on
  target: K0097
  note: 安全集合は完全対を高々一つしか含まず、h点を4形状に分類できる
- type: depends_on
  target: K0334
  note: 整数共円行列式が0なら四パラメータ和が0 mod pとなる必要条件
artifacts:
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1303-remove4-budget100000/input.cnf.gz
  role: data
  note: 保存1302点から4点以下除去で1303点以上を要求した37749変数・129303節の新しい実入力
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1303-remove4-budget100000/result.json
  role: data
  note: 77.497秒・100005衝突でUNKNOWN。候補・モデル・証明はなく不存在を主張しない
- path: research/experiments/parabola-bounded-exchange-20261109/verify_unknown.py
  role: verifier
  note: UNKNOWNの初期記録・実入力byte再生成・変数予約・source hashとモデル等の不在を照合
- path: research/experiments/parabola-bounded-exchange-20261109/output/unknown-remove4-validation.json
  role: data
  note: 新しい4点以下除去の保存入力とUNKNOWNの出典を検査。SAT/UNSATの証拠ではない
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/candidate.txt
  role: certificate
  note: 現在の下界を与える1302点。保存1301点から3点を除き4点を追加
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/geometry.json
  role: data
  note: 全119187179475四点を合同式で被覆し45110020候補を整数行列式で検査、禁止四点0件
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/model.json
  role: certificate
  note: 1302点要求・元の証人から3点以下除去の全129266節を満たす37731変数の完全モデル
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/input.cnf.gz
  role: data
  note: 元の1301点から失う点数に逐次counterの上限3を課した保存入力
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1302-remove3-budget100000/result.json
  role: data
  note: 7.11秒・8180衝突で1302点SATを得た当時の記録。幾何の未検査表示は原記録として保持
- path: research/experiments/parabola-bounded-exchange-20261109/search.py
  role: solver
  note: 固定原点・完全対で選択点の除去数を制限するSAT探索。補助変数の予約上限を保持
- path: research/experiments/parabola-bounded-exchange-20261109/audit.py
  role: verifier
  note: 除去counterの真理値表、保存入力のbyte再生成、完全モデル全節・点抽出・交換差分と幾何receiptを照合
- path: research/experiments/parabola-bounded-exchange-20261109/output/audit-1302/audit.json
  role: data
  note: 768除去counterケース、全129266節、3不正モデル拒否、全変数固定の再生成功
- path: research/experiments/parabola-bounded-exchange-20261109/README.md
  role: source
  note: 有界交換の入力・再現手順と、1302点下界および次の近傍の信頼境界
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1303-remove3-budget100000/result.json
  role: data
  note: 保存1302点から3点以下除去の1303点要求のSOLVER_UNSAT原記録。後の独立LRAT受理とは分離して保持
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1303-remove3-budget100000/input.cnf.gz
  role: data
  note: 1303点要求の36457変数・126721節の実入力。全体を覆わない近傍条件付き
- path: research/experiments/parabola-bounded-exchange-20261109/output/target1303-remove3-budget100000/proof.drat.gz
  role: certificate
  note: 325093行の元DRAT。後にDRAT-trim -Uで受理し変換LRATを別実装で検査。旧RUP-only timeoutは保持
- path: research/experiments/parabola-bounded-exchange-20261109/audit_proof.py
  role: verifier
  note: 保存証明を削除無視・RAT禁止の既存RUP-only検査器で再生するドライバ
- path: research/experiments/parabola-bounded-exchange-20261109/output/proof-audit-1303.json
  role: data
  note: 当初のRUP-only検査は120秒でtimeout、verified false。後のLRAT受理と混同しない歴史的記録
- path: research/experiments/parabola-neighborhood-lrat-20261109/audit.py
  role: verifier
  note: 元DRATを固定upstreamのDRAT-trim -Uで検査・LRAT化し、空節処理修正版の別実装で再生
- path: research/experiments/parabola-neighborhood-lrat-20261109/verify_saved.py
  role: verifier
  note: 実入力のbyte再生成、補助変数領域、元DRAT・LRAT・ソース・制御例を照合
- path: research/experiments/parabola-neighborhood-lrat-20261109/output/target1303-remove3/result.json
  role: manifest
  note: 限定CNFの独立LRAT受理、43074行・80008871 bytesのhashとローカル所在。元DRATはGit管理済み
- path: research/experiments/parabola-neighborhood-lrat-20261109/output/saved-verification.json
  role: data
  note: 36457変数・126721節の実入力byte一致と全証拠hash、DRAT-trim6制御・修正LRAT5制御を照合
- path: research/experiments/parabola-neighborhood-lrat-20261109/output/trim-controls.json
  role: data
  note: K0707の4偽証明・直接偽空節を拒否しresolution正例を受理
- path: research/experiments/parabola-neighborhood-lrat-20261109/output/lrat-controls.json
  role: data
  note: K0714の原版偽受理を再現し、今回使った修正版の5制御の期待判定を確認
- path: research/experiments/parabola-neighborhood-lrat-20261109/README.md
  role: source
  note: 同じ保存証拠からの変換・独立検査の再現方法と有界近傍の範囲
- path: research/experiments/parabola-maximal-1300-20261109/output/exchange-remove-at-most-two/candidate.txt
  role: certificate
  note: 前段の1301点。保存1300点から1300と2262を除き385と610と1723を追加。今回の交換の種
- path: research/experiments/parabola-maximal-1300-20261109/output/exchange-remove-at-most-two/geometry.json
  role: data
  note: 全118821013025四点を合同式で被覆し44971096候補の整数行列式を検査、禁止四点0件
- path: research/experiments/parabola-maximal-1300-20261109/output/exchange-remove-at-most-two/result.json
  role: data
  note: 2点除去・3点追加の投影CNF候補を得た当時の記録。geometry未検査という原記録は保持
- path: research/experiments/parabola-maximal-1300-20261109/output/exchange-validation/completion-model.json
  role: certificate
  note: 1301点要求の旧UNKNOWN入力について全122752節を満たす35121変数の完全モデル
- path: research/experiments/parabola-maximal-1300-20261109/output/exchange-validation/validation.json
  role: data
  note: 3966点選択変数を証人に固定してモデル補完し全節充足・点抽出・幾何receiptのhashを照合
- path: research/experiments/parabola-maximal-1300-20261109/exchange.py
  role: solver
  note: 保存1300点に対して2点以下除去の交換候補を生成した固定ソース
- path: research/experiments/parabola-maximal-1300-20261109/exchange_seeded.py
  role: solver
  note: 証人入力を指定する交換探索版。1302点への局所的試行に使用
- path: research/experiments/parabola-maximal-1300-20261109/verify_exchange.py
  role: verifier
  note: 保存交換・幾何receipt・旧UNKNOWN入力への完全モデルの充足を照合
- path: research/experiments/parabola-maximal-1300-20261109/audit_saved_exchange.py
  role: verifier
  note: SAT・符号化generatorを使わず保存完全モデルの全節と点状態を再評価、3不正モデルを拒否
- path: research/experiments/parabola-maximal-1300-20261109/output/exchange-validation/saved-audit.json
  role: data
  note: 保存完全モデルの独立評価と新しい入力指定交換版の証人byte一致を確認
- path: research/experiments/parabola-maximal-1300-20261109/output/exchange-from1301/result.json
  role: data
  note: 1301点から36066除去候補を試し改善未発見。1302点の不存在は主張しない
- path: research/experiments/parabola-maximal-1300-20261109/README.md
  role: source
  note: 保存1300点の包含極大性と、別の1301点集合を得る交換の再現手順・信頼境界
- path: research/experiments/parabola-warm-improvement-20261109/output/target1301-warm1300-budget500000/input.cnf.gz
  role: data
  note: 当時UNKNOWNだった1301点要求の35121変数・122752節。今回のモデル補完は同じ入力を使用
- path: research/experiments/parabola-warm-improvement-20261109/output/target1299-warm1298-budget500000/candidate.txt
  role: certificate
  note: 前段の1300点のソート済みパラメータ。今回の2点除去・3点追加の起点
- path: research/experiments/parabola-warm-improvement-20261109/output/target1299-warm1298-budget500000/geometry.json
  role: data
  note: 全118455690925四点を合同式で被覆し44831921候補の整数4×4行列式を検査、禁止四点0件
- path: research/experiments/parabola-warm-improvement-20261109/output/target1299-warm1298-budget500000/model.json
  role: certificate
  note: 127836節を全て満たす37665変数の完全モデル。選択結果1300点、空対25
- path: research/experiments/parabola-warm-improvement-20261109/output/target1299-warm1298-budget500000/input.cnf.gz
  role: data
  note: 原点と完全対d=1323を固定し1299点以上を要求した実入力。以前UNKNOWNだった入力とbyte一致
- path: research/experiments/parabola-warm-improvement-20261109/output/target1299-warm1298-budget500000/result.json
  role: data
  note: 1298点をphaseに使い50万衝突予算で83.52秒・190902衝突で1300点を返したSAT記録
- path: research/experiments/parabola-warm-improvement-20261109/output/target1299-warm1298-budget100000/result.json
  role: data
  note: 当時の10万衝突予算ではUNKNOWNだった記録。現在は同じ入力の50万予算でSAT、旧記録は保持
- path: research/experiments/parabola-warm-improvement-20261109/output/target1297-warm1296-budget100000/candidate.txt
  role: certificate
  note: 前段の1298点証人。今回の探索のphase起点
- path: research/experiments/parabola-warm-improvement-20261109/output/target1301-warm1300-budget500000/result.json
  role: data
  note: 当時の1301点以上の探索は50万衝突予算・269.43秒でもUNKNOWN。現在は別の交換で存在を確認、旧記録は保持
- path: research/experiments/parabola-warm-improvement-20261109/verify_saved.py
  role: verifier
  note: 保存した全実入力の再生成・hash、完全モデルの全節充足と点抽出、独立幾何receiptを検査
- path: research/experiments/parabola-warm-improvement-20261109/output/verification.json
  role: data
  note: 1298点SATと1299点UNKNOWNの保存証拠・warm source・凍結符号化の照合結果
- path: research/experiments/parabola-warm-improvement-20261109/output/verification-1301-budget500000.json
  role: data
  note: 5保存試行を照合し、1300点証人の独立幾何と1301点の二予算UNKNOWNを確認
- path: research/experiments/parabola-warm-improvement-20261109/README.md
  role: source
  note: 1298点・1300点証人とUNKNOWNの範囲、凍結符号化・予算・再現手順
- path: research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/candidate.txt
  role: certificate
  note: 前段の1296点証人。今回の探索のphase起点
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
  note: 当時の3形状DRAT受理と112未完了のsnapshot。現在は後述のRUP/LRAT監査を採用
- path: research/experiments/parabola-size1323-drat-20261109/output/shape-112/proof-manifest.json
  role: data
  note: 当初保存した2127240行の原DRAT証明のhash。ローカル保持・Git非収録。受理根拠は別のLRAT receipt
- path: research/experiments/parabola-monotone-rup-20261109/encoding_audit.py
  role: verifier
  note: CardEncを呼ばず修正後4入力の全節を独立schemaとprefix閾値counterへ比較し、全提供辺を再検査
- path: research/experiments/parabola-monotone-rup-20261109/output/encoding-audit-reservation.json
  role: data
  note: 1323点の全4入力で全節schema一致。辺53886件の整数幾何も再検査成功。UNSAT検査とは別
- path: research/experiments/parabola-monotone-rup-20261109/README.md
  role: source
  note: 閾値counterによる安全集合からCNFモデルへの拡張可能性とRUP-only検査の論理
- path: research/experiments/parabola-drat-trim-20261109/output/qualified-upper-1322-preserved.json
  role: data
  note: 修正後の全4入力をschema・原入力hash・3 RUP受理と1 LRAT受理へ結び付けた上界1322の集約
- path: research/experiments/parabola-drat-trim-20261109/output/lrat-stream-replay-112/result.json
  role: data
  note: 残る112の943588行LRATをK0714局所修正版で受理。241.9秒、終了コード0、source/binary/proof hash付き
- path: research/experiments/parabola-drat-trim-20261109/output/lrat-core-preserved-manifest.json
  role: data
  note: 採用した2711546166 bytesのLRAT証明のhashとローカルraw pin。証明本体はGit非収録
- path: research/experiments/parabola-drat-trim-20261109/replay_lrat_stream.py
  role: verifier
  note: 大証明をstreamでhash検査しpreflightを先に永続化して局所修正版LRATを実行するドライバ
- path: research/experiments/parabola-drat-trim-20261109/qualify_upper.py
  role: verifier
  note: 全4入力のhashとschema、検査器回帰・受理receiptを照合し、全件受理時だけ上界を返す
- path: research/experiments/parabola-drat-trim-20261109/lrat-check-empty-fixed.c
  role: verifier
  note: 原版の偽空節受理をK0714で修正したhint検査器。空節には実際のRUP矛盾を要求
- path: research/experiments/parabola-monotone-rup-20261109/rup_check.cpp
  role: verifier
  note: 000/011/101を受理した削除無視・RAT禁止の追加列RUP検査器
- path: research/experiments/parabola-monotone-rup-20261109/output/regression.json
  role: data
  note: 上記RUP実装は毎回初期化するPython UPと516例で一致。K0707の4偽証明を拒否
- path: research/experiments/parabola-drat-trim-20261109/README.md
  role: source
  note: 指定upstream・局所修正・証拠の可用性とstream LRAT再生手順
scope: Q_2647={(t,t² mod 2647):0<=t<2647}の標準q=4安全集合。独立整数幾何検査の下界1302と、修正後のサイズ1323全4形状のRUP/LRAT反駁検査による上界1322。旧K0713の不正入力やK0714の原版LRAT受理は使わない。正確値や他素数への一般化は主張しない。
evidence: 下界は交換で得た1302点の独立整数幾何検査と完全モデルの全129266節の充足確認。上界は全4入力の全節を独立schemaへ照合し53886提供辺の整数幾何を検査。000/011/101はRUP-only追加列として受理、112は局所修正版LRATで受理。入力・証明・検査器hashを集約して全4件を確認。
---

## 命題と構成

**独立監査済みの範囲は1302 <= A(2647) <= 1322**。正確な最大値は未確定。
上界1322は、修正後入力に対する全4形状の反駁検査で確認した有限計算の結論である。

保存CNF（p=2647,d=1323、1323変数・53886節）へ局所探索を100万flip、seed=20261109で行い、
元CNFの41節に違反する割当を得た。Pythonでも元の全節を直接評価して41違反と一致した。
対応する1325点の等号テンプレートから、違反節の支持を被覆する33点を除き、初回1292点証人を構成した。
41は当該CNFの節削除距離の上界であり、最適値とは主張しない。

その後、[K0712](K0712-parabola-empty-pair-ternary-sat-reduction.md) の低側・高側・空対の符号化で、
原点と完全対d=1323を固定し、空対32以下（1293点以上）を要求した。
CaDiCaLは11.233秒でSATを返し、空対29・1296点を選択した。
保存した142992節を再生成してhashを照合し、保存モデルが全節を満たすことと点選択を直接検査した。
初回1292点証人はphase指定に使ったが、新しい集合が初回集合を包含するとは主張しない。

さらに、その1296点証人をphaseにし、1297点以上・空対28以下を要求した。
CaDiCaLは7.761秒・13815衝突でSATを返し、空対27・1298点の新しい証人を得た。
保存した40201変数・132904節の実入力を再生成し、完全モデルの全節充足と点選択を検査した。
warm startは探索のphase指定であり、既存の点を固定したり包含を要求するassumptionではない。

1298点をphaseにした1299点以上の入力は10万衝突予算ではUNKNOWNだったが、同じCNF・同じphaseで
予算を50万へ増やすと83.515秒・190902衝突でSATとなり、空対25・1300点を得た。
両入力のSHA-256は `ec55b41a9d5fee9fbe6e259b69f18ac2446b73d25094212a702034bf7648deb4` で一致する。
37665変数の完全モデルが全127836節を満たすこと、点抽出と保存証人の一致を検査した。

保存1300点集合から `{1300,2262}` を除き、`{385,610,1723}` を加える交換で1301点を得た。
原点と完全対d=1323は維持し、空対は24となる。投影CNFでの候補発見は6.21秒だった。
独立整数幾何検査に加え、以前UNKNOWNだった1301点要求の同じCNFへ3966個の点選択変数を全て固定し、
補助変数を補完した35121変数のモデルが全122752節を満たすことと、点抽出を確認した。
この補完では点選択を固定し、既知の証人に対する充足モデルを構成・検査した。
証人のSHA-256は `1e02ea20ab61516d267887a7a31fa1b2aefd4aa9c305da403c60468da9bfc27b`。

さらにその1301点集合から失う点数を3以下に制限し、1302点以上を要求する有界交換CNFを作った。
CaDiCaLは7.110秒・8180衝突でSATを返し、`{684,1430,1785}` を除き `{150,1217,1294,1963}` を加えた
1302点を得た。原点と完全対d=1323を維持し、空対は23。
保存入力のbyte再生成と、37731変数の完全モデルが全129266節を満たすこと、点抽出・交換差分を検査した。
追加した除去counterは768小規模割当で個数条件と一致し、実入力の補助変数予約上限にも衝突がない。
これは符号化の回帰であり、安全性の根拠は次の独立整数幾何検査である。
1302点証人のSHA-256は `5395d2326e08dfe8ac43b57103cc1d469ceddf68a0b522b4d7092e9db342000b`。

## 下界の独立検査

現在の1302点証人のパラメータの範囲・ソート・重複を検査し、座標を整数として再計算した。
探索とは別の検証器で、全119187179475選択四点を対象に必要合同式で候補を絞り、
45110020候補にgeneric 4×4 Leibniz行列式を適用して0件だった。生出力は
`2647 1302 119187179475 45110020`、終了コード0。

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

## 上界1322の独立監査

安全集合では完全対が高々一つなので、h=1323点の場合は `e=x+c`、x,c∈{0,1}より
次の4形状が全てを尽くす。

| 形状(x,c,e) | 変数 | 節 | 採用した反駁検査 |
|---|---:|---:|---|
| (0,0,0) | 7938 | 73727 | RUP-only、5326追加節 |
| (0,1,1) | 10582 | 79013 | RUP-only、61818追加節 |
| (1,0,1) | 9260 | 76374 | RUP-only、147006追加節 |
| (1,1,2) | 14544 | 85619 | K0714局所修正版LRAT、943588行、241.9秒で受理 |

全4入力の全節を、CardEncを使わないone-hot・点同値・辺回避・prefix閾値counterの別実装へ照合した。
counter補助変数が選択変数や他counterと重ならず、点補助変数より前の予約範囲に収まることも確認した。
112のNONE=2も、重みkの任意の入力をprefix閾値で拡張できる節schemaと一致する。
全53886提供辺の整数幾何も再検査したので、安全な当該形状の集合は対応CNFのモデルへ拡張できる。

000/011/101では、削除を消した追加列の全節をRUPで検査した。
RATは使わず、全追加が元CNFの論理的帰結となるため、削除された節も保持することは健全である。
112では抽出されたLRATを元の85619節に対し再生し、実際のRUP矛盾を要求する空節の受理まで確認した。
[K0714](K0714-lrat-empty-clause-vacuous-rat-unsoundness.md) の原版LRAT検査器の受理は採用しない。
入力・証明・検査器・回帰のhashを照合した集約で全4件の受理を確認した。
従って1323点安全集合は存在せず、より大きい安全集合の1323点部分集合も存在し得ないので上界は1322となる。

112の採用LRAT本体は約2.7GBでローカルに保持し、Gitにはhashと所在manifest・検査receiptを収録する。
別checkoutでは同じ証明本体の復元が必要で、Gitだけで全反駁を再生できるとは主張しない。
元のDRAT生成・gzip処理の最終receiptに依存せず、採用したLRAT自体の検査を根拠にする。

## 旧ソルバ記録と未確定事項

従来の上界1324はK0706の全1323 dのDRAT監査による。1324点の3形状監査で1323へ、今回の4形状監査で1322へ強化した。
保存1300点集合の包含極大性は[K0715](K0715-p2647-saved-1300-witness-inclusion-maximal.md)で全1347個の単点追加の阻止証明を検査した。
この包含極大性はその保存集合についての結論であり、2点を除いて3点を加えた新しい1301点集合と矛盾しない。
現在の1302点集合の最大性や空対23の最小性は未確定。1300点をphaseにした1301点以上の旧試行は、
10万衝突予算・52.79秒に続き、同じCNF・phaseの50万衝突予算・269.43秒でもUNKNOWNだった。
旧UNKNOWNは当時の予算付き観測として保持する。現在は交換と独立検査で1301点の存在を確認済み。
新しい1301点集合に対し2点以下を除く投影CNF交換を試したところ、36066除去候補・286追加候補では改善未発見だった。
固定完全対を保つ実装上の局所探索の結果であり、1302点の不存在や一般の局所最適性を証明したものではない。
現在は3点以下除去へ広げて1302点を構成済み。
その1302点から3点以下除去で1303点以上を要求した次のCNFはSOLVER_UNSATで、
当初の独立RUP-only再生は120秒でtimeoutした。その原記録は保持する。
その後、同じ保存DRATをDRAT-trim -Uで受理・LRAT化し、43074行のLRATを空節処理修正版の
別実装で6.201秒・終了コード0で受理した。36457変数・126721節の実入力のbyte再生成、
追加counterの変数予約、証拠・ソースhash、11制御例も照合した。
これにより当該CNFのUNSATを独立検査済みとする。固定完全対や除去上限を外した1303点の不存在、
一般の局所最適性、または全体の上界の改善は主張しない。
採用LRAT本体は約80MBでローカル保持し、Gitにはhashと所在を収録する。
Git管理された元DRATと変換コードから再生成でき、再現に新しいSAT探索は不要である。
除去上限を4へ広げた1303点要求は77.497秒・100005衝突でUNKNOWNだった。
37749変数・129303節の入力をbyte再生成し、変数予約・source hashと候補・モデル・証明の不在を確認した。
このUNKNOWNを不存在や局所最適性の証明へ読み替えない。
一方、現在の保存1302点集合そのものの包含極大性は[K0716](K0716-p2647-saved-1302-witness-inclusion-maximal.md)で
全1345単点追加の明示禁止四点を独立整数幾何検査して確認した。最大性や交換不能とは別である。
以前の1299点・1300点要求のUNKNOWNも原記録を保持する。
旧commit `666a778c` の「A(2647)<=1103」はp=2207の数値との混同で、その後 `48f916ca` で訂正された。
[訂正後の形状ログ](../../log/2026-11-09-p2647-no-size-h1-set-corrected.md) の1323を今回DRAT独立監査した。
一方、上界1322（サイズ1323の形状クラス判定）の旧ソルバ記録は、
[K0713](K0713-shape-cnf-auxiliary-variable-aliasing.md) の変数衝突が000/101で見つかり、そのままでは根拠として使えない。
当初その機械可読な記録は
(1,1,2) のみで、残り3クラスはログ表だけだったが、2026-11-09 に全4クラスを再実行して
receipts を再生成し、節数が旧ログ表と全件一致した
（[receipts再生成ログ](../../log/2026-11-09-a2647-size1323-receipts-regenerated.md)）。
当初のqualification-finalでは000/011/101だけが完了していたが、現在は上記の修正後全4形状監査を採用する。
旧000/101の不正入力に対するUNSATを根拠へ復帰させたものではない。
本項は有限計算の証人検査であり、Lean形式証明ではない。
小集合96例の全四点検査・合同式フィルタ・Python整数行列式の一致は回帰であり、
一般的健全性の証明と区別する。
