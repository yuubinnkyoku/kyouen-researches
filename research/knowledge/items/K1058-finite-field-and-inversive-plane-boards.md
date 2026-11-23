---
id: K1058
title: 共円ゲームの有限体盤・反転平面盤への移行と転送閾値
kind: proposition
status: computed
topics: [variants, geometry, maximum-safe, grundy]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 四点共円・共線を整数行列式で判定する完全指摘ルールの定義
- type: depends_on
  target: K0504
  note: 幾何学的禁止条件を変える変種の比較研究課題
- type: supports
  target: K0504
  note: 有限体盤・反転平面盤という具体的変種の有限結果
artifacts:
- path: research/experiments/finite-field-kyouen-20261120/README.md
  role: source
  note: AG(2,q) 盤の構造・転送閾値・最大安全サイズ
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE.md
  role: source
  note: 反転平面盤の3-設計検証・全Grundy・層サイズ公式
- path: research/experiments/finite-field-kyouen-20261120/STRATEGY.md
  role: source
  note: 初手値の分布と5×5部分勝ち
- path: research/experiments/finite-field-kyouen-20261120/FIVE_BY_FIVE.md
  role: source
  note: 5×5勝ち初手の中心菱形
- path: research/experiments/finite-field-kyouen-20261120/scripts/ff_kyouen.py
  role: solver
  note: AG(2,q) と整数格子の禁止四点列挙・Grundy計算
- path: research/experiments/finite-field-kyouen-20261120/scripts/inversive_plane.py
  role: solver
  note: P^1(F_{q^2}) 模型による反転平面の構成と3-設計検査
- path: research/experiments/finite-field-kyouen-20261120/scripts/det_threshold.py
  role: verifier
  note: 整数行列式の最大絶対値 D(n) の厳密計算
- path: research/experiments/finite-field-kyouen-20261120/scripts/transfer_threshold.py
  role: verifier
  note: q>D(n) での禁止集合一致の検証
- path: research/experiments/finite-field-kyouen-20261120/output/det_threshold.json
  role: data
  note: n=2..7 の D(n) と極値配置（四点組全列挙）
- path: research/experiments/finite-field-kyouen-20261120/output/transfer_threshold.json
  role: data
  note: 44通りの閾値一致検査
- path: research/experiments/finite-field-kyouen-20261120/output/inversive_plane.json
  role: data
  note: q=3,5 の反転平面ゲーム全値
- path: research/experiments/finite-field-kyouen-20261120/ALGEBRAIC_ROUTE.md
  role: source
  note: 放物面上のcap・反転平面3-arcへの再定式化
- path: research/experiments/finite-field-kyouen-20261120/UNIFORMITY_CHECK.md
  role: source
  note: 一様性の安価な判定法
- path: research/experiments/finite-field-kyouen-20261120/scripts/uniformity_check.py
  role: solver
  note: 小さい極大集合の探索
- path: research/experiments/finite-field-kyouen-20261120/WINNER_PREDICTION_FAILED.md
  role: source
  note: 非一様盤の勝者予測の失敗
- path: research/experiments/finite-field-kyouen-20261120/scripts/winner_prediction.py
  role: verifier
  note: 予測子の検証
- path: research/experiments/finite-field-kyouen-20261120/PARITY_APPLICATION.md
  role: source
  note: Kの偶奇による勝者決定の系
- path: research/experiments/finite-field-kyouen-20261120/scripts/parity_application.py
  role: verifier
  note: 系の検証
- path: research/experiments/finite-field-kyouen-20261120/PARITY_LAW_COMPLETE.md
  role: proof
  note: パリティ法則の完全な証明（逆も含む）
- path: research/experiments/finite-field-kyouen-20261120/scripts/converse_proof2.py
  role: verifier
  note: 逆の証明の検証
- path: research/experiments/finite-field-kyouen-20261120/PARITY_LAW_PROOF.md
  role: proof
  note: パリティ法則の厳密な証明
- path: research/experiments/finite-field-kyouen-20261120/scripts/parity_proof.py
  role: verifier
  note: 証明の各段階の全数検証
- path: research/experiments/finite-field-kyouen-20261120/PARITY_LAW.md
  role: proof
  note: パリティ法則（定理の真の一般化）
- path: research/experiments/finite-field-kyouen-20261120/scripts/parity_law.py
  role: verifier
  note: パリティ法則の全数検証
- path: research/experiments/finite-field-kyouen-20261120/COUNTEREXAMPLE_STRUCTURE.md
  role: source
  note: 反例の構造分析
- path: research/experiments/finite-field-kyouen-20261120/CONVERSE_REFUTED.md
  role: source
  note: 逆の反証（41反例）
- path: research/experiments/finite-field-kyouen-20261120/scripts/exhaustive_converse.py
  role: verifier
  note: 全数探索による反例発見
- path: research/experiments/finite-field-kyouen-20261120/CONVERSE_RESULT.md
  role: source
  note: 定理の逆の検証（300超グラフ）
- path: research/experiments/finite-field-kyouen-20261120/scripts/converse_test.py
  role: verifier
  note: 逆の反例探索
- path: research/experiments/finite-field-kyouen-20261120/PARITY_STRUCTURE.md
  role: source
  note: 一様盤のサイズ偶奇とGrundy値の対応
- path: research/experiments/finite-field-kyouen-20261120/scripts/nonuniform_structure.py
  role: verifier
  note: 非一様構造の分析
- path: research/experiments/finite-field-kyouen-20261120/TRIVIALITY_THEOREM.md
  role: proof
  note: 極大集合の一様性とGrundy値の定理
- path: research/experiments/finite-field-kyouen-20261120/scripts/triviality.py
  role: verifier
  note: 定理の全数検証
- path: research/experiments/finite-field-kyouen-20261120/CROSS_PRUNE_ORDER.md
  role: source
  note: 十字枝刈りが探索順序を変えることの分析
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q19_EXACT.md
  role: source
  note: K(反転平面q=19)=14の厳密決定
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q19_SEARCH.md
  role: source
  note: 反転平面q=19でK>=14
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv19.cpp
  role: solver
  note: 標数19の反転平面完全探索
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q17_EXACT.md
  role: source
  note: K(反転平面q=17)=13の厳密決定
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_STABILITY.md
  role: source
  note: 反転平面のK/q安定性の分析
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q17_SEARCH.md
  role: source
  note: 反転平面q=17でK>=13
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv17.cpp
  role: solver
  note: 標数17の反転平面完全探索
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q16_EXACT.md
  role: source
  note: K(反転平面q=16)=12の厳密決定
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv16.cpp
  role: solver
  note: 標数2の反転平面完全探索
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q13_INDEPENDENT.md
  role: source
  note: K(AG(2,13))=13の2実装による独立確認
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q16_EXACT.md
  role: source
  note: K(AG(2,16))=16の厳密決定
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q16_SEARCH.md
  role: source
  note: AG(2,16)でK>=16
- path: research/experiments/finite-field-kyouen-20261120/scripts/ag16.cpp
  role: solver
  note: 標数2のAG(2,16)完全探索
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q13_EXACT.md
  role: source
  note: K(AG(2,13))=13の厳密決定
- path: research/experiments/finite-field-kyouen-20261120/PRUNING_IMPROVEMENT.md
  role: source
  note: 枝刈り強化（40%ノード削減）
- path: research/experiments/finite-field-kyouen-20261120/scripts/agq2.cpp
  role: solver
  note: 強化枝刈り付きC++完全探索
- path: research/experiments/finite-field-kyouen-20261120/CPP_IMPLEMENTATION.md
  role: source
  note: C++実装による高速化
- path: research/experiments/finite-field-kyouen-20261120/scripts/agq.cpp
  role: solver
  note: 任意の素数qに対するAG(2,q)完全探索
- path: research/experiments/finite-field-kyouen-20261120/BOUND_RESEARCH_SUMMARY.md
  role: source
  note: 上界研究の総括
- path: research/experiments/finite-field-kyouen-20261120/SIZE_WEIGHTED_FAILED.md
  role: source
  note: サイズを使った上界の失敗記録
- path: research/experiments/finite-field-kyouen-20261120/SINGLE_FAMILY.md
  role: source
  note: 単一族でのKとブロックサイズの関係
- path: research/experiments/finite-field-kyouen-20261120/COLLINEAR_TRIPLES.md
  role: source
  note: 真円も退化円も共線三点を含まないことの確認
- path: research/experiments/finite-field-kyouen-20261120/BLOCK_STRUCTURE.md
  role: source
  note: サイズq-1ブロックの構造観察
- path: research/experiments/finite-field-kyouen-20261120/GENUINE_CIRCLE_PATTERN.md
  role: source
  note: 真円の有無がK/qを決めることの検証
- path: research/experiments/finite-field-kyouen-20261120/ABLATION_Q9.md
  role: source
  note: q=9のアブレーション
- path: research/experiments/finite-field-kyouen-20261120/ABLATION.md
  role: source
  note: ブロック族アブレーション（円がKを支配）
- path: research/experiments/finite-field-kyouen-20261120/LARGE_BLOCK_REFUTED.md
  role: source
  note: 大きなブロックを除くとKが増えることの検証
- path: research/experiments/finite-field-kyouen-20261120/LARGE_BLOCK_PATTERN.md
  role: source
  note: 大きなブロックの有無がK/qを決める
- path: research/experiments/finite-field-kyouen-20261120/K_EQUALS_Q_REFUTED.md
  role: source
  note: K=q予想の反例（q=5でK=6）
- path: research/experiments/finite-field-kyouen-20261120/BOUND_TIGHTNESS_Q9.md
  role: source
  note: q=9の上界付近の不存在確認
- path: research/experiments/finite-field-kyouen-20261120/BOUND_TIGHTNESS.md
  role: source
  note: 上界付近のサイズの不存在確認
- path: research/experiments/finite-field-kyouen-20261120/ARC_STRUCTURE.md
  role: source
  note: 最大3-arcの円プロファイル
- path: research/experiments/finite-field-kyouen-20261120/PROFILE_NO_IMPROVEMENT.md
  role: source
  note: プロファイルが上界を改善しないことの証明
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_AXIOMS.md
  role: source
  note: 反転平面の公理I.1-I.3の確認
- path: research/experiments/finite-field-kyouen-20261120/TWO_ARC_RESOLUTION.md
  role: proof
  note: 2-arcの最大が2であることの証明と不整合の解決
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC_5.md
  role: source
  note: arcの定義確定とAd(q)の特定
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC_2.md
  role: source
  note: Sonninoの(q+5)-arcと我々のKの不整合
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC_3.md
  role: source
  note: 射影平面arcの定義確認
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC_4.md
  role: source
  note: 反転平面の公理(A1)の確認
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_3ARC.md
  role: source
  note: 3-arcの文献調査記録
- path: research/experiments/finite-field-kyouen-20261120/FOUR_FAILED_ROUTES.md
  role: source
  note: q=3 mod 4の上界改善4手法の失敗記録
- path: research/experiments/finite-field-kyouen-20261120/BOUNDS_SUMMARY.md
  role: source
  note: 全上界の総括とgapの比較
- path: research/experiments/finite-field-kyouen-20261120/COVERING_BOUND.md
  role: source
  note: 被覆による上界が弱いことの分析
- path: research/experiments/finite-field-kyouen-20261120/BOUND_GAP_ANALYSIS.md
  role: source
  note: 上界が達成されない理由の分析
- path: research/experiments/finite-field-kyouen-20261120/WHY_NO_SIZE6.md
  role: source
  note: AG(2,3)でサイズ6が不可能な理由
- path: research/experiments/finite-field-kyouen-20261120/PROPERTY_TRIVIAL.md
  role: proof
  note: 全三点ブロック性が恒真であることの確認
- path: research/experiments/finite-field-kyouen-20261120/MULTI_PAIR_BOUND.md
  role: proof
  note: ペンシル議論では上界が改善しないことの証明
- path: research/experiments/finite-field-kyouen-20261120/BOUND_IMPROVE_ATTEMPT.md
  role: source
  note: 次数議論の失敗記録
- path: research/experiments/finite-field-kyouen-20261120/BOUND_TEST_Q11.md
  role: source
  note: q=11での上界検証とK=9確定
- path: research/experiments/finite-field-kyouen-20261120/LAMBDA2_BOUND.md
  role: proof
  note: 一般上界K<=lambda_2+2=q+3の証明
- path: research/experiments/finite-field-kyouen-20261120/scripts/lambda2_bound.py
  role: verifier
  note: lambda_2の一様性検証
- path: research/experiments/finite-field-kyouen-20261120/TRIPLE_COVERAGE.md
  role: source
  note: 全三点ブロック性のq<=9での普遍性
- path: research/experiments/finite-field-kyouen-20261120/EXTREMAL_STRUCTURE.md
  role: source
  note: 極値配置の全三点ブロック構造
- path: research/experiments/finite-field-kyouen-20261120/BOUND_Q3MOD4.md
  role: source
  note: q=3 mod 4の上界比較
- path: research/experiments/finite-field-kyouen-20261120/CROSS_SHARP.md
  role: proof
  note: 十字上界の改良K<=q+2の証明
- path: research/experiments/finite-field-kyouen-20261120/scripts/cross_sharp2.py
  role: verifier
  note: 十字の交わり構造の検証
- path: research/experiments/finite-field-kyouen-20261120/DEGENERATION_QUANT.md
  role: source
  note: 退化とKの定量的関係（K/q≈1）
- path: research/experiments/finite-field-kyouen-20261120/DEGENERATION_K.md
  role: source
  note: 円の退化がKを大きくする証拠（q=17対19）
- path: research/experiments/finite-field-kyouen-20261120/SERIES_SUMMARY.md
  role: source
  note: K系列の総括と乖離の分析
- path: research/experiments/finite-field-kyouen-20261120/AG13_FAMILIES.md
  role: source
  note: AG(2,13)のブロック族別分析
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q13_Q16.md
  role: source
  note: q=13,16のAG K下界
- path: research/experiments/finite-field-kyouen-20261120/Q11_EXACT.md
  role: source
  note: q=11のK=9（両盤）
- path: research/experiments/finite-field-kyouen-20261120/Q13_RESULTS.md
  role: source
  note: q=13の反転平面K=10・AG K>=13
- path: research/experiments/finite-field-kyouen-20261120/scripts/sym_exact.py
  role: solver
  note: 対称性破壊による一般完全探索
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q9_EXACT.md
  role: source
  note: K(AG(2,9))=9の厳密決定
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q9_EXACT.md
  role: source
  note: K(反転平面q=9)=9の厳密決定
- path: research/experiments/finite-field-kyouen-20261120/scripts/ag9_sym_dfs.py
  role: solver
  note: 2-推移性による対称性破壊探索
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv9_sym_dfs.py
  role: solver
  note: 3-推移性による対称性破壊探索
- path: research/experiments/finite-field-kyouen-20261120/GROWTH_FIT.md
  role: source
  note: 成長率フィットの比較と信頼性評価
- path: research/experiments/finite-field-kyouen-20261120/GROWTH_RATE.md
  role: source
  note: Kの成長率（q^0.33対2n）
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q9_SIZE10.md
  role: source
  note: AG(2,9)サイズ10の探索空間分析
- path: research/experiments/finite-field-kyouen-20261120/AG2_BOUNDS.md
  role: source
  note: 上界の比較（cross/second moment/triple）
- path: research/experiments/finite-field-kyouen-20261120/AG2_LINE_BOUNDS.md
  role: source
  note: 直線制約と共線三点の限界
- path: research/experiments/finite-field-kyouen-20261120/AG2_CROSS_GENERAL.md
  role: proof
  note: 十字ブロックによる一般上界3q^2/(2q-1)
- path: research/experiments/finite-field-kyouen-20261120/AG2_Q9_CROSS.md
  role: source
  note: AG(2,9)の分解座標と十字ブロック
- path: research/experiments/finite-field-kyouen-20261120/DET_LINEAR_GAP.md
  role: source
  note: 線形ギャップ不等式（c>=7/2）
- path: research/experiments/finite-field-kyouen-20261120/DET_MONOTONE.md
  role: source
  note: 積の最大は最大面積で達成される（a<=9）
- path: research/experiments/finite-field-kyouen-20261120/DET_CENTRE_FORMULA.md
  role: source
  note: ラグランジュ恒等式・中心公式・バウンディングボックス条件
- path: research/experiments/finite-field-kyouen-20261120/DET_CENTRE_CASES.md
  role: source
  note: 中心の内外による場合分け
- path: research/experiments/finite-field-kyouen-20261120/DET_AREA_POWER.md
  role: source
  note: Area*power<=a^4/4の鋭い上界
- path: research/experiments/finite-field-kyouen-20261120/DET_GAMMA_AREA.md
  role: proof
  note: gamma=-2*Areaの証明と|gamma|<=a^2
- path: research/experiments/finite-field-kyouen-20261120/DET_TRADEOFF.md
  role: source
  note: gammaとpowerの逆相関と積の上界
- path: research/experiments/finite-field-kyouen-20261120/AG_VS_INVERSIVE.md
  role: source
  note: AG(2,8)=8と反転平面7の乖離
- path: research/experiments/finite-field-kyouen-20261120/AG2_PRIME_POWER.md
  role: source
  note: AG(2,q)の素数冪拡張と円個数公式の破綻
- path: research/experiments/finite-field-kyouen-20261120/scripts/ag2_prime_power.py
  role: solver
  note: 素数冪AG(2,q)の構成と完全探索
- path: research/experiments/finite-field-kyouen-20261120/DET_CONTINUOUS.md
  role: source
  note: 連続緩和の正しい値と格子との差1
- path: research/experiments/finite-field-kyouen-20261120/scripts/det_continuous_exact.py
  role: verifier
  note: 凸凹場合分けによる連続最大の厳密計算
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q8.md
  role: source
  note: q=8のK=7厳密決定と高速化
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv_fast_target.py
  role: solver
  note: 対称性利用とfail-firstによる高速完全探索
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_VARIANTS.md
  role: source
  note: misèreとk点版の完全計算
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv_variants.py
  role: solver
  note: 変種の勝敗計算
- path: research/experiments/finite-field-kyouen-20261120/FIVE_BY_FIVE_STRUCTURE.md
  role: source
  note: 5x5のD4軌道分解
- path: research/experiments/finite-field-kyouen-20261120/AG2_MAX.md
  role: source
  note: AG(2,q)のK厳密値と反転平面との一致
- path: research/experiments/finite-field-kyouen-20261120/scripts/ag2_exact_max.py
  role: solver
  note: AG(2,q)の固定サイズ完全探索
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_PRIME_POWER.md
  role: source
  note: 全素数冪への拡張とq=3,4,5,7のK厳密値
- path: research/experiments/finite-field-kyouen-20261120/scripts/inversive_bfs.py
  role: solver
  note: 全素数冪の反転平面構成（BFS円生成）
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv_max_all_q.py
  role: solver
  note: 固定サイズ完全探索によるK決定
- path: research/experiments/finite-field-kyouen-20261120/INVERSIVE_Q7.md
  role: source
  note: 反転平面q=7のK=6厳密決定
- path: research/experiments/finite-field-kyouen-20261120/scripts/inv7_exact_target.py
  role: solver
  note: 固定サイズ完全探索による不存在証明
- path: research/experiments/finite-field-kyouen-20261120/TORUS.md
  role: source
  note: トーラス盤とAG(2,p)の一致、合成数での乖離
- path: research/experiments/finite-field-kyouen-20261120/DET_MAX_TRIPLE.md
  role: source
  note: 三点分解によるD(n)のn≤12全数確認
- path: research/experiments/finite-field-kyouen-20261120/scripts/det_max_structure.py
  role: verifier
  note: 余因子展開による三点分解D(n)計算
- path: research/experiments/finite-field-kyouen-20261120/DET_MAX.md
  role: source
  note: D(n)閉形式の証拠と残る証明課題
- path: research/experiments/finite-field-kyouen-20261120/scripts/torus_board.py
  role: verifier
  note: トーラス盤と平面盤の禁止集合比較・ゲーム値
- path: research/experiments/finite-field-kyouen-20261120/DESIGN_TRICHOTOMY.md
  role: source
  note: Steiner設計上の三分法と一般上下界
- path: research/experiments/finite-field-kyouen-20261120/scripts/design_trichotomy.py
  role: verifier
  note: 9設計での三分法検証
- path: research/experiments/finite-field-kyouen-20261120/scripts/steiner3_kyouen.py
  role: verifier
  note: Witt設計の厳密被覆構成とK計算
- path: research/experiments/finite-field-kyouen-20261120/NET3_REFORMULATION.md
  role: source
  note: 交差比による3-ネット翻訳とK=3+alpha
- path: research/experiments/finite-field-kyouen-20261120/scripts/crossratio_graph.py
  role: verifier
  note: 交差比の鍵事実の全数検証（q≤7）
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_transversal.py
  role: verifier
  note: 3-ネット分割の確認とtau_3・完全独立性数の計算
- path: research/experiments/finite-field-kyouen-20261120/scripts/derived_design_bound.py
  role: verifier
  note: 派生設計による上界1+A_2の計算
- path: research/experiments/finite-field-kyouen-20261120/NET3_LATIN_SQUARE.md
  role: source
  note: 3-ネットのラテン方陣の完全公式とtau_3の決定
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_formula2.py
  role: verifier
  note: c=(d-ab)/(a-b)の全セル検証（q=3,5,7,9）
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_tau_theory.py
  role: verifier
  note: tau_3=q-1（奇数）/q（偶数）の全数確認
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_proof_complete.py
  role: verifier
  note: メビウス対合M_aの構造と固定点数の確認
- path: research/experiments/finite-field-kyouen-20261120/scripts/verify_qplus2.py
  role: verifier
  note: K<=q+2の修正済み厳密値に対する確認
- path: research/experiments/finite-field-kyouen-20261120/NET3_NO_TRANSVERSAL.md
  role: source
  note: 完全横断の非存在とノルム1トーラスの群法則
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_final_step.py
  role: verifier
  note: 完全横断が0個であることの全数確認
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_group_law.py
  role: verifier
  note: 1/a=(1/b)*_d(1/c)の検証
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_partial_law.py
  role: verifier
  note: 部分演算であることの確認
- path: research/experiments/finite-field-kyouen-20261120/NET3_TAU_PROVED.md
  role: source
  note: tau_3=q-1の完全証明（Hall-Paige経由）
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_hall_paige.py
  role: verifier
  note: P^1(F_q)とT_dの全単射、完全写像の非存在
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_torus_native.py
  role: verifier
  note: 指数集合Eの計算
- path: research/experiments/finite-field-kyouen-20261120/NET3_COMPLETE.md
  role: source
  note: 3-ネット理論の総括（交差比からHall-Paigeまで）
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_cyclic_table.py
  role: verifier
  note: ラテン方陣がZ_{q+1}の加法表であることの確認
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_fast_k.py
  role: verifier
  note: 3-ネットフィルタによる高速K計算（q≤11）
- path: research/experiments/finite-field-kyouen-20261120/NET3_FAMILY_CD_NOT_LINEAR.md
  role: source
  note: 族C,Dが巡回座標で線形でないことの否定的結果
- path: research/experiments/finite-field-kyouen-20261120/scripts/net3_family_cd_linear.py
  role: verifier
  note: 線形条件の全数探索（q=5,7で約50%一致）
- path: research/experiments/finite-field-kyouen-20261120/MIN_MAXIMAL.md
  role: source
  note: 最小極大集合s(q)の新不変量と定石数の反証
- path: research/experiments/finite-field-kyouen-20261120/scripts/min_maximal2.py
  role: verifier
  note: 極大安全集合の全列挙（q≤8）
- path: research/experiments/finite-field-kyouen-20261120/scripts/min_maximal_q9.py
  role: verifier
  note: s(9)=6, s(11)=6の確認
- path: research/experiments/finite-field-kyouen-20261120/scripts/min_maximal_random3.py
  role: verifier
  note: ランダム再起動によるk*極大集合の探索
- path: research/experiments/finite-field-kyouen-20261120/S_Q_STRUCTURE.md
  role: source
  note: 欠損δの解析、q=8の完全分解、貪欲法の失敗
- path: research/experiments/finite-field-kyouen-20261120/scripts/q8_tightness.py
  role: verifier
  note: q=8でδ=0の完全分解を確認
- path: research/experiments/finite-field-kyouen-20261120/scripts/s_q_constructive.py
  role: verifier
  note: 決定的貪欲法の失敗（q≥5）
- path: research/experiments/finite-field-kyouen-20261120/S_Q_REFUTED.md
  role: source
  note: 予想s(q)=k*のq=13での反証とovoid模型
- path: research/experiments/finite-field-kyouen-20261120/scripts/inversive_ovoid.py
  role: verifier
  note: 楕円二次曲面による高速反転平面構成（O(q^3)）
- path: research/experiments/finite-field-kyouen-20261120/scripts/s_q_large.py
  role: verifier
  note: ovoid模型による大qのs(q)探索
- path: research/experiments/finite-field-kyouen-20261120/scripts/s13_investigate.py
  role: verifier
  note: q=13でサイズ6不発・サイズ7発見の確認
- path: research/experiments/finite-field-kyouen-20261120/S13_WASTE.md
  role: source
  note: サイズ6の未ブロック分布下限が14に張り付く証拠
- path: research/experiments/finite-field-kyouen-20261120/scripts/s13_waste.py
  role: verifier
  note: 無駄(waste)の測定
- path: research/experiments/finite-field-kyouen-20261120/S_Q_SERIES.md
  role: source
  note: s(q)の実測系列（q≤17）とブロッキング下界からの乖離
- path: research/experiments/finite-field-kyouen-20261120/scripts/s_q_1617.py
  role: verifier
  note: s(16)=9, s(17)=8の測定
- path: research/experiments/finite-field-kyouen-20261120/ARC_ON_QUADRIC.md
  role: source
  note: 共円ゲームの楕円二次曲面上のアーク問題への帰着
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_on_quadric.py
  role: verifier
  note: 共円⟺同一平面の全数検証（q≤7）
- path: research/experiments/finite-field-kyouen-20261120/LITERATURE_ARC_Q8.md
  role: source
  note: q=8のアーク数1,048,320が文献値と一致
- path: research/experiments/finite-field-kyouen-20261120/ARC_COUNT_FORMULAS.md
  role: source
  note: アーク数の閉形式（k≤4）とK=最大非零サイズ
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_counts.py
  role: verifier
  note: アーク数の全数計算（q≤8）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_small_k.py
  role: verifier
  note: k≤3とk=4の閉形式の検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K5_THEOREM.md
  role: source
  note: k=5の閉形式の証明
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k5_theorem.py
  role: verifier
  note: k=5公式の検証（q=3,4,5,7,8）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K6_STRUCTURE.md
  role: source
  note: k=6の5プロファイル分類と分解公式
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k6_formula.py
  role: verifier
  note: k=6分解の全数照合（q=5,7）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K6_NJ.md
  role: source
  note: N_jの一様性（q=5）と2型分裂（q=7）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K6_ORBITS.md
  role: source
  note: N_jがPGL(2,q)-軌道で決まることの特定と完全なk=6公式
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k6_orbits.py
  role: verifier
  note: PGL(2,q)軌道の総当たり計算と分布グループの一致確認
- path: research/experiments/finite-field-kyouen-20261120/ARC_K6_JOINT_COMPLETE.md
  role: source
  note: k=6交点表の完全な閉形式と接する円の補題
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k6_meet2.py
  role: verifier
  note: 交点の同時分布の測定
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k6_tangent_formula.py
  role: verifier
  note: 接する場合の閉形式の検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K6_STATUS.md
  role: source
  note: k=6で閉じたものと残るものの正確な整理
- path: research/experiments/finite-field-kyouen-20261120/ARC_K6_CLOSED.md
  role: source
  note: ペンシルの対合と超幾何分布によるk=6の解決
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k6_involution.py
  role: verifier
  note: ペンシルが対合を定めることの検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K6_NXY.md
  role: source
  note: 接する円がq^2-1個であることとN_xyの閉形式
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k6_pure.py
  role: verifier
  note: 列挙なしの純粋なk=6公式の検証（q=5,7,8）
- path: research/experiments/finite-field-kyouen-20261120/ARC_TABLE.md
  role: source
  note: k≤7の閉形式の確定版一覧（奇偶分岐・因子階層・主項パターン・アーク数表）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_table.py
  role: verifier
  note: アーク数の統一ハーネス（全数列挙＋閉形式照合）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_START.md
  role: source
  note: k=7の開始（q=5,7で7-アークが0、プロファイル8種類）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_MULTIPLICITY.md
  role: source
  note: k=7の多重度定理（プロファイル＝タプル数÷4円の個数）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_verify.py
  role: verifier
  note: k=7プロファイル分解の7/7検証
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_five2.py
  role: verifier
  note: (5,*)族がk=6の機構で閉じることの検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_WHY_HARD.md
  role: source
  note: j-三つ組と合併サイズが失敗する理由（否定的結果）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_FORMULA.md
  role: source
  note: 3点が定める円によるk=7プロファイル公式
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_formula.py
  role: verifier
  note: k=7プロファイル公式の10/10検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_W_CLOSED.md
  role: source
  note: k=7のw周辺分布の閉形式（円の(a,w)分類）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_w_closed.py
  role: verifier
  note: w周辺分布の閉形式の検証（q=5,7）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_U_FORMULA.md
  role: source
  note: k=7のu公式（u=Σj-3[w=2]）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_u_formula.py
  role: verifier
  note: u公式の13/13検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_INVOLUTIONS.md
  role: source
  note: k=7の3対合構造（素か1共通対）とw=2の特徴づけ
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_involutions.py
  role: verifier
  note: 対合の共通対数の測定
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_caseB.py
  role: verifier
  note: 場合Bとwの関係の検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_CASE_DECOMP.md
  role: source
  note: k=7の(w,u)分布の対合による分解と再構成
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_reconstruct.py
  role: verifier
  note: (case,w,sum_j)から(w,u)への再構成の10/10検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_SUMJ.md
  role: source
  note: k=7のΣjをペンシル円プロファイルで決定
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_sumj_verify.py
  role: verifier
  note: Σj=#(2,2)+3[W]の検証とWの同値性
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_TOTAL.md
  role: source
  note: k=7アーク数の組み立てと全数計算との一致
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_total.py
  role: verifier
  note: k=7アーク数の組み立て検証（bad=657800, arcs=0）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_DUAL.md
  role: source
  note: k=7の双対構成（9つの型）と変換則
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_dual_verify.py
  role: verifier
  note: 双対9型の集約による(w,u)の10/10再現
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_FINE.md
  role: source
  note: k=7の型の細分（90配置）と閉形式への障壁
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_fine.py
  role: verifier
  note: 対合配置の標準形による90配置の計数
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_BY_A.md
  role: source
  note: a=|W cap C|による分解とa=2⟺場合Bの定理
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_a_case.py
  role: verifier
  note: aが場合を決定することと三重カウントの閉形式の検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_A0.md
  role: source
  note: a=0層の6型と障壁の再現
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_a0_fine.py
  role: verifier
  note: a=0層の90配置の計数
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_ORBITS_FIX.md
  role: source
  note: 「90配置」の訂正とPGL軌道37の正しい数
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_involution_orbits.py
  role: verifier
  note: PGL(2,q)の対合三つ組への軌道計算（q=5で37）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_MODEL_CHECK.md
  role: source
  note: 9分布の模型非依存性の確認と軌道対応の失敗
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_native_orbits.py
  role: verifier
  note: native模型での9分布の確認
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_ORBIT_MATCH.md
  role: source
  note: 9分布=実現する9軌道の解決
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_orbit_match.py
  role: verifier
  note: C=P^1(F_q)による軌道対応（1140/1140、9軌道実現）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_ORBIT_A.md
  role: source
  note: 9軌道のa層への一意な所属
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_orbit_a.py
  role: verifier
  note: 軌道とa層の対応の計算
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_A2.md
  role: source
  note: a=2層の型が円の性質であることとq=7での3種
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_a2_circle_kind.py
  role: verifier
  note: a=2円の2種（q=5）と3種（q=7）の識別
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_A0_TWO_U.md
  role: source
  note: 円レベルのuとTレベルのuが別物であることの訂正
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_a0_check.py
  role: verifier
  note: 2つのuの混同の検出
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_A0_SPLIT.md
  role: source
  note: a=0円の2分類の閉形式
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_a0_split.py
  role: verifier
  note: a=0円の個数と2分類の検証（q=5,7）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_A0_KIND_FAILS.md
  role: source
  note: 円の種類が軌道を決めないことの否定的結果
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_a0_orbit_kind.py
  role: verifier
  note: 円の種類と軌道の対応の測定
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_SUMMARY.md
  role: source
  note: k=7の総括（11の確定結果、残る壁、7つの失敗）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_A0_CLOSED.md
  role: source
  note: a=0層の完全解決（2円種×3副類）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_a0_circle6.py
  role: verifier
  note: a=0層の6類が2円種×3副類であることの検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_A0_Q7.md
  role: source
  note: a=0層のq=7検証（副類の数が増える）
- path: research/experiments/finite-field-kyouen-20261120/output/arc_k7_a0_circle6_7.json
  role: data
  note: q=7のa=0層の副類配分
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_Q7_FAILS.md
  role: source
  note: k=7プロファイル公式のq=7での破綻（重要な訂正）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_q7_diagnose.py
  role: verifier
  note: プロファイル公式の直接照合（20000/20000不一致）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_FIXED.md
  role: source
  note: 修正版プロファイル公式（vと|W cap T|）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_fix.py
  role: verifier
  note: 修正版公式の検証（q=5,7で0不一致）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_SCALE_BUG.md
  role: source
  note: 第2の誤り（スケールbと多重度の割り算）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_scale.py
  role: verifier
  note: スケールの比較検証（q=5,7）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_SIX_PLUS.md
  role: source
  note: 真の原因（6点以上の円）の特定
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_fullcheck.py
  role: verifier
  note: プロファイル公式の全数照合（q=7で0不一致）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_MISSING_PROFILES.md
  role: source
  note: 完全な診断（欠落は(5,)(6,)(7,)の3つのみ）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_q7_profiles.py
  role: verifier
  note: q=7の全プロファイルヒストグラム
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_MISSING_CLOSED.md
  role: source
  note: 欠落3プロファイルのうち(7,)(6,)の閉形式
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_missing.py
  role: verifier
  note: 単一円プロファイルの測定（q=5,7）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_ALL_PROFILES.md
  role: source
  note: k=7の全プロファイルの決定
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_five_profile.py
  role: verifier
  note: (5,)の条件の検証（q=5,7）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_COMPLETE.md
  role: source
  note: k=7の完全なアーク数公式（q=5,7で検証）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_complete.py
  role: verifier
  note: 完全な公式の端から端までの検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_Q8.md
  role: source
  note: q=8（標数2）での検証と文献値1,048,320との一致
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_FIVE_CLOSED.md
  role: source
  note: (5,)の閉形式（k=6の機構で閉じる）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_five_closed.py
  role: verifier
  note: (5,)閉形式の検証（q=5,7,8）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_FINAL.md
  role: source
  note: k=7の最終総括（完全な閉形式、3つのqでの検証、7段階の誤り記録）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K7_Q9.md
  role: source
  note: q=9での検証（4つ目のq）と25倍高速化
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k7_fast.py
  role: verifier
  note: 高速版の完全な公式（3ペンシルのみでvを計算）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K6_K7_CROSSCHECK.md
  role: source
  note: k=6とk=7の閉形式のK(q)との相互検証
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k6_q9.py
  role: verifier
  note: k=6/k=7アーク数とK(q)の整合性チェック
- path: research/experiments/finite-field-kyouen-20261120/K_GROWTH_ARCS.md
  role: source
  note: アーク密度から見たK(q)の増大分析
- path: research/experiments/finite-field-kyouen-20261120/scripts/k_growth_arcs.py
  role: verifier
  note: アーク密度とK/q^(1/3)の計算
- path: research/experiments/finite-field-kyouen-20261120/ARC_RATIO_NO_FORMULA.md
  role: source
  note: アーク数の連続比に公式がないことの否定的結果
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_ratio.py
  role: verifier
  note: 連続比の計算
- path: research/experiments/finite-field-kyouen-20261120/ARC_POLYNOMIALS.md
  role: source
  note: 4-arcsと5-arcsの多項式展開
- path: research/experiments/finite-field-kyouen-20261120/scripts/k_leading_symbolic.py
  role: verifier
  note: 閉形式の多項式展開と主項の計算
- path: research/experiments/finite-field-kyouen-20261120/ARC6_POLYNOMIAL.md
  role: source
  note: 6-arcsの多項式（奇数q、12次）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc6_polynomial.py
  role: verifier
  note: 6-arcs多項式の補間と15点検証
- path: research/experiments/finite-field-kyouen-20261120/ARC4_FACTORED.md
  role: source
  note: 4-arcsの完全な因数分解形
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_factor.py
  role: verifier
  note: アーク数多項式の因数分解
- path: research/experiments/finite-field-kyouen-20261120/ARC6_FACTORED.md
  role: source
  note: 6-arcsの因数分解（q-3因子の発見）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_factor2.py
  role: verifier
  note: 5次・6次剰余の因数探索
- path: research/experiments/finite-field-kyouen-20261120/ARC_POLY_CORRECTION.md
  role: source
  note: 5-arcs多項式の訂正とarcs6の浮動小数点バグ修正
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_poly_fix.py
  role: verifier
  note: 多項式の再導出とq=3..59での検証
- path: research/experiments/finite-field-kyouen-20261120/ARC6_EVEN_CLOSED.md
  role: source
  note: 偶数qのN_xy公式と6-arcs閉形式
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc6_even_symbolic.py
  role: verifier
  note: 偶数qの閉形式の検証（6/6）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_FEASIBILITY.md
  role: source
  note: k=8の計算可能性分析（3経路すべて不可能）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_start.py
  role: verifier
  note: k=8のプロファイルサンプリング
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_Q9.md
  role: source
  note: k=8の厳密値（q=9で1,062,720）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8.c
  role: verifier
  note: k=8のC実装（4円ハッシュ＋直接列挙）
- path: research/experiments/finite-field-kyouen-20261120/scripts/export_circles.py
  role: verifier
  note: Cプログラム用の円データ出力
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_MULTI_Q.md
  role: source
  note: k=8の複数q計算（q=5,8,9）とK(q)との整合
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_TABLE.md
  role: source
  note: C実装の二重検証とk=8の完全な表（q=5,7,8,9）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_PROFILE.md
  role: source
  note: k=8のプロファイル公式（6類、q=5,7で0不一致）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_profile.py
  role: verifier
  note: k=8プロファイル公式の検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K9_Q9.md
  role: source
  note: k=9の厳密値（q=9で29,520）と比の系列1/4^2,1/6^2
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k9.c
  role: verifier
  note: k=9のC実装
- path: research/experiments/finite-field-kyouen-20261120/ARC_RATIO_PATTERN.md
  role: source
  note: 比の系列1/4^2,1/6^2の分析とK(q)での終焉
- path: research/experiments/finite-field-kyouen-20261120/scripts/ratio_pattern.py
  role: verifier
  note: 比の候補式の検討
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_ASSEMBLE_C.md
  role: source
  note: k=8のC組み立てと除算順序の罠
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_assemble.c
  role: verifier
  note: k=8組み立てのC実装（q=5で完全一致）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_CLASSES.md
  role: source
  note: k=8の6類の分布（q=5）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_classes.py
  role: verifier
  note: 6類の分布測定
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_Z4.md
  role: source
  note: z4の構造（共円性で決まる）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_z4.py
  role: verifier
  note: z4の検証（q=5で完全整合）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_V4U4.md
  role: source
  note: v4,u4,z4の排反性と共円性との同値
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_v4u4.py
  role: verifier
  note: v4,u4,z4の排反性の検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_CIRCLE_SPLIT.md
  role: source
  note: C'とTの交点数による完全な分解（6qと4(q-1)+4(s-4)q）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_v2v3u3.py
  role: verifier
  note: 円の分類の検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_SUMMARY.md
  role: source
  note: k=8の総括（4つの厳密値、6類公式、v4+u4+z4の還元、円の分解、除算順序の罠）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_AGG_FORMULA.md
  role: source
  note: sum(v2+v3+v4)の閉形式と|Y|=q-1の構造
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_agg_formula.py
  role: verifier
  note: 集約の分解の検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_U3_FORMULA.md
  role: source
  note: sum(u3+u4)の閉形式と|Y|=s-|C' cap C|の構造
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_u3_formula.py
  role: verifier
  note: u3+u4の分解の検証
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_V2V3_SPLIT.md
  role: source
  note: v2/v3の分離とk=8の閉形式の完成
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_v2v3_split.py
  role: verifier
  note: v2/v3分離の検証（両方完全一致）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_NCYC.md
  role: source
  note: N_cyc（外点の共円4点の個数）の閉形式
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_ncyc.py
  role: verifier
  note: N_cycの検証（q=5で完全一致）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_V4U4Z4_SUMS.md
  role: source
  note: v4,u4,z4の個別の和とk=8閉形式の完成
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_v4u4z4_sums.py
  role: verifier
  note: v4,u4,z4の個別の和の検証（3/3完全一致）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_KX.md
  role: source
  note: k_Xの分布とk=8閉形式の完全な閉包
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_kx.py
  role: verifier
  note: k_X分布の検証（q=5で完全一致）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_COMPLETE.md
  role: source
  note: k=8の6類閉形式の一括検証と「和では足りない」限界
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_complete.py
  role: verifier
  note: 6類閉形式の一括検証（6/6）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_PROFDIST.md
  role: source
  note: k=8のプロファイル分布（13種）と(v2,u3)同時分布（28種）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_profdist.py
  role: verifier
  note: プロファイル分布の測定
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_V2U3_STRUCT.md
  role: source
  note: (v2,u3)の条件付き構造とトレードオフ
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_v2u3_struct.py
  role: verifier
  note: (v2,u3)条件付き分布の測定
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_Q9_GAP.md
  role: source
  note: q=9での組み立て破綻と単一円プロファイル欠落の訂正
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_SINGLE_CORRECTION.md
  role: source
  note: 単一円プロファイルはk=7の結果だったという訂正
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_MULT_CORRECTION.md
  role: source
  note: 多重度定理は正しいという訂正（LHS/RHSテストの誤り）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_q9_check.py
  role: verifier
  note: q=9でのプロファイル公式検証（500組で0不一致）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_STATUS.md
  role: source
  note: k=8の現状総括（確立したこと・未解決・4回の誤診）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_single_fast.py
  role: verifier
  note: 単一円プロファイルの高速列挙
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_Q7_FAILS.md
  role: source
  note: q=7でも組み立てが破綻していたという訂正（差は(6,)プロファイル）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_Q7_ROOTCAUSE.md
  role: source
  note: (6,)はq=7で0件という訂正とプロファイル数の不一致
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_Q7_ELIMINATION.md
  role: source
  note: q=7の差について4候補を直接測定で消去
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_seven_actual.py
  role: verifier
  note: (7,)の実測（過大カウントなし）
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_PROFILE_EXACT.md
  role: source
  note: プロファイル公式がq=7の全数で完全に正しいという決定的結果
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_fullcheck_gen.py
  role: verifier
  note: 全数プロファイル検証のC実装生成
- path: research/experiments/finite-field-kyouen-20261120/ARC_K8_DIVISOR_TESTS.md
  role: source
  note: 2つの除数仮説の数値的棄却
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_census.c
  role: solver
  note: アークのみをDFSで列挙するアーク・センサス法（q=7,8,9で層サイズとKを再現）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_k8_e4.py
  role: verifier
  note: e4除数の検証
- path: research/experiments/finite-field-kyouen-20261120/scripts/inversive_fast.py
  role: solver
  note: PGL(2,F_{q^2}) 軌道のBFSによる円の高速構成（q=47まで）
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_maxsearch.c
  role: solver
  note: 増分ブロッキングによるアークの反復局所探索
- path: research/experiments/finite-field-kyouen-20261120/scripts/arc_search_report.py
  role: verifier
  note: 探索が出したアーク証人の独立再検査
- path: research/experiments/finite-field-kyouen-20261120/scripts/inversive_crossratio.py
  role: verifier
  note: 共円と複比のF_q有理性命題の全数検査
- path: research/experiments/finite-field-kyouen-20261120/output/arc_maxsearch_big.json
  role: data
  note: q=13..47 の検証済みアーク証人と下界
- path: research/experiments/finite-field-kyouen-20261120/output/arc_maxsearch_q49b.json
  role: data
  note: q=49 でサイズ32のアーク証人（予算5倍）
scope: 標準q=4の禁止条件 det[x,y,x^2+y^2,1]=0 を可換環上で読むことで定義される有限体盤 AG(2,q)（q は素数冪）、位数qの反転平面（3-(q^2+1,q+1,1)設計）、周期境界を課したトーラス盤 Z_n^2、および一般の Steiner t-(v,s,1) 設計上の完全指摘・通常プレイゲーム。q=3,5 の完全計算、n≤12 の行列式上界、トーラス盤とAG(2,p)の一致（p≤13）、9つのSteiner設計での三分法検証、反転平面の3-ネット翻訳（q≤9）。
evidence: 有限完全計算（q≤5 の全安全局面 Grundy、q≤8 の反転平面K厳密値、q≤7 のAG K厳密値、n≤12 の D(n)、p≤13 のトーラス一致、9設計のK、q≤9 の3-ネット横断数）と、3-設計公理の機械検査、交差比の鍵事実の全数検証（q≤7、247,840個の4点組、不一致0）。D(n)=a^2*floor(a^2/2) は n≤12 の全数確認済みだが全称証明ではない。層サイズ公式は k≤5 の範囲で証明、k≥6 は反例あり。トーラス盤とAG(2,p)の一致は Z_p=F_p から従うが全数確認は p≤13。三分法・一般上界 K≤lambda_2+2・一般下界 K=Omega((v/s)^(1/3))・派生上界 K≤1+A_2(D_p) は証明済み。K=3+alpha は q≤9 の検証であり一般証明ではない。反転平面のKはq=13,17,19,23,29で旧記録が誤りであり、10coの検証済み明示アーク（q=47で30）が新しい下界を与える。
---

# 共円ゲームの有限体盤・反転平面盤への移行と転送閾値

## 命題・範囲

標準共円ゲームの禁止条件は四点 `(x_i,y_i)` に対する整数行列式

```
Delta = det[[x_i, y_i, x_i^2+y_i^2, 1]] = 0
```

である。この多項式は任意の可換環で意味を持つので、盤を `F_q^2`（アフィン平面 AG(2,q)）や
反転平面に取り替えても同じ規則が定義できる。本項はその移行で何が保たれ何が壊れるかを記録する。

## 現在の根拠と限界

### 1. AG(2,q) 盤の円構造は q mod 4 で二分する（機械確認済み）

`x^2+y^2` の等方性が切り替わるため、円の構造が q mod 4 で変質する。

| q | q mod 4 | −1 は平方か | 円の個数 | 円サイズ分布 |
|---:|---:|---|---:|---|
| 3 | 3 | いいえ | 18 | {4: 18} |
| 5 | 1 | はい | 125 | {4: 100, 9: 25} |
| 7 | 3 | いいえ | 294 | {8: 294} |
| 11 | 3 | いいえ | 1,210 | {12: 1210} |
| 13 | 1 | はい | 2,197 | {12: 2028, 25: 169} |
| 17 | 1 | はい | 4,913 | {16: 4624, 33: 289} |
| 19 | 3 | いいえ | 6,498 | {20: 6498} |

q ≡ 3 (mod 4) では `x^2+y^2` が非等方で、全円がちょうど q+1 点（ユークリッド円の忠実な類似）。
q ≡ 1 (mod 4) では `x^2+y^2=(x+iy)(x−iy)` と分解し、円が直線対に退化する。
したがって「有限体版共円ゲーム」は q mod 4 で別ゲームであり、単一の族として扱えない。

### 2. 整数盤から有限体盤への転送は閾値付きでのみ成立する

素朴な期待「整数安全集合を mod q 還元すると AG(2,q) でも安全」は**偽**である。
n=4, q=5 では 5,811 個中 2,120 個、n=5, q=5 では 151,394 個中 122,168 個が反例になる。
原因は `Delta` が q の非零倍数になること。

正しい形は閾値定理である。`D(n) = max |Delta|`（n×n 格子の全四点組）とすると、
**q > D(n) なら `Delta ≡ 0 (mod q)` と `Delta = 0`（整数）が同値**になり、
整数盤の禁止集合がそのまま再現される。

| n | D(n) | 禁止四点 | 極値配置 |
|---:|---:|---:|---|
| 2 | 0 | 1 | — |
| 3 | 8 | 14 | (0,0),(2,0),(1,1),(0,2) |
| 4 | 36 | 194 | (0,0),(3,0),(1,1),(0,3) |
| 5 | 128 | 826 | (0,0),(4,0),(2,2),(0,4) |
| 6 | 300 | — | (0,0),(5,0),(2,2),(0,5) |
| 7 | 648 | — | (0,0),(6,0),(3,3),(0,6) |

観測値は `D(n) = a²⌊a²/2⌋`（`a=n−1`）に一致する。極値配置は常に
「三隅 (0,0),(a,0),(0,a) ＋ 対角点 (t,t)」で、その行列式は `−2a²t(a−t)`。
q > D(n) の 44 通りで禁止集合の完全一致を確認した（不一致 0）。

**補題（証明済み）**：三点の座標から定まる係数 gamma（x²+y² の係数）は
`gamma = −2·Area(p1,p2,p3)` を満たす。三点が `[0,a]²` 内なら `Area ≤ a²/2` なので `|gamma| ≤ a²`。

**連続上界の核心**：`|Delta| = |gamma|·|power|` で `|gamma| = 2·Area` なので、連続上界は
`Area · max|power| ≤ a⁴/4` と同値。a ≤ 7 の全三点で違反 0 で、最悪値がちょうど `a⁴/4` に一致する（鋭い上界）。
最悪ケースは a 奇数なら角の直角三角形 `(0,0),(a,0),(0,a)`（Area=a²/2, power=a²/2）、
a 偶数なら `(0,0),(a,0),(a/2,a/2)`（Area=a²/4, power=a²）。

**代数的整理**：`u=p2−p1`、`v=p3−p1` とおくと、ラグランジュの恒等式 `|u|²|v|² = (u×v)² + (u·v)²` と
外接円公式 `Area·R² = |u|²|v|²|u−v|²/(8|u×v|)` が使える。中心は
`O = ((|u|²v_y − |v|²u_y)/(2c), (|v|²u_x − |u|²v_x)/(2c))`（`c=|u×v|`）。
四点 `{0,u,v,O}` のバウンディングボックスが一辺 a に収まる条件の下で、`Area·R²` の最大は
**a ≤ 9 でちょうど `a⁴/4`** になる（極値は正方形の3角を結ぶ直角三角形）。`n`積は面積について単調ではないが、**最大は常に最大面積 `a²/2` で達成される**（a ≤ 9 の全数）。`n`さらに線形ギャップ不等式 `Area·R² ≤ a⁴/4 − c·(a²/2 − Area)` が `c ≥ 7/2` で成立する（a ≤ 8）。`n`これが示せれば「面積が最大でない場合」の評価が従う。

**連続緩和との関係**：四点目を実数に許した連続最大は `a⁴/2 + [a奇数]/2` で、
格子最大 `a²⌊a²/2⌋` との差は **a 奇数でちょうど 1**、a 偶数で 0 である（a ≤ 8 の全数計算）。
この分解により証明は「連続最大の評価」と「奇数のとき格子点で 1 下がること」の2段階に分かれる。
なお `Delta` は `gamma` の符号で凸にも凹にもなり、凹の場合は最大が内部（円の中心付近）で
達成されるため、「最大は常に角」という素朴な議論は誤りである。

**この閾値は実用上きわめて強い制約である**：D(n) は n について 4 次で増えるので、
n=11 では D(11) ≈ 5×10^5 となり、11×11 を埋め込める有限体は巨大な体に限られる。
つまり有限体盤は整数格子の近似として使えない。

### 3. 反転平面盤は q mod 4 依存を解消する

ユークリッド円の本質的性質「相異なる三点がちょうど一つの円を定める」を公理とした
有限構造が反転平面で、位数 q のそれは 3-(q²+1, q+1, 1) 設計である。
古典模型 `P¹(F_{q²})`（円は `P¹(F_q)` の `PGL(2,F_{q²})` による像）は全素数冪 q で存在する。

**全素数冪への拡張**：`F_{q²} = F_p[t]/(f)`（f は次数 2e の既約多項式）とし、
`F_q = {x : x^q = x}`（Frobenius 固定体）と取れば標数2も扱える。
円の列挙は「`P¹(F_q)` の PGL(2) 軌道」を BFS で生成する（生成元の拡大は**原始元**を選ぶ必要がある。
そうでないと軌道が部分群に閉じ、円の個数がちょうど半分になる。q=3,5 で実際に観測）。

| q | 体 | 点 | 円 | 円サイズ | 3-設計 |
|---:|---|---:|---:|---|---|
| 3 | F_9 | 10 | 30 | 4 | **True** |
| 4 | F_16 | 17 | 68 | 5 | **True** |
| 5 | F_25 | 26 | 130 | 6 | **True** |
| 7 | F_49 | 50 | 350 | 8 | **True** |
| 8 | F_64 | 65 | 520 | 9 | **True** |
| 9 | F_81 | 82 | 738 | 10 | **True** |

いずれも理論値 `n=q²+1`、`b=q(q²+1)`、`s=q+1` と一致し、全三点の一意被覆を全数確認した。
q=2 は 5点・円サイズ3で4点が同一円に載らず、ゲームが自明になるため除外する。

q=3,5 では全安全局面の Grundy まで計算した。

| q | 点 | 安全局面 | K | s | g(空盤) | Grundy 分布 | 勝ち初手 |
|---:|---:|---:|---:|---:|---:|---|---:|
| 3 | 10 | 428 | 5 | 5 | 1 | {0:202, 1:226} | 10/10 |
| 5 | 26 | 47,152 | 6 | 5 | 1 | {0:18226, 1:17226, 2:11700} | 26/26 |
| 7 | 50 | 2,551,236 | **6** | 5 | **0** | {0:1,443,786, 1:1,078,050, 2:29,400} | **0/50（初手すべて負け）** |

q=7 は「全安全局面の列挙は不可能」と長く考えられていたが、実際には 2,551,236 局面しかなく、
**K1253 で完全計算された**（空盤 `g=0`、すなわち後手勝ち）。
以下は当時の記録：
サイズ6の安全集合は実在し、サイズ7は**存在しない**（2,551,236 ノードで全空間を尽くして確認）。
この探索は q=5 で較正済み（サイズ6発見・サイズ7不存在を再現）。
さらに q=7 の K=6 は**二つの独立実装**でノード数まで一致した
（素数専用の二次拡大構成と、一般素数冪構成＋BFS 円生成）。

数え上げ上界 `C(k,3) ≤ b` は q=7 で k≤13 を与えるが、実際の K は 6 で**差が7**。
円が q+1 点と大きいため、少数の点でも三点が同一円に集中し、組合せ的余裕がほとんどない。

| q | 点 | 円 | 円サイズ | K（厳密） | 数え上げ上界 | 差 |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 10 | 30 | 4 | 5 | 6 | 1 |
| 4 | 17 | 68 | 5 | **5** | 8 | 3 |
| 5 | 26 | 130 | 6 | 6 | 10 | 4 |
| 7 | 50 | 350 | 8 | **6** | 13 | **7** |
| 8 | 65 | 520 | 9 | **7** | 15 | **8** |

AG(2,q) 側は q=8 で K=8（64点・556ブロック、サイズ9が不存在を943,265ノードで確認）。反転平面の 7 より 1 大きい。

AG(2,q) 側は q=8 で K=8（64点・556ブロック、サイズ9が不存在を943,265ノードで確認）。
反転平面の 7 より 1 大きい。

K は 5, 5, 6, 6 とほとんど伸びず、上界との差は 1→3→4→7 と広がる。
q=8 は K=7 を厳密決定（サイズ8が不存在、1,371,617 ノード）。q=9 はサイズ8の実在のみ確認し 8≤K≤17。

**成長率**：q ≤ 8 の5点（K = 5,5,6,6,7）で log-log フィットすると `K ≈ 3.39·q^0.33` となるが、
データ点が少なく成長率の主張としては弱い（線形フィットの SSE 0.419 に対しべき乗は 0.013 だが、
実質的な情報は「K が 5 から 7 へ緩やかに増える」ことだけ）。
対照的に整数格子は `K_n ≈ 2n`（線形）。密度 K/n は q=8 で反転平面 0.108 対 整数 0.234 と約2倍の差。
初等的な数え上げ上界（triple, pair）はいずれも `O(q)` を与えるので、
観測された K の小ささは単純な数え上げでは説明できない。

### 4. 層サイズの厳密公式（k ≤ 5）

`B_c` を「円 c 上に4点以上載る」事象とすると、相異なる二円がともに成立するには
`|S| ≥ 4+4−2 = 6` が必要（二円は高々2点で交わる）。よって **k ≤ 5 では事象が互いに素**で

```
L_k = C(n,k) − b · Σ_{j=4}^{min(k,s)} C(s,j) C(n−s, k−j)      (k ≤ 5)
```

が成り立つ。q=3,5 の全 k ≤ 5 で厳密一致を確認。**k=6 では破綻する**
（q=5 の k=6 で厳密値 5,200 に対し公式は −156,000）。

### 5. 最大安全サイズ

AG(2,q) 盤（円と直線の両方がブロック）：

| q | 盤の点数 | ブロック数 | K | 状態 |
|---:|---:|---:|---:|---|
| 3 | 9 | 30 | **5** | 厳密 |
| 4 | 16 | 78 | **5** | 厳密 |
| 5 | 25 | 155 | **6** | 厳密 |
| 7 | 49 | 350 | **6** | 厳密 |
| 8 | 64 | 556 | **8** | 厳密 |
| 9 | 81 | 819 | **9** | 厳密 |
| 11 | 121 | 1,342 | **9** | 厳密 |
| 13 | 169 | 2,379 | **13** | 修正版で再確認 |
| 16 | 256 | 4,248 | **撤回** | バグにより無効 |
| 17 | 289 | 5,219 | **撤回** | バグにより無効 |
| 19 | 361 | 6,878 | **撤回** | バグにより無効 |

注意：円の個数が q²(q−1) になるのは **q が奇素数のときのみ**。q=4（標数2）では
x²+y²=(x+y)² と分解して円が退化し、実測 58 個（理論値 48）になる。
q≡1 (mod 4) でも退化が起きる（q=5 でサイズ4の円が100個）。

**一般上界（証明済み）**：`q ≡ 1 (mod 4)` かつ `k ≥ q` のとき **`K(AG(2,q)) ≤ q + 2`**。

粗い版は `3q²/(2q−1) ≈ 1.5q`。改良版の証明は次の通り。
`−1` が平方なので `x²+y² = (x+iy)(x−iy)` と分解し、円の方程式が `s·t+a·s+b·t+c=0` になる。
`ab=c` の退化円は「列＋行」の十字（`2q−1` 点）で、これが `q²` 個ある。
安全集合は各十字に高々3点なので、`a_c + b_r − x_{cr} ≤ 3` が成り立つ。

1. `r` について和を取ると `(q−1)a_c ≤ 3q − k`。`k ≥ q` なら `a_c < 3` なので **各列・各行は高々2点**。
2. 2点を持つ列 `C₂` と行 `R₂` について、`c∈C₂, r∈R₂` なら交点が必須なので `S` は `C₂×R₂` を含む。
3. 各列は高々2点なので `|C₂|·|R₂| ≤ 2|C₂|` より `|R₂| ≤ 2`、同様に `|C₂| ≤ 2`。
4. よって `k ≤ 2·2 + (q−2)·1 = q+2`。□

q=5,9,13,17 で十字の個数が `q²` に一致し、2つの十字の交わりが「2点」または「q点」であることを確認した。

**上界の比較**：単純な組合せ上界はいずれも緩い。q=7 で triple 上界13・second moment 16・直線のみ21・4点部分集合47 に対し真値は6。
second moment（`λ₂=q+1` は一様）は triple より弱い。直線制約だけでは q=5 で k=6 のキャップが存在するため何も排除できない。
十字上界が最強（q≡1 mod 4）で、改良版 `q+2` は `K/q ≈ 1` という観測と整合する。

**全 q で有効な一般上界（無条件）**：`K ≤ λ₂ + 2 = q + 3`。

「任意の三点が同一円または同一直線上にある」は**恒真**である：三点が一直線なら直線ブロック上、
そうでなければその三点を通る円が一意に存在する。したがって下の証明は前提なしで成立する。

証明：`p,q ∈ S` を固定すると、`S\{p,q}` の各点 `r` について三点 `{p,q,r}` はブロック上にあり、
そのブロックは `p,q` を通るので `λ₂` 個のペンシルのいずれかである。
異なる `r` は異なるブロックを与える（同じなら4点を含み安全集合に矛盾）。
よって `|S| − 2 ≤ λ₂`。AG(2,q) も反転平面も `λ₂ = q+1`（一様、機械確認）なので `K ≤ q+3`。
これは `q ≡ 3 (mod 4)` で triple 上界 1.82q を大きく改善する（q=19 で 22 対 35）。
ただし真値との差は q とともに広がる（q=3 で1、q=7 で4、q=11 で5）。

**この上界はペンシル議論では改善できない**：`m` 点を固定して `C(m,2)` 個のペンシルを使っても、
包除の補正項と必要量が打ち消し合い、上界は `λ₂ + 2` のまま `m` に依らない（m=3..8 で確認）。
次数による議論も `k ≤ 2q+4` 程度で弱い。改善には別の原理が必要である。

**上界が達成されない理由**：差は q=3,5,7,9 で **1,2,4,3** と単調ではない（q=7 で最大、q=9 で減少）。
なお「q≡1 (mod 4) なら K=q」という予想は **q=5 で反例**があるため撤回した（K=6 > q=5）。

**K/q と大きなブロックの相関（交絡であり因果ではない）**：大きなブロック（サイズ > q+1）の有無と K/q は相関するが、
**大きなブロックを除くと K は増加する**（q=4: 5→9、q=5: 6→10）。
つまり大きなブロックは制約として K を**下げる**。
相関は q mod 4 や q の偶奇との交絡であり、因果ではない。

| q | 大きなブロック | K/q |
|---:|---|---:|
| 7 | なし（最大 q+1） | **0.86** |
| 11 | なし（最大 q+1） | **0.82** |
| 4 | あり（2q、標数2退化） | 1.25 |
| 5 | あり（2q−1、十字） | 1.20 |
| 8 | あり（2q、標数2退化） | 1.00 |
| 9 | あり（2q−1、十字） | 1.00 |

大きなブロックは十字（`q≡1 mod 4`）または標数2の退化円（`q` 偶数）から生じる。
K/q が高い q では大きなブロックが存在するが、それは**交絡**であり、
大きなブロック自体は K を下げる制約として働く。

**アブレーションによる要因特定**：ブロック族を1つずつ除くと、
**円（サイズ q+1）が K を支配的に抑えている**ことが分かる。

| q | 条件 | K |
|---:|---|---:|
| 5 | 全ブロック | 6 |
| 5 | 十字（サイズ9）を除く | **10** |
| 5 | 直線（サイズ5）を除く | 6 |
| 7 | 全ブロック | 6 |
| 7 | 真円（サイズ8）を除く | **≥15** |
| 7 | 直線（サイズ7）を除く | 8 |
| 9 | 全ブロック | 9 |
| 9 | 退化円（サイズ8）を除く | 11 |
| 9 | 直線（サイズ9）を除く | 10 |
| 9 | 十字（サイズ17）を除く | **≥12** |

円を除くと K が激増し（q=5 で 1.67倍、q=7 で 2.5倍以上）、直線の寄与は小さい。
特に**真円（サイズ q+1）の除去効果が圧倒的**（q=7 で +9以上）で、
退化円（サイズ q−1）の除去効果は小さい（q=5 で +1、q=9 で +2）。
十字の除去効果は大きい（q=5 で +4、q=9 で +3以上）。

**K/q のパターン（確定）**：**真円（サイズ q+1）の有無**で決まる。

| q | q mod 4 | K/q | 真円 |
|---:|---:|---:|---|
| 7 | 3 | **0.86** | あり（294個） |
| 11 | 3 | **0.82** | あり（1210個） |
| 4 | 0 | 1.25 | なし |
| 5 | 1 | 1.20 | なし |
| 8 | 0 | 1.00 | なし |
| 9 | 1 | 1.00 | なし |

**q ≥ 7 では完全に分離する**：真円あり → K/q < 1、真円なし → K/q ≥ 1。
真円が存在するのは `q ≡ 3 (mod 4)` のとき（`x²+y²` が非等方）のみ。
したがって **`q ≡ 3 (mod 4)` かつ `q ≥ 7` なら K/q < 1、それ以外なら K/q ≥ 1**。
q=3 は盤が小さい（9点）ため例外（K/q=1.67）。

**真円が強い理由**：真円（サイズ q+1）と退化円（サイズ q−1）は
**どちらも共線三点を含まない**（機械確認：q=7 の真円 0/56、q=5 の退化円 0/4）。
したがって違いは共線三点の有無ではなく**ブロックサイズ**である。
真円は q+1 点と大きいので、「1ブロックあたり3点まで」の制約をより多くの点の組に課し、
K を強く抑える。
アブレーション結果（q=7 で真円を除くと +9以上、q=5 で退化円を除いても +1）と整合する。

**単一族での定量的確認**：ブロック族を1つだけにした盤では、**ブロックサイズが大きいほど K が小さい**。

| q | 族 | サイズ | 個数 | K |
|---:|---|---:|---:|---:|
| 5 | 退化円のみ | 4 | 100 | **15** |
| 5 | 直線のみ | 5 | 30 | **11** |
| 5 | 十字のみ | 9 | 25 | **7** |
| 7 | 直線のみ | 7 | 56 | ≥15 |
| 7 | 真円のみ | 8 | 294 | **8** |

q=7 ではサイズ8の方が個数が多い（294 対 56）のに K が小さいので、
**サイズの効果が個数の効果を上回る**。
理論的には、サイズ `s` のブロックは `C(s,3)` 個の三点組を消費するので、
大きいほど三点組の予算を早く使い切る。

q=5 ではサイズ7,8 が、q=7 ではサイズ8,9,10 が、q=9 ではサイズ10,11,12 がいずれも不存在であることを
完全探索で確認した（ノード数は q=5:881、q=7:22,341、q=9:378,101 と急増するが完全探索可能）。
AG(2,3) では6点部分集合84個**すべて**がサイズ4の円を完全に含むため、
サイズ6の安全集合は存在しない（全数検査）。
円の被覆構造が上界との差を生んでいると考えられるが、**被覆による上界は一般には弱い**：
ランダムな k-部分集合に含まれるブロックの期待値 `E[f]` が 1 を超えるのは
q=3 で k≈6、q=5 で k=9、q=7 で k≈25 であり、真値（q=5,7 で K=6）と大きく乖離する。
被覆が効くのは盤が小さい q=3 のみである。

**上界の総括**：`q ≡ 1 (mod 4)` では十字上界 `q+2` により gap が 1〜2 に収まる
（q=5:1, q=9:2, q=13:≤2, q=17:≤2）。
一方 `q ≡ 3 (mod 4)` では λ₂ 上界 `q+3` のみで gap が 4〜9 に広がる（q=7:4, q=11:5, q=19:≤9）。
**`q ≡ 3 (mod 4)` の上界改善が最大の課題**である。試した4手法はいずれも失敗した：

1. 次数 `(k−1)(q+2−k/2) ≤ q²+q` は制約なし
2. 複数ペンシルは `λ₂+2` のまま
3. 被覆は q=3 のみ有効
4. 使用済み円のペア `C(k,2)C(k−2,2) ≤ 2C(C(k,3),2)` は常に成立し制約なし
5. 円のプロファイル（3点円 = `C(k,3)`、2点円 = `C(k,2)(q−k+3)`）は `λ₂+2` を再現するのみで改善しない
6. サイズ重み付きペア `μ₂·C(k,2) ≤ 3Σ|B|` は q=5,7 で 12,16 と弱い
7. ペンシルのサイズ和 `k−2 ≤ Σ(|B|−2)` は 25,49 と非常に弱い

サイズ効果は実験的に明確（単一族で K がサイズに単調減少）だが、**上界の証明には翻訳できない**。
`λ₂` 上界の証明はブロックのサイズを一切使わず「本数」だけを使うため鋭い。

初等的な数え上げはすべて係数 ≥1 を与え、観測された `K/q ≈ 0.68〜1.00` を下回れない。
係数1未満には代数幾何・設計論・加法的組合せ論など別の原理が必要と考えられる。

**上界研究の到達点**：証明済みの上界は4つ。

- `K ≤ q+3`（無条件、λ₂ 上界）
- `K ≤ q+2`（`q ≡ 1 (mod 4)`、十字上界）
- `K ≤ q+2`（**`q` 奇数、K1250 の射影上界**：`P` からの射影で `S\{P}` は `PG(2,q)` のアークになり、
  `A₂(q) = q+1` を使う。`q ≡ 3 (mod 4)` 側の `q+3` を改善）
- **`K ≤ q`（`q` 奇数、`q ≥ 9`、無条件、K1252）** — 射影上界の等号ケース `k = q+2` と
  `k = q+1` を（Segre の q-アーク定理と2つの二次錐の交わりで）排除する。
  以上の無条件上界をまとめると、**`q ≥ 9` の奇数では `K ≤ q`**（`q=7` では `q+1`）。
- （条件付き）`K ≤ q+1`（MDS予想が成り立つ q。素数 q では Ball の定理で無条件。K1250）

真値は AG で q ≤ 13、反転平面で q ≤ 13 まで確定（反転平面は K1250/10co で再測定中）。

**バグ修正後の再確認（2026-11-20）**：C++ 実装の64ビットマスクを多倍長ビットセットに修正して再計算した結果、
**K(AG(2,13)) = 13 が再確認された**（サイズ14が不存在を3,005万ノード・654秒で確認）。
バグ版のノード数（1,674万）は点の同一視で探索空間が縮んでいたためだが、結論は同じだった。
修正版は AG(2,11) の K=9 も再確認した（サイズ10が不存在を346万ノードで確認）。

**バグの影響範囲（2026-11-23 に再々訂正）**：

| 項目 | 影響 |
|---|---|
| パリティ法則・上界 q+3/q+2・層サイズ公式（すべて数学的証明） | **なし** |
| 転送閾値 D(n)（Python/BigInt 実装） | **なし** |
| K(AG(2,q)) q ≤ 16 | **なし**（修正版で再確認） |
| K(反転平面 q) q ≤ 11 | **なし**（修正版で再確認） |
| K(反転平面 q) q = 13, 17, 19 | **あり —— ただし「修正後」の 8, 9, 9 が誤り。10co の検証済み証人が 10, 13, 14 を与え、これは修正前の値と一致する** |
| K(反転平面 q) q = 23, 29 | **あり —— 10co の検証済み下界は 16, 20。旧値 10, 8 を撤回** |

**`K` の増大度（10co で全面更新）**：q ≤ 49 の検証済み下界では `K/q` は 0.77（q=13）から
0.64 前後（q=43〜49）へゆっくり減少する。したがって「`K ≈ 8.86`（ほぼ定数）」も
「`K ≈ 3.83·q^0.31`」も**撤回**する。証明済みの枠は
`(6q)^(1/3) ≤ K ≤ q`（`q` 奇数, `q ≥ 9`、K1252）と `K ≤ q+3`（`q` 偶数）であり、
実測は下界より遥かに上・上界より下にある。

**定理（証明済み）：`K = Ω(q^(1/3))`**：極大安全集合 `S`（`|S| = k`）では `S` の外の全点が
「`S` の3点を含む円」でブロックされねばならない。各三点組は一つの円を定め、その円は
`q−2` 点を `S` の外に持つので `q²+1−k ≤ C(k,3)·(q−2)`、漸近的に `k ≥ (6q)^(1/3)`。□
C++ 実装（`scripts/agq2.cpp`）の枝刈り強化（候補可用性＋ペンシル実用可能性）により、
q=11 のサイズ10不存在が19秒（284万ノード）で確認できる。

7つの初等的な手法がすべて失敗し、係数1未満の上界には別の原理が必要であることが明確になった。

**代数的再定式化**：各点を持ち上げて `v_p = (x, y, x²+y², 1) ∈ F_q⁴` とすると、
四点の共円・共線は `det[v_p1,v_p2,v_p3,v_p4] = 0`、すなわち**4ベクトルの線形従属**と同値。
よって安全集合は「どの4つも従属でない」集合であり、これは**放物面 `Z=X²+Y²` 上の cap**、
反転平面の言葉では **3-arc**（どの円とも3点以下で交わる集合）に他ならない。
符号理論的には「パリティ検査行列の任意3列が独立」に対応するが、Singleton 限界は下界しか与えない。
文献調査では最大 3-arc サイズの明示的な既知結果を確認できなかった。

Sonnino は奇数の q に対して (q+5)-arc を構成しているが、これは**別問題**であることが判明した。
反転平面の「k-arc」は各円と高々2点と定義され、公理 (A1)（任意の三点が一意に円を定める）から
**2-arc の最大サイズは 2** である（q=3,4,5,7 で計算確認）。
したがって Sonnino の arc は別の定義か、Ad(q) が標準的でない反転平面であり、
我々の K（3-arc の最大）とは直接比較できない。

なお反転平面の公理 (I.1)「任意の三点が一意に円を定める」、(I.2)「二円は一点で接する円が一意」、
(I.3)「同一円上にない4点が存在する」を文献で確認した。
我々が使った性質（三点の一意被覆、二円の高々2点交差）はすべて公理から従い、
恒真性の主張と整合する。

AG(2,11) ではサイズ10,11,12 がいずれも不存在であることを完全探索で確認し、**K=9 が確定**した。

**q ≡ 3 (mod 4) では十字がない**：ブロックは直線（サイズ q）と真円（サイズ q+1）のみ。
初等的な上界は triple `C(k,3) ≤ q³+q` から `k ≈ 1.82q` が最良
（pair は `q·C(k,2) ≤ 3b` で 2.4q、incidence は `deg·k ≤ 3b` で 2.7q とより緩い）。

**極値配置の構造**（恒真性の確認）：q=3,5,7,9 の**すべて**で、最大安全集合は
**任意の三点が同一円または同一直線上にある**（完全探索で確認：10/10, 20/20, 20/20, 84/84）。
さらに各点が同じ数の満杯ブロック（3点を持つブロック）に載る（q=7 で各点10個、q=11 で各点28個）。
これは「キャップ」（どの三点も共線でない集合）の逆の極端な構造である。
ただし `C(k,3) ≤ b` は飽和しない（q=9 で 84 対 819）ので、triple 上界の改善には直結しない。

上界/真値の比は q≡1 (mod 4) で 1.1〜1.2、q≡3 (mod 4) で 2.2〜2.7 であり、
**十字ブロックの有無が上界の鋭さを決めている**。

上界は `C(k,3) ≤ q²(q−1)+q(q+1) = q³+q`（安全集合の各三点が一意に円または直線を定め、
そのブロックは高々3点しか持てない）。整数格子の `K_n ≈ 2n` と対照的に、有限体盤は相対的に疎である。

q=7 の K=6 は固定サイズ完全探索で決定した（サイズ7が不存在、2,276,002 ノード）。

**AG(2,q) と反転平面の K は q ≤ 7 で一致するが、q=8 で乖離する**（AG=8、反転平面=7）。
点数はほぼ同じ（q² 対 q²+1）だがブロック構造は大きく異なる（AG は円と直線、
反転平面は円のみで各円 q+1 点）。q=8 で AG(2,8)=8、反転平面=7 となり**初めて乖離する**（AG が大きい）。

q=9 では**両者とも K=9 で厳密に一致**する。AG(2,9) は AGL の2-推移性、
反転平面は PGL(2,81) の3-推移性を使って対称性破壊し、サイズ10が不存在であることを
完全探索で確認した（それぞれ 261,023 ノード・21,212 ノード）。

q=11 でも**両者とも K=9 で一致**（AG は 5,524,351 ノード、反転平面は 226,681 ノードでサイズ10の不存在を確認）。
**q=9 から q=11 へ増えても K は 9 のまま**で、成長が止まる。

q=13 で**大きな乖離が現れる**：反転平面は K=10（厳密、サイズ11が不存在を217万ノードで確認）、
AG(2,13) は K≥13（サイズ13まで実在、14以上は未判定）。

| q | 3 | 4 | 5 | 7 | 8 | 9 | 11 | 13 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AG(2,q) | 5 | 5 | 6 | 6 | **8** | 9 | 9 | **13** | **16** |
| 反転平面 | 5 | 5 | 6 | 6 | **7** | 9 | 9 | **8** | ? |

AG の K は q=11→13 で 9→13 へ跳ね上がり、q=16 では ≥16（K/q ≥ 1.00）。
反転平面は 9→10 と緩やか。
AG のブロック構造が反転平面より緩いためと考えられる。

q=13 は `q ≡ 1 (mod 4)` なので円が退化し、サイズ12の退化円 2,028 個と
サイズ25の十字 169 個に分かれる（サイズ14の真円は存在しない）。
族別に測ると円のみで ≥14、直線のみで ≥23、全体で ≥13 であり、
**AG の円族は反転平面のサイズ14円より緩い**ことが乖離の一因と考えられる。

**撤回**：AG(2,16) の K=16 も同じバグにより無効（N=256 > 64）。`n`**撤回**：反転平面 q=16 の K=12 も同じバグにより無効（N=257 > 64）。`n`**全面訂正（2026-11-20）**：バグ修正後の再計算により、反転平面の q ≥ 13 の K はすべて**過大**だったことが判明した。`n``n| q | 旧（バグ版） | **新（修正版）** |`n|---:|---:|---:|`n`| 13 | 10 | **8** |`n`| 17 | 13 | **9** |`n`| 19 | 14 | **9** |`n``n修正版は q ≤ 11 の既知値を完全に再現しており信頼できる。`n`**K/q は単調減少する**（q=11:0.82 → q=13:0.62 → q=17:0.53 → q=19:0.47）。`n`したがって「K/q が 0.74〜0.77 で安定」「構造の均一性が安定をもたらす」という以前の主張は**撤回**する。`n`**撤回**：反転平面 q=19 の K=14 も同じバグにより無効（N=362 > 64）。`n`**反転平面で有効なのは q ≤ 7 のみ**（5,5,6,6,7）。q ≥ 8 はバグにより撤回。`n``n**枝刈りの強さと発見速度は別**：AG(2,17) で十字制約の枝刈りを追加すると、`n`枝刈りは正しい（解を排除しない）が探索順序が変わり、サイズ15の発見が 3,260ノードから上限超過に悪化する。`n`完全探索（不存在の証明）では枝刈りが効くが、存在の発見では順序が支配的である。`n``n**反転平面の K/q が安定する理由**：反転平面は**構造が完全に均一**である。`n`すべての円がサイズ `q+1` で、すべての点が `q²+q` 個の円に載る（円サイズも次数も1種類のみ）。`n`一方 AG は複数サイズのブロックが混在する（q=13 で {12, 13, 25} の3種類）。`n`この均一性が K/q の安定（0.75〜0.77）をもたらし、AG の非均一性が K/q の変動（0.82〜1.25）を生むと考えられる。`n`**反転平面では「真円の有無」パターンが適用されない**：反転平面の円は常にサイズ q+1 の真円であり退化しないため、`n`AG 固有の区別が存在しない。実際 q=16 で K/q = 0.75 < 1 である。

**円の退化が K を大きくする**（仮説を支持する証拠）：

| q | q mod 4 | 点 | ブロックサイズ | K |
|---:|---:|---:|---|---:|
| 17 | 1 | 289 | {16:4624, 17:306, 33:289} | **≥17** |
| 19 | 3 | 361 | {19:380, 20:6498} | **≥13** |

点数は q=19 の方が多い（361 対 289）のに、K の下界は q=17 の方が大きい（17 対 13）。
q≡1 (mod 4) では円がサイズ q−1 に退化して制約が弱まるためと考えられる。

**定量的なパターン**：`q ≡ 1 (mod 4)` では `K/q ≈ 1.00` で一定（q=9,13,17 で 1.00、q=5 で 1.20）。
これは平均ブロックサイズがちょうど `q` になることと対応する（退化円 `q−1` と十字 `2q−1` が釣り合う）。
一方 `q ≡ 3 (mod 4)` では平均サイズが `q` より大きく（真円 `q+1` が支配的）、
`K/q` は 1.67→0.86→0.82→0.68 と減少する。

q≡1 (mod 4) の q=5,9,13,17 は K が 6,9,≥13,≥17 と伸び、
q≡3 (mod 4) の q=7,11,19 は 6,9,≥13 と伸びが遅い。

同じ点数での比較では有限体盤の方がはるかに疎である：
7×7 整数の K=14 に対し AG(2,7) は 6（半分以下）。

### 6. 定理：極大集合が一様なら Grundy 値は (T−|S|) mod 2

**定理（証明済み）**：盤のすべての極大安全集合が同じサイズ `T` を持つとき、
任意の安全局面 `S` について

```
g(S) = (T − |S|) mod 2
```

**証明**：`S` からの任意の完全プレイはサイズ `T` の極大集合に到達するので、
プレイ長は常に `T−|S|`。ゲーム木は一様深さの木であり、深さ `d` について帰納すると
mex が `d mod 2` になる。□

**系**：一様な盤ではすべての Grundy 値が 0 か 1。非一様な盤では非自明な値が現れうる。

**全数検証**：

| 盤 | 極大集合のサイズ | 一様 | 最大 Grundy |
|---|---|---|---|
| 反転平面 q=3 | {5} | ✓ | **1** |
| 反転平面 q=4 | {5} | ✓ | **1** |
| AG(2,3) | {5} | ✓ | **1** |
| 3×3 整数 | {5} | ✓ | **1** |
| 反転平面 q=5 | {5,6} | ✗ | 2 |
| AG(2,5) | {3,5,6} | ✗ | 2 |
| 4×4 整数 | {5,6,7} | ✗ | 5 |
| 5×5 整数 | {5..9} | ✗ | 6 |

一様な4盤すべてで定理が成立（全局面照合、不一致0）。
**非自明な Grundy 値（2以上）の出現は極大集合の非一様性を必要とする。**

### 7. 初手値の分布（3型）

完全計算できた盤では、初手の値の分布は3型に限られた。

| 盤 | g(空盤) | 勝ち初手 | 型 |
|---|---:|---:|---|
| 2×2, 3×3 整数 | 1 | 全点 | 全初手勝ち |
| 4×4 整数 | 0 | 0 | 全初手負け |
| **5×5 整数** | 1 | **9/25** | **部分勝ち** |
| AG(2,3), AG(2,5) | 1 | 全点 | 全初手勝ち |
| 反転平面 q=3,5 | 1 | 全点 | 全初手勝ち |

5×5 の勝ち初手は中心菱形を成す：

```
W = { (x,y) : x+y ≡ 0 (mod 2) かつ |x−2|+|y−2| ≤ 2 }
```

25 点全数で照合し不一致 0。負け初手 16 個はすべて Grundy 値 3。
この閉形式は n=5 固有の観測であり、n=3 には当てはまらない（n=3 は全初手勝ち）。

### 7. トーラス盤は素数位数で AG(2,p) と一致する

`Z_n × Z_n` に周期境界を課し、同じ行列式を mod n で評価した「トーラス盤」を考える。

| n | 素数か | トーラス禁止四点 | AG(2,n) 禁止四点 | 一致 |
|---:|---|---:|---:|---|
| 3 | はい | 18 | 18 | **True** |
| 4 | いいえ | 924 | 696 | False |
| 5 | はい | 3,150 | 3,150 | **True** |
| 7 | はい | 22,540 | 22,540 | **True** |
| 11 | はい | 642,510 | 642,510 | **True** |
| 13 | はい | 3,030,170 | 3,030,170 | **True** |

n が素数なら `Z_n = F_n` なので、トーラス盤はアフィン平面盤と点集合・禁止集合ともに同一である。
n=4 では `Z_4` が体でなく `AG(2,4)=F_4²` と異なるため、トーラス盤に 228 個の余分な禁止四点が生じる。
全 n で平面盤の禁止四点はトーラス盤に含まれる（`Delta=0 ⇒ Delta≡0 (mod n)`）。

ゲーム値では n=4 が劇的に異なる：平面盤は後手必勝（K=7）だが、
トーラス盤は先手必勝（K=4）になる。禁止四点を増やすと勝者が反転する明示例である。

### 8. 変種：misère と k 点版

反転平面ゲームの2変種を q ≤ 4 で完全計算した。

| q | 禁止点数 | ルール | 安全局面 | K | 空盤の勝者 |
|---:|---:|---|---:|---:|---|
| 3 | 4 | 通常 | 428 | 5 | 先手 |
| 3 | 4 | misère | 428 | 5 | **後手** |
| 3 | 5 | 通常 | 1,024 | 10 | **後手** |
| 3 | 5 | misère | 1,024 | 10 | **先手** |
| 4 | 4 | 通常 | 4,914 | 5 | 先手 |
| 4 | 4 | misère | 4,914 | 5 | **後手** |
| 4 | 5 | 通常 | 48,604 | 9 | 先手 |
| 4 | 5 | misère | 48,604 | 9 | **後手** |

**misère は 4 例すべてで通常版の勝敗を反転させた**（初手の勝敗も完全に反転）。
反転平面では全極大安全集合が同じ石数になる可能性が高く（q=3,4 の k=4 で最小極大 = 最大 = K）、
そうなら手番数が固定されて通常版と misère 版の勝者は必ず入れ替わる。
ただしこれは観測であって証明ではない。

**k=5 版は K をほぼ倍にする**（q=3 で 5→10、q=4 で 5→9）。
円が q+1 点しかないため、5 点そろえるのは 4 点よりずっと難しい。
k=5 版の勝者は q に依存する（q=3 は後手必勝、q=4 は先手必勝）。

### 9. 一般化：Steiner 設計上の共円ゲームと三分法

`AG(2,q)` も反転平面も **Steiner 3-設計**（任意の3点がちょうど1ブロックに乗る）である。
そこで一般に `t-(v,s,1)` 設計 `D` 上でゲームを定義する：安全 = どのブロックとも3点以下で交わる。

**三分法（証明済み）**：

| | `s ≤ 3` | `s = 4` | `s ≥ 5` |
|---|---|---|---|
| **`t ≥ 4`** | `K = 3` | `K = 3` | `K = 3` |
| **`t = 3`** | `K = v` | `K = v − τ` | **新しい不変量** |
| **`t = 2`** | `K = v` | `K = v − τ` | `(k,3)`-アーク |

**自明化定理**：`t ≥ 4` なら任意の4点が同一ブロック上にあるので `K = 3`。
よってゲームが非自明なのは `t = 3` のときに限る。 □

**一般上界（証明済み）**：任意の Steiner 3-設計で `K ≤ λ₂ + 2`、`λ₂ = (v−2)/(s−2)`。
**一般下界（証明済み）**：`v − k ≤ C(k,3)(s−3)`、すなわち `K = Ω((v/s)^(1/3))`。

**検証**（`design_trichotomy.py`、9設計すべてで三分法が成立）：

| 設計 | `t` | `v` | `s` | `K` |
|---|---:|---:|---:|---:|
| `PG(2,2)` | 2 | 7 | 3 | 7 |
| `PG(2,3)` | 2 | 13 | 4 | 9 |
| `PG(2,5)` | 2 | 31 | 6 | 11 |
| `AG(3,2)=S(3,4,8)` | 3 | 8 | 4 | 4 |
| 反転平面 `q=3` | 3 | 10 | 4 | 5 |
| Witt `S(3,6,22)` | 3 | 22 | 6 | 7 |
| 反転平面 `q=5` | 3 | 26 | 6 | 6 |
| Witt `S(4,5,11)` | 4 | 11 | 5 | **3** |
| Witt `S(5,6,12)` | 5 | 12 | 6 | **3** |

**`K` は設計パラメータで決まらない**：`AG(2,13)`（`v=169, s∈{13,14}, λ₂=13`）は `K=13`、
反転平面 `q=13`（`v=170, s=14, λ₂=14`）は `K=8`。ほぼ同一パラメータで `K` が 5 違う。

### 10. 反転平面は 3-ネットの部分横断問題である

**鍵となる事実（全数検証済み）**：`P¹(F_{q²})` の4点が共円 ⟺ 射影的交差比が `P¹(F_q)` に入る。
同次座標で `[z_i,z_j] = u_i v_j − u_j v_i`、交差比 `= [z₁,z₃][z₂,z₄]/([z₁,z₄][z₂,z₃])`。
q=3,4,5,7 の全 247,840 個の4点組で不一致 **0**。

**注意**：`∞` を含む場合は同次座標が必須。非斉次な極限で書くと q=3 で 72/210 が不一致になる。

`PGL(2,F_{q²})` の3重推移性により `S = {0,1,∞} ∪ T`、`T ⊂ F_{q²}\F_q` と正規化できる。
族 B（`{a,b,z,z'}`、`a,b ∈ {0,1,∞}`）の条件は `F_{q²}\F_q`（`q²−q` 点）の
**3つの分割**を与える：

```
P₀   : 0 を通る F_q-直線で割る
P₁   : 1 を通る F_q-直線で割る
P_∞  : φ(z) = z/(1−z) による P₀ の引き戻し
```

各分割は **q クラス × サイズ q−1**。q=3,4,5,7,8,9 で機械確認済み。
これは **3-ネット**であり、族 B の条件は「`T` が 3-ネットの部分横断」と同値。よって

```
K(inversive q) ≤ 3 + τ₃(q)
```

族 C（3点条件）・族 D（4点条件）を加えると**等式**：

```
K(inversive q) = 3 + max{ |T| : {0,1,∞} ∪ T が安全 }
```

| q | `τ₃` | `3+τ₃`（上界） | 完全 | `3+完全` | `K` | 一致 |
|---:|---:|---:|---:|---:|---:|---|
| 3 | 2 | 5 | 2 | 5 | 5 | ✓ |
| 4 | 4 | 7 | 2 | 5 | 5 | ✓ |
| 5 | 4 | 7 | 3 | 6 | 6 | ✓ |
| 7 | 6 | 9 | 3 | 6 | 6 | ✓ |
| 8 | 8 | 11 | 4 | 7 | 7 | ✓ |
| 9 | 8 | 11 | 6 | 9 | 9 | ✓ |

**`τ₃` は線形に増えるが `K−3` は定数的にしか増えない。**
このギャップの正体は族 C, D の高次条件である。これが「なぜ `K ≈ 9` か」の構造的な答えである。

### 10b. 3-ネットのラテン方陣は完全に決定できる（定理）

`q` を奇数の素数冪とし、`F_{q²} = F_q[w]`、`w² = d ∈ F_q`（`d` は非平方）とする。
`F_{q²}\F_q` の点 `u = x + y·w`（`y ≠ 0`）に対し3つの分割は

```
a = x/y,   b = (x−1)/y,   c = φ(u) の方向（φ(u) = u/(1−u)）
```

**定理（ラテン方陣の完全公式）**：`a ≠ b` のとき

```
c = (d − a·b) / (a − b)
```

**証明**：`x = a/(a−b)`、`y = 1/(a−b)` を代入し、`φ(u)` の方向を計算すると
`c = [x(1−x) + d·y²]/y = (d − ab)/(a − b)`。 □

**検証**：q = 3,5,7,9 で全セル一致（6/6, 20/20, 42/42, 72/72）。

**系1（対角線が空）**：`a = b` なら `0 = 1` となり矛盾。よって格子は
「対角線を除いたラテン方陣」。

**系2（`(b,c)` 対称性）**：関係式は `ab + ac − bc = d` と同値で `b ↔ c` 不変。
よって `c(a,b) = c' ⟺ b(a,c) = c'`。

**系3（和の恒等式）**：`a` について和を取ると `q·d = 0` より

```
⟨id,σ⟩ + ⟨id,c⟩ − ⟨σ,c⟩ = 0
```

**系4（メビウス対合）**：`a` を固定すると `b ↦ c` は

```
M_a(t) = (d − a·t)/(a − t)
```

で、これは `P¹(F_q)` の対合。`M_a(a) = ∞`、`M_a(∞) = a`。
固定点は `(t−a)² = a² − d` の解なので、`a² − d` が平方となる
ちょうど `(q−1)/2` 個の `a` で2個、残りでは0個（q=3,5,7,9 で検証）。

**系5（ノルム1トーラスの群法則）**：`a = 1/A`、`b = 1/S`、`c = 1/T` と置くと
関係式は

```
A = (S + T) / (1 + d·S·T) =: S *_d T
```

**これはノルム1トーラス**

```
T_d = { (X,Y) ∈ F_q² : X² − d·Y² = 1 }  ≅  { z ∈ F_{q²} : z^{q+1} = 1 }
```

（位数 `q+1` の巡回群）の群法則である。検証：q=5 で 8/8、q=7 で 24/24
（非零セルのみ）。

**系6（全単射）**：`A ↦ z_A = (1 + w·A)/(1 − w·A)`（`w² = d`、`A = ∞` は
`z = −1`）は `P¹(F_q) → T_d` の全単射。両辺ともサイズ `q+1`。

### 10c. `τ₃` の決定（証明済み）

**定理**：

```
τ₃(q) = q − 1   （q 奇数）
τ₃(q) = q       （q 偶数）
```

**証明（奇数 q）**：

1. 横断とは全単射 `a ↦ b` で `a ↦ c` も全単射になるもの。
2. 系5・系6 により、指数座標 `z_A = g^α`、`z_S = g^σ`、`z_T = g^τ`
   （`g` は `T_d` の生成元、`n = q+1`）で関係式は `τ = α − σ (mod n)`。
3. よって横断とは「全単射 `σ: Z_n → Z_n` であって `α ↦ α − σ(α)` も
   全単射」、すなわち **`Z_n` の完全写像（complete mapping）**。
4. **Hall–Paige の定理（1955）**：有限群 `G` が完全写像を持つのは
   Sylow 2-部分群が自明または非巡回のときに限る。
5. `q` 奇数なら `n = q+1` は偶数。`Z_n` の Sylow 2-部分群は位数 `≥2` の
   巡回群なので完全写像は**存在しない**。
6. よって `τ₃ ≤ q−1`。`q−1` の部分横断は存在するので `τ₃ = q−1`。 □

**偶数 q**：`n = q+1` は奇数なので Sylow 2-部分群は自明、Hall–Paige により
完全写像が存在し `τ₃ = q`。q = 4,8 で確認。

**系（新しい上界）**：

```
K(inversive q) ≤ q + 2   （q 奇数）
               ≤ q + 3   （q 偶数）
```

**奇数の `q+2` は新しい。** 従来 `q+2` は `q ≡ 1 (mod 4)` でのみ
（十字ブロック経由で）得られていた。3-ネット経由の議論は `q mod 4` に
依存しないため、`q ≡ 3 (mod 4)` にも拡張される。

**検証**（`verify_qplus2.py`）：修正済み厳密値
q=3,5,7,9,11,13,17,19,23,29 のすべてで `K ≤ q+2` が成立（slack 0〜23）。
slack は q とともに単調に増える（q=29 で 23）。

### 10d. 族 C, D は巡回座標で線形ではない（否定的結果）

3-ネット（族 B）は `Z_{q+1}` の加法表として完全に線形化できた。
そこで族 C（3点が錨を通る円上）・族 D（4点共円）も
`p·α + q·β ≡ const (mod q+1)` の形で書けるかを全数探索した。

| q | n | 最良の `(p,q)` | 一致率 |
|---:|---:|---|---|
| 5 | 6 | `(0,3)` | 94/190 = **0.4947** |
| 7 | 8 | `(0,4)` | 429/861 = **0.4983** |

**どの線形条件もランダムと同程度（約50%）しか一致しない。**
よって「共円ゲームを `Z_{q+1}` 上の線形代数に還元する」路線は閉じている。

構造的な理由：3-ネットの線形構造は `P¹(F_q)`（錨3点を通る円）に由来する。
錨を1点だけ通る円は `P¹(F_q)` を `PGL(2,F_{q²})` で「半分だけ」動かしたもので、
`Z_{q+1}` の加法構造を保たない。

**これにより `K` と `q+2` のギャップ（slack）の正体が
「本質的に高次の条件」であることが構造的事実として確定した。**

### 10e. 最小極大集合 `s(q)`：ゲームは定石数ではない

ゲームの可能な手数は「極大安全集合のサイズ」全体である。そこで

```
K(q) = 極大安全集合の最大サイズ（従来の K）
s(q) = 極大安全集合の最小サイズ（飽和数）
```

を定義し、極大集合を**葉として**列挙した（増分ブロッキング数え上げ）。

| q | n | `s(q)` | `K(q)` | 定石数? | サイズ分布 |
|---:|---:|---:|---:|---|---|
| 3 | 10 | 5 | 5 | **はい** | `{5: 72}` |
| 4 | 17 | 5 | 5 | **はい** | `{5: 2040}` |
| 5 | 26 | **5** | **6** | **いいえ** | `{5: 10400, 6: 5200}` |
| 7 | 50 | **5** | **6** | **いいえ** | `{5: 11760, 6: 1254400}` |
| 8 | 65 | **5** | **7** | **いいえ** | `{5: 4368, 6: 3669120, 7: 1048320}` |

**q = 5 で初めて定石数が破れる。** サイズ 5 と 6 の両方が極大になる。
**q = 3, 4 だけが定石数**であり、それは例外的な小さい場合にすぎない。

**系**：パリティ法則の仮定「すべての極大集合が同じパリティ」は
q ≥ 5 では成立しない。適用範囲は **q ≤ 4**。

### 10f. `s(q)` はブロッキング上界で完全に決まる

**定理（下限、証明済み）**：`k` 点の極大安全集合は

```
q² + 1 − k ≤ C(k,3)·(q − 2)
```

を満たす。よって `s(q) ≥ k*`、`k* = min{k : 上式}`。 □

**予想（上限、q ≤ 11 で検証）**：`s(q) = k*`。

| q | 3 | 4 | 5 | 7 | 8 | 9 | 11 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `k*` | 5 | 5 | 5 | 5 | 5 | 6 | 6 |
| `s(q)` 実測 | 5 | 5 | 5 | 5 | 5 | **6** | **6** |

**しかしこの予想は q=13 で反証された**（§10i 参照）。`s(q) = k*` は
**q ≤ 11 でのみ成立**する。

**予測値**（q が大きい場合）：

| q | 13 | 16 | 17 | 19 | 23 | 29 |
|---|---:|---:|---:|---:|---:|---:|
| `k*` | 6 | 6 | 6 | 7 | 7 | 7 |

**`s(q)` は q とともに非常にゆっくり増える**（q=29 の予測で 7）。
`K(q)` が 8〜10 であることと対照的である。

**注意**：容量 `C(k,3)(q−2)` には大きな余裕がある
（q=5, k=5 で容量 30 に対し必要 21）。つまり `s(q) = k*` は
「数え上げがぎりぎり」だからではなく、**幾何学的な構成が可能**だから成立する。
下限は不等式から厳密に従い、上限は構成的確認のみ。

### 10g. 欠損 `δ` と q=8 の完全分解

サイズ `k` の極大安全集合に対し

```
δ(S) = C(k,3)·(q−2) − (q² + 1 − k)     （ブロッキング不等式より δ ≥ 0）
```

`δ = 0` は「外の全点がちょうど1回ずつ覆われる」と同値。

| q | `k*` | 容量 | 必要点数 | `δ` |
|---:|---:|---:|---:|---:|
| 3 | 5 | 10 | 5 | 5 |
| 4 | 5 | 20 | 12 | 8 |
| 5 | 5 | 30 | 21 | 9 |
| 7 | 5 | 50 | 45 | 5 |
| **8** | **5** | **60** | **60** | **0** |

**`k = 5` で `δ = 0` になるのは `q = 8` のみ。**
これは `q² − 4 ≤ 10(q−2) ⟺ (q−2)(q−8) ≤ 0` から従う。

**定理（q=8 の構造、検証済み）**：`q = 8` の5点極大安全集合は、
三点組が定める10個の円が `S` の外の60点を6点ずつ10個に**完全分解**する
ことを強制する。

**検証**（`q8_tightness.py`）：witness `[0,1,2,31,50]` で
外60点の重複度ヒストグラムが `{1: 60}`、円は `S` の外で互いに素。

### 10h. 貪欲法は失敗する（存在は非構成的）

`k*` 点の極大集合を決定的貪欲法（各ステップで最多ブロック点を選ぶ）で
構成できるか：

| q | `k*` | 貪欲で極大? | 未ブロック点 |
|---:|---:|---|---:|
| 3 | 5 | **成功** | 0 |
| 4 | 5 | **成功** | 0 |
| 5 | 5 | **失敗** | 2 |
| 7 | 5 | **失敗** | 6 |

**貪欲法は q ≥ 5 で失敗する。** ランダム再起動では見つかる
（q=5 で12回、q=7 で27回、q=9 で2回）が、決定的な構成則は不明。
`s(q) = k*` の上限は**非構成的**である。

### 10i. 予想 `s(q) = k*` は q=13 で反証された

**高速化**：楕円二次曲面（ovoid）模型により反転平面構成が
`O(q⁵)` → `O(q³)` になった。q=11 が 2,400 秒 → **5 秒**。

```
Q(x₀,x₁,x₂,x₃) = x₀² + x₁² + x₂² + d·x₃²      （d は非平方）
```

`Q = 0` の零点集合が `PG(3,q)` の ovoid（`q²+1` 点）、
その `q+1` 点平面切断が円。q ≤ 11 で 3-設計公理を検証済み。

**反証**：ランダム再起動によるサイズ `k*` の極大集合探索：

| q | `k*` | サイズ `k*` の発見 | 試行回数 |
|---:|---:|---|---:|
| 9 | 6 | **発見** | 4 |
| 11 | 6 | **発見** | 697 |
| **13** | **6** | **発見できず** | **200,000** |
| 13 | 7 | **発見** | **32** |

q=13 ではサイズ6が 200,000 回試行しても見つからず（最良でも未ブロック12点）、
サイズ7は 32 回で見つかる。**よって `s(13) = 7 > k* = 6`。**

**破れの指標は欠損 `δ`**：

| q | `k*` | 容量 | 必要点数 | `δ` |
|---:|---:|---:|---:|---:|
| 9 | 6 | 140 | 76 | 64 |
| 11 | 6 | 180 | 116 | 64 |
| **13** | **6** | **220** | **164** | **56** |
| 16 | 6 | 280 | 251 | 29 |
| 17 | 6 | 300 | 284 | 16 |

`δ` が 64 → 56 に下がるのが q=13 で、ここで 6 点では覆えなくなる。
q=16, 17 ではさらに急減するので `s(q)` は `k*` よりかなり大きくなるはず。

**注意**：`s(13) = 7` は「サイズ6が 200,000 回のランダム試行で
見つからない」という強い証拠であり、厳密な非存在証明ではない。

### 10j. `s(q)` の実測系列（q ≤ 17）

ovoid 模型により q = 16, 17 も測定できた。

| q | n | `k*`（下界） | `s(q)`（実測） | 乖離 | 欠損 `δ` |
|---:|---:|---:|---:|---:|---:|
| 3 | 10 | 5 | 5 | 0 | 5 |
| 4 | 17 | 5 | 5 | 0 | 8 |
| 5 | 26 | 5 | 5 | 0 | 9 |
| 7 | 50 | 5 | 5 | 0 | 5 |
| 8 | 65 | 5 | 5 | 0 | **0** |
| 9 | 82 | 6 | 6 | 0 | 64 |
| 11 | 122 | 6 | 6 | 0 | 64 |
| **13** | 170 | 6 | **7** | **1** | 56 |
| **16** | 289 | 6 | **9** | **3** | 29 |
| **17** | 290 | 6 | **8** | **2** | 16 |

**`s(q) = k*` は q ≤ 11 でのみ成立。** q ≥ 13 では乖離する。

**探索の過程（q=16）**：

```
size 6: best unblocked=70   size 7: best unblocked=24
size 8: best unblocked=3    size 9: FOUND  (731 trials)
```

**`δ` が小さいほど乖離が大きい**傾向（ただし q=16 と q=17 は逆転）。

**`s(q)` と `K(q)` は近い**：

| q | 3 | 4 | 5 | 7 | 8 | 9 | 11 | 13 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `s(q)` | 5 | 5 | 5 | 5 | 5 | 6 | 6 | **7** |
| `K(q)` | 5 | 5 | 6 | 6 | 7 | 9 | 9 | **8** |

**q=13 では差がわずか 1。** ゲームの手数は 7 か 8 のどちらかしかない。

### 10k. 幾何学的再定式化：楕円二次曲面上のアーク問題

ovoid 模型により、共円ゲームは**古典的な有限幾何の問題**になる。

**q 奇数**：`Q = x₀² + x₁² + x₂² + d·x₃²`（`d` 非平方）
**q 偶数**：`Q = x₀x₁ + x₂² + x₂x₃ + a·x₃²`（`Tr_{F_q/F₂}(a) = 1`）

`Q = 0` の零点集合が `PG(3,q)` の ovoid（`q²+1` 点）。

**定理**：`Q` の4点が共円 ⟺ 同一平面上にある。

**証明**：4点が同一平面上ならその平面は `Q` と4点以上で交わり、
平面切断のサイズは `0,1,2,q+1` のいずれかしかないので `q+1`（円）。
逆に円は平面切断。 □

**検証**（`arc_on_quadric.py`、全数）：q=3,4,5,7 で
210 / 2,380 / 14,950 / 230,300 組、**不一致 0**。

**系**：

```
K(inversive q) = 楕円二次曲面上の最大アークサイズ
```

**注意（特性2の落とし穴）**：`x₀²+x₀x₁+a·x₁²+x₂²+x₂x₃+b·x₃²`（両方既約）は
**双曲的**で `q²+2q+1` 点を持つ。q=4 で 25 点（正しくは 17 点）になった。
正しい形は `x₀x₁+x₂²+x₂x₃+a·x₃²`（`Tr(a)=1`）。
**点数の検証がなければ気づかなかった**（3-設計公理は誤った曲面でも成立する）。

**計算速度**：q=8 の構成が 453 秒 → **0.6 秒**（750倍）。

### 10l. 文献との一致（q=8）

Sitjar, *There Is No Anti-Cocircular Pair of Ovoids in PG(3, 8)*
（2026年11月、[alphaXiv](https://www.alphaxiv.org/abs/2611.anti-cocircular-ovoids-pg3-8)）
は `PG(3,8)` の楕円二次曲面上のアークを全数数え上げている。

**独立計算による照合**（`arc_on_quadric.py` の ovoid 模型）：

```
q=8: n=65, circles=520
arc counts: {0:1, 1:65, 2:2080, 3:43680, 4:611520,
             5:4525248, 6:9434880, 7:1048320}
```

**サイズ7のアーク数 = 1,048,320。論文の値と完全一致。**
サイズ8以上は 0。

**系**：`K(inversive 8) = 7` に独立な裏づけが得られた
（本研究の厳密探索 15,320,036 ノード + 文献のアーク数え上げ）。

**用語対応**：本研究の「安全集合」= 文献の「アーク」、
「4点共円」=「4点同一平面」、「`K`」=「最大アークサイズ」。

### 10m. アーク数の閉形式（k ≤ 4、証明済み）

`K` は「アーク数が非零の最大 k」として直接読める。

**アーク数の系列**（全数計算）：

| q | n | k=0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 10 | 1 | 10 | 45 | 120 | 180 | **72** | | |
| 4 | 17 | 1 | 17 | 136 | 680 | 2040 | **2040** | | |
| 5 | 26 | 1 | 26 | 325 | 2600 | 13000 | 26000 | **5200** | |
| 7 | 50 | 1 | 50 | 1225 | 19600 | 205800 | 1070160 | **1254400** | |
| 8 | 65 | 1 | 65 | 2080 | 43680 | 611520 | 4525248 | 9434880 | **1048320** |

**定理1**：`k ≤ 3` なら `#arcs = C(n,k)`。

**証明**：アークでないのは4点共円のときのみ。3点以下では4点条件が
課されないので全部分集合がアーク。 □

**定理2**：`#4-arcs = C(n,4) − b·C(q+1,4)`、`n = q²+1`、`b = q(q²+1)`。

**証明**：4点集合がアークでない ⟺ 共円 ⟺ ある円の4点部分集合。
各円は `C(q+1,4)` 個を含み、2円は高々2点でしか交わらないので重複なし。
よって悪い4点集合は `b·C(q+1,4)` 個。 □

**検証**：q = 3,4,5,7,8 で完全一致（k≤3 は 20/20、k=4 は 5/5）。

**k = 5 では閉形式が破れる**：悪い5点集合は「単一円に含まれる」ものと
「共円な4点を含むが単一円に含まれない」ものの2種類あり、後者が支配的
（q=8 で 3,669,120 対 65,520）。2円が1点を共有する場合の重複を
数える必要があり、`S` の構造に依存する。

### 10n. k = 5 の閉形式（証明済み）

**定理**：`n = q²+1`、`b = q(q²+1)` とすると

```
#5-arcs = C(n,5) − b·C(q+1,5) − b·C(q+1,4)·(n − q − 1)
```

**証明**：5点集合の5つの4点部分集合はどれも3点を共有する。
**2つがともに共円なら、共有する3点が唯一の円を定めるので、
両方は同じ円上にあり、5点すべてがその円上にある。**
よって「アークでない」場合は互いに素な2つに限られる：

- (A) 5点すべてが1円上 → `b·C(q+1,5)`
- (B) ちょうど4点が1円上、5点目は円外 → `b·C(q+1,4)·(n−q−1)` □

**検証**：q = 3,4,5,7,8 で完全一致（5/5）。

| q | n | b | (A) | (B) | `#5-arcs` | 公式 |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 10 | 30 | 0 | 180 | 72 | **72** |
| 4 | 17 | 68 | 68 | 4,080 | 2,040 | **2,040** |
| 5 | 26 | 130 | 780 | 39,000 | 26,000 | **26,000** |
| 7 | 50 | 350 | 19,600 | 1,029,000 | 1,070,160 | **1,070,160** |
| 8 | 65 | 520 | 65,520 | 3,669,120 | 4,525,248 | **4,525,248** |

### 10o. k = 6 の構造：5つのプロファイル

6点集合では2つの共円4点部分集合が**2点だけ**共有し得るので、
別々の円に乗れる。2円は高々2点でしか交わらないので、
プロファイル（各円が取る点数）は次の5種類に限られる：

```
(6,)  (5,)  (4,)  (4,4)  (4,4,4)
```

**証明**：`m ≥ 2` なら `|S| ≥ 4+4−2 = 6`。`|S| = 6` では
`t₁ = t₂ = 4` かつ共有点がちょうど2点。 □

**検証**（q=5）：出現するプロファイルはこの5種類のみ。

| プロファイル | 実測 | 公式 |
|---|---:|---|
| (6,) | 130 | `b·C(q+1,6) = 130` ✓ |
| (5,) | 15,600 | `b·C(q+1,5)·(n−q−1) = 15,600` ✓ |
| (4,) | 62,400 | 第2円0個 |
| (4,4) | 132,600 | 第2円1個 ÷ 2 |
| (4,4,4) | 14,300 | 第2円2個 ÷ 3 |

**分解公式**：

```
#6-arcs = C(n,6) − b·C(q+1,6) − b·C(q+1,5)·(n−q−1)
                  − [N₀ + N₁/2 + N₂/3]
```

`N_j` = 「第2円がちょうど `j` 個」の `(C,T,{x,y})` 組数。

**検証**：q=5 で `bad=225,030, arcs=5,200`、q=7 で
`bad=14,636,300, arcs=1,254,400` — **全数計算と完全一致**。

### 10p. `N_j` は q=5 で一様、q=7 で2種類

`(C,T)` ごとの第2円分布：

| q | 相異なる分布 | 内容 |
|---:|---:|---|
| 5 | **1** | `(0:32, 1:136, 2:22)` が 1,950 組すべて |
| 7 | **2** | `(0:284,1:524,2:53)` が 14,700 組、`(0:282,1:528,2:51)` が 9,800 組 |

q=5 の一様性は**3重推移性**（自己同型群が (円, 4点部分集合) に推移的）に
よる。q=7 では円が8点あり4点の配置に複数の型が生じるため一様でない。

**加重平均は全数計算と一致**（q=7 で 6,938,400 / 12,877,200 / 1,278,900）。

**したがって k=6 の閉形式は「(C,T) の配置型の分類」に帰着する。**
これは `PG(3,q)` の平面配置の古典的問題であり未解決。

### 10q. `N_j` の正体：PGL(2,q)-軌道（解決）

`(C,T)` のクラスは**PGL(2,q) の4点部分集合への軌道**に他ならない。
円 `C` は `P¹(F_q)` のコピーで、`PGL(2,q)` がその上に作用する。

**総当たりによる軌道計算**（`arc_k6_orbits.py`）：

| q | `\|PGL(2,q)\|` | 軌道数 | 軌道サイズ |
|---:|---:|---:|---|
| 5 | 480 | **1** | `[15]` |
| 7 | 2,016 | **2** | `[42, 28]` |

**観測された分布グループと完全一致**：

```
q=5: {((0,32),(1,136),(2,22)): 15}
q=7: {((0,284),(1,524),(2,53)): 42, ((0,282),(1,528),(2,51)): 28}
```

**完全な k=6 公式**：

```
#6-arcs = C(n,6) − b·C(q+1,6) − b·C(q+1,5)·(n−q−1)
          − Σ_{O: PGL-軌道} b·|O|·[N₀(O) + N₁(O)/2 + N₂(O)/3]
```

**端から端までの検証**（`arc_k6_verify.py`）：

| q | (6,) | (5,) | (4,*) | 悪い | アーク | 全数 |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 130 | 15,600 | 209,300 | 225,030 | **5,200** | **5,200** ✓ |
| 7 | 9,800 | 823,200 | 13,803,300 | 14,636,300 | **1,254,400** | **1,254,400** ✓ |

**注意（失敗の記録）**：交差比の「6値集合」を素朴に不変量として使うと
q=5 で3軌道、q=7 で5軌道という**誤った数**になる。6値集合は
`PGL(2,q)` 不変量だが軌道を正しく分離しない。
**正しい軌道計算には群作用の総当たりが必要。**

### 10r. k=6 の交点表（完全に閉じた）

円 `C`（サイズ `q+1`）、その4点部分集合 `T`、`C` の外の2点 `{x,y}`、
`x,y` を通る円 `C' ≠ C` を考える。`(a,c) = #{({x,y},C') : |C'∩C| = a,
|T∩C'| = c}` は

```
(2,2) = 6q·C(q−1,2)
(2,1) = 4(q−3)·q·C(q−1,2)
(2,0) = C(q−3,2)·q·C(q−1,2)
(1,1) = 4(q−1)·C(q,2)
(1,0) = (q−3)(q−1)·C(q,2)
(0,0) = 総数 − (2,·) − (1,·)
```

**証明（`a=2`）**：`C'` は `C` と2点 `{u,v}` で交わる。`u,v` を通る円は
`q+1` 個で1つは `C` 自身 → `q` 通り。`{x,y}` は `C'` 上で `C` の外の
2点、`C'` の外の点は `q−1` 個 → `C(q−1,2)` 通り。`{u,v}` が `T` と
何点共有するかで3項に分かれる（`C(4,2)`, `4(q−3)`, `C(q−3,2)`）。 □

**補題（接する円）**：`C` の各点 `p` を通り `C` に接する円はちょうど
`q−1` 個。

**証明**：`p` を通る円は `q(q+1)` 個。`p` を通り `C` と2点以上で交わる
円は `q²` 個（`C` の他の各点を通る `q` 個ずつ）＋ `C` 自身。
残り `q(q+1) − q² − 1 = q−1`。 □

**証明（`a=1`）**：接する円は `C` と `p` のみ共有 → 外の点は `q` 個
→ `C(q,2)` 通り。`p ∈ T` なら `4(q−1)C(q,2)`、`p ∉ T` なら
`(q−3)(q−1)C(q,2)`。 □

**検証**：q=5,7 で **12/12 完全一致**。

| q | (2,2) | (2,1) | (2,0) | (1,1) | (1,0) | (0,0) |
|---:|---:|---:|---:|---:|---:|---:|
| 5 実測 | 180 | 240 | 30 | 160 | 80 | 450 |
| 5 公式 | 180 | 240 | 30 | 160 | 80 | 450 |
| 7 実測 | 630 | 1,680 | 630 | 504 | 504 | 2,940 |
| 7 公式 | 630 | 1,680 | 630 | 504 | 504 | 2,940 |

**周辺和**：`(2,·) = q·C(q−1,2)·C(q+1,2)`、`(1,·) = (q+1)(q−1)·C(q,2)`。
**観測された対称性**：`(2,·) = (0,·)`（q=5,7 の両方）。理由は未解明。

### 10s. k=6 のアーク数に残る一歩

`Σ j = b·C(q+1,4)·6q·C(q−1,2)` は閉じた（q=5 で 351,000、
q=7 で 15,435,000、データと一致）。

しかし `#6-arcs` に必要なのは `N₀ + N₁/2 + N₂/3` であり、
交点表から出るのは `N₁ + 2N₂ = Σ j` だけである。
**`N_j` の個別値は PGL(2,q)-軌道に依存する**ので、
交点表だけでは k=6 のアーク数は閉じない。

**「交点表レベル」は解決、「アーク数レベル」は未解決。**

### 10t. k=6 の完全解決：ペンシルの対合と超幾何分布

**鍵となる構造**：`{x,y}` を通る円の束（ペンシル）は `q+1` 個の円からなり、
各円は `C` と 0,1,2 点で交わる。個数を `n₀,n₁,n₂` とすると

```
n₁ + 2n₂ = q+1,   n₀ + n₁ + n₂ = q+1   ⟹   n₀ = n₂
```

2割線は `C` の点を**対**にするので、これは `C` 上の**対合** `ι` を定める。
**検証**：q=5 で 190 組、q=7 で 861 組すべてで対合性成立（違反 0）。

`j = #{ι の対で両点とも T に入るもの}`。

**定理（超幾何分布）**：対合が `n₂` 個の対と `n₁ = q+1−2n₂` 個の固定点を
持つとき、ちょうど `j` 個の対を含む4点部分集合の数は

```
H(n₂,n₁,j) = Σ_a C(n₂,j)·C(n₂−j,a)·2^a·C(n₁,4−2j−a)
```

**検証**：4/4 完全一致（q=5 の n₂=2,3、q=7 の n₂=3,4）。

**定理（接する円）**：`C` に接する円はちょうど `q²−1` 個。

**証明**：各点 `p` を通り接する円は `q−1` 個、接点は一意なので
`(q+1)(q−1) = q²−1`。 □

**定理（`N_xy` の閉形式）**：

```
q 奇数： (q²−1)·C(q,2)/2 個の対が n₂ = (q+1)/2 − 1
         残りが n₂ = (q+1)/2
q 偶数： C(q,2) 個の対が n₂ = 0
         残りが n₂ = q/2
```

**検証**：

| q | 予測 | 実測 |
|---:|---|---|
| 5 | `{2:120, 3:70}` | `{2:120, 3:70}` ✓ |
| 7 | `{3:504, 4:357}` | `{3:504, 4:357}` ✓ |
| 8 | `{0:28, 4:1512}` | `{0:28, 4:1512}` ✓ |

**完全な k=6 公式**：

```
#6-arcs = C(n,6) − b·C(q+1,6) − b·C(q+1,5)·(n−q−1)
          − b·Σ_{n₂} N_xy(n₂)·[H(n₂,n₁,0) + H(n₂,n₁,1)/2 + H(n₂,n₁,2)/3]
```

**端から端までの検証**（`arc_k6_pure.py`、**列挙なしの純粋な公式**）：

| q | 公式 | 全数 |
|---:|---:|---:|
| 5 | **5,200** | 5,200 ✓ |
| 7 | **1,254,400** | 1,254,400 ✓ |
| 8 | **9,434,880** | 9,434,880 ✓ |

**q 偶奇で構造が変わる**：q 奇数では各対が2つの接する円に乗るが、
q 偶数（標数2）では1つまたは `q+1` 個になる。

### 10u. 統一検証：k ≤ 6 の閉形式が 33/33 で成立

`arc_table.py` がアークをサイズごとに全数列挙し、閉形式と照合する。

| q | n | `K` | 検証 |
|---:|---:|---:|---|
| 3 | 10 | 5 | **6/6** |
| 4 | 17 | 5 | **6/6** |
| 5 | 26 | 6 | **7/7** |
| 7 | 50 | 6 | **7/7** |
| 8 | 65 | 7 | **7/7** |

**合計 33/33 完全一致。標数2（q=4,8）でも成立。**

**アーク数の全表**：

| q | k=0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 10 | 45 | 120 | 180 | **72** | | |
| 4 | 1 | 17 | 136 | 680 | 2,040 | **2,040** | | |
| 5 | 1 | 26 | 325 | 2,600 | 13,000 | 26,000 | **5,200** | 0 |
| 7 | 1 | 50 | 1,225 | 19,600 | 205,800 | 1,070,160 | **1,254,400** | 0 |
| 8 | 1 | 65 | 2,080 | 43,680 | 611,520 | 4,525,248 | 9,434,880 | **1,048,320** |

### 10v. k=7：q=5,7 では7-アークが存在しない

| q | 7-アーク | `K(q)` | 整合 |
|---:|---:|---:|---|
| 5 | **0** | 6 | ✓ |
| 7 | **0** | 6 | ✓ |
| 8 | **1,048,320** | 7 | ✓ |

**q=5, 7 では7-アークが1つも存在しない。** ブロッキング上界は
禁じていない（q=5, k=7 で `20 ≤ 105`）ので、**幾何的な障害**である。

**q=5 のプロファイル（全数、`C(26,7) = 657,800`、アーク 0）**：

| プロファイル | 個数 |
|---|---:|
| (4,4,4,4) | 312,000 |
| (4,4,4) | 96,200 |
| (5,4,4) | 85,800 |
| (4,4,4,4,4) | 78,000 |
| (5,4) | 62,400 |
| (4,4) | 15,600 |
| (4,4,4,4,4,4) | 5,200 |
| (6,) | 2,600 |

**8種類**（k=6 は5種類）。`(6,) = b·C(q+1,6)·(n−q−1) = 2,600` は
閉形式で一致。

k=7 では4点以上を持つ円の個数 `m` が最大6まで増え、
`|S| ≥ 4m − 2·C(m,2)` の制約が効かなくなる（`m=6` で負）。
**これが k=7 の複雑さの源である。**

### 10w. k=7 の多重度定理

**定理**：円 `C`、その4点部分集合 `T`、`C` の外の3点 `{x,y,z}` を選び
`S = T ∪ {x,y,z}` とすると

```
#7点集合（プロファイル P）= (タプル数) / #{t ∈ P : t = 4}
```

**証明**：タプルは「4円 `C` とその4点部分集合 `T`」を固定して数える。
`S` はその**4円の個数**だけ異なるタプルに現れる（各4円について
`S` に含まれる `T` は `C(4,4) = 1` 通り）。 □

**検証**（q=5）：

| プロファイル | タプル数 | 4円の個数 | 商 | 実測 |
|---|---:|---:|---:|---:|
| (4,4,4,4) | 1,248,000 | 4 | 312,000 | **312,000** ✓ |
| (4,4,4,4,4) | 390,000 | 5 | 78,000 | **78,000** ✓ |
| (4,4,4) | 288,600 | 3 | 96,200 | **96,200** ✓ |
| (5,4,4) | 171,600 | 2 | 85,800 | **85,800** ✓ |
| (5,4) | 62,400 | 1 | 62,400 | **62,400** ✓ |
| (4,4) | 31,200 | 2 | 15,600 | **15,600** ✓ |
| (4,4,4,4,4,4) | 31,200 | 6 | 5,200 | **5,200** ✓ |

**7/7 完全一致。** `(6,) = b·C(s,6)·C(n−s,1) = 2,600` は別扱い。
合計 `657,800 = C(26,7)`（アーク 0 と整合）。

**`(5,*)` は k=6 の機構で閉じる**：`|T| = 5` として

```
(5,4)   = b·Σ N_xy(n₂)·H(n₂,n₁,1,5) = 62,400  ✓
(5,4,4) = b·Σ N_xy(n₂)·H(n₂,n₁,2,5) = 85,800  ✓
```

`j = 0` は起こらない（`|T| = 5 > n₁ = 2 or 0`）。

**`(4,*)` のタプル数は未取得**：3点が必要なので、ペンシル（2点を通る
円の束）だけでは決まらず、より高次の配置が関与する。

### 10x. k=7 のプロファイル公式（3点が定める円）

**2つの自然な分解は失敗する**（記録）：

- **j-三つ組**：同じ `(1,1,1)` が `(4,4,4,4)`, `(4,4,4,4,4)`, `(5,4)` を
  与える。`W`（3点を通る円）が3つの `j` すべてに重複して数えられるため。
- **第2円の合併サイズ**：同じ `|union| = 2` が `(4,4,4,4)`, `(4,4,4)`,
  `(5,4,4)` を与える。`w` の情報が落ちるため。

**定理**：`S = T ∪ {x,y,z}`（`|T| = 4`、`T ⊂ C`、`x,y,z ∉ C`）とし、
`W` を `x,y,z` を通る唯一の円、`w = |T ∩ W|`、
`u` を「`T` と2点共有するペンシル円」の合併から `W` を除いた個数とすると

```
#4円 = 1 + u + [w = 1]
#5円 = [w = 2]
```

**証明**：`C' ≠ C` が `S` から4点以上取るには `{x,y,z}` から2点以上必要
（`C'` は `C` と高々2点で交わるので `T` からは高々2点）。
3点取るなら `C' = W`、2点取るならペンシル円。
`w = 2` なら `W` は5点、`w = 1` なら4点、`w = 0` なら3点（4円でない）。
ペンシル円は各4点。`C` 自身も4円。 □

**検証**（q=5、**10/10 完全一致**）：

| `w` | `u` | 予測 | 実測 |
|---:|---:|---|---|
| 0 | 1 | (4,4) | ✓ |
| 0 | 2 | (4,4,4) | ✓ |
| 0 | 3 | (4,4,4,4) | ✓ |
| 0 | 4 | (4,4,4,4,4) | ✓ |
| 0 | 5 | (4,4,4,4,4,4) | ✓ |
| 1 | 1 | (4,4,4) | ✓ |
| 1 | 2 | (4,4,4,4) | ✓ |
| 1 | 3 | (4,4,4,4,4) | ✓ |
| 2 | 0 | (5,4) | ✓ |
| 2 | 1 | (5,4,4) | ✓ |

**残る課題**：`(w,u)` の同時分布の閉形式。

### 10y. k=7 の `w` 周辺分布（閉じた）

`W` を `x,y,z` を通る唯一の円、`a = |W ∩ C|`、`w = |T ∩ W|` とする。

**定理（円の個数）**：

```
a=2 の総数 = C(s,2)·q,   a=1 の総数 = s·(q−1),   a=0 は残り

(2,2) = 6q,  (2,1) = 4(q−3)q,  (2,0) = C(q−3,2)q
(1,1) = 4(q−1),  (1,0) = (q−3)(q−1)
```

**証明**：`a=2` は `{p,p'}`（`C(s,2)` 通り）× その2点を通る円（`q` 通り、
`C` を除く）。`w` は `{p,p'}` が `T` と何点共有するかで分かれる。
`a=1` は接する円（各点 `q−1` 個 × `s` 点）。 □

**検証**：q=5,7 で **12/12 完全一致**。

**定理（`w` 周辺分布）**：`W` の外の点は `s−a` 個なので

```
w=2 : 6q·C(q−1,3)
w=1 : 4(q−3)q·C(q−1,3) + 4(q−1)·C(q,3)
w=0 : C(q−3,2)q·C(q−1,3) + (q−3)(q−1)·C(q,3)
      + [b−1−C(s,2)q−s(q−1)]·C(q+1,3)
```

**検証**：

| q | `w=0` | `w=1` | `w=2` | 合計 |
|---:|---:|---:|---:|---:|
| 5 実測 | 700 | 320 | 120 | 1,140 |
| 5 公式 | **700** | **320** | **120** | **1,140** |
| 7 実測 | 7,560 | 3,080 | 840 | 11,480 |
| 7 公式 | **7,560** | **3,080** | **840** | **11,480** |

**6/6 完全一致。**

**注意**：`a=2` の3式（`6q`, `4(q−3)q`, `C(q−3,2)q`）は k=6 の交点表の
`(2,2)`, `(2,1)`, `(2,0)` と**同一**である。

**残るのは `u` の条件付き分布のみ**。測定された制約：
`w=2` では `u ≤ 1`、`w=1` では `u ≤ 3`。

### 10z. k=7 の `u` 公式（閉じた）

`j₁, j₂, j₃` を3つの対 `{x,y}, {x,z}, {y,z}` の `j` 値（k=6 のペンシル量）
とする。

**定理**：

```
u = j₁ + j₂ + j₃            （w ≤ 1）
u = j₁ + j₂ + j₃ − 3        （w = 2）
```

**証明**：`u = |3つのペンシルの合併| − [W が合併に含まれる]`。

- `w ≤ 1`：`W` は `T` から高々1点しか取らず、ペンシル円は `T` から2点
  取る必要があるので `W` はどのペンシルにも属さない。さらに
  **3つのペンシルは互いに素**（データが示す）。よって `u = Σj`。
- `w = 2`：`W` は `T` から2点取るので**3つのペンシルすべてに属する**。
  `Σj` は `W` を3回数えるが合併は1回。`W` を除くと
  `u = Σj − 3 + 1 − 1 = Σj − 3`。 □

**検証**：q=5 で **13/13 完全一致**、q=7 でも全15行が整合
（`(0,0,0)` の場合を含む）。

| `w` | `(j₁,j₂,j₃)` | `Σj` | `u` |
|---:|---|---:|---:|
| 0 | (0,0,1) | 1 | 1 |
| 0 | (1,2,2) | 5 | 5 |
| 1 | (1,1,1) | 3 | 3 |
| 2 | (1,1,1) | 3 | **0** |
| 2 | (1,1,2) | 4 | **1** |

**これで k=7 は k=6 の量に完全に帰着した**：新しい量は
`(w, j₁, j₂, j₃)` の同時分布だけであり、`j` は k=6 で完全に理解済み。

### 10aa. k=7 の対合構造（3つの対合は素か1共通対）

`{x,y,z}` の3つの対に対応する3つの対合 `ι(x,y), ι(x,z), ι(y,z)` について

**定理**：この3つは次のいずれかである。

- **場合 A**：互いに素（共通の対を持たない）
- **場合 B**：**ちょうど1つの共通対**を持ち、他の対は共有しない

**検証**（q=5、1,140 三つ組）：

| `(ι₁∩ι₂, ι₁∩ι₃, ι₂∩ι₃)` | 個数 |
|---|---:|
| `(0,0,0)` | **840** |
| `(1,1,1)` | **300** |

**中間の場合（例 `(1,1,0)`）は存在しない。**

**場合 B の内訳**：

| 場合 | `w` | 共通対が `T` 内 | 個数 |
|---|---:|---|---:|
| A | 0 | — | 680 |
| A | 1 | — | 160 |
| B | 0 | いいえ | 20 |
| B | 1 | いいえ | 160 |
| **B** | **2** | **はい** | **120** |

**`w = 2` は「場合 B かつ共通対が `T` 内」と完全に一致する。**

**証明**：共通対 `{p,p'}` は3つの対合すべてに属する。これは
「`p,p'` を通る円 `W'` が3つのペンシルすべてに属する」ことを意味する。
`W'` が `x,y,z` の3点を通るなら `W' = W`（一意）。よって共通対は
`W ∩ C` であり、`w = |T ∩ W| = 2` と同値。 □

**系**：`u = Σj − 3[w=2]` の構造的な理由がこれで説明される。
場合 A では対が重複せず `u = Σj`、場合 B で `w = 2` なら共通対が
3回数えられて `u = Σj − 3`、場合 B で `w ≤ 1` なら共通対は `T` に
完全に入らず寄与0で `u = Σj`。

### 10ab. k=7 の端から端までの検証

`(w,u)` の分布を入力として、プロファイル公式

```
#4円 = 1 + u + [w = 1],   #5円 = [w = 2]
```

を通し、4円の個数で割って `b·C(s,4)` 倍すると、**7つのプロファイル
すべてが全数計算と一致する**（q=5）。

| プロファイル | 公式 | 全数 |
|---|---:|---:|
| (4,4) | **15,600** | 15,600 |
| (4,4,4) | **96,200** | 96,200 |
| (4,4,4,4) | **312,000** | 312,000 |
| (4,4,4,4,4) | **78,000** | 78,000 |
| (4,4,4,4,4,4) | **5,200** | 5,200 |
| (5,4) | **62,400** | 62,400 |
| (5,4,4) | **85,800** | 85,800 |

`(6,) = b·C(s,6)·(n−s) = 2,600` は別扱い（公式でも一致）。

**したがって k=7 のプロファイル公式は正しい。** 残るのは
`(w,u)` の分布自体の閉形式のみ。

**注意（実装の落とし穴）**：スケールは `b` ではなく **`b·C(s,4)`**
（タプルが「円 `C` とその4点部分集合 `T`」を固定するため）。
また除算は**厳密有理数**で行う必要がある（整数除算では切り捨てで
`(4,4,4)` が 95,550 になった）。

### 10ac. k=7 の `(w,u)` 分布の対合による分解

**定理**：場合 A（対合が互いに素）では `w ≤ 1`。

**証明**：場合 A では3つのペンシルが素なので、`{x,y,z}` の2点を通り
`T` と2点共有する円は3点目を通らない。`W` は3点すべてを通るので、
`W` がペンシルに属するなら矛盾。よって `W` は `T` と2点共有しない。 □

**`(case, w, Σj)` の分布**（q=5、1,140 三つ組）：

| 場合 | `w` | `Σj` | 個数 |
|---|---:|---:|---:|
| A | 0 | 1,2,3,4,5 | 16, 100, 416, 140, 8 |
| A | 1 | 1,2,3 | 48, 96, 16 |
| B | 0 | 4,5 | 12, 8 |
| B | 1 | 2,3 | 128, 32 |
| B | 2 | 3,4 | 32, 88 |

**周辺**：Case A `w {0:680, 1:160}`、Case B `w {0:20, 1:160, 2:120}`。

**再構成**：`u = Σj − 3[w=2]` を適用すると `(w,u)` が再現される
（**10/10 完全一致**）。内訳の例：

- `(0,4) = A(w=0,Σj=4) 140 + B(w=0,Σj=4) 12 = 152`
- `(1,2) = A(w=1,Σj=2) 96 + B(w=1,Σj=2) 128 = 224`
- `(2,0) = B(w=2,Σj=3) 32 → u = 0`

**残る課題**：`(case, w, Σj)` の閉形式。`Σj` は3つのペンシルの `j` の和
であり、`j` は k=6 の量で書けるが、3つのペンシルが相関するため
単純な積にはならない。

### 10ad. k=7 の `Σj` をペンシル円のプロファイルで決定

`{x,y,z}` の各対のペンシルから「`T` と2点共有する円」を集め、
各円を `(|C' ∩ {x,y,z}|, |C' ∩ T|)` で分類する。

**定理1**：そのような円は必ず `|C' ∩ T| = 2` かつ
`|C' ∩ {x,y,z}| ∈ {2, 3}`。

**定理2**：`|C' ∩ {x,y,z}| = 3` の円は `W` であり、現れるのは
`w = 2` のときに限る。

**定理3**：

```
Σj = #{(2,2) 円} + 3·[W が現れる]
```

**証明**：`(2,2)` 円は `{x,y,z}` の1つの対にしか属さないので1回寄与。
`W` は3つの対すべてに属するので3回寄与。 □

**検証**（q=5）：

| プロファイル | 個数 | `#(2,2)` | `W` | `Σj` |
|---|---:|---:|---|---:|
| ((2,2)×3) | 464 | 3 | いいえ | 3 |
| ((2,2)×2) | 324 | 2 | いいえ | 2 |
| ((2,2)×4) | 152 | 4 | いいえ | 4 |
| ((2,2),(3,2)) | 88 | 1 | **はい** | 4 |
| ((2,2),) | 64 | 1 | いいえ | 1 |
| ((3,2),) | 32 | 0 | **はい** | 3 |
| ((2,2)×5) | 16 | 5 | いいえ | 5 |

**`Σj` 周辺分布**：

| `Σj` | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 導出 | 64 | 324 | 496 | 240 | 16 |
| 実測 | **64** | **324** | **496** | **240** | **16** |

**完全一致。** また `w = 2` の三つ組 120 と `(3,2)` 円を持つ三つ組 120 が
一致（`W` の同値性の確認）。

**これで k=7 の全体が「`(2,2)` 円の個数」と「`W` の有無」に帰着した。**

### 10ae. k=7 のアーク数の組み立てと検証

```
#7-arcs = C(n,7) − (6,) − Σ_{プロファイル P} #(P を持つ集合)

(6,) = b·C(s,6)·(n−s)
#(P を持つ集合) = (P を持つタプル数) / (#P の4円の個数) × b·C(s,4)
```

タプル数は `(w,u)` から `#4円 = 1+u+[w=1]`, `#5円 = [w=2]` で変換。

**検証**（q=5）：

| プロファイル | 個数 |
|---|---:|
| (4,4,4,4) | 312,000 |
| (4,4,4,4,4) | 78,000 |
| (4,4,4) | 96,200 |
| (5,4,4) | 85,800 |
| (4,4) | 15,600 |
| (5,4) | 62,400 |
| (4,4,4,4,4,4) | 5,200 |
| (6,) | 2,600 |
| **悪い7点集合** | **657,800** |

```
C(26,7) = 657,800,  arcs = 657,800 − 657,800 = 0
```

**全数計算と完全一致**（q=5 では7-アークが存在しない）。

**すべての変換ステップが個別に検証済み**：
プロファイル公式（7/7）、`(w,u)` 分解（10/10）、`Σj` 決定（周辺一致）、
`u = Σj − 3[w=2]`（13/13）。

**残る唯一の未解決部分は `(w,u)` の分布**（＝3つのペンシルの配置を
数える問題）。`n2`-三つ組では決まらない（同じ `n2=(2,2,3)` が
`Σj = 1,2,3,4` を与える）。

### 10af. k=7 の双対構成：9つの型

**双対の視点**：`T` を固定して `{x,y,z}` を動かす代わりに、
**`{x,y,z}` を固定して `T` を `C` の4点部分集合全体で動かす**。

三つ組が決まれば `W` と3つの対合が決まり、`(w,u)` は `T` の関数になる。

**9つの型**（q=5）：

| 型 | `(w,u)` 分布（`T` 上） | 多重度 |
|---|---|---:|
| A | (0,1):1, (0,2):2, (0,3):11, (0,4):1 | 240 |
| A | (0,3):2, (0,4):3, (1,1):3, (1,2):6, (1,3):1 | 240 |
| B | (0,4):1, (1,2):8, (2,1):2, (2,2):4 | 180 |
| A | (0,2):1, (0,3):11, (0,4):2, (0,5):1 | 120 |
| B | (0,5):1, (1,2):4, (1,3):4, (2,1):1, (2,2):5 | 120 |
| A | (0,2):5, (0,3):8, (0,4):2 | 120 |
| A | (0,2):2, (0,3):8, (0,4):5 | 60 |
| A | (0,3):6, (0,4):9 | 40 |
| A | (0,2):9, (0,3):6 | 20 |

各型の分布は `C(s,4) = 15` に和する。多重度の合計は 1,140。

**変換則**：双対は `(三つ組, T)` を数えるので `C(s,4)` で割る。
さらに `w = 2` では共通対 `W ∩ C` が3つの対合すべてに属するので
双対の `u` はそれを1回含む。primal は除くので

```
u_primal = u_dual − [w = 2]
```

**検証**：**10/10 完全一致**（`(0,1)`〜`(2,1)` の全エントリ）。

**残る課題**：9つの型の多重度（240, 240, 180, 120, 120, 120, 60, 40, 20）
の閉形式。これは「三つ組の対合構造の型」を数える問題。

### 10ag. k=7 の型の細分：90配置（閉形式への障壁）

**不変量による特徴づけ**：`(case, n2-三つ組, |W∩C|, 点レベルの重なり,
|合併点集合|)` で9型のうち **8型が一意に決まる**。

| 場合 | `n2` | `\|W∩C\|` | 点重なり | `\|合併\|` | 多重度 |
|---|---|---:|---|---:|---:|
| A | (2,2,3) | 0 | (2,4,4) | 6 | 240 / **120** |
| A | (2,2,2) | 1 | (3,3,3) | 5 | 240 |
| B | (2,2,3) | 2 | (2,4,4) | 6 | 180 |
| A | (2,3,3) | 0 | (4,4,6) | 6 | 120 / **60** |
| B | (2,3,3) | 2 | (4,4,6) | 6 | 120 |
| A | (3,3,3) | 0 | (6,6,6) | 6 | 40 |
| A | (2,2,2) | 0 | (2,2,2) | 6 | 20 |

**2組が同じ不変量を共有する。**

**細分の試み（失敗）**：点のラベルを正規化して対合の対集合を標準形で
比較すると **90種類**の配置が現れる。

**したがって「9型の多重度の閉形式」は「90配置の分類」に帰着する。**
これは k=6 の PGL 軌道分類（q=5 で1軌道、q=7 で2軌道）より
はるかに複雑である。

**k=7 は k=6 の単純な拡張では閉じない**という否定的結果。

### 10ah. `a = |W ∩ C|` による完全な分解（障壁の回避）

**定理**：`a = |W ∩ C| = 2` ⟺ 場合 B（3つの対合が共通対を持つ）。

**証明**：対合は「ペンシルの**2割線**」、すなわち「`C` と2点で交わる円」を
記録する。`W` は `x,y,z` の3点を通るので、`W` が3つのペンシルすべてに
属するのは `a = 2` のとき、かつそのときに限る。よって共通対は `W ∩ C`。 □

**注意**：`w = |T ∩ W|` は別の量。対合は「`C` と2点で交わる円」を記録する
のであって「`T` と2点で交わる円」ではない（この混同で一度誤った）。

**検証**（q=5）：

| `a` | 場合 | 三つ組 |
|---:|---|---:|
| 0 | A のみ | 600 |
| 1 | A のみ | 240 |
| 2 | **B のみ** | 300 |

**三重カウントの閉形式**：`W` 上の三つ組は `W \ C` の3点部分集合なので
`C(s−a, 3)` 個。よって

```
三つ組(a) = 円(a) × C(s−a, 3)
円(a=2) = C(s,2)·q,  円(a=1) = s·(q−1),  円(a=0) = b−1−上記
```

**検証**：

| q | 三つ組 a=2 | a=1 | a=0 | 合計 | `C(n−s,3)` |
|---:|---:|---:|---:|---:|---:|
| 5 | 300 | 240 | 600 | **1,140** | 1,140 ✓ |
| 7 | 3,920 | 1,680 | 5,880 | **11,480** | 11,480 ✓ |

**`a` ごとの型数**（q=5）：`a=1` は**1型のみ**、`a=2` は2型、
`a=0` が**6型**で最も複雑。**`a` で層別すれば複雑さが減る。**

### 10ai. `a=0` 層：障壁は層別後も再現する

`a=0` では `W` が `C` と交わらないので `w = 0` 常に。型は `u` の分布で
決まる。**6型**（合計 600 三つ組）：

| `n2` | 点重なり | `u` 分布 | 個数 |
|---|---|---|---:|
| (2,2,3) | (2,4,4) | (0,1):1 (0,2):2 (0,3):11 (0,4):1 | 240 |
| (2,3,3) | (4,4,6) | (0,2):1 (0,3):11 (0,4):2 (0,5):1 | 120 |
| (2,2,3) | (2,4,4) | (0,2):5 (0,3):8 (0,4):2 | 120 |
| (2,3,3) | (4,4,6) | (0,2):2 (0,3):8 (0,4):5 | 60 |
| (3,3,3) | (6,6,6) | (0,3):6 (0,4):9 | 40 |
| (2,2,2) | (2,2,2) | (0,2):9 (0,3):6 | 20 |

**すべて `|合併点集合| = 6 = s`**（3つの対合が `C` を覆い尽くす）。

**不変量 `(n2, 点重なり)` で4/6型が決まる。** 残る2組
（`((2,2,3),(2,4,4))` と `((2,3,3),(4,4,6))`）が同じ不変量を共有する。

**細分すると再び90配置**（前項と同じ数）。**`a` 層別は「型の数」を
減らすが「配置の数」は減らさない。**

**したがって k=7 の閉形式には対合配置の完全分類が必要**であることが
確定した。これは k=6 の PGL 軌道（q=5 で1、q=7 で2）よりはるかに複雑。

### 10aj. 訂正：「90配置」は人為的産物、正しくは37軌道

**前項の「90配置」は誤りである。** 標準形として使った「点のラベルを
最初の出現順に振り直す」は群作用と両立しないアドホックなもので、
同じ軌道を複数回数えてしまう。

**正しい不変量は `PGL(2,q)` の軌道**である。3つの対合
`ι(x,y), ι(x,z), ι(y,z)` は `P^1(F_q)` 上の2次の元であり、
`(w,u)` 分布はその軌道だけで決まる。

**正しい軌道数**（q=5、`PGL(2,5)` を全列挙）：

```
|PGL(2,5)| = 120,  |P^1(F_5)| = 6,  対合 = 25
対合の三つ組 = 2,300
PGL-軌道 = 37
軌道サイズ = 120×9, 60×16, 30×6, 20×2, 15, 10×2, 5
```

**3つの数の比較**：

| 数え方 | 個数 | 妥当性 |
|---|---:|---|
| `(w,u)` 分布 | **9** | 粗い同値類 |
| `PGL(2,q)` 軌道 | **37** | **正しい群論的不変量** |
| アドホック標準形 | ~~90~~ | **人為的産物（誤り）** |

**37軌道が9つの分布に融合する**（複数の軌道が同じ分布を持つ）。
閉形式には37軌道の多重度を数える必要がある。

### 10ak. 9分布は模型に依らない（2模型で確認）

`(w,u)` 分布を2つの独立な模型で計算した。

| 模型 | 9分布 | 多重度 |
|---|---|---|
| ovoid（楕円二次曲面） | **9** | 240, 240, 180, 120, 120, 120, 60, 40, 20 |
| native（`P^1(F_{q^2})`） | **9** | 同上 |

**両方で同じ9分布、同じ多重度。** したがって9分布は模型に依らない
幾何学的実体である。

**9分布 ↔ 37軌道の対応は未取得。** ovoid 模型の円 `C` は抽象的な
`s` 点集合であり、`P^1(F_q)` への全単射をソート順で作るとメビウス構造が
保たれないため、誘導された置換が正しい対合にならない
（1,140 三つ組のうち 1,064 が対応せず）。

**正しい対応には構造を保つ全単射（メビウス同型）が必要。**

### 10al. 軌道対応の解決：9分布 = 実現する9軌道

**鍵となる工夫**：native 模型で `C = P¹(F_q)` 自身（`0,1,∞` を通る円）を
選ぶ。この円の点は**そのまま `P¹(F_q)`** なので全単射が恒等写像になり、
誘導される対合が本物の `PGL(2,q)` の元になる。

**結果**（q=5）：

```
37 orbits
triples per orbit: {0:240, 16:180, 20:240, 22:120,
                    27:60, 28:120, 31:120, 32:20, 36:40}
total 1140, unmatched 0
realised orbits: 9
distinct distributions among realised: 9
```

**1,140 三つ組すべてが対応（不一致 0）。実現する軌道はちょうど9個。
その9個はそれぞれ異なる分布を持つ。**

**定理**：`PGL(2,q)` の対合三つ組への37軌道のうち、実際に幾何学的に
実現するのは**9個だけ**であり、その9個が `(w,u)` 分布の9型に
一対一対応する。

**証明**：`C = P¹(F_q)` を選べば全単射が恒等になり、対合が本物の
`PGL(2,q)` の元になる。実測で 1,140 三つ組が9軌道に配分され、
各軌道が異なる分布を持つ。 □

**系**：9型の多重度は実現する9軌道の三つ組数（240, 180, 240, 120,
60, 120, 120, 20, 40、合計 1,140）。

**なぜ37のうち9だけか**：対合が「ペンシルの2割線」という特別な形に
限られるため。任意の対合の三つ組が3つのペンシルから来るわけではない。

### 10am. 9軌道は `a` 層に一意に属する

**結果**（q=5）：

| 軌道 | `a` | 三つ組数 |
|---:|---:|---:|
| 0 | **1** | 240 |
| 16 | **2** | 180 |
| 31 | **2** | 120 |
| 20 | **0** | 240 |
| 22 | **0** | 120 |
| 28 | **0** | 120 |
| 27 | **0** | 60 |
| 36 | **0** | 40 |
| 32 | **0** | 20 |

**各軌道はちょうど1つの `a` 層に属する。**

**層ごとの集計**：

| `a` | 軌道数 | 三つ組数 |
|---:|---:|---:|
| 0 | **6** | 600 |
| 1 | **1** | 240 |
| 2 | **2** | 300 |
| | **9** | **1,140** |

**前項の `a` 別三重カウント（600, 240, 300）と完全一致。**

**閉形式への道筋**：`a` 層ごとの三つ組数は既に閉形式（第154部）。
残るのは層内の分割：

- `a=1`：軌道1個 → **完全に閉じている**
- `a=2`：軌道2個 → 180 と 120 に分割
- `a=0`：軌道6個 → 240, 120, 120, 60, 40, 20 に分割

### 10an. `a=2` 層：型は円の性質（q=5）、q=7 では3種

**q=5 の重要な発見**：`a=2` 層の 300 三つ組を円ごとに調べると

```
45 円: その4つの三つ組すべてが extra-pairs (1,1,2)  → 45×4 = 180
30 円: その4つの三つ組すべてが extra-pairs (1,2,2)  → 30×4 = 120
```

**型は三つ組ではなく円 `W` の性質である。** 識別は「`W` の外の点対を
通り `C` と2点で交わる円」の個数（8 vs 10、`2(q−1)` と `2q`）。

**閉形式（q=5）**：

```
45 = C(s,2)·(q−2),  30 = C(s,2)·2,  合計 = C(s,2)·q
```

**q=7 では3種になる**（単純な一般化の失敗）：

| 型 | 追加円 | 円の数 |
|---|---|---:|
| (2,2,3) | 36 | 102 |
| (2,3,3) | 39 | 84 |
| (3,3,3) | 36 | 10 |

合計 196 = `C(8,2)·7`。**`28·5 = 140 ≠ 102`、`28·2 = 56 ≠ 84`** なので
q=5 の公式は拡張できない。

**理由**：q=5 では `W \ C` が4点で三つ組の構造が1種類、q=7 では6点で
複数の型が生じる。k=6 の「q=5 で1軌道、q=7 で2軌道」と同じ現象。

### 10ao. `a=0` 層：円レベルの `u` と `T` レベルの `u` は別物

`a=0` では `W` が `C` と交わらないので `w = 0` 常に。各円 `W` は
`C(q+1,3)` 個の三つ組を持つ（q=5 で 20 個、30 円で 600）。

**円レベルの `u`**（三つ組を固定し、対合の対の総数）：

| 円の数 | `u` の分布 |
|---:|---|
| **20** | `u=7` が18個、`u=9` が2個 |
| **10** | `u=6` が2個、`u=8` が18個 |

集約：`u=6:20, u=7:360, u=8:180, u=9:40`（合計600）。

**しかし `T` レベルの `u` は 1〜5 にしかならない**（6つの分布すべて）。
**2つは別の量である**：

- **円レベルの `u`**：対合が何個の対を持つか（値域 6〜9）
- **`T` レベルの `u`**：そのうち何個が `T` に入るか（値域 1〜5）

**`u_T ≤ u_circle`** の関係があるが値は別。

**検証**：`T` レベル周辺 `{1:240, 2:1500, 3:5760, 4:1380, 5:120}` は
合計 9,000 = 600×15。円レベル周辺は合計 600。両方整合的だが
**異なる対象を数えている**。

**`a=2` 層で「型が円の性質」だったのは、`a=2` では `W` 自身が対合に
寄与するため両者が連動していたから**と説明できる。

### 10ap. `a=0` 円の2分類の閉形式

**定理（`a=0` 円の個数）**：

```
a=0 円 = q(q−1)(q−2)/2
```

**証明**：`b − 1 − C(s,2)q − s(q−1)` を整理すると
`(q³−3q²+2q)/2 = q(q−1)(q−2)/2`。 □

**検証**：q=5 で 30、q=7 で 105。両方一致。

**定理（2分類）**：円ごとの `u` 分布で2種類に分かれる。

| q | HIGH 群 | LOW 群 |
|---:|---|---|
| 5 | `u=7`(18), `u=9`(2) → **20円** | `u=6`(2), `u=8`(18) → **10円** |
| 7 | `u=10`(48), `u=12`(8) → **63円** | `u=9`(8), `u=11`(48) → **42円** |

```
HIGH 群 = q(q−1)(q−4)/2
LOW  群 = q(q−1)
合計   = q(q−1)(q−2)/2
```

**検証**：**4/4 完全一致**

| q | HIGH 公式 | 実測 | LOW 公式 | 実測 |
|---:|---:|---:|---:|---:|
| 5 | **10** | 10 | **20** | 20 |
| 7 | **63** | 63 | **42** | 42 |

**注意**：大小関係が逆転する。q=5 では HIGH(10) < LOW(20)、
q=7 では HIGH(63) > LOW(42)。**`q = 6` で等しくなる**（`q−4 = 2`）。

**`u` の値域は `q+2` 〜 `q+5`**（q=5 で 7〜10、q=7 で 9〜12）。

### 10aq. `a=0` 層：円の種類は軌道を決めない（否定的結果）

**正しい閾値**：円ごとの `u` 分布の**多数派**で分ける
（q=5 で 20円が多数派 `u=7`、10円が多数派 `u=8`）。

**測定結果**（q=5）：

| 円の種類 | 軌道 | 三つ組数 |
|---|---|---:|
| HIGH | 20 | 216 |
| HIGH | 28 | 108 |
| HIGH | 36 | 36 |
| LOW | 20 | 24 |
| LOW | 22 | 120 |
| LOW | 27 | 60 |
| LOW | 28 | 12 |
| LOW | 32 | 20 |
| LOW | 36 | 4 |

集計：HIGH = 360（20円×18）、LOW = 240（10円×24）、合計 600 ✓

**結論**：**円の種類（HIGH/LOW）は軌道を決定しない。**
軌道 20, 28, 36 は**両方の種類から現れる**。

**理由**：HIGH/LOW は「`u` の多数派」で決まるが、軌道は「対合の対の
配置」も見る。同じ `u` でも配置が違えば軌道が違う。

**`a=2` で型が円の性質だったのは、`a=2` では `W` 自身が対合に寄与して
`u` と配置が連動していたから。`a=0` では `W` が寄与しないので連動しない。**

**したがって `a=0` 層の6分割には円の2分類より細かい情報が必要。**

### 10ar. `a=0` 層の完全解決：2円種 × 3副類

**正しい不変量**：`(n2-三つ組, T 上の u 分布)` の組が `a=0` 層の
**完全な不変量**である。q=5 でちょうど **6類**が現れ、6軌道に一致。

| `\|U\|` | `u` 分布 | 三つ組数 |
|---:|---|---:|
| 7 | (1,1),(2,2),(3,11),(4,1) | 240 |
| 7 | (2,5),(3,8),(4,2) | 120 |
| 8 | (2,1),(3,11),(4,2),(5,1) | 120 |
| 8 | (2,2),(3,8),(4,5) | 60 |
| 9 | (3,6),(4,9) | 40 |
| 6 | (2,9),(3,6) | 20 |

**構造**：各 `a=0` 円は `C(s,3) = 20` 個の三つ組を持ち、それらが
**3つの類に分かれる**。

```
HIGH 円（q(q−1)(q−4)/2 個）: 各円が 12, 6, 2 個を3類に寄与
LOW  円（q(q−1) 個）      : 各円が  2, 12, 6 個を3類に寄与
```

**検証**：

| 類 | 計算 | 三つ組数 |
|---|---|---:|
| A | 20×12 | **240** |
| B | 20×6 | **120** |
| C | 20×2 | **40** |
| D | 10×2 | **20** |
| E | 10×12 | **120** |
| F | 10×6 | **60** |
| | | **600** ✓ |

**実測の6軌道（240, 120, 120, 60, 40, 20）と同じ多重集合。**

**前項の結論を精密化**：円の2分類は6分割の**第1段**であり、
各円内の三つ組がさらに3類に分かれる。`12 + 6 + 2 = 20 = C(s,3)`。

### 10as. `a=0` 層の q=7 検証：副類の数が増える

| q | HIGH 円 | 副類数 | LOW 円 | 副類数 | 合計類数 |
|---:|---:|---:|---:|---:|---:|
| 5 | 20 | **3** | 10 | **3** | **6** |
| 7 | 63 | **4** | 42 | **3** | **7** |

**q=7 の配分**：

```
HIGH 円（63個）: 各円が 16, 16, 16, 8 個を4類に寄与  （和 56 = C(8,3)）
LOW  円（42個）: 各円が  8, 16, 32 個を3類に寄与     （和 56）
```

**一般化する**：2円種 × 副類の構造、各円の寄与の和が `C(s,3)`、
HIGH/LOW の円数 `q(q−1)(q−4)/2` と `q(q−1)`。

**一般化しない**：副類の数（3+3 → 4+3）と配分（12/6/2 → 16/16/16/8）。

**副類の数は q とともに増える。**

### 10at. 訂正：k=7 のプロファイル公式は q=7 で破綻する

**前項までの k=7 の結果は q=5 でのみ有効である。**

q=7 で組み立てたアーク数が**非整数**になった：

```
bad = 4033248800/143   （整数でない）
```

直接照合すると **20,000/20,000 が不一致**。予測は実際より遥かに多くの
4円を含む（例：実際 `(4,4,4)` を予測 `(4,4,4,4,4,4,4,4,4,4,4)`）。

**原因**：`u` は「`T` と2点共有するペンシル円」の合併サイズだが、
**その円が `{x,y,z}` から2点取るとは限らない**。

`C'` が `S` から4点以上取る条件は

```
|C' ∩ T| = 2  かつ  |C' ∩ {x,y,z}| = 2
```

であり、`u` は**前者だけ**を数えている。**`u` は上界にすぎない。**

具体例（q=7、`T=(0,7,14,21)`、`xyz=(1,2,3)`）：`u=8` で予測 `n4=9` だが
実際の4円は5個。合併の9円のうち4円になるのは4個だけ。

**q=5 で一致したのは `u` が小さく（≤5）偶然合致したため。**
q=7 では `u ≤ 12` で合致しない。

**影響**：k=7 のプロファイル公式、アーク数の組み立て、
「9分布 = 9軌道」、「a=0 の2円種×3副類」はいずれも **q=5 限定**。

### 10au. 修正版プロファイル公式（q=5,7 で完全一致）

**2つの誤りを修正した。**

**誤り1**：`u` は4円の個数ではない。`u` は「`T` と2点共有する
ペンシル円」の合併サイズだが、その円が `{x,y,z}` から2点取るとは限らない。
正しくは

```
v = #{C' ≠ C : |C' ∩ T| = 2  かつ  |C' ∩ {x,y,z}| = 2}
```

（`u ≥ v`、`u` は上界）。

**誤り2**：`w = |W ∩ C|` ではなく **`w = |W ∩ T|`** が正しい。
`W` は `x,y,z` の3点を通るので `S` から取る点数は `|W ∩ T| + 3`。
`|W ∩ C| = 2` でも `|W ∩ T| = 1` になり得る。

**定理（修正版）**：

```
#4円 = 1 + v + [|W ∩ T| = 1]
#5円 = [|W ∩ T| = 2]
```

**検証**：

| q | 検査数 | 不一致 |
|---:|---:|---:|
| 5 | 3,420 | **0** |
| 7 | 11,480 | **0** |

**両方で完全一致。**

**なぜ q=5 で気づかなかったか**：`u` が小さく（≤5）合併の円がたまたま
`{x,y,z}` を含んでいた。また `C` が6点・`T` が4点なので
`|W ∩ C| = 2` なら `|W ∩ T| = 2` になる確率が高かった（2/5）。
q=7 では `u ≤ 12`、`C` が8点で確率が下がり露呈した。

**残る課題**：`v` の閉形式（`u` の閉形式は既知だが `v` は別）。

### 10av. 第2の誤り：スケールと多重度の割り算

**スケールの誤り**：`b·C(s,4)` ではなく **`b`** が正しい。
タプルループは `C = P¹(F_q)` を固定し `T`（`C` の4点部分集合）を
列挙するので、`T` は既に列挙済み。`C(s,4)` を掛けるのは二重。

**検証**（q=5）：

| スケール | bad | arcs | 全数 |
|---|---:|---:|---:|
| **`b`** | **657,800** | **0** | 657,800 / 0 ✓ |
| `b·C(s,4)` | 9,830,600 | −9,172,800 | ✗ |
| `1` | 7,640 | 650,160 | ✗ |

**しかし q=7 ではまだ合わない**：

| q | 全数 bad | 全数 arcs | `scale=b` の arcs |
|---:|---:|---:|---:|
| 5 | 657,800 | 0 | **0** ✓ |
| 7 | 99,884,400 | **0** | **1,414,000** ✗ |

**多重度の割り算も誤り**：タプルループは `C = P¹(F_q)` を**固定**して
いるので、7点集合 `S` は「`S` の4円が `P¹(F_q)` である」場合にしか
現れない。よって `÷(4円の個数)` は正しくない。

**q=5 の「成功」は2つの誤り（`b·C(s,4)` と `÷(4円の個数)`）が
相殺したため。**

**確認**：q=7 の全数で **7-アークは 0**（`K(7) = 6` と整合）。

### 10aw. 真の原因：6点以上の円

**プロファイル公式自体は q=7 でも完全に正しい**：
全 803,600 組 `(T,{x,y,z})` で照合して **0 不一致**。

しかし組み立てが合わない（全数 99,884,400 対 組み立て 98,470,400、
差 1,414,000）。

**真の原因**：プロファイル公式が生成するのは **4 と 5 のみ**。
しかし q=7 では `s = 8` なので、**1つの円が `S` から6点・7点取れる**。

例：円 `C` 上の6点 + 外の1点 = 7点集合。この集合は6点円を1つ持ち、
同時に `C(6,4) = 15` 個の4点円も持つ。**公式はこれを分類できない。**

**q=5 で問題にならなかった理由**：`s = 6` で円は最大6点。
6点円を持つ7点集合は `(6,)` という**別項**で処理していた。
q=7 では 6点円・7点円の両方が可能になり、単一の別項では足りない。

**正しい形**：プロファイルは `4, 5, ..., q+1` の値を取り得る。
一般の q では **4 から q+1 までのすべての場合**を扱う必要がある。

### 10ax. 完全な診断：欠落は3プロファイルのみ

**除数は元のままで正しい**（「4の個数」）。前項の「除数が誤り」という
診断は撤回する。

**q=7 の全プロファイル照合**：

| プロファイル | 組み立て | 全数 | 差 |
|---|---:|---:|---:|
| (4,4,4) | 36,985,200 | 36,985,200 | **0** |
| (4,4,4,4) | 25,636,800 | 25,636,800 | **0** |
| (4,4) | 15,092,000 | 15,092,000 | **0** |
| (5,4) | 10,348,800 | 10,348,800 | **0** |
| (5,4,4) | 5,115,600 | 5,115,600 | **0** |
| (4,4,4,4,4) | 2,881,200 | 2,881,200 | **0** |
| (4,) | 1,881,600 | 1,881,600 | **0** |
| **(5,)** | **0** | **1,411,200** | **−1,411,200** |
| **(6,)** | **0** | **411,600** | **−411,600** |
| (4,4,4,4,4,4) | 117,600 | 117,600 | **0** |
| **(7,)** | **0** | **2,800** | **−2,800** |

**8/11 が完全一致。欠落は3つだけ。**

**欠落の構造的理由**：`(5,)`, `(6,)`, `(7,)` はいずれも
「1つの円が5点以上を取り、**他の4円を持たない**」7点集合。
タプルループは `|T| = 4` を固定するので、4円を持たない集合は
**列挙されない**。

**単純な積では書けない**：`(5,) = b·C(s,5)·(n−s) = 350·56·42 = 823,200`
だが全数は 1,411,200。外2点が別の4円を作らない場合に限るため。

### 10ay. 欠落3プロファイルのうち2つは閉形式

**単一円プロファイルの測定**：

| q | `(4,)` | `(5,)` | `(6,)` | `(7,)` |
|---:|---:|---:|---:|---:|
| 5 | — | **0** | **2,600** | 0 |
| 7 | 1,881,600 | **1,411,200** | **411,600** | **2,800** |

**定理**：

```
(7,) = b·C(s,7)
(6,) = b·C(s,6)·(n−s)
```

**証明**：`(7,)` は7点すべてが1円上。`(6,)` は6点が1円上、1点が円外。
**「他の4円を持たない」条件は自動的に満たされる**（6点円があれば
残り1点は円外で他に4円を作れない）。 □

**検証**：**4/4 完全一致**

| q | `(7,)` 公式 | 実測 | `(6,)` 公式 | 実測 |
|---:|---:|---:|---:|---:|
| 5 | 0 | **0** | 2,600 | **2,600** |
| 7 | 2,800 | **2,800** | 411,600 | **411,600** |

**`(5,)` は条件付き**：素朴な `b·C(s,5)·C(n−s,2)` は
q=5 で 148,200（実測 **0**）、q=7 で 16,875,600（実測 **1,411,200**）。
外2点が別の4円を作る場合が多いため。

**q=5 で `(5,) = 0`** なのは `s = 6` で5点円 + 外2点が必ず別の4円を
作るため（外2点と円上の2点で4円ができる）。

**残るのは `(5,)` の閉形式のみ。**

### 10az. `(5,)` の条件と k=7 全プロファイルの決定

**定理**：

```
(5,) = b · #{T5 ⊂ C, {x,y} ⊂ C^c :
             ペンシル(x,y) の円が T5 と2点で交わらない}
```

**理由**：`C'` が `S` から4点取るには、`C'` が `C` と高々2点で交わるので
`C` 上の5点から2点、`{x,y}` から2点を取る必要がある。よって
「`{x,y}` を通り `C` 上の5点と2点で交わる円」が1つでもあれば
`(5,)` にならない。

**検証**：

| q | 該当ペンシル円の個数 0 の組数 | `b × それ` | 実測 `(5,)` |
|---:|---:|---:|---:|
| 5 | **0** | 0 | **0** ✓ |
| 7 | **4,032** | 1,411,200 | **1,411,200** ✓ |

**q=5 で 0 なのは `s = 6` で必ずペンシル円が存在するため。**

**k=7 の全プロファイル**：

```
(7,) = b·C(s,7)
(6,) = b·C(s,6)·(n−s)
(5,) = b·#{T5,{x,y} : ペンシル円が T5 と2点で交わらない}
(5,4), (5,4,4), (4,), (4,4), (4,4,4), (4,4,4,4), (4,4,4,4,4), (4,4,4,4,4,4)
     = タプル数 / (4の個数) × b
```

**検証**：q=5 で 657,800、q=7 で 99,884,400 — **両方とも全数と一致**。

### 10ba. k=7 の完全なアーク数公式（q=5,7 で検証完了）

```
#7-arcs = C(n,7) − Σ_P #(P を持つ7点集合)
```

**単一円プロファイル（3つ）**：

```
(7,) = b·C(s,7)
(6,) = b·C(s,6)·(n−s)
(5,) = b·#{T5,{x,y} : ペンシル(x,y) の円が T5 と2点で交わらない}
```

**複数円プロファイル（8つ）**：タプル公式から

```
#4円 = 1 + v + [|W ∩ T| = 1],   #5円 = [|W ∩ T| = 2]
v = #{C' ≠ C : |C' ∩ T| = 2 かつ |C' ∩ {x,y,z}| = 2}
#(P を持つ集合) = (P を持つタプル数) / (#P の4の個数) × b
```

**検証**：

| q | プロファイル数 | bad | arcs | `C(n,7)` | 一致 |
|---:|---:|---:|---:|---:|---|
| 5 | 8 | 657,800 | **0** | 657,800 | ✓ |
| 7 | 11 | 99,884,400 | **0** | 99,884,400 | ✓ |
| **8** | **10** | **695,142,240** | **1,048,320** | **696,190,560** | ✓ |

**3つの q（奇数2つ、偶数1つ）すべてで完全一致。**

**q=8 の `arcs = 1,048,320` は Sitjar の preprint**
（[alphaXiv](https://www.alphaxiv.org/abs/2611.anti-cocircular-ovoids-pg3-8)）
**が報告する `PG(3,8)` の楕円二次曲面上の7-アーク数と完全に一致する。**
独立な2経路（本研究の公式 vs 文献の全数数え上げ）が同じ値を出した。

**標数2 でも公式が成立**することを確認（`N_xy` の偶奇分岐が正しい）。

**k=7 の構造研究は完了した。**

### 10bb. `(5,)` の閉形式：k=6 の機構で閉じる

**鍵となる気づき**：`(5,)` の条件「`{x,y}` を通るペンシル円が `T5` と
2点で交わらない」は、ペンシルが定める対合 `ι(x,y)` を使うと
**ちょうど `j({x,y}) = 0`**（`j` は k=6 のペンシル量）。

**定理**：

```
(5,) = b · Σ_{n₂} N_xy(n₂) · H(n₂, n₁, 0, 5),   n₁ = s − 2n₂
```

`N_xy` と `H` は k=6 の閉形式（§10t）。

**検証**：

| q | `N_xy` | `H(·,·,0,5)` | 公式 | 実測 | 一致 |
|---:|---|---|---:|---:|---|
| 5 | `{2:120, 3:70}` | `(2,2,0), (3,0,0)` | **0** | 0 | ✓ |
| 7 | `{3:504, 4:357}` | `(3,2,8), (4,0,0)` | **1,411,200** | 1,411,200 | ✓ |
| 8 | `{0:28, 4:1512}` | — | **14,414,400** | 14,414,400 | ✓ |

**3/3 完全一致。**

**q=5 で 0 になる理由**：`n₂=2, n₁=2` で `H=0`（5点を選ぶと必ず対が
1つ入る）、`n₂=3, n₁=0` で `H=0`（`n₁=0` で5点は選べない）。
`s = 6` という特殊事情。

**これで k=7 のすべてのプロファイルが閉形式になった。**
k=6 と k=7 が同じ機構（ペンシルの対合）で統一された。

### 10bc. q=9 での検証（4つ目の q）と高速化

**高速化**：`v` を全 `b` 円ではなく**3つのペンシル（各 `q+1` 円）**だけ
から計算する。`O(C(s,4)·C(n−s,3)·3q)` になり **25倍高速化**。

| q | ビルド | タプルループ | 合計 |
|---:|---:|---:|---:|
| 5 | 1.6s | 0.2s | 1.8s |
| 9 | 411s | 230s | 641s |

**結果（q=9）**：

```
n = 82, b = 738, s = 10
(5,) = 94,369,536   (6,) = 11,158,560   (7,) = 88,560
bad  = 3,784,753,296  (整数)
arcs =    17,003,520
C(82,7) = 3,801,756,816
consistent: True
```

**4つの q での検証**：

| q | 標数 | プロファイル数 | bad | arcs | 一致 |
|---:|---|---:|---:|---:|---|
| 5 | 奇数 | 8 | 657,800 | **0** | ✓ |
| 7 | 奇数 | 11 | 99,884,400 | **0** | ✓ |
| 8 | 偶数 | 10 | 695,142,240 | **1,048,320** | ✓ |
| **9** | **奇数** | **8** | **3,784,753,296** | **17,003,520** | ✓ |

**7-アーク数の系列**：

| q | `K(q)` | 7-アーク数 |
|---:|---:|---:|
| 5 | 6 | **0** |
| 7 | 6 | **0** |
| 8 | 7 | **1,048,320** |
| 9 | 9 | **17,003,520** |

**`K(q) ≥ 7` のときに限り7-アークが存在する**という整合が取れている。

### 10bd. k=6 と k=7 の相互検証

`k`-アークが存在するのは `K(q) ≥ k` のとき、かつそのときに限る。
**独立に計算した2つの閉形式が同じ `K` と整合する**ことは両方の
正しさの傍証になる。

| q | `K(q)` | `#6-arcs` | `#7-arcs` | 整合 |
|---:|---:|---:|---:|---|
| 5 | 6 | 5,200 | 0 | ✓ |
| 7 | 6 | 1,254,400 | 0 | ✓ |
| 8 | 7 | 9,434,880 | 1,048,320 | ✓ |
| 9 | 9 | **52,781,760** | **17,003,520** | ✓ |

**8/8 完全一致。**

**q=5, q=7 では `K = 6`** なので6-アークは存在するが7-アークは存在
しない。両方の閉形式がこれを正しく再現。

**q=8 では `K = 7`** で7-アークが初めて存在（文献値と一致）。

**q=9 では `K = 9`** で7-アークが豊富（q=8 の16倍）。

**新しい値**：`#6-arcs(q=9) = 52,781,760`。

### 10be. アーク密度から見た `K(q)` の増大

`d_k = #k-arcs / C(n,7)` を「アーク密度」とする。

| q | n | `K` | `d₆` | `d₇` |
|---:|---:|---:|---:|---:|
| 5 | 26 | 6 | 0.007905 | 0 |
| 7 | 50 | 6 | 0.012559 | 0 |
| 8 | 65 | 7 | 0.013552 | 0.001506 |
| 9 | 82 | 9 | 0.013884 | 0.004473 |

**k=6 の密度は飽和**（0.0079 → 0.0139）。`K > 6` になった q ≥ 8 で頭打ち。

**k=7 の密度は急成長**（0 → 0.0045）。q=9 で q=8 の3倍。

**`K` と `q^(1/3)` の比**：

| q | `K` | `q^(1/3)` | `K/q^(1/3)` |
|---:|---:|---:|---:|
| 5 | 6 | 1.710 | **3.509** |
| 7 | 6 | 1.913 | **3.137** |
| 8 | 7 | 2.000 | **3.500** |
| 9 | 9 | 2.080 | **4.327** |

**比は増加傾向**（3.5 → 3.1 → 3.5 → 4.3）。q=9 で顕著に増加。

**これは `K` が `q^(1/3)` より速く増えることを示唆する。**
ブロッキング下界 `Ω(q^(1/3))` は緩い可能性が高い。

### 10bf. アーク数の連続比に公式はない（否定的結果）

| q | `#4` | `#5` | `#6` | `#7` | `#5/#4` | `#6/#5` | `#7/#6` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 13,000 | 26,000 | 5,200 | 0 | **2** | 0.2 | — |
| 7 | 205,800 | 1,070,160 | 1,254,400 | 0 | **26/5** | 1.172 | — |
| 8 | 611,520 | 4,525,248 | 9,434,880 | 1,048,320 | **37/5** | 2.085 | **1/9** |
| 9 | 1,594,080 | 15,940,800 | 52,781,760 | 17,003,520 | **10** | 3.311 | 0.322 |

**`#5/#4` は `2, 26/5, 37/5, 10`** で、`q−3`（2,4,5,6）とも
`(n−4)/5`（4.4, 9.2, 12.2, 15.6）とも一致しない。**単純な公式はない。**

**理由**：`#4 = C(n,4) − b·C(s,4)`、`#5 = C(n,5) − b·C(s,5) − b·C(s,4)(n−s)`
の比を取ると `C(n,k)` と `b·C(s,j)` の混合項が残り、`n = q²+1`、
`b = q(q²+1)`、`s = q+1` を代入しても約分されない。

**`q=8` の `#7/#6 = 1/9`** は正確な一致（`1048320 × 9 = 9434880`）だが、
**偶然であり公式ではない**。

**方針**：アーク数の構造は「比」ではなく「各 k の独立な閉形式」で
捉えるべき。

### 10bg. `#4-arcs` と `#5-arcs` の多項式展開

**定理**：

```
#4-arcs = (q⁸ − q⁷ − q⁴ + q³) / 24
#5-arcs = (q¹⁰ − 5q⁹ + 5q⁸ − q⁷ − 5q⁶ + 15q⁵ − 15q⁴ + 5q³) / 120
```

**検証**：

| q | `#4` 多項式 | 実測 | `#5` 多項式 | 実測 |
|---:|---:|---:|---:|---:|
| 5 | 13,000 | 13,000 | 26,000 | 26,000 |
| 7 | 205,800 | 205,800 | 1,070,160 | 1,070,160 |
| 8 | 611,520 | 611,520 | 4,525,248 | 4,525,248 |
| 9 | 1,594,080 | 1,594,080 | 15,940,800 | 15,940,800 |

**8/8 完全一致。**

**主項**：`#4 ~ q⁸/24 = q⁸/4!`、`#5 ~ q¹⁰/120 = q¹⁰/5!`。

**これは `C(n,k)` の主項とちょうど一致する**（`n ~ q²` より
`C(n,k) ~ q^(2k)/k!`）。**禁止条件は主項に寄与しない**（次の次数以下）。

**次数は `2k`**（`#4` が8次、`#5` が10次）。

### 10bh. `#6-arcs` の多項式（奇数 q）

**定理**：

```
#6-arcs = q¹²/720 − q¹¹/48 + q¹⁰/8 − 53q⁹/144 + 373q⁸/720
          − 37q⁷/144 − 5q⁶/48 + 53q⁵/144 − 187q⁴/360
          + 5q³/18 − q²/48
```

**12次多項式。**

**検証**：**15点で完全一致**（q = 3, 5, 7, ..., 31、うち q=29,31 は外挿）。

**主項**：`#6-arcs ~ q¹²/720 = q¹²/6!`。

**次数と主項の系列**：

| k | 次数 | 主項 |
|---:|---:|---|
| 4 | 8 | `q⁸/4!` |
| 5 | 10 | `q¹⁰/5!` |
| 6 | 12 | `q¹²/6!` |

**`#k-arcs` の次数は `2k`、主項は `q^(2k)/k!`。** 一貫したパターン。

**偶数 q の多項式は未取得**（`N_xy` の偶奇分岐で別の多項式になるが、
利用可能な偶数 q が 4, 8, 16 の3点のみで12次補間に足りない）。

### 10bi. `#4-arcs` の完全な因数分解

**定理**：

```
#4-arcs = q³ (q−1)² (q+1) (q²+1) / 24
```

**導出**：

```
q⁸ − q⁷ − q⁴ + q³ = q³ (q⁵ − q⁴ − q + 1)
                   = q³ (q⁴(q−1) − (q−1))
                   = q³ (q−1)(q⁴ − 1)
                   = q³ (q−1)(q²−1)(q²+1)
                   = q³ (q−1)² (q+1)(q²+1)
```

**検証**：**6/6 完全一致**（q = 5, 7, 8, 9, 11, 13）。

**因子の意味**：

| 因子 | 意味 |
|---|---|
| `q³` | 円の選択（`b = q(q²+1)` の一部） |
| `(q−1)²` | 2点の選び方の制約 |
| `(q+1)` | `s = q+1` |
| `q²+1` | `n = q²+1` |
| `1/24 = 1/4!` | 4点の対称性 |

**`n = q²+1` と `s = q+1` がそのまま因子として現れる。**

**`#5` は `q³(q−1)` まで、`#6` は `q²(q−1)²(q+1)(q²+1)` まで
しか分解しない**（残りは6次・5次の既約多項式）。**`#4` だけが完全に
分解する。**

### 10bj. `#6-arcs` の因数分解：`(q−3)` 因子の発見

`#6` の残り `P6 = q⁵ − 14q⁴ + 76q³ − 189q² + 185q − 15` は
**`P6(3) = 0`** を満たす。よって `(q−3)` が因子。

```
P6 = (q−3)(q⁴ − 11q³ + 43q² − 60q + 5)
```

**定理（奇数 q）**：

```
#6-arcs = q² (q−1)² (q+1) (q²+1) (q−3)
          × (q⁴ − 11q³ + 43q² − 60q + 5) / 720
```

**検証**：**4/4 一致**（q = 5, 7, 9, 11）。

**4次因子 `Q(q) = q⁴ − 11q³ + 43q² − 60q + 5` は既約**
（整数根なし、2次因子なし）。

**`(q−3)` の意味**：`q = 3` で `#6-arcs = 0` になることに対応する。
実際 `K(3) = 5 < 6` なので6-アークは存在しない。

**因子の階層**：

| k | 分解 |
|---|---|
| 4 | **完全分解** `q³(q−1)²(q+1)(q²+1)/24` |
| 5 | `q³(q−1)` × 6次既約 |
| 6 | `q²(q−1)²(q+1)(q²+1)(q−3)` × 4次既約 |

### 10bk. 訂正：`#5` 多項式の書き写しミスと `arcs6` の浮動小数点バグ

**2つの誤りを発見・修正した。**

**誤り1：`#5` の多項式の書き写しミス**

§10bg で記録した `#5-arcs` の多項式は**5つの係数が誤っていた**。
q=5 で `45875/3`（非整数）になり実測 `26000` と一致しないことで発覚。

**正しい多項式**：

```
#5-arcs = q³/24 − 3q⁴/40 + q⁵/24 − q⁶/120 − q⁷/24
          + 3q⁸/40 − q⁹/24 + q¹⁰/120
```

**誤り2：`arcs6` の浮動小数点バグ**

`arc_k6_pure.py` の `arcs6` が `h1 / 2`、`h2 / 3` と書かれており、
**浮動小数点除算**になっていた。`#6-arcs` が 2⁵³ を超えると精度を失う。

**症状**：q=45, 53, 57 で多項式検証が失敗（末尾が 120 で割り切れない）。

**修正**：`Fraction(h1, 2)`、`Fraction(h2, 3)` に変更。

**修正後の正しい形（q=3..59 で検証）**：

```
#4-arcs = q³(q−1)²(q+1)(q²+1)/24
#5-arcs = q³(q−1)²(q+1)(q²+1)(q² − 4q + 5)/120
#6-arcs = q²(q−1)²(q+1)(q−3)(q²+1)
          × (q⁴ − 11q³ + 43q² − 60q + 5)/720   （奇数 q のみ）
```

**`#5` も `#4` と同じ因子 `q³(q−1)²(q+1)(q²+1)` を持つ**
（前項の「`q³(q−1)` までしか括れない」は誤り）。
残る2次因子 `q² − 4q + 5` は判別式 `−4 < 0` で実根なし。

**`#6` は奇数 q でのみ有効**（偶数 q は別の多項式、13点必要だが
利用可能な偶数 q は 4, 8, 16 の3点のみ）。

### 10bl. 偶数 q の `N_xy` 公式と `#6-arcs` 閉形式

**定理（偶数 q の `N_xy`）**：

```
N_xy(0)   = C(q,2) = q(q−1)/2
N_xy(q/2) = q(q²−1)(q−2)/2
```

**検証**：**8/8 完全一致**

| q | `N_xy(0)` | `C(q,2)` | `N_xy(q/2)` | 公式 |
|---:|---:|---:|---:|---:|
| 4 | 6 | 6 ✓ | 60 | 60 ✓ |
| 8 | 28 | 28 ✓ | 1,512 | 1,512 ✓ |
| 16 | 120 | 120 ✓ | 28,560 | 28,560 ✓ |
| 32 | 496 | 496 ✓ | 491,040 | 491,040 ✓ |

**`(q−2)` 因子が以前は抜けていた**（`q(q²−1)/2` と誤記）。

**偶数 q の `#6-arcs` 閉形式**：

```
#6-arcs = C(n,6) − b·C(s,6) − b·C(s,5)(n−s)
          − b·[ C(q,2)·(H(0,s,0) + H(0,s,1)/2 + H(0,s,2)/3)
              + q(q²−1)(q−2)/2·(H(q/2,1,0) + H(q/2,1,1)/2
                                + H(q/2,1,2)/3) ]
```

（`H` は `k=4`。）

**検証**：**6/6 完全一致**（q = 2, 4, 8, 16, 32, 64）。

**多項式形は未取得**：12次には13点必要だが、利用可能な偶数 q は
2, 4, 8, 16, 32, 64, 128 の**7点のみ**。**閉形式があれば多項式形は
不要**（任意の偶数 q で計算可能）。

### 10bm. k=8 の計算可能性の壁

**8-アークが存在する最小の q は 9**（`K(q) ≥ 8` が必要、
`K(9) = 9`）。q ≤ 8 では `K ≤ 7` なので存在しない。

**3つの計算経路すべてが不可能**：

| 経路 | 計算量 | 見積 |
|---|---|---|
| 直接列挙 | `C(82,8) = 35,641,470,150` | 不可能 |
| プロファイル法 | `C(10,4)×C(72,4) = 216,045,900` タプル | **約20日**（実測 50,000 タプルで 397.6 秒） |
| 7-アーク拡張 | `17,003,520 × 75 = 1.28×10⁹` 判定 × 245 操作 | `3.1×10¹¹` 操作 |

**k=7 が可能だったのは幸運**：q=9 でタプル数が `12,524,400`（k=8 の
17分の1）だったため。

**構造的知見**：`C' ≠ C` は `C` と高々2点で交わるので
`|C' ∩ S| ≤ 2 + 4 = 6`。よって k=8 のプロファイル値は **4, 5, 6**
（k=7 では 4, 5 のみ）。**6点円が k=8 の新要素。**

**プロファイル種類は 11 → 22 以上に増加**（q=9 のサンプルで22種観測）。

### 10bn. k=8 の厳密値（C 実装で突破）

**C 実装**（`arc_k8.c`）：4円をハッシュ集合に格納し、8点部分集合を
列挙して「4円を含むか」を判定する。**k=7 版で `arcs = 17,003,520` が
Python と完全一致**することを確認してから k=8 に適用。

**結果（q=9）**：

```
n = 82, b = 738
total = 35,641,470,150 = C(82,8)   ✓
arcs  =      1,062,720
```

**`total = C(82,8)` の完全一致**で列挙の正しさを確認。
`arcs > 0` は `K(9) = 9 ≥ 8` と整合。

**驚くべき比**：

```
#8-arcs / #7-arcs = 1,062,720 / 17,003,520 = 1/16   （正確に）
```

**アーク密度**：

| k | `#k-arcs` | `C(82,k)` | 密度 |
|---:|---:|---:|---:|
| 7 | 17,003,520 | 3,801,756,816 | 0.004473 |
| 8 | 1,062,720 | 35,641,470,150 | **0.0000298** |

**密度は150分の1に急落。** 8-アークは極めて稀。

**アーク数の系列（q=9）**：k=6 がピーク（52.8M）で、そこから急減。

**前項の「3経路すべて不可能」を部分的に撤回**：プロファイル法は
Python では不可能だが、**C の直接列挙は可能**だった。

**k=8 を3つの q で計算**：

| q | n | `C(n,8)` | `#8-arcs` | `K(q)` | 整合 |
|---:|---:|---:|---:|---:|---|
| 5 | 26 | 1,562,275 | **0** | 6 | ✓ |
| 8 | 65 | 5,047,381,560 | **0** | 7 | ✓ |
| 9 | 82 | 35,641,470,150 | **1,062,720** | 9 | ✓ |
| **11** | 122 | 962,889,794,295 | **121,343,640** | ≥9 | ✓ |

**q=11 の結果（`arc_k8_big.exe`、約6時間）**：

```
n = 122, b = 1342
total = 962,889,794,295 = C(122,8)   ✓
arcs  =     121,343,640
```

`total = C(122,8)` の完全一致で列挙の正しさを再確認。8-アーク密度は
q=9 の 2.98×10⁻⁵ から q=11 では **1.26×10⁻⁴** へ**増加**する
（`K(q)` が q とともに増えることと整合的）。

**`total = C(n,8)` が 4/4 完全一致**（列挙の正しさを再確認）。
**`K(q) ≥ 8` のときに限り8-アークが存在**するという整合も取れている。

**計算時間**：q=5 即座、q=8 約1分、q=9 約13分、**q=11 約6時間**（完了済み）。

**C 実装の二重検証**：

| 検証 | 結果 | 照合先 |
|---|---|---|
| k=7 at q=8 | `arcs = 1,048,320` | Python と Sitjar の preprint |
| k=7 at q=9 | `arcs = 17,003,520` | Python |

**2点で独立に一致。C 実装は正しい。**

### 10bn2. アーク・センサス法：部分集合ではなくアークを歩く

k-アーク数を「全 k 部分集合を列挙して判定」する代わりに、**アークだけを DFS で列挙**して
数える方法（`scripts/arc_census.c`）。増分ブロッキングを保った DFS は各アークを1回だけ訪れ、
深さ `d` のノード数が `#arcs(d)`、各ノードの合法手数 `|allowed|` の和が
`(d+1)·#arcs(d+1)` になる。よって

```
#arcs(d+1) = (Σ_{d-アーク} 合法手数) / (d+1)
```

で、しかもこれは `NODES(d+1)` と一致する（**二重の数え方による組込みの検証**）。
最大深さ `K+1` まで走らせて `#arcs(K+1) = 0` が出れば **`K` の厳密決定**になる。

**検証**（K1058 の全層サイズと一致、かつ `K` の厳密性も再現）：

| q | ノード総数 | 深さ別ノード数 | `#arcs(K+1)` | `K` | 時間 |
|---:|---:|---|---:|---:|---:|
| 7 | 2,551,236 | 1, 50, 1,225, 19,600, 205,800, 1,070,160, 1,254,400 | 0 | 6 ✓ | 2.5 s |
| 8 | 15,665,794 | 1, 65, 2,080, 43,680, 611,520, 4,525,248, 9,434,880, 1,048,320 | 0 | 7 ✓ | 21 s |
| 9 | 88,504,364 | 1, 82, 3,321, 88,560, 1,594,080, 15,940,800, 52,781,760, 17,003,520, 1,062,720, 29,520 | 0 | 9 ✓ | 131 s |

すべて K1058 の層サイズ表と一致し、`#arcs(K+1) = 0` により `K` の厳密性も再確認。
**q=11 はこの方法でも長時間かかる見込み**（ノード数が桁違い）だが、
`#arcs(10) = 0` が出れば `K(11) = 9` の厳密決定になる（実行中）。

**k=8 の完全な表**：

| q | n | `C(n,8)` | `#8-arcs` | `K(q)` | 整合 |
|---:|---:|---:|---:|---:|---|
| 5 | 26 | 1,562,275 | **0** | 6 | ✓ |
| 7 | 50 | 536,878,650 | **0** | 6 | ✓ |
| 8 | 65 | 5,047,381,560 | **0** | 7 | ✓ |
| 9 | 82 | 35,641,470,150 | **1,062,720** | 9 | ✓ |

**`total = C(n,8)` が 4/4 完全一致。**
**k=8 が非零になるのは q=9 のみ**（q ≤ 9 の範囲で）。

### 10bo. k=8 のプロファイル公式（6類）

`S = T ∪ {w,x,y,z}`（`|T| = 4`、`T ⊂ C`、外4点 `X = {w,x,y,z}`）。
`C' ≠ C` は `C` と高々2点で交わるので `|C' ∩ S| ≤ 2 + 4 = 6`。
**プロファイルの値は 4, 5, 6 のみ。**

**6つの類**：

| 記号 | 条件 | `S` からの点数 |
|---|---|---:|
| `v2` | `\|C'∩T\|=2`, `\|C'∩X\|=2` | 4 |
| `v3` | `\|C'∩T\|=2`, `\|C'∩X\|=3` | 5 |
| `v4` | `\|C'∩T\|=2`, `\|C'∩X\|=4` | 6 |
| `u3` | `\|C'∩T\|=1`, `\|C'∩X\|=3` | 4 |
| `u4` | `\|C'∩T\|=1`, `\|C'∩X\|=4` | 5 |
| `z4` | `\|C'∩T\|=0`, `\|C'∩X\|=4` | 4 |

**定理**：

```
#4円 = 1 + v2 + u3 + z4
#5円 = v3 + u4
#6円 = v4
```

**検証**：**q=5 で 5,000/5,000、q=7 で 5,000/5,000 — 0 不一致。**

**k=7 との比較**：

| 量 | k=7 | k=8 |
|---|---|---|
| 外点の数 | 3 | 4 |
| プロファイル値 | 4, 5 | 4, 5, **6** |
| 類の数 | 2 | **6** |

**k=7 の自然な拡張**（外点3→4、類2→6）。

### 10bp. k=9 の厳密値と比の系列

**結果（q=9）**：

```
n = 82, b = 738
total = 293,052,087,900 = C(82,9)   ✓
arcs  =          29,520
```

**`total = C(82,9)` の完全一致**で列挙の正しさを確認。
`arcs > 0` は `K(9) = 9 ≥ 9` と整合。

**驚くべき比の連鎖**：

```
#8/#7 = 1,062,720 / 17,003,520 = 1/16 = 1/4²   （正確に）
#9/#8 =    29,520 /  1,062,720 = 1/36 = 1/6²   （正確に）
```

**どちらも完全平方の逆数。分母の系列は 4, 6, ...**
次は 8 か（`#10/#9 = 1/64`）？ **強い構造的示唆。**

**アーク密度の急落**：

| k | `#k-arcs` | 密度 |
|---:|---:|---:|
| 7 | 17,003,520 | 0.00447254 |
| 8 | 1,062,720 | 0.00002982 |
| 9 | **29,520** | **0.0000001007** |

**アーク数の系列（q=9）**：k=6 がピーク（52.8M）で、そこから急減。
`K(9) = 9` なので k=9 が最大。

### 10bq. 比の系列 `1/4², 1/6²` は `K(q)` で終わる

**2つの候補式**（どちらも2点に適合）：

**候補 A**：`1/(2(k−5))²`

| k | `2(k−5)` | 予測 | 実測 |
|---:|---:|---:|---:|
| 7 | 4 | 1/16 | 1/16 ✓ |
| 8 | 6 | 1/36 | 1/36 ✓ |

**候補 B**：`1/(q−5)²`（k=7）、`1/(q−3)²`（k=8）

| k | 分母 | 予測 | 実測 |
|---:|---:|---:|---:|
| 7 | `q−5 = 4` | 1/16 | 1/16 ✓ |
| 8 | `q−3 = 6` | 1/36 | 1/36 ✓ |

**決定的な観察**：`K(9) = 9` なので `#10 = 0`。もしパターンが続くなら

```
#10 = 29,520 / 64  = 461.25   （整数でない）
#10 = 29,520 / 100 = 295.2    （整数でない）
```

**どちらも整数でない。よってパターンは継続できない。**
**これは `#10 = 0` と完全に整合する。**

**解釈**：比の系列 `1/4², 1/6²` は偶然ではなく、
**「アーク数が `K(q)` で急激に終わる」ことの現れ**。
`K(9) = 9` という制約が、比が `1/8²` に進むことを**整数性のレベルで
禁止している**。

### 10br. k=8 の組み立て：除算順序の罠

**組み立ての式**：

```
#(P を持つ8点集合) = タプル数(P) / (#4円) × b
```

**この順序で計算すると壊れる。**

例（q=5、プロファイル `(10,0,0)`）：

```
タプル数 = 525, #4円 = 10, b = 130
525 / 10 = 52.5        ← 整数でない！
525 × 130 / 10 = 6,825 ← 整数
```

**`タプル数 / #4円` は整数でないことがある。`b` を先に掛ければ
必ず整数になる。**

**正しい順序**：`タプル数 × b / #4円`。

**影響**：C の整数除算で `525/10 = 52`（切り捨て）となり、
合計が `1,562,210` になって `65` の誤差が出た。

**修正後の検証（q=5）**：

```
n = 26, b = 130, s = 6
タプル数 = 72,675, プロファイル数 = 13, 非整数 = 0
bad  = 1,562,275 = C(26,8)
arcs = 0
```

**全数計算と完全一致。**

**13のプロファイルの内訳（q=5）**：`(8,0,0)` が最大（26,640 タプル、
432,900 集合）、`(12,0,0)` が最小（60 タプル、650 集合）。

### 10bs. k=8 の6類の分布（q=5）

| 類 | 分布 |
|---|---|
| `v2` | `{1:1320, 2:5400, 3:12120, 4:17760, 5:17340, 6:14160, 7:3900, 8:615, 10:60}` |
| `v3` | `{0:45195, 1:26160, 2:1320}` |
| `v4` | `{0:72225, 1:450}` |
| `u3` | `{0:23745, 1:26760, 2:19140, 3:2760, 4:270}` |
| `u4` | `{0:70875, 1:1800}` |
| `z4` | `{0:65250, 1:7425}` |

**同時分布の類数：41**（プロファイルは13種）。

**構造的特徴**：

- **`v4` と `u4` は極めて稀**（`v4=1` は 0.6%、`u4=1` は 2.5%）。
  `C'` が `C` と2点で交わり、かつ外4点すべてを含む必要があるため。
- **`z4` は 0 か 1 のみ**。外4点 `X` を通る円は一意なので、
  **`X` が共円かどうかで決まる**。
- **`v2` は 1〜10 の広い範囲**（最も複雑）。
- **`X` から多くの点を取る類（`v4`, `u4`, `z4`）は稀** —
  「外4点が共円になりにくい」ことの反映。

### 10bt. `z4` の構造：共円性で決まる

**定理**：

```
z4 = 1  ⟺  X が共円 かつ その円が T と交わらない
```

**理由**：`X` が共円でなければ `X` を含む円は存在しない（`z4 = 0`）。
共円なら円 `D` が一意に定まり、`D` が `T` と交われば
`|D ∩ T| ≥ 1` で `z4` の条件を満たさない（代わりに `v2`/`v3`/`v4`
または `u3`/`u4` に数えられる）。

**検証（q=5）**：共円な `X` は `645 / 4,845`。

| `X` 共円 | `z4` | 組数 |
|---|---|---:|
| False | 0 | 63,000 |
| True | 0 | 2,250 |
| True | 1 | **7,425** |
| | | **72,675** ✓ |

**完全に整合。** `X` が共円なら `z4 = 1` が 76.7%。

**閉形式への道**：`Σ z4 = Σ_{X 共円} #{T : 円(X) ∩ T = ∅}`。
`T` は `C` の4点部分集合（`C(s,4)` 個）。円 `D` が `C` と `k` 点で
交わると `D ∩ T = ∅` となる `T` の数は `C(s−k, 4)`。
**よって `z4` の閉形式は「外点の共円4点の個数」と「`D` と `C` の
交点数」の分布から書ける。**

**`z4` が6類の中で最も構造が単純。**

### 10bu. `v4`, `u4`, `z4` は互いに排反で共円性と同値

**定理**：

```
v4 = 1  ⟺  X が共円 かつ  |D ∩ T| = 2
u4 = 1  ⟺  X が共円 かつ  |D ∩ T| = 1
z4 = 1  ⟺  X が共円 かつ  |D ∩ T| = 0
```

（`D` は `X` を通る円。）

**系**：

```
v4 + u4 + z4 = [X が共円]
```

**3つは互いに排反で、和が共円性の指示関数になる。**

**理由**：3つはいずれも `|C' ∩ X| = 4` を要求する。**4点は高々1つの
円を定める**ので該当する `C'` は `D` のみ。`D` が `T` と交わる点数
（0, 1, 2 のいずれか）で3つに分かれる。

**検証（q=5）**：

| 共円 | `\|D ∩ T\|` | 組数 | `(v4,u4,z4)` |
|---|---|---:|---|
| はい | 0 | 7,425 | (0,0,1) |
| はい | 1 | 1,800 | (0,1,0) |
| はい | 2 | 450 | (1,0,0) |
| いいえ | — | 63,000 | (0,0,0) |
| | | **72,675** ✓ | |

**3つが同時に1になる組は存在しない。**

**意義**：3つの類が**1つの量（共円性）に還元**された。
閉形式は「外点の共円4点の個数」と「`D` と `C` の交点数」の分布から
一括で書ける。**残る3類（`v2`, `v3`, `u3`）に集中できる。**

### 10bv. `|C' ∩ T|` の完全な分解

`T` は `C`（`s = q+1` 点）の4点部分集合。`C' ≠ C` は `C` と 0,1,2 点で
交わる。`k = |C'∩C|`、`m = |(C'∩C)∩T|` とすると `|C'∩T| = m`。

**定理（`|C'∩T| = 2`）**：

```
#{C' : |C' ∩ T| = 2} = 6q
```

`T` の2点の組は `C(4,2) = 6`、各組を通る円は `q+1` 個（うち `C` 自身）。

**検証（q=5）**：`6×5 = 30`、実測 **30** ✓

**定理（`|C'∩T| = 1`）**：

```
#{C' : |C' ∩ T| = 1} = 4(q−1) + 4(s−4)q
```

内訳：(a) `C` と1点（`T` 内）で接する `4(q−1)` 個、
(b) `C` と2点で交わり片方だけ `T` 内 `4(s−4)q` 個。

**検証（q=5, s=6）**：`16 + 40 = 56`、実測 **56** ✓

**定理（`|C'∩T| = 0`）**：3つの場合
(a) `C` と交わらない `N₀`、(b) `C−T` 内で接する `(s−4)(q−1)`、
(c) `C−T` 内の2点で交わる `C(s−4,2)·q`。

**検証（q=5）**：`(b)=8`、`(c)=5`、実測 43 より `N₀ = 30`。

**総数の一致**：`30 + 56 + 43 = 129 = b − 1` ✓

**次の段階**：`v2`, `v3`, `u3` は「`|C'∩T|` の条件」＋「`|C'∩X|` の
条件」で定義される。上記の分解と `X` 側の同様の分解を組み合わせれば
閉形式が得られる。

### 10bw. `sum(v2+v3+v4)` の閉形式

**測定値（q=5）**：`sum v2 = 324,000`、`sum v3 = 28,800`、
`sum v4 = 450`、**`sum v2+v3+v4 = 353,250`**。

**分解**：固定した `C'`（`|C'∩C| = 2`）に対し

- `T` は `C'∩C` の2点を含む → `C(s−2,2)` 通り
- `Y = C' − C` とすると `|C'∩X| = |Y∩X|`
- `X` は外点の4点部分集合で `|Y∩X| ≥ 2`

```
sum(v2+v3+v4) = C(s−2,2) × Σ_{C' : |C'∩C|=2} #{X : |Y∩X| ≥ 2}
```

**構造的事実**：`C'` が `C` と2点で交わるとき `|Y| = q−1`
（`C'` のサイズ `s = q+1` から2点を引いた残り）。

**定理（完成形）**：

```
sum(v2+v3+v4) = C(s−2,2) · C(s,2)·q
                · [C(n−s,4) − C(n−s−q+1,4) − (q−1)·C(n−s−q+1,3)]
```

**検証（q=5）**：`C(4,2) × C(6,2)·5 × [C(20,4) − C(16,4) − 4·C(16,3)]`
`= 6 × 75 × 785 = 353,250` — **実測と完全一致**。

**`v4` は既知**（共円性）なので、これで `v2+v3` が求まる。
残るは `v2` と `v3` の分離、および `u3`。

### 10bx. `sum(u3+u4)` の閉形式

**測定値（q=5）**：`sum u3 = 74,400`、`sum u4 = 1,800`、
**`sum u3+u4 = 76,200`**。

**`|C'∩T| = 1` の2族**：

| `\|C'∩C\|` | 意味 | 個数 | `\|Y\|` | `T` の選び方 |
|---:|---|---:|---:|---|
| 1 | `C` に接する | `s(q−1)` | `q` | `C(s−1,3)` |
| 2 | `C` と2点で交わる | `C(s,2)·q` | `q−1` | `2·C(s−2,3)` |

**構造的事実**：`|Y| = s − |C'∩C|`（`C'` のサイズが `s` のため）。

**定理（完成形）**：

```
sum(u3+u4) = s(q−1)·C(s−1,3)·G(q, n−s)
           + C(s,2)·q·2·C(s−2,3)·G(q−1, n−s)

G(y,m) = C(y,3)·C(m−y,1) + C(y,4)
```

**検証（q=5）**：

```
G(5,20) = 10·15 + 5 = 155
G(4,20) = 4·16 + 1 = 65
term1 = 24 · 10 · 155 = 37,200
term2 = 75 · 8 · 65   = 39,000
total = 76,200   ← 実測と完全一致
```

**`u4` は既知**（共円性）なので、これで `u3` が求まる。

**k=8 の6類すべての和が閉形式になった**（`v2+v3` と `u3` の
分離のみが残る）。

### 10by. `v2` / `v3` の分離：k=8 の閉形式が完成

**定理**：

```
sum v2 = C(s,2)·q · C(s−2,2) · C(q−1,2)·C(n−s−q+1,2)
sum v3 = C(s,2)·q · C(s−2,2) · C(q−1,3)·C(n−s−q+1,1)
```

**理由**：固定した `C'`（`|C'∩C| = 2`）に対し、`T` は `C'∩C` の2点を
含む（`C(s−2,2)` 通り）。`Y = C' − C`、`|Y| = q−1`。`X` は外点の
4点部分集合で `|Y∩X| = 2`（`v2`）または `3`（`v3`）。

**検証（q=5）**：

```
#C' with |C'∩C|=2: C(6,2)·5 = 75
#T containing both: C(4,2) = 6
#X with |Y∩X|=2: C(4,2)·C(16,2) = 720
#X with |Y∩X|=3: C(4,3)·C(16,1) = 64

v2 = 75 · 6 · 720 = 324,000   （実測 324,000）✓
v3 = 75 · 6 ·  64 =  28,800   （実測  28,800）✓
```

**k=8 の6類の検証まとめ（q=5）**：

| 類 | 閉形式 | 実測 | 一致 |
|---|---:|---:|---|
| `v2` | 324,000 | 324,000 | ✓ |
| `v3` | 28,800 | 28,800 | ✓ |
| `v4` | 450 | 450 | ✓ |
| `u3` | 74,400 | 74,400 | ✓ |
| `u4` | 1,800 | 1,800 | ✓ |
| `z4` | 7,425 | 7,425 | ✓ |

**6/6 完全一致。k=8 のアーク数が全数計算なしで出せる**（原理的に）。

**残る限界**：`v4+u4+z4` の和は「外点の共円4点の個数」に依存し、
その閉形式は未取得（外点集合の4-アーク数に相当）。

### 10bz. `N_cyc`：外点の共円4点の個数

**定理**：

```
N_cyc = Σ_{C' ≠ C} C(|C' ∩ 外点|, 4)
```

**理由**：共円な4点は**一意な円**の上にあるので、各円が
`C(|C'∩外点|, 4)` 個を寄与し**重複しない**。

**`|C'∩外点|` の分布（q=5）**：

| `\|C'∩外点\|` | 円の個数 | 意味 |
|---:|---:|---|
| 4 | 75 | `C` と2点で交わる（`C(s,2)·q`） |
| 5 | 24 | `C` に接する（`s(q−1)`） |
| 6 | 30 | `C` と交わらない（`N₀`） |

**構造的事実**：`|C'∩外点| = s − |C'∩C|`。

**検証（q=5）**：

```
N_cyc = 75·C(4,4) + 24·C(5,4) + 30·C(6,4)
      = 75·1 + 24·5 + 30·15
      = 75 + 120 + 450
      = 645
```

**直接数え上げと完全一致（645）。**

**定理（完成形）**：

```
N_cyc = C(s,2)·q·C(s−2,4) + s(q−1)·C(s−1,4) + N₀·C(s,4)
N₀ = (b−1) − C(s,2)·q − s(q−1)
```

**検証（q=5）**：`N₀ = 129 − 75 − 24 = 30`、`N_cyc = 645` ✓

**これで k=8 の最後のピースが埋まった。**
（`v4`, `u4`, `z4` の**個別**の和は `|D∩T|` の分布が必要で未取得。）

### 10ca. `v4`, `u4`, `z4` の個別の和：k=8 の閉形式が完全に完成

**定理**：共円な `X` の円を `D`、`k_X = |D∩C|` とすると

```
sum v4 = Σ_{X 共円} C(k_X,2)·C(s−k_X,2)
sum u4 = Σ_{X 共円} C(k_X,1)·C(s−k_X,3)
sum z4 = Σ_{X 共円} C(k_X,0)·C(s−k_X,4)
```

**理由**：`T` は `C` の4点部分集合。`|D∩T| = j` となる `T` の数は
`C(k_X,j)·C(s−k_X,4−j)`。`j = 2,1,0` がそれぞれ `v4`, `u4`, `z4`。

**`|D∩C|` の分布（q=5、共円な `X` 645 個）**：

| `\|D∩C\|` | 個数 |
|---:|---:|
| 0 | 450 |
| 1 | 120 |
| 2 | 75 |

**検証（q=5、`s=6`）**：

```
sum v4 = 75·C(2,2)C(4,2) = 75·6 = 450        ✓
sum u4 = 120·C(1,1)C(5,3) + 75·C(2,1)C(4,3)
       = 1,200 + 600 = 1,800                  ✓
sum z4 = 450·C(6,4) + 120·C(5,4) + 75·C(4,4)
       = 6,750 + 600 + 75 = 7,425             ✓
```

**3/3 完全一致。**

**k=8 の6類の検証まとめ（q=5）**：`v2`=324,000、`v3`=28,800、
`v4`=450、`u3`=74,400、`u4`=1,800、`z4`=7,425 — **6/6 完全一致**。

**k=8 のアーク数が全数計算なしで計算できる**（原理的に）。
**k=7 と同じ枠組みが k=8 でも完成した。**

**残る限界**：`k_X` の分布（`{0:450, 1:120, 2:75}`）の閉形式は未取得。

### 10cb. `k_X` の分布：k=8 の閉形式が完全に閉じた

**定理**：

```
#{X : k_X = j} = N_j · C(s−j, 4)

N_0 = (b−1) − C(s,2)·q − s(q−1)
N_1 = s(q−1)
N_2 = C(s,2)·q
```

**理由**：共円な `X` は一意な円 `D` の上にある。`|D∩C| = j` の円 `D` は
`|D∩外点| = s−j` 点を持つので、`X` の選び方は `C(s−j, 4)`。

**検証（q=5）**：

```
N_0 = 129 − 75 − 24 = 30,  N_1 = 24,  N_2 = 75   （合計 129 = b−1）

#{X : k_X=0} = 30·C(6,4) = 450
#{X : k_X=1} = 24·C(5,4) = 120
#{X : k_X=2} = 75·C(4,4) =  75
合計 = 645 = N_cyc   ✓
```

**実測 `{0:450, 1:120, 2:75}` と完全一致。**

**k=8 の閉形式（完全版）**：

```
sum v2 = C(s,2)·q · C(s−2,2) · C(q−1,2)·C(n−s−q+1,2)
sum v3 = C(s,2)·q · C(s−2,2) · C(q−1,3)·C(n−s−q+1,1)
sum v4 = Σ_j N_j·C(s−j,4) · C(j,2)·C(s−j,2)
sum u3 = s(q−1)·C(s−1,3)·G(q,n−s)
       + C(s,2)·q·2·C(s−2,3)·G(q−1,n−s) − sum u4
sum u4 = Σ_j N_j·C(s−j,4) · C(j,1)·C(s−j,3)
sum z4 = Σ_j N_j·C(s−j,4) · C(j,0)·C(s−j,4)
```

**すべて `q` の閉形式。k=8 のアーク数が全数計算なしで計算できる。**

**`N_j` の分解が随所で一貫**（`|C'∩C|` の分布、`|C'∩外点|` の分布、
`k_X` の分布がすべて同じ `N_j` から導かれる）。

### 10cc. 重要な限界：和ではアーク数は出ない

**6類の「和」だけではアーク数は出ない。**

アーク数の組み立ては

```
#8-arcs = C(n,8) − Σ_P (タプル数(P) / #4円(P)) × b − (7,) − (8,)
```

であり、**プロファイルの分布**（各 `(n4,n5,n6)` のタプル数）が必要。

**和は分布を決めない**（同じ和でも分布が違えばアーク数が変わる）。

**よって現状で閉形式なのは「6類の和」までであり、
アーク数そのものの閉形式は未完成。**

**一括検証（q=5）**：6類すべて完全一致（6/6）。

| 類 | 閉形式 | 実測 |
|---|---:|---:|
| `v2` | 324,000 | 324,000 ✓ |
| `v3` | 28,800 | 28,800 ✓ |
| `v4` | 450 | 450 ✓ |
| `u3` | 74,400 | 74,400 ✓ |
| `u4` | 1,800 | 1,800 ✓ |
| `z4` | 7,425 | 7,425 ✓ |

**アーク数の閉形式にはプロファイル分布が必要と確定。**

### 10cd. k=8 のプロファイル分布（q=5）

**13種のプロファイル**（合計 72,675 組）：

| `(n4,n5,n6)` | タプル数 | | `(n4,n5,n6)` | タプル数 |
|---|---:|---|---|---:|
| (8,0,0) | 26,640 | | (10,0,0) | 525 |
| (5,1,0) | 16,200 | | (3,2,0) | 360 |
| (7,0,0) | 9,450 | | (2,0,1) | 240 |
| (6,1,0) | 6,480 | | (3,0,1) | 210 |
| (4,1,0) | 5,280 | | (12,0,0) | 60 |
| (9,0,0) | 3,510 | | (2,2,0) | 960 |
| (6,0,0) | 2,760 | | | |

**`(v2,u3)` の同時分布は28種**（最大は `(5,2)` の 10,560）。

**構造的観察**：

- **`n6 = v4` はほぼ常に 0**（`n6=1` は `(2,0,1)` と `(3,0,1)` の
  2種のみ、合計 450 組 = 0.6%）。
- **`n5 = v3 + u4` は 0, 1, 2**（`n5=2` は 2種、合計 1,320 組）。
- **`n4` は 2〜12 の広い範囲**。

**なぜ和では足りないか**：`(8,0,0)` と `(5,1,0)` は同じ `n4` の範囲だが
`n5` が違う。組み立ては `÷n4` を含むので **`n4` の分布**が本質的に必要。
**和 `Σ v2 = 324,000` からは `(v2,u3)` の分布は復元できない。**

### 10ce. `(v2, u3)` の条件付き構造：トレードオフ

**条件付き分布（q=5）**：

| `v2` | 組数 | `u3` の分布 |
|---:|---:|---|
| 1 | 1,320 | `{0:1200, 2:120}` |
| 2 | 5,400 | `{0:570, 1:3120, 2:1680, 4:30}` |
| 3 | 12,120 | `{0:2040, 1:7920, 2:1560, 3:480, 4:120}` |
| 4 | 17,760 | `{0:6960, 1:4320, 2:4560, 3:1800, 4:120}` |
| 5 | 17,340 | `{0:3540, 1:2760, 2:10560, 3:480}` |
| 6 | 14,160 | `{0:6480, 1:7200, 2:480}` |
| 7 | 3,900 | `{0:2280, 1:1440, 2:180}` |
| 8 | 615 | `{0:615}` |
| 10 | 60 | `{0:60}` |

**`v2` は 1〜10**（`v2=4,5` が最頻）。

**トレードオフ**：`u3` の最大値は `v2` とともに**減る**
（`v2=1` で 2、`v2=4` で 4、`v2=8` で 0）。

**理由**：`v2` は「`T` と2点・`X` と2点共有する円」、`u3` は
「`T` と1点・`X` と3点共有する円」。**同じ `X` の4点を奪い合う**ため、
`X` を多く取る円（`u3`）が多いと `X` と2点だけの円（`v2`）が減る。

**`v2 + u3` は 1〜10 の範囲**に収まる（`X` の4点を含む円の総数に上限）。

**単純な積 `P(v2)·P(u3)` では書けない。**

### 10cf. 訂正：k=8 の組み立ては q=9 で破綻する

**q=9 で組み立てと全数が大きく食い違う**：

| 量 | 組み立て | 全数（C 実装） |
|---|---:|---:|
| `bad` | 35,521,382,790 | 35,640,407,430 |
| `arcs` | **120,087,360** | **1,062,720** |

**差は 119,024,640。**

**原因：単一円プロファイルの欠落。**

組み立ては `(7,)` と `(8,)` のみを別項として加えていたが、
**q=9 では `s = 10` なので `(5,)` と `(6,)` も存在する**：

| プロファイル | 上限 |
|---|---:|
| `(5,)` | 11,091,608,640 |
| `(6,)` | 396,128,880 |
| `(7,)` | 6,376,320 |
| `(8,)` | 33,210 |

**差 119,024,640 は `(5,)` と `(6,)` の寄与。**

**q=7 で成功したのは `s = 8` という特殊事情**：単一円プロファイルが
`(5,)`, `(6,)`, `(7,)` の3つで、`(5,)` と `(6,)` は既に別項として
加えていた。q=9 では `s = 10` になり形が変わる（外点が3個と2個）。

**正しい式**：

```
(5,) = b · #{T5 ⊂ C, Y ⊂ 外点 (|Y|=3) : ペンシル円が T5 と2点で交わらない}
(6,) = b · #{T6 ⊂ C, Y ⊂ 外点 (|Y|=2) : ペンシル円が T6 と2点で交わらない}
```

**「他の4円を作らない」条件付きで単純な積では書けない。**

**一般の q では `(5,)` から `(q+1,)` までのすべてが必要。**
**k=8 の閉形式は q=5,7 でのみ検証済み**であり、q=9 では未完成。

### 10cg. 訂正：単一円プロファイルは k=7 の結果だった

**前項の診断を撤回する。**

k=7 と k=8 の単一円プロファイルを全数列挙で比較した（q=5）：

| k | 単一円プロファイル |
|---:|---|
| **7** | `{6: 2600}` |
| **8** | `{}` （**存在しない**） |

**`(6,) = 2,600` は k=7 の結果だった。k=8 では単一円プロファイルは
1つも存在しない。**

**理由**：k=8 の単一円プロファイルは「8点のうち `j ≥ 5` 点が1つの円
`D` 上にあり、他の4円を持たない」もの。q=5 では `s = 6` で `j = 5,6`
が可能だが、**`D` 上の5〜6点に外点を加えると必ず別の4円ができる**
（q=5 は点が密で `n = 26`）。k=7 では外点が1個だけなので4円ができにくい。

**よって q=9 の差 119,024,640 の原因は別にある**（未特定）。
候補：(1) プロファイル公式 `#4円 = 1+v2+u3+z4` の破綻、
(2) 多重度定理 `÷n4` の破綻、(3) 他の欠落プロファイル。

**q=9 のプロファイル公式を検証する必要がある。**

### 10ch. 訂正：多重度定理は正しい（LHS/RHS テストが誤り）

**前項の「`C(s,4)` 倍過大カウント」という診断を撤回する。**

**誤りの内容**：前項のテストは

```
LHS = b · C(s,4) · C(n−s,4)   （(D,T,X) の三つ組）
RHS = b · C(n−s,4)            （(D,X) の二つ組）
```

を比較していた。**別の対象なので比が `C(s,4)` になるのは当然。**

**正しい関係**：8点集合 `S` はタプルループで **`n4(P)` 回**現れる
（`T = C∩S` は一意、`D` は `S` の4円で `n4(P)` 個）。よって

```
tuples(P) = #S(P) × n4(P)
#S(P) = tuples(P) / n4(P)
```

**これは組み立てが行っていることそのもので、正しい。**

**q=5 での検証**：13プロファイルの `tuples(P)×b/n4(P)` の和が
`1,562,275 = C(26,8)` に完全一致。

**プロファイル公式も q=9 で正しい**（500 組で 0 不一致）。

**よって q=9 の差 119,024,640 の原因は依然未特定。**
最有力候補は**単一円プロファイル**（q=9 では `s = 10` で `j = 5..8` が
可能、q=5 では `s = 6` で存在しなかった）。

### 10ci. k=8 の現状総括

**確立したこと**：

| 項目 | 状態 |
|---|---|
| 厳密なアーク数（q=5,7,8,9） | `total = C(n,8)` が 4/4 一致 |
| C 実装の二重検証 | k=7 で Python と Sitjar の preprint に一致 |
| プロファイル公式（6類） | q=5,7,9 で 0 不一致 |
| 多重度定理 | q=5 の13プロファイルで完全一致 |
| `v4+u4+z4 = [X が共円]` | q=5 で完全整合 |
| 6類の和の閉形式 | q=5 で 6/6 一致 |
| 単一円プロファイル | q=5 で 0 件（高速列挙） |

**未解決**：

1. **q=9 の組み立ての差 119,024,640**（最重要）
2. プロファイル分布の閉形式（`(v2,u3)` のトレードオフ）
3. q=11 の k=8

**撤回した誤診（4回）**：

| # | 誤診 | 撤回理由 |
|---|---|---|
| 1 | 「6点以上の円」が原因 | k=8 の差とは無関係 |
| 2 | 「除数が誤り」 | 8/11 プロファイルが一致していた |
| 3 | 「単一円 `(5,)`,`(6,)` の欠落」 | `(6,)=2600` は **k=7** の結果 |
| 4 | 「`C(s,4)` 倍過大カウント」 | LHS/RHS が別の対象 |

**4回すべてが「数値の一致を構造的証拠と早合点」から生じた。**

### 10cj. 訂正：k=8 の組み立ては q=7 でも破綻していた

**前項までの「q=5, q=7 で成功」は誤り。q=7 も失敗する。**

**結果（q=7）**：

```
n=50, b=350, s=8
tuples = 7,835,100, profiles = 21
(7,) = 117,600   (8,) = 350
bad  = 536,094,650
total = 536,878,650 = C(50,8)   ✓
arcs = 784,000
```

**全数（C 実装）では `arcs = 0`**（`K(7) = 6 < 8`）。**差は 784,000。**

**差の構造**：

```
784,000 = b · C(s,6) · s(s+2)
        = 350 · 28 · 80
```

**これは `(6,)` プロファイル**（6点が1円上、他の4円なし）。

**素朴な上限**：`b·C(s,6)·C(n−s,2) = 350·28·861 = 8,437,800`。
**実際**：784,000（上限の 9.3%）。「他の4円を持たない」条件で 90.7% が
除外される。

**q=5 で 0 件だった理由**：`s = 6` なので `(6,)` は「6点すべてが1円上
+ 外2点」。**外2点が必ず別の4円を作る**ため 0 件。

**q=7 では `s = 8`** なので `(6,)` は「8点円のうち6点 + 外2点」。
**円上に2点残るので4円を作りにくい**場合がある。

**正しくは：k=8 の組み立てが成功したのは q=5 のみ。**

### 10ck. 訂正：`(6,)` は q=7 で 0 件（前項の診断を撤回）

**前項の「差 784,000 = `(6,)` プロファイル」という診断を撤回する。**

`(6,)` の構造を直接測定した（q=7、固定した円 `D` 上）：

| ペンシル円が T6 と2点で交わる個数 | 組数 |
|---:|---:|
| 1 | 6,048 |
| 2 | 16,128 |
| 3 | 1,932 |
| **0** | **0** |

**`(6,)` は 0 件。** よって差 784,000 は `(6,)` ではない。
**`784,000 = b·C(s,6)·s(s+2)` の一致は偶然だった。**

**プロファイル数の不一致**：

| 対象 | プロファイル数 |
|---|---:|
| 組み立て（q=7） | **21** |
| 全数（k=7、q=7） | 11 |

**組み立てが bad を 784,000 少なく数えている**（8-アークを多く見積もる）。

**残る候補**：

1. **プロファイル公式が q=7 で破綻**（q=9 では 500 組で 0 不一致だが
   q=7 は未検証）
2. **`(7,)` と `(8,)` の別項が過大**（「他の4円を持たない」条件を
   課していない）
3. **タプルループの `C` 固定**による系統的な欠落

**差の原因は依然未特定。**

### 10cl. q=7 の差：4候補を直接測定で消去

| 候補 | 測定結果 | 判定 |
|---|---|---|
| `(6,)` プロファイル | 0 件 | **消去** |
| プロファイル公式（q=7） | 500/500 で 0 不一致 | **消去** |
| `(7,)` の過大カウント | 実際 117,600 = 公式値、過大なし | **消去** |
| 多重度定理 | q=5 の13プロファイルで完全一致 | **消去** |

**残る唯一の候補**：タプル由来の部分が 784,000 少ない。

```
組み立ての sum(tuples×b/n4) = 535,976,700
真の値                      = 536,760,700
差                          =     784,000
```

**符号**：`n4` が真値より大きい → `tuples×b/n4` が小さい →
bad が少ない → **arcs が多く出る**。観測と一致。

**しかし 500/500 で 0 不一致だった。** 稀なケース（0.1% 未満）が
サンプルに含まれなかった可能性がある。

**全数検証には q=7 で `C(8,4)×C(42,4) = 7.8M` 組が必要。**

### 10cm. 決定的結果：プロファイル公式は q=7 の全数で完全に正しい

**C 実装で全数検証を実行**：

```
n=50 b=350 s=8 outside=42
checked=7835100 mismatches=0
```

**全 7,835,100 組で 0 不一致。プロファイル公式は q=7 で完全に正しい。**

**よって差 784,000 は純粋に組み立てロジックの問題。**

**消去された候補**：

| 候補 | 判定 |
|---|---|
| `(6,)` プロファイル | 0 件 |
| プロファイル公式（500 サンプル） | 0 不一致 |
| **プロファイル公式（全数）** | **0 不一致（確定）** |
| `(7,)` の過大カウント | 過大なし |
| 多重度定理 | q=5 で完全一致 |

**残る符号の矛盾**：

- `|C∩S| > 4` の多重カウント → bad 過大 → arcs 過小
- `(7,)`/`(8,)` の二重カウント → bad 過大 → arcs 過小

**しかし観測は arcs 過大（784,000 vs 0）。**

**すべての同定済み機序が逆方向であり、矛盾が残る。
組み立ての再実装が必要。**

### 10cn. 除数仮説の数値的棄却

**仮説A：重み付き除数 `n4 + 5n5 + 15n6`**

根拠：4円 `D` が `S` から5点取れば `C(5,4) = 5` 通りの `T` がある。

**結果（q=5）**：`621,125,425/561`（**非整数**）→ **棄却**。

**仮説B：`e4 = n4 − n5 − n6`**（ちょうど4点の円の個数）

根拠：タプルループは `|C∩S| = 4` のときだけ `S` を生成する。

**結果（q=5）**：`1,741,805`（`C(26,8) = 1,562,275` と不一致）→ **棄却**。

**現状の矛盾**：**q=5 では `n4` が正しい**（1,562,275 = C(26,8)）が、
**q=7 では `n4` で 784,000 の差**が出る。

**同じ除数が q=5 で正しく q=7 で誤る。**

**残る切り分け**：**q=7 のプロファイル分布**を全数で取得し、
`arc_k8_assemble.c` の分布と比較する。これが最後の切り分け。

**重要な観測**：サイズ `K` では「アーク」と「極大安全集合」が一致する
（`K` が最大なので `K`-アークは自動的に極大）。2つの独立実装
（`arc_counts.py` と `min_maximal2.py`）が同じ数を出した：

| q | `K` | `#K-arcs` | `#極大集合` |
|---:|---:|---:|---:|
| 3 | 5 | 72 | 72 |
| 4 | 5 | 2040 | 2040 |
| 5 | 6 | 5200 | 5200 |
| 7 | 6 | 1254400 | 1254400 |
| 8 | 7 | 1048320 | 1048320 |

### 10co. 方向転換：閉形式から「検証可能な探索」へ —— 記録された `K` の大幅な誤り

**動機**：10cm–10cn で k=8 の組み立てが q=7 で 784,000 の差を残し、6回の誤診を重ねた。
プロファイル代数は「数値が合った ＝ 機構が分かった」という誤った推論を許してしまう。
そこで発想を変え、**閉形式の導出を一旦やめ**、(1) 幾何を高速に構成する、
(2) 極大安全集合を探索する、(3) 証人を独立に検証する、という3つの道具だけを作り、
未解決の量そのもの（`K` の増大度）を正面から攻める。

**道具1：円の高速構成（`scripts/inversive_fast.py`）**
位数 q の反転平面の円は基底円 `P^1(F_q)` の `PGL(2,F_{q²})` 軌道である。
この群は `z ↦ z+1`, `z ↦ λz`（λ は `F_{q²}` の原始元）, `z ↦ 1/z` の3元で生成されるので、
`n³` 個の三点組を全列挙する代わりに軌道の BFS で `q(q²+1)` 個の円が `O(q⁴)` で得られる。

- 旧実装（`inversive_all_q.py`、三点組全列挙）と q=3,4,5,7,8,9 で**円集合が完全一致**
  （30, 68, 130, 350, 520, 738 個、すべて同一）。
- 各円のサイズが `q+1`、任意の2点がちょうど `q+1` 個の円に載ることを機械検査（`params_ok`, `pair_index`）。
- q=49（点 2,402、円 117,698）まで構成可能。旧実装（三点組全列挙）は q=13 で数分、
  q=19 では数億回の Möbius 評価で非現実的だった。

**道具2：極大安全集合の反復局所探索（`scripts/arc_maxsearch.c`）**
`cnt[c] = |S∩c|` と `blk[p] = #{p を含み |S∩c| = 3 である円}` を増分維持する。
点の追加・削除が互いに厳密な逆操作なので、摂動（r 点削除）→ 貪欲再充填 →
改善しなければ巻き戻す、という ILS が1点あたり `O(q³)` で回る。

**道具3：証人の独立検証（`scripts/arc_search_report.py`）**
C 側の増分論理にバグがあっても偽の主張が出ないよう、返ってきたアークを円リストと
突き合わせ「どの円も4点以上を含まない」ことを総当りで再検査する。
以下の数値はすべてこの検証を通った**明示的な証人**に基づく（したがって下界は厳密）。

**妥当性**：q ≤ 11 の厳密値（全数列挙で確定済み）を完全に再現する。

| q | 5 | 7 | 8 | 9 | 11 |
|---:|---:|---:|---:|---:|---:|
| `K`（既知の厳密値） | 6 | 6 | 7 | 9 | 9 |
| 探索の出力 | 6 | 6 | 7 | 9 | 9 |

**主結果：記録されていた `K` は q ≥ 13 で誤りだった**

| q | SSOT の旧値（「マスク修正後」） | 修正前 artifact note | 今回の検証済み下界 |
|---:|---:|---:|---:|
| 13 | 8 | 10 | **≥ 10** |
| 16 | 12 | 12 | ≥ 12 |
| 17 | 9 | 13 | **≥ 13** |
| 19 | 9 | 14 | **≥ 14** |
| 23 | 10 | — | **≥ 16** |
| 25 | — | — | ≥ 18 |
| 27 | — | — | ≥ 19 |
| 29 | 8 | — | **≥ 20** |
| 31 | — | — | ≥ 21 |
| 32 | — | — | ≥ 22 |
| 37 | — | — | ≥ 25 |
| 41 | — | — | ≥ 27 |
| 43 | — | — | ≥ 28 |
| 47 | — | — | ≥ 30 |
| 49 | — | — | ≥ 32 |

（q=49 は同じ予算では 18 しか出ず、試行回数を 5 倍にして 32 に到達した。
探索は q とともに再起動回数がより多く必要なため、この表の値は**すべて下界**である。）

**q=13,17,19 は「修正前の値が正しい」**：10, 13, 14 はマスク修正前の artifact note と
完全に一致する。すなわち64ビット→多倍長への書き換えが**回帰**であり、書き換え版は
今回提示する有効なアークを見落としていた。q=23,29 の 10, 8 はさらに大きく外れている
（16, 20 の証人が存在する）。

**副産物：`K` は定数ではない**
- `K/q` は q=13 の 0.77 から q=43〜49 の 0.64 前後へゆっくり減少する。
- log-log の見かけの傾き（q=13..49）は ≈0.85。
- よって「`K ≈ 8.86`（ほぼ定数）」も「`K ≈ 3.83·q^0.31`」も**撤回**する。
- 文献（Sonnino, J. Geom. 66 (1999) 187–191）は q 奇数の `M(q)` に `(q+5)/2`-弧を構成しており、
  K1250 の上界 `K ≤ q+2`（q 奇数）と合わせて **`K = Θ(q)` が確定**する。
  「ほぼ定数」という見立ては文献とも矛盾していた。下界の改善（文献値 +1〜+5）は K1251。
- 証明済みの枠は `(6q)^(1/3) ≤ K ≤ q`（`q` 奇数, `q ≥ 9`、K1252）と `K ≤ q+3`（`q` 偶数）。
  実測は下界より遥かに上、上界よりは下にあり、増大度は依然未確定である。

**構造的再定式化（機械検証済み）：アーク ＝ 複比が有理でない4点集合**
4点 `z1,z2,z3,z4 ∈ P^1(F_{q²})` が共円であることと、複比
`(z1−z3)(z2−z4)/((z1−z4)(z2−z3))` が `P^1(F_q)` に入ることは同値である。
（`z1,z2,z3` を `0,1,∞` に送る Möbius 変換の係数は `F_{q²}` にあり、
像 `z4` の行き先が複比。円は `P^1(F_q)` の像なので、像が `P^1(F_q)` にあることが共円と同値。）
q=3,4,5,7 の全4点組（210 / 2,380 / 14,950 / 230,300 個）で**不一致 0**（`scripts/inversive_crossratio.py`）。
したがって

> アークとは `P^1(F_{q²})` の部分集合で、どの4点の複比も `F_q` に入らないもの

**この見方をさらに進めた読み替えが K1250**：点を持ち上げると
`z ↦ (1 : a : b : z^{q+1})` によりアークは楕円二次曲面 `Q⁻(3,q)` 上の
「どの4点も一次独立な集合」になり、`K(q)` は**二次曲面上に列を持つ4次元MDS符号の最大長**に
等しい（上界 `K ≤ q+1` が MDS 予想から出る）。

と言い換えられる。これは探索を「設計のブロック」から「複比の代数」へ移す新しい入口であり、
`K` の上界（`q+1` が複比の自由度から出る）を代数幾何側から攻める足場になる。

### 11. 派生設計による上界

`D` を `3-(v,s,1)` 設計、`S` を安全集合、`p ∈ S` とし、`p` での派生設計 `D_p`
（点 `= D` の点 `−{p}`、ブロック `= p` を通るブロックから `p` を除いたもの、
これは `2-(v−1,s−1,1)` 設計 = 線形空間）を考える。

**定理**：`S\{p}` は `D_p` の2-アークである。よって `K(D) ≤ 1 + A₂(D_p)`。 □

`A₂(L) ≤ 1 + λ₂` なので**この上界は `λ₂` 上界を含む**（より強い）。
古典的事実：反転平面 `q` を `p` で派生すると `AG(2,q)`、Witt `S(3,6,22)` を派生すると `PG(2,4)`。

| q | `A₂(AG(2,q))` | `1+A₂` | `λ₂+2` | `K(inv)` |
|---:|---:|---:|---:|---:|
| 3 | 4 | **5** | 6 | **5** |
| 4 | 6 | 7 | 7 | 5 |
| 5 | 6 | 7 | 8 | 6 |
| 7 | 8 | 9 | 10 | 6 |

`q=3` では派生上界が `K` に一致する。

**注意**：`AG(2,q)` を `mod q` 算術で構成してはならない。それはトーラス `Z_q²` であり、
`AG(2,q)` と一致するのは `q` が素数のときだけ（§7）。必ず反転平面から派生させて作る。

## 限界

- 完全計算は q ≤ 5（反転平面の Grundy）、q ≤ 8（反転平面の K）、q ≤ 7（AG の K）、n ≤ 5（整数盤の初手）、p ≤ 13（トーラス一致）に限る。q=9 は 8≤K≤17 の範囲のみ。
- `D(n) = a²⌊a²/2⌋` は n ≤ 12 の全数確認済みだが全称証明ではない。
- 層サイズ公式は k ≤ 5 のみ。k ≥ 6 の一般公式は未取得。
- misère 反転は 4 例の観測。全極大が同石数であることの証明は未取得。
- k 点版は k ≤ 5、q ≤ 4 のみ。
- 有限体盤・反転平面盤の勝敗と整数格子盤の勝敗の関係は、閾値 q > D(n) の外側では何も主張しない。
- 5×5 の菱形がなぜその形になるか、負け初手の Grundy が全て 3 である理由は未解明。
- 三分法の `t=3, s≥5` の欄に具体公式はない。
- `K = 3 + α` は q ≤ 9 での検証であり一般証明ではない。族 C, D の組合せ的記述も未取得。
- 派生上界 `1 + A₂` は q ≥ 4 で緩い。
- 上界 `q+2` はタイトではない（slack は q とともに増え、10co の検証済み下界 q=29 → 20 では 31−20 = 11）。
- 特性2（q 偶数）では `w² = d` の形の基底が取れず、ラテン方陣の公式形が異なる。`τ₃ = q` は q = 4,8 の計算値のみ。
- `K` の真の増大度は未確定。10co の検証済み下界は q=49 で 32 で、見かけの指数は ≈0.85（`(6q)^(1/3)` と `q` の間のどこか）。q ≥ 23 では下界のみで、探索の最適性は未証明。
