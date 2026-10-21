# K項目一覧

| ID | 知識 | kind | status | topics |
|---|---|---|---|---|
| [K0001](../items/K0001-complete-call-rules.md) | 完全指摘ルールの共円ゲームと安全局面 | definition | active | rules |
| [K0002](../items/K0002-grundy-and-first-move-conventions.md) | Grundy数・P/Nと勝ち初手の向き | definition | active | rules, grundy, first-moves |
| [K0003](../items/K0003-solution-and-evidence-levels.md) | 解決段階と計算・証明書・監査の区別 | definition | active | rules, verification |
| [K0004](../items/K0004-n1-n6-all-safe-grundy.md) | 1×1〜6×6の全安全局面Grundy分類 | computation | computed | grundy, square-outcomes |
| [K0005](../items/K0005-n7-all-safe-grundy-audit.md) | 7×7の全安全局面Grundy・P/N分類と独立監査 | computation | computed | grundy, square-outcomes, verification |
| [K0006](../items/K0006-n8-all-safe-grundy-computed.md) | 8×8の全6,700,711,937安全局面をGrundy DPで完全計算 | computation | computed | grundy, square-outcomes, verification |
| [K0007](../items/K0007-ranked-and-or-certificates.md) | 順位付きAND/OR証明書の局所条件と健全性 | method | active | certificates |
| [K0008](../items/K0008-n1-n9-independent-cpp-certificate-checks.md) | 1×1〜9×9証明書の独立C++全件検査 | verification | verified | certificates, verification |
| [K0009](../items/K0009-lean-soundness-trust-boundary.md) | Lean形式化の範囲と具体証明書の信頼境界 | verification | verified | formalization, certificates |
| [K0010](../items/K0010-kyoenc4-selected-position-certificates.md) | KYOENC4による128-bit局面証明とRust独立検査 | method | active | certificates, verification, search-methods |
| [K0011](../items/K0011-n1-first-player-win.md) | 1×1は先手必勝 | proposition | proved | square-outcomes |
| [K0012](../items/K0012-n2-first-player-win.md) | 2×2は先手必勝 | proposition | proved | square-outcomes |
| [K0013](../items/K0013-n3-first-player-win.md) | 3×3は先手必勝 | proposition | proved | square-outcomes |
| [K0014](../items/K0014-n4-second-player-win.md) | 4×4は後手必勝 | proposition | proved | square-outcomes |
| [K0015](../items/K0015-n5-first-player-win.md) | 5×5は先手必勝 | proposition | proved | square-outcomes |
| [K0016](../items/K0016-n6-first-player-win.md) | 6×6は先手必勝 | proposition | proved | square-outcomes |
| [K0017](../items/K0017-n7-second-player-win.md) | 7×7は後手必勝 | proposition | proved | square-outcomes |
| [K0018](../items/K0018-n8-second-player-win.md) | 8×8は後手必勝 | proposition | proved | square-outcomes |
| [K0019](../items/K0019-n9-first-player-win.md) | 9×9は先手必勝 | proposition | proved | square-outcomes |
| [K0020](../items/K0020-n10-second-player-win.md) | 10×10は後手必勝 | proposition | proved | square-outcomes |
| [K0021](../items/K0021-n9-all-81-first-moves-win.md) | 9×9では81個すべての初手が先手勝ち | computation | computed | first-moves, square-outcomes |
| [K0022](../items/K0022-n10-all-100-first-moves-classified.md) | 10×10の100初手完全分類と検証境界 | computation | computed | first-moves, square-outcomes, verification |
| [K0023](../items/K0023-n11-exact-safe-layers-and-unknown-winner.md) | 11×11は勝敗未確定、層0〜5の安全局面数は厳密 | computation | computed | square-outcomes, verification |
| [K0024](../items/K0024-fixed-width-q-point-threshold.md) | q点版固定幅盤の十分長さ定理 | proposition | proved | rectangles, grundy, variants |
| [K0025](../items/K0025-q-above-two-width-all-lengths.md) | q>2wでは全長の固定幅盤が分離し強解決 | proposition | proved | rectangles, variants, grundy |
| [K0026](../items/K0026-maximum-versus-minimum-maximal.md) | 最大安全サイズK_nと最小極大サイズs_nは別の量 | definition | active | maximum-safe, maximal-safe |
| [K0027](../items/K0027-two-n-minus-one-conjecture-refuted.md) | 全正方形盤でK_n=2n−1という仮説は反証済み | proposition | refuted | maximum-safe |
| [K0028](../items/K0028-n11-truncated-dp-winner-withdrawn.md) | 11×11先手必勝という打切りDP由来の旧結論は撤回 | proposition | withdrawn | square-outcomes, provenance |
| [K0029](../items/K0029-n1-n9-maximum-safe-sizes.md) | 1×1〜9×9の最大安全サイズの既知値 | proposition | computed | maximum-safe |
| [K0030](../items/K0030-n3-n6-maximal-safe-size-distributions.md) | 3×3〜6×6の極大安全集合サイズ分布 | proposition | computed | maximal-safe |
| [K0031](../items/K0031-n7-minimum-maximal-size.md) | 7×7の最小極大安全サイズs_7=7 | proposition | proved | maximal-safe |
| [K0032](../items/K0032-n8-minimum-maximal-size.md) | 8×8の最小極大安全サイズs_8=8 | proposition | proved | maximal-safe |
| [K0033](../items/K0033-n9-minimum-maximal-size.md) | 9×9の最小極大安全サイズs_9=9 | proposition | proved | maximal-safe |
| [K0034](../items/K0034-n10-minimum-maximal-bounds.md) | 10×10の最小極大安全サイズはs_10=10 | proposition | proved | maximal-safe |
| [K0035](../items/K0035-n10-maximum-safe-bounds.md) | 10×10の最大安全サイズは19≤K_10≤23 | proposition | proved | maximum-safe |
| [K0036](../items/K0036-n10-local-19-stone-exchange-limit.md) | 特定19石証人から九石交換以内では安全20石に届かない | proposition | computed | maximum-safe |
| [K0037](../items/K0037-unsafe-maximal-search-witnesses-withdrawn.md) | 安全判定を欠いた極大探索の陽例と境界偏在説は無効 | proposition | withdrawn | maximal-safe, provenance |
| [K0038](../items/K0038-n10-safe-10-stone-maximal-witness.md) | 10×10には安全な十石極大配置が存在する | proposition | proved | maximal-safe |
| [K0039](../items/K0039-n9-17-stone-maximum-conjecture-refuted.md) | K_9=17という旧仮説は18石安全証人により反証 | proposition | refuted | maximum-safe |
| [K0040](../items/K0040-n6-all-maximal-11-stone-claim-refuted.md) | 6×6の極大は全て11石という主張は反証済み | proposition | refuted | maximal-safe |
| [K0041](../items/K0041-grundy-ceiling-and-saturation.md) | Grundy天井・欠損単調性と一度の飽和による全後続層飽和 | proposition | proved | grundy |
| [K0042](../items/K0042-n7-grundy-saturation-layer.md) | 7×7のGrundy飽和開始層はσ_7=4 | proposition | proved | grundy |
| [K0043](../items/K0043-n5-first-move-pattern-and-nimbers.md) | 5×5の勝ち初手は市松偶色から四隅を除く9点、負け初手後のgは3 | proposition | computed | first-moves, grundy |
| [K0044](../items/K0044-n9-certificate-terminal-nodes.md) | 公開9×9証明書の末端は16石WIN十個から17石飽和LOSS一個へ閉じる | proposition | computed | certificates, maximal-safe |
| [K0045](../items/K0045-certificate-depth-versus-maximum-size.md) | 証明書最深石数は最大安全サイズを一般に与えない | proposition | computed | certificates, maximum-safe |
| [K0046](../items/K0046-certificate-parity-law.md) | 証明書の石数パリティとWIN/LOSS分離は形式の帰結 | proposition | proved | certificates, provenance |
| [K0047](../items/K0047-witness-chain-versus-game-length.md) | 証明書のWIN証人鎖の長さは対局長ではない | proposition | computed | certificates |
| [K0048](../items/K0048-n1-n6-fixed-certificate-terminal-sizes.md) | 1×1〜6×6証明書の固定witness戦略での終局石数 | proposition | computed | strategy-length, certificates |
| [K0049](../items/K0049-tstar-and-wft-terminal-guarantees.md) | 勝敗維持終局集合T*と固定長強制集合WFTの区別・偶奇則 | proposition | proved | strategy-length |
| [K0050](../items/K0050-fixed-terminal-guarantee-refuted.md) | 勝者が終局石数を事前宣言して必ず勝てるという仮説は7×7で偽 | proposition | refuted | strategy-length |
| [K0051](../items/K0051-n7-maximum-configurations-two-phases.md) | 7×7最大14石族は16配置・二つのD4相に完全分類される | proposition | computed | maximum-safe, reconfiguration |
| [K0052](../items/K0052-n7-a-b-reconfiguration-widths.md) | 代表A–B変形の幅は全盤12、和集合U内11 | proposition | computed | reconfiguration, maximum-safe |
| [K0053](../items/K0053-d4-orbit-circle-capacities.md) | D4点軌道内の共円性と軌道占有容量 | proposition | proved | geometry, maximum-safe |
| [K0054](../items/K0054-collinear-quadruple-asymptotics.md) | 共線四点組数D_nの主項はn^5、次項は負のn^4 log n | proposition | proved | geometry |
| [K0055](../items/K0055-sixth-order-quadruple-claim-refuted.md) | 共線・共円ともΘ(n^6)という旧外挿は反証・訂正済み | proposition | refuted | geometry, provenance |
| [K0056](../items/K0056-cocircular-quadruple-asymptotics.md) | 非共線共円四点組数C_nはΘ(n^5) | proposition | proved | geometry |
| [K0057](../items/K0057-forbidden-quadruple-counts.md) | 禁止四点組の有限総数と共線・共円の排他的分解 | proposition | computed | geometry |
| [K0058](../items/K0058-fk-circle-maxima-scope-audited.md) | F-K旧走査は半整数中心に限定、n≤112の全中心最大値は後続計算で確定 | verification | verified | geometry, provenance |
| [K0059](../items/K0059-odd-two-square-representation-formula.md) | 奇二平方和表現数odd_repr(2m)の完全公式 | proposition | proved | geometry |
| [K0060](../items/K0060-circle-point-floor-formula-refuted.md) | 最大円点数の暫定式4(⌊n/4⌋+1)はn=16で偽 | proposition | refuted | geometry |
| [K0061](../items/K0061-twelve-point-circle-count-formula.md) | 12点円の個数(n−7)^2はn=11で全円を数えなくなる | proposition | computed | geometry |
| [K0062](../items/K0062-twelve-point-circle-radius-families.md) | 12点円の半径族分解と有限盤窓での切断 | proposition | computed | geometry |
| [K0063](../items/K0063-n10-circle-catalogue.md) | 10×10の非退化円カタログとサイズ欠落 | proposition | computed | geometry |
| [K0064](../items/K0064-n9-n10-maximum-point-degrees.md) | 9×9と10×10の危険四点組への点次数最大位置は異なる | proposition | computed | geometry |
| [K0065](../items/K0065-n10-two-three-stone-d4-orbits.md) | 10×10の二石・三石D4軌道は120・680 | proposition | computed | geometry |
| [K0066](../items/K0066-n10-three-stone-completions.md) | 10×10の三点補完数は最大9で8を欠き、三石mobility=97−補完数 | proposition | computed | geometry |
| [K0067](../items/K0067-triple-completion-cover-bound.md) | 三点補完被覆による小さい極大集合の必要条件 | proposition | proved | maximal-safe, geometry |
| [K0068](../items/K0068-standard-fixed-width-parity-threshold.md) | 標準q=4固定幅盤はm≥3+2{C(3w−2,3)−(w−1)}で全局面偶奇式 | proposition | proved | rectangles, grundy |
| [K0069](../items/K0069-two-row-all-lengths-strong-solution.md) | 標準二行盤は全mで強解決、m≥6の空盤は後手勝ち | proposition | proved | rectangles, grundy |
| [K0070](../items/K0070-width-three-q6-stabilization.md) | 3×m・q=6の真の満容量安定化長M_{3,6}=9 | proposition | proved | rectangles, variants, grundy |
| [K0071](../items/K0071-width-three-q5-exact-stabilization.md) | 3×m・q=5の真の満容量安定化長はM_{3,5}=12 | proposition | proved | rectangles, variants, grundy |
| [K0072](../items/K0072-mod9-integer-row-separation.md) | 標準整数行の合同条件は高q全長分離領域を拡大する | proposition | proved | rectangles, geometry, variants |
| [K0073](../items/K0073-q-two-width-circle-criterion.md) | q=2w共円の一般必要十分条件は行ペア和一致と積の二階差 | proposition | proved | geometry, rectangles |
| [K0074](../items/K0074-single-forbidden-type-variants.md) | 片禁止q点変種の全長強解決定理 | proposition | proved | variants, rectangles |
| [K0075](../items/K0075-line-only-all-lengths-solution.md) | line-onlyはq>wで全m強解決 | proposition | proved | variants, rectangles, grundy |
| [K0076](../items/K0076-circle-only-all-points-legal.md) | circle-onlyはq>2wで全未占有点が合法 | proposition | proved | variants, rectangles, grundy |
| [K0077](../items/K0077-width-four-q8-stabilization.md) | 4×m・q=8の真の満容量安定化長はM_{4,8}=11 | proposition | proved | rectangles, variants, grundy |
| [K0078](../items/K0078-width-three-q5-intermediate-range-closed.md) | 3×m・q=5のm=22..39にも不足極大安全集合は存在しない | proposition | computed | rectangles, variants |
| [K0079](../items/K0079-600-original-claims-audit-boundary.md) | 600原文の監査状態と弱化版作業ラベルは別の量 | verification | verified | migration, provenance |
| [K0080](../items/K0080-n10-subset-csv-coordinate-frame.md) | 10×10 subset CSVのstateは入力座標で、D4正規形とは限らない | proposition | computed | provenance |
| [K0081](../items/K0081-loss-core-d4-invariant-refuted.md) | H1/H2のLOSS共通コアをD4不変構造とみなす仮説は偽 | proposition | refuted | residual-games, provenance |
| [K0082](../items/K0082-n10-three-stone-degree-cost-correlation.md) | 10×10の3石探索コストとΣdの負相関は固定R内限定 | proposition | observed | statistics, search-methods |
| [K0083](../items/K0083-fixed-r-four-stone-loss-separation.md) | R内4石のΣdとLOSS分離、二石順位の旧記述は訂正済み | proposition | observed | statistics |
| [K0084](../items/K0084-outside-r-loss-trend-full-width-memo.md) | R外4石36局面のΣd→LOSS方向は全幅memo再求解でも維持 | proposition | observed | statistics, verification |
| [K0085](../items/K0085-three-to-four-stone-pair-gain.md) | 3→4石ではpair gainはunique gainに一致、4石以降は一般に過大計数 | proposition | proved | geometry, search-methods |
| [K0086](../items/K0086-blind-probe-median-improvement-withdrawn.md) | 旧blind probe中央値3対6の改善主張は対象盤と累積memoの訂正で撤回 | proposition | withdrawn | search-methods, statistics |
| [K0087](../items/K0087-n9-factorial-holm-comparisons.md) | 9×9 pair成分factorial四比較はHolm補正後いずれも棄却なし | proposition | observed | statistics, search-methods |
| [K0088](../items/K0088-n9-factorial-membership-versus-interaction.md) | 9×9 factorial全体符号差は共有親interactionよりmembership差に由来 | proposition | observed | statistics |
| [K0089](../items/K0089-n8-replication-of-n9-o-strata.md) | 9×9 O0-only正方向の構造仮説は8×8全censusへ再現しなかった | proposition | observed | statistics, verification |
| [K0090](../items/K0090-n10-cache-aware-capacity-rerun.md) | 10×10 cache-aware below-root改善は容量再実行の固定12親で確認 | proposition | observed | search-methods, statistics |
| [K0091](../items/K0091-d9-memo-read-mask-logical-epoch.md) | D9 one-shot memo read-maskは物理slot書換えでなく論理epochが必要 | proposition | proved | search-methods, provenance |
| [K0092](../items/K0092-n11-dfpn-search-status.md) | 11×11 DFPN hybridの局所完了と回帰は空盤勝敗を閉じていない | proposition | observed | search-methods, verification |
| [K0093](../items/K0093-coordinate-three-ply-information.md) | 同一盤の座標付き三手合法性は全継続ゲームを決める | proposition | proved | residual-games |
| [K0094](../items/K0094-n5-relocation-preserves-two-ply-changes-grundy.md) | 二手情報を保つ一石移動で5×5のgが0から3へ変わる | proposition | proved | residual-games, grundy |
| [K0095](../items/K0095-split-prime-safe-quadratic-construction.md) | p≡1 mod4の全素数に安全p点の有限体二次構成がある | proposition | proved | maximum-safe, geometry |
| [K0096](../items/K0096-mod-prime-quadratic-certification-bound.md) | 二次パラメータmodp非零認証の最大はp≡3 mod4で(p+13)/4 | proposition | proved | maximum-safe, geometry |
| [K0097](../items/K0097-integer-residue-parabola-bounds.md) | 整数剰余放物線の安全最大は高々(p+3)/2、5..2000では等号 | proposition | proved | maximum-safe, geometry |
| [K0098](../items/K0098-p23-half-interval-counterexample.md) | 剰余放物線の前半区間安全説はp=23で反例 | proposition | refuted | maximum-safe, geometry |
| [K0099](../items/K0099-private-passes-terminal-pass-allowed.md) | 終端パス可の有限私有パス版は残数差と通常gで勝敗・mexを分類 | proposition | proved | variants, grundy |
| [K0100](../items/K0100-private-passes-immediate-terminal.md) | 通常終端即終了の私有パス版は一手終端可能性も必要 | proposition | proved | variants, grundy |
| [K0101](../items/K0101-prime-parabola-equality-open.md) | 全奇素数で剰余放物線上界(p+3)/2が達成されるかは未確定 | question | open | maximum-safe, geometry |
| [K0102](../items/K0102-concrete-lean-certificate-checker-open.md) | 具体巨大証明書をLean核のみで検査する実装は未完成 | question | open | formalization, certificates |
| [K0103](../items/K0103-n10-single-empty-root-certificate-open.md) | 10×10空盤面全体の単一KYOENC4証明書は未統合 | question | open | certificates, verification |
| [K0104](../items/K0104-prior-work-search-scope.md) | 先行研究・初出主張は2026-09-23調査範囲に限定 | proposition | observed | provenance |
| [K0105](../items/K0105-n11-empty-root-winner-open.md) | 11×11の真の空盤勝敗は現在の主要未解決問題 | question | open | square-outcomes |
| [K0106](../items/K0106-minimum-maximal-exponent-lower-bound.md) | 固定qの最小極大サイズには漸近指数下界2/3がある | proposition | proved | maximal-safe, geometry, variants |
| [K0107](../items/K0107-sharp-point-cover-bound.md) | 安全k石の一空点被覆はk≥4で二次上限から必ず1減る | proposition | proved | geometry, maximal-safe |
| [K0108](../items/K0108-residual-hypergraph-versus-pair-graph.md) | 残余禁止hypergraphは継続ゲームを表し、二点グラフだけでは足りない | definition | active | residual-games, grundy |
| [K0109](../items/K0109-n7-n9-certificate-loss-ratios.md) | 7〜9×9公開証明書のLOSS比34〜35%は三サイズの観測 | proposition | observed | certificates, statistics |
| [K0110](../items/K0110-certificate-compression-finite-comparison.md) | 公開証明書と探索記録の圧縮比はn1〜9で有限比較できる | proposition | computed | certificates, search-methods |
| [K0111](../items/K0111-n5-minimal-maximal-first-move-cells.md) | 5×5の5石極大四配置は各々勝ち初手セル4・負け初手セル1を含む | proposition | computed | maximal-safe, first-moves |
| [K0112](../items/K0112-random-greedy-versus-minimum-maximal.md) | 乱貪欲の最小観測サイズは真の最小極大サイズと一致しない | proposition | observed | maximal-safe, search-methods |
| [K0113](../items/K0113-losing-first-move-odd-nimber-open.md) | 負け初手後のnimberは奇数 | question | open | residual-games, first-moves |
| [K0114](../items/K0114-j5-nonisolated-connectivity.md) | 5×5のJ_5の非孤立部分は連結 | proposition | computed | residual-games, first-moves |
| [K0115](../items/K0115-j5-short-cycle-generation-refuted.md) | 5×5のJ_5は短いサイクルだけで生成される | proposition | refuted | residual-games, first-moves |
| [K0116](../items/K0116-j5-automorphisms-beyond-d4-refuted.md) | J_5の自己同型にはD4以外のものがある | proposition | refuted | residual-games, first-moves |
| [K0117](../items/K0117-j5-bipartiteness-refuted.md) | J_5の非孤立部分は二部グラフ | proposition | refuted | residual-games, first-moves |
| [K0118](../items/K0118-j5-perfect-matchings.md) | J_5の非孤立部分に完全マッチングがある | proposition | computed | residual-games, first-moves |
| [K0119](../items/K0119-jn-losing-board-connectivity-open.md) | 後手勝ち正方形盤のJ_nは連結 | question | open | residual-games, first-moves |
| [K0120](../items/K0120-same-two-stone-p-graph-different-higher-outcomes.md) | 二石Pグラフが同じでも高層の勝敗は違う盤 | proposition | computed | residual-games, first-moves |
| [K0121](../items/K0121-uniform-saturation-by-layer-four-open.md) | 飽和開始は4石以内 | question | open | grundy |
| [K0122](../items/K0122-tstar-parity-hole-claim-refuted.md) | T*(S)に同じ偶奇の穴は開かない | proposition | refuted | strategy-length, grundy |
| [K0123](../items/K0123-pair-only-symmetric-p-involution-claim-refuted.md) | 2点制約だけの対称P局面は対合証明を持つ | proposition | refuted | residual-games, reconfiguration |
| [K0124](../items/K0124-same-residual-game-exchange-connectivity-refuted.md) | 同じ残余ゲームを与える占有集合は交換でつながる | proposition | refuted | residual-games, reconfiguration |
| [K0125](../items/K0125-three-stone-p-graph-three-colorability-refuted.md) | 三石局面のP(S)の彩色数は3以下 | proposition | refuted | residual-games, reconfiguration |
| [K0126](../items/K0126-first-four-stone-conflict-types.md) | 四石以降で初めて現れる競合グラフの最小型がある | proposition | proved | residual-games, reconfiguration |
| [K0127](../items/K0127-tree-p-graph-higher-constraints-change-outcome.md) | P(S)が木でも高階制約が勝敗を変える | proposition | computed | residual-games, reconfiguration |
| [K0128](../items/K0128-empty-p-graph-high-nimber.md) | P(S)が空でも高nimberを持つ | proposition | computed | residual-games, reconfiguration |
| [K0129](../items/K0129-late-p-graph-induced-odd-cycles-refuted.md) | 終盤のP(S)には大きな誘導奇サイクルがない | proposition | refuted | residual-games, reconfiguration |
| [K0130](../items/K0130-same-p-degree-spectrum-different-outcome.md) | 同じP(S)の次数列・スペクトルでも勝敗が違う | proposition | computed | residual-games, reconfiguration |
| [K0131](../items/K0131-finite-forbidden-conflict-types.md) | 実現できる競合グラフには有限の小さい禁止型がある | proposition | proved | residual-games, reconfiguration |
| [K0132](../items/K0132-point-cover-triples-form-linear-family.md) | 一つの禁止点を作る三つ組族は線形 | proposition | proved | maximal-safe, geometry |
| [K0133](../items/K0133-quadratic-point-cover-bound.md) | 点ごとの被覆重複には二次上限がある | proposition | proved | maximal-safe, geometry |
| [K0134](../items/K0134-point-cover-bound-equality-witness.md) | B072に等号を達成する非自明な配置 | proposition | refuted | maximal-safe, geometry |
| [K0135](../items/K0135-linear-point-cover-bound-refuted.md) | 幾何によりB072より厳しい線形上限がある | proposition | refuted | maximal-safe, geometry |
| [K0136](../items/K0136-triple-completion-overlap-bound.md) | 二つの三つ組補完集合の重複は小さい | proposition | proved | maximal-safe, geometry |
| [K0137](../items/K0137-maximal-all-empty-points-multiply-covered.md) | 極大なのにすべての空点が二重以上に禁止される | proposition | computed | maximal-safe, geometry |
| [K0138](../items/K0138-minimum-maximal-single-cover-refuted.md) | 全nの最小極大配置に一重被覆点があるというB078はn=1で偽 | proposition | refuted | maximal-safe, geometry |
| [K0139](../items/K0139-six-stone-exclusion-short-cover-proof-open.md) | 六石非存在は三つ組の共起だけで短く説明できる | question | open | maximal-safe, geometry |
| [K0140](../items/K0140-maximal-single-cover-all-empty-points.md) | 全空点をちょうど一度ずつ禁止する極大配置 | proposition | computed | maximal-safe, geometry |
| [K0141](../items/K0141-n10-20-stone-existence-open.md) | 10×10では20石まで届くか | question | open | maximum-safe, geometry |
| [K0142](../items/K0142-maximum-configuration-boundary-extension.md) | 既存最大配置に外周を足すだけでは次の最大へ届かない | proposition | computed | maximum-safe, geometry |
| [K0143](../items/K0143-asymptotic-two-n-safe-construction-open.md) | 2n−O(1)石の安全配置を無限族で作れる | question | open | maximum-safe, geometry |
| [K0144](../items/K0144-few-algebraic-curves-optimality-refuted.md) | 少数の代数曲線の和で漸近最適になる | proposition | refuted | maximum-safe, geometry |
| [K0145](../items/K0145-n10-minimum-maximal-ten-open.md) | 10×10の最小極大は10石 | question | superseded | maximal-safe, geometry |
| [K0146](../items/K0146-n10-minimum-maximal-eleven-refuted.md) | 10×10の最小極大は11石 | proposition | refuted | maximal-safe, geometry |
| [K0147](../items/K0147-sublinear-minimum-maximal-open.md) | 最小極大は線形より小さくなる | question | open | maximal-safe, geometry |
| [K0148](../items/K0148-minimum-maximal-exponent-two-thirds-open.md) | 最小極大の指数は2/3 | question | open | maximal-safe, geometry |
| [K0149](../items/K0149-minimum-maximal-monotonicity-open.md) | s_nは単調増加する | question | open | maximal-safe, geometry |
| [K0150](../items/K0150-minimum-maximal-jump-by-two.md) | s_nが一段の拡大で2以上増える | proposition | computed | maximal-safe, geometry |
| [K0151](../items/K0151-fourth-order-cocircular-count-refuted.md) | 非共線共円四点組はn^(4+o(1)) | proposition | refuted | geometry |
| [K0152](../items/K0152-primitive-direction-leading-constant.md) | 共線数の主項定数を原始方向の収束級数で書ける | proposition | proved | geometry |
| [K0153](../items/K0153-fixed-similarity-types-negligible.md) | 固定個数の相似型では大盤の大半を覆えない | proposition | proved | geometry |
| [K0154](../items/K0154-width-three-eventual-periodicity.md) | 幅3で既に最終周期性が破れる | proposition | refuted | rectangles, variants |
| [K0155](../items/K0155-fixed-width-infinitely-partial-first-moves-refuted.md) | 固定幅でも部分勝ち初手盤は無限にある | proposition | refuted | rectangles, variants |
| [K0156](../items/K0156-rectangle-boundary-first-move-classification.md) | 長方形の例外初手は端からの距離で分類できる | proposition | proved | rectangles, variants |
| [K0157](../items/K0157-few-circles-preserve-first-move-pattern.md) | 少数の円だけで標準版の初手分類を再現できる | proposition | computed | variants |
| [K0158](../items/K0158-equal-private-passes-grundy-claim-refuted.md) | 一回だけパスできる版はgだけでは分類できない | proposition | refuted | variants |
| [K0159](../items/K0159-circle-size-rule-relaxation-nonmonotonicity.md) | 円の点数に応じた禁止緩和が非単調な勝敗列を作る | proposition | computed | variants |
| [K0160](../items/K0160-single-rule-removal-winner-flip-open.md) | 禁止四点組一つを外すだけで空盤勝者が反転する | question | open | variants |
| [K0161](../items/K0161-whole-circle-versus-scattered-removal.md) | 円一つの禁止解除が、同数のばらばらな解除より強く効く | proposition | computed | variants |
| [K0162](../items/K0162-joint-rule-removal-synergy.md) | 各禁止を単独解除しても不変だが同時解除で反転する | proposition | computed | variants |
| [K0163](../items/K0163-same-maximum-configurations-different-winner.md) | 最大配置の分類を完全保存しても勝者は変わる | proposition | computed | variants |
| [K0164](../items/K0164-minimal-winner-preserving-rules-d4-asymmetry-refuted.md) | 勝者を保つ最小禁止族はD4非対称である | proposition | refuted | variants |
| [K0165](../items/K0165-mandatory-rule-types-refuted.md) | n≥4の最小勝敗保持禁止族に共通必須D4型があるというB258は偽 | proposition | refuted | variants |
| [K0166](../items/K0166-two-move-blocking-synergy.md) | 一手ずつは弱いが二手そろうと大量に塞ぐ | proposition | proved | geometry |
| [K0167](../items/K0167-residual-triples-two-move-synergy.md) | 二手相乗作用を少数の残余三点制約で表せる | proposition | proved | geometry |
| [K0168](../items/K0168-j5-detoured-square-structure.md) | J_5は四角形の各辺に長さ4の迂回路を添えたグラフ | proposition | computed | residual-games, first-moves |
| [K0169](../items/K0169-j5-cycle-space-basis.md) | 四つの5サイクルと角の4サイクルがサイクル空間の基底になる | proposition | computed | residual-games, first-moves |
| [K0170](../items/K0170-j5-minimum-odd-cycle-transversal.md) | J_5の最小奇閉路横断集合は2点 | proposition | computed | residual-games, first-moves |
| [K0171](../items/K0171-j5-all-edges-in-perfect-matchings.md) | J_5のすべての辺は何らかの完全マッチングに属する | proposition | refuted | residual-games, first-moves |
| [K0172](../items/K0172-j5-no-d4-invariant-perfect-matching.md) | J_5の完全マッチングにはD4不変なものがない | proposition | computed | residual-games, first-moves |
| [K0173](../items/K0173-j5-alternating-cycle-matching-connectivity.md) | J_5の完全マッチングは小サイクル上の交替で相互に移れる | proposition | refuted | residual-games, first-moves |
| [K0174](../items/K0174-j5-corner-deletion-paths.md) | J_5から角4点を除くと同型な4本のパスになる | proposition | computed | residual-games, first-moves |
| [K0175](../items/K0175-j5-response-hubs-not-diagonal-corners.md) | J_5の最小応答拠点は対角の角ペアで表せない | proposition | computed | residual-games, first-moves |
| [K0176](../items/K0176-losing-first-move-response-terminal-lengths.md) | 一つの負け初手への応答選択で、後の強制長が分かれる | proposition | computed | residual-games, first-moves |
| [K0177](../items/K0177-j4-two-point-dominating-set.md) | J_4には二点の全域支配集合がある | proposition | computed | residual-games, first-moves |
| [K0178](../items/K0178-jn-perfect-or-near-perfect-matching.md) | 後手勝ち正方形盤のJ_nには完全マッチングまたは一頂点だけ余すマッチングがある | proposition | refuted | residual-games, first-moves |
| [K0179](../items/K0179-jn-nonisolated-no-bridges.md) | J_nの非孤立部分には橋がない | proposition | refuted | residual-games, first-moves |
| [K0180](../items/K0180-jn-articulation-point-claim.md) | J_nの非孤立部分に関節点が現れる | proposition | computed | residual-games, first-moves |
| [K0181](../items/K0181-jn-fixed-pairing-breaks-midgame.md) | J_nにある固定ペア分けは中盤では必ず破れる | proposition | computed | residual-games, first-moves |
| [K0182](../items/K0182-all-losing-first-moves-few-nimbers-open.md) | 全初手負け盤でも一石nimberの種類数は小さい | question | open | residual-games, first-moves |
| [K0183](../items/K0183-saturation-missing-nimber-contiguity-open.md) | 飽和開始層で欠けるnimberは連続しない | question | open | grundy |
| [K0184](../items/K0184-saturation-missing-nimbers-powers-of-two-open.md) | 飽和開始層で欠ける正のnimberは2の冪だけ | question | open | grundy |
| [K0185](../items/K0185-ceiling-with-small-mobility-slack-open.md) | 天井達成局面は合法手数の小さい余裕で作れる | question | open | grundy |
| [K0186](../items/K0186-ceiling-three-distinct-winning-orbits-open.md) | g=h≥3の局面に軌道サイズ1か2の勝ち手が常にあるか | question | open | grundy |
| [K0187](../items/K0187-empty-root-wft-singleton-open.md) | 空盤のWFTは空でなければ単元 | question | open | strategy-length, grundy |
| [K0188](../items/K0188-wft-parity-hole-claim-refuted.md) | WFT(S)の同じ偶奇の穴はない | proposition | refuted | strategy-length, grundy |
| [K0189](../items/K0189-three-terminal-sizes-empty-wft.md) | T*(S)が3種類でもWFT(S)は空 | proposition | computed | strategy-length, grundy |
| [K0190](../items/K0190-forced-terminal-median-open.md) | 空盤で強制できる終局長はT*の中央値 | question | open | strategy-length, grundy |
| [K0191](../items/K0191-forest-p-graph-single-triple-grundy-gap.md) | 二点競合が森なら一つの三点制約によるnimber差は3以下 | proposition | refuted | residual-games, reconfiguration |
| [K0192](../items/K0192-single-residual-triple-replaces-winning-moves.md) | 残余三点制約が一つでも、それを外すと必勝手が全交換される | proposition | computed | residual-games, reconfiguration |
| [K0193](../items/K0193-effective-triple-tree-minimal-type-open.md) | 木の競合グラフで効く三点制約には最小の接続型がある | question | open | residual-games, reconfiguration |
| [K0194](../items/K0194-cross-clique-triple-redundancy.md) | 完全グラフ成分をまたぐ三点制約は冗長か値不変 | proposition | refuted | residual-games, reconfiguration |
| [K0195](../items/K0195-joint-higher-constraint-removal-synergy.md) | 高階制約を二つ同時に外したときだけ値が変わる | proposition | computed | residual-games, reconfiguration |
| [K0196](../items/K0196-effective-residual-quadruple-minimum.md) | 残余四点制約が効く最小局面は三点制約の例と別型 | proposition | proved | residual-games, reconfiguration |
| [K0197](../items/K0197-same-grundy-different-best-moves-after-removal.md) | 高階制約を全削除してもgは同じだが最善手は違う | proposition | computed | residual-games, reconfiguration |
| [K0198](../items/K0198-point-cover-deficit-linear-lower-bound.md) | 被覆欠損は石数の半分以上 | proposition | proved | maximal-safe, geometry |
| [K0199](../items/K0199-cocircular-avoidance-superlinear-deficit-open.md) | 共円回避を加えると欠損は超線形 | question | open | maximal-safe, geometry |
| [K0200](../items/K0200-integer-linear-cover-deficit-family.md) | 被覆欠損が線形にとどまる格子配置の無限族 | proposition | refuted | maximal-safe, geometry |
| [K0201](../items/K0201-rational-versus-real-cover-optimum.md) | 有理点での最適重複被覆は実数点での最適値より小さい | proposition | proved | maximal-safe, geometry |
| [K0202](../items/K0202-high-cover-cubic-localization.md) | 高いbを持つ配置は反転後の三次曲線付近に集中する | proposition | proved | maximal-safe, geometry |
| [K0203](../items/K0203-two-points-quadratic-cover-overlap.md) | 二つの空点で同時に二次的な重複被覆を持つ | proposition | proved | maximal-safe, geometry |
| [K0204](../items/K0204-high-cover-points-competition-refuted.md) | 高被覆点は互いに競合する | proposition | refuted | maximal-safe, geometry |
| [K0205](../items/K0205-local-cover-versus-global-efficiency.md) | 点ごとの被覆上限は大きくても全面被覆は極端に非効率 | proposition | proved | maximal-safe, geometry |
| [K0206](../items/K0206-minimum-maximal-one-stone-fragility-withdrawn.md) | B361の全n版ρ=1はn=1で定義不全 | proposition | withdrawn | maximal-safe, geometry |
| [K0207](../items/K0207-maximal-no-original-empty-point-unblocked.md) | どの一石を抜いても元の空点は合法にならない極大配置 | proposition | computed | maximal-safe, geometry |
| [K0208](../items/K0208-overlapping-cover-many-points-unblocked.md) | 被覆重複が大きいのに一石で大量解除できる | proposition | computed | maximal-safe, geometry |
| [K0209](../items/K0209-minimum-maximal-stones-essential.md) | 最小極大配置の各石には固有の仕事がある | proposition | refuted | maximal-safe, geometry |
| [K0210](../items/K0210-maximum-configurations-cover-redundant-stones.md) | 最大配置には全面被覆に不要な石がある | proposition | computed | maximal-safe, geometry |
| [K0211](../items/K0211-eight-stone-cover-line-circle-compression.md) | 8石極大の被覆は二本の三点直線と少数の円へ圧縮できる | proposition | refuted | maximal-safe, geometry |
| [K0212](../items/K0212-n8-seven-stone-at-least-two-legal-points.md) | 安全7点集合では8×8に必ず2点以上の合法手が残る | proposition | computed | maximal-safe, geometry |
| [K0213](../items/K0213-n8-to-n9-small-maximal-two-relocations.md) | 8石極大から9×9の小さい極大を作るには2石の再配置で足りる | proposition | computed | maximal-safe, geometry |
| [K0214](../items/K0214-n7-maximum-external-radius-two.md) | 7×7の16最大配置のr(S)はすべて2 | proposition | computed | maximum-safe, geometry |
| [K0215](../items/K0215-n7-first-external-legal-point-orbits.md) | 7×7最大配置の最初の合法外点はD4軌道で少数型になる | proposition | computed | maximum-safe, geometry |
| [K0216](../items/K0216-uniform-external-saturation-radius-open.md) | 最大配置の外部飽和半径は一様有界 | question | open | maximum-safe, geometry |
| [K0217](../items/K0217-minimum-maximal-external-blocking-band-open.md) | 盤内では最小極大なのに盤外の広い帯まで塞ぐ | question | open | maximum-safe, geometry |
| [K0218](../items/K0218-n7-to-n8-maximum-two-discard-bound-refuted.md) | 7×7最大配置を8×8の15石へ変えるには元の石を2個以上捨てる必要がある | proposition | refuted | maximum-safe, geometry |
| [K0219](../items/K0219-n7-phase-dependent-n8-extension.md) | 7×7最大配置の一方の相だけが少ない再配置で8×8最大へ届く | proposition | computed | maximum-safe, geometry |
| [K0220](../items/K0220-distant-forbidden-points-collinear.md) | 外点の禁止理由は遠方で直線だけに変わる | proposition | proved | maximum-safe, geometry |
| [K0221](../items/K0221-interior-relocation-external-gap-open.md) | 内側の石を動かすだけで盤外の最初の合法点が遠くへ飛ぶ | question | open | maximum-safe, geometry |
| [K0222](../items/K0222-same-residual-family-two-exchange-connectivity-refuted.md) | 各族は二点交換まで許せば連結する | proposition | refuted | residual-games, reconfiguration |
| [K0223](../items/K0223-only-disconnected-residual-families-split-refuted.md) | 非連結性はRが空または非連結の族に限られる | proposition | refuted | residual-games, reconfiguration |
| [K0224](../items/K0224-connected-residual-game-split-fibers.md) | 非空で連結なRを持つ族も分裂する | proposition | computed | residual-games, reconfiguration |
| [K0225](../items/K0225-fiber-components-deletion-robustness.md) | 同一残局族の異なる成分は石除去への耐性が違う | proposition | computed | residual-games, reconfiguration |
| [K0226](../items/K0226-one-fewer-stone-fiber-bridges-open.md) | 一石少ない中間配置を許すと同一残局族を少数の橋で結べる | question | open | residual-games, reconfiguration |
| [K0227](../items/K0227-abstract-residual-isomorphism-split-fibers.md) | 残余ゲームの抽象同型まで緩めても配置族は分裂する | proposition | computed | residual-games, reconfiguration |
| [K0228](../items/K0228-circle-center-denominator-prime-factors.md) | 中心分母の素因数型で格子点数上限を整理できる | proposition | proved | geometry |
| [K0229](../items/K0229-power-two-denominator-smaller-board-refuted.md) | 分母が2の冪の円は奇分母の円より最小収容盤が小さい | proposition | refuted | geometry |
| [K0230](../items/K0230-many-point-circle-residue-description-refuted.md) | q≥3の多数点円は、整数中心円の剰余類選択として最適に記述できる | proposition | refuted | geometry |
| [K0231](../items/K0231-fixed-denominator-radius-monotonicity.md) | 分母qを固定した最良点数は半径の単調増加だけでは達成できない | proposition | proved | geometry |
| [K0232](../items/K0232-circle-window-single-point-cuts-open.md) | 円窓B457の種類数比較は量化が未指定、q≥3の穴なしは証明済み | question | scope-unclear | geometry |
| [K0233](../items/K0233-circle-first-board-summary-refuted.md) | 完全点数・外接幅・原始二次係数では四点初出を決定できない | proposition | refuted | geometry |
| [K0234](../items/K0234-radius-25-over-2-no-eleven-point-square-window.md) | 半径二乗25/2の12点円は、正方形窓で11点だけを残せない | proposition | proved | geometry |
| [K0235](../items/K0235-n11-first-eleven-point-circle.md) | 11×11は11点を載せる円の最初の正方形盤 | proposition | proved | geometry |
| [K0236](../items/K0236-extreme-point-multiplicity-single-loss.md) | 1点だけ失えるかは上下左右の極値点の重複度で決まる | proposition | proved | geometry |
| [K0237](../items/K0237-rectangle-versus-square-circle-spectra.md) | 長方形窓なら実現する点数が正方形窓では実現しない | proposition | refuted | geometry |
| [K0238](../items/K0238-half-center-symmetric-circle-near-max-odd-gap.md) | q=2の対称な完全円では最大点数直下の奇数が欠ける | proposition | proved | geometry |
| [K0239](../items/K0239-circle-window-spectrum-coordinate-orders.md) | 円の窓点数スペクトルは円周上の点の座標順序で決まる | proposition | proved | geometry |
| [K0240](../items/K0240-circle-symmetry-hole-monotonicity-refuted.md) | 円の対称群が大きいほど窓スペクトルの穴が増える単調性は偽 | proposition | refuted | geometry |
| [K0241](../items/K0241-three-stone-mobility-gaps-circle-cuts.md) | 三石後の合法手数の欠落は少数の円切断型で説明できる | proposition | proved | geometry |
| [K0242](../items/K0242-collinear-large-slope-uniform-tail.md) | 共線数の大きい傾きの尾部は一様に小さい | proposition | proved | geometry |
| [K0243](../items/K0243-direction-height-cubic-leading-decay.md) | 固定方向の主項係数は方向高さの三乗で減衰する | proposition | proved | geometry |
| [K0244](../items/K0244-collinear-boundary-gcd-corrections.md) | 共線数の有限サイズ補正を境界長とgcd和へ分けられる | proposition | proved | geometry |
| [K0245](../items/K0245-fixed-circle-size-positive-quadruple-share.md) | 点数が固定の円が共円四点数の正の割合を担う | proposition | proved | geometry, statistics |
| [K0246](../items/K0246-quadruple-weighted-circle-size-divergence-refuted.md) | 四点寄与で重み付けすると円上点数は発散する | proposition | refuted | geometry, statistics |
| [K0247](../items/K0247-primitive-chord-circle-count-description.md) | 円を半径でなく弦の原始型で分解すると重複の少ない式が得られる | proposition | proved | geometry, statistics |
| [K0248](../items/K0248-random-forbidden-count-conditional-poisson.md) | 無作為k点の最初の禁止数はPoisson型になる | proposition | proved | geometry, statistics |
| [K0249](../items/K0249-first-forbidden-cluster-claim-refuted.md) | 最初の禁止は単発でなく同じ円・直線の束として現れる | proposition | refuted | geometry, statistics |
| [K0250](../items/K0250-safe-probability-three-point-overlap-correction.md) | 安全確率の最初の補正は三点共有の禁止ペアが決める | proposition | proved | geometry, statistics |
| [K0251](../items/K0251-random-win-p-bound-two-thirds-refuted.md) | 標準盤のP局面のランダム勝率は2/3以下 | proposition | refuted | statistics, grundy |
| [K0252](../items/K0252-random-win-p-above-three-quarters.md) | P局面でランダム勝率3/4を超えられる | proposition | computed | statistics, grundy |
| [K0253](../items/K0253-height-three-p-random-win-half-bound.md) | 残り最大手数が3以下ならPのランダム勝率は1/2以下 | proposition | refuted | statistics, grundy |
| [K0254](../items/K0254-n4-any-two-rule-removals-preserve-winner.md) | 4×4はどの二つの禁止四点を同時解除しても後手勝ち | proposition | computed | variants |
| [K0255](../items/K0255-n4-three-rule-removals-flip-winner.md) | 4×4の三つの禁止解除で勝者が反転する | proposition | computed | variants |
| [K0256](../items/K0256-minimum-flip-common-triple-refuted.md) | 最小反転解除族は共有する三点を持つ | proposition | refuted | variants |
| [K0257](../items/K0257-minimum-flip-no-common-point.md) | 共通点を一つも持たない最小反転解除族がある | proposition | computed | variants |
| [K0258](../items/K0258-n4-whole-circle-removal-preserves-winner-refuted.md) | 一つの真円の制約を全部解除しても4×4の空盤勝者は変わらない | proposition | refuted | variants |
| [K0259](../items/K0259-two-row-opposite-row-first-response.md) | m≥6の後手は最初の応答を反対行に選べる | proposition | proved | rectangles, variants |
| [K0260](../items/K0260-two-row-large-midgame-nimber.md) | 二行盤でも中盤nimberは幅から予想するより大きい | proposition | refuted | rectangles, variants |
| [K0261](../items/K0261-three-by-three-row-translation-safe-intervals.md) | 3対3の安全配置は一方の行を平行移動しても安全な区間を多数持つ | proposition | proved | rectangles, variants |
| [K0262](../items/K0262-three-row-first-move-density-third-refuted.md) | 部分勝ちとなる三行盤の勝ち初手密度は1/3へ近づく | proposition | refuted | rectangles, variants |
| [K0263](../items/K0263-three-row-periodic-winner-nonperiodic-moves-refuted.md) | 三行盤で周期が続いても勝ち初手集合の幾何は非周期になる | proposition | refuted | rectangles, variants |
| [K0264](../items/K0264-three-stones-per-row-minimum-length-refuted.md) | 各行3石を置ける最小長はw≥2で2w+1 | proposition | refuted | rectangles, variants |
| [K0265](../items/K0265-row-arithmetic-progression-capacity-construction.md) | 3w石の配置は行ごとに等差数列を置く構成で達成できる | proposition | proved | rectangles, variants |
| [K0266](../items/K0266-n7-maximum-exchange-distance.md) | 7×7全最大配置の交換距離は5が最小で、最小対は八A–Bペア | proposition | computed | maximum-safe, reconfiguration |
| [K0267](../items/K0267-n7-two-stone-determination-and-13-stone-completion.md) | 7×7最大配置は全て二石で一意に決まり、十三石部分集合は一意完了 | proposition | computed | maximum-safe, reconfiguration |
| [K0268](../items/K0268-n7-six-orbit-skeleton-exclusive-extensions.md) | 7×7必須六軌道骨格の容量13は排他的二拡張だけで14へ上がる | proposition | computed | maximum-safe, geometry |
| [K0269](../items/K0269-n7-skeleton-capacity-certificate.md) | 骨格容量α(M)≤13は120占有候補と七残余補題で認証される | proposition | proved | maximum-safe, certificates |
| [K0270](../items/K0270-n7-g12-maximum-containing-components.md) | 7×7のG12で最大配置を含む成分は八個・各903局面 | proposition | proved | maximum-safe, reconfiguration |
| [K0271](../items/K0271-n7-fourth-corner-global-gate.md) | 代表最大A–B間の十二石経路は第四の角を大域的に必ず通る | proposition | proved | reconfiguration, maximum-safe |
| [K0272](../items/K0272-n7-union-width-eleven-static-barrier.md) | 代表U内の幅11障壁は占有差二層と整数最適21四点で証明 | proposition | proved | reconfiguration, certificates |
| [K0273](../items/K0273-n7-orbit-omission-capacity-loss.md) | 7×7の軌道省略容量損失は5・6盤より強い | proposition | computed | maximum-safe, geometry |
| [K0274](../items/K0274-center-alone-two-phase-explanation-refuted.md) | 中心点の存在だけで最大配置のA/B二相が生じるという説明は反証 | proposition | refuted | maximum-safe, geometry |
| [K0275](../items/K0275-n7-13-stone-layer-versus-maxima.md) | 13石層の豊富さと最大14石層の二型は同じ分類ではない | proposition | computed | maximum-safe, geometry |
| [K0276](../items/K0276-h-dense-independent-holdout-open.md) | H-denseはn≤10の記述を越える独立確認が未完了 | proposition | conjectured | first-moves, statistics |
| [K0277](../items/K0277-maximum-parity-does-not-determine-winner.md) | 最大安全石数の奇偶だけで空盤勝者は決まらない | proposition | refuted | square-outcomes, maximum-safe |
| [K0278](../items/K0278-n5-first-move-pattern-transfer-refuted.md) | 5×5勝ち初手の幾何パターンは9×9へ一様転送できない | proposition | refuted | first-moves |
| [K0279](../items/K0279-fixed-r-static-pair-core-rank.md) | 固定R内LOSS pairコアのstatic witness順位は深さ一様でない | proposition | refuted | search-methods, geometry |
| [K0280](../items/K0280-independent-rust-verification-boundaries.md) | 独立Rust実装の検査は参照探索・CSV監査・証明書局所検査を分ける | verification | verified | verification, certificates |
| [K0281](../items/K0281-n7-geometric-two-phase-proof-open.md) | 7×7二相選択を制約solverなしの幾何だけで導く証明は未完成 | question | open | maximum-safe, geometry |
| [K0282](../items/K0282-n7-g11-global-connectivity-open.md) | 11石を許したG11で最大由来八成分が全て接続するか未確定 | question | open | maximum-safe, reconfiguration |
| [K0283](../items/K0283-fresh-memo-desc-slower-on-seven-parents.md) | fresh-process memo-descは既知七親でdefaultとrandom双方より遅い | proposition | observed | search-methods, statistics |
| [K0284](../items/K0284-independent-memo-ascending-rank-replication.md) | 独立memo昇順のLOSS順位改善は凍結cohortで再現、信頼境界あり | proposition | observed | search-methods, statistics |
| [K0285](../items/K0285-staged-v3-loss-shortlist-recall.md) | staged10k→top11→1MはV3十二親でLOSS shortlist recall12/12 | proposition | observed | search-methods, statistics |
| [K0286](../items/K0286-native-parent-solver-speedup-gate-failed.md) | 10k root-orderとstaged V3のnative親solver加速は凍結gate失敗 | proposition | observed | search-methods, statistics, verification |
| [K0287](../items/K0287-cumulative-memo-feature-semantics.md) | multi-state probeの累積memoは候補独立特徴でない | method | active | search-methods, provenance |
| [K0288](../items/K0288-certified-witness-rank-and-coordinate-join.md) | certified witness順位と真のfirst LOSS順位は別、座標joinにも検査が必要 | method | active | provenance, verification, search-methods |
| [K0289](../items/K0289-same-distance-two-stone-opposite-outcomes.md) | 10×10では同じ二点間距離でも二石局面の勝敗が異なる | proposition | computed | first-moves, geometry |
| [K0290](../items/K0290-raw-gain-versus-filtered-response-overlap.md) | 9×9 raw gainとfiltered responseのpair重複は異なる量 | proposition | proved | geometry, search-methods |
| [K0291](../items/K0291-all-maximal-terminal-parity-refuted.md) | 全極大終局の石数偶奇が固定される仮説は4×4で反証 | proposition | refuted | maximal-safe, strategy-length |
| [K0292](../items/K0292-n5-central-window-first-move-claim-refuted.md) | 5×5の勝ち初手は中央3×3窓ではない | proposition | refuted | first-moves |
| [K0293](../items/K0293-n1-n7-global-grundy-spectra.md) | 1〜7×7のGrundy全体スペクトルは連続だが最大値は異なる | proposition | computed | grundy |
| [K0294](../items/K0294-n4-two-stone-grundy-gaps.md) | 4×4二石層はGrundy1と4を持たず、全120局面は四値に分かれる | proposition | computed | grundy, residual-games |
| [K0295](../items/K0295-n1-n7-full-tstar-and-wft.md) | 1〜7×7空盤の全勝敗維持終局T*と固定長保証WFTは区別される | proposition | computed | strategy-length, grundy |
| [K0296](../items/K0296-n5-five-stone-optimal-terminal-exclusion-refuted.md) | 5×5の全勝敗維持対局では五石で終わらないという説明は偽 | proposition | refuted | strategy-length, maximal-safe |
| [K0297](../items/K0297-minimum-maximal-private-point-open.md) | n≥2の全最小極大配置に一重被覆点があるか | question | open | maximal-safe, geometry |
| [K0298](../items/K0298-minimum-maximal-rho-one-open.md) | n≥2の全最小極大配置で故障耐性ρが1か | question | open | maximal-safe, geometry |
| [K0299](../items/K0299-denominator-three-circle-window-spectra.md) | q≥3の完全格子円の窓点数スペクトルは可変0..m・固定0..M_n | proposition | proved | geometry |
| [K0300](../items/K0300-minimal-effective-tree-triple-star.md) | 効く極小三点辺の最小接続木は三葉上のK1,3 | proposition | proved | residual-games |
| [K0301](../items/K0301-four-stone-johnson-layer-bridge.md) | 安全四石配置対は三石Johnson交換層を経由して接続できる | proposition | proved | reconfiguration |
| [K0302](../items/K0302-fixed-width-five-exact-stabilization-thresholds.md) | 固定幅の真の満容量安定化長5件は24,12,16,13,11 | proposition | proved | rectangles, variants, grundy |
| [K0303](../items/K0303-width-three-all-q-all-length-grundy.md) | 幅3・全q≥4・全長の空盤Grundyと全局面最大値を分類 | computation | computed | rectangles, variants, grundy |
| [K0304](../items/K0304-odd-q-fixed-point-free-reflection-p-position.md) | 奇数qの固定点なし鏡映対称安全局面はP局面 | proposition | proved | rectangles, variants, grundy |
| [K0305](../items/K0305-binary-grundy-iff-maximal-parity.md) | 有限下方閉配置ゲームで全Grundy値が0/1であることと極大集合の同偶奇性は同値 | proposition | proved | grundy, variants |
| [K0306](../items/K0306-lattice-circle-width-sixteen-theorem.md) | 幅w≥16の連続整数行に任意の円が持つ格子点は高々w | proposition | proved | geometry, rectangles |
| [K0307](../items/K0307-square-circle-maxima-through-112.md) | n≤112の正方形盤に載る円上格子点数の最大値を全中心・全半径で完全分類 | computation | computed | geometry |
| [K0308](../items/K0308-circle-denominator-5-6-8-formulas.md) | 中心分母5・6・8の格子円には点数・最小半径の厳密公式がある | proposition | proved | geometry |
| [K0309](../items/K0309-misere-small-legal-set-exchange.md) | 合法点5個以下では通常値とmisère補助値は0と1だけ交換される | proposition | proved | variants, grundy |
| [K0310](../items/K0310-misere-square-outcomes-through-eight.md) | misère版の6×6は後手勝ち、7×7・8×8は先手勝ち | computation | computed | variants, square-outcomes, first-moves |
| [K0311](../items/K0311-misere-n9-outcome-open.md) | misère版9×9の空盤勝敗は未確定 | question | open | variants, square-outcomes, search-methods |
| [K0312](../items/K0312-n11-minimum-maximal-bounds.md) | 11×11の最小極大サイズは8≤s_11≤10 | proposition | computed | maximal-safe, geometry |
| [K0313](../items/K0313-large-safe-constructions-n11-n12.md) | K_11≥21かつK_12≥22の明示安全極大構成がある | proposition | computed | maximum-safe, maximal-safe, geometry |
| [K0314](../items/K0314-line-only-saturation-sharp-constant.md) | line-only版の最小極大サイズは主係数(3π²/8)^(1/3)でn^(2/3)以上 | proposition | proved | maximal-safe, geometry, variants |
| [K0315](../items/K0315-n10-pair-sum-relaxation-optimum.md) | 10×10で行・列の点対和制約だけを課した緩和問題の最大値は23 | proposition | proved | maximum-safe, geometry |
| [K0316](../items/K0316-n10-nineteen-stone-local-barriers.md) | 10×10の既知19石近傍には安全20石が存在しない大きな局所障壁がある | computation | computed | maximum-safe, reconfiguration, geometry |
| [K0317](../items/K0317-four-row-q8-pell-circle-family.md) | 四連続整数行を2点ずつ通る8点円には無限Pell族がある | proposition | proved | geometry, rectangles, variants |
| [K0318](../items/K0318-fixed-width-curve-packing-upper-bound.md) | 禁止曲線の三つ組・点対充填から固定幅q点版の一般安定化上界が得られる | proposition | proved | rectangles, geometry, variants, grundy |
| [K0319](../items/K0319-misere-direct-sum-normal-grundy-rule.md) | swap則が全後続局面で成り立つ部品のmisère直和は通常Grundy値だけで解ける | proposition | proved | variants, grundy |
| [K0320](../items/K0320-n11-n15-n-minus-one-maximal-constructions.md) | n=11..15にはn−1石の安全極大配置が存在する | proposition | computed | maximal-safe, geometry |
| [K0321](../items/K0321-n4-board-deletion-strategic-interaction.md) | 4×4は容量損失ゼロの二点削除で勝者が反転する | proposition | computed | variants, maximum-safe, grundy |
| [K0322](../items/K0322-equal-nimber-geometric-extension-split.md) | 同nimberの占有配置は共通の幾何的追加で勝敗が分かれる | proposition | computed | residual-games, grundy |
| [K0323](../items/K0323-finite-gibbs-two-phase-concentration.md) | 7×7のGibbs分布は有限活動度で二つの最大相へ集中できる | proposition | proved | statistics, maximum-safe, reconfiguration |
| [K0324](../items/K0324-n4-incomplete-position-invariants.md) | 4×4では幾何・局所手・極大拡張の各集計が一致しても勝敗が異なる | proposition | computed | grundy, geometry, residual-games, maximal-safe |
| [K0325](../items/K0325-n4-conditional-gain-variance.md) | 同じ合法数・利得総和でも利得分散でP率が異なる4×4完全層 | computation | computed | statistics, grundy |
| [K0326](../items/K0326-fault-tolerance-precludes-single-swap.md) | 故障耐性ρが2以上の極大安全配置には一石交換がない | proposition | proved | maximal-safe, reconfiguration |
| [K0327](../items/K0327-square-position-grundy-unboundedness-open.md) | 標準正方形盤の安全局面のGrundy値は無界か | question | open | grundy, residual-games |
| [K0328](../items/K0328-maximal-fault-tolerance-bound-open.md) | n≥2の標準盤の全極大配置で故障耐性ρは一様有界か | question | open | maximal-safe, geometry |
| [K0329](../items/K0329-n11-s5-verdict-recovery-and-s4-manifest.md) | 11×11のs5 verdict cacheの回収とcoordinator永続化でLOSS class 2個・WIN 1個・verified certificate 2件を確定した | computation | computed | search-methods, verification |
| [K0330](../items/K0330-maximal-fault-tolerance-average-cover-bound.md) | 極大配置の故障耐性は三石被覆の平均多重度で上から抑えられる | proposition | proved | maximal-safe, geometry |
| [K0331](../items/K0331-width-five-q8-exact-stabilization.md) | 5×m・q=8の真の満容量安定化長はM_{5,8}=16 | proposition | proved | rectangles, variants, grundy, certificates |
| [K0332](../items/K0332-width-five-q7-stabilization-bounds.md) | 5×m・q=7の満容量安定化長は19以上158以下 | proposition | proved | rectangles, variants, maximal-safe |
| [K0333](../items/K0333-modular-polynomial-curve-q-point-bound.md) | 次数k≥2の剰余多項式グラフは直線高々k点・円高々2k点でq≥2k+1版が全点安全 | proposition | proved | geometry, variants, maximum-safe, residual-games |
| [K0334](../items/K0334-residue-parabola-nae-origin-decomposition.md) | 剰余放物線の等号問題はsigned NAE3/4と原点由来2/3節へ厳密に分解できる | proposition | proved | geometry, maximum-safe, search-methods |
| [K0335](../items/K0335-center-corner-s4-cover-exact-all-odd-squares.md) | 奇数盤の中心・隅rootのs4 class cover最小数はceil((n²+n−8)/4) | proposition | proved | search-methods, certificates, geometry |
| [K0336](../items/K0336-independent-residual-twins-parity-compression.md) | 同一linkの独立双子点は正の偶奇数へ減らしてもGrundy数が一致する | proposition | proved | residual-games, grundy, search-methods |
| [K0337](../items/K0337-odd-uniform-involution-scope.md) | 奇数qの鏡映戦略の抽象十分条件と任意禁止族での最小q+1点反例 | proposition | proved | variants, grundy, residual-games |
| [K0338](../items/K0338-high-stabilizer-safe-state-classification.md) | 標準正方形盤の安定化群位数4以上の安全集合は高々五石で正確にO(n²)個 | proposition | proved | geometry, grundy, search-methods |
| [K0339](../items/K0339-multiplayer-terminal-modulus.md) | r人巡回配置ゲームで敗者が戦略に依存しない人数は極大サイズ差のgcdで完全に決まる | proposition | proved | variants, strategy-length, maximal-safe |
| [K0340](../items/K0340-three-dimensional-prism-capacity-and-grundy.md) | 三次元の平行格子列では高qでも二列容量が残り、列数の偶奇が全Grundy0/1を決める | proposition | proved | variants, geometry, grundy, maximal-safe |
| [K0341](../items/K0341-odd-column-prism-root-mod4-and-odd-r-grundy.md) | 奇数列の三次元長盤はq≡2 mod4でだけ先手勝ち、奇数rの全Grundyは閉公式を持つ | proposition | proved | variants, geometry, grundy |
| [K0342](../items/K0342-sharp-horizontal-chord-sum-energy.md) | r点の同和弦energyには等差数列で達成される鋭い三次上界がある | proposition | proved | geometry, rectangles |
| [K0344](../items/K0344-exchangeable-residual-class-rank-kernel.md) | 交換可能残余classはrank以下へ縮めて通常Grundyとmisère補助mexを保存し、誘導削除上限は全rankで最良 | proposition | proved | residual-games, grundy, search-methods, variants |
| [K0345](../items/K0345-even-capacity-odd-column-prism-all-lengths-grundy.md) | 偶数ペア容量・奇数列の三次元盤は任意長で全Grundy閉公式を持つ | proposition | proved | variants, geometry, grundy |
| [K0346](../items/K0346-arbitrary-integer-board-unbounded-circle-fault-tolerance.md) | 任意有限整数点盤では三共線なし・唯一最大配置でも故障耐性が無界 | proposition | proved | geometry, maximal-safe, maximum-safe, variants, grundy |
| [K0347](../items/K0347-prism-all-length-two-maxima-grundy-kernel.md) | 奇数列の平行列版は全長・全局面のGrundyを二最大占有数の表と偶奇へ縮約できる | proposition | proved | variants, grundy, residual-games, search-methods |
| [K0348](../items/K0348-circle-fault-tolerance-vertex-cover-np-complete.md) | 任意有限整数点盤の一空点円故障耐性はVertex Coverを表現し唯一最大配置でもNP完全 | proposition | proved | geometry, maximal-safe, maximum-safe, variants, search-methods |
| [K0349](../items/K0349-q-point-local-saturated-curve-bounds.md) | 全q点版の空点・既存石の飽和曲線数は反転とMelchiorで抑えられる | proposition | proved | geometry, variants |
| [K0350](../items/K0350-parallel-q-two-width-chord-stabilization.md) | 任意のw本の平行線のq=2w版は同和弦energyで満容量安定化する | proposition | proved | rectangles, geometry, variants, grundy |
| [K0351](../items/K0351-width-three-q4-exact-stabilization.md) | 3×m・q=4の真の満容量安定化長はM_{3,4}=24 | proposition | proved | rectangles, variants, grundy |
| [K0352](../items/K0352-general-dimensional-parallel-columns.md) | 任意次元平行列盤ではd−1列容量が極大配置・多人版・二値Grundyを完全に決める | proposition | proved | variants, geometry, grundy, maximal-safe, strategy-length |
| [K0353](../items/K0353-two-dimensional-parallel-columns.md) | 二次元平行列盤では各列独立容量となり全局面Grundyは石数偶奇だけで決まる | proposition | proved | variants, geometry, grundy, maximal-safe, strategy-length |
| [K0354](../items/K0354-general-prism-maximal-count.md) | 任意次元平行列盤の極大安全集合数は母関数で閉形式に数えられる | proposition | proved | variants, geometry, maximal-safe, statistics |
| [K0355](../items/K0355-n11-reply27-cache-recovery-frontier.md) | 11×11 reply27の保存済みexact結果から復元したcache frontier | computation | computed | square-outcomes, search-methods, verification, provenance |
| [K0356](../items/K0356-capacity-boundary-grundy-bound.md) | 任意次元平行列容量ゲームの容量境界ではGrundy値が残り手数の偶奇に一致する | proposition | proved | variants, grundy |
| [K0357](../items/K0357-n11-v104-hypothetical-win-witness-cover.md) | 11×11の{60,27}後の第三手104に対する仮想WIN witness cover | computation | computed | search-methods, square-outcomes, verification, provenance |
| [K0358](../items/K0358-capacity-slack-one-grundy-child-count-bound.md) | 容量余裕1のGrundy値は常に3以下で境界子の型から完全決定できる | proposition | proved | variants, grundy |
| [K0359](../items/K0359-capacity-slack-two-exact-grundy.md) | 任意次元容量ゲームの余裕2層は全局面二値Grundyで閉公式を持つ | proposition | proved | variants, grundy, strategy-length |
| [K0360](../items/K0360-capacity-slack-three-exact-grundy.md) | 任意次元の容量余裕3は二値境界署名で全Grundyを決定でき上界3が鋭い | proposition | proved | variants, grundy, strategy-length |
| [K0361](../items/K0361-capacity-conditional-maximal-counts-and-play-paths.md) | 任意の容量ゲーム途中局面からの極大盤面数と全合法着手順序数を母関数で厳密決定する | proposition | proved | variants, maximal-safe, statistics, strategy-length |
| [K0362](../items/K0362-capacity-height-random-terminal-distribution.md) | 容量ゲームの高さ無限極限では完成対局一様と逐次合法点一様の終局分布が乖離する | proposition | proved | variants, statistics, strategy-length, maximal-safe |
| [K0363](../items/K0363-capacity-finite-height-distribution-error.md) | 容量ゲームの逐次合法点一様モデルの有限高さ誤差は明示的にO(1/m)で全終局確率の一次係数も計算できる | proposition | proved | variants, statistics, strategy-length |
| [K0367](../items/K0367-uniform-sublinear-circle-double-rows.md) | 標準整数格子円の二重点行数は幅に対して一様に劣線形 | proposition | proved | geometry, rectangles, variants |
| [K0368](../items/K0368-exact-double-hit-rows-width-five-to-forty-three.md) | 標準整数格子円の二重点行数の厳密最大値（5〜43行） | proposition | proved | geometry, rectangles, variants |
| [K0369](../items/K0369-exact-double-rows-fortyfour-to-sixtythree.md) | 標準整数格子44〜63行で円が二点ずつ通る行数の厳密最大値 | proposition | proved | geometry, rectangles, variants |
| [K0370](../items/K0370-quantitative-uniform-circle-density.md) | 連続整数行の円の二重点行数に対する定量的一様上界 | proposition | proved | geometry, rectangles, variants |
| [K0371](../items/K0371-fixed-player-s7-propagation-and-cache-quarantine.md) | reply27のS7境界での先手固定伝播と旧2件のS5 WIN根拠撤回 | verification | verified | square-outcomes, verification, certificates, provenance |
| [K0372](../items/K0372-n11-independent-exact-evidence-trust-audit.md) | 11×11 exact境界の独立監査とraw・cache・minimaxの信頼分離 | verification | verified | square-outcomes, verification, certificates, provenance |
| [K0373](../items/K0373-n11-reply27-100-108-reflection-equivalence.md) | 11×11二石局面60・27の第三手100と108は反射対称 | proposition | proved | square-outcomes, search-methods, verification |
| [K0374](../items/K0374-n11-reply27-s6-universal-closure.md) | 11×11 reply27の難S5局面を全90 S6子WINで確定 | computation | computed | square-outcomes, search-methods, certificates, verification |
| [K0375](../items/K0375-n11-shared-proof-dag-and-tt-order.md) | 11×11の既知S5六局面で共有TTと終局閉包証明DAGを実測 | computation | computed | square-outcomes, search-methods, certificates, verification, provenance |
| [K0376](../items/K0376-n11-third-move-loss-class-cover-minimum.md) | 11×11 `{60,27}` の現行117手被覆には既知LOSS class 31個が全て必要 | computation | computed | square-outcomes, certificates, verification |
| [K0377](../items/K0377-n11-compact-witness-switch-proof-verification.md) | 11×11の三S5共有証明DAGをcompact化し、既知S6証人の共有で縮約 | verification | verified | square-outcomes, certificates, verification, provenance |
| [K0378](../items/K0378-n11-six-root-incremental-shared-proof-verification.md) | 11×11の独立検証済みS5証明6根を段階統合、群間重複なし | verification | verified | square-outcomes, certificates, verification, provenance |
| [K0379](../items/K0379-n11-s5-hierarchical-adaptive-cost-audit.md) | 11×11 S5階層分割の費用比較と証拠対応ルーティング | computation | computed | square-outcomes, search-methods, verification, provenance |
| [K0380](../items/K0380-n11-s5-loss-witness-budgeted-benchmark.md) | 11×11既知S5 LOSSの分割証人探索は小予算で節点削減を示さない | computation | observed | square-outcomes, search-methods, provenance |
| [K0382](../items/K0382-n11-s5-loss-proof-cost-decomposition.md) | 11×11既知S5 LOSS標本では決定S6証明が探索費用の主成分 | computation | observed | square-outcomes, search-methods, certificates, provenance |
| [K0383](../items/K0383-nonprimitive-double-row-min-width-2-32.md) | 非原始二重点行の最小幅 F(k)：2〜32本 | proposition | proved | geometry, rectangles, variants |
| [K0384](../items/K0384-capacity-all-slack-grundy-three.md) | 全容量余裕の容量占有ゲームにおけるGrundy値の一様上界 | proposition | proved | variants, grundy |
| [K0385](../items/K0385-gcd-one-double-rows-up-to-400.md) | 400幅以内に25二重点行を持つ円の行差最大公約数は1 | proposition | proved | geometry, rectangles |
| [K0386](../items/K0386-capacity-all-slack-winning-move-classification.md) | 全容量余裕の容量占有ゲームにおける全勝ち手分類 | proposition | proved | variants, grundy, strategy-length |
| [K0387](../items/K0387-unequal-capacity-even-slack-grundy-three.md) | 異容量の列制約では偶数余裕でもGrundy値3が生じる | proposition | proved | variants, grundy |
| [K0388](../items/K0388-central-three-row-two-squares-density.md) | 中央弦型2+1+1共円完成数と弦長集合の密度 | proposition | proved | geometry, statistics |
| [K0389](../items/K0389-rectangle-reflection-parity-and-mod4.md) | 長方形盤の共円・共線点組数の鏡映公式（法2・法4） | proposition | proved | geometry, rectangles, statistics |
| [K0390](../items/K0390-unequal-capacity-grundy-five.md) | 異容量上位列和制約ゲームでGrundy値5が実現する | proposition | proved | variants, grundy |
| [K0391](../items/K0391-central-three-row-finite-width-counts.md) | 3行盤の中央弦型2+1+1共円四点組の有限幅厳密計数 | proposition | proved | geometry, statistics |
| [K0392](../items/K0392-cocircular-211-rectangle-parity.md) | 長方形盤の2+1+1型共円四点組数の法4公式 | proposition | proved | geometry, rectangles, statistics |
| [K0393](../items/K0393-row-two-two-circle-count.md) | 標準整数格子の二行二点型共円四点組数の厳密公式 | proposition | proved | geometry, rectangles, statistics |
| [K0394](../items/K0394-unequal-six-column-grundy-exclusion.md) | 最大容量7以下の異容量6列ゲームではGrundy値6が生じない | proposition | computed | variants, grundy |
| [K0395](../items/K0395-quarter-turn-forbidden-quadruples-mod4.md) | 90度回転対称点集合の共円・共線四点組数の法4公式 | proposition | proved | geometry, statistics |
| [K0396](../items/K0396-d-dimensional-box-collinear-q-formulas.md) | 任意次元整数直方格子の共線q点組数と直線長分布の厳密公式 | proposition | proved | geometry, statistics |
| [K0397](../items/K0397-collinear-q-overlap-distribution.md) | 共線q点組の交差分布と局所次数は直線長で決まる | proposition | proved | geometry, statistics |
| [K0398](../items/K0398-forbidden-four-overlap-spectrum.md) | 共円・共線禁止四点組の全交差分布の厳密公式 | proposition | proved | geometry, statistics |
| [K0399](../items/K0399-quarter-turn-q-point-congruences.md) | 90度回転対称点集合の任意q点共円・共線数の法4公式 | proposition | proved | geometry, statistics |
| [K0400](../items/K0400-forbidden-q-overlap-incidence-inversion.md) | 共円・共線q点禁則の全交差分布を点次数から復元する公式 | proposition | proved | geometry, statistics |
| [K0401](../items/K0401-n11-q12-terminal-extrema.md) | 11×11・q=12の極大安全配置の石数範囲103〜114 | proposition | proved | maximum-safe, maximal-safe, variants, strategy-length |
| [K0402](../items/K0402-nonprimitive-thirtythree-double-row-width-bounds.md) | 33本の非原始二重点行の初出幅 F(33) は631〜743 | proposition | proved | geometry, rectangles, variants |
| [K0403](../items/K0403-unequal-top-h-terminal-spectrum-and-hole-count.md) | 異容量上位h列ゲームの極大配置・終局石数と欠番数 | proposition | proved | variants, maximal-safe, statistics, strategy-length |
| [K0404](../items/K0404-two-tall-unequal-capacity-grundy.md) | 異容量二高列上位2列ゲームの終局石数と完全Grundy公式 | proposition | proved | variants, grundy, maximal-safe, strategy-length |
| [K0405](../items/K0405-unequal-capacity-extremal-terminal-spectrum.md) | 容量上限Mの全異容量ゲームで均一容量が終局スペクトル3指標を同時最大化 | proposition | proved | variants, maximal-safe, statistics, strategy-length |
| [K0406](../items/K0406-one-tall-all-h-grundy.md) | 一高列と単位容量短列からなる全上位hゲームのGrundy値 | proposition | proved | variants, grundy, maximal-safe, strategy-length |
| [K0407](../items/K0407-unequal-row-chord-energy-multiline-optimum.md) | 異なる高さの行対の2+2共円数に対する鋭い上界と同時達成 | proposition | proved | geometry, statistics, rectangles |
| [K0408](../items/K0408-three-row-211-classification-and-counts.md) | 3水平行盤の2+1+1共円四点組の分類と厳密計数 | proposition | proved | geometry, statistics, rectangles |
| [K0409](../items/K0409-outer-211-chord-length-density-zero.md) | 外側二重点型の共円完成弦長は無限に存在するが自然密度0 | proposition | proved | geometry, statistics, rectangles |
| [K0410](../items/K0410-scaled-circle-gcd-family.md) | 整数円の拡大族における二重点行数・gcd・短区間構成 | proposition | proved | geometry, rectangles, verification |
| [K0411](../items/K0411-central-chord-enclosed-length-bound.md) | 三水平行中央弦型の共円完成点が弦内にある場合の鋭い長さ上界 | proposition | proved | geometry, rectangles |
| [K0412](../items/K0412-exact-double-rows-sixtyfour-to-threehundredthirtysix.md) | 標準整数格子64〜336行で円が二点ずつ通る行数の厳密最大値 | proposition | proved | geometry, rectangles, variants |
| [K0413](../items/K0413-explicit-double-row-constructions-49-384.md) | 整数円の二重点行49〜384本に対する明示的構成下界 | proposition | proved | geometry, rectangles |
| [K0414](../items/K0414-n11-reply27-root-loss.md) | 11×11二石局面{60,27}は元先手固定視点でLOSS | proposition | computed | square-outcomes, certificates, verification, provenance |
| [K0415](../items/K0415-n11-opening-first-move-d4-partial-classification.md) | 11×11空盤の初手D4分類で2軌道をLOSS、19軌道は未確定 | proposition | computed | square-outcomes, first-moves, certificates, verification |
| [K0416](../items/K0416-n11-reply27-terminal-proof-dependency-gap.md) | 二石root {60,27} のterminal-only証明には2,992個の未閉鎖S5依存根が残る | computation | computed | square-outcomes, search-methods, certificates, verification, provenance |
| [K0417](../items/K0417-n11-joint-s5-proof-plan-19-roots.md) | 19残存初手の共同S5計画は第8次更新（層別外3件＋S6未反映2件＋150871 LOSS）で上界31,859・整数下界6,587 | computation | computed | square-outcomes, search-methods, certificates, verification, provenance |
| [K0418](../items/K0418-n11-joint-plan-dual-certificate-integer-bound.md) | 第8次更新後の共同計画の厳密双対182572529/27720は整数下界6,587 | computation | computed | square-outcomes, search-methods, certificates, verification, provenance |
| [K0419](../items/K0419-n11-noncentral-replies-lose-to-central.md) | 初手49・38・16の非中央応手27・93は中央応手に楽観的S5数で約1.5倍劣る | computation | computed | square-outcomes, search-methods, certificates, verification, provenance |
| [K0420](../items/K0420-n11-firstmove-win-side-cost-and-strategy.md) | 初手49のWIN側frontierは第8次再被覆で1,928証人・6.6k AND幅・未閉鎖1,661 | computation | computed | square-outcomes, search-methods, certificates, verification, provenance |
| [K0421](../items/K0421-safe-child-d4-equivalence-stabilizer-orbits.md) | 四石以上の安全局面では子のD4同値と親安定化群の着手軌道が一致する（四石条件は鋭い） | proposition | proved | geometry, search-methods, certificates, verification |
| [K0422](../items/K0422-n11-joint-s6-quotient-and-corrected-pilots.md) | 11盤共同S5計画の319万合法辺は156万相異なるS6へ縮約し、訂正済み39パイロットは2269子 | computation | computed | search-methods, certificates, verification, square-outcomes, provenance |
| [K0423](../items/K0423-n11-symmetric-s5-terminal-loss-and-win-pilots.md) | 11盤の対称S5二局面を終局DAGで独立証明し、共同計画の衝突候補209644は先手WIN | proposition | proved | square-outcomes, certificates, verification, search-methods, provenance |
| [K0424](../items/K0424-n11-nine-s5-terminal-verdicts-and-stratified-plan.md) | 11盤のS5九局面を終局DAGで独立証明し、共同計画を層別13・上界31,774・下界6,585へ更新 | proposition | proved | square-outcomes, certificates, verification, search-methods, provenance |
| [K0425](../items/K0425-four-row-eight-point-chord-gap.md) | 4行8点円の非局所型は単調で隣接弦長差が10以上 | proposition | proved | geometry, rectangles, variants |
| [K0426](../items/K0426-n11-targeted-terminal-lift-and-s6-loss.md) | 11盤のS6 LOSSと3件のS8 LOSSの終局証明を独立検証し、固定計画の要求S5和集合を31,774から31,771へ縮小 | verification | verified | square-outcomes, certificates, verification, search-methods, provenance |
| [K0427](../items/K0427-four-row-q8-mod27-chord-classes.md) | 4行8点円の弦長平方は法27で四つの型に限られる | proposition | proved | geometry, rectangles, variants |
| [K0428](../items/K0428-four-row-q8-mod27-type-locally-soluble.md) | 未出現の法27第四弦長型は全ての有限法で局所可解 | proposition | proved | geometry, rectangles, variants |
| [K0429](../items/K0429-four-row-q8-circle-count-reflection-congruence.md) | 4行8点円数は反射対称性から法2・法4で決まる | proposition | proved | geometry, rectangles, variants |
| [K0430](../items/K0430-four-row-q8-three-circle-union-finite-bound.md) | 2000001列まで異なる三つの4行8点円は合併20点以上 | proposition | computed | geometry, rectangles, variants |
| [K0431](../items/K0431-four-row-q8-every-nonlocal-circle-pell-extension.md) | 四行8点円の全ての非局所型は同じ傾きの無限Pell族へ延長する | proposition | proved | geometry, rectangles, variants |
| [K0432](../items/K0432-four-row-q8-slope-finite-criterion-and-congruence.md) | 非局所4行8点円の傾きは有限判定でき、各円型は任意法で無限延長する | proposition | proved | geometry, rectangles, variants |
| [K0433](../items/K0433-n11-unclosable-replies-pool-shortage-and-certificate-reuse.md) | 初手49の閉鎖不能8応手は保存pool制約の産物であり、証明書の逆向き再利用は新規S5 WINを与えない | computation | computed | square-outcomes, search-methods, certificates, verification, provenance |
| [K0434](../items/K0434-integer-determinant-circle-line-equivalence.md) | 整数座標四点の行列式と分母を払った円・直線方程式の同値 | proposition | proved | rules, geometry, formalization |
| [K0435](../items/K0435-three-cube-five-point-lean-certificate-check.md) | 3×3×3・5点禁止ゲームの839局面証明書をLeanで具体検査し空盤後手必勝を証明 | verification | verified | formalization, certificates, variants |
| [K0436](../items/K0436-anisotropic-mod9-all-widths.md) | 異方整数格子の全幅で3進付値条件下の円点数は2ceil(2w/3)以下 | proposition | proved | geometry, rectangles, variants, grundy |
| [K0437](../items/K0437-few-residual-hyperedges-grundy-ceiling.md) | 残余禁止辺h本の一点追加ゲームはGrundy値が最大2^h−1（h≥1） | proposition | proved | grundy, residual-games, variants, geometry |
| [K0438](../items/K0438-finite-point-kayles-pspace-complete.md) | 任意有限整数点盤の指定安全局面の共円ゲーム勝敗判定はPSPACE完全 | proposition | proved | geometry, grundy, residual-games, variants, search-methods |
| [K0439](../items/K0439-five-edge-grundy-seven.md) | 5個の残余禁止集合でGrundy値7を達成する抽象回避ゲーム | proposition | proved | grundy, residual-games, variants |
| [K0440](../items/K0440-five-row-anisotropic-mod3-circle-exclusion.md) | 異方整数格子の五行で9点円は存在せず、3進付値条件下で全長強解決する | proposition | proved | rectangles, geometry, variants, grundy |
| [K0441](../items/K0441-fixed-grundy-five-witness-residual-exclusion.md) | 固定11点Grundy5証人は13×13以下の標準盤で正確な残余ゲームにならない | proposition | computed | grundy, residual-games, geometry |
| [K0442](../items/K0442-four-point-pair-sums-reflection-only.md) | 4点の無順序二点和復元では中心反射が唯一の曖昧性 | proposition | proved | geometry, variants |
| [K0443](../items/K0443-four-residual-edges-rank4-nimber-five.md) | 残余禁止辺4本以下・rank4の通常Grundy値は5以下で、孤立点なしの達成型は2種類 | proposition | proved | residual-games, grundy, search-methods |
| [K0444](../items/K0444-four-row-pell-orbit-count-oscillation.md) | 4行8点円の既知Pell族の円数は厳密閉公式を持ち対数周期振動する | proposition | proved | geometry, rectangles, variants, statistics |
| [K0445](../items/K0445-four-row-q8-circle-count-log-upper.md) | 四行8点円の総数は O(m² log m) 以下 | proposition | proved | geometry, rectangles, variants |
| [K0446](../items/K0446-four-row-q8-gaussian-census-100m.md) | 四行8点円の最大弦長1億までの有限完全分類 | computation | computed | geometry, rectangles, statistics |
| [K0447](../items/K0447-four-row-q8-infinite-slope-accumulation-loglog.md) | 四行8点円の実現傾きは無限個の集積点を持ち種類数は対数×二重対数以上 | proposition | proved | geometry, rectangles, variants |
| [K0448](../items/K0448-four-row-q8-infinitely-many-distinct-slopes.md) | 4行8点円には相異なる実現可能な既約傾きが無限種類ある | proposition | proved | geometry, rectangles, variants |
| [K0449](../items/K0449-four-row-q8-mod64-odd-denominator-obstruction.md) | 4行8点円の奇数分母傾きは法64で4合同類に限られる | proposition | proved | geometry, rectangles, variants |
| [K0450](../items/K0450-four-row-q8-perfect-slope-closure.md) | 四行8点円の実現傾きは非空な完全閉包を持ち集積点が非可算個存在する | proposition | proved | geometry, rectangles, variants |
| [K0451](../items/K0451-four-row-q8-slope-dimension-two-sieve.md) | 4行8点円の実現可能な既約傾き数R(H)はO(H²/(log H)²)以下 | proposition | proved | geometry, rectangles, variants, statistics |
| [K0452](../items/K0452-four-row-q8-three-dual-pell-slope-limits.md) | 四行8点円の実現傾きには少なくとも三つの集積点があり種類数は対数以上 | proposition | proved | geometry, rectangles, variants |
| [K0453](../items/K0453-geometric-four-q4-grundy-five.md) | 整数6×6内の11点と4共円禁則でGrundy値5が実現し、点数・包含正方形が最小 | proposition | proved | geometry, grundy, residual-games, variants |
| [K0454](../items/K0454-half-integral-center-circle-band-maxima-through-63.md) | 5〜63連続整数行で水平中心が半整数の円の最大格子点数は二重点行数の2倍 | proposition | proved | geometry, rectangles, variants |
| [K0455](../items/K0455-independent-row-capacity-state-counts.md) | 独立行容量ゲームの勝敗局面数と非終局負け局面の漸近密度 | proposition | proved | rectangles, variants, grundy, statistics |
| [K0456](../items/K0456-independent-row-win-loss-mobility-distribution.md) | 独立行容量ゲームの勝敗別合法手数分布と条件付き平均の厳密公式 | proposition | proved | variants, grundy, statistics |
| [K0457](../items/K0457-lattice-three-parallel-four-q6-circles.md) | 3本の平行直線に各4整数点で6点円3本を実現できる | proposition | proved | geometry, variants, rectangles |
| [K0458](../items/K0458-new-four-row-q8-slope-181273-over-40152.md) | 四行8点円には新しい既約傾き181273/40152の無限Pell族がある | proposition | proved | geometry, rectangles, variants |
| [K0459](../items/K0459-pairsum-reconstruction-power-of-two.md) | 無順序二点和からのn点復元はnが2の冪のときに限り非単射 | proposition | proved | geometry, rectangles, variants |
| [K0460](../items/K0460-path-cycle-grundy-periodicity.md) | 二点禁止の道Grundyは52以降最小周期34、最大次数2の鋭い上界は15 | proposition | proved | grundy, residual-games, search-methods, strategy-length |
| [K0461](../items/K0461-prime-adic-anisotropic-row-sparsity.md) | 異方格子の水平間隔に余分な奇素因子があれば円は幅以下の点しか持たない | proposition | proved | geometry, rectangles, variants, grundy |
| [K0462](../items/K0462-residual-three-small-edges-grundy-bound.md) | 残余禁止集合が3個以下かつ各4点以下ならGrundy値は3以下 | proposition | proved | grundy, residual-games, search-methods, variants |
| [K0463](../items/K0463-safe-extension-counting-and-terminal-gap.md) | 任意有限整数点盤の安全延長・終局計数は#P完全で極大長差は無界 | proposition | proved | geometry, variants, maximal-safe, maximum-safe, residual-games, search-methods |
| [K0464](../items/K0464-spaced-five-row-q9-mod9.md) | 5本の等間隔整数行で間隔が3の倍数でなければ9点円は存在せず全長強解決 | proposition | proved | rectangles, geometry, variants, grundy |
| [K0465](../items/K0465-sunflower-residual-grundy-closed-form.md) | ヒマワリ型残余禁止集合の全Grundy値は閉形式で高々3 | proposition | proved | grundy, residual-games, search-methods |
| [K0466](../items/K0466-symmetric-five-column-q6-rigidity.md) | 3×5・q=6の左右対称列では非等差なら6点円は最大2本、等差なら最大4本 | proposition | proved | rectangles, variants, geometry, grundy, maximal-safe |
| [K0467](../items/K0467-tangent-mod16-fixed-width-circle-capacity.md) | 接線行の法16制約による固定幅円点数の上界と5〜16行の厳密値 | proposition | proved | geometry, rectangles, variants, grundy |
| [K0468](../items/K0468-three-by-five-q6-real-row-gap-classification.md) | 3×5・q=6は任意の正実数行間隔で6点円が最大4本、空盤Grundyは円1本の場合のみ0 | proposition | proved | rectangles, variants, geometry, grundy, maximal-safe, statistics |
| [K0469](../items/K0469-three-by-four-q6-row-spacing-classification.md) | 3×4・6点版は行間隔の3等式で禁止円数と空盤Grundyが完全に決まる | proposition | proved | rectangles, variants, geometry, grundy |
| [K0470](../items/K0470-three-column-arbitrary-integer-spacing.md) | 任意の整数間隔の三列格子における最大共円点数の完全分類 | proposition | proved | geometry, rectangles, variants |
| [K0471](../items/K0471-three-column-constant-five-unbounded-six-onset.md) | 三列異方格子では5点円初出を3行に固定して6点円初出を無界にできる | proposition | proved | geometry, rectangles, variants |
| [K0472](../items/K0472-three-column-five-implies-six.md) | 任意の整数間隔の三列格子で5点円があれば6点円が無限に存在する | proposition | proved | geometry, rectangles, variants |
| [K0473](../items/K0473-three-column-five-six-height-gap.md) | 三列異方格子の5点円と6点円の初出行数差は無界で初出円は2本と1本 | proposition | proved | geometry, rectangles, variants |
| [K0474](../items/K0474-three-column-four-row-generic-q4.md) | 不等間隔三列四行q4の一般位置は後手勝ちで全初手Grundy値4 | proposition | proved | rectangles, variants, geometry, grundy, first-moves, maximal-safe |
| [K0476](../items/K0476-three-parallel-four-point-q6-circle-count.md) | 3本の平行直線・各4候補点で6点円は最大3本、達成可能 | proposition | proved | geometry, variants, grundy |
| [K0477](../items/K0477-three-parallel-four-q6-minimum-integer-box.md) | 3整数水平行・各4点の6点円3本を実現する最小包囲格子は7×4 | proposition | proved | geometry, variants |
| [K0478](../items/K0478-three-parallel-q6-eighteen-candidate-obstruction-rigidity.md) | 任意三平行線の6点禁止ゲームで18候補不足極大は同和弦energy14の剛性型に限る | proposition | proved | rectangles, geometry, variants, maximal-safe |
| [K0479](../items/K0479-three-row-five-circle-and-q5-grundy.md) | 不等間隔三列・三行の5点円本数とq=5全安全局面Grundyを完全分類 | proposition | proved | geometry, rectangles, variants, grundy |
| [K0480](../items/K0480-three-row-five-common-columns-six-point-circles.md) | 3行・共通5列の6点円は最大4本で等号は正方格子型に限る | proposition | proved | geometry, rectangles, variants |
| [K0481](../items/K0481-three-row-q4-all-spacing-first-moves.md) | 不等間隔三列三行q=4は全正整数間隔で全9初手が勝ち | proposition | proved | geometry, rectangles, variants, grundy |
| [K0482](../items/K0482-tree-grundy-minimum-orders-through-eight.md) | 二点禁止残局の木でGrundy値0〜8を実現する最小頂点数 | proposition | proved | grundy, residual-games |
| [K0483](../items/K0483-two-forbidden-hyperedges-closed-grundy.md) | 禁止集合が高々二つの有限配置ゲームは全安全局面のGrundy値に閉公式を持ち3以下 | proposition | proved | grundy, residual-games, search-methods, variants |
| [K0484](../items/K0484-width-five-q9-all-lengths.md) | 五行九点版は全長で行容量だけに分離しM_{5,9}=8 | proposition | proved | rectangles, geometry, variants, grundy |
| [K0485](../items/K0485-n11-four-s7-win-and-s6-correction-verified.md) | 11盤の既知S7 WIN四件を終局から独立再検証し、S6のUNKNOWN誤記を訂正 | verification | verified | square-outcomes, certificates, verification, provenance |
| [K0486](../items/K0486-n11-compact385-terminal-proof-and-s7-lift-verified.md) | 11盤35個のS8 LOSSの385終局葉証明と246個のS7 LOSSへの伝播を独立検証 | verification | verified | square-outcomes, certificates, verification |
| [K0487](../items/K0487-n12-twelve-stone-maximal-safe-set-verified.md) | 12×12に12石の極大安全集合が存在する（検証済みwitness） | proposition | computed | maximal-safe, geometry |
| [K0488](../items/K0488-n13-thirteen-stone-maximal-safe-set-verified.md) | 13×13に13石の極大安全集合が存在する（検証済みwitness） | proposition | computed | maximal-safe, geometry |
| [K0492](../items/K0492-three-row-six-circle-first-width-two-squares.md) | 等間隔三行の6点円の最初の可能幅と二平方和による円数公式 | proposition | proved | geometry, rectangles, variants |
| [K0493](../items/K0493-residual-closed-form-kernel-saved-n11-benchmark.md) | 監査済み残余ゲームの構造別評価は保存済み11×11由来826局面で再帰呼出数を約21%削減 | computation | observed | residual-games, grundy, search-methods, verification, statistics |
| [K0494](../items/K0494-residual-handoff-gate-fixed-corpus-calibration.md) | 固定52局面の残余切替閾値比較ではOFFが最速で、深い3局面のUNKNOWN数も改善しなかった | computation | observed | residual-games, search-methods, verification, statistics |
| [K0495](../items/K0495-residual-completion-index-profile.md) | completion索引による残余構築は固定局面で従来scanと一致し、構築費用を削減した | computation | observed | residual-games, search-methods, verification, statistics |
| [K0496](../items/K0496-bounded-residual-outcome-search.md) | 予算付きP/N残余探索は固定826局面で独立oracleと一致しkernel呼出しを84%削減した | computation | observed | residual-games, search-methods, verification, statistics |
| [K0497](../items/K0497-small-residual-quota-prospective-confirmation.md) | 事前選択した残余quota128・閾値6は新規26局面でOFFより20.8%速く、固定深い3局面でも数値採用条件を満たした | computation | observed | residual-games, search-methods, verification, statistics |
