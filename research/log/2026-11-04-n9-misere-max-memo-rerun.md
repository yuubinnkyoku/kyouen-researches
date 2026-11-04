# 2026-11-04 9x9 misère のリソース拡大再実行（UNKNOWN）

 2026-11-04、日付が11/5に跨いだ。2026-10-03の既存2試行（130M上限）と同じ構成で、`search_memo_cap` を
201,326,611 スロット（ソルバ内部のメモ配列サイズ）まで拡張し、相手にパターン外部の 7200 秒時間枠で
中央開幕（opening 40）と角開幕（opening 0）の2プロセスを並行させた（同じWSL/16スレッドマシンに置き、
壁時計は起動ラッパが 7320 秒で watchdog 停止させた）。

## 結果（いずれも未解決・証明書なし・UNKNOWN のまま）
| 開幕 | memo | elapsed | tiny calls | max RSS |
|---|---:|---:|---:|---:|
| 中央 (4,4) 点40 | 200,000,000 に到達 | 1400s | 546,856,176 | 1,635,160 KiB |
| 角 (0,0) 点0 | 200,000,000 に到達 | 未記録（watchdog停止） | 未記録 | 1,635,100 KiB |

両試行とも、watchdog（7320秒＝7200+120）で内部の `seconds=7200` 上限を超過したため外部割り込み
であり、`complete:false`・証明書不在・root_status=UNKNOWN の記録に留まる。
検証鍵・primitive validation（forbidden 29,152 / 1,000標本）はすべて通過し、
ソルバそのものの幾何は正常に来ていた。

## 重要な含み
- メモは 201M 上限（=ソルバのハッシュスロット数）までほぼ到達したにもかかわらず、
  探索自体は終了しなかった。130M上限の旧試行（328秒/メモ約1.6GB）と比較すると約 10 倍の探索領域を
  調査領域下に置いたことになるが、証明書を生まない。
- これは「9x9 misère が難しい」の裏付けではなく、純粋な資源打ち切りである。
  K0311 は open のまま持続する（探索ボトルネックは2試行共通で、tiny calls の増速度は1秒あたり約25M）。

## 再現
```sh
# C++ ソルバの memo 上限を解除済み（2026-11-04の game_structure_20261003_nine.cpp）
python research/experiments/game-structure/scripts/game_structure_20261003_nine_reproduce.py \
  --work-dir /mnt/d/kyouen-n9-center --output /mnt/d/kyouen-n9-center/nine_center_search.json \
  --seconds 7200 --opening 40 --node-cap 201326611 --samples 1000

python research/experiments/game-structure/scripts/game_structure_20261003_nine_reproduce.py \
  --work-dir /mnt/d/kyouen-n9-corner --output /mnt/d/kyouen-n9-corner/nine_corner_search.json \
  --seconds 7200 --opening 0 --node-cap 201326611 --samples 1000
```
