---
id: K1298
title: "parity-graded 共演ゲーム — Grundy 値が {0,1} に限ることは極大安全集合のパリティ一様と同値"
kind: proposition
status: proved
topics: [grundy, geometry, strategy-length]
aliases:
- parity characterization for 0/1 Grundy games
- uniform maximal parity iff Grundy in {0,1}
- parity-graded Grundy lemma
relations:
- type: related
  target: K1253
  note: 反転平面盤では極大サイズのパリティが混ざり Grundy 2 以上が現れる具体例
- type: related
  target: K1293
  note: 設計ボードの graded 性（全極大が同一サイズ）は本定理の特別な場合
- type: depends_on
  target: K1058
  note: 共演ゲームの定義。K1058 §6 は「同一サイズ」版を証明済み
- type: generalizes
  target: K1058
  note: §6 の同一サイズ版をパリティ一様版へ一般化し、さらに逆（必要性）を与える
- type: related
  target: K1300
  note: s-パラメータゲームでパリティ一様/混在の両方の実例を与える
artifacts:
- path: research/experiments/parity-characterization-20261125/scripts/verify_small_boards.py
  role: verifier
  note: 8,360 個の小盤（網羅＋ランダム）で (a)⇔(b)、局所形、Grundy/misère 公式を検査
- path: research/experiments/parity-characterization-20261125/output/verification.json
  role: certificate
  note: 8,360 盤・uniform 5,263・mixed 3,097・violations 0
- path: research/experiments/s-parameter-kyouen-20261125/output/grundy_general.json
  role: data
  note: パリティ一様（AG(2,4) s=2）と混在（AG(2,5) s=2 など）の完全 Grundy データ
- path: research/experiments/projective-blocking-kyouen-20261125/report.md
  role: proof
  note: 元の十分条件（パリティ一様 ⇒ {0,1}）の帰納証明と PG 盤での適用
- path: research/experiments/parity-characterization-20261125/independent/REPORT.md
  role: log
  note: 独立検証の総括（定理監査 PASS、小盤 13,096 インスタンス違反 0、PG(2,5) 3 手法一致）
- path: research/experiments/parity-characterization-20261125/independent/verify_boards.py
  role: verifier
  note: 独自実装による小盤の (a)⇔(b)⇔(c)・公式・局所形の検査
- path: research/experiments/parity-characterization-20261125/independent/out/verification_boards.json
  role: certificate
  note: 5,048 盤 / 13,096 インスタンスの検査結果（違反 0）
- path: research/experiments/parity-characterization-20261125/independent/out/pg2q5_verification.json
  role: certificate
  note: PG(2,5) キャップ・ゲームの独立再計算（3 手法一致）
scope: 有限ハイパーグラフ盤（点集合 + ブロック族）上の共演ゲーム。局面は各ブロックと高々 s 点で交わる点集合、手は 1 点追加、通常プレイ（打てない方が負け）。s は固定（s=2,3,4 など）。
evidence: "定理: 次の 3 条件は同値。(a) すべての局面の Grundy 値が 0 か 1。(b) すべての極大安全集合のサイズのパリティが一様。(c) 任意の局面 S について、S の極大拡大のサイズのパリティがすべて一様。さらに (b) が成り立つとき共通パリティ p で Grundy(S)=(p−|S|) mod 2、misère は (p−|S|) が偶数なら勝ち。**証明**: (b)⇒(a) は極大集合がすべてサイズ ≡p なので任意の完全プレイの長さが p−|S| と同パリティになり、K1058 §6 と同じ帰納で mex が (p−|S|) mod 2 になる（サイズ自体は一様でなくてよい）。(a)⇒(c): 全 Grundy が {0,1} なら、Grundy 0 の局面の子はすべて 1、Grundy 1 の局面の子はすべて 0（mex の定義）。極大局面は Grundy 0 なので、任意の極大プレイに沿って値は 0,1,0,1,… と交互に並び、終点 0 までの距離のパリティは Grundy(S) で決まる。よって (c)。(c)⇒(b) は空盤で自明。**検証**: 8,360 個の小盤（n=4,5 の全 2/3/4-一様族、n=6,7,8 のランダム族、s=2,3,4）で (a)⇔(b)・局所形・公式を検査し、uniform 5,263 盤・mixed 3,097 盤・violations 0。実データでも AG(2,4) s=2（極大 4,6 の偶数一様）は Grundy {0,1}、AG(2,5) s=2（5,6 混在）・AG(2,4) s=3（8,9）・AG(2,5) s=3（9,10,11）・PG(2,4) s=4（12,13,14,16）・M(q)（q≥5）は Grundy ≥2 をもつ。独立検証（別実装）は 5,048 盤 / 13,096 インスタンス（n=4,5 網羅＋n=6,7 ランダム、s=2,3,4）で (a)⇔(b)⇔(c)・Grundy/misère 公式・局所形の違反 0、PG(2,5) は 3 手法でキャップ 41,572・極大 3,100（すべて 6）・Grundy {0:19066,1:22506}・G(∅)=0・misère=1 を確認。さらに PG(2,5) s=3 の全 7,906,892 局面で局所形（パリティ混在 ⇔ 上位局面に Grundy ≥2）を検査し 0 violations。"
---

# parity-graded 共演ゲーム

## 定理

有限な盤（点集合 `V` とブロック族）上の共演ゲーム（局面 = 各ブロックと高々 `s` 点で
交わる集合、手 = 1 点追加、通常プレイ）について、次は同値:

- **(a)** すべての局面の Grundy 値が `0` か `1`。
- **(b)** すべての極大安全集合のサイズのパリティが一様。
- **(c)** 任意の局面 `S` について、`S` の極大拡大のサイズのパリティがすべて一様。

さらに (b) が成り立ち、共通パリティを `p` とすると

```
Grundy(S) = (p − |S|) mod 2,      misère 勝利 ⟺ (p − |S|) が偶数.
```

## 証明

**(b) ⇒ (a)**: 任意の安全集合 `S` の極大拡大はすべてサイズ `≡ p` の極大集合なので、
`S` からの完全プレイの長さは常に `p − |S|` と同パリティ。深さについての帰納で
`Grundy(S) = (p − |S|) mod 2`（K1058 §6 の同一サイズ版と同じ議論）。□

**(a) ⇒ (c)**: すべての Grundy 値が `{0,1}` に属すると仮定する。mex の定義から

- `Grundy(T) = 0` なら、`T` のすべての子は Grundy `1`（0 が子に現れない）。
- `Grundy(T) = 1` なら、`T` のすべての子は Grundy `0`（0 が現れ、1 は現れない）。

したがって任意のプレイに沿って Grundy 値は `0,1,0,1,...` と交互に並ぶ。
極大局面の Grundy は `0` だから、`S` から極大局面までの距離のパリティは
`Grundy(S)` で一意に決まる（`Grundy(S)=0` なら偶数、`1` なら奇数）。
よって `S` の極大拡大はすべて同じパリティをもつ。□

**(c) ⇒ (b)**: 空盤に (c) を適用すればよい。□

**系（局所形）**: 局面 `S` 以下の部分ゲームの Grundy 値がすべて `{0,1}` に限ることは、
`S` の極大拡大のパリティが一様であることと同値（S を固定した残余ゲームに同じ帰納を適用する。残余容量 s−|S∩B| は一様でないが、定理の証明は容量の一様性を使わない）。

**注意（S 自身の Grundy ではない）**: 系は「S の上（S を含む局面全体）」についての主張であり、
`Grundy(S) ≤ 1` とは同値でない。小盤の探索では、S の極大拡大がパリティ混在でも
`Grundy(S) ≤ 1` となる例が 20,539 個中 6,757 個あった（例: n=5, s=2, blocks
{(0,2),(0,4),(1,2),(2,4),(1,3,4),(0,2,3,4)} の S={} は極大拡大 6 個でパリティ混在、
`Grundy(S)=1`、misère の値が 0）。2 以上の Grundy は S の子孫に現れる。

## 意味

- **Grundy 2 以上の出現は、極大安全集合のパリティ混在とちょうど同値**である。
  したがって「ゲームが複雑か」は Grundy を計算せずに、極大集合のサイズの
  パリティを見るだけで判定できる。
- K1058 §6（全極大が同一サイズ ⇒ `(T−|S|) mod 2`）は (b) の特別な場合。
  本定理はサイズ一様でなくてよいこと、および逆（必要性）を与える。
- 設計ボード（全極大が同一 `K`）、`PG(2,q)` の s=2（全極大が最大サイズ）、
  `AG(2,4)` の s=2（極大 4,6 で偶数一様）は (a) の例。
  `AG(2,5)` の s=2（5,6）、`AG(2,4)` の s=3（8,9）、`AG(2,5)` の s=3（9,10,11）、
  `PG(2,4)` の s=4（12,13,14,16）、反転平面 `M(q)`（q≥5）は (b) を満たさず
  Grundy 2 以上が現れる。

## 予測応用（PG(2,7), s=2）

`PG(2,7)` の s=2 ゲームは 2^57 局面で全数計算できない。しかし 30,000 回の
ランダム貪欲探索で見つかる極大アーク（complete arc）はサイズ **6 と 8 のみ**
（両方偶数）だった。定理より、もし全極大アークが偶数サイズなら Grundy は
`{0,1}` と**予測**される（サイズは混在するがパリティは一様）。
全数計算なしにゲームの複雑さを幾何から判定できる例。

## 検証

- 小盤 8,360 個（n=4,5 の 2/3/4-一様族の網羅、n=6,7,8 のランダム族、
  s=2,3,4）で (a)⇔(b)・局所形・Grundy/misère 公式を検査:
  uniform 5,263 盤、mixed 3,097 盤、**violations 0**。さらに `PG(2,5)` s=3 の
  全 7,906,892 局面で局所形「パリティ混在 ⇔ 上位局面に Grundy ≥2」を検査し
  **violations 0**（独立実装、K1300）。
  （`parity-characterization-20261125/output/verification.json`）。
- 実データ: K1300 の 10 ゲーム＋PG(2,5) の s=2 で、パリティ一様な盤は
  Grundy `{0,1}`、混在盤は Grundy ≥2 をもつことを確認。

## 注意

- 仮定は「盤全体で極大サイズのパリティが一様」であり、サイズ一様ではない
  （`AG(2,4)` s=2 は 4 と 6 の 2 種類）。
- misère の公式は (b) の下でのみ成立する。
