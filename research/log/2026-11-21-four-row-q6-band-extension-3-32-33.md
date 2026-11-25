# 2026-11-21 four-row q=6 第3次帯延伸（m=32,33）— M_{4,6} = 16 or ∈ [34,103]

レーン: four-row (w=4) q=6/q=7 frontier（単一オーナー宣言 528ec960 の継続・同日 4 度目の band extension）。第2次帯延伸（m=30,31・commit 46ad35fd/b16120a0）に続いて q=6 の witness-free band をもう 2 幅延伸した。先行セッション（2026-11-21 環境喪失）が m=32,33 を掃引済みだったが出版前に失われた値を含めて再実行・出版した。

## 実行記録

1. **較正 (4,31,6)**: genfast3.js（md5 12c2bd9c…・closure 実験 dir 出版と byte-identical・SEVEN_SCRIPTS 参照・core は frontier sat2.js 282ae832…）を再取得し q=6=w+2 に適用。生成 CNF md5 `7c6acc085ddf1820b4742bd2c47286a6` が第2次帯延伸の出版 CNF（s4x31q6_def）と byte 一致・curves 866/vars 19246/clauses 66931 同一。較正 meta: output/q6ext3/calib_4x31q6_genfast3.json。
2. **掃引（各幅 2 回の独立実行・conflicts bit-exact）**: (4,32,6) UNSAT（conflicts 4,272,621・process-time 292.77 / 295.78 s・rc=20）、(4,33,6) UNSAT（conflicts 4,410,392・328.25 / 323.28 s・rc=20）。pinned kissat 4.0.4（md5 3a5eba83…・公式 rel-4.0.4 linux-amd64 zip から再取得し同一 md5 確認）。sec_cap null=上限なし実行（nohup 単独 detached 実行で shell の実行時間上限を回避・同時複数プロセスは次コマンド開始時killされるため 1 プロセスのみ）。生成は genfast3 0.1 s/幅・vars 20609/21972・clauses 71672/76413・curves 929/992・CNF md5 65255d98…/bf058f40…。solve log（双実行 4 本）: output/q6ext3/。
3. **独立先行実行との一致**: 環境喪失前の前セッション（非出版・2026-11-21 深夜）の記録値 (4,32,6) 4,272,621（2 回実行 294.05/320.15 s）・(4,33,6) 4,410,392（368.50 s）と conflicts bit-exact 一致（実行環境を跨いだ決定性の交叉確認）。出版の正本は今回実行。
4. **追記（commit: records 114→116）**: scripts/append_records_q6b.js。fail-closed: 入力 114 件検査・s4x31q6_def 親レコード較正 pin（vars/clauses/curves/cnf_md5/conflicts）・q6ext3/ の live gen meta・双実行 solve log との照合（conflicts・verdict・exit・process-time・run 間一致）・tag 冪等。
5. **負の結果（先行セッション記録・非権威）**: m=32 の plain-def 280 s cap は打切り時 4,060,733 conflicts・lex=H 200 s cap は 2,921,868 conflicts でいずれも cap 下 INDET（今出版の上限なし実行で m=32 は 4,272,621 conflicts・約 293-296 s で完全決着）。lex=H は決定的加速ではない。m=34 以降は 1 幅あたり外挿 ~340-420 s で長時間実行か解析的排除が引き続き課題。

## 結論

- q=6 witness-free band **16..33** → **M_{4,6} = 16 or M_{4,6} >= 34**（K0821/K1134 規約）。U_{4,6}=103（K0318）と組み合わせ **M_{4,6} = 16 or ∈ [34,103]**。残る未掃引幅: 34..102（69 幅）。
- K1177 に第3次帯延伸節を追記・K1182 の q6 注記を値更新・frontier README と knowledge README（K1177/K1182 bullet）の数値を更新。
- 標準 11×11 空盤・二石 root 等の未解決局面には影響しない（固定幅レーン）。有限掃引のみで、未掃引幅への主張はしない。REFUTED-D10 は LOSS 証明ではない。

## 制約の遵守

- branch/PR なし・main 直接。push 前に最新 main 取得（base の md5 突合）・全編集は anchor 一意性検査つき差分置換・knowledge README は挿入可逆性検査（挿入語句を削除して原文に byte 等価で戻ることを機械確認）・fetch-back 全ファイル byte 検証。
- 有限実験を全称定理として過大主張していない（本延伸は規約形の更新であり、M_{4,6} の確定ではない）。
