---
id: K0415
title: 11×11空盤の初手D4分類で2軌道をLOSS、19軌道は未確定
kind: proposition
status: computed
topics: [square-outcomes, first-moves, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の交互AND/OR規則
- type: depends_on
  target: K0414
  note: 二石root {60,27} の119手solver-trusted LOSS結果
artifacts:
- path: research/experiments/n11-opening-orbits-weak-solve-20261012/README.md
  role: source
  note: 軌道分類、応手境界、信頼範囲、再現手順
- path: research/experiments/n11-opening-orbits-weak-solve-20261012/scripts/analyze_openings.py
  role: verifier
  note: 独立BoardによるD4 orbitと限定応手boundaryの列挙
- path: research/experiments/n11-opening-orbits-weak-solve-20261012/output/opening-analysis.json
  role: data
  note: 121初手全ての21軌道、各マス、status、sample response boundaries
- path: research/experiments/n11-s4-boundary-direct-20261012/output/root-60-27-loss-proof.json
  role: certificate
  note: "`{60,27}` の119/119第三手LOSS応手表"
- path: research/experiments/n11-central-reply-frontier-20261012/README.md
  role: source
  note: 19初手軌道の中央後手応手境界、代替応手順位、次のexact探索候補
- path: research/experiments/n11-central-reply-frontier-20261012/scripts/analyze_central_reply_frontier.py
  role: verifier
  note: 独立整数幾何で19二石rootのS3/S4境界・119手被覆・cache/raw再利用を再構成
- path: research/experiments/n11-central-reply-frontier-20261012/output/central-reply-frontier.json
  role: data
  note: 19中央応手rootの全第三手表、S4/S5 boundary、未知境界、raw SHA検査、共有量、順位
- path: research/experiments/n11-central-reply-frontier-20261012/scripts/rank_cached_second_replies.py
  role: verifier
  note: current exact S5 cacheから全cache-derived LOSS S4を逆引きし第二手を順位付け
- path: research/experiments/n11-central-reply-frontier-20261012/output/cached-second-reply-ranking.json
  role: data
  note: 485 cache file検査、32 LOSS S4のK0414照合、19初手代表の中央・代替応手候補
- path: research/experiments/n11-central-reply-frontier-20261012/scripts/select_small_s5_probe.py
  role: verifier
  note: 上位中央rootのUNKNOWN S4に必要なS5 exact子数と共有効果を測定
- path: research/experiments/n11-central-reply-frontier-20261012/output/small-s5-probe-readiness.json
  role: data
  note: 9,517 S4 classの現状と、少数S5探索で閉じられる候補の有無
scope: 11×11標準通常版の空盤面における初手マス。現時点で勝敗を確定したのは21 D4軌道中2軌道だけ。
evidence: >-
  11×11 D4の21軌道・121マスを独立幾何で列挙した。二石局面は着手順を入れ替えても局面と次手番が同じなので `{60,27}` LOSS は `{27,60}` LOSSを与える。さらにD4で中心60を固定し、27の軌道 `{27,57,63,93}` 全てを初手LOSSへ移す。従って初手60とこの4マスの2軌道（5/121マス）がLOSS。K0414の `{60,27}` 境界を独立再生成し、19残存軌道の `{first,60}` 全てで119第三手を列挙した。cache-derived S4 LOSS応手被覆は4〜10/119で全root UNKNOWN。現行exact S5 cacheから逆引いた32 LOSS S4 classはK0414の使用32 classと一致し、485 tracked cache fileにstandalone S4 exact cacheはない。23 receipt・176 unique rawのSHA-256とreplay fieldsを再監査し、untracked-local raw参照は0。全 second reply orbitも比較し、最良の非中央応手は `{0,63}` の4/119で、中央応手の上位10/119を超えない。上位3中央rootのUNKNOWN S4は9,322件で、最小でも51個のS5 exact childが未確定、3件以下で閉じる候補は0だったためsolver探索は起動しない。初手60と `{27,57,63,93}` の2軌道（5/121マス）だけがLOSS確定、残る19軌道・116マスは未分類で、空盤面全体の弱解決ではない。
---

独立D4分類は21軌道・121マスを全て覆う。二石位置 `{60,27}` の固定元先手視点LOSSは2手の順序交換で `{27,60}` にも適用できる。D4回転・反射で27は `{27,57,63,93}` に移るため、初手60とこの4マスはLOSSである。

残る19代表は `16,38,49,24,0,26,48,12,25,3,13,2,14,5,15,4,1,37,36`。中央応手rootで既知LOSS S4の被覆が最多なのは `{16,60}`, `{38,60}`, `{49,60}` の各10/119だが、全てUNKNOWNのままである。最大の現行cache hitでも1,168/123,066 S5子（約0.95%）である。上位3 rootで再構成した9,517 S4 classのうち9 LOSS / 186 WIN / 9,322 UNKNOWN。中央応手root以外も比較したが、初手LOSSを示す新しい完全119/119被覆はない。

保存rawの直接再利用とsolver-trusted exact cacheのラベルを区別する。S4 LOSS/WINは既存exact S5子から伝播したラベルで、terminal-only独立minimax証明への置換は行っていない。二石rootが将来WINと判明しても、それだけで空盤初手WINを意味しない。空盤面全体の勝敗、初手の完全分類、独立terminal-only証明は含まない。
