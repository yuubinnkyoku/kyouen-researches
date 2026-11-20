# 単一オーナー宣言: 2トークン残余ゲーム y=6族パラメトリック全称証明

- 宣言時刻: 2026-11-20T06:02:16.073Z（HEAD ?・直前は自レーンのK1126 indexコミット）
- 作業: y=6族の同型機械化。K1126（y=5族パラメトリック全称証明）の完成を受け、
  K1023(y=1)→K1099(y=2)→K1104(y=3)→K1112(y=4)→K1126(y=5)に続く
  高速レーン第5段の実行である。
- 範囲: 全z>=0・全x>=6・全R>=0で H(R;(x,6);z)=cand6(z,x,R)（z偶奇別パラメトリック
  T/P集合表）の導出・全称証明・独立監査。マージ行 x<=z-7 の単一トークン閉形式
  一致（マージ命題のy=6版の全称昇格・y=1..6拡張）、値1基底点6点
  {z+1,z+3,z+5,z+7,z+9,z+11}（基底点y点仮説のy=6版）、tail R>=x+z+7 の
  (x+6) mod 2（tail開始族式 x+z+y+1 のy=6帯・偶数yではy=4と同型の偶奇反転に
  注意）、掃引行 x=z+7、中間帯下端 2y+z+2=z+14、clip窓のy=6要件式
  （2y+2=14候補・y=4の±12/±13からの広げ直し）を含めて横断法則候補の
  y=6検証が最初の関門である。
- 子の参照: A子は同切片x-1行（x=6では(5,6)≡(6,5)合流でK1126のy=5族x=6行）、
  B子はK1126のcand5（出版済み・SHA pin済み）、C子は1⊕cand6(z-1,・,・)の
  z外帰納。すべて出版済み機材の上に閉じる。
- 予定実験dir: research/experiments/vertical-fiber-two-token-y6-parametric-allz-proof-20261120/
  （report.md・verify_y6_universal.py・census_rows.py・output/audit.json・output/census.txt）
- 予定log: research/log/2026-11-20-two-token-y6-parametric-allz-proof.md
- K番号: 仮番号は使用しない。push直前に3点確認（README grep・items 404・list_commits）
  で空きを取得する。
- 並走レーン（n11 fold/extract・K1058円整数論）との経路不競合を確認済み。
  fold19は並走宣言済み（3a23ccf3・着手禁止）。
- y<=5族と異なる点（y=6で新規に現れうる差異・特に偶数yのtail値偶奇と
  clip窓拡張の必要性）は予備probeで確認してからcand6を固定する。
  有限観察・ヒューリスティック・全称証明を明確に区別する。
