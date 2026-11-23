# 単一オーナー宣言: 2トークン残余ゲーム y=18族の正本検証器（verify_y18_universal.py）着手

- 宣言時刻: 2026-11-23T03:19Z（push 時刻で確定）
- 宣言時点の観測 HEAD: c15b1c3f（y=19 two-token fit 宣言・2026-11-23T03:11:39Z）。
  y=18 全称段階への対抗宣言・着手は不存在を確認した: search_commits
  "repo:yuubinnkyoku/kyouen-researches verify_y18" は 4 件で、すべて
  y=18 fit 体裁（K1242 item・fit 実験dir・README bullet）と z6 スライス検証器で
  全称検証器の着手を含まない。"y18 universal" 2 件・"y=18 universal" 3 件も
  すべて fit 体裁のみ。実験dir
  vertical-fiber-two-token-y18-parametric-allz-proof-20261123 は不存在。
  並走の y=19 fit 宣言（c15b1c3f）は保持範囲を y=19 fit に限定し
  "Universal stage requires a separate declaration" と明記しており、本宣言
  （y=18 全称のみ）と非接触。長期レーン（batch-20/Part BG・Part BH）・K1058 とも
  非接触。
- 宣言者: 高速レーン（vertical-fiber 系・別実行。y=1..17 の出版系列
  K1023 → … → K1141 → K1231/K1233/K1235 → K1237/K1238/K1239（y=16 全称）→
  K1240/K1241（y=17 fit + 全称・observed→proved 昇格済み）→ K1242（y=18 fit・
  status observed・commit 738ab049/9e898f45/e9bf7991/fa789e27）に続く
  第18族 y=18 の全称段階のみを着手する。K1242 item の解釈規約節は
  「y=18 全称段階は別の単一オーナー宣言が必要」と明示しており、K1242 の
  次段階も全称段階を指名している。y=18 fit 宣言ノート
  （2026-11-23-y18-two-token-skeleton-single-owner-note.md・commit 738ab049）は
  全称段階を自宣言の保持範囲外と明記した上で着手していない。本宣言後に着手する。

## 保持範囲

1. **part1（本着手）**: 検証正本 verify_y18_universal.py の構築と全12機械チェック
   （C1/C1b/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C12・y=17 出版機
   verify_y17_universal.py part2〔SHA-256 4253cf29…・commit
   ab23d12014afaa57eb3da83b3ffd056e86df4949〕と同型の12チェック構成）の実行・
   3回実行 byte-identical 確認・fail-closed 検査・実験dir・研究 log・
   K 項目の出版。仕様は K1242 item の解釈規約・次段階記載に従う:
   - A子 = H(R-1;(x-1,18);z)・x=18 合流子 {17,18}≡{18,17}〔y=17 族 x=18 行と
     同一状態・合流子 cand17(z,18,R-1)。正準順序扱いは y=14 合流事故で実証済みの
     知見を y=17 機と同型に適用〕
   - B子 = 出版 cand17（K1240 全称証明済み族の閉形式・出版 verify_y17 正本の
     cand17 ブロックを逐語転写・ブロック内 Y→Y17 改名して y=18 機の
     cand18 ブロックが Y=18 を持てるようにする。cand17 の使用範囲
     （B子 x>=18 行・x=18 A子合流）は K1240 全称の定義域 x>=17 の内側）
   - C子 = 1 xor cand18(z-1,x,R-1)
   - cand18 正本の逐語転写元は出版 cand18.py（K1242 fit 実験
     vertical-fiber-two-token-y18-parametric-allz-fit-20261123・commit
     9e898f45404fb3bf2ee1d882c9807f414418e62f・SHA-256 別途記録）・
     fit driver 省き。転写の正しさは scripts/check_transcriptions_y18.py
     （出版 bytes との正規化差分比較・B子は出版 verify_y17 cand17 ブロックと
     出版 cand17.py fit の二系統 byte-equality）で実行前に機械検証する。
   - 型機械 clip 窓 2y+2 = 38・番兵 ±39（tight 判定の 13 族連続 y=5..17:
     12/14/16/18/20/22/24/26/28/30/32/34/36 に続く 2y+2=38 は 14 族目候補。
     事前予想は「tight のまま」で、clip 37 で型収束違反が出るはず〔y=14 part1 の
     clip 29 違反・y=15 clip 31 違反・y=16 clip 33 違反 1,638・y=17 clip 35 違反と
     同型〕。違反ゼロなら再審する）
   - census アンカー z=0..79・x=18..70（行数 80*53=4,240・R<=x+z+19。
     メモリ上限を見て y=16/y=17 機と同一の bounded-memoization twin・
     LRU cap 1,600,000）
   - merge 帰結: x<=z-19 なら H == single_token(x+18,z,R)（y=18 版。
     census x範囲では z>=37 で初めて非空）
   - tail 帰結: R >= x+z+19 なら H == (x+18) mod 2
   - C7 seed は 20261182（y=15: 20261152・y=16: 20261162・y=17: 20261172 の系列）
   - C8 の x=17 行は正準拡張としてのみ恒等式に入り（cand18 定義域外評価の
     B子は cand17〔x>=17 の証明済み域〕・A子 x=18・x=17 行の特殊性は
     y=17 機の x=16 行と同一の扱い）、tail 窓照合は出版 cand17 の tail 主張
     R>=x+z+18→(x+17) mod 2（x>=17）に対して行う
2. **part2（part1 着地後・本宣言の継続）**: C1d（出版固定z切片アンカー
   A8u..A17u の y=18 行特殊化・preflight fail-closed・出版 verify_y17 正本から
   逐語転写）と census_rows.py（y=18 版第三実装・XMIN=18・XMAX=70・RBUF=20）に
   よる独立 census 照合（C11r）を構成し、K1242 の observed→proved 昇格を判定・
   出版する（K1141/K1152/K1231/K1233/K1235/K1237/K1240 と同一手続き・同一K
   項目・昇格時の新規採番なし）。part1 が着地するまでは着手しない。
3. 採番は push 直前に最新 main を再取得して確認（part1 item は K1244 を仮採番と
   する。K1243 は並走 y=19 fit レーンが宣言で予約済み。404 確認後に確定する。
   衝突時は AGENTS.md の仮採番規約に従う）。

## 事前の横断予想（すべて検証前の外挿・y=18 の証明ではない・点数は宣言前に機械算出）

- **part1 12チェック点数（機械算出・ループ幾何のみ・ゲーム値評価なし）**:
  C1=23,940・C1b=43,296・C2=225,449・C2b=19,492・C3=1,305・C4=585,189・
  C4t=585,189・C7=200,000・C8=1,035,729・C9=900,534・C11=877,680
  （両 engine 438,840×2）・C12=1,856,987・**part1 総点数 6,354,790
  （C4t の points 込み・C4t の bad は情報提供扱い）**。同一算術関数が
  y=17 part1 全チェック点数（総 6,343,825）を出版 audit と完全一致で再現する
  ことを確認済み。
- **census 幾何（機械算出）**: 行数 4,240=80*53・1 engine あたり points 438,840・
  merge 領域 105,651 点（x<=z-19 は z>=37 で初めて非空・fit の「box 内マージ
  0 行」4 族連続観察と整合）・tail 各行 1 点（計 4,240）。
- **C11r（part2・機械算出）**: rows 4,240・点数 443,080（R=0..x+z+20。
  census_rows y18 版の全行値数と同一）。
- **C1d（part2・機械算出）**: anchor 12,432（preflight x=18..45・R<=x+z0+30 の
  6 切片和）→ verifier 掃引は 127,374（6 切片×x=18..159×R<=x+62−1）+
  lowR 9,372 = 136,746。preflight は anchor 12,432 + lowR 9,372。
- **part2 14チェック総点数の予想: 6,354,790 + 136,746 + 443,080 = 6,934,616**。
- clip 窓 2y+2=38 は tight（C4t で clip 37 の違反 > 0 を予想・違反ゼロなら
  tight 判定を再審）。
- pin 格子統一式 pin=z+(d+54)/2・o_pin∈[19,36]・奇z 9 pin 行 d≡2 (mod 4)
  {-14,…,18}・偶z 9 pin 行 d≡0 (mod 4) {-16,…,16}（K1242 fit で確定した
  両偶奇 9 pin 行・偶y pin 行数 y/2 則）は型機械の箱内 C4 confluence として
  再確認される。値域 {0,1,2}。
- 型総数は clip 38/sentinel 39 の型空間で増加（y=15: 335,658〔clip 32〕→
  y=16: 394,686〔clip 34〕→ y=17: 457,645〔clip 36〕に続く記録をする。
  事前数値予想はしない）。
- B子 cand17 の使用域（B子 x>=18 行・A子 x=18 合流）は K1240 の証明済み
  定義域（x>=17・全 z・全 R）の内側であり、新規の raw 主張を含まない。
- C1d の事前予想（part2）: 出版切片 A8u..A17u の y=18 行は cand18 に一致する
  （fit の spot と独立の第三系アンカー）。preflight が不一致を検出した場合は
  fail-closed で part2 統合を中止する。

## 範囲外の明示

- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 には
  本宣言・本工程は一切関係しない。
- 3トークン以上・y>=19 族全称・固定幅・q点版安定化長・fold 系は対象外
  （横断法則（基底点・tail・マージ・clip 窓・pin 格子・対角行規則・I 帯 th）の
  y>=18 一般補題化レーンとも本工程は非接触。本工程の結果は同レーンのデータ点
  となる。）。y=19 族 fit は並走実行の宣言（c15b1c3f）が保持しており
  本宣言・本工程は一切着手しない。
- n11 central-reply grind（並走長期レーン・batch-19/20・Part BG/BH 系）・
  K1058 k=8 系（並走）・even-y 統一テンプレートの拡張（K1238 の継続）には
  一切着手しない。
- 本宣言と競合する y=18 全称段階の宣言が main に存在することが判明した場合は
  本宣言を撤回して譲る。

## 解釈規約（前もって明記）

- part1 の 12チェックは cand18 全称命題の機械的証拠の構成であり、K1242 の
  status 昇格は part2 完了まで行わない（part1 出版時の K item は
  status: computed）。
- 有限照合は有限観察であり、trust 境界（選択肢分解の健全性・mex 恒等式・
  有限型空間の完全性）は y=1..17 系列と同一の機械分類に依存する。
- A子の x=18 行は正準順序 {17,18}≡{18,17} で y=17 族 x=18 行と同一状態になる
  （合流子 cand17(z,18,R-1)）。この行の特殊扱いを誤ると C4 型機械が偽陽性を
  生む（y=14 の C11 事故型で実証済み）。
- 実行環境がメモリ上限に達した場合は census cap を下げて再実行し、決定的再現を
  記録する（cap 低下は値に影響しない・誠実記録する）。
- byte-identical 主張にはバイトコードキャッシュ衛生（__pycache__ purge・
  python3 -B・PYTHONDONTWRITEBYTECODE=1）を適用する（y=18 fit レーンの
  運用正則を継承）。
