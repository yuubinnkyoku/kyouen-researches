# 2トークン残余ゲーム y=13族パラメトリック閉形式候補 cand13 の fitting と box 外 spot 検証（2026-11-20 高速レーン）

単一オーナー宣言（[先行出版](../../log/2026-11-20-y13-two-token-skeleton-single-owner-note.md)・2026-11-20T22:16:00Z・commit 4bdff59）に基づく y=13 族着手の第一段階。
H(R;(x,13);z) について、z 偶奇・x 偶奇別のパラメトリック T/P 集合表（閉形式候補 cand13）を生二重再帰 probe から導出し、
probe box 全点 72,664 点・box 外 spot 4,959 点・merge 回帰 10,608 比較・tail assertion 12,896 点で
生エンジン・出版単一トークン閉形式（K0832）と完全一致（不一致 0・T/P 重複 0）を確認した。
シードは y=10 族（[K1141](../../knowledge/items/K1141-two-token-y10-parametric-closed-form-fit.md)）、y=11 族
（[K1143](../../knowledge/items/K1143-two-token-y11-parametric-closed-form-fit.md)）、y=12 族
（[K1152](../../knowledge/items/K1152-two-token-y12-parametric-closed-form-fit.md)・いずれも全称証明済み）の構造則だが、
y=13 では**族系列で初めて主要な族式の多くが破れ、3つの新レジーム（小z x錨定・slope 1 pin・merge 中心 S−2）が出現した**
（下記）。本段階は有限 fitting と spot 検証のみであり、全称証明（正本検証器・型機械・census）は含まない。

## 命題候補（observed・有限範囲で確定・全称は未証明）

すべての z>=0・x>=13・R>=0 に対して H(R;(x,13);z) = cand13(z,x,R)。cand13 は以下の T/P 集合表
（`cand13.py` が正本・Y=13・b_k = 奇 offset {1,3,...,2k-1}・I[t] = offset t 以上連続・offset o = R-z・d = x-z）。

### 値2集合 in_T13（probe 72,664 点で mismatch 0・probe box 内に値3は出現せず値域 {0,1,2}）

- ラダー: 奇z 奇R O[1,z]／偶z 奇R O[1,z-1]（族式どおり・y=10..12 と同一）
- 深帯 d<=-12（x<=z-12）: 単一トークン single_token(x+11) の値2そのもの O[1, q_odd(x+11)]
  （**merge 中心が族式 x+y=S でなく S-2=x+11・境界も族式 x<=z-(y+1)=z-14 でなく 2 列浅い x<=z-12**）
- d=-11 遷移行: z奇(x偶) 偶offset [2,10]／z偶(x奇) 奇offset [1,11]（ラダーに加算される固定短帯）
- 遷移層 z=13（A・d=0 x偶・x=13 のとき pin {x+8,x+10}）: 偶offset pin 2 点 {z+d+21, z+d+23}（二重 pin・y13 初出）
- 遷移層 z=14（C・x奇）: 偶offset pin 2 点 {z+d+22, z+d+24}（二重 pin）
- 汎用 pin: A（z奇 x偶 z>=15）単一 pin z+d+21（d は全奇数・mod 4 制限なし）／
  C（z偶 x奇 z>=16）単一 pin z+d+22（d 全奇数）。**pin の d-slope が 1/2（族式 z+(d+3y)/2）から 1 に変化**し、
  pin 行が d≡y (mod 4) の格子でなく全 d 行に現れる
- 掃引行 d=y+1=14・定常行 d>=15 は**存在しない**（y=10..12 にあった band/定常 pin が y13 では生成しない。
  大 d 側は B/D の base+interval が tail へ連続移行・spot で d=35/60 まで照合）

### 値1集合 in_P13（probe 全点で mismatch 0・Tとの重複 0）

- 深帯 d<=-12: single_token(x+11) の値1そのもの。x 偶の行のみ I[x+12, infty)
- d=-11 遷移行: z奇(x偶) 奇offset {1..11} ∪ I[12]／z偶(x奇) 値1なし
- **小z x錨定レジーム（y13 で初観察・行が d でなく x だけで決まる）**:
  - A（z奇 x偶 z<=13）: P = 奇offset 全域 ∪ I[x+11)
  - D（z偶 x偶 z<=12）: P = 奇offset 全域 ∪ I[x+11)（A と同一式）
  - B（z奇 x奇 z<=13）: P = 奇offset {1..x+10}（有限 base・tail なし）
  - C（z偶 x奇 z<=12）: P = 奇offset {1..x+10}（B と同一式）
  - x+10/x+11 は single_token(x+11) の cap/band 開始と同じ指数（小zでは 2 トークンの相互作用が消失し
    x 錨定の単一トークン型に潰れるという横断法則候補）
- 遷移層 z=14（C）: P = 奇offset {1..d+20}（d錨定に転換・pin 2 点は別置き）
- 汎用レジーム（d錨定）:
  - A（z奇 d奇 z>=15）: k=(d+23)//2・P = b_k ∪ I[2k, infty)（th=2k=d+23・必ず偶）
  - D（z偶 d偶 z>=14）: k=(d+22)//2・P = b_k ∪ I[2k, infty)（th=d+22・偶）
  - B（z奇 d偶 z>=15）: P = 奇offset {1..d+21}（有限 base）
  - C（z偶 d奇 z>=16）: P = 奇offset {1..d+20}（有限 base・pin 別置き）
  - base rank k(d) の d-slope は 1/2（y=10..12 は 1/4）・飽和なし
- tail: R>=x+z+14（= x+z+y+1）の値 (x+13) mod 2・値1無限帯と tail は x 偶行（y=11 と同じ奇数 y 型）。
  probe 12,896 点全一致。

### 初稿からの修正点（fitting 反復の記録）

y=10..12 族式の素直な外挿初稿（merge 中心 x+13・pin 式 z+(d+39)/2・base k=(d+40)/4 相当）は
probe 72,664 点中 11,151 点不一致（深帯の merge 破れと小z層の大部分）。
修正 1（深帯 single_token(x+11) と d=-11 遷移行の導入）で 763 点残り、
残りはすべて z<=13/14 の遷移層と小z行に集中していたため、クラス別 (z,x) 偶奇 4 分割×(小z/遷移/汎用) の
全レジーム再分析で**小z x錨定レジームを発見**して全面改訂し全点一致に到達した（修正 2）。
最終 selfcheck では negative offset（R<z では off=R-z が負で Python の負奇数剰余が True を返す）の
pbase ガード 1 行を追加して mismatch 0・overlap 0 確定。

## マージ系（対角線下・y=13 の回帰）

x <= z-12 の probe 1,449 点が行全体で single_token(x+11)（K0832 出版閉形式の第3実装相当）に一致
（値0/1/2 すべて・不一致 0・対角線 d=-13 は深帯に吸収され『対角行 cap 族式 z+y-[z≡y mod 2]』の
適用行が y13 では消滅）。box 外では cand13 と single_token(x+11) の直接回帰 10,608 比較
（z=0..40・x=13..z-12・R<=x+z+26）も不一致 0。
**族式マージ命題 x<=(z-(y+1))→single_token(x+y) は y=13 では有限 fit 内で破れている**
（x=z-13, z-14 の行がすでに single_token(x+11) に従い・なお境界 2 列分は汎用側に残る d=-11 遷移が担当）。

## 検証規模（本 report の時点・合計 88,231 点比較 + tail affirmation 12,896 点・不一致 0）

- probe box: z=0..30・x=13..z+29・R<=x+z+26 の生二重再帰 992 行・72,664 点
  （`probe_rows.txt` RLE・本 repo には未公開・`probe_y13.py` で決定論的に再生可能・約 3.5 秒）
  - cand13 全点一致（mismatch 0・T/P 重複 0・値頻度 0:35,658 / 1:27,709 / 2:9,297・値3なし）
  - tail assertion R>=x+z+14 → (x+13) mod 2 の領域 12,896 点一致
  - merge assertion x<=z-12 → single_token(x+11) の 1,449 点一致
- box 外 spot（`spot_y13.py`・約 8.9 秒）: 生エンジン直接照合 4,959 点 bad 0
  - ext-z: z=31..40 × {x=z-20（深帯）, z-11（遷移）, z-5, z+3（汎用）} × R<=min(x+z+26,120)（3,412 点）
  - large-d/ext-R: z∈{3,12,13,14,15,16,20,30} × x=z+35/z+60 × R<=min(x+z+26,120)（1,414 点）
  - edge x=13: z=25,30 × R<=x+z+26（133 点）
  - merge 回帰グリッド（cand13 vs single_token(x+11)・z=0..40・x=13..z-12・R<=x+z+26）10,608 比較不一致 0
- 決定性: probe_rows.txt は別実行再生成で byte-identical。要件・監査数値は `output/audit.json` に SHA-256 付きで記録。

## y=10..12 出版表との横断判定（有限範囲・全称ではない）

- 成立（y=13 で追加確定）:
  - tail 開始族式 x+z+y+1（y=13 で x+z+14・y=2..13 の 12 族連続の支持例）
  - tail 値 (x+y) mod 2・値1無限帯が x 偶行（y 奇族型・y=11 と同型・「y の偶奇が行型を決める」13 族連続）
  - ラダー族式・値域 {0,1,2}・probe box 内に値3なし
  - 偶 z 側値1全欠如系（y=8..13 で 6 族連続・ただし y=13 では x 奇深帯 single_token(S 偶) からの帰結として成立）
- 破れ（y13 で初・y=5..12 の族系列が y=13 で途切れた）:
  1. マージ中心 S-2（x+11 ≠ x+y）・境界 x<=z-12（≠ z-(y+1)）
  2. pin 統一式 z+(d+3y)/2 の不成立（y13 の pin は slope 1 の z+d+21/z+d+22・全 d 行・mod 4 格子なし・8族連続が y13 で停止）
  3. 掃引行・定常 pin 行の不生成（大 d は base+interval の連続的拡大のみ）
  4. base rank k(d) が slope 1/2（y=10..12 は 1/4）・基底点 y 点仮説の直接対応なし
     （小zレジームの cap x+10/x+11 が代わりに現れる）
  5. 奇 z I 帯 th: y=10 は 2k・y=11 は 2k+1・y=12 は連続整数掃引だったのに対し、y13 は A/D とも th=2k 偶・slope 1
- 新規（y13 固有・初観察）:
  6. 小z x錨定レジーム（z<=y 内は d 非依存・single_token(x+11) 型指数で潰れる）
  7. d=-11 遷移行（固定帯 [2,10]/[1,11] と I[12)/空 の偶奇分割）
  8. z=13/14 の二重 pin 遷移層（汎用単一 pin への橋渡し）

## 次段階（範囲外の明示）

- 全称段階: verify_y13_universal.py（正本検証器・A子 H(R-1;(x-1,13);z)・B子 出版 cand12 逐語転写
  （x=13 合流子 (12,13)≡(13,12)）・C子 1 xor cand13(z-1,x,R-1)・型機械 clip 窓 2y+2=28 の tight 判定、
  census z=0..79・x=13..70）は本実験の範囲外・別宣言で着手可能。
- clip 窓族式候補 2y+2=28 は fit 段階では予想のみ（型機械は範囲外）。
- 標準 11×11 の空盤勝敗・二石 root・S2 {59,60} には一切言及しない。
- 3トークン以上・y>=14 族・固定幅・q点版・fold 系は対象外。
