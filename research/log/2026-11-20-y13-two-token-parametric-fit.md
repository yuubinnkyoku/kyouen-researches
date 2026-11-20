# y=13 族パラメトリック閉形式 fit の工程記録（2026-11-20 高速レーン）

単一オーナー宣言（[宣言ノート](2026-11-20-y13-two-token-skeleton-single-owner-note.md)・2026-11-20T22:16:00Z・
commit 4bdff59be86bf96626a4333cf16da8545f07eb1d）に基づく y=13 族着手の fitting 段階の記録。
成果物は [実験](../experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261120/report.md)・
知識は [K1171](../knowledge/items/K1171-two-token-y13-parametric-closed-form-fit.md)。

## 発見順

1. **probe 生成**（`probe_y13.py`・y=10/11/12 と同型の canonical descending-multiset engine・
   z=0..30・x=13..z+29・R<=x+z+26・992 行 72,664 点・約 3.5 秒）。
2. **外挿初稿**: 族式（merge 中心 x+13・pin z+(d+39)/2・base k=floor((d+40)/4)・band 下端 28）
   の素直な引き伸ばし → probe 72,664 点中 **11,151 点不一致**。
   主因: (a) 深帯が single_token(x+13) に落ちない、(b) z<=14 の小z行が全く別構造、
   (c) pin/th/base の d-slope が 1/2 でなく 1。
3. **深帯の発見**: 深帯 d<=-12 の全行が single_token(x+11)（= S-2・族式の S=x+y と異なる）に
   値ごと一致。族式境界 x<=z-14 でなく 2 列浅い d<=-12。d=-11 に固定短帯 [2,10]/[1,11] と
   I[12)/空 の遷移行。ここまでで残不一致 763 点・すべて z<=14 層に集中。
4. **小z x錨定レジームの発見**: 残った不一致は (z,x) 偶奇 4 クラス×小z/遷移/汎用の完全再分析で
   解消。z<=13（奇z）/z<=12（偶z）では行が d に依存せず x だけで決まる:
   x 偶 = 奇 offset 全域 ∪ I[x+11)、x 奇 = 奇 offset <= x+10。cap x+10/x+11 は
   single_token(x+11) の指数と一致（「z<=y では 2 トークン相互作用が消える」横断法則候補）。
   遷移層 z=13/14 は二重 pin {z+d+21, z+d+23} / {z+d+22, z+d+24} を持ち、
   z>=15（奇z）/z>=14（偶z・D）/z>=16（偶z・C）から d 錨定の汎用レジーム
   （A: k=(d+23)//2・pin z+d+21・B: base<=d+21・D: k=(d+22)//2・C: base<=d+20・pin z+d+22）へ。
5. **全点一致**: probe 72,664 点 mismatch 0・T/P overlap 0
   （最後に negative offset の pbase ガード 1 行・Python の負奇数剰余バグ 3,799 偽不一致の解消）。
6. **検証**: tail assertion 12,896 点（R>=x+z+14 → (x+13) mod 2）・merge 回帰 10,608 比較
   （z=0..40・x<=z-12）・box 外 spot 4,959 点（z=31..40・大 d=35/60・x=13 edge）すべて不一致 0。

## 判断の要点

- **y=13 は族系列（y=5..12）で初めて主要族式が揃って破れた族**である: merge 中心 S-2・
  pin slope 1（mod 4 格子の消滅）・掃引/定常行の不生成・base k slope 1/2。
  これらは probe + spot の有限範囲で確定した観察（observed）であり、全称破れの主張ではない。
  y<=12 の全称証明済み構造を cand13 が否定するものでもない（量化範囲が異なる）。
- 小z x錨定レジームは y<=12 の出版表に明示されていなかった構造で、
  単一トークン型の指数で潰れる点から「z<=y 則」の横断候補として報告する。
  y=11/y=12 の小 z 行が実は同型かどうかは今後の検証課題（本 fit では未実施）。
- 採番: push 直前に最新 main で K1170 までの使用を確認し K1171 とした
  （README 末尾・items・直近 commit 3 点確認）。

## 失敗・限界の記録

- 初稿の族式外挿は y13 では全く当たらない（不一致 15%）。「族式の素直な延長」戦略は
  y<=12 で 9 族連続で有効だったが y13 で初めて全域破綻したため、fitting は実質
  data-driven の再発見になった。この枠組みの変化自体が y>=13 の族の新しい情報。
- probe の R 上限 x+z+26 は tail 開始 x+z+14 を 12 点分余裕をもって含み、
  cand13 の tail 带・k(d) の大きい d 行の上端は cap 内でしか検証していない
  （large-d-ext-R spot で d=60 まで R<=120 の範囲で照合）。
- 全称証明段階（正本検証器・型機械・census・clip 窓 2y+2=28 の tight 判定）は宣言どおり
  範囲外。別宣言で着手可能。

標準 11×11 の勝敗・二石 root・S2 {59,60} には一切言及しない。
