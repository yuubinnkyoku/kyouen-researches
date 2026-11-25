---
id: K1171
title: "2トークン残余ゲーム y=13族のパラメトリック閉形式候補 cand13（fitting段階・observed・全z/x/Rの全称は未証明）"
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases:
  - "two-token y=13 parametric closed-form candidate cand13 (fitting stage, observed)"
  - "cand13 fitting probe 992 rows 72664 pts + box-out spot + merge/tail regression"
  - "y=13 first family breaking the y=5..12 cross-family laws (merge center S-2, slope-1 pins, no sweep/steady rows, small-z x-anchored regime)"
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義と単一トークン閉形式。深帯d<=-12がsingle_token(x+11)（S-2）に一致することのmerge回帰・tail回帰に使用
- type: extends
  target: K1152
  note: y=12族全称閉形式cand12に続く第13族の fitting。ただし本項は有限fit（observed）でありy12の族式の多く（merge中心・pin統一式・掃引/定常行・base rank）がy=13では有限範囲で破れることを報告する
artifacts:
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261120/report.md
  role: proof
  note: fitting実験記録（構造表・修正記録・検証規模・横断判定。正本のコードは同dirのcand13.py）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261120/cand13.py
  role: source
  note: 閉形式表の正本実装。selfcheckがprobe全点と照合し「points 72664 mismatch 0 overlap 0」を出力
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261120/probe_y13.py
  role: source
  note: 生二重再帰probe生成器（決定性・約3.5秒）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261120/spot_y13.py
  role: verifier
  note: box外spot検証器（ext-z・大d・edge・merge回帰グリッド・不一致0）
- path: research/experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261120/output/audit.json
  role: data
  note: 要件・監査数値・SHA-256
---

## 命題・範囲

2トークン残余ゲーム H(R;(x,13);z)（z>=0・x>=13・R>=0・d=x-z・offset o=R-z・
b_k=奇offset{1..2k-1}・I[t]=offset t 以上連続）について、単一オーナー宣言
（宣言時刻 2026-11-20T22:16:00Z・commit 4bdff59）の下で fitting した閉形式候補
cand13 は次の T/P 集合表である（正本は cand13.py）。

値2（in_T13）:

- ラダー: 奇z 奇R O[1,z]／偶z 奇R O[1,z-1]。
- 深帯 d<=-12: single_token(x+11) の値2そのもの（merge 中心が族式 x+y でなく **S-2=x+11**）。d=-11: z奇(x偶) 偶offset [2,10]／z偶(x奇) 奇offset [1,11]。
- 小z: ラダーのみ（z=13 の A に二重 pin {z+d+21,z+d+23}・z=14 の C に二重 pin {z+d+22,z+d+24}）。
- 汎用: A（z奇 x偶 z>=15）単一 pin z+d+21／C（z偶 x奇 z>=16）単一 pin z+d+22。
  pin の d-slope が 1（族式 z+(d+3y)/2 の 1/2 でなく）・mod 4 格子なし。
  掃引行・定常 pin 行は存在しない。

値1（in_P13）:

- 深帯 d<=-12: single_token(x+11)。d=-11: z奇 奇{1..11}∪I[12)／z偶 空。
- 小z x錨定レジーム: A/D（x偶・z<=13/z<=12）奇offset全域∪I[x+11)・B/C（x奇）奇offset{1..x+10}。
  行が d に依存せず x だけで決まる（**y13 で初観察**。cap x+10/x+11 は single_token(x+11) の指数）。
- 遷移層 z=14（C）: 奇offset{1..d+20}。汎用: A k=(d+23)//2・b_k∪I[2k)／D k=(d+22)//2・b_k∪I[2k)／
  B 奇offset{1..d+21}／C 奇offset{1..d+20}。base rank の d-slope は 1/2（y<=12 は 1/4）。
- tail: R>=x+z+14（族式 x+z+y+1 は維持）・値 (x+13) mod 2・値1無限帯と tail は x 偶行（y 奇族型）。
  偶 z 側の値1全欠如系は 6 族連続（y=8..13・y13 では深帯則からの帰結）。

## 現在の根拠と限界

根拠は有限 fitting: probe box（z=0..30・x=13..z+29・R<=x+z+26）992 行 72,664 点の
生二重再帰との全点一致（mismatch 0・T/P overlap 0・値域 {0,1,2}・値3なし）、
tail assertion 12,896 点、merge 回帰 10,608 比較、box 外 spot 4,959 点
（z=31..40・大 d 35/60・x=13 edge）すべて不一致 0。
probe は決定的に再生可能（約3.5秒）。初稿の族式外挿は 11,151 点不一致で、
深帯 S-2 と小z x錨定の発見による全面改訂で 0 に到達した（工程は実験 log・研究 log 参照）。

限界の明示:

- 本項は **observed**（有限範囲の適合）であり「全 z>=0・全 x>=13・全 R>=0」への全称主張ではない。
  正本検証器・型機械・census（clip 窓 2y+2=28 の tight 判定を含む）は宣言範囲外・未実施。
- 本項は y<=12 の全称構造と矛盾しない（量化範囲が異なる）。「族式が破れた」は
  probe/spot の有限範囲での観察であり、族系列 y>=13 への外挿も主張しない。
- 小z x錨定レジームの y<=12 族での同型性は未検証（今後の課題）。標準 11×11 の勝敗には一切言及しない。
