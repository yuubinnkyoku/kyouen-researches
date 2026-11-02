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
evidence: 固定終局証明22,364局面を独立整数幾何で再生し、勝敗帰納規則を8反復して256,561生局面・256,193正準類を計数。手元で再現、専用CIは完了確認待ち。
---

# 終局戦略を再利用した局所的な勝ち局面の拡大

元先手WINが確定した局面集合から、元先手番なら一つでもWIN子がある局面を、相手番ならすべての合法子がWINである局面を追加する。後者は相手に合法手がない終局を含む。既知の勝ち局面から一点を取り除いて候補を生成し、この規則を反復するので、追加される局面のWINは帰納的に証明される。

K0628の固定終局戦略が訪問する22,364生局面を出発点として、**234,197生局面を新たに証明**し、合計**256,561生局面**（D4正準化後**256,193類**）に達した。追加数は83,556、19,589、99,467、7,567、22,511、291、1,216、0の順で、8回目に候補集合の閉包が安定した。

六石生局面は6個増えたが、これはK0628で既に証明した七石共有親の6個であり、**新しい六石正準類の勝敗判定ではない**。七石生局面の追加は0。証明対象の大部分は深い中間局面であり、既存勝敗cacheへの統合や探索時間短縮率は未測定。

この計数は独立C++の4×4整数行列式による全合法手の再計算、固定SHAの証明書検査、各反復件数の照合で再現可能。二石rootと11×11空盤の勝敗は引き続き**UNKNOWN**。
