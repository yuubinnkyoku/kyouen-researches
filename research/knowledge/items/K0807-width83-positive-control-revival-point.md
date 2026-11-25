---
id: K0807
title: "w=83..86正制御の完走 — REST6掃引機の生存検出感度を4幅で実証（w83生残2件・w84生残4件・w85生残6件・w86生残ユニーク10件・全て11050円の実窓で実現・certificate-phantom 0件）・level 17復活点の実測確定はちょうどw=83・w83..86の生残パターン完全特定・w84の事前予測leaves=2は反証（実窓は4窓）・w85・w86の機械census予測はいずれも完全的中（6・10）・w87事前予測（ユニーク生残≥46）登録"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w∈{83,84,85,86}・長さm可変の標準整数格子におけるlevel 17 REST6生残パターンの完全決定（有限計算の全称: 全3,300 maximal mask走査・各幅）。主張: (1) w=83のREST6生残17行パターンはちょうど2件 {0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82} と {0,5,7,19,27,32,40,52,54,59,63,70,73,76,77,81,82}（他は全滅）。(2) w=84のREST6生残17行パターンはちょうど4件（mask 456・1909・2612・3119・各1 leaf）。w=85のREST6生残17行パターンはちょうど6件（mask 456・1909・2612・2696・3052・3119・各1 leaf・11050円の85幅窓 a=−2..0,21..23 で実現・phantom 0）。(2b) w=86のREST6生残17行パターンはユニークちょうど10件（mask 126・169・456・1376・1909・2612・2696・3052・3119・3249・11050円の86幅窓 a=−3..1,19..23 の10窓で実現・phantom 0・素朴leaves計上はaborted chunk二重計上により11）。(3) いずれのパターンもREST16の16法全てで生残（phase 2でも死なない）。(4) いずれのパターンも11050円の窓で34点・17行として実現（行集合はパターンと完全一致）→ certificate-phantom 0件・REST6⊇REST16⊇実現可能 の差分は w∈{83,84,85,86}・level 17 では空。(5) level 17の復活点は実測でちょうど w=83。P(83)..P(86)≥34 は witness で既知・上界はopen。(6) w=83 log に事前登録された w84 予測（leaves=2・2窓）は反証: 11050円の84幅窓の34点窓は a=−1,0,22,23 の4窓（手書き窓列挙の数え落とし・機械不具合ではない）。w85・w86の機械census予測（leaves≥6・≥10）はいずれも完全的中"
evidence: "数学的証明（K0804機 width_sweep.mjs の w=83..86 完走 + 段階追試）。(a) w83完走: 505チャンク・2,420,302,072 nodes・capEsc 72・unique 3,456・leaves=2・生残2。w84完走: 597チャンク・2,876,302,072 nodes・capEsc 78・unique 3,465・leaves=4・生残4・2回の独立完走でnode総数bit-exact。w85完走: 693チャンク・3,476,385,481 nodes・capEsc 92・unique 3,476・leaves=6・生残6（収集版再完走 3,478,785,481・チャンク境界差のみ・verdict不変）。w86完走: 833チャンク・4,250,048,258 nodes・capEsc 110・unique 3,487・maximal 3,300・leaves計上11（ユニーク生残10・p3249がaborted chunk from=3239→from=3249の再探索で二重計上）。(b) 生存帰属: width83_survivor_probe.mjs（repo verbatim）でw83 mask 456/3119・w84 mask 456/1909/2612/3119・w85 mask 456/1909/2612/2696/3052/3119・w86 mask 126/169/456/1376/1909/2612/2696/3052/3119/3249 を特定（w83公表値を制御としてbit-exact再現）。(c) REST16再検査: w84..w86全パターンが16法全てで共通証明書非空。(d) 実現の直接検証: 11050円の独立直接列挙（circle11050_window_census.mjs）で w83=2窓・w84=4窓・w85=6窓・w86=10窓が34点・17行で各パターンと完全一致・掃引生残とbit-exact一致。(e) 有限実在スキャン: R'≤1e6・1mod4-smooth・prod(e+1)≥9 の全1,964円・3実現形で生残行集合のrealizerはR'=5525のみ（w86の10パターンも全て）。修正check（width86_realizability_scan.mjs）: 旧width84/85_realizability_scan.mjsのcheckは窓先頭行=キーL自身を仮定しpattern[0]>0の窓を数え落とすunder-approximationだった（偽陰性方向のみ・過大主張なし）。修正版checkでw84生残4・w85生残6を再スキャン: realizerはいずれも5525のみで結論不変。正制御: witnessが予測する生残が4幅で機械検出側でちょうど再現 → 生存検出感度が実証され、w≤82の全滅結果（K0801..K0804）の誤殺なしの裏付けになる"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: "w=83..86の生残パターン完全特定は各幅全3,300 maximal maskの全走査による全称（有限計算）。P(83)..P(86)≥34は全m≥1でのwitness"
  conditions: "連続整数行"
  verification: [mathematical-proof, exhaustive-enumeration]
  certificate: "幅83..86 REST6 level 17 掃引完走（2.42G / 2.88G / 3.48G / 4.25G nodes）+ 生残mask・生残集合の帰属再現（probe・制御込み）+ REST16 16法再検査 + 11050円全窓の直接列挙一致（2/4/6/10窓）+ R'≤1e6 実現スキャン（realizerは5525のみ・修正checkでw84/85再スキャン済み）"
  independent_check: "probe の帰属（w83: mask456/3119・w84: mask456/1909/2612/3119・w85: +2696/3052・w86: +126/169/1376/3249・各1 leaf）・w83公表生残のbit-exact再現・11050円の独立直接列挙（w83 2窓・w84 4窓・w85 6窓・w86 10窓・34点17行）・REST16再検査（全幅全通過）・実現スキャン（1,964円・realizer 5525 のみ・修正checkでw84..86全パターン再確認）・w84 node総数2回の独立完走で一致（2,876,302,072）・state_w83..w86.json"
  note: "w=83 は K0797 会計（g0≥2形・w≤84）の範囲内だが、witness が既知のため level 17 全滅は P≤32 を与えない（K0804の限界どおり）。本項の価値は (i) 掃引機の生存検出感度の正制御が4幅で通過（w≤82全滅の信頼性の実証的裏付け）・(ii) 復活点の実測確定・(iii) 生残パターンの孤立性（realizerは11050円のみ）・(iv) 事前予測プロトコルの反証→原因特定→修正→的中→的中のサイクル（w84手書き予測leaves=2は窓列挙の数え落としで反証・実窓は4 → 修正された機械census予測は w85 leaves≥6 がちょうど6・w86 leaves≥10 がユニークちょうど10で連続完全的中）。教訓: (1) 生残数の事前予測は必ず機械による窓全列挙から導出する。(2) aborted chunk 境界で leaf が二重計上されうる（w86で初観測: leaves計上11 vs ユニーク10）・生残数は survPats の unique 化で読むこと"
relations:
- type: depends_on
  target: K0804
  note: "掃引機（width_sweep.mjs）と w≤82 全滅の境界。本項はその正制御完了（w83..86）"
- type: depends_on
  target: K0785
  note: "11050円 witness（P(83..86)≥34・34点最小幅83）が生残予測の源（w86の生残も本円の窓censusから予測された）"
- type: depends_on
  target: K0791
  note: "34点最小幅83（復活点の右端の理論的裏付け）"
- type: supports
  target: K0785
  note: "level 17 復活点を理論値 (82,83] から実測でちょうど w=83 に確定・witness パターンの掃引機内での完全特定（w83..w86）"
artifacts:
- path: research/experiments/width83-positive-control-20261114/scripts/width83_survivor_probe.mjs
  role: verifier
  note: "生存mask・生残17行集合の帰属ログ付きプローブ（width_sweep.mjs と同一アルゴリズム・w84..86でもそのまま使用）"
- path: research/experiments/width83-positive-control-20261114/scripts/width83_realizability_scan.ts
  role: verifier
  note: "REST16再検査 + 11050円2窓の直接検証 + R'≤1e6 実現スキャン"
- path: research/experiments/width83-positive-control-20261114/output/width83_positive_control.json
  role: data
  note: "w=83完走・帰属・REST16・実現・スキャンの全記録"
- path: research/experiments/width69-84-sweep-20261114/output/state_w83.json
  role: data
  note: "w=83完走状態（2.4M capプロトコル・2,420,302,072 nodes・leaves=2・生残2・capEsc 72）"
- path: research/experiments/width69-84-sweep-20261114/output/state_w84.json
  role: data
  note: "w=84完走状態（2.4M capプロトコル・2,876,302,072 nodes・leaves=4・生残4・capEsc 78・unique 3,465）"
- path: research/experiments/width84-positive-control-20261114/scripts/width_survivor_collect.mjs
  role: verifier
  note: "width_sweep.mjs に生残パターン記録を追加したプローブ版（w84の2回目の完走でnode-exact再現と生残4パターン抽出を同時に達成・w86でも使用）"
- path: research/experiments/width84-positive-control-20261114/scripts/circle11050_window_census.mjs
  role: verifier
  note: "11050円の幅w窓センサスの独立直接実装（w83=2・w84=4・w85=6・w86=10窓・34点窓全列挙）"
- path: research/experiments/width84-positive-control-20261114/scripts/width84_realizability_scan.mjs
  role: verifier
  note: "REST16再検査 + 11050円4窓の直接検証 + R'≤1e6 孤立性スキャン（width83_realizability_scan.ts の w=84 版・checkは旧版）"
- path: research/experiments/width84-positive-control-20261114/output/width84_positive_control.json
  role: data
  note: "w=84完走・帰属・REST16・実現・スキャン・窓センサス（w83..86）の全記録"
- path: research/log/2026-11-14-width83-positive-control.md
  role: log
  note: "w83判断・教訓・レジューム・w84事前予測（本項で反証）"
- path: research/log/2026-11-14-width84-positive-control.md
  role: log
  note: "w84実行記録・予測反証の原因特定・w85/86事前予測"
- path: research/experiments/width84-positive-control-20261114/scripts/width85_realizability_scan.mjs
  role: verifier
  note: "w85のREST16再検査 + 11050円6窓の直接検証 + R'≤1e6 孤立性スキャン（checkは旧版）"
- path: research/experiments/width84-positive-control-20261114/output/width85_positive_control.json
  role: data
  note: "w85完走・帰属・REST16・実現・スキャンの全記録（機械census予測leaves≥6の完全的中）"
- path: research/experiments/width84-positive-control-20261114/report-w85.md
  role: proof
  note: "w85正制御報告（予測プロトコル修正後の初の完全的中）"
- path: research/experiments/width69-84-sweep-20261114/output/state_w85.json
  role: data
  note: "w=85完走状態（2.4M capプロトコル・3,476,385,481 nodes・leaves=6・生残6・capEsc 92・unique 3,476）"
- path: research/log/2026-11-14-width85-positive-control.md
  role: log
  note: "w85実行記録・予測的中判定・w86 leaves≥10予測"
- path: research/experiments/width69-84-sweep-20261114/output/state_w86.json
  role: data
  note: "w=86完走状態（収集版・survPats込み・4,250,048,258 nodes・833チャンク・unique 3,487・leaves計上11・survPats unique 10・capEsc 110・p3249二重計上の生データ）"
- path: research/experiments/width84-positive-control-20261114/scripts/width86_realizability_scan.mjs
  role: verifier
  note: "w86のREST16再検査 + 11050円10窓の直接検証 + R'≤1e6 孤立性スキャン（修正check: 窓開始A=k0−2·pat[0]を全キーから試行・w84/85生残の再スキャン込み）"
- path: research/experiments/width84-positive-control-20261114/output/width86_positive_control.json
  role: data
  note: "w86完走・REST16・実現・スキャン・w84/w85修正check再スキャンの全記録（機械census予測ユニーク≥10の完全的中）"
- path: research/experiments/width84-positive-control-20261114/report-w86.md
  role: proof
  note: "w86正制御報告（leaves 11 vs unique 10 の二重計上注記・check修正の経緯）"
- path: research/log/2026-11-14-width86-positive-control.md
  role: log
  note: "w86実行記録・予測的中判定・w87..91の36点窓censusに基づく次回予測"
- path: research/experiments/width84-positive-control-20261114/scripts/circle11050_window36_census.mjs
  role: verifier
  note: "11050円の36点（18行）窓censusの独立直接実装（w83..92）"
- path: research/experiments/width84-positive-control-20261114/output/circle11050_window36_census.json
  role: data
  note: "36点窓census出力: w87=2窓（a=0,19）・w88=4窓・w89=6窓・w90=8窓・w91=10窓（各36点18行）・34点窓は w87=10・w88=10・w89=12・w90=14・w91=18窓"
---

## 命題（証明済み・有限全称）

1. **w=83 の level 17 REST6 生残パターンはちょうど2件**:
   - P₁ = {0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82}（maximal mask 3119 内）
   - P₂ = {0,5,7,19,27,32,40,52,54,59,63,70,73,76,77,81,82}（maximal mask 456 内）
   - 他の全 maximal mask（3,298件）は leaves=0・生残0。
2. **w=84 の level 17 REST6 生残パターンはちょうど4件**:
   - mask 3119 → {0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82}
   - mask 2612 → {1,2,6,7,10,13,20,24,29,31,43,51,56,64,76,78,83}
   - mask 456 → {0,5,7,19,27,32,40,52,54,59,63,70,73,76,77,81,82}
   - mask 1909 → {1,6,8,20,28,33,41,53,55,60,64,71,74,77,78,82,83}
   - 他の全 maximal mask（3,296件）は leaves=0・生残0。完走 2,876,302,072 nodes・
     2回の独立完走で node 総数 bit-exact。
2b. **w=85 の level 17 REST6 生残パターンはちょうど6件**: mask 3119（a=0）・
    2612（a=−1）・2696（a=−2）・456（a=23）・1909（a=22）・3052（a=21）。
    他の全 maximal mask は leaves=0・生残0。完走 3,476,385,481 nodes。
2c. **w=86 の level 17 REST6 生残17行パターンはユニークちょうど10件**:
    mask 126（a=1）・169（a=19）・1376（a=20）・3052（a=21）・1909（a=22）・
    456（a=23）・3249（a=−3）・2696（a=−2）・2612（a=−1）・3119（a=0）。
    他の全 maximal mask は生残0。完走 4,250,048,258 nodes・833チャンク・
    unique 3,487。素朴 leaves 計上は11だが、p3249 の leaf が aborted chunk
    from=3239 の部分探索と from=3249 の再探索で二重計上されたもので、
    ユニーク生残行集合は10（survPats の unique 化で確認）。
3. **全パターンとも REST16 を通過**（16法全てで共通証明書非空）→ phase 2 でも死なない。
4. **全パターンとも 11050 円で実現**:
   - w=83: 窓 x∈[0,82] = P₁・窓 x∈[23,105] = P₂（各34点・17行）
   - w=84: 窓 x∈[−1,82]（mask 2612）・[0,83]（mask 3119）・[22,105]（mask 1909）・
     [23,106]（mask 456）（各34点・17行・行集合はパターンと完全一致）
   - w=85: 窓 x∈[−2,82]（mask 2696）・[−1,82]（mask 2612）・[0,84]（mask 3119）・
     [21,105]（mask 3052）・[22,105]（mask 1909）・[23,105]（mask 456）（各34点・17行）
   - w=86: 窓 x∈[−3,82]（mask 3249）・[−2,83]（mask 2696）・[−1,84]（mask 2612）・
     [0,85]（mask 3119）・[1,86]（mask 126）・[19,104]（mask 169）・[20,105]（mask 1376）・
     [21,106]（mask 3052）・[22,107]（mask 1909）・[23,108]（mask 456）（各34点・17行）
   - ⟹ **certificate-phantom 0件**（REST6 ⊇ REST16 ⊇ 実現可能 の差分は w∈{83..86}・level 17 では空）
5. **level 17 の復活点は実測でちょうど w=83**（K0804: w≤82 全滅 + 本項: w=83 生残2件・実現可能）。
6. **w85・w86 予測の連続完全的中**: 機械censusから事前登録した
   「w85掃引 leaves≥6・全て実現可能・phantom 0」は**ちょうど6で完全的中**、
   「w86掃引 leaves≥10・全て実現可能・phantom 0」は**ユニーク生残ちょうど10で
   完全的中**（生残はcensusの窓と bit-exact 一致・leaves計上11との差は
   aborted chunk 二重計上で機械不具合ではない）。
7. **w84 事前予測の反証**: w=83 log に事前登録された「w84 は leaves=2・生残2・
   11050円の84幅窓は x∈[0,83] と x∈[22,105] のちょうど2窓」は反証。
   11050円の84幅窓で34点に達するのは a=−1,0,22,23 の**4窓**
   （独立直接列挙・掃引生残4と bit-exact 一致）。原因は予測側の窓列挙が
   「窓の左端が円の行に載る」場合しか数えていなかったことで、機械の誤検出ではない。
8. **実現スキャンの check 修正と再検証**: 旧 width84/85_realizability_scan.mjs の
   check は窓先頭行 = キー L 自身を仮定しており、pattern[0]>0 の窓
   （窓開始 x が円の行でないアラインメント）を数え落とす under-approximation
   だった（偽陰性方向のみ・誤った孤立性主張は生じていない）。
   修正 check（窓開始 A = k0 − 2·pat[0] を全キーから試行）で w84 生残4・
   w85 生残6・w86 生残10 の全パターンを再スキャンした結果、realizer は
   いずれも R'=5525 のみで、旧結論は不変。

## 正制御としての意義

- K0785 の witness 予測が機械検出側で4幅連続してちょうど再現:
  掃引機の**生存検出感度が実証**された。w=49..82 の全滅掃引（K0790..K0804）は
  「生残が出た時に検出できる」ことが実機で裏付けられたことになる。
- w=84 の4生残は**2つの円行集合 × 2つの窓アラインメント**・w=85 の6生残は
  **2行集合 × 3アラインメント**・w=86 の10生残は**2行集合 × 5アラインメント**
  （いずれも窓左端の位置の違いのみ）: 行集合は w=83 の P₁/P₂ に一致し、
  独立した witness 族は増えていない。

## 構造観察・次の事前予測（反証可能）

- witness の孤立性: w=83..86 で生残するのは witness 円の行パターンのみ
  （R'≤1e6・prod(e+1)≥9 の全1,964円・3実現形のスキャンで realizer は R'=5525 のみ）。
- 34点窓の個数は幅とともに増える: 11050円の34点（17行）窓は w83:2・w84:4・
  w85:6・w86:10窓。w=87 で初めて**36点（18行）窓**が現れる
  （circle11050_window36_census.mjs による直接列挙: 36点窓は
  w87=2窓（a=0,19）・w88=4窓・w89=6窓・w90=8窓・w91=10窓・34点窓は
  w87=10・w88=10・w89=12・w90=14・w91=18窓）。
- **w=87 の事前予測（本項で登録・反証可能）**: w87 の34点以上の窓は12窓
  （17行窓10窓 + 18行窓 a=0,19 の2窓）。level 17 掃引は17行部分集合を数えるため、
  18行窓からは全18個の17行部分集合が REST6 を通過
  （行集合の共通証明書は部分集合上でも非空）。
  よって **w87掃引のユニーク生残17行パターン ≥ 10 + 2×18 = 46**、
  全て11050円で実現可能・phantom 0予想・census 超過の生残は phantom の存在を意味する。
  leaves の正確な値は maximal mask のサイズ（18行を含む T が他に行を持つか）に
  依存し予測しない。aborted chunk による leaf 二重計上にも注意
  （生残数は survPats の unique 化で判定する）。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- **P(83)..P(86) の上界は open**（35点以上の円が幅83..86に収まる可能性は
  排除していない。level 18 掃引が必要）。P(83..86)≥34 のみ確定。
- w=87 以降の正制御は未実行（w87 予測 ≥46 は本項で登録済み・掃引は ~5G nodes
  で重いので実行は次レーン以降）。
- 実現スキャンの円の範囲は R'≤1e6・prod(e+1)≥9（r2≥36）に限定。
  より小さい r2 の円や R'>1e6 は掃引していない（ただし生残パターンの実現は
  11050円で直接的に確認済みのため、スキャンは孤立性の補助証拠）。
- 旧 width84/85_realizability_scan.mjs（repo内・旧checkのまま）は窓アラインメントの
  数え落としを持つ。孤立性の読み取りには修正check版
  （width86_realizability_scan.mjs・w84/85再スキャン結果を width86_positive_control.json に同梱）を用いること。
- 11×11 空盤・二石 root {49,60} は本項目と無関係に UNKNOWN のまま。
