# 円故障耐性の無界族から計算困難性へ

2026-10-05。K0346の構成・独立監査を完了後、成果をpushする親checkpointを待つ間に一般化した。
最新mainの既存故障耐性研究は正方形全格子盤の一様上界K0328を未解決としている。
ここではarbitrary finite integer point setへの拡張の限界をさらに確定する。

互いに素な零和三つ組という制約を外し、graphのvertexを正10冪、
edgeをendpoint二つの負和という固有パラメータにする。
base10の桁一意性により余分な零和三つ組が生じない。
三次グラフ・反転・整数化を再利用して、pを共有する円blockerを任意graphの辺に対応させた。
一空点解除の最小削除数は、private edge石をendpointへ置き換える論証でvertex cover数と厳密に一致する。

巨大座標を隠して指数時間reductionとしないよう、LCMのbit長を積で評価し
O(n(n+m))と証明した。二つの独立K2追加でSが唯一最大という制限を強制できる。
元空点がp一つだけなら唯一最大性も全一石削除で多項式検査できるため、
決定問題ρ≤hのNP所属も示し、三共線なし・circle-only・唯一最大配置でもNP-completeまで確定した。

n≤5の全1100graphで、graph側全vertex coverと零和側全横断集合の二つの探索を比較した。
101整数盤の全19842四点をshared coreとgeneric Leibnizで二重検査し、全10004三点で非共線確認。
出力を `geometry-frontier-followup-20261005/graph-cover-audit.json` に保存した。
これは全称reductionの支持・独立検査であり、NP完全性を有限観測から推測していない。

K0328の標準正方形全格子盤は引き続きOPEN。
この結果は、局所円blocker横断数を毎回厳密に求める方式が一般に任意graph Vertex Coverを内包することを示す。
一律の安価な局所閉式を探すより、正方形格子の外部飽和や限定されたblocker構造を使う方が価値が高い。
新しい知識単位はK0348（親統合時に必要なら再採番）。
