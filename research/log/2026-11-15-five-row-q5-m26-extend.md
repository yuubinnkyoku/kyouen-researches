# 2026-11-15：(5,5) witness 帯 m=5..26 延伸 — 5×26 class {0} SAT（1,631,556 conflicts）・M_{5,5} ∈ [27,336]・m=27 honest negatives・1/2石 surgery 完全列挙負・witness jump sd=30

高速レーン(five-row-q5-m26-extend-20261115)。(5,5) 前線 5×26 を sat3.js class {0} 符号化で解決し、
witness 帯を m=5..25 から **m=5..26** に延伸した。**M_{5,5} ∈ [26,336] → [27,336]**
(上界は不変・K0318 curve-packing 代入 U_{5,5}=336)。

## 主結果

1. **5×26 class {0} SAT**: kissat 4.0.4 official・**1,631,556 conflicts / 199.80s**
   (vars 41,030 / clauses 142,643・CNF md5 60e71cfd2f1620cfa9b4070f259c1572)。
   witness 19石 rows [3,4,4,4,4](単一欠損 w(q-1)-1 石):
   (17,0),(19,0),(20,0) / (9,1),(17,1),(19,1),(24,1) / (5,2),(14,2),(16,2),(17,2) /
   (13,3),(14,3),(16,3),(18,3) / (11,4),(13,4),(18,4),(19,4)。
2. **2系統検証**: sat3.js decode + sat.js verifyConfig(census 不使用)と、
   自作 `verify_witness_indep.py`(純Python Fraction・census-free・ロジック独立)の両方で
   safety(111空セル全遮断)・maximality(全1石追加で遮断発火)・deficiency ok。
3. **cross-reset bit-exact**: 環境リセット2回を跨ぎ、較正(5×25 SAT 35,972)と
   5×26 SAT の conflicts とも bit-exact 再現(3回目の再生)。

## m=27 honest negatives(INDET — 不在主張ではない)

- class {0} plain: session1 250s INDET 1,777,156(進捗行値)・再生成 log は 250s cap で kissat が
  SIGTERM を捕捉し最終統計 **1,924,144 conflicts**(process-time 243.76s・壁時計カットなので
  同 trajectory だが bit-exactではない)。
- class {0} deep: 817.04s で **≥5,424,572 conflicts** まで到達しても未決着
  (環境ハードリセットで raw log 喪失・進捗行値のみ記録)。
- class {0} krow=0:3: session1 240s INDET 1,804,438・再生成 log 240s cap SIGTERM 237.22s・
  **1,829,756 conflicts**。
- class {0} krow=0:3 minpos=0: 200s INDET 1,644,162(raw log 保存)。
- 残りの minpos p=1..13(sound H-split bound ⌊(m−1)/2⌋=13)は class-split 掃引レーンに委譲。
  **前線は m=27 のまま。**

## 1石・2石 surgery 完全列挙(負・局所)

seed = 5×26 witness(kissat seed@off0)とその H 鏡像(seed@off1・本質的に異なる第2配置)の両方から:

- 欠損性(|S| ≤ 19 = w(q−1)−1)により add-only(a≥1 → |S|≥20)と rm1+add2(|S|=20)は
  **解析的に除外**。
- **sd≤1**: 4,446 候補/実行・**rm2/rm2add1/rm2add2**: 2,321,154 候補/実行(buildOnce/checkFast・
  枝刈り付き完全列挙・決定的12s/実行)。2 seed で同一結果・**0 witness**。
- 合計 2,325,600 候補×2 seed = 4,651,200 編集を完全列挙。
  **m=27 witness(があれば)は両 seed から3石移動以上離れている**(不在主張ではない)。

## witness jump 幾何

- 5×27 埋め込み: offX=0 → (26,0)・offX=1 → (0,0) の**1セルのみ未遮断**
  ((5,6) m=23 レーンと同型の「1石足りない」構造)。
- 石距離: sd(m26, m25+off1) = 30・sd(m26, m24+off1) = 30(≥15石移動)。
  隣接幅間 witness jump が大きいという先行観察((4,4)(4,5)(5,6)(5,7))に (5,5) が加わり、
  5 ファミリーで構造的証拠が揃った。

## 信頼境界

- SAT は 5×26 の欠損極大安全配置の存在証明。m=27 の全 sub-instance は INDET であり
  **不在は未確定**。上界 336 は K0318 代入で不変。
- 標準11×11空盤・二石root・S2 {59,60}・class1・class2・class4 はいずれも UNKNOWN。

## 再現

```sh
node sat3.js 5 26 5 --class=0 c5x26q5_c0.cnf
kissat c5x26q5_c0.cnf                       # SAT 1,631,556 conflicts
node sat3.js 5 26 5 --class=0 c5x26q5_c0.cnf --decode ...   # sat.js verifyConfig
python scripts/verify_witness_indep.py output/witness_5x26_c0_stones.json   # 独立系統
node scripts/surgery2.js                     # 2,321,154 candidates, 0 witnesses
```

記録: research/experiments/five-row-q5-m26-extend-20261115/(README.md・output/records.jsonl・
output/summary.json・raw logs)。CSV results/fixed-width/mwq_stabilization.csv の (5,5) 行を
27..336 に更新。
