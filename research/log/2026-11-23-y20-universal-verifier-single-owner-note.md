# 単一オーナー宣言: 2トークン残余ゲーム y=20族の正本検証器（verify_y20_universal.py）着手

- 宣言時刻: 2026-11-23（push 時刻で確定）
- 宣言時点の観測 HEAD: 69f76309（K1251 commit・2026-11-23T08:04:25Z。
  y=20 全称段階への対抗宣言・着手は不存在を確認した: search_commits
  \"y20 universal\" は y=20 fit 体裁（K1246 item・commit B ed7d3190・
  commit C 1a868d05）のみで、search_commits \"K1249\" は 0 件。
  K1246 item は「y=20 全称段階の B子は出版 cand19（K1243 proved）の逐語転写の
  予定（全称は本項の範囲外・別宣言が必要）」と明記しており、対抗なし。
  実験dir
  vertical-fiber-two-token-y20-parametric-allz-proof-20261123 は不存在
  （experiments 直下の two-token 系は until-20261122 old-style
  even-y check と y19 proof/y19 fit/y20 fit のみ）。並走の
  y=21 fit lane（宣言 2d3aeac2・K1248 予定・seed cand19・odd-y 直接
  翻訳で y20 機体・y20 全称とは非接触）・3トークン x11 first-family
  lane（41a6dda2）・batch-26 Part BQ lane（8e64ba1c/309386d5）・
  inversive arc lane（K1250/K1251/K1252/K1253・300dd361 前後）・
  n11 grind 長期レーンとも非接触）。
- 宣言者: 高速レーン（vertical-fiber 系。y=1..19 の出版系列
  K1023 → … → K1242（y=18 fit + 全称）→ K1243（y=19 fit・
  observed→proved 昇格済み）→ K1245（y=19 全称機体・単一出版）→
  K1246（y=20 fit・observed・seed 法則 8 連続一発一致・出版 cand18
  〔K1242 proved〕の Y=18→20 機械翻訳）に続く第20族 y=20 の全称段階のみを
  着手する。K1246 item の次段階記載が全称段階を指名している）。

## 保持範囲

1. **検証正本 verify_y20_universal.py の構築と全14機械チェック
   （C1/C1b/C1d/C2/C2b/C3/C4/C4t/C7/C8/C9/C11/C11r/C12）の実行**。
   構成は出版 y=19 単一出版機体（K1245・verify_y19_universal.py・
   git blob c0cec1d5…・現在の main bytes・HEAD 69f76309 で再照合済み）と
   同型で、y=19 機の単一機体単一出版変形手続きの直接継承:
   機体は最初から 14チェック版として構築・出版し、実行は段階分けする
   （transcription check → C1d preflight → census 生成 → 12チェック電池 →
   14チェック電池）。12チェック部分の audit は audit-part1-12checks.json
   として別 artifacts に残す。仕様は K1246 fit item の記載に従う:
   - A子 = H(R-1;(x-1,20);z)・x=20 合流子 {19,20}≡{20,19}〔y=19 族
     x=20 行と同一状態・合流子 cand19(z,20,R-1)〕
   - B子 = 出版 cand19（K1243 全称証明済み族の閉形式・出版
     verify_y19 正本の cand19 ブロック = 出版 cand19.py fit〔git blob
     cb05633f…〕の Y→Y19 改名と byte-equality、両系統で転写検証。
     cand19 の使用範囲（B子 x>=20 行・A子 x=20 合流）は K1243 全称の
     定義域 x>=19 の内側）
   - C子 = 1 xor cand20(z-1,x,R-1)
   - cand20 正本の逐語転写元は出版 cand20.py（K1246 fit 実験
     vertical-fiber-two-token-y20-parametric-allz-fit-20261123・
     git blob a54cfb40…・HEAD 69f76309 で再照合済み）・fit driver 省き。
     転写の正しさは scripts/check_transcriptions_y20.py
     （engine/アンカー blocks は出版 y=19 機から・B子 cand19 ブロックは
     出版 y=19 機の cand19 ブロックと出版 cand19.py fit の二系統
     byte-equality〔cand19.py 側は Y→Y19 word-boundary 改名〕・
     cand20 ブロックは出版 cand20.py と byte-equality）で実行前に
     機械検証する
   - 型機械 clip 窓 2y+2 = 42・番兵 ±43（tight 判定の 15 族連続
     y=5..19: 12/14/16/18/20/22/24/26/28/30/32/34/36/38/40 に続く
     2y+2=42 は 16 族目候補。事前予想は「tight のまま」で、clip 41 で
     型収束違反が出るはず〔y=19 機 clip 39 違反 770・最初違反
     (60,102,102) と同型〕。違反ゼロなら再審する）
   - census アンカー z=0..79・x=20..70（行数 80*51=4,080・R<=x+z+21。
     出版 y=12..y=19 と同一の bounded-memoization twin・LRU cap 1,600,000）
   - merge 帰結: x<=z-21 なら H == single_token(x+20,z,R)（y=20 版。
     census x範囲では z>=41 で初めて非空）
   - tail 帰結: R >= x+z+21 なら H == (x+20) mod 2
   - C7 seed は 20261202（y=16: 20261162・y=17: 20261172・y=18: 20261182・
     y=19: 20261192 の系列）
   - C8 の x=19 行は正準拡張としてのみ恒等式に入り（cand19 定義域内
     評価の B子と x=20 合流・x=19 行の特殊性は y=19 機の x=18 行と同一の
     扱い）、tail 窓照合は出版 cand19 の tail 主張 R>=x+z+20→(x+19)
     mod 2（x>=19）に対して窓 (x+z+21, x+z+22, x+z+23) で行う
   - C11r: census_rows.py（y=20 版第三実装・XMIN=20・XMAX=70・RBUF=22）の
     台帳 census.txt を cand20 から行単位再導出して照合
2. **K1246 の observed→proved 昇格判定**（C11r 含む14チェックの overall
   PASS・bad 0・3回 byte-identical・fail-closed 電池合格を条件に、同一
   K項目で昇格・K1141/K1152/K1231/K1233/K1235/K1237/K1240/K1242/K1243
   ・K1245 機体と同一手続き）。
   part2 相当の機体 item は新規 K 番号（仮採番 K1249。push 直前に
   再確認。K1249 は現在本 main 上に存在せず〔search_commits 0 件〕。
   K1247 は 3トークン x11 fit lane・K1248 は y21 fit lane がそれぞれ
   宣言済み）。
3. 採番は push 直前に最新 main を再取得して確認する。
4. 昇格後は B子逐語連鎖 cand9..cand19 が出版機体系列で完成し、
   マージ命題は y=1..20 全称に拡張される（本宣言の範囲外の一般補題化
   レーンのデータ点となる）。

## 事前の横断予想（すべて検証前の外挿・y=20 の証明ではない・点数は宣言前に機械算出）

点数予想はループ幾何のみの算術関数（predict_y20_counts.py・ゲーム評価なし）
で機械算出した。**同一算術関数が y=19 出版単一出版機体 audit
（総 6,941,913・C1 24,510/C1b 44,027/C1d 136,206/C2 229,663/C2b 19,580/
C3 1,335/C4 579,657/C4t 579,657〔最初違反 (60,102,102)〕/C7 200,000/
C8 1,057,317/C9 897,930/C11 873,600/C11r 440,960/C12 1,857,471）の
14チェック点数を全て完全一致で再現することを確認済み**。

- **12チェック電池点数（C4t の points 込み・bad は情報提供扱い）**:
  C1=25,080・C1b=44,758・C2=233,877・C2b=19,668・C3=1,365・C4=574,040・
  C4t=574,040・C7=200,000・C8=1,078,938・C9=895,302・C11=869,040
  （両 engine 434,520×2）・C12=1,857,592・**12チェック小計 6,373,700**
  （出版系列: y=17 6,343,825→y=18 6,354,790→y=19 6,364,747→
  y=20 6,373,700）。
- **C1d（機械算出）**: anchor 掃引 126,420（6 切片×x=20..159×R<=x+61）+
  lowR 9,240（3 切片×x=20..159×21+22+23 点）= **135,660**。
  preflight は anchor 11,700（x=20..45・R<=x+z0+30・z別
  1,833/1,859/1,885/2,015/2,041/2,067）+ lowR 9,240 = **20,940**
  （y19 preflight 21,375 と同一構成式・fail-closed を機体実行前に
  実施する）。
- **census 幾何（機械算出）**: 行数 4,080=80*51・1 engine あたり
  points 434,520・merge 領域 94,380 点/engine（x<=z-21 は z>=41 で
  初めて非空）・tail 各行 1 点（計 4,080）/engine。
- **C11r（機械算出）**: rows 4,080・点数 438,600（R=0..x+z+22）。
- **part2 14チェック総点数の予想: 6,373,700 + 135,660 + 438,600 =
  6,947,960**（出版系列 y=18 6,934,616→y=19 6,941,913→y=20 6,947,960）。
- **merge 帰結総点数（全チェック合計・機械算出）: 1,003,367**・
  **tail 帰結総点数: 192,254**（y19 機の merge 1,062,109・tail
  192,520 に対応）。
- clip 窓 2y+2=42 は tight（C4t で clip 41 の違反 > 0 を予想・違反
  ゼロなら tight 判定を再審）。**最初違反が band 下端と歩む系列の
  8 観測目と予想し、y=13..19 の (60,90,90)/(60,92,92)/(60,94,94)/
  (60,96,96)/(60,98,98)/(60,100,100)/(60,102,102) に続き
  (60,104,104) を予想する**（違反ゼロ・または別位置なら誠実記録する）。
- pin 格子統一式 pin=z+(d+60)/2・o_pin∈[21,40]・奇z 10 pin 行
  d≡0 (mod 4) {-16,…,20}・偶z 10 pin 行 d≡2 (mod 4) {-18,…,18}（K1246 fit で確定した偶数 y 族の pin 行数
  y/2=10 両偶奇則・両偶奇とも 10 行は族初）は型機械の箱内 C4
  confluence として再確認される。値域 {0,1,2}。
- 型登録数は clip 42/sentinel 43 の型空間で変化する
  （y=19 機の C4 箱内登録型数 386,487〔clip 40〕の記録に続く。
  事前数値予想はしない）。
- B子 cand19 の使用域（B子 x>=20 行・A子 x=20 合流）は K1243 の証明済み
  定義域（x>=19・全 z・全 R）の内側であり、新規の raw 主張を含まない。
- C1d の事前予想: 出版切片 A8u..A17u の y=20 行は cand20 に一致する
  （fit の spot・K0913 z=6 切片交差検証と独立の第三系アンカー）。
  preflight が不一致を検出した場合は fail-closed で機体実行を中止・
  報告する。
- C10 相当（次族 seed 一発一致）は本機体の範囲外（y=21 fit lane の
  事前登録に既に含まれる）。

## 範囲外の明示

- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 には
  本宣言・本工程は一切関係しない。
- 3トークン以上・y>=21 族（fit・全称とも）・固定幅・q点版安定化長・fold 系は
  対象外（横断法則一般補題化レーンとも本工程は非接触。本工程の結果は
  同レーンのデータ点となる。y=21 fit は並走レーンが宣言済み・非接触）。
- n11 central-reply grind（batch-26/Part BQ 以降の長期レーン）・
  3トークン x11 first-family lane・K1058/K1250/K1251/K1252/K1253
  inversive arc lane・canonical exact-S5 cache 系には一切着手しない。
- 本宣言と競合する y=20 全称段階の宣言が main に存在することが判明した場合は
  本宣言を撤回して譲る（first-completer 規則も参照）。

## 解釈規約（前もって明記）

- 有限照合は有限観察であり、trust 境界（選択肢分解の健全性・mex 恒等式・
  有限型空間の完全性）は y=1..19 系列と同一の機械分類に依存する。
- K1246 の status 昇格は 14チェックの overall PASS + bad 0 + 3回
  byte-identical + fail-closed 電池合格まで行わない。
- A子の x=20 行は正準順序 {19,20}≡{20,19} で y=19 族 x=20 行と同一状態になる
  （合流子 cand19(z,20,R-1)）。この行の特殊扱いを誤ると C4 型機械が偽陽性を
  生む（y=14 の C11 事故型で実証済み）。
- 実行環境がメモリ上限に達した場合は census cap を下げて再実行し、決定的再現を
  記録する（cap 低下は値に影響しない・誠実記録する）。
- byte-identical 主張にはバイトコードキャッシュ衛生（__pycache__ purge・
  python3 -B・PYTHONDONTWRITEBYTECODE=1）を適用する（y=18 fit レーンの
  運用正則を継承）。
- fail-closed 電池（y19 機の種を y20 に翻訳・scratch copy で検出確認）:
  census.txt 欠落・行削除・行重複・T/P 改ざん・idx 改ざん・C11r tail flip・
  C1d anchor 誤結合・lowR R→R+1・merge 境界 z-21→z-20・clip 42→40・
  in_P20 tail parity x%2==1→==0・band parity 改ざん。検出不能なら電池設計を
  誤りとして正直記録する。
