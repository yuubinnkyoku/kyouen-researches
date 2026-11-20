# 2トークン残余ゲーム y=12族パラメトリック fitting の経過記録（2026-11-20 高速レーン）

[単一オーナー宣言](2026-11-20-y12-two-token-skeleton-single-owner-note.md)（2026-11-20T14:25:00Z・commit fe93c969・先行出版）に基づく
y=12 族 fitting（[実験](../experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/report.md)・
K item [K1150](../knowledge/items/K1150-two-token-y12-parametric-closed-form-fit.md) として出版）の経過・判断の記録。

## 初稿と不一致プロファイル

初稿は y=10 published 定数表（K1141 verify_y10_universal.py）と y=11 fit 正本（K1143）
からの構造則の素直な引き伸ばし: PINS_ODD={-8,-4,0,4,8,12}・PINS_EVEN={-10,-6,-2,2,6,10}・
K_I_odd=(d+38)//4・K_B_odd=(d+37)//4・K_I_even=(d+36)//4・K_B_even=(d+33)//4・
z 偶数 I 開始 off>=2k・z 奇数 I 開始 off>=2k。
probe（z=0..30・x=12..z+28・R<=x+z+26・992 行・71,672 点・約 3.4 秒・71,672 点中値3なし）に対して
**不一致 240 点・T/P 重複 48**。不一致は (0, d) の (z 偶, すべての d∈[-11,12]) に分布
（d=12 で 16 点・d=-11 で 4 点・単調減少）で、**z 奇数行は全点一致**していた。

## 行型抽出による原因の特定

probe 行ごとの value-2（ladder 外=pin）offset・value-1 の基底奇数連続長 k・
行末尾 contiguous 帯の抽出表（`table.py` 相当・z=0..30 偶数の全行）と
代表行の (R: 値) 生 decode（z=20 x=12/14/24、z=8 x=20/22、z 奇数対照行）から:

1. **偶z base 行（d 偶）の k は (d+33)//4 ではなく (d+37)//4**（例: z=20 d=4 → off19 上端、
   z=22 d=-10 → off11 上端・pin13=上端+2）。
2. **偶z I 帯行（d 奇）は k=(d+35)//4・th=2k+1**（I 開始は 2k ではなく 2k+1。
   th は 13,13,15,15,...,23,23。z=2 d=1 で off22=0 が初稿誤りの直接反例）。
3. **奇z 側は th を 1 行 1 类に割り当て直すと (d+3y)/2 スロットが th-1 に落ちる**:
   d≡0 (mod 4) ではスロット=偶 offset=pin（値2）、d≡2 (mod 4) ではスロット=奇 offset=b_k 上端（値1）。
   生 decode で z=21 x=13（d=-8）off14=2・off15=1・z=5 x=17（d=12）off24=2・off25=1・
   z=13 x=15（d=2）off20=1・off18=0 を確認。**th(d)=ceil((d+37)/2)** の連続整数掃引
   （13,14,...,25）にまとまった。
4. 対角 d=-12 偶z（旧想定どおり値1全欠如・pin{1..11}）と merge 行・tail 回帰は初稿から不変。

## 検証（[実験 report](../experiments/vertical-fiber-two-token-y12-parametric-allz-fit-20261120/report.md) に全文）

probe 71,672 点（mismatch 0・T/P 重複 0・値頻度 0:35,102/1:26,780/2:9,790）＋
box 外 spot 26,272 点 bad 0（深 R<=130・大 z=31..40・x=y=12 エッジ・大 d∈{30,41,52}）＋
tail raw 84 点＋merge 回帰 16,542 比較の計 114,570 点比較・不一致 0。
probe_rows.txt は別 cwd 再生成 byte-identical・audit.json は 3 実行 byte-identical。

## 横断観察（y=6..12 の pin 格子・族式の確定）

- 横断 pin 法則（pin=z+(d+3y)/2・d≡y (mod 4) 奇z／d≡y+2 (mod 4) 偶z）が y=12 で 8 族連続。
- 奇z pin 行 d 範囲 [−y+4, y]（y 偶）4 族的確定（6/8/10/12・y=11 は 6 行で同数）。
- 偶z pin 行 d 範囲 [−y+2, y−2]（y 偶）4 族的確定（6/8/10/12）。**偶z 6 行は y=12 が初例**。
- base 行 k(d)=floor((d+3y+1)/4) が y=10/11/12 の base 行全部で同一。
- 偶z I 帯行 k(d)=floor((d+3y−1)/4) が y=11/12 で同一（y=10 は (d+3y+3)/4）。
- 奇z I 帯 th は y=10: 2k・y=11: 2k+1・y=12: ceil((d+3y+1)/2)（連続整数）で、
  y=11/y=12 は「pin が th−1 を占有」型・y=10 は th−2 型。y=13 fit でどちらに付くかが
  横断型決定の次の判定材料（[margin 塔分析](2026-11-20-two-token-general-laws-regime-subsumption-note.md)と接続）。

## 出版と採番

- 実験 5 ファイル（report.md・cand12.py・probe_y12.py・spot_y12.py・output/audit.json）を part1、
  本 log と K item を part2、knowledge README bullet を part3 として main に直接出版。
- K番号は push 直前に 3 点確認（README 実ファイル grep・item 404・list_commits）で採番した。
  確認時点の README 掲載最大は K1149（ただし K1149 は二重採番・未解消の記載があるため
  後続番号 K1150 を使用）。
- cand12 の正本監査（verify_y12_universal.py・12チェック）は宣言の保持範囲外・次段階。
