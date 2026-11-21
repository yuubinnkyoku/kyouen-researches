# 2026-11-21 four-row q=6 第2次帯延伸（m=30,31）— M_{4,6} = 16 or ∈ [32,103]

レーン: four-row (w=4) q=6/q=7 frontier（単一オーナー宣言 528ec960 の継続・同日 3 度目の band extension）。q=7 closure（K1182・b9829794/a4feaec4 着地直後）に続いて q=6 の witness-free band を延伸した。

## 実行記録

1. **較正 (4,29,6)**: genfast3.js（md5 12c2bd9c…・six-row-q8-band-closure 出版と byte-identical・SEVEN_SCRIPTS 参照・core は frontier sat2.js 282ae832…）を q=6=w+2 に適用（q ≥ w+2 完全性論）。生成 CNF md5 `95816b6c04c14de5f0256ca871dfcc97` が s4x29q6_def の sat2.js 出版 CNF と byte 一致・curves 748/vars 16688/clauses 58033 同一。較正 meta: output/q6ext/calib_4x29q6_genfast3.json。
2. **掃引**: (4,30,6) UNSAT（conflicts 3,091,289・process-time 202.54 s・rc=20）、(4,31,6) UNSAT（conflicts 3,492,659・237.06 s・rc=20）。pinned kissat 4.0.4（3a5eba83…）。sec_cap 280 は運用上の壁時計予算（kissat 自身は無制限実行・両幅とも予算内に完了）。生成は genfast3 0.2/0.1 s・vars 17967/19246・clauses 62482/66931・curves 807/866。solve log: output/q6ext/。
3. **独立先行実行との一致**: 環境喪失前の前セッション（非出版・staging 喪失）の記録値 (4,30,6) 3,091,289 / (4,31,6) 3,492,659 と conflicts bit-exact 一致。出版の正本は今回実行。
4. **追記（commit 46ad35fd）**: scripts/append_records_q6.js で records.jsonl 112→114。fail-closed: 入力 112 件検査・s4x29q6_def 親レコード較正 pin・q6ext/ の live gen meta・solve log との照合（conflicts・verdict・exit・process-time）・tag 冪等（再実行で拒否を確認）。
5. **負の結果（先行セッション記録・非権威）**: m=32 は plain-def 280 s cap で INDET（打切り時 4,060,733 conflicts）・def+lex=H 200 s cap でも INDET（2,921,868）。lex=H は決定的加速ではない。m=32 以降は長時間実行か解析的排除が引き続き課題。

## 結論

- q=6 witness-free band **16..31** → **M_{4,6} = 16 or M_{4,6} >= 32**（K0821/K1134 規約）。U_{4,6}=103（K0318）と組み合わせ **M_{4,6} = 16 or ∈ [32,103]**。残る未掃引幅: 32..102（71 幅）。
- K1177 に第2次帯延伸節を追記・K1182 の q6 注記を値更新・frontier README と knowledge README（K1177/K1182 bullet）の数値を更新。
- 標準 11×11 空盤等の未解決局面には影響しない（固定幅レーン）。有限掃引のみで、未掃引幅への主張はしない。

## 制約の遵守

- branch/PR なし・main 直接。push 前に最新 main 取得・全編集は anchor 一意性検査つき差分置換（1回の変換ミスを fail-closed が捕捉）・fetch-back 全ファイル byte 検証。
- 有限実験を全称定理として過大主張していない（本延伸は規約形の更新であり、M_{4,6} の確定ではない）。
