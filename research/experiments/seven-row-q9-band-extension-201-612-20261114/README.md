# seven-row-q9-band-extension-201-612-20261114

COMPLETED 2026-11-15. K0820 (7,9) witness-free band was 24..200 (m=101..200 by
seven-row-q9-q10-band-extension-101-200-20261114). 本実験は残る幅 **m=201..612**
を掃引した結果、**全 412 幅が kissat UNSAT**（deficient band、200s cap 内で
全幅決着、最難幅も 5.5 秒）。K0318 substitution 上界 U_{7,9}=613 と組み合わせて
**M_{7,9} = 24 が exact に決着**した。

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
  曲線列挙順（線→円・pts 昇順）も同一にすることで **CNF バイト一致**を検証で確認
  （scripts/controls_genfast3.json: 7×24/30/45q10/51/60rowY3 vs genfast.js、
  7×101/110lex H,V,HV/150/200・8×26 vs genfast2.js、全て 0 diff）。
- 制約: genfast3 は q ≥ w+2 限定（q = w+1 では二重行 1 つの q 点円が存在し得るため
  assert で拒否 — その場合は genfast/genfast2 を使う）。
- ソルバ: kissat 4.0.4 official linux-amd64・200s cap（実際は全幅 ≤5.5 秒）。

## 結果（2026-11-15 掃引完了）

- **m=201..612 の全 412 幅: UNSAT**（kissat exit 20、conflicts 14082..36876、
  process-time 0.98..5.49s、m=612: vars=107928 / clauses=392741 / curves=1217）。
  records.jsonl に per-width レコード、kissat_summaries.jsonl に per-width
  conflicts/process-time/max-RSS と生ログ md5。
- **lex 交差検証**: m=300/400/500/612 × lex=H,V,HV の12件すべて UNSAT
  （lex_records.jsonl、生ログのうち m=612 の3本を raw-logs/ に格納）。
- 生 kissat ログ: 全 412 幅分を作業環境で保持したがrepoには
  代表幅（201/306/400/505/612 + lex m=612 H,V/HV）のみ格納。
  全幅の要約（conflicts・process-time・exit 20 確認済み・log_md5）は
  kissat_summaries.jsonl で機械検証可能。

## 決着の構成（M_{7,9} = 24 exact）

1. witness 幅 9..23: (7,m,9) SAT 構成（K0820）→ M_{7,9} ≥ 24
2. witness-free 24..200: K0820 + m=101..200 掃引（前実験、全 UNSAT）
3. witness-free 201..612: 本実験（全幅 UNSAT・完全列挙）
4. m ≥ 613 の持続性: K0318 substitution 上界 U_{7,9}=613
   → よって **M_{7,9} = 24**（行欠損極大が存在する最小幅は 24、
   それ以降 m≤612 では存在せず、m≥613 では substitution 補題により非存在）。

## スコープ

有限機械検証（census 完全性・kissat 正確性まで）。m=201..612 の各幅 UNSAT は
その幅の行欠損極大非存在の完全証明。決着は K0820/K0318 と組み合わせた
machine-verified chain による（reviewer は各リンクのK項目・records を参照）。

## scripts/

- genfast3.js: 弦対抽象円 census 生成器（scripts/controls_genfast3.json に
  byte-identity 検証記録）
- leanband3.sh: 1 幅分の genfast3→kissat→record パイプライン
- batchband3.sh: 連続幅バッチ（wall-clock guard 付き）
