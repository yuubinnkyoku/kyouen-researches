---
id: K1373
title: Baer部分平面対によるPG(2,q^2)の2重ブロッキングと PG(2,9) ≤ 26 < 3q
kind: proposition
status: proved
topics: [blocking-sets, finite-geometry, baer-subplanes]
aliases: [Baer pair double blocking, PG29 min 26]
relations:
- type: depends_on
  target: K1371
  note: 一般構成 (3q上界) とレジューム(d) (Baer対候補の厳密判定) を受け継ぐ。
    K1371 の「Baer対による3q未満候補はq<=9で未発見」記録は本項目で修正される
- type: depends_on
  target: K1370
  note: t=2 blocking の語彙・較正 (PG(2,4) 11 UNSAT/12 SAT, PG(2,5) 14/15)
- type: depends_on
  target: K1372
  note: 同セッションの軌道census手法 (PGL全生成・orbit-stabilizer整合) を共有
artifacts:
- path: research/experiments/pg2q9-baer-pair-blocking-20261128/scripts/boards9.py
  role: verifier
  note: GF(4)/GF(9)/GF(16) 独立構成 + design 検査 + Baer基底 (部分体有理点)
- path: research/experiments/pg2q9-baer-pair-blocking-20261128/scripts/baer.py
  role: verifier
  note: Baer性検査・PGL(3,q^2) 軌道BFS・全対交差census・2重ブロッキング判定
- path: research/experiments/pg2q9-baer-pair-blocking-20261128/scripts/verify_baer.py
  role: verifier
  note: 盤再構成による witness 定義直接再検査・軌道再計算・counting bound (ALL_OK)
- path: research/experiments/pg2q9-baer-pair-blocking-20261128/out/baer_pairs.json
  role: data
  note: PG(2,4)/(2,9) full census + PG(2,16) sampled witness・witness点列
- path: research/log/2026-11-28-pg2q9-baer-pair-blocking.md
  role: log
  note: 宣言・実行・検証・出版の一次記録
scope: >-
  (a) 有限結果: PG(2,4) と PG(2,9) の Baer 部分平面対全数census、
  PG(2,16) のサンプリング witness。(b) 一般条件付き補題:
  PG(2,q^2) における2つの disjoint Baer 部分平面の union は
  size 2(q^2+q+1) の2重ブロッキングであり、q>=3 のとき 3q^2 未満。
evidence: >-
  (b) は数学的証明: Baer 性 (各直線は Baer 部分平面と 1 または q+1 点で交わる)
  より disjoint な2枚の和集合は各直線と >=2 点で交わる。
  2(q^2+q+1) < 3q^2 は q>=3 で成立。disjoint 対の存在は q=2 (2,880対)
  と q=3 (3,265,920対) で全数機械検証、q=4 は seed 固定サンプリング
  (510/3000) で開示。(a) は PGL(3,q^2) 軌道の全対交差census +
  定義直接2重ブロッキング判定 (PG(2,9): 交差>=1 の対 25,293,900 は全て失敗、
  disjoint 3,265,920 は全て成功) + 盤再構成による再検証。
  witness 26点は PG(2,9) 全91直線との交差 >=2 を定義直接検証済み
  (プロファイル {2:65, 5:26})。較正: PG(2,4) では Baer 対最小 union 13 と
  既知 min 12 (SAT境界) が無矛盾 (12点minimal DBはBaer対でない)。
  再現性: クリーン再実行で出力 byte-identical。
---

## 命題・範囲

1. **PG(2,9) の t=2 最小2重ブロッキングは 19 ≤ min ≤ 26**。
   上界 26 は2つの disjoint Baer 部分平面 PG(2,3) の union の witness による
   (全 Baer 対 28,559,820 について、2重ブロッキングになるのは disjoint 対
   ちょうど 3,265,920 個・最小 union 26)。下界 19 は counting bound。
   **27 = 3q を下回るため、「PG(2,n) の t=2 min = 3n」パターンは n=9 で不成立**。
2. **条件付き一般補題**: disjoint Baer 対が存在する PG(2,q²) では
   min ≤ 2(q²+q+1) < 3q² (q≥3)。q=2 (n=4) では改善なし
   (Baer対最小 union 13 > 12 = min)。
3. PG(2,16): disjoint Baer 対 union 42 の witness (サンプリング発見・
   定義検証済み) → 33 ≤ min ≤ 42 < 48 = 3·16。
4. AG(2,9): Baer 対の AG 制限はサンプル (3,000対×91直線) で全て不可。
   AG(2,9) 上界は 26 (3q−1, K1371) のまま。

## 現在の根拠と限界

PG(2,4)/(2,9) は全数 (軌道全列挙 + 全対判定)、PG(2,16) はサンプリング
(開示)。PG(2,9) min の下界は counting bound のみで、SAT による緊め付け
(k=25 UNSAT で min=26 確定、等) は未実施 (重い・長期レーン向け)。
「全ての q≥3 で disjoint Baer 対が存在する」は未証明 (本項目では条件付き)。

## 次の接続

- PG(2,9) k=25 (または 26 の別構成の非存在) の SAT 判定で min 確定。
- PG(2,16) disjoint Baer 対の全数census (軌道 ~10^4〜10^5 規模・要分割)。
- 一般 q での disjoint Baer 対存在の証明 (Baer partition 文献との接続)。
