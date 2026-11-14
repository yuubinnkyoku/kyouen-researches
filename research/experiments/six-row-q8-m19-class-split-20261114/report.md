# 6×19 q=8 row-deficient maximal nonexistence — class-split UNSAT sweep（2026-11-14）

## 主張

1. 6×19 整数格子盤（q=8・q点共円/共線禁止・標準ルール）において、
   6行の行鏡映正準欠損クラス D ⊆ {0..5}（63個の非空部分集合のうち35個）それぞれについて
   class-split SAT インスタンス（rows∈D は ≤6石、rows∉D はちょうど7石、安全+極大）は
   **すべて UNSAT**（kissat 4.0.4、計 15,492,764 conflicts・35インスタンス）である。
2. したがって **6×19 に行欠損の極大安全配置は存在しない**（6×19 の全極大安全配置は
   満容量 6×7=42石）。
3. K0815 の 6×18 41石欠損極大witness（行構成 7,6,7,7,7,7）と合わせて
   (6,8) の witness 幅集合は「18 に witness があり 19 にない」ことが確定し、
   **M_{6,8} = 19 または M_{6,8} ≥ 21**（∈ {19} ∪ [21,371]・上界371は不変）。
   K0815 が未決着として残した「6×19 q=8（kissat 255s・4.52M conflicts）」を決着。

## 被覆議論（ class-split の完全性 ）

安全条件から各行 ≤ 7石（行は長さ19 ≥ q の直線）。よって任意の極大安全配置の行占有は
各行 ≤7 であり、「石数 ≤6 の行」の集合 D が空でないことが欠損配置の定義と同値
（総石数 < 42 ⟺ 何らかの行が ≤6）。Dごとに分割したインスタンス
（rows∈D は ¬rowGe 単元で ≤6、rows∉D は rowGe 単元で ≥7・安全と併せてちょうど7）
は欠損配置全体を過不足なく覆う。行鏡映 y→5−y は符号化・安全・極大を保存するので
D と mirror(D) の可満性は同値であり、35正準クラスで63クラス分を決定できる。

## 符号化

sat3.js（本実験 scripts/）: K0810 sat.js の census（circleABC 整数三元組・直線対）と
sat2.js の sequential counter をそのまま使い、class 単元節を追加したもの。
cell 変数は P の行優先順で最初の n=114 個（decode は var i+1 = cell[y*m+x]）。
全インスタンスの DIMACS は `node sat3.js 6 19 8 --class=D out.cnf` で決定的に再生成可能
（cnf は容量削減のため未格納・meta json に vars/clauses 数を記録）。
sat3.js は --krow=y:k（欠損行の石数正確指定）と --minpos=P（H鏡映による位置分割）、
--lex=H（列鏡映lex・class保存で健全）も持つ。

## 検証プロトコル

- 制御（陽性）: 2×8 q=4 class{0} SAT 5石 rows(2,3)（K0796 witness 再発見・census不使用
  verifyConfig PASS）・6×18 q=8 class{1} SAT 41石 rows(7,6,7,7,7,7)（K0815 witness盤・
  511,895 conflicts・verifyConfig PASS）・6×23 q=6 class{1} SAT 29石 rows(5,4,5,5,5,5)
  （K0815 extend6 witness盤・77,932 conflicts・verifyConfig + Python Fraction 別実装の
  2系統 PASS・positive_control_6x23_class1_witness.json）。
- 制御（陰性）: 2×9 q=4 class{0} UNSAT（M_{2,4}=9 と整合）。
- **end-to-end 論理検証**: 3×7/3×8/2×8/2×9/3×9 q=4 の小盤5面・全正準クラス19インスタンス
  が全mask完全列挙の ground truth（欠損クラス集合）と SAT/UNSAT 19/19 で完全一致
  （smallboard_validation/）。
- **交差符号化**: 4つの最難クラス {1},{2},{1,2},{2,3} を --lex=H（別節構造）でも UNSAT
  （2,142,822 / 3,246,250 / 2,118,969 / 1,348,948 conflicts）。
- **決定性**: 実行環境リセット（ワークスペース喪失）を挟んで全クラス・全制御の
  conflicts 数が bit-exact 再現（{1}=2,279,372・{0}=565,010・{2}=4,008,520・6×18=511,895・
  6×23=77,932 など）。旧実装パス（sat2.encodeCore）と新パス（sat3.encodeCore2）も同一
  DIMACS を生成。
- UNSAT 判定は kissat exit 20（生ログ output/c6x19q8_*.txt に conflicts と実行統計込み）。

## 結果一覧（records.jsonl の要約）

35クラスすべて UNSAT。所要 conflicts 上位:
{2}: 4,008,520 (228.8s)・{1}: 2,279,372 (145.8s)・{1,2}: 2,071,998 (100.7s)・
{2,3}: 1,356,618・{0}: 565,010・{1,3}: 678,327・{0,1}: 617,594・{0,5}: 552,202。
多行欠損クラス（|D|≥3）は 5〜14s 程度で高速に潰れた（付加制約が効く）。
計 15,492,764 conflicts・920.1 秒（2並列実行・実行環境により±）。

## 範囲と限界

有限機械検証であり、census 完全性（6×19 の全曲線が sat.js census で列挙されていること）
と kissat の正確性まで。数論的証明ではない（K0816 と同水準）。
**M_{6,8} の確定には m≥20 の持続性が残る**（K0024 の T=371 まで。上界側の tail 評価が
次の一手・K0342 型の chord energy 引き下げが有望）。6×19 単盤の不在確定は
「M=19 または ≥21」を意味し、K0815 の下界 M≥19 と合わせて (6,8) 行の
M 列を {19},21..371 に細分化した。

## 未決着（negative・非不在）

- 5×22 q=6 class{0}: 280s 2,182,652 conflicts・class{1}: 280s 2,228,966 conflicts・
  class{0}+lex=H: 280s 3,997,714 conflicts — INDET（環境リセット前の観測・raw消失のため
  再実行による裏付けが残作業）。--krow/--minpos 分割が次の一手。
- 6×21 q=7 class{0}: 2,652,745・class{1}: 2,577,348 conflicts（280s INDET・同上）。
- 6×30 q=5 class{4}: 1,372,573 conflicts/275s INDET（K0815 witness 盤の SAT 側対照・
  extend6 でwitness既知のため継続不要）。

## 再現

```sh
./scripts/sweep1.sh 6 19 8 "D" <outdir>       # 1クラス（cnf生成→kissat→JSONL追記）
node scripts/sat3.js 6 19 8 --class=D out.cnf # DIMACS生成
node scripts/sat3.js decode 6 19 8 model.txt   # SATモデル→石座標→verifyConfig
```

kissat 4.0.4 は公式リリース kissat-4.0.4-linux-amd64（GitHub rel-4.0.4）をそのまま使用。
