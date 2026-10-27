# 共円ゲームの計算・証明・構造研究

完全指摘ルールの共円ゲームについて、標準 **1×1〜10×10の空盤勝敗を確定**しています。
**1×1〜8×8は全安全局面のGrundy数まで解析済み、9×9・10×10は弱解決、11×11は未解決**です。
8×8の全状態独立再計算と全局面証明書は未整備で、計算範囲と検証範囲を区別します。

固定幅q点版の一般定理と厳密閾値（**M_{3,5}=12、M_{4,8}=11**）に加え、misère、最大・極大安全配置、格子幾何、再配置、探索方式も研究対象です。
現在の命題・計算結果・反証・未解決問題・検証境界の唯一の正本は
[research/knowledge/items/](research/knowledge/README.md)です。
以下の解決状況は正本から生成します。実験記録や旧まとめは現在の結論を維持する場所ではありません。

## 記号・用語

このリポジトリでは正方形盤・長方形盤・q点版、Grundy数、最大・極大配置などを同時に扱います。
READMEと主要な研究ノートでは、基本的に次の意味で使います。厳密なルールは
[K0001](research/knowledge/items/K0001-complete-call-rules.md)、Grundy数とP/Nは
[K0002](research/knowledge/items/K0002-grundy-and-first-move-conventions.md)、解決段階は
[K0003](research/knowledge/items/K0003-solution-and-evidence-levels.md)を正本とします。

| 記号・用語 | 意味 |
|---|---|
| 完全指摘 | 新しく置いた石を含む4点が同一円または同一直線上になれば着手者が負けるルールを、安全な追加だけを合法手として扱う等価な有限通常プレイ。合法手がない側が負ける。 |
| $n$ | 標準の **$n\times n$ 正方形盤の一辺の点数**。正方形盤の分類では $n$、固定幅長方形盤では $w\times m$ を使う。 |
| $B_n$ | 標準 $n\times n$ 盤の点集合 $\{0,\ldots,n-1\}^2$。 |
| $w$ | 長方形盤 $w\times m$ の **行数（固定する幅）**。 |
| $m$ | 長方形盤 $w\times m$ の **各行の点数（長さ）**。固定幅研究では $w$ を固定して $m$ を大きくする。 |
| $q$ | **同一円または同一直線上に何点そろうと禁止か**を表す。標準の共円ゲームは $q=4$。q点版では通常 $q\ge4$。 |
| $D(w,m)$ | 長方形盤の点集合 $\{0,\ldots,m-1\}\times\{0,\ldots,w-1\}$。 |
| $S$ | ある局面で **すでに石が置かれている点の集合**。$\lvert S\rvert$ は石数。禁止q点集合を含まない $S$ を「安全」と呼ぶ。 |
| $g(S)$ | 局面 $S$ の **Grundy数**。$g(S)=\operatorname{mex}\{g(S\cup\{p\})\}$。通常プレイでは $g(S)=0$ がP局面、$g(S)>0$ がN局面。 |
| P局面 / N局面 | Pは **手番側が負ける局面**、Nは **手番側が勝てる局面**。初手 $p$ が先手の勝ち手である条件は、子局面 $\{p\}$ がPであること。 |
| $K_n$ | 標準 $q=4$ の $n\times n$ 盤で作れる **安全集合の最大石数**。$s_n$ は別の量。 |
| $s_n$ | 標準 $q=4$ の $n\times n$ 盤で、**極大安全集合のうち最小の石数**。古いノートでは $K_{\min}$ と書いている場合がある。 |
| $M_n(k)$ | $n\times n$ 盤の **$k$石安全局面に現れるGrundy数の最大値**、$M_n(k)=\max_{\lvert S\rvert=k}g(S)$。固定幅の $M_{w,q}$ とは別物。 |
| $T_{w,q}$ | q点版固定幅定理で使う **明示的な十分長さ**。$m\ge T_{w,q}$ なら全安全局面を一般定理で強解決できる。証明から得る上界で、真の開始長 $M_{w,q}$ とは限らない。 |
| $M_{w,q}$ | **満容量への真の安定化長**。これ以降の全 $m$ で、全極大安全集合が $(q-1)w$ 石になる最小の長さ。通常 $M_{w,q}\le T_{w,q}$。 |
| $W(w,m)$ | 長方形盤での **勝ち初手の集合**。点 $p$ を初手に置いた後の局面がPになる点全体。 |
| $F_n$ | 文脈上、標準 $n\times n$ 盤に含まれる **禁止4点組の総数**を表す記号。 |
| D4対称性 | 正方形の回転4通りと反転を合わせた **8個の対称変換**。同値な局面・初手をまとめるために使う。 |
| 極大 (maximal) | **これ以上1石も合法に追加できない**安全集合。石数が全安全集合中で最大とは限らない。 |
| 最大 (maximum) | 安全集合の中で **石数が最も多い**もの。最大なら極大だが、極大だから最大とは限らない。 |
| 超弱解決 (ultra-weak solution) | **初期局面の結果だけ**を決めること。空盤が先手勝ちか後手勝ちかを確定する段階で、具体的な必勝戦略までは要求しない。 |
| 弱解決 (weak solution) | **初期局面から最適結果を実現する戦略まで**与えること。初期戦略から外れた全局面の分類までは要求しない。 |
| 強解決 (strong solution) | **任意の合法局面**について勝敗と最適手を決められること。全安全局面のP/N分類があれば勝ち手を選べ、全Grundy数はさらに強い情報を与える。 |

<!-- BEGIN GENERATED SOLUTION STATUS -->
## 解決状況

現在の研究結果と未解決問題は [research/knowledge/](research/knowledge/README.md) に整理しています。各結果には参照用の `K0001` のような番号を付けています。以下は、そのうち盤面の解決状況に関する結果を自動生成した一覧です。

| 盤面・条件 | 参照・状態 | 段階・勝敗 | 分類・範囲 | 検証 | 証明書・独立検査・留保 |
|---|---|---|---|---|---|
| 1×1〜6×6; 標準q=4・完全指摘・通常プレイ | [K0004](research/knowledge/items/K0004-n1-n6-all-safe-grundy.md) · computed | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全安全局面 | exhaustive-enumeration | 空盤は各nのAND/OR証明書あり; 小盤参照実装照合、空盤C++検査; 勝者は各盤の個別項目を参照 |
| 7×7; 標準q=4・完全指摘・通常プレイ | [K0005](research/knowledge/items/K0005-n7-all-safe-grundy-audit.md) · computed | strong; second-player-win | root, all-safe-win-loss, all-safe-grundy; 179,810,350/179,810,350安全局面 | exhaustive-enumeration, independent-enumeration | 空盤証明書あり。強解決単独証明書は未整理; 全層独立再帰照合; README旧説明に全Grundy結果を補完 |
| 8×8; 標準q=4・完全指摘・通常プレイ | [K0006](research/knowledge/items/K0006-n8-all-safe-grundy-computed.md) · computed | strong; second-player-win | root, all-safe-win-loss, all-safe-grundy; 6,700,711,937/6,700,711,937安全局面 | reported-streaming-dp | 全局面証明書なし。空盤証明書は別項目; n=6で既知値と全一致、n=7で既知層サイズを照合。8×8全状態の独立再計算は未実施; 全局面Grundy DP完走済み。独立全状態検査・強解決証明書は未整備 |
| 1×1; 標準q=4・完全指摘・通常プレイ | [K0011](research/knowledge/items/K0011-n1-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 2×2; 標準q=4・完全指摘・通常プレイ | [K0012](research/knowledge/items/K0012-n2-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 3×3; 標準q=4・完全指摘・通常プレイ | [K0013](research/knowledge/items/K0013-n3-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 4×4; 標準q=4・完全指摘・通常プレイ | [K0014](research/knowledge/items/K0014-n4-second-player-win.md) · proved | weak; second-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 5×5; 標準q=4・完全指摘・通常プレイ | [K0015](research/knowledge/items/K0015-n5-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 6×6; 標準q=4・完全指摘・通常プレイ | [K0016](research/knowledge/items/K0016-n6-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 7×7; 標準q=4・完全指摘・通常プレイ | [K0017](research/knowledge/items/K0017-n7-second-player-win.md) · proved | weak; second-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 8×8; 標準q=4・完全指摘・通常プレイ | [K0018](research/knowledge/items/K0018-n8-second-player-win.md) · proved | weak; second-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 9×9; 標準q=4・完全指摘・通常プレイ | [K0019](research/knowledge/items/K0019-n9-first-player-win.md) · proved | weak; first-player-win | root; 空盤面からの勝敗維持戦略 | ranked-and-or-certificate, independent-cpp-check | 空盤面AND/OR証明書あり; 共通C++全件検査; 全局面分類とは別 |
| 10×10; 標準q=4・完全指摘・通常プレイ | [K0020](research/knowledge/items/K0020-n10-second-player-win.md) · proved | weak; second-player-win | root; 15 D4代表＝100初手 | exact-search, csv-audit, partial-kyoenc4 | 空盤面の単一KYOENC4証明書は未統合; CSV構造監査＋選択局面Rust証明検査; 勝敗確定。全巨大探索の独立再求解ではない |
| 9×9（全初手）; 標準q=4・完全指摘・通常プレイ | [K0021](research/knowledge/items/K0021-n9-all-81-first-moves-win.md) · computed | weak; first-player-win | root, first-moves; 81/81 first moves | exact-search | 中央初手の空盤証明書あり。全81初手は別探索; 14非中央D4クラスの独立探索記録; 全81初手が先手勝ち |
| 10×10（全初手）; 標準q=4・完全指摘・通常プレイ | [K0022](research/knowledge/items/K0022-n10-all-100-first-moves-classified.md) · computed | weak; second-player-win | root, first-moves; 100/100 first moves; 15 D4 representatives | exact-search, csv-audit, partial-kyoenc4 | 空盤全体の単一KYOENC4なし; CSV監査と選択局面独立Rust検査; 100初手完全分類と空盤証明書未統合を区別 |
| 11×11; 標準q=4・完全指摘・通常プレイ | [K0023](research/knowledge/items/K0023-n11-exact-safe-layers-and-unknown-winner.md) · computed | unsolved; unknown | safe-layers; 厳密列挙は層0〜5のみ | exhaustive-enumeration | 空盤勝敗証明書なし; 禁止四点独立再計数・小盤回帰; 打切りP/Nは真の勝敗ではない |
| w×m・q点版; q≥4,w固定,m≥T_{w,q}=min(A,B) | [K0024](research/knowledge/items/K0024-fixed-width-q-point-threshold.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全安全局面 | mathematical-proof | 一般証明。具体盤の巨大証明書は不要; 67盤の有限検算は支持資料; 先手勝ち iff q偶数かつw奇数 |
| w×m・q>2w; q≥4,q>2w,m≥1 | [K0025](research/knowledge/items/K0025-q-above-two-width-all-lengths.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof | 一般分離証明; 整数幾何と容量の証明; g=(w min(m,q−1)−\|S\|) mod2 |
| w×m・標準q=4; w固定、m≥T_w=3+2{C(3w−2,3)−(w−1)} | [K0068](research/knowledge/items/K0068-standard-fixed-width-parity-threshold.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全安全局面 | mathematical-proof | 全称証明; 有限長方形検算は支持; g=(3w−\|S\|) mod2 |
| 2×m・q=4; q=4,m≥1 | [K0069](research/knowledge/items/K0069-two-row-all-lengths-strong-solution.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | exhaustive-enumeration, mathematical-proof | 短盤全数＋長盤一般証明; 短盤参照mex検算; m≥6は空盤後手勝ち。短盤は個別分類 |
| 3×m・q=6; q=6,w=3,m≥9 | [K0070](research/knowledge/items/K0070-width-three-q6-stabilization.md) · proved | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥9の全安全局面 | mathematical-proof, exhaustive-enumeration | 解析証明＋有限排除; 下界証人と有限補完検査; M_{3,6}=9、g=(15−\|S\|) mod2 |
| 3×m・q=5; q=5,w=3,m≥12 | [K0071](research/knowledge/items/K0071-width-three-q5-exact-stabilization.md) · proved | strong; second-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥12の全安全局面 | mathematical-proof, exhaustive-enumeration, independent-enumeration | 解析上界m≥40＋m=12..39有限完全排除; 小盤subset DPと独立determinant監査; g(S)=(12-\|S\|) mod 2 |
| 高qの標準整数格子; 連続整数行、(q=2w,w≥5)または(q=2w−1,w≥6) | [K0072](research/knowledge/items/K0072-mod9-integer-row-separation.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof | mod9有限剰余証明; 円条件の独立determinant照合; M=q−1 |
| line-only w×m; line-only,q≥4,q>w | [K0075](research/knowledge/items/K0075-line-only-all-lengths-solution.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof | 幾何分離証明; 有限検算を一般証明と区別; g=(w min(m,q−1)−\|S\|) mod2 |
| circle-only w×m; circle-only,q≥4,q>2w | [K0076](research/knowledge/items/K0076-circle-only-all-points-legal.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全局面 | mathematical-proof | 禁止なしの一般証明; 円と直線の交点上界; g=(wm−\|S\|) mod2 |
| 4×m・q=8; q=8,w=4,m≥11 | [K0077](research/knowledge/items/K0077-width-four-q8-stabilization.md) · proved | strong; second-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥11の全安全局面 | mathematical-proof, exhaustive-enumeration | m≥13の一般計数＋m=11,12完全排除＋m=10不足極大証人; m=10証人を全三点曲線生成で独立検査; g(S)=(28-\|S\|) mod 2 |
| 5×m・q=8; 標準整数格子・q=8,w=5,m≥16・通常プレイ | [K0331](research/knowledge/items/K0331-width-five-q8-exact-stabilization.md) · proved | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥16の全安全局面 | mathematical-proof, exact-search, independent-enumeration | 現在必要なm=16..100の255 CNFは過去に全DRAT検査済。全510の独立統合再検査receiptも保存; 全有限長の円集合が別C++生成と一致、m=15証人は全三点曲線で検査。短縮末尾は弦energy proof; g(S)=(35-\|S\|) mod2。境界3トレースを保存、他はhashと再生成コードを保存 |
| 3×m・q=4; q=4,w=3,m≥24 | [K0351](research/knowledge/items/K0351-width-three-q4-exact-stabilization.md) · proved | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥24の全安全局面 | mathematical-proof, exhaustive-enumeration, independent-enumeration | m≥69の解析上界＋m=24..68有限完全排除＋m=23不足極大証人; lifted determinant監査、m=7全安全局面直接照合、m=7と23の例外遷移監査; g(S)=(9-\|S\|) mod 2 |
| 11×11; 標準q=4・完全指摘・通常プレイ・元先手固定視点 | [K0414](research/knowledge/items/K0414-n11-reply27-root-loss.md) · computed | weak; second-player-win | root, first-moves; 119/119 legal moves from root {60,27}; 100 and 108 use S4 (1297036692683752448,0) | exact-search, csv-audit, independent-enumeration | 全119手に少なくとも一つS4 LOSS応手。新規S4の106 S5子は全てexact LOSS。solver-trusted leavesを使用。; 独立Boardが全合法root手、S4応手、各S4の完全S5境界、AND/OR極性を再生成・照合。終局のみの独立DAGではない。; 二石局面{60,27}だけをLOSSと分類。11×11空盤面の勝者は未確定。 |
| 異方格子w×m・q点版; w≥5、h,d≥1、v₃(d)≤v₃(h)、q>2ceil(2w/3) | [K0436](research/knowledge/items/K0436-anisotropic-mod9-all-widths.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof, independent-enumeration | 3進二階差商・法9剰余の81組完全分類と9周期帰納; 17種類の有限盤の全非共線三点から整数円を独立列挙; M=q−1、g(S)=(w min(m,q−1)−\|S\|) mod2 |
| 五本の異方整数格子水平行・q点版; h,d≥1、v₃(d)≤v₃(h)、q≥9、五本の等間隔水平行 | [K0440](research/knowledge/items/K0440-five-row-anisotropic-mod3-circle-exclusion.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof, independent-enumeration | 3進降下法と法9の16剰余組の全称証明; 14種類の有限盤で全非共線三点から円を生成・整数係数で照合; M=q−1、g(S)=(5min(m,q−1)−\|S\|) mod2 |
| 異方格子のw×m・q点版; w≥4、q≥w+1、ある奇素数pでv_p(h)>v_p(d) | [K0461](research/knowledge/items/K0461-prime-adic-anisotropic-row-sparsity.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof, independent-enumeration | 二点行の中心整数性と法p²への単根持上げによる全称証明; 非共線三点から円を整数係数で独立生成した56有限盤; g(S)=(w min(m,q-1)-\|S\|) mod2、M=q-1 |
| 3×5・q=6・左右対称な実数5列; 各行の横座標が共通の{-u,-v,0,v,u}、縦座標{0,a,a+b} | [K0466](research/knowledge/items/K0466-symmetric-five-column-q6-rigidity.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全u>v>0、a,b>0、全安全局面 | mathematical-proof, exhaustive-enumeration, independent-enumeration | 二点和の重複条件と円の根の積から全称3型帰着、15点全局面mex; 5整数代表について全5005六点組を独立行列式検査し全局面結果を照合; u≠2vでは最大2円、空盤gは円本数0,1,2に対して1,0,1。u=2vでは最大4円。 |
| 標準整数格子 w×m・q点版; w=5..16かつq>P(w)、またはw≥15かつ本文の合同別十分条件 | [K0467](research/knowledge/items/K0467-tangent-mod16-fixed-width-circle-capacity.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof, independent-enumeration | K0072の二重点行数定理と接線行のmod16全剰余証明; 有限6盤の三点円列挙、法16の独立2方式; g(S)=(w min(m,q−1)−\|S\|) mod2、M=q−1 |
| 3×5・q=6・実数行間隔; 横座標{0,1,2,3,4}共通、縦座標{0,a,a+b}、q=6 | [K0468](research/knowledge/items/K0468-three-by-five-q6-real-row-gap-classification.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全a,b>0、各場合の全安全局面 | mathematical-proof, exhaustive-enumeration, independent-enumeration | 円成立条件の6直線・13場合への全称帰着と15点全局面mex; 全13代表の5005個の6点組を4×4整数行列式で独立生成し全局面結果と照合; 空盤g=0 iff 円1本、それ以外は1。最大円4本はa=b=1のみ |
| 不等間隔3列×4行・q=4; d²がab(a+b)を割らない、またはab>6d²、より一般に三列円判定式288個が全て不成立 | [K0474](research/knowledge/items/K0474-three-column-four-row-generic-q4.md) · proved | strong; second-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; 指定された算術条件を満たす全正整数a,b,dの全安全局面 | mathematical-proof, exhaustive-enumeration, independent-enumeration | 円の完全算術判定と27禁止組への還元、12ビット1655安全局面の完全mex計算; Pythonの整数3×3行列式とC++の整数4×4置換行列式、別方式の再帰が一致; 空盤g=0、全12初手g=4、極大石数5/6/7 |
| 不等間隔3列×3行・q=4; 完全指摘・通常プレイ、列位置0,a,a+b、行位置0,d,2d | [K0481](research/knowledge/items/K0481-three-row-q4-all-spacing-first-moves.md) · proved | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; 全正整数a,b,d・全安全局面（8種類の禁止集合型へ帰着） | mathematical-proof, exhaustive-enumeration, independent-enumeration | 126組の行列式の全称符号分類と8種類の9-bit mex完全再帰; 4096盤の整数行列式による独立4点組照合; 空盤g=1、9通りの初手後g=0 |
| 5×m・q=9; 標準整数格子・q=9,w=5・完全指摘・通常プレイ | [K0484](research/knowledge/items/K0484-width-five-q9-all-lengths.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1・全安全局面 | mathematical-proof, independent-enumeration | 五連続行の平方剰余mod9による全称証明; m=4,5,7,9,12,14の全非共線三点から整数行列式で円を再生成; g=(5min(m,8)−\|S\|) mod2。m≥8は後手勝ち。M_{5,9}=8 |
| n×n×n・3次元q=5・偶数n≥4; 5点共平面または共球面禁止・完全指摘・通常プレイ | [K0502](research/knowledge/items/K0502-even-cubes-q5-constructive-weak-solution.md) · proved | weak; second-player-win | root, first-moves; 全偶数n≥4・全初手n³個への合法な必勝応手 | mathematical-proof, independent-enumeration | τ(x,y,z)=(n−1−x,y,z)による構成的戦略証明; 4×4×4の529対称安全局面と2048合法応手を余因子法と直接行列式の別実装で照合; 4×4×4、6×6×6以降の全偶数辺長。奇数辺長はこの定理の対象外 |
| 5×5×5・3次元q=5; 5点共平面または共球面禁止・完全指摘・通常プレイ | [K0503](research/knowledge/items/K0503-five-cube-q5-certified-weak-solution.md) · computed | weak; second-player-win | root, first-moves; 空盤・125/125初手（10軌道）への必勝応手 | exact-search, ranked-and-or-certificate, independent-cpp-check | empty-5.cert.gz・1368687局面・1655414関係・最大12石; Bareiss 5×5整数行列式で合法手・全P境界・N証人・全収録局面の到達性を確認; 全初手後は次手番側N。任意の非収録局面・全Grundy・7以上の奇数辺長は対象外 |
| n×n×n・3次元q=5・奇数n≥7; 5点共平面または共球面禁止・完全指摘・通常プレイ | [K0505](research/knowledge/items/K0505-odd-cubes-q5-weak-frontier.md) · open | unsolved; unknown | root; 7立方{0,5}の残り35第三手を19軌道化。各25万df-pn展開でも全てUNKNOWN | exact-search | 根はUNKNOWNで勝敗証明書なし。K0506の有限部分証明は別に独立検査済み; K0506の6石N・7石P・17石および18石終端を独立検査。標本幾何・既知3立方の回帰も確認。空盤証明ではない; 5立方のK0503および全偶数辺長のK0502から奇数n≥7の勝敗は従わない |
| 2×2×2・共面4点禁止; 立方体の8頂点、4点共面のみ禁止、通常・misère別々 | [K0526](research/knowledge/items/K0526-cube-coplanar-four-all-safe.md) · proved | strong; second-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; 全159安全局面（通常版とmisère補助mex） | exhaustive-enumeration, independent-enumeration | 256全ビット集合の有限完全列挙; 排他的論理和による幾何と直接整数行列式の独立一致; 両版とも空盤後手勝ち。通常g(空)=0、全一石g=2。K=5、s=4 |
| 2×2×m・4点共面禁止; m≥3は通常先手勝ち・misère後手勝ち、m=2はK0526参照 | [K0527](research/knowledge/items/K0527-coplanar-prism-all-length-strong-solution.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; m≥3の全安全局面、m=1,2は別途境界分類 | mathematical-proof, exhaustive-enumeration, independent-enumeration | 幾何学的な全称証明とm=1〜12の完全列挙; C++の直接4×4整数行列式とPython外積判定が一致; m≥3ではK=5,s=3、全局面g=(5-\|S\|) mod 2、misère補助値h=1-g |
| 3×3×3・4点共面禁止; 3次元共面4点のみ禁止、退化を含む、m=3 | [K0529](research/knowledge/items/K0529-coplanar-three-by-three-prism-capacity-and-cube-grundy.md) · proved | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; 全72,204安全局面の通常Grundyとmisère補助mex | mathematical-proof, exhaustive-enumeration, independent-enumeration | 全2^27部分集合を安全集合の昇順生成で網羅し72,204局面を完全再帰; Pythonの4×4行列式展開とC++の外積式が全局面のg/h分布まで一致; g(空)=2、h(空)=1、通常は中央以外26初手勝ち、misèreは全27初手勝ち。全mのK=3,6,8,8,9（m≥5は9）、s=3 |
| 2×3×3・4点共面禁止; 通常は先手勝ち、misèreは後手勝ち。一般の2×k×mの空盤勝敗は未解決 | [K0530](research/knowledge/items/K0530-two-layer-coplanar-capacity-and-233-strong.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy, safe-layers; 2×3×3の全6456安全局面。全k,mのK,s,三石極大数は数学的証明 | mathematical-proof, exhaustive-enumeration, independent-enumeration | 全k,mの容量・三石極大数の初等証明と2×3×3の全2^18部分集合検査; Python外積とC++4×4行列式展開で4盤の全局面集計が一致; k,m≥3はK=6,s=3。2×3×3ではg(空)=1,h(空)=0、通常勝ち初手8個 |
| λ=0・鉛直w列・各列M_w候補以上; det[x²,x,y,1]=0の四点禁止、各列M_w点以上、M_w=max(3,1+(w−2)(w−3)(w+2)/6) | [K0533](research/knowledge/items/K0533-degenerate-quadratic-strips-sharp-uniform-grundy-threshold.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全w≥3・全安全局面 | mathematical-proof | 補間数による終局分類と全局面mex閉公式。閾値下界は任意幅の整数構成; 条件内3384859局面の二方式個別SG照合、条件外例も別に保存; 偶数wは空盤先手勝ち、奇数wは後手勝ち。全局面g≤2 |
| λ=0・標準鉛直5列×m候補・m≥6; det[x²,x,y,1]=0の四点禁止、x=0..4、y=0..m−1 | [K0535](research/knowledge/items/K0535-degenerate-quadratic-five-column-exact-stabilization.md) · proved | strong; second-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥6・全安全局面 | mathematical-proof, exhaustive-enumeration | m≥8の一般証明とm=6,7の有限完全基底。m=5は明示反例; 高さ6,7の計531060局面で二方式mexと閉公式が個別一致; 全局面g≤2、真の公式安定化高さ6。全初手が負け手 |
| 多項式持ち上げ行列式版・各列3候補以上; q=d+2、det[x^d,x^(d−1),...,x,y,1]=0を禁止、退化を含む | [K0538](research/knowledge/items/K0538-polynomial-lift-degree-parity-constructive-outcomes.md) · proved | weak; conditional | root, first-moves; 全d≥3・総点数N≥d+1の対象盤の空盤と全初手 | mathematical-proof | 同列三点を先手5手目・後手4手目までに完成し終局をd+1石へ固定する戦略; 9有限盤の二方式行列式・全局面mex。無界性は別途数学的証明; 偶数dは全初手勝ち、奇数dは全初手負け。全安全局面の強解決ではない |
| 任意三平行線・各線18候補以上; q=6の共円または共線禁止、完全指摘、通常プレイ | [K0539](research/knowledge/items/K0539-three-arbitrary-parallel-lines-q6-eighteen-sites.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 任意の実数位置の対象有限盤の全安全局面 | mathematical-proof, independent-cpp-check | K0478のE14障害の全称排除、連続156有理式および固定4823四円組; SymPy生成証明書を標準ライブラリで再計算、固定型はPythonと独立C++が全件一致; g(S)=(15−\|S\|) mod2。空盤先手勝ち・全初手勝ち。18の最小性は未主張 |
| 2×k×m・4点共面禁止; 通常先手勝ちは薄い非正方断面または3×3断面。misère先手勝ちは1×1断面または3×3以外の両辺3以上 | [K0540](research/knowledge/items/K0540-coplanar-two-layer-all-openings.md) · proved | weak; conditional | root, first-moves; 全正整数k,mの空盤と全2km初手について通常Grundy・misère補助値を分類 | mathematical-proof, exhaustive-enumeration, independent-enumeration | K0527・K0530の無界定理と有限境界6盤の完全mex列挙、2×2例外の完全列挙; 原始方向集合方式と直接整数行列式方式で7盤の全初手値分布まで一致; 3×3断面のみ通常初手の値が三種類(0,2,3)に分かれる。2×2断面は両ルール後手勝ち |
| 任意三平行線・各線17候補以上; q=6の共円または共線禁止、完全指摘、通常プレイ | [K0541](research/knowledge/items/K0541-three-arbitrary-parallel-lines-q6-seventeen-sites.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 任意の実数位置の対象有限盤の全安全局面 | mathematical-proof, independent-cpp-check | E13以上での一点三円上界、E12以下の円予算から不足線の利用不能点を16以下へ抑える; 旧Pythonと独立C++の全記号候補・有理候補の再実行一致。全称帰着も別途論理監査; 全終局15石、g(S)=(15−\|S\|) mod2。空盤先手勝ち・全初手勝ち。17の最小性は未主張 |
| 2×2×2×2・5点共超平面禁止; 四次元二値立方体・5点が同一アフィン超平面にあると禁止 | [K0545](research/knowledge/items/K0545-four-cube-hyperplane-strong-and-binary-rectangles.md) · proved | strong; second-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; 全6613安全局面、通常・misère | mathematical-proof, exhaustive-enumeration, independent-enumeration | 全5点組4368個・全65536部分集合の二方式完全列挙と偶奇帰納; Pythonの4×4直接行列式、C++のGram行列式・別方式安全判定で一致; 通常版後手必勝、misère版先手必勝。全局面g(S)=\|S\| mod2、h(S)=1-g(S) |
| 2×2×2×2×2・6点共超平面禁止; 五次元二値立方体の6点が一つのアフィン超平面に入ると禁止、退化含む | [K0546](research/knowledge/items/K0546-five-cube-hyperplane-strong-and-general-lower-bound.md) · proved | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy, safe-layers; 全1108073安全局面・通常版とmisère版・全32初手 | mathematical-proof, exhaustive-enumeration, independent-enumeration | 全906192個の6点組と全8石候補を二方式で完全検査; 5×5整数Bareiss行列式と6×6増補行列mod1009、増分列挙と直接組合せ列挙で一致; K=7、s=5。通常先手必勝・全32初手勝ち、misère後手必勝。全局面で0↔1交換則成立 |
| x={0,1,(1±√13)/2}、整数高さ0..m−1の三線q6帯; q6共円共線禁止、通常プレイ | [K0547](research/knowledge/items/K0547-sqrt13-three-line-q6-sharp-stabilization-seven.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1。m6は有限全局面DP、その他は閉形式 | mathematical-proof, independent-cpp-check | m≤4は3m石、m5は14石、m≥7は15石の固定終局。m6は二方式の全安全局面点別一致; Q(α)の直接六点判定と二方式mex。m6の243324局面を全照合、全初手の子SG0; P長はm2,4,5のみ、他長は全初手勝ち。m6ではSG最大3のため全局面偶奇式を用いない |
| 無理数間隔比・有理数高さの三平行線、各線13候補以上; q=6共円または共線禁止、通常プレイ、全候補高さが共通座標で有理数 | [K0548](research/knowledge/items/K0548-irrational-spacing-rational-heights-q6-thirteen-sites.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 条件を満たす有限盤の全安全局面 | mathematical-proof | 差の円方程式から弦積差一定、非零同積弦は高々二組、利用不能点は12以下; 数学的証明。特定二次無理数帯の直接二次体監査はK0549; 全終局15石、g(S)=(15−\|S\|) mod2、空盤先手勝ち・全初手勝ち。13の最小性は未主張 |
| x={0,1,(1±√17)/2}、整数高さ0..m−1の三線q6帯; 共円または共線の6石禁止、通常プレイ、α²−α−4=0 | [K0549](research/knowledge/items/K0549-quadratic-irrational-three-line-q6-all-length-strong-solution.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 全m≥1の全安全局面 | mathematical-proof, independent-cpp-check | 六点円は二線の高さt,t+5とα線のt+1,t+4だけ、全円数max(0,m−5)から満容量を証明; 厳密Q(α)行列式による全六点組と二方式の全安全局面mex、有限範囲を明示; T=3min(m,5)、g(S)=(T−\|S\|) mod2。Pはm2,4のみ、他の全長は先手勝ち・全初手勝ち |
| x={0,1,α}、α²−α−c=0、c=1または素数p≥5または素数平方p²; 整数高さ0..m−1、q6共円共線禁止、通常プレイ | [K0550](research/knowledge/items/K0550-prime-quadratic-irrational-q6-strips-all-length-family.md) · proved | strong; conditional | root, first-moves, all-safe-win-loss, all-safe-grundy; 上記の全cと全m≥1の全安全局面 | mathematical-proof, independent-cpp-check | 非退化因子対は高々一つ、円の幅は5以上、全円数はmax(0,m−5)以下; c1,4,5,7,9,11の厳密二次体・二方式mex。無限族と無界長は別途数学的証明; T=3min(m,5)、g(S)=(T−\|S\|) mod2。Pはm2,4のみ、安定化開始値は5 |
| 3×3×4・4点共面禁止; 3次元共面4点のみ禁止、退化を含む、3×3×4 | [K0569](research/knowledge/items/K0569-coplanar-3x3x4-strong-solution.md) · computed | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; 全525,595安全局面の通常Grundyとmisère補助mex | exhaustive-enumeration, independent-enumeration | 安全集合の昇順全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙; PythonのLeibniz行列式列挙とC++の外積行列式DFSが、禁止組数・層別局面数・層別終局数・g/h分布・全36初手の値まで一致; g(空)=3、h(空)=3。通常の勝ち初手は端面中央（1,1,0）と（1,1,3）の2点のみ。8石最大配置1,028個はD4×Z2で65軌道 |
| 3×3×5・4点共面禁止; 3次元共面4点のみ禁止、退化を含む、3×3×5 | [K0570](research/knowledge/items/K0570-coplanar-3x3x5-strong-solution.md) · computed | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; 全2,588,710安全局面の通常Grundyとmisère補助mex | exhaustive-enumeration, independent-enumeration | 安全集合の昇順全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙; PythonのLeibniz行列式列挙とC++の外積行列式DFSが、禁止組数・層別局面数・層別終局数・g/h分布・全45初手の値まで一致; g(空)=1、h(空)=2。全45初手とも子のgが0で全て勝ち手。misèreで子のhが0になるのは中央列（1,1,z）の5点のみ。9石最大配置304個はD4×Z2で19軌道（全てサイズ16） |
| 3×3×6・4点共面禁止; 3次元共面4点のみ禁止、退化を含む、3×3×6 | [K0571](research/knowledge/items/K0571-coplanar-3x3x6-strong-solution.md) · computed | strong; first-player-win | root, first-moves, all-safe-win-loss, all-safe-grundy; 全10,447,786安全局面の通常Grundyとmisère補助mex | exhaustive-enumeration, independent-enumeration | 安全集合の昇順全生成による階層mex。証明書ファイル形式ではなく再生成可能な列挙; PythonのLeibniz行列式列挙とC++の外積行列式DFSが、禁止組数・層別局面数・層別終局数・g/h分布・全54初手の値まで一致; g(空)=1、h(空)=2。全54初手とも子のgが0で全て勝ち手。misèreで子のhが0になるのは中央列（1,1,z）の6点のみ。全局面の最大nimberは7（g=7は8局面のみ）。9石最大配置5,376個はD4×Z2で338軌道 |
<!-- END GENERATED SOLUTION STATUS -->

## 読み方

- 現在の研究結果と未解決問題：[knowledgeの入口](research/knowledge/README.md)、[全K項目](research/knowledge/generated/index.md)、[検証境界・警告](research/knowledge/generated/summary.md)。
- ルール・使い方・証明方式：[reader向け文書](docs/README.md)。
- 再現コード・入力・出力・監査：[実験の入口](research/experiments/README.md)。
- 発見順・判断・失敗：[研究ログ](research/log/README.md)。旧計画・撤回済みまとめ・当時の索引：[archive](research/archive/README.md)。
- 構造整理の履歴とprovenance：[MIGRATION](research/MIGRATION.md)。

## リポジトリ構成

```text
research/
  knowledge/       現在知識の正本items、生成ビュー、schema、語彙、template
  experiments/     再現可能な実験単位：scripts、input/output、report、hash
  log/             研究の時系列、発見・失敗・引き継ぎ
  archive/         歴史的資料、旧索引、移行時のpath対応表
  README.md        研究全体の恒久的な入口
  MIGRATION.md     移行履歴
docs/             現在有効なreader向け説明
results/          公開・横断集計のmachine-readable outputs
certificates/     証明書の案内・公開資産
tools/knowledge/  knowledge検査・生成と参照検査
cpp/              共通C++ solver・証明書生成器・検査器
scripts/          共通再現runner・監査・共有研究ライブラリ
rust/             独立verifier
Kyouen/           Leanのルール・証明書健全性定理
```

実験固有の小さな出力は各experimentのoutputに置き、横断集計をresultsに置きます。
巨大証明書の圧縮配布とhashは[release-assets](release-assets/README.md)を参照してください。

## ビルドと検査

repo rootで実行します。

```sh
uv sync --locked
uv run --locked python tools/knowledge/check.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
uv run --locked python tools/knowledge/build.py
git diff --exit-code -- README.md research/knowledge/generated
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel 2
lake build
```

C++検査器の使用方法は[reproducibility guide](docs/REPRODUCIBILITY.md)、
証明書形式は[順位付きAND/OR形式](docs/CERTIFICATE_FORMAT.md)と[KYOENC4](docs/KYOENC4.md)、
検証の信頼境界は[証明方式の説明](docs/PROOF_STATUS.md)を参照してください。
CIは小盤証明書、固定幅・幾何・ゲーム構造・飽和配置の既存回帰検査、Lean、knowledge integrityを検査します。

## English

Research on Kyouen covers square-board optimal play, fixed-width q-point games, misère play, safe configurations and lattice geometry.
The canonical current knowledge is in research/knowledge/items; experiments, chronological logs and historical archives have separate physical homes.
