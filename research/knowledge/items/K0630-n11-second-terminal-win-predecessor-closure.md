---
id: K0630
title: 11×11の第二終局WIN証明から後退閉包で256,561生局面を帰納証明
kind: computation
status: computed
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 完全指摘・通常プレイの合法手と手番
- type: depends_on
  target: K0003
  note: 局所証明と空盤勝敗の区別
- type: depends_on
  target: K0628
  note: 第二の固定終局戦略と独立終局検証
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/terminal_s6_60_strategy.b64
  role: certificate
  note: 出発点の終局戦略、復号14,440バイト・SHA-256 debb5464282eb28e6a30496f8728515433d6f9507ffdeeda1eeaf04e3c5d7de4
- path: research/experiments/n11-central-19-cover-20261031/verify_terminal_s6_60_closure.cpp
  role: verifier
  note: 独立4×4整数行列式による終局再生と勝敗帰納閉包・D4計数
- path: research/experiments/n11-central-19-cover-20261031/verify_terminal_s6_60_closure.py
  role: verifier
  note: 固定SHA検査・一時復号・C++検査実行・期待件数照合
- path: research/log/2026-11-02-n11-central49-second-terminal-win-closure-256561.md
  role: log
  note: 層ごとの証明再利用と限界の記録
scope: 標準11×11完全指摘・通常プレイ。K0628の第二六石終局戦略から、既知WIN局面の一点除去と手番別の帰納規則で到達できる局所的な元先手WIN閉包。生局面とD4正準類を区別する。
evidence: 固定終局証明22,364局面を独立整数幾何で再生し、勝敗帰納規則を8反復して256,561生局面・256,193正準類を計数。手元で再現し、専用GitHub Actions 41382200963でも独立検査成功。
---

# 終局戦略を再利用した局所的な勝ち局面の拡大

元先手WINが確定した局面集合から、元先手番なら一つでもWIN子がある局面を、相手番ならすべての合法子がWINである局面を追加する。後者は相手に合法手がない終局を含む。既知の勝ち局面から一点を取り除いて候補を生成し、この規則を反復するので、追加される局面のWINは帰納的に証明される。

K0628の固定終局戦略が訪問する22,364生局面を出発点として、**234,197生局面を新たに証明**し、合計**256,561生局面**（D4正準化後**256,193類**）に達した。追加数は83,556、19,589、99,467、7,567、22,511、291、1,216、0の順で、8回目に候補集合の閉包が安定した。

六石生局面は6個増えたが、これはK0628で既に証明した七石共有親の6個であり、**新しい六石正準類の勝敗判定ではない**。七石生局面の追加は0。証明対象の大部分は深い中間局面であり、既存勝敗cacheへの統合や探索時間短縮率は未測定。

この計数は独立C++の4×4整数行列式による全合法手の再計算、固定SHAの証明書検査、各反復件数の照合で再現可能。二石rootと11×11空盤の勝敗は引き続き**UNKNOWN**。


## 2026-11-02追補：対称性を帰納の途中で共有すると551正準類増える

上記の256,561生局面・256,193正準類は、**生局面のまま帰納を完了してからD4正準化**した数である。証明済み集合を先にD4正準化し、各候補の全合法子も正準化して照合すると、同じ固定終局戦略から**256,744正準WIN類**まで帰納できる。これは元の256,193正準類を実際に集合として包含し、**551正準類の厳密な増分**を持つ。

追加551類の石数別内訳は、10石38、11石6、12石156、13石20、14石285、15石46。6〜9石と16〜19石の追加は0類で、六石7類・七石1類という既存の局所証明範囲は増えていない。

新しい検証器 `research/experiments/n11-central-19-cover-20261031/verify_terminal_s6_60_d4_quotient.cpp` は、元の14,440バイトの終局戦略を独立整数幾何で再生したうえで、石数19→6の降順帰納を行う。さらに生局面側の帰納閉包を別に再構成し、256,561生局面→256,193正準類と、今回の256,744正準類の**集合としての包含**を照合する。固定SHA・層別件数・改変検出は同ディレクトリの `verify_terminal_s6_60_d4_quotient.py` が監査する。詳細は `research/log/2026-11-02-n11-second-terminal-d4-quotient-ranked-closure-256744.md`。

この551類はすべて元先手WINの**局所証明**であり、未確定S5のLOSS判定や中央49の2,207七石条件付き計画の成立を意味しない。二石rootと11×11空盤は引き続き**UNKNOWN**。
