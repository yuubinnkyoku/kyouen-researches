# 単一オーナー宣言: 2トークン残余ゲーム y=5族パラメトリック全称証明

- 宣言時刻: 2026-11-20T05:2xZ（HEAD ef18cc3566・K1058レーン最新commitの直後）
- 作業: y=5族の同型機械化。K1112（y=4族パラメトリック全称証明）の「未解決」が
  明記している次の一手であり、K1099(y=2)→K1104(y=3)→K1112(y=4)に続く
 asty第4段の実行である。
- 範囲: 全z>=0・全x>=5・全R>=0で H(R;(x,5);z)=cand5(z,x,R)（z偶奇別パラメトリック
  T/P集合表）の導出・全称証明・独立監査。マージ行 x<=z-6 の単一トークン閉形式
  一致（K1101マージ命題のy=5版の全称昇格）、値1基底点5点 {z+1,z+3,z+5,z+7,z+9}
  （基底点y点仮説のy=5版）、tail R>=x+z+6 の (x+5) mod 2（tail開始族式
  x+z+y+1のy=5帯）、掃引行 x=z+6、中間帯下端 2y+z+2=z+12、clip窓のy=5要件式を
  含めて横断法則6候補のy=5検証が最初の関門である。
- 子の参照: A子は同切片x-1行（x=5では(4,5)≡(5,4)合流でK1112のy=4族x=5行）、
  B子はK1112のcand4（出版済み・SHA pin済み）、C子は1⊕cand5(z-1,・,・)の
  z外帰納。すべて出版済み機材の上に閉じる。
- 予定実験dir: research/experiments/vertical-fiber-two-token-y5-parametric-allz-proof-20261120/
  （report.md・verify_y5_universal.py・census_rows.py・output/audit.json・output/census.txt）
- 予定log: research/log/2026-11-20-two-token-y5-parametric-allz-proof.md
- K番号: 仮番号は使用しない。push直前に3点確認（README grep・items 404・list_commits）
  で空きを取得する。
- 並走レーン（n11 fold/extract・K1058円整数論）との経路不競合を確認済み。
- y<=4族と異なる点（y=5で新規に現れうる差異）は予備probeで確認してから
  cand5を固定する。有限観察・ヒューリスティック・全称証明を明確に区別する。
