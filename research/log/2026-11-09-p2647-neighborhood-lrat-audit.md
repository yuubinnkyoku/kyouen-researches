# 2026-11-09 1303点要求の有界近傍CNFを独立LRAT検査

AGENTS・knowledge README・K0693/K0702/K0706/K0711と最新log・experimentを確認した。
fetch・status・実行中プロセスを調べ、同じ対象の計算は実行されていなかった。
開始mainはf6fa3c9d。他者の未追跡shape出力2件は保持した。
origin/mainのa2e89dd8（binary-cubeのside-support証明1ファイル）をmergeした。

## 検査経路の変更

前回の保存1302点から除去3点以下で1303点以上を要求するCNFはSOLVER_UNSATだったが、
削除を保持するRUP-only実装では120秒でtimeoutした。
同じSAT探索や同じ120秒監査を反復せず、既存の固定DRAT-trimと修正LRAT検査器を選んだ。
元の36457変数・126721節の入力と325093行のDRATは変更していない。

DRAT-trim -Uは11.891秒でVERIFIED。25007 core lemmas、0 RAT、10914690 resolution steps。
抽出LRATは43074行・80008871 bytes、SHA-256は
`af1214d3c8eb33246b19a56ace712c137df89d034c2b311d7e5626f967797cfe`。
空節に実際のRUP矛盾を要求する既存修正版lrat-checkで元CNFに対し再生し、6.201秒・終了コード0で受理した。
変換器のVERIFIEDと、別実装によるLRAT自体の受理を区別して記録した。

## 証拠と信頼境界

実入力を元の凍結ソースからbyte再生成し、追加除去counterの予約上限・点選択変数領域を照合した。
元DRAT・LRAT・ソース・受理receiptのhash照合も成功。
DRAT-trimの6制御と修正LRATの5制御が期待通り。K0707/K0714の既知偽証明を拒否し、
原版LRATの偽受理も再現した。原版の受理は採用しない。

約80MBのraw LRATはローカル保持し、Gitには所在・hash・サイズ・行数のmanifestを保存する。
元DRATはGit管理済みなので、別checkoutでも固定ソースで再変換・再検査できる。
新しいSAT探索は必要ない。過去のtimeout・未監査と記した原記録は保持し、現在の正本K0711だけを更新する。

採用するのは特定の有界近傍CNFのUNSATの独立検査完了である。
固定完全対・除去上限のない1303点の不存在、一般の局所最適性、全体の最大性を証明したとは扱わない。
境界は `1302 <= A(2647) <= 1322` のまま。
K0693/K0702の未完了DRAT監査も進展したと混同しない。

## 次回

同じ3除去近傍のSATや原RUP-only120秒条件は繰り返さない。
次は除去上限4への拡張、同サイズ交換で別の種、別の完全対dを検討する。
独立検査済みのCNF反駁から幾何的な近傍定理を切り出すなら、符号化の一般的拡張可能性を明示して別の知識単位にする。

## 統合検証

uv sync --lockedとknowledge check（697項目、error 0 / warning 0）は成功。
実入力・元DRAT・採用LRAT・ソース・受理receiptの照合、6 DRAT制御と5修正LRAT制御も成功した。
stageしたsourceと証拠のbytesは作業ファイルと一致し、80MB raw LRATのローカル保持とGit除外も確認した。
他者の未追跡shape出力2件は含めていない。
共通unittest33件は307.755秒で全成功した。
build.pyは697項目から6ビューとREADMEを正常に再生成した。変化はgenerated内の2ファイルのみ。
生成物stage後の指定diff 0とstaged whitespace検査の成功を確認し、自分の検証済み変更のみをmainへ直接commitする。
変換・独立証明検査・共通検査は全て終了しており、同じ対象の計算は残していない。
