# K1168（fold21外部第二検証）のpristine再実行第三検証（2026-11-21）

## 経緯

- 最新mainを確認し、宣言時HEAD 429232fd7e8322f5ca11af567c8e9f4ca6d303ad を固定した。mainへの宣言commitは 3e7447021b82347b38c162e90ace39472cdddb24。
- K1168 item・README・実行log・出版検証器・再構成機を確認。K1168第三検証の先行宣言はなく、fold18/19外部第二検証、fold23/24/25/26、round-5 refsolve、WIN8抽出・行共有監査など宣言済み作業には重複着手しなかった。
- 単一オーナー宣言ノートを先行出版し、既存K1168の第三再現を担当した。新しいK番号は作らない。

## 実施

1. K1168実験dirの5ファイルを固定refから再取得し、Git blob SHA-1とSHA-256を照合。全5点一致。
2. 出版再構成機を固定ref 429232fd7e8322f5ca11af567c8e9f4ca6d303ad で2回実行。W 57 files/13,574,816 bytes、pub 4 files/137,719 bytes。12 blob + 40 SHA-256 pin、fold20機pin subsetを再確認。2 treeはbyte-identical。
3. 出版検証機を改変せず3回実行。run1/run2は同一W・通常環境、run3は別W・隔離cwd/HOME・PYTHONHASHSEED=random。全実行1,394 gates PASS。
4. 3監査出力は各135,723 bytes・SHA-256 80f004403e2538914605a22c0df8d9a86bf575d896eadfc70d14531b92767a63。K1168出版監査正本および3実行間でbyte-identical。
5. 各実行に含まれる2 tamper probes（worklist offset 253・K1124証明書 offset 17522）がfail-closedで通過。計6回の再試験。
6. 検証後のfresh reconstruction controlでも、検証前のW/pub tree digestを再現。

## 実験事実・制約

最初に3回を一括したリモートコマンドは60秒上限でrun2途中にtimeoutした。run1は完了していたが、中断run2の監査出力はなく、成功数には含めなかった。プロセス一覧とscratchを確認して残存プロセスなし・scratch空を確認後、run2とrun3を個別実行し、両方成功した。

CT204のroot filesystem空きは143 MiBだったため、全作業木とscratchを/dev/shmに配置し、CPUは逐次使用。CT199はroot filesystem 100%で読み取りコマンドもtimeoutしたため使用しなかった。

## 結果と限界

K1168の外部第二検証監査を第三の実行環境で3回再現し、入力tree・監査出力のbyte決定性を確認した。これはK1168の第三再現であり、別実装の新しい証明器ではない。

行は1行も新たに閉じない。receipt fold、WIN/LOSS verdict、証明書抽出は行っていない。WIN8-D10は当該8石rootのゲーム木に限る。REFUTED-D10はLOSS証明ではない。nodes・solved・coverage数を勝敗と読まない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はUNKNOWNのまま。**
