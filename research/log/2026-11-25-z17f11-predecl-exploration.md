# z=17 min>=11 (floor-11) pre-declaration exploration — 2026-11-25

高速レーン (自実行・同一実行の第 4 成果: K1322 knowledge 更新 → z17-min12 kit
→ z16-min10 kit → 本 kit)。K1322 公表残余帯「m=11 行 z∈{17..20}」の第 1
エントリ (= m=11 行 z=17) の宣言前 census と、z17 floor-12 census の床非感受
性検証。本 log と kit は観測記録であり、K slot・定理の主張はしない。

## 成果物 (kit)

`research/experiments/strip-z17-min11-20261125/`:

- `engine_block.py` sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (K1282..K1322 chain と byte 同一・pin `bd5f22e4…`・startup gate PASS)
- `explore_z17f11.py` sha256 `30dcc060bfa30e9ea62a2218ec7f56a53661584daa014be9a92e7284b743ff23`
- `explore_z17f11.out` sha256 `8ecbd60599a2b6212e6972c9eb9a4ee00306d64650ea085c0ed24c042122e627`
  (3 走 byte-identical・rc 0・各 ~13 s)
- `README.md`

構成: z17-min12 kit のテキスト差分改造 (floor 12→11・s 域 {0}∪{11..41}=
各 183 形状)。11 セル (F..A5・j∈{1..11}・R=j+18) + tail spots s∈{42..49} +
below-band 子 H(18;Y;18) (min(Y)>=11)。strip・行記録・spot section は重複
測定回避のため省略 (すべて z17-min12 kit 出版済み)。

## 観測 (すべて判定外・機械観測)

1. **11 セルすべて s-only (各 183 形状・multivalue 0)**。deviant 表:
   F {16 DOWN:1, 17 穴, s>=18 恒常 2 尾}・G {16 DOWN:0}・
   E {14 DOWN:1, 16 UP:2}・D {14 DOWN:0}・C {12 DOWN:1, 14 UP:2}・
   B {12 DOWN:0}・A {12 UP:2}・**A2..A5 完全崩壊 (4 連続)**。
2. **s=11 に全セル deviant なし** — これまでの掃引で観測された deviant
   クラスは偶数 s {8,10,12,14,16} のみで、s=11 の定義域復帰はこの系列で
   初めての奇数 s の直接テスト。**奇数 s クラスの不在**が観測された
   (観測レベル。deviant クラスの偶数 s 偏在の一般則は宣言レーンの帰納
   対象候補)。
3. s>=12 クラスは出版 z17-min12 (floor-12) 表とセル単位で完全一致
   (s>=12 で形状共有による engine 自動交叉検証)。F 恒常尾も floor 11/12
   で同一構造 (床非感受性)。
4. **A517f11 (j=11・R=29) = m=11 行 z=17 全域 (min=11 厳密・co-token 11
   許容・arity<=4・s∈{11..41}): 183 形状 0 deviant・0 multivalue = 完全
   Sigma 崩壊。** A417f11 も崩壊。tail spots の A4 単一トークン 8/8 match
   と合わせ、出版 z17-min12 section-(d) (arity<=3・S∈{11..49}・110 形状
   0 分離) を arity<=4 census 側から補完。**K1322 残余帯 m=11 z∈{17..20}
   の第 1 エントリ (z=17) の in-domain 証拠完備** (宣言レーン専権)。
5. tail spots: F の 8/8 mismatch (value 2 vs collapse 0) — F 系第 8 尾形
   (恒常尾の再誕) が床 11/12 で同一 (他 80 spot は match)。
6. **below-band 子 H(18;Y;18) = v(s,18,18) が floor-11 域 183 形状で完全
   崩壊** (0 deviant・0 multivalue)。floor-12 版 (155 形状) と合わせ z=17
   の below-band 供給子完全崩壊は両床で成立 — K1320 補題 BB 族パターン
   の z=17 床非感受性。

## honest 記録

1. 本 kit は同一実行で 3 つ目の新規 census (z17-min12・z16-min10 と相互に
   重複 section なし・対象スライスも異なる)。出版済み測定 (strip 358/0・
   m=11/m=10/m=8 記録・base spot) の再実行は重複回避のため省略した。
2. 凍結 .out bytes は最終 script の 3 走のみに由来。`env -i` 走は
   `/usr/local/bin/python3` 明示 (rc127 教訓・今回は未発生)。
3. すべて pinned engine の有限機械観測。定理・全称主張なし。いかなる
   verdict も消費しない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2
   {59,60}・class 1/2/4 は全時点 UNKNOWN のまま。**

## 次の実行への申し送り (着手前に必ず最新 main 再取得)

(a) **T-Z17 宣言** (z17-min12 kit `2c74f1c6` + 本 kit `explore_z17f11`
   が供給構造を丸ごと提供: 11 閉形式 (s-only)・床非感受性 11/12・below-band
   完全崩壊両床・底 m=12 第 3 連続自明吸収 (A5 セル崩壊 + 行記録 0 分離)。
   K1322 との相違義務は A17f12 {s=12 UP:2} 供給と F 尾 (s>=18) 全称化。
   奇数 s クラス不在の帰納証明が可能なら「偶数 s 偏在則」として論じ得る
   (観測のみで据え置き)。
(b) **m=11 行 z=17 閉鎖候補** (行主張・別レーン): 本 kit A517f11 全域
   崩壊 + z17-min12 (d) 110/0。m=11 行残余帯 {18,19,20} の記録 (行 z=18 の
   記録掃引 R=30・floor 11) は未測定 — 次候補。
(c) 残る floor 誌上: m=10 行 z=17 用の floor-10 z=17 セル族は未探査
   (行記録 130/0 は出版済みだが arity<=4 セル形式は未測定)。
(d) **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
   全時点 UNKNOWN・verdict 不消費・本 kit の全 census は主張前の観測**。
