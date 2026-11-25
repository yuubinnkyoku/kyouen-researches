# 単一オーナー宣言: 2トークン残余ゲーム y=12族の正本検証器（verify_y12_universal.py）着手

- 宣言時刻: 2026-11-20T17:12:00Z
- 宣言者: 長期レーン（n11 11x11 証明基盤担当とは別線の本実行。本宣言は y=12 族の全称段階のみを対象とし、n11 系は着手しない）
- 前提: y=12 族 fit（[K1152](../knowledge/items/K1152-two-token-y12-parametric-closed-form-fit.md)・commit f7da7adafd→da7f032cf8・2026-11-20 出版）は
  単一オーナー宣言ノート（commit fe93c969・14:25:00Z）の保持範囲が「全称証明段階（verify_y12_universal.py）は本宣言の保持範囲外」と明示しており、
  main の最新コミットにも本段階への着手・宣言は存在しないことを確認した（着手直前再取得 POST 17:02Z HEAD 2f7faf49 まで）。

## 保持範囲

1. **part1（本着手）**: 検証正本 verify_y12_universal.py の構築と全12機械チェック
   （C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12・y=11 出版機 K1143 part1 commit d6f001421d と同型）の実行・3回実行 byte-identical 確認・
   実験dir・研究log の出版。仕様は K1152 audit の next_stage 記載に従う:
   - A子 = H(R-1;(x-1,12);z)・x=12 合流子 (11,12)≡(12,11)
   - B子 = 出版 cand11.py（K1143 fit 出版正本）の逐語転写
   - C子 = 1 xor cand12(z-1,x,R-1)
   - 型機械 clip 窓 2y+2 = 26・番兵 ±27（tight 判定の 7 族継続 y=5..11 に続く 8 族目候補）
   - census アンカー z=0..79・x=12..70
2. **part2（part1 着地後・本宣言の継続）**: C1d（出版固定z切片アンカーの y=12 行特殊化）と census_rows.py による
   独立 census 照合を構成し、K1152 の observed→proved 昇格を判定・出版する。part1 が着地するまでは着手しない。
3. 採番は push 直前に最新 main を再取得して 3 点確認（commits・item path 404・knowledge README grep）。

## 範囲外の明示

- 標準 11×11 の空盤勝敗・二石root・S2 {59,60}・class 1/2/4 には本宣言・本工程は一切関係しない。REFUTED-D10 とは無関係。
- 3トークン以上・y>=13 族・固定幅・q点版安定化長・fold 系・q5-m22・remo 周期系・m22 class-split は対象外。
- y=11 part2（C1d+census・y11 出版レーン保留中）・y=10 誤植修正系は着手しない。
- 他レーンが宣言済みの工程（fold26・round-5 refsolve・WIN8-D10 証明書抽出等）は着手しない。
- 本宣言と競合する y=12 全称段階の宣言が main に存在することが判明した場合は本宣言を撤回して譲る。

## 解釈規約（前もって明記）

- part1 の12チェックは cand12 全称命題の機械的証拠の構成であり、K1152 の status 昇格は part2 完了まで行わない。
- 有限照合は有限観察であり、trust 境界（選択肢分解の健全性・ mex 恒等式・有限型空間の完全性）は y=1..11 系列と同一。
