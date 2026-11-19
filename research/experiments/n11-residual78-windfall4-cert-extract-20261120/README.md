# n11-residual78-windfall4-cert-extract-20261120

K1063 (resolve6) が「windfall」として記録した 4 本の WIN7-D10 root
（class2-lane-cost65h child `00000000000000803202000000001000` の
bit 40/43/99/118・残余 78 行のうち 4 行を被覆）について、
resolve6 の宣言どおり「証明書抽出 + 独立検証」を実行した。
branch/PR は作らず main に直接出版。

## 何をしたか

- **抽出**: repo-verbatim `class4_child1_cert_extractor_exact_ms23.ts`
  （FBS=1<<20 forbidden-bit table・MS=1<<23 memo・CAP=1e9）を
  `scripts/cert_driver_windfall.ts` から blind（kill table 空・pref=null）で
  起動し、各 root の legal loser first-move 全て (48/58/52/56 手) にわたり
  完全な winning strategy tree を抽出。fbt_drops=0・全 move ok・uncapped・
  terminal 石数 [13,17]。**2 回実行で証明書 byte-identical・node 数完全一致**。
- **独立検証 1**: `verify_bit7_win7_cert.ts`（number Bareiss 4x4・sub-root
  分解・全 loser reply 展開）。全 sub-root PASS、consumed union ==
  strategy rows 完全一致 (missing 0 / extra 0)。
- **独立検証 2**: `verify_cost71c_win7_bareiss_independent.py`
  （純 python・exact 整数 Bareiss・root から全 subtree を再帰展開）。
  全 sub-root PASS・union 完全一致・terminal {13,15,17}。
- **独立検証 3**: `verify_win7_certificate_bigint_independent.mjs`
  （BigInt 3x3 cofactor 展開・Sweep 両方の lemma と同一方式）。
  全 sub-root PASS・rows sorted unique・union 完全一致・terminal [13,17]。
- **runner v16 node-exact 再現**: repo-verbatim runner v16
  （depth 10・andclose=1・cap 1e9）で 4 bit を fresh に再解き、
  出版 raw batch 行 (batch3/4/7/8) と** node 数完全一致**
  （40: 1,105,860 / 43: 3,269,824 / 99: 1,114,855 / 118: 2,307,338。
  bit 43 は resolve6 記録の determinism_rerun_node_exact 与同値）、
  pilot_d6 制御行 loss=false (3,402 nodes) 合格。

## 結果（output/windfall4-cert-triple-verification-20261120.json が正本）

| bit | raw root hex (証明書 root 行) | moves | 抽出 nodes | rows | SHA-256 |
|----|----|----|----|----|----|
| 40 | 00000000000000803202010000001000 | 48 | 3,074,926 | 31,189 | 02778cf535bb3a269496f8b1cf0064fbadeb3b302bc4476d6b2d1c391bc37a34 |
| 43 | 00000000000000803202080000001000 | 58 | 7,700,023 | 51,767 | 27e60fdca5eeed3fb1c188edd35a2d6ba3212df2b16cd309f4247b902e366d7b |
| 99 | 00000008000000803202000000001000 | 52 | 3,355,354 | 36,625 | 04f545c8861015ff15ba8506322b9e78574cd523c54100d9bff424cd587f59ed |
| 118 | 00400000000000803202000000001000 | 56 | 6,137,302 | 55,838 | 05356cbc162adc318b9c208e607ebff872deda1d266541b1585b83ea7a38cdf5 |

- 全 50 gate 合格（fail-closed・builder `scripts/build_verify_record_20261120.py`
  が artifacts から gate を再計算して JSON を組む。2 回実行 byte-identical、
  出力 SHA-256 `a3ca1b3dfd2fcdbd28fc88a6f993c4ff5ad81ee92d4a22800ff2f6477c476feb`）。
- bit 99 / 118 の raw root は D4 非正準形。canonical root
  （00000000000000803800000008001200 / 00000000010000803800000008100000）
  への写像は resolve6 evidence root と一致（gate `canonical-mapping-*`）。
  証明書は root 行 = raw root で出版（抽出の corpus provenance
  (child, bit)=(c65h, 40/43/99/118) と一致させるため。D4 不変性により
  どの像でも同一の game tree 主張になる）。

## 解釈規約（他の n11 項目と同一）

- 各証明書が主張するのは「この 7 石 root で second mover が to move のとき、
  original first mover が必勝（全 loser 分岐が loser stuck の terminal
  13-17 石で終端）」という game-theoretic fact のみである。
- **本項は残余 78 行のどの行も閉鎖しない**。行の閉鎖計上は、これらの証明書を
  入力として消費する receipt-fold 記録（K1057/K1063 系譜の fold 機械）が
  別途必要。fold が存在するまで、被覆 4 行は pending-win のまま扱い、
  resolve6 の 39-root live witness 計画は依然として 78 行を独立に全被覆する。
- REFUTED-D10 は LOSS 証明ではない。pn/dn や solved 数を勝敗として
  読まない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4
  はすべて UNKNOWN のまま。**

## 次の一手

1. 4 証明書を入力とする receipt fold（4 行の閉鎖計上・fold9 機械の
   入力 chain 再構築が必要）。
2. 39 live witness の depth-10 両順序掃引（K1059 と同一 driver/runner v17
   規約・pilot_d6 制御）。
