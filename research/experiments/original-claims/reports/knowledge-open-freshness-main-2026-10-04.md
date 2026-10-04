# 最新mainのopen / conjectured再監査（2026-10-04）

基準HEAD: `5ab6e04436201e0de8045cea6e9a42bddd2c4f28`。正本は`research/knowledge/items/`。

開始時の全317項目からkindを限定せずopen/conjectured/needs-review/scope-unclearを抽出した。対象は35件（34 open、1 conjectured）。全件をK-ID・alias・主要語でrepo横断検索し、出典の量化と後続成果を照合した。python/はこのmainに存在しないため、Python実装はscripts/とresearch/verification/scripts/を検索した。

[機械抽出・全35件の本文/metadata・検索候補・採用境界・証拠hash](knowledge-open-freshness-main-2026-10-04.json)。検索候補の全ファイルを逐一再実行したという意味ではない。

## 集計

| 指標 | 件数 |
|---|---:|
| 監査対象 | 35 |
| 結論の未確定を維持 | 35 |
| 最終open / conjectured / scope-unclear | 33 / 1 / 1 |
| 今回新たに解決済みへ更新 | 0 |
| 対象Kの修正 | 10 |
| 部分知識・証拠境界の本文更新（scope修正と重複） | 8 |
| scopeの明示・訂正（本文更新と重複） | 10 |
| 新規K | 0 |

判定はA=26（未解決維持）、C=6（部分結果の具体化）、E=3（量化・意味の修正）。B/Dは0。scope明示には通常版とmisère版、およびhの定義の分離も含む。

## 全件判定

| K-ID | 開始title | 判定 | 現在の根拠と残件 |
|---|---|---|---|
| [K0101](../knowledge/items/K0101-prime-parabola-equality-open.md) | 全奇素数で剰余放物線上界(p+3)/2が達成されるかは未確定 | A / open | Q_pの等号達成は29素数5..127の完了証人。全奇素数の構成は未証明。全盤下界とは量化が異なる。 |
| [K0102](../knowledge/items/K0102-concrete-lean-certificate-checker-open.md) | 具体巨大証明書をLean核のみで検査する実装は未完成 | A / open | Kyouenの一般健全性とC++/Rustの具体binary検査を分離。Lean内の巨大具体証明書parse・全条件検査は未実装。 |
| [K0103](../knowledge/items/K0103-n10-single-empty-root-certificate-open.md) | 10×10空盤面全体の単一KYOENC4証明書は未統合 | A / open | 100初手は分類済みだが、空盤全分岐を一本にしたKYOENC4は未統合。選択局面証明では代替しない。 |
| [K0105](../knowledge/items/K0105-n11-empty-root-winner-open.md) | 11×11の真の空盤勝敗は現在の主要未解決問題 | C / open | 標準通常版空盤はUNKNOWN。exact層0..5、層6資源下界、df-pn、s_11とK_11の別結果を明示。 |
| [K0113](../knowledge/items/K0113-losing-first-move-odd-nimber-open.md) | 負け初手後のnimberは奇数 | A / open | n≤7の一石非零gは奇数。8盤全Grundy DPは完走報告があるが保存集計はP/Nで、一石値の偶奇を追加認定できない。 |
| [K0119](../knowledge/items/K0119-jn-losing-board-connectivity-open.md) | 後手勝ち正方形盤のJ_nは連結 | A / open | J4/J7の連結は完全確認。8盤二石P数1380だけではJ8連結は判断できず、全後手勝ち盤の一般証明もない。 |
| [K0121](../knowledge/items/K0121-uniform-saturation-by-layer-four-open.md) | 飽和開始は4石以内 | A / open | σ4=2,σ5=σ6=3,σ7=4。8盤保存集計には層別最大g・σ8がなく、全nのσ≤4は未証明。 |
| [K0139](../knowledge/items/K0139-six-stone-exclusion-short-cover-proof-open.md) | 六石非存在は三つ組の共起だけで短く説明できる | A / open | 10盤六石補完総数最大85は完全最適化済み。原文の短い非列挙証明は未完成。 |
| [K0141](../knowledge/items/K0141-n10-20-stone-existence-open.md) | 10×10では20石まで届くか | E / open | 20石存在K_10≥20と旧B082の等号K_10=20を分離。19≤K_10≤23とT/U近傍の局所排除を維持。 |
| [K0143](../knowledge/items/K0143-asymptotic-two-n-safe-construction-open.md) | 2n−O(1)石の安全配置を無限族で作れる | A / open | 全分裂素数でKp≥pの自足証明あり。repo内の2n-o(n)先行研究紹介も2n-O(1)の構成ではない。 |
| [K0145](../knowledge/items/K0145-n10-minimum-maximal-ten-open.md) | 10×10の最小極大は10石 | A / open | s10は9..10。8石全域排除と10石証人は有効だが、9石の有無は未確定。 |
| [K0147](../knowledge/items/K0147-sublinear-minimum-maximal-open.md) | 最小極大は線形より小さくなる | C / open | 指数下界とn=11..15のn-1石極大構成を反映。有限n-1上界はo(n)を意味しない。 |
| [K0148](../knowledge/items/K0148-minimum-maximal-exponent-two-thirds-open.md) | 最小極大の指数は2/3 | C / open | 全固定qへの指数下界と円ノルム改良を反映。標準版の指数等号に必要な上界は未証明。 |
| [K0149](../knowledge/items/K0149-minimum-maximal-monotonicity-open.md) | s_nは単調増加する | C / open | n≤10の非減少性は有効。8≤s11≤10では10→11の大小関係は判断できない。 |
| [K0160](../knowledge/items/K0160-single-rule-removal-winner-flip-open.md) | 禁止四点組一つを外すだけで空盤勝者が反転する | A / open | n≤7全単独禁止解除に勝者反転なし。有限除外を全n不存在へ昇格させない。 |
| [K0182](../knowledge/items/K0182-all-losing-first-moves-few-nimbers-open.md) | 全初手負け盤でも一石nimberの種類数は小さい | A / open | 7盤一石gは全49点で1。8盤DPのP/N集計だけでは値の種類数を認定できず一般上限は未証明。 |
| [K0183](../knowledge/items/K0183-saturation-missing-nimber-contiguity-open.md) | 飽和開始層で欠けるnimberは連続しない | A / open | 7盤飽和開始層0..10は穴なし。全盤の欠落連続性は未証明。8盤に必要なg分布は公開集計にない。 |
| [K0184](../knowledge/items/K0184-saturation-missing-nimbers-powers-of-two-open.md) | 飽和開始層で欠ける正のnimberは2の冪だけ | A / open | 7盤開始層に正の穴なし。全盤で欠落値が二冪だけという一般則は未証明。 |
| [K0185](../knowledge/items/K0185-ceiling-with-small-mobility-slack-open.md) | 天井達成局面は合法手数の小さい余裕で作れる | C / open | 7盤の最小余裕列とhの定義を明示。h→∞の固定余裕族は未証明。misère補助mexのhとは別。 |
| [K0186](../knowledge/items/K0186-ceiling-three-distinct-winning-orbits-open.md) | g=h≥3の局面には、対称性ではまとめられない勝ち手がある | E / open | 原文の軌道サイズ1/2をtitleとscopeへ反映。7盤全件成立は全盤定理ではなく、hは通常最大残り手数。 |
| [K0187](../knowledge/items/K0187-empty-root-wft-singleton-open.md) | 空盤のWFTは空でなければ単元 | A / open | 空盤WFTはn1..6単元、n7空。B040の反例はB331の一意性の反例ではない。 |
| [K0190](../knowledge/items/K0190-forced-terminal-median-open.md) | 空盤で強制できる終局長はT*の中央値 | A / open | n≤6の単元WFTはT*中央値、n7は前件外。固定証明書終局一覧はT*の代替でない。 |
| [K0193](../knowledge/items/K0193-effective-triple-tree-minimal-type-open.md) | 木の競合グラフで効く三点制約には最小の接続型がある | A / open | 最小接続木K1,3と三葉三点辺は確定。新しいmisère局所定理や三手情報の定理は大木の距離偶奇分類を閉じない。 |
| [K0199](../knowledge/items/K0199-cocircular-avoidance-superlinear-deficit-open.md) | 共円回避を加えると欠損は超線形 | A / open | δ>k(log log k)^ηの一般下界は有効。固定ε>0のk^(1+ε)へは届かない。 |
| [K0216](../knowledge/items/K0216-uniform-external-saturation-radius-open.md) | 最大配置の外部飽和半径は一様有界 | A / open | 整数拡大でr=1にできる一般定理は最大性を保存しない。12盤22石外周例も最大性未確定で全最大Sの一様上界を閉じない。 |
| [K0217](../knowledge/items/K0217-minimum-maximal-external-blocking-band-open.md) | 盤内では最小極大なのに盤外の広い帯まで塞ぐ | A / open | 拡大定理は最小極大性を保存しない。外周を塞ぐ22石配置の最小性も未証明なので無界最小極大族の証人ではない。 |
| [K0221](../knowledge/items/K0221-interior-relocation-external-gap-open.md) | 内側の石を動かすだけで盤外の最初の合法点が遠くへ飛ぶ | A / open | 拡大は複数石移動であり一石移動ではない。外周2層までの有限例はr差の無界族を与えない。 |
| [K0226](../knowledge/items/K0226-one-fewer-stone-fiber-bridges-open.md) | 一石少ない中間配置を許すと同一残局族を少数の橋で結べる | A / open | 四石対の三石Johnson橋は一般証明済み。k≥5の少数橋分類と全族の接続は未証明。 |
| [K0232](../knowledge/items/K0232-circle-window-single-point-cuts-open.md) | q≥3の円は境界に切られても点数を一つずつ変えやすい | E / scope-unclear | qは中心分母。固定窓穴なしはprovedな部分だが、種類数がより多い統計比較の母集団・窓条件は未指定。scope-unclearに更新。 |
| [K0276](../knowledge/items/K0276-h-dense-independent-holdout-open.md) | H-denseはn≤10の記述を越える独立確認が未完了 | A / conjectured | conjecturedの命題も対象に含めた。標準通常版n>10の独立holdoutは未完了。misère8盤混在初手は反例ではない。 |
| [K0281](../knowledge/items/K0281-n7-geometric-two-phase-proof-open.md) | 7×7二相選択を制約solverなしの幾何だけで導く証明は未完成 | A / open | 有限核の二相分類は完了。COMPLETE solver容量・七残余・相liftを一般幾何だけへ置き換える証明は未完成。 |
| [K0282](../knowledge/items/K0282-n7-g11-global-connectivity-open.md) | 11石を許したG11で最大由来八成分が全て接続するか未確定 | A / open | G12八成分と代表Uの幅11経路は確定。全盤で八成分がG11で接続することや全成分分類は未確定。 |
| [K0297](../knowledge/items/K0297-minimum-maximal-private-point-open.md) | n≥2の全最小極大配置に一重被覆点があるか | A / open | n2..8の全最小極大とn9の限定16配置で一重被覆点を確認。新11盤10石は最小性未確定なので一般全称を閉じない。 |
| [K0298](../knowledge/items/K0298-minimum-maximal-rho-one-open.md) | n≥2の全最小極大配置で故障耐性ρが1か | A / open | n2..8全件とn9限定16配置でρ=1。単なる極大例への故障耐性を全最小極大の結果と混同しない。 |
| [K0311](../knowledge/items/K0311-misere-n9-outcome-open.md) | misère版9×9の空盤勝敗は未確定 | C / open | misère9盤の中央・角JSONは130,000,000保存局面でUNKNOWN、証明書なし。通常9盤との相違とmisère6..8盤の直前結果を明示。 |

## 開始前の移植で閉じた旧open

今回の35件に「解けているのにopen」の追加例はない。以下はe8794fdから開始HEADまでの移植で閉じており、今回の解決件数には加えない。

| K-ID | 移植前title | 現行結論 / status | 根拠 |
|---|---|---|---|
| K0071 | 3×m・q=5は12≤M_{3,5}≤56、m=12..21とm≥56は強解決（proved） | 3×m・q=5の真の満容量安定化長はM_{3,5}=12 / proved | [q35-exact-threshold.md](../q35-exact-threshold.md) |
| K0077 | 4×m・q=8の真の安定化長は未確定（open） | 4×m・q=8の真の満容量安定化長はM_{4,8}=11 / proved | [q48-exact-threshold.md](../q48-exact-threshold.md) |
| K0078 | 3×m・q=5のm=22..55に不足極大が再出現するかは未確定（open） | 3×m・q=5のm=22..39にも不足極大安全集合は存在しない / computed | [q35-exact-threshold.md](../q35-exact-threshold.md) |

K0071は旧時点でもboundsをprovedとした命題で、旧openはK0077/K0078の2件。さらにM_{3,4}=24、M_{4,6}=16、M_{4,7}=13はK0302に採用済みで、同じ問いのopen重複はない。

## 逆方向の証拠境界

- K0006: 8盤全Grundy完走報告と独立全件検査未整備を分離。公開P/N集計から一石g等を新規推定しない。
- K0023: 層0..5 computed/solution unsolvedは整合。
- K0028: 旧打切り勝敗はwithdrawnで正しい。反対の勝者を証明したのではない。
- K0035: 19≤K10≤23は局所排除後も維持。
- K0058: 旧半整数走査の限界を維持し、後続全中心n≤112のK0307へ案内を更新。
- K0071/K0077/K0078: 閉鎖済みstatusと全称末尾・有限排除・直前証人の範囲が整合。
- K0106: ノルム2(n-1)^6の証明pathをgeometry-20261003 §10へ訂正。
- K0302: 5閾値は24,12,16,13,11。5件に含まれないM3,6=9のK0070をgeneralizesする誤った辺を除去。
- K0307: 全中心n≤112完全計算、小盤独立検算。有限を全nへ昇格していない。
- K0310: 主出典と6/7盤JSONを追加。6盤全局面mex対、7/8盤rootと全初手P/Nを区別。
- K0312: 完了排除記録は有効。別再実行の証拠を確認できなかったため再実行でも計数一致という一文を削除。
- K0313: 21/22石の直接安全・極大検査による存在下界。最適値ではない。
- K0316: T/Uへの条件付き完了非存在を全域上界19へ拡張していない。

## 旧記録・今回決着しなかった範囲

- N11-STATE-SPACE.mdのK_11=11・204,424,228状態は64-bit truncation由来。冒頭の廃止注記が現行で、後半の旧数値を再採用しない。N11の層5打切り勝敗も撤回済み。
- F-Kの「n=8..24で16点」と「n=8..11で12点」の矛盾は、全中心n≤112の完全計算で有限範囲が解消された。半整数走査そのものを全中心証明へ読み替えない。
- Round5の8盤DPはGrundy全計算の報告があるが、公開JSONは層別P/N等の集計。一石値・σ8・飽和層の穴・J8連結・WFTを追加認定するには個別の保存値や監査が必要。再計算は今回行わない。
- 新11盤10石極大の最小性は未確定。私有点・故障耐性や外周被覆の有限例を、全最小極大族・全最大族の定理へ拡張しない。
- 幅17..31の全中心無限帯の等号P(w)=Q(w)、最大安全の漸近構成、20石存在、標準11盤とmisère9盤の勝敗は今後の研究対象。今回新たにKを増やしたり探索したりしていない。
- 旧open-freshness-auditブランチは現行mainの正本ではない。開始時にmainへ切り替えてfetch/ffし、旧監査の判定を流用しなかった。

## 検証

- uv sync --locked: 成功。
- check.py: 317 items、0 errors、0 warnings。
- unit tests: 29 tests、OK。
- build.py: 317項目から6生成viewとREADME管理領域を更新。
- commit直前にorigin/mainを再取得し、HEADが基準の5ab6e04のままで競合更新がないことを確認済み。commit後のbuild.py再実行とgenerated diff --exit-code、最終commitのCI結果は最終報告に記す。
- 基準HEADの[通常CI](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/37139442882)と[Knowledge integrity](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/37139442877)は成功。最終commitのCI結果は最終報告に記す。

READMEの既存詳細本文は保護し、K項目からのgenerator管理領域のみを再生成した。knowledge READMEの旧K0071リンクとMIGRATIONの旧固定幅残件表現を修正した。
