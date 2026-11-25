# five-row-q5-m26-extend-20261115

高速レーン。(5,5) witness band 延伸レーン。**COMPLETED (2026-11-15)**。

## 結果(2026-11-15 09:1x–10:3x UTC)

- **(5,5) 前線 5×26 class {0} SAT**(witness 発見)→ **witness 帯 m=5..26 に延伸**。
  **M_{5,5} ∈ [27, 336]**(着手前 [26, 336]。上界は K0318 substitution U_{5,5}=336)。
- 5×26 witness: 19石(rows [3,4,4,4,4]・deficient row 0)、kissat 4.0.4 SAT
  **1,631,556 conflicts / 199.80s**。
- m=27 は全 sub-instance INDET(下記)で**前線は m=27 のまま**。

## 手法・較正

- 生成器: sat3.js / sat2.js / sat.js(five-row-q5-m24-class-split-20261115/scripts と md5 一致:
  sat3 d03f908ea99ba819caee2a6fbb471c1b・sat2 282ae832efa0080127c6c153e65e1c3c・
  sat.js 0cc6021a4e523a0d7f4d5ea0f5f5d40c)。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64(md5 3a5eba830aa6008a604fcc9bbe99a325)。
- 較正(エンドツーエンド bit-exact): 5×25 class {0} SAT **35,972 conflicts / 8.32s**
  (vars 37,565 / clauses 130,600) — five-row-q5-m24-class-split-20261115 の値と bit-exact。
  CNF md5: 5×25 c0 1d62f2428fd5fb2fdba5cfd19114d78e・5×26 c0 60e71cfd2f1620cfa9b4070f259c1572・
  5×27 c0 bbea574b6a9a094586afd4eb98539755・5×27 c0k3 2c59afdd1d5f416a6aa953c959142669・
  5×27 c0k3p0 4d2b52a8203591e13cfc8ae126beb9b5。
- 環境リセット(2回)を跨いで較正値・5×26 SAT 値とも conflicts bit-exact 再現。

## 5×26 witness(検証 2系統)

rows [3,4,4,4,4]、stones (x,y):
(17,0),(19,0),(20,0) / (9,1),(17,1),(19,1),(24,1) / (5,2),(14,2),(16,2),(17,2) /
(13,3),(14,3),(16,3),(18,3) / (11,4),(13,4),(18,4),(19,4)。

- 系統1: sat3.js decode → sat.js verifyConfig(census 不使用)ok。
- 系統2: verify_witness_indep.py(自作・Fraction 中心・census-free・checkFast と
  独立ロジック): safety 111空セル全遮断 ok・deficiency 1(row 0)・
  maximality(1石追加全 111 候補で遮断発火)ok。
- witness_5x26_c0.json(SAT モデル復号・verify ok)・witness_5x26_c0_stones.json 参照。

## m=27 honest negatives(INDET — 不在主張ではない)

| key | 制約 | cap | conflicts | 備考 |
|---|---|---|---|---|
| c0 | plain class {0} | 250s | session1 1,777,156 / 再生成 1,924,144 (SIGTERM 243.76s) | rc=124 INDET・壁時計カットは同 trajectory で bit-exact でない |
| c0-deep | plain class {0} | 817.04s | ≥5,424,572 | deep 実行・raw log は環境リセットで喪失(進捗行値のみ記録) |
| c0k3 | --krow=0:3 | 240s | session1 1,804,438 / 再生成 1,829,756 (SIGTERM 237.22s) | rc=124 INDET |
| c0k3p0 | --krow=0:3 --minpos=0 | 200s | 1,644,162 | rc=124 INDET・raw log 保存 |

全て cap 到達 INDET。**5×27 欠損極大安全配置の不在は未確定**。
minpos は p=0 のみ実施(min(x₁,26−x_k)≤13 の sound H-split は 14 値あるが、
p=0 が単独で前線抵抗を示したため、残りは class-split 掃引レーンに委譲)。

## 1石・2石 surgery 完全列挙(負・局所 — 不在主張ではない)

seed = 5×26 witness(kissat seed@off0)とその H 鏡像(seed@off1・c0 run の
seed 依存で得られた本質的に異なる第2配置、H 鏡像で結びつく)の両方から:

- 欠損性(|S|<20)により add-only(a≤2)と rm1+add2 は**解析的に除外**
  (rows [3,4,4,4,4] から 1 石削除は row 0 が 2 石になり 5 点円が現れる)。
- **sd≤1**(1石移動)4,446 候補/実行・seed・mirror 両方 → 0 witness。
- **rm2/rm2add1/rm2add2**(2石移動・枝刈り付き完全列挙)2,321,154 候補/実行・
  seed・mirror 両方 → 0 witness(surgery2.js buildOnce/checkFast 12s/実行)。
- 合計 2,325,600 候補×2 seed = 4,651,200 編集を完全列挙し **0 witness**。
  **5×26 witness から石2個以内の編集で m=27 witness は作れない**
  (m=27 witness が存在すれば seed から3石以上の移動距離にある)。

## witness jump 幾何

- 5×26 witness の 5×27 埋め込みは offX=0 → (26,0)・offX=1 → (0,0) の
  **1セルのみ未遮断**(5×26→27 の「1石足りない」構造。(5,6) m=23 レーンと同型)。
- 石距離: sd(m26 witness, m25 witness+off1) = 30・sd(m26, m24 witness+off1) = 30
  (≥15石移動)。先行観察(witness jump ≥10石)と整合し、隣接幅間の witness は
  局所編集で遷移しない構造的証拠が 3 ファミリー((4,4)(4,5)(5,5))で揃った。

## スコープ

有限機械検証まで。SAT はその幅の欠損極大安全配置の存在証明(witness)。INDET は cap 到達であり不在を意味しない。
11×11 空盤・二石 root・S2 {59,60}・class1・class2・class4 はいずれも UNKNOWN。
上界不変: K0318 U_{5,5}=336。

## 成果物

- output/records.jsonl: 全ラン記録(較正・5×26 SAT・m=27 各 INDET・surgery・jump 幾何)
- output/summary.json
- output/rc5x25q5_c0.txt(較正)・r5x26q5_c0.txt(5×26 SAT)・witness_5x26_c0.json・
  witness_5x26_c0_stones.json・witness_5x26_c0_mirror_stones.json・
  w24.json / w25.json(m=24/25 witness 参照・jump 計算用)
- output/r5x27q5_c0.txt / r5x27q5_c0k3.txt / r5x27q5_c0k3p0.txt(INDET raw logs)
- scripts/verify_witness_indep.py・scripts/surgery1.js・scripts/surgery2.js
