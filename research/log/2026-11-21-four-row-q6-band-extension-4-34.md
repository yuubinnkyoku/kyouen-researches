# 2026-11-21 four-row q=6 第4次帯延伸（m=34）— M_{4,6} = 16 or ∈ [35,103]

レーン: four-row (w=4) q=6/q=7 frontier（単一オーナー宣言 528ec960 の継続・同日 5 度目の band extension）。第3次帯延伸（m=32,33・commit ebda281e/9e0fb740）に続いて q=6 の witness-free band をもう 1 幅延伸した。

## 実行記録

1. **較正 (4,33,6)**: genfast3.js（md5 12c2bd9c…・第3次帯延伸で較正済みの同一バイナリ）を q=6=w+2 に適用。生成 CNF md5 `bf058f40f6bd70a4f00ddfdf72f01f72` が第3次帯延伸の出版 CNF（s4x33q6_def）と byte 一致・curves 992/vars 21972/clauses 76413 同一。較正 meta: output/q6ext4/calib_4x33q6_genfast3.json。
2. **掃引（2 回の独立実行・conflicts bit-exact）**: (4,34,6) UNSAT（conflicts 4,480,309・process-time 311.94 / 312.58 s・rc=20）。pinned kissat 4.0.4（md5 3a5eba83…）。sec_cap null=上限なし実行（nohup 単独 detached 実行）。生成は genfast3 0.1 s・vars 23419・clauses 81446・curves 1059・CNF md5 `1f58cdfc895ef4de493528ebf40d33f2`。solve log（双実行 2 本）: output/q6ext4/。
3. **独立先行実行との一致**: 第1実行（環境リセットで生ログ喪失・非出版・353.53 s）の記録値も conflicts 4,480,309 と bit-exact 一致（実行環境を跨いだ決定性の交叉確認・今回の出版 2 本が正本）。実行環境の detached 実行の不安定さにより第2実行の確定まで 2 度のインフラ打切り（~10 s 時点・296 s 時点 4,300,893 conflicts・いずれも判定には非寄与）を経て、投入呼び出しを短縮した運用（即時 launch + 別呼び出しの light poll + 短い完了確認）で確定した。
4. **追記（commit: records 116→117）**: scripts/append_records_q6c.js。fail-closed: 入力 116 件検査・s4x33q6_def 親レコード較正 pin（vars/clauses/curves/cnf_md5/conflicts）・q6ext4/ の live gen meta・較正 meta・双実行 solve log との照合（conflicts・verdict・exit・process-time・run 間一致）・tag 冪等。
5. **外挿**: conflicts 3.09M/3.49M/4.27M/4.41M/4.48M（m=30..34・単調増加が継続）。1 幅あたり ~330-430 s で残り 68 幅（35..102）の掃引は生成壁なし・計算資源の逐次投入で閉包可能。lex=H は決定的加速ではない（第3次帯延伸の負の結果を継承）。

## 結論

- q=6 witness-free band **16..34** → **M_{4,6} = 16 or M_{4,6} >= 35**（K0821/K1134 規約）。U_{4,6}=103（K0318）と組み合わせ **M_{4,6} = 16 or ∈ [35,103]**。残る未掃引幅: 35..102（68 幅）。
- K1177 に第4次帯延伸節を追記・K1182 の q6 注記を値更新・frontier README と knowledge README（K1177/K1182 bullet）の数値を更新。
- 標準 11×11 空盤・二石 root 等の未解決局面には影響しない（固定幅レーン）。有限掃引のみで、未掃引幅への主張はしない。REFUTED-D10 は LOSS 証明ではない。

## 制約の遵守

- branch/PR なし・main 直接。push 前に最新 main 取得・全編集は anchor 一意性検査つき差分置換・knowledge README は挿入可逆性検査（挿入語句を削除して原文に byte 等価で戻ることを機械確認）・fetch-back 全ファイル byte 検証。
- 有限実験を全称定理として過大主張していない（本延伸は規約形の更新であり、M_{4,6} の確定ではない）。
