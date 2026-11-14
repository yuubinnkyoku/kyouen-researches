# seven-row-q9-band-extension-201-612-20261114

IN FLIGHT (claim). K0820 (7,9) witness-free band is 24..200 (m=101..200 by
seven-row-q9-q10-band-extension-101-200-20261114). 本実験は残る幅
**m=201..612** を掃引し、K0318 substitution 上界 U_{7,9}=613 と組み合わせて
**M_{7,9} = 24 の完全決着**（または帯内 SAT witness の発見・その場合は
M_{7,9} の下界更新と witness dual-verify）を目指す。

## 手法（新生成器 genfast3.js — 弦対抽象円 census）

- 完全性の根拠: q ≥ w+2 では任意の q 点円は鳩の巪原理で **≥2 つの二重行**
  （同一行に2格子点を持つ行）を持つ。二重行対 (ya,yb) の弦長対 (ℓ,ℓ') から
  円の (v, ρ²) が**u 非依存に**厳密に決まる（両弦の中心 x が同一の u）。
  全 (ya,yb,ℓ,ℓ')（ℓ≡ℓ' mod 2 必須）を列挙して抽象円を生成し、
  各行 y の t''² = ρ²−(y−v)² が (4δk'')² 型の完全平方で k'' ≡ ℓ (mod 2)
  の行だけが点を寄与する。残る自由度は u（半整数・窓内）だけで、
  窓走査で点数を数え ≥q 点の円だけを残す。計算量 O(C(w,2)·m²·w)
  — genfast/genfast2 の O(w·m³) ペア走査より桁違いに軽い。
- 線 census: q ≥ w+1 では ≥q 点の直線は w 本の水平行のみ（非水平線は
  各行と高々1点で交わり ≤w<q 点）なので、行から直接構築（ペア走査不要）。
- genfast.js / genfast2.js と同じく S.buildCensus を monkey-patch し
  sat2.js の符号化を verbatim 再利用（エンコード drift ゼロ）。
  曲線列挙順（線→円・pts 昇順）も同一にすることで **CNF バイト一致**を検証で確認する
  （scripts/controls_genfast3.json: 7×24/30/45q10/51/60rowY3 vs genfast.js、
  7×101/110lex H,V,HV/150/200・8×26 vs genfast2.js、全て 0 diff）。
- 制約: genfast3 は q ≥ w+2 限定（q = w+1 では二重行 1 つの q 点円が存在し得るため
  assert で拒否 — その場合は genfast/genfast2 を使う）。
- ソルバ: kissat 4.0.4 official linux-amd64・200s cap。
- m=612 参考値: curves=1217（7行 + 2m−14=1210 族円）、vars=107928、
  clauses=392741、生成 ~1s。

## スコープ

有限機械検証（census 完全性・kissat 正確性まで）。m=201..612 の各幅 UNSAT は
その幅の行欠損極大非存在の完全証明。全幅 UNSAT の場合、witness 幅集合 {9..23}
（K0820）・witness-free 24..200（K0820 + 前実験）・m ≥ 613 の持続性
（K0318 substitution U=613）と合わせ **M_{7,9} = 24 が exact に決着**する。

## 進捗

- 2026-11-15: genfast3.js 実装完了・全対照サンプルで CNF バイト一致を確認
  （controls_genfast3.json）。掃引 m=201..612 は後続コマンドで実施。
