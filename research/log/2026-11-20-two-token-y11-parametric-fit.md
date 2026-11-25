# 2トークン残余ゲーム y=11族パラメトリック閉形式候補 cand11 の fitting（2026-11-20 高速レーン）

単一オーナー宣言（[宣言ノート](2026-11-20-y11-two-token-skeleton-single-owner-note.md)・2026-11-20T11:58:00Z・commit ed778278）に基づく
y=11 族着手の第一段階（fitting）の記録。正本は
[実験dir](../experiments/vertical-fiber-two-token-y11-parametric-allz-fit-20261120/report.md)・
知識項目は [K1143](../knowledge/items/K1143-two-token-y11-parametric-closed-form-fit.md)。

## 採番

push 直前に最新 main を再取得（HEAD 259e4019・2026-11-20T12:02:53Z）し、README 末尾 bullet が K1142 までであること・
items 一覧に K1143 が存在しないことを確認して K1143 に採番した。

## 経緯

1. probe（`probe_y11.py`・y=10 版 probe_y10.py の正当写し・Y=11・x range(11, z+28)・merge marker x<=z-12）を
   実行し、992 行・70,680 点・約 4.8 秒で probe_rows.txt を生成。
2. `extractor.py`（行別 T/P offset 構造抽出ツール）で z 奇 31 行・z 偶 31 行の全 d を横断し、
   y=10 族表（K1141）の予想（対角 cap・pin 格子・th ジグザグ・掃引・定常・tail・band 下端）を実データで検定。
   - 予想どおりだったもの: 対角 cap = z+y-[z≡y mod 2]（奇z z+10／偶z z+11・両偶奇で初めて直接確認）・
     pin = z+(d+33)/2（奇z d≡3 mod 4: {-9,-5,-1,3,7,11} の 6 行・偶z d≡1 mod 4: {-7,-3,1,5,9} の 5 行）・
     掃引行 d=12 の帯 O[2y+z, x+z+y]／O[2y+z+1, x+z+y]・定常 pin z+22/z+23・基底点 11 点 {z+1..z+21}・
     band 下端 2y+2=24・tail R>=x+z+12 値 (x+11) mod 2・マージ境界 x<=z-12・偶z 対角行の値1全欠如（4 族連続）。
   - 予想から修正したもの: 奇z の th ジグザグが単一式 k(d)=floor((d+34)/4)（th=2k+1・最終 pin 行で I[23)）で
     全行統一される点（y=10 にあった d=y 行の飽和が y=11 では発生しない）。偶z の I 帯行は
     k(d)=floor((d+32)/4) の別式（+2 シフト）。定常 I 行の I 帯は th ではなく tail 開始 x+z+12 そのもの
     （band 偶offset [24, x+10] ∪ I[x+12, ∞) に分解される）。
   - 宣言ノートの予想表（pin 行 6/5・掃引 d=12・定常 pin z+22/z+23・対角 cap・tail）は全て的中。
3. `cand11.py`（cand10.py を写した z 偶奇別 T/P テーブル・Y=11）を実装し、probe 全点照合:
   **初稿から一発で probe points: 70680 mismatch: 0 overlap: 0**（値頻度 0:34,618 / 1:26,301 / 2:9,761・値3なし）。
4. `spot_y11.py`（box 外 spot・y=10 版の正当写し）: 深 R<=130 の 9 行・大 z=31..40×代表 17 d・
   x=y=11 エッジ（z=11..40・R<=z+130）・大 d∈{30,41,52} の 28,238 点 bad 0・約 21.8 秒。
   merge 回帰（cand11 vs K0832 single_token・x=11..z-12・R<=x+z+29）26,015 比較不一致 0。
   tail raw 回帰（d>=13・6 行・R∈[x+z+12, x+z+25]）84 点 0。
5. 合計 125,017 点比較・不一致 0・決定論的（純 Python 標準ライブラリのみ）。

## 主要な観察（全て fitting レベル・全称ではない）

- y=10（K1141・全称証明済み）の表と、S=x+y の偶奇による行型反転（y=11 は y 奇型: 値1無限帯・tail は x 偶の行）と
  pin 格子の d≡y (mod 4) シフトを除けば同一構造。横断族法則（tail 開始 x+z+y+1・基底点 y 点・マージ境界
  x<=z-(y+1)・対角 cap・pin 統一式・掃引帯・定常 pin・band 下端 2y+2）が y=11 でも全て成立し、
  tail x+z+y+1 は 10 族連続・pin 統一式は 7 族連続・基底点 y 点は 11 例目・偶z 対角行値1全欠如は 4 族連続・
  最終 pin 行 d=y の I[2y+z+1) 型は 5 族連続。
- clip 窓族式候補 2y+2 の y=11 値 24（±24/番兵±25）が band 下端として出現。型機械での tight 判定は次段階。
- 奇z pin 行が 6 行（y 奇族で (y+1)/2 行）になるのは初例（y=9 は 5 行）。偶z は 5 行のまま。

## trust 境界

本成果は有限 fitting と spot 検証であり全称定理ではない。cand11 が全 z>=0・全 x>=11・全 R>=0 で成り立つという
主張は次段階の 12 チェック監査（A子=H(R-1;(x-1,11);z)・B子=K1141 の cand10 逐語転写〔B子に全称証明済みの
y=10 を使う初の族〕・C子=1 xor cand11(z-1,x,R-1)・x=11 合流子 (10,11)≡(11,10)・型機械 clip 窓 2y+2=24・
census z=0..79・x=11..70）で判定する。3 トークン以上・y>=12 族・固定幅・q 点版安定化長・標準 11×11 は範囲外。
