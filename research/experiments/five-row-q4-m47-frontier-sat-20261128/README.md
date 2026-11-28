# (5,4) 5x47 前線 SAT 攻撃 — 第1セッション (2026-11-28 高速レーン)

単一オーナー宣言: research/log/2026-11-28-five-row-q4-m47-frontier-sat-declaration.md (commit 86eb9df6・宣言時 HEAD pin b841063a・publish-then-execute)。

## 位置づけ

- M_{5,4} ∈ [47, 567] (下界: five-row-q4-band-45-46-surgery-20261121 の m=45/46 witness・上界 T_5=567)。
- m=47 は surgery budget 2/3 scoped negative のみで UNDETERMINED だった。本セッションが初の m=47 SAT 攻撃。
- 結果: 全 piece INDET (honest negative・不在主張なし)。M_{5,4} ∈ [47, 567] 不変・前線 5x47 のまま。

## 器材

- 生成器: sat3.js streaming rowfixed (six-row-q4-m47-rowY0-oom-20261115 kit 出版 byte・sha256 aa9a0f38…) + core sat.js (sha256 fcc0cfd8…)。q=4 ≤ w=5 の all-triples census を streaming で通す (sat2 直系は 5x39 でも heap OOM)。
- ソルバ: kissat 4.0.4 static linux-amd64 (sha256 pin 21da5d98…・出版 pin と同一 binary)。
- 新規部品 scripts/pin.js: rowfixed CNF に krow (欠損行の正確な石数 k・sat3s の counter() を verbatim 使用) と minpos (欠損行左端石ピン・sound H-split p ∈ 0..floor((m-1)/2)=23) を後段追加するピン層。header 書換・append は決定的。

## 較正・対照 (全て PASS)

1. 5x39 rowY=1 lex=H,V,HV = SAT 21,147 conflicts = 出版値 bit-exact (four-row-q4-q5-frontier-20261115 の m=39 記録と同一)。
2. 5x39 rowY=1 lex 無し = SAT 13,787 conflicts・CNF md5 5e59b097… は環境リセット跨ぎで同一 (cross-reset bit-exact)。14石 witness rows [3,2,3,3,3] row1 x=[37,38]。
3. pin.js 対照電池: 14 witness 石を unit ピン → SAT 0 conflicts (cell var 写像・append 機構)。13 石 + unsafe 点 (0,0) → UNSAT 0 conflicts (fail-closed)。H-image witness + krow=1:2 + minpos=0 chain → SAT 0 conflicts (krow chain / minpos semantics を既知 witness で検証)。5x39 k=2 p=20 (音域外) → SAT 29,220 (ピン付き witness 発見の実演)。
4. 開示: 初版 pin.js の自作 sequential counter に符号化バグがあり偽 UNSAT (0 conflicts) を返した → 対照電池で即検出 → sat3s の exported counter() に差し替え (zero drift)。偽の値は records に含めない。

## 記録 (output/records.jsonl)

- pre-reset 観測 (rowY=0/1/2 lex=H,V,HV 270s・rowY=1 lex 無し 270s・全て UNKNOWN・raw log は環境リセットで消失・conflicts は決定的軌跡の記録値として開示): 14,182 / 8,494 / 8,649 / 10,962。
- post-reset: rowY=1 krow=1:2 minpos p=0..6 @225-240s 全て UNKNOWN (9,083-11,154・ほぼ一様抵抗)・lex=H base p=0 @210s UNKNOWN 10,210。実行環境がセッション末に不安定化し .out raw の出版はできず、conflicts 値は records.jsonl に保存 (決定的 bookkeeping)。
- 硬さ較正 m=46: rowY=1 lex 無し @225s UNKNOWN 11,316 — m=46 は R=46 placement (既知 SAT・V-image は rowY=1 に入る) なのに 225s では発見できず → この幅では 225s 級 cap は SAT 側でも不十分。m=47 の INDET 群は不在を示唆しない。

## 手引き (次回)

- bash 1呼び出し ≤300s の制約上、実効 cap ~270s。決着には (a) 長時間実行可能な環境での深 cap (600-1200s)、(b) 別符号化 (counter=tot・lex 組み合わせ)、(c) k=2 残り minpos p=7..23・k=1 p=0..23・k=0 の掃引、(d) m=46 既知 witness を種にした bounded surgery budget ≥4、が候補。
- 生成は全て決定的 (CNF md5 を records に pin)。verdict 不消費。標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・全 closure class は全時点 UNKNOWN。
