# 単一オーナー宣言: 2トークン残余ゲーム y=17族の正本検証器（verify_y17_universal.py）着手

- 宣言時刻: 2026-11-23T01:05Z（push 時刻で確定）
- 宣言時点の観測 HEAD: 3efab5b9（Part BF note status update・2026-11-23T00:43:59Z）。
  y=17 全称段階への対抗宣言・着手は不存在を確認した: search_commits
  "y=17 universal" 0 件・"verify_y17" 言及は fit レーンの体裁のみ（K1240 item・
  fit report・fit log・fit宣言ノート）で全称検証器の着手を含まない・proof 実験dir
  vertical-fiber-two-token-y17-parametric-allz-proof-20261123 は不存在・
  K1241 は commits 0 件・code search 0 件で空番。直近コミット列は
  長期レーン batch-19/Part BE/BF（class 16513 exact-S5・第三実装交叉検証）と
  K1058 k=8 系訂正のみで y=17 族全称段階と非接触。
- 宣言者: 高速レーン（vertical-fiber 系・別実行。y=1..16 の出版系列
  K1023 → … → K1141 → K1233/K1234 → K1235/K1236 → K1237/K1238/K1239
  （y=16 全称 part1+part2・observed→proved 昇格済み）→ K1240（y=17 fit・
  status observed・commit 6ca80e0e/d59cc940）に続く第17族 y=17 の全称段階のみを
  着手する。K1240 item の解釈規約節は「全称段階は別の単一オーナー宣言が必要」と
  明示しており、K1240 のレジュームも y=17 全称を次の最有力として指名している。
  y=17 fit 宣言ノート（2026-11-23-y17-two-token-skeleton-single-owner-note.md・
  commit eeeb1a8e）は全称段階を自宣言の保持範囲外と明記した上で着手していない。
  本宣言後に着手する。

## 保持範囲

1. **part1（本着手）**: 検証正本 verify_y17_universal.py の構築と全12機械チェック
   （C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12・y=16 出版機
   verify_y16_universal.py part2〔SHA-256 bdf4fe04…・commit b706b214/847c4043〕
   と同型の12チェック構成）の実行・3回実行 byte-identical 確認・fail-closed
   検査・実験dir・研究 log・K 項目の出版。仕様は K1240 item の解釈規約・次段階
   記載に従う:
   - A子 = H(R-1;(x-1,17);z)・x=17 合流子 {16,17}≡{17,16}〔y=16 族 x=17 行と
     同一状態・合流子 cand16(z,17,R-1)。正準順序扱いは y=14 合流事故で実証済みの
     知見を y=15/y=16 機と同型に適用〕
   - B子 = 出版 cand16（K1237 全称証明済み族の閉形式・出版 verify_y16
     正本の cand16 ブロックを逐語転写・ブロック内 Y→Y16 改名して y=17 機の
     cand17 ブロックが Y=17 を持てるようにする。cand16 の使用範囲
     （B子 x>=17 行・x=17 A子合流）は K1237 全称の定義域 x>=16 の内側）
   - C子 = 1 xor cand17(z-1,x,R-1)
   - cand17 正本の逐語転写元は出版 cand17.py（K1240 fit 実験
     vertical-fiber-two-token-y17-parametric-allz-fit-20261123・commit 6ca80e0e・
     SHA-256 別途記録）・fit driver 省き。転写の正しさは独立の
     scripts/check_transcriptions_y17.py（出版 bytes との正規化差分比較）で
     検証してから実行する。
   - 型機械 clip 窓 2y+2 = 36・番兵 ±37（tight 判定の 12 族連続 y=5..16:
     12/14/16/18/20/22/24/26/28/30/32/34 に続く 2y+2=36 は13族目候補。
     事前予想は「tight のまま」で、clip 35 で型収束違反が出るはず〔y=14 part1 の
     clip 29 違反・y=15 part1 の clip 31 違反・y=16 の clip 33 違反 1,638 と
     同型〕。違反ゼロなら再審する）
   - census アンカー z=0..79・x=17..70（行数 80*54=4,320・R<=x+z+18。
     メモリ上限は本hostの~1.0GiB cgroup を踏まえ y=16 機と同一の
     bounded-memoization twin・LRU cap 1,600,000）
   - merge 帰結: x<=z-18 なら H == single_token(x+17,z,R)（y=17 版。
     census x範囲では z>=35 で初めて非空）
   - tail 帰結: R >= x+z+18 なら H == (x+17) mod 2
   - C7 seed は 20261172（y=14: 20261142・y=15: 20261152・y=16: 20261162
     の系列を継承）
   - C8 の x=16 行は正準拡張としてのみ恒等式に入り（cand17 の定義域外評価の
     B子は cand16〔x>=16 の証明済み域〕・A子 x=17・x=16 行の特殊性は
     y=16 機の x=15 行と同一の扱い）、tail 窓照合は出版 cand16 の tail 主張
     R>=x+z+17→(x+16) mod 2（x>=16）に対して行う
2. **part2（part1 着地後・本宣言の継続）**: C1d（出版固定z切片アンカー
   A8u..A17u の y=17 行特殊化・preflight fail-closed・出版 verify_y16 正本から
   逐語転写）と census_rows.py（y=17 版第三実装・XMIN=17・XMAX=70・RBUF=19）
   による独立 census 照合（C11r）を構成し、K1240 の observed→proved 昇格を
   判定・出版する（K1141/K1152/K1231/K1233/K1235/K1237 と同一手続き・同一K
   項目・昇格時の新規採番なし）。part1 が着地するまでは着手しない。
3. 採番は push 直前に最新 main を再取得して確認（K1241 は本宣言時点で
   commits・code search とも 0 件の空番・part1 item の仮番号として使用する。
   K1240-two-token-y17-parametric-closed-form-fit.md が現時点の main 最新 item）。

## 事前の横断予想（すべて検証前の外挿・y=17 の証明ではない）

- clip 窓 2y+2=36 は tight（C4t で clip 35 の違反 > 0 を予想・違反ゼロなら
  tight 判定を再審）。
- census 幾何: 4,320行・点数は行和 Σ(x+z+19)〔R=0..x+z+18〕の機械再計算値・
  merge 帰結領域は x<=z-18 で z>=35 で初めて非空（fit の probe box 観察
  〔box 内マージ 0 行〕と y=15/y=16 に続く3族連続の box 内マージ 0 行と整合・
  census 箱内では z=35..79 で anchor される）。
- pin 格子統一式 pin=z+(d+51)/2・o_pin∈[18,34]・奇z 9 pin 行・偶z 8 pin 行は
  型機械の箱内で機械的に（C4 の confluence として）再確認される。値域 {0,1,2}。
- 型総数は clip 36/sentinel 37 の型空間で増加（y=14: 281,912〔clip 30〕→
  y=15: 335,658〔clip 32〕→ y=16: 394,686〔clip 34〕に続く4点目として記録
  する・事前数値予想はしない）。
- 12チェックの構成は y=15/y=16 part1 と同一で、期待される照合点規模は同等
  （~6.4M 点）。
- B子 cand16 の使用域（B子 x>=17 行・A子 x=17 合流）は K1237 の証明済み定義域
  （x>=16・全 z・全 R）の内側であり、新規の raw 主張を含まない。
- C1d の事前予想（part2）: 出版切片 A8u..A17u の y=17 行は cand17 に一致する
  （fit の spot と独立の第三系アンカー）。preflight が不一致を検出した場合は
  fail-closed で part2 統合を中止する。

## 範囲外の明示

- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 には
  本宣言・本工程は一切関係しない。
- 3トークン以上・y>=18 族・固定幅・q点版安定化長・fold 系は対象外
  （横断法則（基底点・tail・マージ・clip 窓・pin 格子・対角行規則・I 帯 th）の
  y>=17 一般補題化レーンとも本工程は非接触。本工程の結果は同レーンの
  データ点となる。y=18 族 fit も本宣言の保持範囲外・別宣言が必要）。
- n11 central-reply grind（並走長期レーン・batch-19/Part BE/BF 系・
  class 16513・51 unprobed キー・17 unconsumed closure WIN の採用判断は
  scrutiny owner 待ち）・K1058 k=8 系（並走・直近コミット群）・
  even-y 統一テンプレートの拡張（K1238 の継続）には一切着手しない。
- 本宣言と競合する y=17 全称段階の宣言が main に存在することが判明した場合は
  本宣言を撤回して譲る。

## 解釈規約（前もって明記）

- part1 の12チェックは cand17 全称命題の機械的証拠の構成であり、K1240 の
  status 昇格は part2 完了まで行わない。
- 有限照合は有限観察であり、trust 境界（選択肢分解の健全性・mex 恒等式・
  有限型空間の完全性）は y=1..16 系列と同一の機械分類に依存する。
- A子の x=17 行は正準順序 {16,17}≡(17,16) で y=16 族 x=17 行と同一状態になる
  （合流子 cand16(z,17,R-1)）。この行の特殊扱いを誤ると C4 型機械が偽陽性を
  生む（y=14 の C11 事故型で実証済み）。
- 実行環境は ~1.0GiB cgroup メモリ上限をもつ本hostで、census は
  bounded-memoization twin（出版 raw engine のコードオブジェクトを再束縛した
  純関数の透過的メモ化・LRU 退避は固定訪問順序の下で決定的）で行う。
  メモリ上限で実行が失敗した場合は cap を下げて再実行し、決定的再現を記録
  する（低下は値に影響しない・誠実記録する）。
