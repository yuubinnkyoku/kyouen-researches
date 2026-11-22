# 巨大ログの格納形式（.log.gz.b64）

SAT model の v 行を含む3本の生ログ（v3n10k10・v2n10k10_unsat・v2n10k10sh7_unsat・各~1.7MB）は、
刊行経路のペイロード制約のため base64(gzip(生ログ)) のテキストファイル `.log.gz.b64` として格納する。
ファイル先頭4行に生ログ・gzip の sha256 と復元コマンドを記してある。base64部はfold -w 120で折り返してある（base64 -d は改行を無視するため復元に影響しない）。

```
grep -v '^#' <name>.log.gz.b64 | base64 -d | gunzip > <name>.log   # byte 完全復元
sha256sum <name>.log   # 先頭行の raw-log sha256 と一致すること
```

それ以外の26本は平文 `.log` のままである。MANIFEST-sha256.txt は刊行ファイルの実ハッシュを記録する
（.gz.b64 の行は b64 ファイル自体のハッシュ）。生ログの事前計算ハッシュは b64 ヘッダ行を参照のこと。
