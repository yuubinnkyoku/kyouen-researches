# 11×11: 35 S8 LOSS からの 246 S7 LOSS 逆向き伝播

標準 q=4、完全指摘、通常プレイ、元先手固定視点。空盤勝敗は UNKNOWN。

本フォルダの `roots35.txt` と `selected385.txt` は、完全証明書 `n11-s8-compact385-pruned1946-20261020.zip`（SHA-256 `2ff704ef0a1805556d1cad0b6502add91f68629ac4ba82879801714546aeeb63`）から取り出したもの。

`python3 verify_and_lift.py --archive /path/to/n11-s8-compact385-pruned1946-20261020.zip --terminal-only` で、385個の10石LOSS葉を終局まで再計算し、35個の8石LOSSと246個の7石LOSSを独立検証できる。古いS7 LOSS 2232件との比較には、GitHub mainの `research/experiments/n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt` が必要。main上の所定の実験ディレクトリにこのフォルダを置いて `python3 verify_and_lift.py --archive /path/to/archive.zip` を実行する。

古い2232件に対し新規238件。6石候補 `00000000041000001000401000100000` は49個の7石子のうち45個が既知LOSS（古いcacheに条件付き）で、4個が未確定。新しい6石LOSSや二石root閉鎖はない。
