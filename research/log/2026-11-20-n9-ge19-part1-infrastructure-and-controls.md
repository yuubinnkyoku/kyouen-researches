# n9-ge19 (K_9 上界) 決着レーン part1 出版: 検証基盤・正負制御・較正と 2 件の符号化バグ修正 (2026-11-20)

単一オーナー宣言 (21f8610464d2711f768b5764d23b21a40295dee5) に基づく
`research/experiments/n9-ge19-k9-upper-decision-20261120/` の part1 出版。
判定自体は**未決着 (INDET) のまま**。不在・上界の主張は一切ない。

## 出版したもの

1. **強化 CNF 生成器** gen_strong_cnf.js: at-least-K 逐次カウンタ (fwd) +
   冗長強化 (S1: 曲線ごとの at-most-3 カウンタ、S2: 逆順 at-least-K カウンタ) +
   全 forbidden quads。8 種 (n=5,7,8,9 × ge_K/ge_{K+1}) を FNV で固定して発行。
   n9_ge19_strong: 89,733 vars / 278,538 clauses / FNV-1a-64 `83f9407a12eff3ea`。
   宣言条件「冗長で sound な付加節のみ」を満たす構成。
2. **第三系評価器** eval_strong.js: CNF + 変数マップ + witness から、補助変数を
   定義の意味論 (個数比較) で独立に値決定して全節を評価、加えて witness の安全性を
   4x4 整数行列式で全 4 点組再検査する。
3. **正負制御全 PASS**:
   - 正: W5(naive fresh)/W7(naive fresh)/W8(naive fresh)/W9(既刊) がそれぞれ
     ge_k_strong を全節 0 違反で充足。
   - 負: 同 witness は ge_{k+1}_strong で「fwd/rev の at-least ユニット 2 節のみ」
     違反 (W9 対 n9_ge19_strong: var 1449 / 89733)。det4 再検査 forbidden 0。
   - fastsat が発見した新 9 石 witness [2,4,5,7,11,12,21,23,24] も第三系で完全検証
     (SAT モデル復号パイプラインの動作確認)。
   - センサス: F_5/7/8 = 826/6,364/14,564 (naive 全列挙), F_9=29,152・直線 92・円 6,722
     (生成器カタログ) が既刊値と完全一致。
4. **2 系較正**:
   - 探索系 ksearch.js: n7-15 (既知 UNSAT) を 11,880,598 nodes / 17.4s で再現。
   - SAT 系 fastsat (既刊 pinned @2e9ec4c5…): n5_ge10_strong (既知 UNSAT) を
     **UNSAT 12,583 conflicts / 2.6s** で判定 (n5 で 2 系一致)。
   - ただし n7_ge15_strong / n8_ge16_strong は予算内 TIMEOUT
     (280s でそれぞれ 197,359 / 82,904 conflicts、約 300-705 conf/s)。
     ポートフォリオ (cellphase=0 / seed=7 / base=64) でも 90s で届かず。
   - よって**ラダーゲート未達**として n9_ge19_strong への fastsat 投入は
     見送り (小さい既知 UNSAT を閉じられない符号化・環境で対象を実行しても
     確証が出ない)。これは予定内の受け入れ条件 4 (INDET honest negative) の経過。

## バグ 2 件 (生成器で発見・修正、制御で捕捉)

- **bug1** 鏡像節内リテラル 0 出力 (13,662 行の「... 0 0」= 不正 DIMACS)。
  ソルバ実行前の構造検証 + eval_strong 節数不一致で捕捉。
  通過していれば空節として**偽 UNSAT**を返しうる状態だった。
- **bug2** 対角・境界の上界鏡像 (`s(1,1)->x_1`, `s(i,i)->x_i`) 欠落。
  **既知 UNSAT ネガティブ制御**で捕捉: fastsat が n5_ge10 に 0 conflicts で
  偽 SAT (8 cell True で全節充足) を返した。修正後 n5-10 は正しく UNSAT。
  この種の欠落は正制御では絶対に検出できない。
- **既刊監査 (参照のみ)**: 同型パターンを持つ n9-k9-upper-sat-20261115 の
  gen_n9_cnf.mjs を監査し、**定数置換が正しく健全** (c1 が常に x_i を含む) と
  確認。同レーンのファイルは変更していない。

## 次回までの再開手順

実験 dir の README「再開手順」に記載 (FNV 照合 → 較正ゲート (n7/n8 既知 UNSAT
を fastsat で閉じる) → n9_ge19_strong 投入、ksearch 系は宣言方法 (a) の
chunk resume。両系一致でのみ判定出版)。

2026-11-20 高速レーン
