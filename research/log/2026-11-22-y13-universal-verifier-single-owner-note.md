# 単一オーナー宣言: 2トークン残余ゲーム y=13族の正本検証器（verify_y13_universal.py）着手

- 宣言時刻: 2026-11-22T17:59:40Z
- 宣言時点の観測 HEAD: 5b6af2ed（y=13 全称段階への対抗宣言・着手は不存在を確認）
- 宣言者: 高速レーン（vertical-fiber 系・本実行。y=1..12 の出版系列
  K1023 → K1099 → K1104 → K1112 → K1126 → K1127 → K1131 → K1135 → K1138 →
  K1141 → K1143 → K1152（observed→proved）に続く第13族 y=13 の全称段階のみを
  着手する。K1231（y=13 fit・status observed・2026-11-22 出版）の本文は次段階を
  「12チェック監査（A子/B子=K1152のcand12逐語転写/C子/x=13合流子(12,13)≡(13,12)/
  型機械clip窓2y+2=28のtight判定/census z=0..79）」と明示的に指名しており、
  fit宣言ノート（2026-11-22-y13-two-token-skeleton-single-owner-note.md・commit d3404db8）
  は全称証明段階を自宣言の保持範囲外と明示した上で着手していない
  （同noteの宣言更新節で本着手を記録）。

## 保持範囲

1. **part1（本着手）**: 検証正本 verify_y13_universal.py の構築と全12機械チェック
   （C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12・y=12 出版機 K1162（commit 60622f35）と同型）の
   実行・3回実行 byte-identical 確認・fail-closed 検査・実験dir・研究log の出版。
   仕様は K1231 audit の next_stage 記載に従う:
   - A子 = H(R-1;(x-1,13);z)・x=13 合流子 (12,13)≡(13,12)
   - B子 = 出版 cand12（K1152 全称証明済み族の閉形式・verify_y12_universal.py
     正本〔SHA-256 e2092976…〕の cand12 ブロックをブロック内 Y→Y12 改名のみで逐語転写）
   - C子 = 1 xor cand13(z-1,x,R-1)
   - 型機械 clip 窓 2y+2 = 28・番兵 ±29（tight 判定の 8 族連続 y=5..12: 12/14/16/18/20/22/24/26
     に続く 9 族目候補）
   - census アンカー z=0..79・x=13..70
   - cand13 正本の逐語転写元は出版 cand13.py（K1231 fit 実験・SHA-256 cb903c56…）
2. **part2（part1 着地後・本宣言の継続）**: C1d（出版固定z切片アンカー A8u..A17u の
   y=13 行特殊化・preflight fail-closed）と census_rows.py（y=13 版第三実装）による
   独立 census 照合（C11r）を構成し、K1231 の observed→proved 昇格を判定・出版する。
   part1 が着地するまでは着手しない。
3. 採番は push 直前に最新 main を再取得して 3 点確認（commits・item path 404・knowledge README grep）。

## 範囲外の明示

- 標準 11×11 の空盤勝敗・二石root・S2 {59,60}・class 1/2/4 には本宣言・本工程は一切関係しない。
- 3トークン以上・y>=14 族・固定幅・q点版安定化長・fold 系・remo 周期系・m22 class-split は対象外。
- n11 central-reply closure grind（batch-14 Part AS 41 LOSS canonical adoption 等・並走長期レーン）・
  K1058 k=8/k=9 arc count レーン・r=10 sweep レーンには一切着手しない。
- 本宣言と競合する y=13 全称段階の宣言が main に存在することが判明した場合は本宣言を撤回して譲る。

## 解釈規約（前もって明記）

- part1 の12チェックは cand13 全称命題の機械的証拠の構成であり、K1231 の status 昇格は
  part2 完了まで行わない。
- 有限照合は有限観察であり、trust 境界（選択肢分解の健全性・mex 恒等式・有限型空間の完全性）は
  y=1..12 系列と同一の機械分類に依存する。
