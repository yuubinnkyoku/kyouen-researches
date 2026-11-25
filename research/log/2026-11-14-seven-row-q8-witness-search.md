# 2026-11-14 7行 q=8 witness 探索（新ファミリー (7,8)・witness 7×8..7×24）

高速レーン第9回。repo最新mainを確認し、並走レーン（n11 class2-lane・class4-lane・
w8q9 witness探索・素数census等）の宣言領域を回避して、未着手だった
**(7,8) ファミリー**（mwq_stabilization.csv に行すらない・K0318 上界 U=651 のみ既知）
の行欠損witness探索を選定した。

## 経過

1. **環境再構築**: 今回のsandboxにはコンパイラ・パッケージマネージャがなく
   kissat をソースビルドできないため、**kissat 4.0.4 公式 linux-amd64
   リリースバイナリ**を使用（READMEの記載通り・変更なし）。
2. **較正**: (a) 2×8/2×9 q=4 def+lex 制御が K0820 controls と bit-exact
   （fastsat 121 SAT / 535 UNSAT）、def 単独でも両ソルバ一致（81/2002・65/1268）。
   (b) (7,10) m=46 def+lex 再生成で kissat 861 conflicts・K0820 q10-band と
   bit-exact（インスタンス同一性）。 (c) genfast.js を q=8 で初適用し
   sat2.js と CNF バイト一致を4サンプル（m=9,12・lex有無）で検証
   （genfastの半整数中心保証は q≥w+1 に依存し q=8 は境界ケース）。
3. **witness探索 m=8..23**: 全幅 SAT。m=8,9 は38石（deficiency 11）、
   m=10..12 は 45,46,47石、m=13..23 は単一欠損48石。
   conflicts は m=19 で 4,717 → m=22 で 681,530 → m=23 で 1,325,637 と急増。
   全witness 2系統検証 PASS。
4. **実行環境リセット1回**（m=23/24 同時実行の290sコマンドタイムアウトが原因・
   既知の運用教訓の再発）: m=8..22 を再生成し全 conflicts bit-exact 復元
   （cross-reset決定性の追加証拠）。以後バッチを細かくして push も早めに実施。
5. **m=24**: def OR 実例は 240s で INDET（3,829,302 conflicts）・lex 付きでも
   INDET（3,710,480）。**rowY=3 固定分解**（欠損行を第4行に固定・sat2 --rowY）で
   641,005 conflicts（41秒）で SAT・48石 witness [7,7,7,6,7,7,7] 2系統検証 PASS。
   → **witness 7×8..7×24・M_{7,8} ≥ 25**。
6. **m=25**: rowY=3 分解でも 250s で INDET（3,534,747 conflicts）。
   他3行クラス（V対称で全4クラス）は未走査。正直な負記録として記録。

## 判断メモ

- m=24 の OR→行固定分解の劇的緩和（3.8M INDET → 641k SAT）は、
  (7,8) 帯の以後の評価方針を行固定分解軸にする根拠。K0816/K0818/K0821 の
  行鏡映クラス分割（不在証明側）と対になる、SAT側の分解。
- (7,9) では witness が m=23 で止まり m=24 が容易に UNSAT（43,743 conflicts）だった
  のに対し、(7,8) は m=24 でも witness が存在し両向きに難化。
  q が小さいほどwitness帯が長い傾向と整合（(6,8) と同様の難化予想）。

## 次の一手

1. (7,8) 7×25 以降: rowY=0..3 の4クラス走査（SAT なら前線前進・全 UNSAT なら
   row-mirror class-split で不在確定の候補）。
2. (7,7)（q=7=w・genfast不适用・sat2.js の全三つ組censusは m~30 まで実用）
   のwitness探索 — 次の未着手ファミリー。
3. (7,9)/(7,10) 帯延長 m=101..200（軽い・lean2相当の genfast+kissat）。

11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN
（固定幅Mの更新は無盤面勝敗に無関係）。
