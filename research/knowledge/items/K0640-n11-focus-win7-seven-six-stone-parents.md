---
id: K0640
title: 11×11中央49の確定WIN7から七つの六石WINを導出（うち六類が追加）
kind: proposition
status: proved
topics: [square-outcomes, certificates, verification, search-methods]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 安全な追加と通常プレイの終局規則
- type: depends_on
  target: K0003
  note: 局所WIN証明と空盤弱解決の区別
- type: depends_on
  target: K0638
  note: 固定七石の元先手WINを全応手・終局まで独立検証した根拠
artifacts:
- path: research/experiments/n11-central-19-cover-20261031/verify_focus_s6_win_refutation.py
  role: verifier
  note: 元となる七石WINの固定終局戦略と4×4整数幾何の独立監査
- path: research/experiments/n11-central-19-cover-20261031/verify_central49_post_seven_win6_repair_2301.py
  role: verifier
  note: 七石の全七親の合法な復帰手、D4正準類の相異、従来138 WIN6との非重複を独立4×4幾何で検査
- path: research/log/2026-11-02-n11-central49-seven-win6-exclusion-and-2301-repair.md
  role: log
  note: 七親への逆向き証明、旧証人集合との交差、証明境界
scope: 標準11×11完全指摘・通常プレイ。元先手WIN7と終局証明された七石0000000000000020380a100000000000から一点を除いた七つの六石正準局面。二石root・空盤は対象外。
evidence: K0638の七石WIN終局証明に基づき、七つの六石親のいずれも欠けた点へ合法に戻せることを4×4整数BareissとD4で検査。七つの正準類は相異なり、既存19 WIN7からの117六石親とK0624/K0627/K0628の21六石WINに重複しない。専用幾何監査CI 41443189538成功。新規六石WINは六類で、既知のK0638六石一類を含む。
---

# 確定した一つの七石戦略を七つの六石親へ持ち上げる

K0638で、元先手WIN7 `0000000000000020380a100000000000` の固定戦略が、元後手の全合法応手を含め終局まで独立検証された。この七石の任意の一点を除いた六石局面では、元先手が除いた点へ置くことで**同じ証明済み七石に戻れる**。したがって七つの六石局面はいずれも元先手WINである。

| 除いた点 | 六石正準鍵 |
| ---: | --- |
| 44 | `0000000000000020380a000000000000` |
| 49 | `00000000000000203808100000000000` |
| 51 | `00000000000000203802100000000000` |
| 59 | `0000000000000020300a100000000000` |
| 60 | `0000000000000020280a100000000000` |
| 61 | `0000000000000020180a100000000000` |
| 69 | `0000000000000000380a100000000000` |

七つの正準類は相異なる。K0638で直接証明した除去点44の六石を除く**六類が新規の帰結**である。七親の幾何・復帰手と旧117+21類との非重複は `verify_central49_post_seven_win6_repair_2301.py` によって独立監査済み（GitHub Actions 41443189538成功）。七親それぞれの終局戦略を新たに七回再生成したのではなく、K0638の固定七石戦略を合法な一手で再利用する構成的証明である。

この七親のうち二類は歴史的な1,980七石条件付きLOSS証人46類に含まれ、当該計画をさらに反証する。六石LOSS・四石LOSS・二石rootの新規閉鎖はない。**標準11×11空盤の勝敗はUNKNOWN。**
