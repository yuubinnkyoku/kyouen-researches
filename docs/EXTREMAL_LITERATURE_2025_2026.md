# 共円・共線4点回避：2025〜2026年の外部研究と計算記録

最終資料確認日：**2026-11-13**。文献の書誌事項は論文の原文、学術誌掲載情報、発表元の公開資料を照合した。以下は**外部研究の整理**であり、本リポジトリが個々の外部論文の全証明や公開座標を独立検証したとの主張ではない。引用は本文中の [R1]〜[R8] と末尾の参考文献を対応させる。再利用可能な [BibTeX書誌データ](EXTREMAL_LITERATURE_2025_2026.bib) も添付した。

## 1. 対象の一致・不一致

本リポジトリの最大安全配置数 `K_n`（`README.md` の定義）と、Erdős–Purdy の no-four-on-a-circle 関数 `f_circ(n)` は、いずれも
`[n]^2` から「**どの4点も同一円周上・同一直線上にない**」ように選べる最大点数を表す。したがって、この条件で得られた構成は `K_n` の**下界**になる。ただし、単なる4点共円禁止（共線を許容）や等脚台形のみ禁止の数値は同一問題ではない [R3, R5]。

極値配置の最大点数と、石を交互に置く**2人ゲームの必勝判定**も異なる。たとえば `K_9=18` の事実それ自体から、9×9空盤の勝敗は決定できない。2人ゲーム側の解決範囲は [`README.md`](../README.md) と [`docs/RELATED_WORK.md`](RELATED_WORK.md) を参照する。

## 2. 漸近理論の進展

- **Dong–Xu（2025）[R1]**：射影代数幾何の発想による構成で、平面の場合 `K_n ≥ n − o(n)` を示した。さらに `d` 次元の `[n]^d` で、同一球面または超平面上に `d+2` 点がない `n−o(n)` 点の構成を与える。1995年の Thiele による `n/4` 型下界からの大きな改善。
- **Ghosal–Goenka–Keevash（2025年公開、2026年学術誌掲載）[R2]**：共円・共線の禁止四点組数の漸近評価と確率的削除法により、十分大きな `n` で `K_n ≥ 7n/12` を証明（Corollary 1.4）。この定数は [R1] の `n-o(n)` より弱いが、**独立した確率的手法**と共円四点組の評価が重要である。論文は *Discrete & Computational Geometry* 76巻1886–1911頁（2026年）に掲載された。
- **Ghosal–Goenka–Grebennikov–Keevash–Kwan–Pham（2026）[R3]**：Theorem 1.5 は任意の `η>0` に対し、十分大きな `n` で `K_n ≥ (2−η)n` を与える。すなわち **`K_n ≥ 2n−o(n)`**。擬ランダムな超グラフ・マッチングと削除の議論を利用する。同論文はさらに `(2+λ)n` への改善可能性を**予想・示唆**するが、これは証明済み定理ではない。
- **Ghosal–Goenka（2026）[R4]**：Theorem 1.1 は、単一の無限集合 `S ⊆ ℤ²` で共円・共線4点を避け、ある `c>0` と `n₀` に対して、**すべての `n≥n₀` で `|S∩[n]²| ≥ cn`** を満たすことを証明した。各 `n` ごとに独立に配置を作る通常の `K_n` 下界とは**量化が異なる**。

[R3, R4] の導入に従えば、既知上界は Thiele による `K_n ≤ (5n−3)/2`。2026年11月13日に確認した漸近保証は
`2−o(1) ≤ K_n/n ≤ 5/2−3/(2n)` である。比 `K_n/n` の極限の**存在**や正確な値が決着したわけではない。

本リポジトリ [`K0143`](../research/knowledge/items/K0143-asymptotic-two-n-safe-construction-open.md) の「**明示的な**無限構成で `2n−O(1)` を達成できるか」は、[R3] の漸近的**存在**定理より強い要求であり、未解決のままでよい。

## 3. 有限盤面の探索結果：問題条件と証拠を分ける

### 3.1 AlphaEvolve と代理問題

[R3] の Appendix B は、Google DeepMind の AlphaEvolve を使って `1≤n≤30` の配置下界を報告し、実際の点集合を付属ファイルとして配布している。同付録では二つの異なる量を扱う。

- `f_circ(n)`：**共円4点と共線4点をともに禁止**。標準の `K_n` と一致。
- `f_IT(n)`：**等脚台形4点と共線4点を禁止**。共円4点一般の禁止とは異なる**代理問題**で、`f_IT(n)` の値をそのまま `K_n` の下界とはできない。

Appendix B の `f_circ(n)` の値は**達成した下界**であって、一般に最大値の決定ではない。たとえば `n=30` の下界は55点 [R3]。

### 3.2 Geometry-Aware MCTS

Zhang–Zhuang–Wang–Kaplan [R5] は、幾何条件に従った合法候補の差分更新、対称性による枝刈りなどを組み込んだモンテカルロ木探索を報告している。論文の Max-No-4-on-Circle は**有限半径の円周上の4点だけを禁止し、4点共線を禁止しない**（原論文の問題定義）。`39×39` で69点という例もこの条件下の構成である。したがって**標準共円 `K_{39}≥69` の証拠にしてはならない**。

論文は *Transactions on Machine Learning Research*（2026年）掲載として著者らの公式実装が書誌情報を公開している [R5]。手法の転用可能性と、標準ルールの記録認定は分離する。

### 3.3 IRSIの2026年10月の外部記録

Institute for Recursive Self Improvement（IRSI）[R6] は、共円・共線4点をともに禁止する**標準条件**について、中心対称配置を含むタブー探索による以下の構成を公表した。

| n | AlphaEvolve の `K_n` 下界 [R3] | IRSI の `K_n` 下界 [R6] | 差 |
|---:|---:|---:|---:|
| 19 | 36 | **37** | +1 |
| 23 | 44 | **45** | +1 |
| 24 | 45 | **46** | +1 |
| 25 | 47 | **48** | +1 |
| 26 | 49 | **50** | +1 |
| 27 | 50 | **51** | +1 |
| 30 | 55 | **56** | +1 |

これは各 `n` の**存在下界**であって、上界まで確定した「厳密な最大値」ではない。IRSIは2026-10-01および10-02の日付で整数演算の証明書と、独立に書かれた複数の検証器による受理を報告しているが、**査読前**であり、**本リポジトリ側での証明書の再実行・全座標独立検査は未実施**である [R6]。

- 原記録：<https://irsi.ai/records.html#no-four-on-a-circle>（節見出し「Larger grid sets with no four points on a circle or line」）
- 検証方法の一例：2026-10-01配布物の `no-four-on-a-circle` 内で `python3 check.py circ_n30_k56.json`、または独立検証器 `python3 recheck_circ.py circ_n30_k56.json 56`。
- 配布物 SHA-256（同サイトの宣言値、当repoでは未照合）：`irsi-certificates-2026-10-01.zip` = `f89d9255e75860d4a9d08ab2b96ac8b891a02bf53340171c9320563a2afe3a6d`。`2026-10-02.zip` および `2026-10-02b.zip` は [R6] の公式記録参照。

**取り込みの次段階**は、配布物のSHA-256、点集合の座標範囲、全4点組の整数行列式 `det[x,y,x²+y²,1]`、既存実装との照合を独立に実行してから、新しい「当repoで検証済み」の主張として記録することである。現段階では**文献確認済み／配置独立検証は未実施**に留める。

## 4. 2人ゲーム・計算量の先行研究との接続

- GPCCの**公式問題**は9×9の共円を題材とする。公式ページには2026-09-28追記として `yuubinnkyoku` の解答が登録され、解答詳細には**2026-09-26提出**とある [R7]。解答本文は1×1〜10×10の勝敗と検証範囲を記録する。9×9の全局面を強解決したという意味ではない。
- 山本一揮・平原秀一による、**配置禁止マスを追加した変種**のPSPACE完全性研究は、[`RELATED_WORK.md`](RELATED_WORK.md) §3.3 の学会発表資料に記録されている。元の正方形全格子空盤にそのまま移せない。
- 当repoの [`K0438`](../research/knowledge/items/K0438-finite-point-kayles-pspace-complete.md) は**任意有限整数点盤と指定安全占有集合**を入力とする別のPSPACE完全性定理。こちらも「正方形全格子・空盤」の完全性を証明しない。一般のNode Kaylesの計算量については Schaefer [R8] を基礎文献とする。

## 5. 参考文献（著者・年・正式題名・掲載先・恒久識別子）

[R1] Dong, Z., & Xu, Z. (2025). *Large grid subsets without many cospherical points*. arXiv:2506.18113 [math.CO]. <https://doi.org/10.48550/arXiv.2506.18113> （[原文](https://arxiv.org/abs/2506.18113)）

[R2] Ghosal, A., Goenka, R., & Keevash, P. (2026). On subsets of lattice cubes avoiding affine and spherical degeneracies. *Discrete & Computational Geometry, 76*, 1886–1911. <https://doi.org/10.1007/s00454-026-00853-7> （[2025年公開の原稿](https://arxiv.org/abs/2509.06935)、Corollary 1.4）

[R3] Ghosal, A., Goenka, R., Grebennikov, A., Keevash, P., Kwan, M., & Pham, H. T. (2026). *No-$(k+1)$-in-line problem for $k\geqslant 3$*. arXiv:2607.05255 [math.CO]. <https://doi.org/10.48550/arXiv.2607.05255> （[本文・付録B](https://arxiv.org/html/2607.05255v1)、Theorem 1.5）

[R4] Ghosal, A., & Goenka, R. (2026). *The extensible no-four-on-a-circle problem*. arXiv:2609.20447 [math.CO]. <https://doi.org/10.48550/arXiv.2609.20447> （[本文](https://arxiv.org/abs/2609.20447)、Theorem 1.1）

[R5] Zhang, L., Zhuang, X., Wang, T., & Kaplan, N. (2026). Geometry-Aware MCTS for Extremal Problems in Combinatorial Geometry. *Transactions on Machine Learning Research*. [掲載ページ](https://openreview.net/forum?id=xtlbkvz6qb)；[arXiv:2606.26399](https://arxiv.org/abs/2606.26399)；[著者らの公式実装（掲載誌表記・引用例）](https://github.com/luoninz1/Geometry-Aware-MCTS)。

[R6] Institute for Recursive Self Improvement. (2026, October 1–2). *Larger grid sets with no four points on a circle or line: n = 19, 23, 24, 25, 26, 27, 30* [オンライン研究記録・整数検証用ファイル、未査読]. <https://irsi.ai/records.html> （2026-11-13閲覧）

[R7] GPCC（プログラミング・シンポジウム分科会）. (2026). *GPCC2026問題「共円」*（9月28日追記）. <https://prosym.org/gpcc/gpcc26.htm>；同「*共円（きょうえん）の解答*」（9月26日提出）. <https://prosym.org/gpcc/26p1.htm> （2026-11-13閲覧）

[R8] Schaefer, T. J. (1978). On the complexity of some two-person perfect-information games. *Journal of Computer and System Sciences, 16*(2), 185–225. <https://doi.org/10.1016/0022-0000(78)90045-4>.

---

**引用・再利用時の注意**：本文の「原論文の定理」「査読済み論文」「原論文付属の計算」「未査読の外部証明書」「当repo独立検証」を混同しない。掲載先が明示されていないプレプリントに学術誌名を付加しない。数値構成は最大値の上界・最適性証明ではない。
