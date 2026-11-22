# 2トークン残余ゲーム y=13族パラメトリック閉形式候補 cand13 の fitting（2026-11-22 高速レーン）

単一オーナー宣言（[宣言ノート](2026-11-22-y13-two-token-skeleton-single-owner-note.md)・2026-11-22T17:01:05Z・commit d3404db8）に基づく
y=13 族着手の第一段階（fitting）の記録。正本は
[実験dir](../experiments/vertical-fiber-two-token-y13-parametric-allz-fit-20261122/report.md)・
知識項目は [K1231](../knowledge/items/K1231-two-token-y13-parametric-closed-form-fit.md)。

## 採番

push 直前に最新 main を再取得し、README 末尾 bullet が K1230 までであること・
items 一覧に K1231 が存在しないこと（K1231 ファイル直接 404・README grep 空）を
確認して K1231 に採番した。

## 経緯

1. K1152（y=12 族全称証明・同レーン成果）の横断観察セクション「次段階の判定材料」が
   y=13 fit での横断型（pin スロット=th-1 型・y 奇族の行型）の追完を明示的に指名しており、
   y>=13 族は K1152 の全称範囲外で本高速レーンに残されていたため、y=13 fit を最優先課題として選定。
2. probe（`probe_y13.py`・y=11/y=12 版 probe の正当写し・Y=13・x range(13, z+30)・merge marker x<=z-14）を
   実行し、992 行・72,664 点・約 5.1 秒で probe_rows.txt を生成（別 cwd 再生成で byte-identical を確認）。
3. y=11 族出版表（K1143・y=13 と同じ y 奇型の直接テンプレート）の族法則を
   Y=13 に外挿した予想表 cand13.py を実装。y=10/y=12 出版表（K1141・K1152）の pin 行を
   横断して導いた **pin 格子統一式 o_pin=(d+3y)/2∈[y+1,2y]・o_pin≡z+1 (mod 2)** を中心に
   奇z o_pin 偶（d∈{-11,-7,-3,1,5,9,13} の 7 行・y 奇族初の 7 行）・偶z o_pin 奇
   （d∈{-9,-5,-1,3,7,11} の 6 行）を配置。
4. `cand13.py`（z 偶奇別 T/P テーブル・Y=13）の probe 全点照合:
   **初稿から一発で probe points: 72664 mismatch: 0 overlap: 0**
   （値頻度 0:35,581 / 1:27,281 / 2:9,802・値3なし）。
   y=12 fit が外挿初稿から 240 点の修正を要したのと対照的で、y=11 に続き 2 例目の
   一発一致。奇数 y 族のテンプレート外挿が Y+2 にそのまま伸びることが fitting レベルで確定。
5. `spot_y13.py`（box 外 spot）: 深 R<=130 の代表 15 行（対角・pin・掃引・定常・マージ合流境界）・
   大 z=31..40 × 代表 22 d・x=y=13 エッジ（z=13..40・R<=z+130）・大 d∈{30,41,52} の
   31,750 点 bad 0・約 22.4 秒。merge 回帰（cand13 vs K0832 single_token・x=13..z-14・R<=x+z+29）
   17,277 比較不一致 0。tail raw 回帰（d>=14 の 6 行・R∈[x+z+14, x+z+27]）84 点 0。
6. 合計 121,775 点比較・不一致 0・決定論的（純 Python 標準ライブラリのみ）。
7. K1152 の横断型の問いへの回答（fit レベル）: 奇z pin 行 7 行すべてで pin が off=2k=th-1
   （k=base rank floor((d+40)/4)）をちょうど占有する「pin スロット=th-1」型が y=11/12/13 の
   3 族連続で確定。最終 pin 行 d=13=y は I[2y+z+1)=I[27,∞) 型（pin off 26 skip・7 族連続候補）。
   偶z 対角行 d=-13 の値1全欠如は y=8..13 の 6 族連続候補。band 下端 2y+2=28・
   定常 pin z+26/z+27・基底点 z+1..z+25 の 13 点も族式どおり。
8. 出版: 単一オーナー宣言ノート（commit d3404db8）→ 実験 dir 5 ファイル
   （commit 2287399）→ commit-pinned fetch-back 検証で report.md・audit.json に
   転写スリップ 5 箇所を検出し正本側を修正・fix コミット（commit 76a4f28）で再出版・
   fetch-back 再検査で両ファイルともローカル正本と byte 一致
   （report sha 3da1538c・audit sha 795c37ff）を確認。

## 主要な観察（全て fitting レベル・全称ではない）

- **pin 格子統一式（本 fit の主眼・新規の横断式）**: o_pin=(d+3y)/2∈[y+1,2y]・o_pin≡z+1 (mod 2) の
  単一式が y=10/y=11/y=12 の出版 pin 行集合（d 基準 mod 4 則・行範囲）をすべて正確に再現し、
  y=13 では 奇z 7 行／偶z 6 行を与える。偶z pin 行数が y 奇族で初めて 5 行→6 行に増加。
- 「pin スロット=th-1」型が y=11/12/13 の 3 族連続（K1152 指名の問いに fit レベルで回答）。
  偶z 側 slot 則（pin=base 上端 2k-1 の +2 位置）も 3 族同一。
- 横断族法則（tail 開始 x+z+y+1 の 12 族連続・基底点 y 点 13 例目・マージ境界 x<=z-(y+1)・
  対角 cap=z+y-[z≡y mod 2]・定常 pin 2y+z/2y+z+1・band 下端 2y+2=28）が y=13 でも全て成立。
- base 行 rank 族式 k(d)=floor((d+3y+1)/4) が y=10/11/12/13 の 4 族で全 base 行同一。
  偶z I 帯 k(d)=floor((d+3y-1)/4) が y=11/12/13 の 3 族同一。奇z th=2k+1 は奇 y 族 3 例目
  （y 偶奇が th 則を決める観察・y=10 は 2k・y=12 は連続整数掃引）。

## trust 境界

本成果は有限 fitting と spot 検証であり全称定理ではない。cand13 が全 z>=0・全 x>=13・全 R>=0 で
成り立つという主張は次段階の 12 チェック監査（A子=H(R-1;(x-1,13);z)・B子=K1152 の cand12
逐語転写〔B子に全称証明済み族を使う初の序列〕・C子=1 xor cand13(z-1,x,R-1)・
x=13 合流子 (12,13)≡(13,12)・型機械 clip 窓 2y+2=28〔9 族 tight 連続候補〕・
census z=0..79・x=13..70）で判定する。3 トークン以上・y>=14 族・固定幅・q 点版安定化長・
標準 11×11 は範囲外。
