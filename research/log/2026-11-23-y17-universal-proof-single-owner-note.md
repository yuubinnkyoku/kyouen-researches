# 単一オーナー宣言: 2トークン残余ゲーム y=17族 全称証明（verify_y17_universal.py part1 + part2）の着手（先行出版）

- 宣言時刻: push 時刻で確定（2026-11-23T01:0XZ 頃）
- 宣言時点の観測 HEAD: `3efab5b9`（2026-11-23T00:43:59Z・push 直前の最新 main 再取得で確認し、
  push 成功後の fetch-back で着地を確認する）
- 宣言者: 高速レーン（vertical-fiber 系・別実行）。y=17 族 fit（K1240・status observed・
  commit 6ca80e0e/d59cc940/91f6f204・実験dir vertical-fiber-two-token-y17-parametric-allz-fit-20261123）
  の直後に、K1240 README bullet が指名する「verify_y17_universal.py 着手は別宣言必須」の
  当該別宣言である。前回レジュームの3候補（y=17全称・横断法則一般補題化・y=18 fit）から
  情報価値最上位の y=17 全称（2トークン族の全称が y=1..17 に伸びる・K1240 昇格パイプライン）
  を選択する。
- 対抗確認（宣言前の最新 main で実施）: 最新 25 コミット（HEAD `3efab5b9` まで）に
  y=17 全称・y=18 fit・横断法則補題化の着手宣言なし。search_code "verify_y17_universal"
  は fit 3 ファイルの「別宣言必須」注記のみで実装・宣言とも不存在。
  K1237/K1239 (y=16 part2)・K1240 (y=17 fit) は 3トークン以上・y>=18 族・固定幅・
  q点版安定化長を範囲外と明記しており本着手と矛盾しない。
- 対象・範囲: H(R;(x,17);z) の全 z>=0・全 x>=17・全 R>=0 に対する主張
  「cand17 == H」の正本機械検証。y=14/y=15/y=16 と同一の2段階手続きとする:
  - part1（12チェック）: C1（生両エンジン vs cand17・z=0..14・x=17..35・R<=x+z+47）・
    C1b（K0832 単一トークン生アンカー・出版 y=16 族 cand16〔K1237 proved・B子〕生アンカー
    z=0..24・x=16..28・R<=x+z+30・x=17 マルチセット合流 (16,17)==(17,16) 生アンカー
    == cand16(z,17,R-1)・R<=z+45）・C2（閉形式 identity 格子 z=0..48・x=17..58・
    R<=x+z+43）・C2b（deep tail z∈{60..400}・x=17..66(step5)）・C3（選択肢分解の
    生照合・x=17 は合流子 (16,17) の正準順序注意）・C4（型機械・free 座標 box ±60・
    clip 窓 2y+2=36・sentinel 37・型 confluence）・C4t（tightness probe clip 35・
    13 族連続 tight 候補の判定・violation は bad 総計に含めない情報提供）・
    C7（固定 seed 20261172・200k 点・z,x<=3000）・C8（境界多様体・x=16 行は閉形式
    extension-consistency 行のみ〔生主張は x>=17〕）・C9（v-space shell 掃引）・
    C11（生 census アンカー z=0..79・x=17..70・R<=x+z+18・両エンジン別コマンド
    C11ordered/C11canonical・bounded-memoization twin・LRU cap 1,600,000）・
    C12（deep 閉格子 z=0..120・x=17..120・R<=x+z+19）。副命題: merge x<=z-18 ⇒
    H == single_token(x+17,z,R)・tail R>=x+z+18 ⇒ H == (x+17)%2。
  - part2（14チェック）: part1 機械に C1d（出版固定 z スライスアンカー
    z=8/9/10/15/16/17・K0999/K1000/K1001/K1011/K1065/K1077/K1087 の y=17 行評価・
    x=17..159・R<=x+61・関数は y=10 part2 検証器から verbatim・採用前に
    scripts/preflight_c1d_y17.py で三方 fail-closed 事前検査〔生両エンジン・cand17〕・
    + 低 R 単一トークン還元 R<=z+6〔z=15..17〕）と C11r（census_rows.py 第三実装の
    census.txt〔z=0..79・x=17..70・R=0..x+z+19・80*54=4320 行〕の cand17 からの
    行ごと再導出照合・T/P 集合・Thue-Morse index・tail）を追加し、
    フル14チェック総合 PASS・3実行 byte-identical・fail-closed 電池検出を条件に
    **K1240 を observed → proved に昇格する**（K1141/K1152/K1231/K1233/K1235/K1237
    と同一手続き・同一 K 項目昇格）。part2 は pre-flight を含めて本宣言の保持範囲内
    （前回 y=15/y=16part1 宣言と同じく part1+part2 保持スコープで宣言する）。
- 手続き・決定性: 全ての出版 transcribed block（生エンジン・K0832 single_token・
  cand16〔B子・K1237 proved・出版 verify_y16_universal.py cand16 ブロックから
  block-local Y 改名 Y16〕・cand17〔K1240 fit 出版 cand17.py から fit driver 省略〕）は
  出版 byte を検証器に組み込み、C1/C1b/C3/C11 で生エンジンに再錨する。
  検証品質: 3実行 byte-identical（同一 cwd 2回 + 隔離 tree/cwd/HOME +
  PYTHONHASHSEED=random 1回・隔離側で census part 再生成）・fail-closed 改ざん電池
  （C11 part 改ざん/欠落・census 幾何 mismatch・type 改ざん等・種 TBD）・
  audit は sort_keys JSON・seed 固定・clock なし。
- 信任境界: 選択肢分解の健全性（C3 生照合）・閉形式 mex 恒等式（C2/C4/C12 格子）・
  有限型空間の完全性（C4 型機械 confluence・clip 窓 2y+2=36）を生エンジン（C1/C1b/C11）
  と出版 y=16 族（K1237 proved・C1b 生アンカー・B子）に錨る。K1237 の正しさは
  y=16 part2 機械の claim であり本機械では再証明しない（出版系列の trust chain）。

## 事前の横断予想（y=5..y=16 出版表からの外挿であり y=17 の証明ではない）

- clip 窓 2y+2=36 tight（**13 族連続 tight 候補**・y=5..16 の 12/14/16/…/34 に続く）:
  C4 は clip 36/sentinel 37 で confluence violation 0、C4t は clip 35/sentinel 36 で
  violation > 0 を予想する。
- 型数: y15 = 335,658（clip 32）→ y16 = 394,686（clip 34）の増加傾向に従い
  y17 では 40 万点台（clip 36・box ±60）。正確な値は機械が決める。
- census（C11）: z=0..79・x=17..70・R<=x+z+18 の点数は機械期待値
  Σ(x+z+19) = 440,640点/エンジン（両エンジン 881,280点）・merge 副命題は
  z>=35 で初めて box 内に行を持ち（z=35・x=17 〔x<=z-18〕から）、
  bad 0 を予想する。
- 値域: 全照合点で値 ∈ {0,1,2}・mex 恒等式の右辺も {0,1,2}（値 3 なし）。
- B子逐語転写構成の継続: y17 機械の B子は cand16（出版最終構造・even-y 型）で
  あり、y13..y16 機械が証明済み族を B子に使った構成（cand10/12/13/14/15/16）の
  継続（**7連目候補**）。
- 合流子の正準順序: x=17 行の A子は (16,17)≡(17,16) で cand16(z,17,R-1)。
  y=14 の (19,13) 事故型（A子評価を行 x 未満で誤る）を構造的に排除するため、
  opts17 は x==17 分岐・C3 は生の子列挙 (16,17)/(17,16) で直接照合する。
- part2 への条件: part1 12チェックが PASS した場合のみ part2（C1d 組み込み・
  census.txt 第三実装・K1240 昇格）に進む。part1 で bad > 0 が出た場合は
  昇格せず、反例として記録・出版する（全体を過大主張しない）。

## 範囲外の明示

標準 11×11 の空盤勝敗・二石 root・S2 {59,60} には一切言及しない。
3トークン以上・y>=18 族・固定幅・q点版安定化長・fold 系は対象外。
n11 系（batch-19 残51キー・closure 採用判断・scrutiny owner 待ち）には非接触。
nodes/census 点数を勝敗として読まない。

