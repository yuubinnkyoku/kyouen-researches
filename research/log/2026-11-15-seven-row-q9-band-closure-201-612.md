# (7,9) 帯閉包 201..612 完走 — M_{7,9} = 24 exact（w=7 で2例目・M_{7,10}=19 に続く）

実験: research/experiments/seven-row-q9-band-extension-201-612-20261114
知識: K0820 追記5・results/fixed-width/mwq_stabilization.csv (7,9) 行 → exact-threshold M=24 proved
（results/fixed-width/README.md の exact-threshold 10件・bounds 11件に更新）

## 決着の構成

1. witness 幅 9..23（K0820: 52..55石・2系統検証済み）
2. witness-free 24..200（K0820 + seven-row-q9-q10-band-extension-101-200-20261114）
3. witness-free 201..612（本レーン: 全412幅 kissat 4.0.4 def-mode UNSAT・INDET 0・SAT 0）
4. m >= 613 は K0318 substitution U=613（proved）で witness 不可能在
→ **M_{7,9} = 24**。

## 本レーンの新規技術成果: genfast3.js（弦対抽象円census）

- q ≥ w+2 では任意の q 点円は鳩の巪原理で ≥2 つの二重行を持つ。二重行対 (ya,yb) の
  弦長対 (ℓ,ℓ')（ℓ≡ℓ' mod 2 が必然）から円の (v,ρ²) が u 非依存に厳密決定される
  （閉形式: B_y = 16δ·E_y, E_y = δℓ² + 4δ(ya−y)(y−yb) + (ya−y)(ℓ²−ℓ'²)、
  完全平方判定 E_y = δk²・寄与条件 k ≡ ℓ (mod 2)・u = j/2 窓走査）。
  全 (ya,yb,ℓ,ℓ') 列挙で O(C(w,2)·m²·w)。m=612 生成 ~1 秒（genfast/genfast2 の
  O(w·m³) ペア走査では同幅 ~53 秒かつメモリ2GB超で実行環境の上限に抵触）。
- 線census: q ≥ w+1 では ≥q 点直線は w 本の水平行のみ（非水平線は各行と ≤1 点）なので
  行から直接構築。ペア走査 Map のメモリ問題（m=612 で ~920万エントリ）を完全解消。
- CNF byte-identity: genfast.js（7×24/30/45q10/51/60rowY3）・genfast2.js
  （7×101/110lex=H,V,HV/150/200・8×26）との cmp 0 diff・計13対照
  （scripts/controls_genfast3.json・md5 12c2bd9c）。sat2.js 符号化を monkey-patch で
  verbatim 再利用のためエンコード drift ゼロ。
- 制限: q = w+1 では単一二重行の q 点円が存在し得るため assert で拒否（q ≥ w+2 限定）。
  開発中の最初の閉形式導出で a+b の展開を誤り一時的に不一致が出たが、家族円
  (2x−(2k+1))²+(2y−5)²=50 の (0,6) 弦対 (5,1) による直接検証で修正（負記録）。

## 掃引結果

- m=201..612 全412幅: kissat 4.0.4 UNSAT（conflicts 14,082..36,876・process-time 0.98..5.49s・
  200s cap 内完走・INDET 0・SAT 0）。m=612: vars=107,928 / clauses=392,741 / curves=1,217
  （7行 + 1,210 円・2m−14 構造・≥10点円分類（e944f0c）と整合）。
- 別符号化交差確認: def+lex=H,V,HV @ m=300/400/500/612 の12件すべて UNSAT
  （lex_records.jsonl・conflicts 15,505..29,839）。
- 証拠輸送: records.jsonl（412行）・kissat_summaries.jsonl（412行・log_md5 結合）とも
  GitHub blob md5 で byte-exact 着地を検証（q10 閉包レーンが記録した read_file 64KB
  トランケーション障害は was_truncated/next_offset ループで回避・末尾改行喪失なし）。
  生ログはrepoに代表幅のみ格納（201/306/400/505/612・lex m=612 H,V/HV）。
  lex_records.jsonl 初回 push の無効 JSON（sec: 2s・シェル awk の引用バグ）は
  raw ログから再解析して即修復。
- 較正: m=200 相当の band-extension レーン record との回帰確認に加え、
  13対照バイト一致がインスタンス同一性を保証。

## 帰結と波及

- **M_{7,9} = 24 exact**: M_{7,10}=19 に続く w=7 で2例目・w≥6 でも2例目の完全決着。
  mwq_stabilization.csv は exact-threshold 10件・bounds 11件に。
- genfast3.js は (7,10) 閉包（追記4）で再利用済み。q ≥ w+2 の帯閉包
  （8行 q=10/11、(7,11) q=13 など・m 数百の掃引）に直接適用可能。
- w=7 の残る open: (7,4)/(7,5)/(7,6)/(7,7)/(7,8)（前線 7×22/32/27/27/25）。
  (7,8) は q=8 = w+1 で genfast3 の前提外（単一二重行円が可能）— genfast2 延長か
  rowY 分解が引き続き必要。q=9/10 の両帯は閉じた。
- 11×11 root 証明（WIN7/LOSS7）には無関係・無影響（本レーンは7行帯のみ）。

## 運用メモ

- 1実行で閉包まで完走（生成器開発→13対照検証→412幅掃引→lex交差確認→統合）。
  実行環境の ~290 秒ハードストップは batchband3.sh の適応ガードで回避（5バッチ分割）。
- 並走(q10)レーンとの衝突なし: push前に最新mainを再取得し、K0820 追記4（q10閉包）を
  取り込んだ上で追記5として追記。CSV の (7,10) 行は本レーン不変。
