---
id: K1220
title: 10×10の安全十石極大配置の格子同型類は既知で5類以上（既刊2類に加え、SAT再探索が互いに非合同な3つの新規配置を3系統検証・tamper陰性対照つきで明示）。同一チェーンの較正でs_7=7を両側再導出、n=8/9には検証済み明示witness 2件ずつを追加
kind: computation
status: computed
topics: [maximal-safe, geometry, search-methods]
aliases: ["n10 ten-stone witness lattice classes 3-5", "s7 SAT re-derivation calibration"]
relations:
- type: extends
  target: K0038
  note: "K0038 witness（第1類）とK0034本文の別witness（第2類）に続き、本計算は3つの非合同配置（第3〜5類）を追加した。5類は十石配置全体の分類ではなく既知の明示例の個数の下界"
- type: related
  target: K0034
  note: "s_10=10の値は不変（上界側の明示例を増やしたのみ）。九石全域排除による下界とも独立"
- type: related
  target: K0031
  note: "同一SAT機材の較正: n7k6 UNSAT（default+--shuffle=42の2符号化一致）とn7k7 SAT witnessのK0031合同によりs_7=7を両側再導出。K0031の値の更新ではなく独立機材による再現"
- type: related
  target: K0032
  note: "n=8のSAT witnessは全408カタログが既存のため新規性を主張しない（追加の検証済み明示例として記録）"
- type: related
  target: K0033
  note: "s_9=9の明示witnessがknowledge項目本文にないため、検証済み2例（互いに非合同・draft/v2.1各1）を追加記録"
- type: related
  target: K1206
  note: "格子同型分類はK1206のclassify.mjsと同一規約（D4×整数平行移動・8像正規化・辞書式最小キー）"
artifacts:
- path: research/experiments/s12-s13-sat-stabilization-20261122/README.md
  role: source
  note: "全件の正本: 符号化・ラン表・分類検証・再現手順・非主張"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/enc_sat2.mjs
  role: verifier
  note: "検証済みlex-leader鎖を持つv2.1符号化（本計算のSAT witness供給源・生成もCNF sha256記録で再現可能）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/verify_witness.py
  role: verifier
  note: "Python整数順列4x4行列式検証器（空点ごと証人つき、K1206と同一系統）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/verify_witness.mjs
  role: verifier
  note: "Node BigInt Bareiss第2系統（列順序・展開が.pyと相違）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/check_model2.mjs
  role: verifier
  note: "第3系統: K1204アンカー照合済みcensus直結の述語評価+D4 lex-leader記録"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/classify_sat_witnesses.mjs
  role: verifier
  note: "正準形分類（アンカー: K0031/K0038/K0034別/K0320 n12・n13）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/classify_v3.mjs
  role: verifier
  note: "v2.1 witnessを含む拡張分類（本項の5類主張の機械可読正本）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/output/wit_n10k10.json
  role: data
  note: "第3類witness（v2-draft n10k10 SAT modelから、span 10×9）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/output/wit_n10k10_sh7.json
  role: data
  note: "第4類witness（--shuffle=7から、span 7×7）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/output/v3wit_n10k10.json
  role: data
  note: "第5類witness（v2.1 n10k10 SAT・4.37秒から、span 10×4）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/output/v3classification.json
  role: certificate
  note: "5類相互・既刊2類アンカーとの対比較（正準形辞書式最小キー）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/output/v3wit_n10k10_py.json
  role: certificate
  note: "第5類の空点90点全証人つき安全性・極大性検証（draft側2類は wit_n10k10_py.json / wit_n10k10_sh7_py.json）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/output/tamper_v3_n10k10_py.json
  role: data
  note: "tamper陰性対照: 1石除去で両幾何検証器がrc=1 NOT-MAXIMAL-SAFE を出すことの確認（draft側も同様に全6件で確認済み）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/logs/v3n7k6.log
  role: log
  note: "s_7>=7側のUNSAT（13.56秒・174,155 conflicts; 第2符号化 v3n7k6sh42.log もUNSAT）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/logs/v3n7k7.log
  role: log
  note: "s_7<=7側のSAT（witnessはK0031と合同の再発見・陽性対照）"
- path: research/experiments/s12-s13-sat-stabilization-20261122/scripts/cnf-sha256.txt
  role: manifest
  note: "全CNF（非刊行）のsha256記録: v1 9件・v2-draft 16件・v2.1 8件が(n,k,seed)からbyte再現可能"
---

# 10×10十石witnessの格子同型類（2→5）とs_7再導出・n=8/9明示例

## 1. 十石極大安全配置の3つの新規類（主成果）

10×10標準盤（q=4）の安全十石極大配置をSAT modelから3つ新たに明示した。3系統の独立検証
（Python整数順列行列式・Node BigInt Bareiss・census直結の述語評価、いずれもK1204アンカー照合gateつき）、
tamper陰性対照（1石除去で全検証器が拒否）、格子同型分類（D4×整数平行移動の正準形辞書式最小キー、
K1206規約）を機械実施した:

- 第3類: `[[9,1],[1,2],[8,2],[9,2],[0,3],[3,4],[5,6],[9,6],[8,7],[2,9]]`（span 10×9。v2-draft n10k10 SATから）
- 第4類: `[[2,0],[1,1],[7,2],[4,3],[5,3],[6,3],[3,4],[5,5],[1,6],[6,6]]`（span 7×7。--shuffle=7から）
- 第5類: `[[6,3],[7,3],[0,4],[7,4],[8,4],[1,5],[2,5],[9,5],[2,6],[3,6]]`（span 10×4。v2.1 n10k10から・4.37秒）

いずれも既刊2類（K0038 witness・K0034本文の別witness）と非合同、相互にも非合同。よって
**10×10の十石極大安全配置の既知の格子同型類は2類から5類へ増えた**。5類は明示例の個数であり、
十石配置全体の分類でもうまく値の更新でもない（s_10=10不変）。

## 2. 較正: s_7=7の両側SAT再導出・n=8/9の明示witness

- n=7: at-most-6がUNSAT（v2.1 defaultと--shuffle=42の独立2符号化で一致、受理言語は実験README §3の
  軌道被覆機械検査済み）、at-most-7がSATでwitnessはK0031証人と合同の再発見。
  よって s_7=7 を独立機材で両側再現（値主張はK0031のまま）。
- n=8 / n=9: at-most-8 / at-most-9 がSATで、それぞれ2件（draft/v2.1、互いに非合同）の検証済み
  明示witnessを記録。n=8は全408カタログ（K0032）が既存のため新規性不主張。
  n=9はknowledge本文に明示witnessがなく追加の明示例として提供。
- gap-1 UNSAT（n8k7/n9k8/n10k9）とn≥12は単発270秒級cap内ではすべて INDET（不在不主張、
  詳細は実験READMEのラン表）。

## 限界

- 3類の新規性は「既刊2類と非合同」という分類主張であって、全部署の列挙ではない。6類目以降の有無は未確定。
- UNSAT判定はDRAT証明書なしのkissat 4.0.4への信頼境界（第2符号化一致が唯一の交差検査）。
- witness導出のdraft符号化の対称性破り鎖には瑕疵（K1221）があったが、充足方向のmodel→配置は
  影響を受けず、全witnessは幾何の独立検証で成立する。第5類は軌道被覆検査済みのv2.1から直接得た。
- n≥12への方法の外挿はしない。
