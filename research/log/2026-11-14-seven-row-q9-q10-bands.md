# 2026-11-14 高速レーン — 7行 q=9/q=10 witness帯のkissat交叉確認・延長・(7,9) witness探索とK0820統合

## 背景

`seven-row-inband-families-20261114`（13:22 push・commit 32fdcac3）は
(7,10) witness m=10..18・fastsat def+lex UNSAT 帯 m=19..40・(7,9) witness m=9..14・
U_{7,q}/U_{8,q} 表を含むが、**K項目化・CSV行・log が一切ない未統合実験**だった。
また UNSAT 帯は単一カスタムCDCL（fastsat）のみの根拠で、repoの水準
（K0816/K0818/K0819 は kissat 主体）より弱い。本実行はこの確認・延長と
(7,9) 前線の推進・統合を1回で完了させた。

## 判断と作業

1. **符号化の健全性確認**: sat2.js の def 単一節（∨¬rowGe[y]）は
   「総石数 < w(q−1) ⟺ ある行 ≤ q−2」（行は長さ m ≥ q の直線で安全から各行 ≤ q−1）
   により行欠損存在の完全符号化。節は H/V/HV 不変なので def+lex=H,V,HV は健全
   （K0815 第4弾の「lex は UNSAT 側に有効・SAT 側に有害」の教訓どおり、
   (7,9) witness 探索は lex なしで実行）。
2. **(7,10) 帯の交叉確認**: m=19..40 の CNF を決定的再生成し fastsat を走らせたところ
   **全22幅で conflicts が元実験 results.jsonl と bit-exact 一致**（同一インスタンス性の較正）。
   kissat 4.0.4 が全幅 UNSAT。制御 2×8/2×9 q=4 も bit-exact（121/535）。
3. **(7,10) 帯の延長**: m=41..51 を fastsat+kissat 両方で UNSAT（ worst m=46: 15,399
   fastsat conflicts・m=36: 41,278）。→ witness-free 帯 {19..51}・M_{7,10} = 19 or ≥52。
4. **(7,9) witness 探索**: m=15..23 がすべて SAT（55石・m=15のみ54石）。
   全witnessを census 不使用 JS verifyConfig + Python Fraction の2系統で検証 PASS。
   → witness 幅 {9..23}（m=9..14 は元実験）・下界 M_{7,9} ≥ 24。
5. **(7,9) 不在帯**: m=24..33 が kissat def-nolex で全幅 UNSAT（43,743〜94,368 conflicts）。
   m=24/33 は def+lex 別符号化でも UNSAT。
   **負記録**: fastsat は m=24 を 60秒 cap で解けず（210k conflicts TIMEOUT）—
   (7,9) 帯は kissat 単独であり (7,10) 帯（2ソルバ一致）より根拠水準が一段低い。
   K0820 に明記。
6. **統合**: K0820 新設（kind: proposition, status: computed）・mwq CSV に
   (7,9) "{24},34..613"・(7,10) "{19},52..587" の2行追加・
   実験 `seven-row-q9-q10-bands-20261114`（scripts 3 + README + report + output
   records/summary/witness/kissat 生ログ）。

## 運用メモ

- 本セッションで実行環境リセット2回（290秒タイムアウトでワークスペース消滅）。
  両方とも決定的再実行で**全記録数値が bit-exact 再現**（fastsat 較正値・kissat
  conflicts とも）。この再現性の記録自体が K0820 の evidence に含まれる。
- リセットの原因は (7,9) UNSAT 帯への fastsat 275秒 cap 交差確認（1インスタンスが
  cap まで燃焼）。以後の教訓: **交差確認ソルバには短い cap（60秒）を設定し、
  TIMEOUT は正記録として残す**。
- (7,9)/(7,10) は w=7 の帳尻2ファミリー（q≥11 は分離帯で M=q−1 既証明）。
  残る w=7 の open は (7,4..8)。（8,q) は q=4..12 が open・U 表は既存。
- views再生成（generated/・root README）は統合レーンに委ねる（K0820 は
  generated 未反映・CSV/README は本コミットで更新）。

## 次の一手（レジューム）

1. **(7,9) 7×34 以降の不在帯延長**（kissat 単独・1幅あたり~40秒）。
   どこまで伸びるか。並びに (7,10) 7×52 以降（符号化時間が O(m^3) で増加）。
2. **(7,8)・(7,7) の同型調査**（witness 帯の端・不在帯の開始点。q=8 は
   U=651・(6,8) との比較が面白い）。
3. **(8,9)/(8,10) への拡張**（U=984/940。8行盤の census は w=7 と同程度に軽い）。
4. K0342 型 tail 評価（U=613/587 を大きく下げられれば M 確定に直結）。

**11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN**
（本成果は固定幅Mの話で無盤面勝敗に無関係）。
