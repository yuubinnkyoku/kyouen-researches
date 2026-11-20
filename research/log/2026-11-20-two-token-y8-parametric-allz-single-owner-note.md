# 単一オーナー宣言: 2トークン残余ゲーム y=8族パラメトリック全称証明

- 宣言時刻: 2026-11-20T07:44:44.643Z（HEAD 9c156ea3・K1131 y=7族出版直後）
- 作業: y=8族の同型機械化。K1131（y=7族パラメトリック全称証明）の完成を受け、
  K1023(y=1)→K1099(y=2)→K1104(y=3)→K1112(y=4)→K1126(y=5)→K1127(y=6)→K1131(y=7)に続く
  高速レーン第8族の実行である。
- 範囲: 全z>=0・全x>=8・全R>=0で H(R;(x,8);z)=cand8(z,x,R)（z偶奇別パラメトリック
  T/P集合表）の導出・全称証明・独立監査。マージ行 x<=z-9 の単一トークン閉形式
  一致（マージ命題のy=8版の全称昇格・y=1..8拡張）、値1基底点8点
  {z+1,z+3,z+5,z+7,z+9,z+11,z+13,z+15}（基底点y点仮説のy=8版）、tail R>=x+z+9 の
  (x+8) mod 2（tail開始族式 x+z+y+1 のy=8帯・偶数yへの復帰で値1無限帯は奇数x行・y=6型）、
  掃引行 x=z+9、中間帯下端 2y+z+2=z+18、前倒しpin格子公式
  pin=2y+((x-y)+z)/2〔(x-y)+z≡2 mod 4・pin行 d≡y (mod 4)（奇z）/d≡y+2 (mod 4)（偶z）
  のy=8版・y=8はd≡0(奇z)/d≡2(偶z)〕、対角行 x=z-8 の格子規則 r=z+y-[2(z-y)≡0 mod 4]、
  clip窓のy=8要件式（2y+2=18候補・y=7の±16/±17からの広げ直し）を含めて
  横断法則候補のy=8検証が最初の関門である。
- 子の参照: A子は同切片x-1行（x=8では(7,8)≡(8,7)合流でK1131のy=7族x=8行）、
  B子はK1131のcand7（出版済み・verify_y7_universal.py SHA-256
  9200b591a30adf74dd62015ee11cb31d1bb37d9f1f0c00a626ebce9106d87abb・repo実験dirが正本）、
  C子は1⊕cand8(z-1,・,・)のz外帰納。すべて出版済み機材の上に閉じる。
- 予定実験dir: research/experiments/vertical-fiber-two-token-y8-parametric-allz-proof-20261120/
  （report.md・verify_y8_universal.py・census_rows.py・output/audit.json・output/census.txt）
- 予定log: research/log/2026-11-20-two-token-y8-parametric-allz-proof.md
- K番号: 仮番号は使用しない。push直前に3点確認（README grep・items 404・list_commits）
  で空きを取得する。
- 並走レーン（n11 fold/extract・K1058円整数論・その他）との経路不競合を確認済み。
  y=8族に関する宣言は他レーンに存在しない（K1131のreport/logはy>=8を範囲外と明記）。
- y<=7族と異なる点（偶数yへの復帰でP表の値1無限帯の偶奇がy=6型＝奇数x行に戻る・
  pin行の個数・clip窓±18/番兵19への広げ直しの必要性）は予備probeで確認してから
  cand8を固定する。有限観察・ヒューリスティック・全称証明を明確に区別する。
