# 単一オーナー宣言: 2トークン残余ゲーム y=7族パラメトリック全称証明

- 宣言時刻: 2026-11-20T07:02:30.071Z（HEAD 71b9d079・n11: declare single owner for WIN8 receipt fold root 0000000）
- 作業: y=7族の同型機械化。K1127（y=6族パラメトリック全称証明）の完成を受け、
  K1023(y=1)→K1099(y=2)→K1104(y=3)→K1112(y=4)→K1126(y=5)→K1127(y=6)に続く
  高速レーン第7族の実行である。
- 範囲: 全z>=0・全x>=7・全R>=0で H(R;(x,7);z)=cand7(z,x,R)（z偶奇別パラメトリック
  T/P集合表）の導出・全称証明・独立監査。マージ行 x<=z-8 の単一トークン閉形式
  一致（マージ命題のy=7版の全称昇格・y=1..7拡張）、値1基底点7点
  {z+1,z+3,z+5,z+7,z+9,z+11,z+13}（基底点y点仮説のy=7版）、tail R>=x+z+8 の
  (x+7) mod 2（tail開始族式 x+z+y+1 のy=7帯・奇数yへの復帰で値1無限帯は偶数x行）、
  掃引行 x=z+8、中間帯下端 2y+z+2=z+16、前倒しpin格子公式
  pin=2y+((x-y)+z)/2〔(x-y)+z≡2 mod 4〕・pin行 d≡y (mod 4)（奇z）/d≡y+2 (mod 4)（偶z）
  のy=7版、対角行 x=z-7 の格子規則 r=z+y-[2(z-y)≡0 mod 4]、
  clip窓のy=7要件式（2y+2=16候補・y=6の±14/±15からの広げ直し）を含めて
  横断法則候補のy=7検証が最初の関門である。
- 子の参照: A子は同切片x-1行（x=7では(6,7)≡(7,6)合流でK1127のy=6族x=7行）、
  B子はK1127のcand6（出版済み・SHA pin済み・repo実験dirが正本）、
  C子は1⊕cand7(z-1,・,・)のz外帰納。すべて出版済み機材の上に閉じる。
- 予定実験dir: research/experiments/vertical-fiber-two-token-y7-parametric-allz-proof-20261120/
  （report.md・verify_y7_universal.py・census_rows.py・output/audit.json・output/census.txt）
- 予定log: research/log/2026-11-20-two-token-y7-parametric-allz-proof.md
- K番号: 仮番号は使用しない。push直前に3点確認（README grep・items 404・list_commits）
  で空きを取得する。
- 並走レーン（n11 fold/extract・K1058円整数論・6行q=8 band-closure〔宣言7bc633a6〕）
  との経路不競合を確認済み。y=7族に関する宣言は他レーンに存在しない。
- y<=6族と異なる点（y=7で新規に現れうる差異・特にpin行の個数とclip窓拡張の必要性）
  は予備probeで確認してからcand7を固定する。
  有限観察・ヒューリスティック・全称証明を明確に区別する。
