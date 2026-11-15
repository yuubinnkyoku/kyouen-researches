# five-row-q5-m26-extend-20261115

高速レーン。(5,5) witness band 延伸レーンの IN FLIGHT claim。

## Claim(2026-11-15 09:1x UTC)

- 本レーンは **(5,5) 前線 5×26 の witness 探索**(class {0} family: plain → krow k=0..2 →
  k=3 × minpos 0..⌊(m−1)/2⌋ の段階的分解・extend55.sh と同一手順)を着手する。
  SAT なら witness band は 26 に延伸(M_{5,5} 下界 26→27)し、m=27.. へ自動延伸する。
  全 sub-instance INDET なら 19 正準類の absence-capable class-split sweep
  (K0851 と同一プロトコル)へ拡張する。
- 着手前の境界: witness 帯 m=5..25(five-row-q5-m24-class-split-20261115 で m=24 698,570・
  m=25 35,972 conflicts の class {0} SAT)・**M_{5,5} ∈ [26, 336]**(上界は K0318 substitution U=336)。
- repo 検索時点で 5×26 は未着手・未 claim(5×26/5x26 で commits・experiments 検索 0 hit)。

## 手法・較正

- 生成器: sat3.js / sat2.js / sat.js(five-row-q5-m24-class-split-20261115/scripts と md5 一致:
  sat3 d03f908ea99ba819caee2a6fbb471c1b・sat2 282ae832efa0080127c6c153e65e1c3c・
  sat.js 0cc6021a4e523a0d7f4d5ea0f5f5d40c)。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64(md5 3a5eba830aa6008a604fcc9bbe99a325)。
- 較正(エンドツーエンド bit-exact): 5×25 class {0} SAT **35,972 conflicts** —
  five-row-q5-m24-class-split-20261115/rc5x25q5_c0.txt と conflicts bit-exact(vars 37,565 / clauses 130,600)。

## スコープ

有限機械検証まで。SAT はその幅の欠損極大安全配置の存在証明(witness)。INDET は cap 到達であり不在を意味しない。
11×11 空盤・二石 root・S2 {59,60}・class1・class2・class4 はいずれも UNKNOWN。
