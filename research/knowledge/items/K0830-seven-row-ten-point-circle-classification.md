---
id: K0830
title: "7行窓の≥10点円の完全分類（m ≤ 15001）: 50族 2m−14 本＋例外 R=4ρ²=2353705250・全て行 0,3,6 通過"
kind: proposition
status: computed
topics: [geometry, rectangles]
aliases: []
scope: "7つの連続整数行（7×m 盤・m ≤ 15001・横方向は盤幅で制限）に ≥10 格子点を持つ真円の完全リスト。m ≤ 1079 では 50 族 ((2x−(2k+1))²+(2y−5)²=50 と (2y−7)² 版) のちょうど 2m−14 本のみ。m ≥ 1080 では更に弦 1079 の例外円 R = 4ρ² = 2353705250（行プロファイル {0,2,3,5,6}・中心 y = 48515/2）が 2(m−1079) 本加わる。全ての ≥10 点円は行 0, 3, 6 を通る。弦 ≤ 15000 かつ R ≤ 10¹⁵ の全列挙でこれ以外の構成は不在。"
evidence: "数学的証明（補題: 行点構造 L1・分母補題 L2 = K0831・parity 排除 L3。≥10 点 ⟺ 5二重行 or 4二重+2接点・q=1 強制）＋2つの独立な有限全列挙（弦上界版: 弦 ≤ UMAX ⟹ |Z| ≤ UMAX²/4 で Z 有限、因子対 (u−u′)(u+u′)=4|Z+1| 全列挙・7×m は UMAX=m−1 で全称。R 上界版: R ≤ 10¹⁵。独立実装 crosscheck: 表現ペアバケット化で R ≤ 10⁶ 一致・q=2,4,8 空）。例外 R = 2353705250 は u = 0..isqrt(R) 直接全走査（192 表現）で三重検証。census 一致: 7×13/16/19 = 12/18/24（K0764）・7×30/100/300 = 46/186/586 = 2m−14。"
solution:
  board: 幅7固定長m可変（m ≤ 15001）の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: ≥10点円の分類は 7×m・m ≤ 15001 で完備（弦 ≤ 15000・R ≤ 10¹⁵）
  conditions: 真円（a≠0）・連続整数行 7 本・弦上界と R 上界の両検証範囲内
  verification: [mathematical-proof, independent-enumeration, exhaustive-search]
  certificate: "定理A: m ≤ 1079 は 50 族のみ（stripsearch_u 1078）。定理B: 例外は弦 1079・R=2353705250 のみ（stripsearch_u 15000・stripsearch R ≤ 10¹⁵ 一致）。50 族の位置数 m−7/族は代数的に厳密（α ∈ [3.5, m−4.5] の半整数）。"
  independent_check: crosscheck.js（独立実装・R ≤ 10⁶）と例外表現直接全走査の一致
  note: "弦 > 15000 かつ R > 10¹⁵ の追加例外の不在は主張しない。例外が無限族か sporadic かは open。"
relations:
- type: depends_on
  target: K0764
  note: P(7) = 10（上界）と 10点円プロファイル（5二重行+2空行）の全称証明。本項目は等号ケースの分類
- type: depends_on
  target: K0831
  note: 分母補題 q | 4δ′（L2）と parity 排除（L3）が探索の有限性を与える
- type: supports
  target: K0820
  note: (7,10) 帯の ≥10 点危険円は m ≤ 587 では 50 族のみ（2m−14 本・行 0,3,6 強制通過）
artifacts:
- path: research/experiments/seven-row-ten-point-circle-classification-20261114/README.md
  role: report
  note: 定理A/B・系・補題 L1-L3 の証明骨子・検証表・スコープ
- path: research/experiments/seven-row-ten-point-circle-classification-20261114/scripts/stripsearch_u.js
  role: verifier
  note: 弦上界全列挙（|Z| ≤ UMAX²/4・因子対全列挙・q=1 前提は L2/L3 で証明済み）
- path: research/experiments/seven-row-ten-point-circle-classification-20261114/scripts/stripsearch.js
  role: verifier
  note: R 上界版全列挙（R ≤ 10¹⁵）
- path: research/experiments/seven-row-ten-point-circle-classification-20261114/scripts/crosscheck.js
  role: verifier
  note: 独立実装（表現ペアバケット化・因子対論理不使用）
- path: research/experiments/seven-row-ten-point-circle-classification-20261114/output/stripsearch_u1078.json
  role: data
  note: 定理A の直接根拠（m ≤ 1079: R=50 のみ）
- path: research/experiments/seven-row-ten-point-circle-classification-20261114/output/stripsearch_u15000.json
  role: data
  note: m ≤ 15001 の分類根拠（例外 含む）
- path: research/experiments/seven-row-ten-point-circle-classification-20261114/output/stripsearch_R1e15.json
  role: data
  note: R ≤ 10¹⁵ で2構成のみ
- path: research/experiments/seven-row-ten-point-circle-classification-20261114/output/exception_R2353705250_reps.txt
  role: data
  note: 例外円の 192 表現の直接全走査（三重検証）
---

## 命題（有限範囲完備・機械検証）

1. **定理 A**: m ≤ 1079 の全 7×m 盤で、≥10 格子点を持つ円は 50 族
   (2x−(2k+1))²+(2y−5)²=50 および (2x−(2k+1))²+(2y−7)²=50 のちょうど **2m−14 本**。
   各円ちょうど 10 点・5二重行・接点なし・行プロファイルは {0,2,3,5,6} / {0,1,3,4,6}。
2. **系 A1**: 同範囲で ≥10 点円はすべて**行 0, 3, 6 を通る**。
3. **定理 B**: 第2の構成 R = 4ρ² = 2353705250 = 25·(9703²+1)（中心 y = 48515/2、
   弦 u ∈ {5,623,763,985,1079}・二重行 Z = 2y−48515 ∈ {−48515,−48511,−48509,−48505,−48503}）
   が存在し、弦 ≤ 15000 と R ≤ 10¹⁵ の全探索で他の構成は不在。
   従って m ≤ 15001 では ≥10 点円 = 50 族 2(m−7) 本 +（m ≥ 1080 のとき）例外 2(m−1079) 本と完全確定。
4. rowcov 観察（q=10 の 7×m 円 census = 2m−14 本・全円が行 {0,3,6} 通過・全円ちょうど 10 点）は
   m ≤ 15001 で証明付きで昇格（m ≤ 300 の census と bit-exact 一致）。

## 限界

- 補題 L1（行点構造）・L2（分母）・L3（parity）は全称証明だが、分類の一意性は有限計算
  （弦 ≤ 15000・R ≤ 10¹⁵）。弦 > 15000 かつ R > 10¹⁵ の追加例外の不在は主張しない。
- 例外が無限族か sporadic かは open。
- P(w)（w = 8..14・K0764 open 帯）への L2 の一般化（q | 4⌈(w−1)/(d−1)⌉）は未実施。
