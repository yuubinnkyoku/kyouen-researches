# 単一オーナー宣言: 2トークン残余ゲーム y=15族の正本検証器（verify_y15_universal.py）着手

- 宣言時刻: 2026-11-22T20:33:30Z（push 時刻で確定）
- 宣言時点の観測 HEAD: bcc761b8（K1058 k=8 sum(u3+u4) 導出・2026-11-22T20:31:11Z。
  y=15 全称段階への対抗宣言・着手は不存在を確認した: 単一オーナー宣言 note
  不存在（最新 log 一覧に y15 universal 系 note なし）・proof 実験 dir
  `vertical-fiber-two-token-y15-parametric-allz-proof-20261122` 不存在・
  search_code "verify_y15" = 0 件・直近コミットは K1058 系（k=8 閉形式）と
  n11 Part AW 宣言のみで y=15 族と非接触）
- 宣言者: 高速レーン（vertical-fiber 系・別実行。y=1..15 の出版系列
  K1023 → … → K1141 → K1143 → K1152 → K1231/K1232 → K1233（observed→proved）/
  K1234 → K1235（y=15 fit・status observed・commit 6cd72dd1）に続く第15族
  y=15 の全称段階のみを着手する。K1235 item の next_stage は
  「verify_y15_universal.py の監査体制（A子・B子=出版cand14逐語転写・C子・
  型機械 clip 2y+2=32〔11 族 tight 候補〕・census・C1d published アンカー）は
  y=1..14 出版系列と同一の手続きで、着手には新規単一オーナー宣言が必要」と
  明示的に指名しており、y=15 fit 宣言ノート
  （2026-11-22-y15-two-token-skeleton-single-owner-note.md・commit 26a1ad28）は
  全称段階を自宣言の保持範囲外と明記した上で着手していない。本宣言後に着手する）

## 保持範囲

1. **part1（本着手）**: 検証正本 verify_y15_universal.py の構築と全12機械チェック
   （C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12・y=14 出版機
   verify_y14_universal.py 正本〔SHA-256 6ac219cf…・commit 7026c860 の
   part2 版〕と同型の12チェック構成）の実行・3回実行 byte-identical 確認・
   fail-closed 検査・実験dir・研究 log の出版。仕様は K1235 item/knowledge README
   の next_stage 記載に従う:
   - A子 = H(R-1;(x-1,15);z)・x=15 合流子 (14,15)≡(15,14)〔y=14 族 x=15 行と
     同一状態・合流子 cand14(z,15,R-1)。A子合流の正準順序扱いは y=14 fit の
     (19,13) 事故と y=14 全称 part1/part2 で実証済みの知見を適用〕
   - B子 = 出版 cand14（K1233 全称証明済み族の閉形式・verify_y14_universal.py
     正本の cand14 ブロックを逐語転写・ブロック内 Y→Y14 改名。y=14 part1 が
     出版 cand14.py から転写したのと同型の二重正本管理。cand14 の使用範囲
     （x>=15 行・B子 / x=15・A子合流）は K1233 全称の定義域 x>=14 の内側）
   - C子 = 1 xor cand15(z-1,x,R-1)
   - cand15 正本の逐語転写元は出版 cand15.py（K1235 fit 実験
     `vertical-fiber-two-token-y15-parametric-allz-fit-20261122`・commit 8222f6f6・
     SHA-256 f61997dd…）・fit driver 省き。
   - 型機械 clip 窓 2y+2 = 32・番兵 ±33（tight 判定の 10 族連続 y=5..14:
     12/14/16/18/20/22/24/26/28/30 に続く 2y+2=32 は 11 族目候補。本宣言の事前
     予想は「tight のまま」で、clip 31 で型収束違反が出るはず〔y=14 part1 の
     clip 29 で 2,480違反・最初 (60,92,92) と同型〕。違反ゼロなら再審する）
   - census アンカー z=0..79・x=15..70（行数 80*56=4,480・R<=x+z+16）
   - merge 帰結: x<=z-16 なら H == single_token(x+15,z,R)（y=15 版・
     probe box 内マージ行 0 行の fit 観察と helpersingle_token_val の領域一致は
     C2/C7/C8/C12 の corollary 掃引と census で初めて全域 raw anchor される）
   - tail 帰結: R >= x+z+16 なら H == (x+15) mod 2
2. **part2（part1 着地後・本宣言の継続）**: C1d（出版固定z切片アンカー
   A8u..A17u の y=15 行特殊化・preflight fail-closed・出版 verify_y14
   正本から逐語転写）と census_rows.py（y=15 版第三実装・XMIN=15・XMAX=70・
   RBUF=17）による独立 census 照合（C11r）を構成し、K1235 の observed→proved
   昇格を判定・出版する（K1141/K1152/K1231/K1233 と同一手続き・同一K項目・
   新規採番なし）。part1 が着地するまでは着手しない。
3. 採番は push 直前に最新 main を再取得して 3 点確認（commits・item path 404・
   knowledge README grep。part1 item は仮番号 K1236 を予備採番）。

## 事前の横断予想（すべて検証前の外挿・y=15 の証明ではない）

- clip 窓 2y+2=32 は tight（C4t で clip 31 の違反 > 0 を予想・違反ゼロなら
  tight 判定を再審）。
- census 幾何: 4,480行・点数は行和 Σ(x+z+17) の機械再計算値・merge 帰領域は
  z>=31 で初めて非空（fit の probe box 観察と整合）。
- pin 格子統一式 pin=z+(d+45)/2・o_pin∈[16,30] は型機械の箱内で機械的に
  （C4 の confluence として）再確認される。値域 {0,1,2}。
- 型総数は clip 32/sentinel 33 の型空間で増加（y=13: 234,180〔clip 28〕→
  y=14: 281,912〔clip 30〕に続く3点目として記録する・事前数値予想はしない）。
- 12チェックの構成は y=14 part1 と同一で、期待される照合点規模は同等
  （~6.4M 点）。

## 範囲外の明示

- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 には
  本宣言・本工程は一切関係しない。
- 3トークン以上・y>=16 族・固定幅・q点版安定化長・fold 系は対象外
  （横断法則（基底点・tail・マージ・clip 窓・pin 格子・対角行規則・I 帯 th）の
  y>=15 一般補題化レーンとも本工程は非接触。本工程の結果は同レーンの
  データ点となる）。
- n11 central-reply grind（batch-17 Part AU/AV/AW 系・並走長期レーン）・
  K1058 k=8 系（並走）には一切着手しない。
- 本宣言と競合する y=15 全称段階の宣言が main に存在することが判明した場合は
  本宣言を撤回して譲る。

## 解釈規約（前もって明記）

- part1 の12チェックは cand15 全称命題の機械的証拠の構成であり、K1235 の
  status 昇格は part2 完了まで行わない。
- 有限照合は有限観察であり、trust 境界（選択肢分解の健全性・mex 恒等式・
  有限型空間の完全性）は y=1..14 系列と同一の機械分類に依存する。
- A子の x=15 行は正準順序 {14,15}≡(15,14) で y=14 族 x=15 行と同一状態になる
  （合流子 cand14(z,15,R-1)）。この行の特殊扱いを誤ると C4 型機械が偽陽性を
  生む（y=14 の C11ordered/C11canonical で実証済みの事故型）。
