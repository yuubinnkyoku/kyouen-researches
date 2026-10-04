"""Lossless original-hypothesis inventory plus explicitly reviewed evidence.

Legacy labels are evidence pointers, never an automatic settled verdict.
The reviewed map is deliberately conservative: unreviewed is not unresolved.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import tempfile


BASE = Path(__file__).resolve().parents[1]
OUTPUT = BASE / "output"
REPORTS = BASE / "reports"
RESEARCH = BASE.parents[1]
BANKS = [RESEARCH/'archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md',
         RESEARCH/'archive/hypothesis-ledgers/hypothesis-bank-round2-2026-09-27.md']
ORIGINAL = re.compile(r'^- \*\*(B\d{3}) \[([^]]+)\] (.*?)\*\* (.+)$')
ID = re.compile(r'B\d{3}(?!\d)')
LABEL = re.compile(r'(?<![A-Z-])(SUPPORTED|REFUTED|PARTIAL|INCONCLUSIVE|NOT-CHECKED)(?![A-Z-])')
REVIEWED = {}


def atomic_text(path, text):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                                         dir=path.parent, prefix=path.name+'.', suffix='.tmp',
                                         delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(text)
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def review(ids, status, kind, source, reason, additional=()):
    for bid in ids.split():
        assert bid not in REVIEWED
        REVIEWED[bid] = {'original_status': status, 'evidence_kind': kind,
                         'preferred_report': source, 'reason': reason,
                         'additional_reports': list(additional)}


review('B088', 'PARTIAL', 'explicit_full_split_prime_linear_construction',
       'round61-full-split-prime-safe-construction.md',
       'p≡1 mod4でa²=-1、(t²+t,a(t²-t))の全p整数代表が安全。四点行列式8a VandermondeでKp≥pを自足証明・独立検算。既知線形下界の再構成、原文2n−O(1)は未達。')
review('B082', 'PARTIAL', 'independent_nineteen_stone_extension_and_local_exclusion',
       'round57-nineteen-stone-ten-board-bound.md',
       '公開九盤18石を移動して一点追加、全3876四点組で十盤19石安全。行内点対上界23。特定19石から除去9まで完全に20石なし、一般20石の不在や等号20は未証明。',
       ('round59-60-final-ten-board-search.md',))
review('B087', 'SUPPORTED', 'complete_maximum_catalogue_embedding_obstruction',
       'round58-original-maximum-extension-obstruction.md',
       '完全n7最高層16配置が旧カタログと一致。全64平行移動・3200空点は直接行列式と曲線係数で全禁止。独立安全15石によりK8≥15>14、K8上界に依存せず原文存在を証明。')
review('B081', 'REFUTED', 'published_construction_with_independent_coordinate_certificate',
       'round55-eighteen-stone-original-counterexample.md',
       'モナカ氏公開図の18石を座標化し全3060四点組・禁止族・全三点曲線で安全性を独立検算。K9≥18で原文17を反証、上界18や全軌道分類は未証明。')
review('B098', 'SUPPORTED', 'complete_small_board_saturation_jump',
       'round54-small-board-saturation-jump.md',
       '原文にn≥4の指定なし。全n2/n3集合の監査でs2=3・s3=5、差2の存在を証明。n≥4を追加した問いの決着は主張しない。')
review('B097', 'PARTIAL', 'complete_finite_saturation_sequence',
       'round54-small-board-saturation-jump.md',
       '完全値s1..s9=1,3,5,5,5,6,7,8,9、十盤八石全域除外でs10∈[9,10]。有限n1..10の単調性まで確認、全nの原文は未決。',
       ('round56-ten-board-eight-stone-exclusion.md',))
review('B095 B096', 'PARTIAL', 'general_asymptotic_lower_exponent_proof',
       'round52-general-saturation-exponent-lower-bound.md',
       '原始方向別に直線被覆O(n k^(3/2))、三点真円の整数係数と約数上界でR(n)=n^o(1)。全ε>0でs_n>n^(2/3−ε)を証明。対応する上界・s_n=o(n)は未証明。')

review('B079', 'PARTIAL', 'exact_geometric_cover_incidence_maximization',
       'round48-six-stone-cover-incidence.md',
       '十盤六石の重複被覆総数は全安全集合最大85<必要94、等号証人を独立検算。上界は完全最適化に依存し、原文の短い非列挙証明は未達。')
review('B094', 'REFUTED', 'independently_verified_ten_stone_maximal_witness',
       'round49-ten-stone-maximal-counterexample.md',
       '十盤S=[21,27,31,35,36,46,65,81,29,48]は全210四点安全・全90空点禁止、s10≤10で原文11を反証。')
review('B093', 'PARTIAL', 'complete_eight_stone_prefix_suffix_exclusion_and_ten_stone_witness',
       'round56-ten-board-eight-stone-exclusion.md',
       's9=9から十盤八石候補を全幅・初点0..4へ帰着。旧完了接頭部と今回全五再開部分を接続し八石全域除外、s10∈[9,10]。九石の有無が未決。',
       ('round49-ten-stone-maximal-counterexample.md','round51-ten-board-seven-stone-exclusion.md',
        'round59-60-final-ten-board-search.md'))

review('B091', 'SUPPORTED', 'complete_all_lower_sizes_exclusion_and_finite_witness',
       'round46-small-saturation-and-window-reduction.md',
       '8×8のk≤4は三つ組補完上界、k5/6/7は個別の完全探索で除外。八石極大証人を独立幾何で検算しs8=8。')
review('B092', 'SUPPORTED', 'complete_lower_sizes_exclusion_and_window_orbit_exhaustion',
       'round46-small-saturation-and-window-reduction.md',
       '9×9のk≤7を除外、九石証人を検算。408配置の全1632埋め込みに合法外点、八石候補の初点をD4で0..4へ帰着し全19.5億節点探索が完了、s9=9。')
review('B077 B080', 'SUPPORTED', 'finite_witness_and_general_minimum_stone_count_proof',
       'round47-private-cover-and-global-minima.md',
       '4×4の全空点二重以上六石証人・完全一重被覆五石証人を独立検算。曲線上界と残る小盤の全域検査で最小石数6/5、最小盤4を証明。')
review('B078 B361', 'SCOPE_UNCLEAR', 'degenerate_endpoint_and_complete_finite_nondegenerate_support',
       'round47-private-cover-and-global-minima.md',
       'n1の全占有最小極大には空点なし、B078の存在節は偽・ρは未定義。非空空点の読みはn2..8全最小極大でmin b1・ρ1、n≥9一般命題は未証明。',
       ('round50-nine-board-private-point-family.md',))


review('B349', 'SUPPORTED', 'general_minimum_classification_and_finite_realizations',
       'round40-b349-minimum-four-edge-classification.md',
       '二点競合ありの最小合法点数5・全9型を証明し全型を格子実現。競合なしを含める読みの最小4・単独辺1型も分類。')
review('B057 B441 B443', 'REFUTED', 'complete_exact_family_counterexample',
       'round42-exact-residual-family-audit.md',
       '4×4四石・同一L/Rの完全族は二集合のみ。三石交換が必要、Rは連結な四点パス。全65536集合から抽出。')
review('B444 B446 B449', 'SUPPORTED', 'complete_exact_family_witness',
       'round42-exact-residual-family-audit.md',
       '非空連結Rの分裂、同一族別成分で最大一石解除数8対7、厳密抽象同型40集合の四成分分裂を検算。B446旧反証を訂正。')
review('B448', 'PARTIAL', 'general_four_stone_bridge_proof',
       'round42-exact-residual-family-audit.md',
       '任意の安全四石配置対は常に安全な三石層のJohnsonグラフを通って結べる。k≥5の原文全体は未証明。')
review('B350', 'SUPPORTED', 'finite_witness_and_general_minimum_legal_size_proof',
       'round43-b350-value-preserving-move-switch.md',
       '5×5の合法5点で両版g1・勝ち手1対5。全m≤4極小残余族を二方式全列挙し最小合法点数5、n≤3全域除外と4×4証人で最小盤4。')
review('B062', 'REFUTED', 'infinite_clique_family_and_minimum_board_counterexample',
       'round44-three-stone-cliques-and-tree-minima.md',
       '三石の標準整数盤に任意大のK4Mを実現、彩色数は無界。4×4初例は厳密χ6、全n≤3三石は三色で最小盤4。')
review('B064', 'SUPPORTED', 'finite_witness_and_general_minimum_legal_size_proof',
       'round44-three-stone-cliques-and-tree-minima.md',
       '3×3のP5+一三点辺でg0対3、最小盤3。木の勝敗反転の最小合法点数5を証明。値だけの変更の最小4と区別。')
review('B344', 'PARTIAL', 'minimum_connecting_tree_classification',
       'round44-three-stone-cliques-and-tree-minima.md',
       '効く三点辺の最小接続木はK1,3・三葉上の辺、格子実現を検算。大きな木の距離偶奇による一般分類は未証明。')
review('B071 B072 B075', 'SUPPORTED', 'general_geometric_proof_and_sharpness_certificates',
       'round45-cover-gap-and-sharp-overlap.md',
       '三点族の線形性と点対計数、異なる曲線の交点数で全盤証明。k≥4の改善上限−1、六石等号、二空点交差の最小石数6も検算。')
review('B073', 'REFUTED', 'general_impossibility_using_melchior_inequality',
       'round45-cover-gap-and-sharp-overlap.md',
       '反転後の通常直線数δ≥3。全k≥4で床付き二次上限から必ず1減り、床等号もSteiner等号も不可能。')


review('B211 B212 B215 B216 B220 B541 B546 B550', 'SUPPORTED', 'general_proof',
       'round4-fixed-width.md', '全固定幅の一様終局定理。必要な短い二行盤と区間証人も全数検査。')
review('B213 B219 B544 B555 B556', 'REFUTED', 'general_impossibility',
       'round4-fixed-width.md', '固定幅の全極大サイズ3w・全局面偶奇式により、原文の無限量化を除外。')
review('B542', 'SUPPORTED', 'general_proof_and_finite_certificate',
       'round4-two-row-order-strategy.md', 'm=6..8の順序型表と全m≥9の一般証明。旧PARTIALは上書き。')
review('B141 B145 B150 B471 B472 B473', 'SUPPORTED', 'general_proof',
       'round4-collinear-asymptotic.md', '整数方向別の恒等式と一様誤差による漸近証明。B141の旧REFUTEDを訂正。')
review('B074', 'REFUTED', 'infinite_counterexample_family',
       'round5-quadratic-cover.md', '安全格子の無限族でb/k→∞、絶対定数の線形上界を反証。')
review('B356', 'SUPPORTED', 'infinite_witness_family',
       'round5-quadratic-cover.md', '安全二コピーの合併補題で二空点の固定二次下界。round24は別証明。',
       ('round24-circular-cubic-multiple-cover.md',))
review('B357', 'REFUTED', 'infinite_counterexample_family',
       'round7-parabola-cover.md', '固定εでも高被覆空点数Ω(k)。二次幅の整数盤。round24は別証明。',
       ('round7-ellipse-cover.md', 'round24-circular-cubic-multiple-cover.md'))
review('B360', 'SUPPORTED', 'infinite_witness_family',
       'round5-cover-union.md', '同盤・同石数・双方bmax=Θ(k²)で禁止点和集合比が無界。')
review('B557', 'REFUTED', 'finite_exhaustion_and_witness',
       'round5-row-thresholds.md', '五行幅11の不存在と幅12の安全15石。全称のw=5反例。')
review('B558', 'SUPPORTED', 'general_proof',
       'round8-ap-quadratic-prime.md', '全wに対する素数公差の三点AP、幅O(w²)。旧公差1候補の未証明と区別。')
review('B351 B354 B355', 'SUPPORTED', 'general_proof_using_published_theorems',
       'round6-rational-orchard.md', '反転・安全化補題、Green–TaoとMazurの適用条件を確認した一般証明。')
review('B353', 'REFUTED', 'general_impossibility_using_published_theorems',
       'round6-rational-orchard.md', '有理点のδ/k→∞で、原文の線形欠損の無限族を除外。')
review('B352', 'PARTIAL', 'partial_general_bound',
       'round6-rational-orchard.md', 'δ>k(log log k)^ηは固定冪k^(1+ε)の下界ではない。')
review('B381 B382', 'SUPPORTED', 'finite_complete_classification',
       'round9-n7-outer-patterns.md', '既存全16最大配置の全外点を二方式で照合し、最初の半径2の型を分類。')
review('B386', 'REFUTED', 'finite_counterexample',
       'round9-n7-n8-overlap.md', '7×7最大から一石除去・二石追加で8×8安全15石。')
review('B387', 'SUPPORTED', 'finite_exhaustion_and_witness',
       'round9-n7-n8-overlap.md', '全16最大・全埋込みでA型の最小除去1、B型2。既知K8=15を使用。')
review('B388', 'SUPPORTED', 'general_proof',
       'round9-external-rays.md', '二乗直径による円の外接領域上界と、遠方直線だけの合法外点算法。')
review('B384 B385 B390', 'PARTIAL', 'finite_evidence_and_partial_general_result',
       'round16-dilation-exterior.md', '拡大後r=1は最大性・最小極大性・一石移動を保存せず、原文は未決着。')
review('B376', 'REFUTED', 'finite_exhaustion',
       'round10-small-saturation.md', '8×8全408安全8石極大に被覆曲線13本以上。貪欲上界を下界に使わない。')
review('B377 B379', 'SUPPORTED', 'finite_exhaustion_and_witness',
       'round10-small-saturation.md', '7石一合法点の縮約と、8石から9×9の9石極大への具体的拡張。')
review('B453', 'SUPPORTED', 'general_proof',
       'round10-circle-denominator.md', '分母素因数型と剰余類の完全格子点数上界、q=3/4の等号。')
review('B454', 'REFUTED', 'finite_counterexample_and_exhaustion',
       'round12-b454-counterexample.md', 'm=11で奇分母q=11のスパン161を実現し、全2冪分母候補を除外。')
review('B455', 'REFUTED', 'general_impossibility',
       'round11-residue-orbits.md', 'q≥3の剰余類は90度回転の四個組。一つだけが厳密最大にはならない。')
review('B456', 'SUPPORTED', 'general_proof',
       'round11-circle-records.md', '固定分母の記録円に必要な平方類が無限。過去の最良円の整数拡大を除外。')
review('B461 B463 B465 B467', 'SUPPORTED', 'general_proof',
       'round4-circle-windows.md', '完全円の可変サイズ整数窓のスペクトルと一点削除の必要十分条件。')
review('B464', 'REFUTED', 'general_impossibility',
       'round4-circle-windows.md', '完全格子円の長方形窓・正方形窓スペクトルは常に一致。')
review('B462 B470', 'SUPPORTED', 'general_reduction_and_finite_exhaustion',
       'round4-circle-windows.md', '候補縮約を証明しn≤12を整数全走査。11点の最初の盤は11×11。')
review('B457', 'PARTIAL', 'partial_general_spectrum_result',
       'round4-circle-windows.md', '全サイズ和集合と固定窓の穴に一般結果。原文の同点数での統計比較は未完了。')
review('B458', 'SCOPE_UNCLEAR', 'counterexample_to_precise_subclaim',
       'round16-first-appearance.md', '指定要約量で四点初出が決まる強い読みは反証。「短く分類」の原文全体は未指定。')
review('B468', 'SCOPE_UNCLEAR', 'counterexample_to_monotonic_reading',
       'round4-circle-windows.md', '同完全点数・同スパンで単調性の反例。統計傾向には追加の母集団指定が必要。')
review('B142', 'REFUTED', 'general_asymptotic_refutation_using_published_theorem',
       'round17-original-scope-audit.md', '公刊C_n=Θ(n^5)は原文n^(4+o(1))と両立しない。n^6ではない。')
review('B475', 'SUPPORTED', 'general_proof_using_published_count',
       'round13-four-point-circles.md', '四点重みで盤内点数4へ集中。完全円上点数と区別。')
review('B476', 'REFUTED', 'general_asymptotic_refutation',
       'round13-four-point-circles.md', '四点重みの平均点数は4へ収束し、発散しない。')
review('B477', 'SUPPORTED', 'general_identity',
       'round15-standard-chord.md', '標準弦の原始方向・整数内積・既約分数による重複なし計数。')
review('B478', 'SUPPORTED', 'general_proof_using_published_count',
       'round13-poisson-limit.md', '固定kの依存辺評価でPoisson極限。有限nの束は反例にならない。')
review('B479', 'REFUTED', 'general_asymptotic_refutation',
       'round13-poisson-limit.md', '同尺度の束の確率は0へ。非自明な複合Poissonにはならない。')
review('B480', 'SUPPORTED', 'general_asymptotic_expansion',
       'round14-safety-correction.md', 'log安全確率の次項を三点共有の禁止ペアから導出。')
review('B089', 'REFUTED', 'general_asymptotic_refutation',
       'round17-b089-bounded-degree.md', '固定本数低次数曲線のo(n)上界と素数盤のK_n線形下界。')
review('B070 B261 B266', 'SUPPORTED', 'general_proof_and_infinite_construction',
       'round18-pair-synergy.md', '二手相乗を石ごとの一般化円へ分解し、無界の利得を整数格子で実現。')
# B070 has its own proof, not the pair-synergy report.
REVIEWED['B070'].update(preferred_report='round18-competition-stars.md',
                         reason='固定kのクリーク分割辺の和。全kで誘導星の禁止と鋭い整数実現。')
review('B227', 'REFUTED', 'general_impossibility',
       'round18-equal-passes.md', '両者各一回の未使用パス権で開始。同数有限パスの後追い応答。履歴の不均等状態と区別。')
review('B063', 'SUPPORTED', 'general_lower_bound_and_finite_witness',
       'round19-b063-stone-hierarchy.md', '誘導K1,4は三石で不可能、四石で実現。最小頂点数5も全型で確認。')
review('B253 B522', 'SUPPORTED', 'finite_witness_and_exhaustion',
       'round19-rule-removal-audit.md', '全単独・全ペア解除を除外し、三組解除の全真部分族と真のmexを検算。')
review('B255', 'SUPPORTED', 'finite_witness_and_minimum_board_proof',
       'round20-b255-maximum-preserving-flip.md', '5×5で最大サイズ9・全100最大配置を保存して反転。4×4以下は不可能。')
review('B224', 'SUPPORTED', 'finite_witness',
       'round21-b224-ten-curves.md', '5×5の四円・六直線で標準の非空勝ち初手9点を完全保存。最小本数とは言わない。')
review('B228', 'SUPPORTED', 'finite_witness',
       'round22-b228-circle-thresholds.md', '全直線を保持し円を点数降順に丸ごと追加、空盤g=2→0→2。')
review('B252', 'SUPPORTED', 'finite_witness',
       'round22-b252-one-circle-versus-scattered.md', '4×4で一円全70解除だけが反転。散在70解除では保存。')
review('B256', 'REFUTED', 'general_impossibility',
       'round23-b256-symmetric-minimum.md', '全nで非空最小族1または2をD4不変な互いに素な四点組が達成。')
review('B258', 'SCOPE_UNCLEAR', 'general_result_with_quantifier_ambiguity',
       'round23-b256-symmetric-minimum.md', '全n≥4に共通必須型なし。n=2を存在量化に含む読みは自明に真で、全体判定は保留。')
review('B251', 'PARTIAL', 'finite_exhaustion',
       'round32-b251-seven-board-exclusion.md', '7×7全6364単独解除を935軌道・二方式で除外。共有標準表全179810350局面の証明条件も検算。存在証人はn≥8。',
       ('round23-b251-six-by-six-exclusion.md',))
review('B333', 'REFUTED', 'finite_counterexample_and_minimum_board_proof',
       'round25-forced-length-holes.md', '6×6でWFT={7,11}、9なし。n≤5全状態の二方式検査。')
review('B031', 'REFUTED', 'finite_counterexample_and_minimum_board_proof',
       'round25-forced-length-holes.md', '6×6でT*={7,11}、9なし。旧n=5反例T*={6,7,9}は偶奇混在で不可能。')
review('B334', 'SUPPORTED', 'finite_witness_and_minimum_board_proof',
       'round25-forced-length-holes.md', '6×6の3石N局面でT*={6,8,10}、WFT空。固定長AND/ORでも確認。')
review('B022 B315', 'SUPPORTED', 'finite_complete_classification_and_witness',
       'round28-seven-board-original-verdicts.md', '7×7全179810350安全局面を二方式で照合。σ7=4、J7中央は関節点。')
review('B040 B313 B314', 'REFUTED', 'finite_counterexample_and_complete_verification',
       'round28-seven-board-original-verdicts.md', '7×7空盤WFTは空。四隅の唯一の応答先が中央で、近完全マッチングなし・橋四本。')
review('B006 B016 B021 B319 B321 B322 B331 B335', 'PARTIAL', 'finite_complete_classification',
       'round28-seven-board-original-verdicts.md', '7×7までの一石・飽和・J・空盤WFTを完全検査したが、原文の無界全称は未証明。')
review('B362 B367 B369', 'SUPPORTED', 'finite_witness',
       'round29-fault-witness-audit.md', '独立幾何で原文の故障耐性・解除割合・最大集合不要石の具体的証人を照合。旧決着の監査。')
review('B368', 'REFUTED', 'finite_counterexample_and_exhaustion',
       'round29-fault-witness-audit.md', '3×3全512部分集合の極大は全て5石。最小極大の石2を除いても元の空点は全て禁止。')
review('B047', 'REFUTED', 'finite_counterexample_with_exact_residual_game',
       'round31-b047-odd-cycle-counterexample.md', '5×5の6石から残余C5を正確に実現。頂点推移的Pで合法点5個なので固定点なしの応答対合は不可能。')
review('B343', 'SUPPORTED', 'finite_witness_with_sole_triple_and_full_certificate',
       'round33-b343-single-triple-switch.md', '6×6でRの三点辺がちょうど一つ。単独除去でg=1→3、勝ち手{14}→{15,19}は互いに素。全256拡張を独立検算。')
review('B067', 'REFUTED', 'finite_counterexample_with_exact_height',
       'round34-b067-induced-seven-cycle.md', '4×4でh=3の全256拡張を検査。二点競合の誘導C7に弦なし。旧K(S)の計算バグの留保を解消。')
review('B068', 'SUPPORTED', 'finite_cospectral_witness_pair',
       'round34-b068-cospectral-opposite-games.md', '6×6の二点残余のみの8頂点対で次数列・厳密特性多項式が一致、g=3と0。両256拡張と多項式行列式を独立検算。')
review('B524', 'SUPPORTED', 'finite_witness_and_cardinality_minimum_proof',
       'round35-empty-intersection-minimum.md', '4×4で三組の共通点が空、全三組だけg=0→2。全8部分族全安全局面の独立mex一致と既存全単独・全ペア除外で基数最小。')
review('B523', 'REFUTED', 'cardinality_minimum_counterexample',
       'round35-empty-intersection-minimum.md', '基数最小の三組反転解除族の共通部分が空。共有三点を要求する全称への反例。',
       ('round19-rule-removal-audit.md',))
review('B521', 'SUPPORTED', 'finite_complete_exhaustion',
       'round19-rule-removal-audit.md', '4×4全18721二組解除を2554D4軌道で検査し全てP。既存原文決着の採用。')
review('B501 B506', 'REFUTED', 'exact_rational_finite_counterexamples',
       'round36-random-original-witness-audit.md', '既存P証人を独立整数幾何・全継続Fraction再帰で再検算。5×5でp=2383/3360>2/3、4×4のh3で76/135>1/2。')
review('B502', 'SUPPORTED', 'exact_rational_finite_witness',
       'round36-random-original-witness-audit.md', '6×6のP証人mask35652737、p=5162/6615>3/4。全115安全拡張のg・p・hを厳密検算。既存決着の採用。')
review('B342', 'REFUTED', 'finite_counterexample_with_forest_and_single_deletion',
       'round37-residual-original-witness-audit.md', '4×4のS=[0,2]、二点競合は五辺マッチング。極小三点辺[1,10,12]の単独除去でg=5→0を独立全安全mex検算。')
review('B346', 'SUPPORTED', 'finite_pair_synergy_witness',
       'round37-residual-original-witness-audit.md', '3×3のS=[0,1,4]、極小三点辺二つの単独除去はg0、同時除去だけg3。既存証人を原文照合・全安全mex再検算。')
review('B525', 'REFUTED', 'finite_whole_circle_counterexample',
       'round22-b252-one-circle-versus-scattered.md', '4×4の中央八点真円の全70四点組を丸ごと解除し空盤g=0→1。既存B252証人はB525の全称にも直接反例。')
review('B345', 'REFUTED', 'sole_minimal_triple_counterexample_and_minimum_legal_size',
       'round38-b345-sole-triple-clique-counterexample.md', '5×5のR=一二点辺+一三点辺。二点競合はK2+K1+K1、唯一の三点辺でg=1→3。全16拡張検算、非退化の最小合法点数4。')
review('B065', 'SUPPORTED', 'finite_witness_and_minimum_board_proof',
       'round41-b065-pair-empty-grundy-five.md',
       '8×8で二点辺0・合法7点・g=5。全128拡張を四方式、全67安全mexを三方式検算。n≤7全域除外と合わせ最小盤8。',
       ('round39-b065-seven-board-exclusion.md',))
review('B325 B326', 'PARTIAL', 'finite_complete_census_and_small_board_crosscheck',
       'round30-ceiling-orbit-finite-audit.md', '7×7全安全局面の天井・軌道・余裕を計算。B325の無限族とB326の全盤条件は未決着。')
review('B011 B015 B018 B301 B302 B303 B305 B307 B308 B309 B311', 'SUPPORTED',
       'finite_complete_classification_and_witness', 'round27-fixed-response-audit.md',
       '原文の固定盤量化を全状態再計算・全グラフ構成で検査。無限の全盤主張へ外挿しない。')
review('B012 B013 B014 B304 B306', 'REFUTED', 'finite_complete_classification',
       'round27-fixed-response-audit.md', 'J5全20辺と全マッチングを検査。B306は単一16交替サイクルで、旧説明を訂正。')
review('B317', 'SUPPORTED', 'finite_witness_and_exhaustive_certificates',
       'round27-fixed-response-audit.md', '4×4全112212完全マッチングが4/6手目で破れる。全証明書と逆順独立列挙で網羅。')


# 2026-10-04: B401-B450 original-scope audit.
# Legacy report labels are not copied blindly; quantifiers and "exactly" clauses are rechecked.
review('B401', 'REFUTED', 'finite_complete_counterexample',
       'round2-batch-b381.md',
       '7×7全16最大配置の最小特定ペアを全列挙。全16配置に同一D4点軌道からなる最小特定ペアがあり、「必ず異なる軌道」は反証。')
review('B402', 'PARTIAL', 'finite_structural_evidence',
       'round2-batch-b381.md',
       '最小特定ペアの相・方向分離を全16配置で照合したが、一方の点軌道だけで相を定められるのは6/16。完全な二段符号化は未構成。')
review('B403', 'SUPPORTED', 'finite_complete_witness',
       'round2-batch-b381.md',
       '7×7のB相8配置は全て、相をBに固定すれば一点で一意特定できる。原文の「場合がある」を満たす。')
review('B404', 'PARTIAL', 'finite_statistical_evidence',
       'round2-batch-b381.md',
       '7×7全16では特定ペア数17対21でも最近接最大配置距離は双方10。6×6標本では弱い正相関のみで、一般統計主張は未決着。')
review('B405', 'INCONCLUSIVE', 'audited_no_direct_test',
       'round2-batch-b381.md',
       '原文の逐次観測で最尤相が複数回切り替わるという条件を直接検査した証拠がない。既存特定ペア計算だけでは判定不能。')
review('B406', 'PARTIAL', 'finite_rank_computation',
       'round2-batch-b381.md',
       '7×7最大配置の49×49共起行列はrank 15で低ランク。ただし中心占有以外の主成分によるA/B分離と残りのD4方向表現は未検証。')
review('B407 B408', 'INCONCLUSIVE', 'audited_missing_asymptotic_evidence',
       'round2-batch-b381.md',
       '7×7有限配置の識別計算はあるが、VC次元の全n一様上界も、識別難度がlog nを超える盤列も証明・反証する証拠がない。')
review('B409', 'REFUTED', 'finite_complete_counterexample',
       'round2-batch-b381.md',
       '7×7全16最大配置で占有点のみの最小観測数も占有・非占有混合の最小観測数も2。空点情報で2点未満へ短縮できず原文を反証。')
review('B410', 'INCONCLUSIVE', 'single_board_comparison',
       'round2-batch-b381.md',
       '7×7ではD4型2種・共起rank15・最大配置側G12八成分が既知だが、「有効rankが型数より障壁を説明する」には複数盤比較が必要。')
review('B411', 'REFUTED', 'finite_complete_shortest_path_classification',
       'round2-batch-b411.md',
       '代表A-B間の最短14操作経路8本を全列挙。隣接合法交換で結ぶ経路グラフは3次元立方体ではない。')
review('B412', 'REFUTED', 'finite_complete_poset_obstruction',
       'round2-batch-b411.md',
       '8最短路は同じ14事象を使うが、全8路に共通する順序関係の交叉半順序だけで線形拡張が32個ある。8路すべてを線形拡張に含む任意の半順序はこの共通順序の部分関係なので拡張数は32以上となり、「ちょうど8」を満たせない。')
review('B413 B414 B415', 'SUPPORTED', 'finite_complete_shortest_path_classification',
       'round2-batch-b411.md',
       '最短8経路を全列挙。一時除去される共通石は全路で一点39のみ、同一点で一致し、第四角48の占有窓も全路で同じ長さ。')
review('B416', 'PARTIAL', 'finite_shortest_path_structure',
       'round2-batch-b411.md',
       '最短路誘導グラフ21頂点24辺に6個の4-cycleと6分岐を確認。ダイヤ形分岐は実在するが「すべての分岐が操作順のみ」という完全還元は未証明。')
review('B417', 'REFUTED', 'finite_complete_constrained_bfs',
       'round2-batch-b411.md',
       'A∪Bと第四角以外の点を使うG12内A-B経路の最短は20操作で、最短14より+6。「+2で長さ16」は反証。')
review('B418', 'REFUTED', 'finite_complete_constrained_bfs',
       'round2-batch-b411.md',
       '第四角の占有区間を2回にした最短経路は16操作で、1回の14操作から+2に過ぎない。「少なくとも+4」を反証。')
review('B419', 'REFUTED', 'finite_complete_obstruction_classification',
       'round2-batch-b411.md',
       '最短8経路の交換不能箇所を全検査すると原因となる禁止四点組は9種類。単一D4幾何型への集約は成立しない。')
review('B420', 'SUPPORTED', 'finite_complete_constrained_bfs',
       'round2-batch-b411.md',
       '第四角48の初使用までの最短操作数はA側9、B側3で非対称。原文の存在する非対称性を全BFSで確認。')
review('B421', 'REFUTED', 'finite_counterexample_component',
       'round2-batch-b411.md',
       '最大14石を含まないG12の311頂点成分に閉路があり、木ではない。')
review('B422', 'SUPPORTED', 'finite_witness_component',
       'round2-batch-b411.md',
       '最大14石を含まない311頂点G12成分に長さ16の誘導閉路を明示。長さ10以上という存在命題を満たす。')
review('B423', 'PARTIAL', 'finite_component_search',
       'round2-batch-b411.md',
       '発見済み非最大成分5個は最大311<903だが、全非最大成分の完全列挙ではないため全称は未決着。')
review('B424', 'REFUTED', 'finite_counterexample_component',
       'round2-batch-b411.md',
       '最大配置外の311頂点G12成分は13石局面を25個含む。8個以下という全称を反証。')
review('B425', 'PARTIAL', 'finite_component_typing',
       'round2-batch-b411.md',
       '孤立12石5例の一石除去後の再追加数多重集合は4型に圧縮できるが、孤立12石全体の完全分類ではない。')
review('B426', 'INCONCLUSIVE', 'finite_negative_search',
       'round2-batch-b411.md',
       '検査した孤立12石5例では、どの例にも元へ戻す以外の追加手を持つ11石子があり証人なし。存在命題なので有限不発見だけでは反証できない。')
review('B427', 'PARTIAL', 'finite_complete_bfs_on_known_examples',
       'round2-batch-b411.md',
       '既知の孤立12石5例は全てG11で13石へ到達したが、孤立12石全体の完全列挙ではないため「各」を確定しない。')
review('B428 B429', 'PARTIAL', 'finite_statistical_evidence',
       'round2-batch-b411.md',
       '孤立12石5例と903成分内12石を比較し、中心占有率と最大配置未使用軌道占有に差を観測。ただし標本5例かつ条件付き統制未完。')
review('B430', 'SUPPORTED', 'finite_witness',
       'round2-batch-b411.md',
       '同じ10軌道占有ベクトルを持ちながら、孤立12石と903成分内12石に分かれる型を2種確認。存在命題の証人。')
review('B431', 'SUPPORTED', 'exact_integer_and_fractional_certificates',
       'round2-batch-b411.md',
       '59禁止四点×6460候補の被覆で21本の整数解を明示し、分数双対値102/5=20.4>20を厳密検算。整数最適値は正確に21。')
review('B432', 'REFUTED', 'exact_fractional_optimum',
       'round2-batch-b411.md',
       '同じ被覆問題の分数primal/dual最適値は102/5=20.4。総重み21の実行可能双対は存在しない。')
review('B433', 'SUPPORTED', 'exact_integrality_gap',
       'round2-batch-b411.md',
       '整数最適21、分数最適102/5=20.4を厳密証明し、真のintegrality gap 3/5を確認。')
review('B434', 'REFUTED', 'fractional_upper_bound_impossibility',
       'round2-batch-b411.md',
       '各禁止四点が高々一候補を覆う21候補packingは分数双対の特殊場合だが分数最適20.4。21候補の存在は不可能。')
review('B435', 'PARTIAL', 'finite_minimum_cover_samples',
       'round2-batch-b411.md',
       '得られた21本最小被覆2解は20本を共有するが、全最小被覆の完全列挙ではないため「全最小被覆に共通」を確定しない。')
review('B436', 'PARTIAL', 'finite_minimum_cover_samples',
       'round2-batch-b411.md',
       '13石候補だけから得た最小21被覆72個は全て14石以上も覆った。ただし13石候補を覆う全最小被覆の完全分類ではない。')
review('B437', 'PARTIAL', 'finite_minimum_cover_samples',
       'round2-batch-b411.md',
       '見つかった最小21被覆2解は一対一入替で隣接するが、全最小解グラフの連結性は未証明。')
review('B438', 'SUPPORTED', 'finite_optimal_witness_pair',
       'round2-batch-b411.md',
       '整数最適21の被覆を2つ得ており、D4像でも同一円内交換でも一致しない幾何型を持つ。存在命題を満たす。')
review('B439', 'REFUTED', 'exact_class_weight_optimization',
       'round2-batch-b411.md',
       '候補を占有差dと角数だけの7属性クラスにまとめた双対最適化では最良値3.53で、21の下界に届かない。原文の指定属性だけでは不可能。')
review('B440', 'INCONCLUSIVE', 'audited_no_direct_test',
       'round2-batch-b411.md',
       'd=2,3被覆とは別の占有ポテンシャルへ枠を変えた短い静的証明は未探索。存在も不存在も判定できない。')
review('B442', 'PARTIAL', 'finite_exchange_width_lower_bounds',
       'round2-batch-b441.md',
       '4×4同一残局族で2交換非連結92族、3交換でも33族、4交換でも17族が非連結。交換幅が4を超える有限例は支持するが無界性は未証明。')
review('B445', 'SUPPORTED', 'finite_structural_classification',
       'round2-batch-b441.md',
       'n=4主要12残局族で、空点を塞ぐ担当石集合のシグネチャが分裂成分間で全て互いに素。成分ラベルとして実際に機能する具体例を確認。')
review('B447', 'REFUTED', 'finite_statistical_counterevidence',
       'round2-batch-b441.md',
       'n=4同一残局族64族で、分裂族の平均被覆分散0.0082は連結族0.178より小さく、原文予想と逆向き。')
review('B450', 'PARTIAL', 'finite_component_fixed_core_evidence',
       'round2-batch-b441.md',
       '分裂族8族で各成分の共通固定石群を列挙し局所遮蔽部品候補を得たが、別盤への置換・移植則そのものは未検証。')


# 2026-10-04: B451-B500 original-scope audit.
review('B451', 'SUPPORTED', 'exact_finite_witness',
       'round63-b451-b500-original-scope-audit.md',
       '同半径r²=221で整数中心16点・分母5中心4点の厳密証人。双方4点以上の存在条件を満たす。')
review('B452', 'PARTIAL', 'finite_exclusion_only',
       'round63-b451-b500-original-scope-audit.md',
       'M≤6000・分母≤12ではq≥3がq=1を一度も上回らないが、無界存在命題なので有限不発見を反証へ昇格しない。')
review('B459', 'INCONCLUSIVE', 'audited_no_direct_test',
       'round63-b451-b500-original-scope-audit.md',
       'q≥3由来制約で初めて現れる残余ゲーム型を直接抽出した記録がない。')
review('B460', 'INCONCLUSIVE', 'audited_no_direct_test',
       'round63-b451-b500-original-scope-audit.md',
       'q≥3とq≤2の禁止を同数解除して浅層P/N影響を比較する原文どおりの実験が未実施。')
review('B466', 'SUPPORTED', 'finite_witness_reaudited_against_full_center_maxima',
       'round63-b451-b500-original-scope-audit.md',
       'N=650既知円族が25盤20点・26盤24点。後続全中心完全走査でも真の最大M25=20,M26=24で、同円族の境界切断改善による連続二増分が有効。')
review('B469', 'INCONCLUSIVE', 'audited_no_direct_test',
       'round63-b451-b500-original-scope-audit.md',
       '最多点円と少し小さい円の三つ組による四辺被覆均衡を直接比較した記録がない。')
review('B474', 'PARTIAL', 'finite_statistical_evidence',
       'round63-b451-b500-original-scope-audit.md',
       'n=3..6で増分と新規円型数を比較したが、原始円型の定義が暫定で一般傾向は未確定。')
review('B481', 'REFUTED', 'finite_statistical_counterexample',
       'round63-b451-b500-original-scope-audit.md',
       'n=4層別解析でクリーク成分数偶奇を固定しても三角形-nimber正相関が弱まらず、強まる層がある。')
review('B482', 'REFUTED', 'finite_complete_direction_reversal',
       'round63-b451-b500-original-scope-audit.md',
       'n=5全状態の集中型/離散型比較で、離散型の方がnimber種類数が多いセルは0/14。原文方向と逆。')
review('B483', 'INCONCLUSIVE', 'proxy_only',
       'round63-b451-b500-original-scope-audit.md',
       '主変数である二点競合成分をつなぐ三点辺の絶対本数を直接数えた近似誤差解析が未実施。')
review('B484', 'REFUTED', 'finite_controlled_statistical_counterevidence',
       'round63-b451-b500-original-scope-audit.md',
       'b=0込み分散とb>0限定分散の相関はn=5の実分散セルでほぼ同値。前者だけに見かけ相関が出るという主張を反証。')
review('B485', 'REFUTED', 'finite_controlled_pairwise_counterevidence',
       'round63-b451-b500-original-scope-audit.md',
       'n=4,5で(k,|L|,b_hist)固定の全対比較はspreadと必勝手比率がほぼコイントス。高被覆点数側の説明力が強く原文方向と逆。')
review('B486', 'PARTIAL', 'finite_controlled_statistical_evidence',
       'round63-b451-b500-original-scope-audit.md',
       'μ≥3かつn,k,|L|固定ではランダム勝率がP/Nを分けるが、原文が要求するh固定まで入れた比較は未実施。')
review('B487', 'PARTIAL', 'mixed_controlled_statistical_evidence',
       'round63-b451-b500-original-scope-audit.md',
       'pooledではgain種類数がu_maxよりgと強く相関するが、u_max,u_min固定セルでは正負が混在し原文の単調傾向は未確定。')
review('B488', 'REFUTED', 'finite_complete_deduplication_test',
       'round63-b451-b500-original-scope-audit.md',
       'n=3..5で真の残余同型ハッシュを含む重複除去をしても相関符号反転は0件。効果減衰はあるが原文の符号反転はない。')
review('B489', 'PARTIAL', 'finite_exact_tstar_wft_evidence',
       'round63-b451-b500-original-scope-audit.md',
       'n=4,5全局面のT*/WFTで原文方向の相関は確認したが、P率より説明力が高いという比較は未実施。')
review('B490', 'PARTIAL', 'finite_feature_collision_evidence',
       'round63-b451-b500-original-scope-audit.md',
       '共有局所特徴ではg・強制長各軸に衝突が残るが、二軸を完全分離し第三軸だけ衝突するという原文の具体構造は未取得。')
review('B491 B492', 'PARTIAL', 'finite_asymptotic_evidence_only',
       'round63-b451-b500-original-scope-audit.md',
       'n≤8の厳密値・標本は3n/2主項とVar=O(n)に整合するが、いずれも漸近命題で有限計算からは確定しない。')
review('B493', 'PARTIAL', 'finite_exact_correlation',
       'round63-b451-b500-original-scope-audit.md',
       'n=4全極大で中間層平均log|L|と到達順位に強い相関があるが、他盤再現と初終盤指標との統制比較が不足。')
review('B494', 'REFUTED', 'finite_complete_statistical_counterevidence',
       'round63-b451-b500-original-scope-audit.md',
       'n=5全16860極大で安定化群と途中選択肢・到達確率の相関がほぼ0。途中選択肢自体は効くが高対称性による説明は崩れる。')
review('B495', 'PARTIAL', 'square_board_exhaustion_and_out_of_scope_witness',
       'round63-b451-b500-original-scope-audit.md',
       '標準正方形n=4,5では完全ヒストグラム一致なら到達確率も全て一致。3x5等の反例は節の標準正方形スコープ外なので原文決着へ使わない。')
review('B496', 'PARTIAL', 'finite_growth_evidence',
       'round63-b451-b500-original-scope-audit.md',
       '同サイズ同D4安定化群で到達比はn=4の3.55からn=5の9.97まで増えるが、任意Mの無界性は未証明。')
review('B497', 'REFUTED', 'finite_statistical_counterevidence',
       'round63-b451-b500-original-scope-audit.md',
       'n=5,6の初手固定標本で最大終局条件付きの初期外周占有増加が一貫せず、原文の統計方向に反する。')
review('B498', 'PARTIAL', 'finite_statistical_support',
       'round63-b451-b500-original-scope-audit.md',
       'n=5,6では最小終局条件付き三石補完数が高い方向を観測するが、n=6標本が少なく一般傾向は未確定。')
review('B499', 'SUPPORTED', 'exact_finite_witness',
       'round63-b451-b500-original-scope-audit.md',
       'n=5厳密DPで平均長差0.00523の二初手が最小終局確率0対正に分かれ、比∞で10倍条件を満たす。')
review('B500', 'PARTIAL', 'counterevidence_to_specific_weakening',
       'round63-b451-b500-original-scope-audit.md',
       'n=4,5では鋭い単一中間層ボトルネックは無いが、少数の特定部分集合による一般的な上下界までは反証していない。')

# 2026-10-04: B501-B600 original-scope audit.
review('B503', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '節の前提から「約1/11」はN局面の割合ではなく p_rand≈1/11 の意味。旧REFUTEDは誤読。n=4でN最小1/11は確認済みだが、その極小例を残余同型で「1救済+10同値誘惑」に縮約する原文の構造分類は未完。')
review('B504', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=4,5で一意必勝手を保つ誘惑手数は13→22まで増えるが、任意個へ増幅する無限構成は未提示。')
review('B505', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=4,5では必勝手比率≥1/2のN局面の p_rand 最小は1/2で証人なし。存在する無限族の不発見だけでは反証しない。')
review('B507', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'h別のP局面最大ランダム勝率は有限盤で厳密計算済みだが、包含閉性を使った一般の明示上限列は未証明。')
review('B508', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '同一 p_rand で最善手比率差2/3の有限証人はあるが、差を任意に大きくする族は未構成。')
review('B509', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=4 pooledでは予言方向の相関 r=+0.264、順位一致91.2%。原文が要求する n,k,∣L∣,必勝手数固定の比較は未実施。')
review('B510', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=4,5全走査で真の必勝手が子p_rand評価で厳密最下位になる例は0。存在命題なので有限不発見では反証しない。')
review('B511', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=3,4,5の全一点削除では勝者不変。ただし原文は全n≥3の正方形盤であり n≥6 は未証明。')
review('B512', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '7×7最大16集合の点被覆数は2、すなわち δ_K(7)=2<3。全称を反証。')
review('B513', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '同じ完全被覆計算で δ_K(7)=2。候補値3を反証。')
review('B514', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=4でδ_out=2、δ_K≥4から差≥2を確認するが、差を任意に大きくする盤列は未構成。')
review('B515', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4では反転削除12辺中8辺が二石P辺で原文の性質を満たさないが、原文は「あるn」の存在命題。n=4の反例だけでは存在を反証しない。')
review('B516', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4反転12ペアは端点種別とマンハッタン距離の二条件で3群に整理できる。固定盤の構造命題を全12辺で確認。')
review('B517', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4反転削除ペアグラフ12辺を全構成し二部グラフであることをBFS二彩色で確認。')
review('B518', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4に、どの二点削除も不変だが三点全部で反転する12組を全数確認。指定盤条件を満たす。')
review('B519', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4の最小反転削除は2点で、サイズ≥4という前件が生じない。サイズ≥4の最小反転集合を持つ盤が未発見で全称を判定できない。')
review('B520', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=3のδ_K達成8集合は全て勝者・Wを変えるため証人なし。存在命題なので有限不発見では反証しない。')
review('B526', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4では一直線上の禁止四点束は各1組だけで、全10直線の単独解除はいずれも勝者不変。固定4×4存在命題を反証。')
review('B527', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '禁止追加時の局所臨界証明サイズを一般に上から押さえる定理・証明書が未構成。')
review('B528', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4で完成族からの単独解除感度は全194組0なのに追加経路では12–16回反転する。重要度概念の乖離はあるが頻度順位の定量比較は未完。')
review('B529', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '最小勝敗保持禁止族の完全列挙がなく、全最小族の共通四点の有無を判定できない。')
review('B530', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '円束単位の幾何順は4×4で12反転、乱択順は16反転だが、最小性と幾何的特徴づけの一般証明は未完。')
review('B531', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '5×5円のみW={12}に主対角線二本の禁止を加えるとWが5点へ増加。完全Grundyで確認。')
review('B532', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '5×5円のみ+水平垂直では標準Wの辺中央4点が欠落し、斜め禁止を含めないと標準Wに一致しない。')
review('B533', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '5×5の直線禁止D4三軌道を各単独で全検査したがWは最大5点で標準9点を復元できない。')
review('B534', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '主対角線軌道と軸平行軌道はいずれも同じ内側対角4点を救い、辺中央は二軌道併用で初めて救われる。「別の直線族」の分離を反証。')
review('B535', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '5×5の単一直線16本を一つずつ戻して全検査。同じ一本で勝ち入りと負け入りが同時に起きる例は0。')
review('B536', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '内側対角4点は各2本のP応答が一軌道で全消滅するが、辺中央4点は各12本で一軌道では消えきらない。原文の8点一括説明は未成立。')
review('B537', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '5×5で直線D4三軌道の全2^3中間族を完全計算し、中央初手は全8段階で勝ち初手に残る。')
review('B538', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4に g_circle=0, g_line=0, g_standard≠0 の局面を96件確認。存在命題を満たす。')
review('B539', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4に g_circle≠0, g_line≠0, g_standard=0 の局面を320件確認。存在命題を満たす。')
review('B540', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '5×5復元8点では円のみと標準で浅層合法手集合・手数が完全一致する一方、子P/Nだけが反転。原文の機構を直接確認。')
review('B543', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '2×8に一行3石・他行2石で終局する8例がある。正しい閾値はm≥9。')
review('B545', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '2×5の全3対3安全配置6件で二行のペア和集合は完全分離。混在型の初出はm=6。')
review('B547', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '二行盤の極大性を反射 s−a の和集合被覆で正確に判定する条件を導出し、完全列挙と一致。')
review('B548', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '一般証明によりm≥9の二行盤では全極大配置が6石。有限走査もm=200まで整合。')
review('B549', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'B548の一般定理によりm≥9では5石極大は存在しない。「任意に長い」に反する。')
review('B551', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '三行盤m=9で空盤g=2だが式(m+1) mod 3は1。全称を反証。')
review('B552', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '三行盤でg(6)=1≠g(9)=2、g(7)=2≠g(10)=1。長さ3伸長で同値部品が加わる主張を反証。')
review('B553', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'm=9（3の倍数）の勝ち初手集合が端二列除外帯型にならず、全称を反証。')
review('B554', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'm=7では候補十字と一致するがm=10で不一致。t≥2全称を反証。')
review('B559', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '行間隔を{0,1,2}から{0,1,3}へ変えるとm=7で空盤g列が3周期候補から外れる。存在命題を満たす。')
review('B560', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'm=7では2+2型だけですでに15点の内部帯Wが現れ、併用すると1点へ縮む。「両型併用で初めて現れる」を反証。')
review('B561', 'REFUTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '5×5安全5石に f=[1,10,20,4,1] の反例があり、20? inequality では f3^2=16<20=f2*f4。全称を反証。')
review('B562', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'R(S)が二点辺のみの局面はn≤5の検査範囲でa_S対数凹に違反なし。ただし全局面・全盤の一般証明はない。')
review('B563', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n≤5の全一石固定f_pは対数凹で、既知最小破壊は5石固定。より大盤の一石証人の存在は未決着。')
review('B564', 'SCOPE_UNCLEAR', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '既知B561反例を生む最小誘導部分は∣L∣=10中9点で、局所的とは言い難い。一方3点残余は1軌道型にまとまる。「小さい」「少数」の定量が未指定。')
review('B565', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=4,5の(k,∣L∣)ビンではfピーク位置の終局長相関がgより強いが、原文のh固定・p_randとの対比まで満たしていない。')
review('B566', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=5に同一f_Sでランダム終局分布が異なる明示局面対があり、n=4にも独立証人。存在命題を満たす。')
review('B567', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '7×7の16最大集合の単体和を神経補題で計算し、非零簡約ホモロジーは次数3のみ（6個）。次数3以下という原文を満たす。')
review('B568', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '13石極大400例・12石極大200例で一つ追加して穴が消える例は0だが全1952/152776の完全走査ではない。存在命題を有限不発見で反証しない。')
review('B569', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '比較可能なBetti数の異なる/同条件複体母集団が足りず、必勝手比率との統計関係を判定できない。')
review('B570', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '同一Betti列・同一最大サイズで変形障壁だけ異なる格子部分盤対の証人が未構成。')
review('B571', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4 k=3の同一交換成分内にg=0→1→2→3→4と各交換で1ずつ増える明示経路がある。')
review('B572', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4の一石交換でnimber跳躍5までは達成したが、跳躍を無界にする盤列は未構成。')
review('B573', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=4,5の条件を満たすP局面149件では全て1/2点交換先Pがあるが、全盤全局面の全称証明はない。')
review('B574', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=4,5に隣接N局面で必勝手集合が互いに素、かつ共通合法点数が3.25n/4.2nの証人がある。')
review('B575', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '固定したL対称差層ではP/N反転交換のbヒストグラム変化が大きい傾向をn=4,5で観測するが層依存が残る。')
review('B576', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '4×4にL(S)=L(T)、両方N、必勝手が各一つで13対14と異なる隣接局面対を確認。')
review('B577', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '5×5 k=2のP交換グラフでサイクル空間次元17に対し長さ3/4閉路生成ランク12。短閉路で生成できないサイクルが存在。')
review('B578', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '同一必勝手を共有するN局面対で対称差12まで確認したが、盤サイズとともに無界に増やす族は未構成。')
review('B579', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'WFT単元と必勝手安定性の有限相関は示唆されるが、WFT分布が偏り、gとの統制比較を含む原文統計は未確定。')
review('B580', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '一石交換の円束差分が小さい反転例はあるが、その小部分ハイパーグラフだけでP/N反転を十分に証明するクラスは未確立。')
review('B581', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '残余制約が純粋なパスP_mとなる格子残局をm=3..6で多数確認したが、任意長mの一般構成は未証明。')
review('B582', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '純粋な奇サイクル残局C3,C5は実現したがC7以降を任意長に構成する証明はない。')
review('B583', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'm≤6のパス残局では固定石数はO(m)に整合し盤辺長も多項式範囲だが、任意mの構成・上界証明はない。')
review('B584', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '同じ抽象残局C3を4石と9石で実現する配置を確認し、埋め方による遮蔽コスト差の存在を満たす。')
review('B585', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '共有遮蔽で有限例のコスト削減は確認されたが、原文が要求する無限族は未構成。')
review('B586', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'Lを保った一石移動で残余2成分↔1成分を切替える証人はあるが、結合機構は二点辺であり原文の「高階制約が現消する」は未実現。')
review('B587', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '接続によりg=4へ増幅する例は得たが、nimber2部品二個を指定してnimber4にする原文どおりの構成は未達。')
review('B588', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '後続全数探索で同じ二部品を用いながら幾何配置によりxor則から外れ、合成gが少なくとも3種類になる明示証人をn=4,5で確認。')
review('B589', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '有限な部品接続でg=0..4までは実現したが、有限部品集合から無界nimberを生成する閉じた構成族は未証明。')
review('B590', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'g固定でT*変化、T*固定でg変化の両方向証人はあるが、原文のWFTを使った二方向構成は未完。')
review('B591', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '一石不足層の厳密d_max最大はn=4..8で2,3,4,8,6。C=8は有限範囲を覆うが絶対定数の全n存在は未証明。')
review('B592', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n=7にd_max=8≥(8/7)nの有限証人はあるが、c>0を保つ無限盤列は未構成。')
review('B593', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n≤8ではC=8がd_max≤C(K_n−∣S∣)を覆うが、n非依存定数の一般証明はない。')
review('B594', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '7×7極大13石1952件を全数集計し(d_A,d_B)は48型、軌道占有ベクトル143型より少ない。')
review('B595', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '7×7極大13石1952件にA偏り624、B偏り832、等距離496があり、原文の両種類の存在を全数確認。')
review('B596', 'SUPPORTED', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '7×7全13石2176件をG12/G11で完全BFS。等距離群は一方偏り群より最大への到達率が低く平均最短路も長い。')
review('B597', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '固定cの層/最大集合比はn≤7で多項式的規模に見えるが、全nの多項式上界は未証明。')
review('B598', 'INCONCLUSIVE', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', 'n≤7では比が任意固定多項式を超える兆候はないが、超多項式となる盤列の存在命題を有限不発見で反証しない。')
review('B599', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '7×7最遠13石のd_max下界は円・直線飽和閉包だけで構成的に証明できるが、証明には32 Carrierを要し「少数・わずか」の部分は未達。')
review('B600', 'PARTIAL', 'audited_original_scope',
       'round64-b501-b600-original-scope-audit.md', '5×5に条件を満たすN局面2380件があり、全必勝手が最短修正候補外かつ勝敗維持対局が最大配置へ到達しない。ただし盤サイズをまたぐ族の構成は未証明。')

# 2026-10-04: B001-B100 remaining original-scope audit.
review('B001', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=6..10ではW_nが空集合または全体だが、原文はn≥6の全称。n≥11を覆う証明がない。')
review('B002', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n≤10で部分勝ち初手盤は5×5のみ。原文はn≥11で第二例が存在するという存在命題で、証人未発見。')
review('B003', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=1..8,10では空盤nimberは0/1だが、n=9は勝敗しか分からずnimber値未確定。全nの証明もない。')
review('B004', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '既知の奇数先手勝ち盤n=1,3,5,9では中央が勝ち初手。原文は奇数n全体の全称で一般証明はない。')
review('B005', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=4..10では角が勝ち初手なら全初手勝ちだが、n≥11を含む全称は未証明。')
review('B007', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '5×5では勝ち初手がmod2型で正確に記述でき中心距離より説明的だが、複数の部分勝ち盤比較という原文前提が未充足。')
review('B008', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n≤10では先手勝ち・後手勝ちがともに出現するが、双方が無限にあるという漸近命題は有限データでは決まらない。')
review('B009', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '既知10項は小周期と矛盾するが、最終的非周期という無限列主張と格子円出現による機構は未証明。')
review('B010', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '6×6は全初手勝ちで、初手ごとのT*が異なる点対を完全計算から確認。存在命題の条件を満たす。')
review('B017', 'REFUTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '5×5全比較で危険補完集合の自然な重なり量はPペア側の方が大きく、原文方向と逆。')
review('B019', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '後手勝ち4×4でJ_4の支配数γ=2≪16を完全計算したが、後手勝ち盤一般の統計主張までは未検証。')
review('B020', 'SCOPE_UNCLEAR', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '5×5のPペア20本は3種の整数関係で尽くせるがD4辺軌道代表も3種。「より短い」の尺度が未定義。')
review('B023', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '原文は固定命題σ_8=3だが、8×8の必要なGrundy層が未計算で直接証拠がない。')
review('B024', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n≤6の全初手勝ち盤の二石nimberは奇数のみ。原文はn≥9で偶数nimber二石局面が存在するという存在命題で証人未取得。')
review('B025', 'REFUTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '4×4の飽和開始層k=2でnimber 1,4が欠落し、6×6 k=3でも4が欠落。全称を反証。')
review('B026', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '4×4・5×5にg(S)=K(S)−∣S∣かつK(S)<K_nの非終局局面を多数確認。存在命題を満たす。')
review('B027', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=4,5の(k,∣L∣)固定セルでは高nimber群の終局サイズ幅が広い傾向が優勢だが逆向きセルもあり一般統計則は未確定。')
review('B028', 'REFUTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '4×4・5×5に、最大移動度の合法手ではg−1へ行けない反例がある。全称の幾何条件を反証。')
review('B029', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'nimber側と残余成分数の一部統計はあるが、原文の残余成分型多様性と最上位ビットの結合データが未整備。')
review('B030', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '同じ石数・同じ到達終局サイズ集合でもnimberが異なる局面対を4×4・5×5で明示。')
review('B032', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '5×5・6×6および小矩形では最短勝ち初手集合と最長勝ち初手集合が交わる。存在命題の証人は未発見。')
review('B033', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '5×5の中央以外の8勝ち初手も最悪時7石勝ちを強制でき、最短勝ちを実現する。固定盤全称を満たす。')
review('B034', 'REFUTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '勝敗維持T*は空盤勝敗に応じ単一パリティになるため、K_n∉T*(∅)が『パリティ以外』で起こるという原文の合条件は不可能。')
review('B035', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=4,5で勝ち手数とT*幅の関係はセルごとに混在し、原文の統計方向を支持も反証もできない。')
review('B036', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '4×4・5×5に、ある負け手が全勝ち手より最大到達終局を小さくする局面を明示。')
review('B037', 'SCOPE_UNCLEAR', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '代理量では分岐圧縮傾向があるが、原文の『強制的区間の縮約』『分岐型』の操作的定義がない。')
review('B038', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '同一N親から異なる勝ち手でP子へ行き、子のT*が互いに素となる明示例を4×4・5×5で確認。')
review('B039', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=4,5全1石交換で近終局層より中盤のP/N反転率が高い方向は確認したが、最大層位置は盤で異なり『中盤』の定義も未固定。')
review('B041', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'Aut(Q_n)=D4をn=3..6で完全列挙しn=5,6を確認したが、原文は全n≥5で一般証明はない。')
review('B042', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'D4安定化群が自明でも残余自己同型が非自明な有限証人は多数あるが、Rが空の退化例が中心で『頻出』・一般性は未確定。')
review('B043', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '180度回転で対称局面の合法手が合法応手へ写る補題はn=7にも成立するが、7×7後手必勝戦略全体と『少数』の動的切替えは未構成。')
review('B044', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '4×4・5×5に、非自明D4対称局面の全必勝手がその対称性を壊す明示局面がある。')
review('B045', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '5×5全極大ではstab≥2が最小側100%、典型0.2%、最大側4%と両端偏りを示すが、4×4では再現せず高対称=stab≥2の定義も弱い。')
review('B046', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '4×4・5×5で全幾何対合が失敗する一方、非幾何的自由対合による固定ペア応答が成立する残局面を計算で確認。')
review('B048', 'REFUTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '4×4・5×5で必勝手比率の説明力は合法手数だけとほぼ同じで、軌道数追加の改善がほぼゼロ。原文方向を反証。')
review('B049', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '同じ∣L∣・制約件数・残余自己同型群の『位数』でP/Nが分かれる対はあるが、原文の群同型そのものは未検証。')
review('B050', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '5×5負け初手16点は3 D4軌道すべてg=3だが、残余制約個数は3通り。共通商ゲームへの縮約写像が未構成。')
review('B051', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '同一盤・同石数でL(S)=L(T)なのに一方P・他方Nとなる局面対を4×4・5×5で明示。')
review('B052', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '5×5でLと二点残余制約P(S)が一致し、高階残余制約差だけでP/Nが分かれる局面対を確認。')
review('B053', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=4,5全局面で包含極小化後の3/4点制約が終盤ほど急減することを確認したが、一般統計則としては有限範囲。')
review('B054', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '残り最大手数4でも非自明分裂する5×5証人はあるが、n増加とともに『無視できない割合』になる部分は未確認で閾値も未定義。')
review('B055', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '格子隣接グラフが非連結なのに残余ゲームR(S)が連結な局面を4×4・5×5で多数確認。')
review('B056', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '格子隣接グラフは連結だがR(S)が非自明に分解する局面を4×4・5×5で明示。')
review('B058', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '高階制約消滅とP率の差は観測されたが、原文の『消滅直後から全安全拡張でP/Nが石数偶奇だけに固定』は未測定。')
review('B059', 'REFUTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '4×4全D4軌道を残余抽象型でまとめても中終盤の圧縮比は1.02〜1.07倍で、原文の『1桁以上減る盤』方向に強く反する。')
review('B060', 'SUPPORTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '異なる正方形盤4×4と5×5に、合法点6点以上で同型な残余ゲームを持つ局面対を構成済み。本文の明示条件を満たす。')
review('B061', 'REFUTED', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=4,5の主要層で三角形密度とnimberの相関は負でなく主に正。原文方向を反証。')
review('B066', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '二点近似の誤り局面では残余3点制約数が3〜4.5倍多いが、原文指定の『3点辺どうしの2点共有』は逆相関。測度の核心が未成立。')
review('B069', 'SCOPE_UNCLEAR', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'separatorの小ささは測れるが、『戦略を分割』『小さな勝敗証明』の証明系・サイズ定義がない。')
review('B076', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=2..5全極大で小サイズ側ほど空点平均被覆bが小さい方向を確認したが、一般統計則としては有限範囲。')
review('B083', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '既知K_n/nは2近傍だが、K_n/n→2という漸近極限は有限列では決まらない。')
review('B084', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n≤9では∣K_n−2n∣≤1だが、絶対定数で全nを抑える全称は未証明。')
review('B085', 'INCONCLUSIVE', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '既知範囲ではK_n−2n≤0で上振れなし。任意Mの上振れ盤列という存在命題は証人も反証もない。')
review('B086', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', '既知連続盤ではK_{n+1}−K_n≤3だが、全nの上界定理は未証明。')
review('B090', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=6,7,8で最大集合型数と交換障壁を比較したが単調関係が崩れ、サイズとの因果分離も未完。')
review('B099', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=3..6の最小極大標本では直線・円双方の被覆寄与を併用する方向を確認したが、n≥7と統計的一般性は未検証。')
review('B100', 'PARTIAL', 'audited_original_scope',
       'round65-b001-b100-original-scope-audit.md', 'n=3..7の完全極大サイズスペクトルは区間だが、標準正方形盤すべてという全称の一般証明はない。')

# 2026-10-04: B101-B150 remaining original-scope audit.
review('B101', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=6,7全最大配置は四辺すべてに触れるが、原文はn≥4全体の全称。一般証明はない。')
review('B102', 'REFUTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '6×6最大464集合のうち84集合が空行を1本持つ。行・列射影全域というn≥4全称を反証。')
review('B103', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=4..7全最大集合で行占有2への集中傾向を完全集計したが、n増加一般の統計則としては有限範囲。')
review('B104', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '7×7には全最大集合から排除されるD4点軌道がある一方n≤6にはない。現象の有限例はあるが『無限回』は未証明。')
review('B105', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=6では全点が最大集合に出現し、n=7の最大損失もK−1。K−2以下となる点の存在は未発見だが存在命題なので反証できない。')
review('B106', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=4..7で最大配置の最小特定点数は2〜6程度でlog∣M∣と同程度だが、O(log n)の全称上界は未証明。')
review('B107', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '最大集合数と最小特定点数はn=4..7で非単調に動き、単純情報量以上の改善という統計主張は確定しない。')
review('B108', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=6,7では全最大集合の共通部分は空だが、原文は全n≥4の全称で一般証明はない。')
review('B109', 'SUPPORTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '6×6で同一D4軌道占有ベクトル内に1-swap次数0〜6が共存し、最大配置への最小低下幅が異なる例がある。')
review('B110', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '容量不等式による上界証明の枠組みとn=7の被覆データはあるが、n≤10各盤のK_nを少数の円・直線だけで証明する原文の構成は未完成。')
review('B111', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '7×7のG_11で最大由来8成分が全接続するかは現行knowledgeでもopen。原文の固定有限命題は未決着。')
review('B112', 'REFUTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '最大配置を含まない孤立12石G_12成分が存在し、最高13・13石局面ありという全称を反証。')
review('B113', 'SUPPORTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '7×7の該当903成分を完全BFSしA–B最短距離14を確定。13操作以下の経路はない。')
review('B114', 'SUPPORTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'A–B最短8経路を全列挙し、A∪B外で使う点は全て同じ角48だけ。他点を使う最短抜け道はない。')
review('B115', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '既存250局面は粗い3変数で39型に分かれ、2〜3局所カウントでの閉包記述は未構成。')
review('B116', 'REFUTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'U内の占有差2,3かつ13石以上を排除するには20個以下の禁止四点組では足りないことを既存証明書で確認。')
review('B117', 'REFUTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '903成分のA,Bは2近傍次数ヒストグラムが異なり、グラフ自己同型でA↔Bを交換できない。')
review('B118', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '14手最短路8本の共通角は分かるが、原文の定数サイズ石移動パターンへの縮約と説明は未構成。')
review('B119', 'REFUTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '最大配置由来8成分外に孤立12石G_12成分を明示。『最大配置を含まない成分はない』を反証。')
review('B120', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'A/B相4+4の大分類は既存不変量で捉えるが、8成分を保存する3bit相当の角・辺ラベルは未構成。')
review('B121', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=6ではK−2層で最大配置が連結だが、n=7のK−3=11石層の全接続がopen。全nの全称は未証明。')
review('B122', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '必要低下幅はn=6で2、n=7で少なくとも3だが、任意cに対する非連結最大配置という無界存在命題は未証明。')
review('B123', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=4全最大配置対ではA∪B外の補助点は不要。より大盤で補助点2個以上を必須とする存在証人は未取得。')
review('B124', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=4では補助点自体が不要。より大盤で補助点必須かつ共通必須点なしとなる存在証人は未取得。')
review('B125', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=4ではA∩Bを保持した経路が全対象対に存在。より大盤で共通点一時除去が幅改善に必須となる存在証人は未取得。')
review('B126', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '同じ∣A\\B∣・∣A∩B∣でも必要幅9/10が分かれることは確認したが、原文指定の残余禁止四点交差密度では幅を説明できていない。')
review('B127', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '既知障壁は無重み占有差で説明でき、±1以外の小整数重みが初めて必要になる具体例・証明書は未発見。')
review('B128', 'SCOPE_UNCLEAR', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '安全族の下方閉性により2点交換は逐次除去・追加へ直列化できる。『浅く』『より小さい』の比較基準次第で自明にも偽にもなり、原文の障壁量が未定義。')
review('B129', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=4,5全極大で正規化1-swap可動性を測定し最大側が小さい方向を観測したが、定義差の不一致もあり一般統計則は未確定。')
review('B130', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n≤5の検査層では成分内P/N一定となる例がないが、原文はあるn,kの存在命題。有限不発見では反証しない。')
review('B131', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '後続の全中心探索で少なくともn≤112の最大円は半整数中心から選べるが、任意nの全称証明はない。')
review('B132', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '全中心探索n≤112でも最多点円が半整数中心でない反例は見つかっていない。存在命題は未決着。')
review('B133', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '中心分母q別には初出・最大点数へ強い制限を確認したが、原始方程式係数aごとの鋭い初出サイズ・可能点数分類という原文完全形は未完成。')
review('B134', 'REFUTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '同一直径上限でq=3の最大4点に対しq=4で6点の円があり、分母qに対する最大点数の非増加性を反証。')
review('B135', 'SUPPORTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '同半径r²=2で整数中心は4格子点、半整数中心は0格子点となる無限格子上の明示例がある。')
review('B136', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '有限盤円点数の欠落を完全円の窓切断スペクトルとして解析する方法と多数の有限分類はあるが、必要十分な一般分類は未完成。')
review('B137', 'REFUTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'n=25→26で最大円点数20→24が同じN=650円族の収容改善だけで起こる。新算術型初出が常に必要という全称を反証。')
review('B138', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '有限盤で上位点数円が少数の有理中心型へ集中する傾向は完全集計で確認したが、n一般の統計則は未確定。')
review('B139', 'SUPPORTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '8×8で最多12点円族の禁止四点寄与495より、10点円族840・8点円族5670が大きい。存在命題の証人。')
review('B140', 'INCONCLUSIVE', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '反転は共円・共線を保つが整数格子点性を保つ条件が厳しく、安全・極大配置を別盤へ写す具体構成は未取得。')
review('B143', 'SUPPORTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '現行knowledge K0056が公刊一般定理に基づきC_n=Θ(n^5)を採用しており、liminf C_n/n^5>0は直ちに従う。')
review('B144', 'REFUTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'K0054でD_n~c_D n^5、K0056でC_n=Θ(n^5)。C_nにも正のn^5下界があるためD_n/(C_n+D_n)は1へ収束できない。')
review('B146', 'REFUTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '格子長方形は原始方向(p,q)、二辺倍率a,b、基点で数えるとO(n^4 log n)。一方C_n=Ω(n^5)なのでR_n/C_n=O(log n/n)→0。正のliminfを反証。')
review('B147', 'SUPPORTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', 'B146と同じ数え上げでR_n=O(n^4 log n)、K0056よりC_n=Ω(n^5)。したがってR_n/C_n→0を一般に証明できる。')
review('B148', 'PARTIAL', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '固定した一つの円テンプレートの平行移動数は(n−w)(n−h)という二次式だが、全C_n増分を既存族成長＋新族初出の扱いやすい閉式へまとめる部分は未完成。')
review('B149', 'SUPPORTED', 'audited_original_scope',
       'round66-b101-b150-original-scope-audit.md', '上位10相似型の被覆率はn=4で84.5%、n=5で70.2%、n=6で51.8%。n≤3は総数上10型で半数超を自明に覆えるため、固定m=6が原文存在条件を満たす。')

# 2026-10-04: B151-B200 original-scope audit.
review('B151', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4..10の既知完全計算では最小点次数が角の値に一致するが、n≥4全体の全称証明はない。')
review('B152', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '5×5で中心d=116に対し最大d=156は中心からずれた4点で達成。奇数盤で中心最大が破れる存在証人。')
review('B153', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '平均次数は共線・共円総数からΘ(n^3)だが、p/n→(u,v)ごとの連続形状関数への収束は未証明。同じ巨視的位置内の有限n揺らぎも大きい。')
review('B154', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '同一境界距離・近接巨視的位置で次数揺らぎはn=4..6で拡大するが、正規化後に異なる極限を持つ二系列の厳密構成は未取得。')
review('B155', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '距離固定後にgcd・既約傾きで群内spreadは16.1→12.6へ減り説明力はあるが、同一offsetでも位置効果12.6が残る。『距離より敏感』という強い比較は成立していない。')
review('B156', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '一般にd(p,q)はp,qを含む各直線・円CについてC(∣C∣−2,2)を足したもの。円中心は垂直二等分線上に限られ、四点組全列挙なしのcarrier走査で計算できる。n=5全300対で一致。')
review('B157', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4,5の全安全2石局面でΣd固定の混在群を比較し、二点次数行列のλ_maxが複数群でP/Nを追加分離。Σd単独より説明力を持つという原文の統計主張を直接確認。')
review('B158', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4,5にd(p)>d(q)なのに∣L(S+p)∣>∣L(S+q)∣となる非空親Sの証人があり、最大次数点対最小次数点でも逆転する。')
review('B159', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '外周追加による次数増分はn=5→6,6→7で盤中心まで境界と同程度以上に及ぶが、n→∞でも中心比が正に保たれる漸近部分は未証明。')
review('B160', 'INCONCLUSIVE', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n≤6では同次数点がD4同値にまとまり、原文条件を満たす候補自体がない。より大盤で同次数D4非同値かつ一石g/勝敗差が出る存在証人は未取得。')
review('B161', 'REFUTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=6,7の非共線共円四点で(x mod2,y mod2)の35多重集合型と市松偶奇5型がすべて実現。座標偶奇だけで排除できる組合せはない。')
review('B162', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=5全共円四点で小さい法の剰余パターンと中心分母に100%純粋な分類セルが存在し、後続の固定分母整数論とも整合。『一部判別できる』という存在的な構造主張を満たす。')
review('B163', 'INCONCLUSIVE', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '5×5 mod2各類では強制使用による容量損失はないが、原文はある領域・合同類の存在命題。mod3/5や大盤での証人可能性は残る。')
review('B164', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '5×5全100最大配置で盤内クラス点数補正後もmod2占有率が0.42/0.38/0.38/0.16と強く非一様。『法2,3,5の少なくとも一つ』を満たす。')
review('B165', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '一般構成あり。素数p≥13、r=floor((p−1)/4)、S={(t,t² mod p):0≤t≤r}⊂[0,p−1]²とする。4点t_iのdet[x²+y²,x,y,1] mod pは列操作でdet[t_i^4,t_i,t_i²,1]=±∏_{i<j}(t_j−t_i)·Σt_i。t_iは相異なり、4点和は6以上p未満なので非零。従って全四点det≠0 mod pで安全、∣S∣=r+1=Θ(p)、盤辺長p。')
review('B166', 'SCOPE_UNCLEAR', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '本文の『指定した範囲』が未指定。p≤11という有限小素数範囲なら5×5最大配置が証人になる一方、全素数という読みは任意の有限安全Sでp>max∣det∣を取れば必ず一素数で証明できるため偽。')
review('B167', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '任意の有限安全Sでは全四点detは非零整数なので、p>max∣det∣の素数を一つ選べば全detが同時に非零mod p。よって必要素数集合の要素数は常に1で、nに比べて非常に小さい。')
review('B168', 'INCONCLUSIVE', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n≤6全安全局面で占有点XORや10特徴量XORによるmod2線形不変量は不存在だが、原文は『適切な応答で維持される有限状態のパリティ量』まで許す。より一般の有限状態不変量は未排除。')
review('B169', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=5でm=2,3,4には同一座標剰余パターン・同石数でP/Nが逆の証人があるが、『任意の固定m』を十分大盤へ延ばす一般構成は未証明。')
review('B170', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=3..7最大集合数56,64,100,464,16にn=7の谷があり円型増加と同居するが、円族初出が谷を作る因果・漸近傾向は未証明。')
review('B171', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=2..5の完全f_n(k)はすべて単峰だが、全nで一度だけ増加から減少へ切り替わる全称証明はない。')
review('B172', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=2..5の完全fベクトルはすべて対数凹だが、全nの不等式は未証明。')
review('B173', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=2..5の安全確率a_kはすべて対数凹だが、全nの不等式は未証明。')
review('B174', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'Δ_4でQとF_2,F_3,F_5,F_7のBettiが一致し小素数捩れは見えないが、整数Smith標準形による全捩れ排除も全n証明もない。')
review('B175', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'Δ_4の自由部分Bettiは211個のS^4と22個のS^5の一端和と一致するが、ホモロジー一致だけではホモトピー同値を与えず、離散Morse等の証明は未実施。')
review('B176', 'REFUTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4,5でBetti数増大の立ち上がり層とP率が0/1から離れる層を同時計測すると一致せず、原文の対応関係を直接反証。')
review('B177', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4の13点部分盤に、安全集合数fベクトルが完全一致するのに空盤nimber/P/Nが異なる明示ペアを発見。存在命題を満たす。')
review('B178', 'INCONCLUSIVE', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '禁止四点組どうしの共有パターン分布は完全計数済みだが、それからΔ_nの最初の非零ホモロジー生成関係を記述する写像・証明は未構成。')
review('B179', 'SCOPE_UNCLEAR', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'I_n(−1)の値は計算済みだが、『剛性』『関係する』の操作的定義がない。最大集合数やKとの単純相関も弱く、真偽を一意に判定できない。')
review('B180', 'SCOPE_UNCLEAR', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '放物面持ち上げと共円det=0の同値は正しいが、『選択定理を短くする』『少数の平面配置』の短さ・少数の尺度が未定義で、7×7証明への具体的縮約も未構成。')
review('B181', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '小盤ではE[X_n]/K_nが減少するが、比が0へ収束する漸近証明はない。')
review('B182', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=3..5厳密DPでは中央値をn^(2/3)(log n)^(1/3)で割った比はほぼ一定だが、無界漸近の定数倍評価は未証明。')
review('B183', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4..8でVar(X)/E[X]^2は0.0078→0.0045と減少するが、0への極限は未証明。')
review('B184', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=3..5の標準化分布は歪度・尖度が0へ近づく兆候を示すが、中心極限定理に必要な一般的混合・依存制御は未証明。')
review('B185', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '同じ終局サイズの極大集合でもランダム貪欲到達確率に10倍超の差があることを厳密計算・独立標本で確認。サイズだけでは説明できない。')
review('B186', 'REFUTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '4×4極大集合を同サイズで比較すると、D4安定化群が大きい高対称集合ほどラベル付き1集合当たり到達確率が低い方向で、原文と逆。')
review('B187', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '初手固定ランダム貪欲でn=5,6とも角初手の平均終局長が内部/中央近傍より大きい。独立二盤で原文方向を再現。')
review('B188', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=3,4とn=5代表点で初手別平均長差の相対幅は小さいが、最大相対差→0の漸近主張は未証明。')
review('B189', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=5,6では終局最後手が初期低次数側へ過剰出現する方向を観測するが、n=4は弱く、角・辺に限定した定義と大標本再現が未完。')
review('B190', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4..6で残余need3等が次手の合法手純減を∣L∣単独より予告するが、原文の『次の数手』の連鎖的急減は未測定。')
review('B191', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4全5811・n=5全151394局面で(k,∣L∣)別P率に明確な山谷があり、十分大きい母数の層でも非単調性を再現。')
review('B192', 'REFUTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4,5のN局面で(k,∣L∣)固定後、b_S(p)分散と必勝手比率の相関は負ではなく正寄り。『ばらつき大ほど勝ち手集中』の方向を反証。')
review('B193', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=5大標本でΣdとP率をneed2比率で層別しても符号は一貫せず、原文の整理則を支持しない。ただし指定した二次元固定法を完全母集団で尽くしてはいない。')
review('B194', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=4,5の同じ(n,k,∣L∣)セル内でランダム残手偶奇確率がP/Nを追加分離し、分布は重なるため『予測するが決定しない』まで確認。')
review('B195', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'N局面のランダム勝率最小はn=4で1/31、n=5で1/37まで低下するが、任意εへ近づける無限族は未構成。')
review('B196', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'P局面のランダム勝率最大はn=5で21/26まで上がるが、1へ近づける無限族は未構成。')
review('B197', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', '子局面残余特徴の分散は一部標本でP>Nだが、(k,∣L∣)固定のより大きい標本ではP>NとN>Pがほぼ拮抗。原文の一般統計方向は確定しない。')
review('B198', 'PARTIAL', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=5で局所特徴の交互作用が単独特徴を改善する例はあるが、原文指定の点次数×unique gainまたは順位不一致が支配することは未確認。')
review('B199', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=3,4,5全安全集合のP率曲線を比較すると、生kよりk/K_nで揃えた方が盤間レンジが小さいことを定量確認。原文の『k/K_nまたは∣L∣/n²』を満たす。')
review('B200', 'SUPPORTED', 'audited_original_scope',
       'round67-b151-b200-original-scope-audit.md', 'n=5の3万局面標本でP/N相関とN内nimber相関の特徴順位が明確に不一致（順位Spearmanも負）。『零かどうか』と高nimberが別軸という統計主張を直接確認。')


review('B201', 'INCONCLUSIVE', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "標準盤は原文冒頭でn×nと定義され、K_nも正方形容量。n≤6の一点削除では証人なし。2×6のK=6保存・勝者反転は長方形への弱化であり原文の正方形存在証人にはしない。",
       ('round5-batch-b201-b230-followup.md',))
review('B202', 'INCONCLUSIVE', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n≤6の正方形では一点削除後もKが保存され、容量低下の前提を満たす証人がない。有限不発見は一般存在命題の反証ではない。",
       ('round5-batch-b201-b230.md',))
review('B203', 'INCONCLUSIVE', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "原文の対象は9×9の全81一点削除盤。確認済みn=5,6の頑健性は別盤の結果で、9×9の削除盤勝敗は未計算。K0021の全初手勝ちとも別の操作。",
       ('round5-batch-b201-b230.md',))
review('B204', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "4×4からp=0,q=3を単独削除するとg=0、同時削除するとg=2。batch09_pairs_n4.jsonの全120対と一点削除値を照合し原文の存在を満たす。",
       ('round5-batch-b201-b230.md',))
review('B205', 'INCONCLUSIVE', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n=5全100最大配置の各点被覆は正で、排除点がない。長方形での同様の不発見も一般反証ではなく、排除点かつ勝者反転の証人は未取得。",
       ('round5-batch-b201-b230-followup.md',))
review('B206', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n=4の勝ち手頻度・gateと次数の相関、矩形で同次数の削除効果差はある。しかし原文の同次数条件下で媒介性とg変化を比較する回帰は未実施。次数で決まらないことだけでは媒介性優位を証明しない。",
       ('round5-batch-b201-b230-followup.md',))
review('B207', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "4×4のp=0,q=3でK_full=K_p=K_q=K_pair=7、容量損失0は加法的。一方g_full=g_p=g_q=0、g_pair=2。原文は非零容量損失を要求せず、正方形の証人で決着。",
       ('round5-batch-b201-b230.md',))
review('B208', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n=3の外周付加は変化4/不変12、n=4は変化12/不変8。任意の十分大きいnで両型があるという量化を満たす一般構成はない。",
       ('round5-batch-b201-b230.md',))
review('B209', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n=4では対称孔の反転率が高いが非対称反転も8組。原文は同サイズ・同削除次数和で対称孔のみ反転する盤の存在であり、次数和を統制した証人は未取得。他群の非対称反転は存在命題全体を反証しない。",
       ('round5-batch-b201-b230-followup.md',))
review('B210', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "矩形の端距離・角で盤全体の削除結果を分類した有限例はあるが、終盤R(S)の点削除に適用する一般局所規則は未構成。90%の分類精度はゲーム値の完全保存条件ではない。",
       ('round5-batch-last21.md',))
review('B214', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "二行の(a,0),(b,0),(c,1),(d,1)の共円はa+b=c+dと同値。各行高々3石、対和集合の交差を禁止する状態で全継続を表せる。3+1の円はなく同一行4石だけが共線禁止。K0069の全長強解決とも整合。",
       ('round4-two-row-order-strategy.md',))
review('B217', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "2×6と3×4は面積12・最大安全6で、空盤gは0対2。長方形を明示した原文の存在条件を満たす。最小性の完全証明は別であり採用しない。",
       ('round5-batch-b201-b230-followup.md',))
review('B218', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "面積16の2×8対4×4で空盤反転の差を確認。しかし原文は安全局面母集団のP/N変化率の縦横比依存で、空盤の0/1比較はその統計を測っていない。",
       ('round5-batch-b201-b230-followup.md',))
review('B221', 'INCONCLUSIVE', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "対象はn≤9の正方形。n=4,5では標準と円のみの空盤勝者は一致。2×6等の反転は長方形への弱化で、正方形n=6..9に原文証人なし。",
       ('round5-batch-b201-b230.md',))
review('B222', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "原文本文はW非空を条件にしない。4×4の標準と直線のみは共に空盤g=0、W=空集合で一致し、禁止制約のあるn≥4盤という条件を満たす。追撃が追加した非空Wの存在は別の未解決問い。円のみ計算との取り違えには依拠しない。",
       ('round5-batch-b201-b230.md',))
review('B223', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "原文本文の増加する範囲は、共通の標準安全集合を母集団としたn4のk3→4で56/560=10%から348/1626≈21.4%へ上昇。batch10_extra.jsonを優先し、円のみ集合を分母とした追撃表の21.3%は採らない。全終盤での単調増加までは主張しない。",
       ('round5-batch-b201-b230-followup.md',))
review('B225', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "q5・n4でmax g=5に4石で達する有限結果はあるが、h(S)=K(S)−|S|の天井到達を示す資料ではない。q≥5の盤族と少占有での天井達成の一般化は未証明。",
       ('round5-batch-b201-b230-followup.md',))
review('B226', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "現在のK0310では8×8のmisère空盤は先手勝ちで、通常版K0006も先手勝ち。一致例n8と不一致例n4（通常後手/misère先手）により、指定n≥4正方形内の両存在を満たす。",
       ('round5-batch-b201-b230-followup.md',))
review('B229', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n4で閾値2に最大配置数64→8が容量低下より先に起きるが、D4軌道サイズは全て8のまま。対称性分布の先行変化を証明したわけではなく、高対称配置はこの盤にない。",
       ('round5-batch-b201-b230-followup.md',))
review('B230', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n4で点数≤4のcarrierに由来する禁止を省略しても石数0,1層のP/Nを完全保存する有限例がある。原文は特定層と非自明条件の存在であり、全層保存も全n定理も要求しない。",
       ('round4-batch-b228-b290.md',))
review('B231', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "K0293の全n1..7スペクトルでg=0..9を実現。任意mの一般実現は未証明。mexによる小さい値の実現は最大nimberの無界性の代わりにはならない。",
       ('round5-batch-b231-b250-push3.md',))
review('B232', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "小グラフの二点影P(S)の出現は計算済みだが、scriptsのresidual_graphは三点・四点極小辺を落とす。K0108のR(S)全体が指定グラフのみになることと全有限グラフの実現は未証明。",
       ('round5-batch-b231-b250-push3.md',))
review('B233', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "有限の木の次数列をP(S)成分で検出したが、成分の出現は全Rの木実現ではなく高階辺排除も未検査。次数列は一般に完全同型不変量でない。全ての木の量化は未証明。",
       ('round5-batch-b231-b250-followup.md',))
review('B234', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n5二石のP(S)にK2九成分という有限観測はあるが、三点・四点辺が成分を結ぶ可能性を落とした旧計算。非自明Hの正確なR直和を任意r構成する一般族は未取得。",
       ('round5-batch-b231-b250-push3.md',))
review('B235', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n5で二点影の成分が平行移動対応する20例はあるが、完全Rの遮蔽付き合成を保証する座標十分条件ではない。高階横断辺の排除と一般写像は未証明。",
       ('round5-batch-b231-b250-push3.md',))
review('B236', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n4,5の全Grundyに基づく後退解析で連続一意勝ちr=2の証人を確認。任意rの族は未構成。有限でr3不発見は全盤での不可能性ではない。",
       ('round5-batch-b231-b250-push3.md',))
review('B237', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n5で一手後の二点影の成分数が3増える観測はあるが、高階辺を含むRの独立分裂は保証しない。任意rの独立領域を作るという主張の一般構成もない。",
       ('round5-batch-b231-b250-push3.md',))
review('B238', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n4のS空、q1=0,q2=1,p=2で子gは1,1、p後は5,0。nimber同値から分岐する有限核は確認。ただし同nimberは継続ゲーム同型ではなく、原文の同じ継続型を満たす証人まではない。",
       ('round5-batch-b231-b250.md',))
review('B239', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "N2・N3で局所正方形内の中間点を全禁止して四隅を合法に保つ固定石証人はある。より大きい全盤にFを置くため、その盤の残り合法点も含めた元ゲームの正確な実現・一般クラスの証明はない。",
       ('round5-batch-b231-b250-push3.md',))
review('B240', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "4×4で占有集合S1={0},S2={1}はg=1で直和同値。共通の占有T={2}を加えるとg=5対0。round5_b231_n4.jsonのembedding_splitに具体値があり、同nimberと幾何置換の違いを示す。",
       ('round5-batch-b231-b250.md',))
review('B241', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "5×5の九勝ち初手と三D4軌道は確定。追撃のmin_child_L等は完全Grundyで勝ち手を選別した後の規則で、共通の短い応答証明の抽出を与えない。全勝利の有限事実と幾何的短証明を区別。",
       ('round5-batch-b231-b250-followup.md',))
review('B242', 'SCOPE_UNCLEAR', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "戦略モードの表現言語・サイズが未定義。完全Grundyの勝ち手oracleを一モードと数える追撃なら自明になるが、原文の局面幾何による切替10種類との同一性を判断できない。36初手勝ち自体はK0004で確定。",
       ('round5-batch-b231-b250-followup.md',))
review('B243', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "K0268/K0269の軌道骨格・容量制約で最大配置の排他相を確認。旧追撃は中心説を修正したが、同じ補題が勝敗証明で大量局面を処理することは未提示。",
       ('round5-batch-b231-b250-push3.md',))
review('B244', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "K0295で5×5勝者は終局7石を全応手に対し保証でき、K5=9より小さい。7と9は同じ勝者側の偶奇なので9を避ける保証は偶奇だけから出ない。n4の6<K4=7だけの旧証拠より強い現在の固定長保証を使う。",
       ('round25-forced-length-holes.md',))
review('B245', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n4では勝ち手数を固定すると反復群の生proofは大きく、n5追撃の圧縮差平均38.4対1.5は勝ち手数を固定していない。WLと二点影による共有は完全R同型の証明でもない。原文指定の統制下の共有量増加は未確定。",
       ('round5-batch-b231-b250-followup.md',))
review('B246', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "完全な残余禁止hypergraphの同型を十分条件とすれば全手・全子・証明を写せる（K0108）。K0227の非D4同値配置の正確なR同型が、D4より粗い分類が実際にある証拠。二点影だけの旧Node-Kayles論証は採用しない。",
       ('round42-exact-residual-family-audit.md',))
review('B247', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n5で64件の非交差最小化手を検出する旧proof_mはP節点で1+Σ子proof、N節点で1+min子proofという木サイズ。共有可能なDAG最小化とは異なるため、原文の最小DAGとの食い違いまでは未証明。",
       ('round5-batch-b231-b250.md',))
review('B248', 'SUPPORTED', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "n3全安全局面はK0004のg∈{0,1}、全極大5石。石数偶奇という一整数で勝敗を分け、Nから任意合法手がPへ行く共通応答形式を与える。原文は小盤の存在であり、n4,5の不完全な特徴分類を一般証明にしない。",
       ('round5-batch-b231-b250-push3.md',))
review('B249', 'PARTIAL', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "g1の有限木proofサイズ急増はn4,5で測定したが、無界盤族の指数下界はない。Pで子サイズを加算する旧DPはDAG共有を最小化せず、深さ別有限比を漸近定理へ昇格しない。",
       ('round5-batch-b231-b250-push3.md',))
review('B250', 'SCOPE_UNCLEAR', 'original_scope_and_current_evidence_audit',
       'round68-b201-b250-original-scope-audit.md', "定数の一様性、円束パラメータの表現・許すクラスが未指定。旧反証は一石効果の加算という追加条件を否定するだけで、原文のあるクラスの存在を否定しない。",
       ('round5-batch-b231-b250.md',))

def main():
    originals = {}
    hashes = {}
    for bank in BANKS:
        lines = bank.read_text(encoding='utf-8-sig').splitlines()
        hashes[bank.name] = hashlib.sha256(bank.read_bytes()).hexdigest()
        section_title, section_start = '', 0
        for line_no, line in enumerate(lines, 1):
            if line.startswith('## '):
                section_title, section_start = line[3:], line_no
            match = ORIGINAL.match(line)
            if match:
                bid, kind, title, claim = match.groups()
                assert bid not in originals
                originals[bid] = {'id': bid, 'bank': '../../' + bank.relative_to(RESEARCH).as_posix(),
                                  'original_line': line_no, 'original_exact_line': line,
                                  'tag': kind, 'title': title, 'claim': claim,
                                  'section_title': section_title, 'section_line': section_start,
                                  'section_setup': '\n'.join(lines[section_start:line_no-1]).split('- **B')[0].strip(),
                                  'evidence_pointers': []}
    assert set(originals) == {f'B{i:03}' for i in range(1, 601)}
    # The historical batch reports moved to log; retain their evidence pointers.
    sources = sorted(REPORTS.glob('*.md')) + sorted((RESEARCH/'log/claim-audit').glob('*.md'))
    for path in sources:
        if path.name.startswith('round26') or path.name in {'CONTINUATION-kyouen-hypotheses.md'}:
            continue
        lines = path.read_text(encoding='utf-8-sig').splitlines()
        for i, line in enumerate(lines):
            if not re.match(r'^#{1,6}\s+B\d{3}', line):
                continue
            heading_ids = ID.findall(line)
            if re.search(r'B\d{3}\s*[-–〜]\s*B\d{3}', line):
                continue  # batch/range headers do not assign one verdict to every member
            end = next((j for j in range(i+1,len(lines)) if lines[j].startswith('#')),len(lines))
            labels = [{'line': j+1, 'labels': LABEL.findall(lines[j]), 'exact_text': lines[j]}
                      for j in range(i+1,end) if LABEL.search(lines[j]) and
                      any(word in lines[j] for word in ('判定','原命題','弱化版','SUPPORTED','REFUTED'))]
            report_name = path.name if path.parent == REPORTS else '../../../log/claim-audit/' + path.name
            pointer = {'report': report_name, 'heading_line': i+1, 'heading': line,
                       'joint_heading_ids': heading_ids, 'labels_in_section': labels,
                       'weakening_mentioned': any('弱化' in z for z in lines[i:end])}
            for bid in heading_ids:
                if bid in originals:
                    originals[bid]['evidence_pointers'].append(pointer)
    for bid, row in originals.items():
        row.update(REVIEWED.get(bid, {'original_status': 'NOT_AUDITED', 'evidence_kind': 'unreviewed',
                                     'preferred_report': None, 'reason': '旧ラベルの再集計だけでは原文決着を採用しない。',
                                     'additional_reports': []}))
        if row['preferred_report']:
            for report in [row['preferred_report']]+row['additional_reports']:
                assert (REPORTS/report).is_file(), report
    rows = [originals[f'B{i:03}'] for i in range(1,601)]
    counts = dict(Counter(row['original_status'] for row in rows))
    reviewed_count = 600-counts.get('NOT_AUDITED',0)
    payload = {'total_originals': 600, 'reviewed_originals': reviewed_count,
               'counts_are_audit_states_not_total_unresolved': True, 'audit_state_counts': counts,
               'original_source_sha256': hashes,
               'index_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'rows': rows}
    report_names = {p['report'] for row in rows for p in row['evidence_pointers']}
    report_names |= {row['preferred_report'] for row in rows if row['preferred_report']}
    report_names |= {p for row in rows for p in row['additional_reports']}
    payload['evidence_report_sha256'] = {name: hashlib.sha256((REPORTS/name).read_bytes()).hexdigest()
                                        for name in sorted(report_names)}
    atomic_text(OUTPUT/'round26_original_scope_index.json',json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    lines = ['# 全600原命題の証拠索引（原文監査は途中）','',
             '更新: 2026-10-04。原文600件を重複・欠落なく抽出し、原文と証拠への参照を固定した。',
             '**未監査は未解決と同義ではない。この表から研究全体の未解決数はまだ確定できない。**','',
             f'原文照合して採用した記録は{reviewed_count}件。残りは旧ラベルを採用せずNOT_AUDITEDとする。',
             '旧個票の原命題・弱化版ラベルはJSONのevidence_pointersに行番号・原文ごと保存した。',
             '最も強いラベルを自動選択したり、弱化版を原命題へ昇格したりしていない。',
             'SUPPORTEDは原文の量化を満たす記録、REFUTEDはその反証記録。PARTIALは明示した部分結果。',
             'SCOPE_UNCLEARは原文の解釈・統計母集団が足りず、より強い読みの反証だけでは全体を決めないもの。','',
             '## 監査状態の内訳','', '| 状態 | 件数 |','|---|---:|']
    lines += [f'| {status} | {count} |' for status,count in sorted(counts.items())]
    lines += ['', 'この内訳は「この索引で照合を済ませた範囲」の件数。194件などの旧暫定残数との単純な減算はしない。',
              'B356/B357はround5/7の一般構成を優先し、round24の別証明を二件追加とは数えない。','',
              '## B001〜B600','', '| ID | 原文の題名・種別 | 原文監査 | 採用した証拠 |','|---|---|---|---|']
    for row in rows:
        title = row['title'].replace('|','∣')
        original = f"[{row['id']}](../{row['bank']}#L{row['original_line']})"
        evidence = f"[{row['preferred_report']}]({row['preferred_report']})" if row['preferred_report'] else f"旧個票参照{len(row['evidence_pointers'])}箇所（JSON）"
        lines.append(f"| {original} | [{row['tag']}] {title} | {row['original_status']} | {evidence} |")
    lines += ['', '再現: `python research/experiments/original-claims/scripts/round26_scope_index.py`。',
              '[機械可読索引](../output/round26_original_scope_index.json)には各原文行、節の前提、根拠の種類と採用理由を含める。',
              '根拠の更新はスクリプト内の明示的なREVIEWEDへ加える。推測したステータスで空欄を埋めない。','']
    atomic_text(REPORTS/'round26-original-scope-index.md','\n'.join(lines))
    print('PASS originals=600; reviewed=',reviewed_count,'audit states=',counts,'pointers=',sum(len(r['evidence_pointers']) for r in rows))


if __name__ == '__main__':
    main()
