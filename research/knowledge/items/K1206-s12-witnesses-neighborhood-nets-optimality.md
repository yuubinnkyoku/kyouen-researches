---
id: K1206
title: 12×12の11石安全極大witnessを追加2件明示（s_12≤11の第2・第3 witness、3系統検証・133/133空点blocked）しwitness近傍のremove-2/add-1完全走査と壁状態の2-swap完全走査は陰性、score-4壁はstrict局所最適
kind: computation
status: computed
topics: [maximal-safe, geometry]
aliases: ["s12 upper witness triplet", "witness neighborhood nets negative", "2-swap strict optimality"]
relations:
- type: supports
  target: K0320
  note: "K0320のs_12≤11構成に続く独立に検証された第2・第3の明示witness 2件（W_b=[[6,0],[5,1],[6,2],[2,6],[7,6],[10,6],[2,7],[4,7],[9,7],[2,11],[5,11]]、W_c=[[5,1],[4,2],[5,4],[9,5],[0,6],[10,6],[4,7],[0,9],[4,9],[5,9],[11,11]]）。3系統検証（Python整数順列4x4行列式・Node BigInt Bareiss・quartetカタログState）すべてSAFE+MAXIMAL、133/133空点blocked。K0320の上界を改善しない・等しくしない。s_13側には新witnessなし"
- type: related
  target: K0312
  note: "11盤の8≤s_11≤10決定レーン（a45a626d）と本計算は無関係。本項は12×12・13×13のみを対象とし、s_11には一切触れない"
- type: related
  target: K0149
  note: "s_12/s_13の下界には影響しない。陰性走査はすべて有界探索の不成功であり非存在証明ではない（SLSの弱さは陰性対照 ctrl2_k11_scratch/ctrl_k12_n13 で明示的に記録済み）"
artifacts:
- path: research/experiments/s12-s13-upper-witness-20261121/witness_s12_11b.json
  role: data
  note: "W_b witness JSON（SLS seed 2024、環境リセット跨ぎの再検証品）"
- path: research/experiments/s12-s13-upper-witness-20261121/witness_s12_11c.json
  role: data
  note: "W_c witness JSON（post-reset SLS seed 5150、45.8秒、records/ctrl_k11_seeded.json）"
- path: research/experiments/s12-s13-upper-witness-20261121/records/verify_py_s12_11b.json
  role: certificate
  note: "Python整数順列4x4行列式検証器の全空点証人（攻撃tripleと正準化曲線係数を空点ごとに明示）SAFE+MAXIMAL"
- path: research/experiments/s12-s13-upper-witness-20261121/records/verify_py_s12_11c.json
  role: certificate
  note: "W_cの同形式全空点証人"
- path: research/experiments/s12-s13-upper-witness-20261121/records/verify_mjs_s12_11b.json
  role: certificate
  note: "第2系統: Node BigInt Bareiss（列順序・展開が.pyと異なる）SAFE+MAXIMAL"
- path: research/experiments/s12-s13-upper-witness-20261121/records/verify_mjs_s12_11c.json
  role: certificate
  note: "W_cの第2系統検証"
- path: research/experiments/s12-s13-upper-witness-20261121/records/verify_state_s12_11b.json
  role: certificate
  note: "第3系統: quartetカタログState機械の判定"
- path: research/experiments/s12-s13-upper-witness-20261121/records/verify_py_negctrl.json
  role: data
  note: "陰性対照: W_bから1石除去で検証器がrc=1・uncovered>0で拒否（検証器が虚陰性を持たないことの確認）"
- path: research/experiments/s12-s13-upper-witness-20261121/records/verify_mjs_negctrl.json
  role: data
  note: "同上の第2系統"
- path: research/experiments/s12-s13-upper-witness-20261121/records/nets_n12.json
  role: data
  note: "12×12 K0320 11石witness周囲の完全近傍: remove-1 (11)・remove-2 (55)・remove-2/add-1完全 (55×1,735候補) で10石極大安全なし"
- path: research/experiments/s12-s13-upper-witness-20261121/records/nets_n13.json
  role: data
  note: "13×13 K0320 12石witness周囲: remove-1 (12)・remove-2 (66)・remove-2/add-1完全 (66×2,457) で11石極大安全なし"
- path: research/experiments/s12-s13-upper-witness-20261121/records/probe2_wall_n12.json
  role: data
  note: "12×12壁状態（score 4 = K0320 witness−1石）の完全2-out/2-in走査: 45対・1追加6,099・2追加413,100検査でwitnessなし・best score 4のまま=strict局所最適"
- path: research/experiments/s12-s13-upper-witness-20261121/records/probe_wall_n12.json
  role: data
  note: "壁状態の第一次近傍probe（completion順序制限版）陰性"
- path: research/experiments/s12-s13-upper-witness-20261121/records/probe2_pl_n13.json
  role: data
  note: "13×13 plateau（score 6）の完全2-out/2-in: 55対・8,781+699,600検査でwitnessなし・strict局所最適"
- path: research/experiments/s12-s13-upper-witness-20261121/records/probe_ctrl_n11.json
  role: data
  note: "機械対照: 公式n=11 witness（既知最大性）に対するprobe走査の挙動記録"
- path: research/experiments/s12-s13-upper-witness-20261121/records/sls_k10_v1_a.json
  role: data
  note: "12×12 k=10 SLS seeded走査（4×60s+100s）: 全run score 4にplateau・同一basin 収束"
- path: research/experiments/s12-s13-upper-witness-20261121/records/sls_k10_scratch_b.json
  role: data
  note: "12×12 k=10 SLS scratch走査（seedなし）: score 8 plateau"
- path: research/experiments/s12-s13-upper-witness-20261121/records/sls_k11_n13_a.json
  role: data
  note: "13×13 k=11 SLS: score 6 plateau"
- path: research/experiments/s12-s13-upper-witness-20261121/records/ctrl2_k11_scratch.json
  role: data
  note: "陰性対照（SLS弱さの明示）: 実行可能なk=11をscratchから3×35sで探索するとscore 2で全滅"
- path: research/experiments/s12-s13-upper-witness-20261121/records/ctrl_k12_n13.json
  role: data
  note: "陰性対照: 13×13 k=12（実行可能）もscratchではscore 2で全滅"
- path: research/experiments/s12-s13-upper-witness-20261121/scripts/verify_witness.py
  role: verifier
  note: "整数順列4x4行列式検証器（全空点証人つき）。行列式==0⇔共線または共円"
- path: research/experiments/s12-s13-upper-witness-20261121/scripts/verify_witness.mjs
  role: verifier
  note: "BigInt Bareiss検証器（列順序が.pyと異なる別code path）"
- path: research/experiments/s12-s13-upper-witness-20261121/README.md
  role: source
  note: "全結果・環境リセット事故の復旧記録・再現手続き・解釈規約"
---

# 12×12の11石witness追加2件と12×12/13×13近傍の完備陰性

## 1. s_12≤11の第2・第3 witness（新規、陽性成果）

12×12盤に11石の安全極大配置を2件新たに明示した（冒頭W_b・W_c）。いずれも3系統の独立検証（Python整数順列4x4行列式、Node BigInt Bareiss〔列順序・展開手順が異なる〕、quartetカタログState〔K1204のcensusゲート通過後〕）でSAFE+MAXIMAL、133/133の空点がなんらかの3石tripleと曲線（共線または円）上でblockedであることを空点ごとの証人つきで確認した。1石除去の陰性対照は両幾何検証器がrc=1で拒否し、検証器が虚合格を出さないことを確認した。K0320のs_12≤11に先行性はあり、本項は同じ上界に対する独立に再検証された明示構成を2件追加する。**s_12≤10のwitnessは本レーンでは発見できていない**。

## 2. witness近傍の完全走査（陰性、有界探索の不成功）

12×12のK0320 11石witness周囲: 石1つ除去(11通り)・2つ除去(55通り)は当然非極大、2つ除去+1追加の全候補55×1,735配置で10石の安全極大なし。13×13の12石witness周囲: 66×2,457で11石なし。いずれも「witnessから2石以内の除去と1追加の範囲にk−1石witnessは存在しない」という有限事実である。

## 3. 壁状態のstrict局所最適性（2-swap完全走査）

12×12のSLS探索はすべてscore 4（未blocked空点4つ）のD4・平行移動同族状態（K0320 witness−1石）に収束した。この壁状態に対する完全2-out/2-in走査（石対45を除き、除いた状態の各空点を満たしうる追加候補の全1追加・全2追加対）6,099+413,100検査で、witnessも9石極大もscore 4未満の状態も1つも存在せず、**壁状態はこの近傍のexhaustionでstrict局所最適**である。13×13のplateau（score 6）も55対・8,781+699,600検査で同様にstrict。数時間スケールのSLS再挑戦は、この2-swap近傍にとどまる限り無意味であることを機械が保証する。

## 4. SLSの範囲と誠実な陰性対照

k=10 (12×12) seeded 4×60s+100s は全てscore 4 plateau・同一basin。k=10 scratchはscore 8。k=11 (13×13) はscore 6。**非存在は主張しない**。同じエンジンのseedなし設定は実行可能なk=11（12×12）・k=12（13×13）の再発見にも3×35s・120sで全て失敗する（score 2で停止）ため、k=10/11の未発見は探索の弱さと分離できない。moves/evals/restart数は判定ではない。

## 限界

- 陰性はすべて有界近傍・有界時間の探索不成功であり、非存在証明ではない。特にs_12≥11・s_13≥12の下界は本項から生じない（UNSAT/下界機構は本レーンの非目標）。
- W_b・W_cとK0320 witnessのD4+平行移動同値性は未分類（3件が別個の配置であることの確認にとどまる）。正準形分類は次課題。
- 13×13の11石上界（s_13≤12の改善）には本期間の進展なし。
