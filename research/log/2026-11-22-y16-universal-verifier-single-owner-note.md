# 単一オーナー宣言: 2トークン残余ゲーム y=16族の正本検証器（verify_y16_universal.py）着手

- 宣言時刻: 2026-11-22T22:50Z（push 時刻で確定）
- 宣言時点の観測 HEAD: 76abc080（K1058 single-circle diagnosis retract・
  2026-11-22T22:27:36Z）。
  y=16 全称段階への対抗宣言・着手は不存在を確認した: 単一オーナー宣言
  コミット列（search_commits "single-owner" 直近）は Part BB amendment
  `dafe9651`・even-y unified template `e083ac28`・y=16 fit `e0fbd99d` が最新で
  いずれも y=16 全称段階の着手を含まない・search_code "verify_y16"/"K1238" で
  verify_y16_universal 言及 0 件・proof 実験dir
  `vertical-fiber-two-token-y16-parametric-allz-proof-20261122` 不存在・
  直近コミットは K1058 系（k=8 切片まわりの訂正系列）と n11 session log のみで
  y=16 族と非接触。
- 宣言者: 高速レーン（vertical-fiber 系・別実行。y=1..16 の出版系列
  K1023 → … → K1141 → K1233（observed→proved）/K1234 → K1235（observed→
  proved）/K1236 → K1237（y=16 fit・status observed・commit 33e1c22e）・
  K1238（even-y 統一テンプレート機械検証・単一Y点火コードで偶数y族
  y=10..16 の出版表再生を確認・y=16 の正しさは K1237 observed 前提）に続く
  第16族 y=16 の全称段階のみを着手する。K1237 item の限界節は
  「全称証明（verify_y16_universal.py・A子/B子/C子・型機械・census）は本項の
  範囲外・別工程」と明示しており、K1238 のレジュームも y=16 全称を次の
  最有力として指名している。y=16 fit 宣言ノート
  （2026-11-22-y16-two-token-skeleton-single-owner-note.md・commit e0fbd99d）は
  全称段階を自宣言の保持範囲外と明記した上で着手していない。本宣言後に着手する。

## 保持範囲

1. **part1（本着手）**: 検証正本 verify_y16_universal.py の構築と全12機械チェック
   （C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12・y=15 出版機
   verify_y15_universal.py part1〔正本 part2 版 SHA-256 a39e7ab1…・commit
   0bf18752〕と同型の12チェック構成）の実行・3回実行 byte-identical 確認・
   fail-closed 検査・実験dir・研究 log の出版。仕様は K1237/K1238 item と
   knowledge README の next_stage 記載に従う:
   - A子 = H(R-1;(x-1,16);z)・x=16 合流子 (15,16)≡(16,15)〔y=15 族 x=16 行と
     同一状態・合流子 cand15(z,16,R-1)。A子合流の正準順序扱いは y=14 fit の
     (19,13) 事故と y=14/y=15 全称 part1/part2 で実証済みの知見を適用〕
   - B子 = 出版 cand15（K1235 全称証明済み族の閉形式・published_cand15.py
     〔K1235 part2 実験 dir・commit 0bf18752・SHA-256 別途記録〕を逐語転写・
     ブロック内 Y→Y15 改名。y=15 part2 が出版 cand15 を検証器に組み込んだのと
     同型の二重正本管理。cand15 の使用範囲（x>=16 行・B子 / x=16・A子合流）は
     K1235 全称の定義域 x>=15 の内側）。
   - C子 = 1 xor cand16(z-1,x,R-1)
   - cand16 正本の逐語転写元は出版 cand16.py（K1237 fit 実験
     `vertical-fiber-two-token-y16-parametric-allz-fit-20261122`・commit
     33e1c22e・SHA-256 別途記録）・fit driver 省き。
   - 型機械 clip 窓 2y+2 = 34・番兵 ±35（tight 判定の 11 族連続 y=5..15:
     12/14/16/18/20/22/24/26/28/30/32 に続く 2y+2=34 は 12 族目候補。本宣言の
     事前予想は「tight のまま」で、clip 33 で型収束違反が出るはず〔y=14 part1 の
     clip 29 違反 2,480・y=15 part1 の clip 31 違反と同型〕。違反ゼロなら再審する）
   - census アンカー z=0..79・x=16..70（行数 80*55=4,400・R<=x+z+17）
   - merge 帰結: x<=z-17 なら H == single_token(x+16,z,R)（y=16 版・fit の
     probe box 内マージ行 0 行の観察と K0832 helper の領域一致は C2/C7/C8/C12
     の corollary 掃引と census で初めて全域 raw anchor される）
   - tail 帰結: R >= x+z+17 なら H == (x+16) mod 2
   - C7 seed は 20261162（y=14: 20261142・y=15: 20261152 の系列を継承）
   - C8 の x=15 行は正準拡張としてのみ恒等式に入る（x<16 には raw 主張なし。
     y=15 機の x=14 行・y=14 機の x=13 行と同一の扱い）
2. **part2（part1 着地後・本宣言の継続）**: C1d（出版固定z切片アンカー
   A8u..A17u の y=16 行特殊化・preflight fail-closed・出版 verify_y15
   正本から逐語転写）と census_rows.py（y=16 版第三実装・XMIN=16・XMAX=70・
   RBUF=18）による独立 census 照合（C11r）を構成し、K1237 の observed→proved
   昇格を判定・出版する（K1141/K1152/K1231/K1233/K1235 と同一手続き・同一K項目・
   昇格時の新規採番なし）。part1 が着地するまでは着手しない。
3. 採番は push 直前に最新 main を再取得して 3 点確認（commits・item path 404・
   knowledge README grep。part1 item は仮番号 K1239 を予備採番・
   K1238-two-token-even-y-unified-template-check.md が現時点の main 最新 item）。

## 事前の横断予想（すべて検証前の外挿・y=16 の証明ではない）

- clip 窓 2y+2=34 は tight（C4t で clip 33 の違反 > 0 を予想・違反ゼロなら
  tight 判定を再審）。
- census 幾何: 4,400行・点数は行和 Σ(x+z+18) の機械再計算値・merge 帰結領域は
  x<=z-17 で z>=33 で初めて非空（fit の probe box 観察〔box 内マージ 0 行〕と整合）。
- pin 格子統一式 pin=z+(d+48)/2・o_pin∈[17,32] は型機械の箱内で機械的に
  （C4 の confluence として）再確認される。値域 {0,1,2}。
- 型総数は clip 34/sentinel 35 の型空間で増加（y=13: 234,180〔clip 28〕→
  y=14: 281,912〔clip 30〕→ y=15: 335,658〔clip 32〕に続く4点目として記録する・
  事前数値予想はしない）。
- 12チェックの構成は y=14/y=15 part1 と同一で、期待される照合点規模は同等
  （~6.4M 点）。
- B子 cand15 の使用域（B子 x>=16 行・A子 x=16 合流）は K1235 の証明済み定義域
  （x>=15・全 z・全 R）の内側であり、新規の raw 主張を含まない。
- C1d の事前予想（part2）: 出版切片 A8u..A17u の y=16 行は cand16 に一致する
  （fit の spot と独立の第三系アンカー）。preflight が不一致を検出した場合は
  fail-closed で part2 統合を中止する。

## 範囲外の明示

- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 には
  本宣言・本工程は一切関係しない。
- 3トークン以上・y>=17 族・固定幅・q点版安定化長・fold 系は対象外
  （横断法則（基底点・tail・マージ・clip 窓・pin 格子・対角行規則・I 帯 th）の
  y>=15 一般補題化レーンとも本工程は非接触。本工程の結果は同レーンの
  データ点となる）。
- n11 central-reply grind（並走長期レーン・Part AV 出版監視・batch-17/18 系）・
  K1058 k=8 系（並走・直近コミット群）・even-y 統一テンプレートの拡張（K1238 の
  継続）には一切着手しない。
- 本宣言と競合する y=16 全称段階の宣言が main に存在することが判明した場合は
  本宣言を撤回して譲る。

## 解釈規約（前もって明記）

- part1 の12チェックは cand16 全称命題の機械的証拠の構成であり、K1237 の
  status 昇格は part2 完了まで行わない。
- 有限照合は有限観察であり、trust 境界（選択肢分解の健全性・mex 恒等式・
  有限型空間の完全性）は y=1..15 系列と同一の機械分類に依存する。
- A子の x=16 行は正準順序 {15,16}≡(16,15) で y=15 族 x=16 行と同一状態になる
  （合流子 cand15(z,16,R-1)）。この行の特殊扱いを誤ると C4 型機械が偽陽性を
  生む（y=14 の C11ordered/C11canonical で実証済みの事故型）。
