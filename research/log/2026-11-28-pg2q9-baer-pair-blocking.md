# 完了log: PG(2,q^2) Baer部分平面対による2重ブロッキング — PG(2,9) ≤ 26 < 3q

- 日時: 2026-11-28
- 宣言: `e30035a2` (research/log/2026-11-28-pg2q9-baer-pair-blocking-declaration.md,
  宣言時 HEAD pin `2cad2042`・publish-then-execute・単一オーナー)。
- 実験dir: research/experiments/pg2q9-baer-pair-blocking-20261128/
- K項目: K1373（仮番号・統合時に再採番可能性あり）

## 実行内容（宣言どおり・クリーン作業dirで最初から再実行）

1. boards9.py: GF(4)/GF(9)/GF(16) 独立構成。design 検査 PASS
   （PG(2,4) 21点・PG(2,9) 91点・PG(2,16) 273点）。
   Baer 基底 = 部分体有理点（7/13/21点）。
2. baer.py: Baer 性検査 PASS（全直線交差 ∈ {1, q+1}・内部 design
   2-(q²+q+1, q+1, 1)）。
   - PG(2,4): 軌道 360（安定化群 168）・全対 census
     交差 {0:2880, 1:7560, 2:30240, 3:13860, 4:10080}。
     **Baer対2重ブロッキング最小 union = 13**（∩=1 の 7560 対全て成功・
     ∩≥2 全て失敗）。既知 min 12 と無矛盾（12点 minimal DB は Baer 対でない）。
   - PG(2,9): **軌道 7,560**（|PGL(3,9)| 42,456,960・安定化群 5,616=PGL(3,3)・
     整合 ✓）・**全対 28,559,820 census**
     交差 {0:3,265,920, 1:7,665,840, 2:10,614,240, 3:5,307,120, 4:393,120, 5:1,326,780}。
     **2重ブロッキングになるのは disjoint 対のみ（3,265,920/3,265,920 成功・
     交差≥1 は 0/25,293,900）→ 最小 union 26**。
     witness 26点・プロファイル {2:65, 5:26}・全91直線 ≥2 定義直接検証 ✓。
     **→ PG(2,9) t=2 min ∈ [19, 26]（下界はcounting bound 10k ≥ 182）。
     27 = 3q を下回り「min=3n」パターンが n=9 で不成立。**
     K1371 の「Baer対による3q未満候補は q≤9 で未発見」は本結果で修正
     （局所探索では発見できなかった disjoint Baer 対構成が存在）。
   - PG(2,16): seed 固定サンプリング 3,000 歩（disjoint 510）。
     **disjoint union 42 witness**（定義検証 ✓）→ **PG(2,16) ≤ 42 < 48**。
     min ∈ [33, 42]（counting bound 17k ≥ 546）。
3. ag_scan.py: AG(2,9) 制限スキャン（disjoint 3,000対 × ℓ∞ 91選択）:
   feasible なし（負のサンプル・正直な負）。AG(2,9) 上界は 26 のまま。
4. verify_baer.py: 盤再構成による再検証 ALL_OK
   （witness 定義直接再検査・軌道再計算（生成元順序変更で同一 7,560/360）・
   counting bound 9/19/33）。
5. 再現性: 宣言後のクリーン再実行で out/ 3 file とも byte-identical
   （seed 固定・PG(2,16) サンプリングも含め完全決定性）。

## 一般補題（証明つき・K1373 に正式記載）

disjoint Baer 対 A,B ⊆ PG(2,q²) の union は size 2(q²+q+1) の2重ブロッキング
（Baer 性より各直線が A・B に各 ≥1 点）。2(q²+q+1) < 3q² ⟺ q ≥ 3。
よって disjoint Baer 対の存在下で「PG(2,n) min = 3n」は平方位数 n ≥ 9 で
不成立。q=2 (n=4) は 14 > 12 で改善なし（機械検証とも一致: Baer対最小 13）。

## 教訓（fail-closed が機能した例）

- GF(9) を GF(3)[x]/(x²−1) で構成する初版バグ（x²=1 は既約でない）→
  inv table 欠落で canon KeyError が即捕捉。
- PG(2,16) の Baer 基底を素体 GF(2) 有理点（7点 = Fano）とした誤り →
  基底サイズ assertion (q²+q+1=21) が即捕捉。部分体 GF(4) 判定に修正。
- 出力 JSON のマージ順序誤り（計算結果を既存ファイルで上書き）→
  空ファイル検出で即捕捉。
- 交差ペアは2重ブロッキングに失敗し得る（共有点を通る両部分平面の
  Baer線でない直線が union と1点だけ交わる）— 最初の「交差≥1でも
  サイず25以下の候補」という予想は全数判定で完全に否定された。
  有限全数censusの価値を示す例。

## Non-claims

- 「全ての q≥3 で disjoint Baer 対が存在」は一般証明しない
  （q=2,3 全数・q=4 サンプリング）。
- PG(2,9) min の SAT 締め付け (k=25 UNSAT → min=26) は未実施・長期レーン向け。
- witness の全2重ブロッキング集合としての最小性は主張しない。
- verdict 不消費: 標準 11×11 空盤・19 central-reply roots・二石 root {60,27}・
  第三手 {100,108}・S2・全 closure class は全時点 UNKNOWN。

## レジューム（着手前に必ず最新main再取得・hourly並走注意）

- PG(2,9) k=25 SAT (UNSAT で min=26 確定) は CNF が大きいので長期レーン向け。
- PG(2,16) disjoint Baer 対の全数census（軌道サイズ要計測・メモリ分割）。
- AG 側: Baer 対以外の構成 (AG(2,9) ≤ 25?) は未探索。
- 他レーン所有中の 8x29 / n11 / six-row 系には不参入。
