# z=16 min>=10 (floor-10) pre-declaration exploration — 2026-11-25

高速レーン (自実行・同一実行の第 3 成果: K1322 knowledge 更新後、z17-min12 kit、
本 kit)。K1320 系2 の公表残余「m=10 行 z∈{16,17}」の z=16 側閉鎖候補に向けた
宣言前 census。本 log と kit は観測記録であり、K slot・定理の主張はしない。

## 成果物 (kit)

`research/experiments/strip-z16-min10-20261125/`:

- `engine_block.py` sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (K1282..K1322 chain と byte 同一・pin `bd5f22e4…`・startup gate PASS)
- `explore_z16f10.py` sha256 `ad2b44a8d9e156ad880395d394d2e50c9319094a51f455de19d7d7b173d1f4de`
- `explore_z16f10.out` sha256 `45aa409a458e5704263ab8dc29d0c783fd324f2e4dc7ae4f125cd55701db50a1`
  (3 走 byte-identical・rc 0・各 ~12 s)
- `README.md`

構成: 出版 z16-min11 kit (`explore_z16pre.py` `87f3bb71…`) のテキスト差分改造
(floor 11→10・s 域 {0}∪{10..40}〔z15-min10 kit と同一の 221 形状/セル域〕)。
10 セル (F..A4・j∈{1..10}・R=j+17) + tail spots s∈{41..48} + below-band 子
`H(17;Y;17)` (min(Y)>=10) の 3 section。strip/base/行記録 section は本 edition
では省略 (m>=11 行は T-Z16 で証明済み・m=10 行は A4 セルそのもの)。

## 観測 (すべて判定外・機械観測)

1. **10 セルすべて s-only (各 221 形状・multivalue 0)**。deviant 表:
   F {16 UP:1}・G {14 DOWN:0, 16 UP:2}・E {14 UP:1}・D {12 DOWN:0, 14 UP:2}・
   C {12 UP:1}・B {10 DOWN:0, 12 UP:2}・A {10 UP:1}・A2 {10 UP:2}・
   **A3 なし・A4 なし** (梯子上位 2 rung 連続完全崩壊)。
2. **s>=12 クラスは出版 K1322 (floor-11) の deviant 表とセル単位で完全一致**
   (floor 10/11 は s>=12 で形状を共有するため engine 同一性による自動
   交叉検証: F/G/E/D/C・B の s=12 まで同一)。
3. **s=10 クラスの復活 =「死点化第 2 事象」の正体が床 (定義域) による除外
   だと確定**。floor 11 では消えた z=15 由来 s=10 供給クラスが、floor 10 で
   再び定義域に入ると z=16 でも生存: 出版 z=15 の位置 {A,B,C}@10 から
   {B DOWN:0, A UP:1, A2 UP:2}@10 に再構成 (C の s=10 partner 消滅・クラスが
   A 側に 1 rank climb・B は方向反転)。**z 遷移はクラスを殺さず再構成する
   だけ**という構造判定の最初の直接実測 (観測レベルの主張であり、定理化は
   宣言レーン)。
4. **A416f10 (j=10・R=27) = m=10 行 z=16 の全域 (min=10 厳密・co-token 10
   許容・arity<=4・s∈{10..40}): 221 形状 0 deviant・0 multivalue = 完全
   Sigma 崩壊。** 出版 z16-min11 kit section-(d) の arity<=3・S∈{10..48}・
   130 形状 0 分離と合わせ、m=10 行 z=16 閉鎖候補の in-domain 証拠が
   arity<=4 census まで完備。tail spots (単一トークン s∈{41..48}) も 8/8
   で A4 を含む全セル match (80/80)。
5. tail spots 全体 (80/80): floor 10 z=16 に恒常尾なし (F {16 UP:1} 単点構造
   は floor 11 と同一・尾の再誕は z17-min12 kit 観測の z=17 事象であって
   floor 事象でないことをも裏付ける)。
6. **below-band 子 (floor 10): H(17;Y;17) = v(s,17,17) が 221 形状で完全
   崩壊** (0 deviant・0 multivalue)。出版 floor-11 版 (183 形状) より広い
   min(Y)>=10 域まで完全崩壊が拡張 — K1320 補題 BB 族の z=16 floor-10
   analog の観測的成立。

## honest 記録

1. 本 kit は z17-min12 kit と同一実行内で構築 (両 kit は独立した観測対象:
   z=17 floor-12 census と z=16 floor-10 census。重複セクションなし:
   m=10 行 z=17 は z17 kit (d2)、m=10 行 z=16 は本 kit A4 ランク)。
2. 中間走 (run_test) は 3 走取り直しの前に破棄。凍結 .out bytes は最終
   script 由来のみ。`env -i` 走は `/usr/local/bin/python3` 明示 (rc127 教訓)。
3. m=9 z=17 frontier (z16-min9 kit 出版済み) との重複測定なし。
4. すべて pinned engine の有限機械観測。定理・全称主張なし。いかなる
   verdict も消費しない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2
   {59,60}・class 1/2/4 は全時点 UNKNOWN のまま。**

## 次の実行への申し送り (着手前に必ず最新 main 再取得)

(a) **m=10 行閉鎖宣言候補**: 本 kit の A416f10 全域崩壊 + 出版 (d) 130/0 +
   z17 kit (d2) の z=17 側 130/0 + tail 8/8 で、宣言レーンは
   「m=10 行 z∈{16,17} 閉鎖」(H(27;X;16)=v(ΣX,16,27) for all min=10;
   H(28;X;17)=v(ΣX,17,28) for all min=10) の紙面証明を検討できる。梯子は
   本 kit の 10 セル表が供給構造 (s=10 復活クラス {B,A,A2} と A3/A4 崩壊)。
   z=17 側の行証明には z=17 floor-10/11 版のセル族が別途必要になる可能性
   (z17-min12 kit は floor-12 のみ) — 宣言の scope 決定時に注意。
(b) **S 系 (死点化) の解釈更新**: K1322 完了 log・z17-min12 log の
   「死点化」記述は「床による census 定義域から s=10 クラスが除外される
   こと」の観測的表現であり、z 遷移がクラスを消すわけではない (本 kit
   実測)。次のスライス編集時に反映。
(c) **同型の次 kit 候補**: m=9 行 z=16 の floor-9 版 (F16f9..A316f9 は出版
   済み 9 セル — 同一実行対象外)、m=11 行 z=17 の floor-11 版 (z17-min12
   は floor-12 のみで m=11 行 z=17 の証明用セル族は未探査)。
(d) K1323 以降の採番は最新 main の items 最高番号で再確認 (並走 conic
   lane が「K1321」別 item を持つ双重刊番状況に注意・AGENTS.md 再採番規則)。
(e) **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
   全時点 UNKNOWN・verdict 不消費・本 kit の全 census は主張前の観測**。
