# 単一オーナー宣言: 2トークン残余ゲーム y=14族の正本検証器（verify_y14_universal.py）着手

- 宣言時刻: 2026-11-22T19:08:21Z
- 宣言時点の観測 HEAD: cd2c10954（y=14 全称段階への対抗宣言・着手は不存在を確認:
  単一オーナー宣言note不存在・proof実験 dir 不存在・log grep 空）
- 宣言者: 高速レーン第二実行（vertical-fiber 系。本日の y=14 fit 二重並走では独立導後に
  対抗宣言 `e3a856ad`（2026-11-22T18:42:55Z）に19秒差で先行を取られ fit 出版を譲り、
  完成済みの導出を独立第二検証として出版した実行〔実験dir
  `vertical-fiber-two-token-y14-parametric-fit-second-verification-20261122`
  commit `dc0a7cfc`・SV log `04f1b30e`・K1233 evidence 更新 `cd2c1095`〕。
  y=1..13 の全称系列 K1141 → K1143 → K1152 → K1231（observed→proved）に続く
  第14族 y=14 の全称段階のみを着手する。K1233（y=14 fit・status observed・
  2026-11-22T18:55:45Z 出版）の本文は次段階を「12チェック監査（A子/B子=K1231の
  cand13逐語転写〔x=14合流子(13,14)≡(14,13)〕/C子=1 xor cand14(z-1,x,R-1)/
  型機械clip窓2y+2=30のtight判定〔10族連続候補〕/census z=0..79・x=14..70）」と
  明示的に指名しており、fit宣言ノート
  （2026-11-22-y14-two-token-skeleton-single-owner-note.md・commit e3a856ad）は
  全称段階を自宣言の保持範囲外と明示した上で着手していない。本宣言後に着手する）。

## 保持範囲

1. **part1（本着手）**: 検証正本 verify_y14_universal.py の構築と全12機械チェック
   （C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12・y=13 出版機 verify_y13_universal.py
   正本〔SHA-256 079b49ad…・commit 7835937d の part2 版〕と同型の12チェック構成）の
   実行・3回実行 byte-identical 確認・fail-closed 検査・実験dir・研究log の出版。
   仕様は K1233 item/knowledge README の next_stage 記載に従う:
   - A子 = H(R-1;(x-1,14);z)・x=14 合流子 (13,14)≡(14,13)〔y=13 族 x=14 行と同一状態。
     K1233 fit の spot 深行誤選択 (19,13) が生値1で正しいことを実証済み〕
   - B子 = 出版 cand13（K1231 全称証明済み族の閉形式・verify_y13_universal.py 正本の
     cand13 ブロックを逐語転写。y=13 part1 が出版cand13.py（K1231 fit 実験・
     SHA-256 cb903c56…）から転写したのと同型の二重正本管理）
   - C子 = 1 xor cand14(z-1,x,R-1)
   - 型機械 clip 窓 2y+2 = 30・番兵 ±31（tight 判定の 9 族連続 y=5..13:
     12/14/16/18/20/22/24/26/28 に続く 2y+2=30 は 10 族目候補。本宣言の事前予想は
     「tight のまま」で、clip 29 で型収束違反が出るはず〔y=13 part1 の clip 27 で
     2,987違反・最初 (60,90,90) と同型〕。違反ゼロなら tight 判定を再審する）
   - census アンカー z=0..79・x=14..70
   - cand14 正本の逐語転写元は出版 cand14.py（K1233 fit 実験
     `vertical-fiber-two-token-y14-parametric-allz-fit-20261122`・commit b6f74dfc・
     SHA-256 61782b6e…）。
   - 第二検証（本宣言者の当日出版・V1-V4 overall PASS）により両レーンの cand14 実装の
     判定等価（2,241,162点）は既に確定しており、seed 選択は結果に不変。
2. **part2（part1 着地後・本宣言の継続）**: C1d（出版固定z切片アンカー A8u..A17u の
   y=14 行特殊化・preflight fail-closed）と census_rows.py（y=14 版第三実装）による
   独立 census 照合（C11r）を構成し、K1233 の observed→proved 昇格を判定・出版する。
   part1 が着地するまでは着手しない。
3. 採番は push 直前に最新 main を再取得して 3 点確認（commits・item path 404・
   knowledge README grep）。

## 範囲外の明示

- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 には
  本宣言・本工程は一切関係しない。
- 3トークン以上・y>=15 族・固定幅・q点版安定化長・fold 系・remo 周期系・m22 class-split は対象外。
- n11 central-reply closure grind（batch-17 Part AU 系・並走長期レーン）・
  K1171/K1231 併存の maintainer 判定事項には一切着手しない（SV log に記録済み）。
- 本宣言と競合する y=14 全称段階の宣言が main に存在することが判明した場合は
  本宣言を撤回して譲る。

## 解釈規約（前もって明記）

- part1 の12チェックは cand14 全称命題の機械的証拠の構成であり、K1233 の status 昇格は
  part2 完了まで行わない。
- 有限照合は有限観察であり、trust 境界（選択肢分解の健全性・mex 恒等式・有限型空間の
  完全性）は y=1..13 系列と同一の機械分類に依存する。
- A子の x=14 行は正準順序 {13,14}≡(14,13) で y=13 族 x=14 行と同一状態になる
  （合流子 cand13(z,14,R-1)）。この行の特殊扱いを誤ると C4 型機械が偽陽性を生む。
