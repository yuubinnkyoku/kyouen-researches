---
id: K0401
title: 11×11・q=12の極大安全配置の石数範囲103〜114
kind: proposition
status: proved
topics:
- maximum-safe
- maximal-safe
- variants
- strategy-length
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共円・共線q点禁止版の安全配置を使用
artifacts:
- path: research/experiments/geometry/reports/n11-q12-terminal-extremes-20261012.md
  role: proof
  note: 半整数中心による完全列挙と横断集合の両端値の証明
- path: research/experiments/geometry/scripts/verify_n11_q12_terminal_extremes_20261012.py
  role: verifier
  note: 独立2方式による21円列挙、210通りの19円部分集合の排除、両端証人
- path: research/experiments/geometry/output/n11-q12-terminal-extremes-20261012.txt
  role: data
  note: 検証器の実行結果
---

# 11×11・q=12の極大安全配置の最小石数103と最大石数114

標準11×11整数格子の**q=12版**では、極大安全配置の石数は103以上114以下で、両端とも実現する。これは標準q=4版のs_11・K_11の値ではない。

12点を通る円は21本だけで、12点を通る直線や13点以上を通る曲線はない。q>max(w,m)のときに限って成立する円中心の半整数性から441中心を有限完全列挙し、全三点組による独立な整数円生成と一致した。

安全集合の補集合は21円の横断集合。点次数最大3から最小横断集合サイズは7以上、7点の包含極小証人がある。19点以上の包含極小横断集合は、私有円19本がそれぞれ排他的点を持つ必要があるが、19本の選択210通りすべてでこの必要条件が破れる。18点の包含極小証人があるため、最小・最大極大安全サイズは121−18=103、121−7=114。

**石数スペクトルも完全確定**：7〜18点の包含極小横断集合はすべてのサイズで存在する。両端7・18の証人に加えて、8〜17点の10種類の座標証人を直接検証した。各証人が21円をすべて遮り、各点が私有円を持つことを整数ビット集合演算で確認している。したがって、包含極大安全配置の石数集合は厳密に

\[
\boxed{\{103,104,105,106,107,108,109,110,111,112,113,114\}}
\]

であり、中間に欠番はない。安全性は部分集合について下方閉なので、各極大安全配置の石を任意の順番で置く合法対局が存在する。従って**空盤から到達可能な終局手数の集合**も同じ12整数である。ただし各手数を一方のプレイヤーが強制できるという意味ではない。追加の一次資料は [石数スペクトルの証明](../../experiments/geometry/reports/n11-q12-terminal-spectrum-extension-20261012.md) と [座標証人・独立ビット検証器](../../experiments/geometry/scripts/verify_n11_q12_terminal_spectrum_extension_20261012.py)。前者は既存の両端値の証明に依存し、後者は既存の二方式完全円列挙器を再利用する。

証拠は有限完全列挙・明示的証人と数学的帰着であり、11×11・q=12に限定される。空盤勝敗と全Grundyは依然として未解決。
