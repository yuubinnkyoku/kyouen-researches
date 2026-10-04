> **監査一次資料**：旧カードの原文・節の前提、実装、raw出力と現行Kを照合した。現在の結論の正本はknowledge。

# B201–B250 残る40件の原文監査

更新: 2026-10-04。開始時main 3e8470fではB151–B200が既に監査済み。ここではNOT_AUDITEDの40件だけを追加する。

標準盤の既定は正方形であり、長方形の弱化証人を正方形へ移さない。Rは全極小残余禁止hypergraph、Pは二点影（K0108）。旧residual_graph実装はPを返す。旧proof_mの子和DPは木のサイズであって最小共有DAGではない。

| ID | 原文監査 | 根拠・量化・限界 | 個別一次資料 |
|---|---|---|---|
| B201 | INCONCLUSIVE | 標準盤は原文冒頭でn×nと定義され、K_nも正方形容量。n≤6の一点削除では証人なし。2×6のK=6保存・勝者反転は長方形への弱化であり原文の正方形存在証人にはしない。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B202 | INCONCLUSIVE | n≤6の正方形では一点削除後もKが保存され、容量低下の前提を満たす証人がない。有限不発見は一般存在命題の反証ではない。 | [round5-batch-b201-b230.md](round5-batch-b201-b230.md) |
| B203 | INCONCLUSIVE | 原文の対象は9×9の全81一点削除盤。確認済みn=5,6の頑健性は別盤の結果で、9×9の削除盤勝敗は未計算。K0021の全初手勝ちとも別の操作。 | [round5-batch-b201-b230.md](round5-batch-b201-b230.md) |
| B204 | SUPPORTED | 4×4からp=0,q=3を単独削除するとg=0、同時削除するとg=2。batch09_pairs_n4.jsonの全120対と一点削除値を照合し原文の存在を満たす。 | [round5-batch-b201-b230.md](round5-batch-b201-b230.md) |
| B205 | INCONCLUSIVE | n=5全100最大配置の各点被覆は正で、排除点がない。長方形での同様の不発見も一般反証ではなく、排除点かつ勝者反転の証人は未取得。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B206 | PARTIAL | n=4の勝ち手頻度・gateと次数の相関、矩形で同次数の削除効果差はある。しかし原文の同次数条件下で媒介性とg変化を比較する回帰は未実施。次数で決まらないことだけでは媒介性優位を証明しない。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B207 | SUPPORTED | 4×4のp=0,q=3でK_full=K_p=K_q=K_pair=7、容量損失0は加法的。一方g_full=g_p=g_q=0、g_pair=2。原文は非零容量損失を要求せず、正方形の証人で決着。 | [round5-batch-b201-b230.md](round5-batch-b201-b230.md) |
| B208 | PARTIAL | n=3の外周付加は変化4/不変12、n=4は変化12/不変8。任意の十分大きいnで両型があるという量化を満たす一般構成はない。 | [round5-batch-b201-b230.md](round5-batch-b201-b230.md) |
| B209 | PARTIAL | n=4では対称孔の反転率が高いが非対称反転も8組。原文は同サイズ・同削除次数和で対称孔のみ反転する盤の存在であり、次数和を統制した証人は未取得。他群の非対称反転は存在命題全体を反証しない。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B210 | PARTIAL | 矩形の端距離・角で盤全体の削除結果を分類した有限例はあるが、終盤R(S)の点削除に適用する一般局所規則は未構成。90%の分類精度はゲーム値の完全保存条件ではない。 | [round5-batch-last21.md](round5-batch-last21.md) |
| B214 | SUPPORTED | 二行の(a,0),(b,0),(c,1),(d,1)の共円はa+b=c+dと同値。各行高々3石、対和集合の交差を禁止する状態で全継続を表せる。3+1の円はなく同一行4石だけが共線禁止。K0069の全長強解決とも整合。 | [round4-two-row-order-strategy.md](round4-two-row-order-strategy.md) |
| B217 | SUPPORTED | 2×6と3×4は面積12・最大安全6で、空盤gは0対2。長方形を明示した原文の存在条件を満たす。最小性の完全証明は別であり採用しない。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B218 | PARTIAL | 面積16の2×8対4×4で空盤反転の差を確認。しかし原文は安全局面母集団のP/N変化率の縦横比依存で、空盤の0/1比較はその統計を測っていない。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B221 | INCONCLUSIVE | 対象はn≤9の正方形。n=4,5では標準と円のみの空盤勝者は一致。2×6等の反転は長方形への弱化で、正方形n=6..9に原文証人なし。 | [round5-batch-b201-b230.md](round5-batch-b201-b230.md) |
| B222 | SUPPORTED | 原文本文はW非空を条件にしない。4×4の標準と直線のみは共に空盤g=0、W=空集合で一致し、禁止制約のあるn≥4盤という条件を満たす。追撃が追加した非空Wの存在は別の未解決問い。円のみ計算との取り違えには依拠しない。 | [round5-batch-b201-b230.md](round5-batch-b201-b230.md) |
| B223 | SUPPORTED | 原文本文の増加する範囲は、共通の標準安全集合を母集団としたn4のk3→4で56/560=10%から348/1626≈21.4%へ上昇。batch10_extra.jsonを優先し、円のみ集合を分母とした追撃表の21.3%は採らない。全終盤での単調増加までは主張しない。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B225 | PARTIAL | q5・n4でmax g=5に4石で達する有限結果はあるが、h(S)=K(S)−|S|の天井到達を示す資料ではない。q≥5の盤族と少占有での天井達成の一般化は未証明。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B226 | SUPPORTED | 現在のK0310では8×8のmisère空盤は先手勝ちで、通常版K0006も先手勝ち。一致例n8と不一致例n4（通常後手/misère先手）により、指定n≥4正方形内の両存在を満たす。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B229 | PARTIAL | n4で閾値2に最大配置数64→8が容量低下より先に起きるが、D4軌道サイズは全て8のまま。対称性分布の先行変化を証明したわけではなく、高対称配置はこの盤にない。 | [round5-batch-b201-b230-followup.md](round5-batch-b201-b230-followup.md) |
| B230 | SUPPORTED | n4で点数≤4のcarrierに由来する禁止を省略しても石数0,1層のP/Nを完全保存する有限例がある。原文は特定層と非自明条件の存在であり、全層保存も全n定理も要求しない。 | [round4-batch-b228-b290.md](round4-batch-b228-b290.md) |
| B231 | PARTIAL | K0293の全n1..7スペクトルでg=0..9を実現。任意mの一般実現は未証明。mexによる小さい値の実現は最大nimberの無界性の代わりにはならない。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B232 | PARTIAL | 小グラフの二点影P(S)の出現は計算済みだが、scriptsのresidual_graphは三点・四点極小辺を落とす。K0108のR(S)全体が指定グラフのみになることと全有限グラフの実現は未証明。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B233 | PARTIAL | 有限の木の次数列をP(S)成分で検出したが、成分の出現は全Rの木実現ではなく高階辺排除も未検査。次数列は一般に完全同型不変量でない。全ての木の量化は未証明。 | [round5-batch-b231-b250-followup.md](round5-batch-b231-b250-followup.md) |
| B234 | PARTIAL | n5二石のP(S)にK2九成分という有限観測はあるが、三点・四点辺が成分を結ぶ可能性を落とした旧計算。非自明Hの正確なR直和を任意r構成する一般族は未取得。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B235 | PARTIAL | n5で二点影の成分が平行移動対応する20例はあるが、完全Rの遮蔽付き合成を保証する座標十分条件ではない。高階横断辺の排除と一般写像は未証明。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B236 | PARTIAL | n4,5の全Grundyに基づく後退解析で連続一意勝ちr=2の証人を確認。任意rの族は未構成。有限でr3不発見は全盤での不可能性ではない。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B237 | PARTIAL | n5で一手後の二点影の成分数が3増える観測はあるが、高階辺を含むRの独立分裂は保証しない。任意rの独立領域を作るという主張の一般構成もない。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B238 | PARTIAL | n4のS空、q1=0,q2=1,p=2で子gは1,1、p後は5,0。nimber同値から分岐する有限核は確認。ただし同nimberは継続ゲーム同型ではなく、原文の同じ継続型を満たす証人まではない。 | [round5-batch-b231-b250.md](round5-batch-b231-b250.md) |
| B239 | PARTIAL | N2・N3で局所正方形内の中間点を全禁止して四隅を合法に保つ固定石証人はある。より大きい全盤にFを置くため、その盤の残り合法点も含めた元ゲームの正確な実現・一般クラスの証明はない。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B240 | SUPPORTED | 4×4で占有集合S1={0},S2={1}はg=1で直和同値。共通の占有T={2}を加えるとg=5対0。round5_b231_n4.jsonのembedding_splitに具体値があり、同nimberと幾何置換の違いを示す。 | [round5-batch-b231-b250.md](round5-batch-b231-b250.md) |
| B241 | PARTIAL | 5×5の九勝ち初手と三D4軌道は確定。追撃のmin_child_L等は完全Grundyで勝ち手を選別した後の規則で、共通の短い応答証明の抽出を与えない。全勝利の有限事実と幾何的短証明を区別。 | [round5-batch-b231-b250-followup.md](round5-batch-b231-b250-followup.md) |
| B242 | SCOPE_UNCLEAR | 戦略モードの表現言語・サイズが未定義。完全Grundyの勝ち手oracleを一モードと数える追撃なら自明になるが、原文の局面幾何による切替10種類との同一性を判断できない。36初手勝ち自体はK0004で確定。 | [round5-batch-b231-b250-followup.md](round5-batch-b231-b250-followup.md) |
| B243 | PARTIAL | K0268/K0269の軌道骨格・容量制約で最大配置の排他相を確認。旧追撃は中心説を修正したが、同じ補題が勝敗証明で大量局面を処理することは未提示。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B244 | SUPPORTED | K0295で5×5勝者は終局7石を全応手に対し保証でき、K5=9より小さい。7と9は同じ勝者側の偶奇なので9を避ける保証は偶奇だけから出ない。n4の6<K4=7だけの旧証拠より強い現在の固定長保証を使う。 | [round25-forced-length-holes.md](round25-forced-length-holes.md) |
| B245 | PARTIAL | n4では勝ち手数を固定すると反復群の生proofは大きく、n5追撃の圧縮差平均38.4対1.5は勝ち手数を固定していない。WLと二点影による共有は完全R同型の証明でもない。原文指定の統制下の共有量増加は未確定。 | [round5-batch-b231-b250-followup.md](round5-batch-b231-b250-followup.md) |
| B246 | SUPPORTED | 完全な残余禁止hypergraphの同型を十分条件とすれば全手・全子・証明を写せる（K0108）。K0227の非D4同値配置の正確なR同型が、D4より粗い分類が実際にある証拠。二点影だけの旧Node-Kayles論証は採用しない。 | [round42-exact-residual-family-audit.md](round42-exact-residual-family-audit.md) |
| B247 | PARTIAL | n5で64件の非交差最小化手を検出する旧proof_mはP節点で1+Σ子proof、N節点で1+min子proofという木サイズ。共有可能なDAG最小化とは異なるため、原文の最小DAGとの食い違いまでは未証明。 | [round5-batch-b231-b250.md](round5-batch-b231-b250.md) |
| B248 | SUPPORTED | n3全安全局面はK0004のg∈{0,1}、全極大5石。石数偶奇という一整数で勝敗を分け、Nから任意合法手がPへ行く共通応答形式を与える。原文は小盤の存在であり、n4,5の不完全な特徴分類を一般証明にしない。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B249 | PARTIAL | g1の有限木proofサイズ急増はn4,5で測定したが、無界盤族の指数下界はない。Pで子サイズを加算する旧DPはDAG共有を最小化せず、深さ別有限比を漸近定理へ昇格しない。 | [round5-batch-b231-b250-push3.md](round5-batch-b231-b250-push3.md) |
| B250 | SCOPE_UNCLEAR | 定数の一様性、円束パラメータの表現・許すクラスが未指定。旧反証は一石効果の加算という追加条件を否定するだけで、原文のあるクラスの存在を否定しない。 | [round5-batch-b231-b250.md](round5-batch-b231-b250.md) |

追加照合資料:

- [原文の定義とB201以降](../../../archive/hypothesis-ledgers/hypothesis-bank-2026-09-27.md)。原文の正確な行と前提は生成JSONに保持する。
- [4×4二点削除全120対](../output/batch09_pairs_n4.json)：B204/B207のp0,q3の値。
- [共通安全母集団の層別値](../output/batch10_extra.json)：B223の分母は1626であり1636ではない。
- [二点影をRと呼ぶ旧コード](../scripts/round5_b231_n5.py)：residual_graphとproof_mの定義を直接監査。
- [5×5有限証人](../output/round5_b231_n5.json)、[4×4証人](../output/round5_b231_n4.json)、[終端上限DP](../output/round5_b231_n4b.json)。
- [K0295](../../../knowledge/items/K0295-n1-n7-full-tstar-and-wft.md)：B244をWFT7で支持。
- [K0310](../../../knowledge/items/K0310-misere-square-outcomes-through-eight.md)：B226のn8一致例。
- [K0227](../../../knowledge/items/K0227-abstract-residual-isomorphism-split-fibers.md)、[正確な族監査](round42-exact-residual-family-audit.md)：B246で二点影の代わりに完全R同型を使う。

有限・弱化結果だけを持つカードは独立Kを量産しない。B204/B207の正方形削除相互作用とB240の幾何置換非保存は独立した有限知識として保持する。
