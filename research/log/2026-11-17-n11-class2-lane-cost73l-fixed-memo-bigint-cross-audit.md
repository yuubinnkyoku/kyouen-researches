# 2026-11-17 n11 class2-lane: cost73l fixed-memo battery × BigInt証明書再検証の横断監査

## Context

cost73lの32本について、第三実装BigInt verifierによる独立再検証（32/32 PASS）が公開された。同じ32本に対して、K0907のfixB memo修正batteryも、出版済み証明書とのbyte同一（32/32）を報告している。

両者は別々の監査だが、同じ32 rootを対象にしている。per-bitのroot・行数・hash・mobility・終端範囲を三つの公開結果の間で照合し、性能修正の結果と独立証明書検証の対象が本当に同じ集合かを確認した。

## Method

新しいスクリプト `audit_cost73l_fixed_memo_bigint_cross_20261117.py` は、次の3ファイルをGit blob SHAで固定して読む。

- fixed-memo battery: `963dccc777340974981eb3799e753657b3743e53`
- certificate manifest: `6e0a94aba212ba54bb5329fbea4643c9dcdb1ec4`
- BigInt independent re-verification: `547fe617abc179ff47f3607079d3ca8c1de4359b`

各bitについて、battery↔manifest↔BigInt結果の行数、MD5、SHA-256、root、mobility、終端石数範囲、verifier status、union missing/extra、byte-identicalを照合した。加えてper-bit値から総節点数・戦略行数・BigInt訪問状態・終端数・敗者応手辺数を再集計した。

この監査は公開済みJSONの相互整合を調べるものであり、BigInt verifierの再実行や61MBの証明書本文の再読込ではない。

## Results

- 対象bit集合: battery / manifest / BigInt結果の32件が一致
- per-bit cross-agreement: **不一致0**
- fixB nodes: **52,079,030**（per-bit再合計と記録値一致）
- 出版verbatim ms23 nodes: **424,657,112**（per-bit再合計・manifest総数一致）
- fixB/verbatim比: **0.122637837748**（節点削減87.736%、約8.154倍）
- 証明書戦略行: **1,693,203**（battery / manifest / BigIntの三者一致）
- byte-identical: **32/32**
- BigInt verifier: **32/32 PASS**
- BigInt訪問状態: 3,599,832
- 終端状態: 613,366
- 敗者応手辺: 3,178,030
- 最良のper-bit比: bit25 = 0.0981
- 最大のper-bit比: bit119 = 0.1587

8個の集計gateはすべてPASS。

## Interpretation

今回の横断監査により、fixBの性能測定が対象にした32本と、BigIntで独立検証された32本が、per-bitの識別子だけでなく証明書hash・戦略行数・root mobility・終端範囲まで一致することを確認した。

したがって、cost73lでは「memo修正で探索節点を大幅に減らしても、出版済み証明書bytesは変わらない」という既存batteryの結果と、「その出版bytesがBigInt verifierを通る」という独立検証結果が、同じ32本に対して接続された。これは今後の新規証明書抽出でfixBを使う判断材料になる。ただしrepo-verbatim extractorの歴史的決定性記録は変更せず、修正版の採用自体もこの監査では行わない。

本監査は既存の証明書を新しく増やさず、manifestの行も閉じない。WIN7-D10は個別7石rootの深さ10以内の先手勝ちであり、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続きUNKNOWN。

## Artifacts

- Script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost73l_fixed_memo_bigint_cross_20261117.py`
- Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost73l-fixed-memo-bigint-cross-audit-20261117.json`

mainへ直接反映。branch / PRなし。
