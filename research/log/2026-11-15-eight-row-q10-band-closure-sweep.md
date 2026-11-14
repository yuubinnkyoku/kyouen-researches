# 2026-11-15 eight-row q10 帯閉包・連続掃引レーン（高速レーン）

## 目的

(8,10) の真の安定化長 M_{8,10} の決着。既知: witness 帯 m=10..25
（`eight-row-bands-20261114`）・上界 U_{8,10}=940（K0318 代入）。残る帯
m=26..939 の def-mode UNSAT 掃引（全幅 UNSAT なら M=26・w=8 で初の完全決着）。

## 実施内容

1. **claim + 較正**（`eight-row-q10-band-closure-26-939-20261115/`・461475f4）:
   genfast3 vs genfast CNF byte-identity 3/3 MATCH（8x26 def・8x32 def・
   8x32 def+lex=H,V,HV）。instance-identity: 8x26 meta（vars 8,963）bit-exact・
   陽性対照 m=20 SAT 703 / m=25 SAT 1,221,994 conflicts bit-exact
   （eight-row-bands records と一致）。leanband3 パイプライン smoke:
   8x20 SAT witness 71石 decode+dual-verify ok。
2. **連続掃引（本レーン）**: laneA 79..138（UNSAT 連続・13..45s/幅）、
   laneB 501..513（UNSAT・22..58s/幅）、laneC 61..69（UNSAT・62..103s/幅）、
   laneD 60..53（UNSAT・112..142s/幅）。INDET は m=31 のみ
   （200s cap・4,823,685 conflicts・事前プローブとして記録済み）。
   records はバッチごとに chunk として即時 push（c0001..c0004・h0001..h0003・
   manifest に md5/行数記録・c0004 の sec 27.0/24.0 は push 直後の raw CDN
   キャッシュで古いバージョンが見えた輸送アーティファクトで、get_file_contents
   で最新版 byte-exact を確認）。
3. **並走セッションとの合流**: 同一対象の claim が対側
   （`eight-row-q10-band-closure-20261115/`）からも出ていた。対側は難所帯
   （26..59）を主戦場にしており、43..60 UNSAT（cap ≤250s）・m=42 INDET
   （250s/6,309,677 conflicts・honest negative）・m=27/28/29/31 プローブ INDET・
   サンプル幅 80/100/150/200/300/500/700/939 UNSAT（m=939 42s/116,323 conflicts）
   を push 済み。本レーンは連続掃引（61..69・70..138・501..513）を担うことで
   重複を回避。laneD（53..32 方向）は対側の 250s cap 掃引と重複するため廃止。
   **クロス検証**: m=53..60 の UNSAT conflict 数が両セッションで完全一致
   （kissat 決定性・同一 CNF md5 の独立確認・例: m=60 1,529,015・m=53 1,970,208）。
4. **CSV 統合**: (8,9) と (8,10) の bounds 行を追加（`results/fixed-width/
   mwq_stabilization.csv)。(8,9) は eight-row-bands 未統合分の反映:
   witness 8x9..8x26 SAT（m=26 63石 rows [8,8,8,8,7,8,8,8]・2,496,508
   conflicts）・frontier m=27 は def 230s/5,721,584 + def+lex 230s/5,460,948
   INDET・U=984 → **M_{8,9} ∈ [27, 984]**（初の w=8 CSV 行）。

## 現在の状態

- witness-free 連続区間 **43..138**、加えて 501..513 とサンプル 150..939。
- M_{8,10} ∈ [26, 940]（前線 26..42 が律速: m=26 は4符号化 INDET・m=42 INDET
  250s/6.31M・m=30/32..41 未掃引）。
- 11×11 長期レーンへの接続: 固定幅 M の決着は無盤面勝敗と独立だが、
  def-mode の曲線 census と K0318 上界の代入方法は共通基盤。

## 障害・honest negative

- 実行環境の sandbox reset 2回（いずれもコマンド timeout 起因）で作業ディレクトリ
  一時喪失→raw fetch で再構築。23:05Z 前後の filesystem rollback failure で
  バックグラウンドレーン死亡。未 push の laneA 139..151 相当は喪失（再実行対象）。
- m=26..31（26 は8行4符号化・31 は200s/4.82M）・m=42（250s/6.31M）は
  INDET honest negative として記録（non-absence 主張なし）。
- c0004 sec 27.0/24.0 表示: raw CDN キャッシュ由来の見かけの差（最新版は
  byte-exact）。

## 次の一手

1. laneA を m=139 から 500 まで再開（chunk push 継続）。
2. laneB を m=514 から 939 まで再開（対側サンプルと小刻みに照合）。
3. 難所 26..42: 対側レーンが 250s cap で継続。それでも INDET の幅は
   rowY=0..3 分割（K0829 型・w=8 は4鏡像クラス）または K0818/K0819 型の
   クラス分割符号化で攻略。m=26 は (6,8) m=22 と同型の最難関候補。
4. 全幅閉包後: M_{8,10} exact 決着として K 項目 + CSV exact-threshold 行化
   （その際に最新 main から K 番号・CSV を再取得して統合）。
