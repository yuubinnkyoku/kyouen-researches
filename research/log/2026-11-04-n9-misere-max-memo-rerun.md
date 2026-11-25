# 2026-11-04 9x9 misère のリソース拡大再実行（UNKNOWN）

2026-11-04、日付が11/5に跨いだ。2026-10-03の既存2試行（130M上限）と同じ構成で、`search_memo_cap` を
201,326,611 スロット（ソルバ内部のメモ配列サイズ）まで拡張し、同じWSL/16スレッドマシン上で
中央開幕（opening 40）と角開幕（opening 0）の2プロセスを並行させた（起動ラッパの
7200秒＋120秒の externally watchdog で停止、実測 7320秒）。

## 結果（いずれも未解決・証明書なし・UNKNOWN のまま）
| 開幕 | search.json の記録 | resources |
|---|---:|---|
| 中央 (4,4) 点40 | `complete:false, winner:UNKNOWN, interruption:external_watchdog`, memo カウンタはHTTPで計測できず | elapsed 7320.465 s, max RSS 1,634,520 KiB, user 7,888.94 s |
| 角 (0,0) 点0 | `complete:false, winner:UNKNOWN, interruption:external_watchdog` | elapsed 7320.463 s, max RSS 1,635,100 KiB, user 7,888.55 s |

中央開幕の search.log では、メモ5M刻みの進行が記録されており、
200,000,000 に到達（elapsed 1399.958s、tiny calls 546,856,176）した。
検証鍵・primitive validation（forbidden 29,152 / 1,000標本）はすべて通過し、
ソルバそのものの幾何は正常に来ていた。

## 重要な含み
- 二つの開幕ともメモ上限まで実行したが、探索はその後も終了しなかった。
  「130M上限では328秒/メモ約1.6GBだった旧試行」よりはるかに広い領域を走ったが、
  証明書は生まなかった。
- これは「9x9 misère が難しい」の裏付けではなく、純粋な資源打ち切りである。
  K0311 は open のまま持続する。

## 再現
```sh
# C++ ソルバの memo 上限を201Mまで開放済み（2026-11-04の game_structure_20261003_nine.cpp）
python research/experiments/game-structure/scripts/game_structure_20261003_nine_reproduce.py \
  --work-dir /mnt/d/kyouen-n9-center --output /mnt/d/kyouen-n9-center/nine_center_search.json \
  --seconds 7200 --opening 40 --node-cap 201326611 --samples 1000

python research/experiments/game-structure/scripts/game_structure_20261003_nine_reproduce.py \
  --work-dir /mnt/d/kyouen-n9-corner --output /mnt/d/kyouen-n9-corner/nine_corner_search.json \
  --seconds 7200 --opening 0 --node-cap 201326611 --samples 1000
```
