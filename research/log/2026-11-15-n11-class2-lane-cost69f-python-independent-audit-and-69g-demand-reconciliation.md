# n11 class2: cost69f全9証明書のPython第三完全独立監査とcost69g demand不整合の解消

2026-11-15 JST。最新main（K0783、cost69f 9件統合記録・split 8 part、receipt fold、並走の第二独立検証
`cost69f-second-independent-verification-20261115.json`、cost69g/cost65jのinflight claim）を確認した上で、
本レーンは探索を重ねず2つの検証・整理作業を行った。

## 成果1: 全9証明書のPython第三完全独立監査 — 9/9 PASS

第二独立検証（別V8実行、BigInt 3x3余因子、未検証だった4証明書 bits 2/94/109/119）に対し、
本監査は**言語も幾何実装も異なる第三の実装（Python、整数Bareiss 4x4行列式、浮動小数点なし）で、
最初に公開された5証明書（bits 20/44/68/69/118）を含む全9件**を対象とした。
repoの検証器・engine・verdict cache・solverは一切importしていない。禁止手（三石共円トリプル）マスクも
盤面定義から再計算した。敵の全合法手を各局面で展開する完全な戦略リプレイを行い、
sub-root分解・union（missing 0 / extra 0）・終局石数13〜17・records全フィールド照合
（winner/loser states、loser reply edges、visited、terminal count、fbt_drops 0、
v15 cross-engine anchorのloss=trueとnode数）を確認した。

| bit | rows | sub-roots | visited | 終局数 | v15 anchor nodes |
|---:|---:|---:|---:|---:|---:|
| 20 | 48,171 | 56 | 106,145 | 18,015 | 8,760,558 |
| 44 | 49,220 | 55 | 106,226 | 17,381 | 12,335,445 |
| 68 | 47,977 | 58 | 101,093 | 17,736 | 6,780,201 |
| 69 | 35,501 | 51 | 82,185 | 13,431 | 6,934,812 |
| 118 | 52,480 | 54 | 117,950 | 21,162 | 9,668,618 |
| 2 | 69,879 | 58 | 142,740 | 22,921 | 16,285,738 |
| 94 | 53,449 | 56 | 120,250 | 20,161 | 15,200,842 |
| 109 | 71,485 | 60 | 153,920 | 26,397 | 13,955,169 |
| 119 | 67,423 | 61 | 143,363 | 23,779 | 13,661,829 |
| **計** | **495,585** | **509** | **1,073,872** | **180,983** | — |

bits 2/94/109/119の4件は第二検証と全フィールドで一致（行数・合法手数・visited・終局数・v15 anchor含む）。
これでcost69fの9証明書は「元のBigInt検証器 → 第二独立（V8, 4件）→ 第三独立（Python/Bareiss, 9件）」の
三重検証となった。保存照合（単一ファイル5件・2-part分割4件のbytes/md5/sha256/git blob sha、行境界分割、
連結後ハッシュのrecords一致）も全件PASS。

## 成果2: cost69g demand不整合の解消 — 両側とも誤りなし

第三方法監査 `class2-lane-next-fold-prediction-independent-audit-20261115.json` が指摘した
「measured 3 distinct open S5 parents」vs chain需要 c1=0,c2=2,c4=2（和4）の不整合は、
**需要の意味論の誤読**で両側とも正しかった。

- chainの `classes` 列はbitmask（bit0=class1, bit1=class2, bit2=class4）で、per-child需要は
  各open親S5を**class bitごとに**1回ずつ数える（`recompute_frontier_full.py` の `if bits&2: c2+=1` 等）。
- cost69g子 `00000000000000809102000000002000` のopen親は3軌道:
  `00000000000000809102000000000000`(classes=2), `00000000000000801202000000080000`(**classes=6,
  class2とclass4の二重役割**, rem 72/5,477), `00000000000000003800000000810000`(classes=4, rem 84/6,815)。
  二重役割S5がc2とc4の両方に+1するため c1=0,c2=2,c4=2（和=4）となり、distinct open parentsは3で正しい。
- 誤読の構造的原因を再発防止として記録する: **claims/auditsは両方の数（distinct open parents と
  per-class demand c1/c2/c4）を明記すべき**。
- 副産物: audit-blocked S5 `00000000000000809082000000000000` はclasses=3（class1+class2）で、
  その子は全てc1>=1となるためopen_classes（c1==0）帳簿から外れる。これがreceipt-unclosableの構造的理由。
- コントロール: cost-72子 `00000000000000809102000002000000`（c1=0,c2=2,c4=0）、69f子、65j子でも
  幾何再導出（D4正準化、canon検証済み）によるper-class需要がchain公開値と全件一致。

manifest（7,867行・6 part）と175行open-S5 rankingからの完全独立再計算で、chain実行は使っていない。

## 再現

```
python3 research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost69f_win7_certs_20261115.py
python3 research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconcile_cost69g_demand_20261115.py
```

- [Python第三独立監査JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69f-9cert-python-independent-audit-20261115.json)
- [69g demand reconciliation JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost69g-demand-reconciliation-20261115.json)

## 現在の確定状況

canonical chain headは 1,163/6,684/527,280/4,954/391,003 のまま（本作業は証拠の確度向上と帳簿意味論の
確定であり、frontier数値は不変）。cost69g（00000000000000809102000000002000）とcost65jは並走が
in flightのため本レーンは触れていない。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続きUNKNOWN。**
