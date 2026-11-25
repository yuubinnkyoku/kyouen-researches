# 単一オーナー宣言: seven-row q=5 前線 7×38 の class-split 直接評価 (publish-then-execute)

- 宣言日時: 2026-11-23T15:20Z 前後。observed HEAD-before-push: 551c17f4 (2026-11-23T15:14:48Z)。
- 対象: K0827 が「次の枝」として挙げた **sat3 による (7,5) 7×38 直接評価**（2編集surgery完全負記録 seven-row-q5-m38-surgery-negative-20261115 の次段）。witness 帯は m=5..37・M_{7,5} ∈ [38, 1142]・前線 7×38 のまま。
- 手法: deficient 行の row-mirror 正準類 rowY ∈ {0,1,2,3}（0↔6, 1↔5, 2↔4, 3↔3。K0829/K0848/K0822 規約により全不足行ケースを尽くす）について
  `sat3.js 7 38 5 --rowY=Y`（streaming all-triples census・sat2.js と DIMACS byte-identical・q ≤ w 族）の CNF 4本を
  **kissat 4.0.4 公式 linux-amd64 バイナリ**（変更なし）で評価する。SAT なら decode + 2系統検証
  （`decode_verify.js` sat.js verifyConfig〔census 不使用〕 + `verify_witness.py` Python Fraction・いずれも出版実験 dir の verbatim複写）までをこの宣言の一本道で実行する。
- 先行宣言なし確認: 2026-11-22 以降の research/log に seven-row q5 関連の対抗宣言なし（551c17f4 時点で最終走査）。(7,6) c3_7x32 は 2026-11-20 宣言 (e30cec0a) の resume として IN FLIGHT のため**本レーンは非接触**。
- 較正（宣言前に本hostで実施・全項目出版記録と一致）: sat3.js + sat.js (raw取得) による (7,32,5) rowY=0 CNF 再生成が vars 193,644 / clauses 676,415 / curves 9,801・kissat 4.0.4 rc=10 **SAT・conflicts 129,923 bit-exact**（出版 q5-m32-row-split records.jsonl と全項目一致）・decode witness 27石・rows [3,4,4,4,4,4,4]・jsVerify ok=true・pyVerify ok=true。CNF は決定的再生成可能。
- 7×38 CNF（meta 4類共通: vars 288,546 / clauses 1,007,501 / curves 14,705）:
  - rowY=0: md5 `51bf641322378b28d6e7aaecd80fd90f`
  - rowY=1: md5 `505a17f56ce874cd081644cce5592587`
  - rowY=2: md5 `e69fe113ac00459b74e8fd5b8afba601`
  - rowY=3: md5 `f50729ed20a68e8fa1f7e09151e25164`
- cap 方針: 1インスタンスあたり **cap 7,200s**・実行順 rowY=0, 1, 2, 3・逐次（RAM 3.2GB 環境のため逐次実行）。cap 到達・環境障害は INDET として正直記録し、判定の過大主張をしない。
- 報告: 判定 (SAT: witness → M_{7,5} ≥ 39) または全 INDET 到達時に、experiment dir + records.jsonl + K0827 追記として main へ反映する。UNSAT 判定が 4類とも揃った場合のみ「7×38 witness-free」を記録する（それでも M の不在主張は次幅以降に依存し、M_{7,5} は {38} ∪ [40, 1142] と表現する）。
- 範囲と限界: 有限機械評価。census 完全性とソルバ正確性までを保証し、数論的証明ではない。上界 1142 (K0318) 不変。標準 11×11 空盤・二石root・S2・closure class への主張は一切ない (UNKNOWN担保不変)。

