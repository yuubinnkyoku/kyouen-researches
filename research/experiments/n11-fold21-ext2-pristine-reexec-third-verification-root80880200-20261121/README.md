# K1168（fold21外部第二検証）のpristine再実行第三検証（2026-11-21）

## 位置づけ

対象は [K1168](../../knowledge/items/K1168-n11-fold21-external-second-verification-root80880200.md) のfold21外部第二検証である。K1168の第三実装検証器を改変せず、別の実行環境で再構成・再実行し、出版監査JSONが同じbyteになるかを確認した。

これは**K1168の第三再現**であり、別実装による新しい第三の証明器を作ったという意味ではない。元の検証器が出版社のfold21機・fold20以下の出版機と実装を共有しない第三実装であることはK1168の範囲を引き継ぐ。

単一オーナー宣言は [宣言ノート](../../log/2026-11-21-n11-k1168-fold21-ext2-pristine-reexec-third-single-owner-note.md)（commit 3e7447021b82347b38c162e90ace39472cdddb24）。宣言時のmain HEADは 429232fd7e8322f5ca11af567c8e9f4ca6d303ad。入力再構成にはこの不変commitを固定して使った。

## 出版byteの固定

K1168実験dirの5ファイルを固定refから再取得し、Git blob SHA-1とSHA-256を照合した。全5点が一致した。詳細は [publication-pins.json](output/publication-pins.json)。

| ファイル | bytes | SHA-256 |
|---|---:|---|
| README | 11,812 | 5c4f121fbd2c1479decfe35994695c65ed73c5a01b8690fc1316c6b3c9790e66 |
| 再構成機 | 10,765 | a70b79834bb38fa3b02a563b75ae5cdf528a789e4f65150a5a9bcce775230095 |
| 出版検証機 | 50,946 | 322ad6ca93676ad3bdebcaae23eb91a2f12a17ababc14f430b5029529332482d |
| K1168監査正本 | 135,723 | 80f004403e2538914605a22c0df8d9a86bf575d896eadfc70d14531b92767a63 |
| K1168実行記録 | 5,430 | 1058c67b7f99b0d5dcf4aae74fe50683d01e2d8668ca72d36ff30429d29619f5 |

## 再構成と第三再現

固定ref 429232fd7e8322f5ca11af567c8e9f4ca6d303ad から、出版再構成機を2回独立実行した。

- W入力木: 57 files・13,574,816 bytes・tree SHA-256 c3b4f7cbbe09baa74b4a39dbb9e9c1fde1927d3b882c665c5f564a53d91c54c6
- fold21出版資料木: 4 files・137,719 bytes・tree SHA-256 c3e01b925db1677535cfcd28c293e549dc7ebbc935655b05473941a9ffc2a783
- 12 Git blob pin + 40 SHA-256 pinを再照合。fold20機の12 blob + 37 SHA-256 pinがfold21機の52 pinの部分集合であることも再確認した。
- 2回のW・出版資料木は全ファイルbyte-identical。検証後に行った第三のfresh再構成も、検証前の57-file W digestと出版資料digestを再現した。

出版検証機 verify_fold21_external_20261120.py は、3回とも改変せず実行した。

| 実行 | 入力 | 環境 | 結果 |
|---|---|---|---|
| 1 | W1 | 通常 | 1,394/1,394 PASS |
| 2 | W1 | 同じ作業環境 | 1,394/1,394 PASS |
| 3 | W2 | 別cwd・別HOME・PYTHONHASHSEED=random | 1,394/1,394 PASS |

全実行の出力は135,723 bytes、SHA-256 80f004403e2538914605a22c0df8d9a86bf575d896eadfc70d14531b92767a63 で、K1168の出版監査正本とbyte-identical。3出力同士もbyte-identicalだった。

検証器内のpristine fold21機再実行は各回4回、tamper試験は各回2件。したがって今回の3回で、内部のfold21機再実行12回と、1 byte改変のfail-closed試験6回を再確認した。tamper対象はworklist byte offset 253とK1124証明書 byte offset 17522。監査出力を残さず拒否する既存T gateが全実行で通過した。

第三検証harnessの [harness-audit.json](output/harness-audit.json) は3実行の結果をまとめた時刻非依存の正本である。[reproduction.log](output/reproduction.log) に実行記録を置いた。

## 実行上の事実

最初に3回を一つのリモートコマンドへまとめた際、60秒のコマンド上限に達し、run1完了後・run2途中で中断した。中断run2の監査出力はなく、成功数には含めていない。プロセス一覧とscratchを確認し、残存プロセスなし・scratch空を確認した後、run2とrun3を別々に再実行して完了した。

実行はProxmox CT204、Python 3.13.5、逐次実行。root filesystemの空きが143 MiBだったため、作業木・scratchは /dev/shm に置いた。CT199はroot filesystem 100%かつ読み取りコマンドがtimeoutしたため使用していない。

## 再現方法

リポジトリのルートから、標準ライブラリだけで実行できる。/home/user/work が未使用であることを確認したうえで、harnessが一時symlinkを作成・削除する。--phase all は一括実行、個別phaseは中断後の再開用。

```sh
python3 research/experiments/n11-fold21-ext2-pristine-reexec-third-verification-root80880200-20261121/scripts/verify_k1168_third.py --work-root /dev/shm/k1168-third --phase prepare
python3 research/experiments/n11-fold21-ext2-pristine-reexec-third-verification-root80880200-20261121/scripts/verify_k1168_third.py --work-root /dev/shm/k1168-third --phase run1
python3 research/experiments/n11-fold21-ext2-pristine-reexec-third-verification-root80880200-20261121/scripts/verify_k1168_third.py --work-root /dev/shm/k1168-third --phase run2
python3 research/experiments/n11-fold21-ext2-pristine-reexec-third-verification-root80880200-20261121/scripts/verify_k1168_third.py --work-root /dev/shm/k1168-third --phase run3
python3 research/experiments/n11-fold21-ext2-pristine-reexec-third-verification-root80880200-20261121/scripts/verify_k1168_third.py --work-root /dev/shm/k1168-third --phase finalize
```

harness SHA-256: c4201ad98fb231d62f7fd78e4414843eb1c55f695216d461452fe16eaeecf77d。

## 解釈上の限界

本検証はK1168の入力固定・再構成・監査byte決定性・fail-closed動作の再現であり、receiptを追加適用しない。S6行は1行も新たに閉じていない。新しいWIN/LOSS verdictもない。WIN8-D10は当該8石rootのゲーム木に限り、REFUTED-D10はLOSS証明ではない。nodes数・solved数・coverage数を勝敗と読まない。

**標準11×11空盤、二石root {49,60}・{59,60}、S2 {59,60}、class 1/2/4はすべてUNKNOWNのまま。**
