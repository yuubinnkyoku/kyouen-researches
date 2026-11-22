---
id: K1223
title: n=11 K0320 witness周囲のsit-at込み完全近傍陰性（7走査219万構成・9・8石witnessなし・s_11∈{8,9,10}不変）、s_12/s_13 witness近傍の拡張陰性、10×10五類witnessのpairwise shape距離≥14、n11 SAT/SLS honest negatives
kind: computation
status: computed
topics: [maximal-safe, geometry]
aliases: ["s11 witness neighborhood full negative", "s12 s13 r3a2 neighborhood negative", "n10 five classes pairwise distance 14"]
relations:
- type: related
  target: K0312
  note: "s_11∈[8,10]の決定レーン。本項はseed近傍の有限陰性のみで、s_11の値は不変（[8,10]のまま）。全域探索はheavy lane債務。"
- type: related
  target: K0320
  note: "n=11..15のn−1石構成のうちn=11/n=12/n=13 witnessをseedとして使用。上界の値更新なし。"
- type: related
  target: K1206
  note: "12×12両11石witness（K0320-n12・W_c）周囲のr3a1/r3a2拡張陰性（各22,440/1,514,700・0 witness）と、wall/plateau監査はK1222の方法執筆と同じ実験で実施。"
- type: related
  target: K1220
  note: "10×10五類のpairwise shape距離はK1220の分類に数値補完を与える（全10組の対称差∈{14,16}・最小14→2類間は最低7swap手）。SAT/SLS側は同レーンの単一オーナー規約を継承し値主張なし。"
artifacts:
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/records/ext_n11w10_r4a2.jsonl
  role: data
  note: "n=11 witness周囲の最深走査: 210×C(115,2)=1,376,550構成・0 witness・bestScore 13"
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/records/ext_k13_r3a2.jsonl
  role: data
  note: "n=13 witness周囲r3a2-full: 220×C(160,2)=2,798,400構成・0 witness（11石witnessなし）"
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/records/kissat-indet/cnf3gen-sha256.txt
  role: manifest
  note: "再生成CNF 7件のsha256（n7k6=0aecb030…は既知アンカーと完全一致、n11k8=4d73d322…・n11k9=42c88905…・n11k10=822fd7ac…・n8k7=2b9a2d76…・n9k8=55307510…・n10k9=ca981f54…）"
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/records/kissat-indet/indet-n11k10-default-240s.log
  role: log
  note: "既知SAT（K0320 10石witnessで充足可能）なのに240秒UNKNOWN・198,812 conflicts。n11 SAT近傍の最も強いhonest negative"
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/records/sls/sls2-n11k10-seed7-60s.json
  role: data
  note: "SLS v2 60秒・transplant seedingでも既知10石witnessを再発見できず（bestScore 5）。k=9（bestScore 7）・k=8（bestScore 15）の不発見は探索力不足と分離不能"
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/records/pairwise-shape-dist-n10.json
  role: data
  note: "10×10五類（K0038/K0034-another/draft/draft-sh7/v2.1）の2類間対称差: 原点揃え+D4像最小で全10組∈{14,16}・最小14。v2.1は再生成CNFのSATモデルから決定的復号しK1220公刊座標と一致"
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/records/verify/verify-k0320-n11.json
  role: certificate
  note: "seed 6件のverify_witness.py（整数行列式公開検証器）出力。K0320-n11は111/111空点blocked、wall12のuncovered=[(4,11),(5,11),(8,11),(11,11)]はK1206記録と完全一致"
- path: research/experiments/minimal-maximal-neighborhood-full-nets-20261122/README.md
  role: source
  note: "全走査表（25走査・10,082,387構成）・恒等式・解釈規約・再現手順"
---

# s_11/s_12/s_13 witness近傍のsit-at込み完全陰性・honest negatives・五類shape距離

## 命題・範囲

標準共円盤（q=4）の n×n 盤・有限近傍の列挙事実。いずれも
「走査した近傍内での不存在」であり、全域の非存在証明ではない。

1. **n=11（K0320 10石witness 周囲）**: remove-m/add-a
   （(m,a) = (1,0),(2,0),(2,1),(3,1),(3,2),(4,1),(4,2)）の
   計2,192,440構成を走査し、9石witnessも8石witnessも**近傍に存在しない**。
   s_11∈{8,9,10}（K0312）は不変。r4a1（7石構成のみ）のfound=0は
   K0312「k≤7では極大不可」と整合する期待値制御。
2. **n=12**: 両11石witness（K0320-n12・K1206 W_c）周囲のr3a1/r3a2拡張
   （各22,440・1,514,700×2）で**10石witnessなし**。s_12≤11不変。
3. **n=13**: K0320 12石witness周囲r2a2 829,026（found=66は全てtrivial自己再構成）
   ・r3a1 35,200・r3a2 2,798,400で**11石witnessなし**。s_13≤12不変。
4. **10×10五類のshape距離**: K1220の5類の2類間対称差は
   原点揃え+D4最小で全10組∈{14,16}・最小14（≥7 swap手）。
5. **SAT/SLS honest negatives**: n11k8/k9/k10（v2.1）は240秒INDET
   （特にn11k10は充足可能既知）。SLS v2 60秒では既知10石witnessの
   再発見にも失敗（bestScore 5）。いずれも値主張・不在主張なし。

## 現在の根拠と限界

全走査はext_nets.mjs（K1222）による有限完全列挙で、構成数が
C(k0,m)×(a=0?1:C(n²−(k0−m),a)) と全件一致する（完備性の独立検証）。
seedの安全性・極大性はverify_witness.py（整数行列式・quartetカタログ非依存）
で証人つき確認（n11: 111/111・n12: 133/133・n13: 157/157 blocked）。
ext_netsの決定性（再実行のbyte一致、ms・argvフィールド除く）も確認済み。

**限界**: 陰性はすべて「K0320既知witness近傍の有限近傍内」の不在であり、
s_11=9/8の全域・s_12≤10・s_13≤11の全域には一切言及しない。
SAT/SLSの数値（conflicts・bestScore・checked数）は勝敗でも探索費用でもない。
6×6/7×7等の矩形レーン・11×11空盤・二石root・class 1/2/4は非接触。
