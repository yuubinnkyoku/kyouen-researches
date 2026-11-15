# five-row-q5-m27-minpos-sweep-20261115

高速レーン。**IN FLIGHT claim (2026-11-15 10:2x UTC)**。

## Claim

- 本レーンは **(5,5) 前線 5×27 の class {0} krow=0:3 minpos p=1..13 掃引**を着手する
  (sat3.js・cap 400s・resumable・records 増分 push)。
  `five-row-q5-m26-extend-20261115`(COMPLETED)が委譲した残り minpos 帯。
  sound H-split bound: min(x₁, 26−x₃) ≤ ⌊(m−1)/2⌋ = 13。
- 着手時点の境界: witness 帯 m=5..26・**M_{5,5} ∈ [27, 336]**(上界 K0318 U=336)。
  m=27 の honest negatives: c0 plain 250s INDET 1,777,156(session1)/1,924,144(再生成)・
  c0 deep 817.04s ≥5,424,572・c0k3 240s INDET 1,804,438/1,829,756・
  c0k3p0 200s INDET 1,644,162(five-row-q5-m26-extend-20261115)。
  1/2石 surgery 完全列挙負(seed + H鏡像・4,651,200 編集・0 witness)。
- **SAT ⟹ witness 帯は m=5..27 に延伸し M_{5,5} ∈ [28, 336]**。
  全 p UNSAT でも単独で 5×27 不在は確定しない(k=0..2・他クラス残る・absence には
  19 正準類の完全掃引が必要)。INDET は cap 到達であり不在主張ではない。
- repo 検索時点で 5×27 minpos 掃引は未着手・未 claim。

## 手法・較正

- 生成器: sat3.js(five-row-q5-m26-extend-20261115/scripts と md5 一致:
  d03f908ea99ba819caee2a6fbb471c1b)。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64(md5 3a5eba830aa6008a604fcc9bbe99a325)。
- 較正: 同一 toolchain で 5×26 class {0} SAT 1,631,556・5×25 35,972 を本日
  cross-reset bit-exact 再現済み(five-row-q5-m26-extend-20261115)。
  c0k3p0 CNF md5 4d2b52a8203591e13cfc8ae126beb9b5(前レーン記録と同一生成器)。

## スコープ

有限機械検証まで。SAT は witness 存在証明。UNSAT は符号化限定の不在。
INDET は cap 到達であり不在を意味しない。上界不変: K0318 U_{5,5}=336。
