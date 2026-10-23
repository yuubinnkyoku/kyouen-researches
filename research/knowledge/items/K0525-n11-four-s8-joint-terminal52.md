---
id: K0525
title: 標準11×11の4個の8石LOSSは終局52葉で同時証明でき、同じ証明形式で葉数最小
kind: verification
status: verified
topics: [square-outcomes, certificates, verification, provenance]
aliases: []
relations:
- type: depends_on
  target: K0001
  note: 共円4点禁止・合法手と終局規則
- type: depends_on
  target: K0002
  note: 元先手固定の偶数OR・奇数AND極性
- type: depends_on
  target: K0371
  note: 誤ったS7 LOSSからS6 WINへの伝播を排除した固定極性
artifacts:
- path: research/experiments/n11-four-s8-joint-terminal52-20261023/README.md
  role: proof
  note: 四根の完全境界、52葉と下界の定義、再現手順
- path: research/experiments/n11-four-s8-joint-terminal52-20261023/s10-all1017.tsv
  role: data
  note: 全1017合法10石候補の独立終局WIN780・LOSS237と再帰状態数
- path: research/experiments/n11-four-s8-joint-terminal52-20261023/selected52.keys
  role: certificate
  note: 全103個の9石義務を覆う52個の10石LOSS葉
- path: research/experiments/n11-four-s8-joint-terminal52-20261023/dual-weights.tsv
  role: certificate
  note: 25個の重み1と54個の重み1/2で合計52となる有理数双対下界
- path: research/experiments/n11-four-s8-joint-terminal52-20261023/verify_global.py
  role: verifier
  note: 全合法境界・被覆・双対不等式・旧cache矛盾を再検査
- path: research/experiments/n11-four-s8-joint-terminal52-20261023/verify_s10_direct.cpp
  role: verifier
  note: 4×4整数行列式による10石終局探索
- path: research/experiments/n11-four-s8-joint-terminal52-20261023/terminal_geometry.py
  role: verifier
  note: 3×3整数行列式による独立10石終局探索
- path: research/log/2026-10-23-n11-four-s8-joint-terminal52.md
  role: log
  note: 旧53葉との比較、証明範囲、信頼境界
scope: 標準11×11・完全指摘・通常プレイ・元先手固定視点。指定した4個の正準8石局面を10石LOSS葉で同時に証明する形式に限る。空盤勝敗は含まない。
evidence: 4根の全9石合法子は延べ106・相異なる103。そこからの全10石合法子1017件をC++4×4とPython3×3整数行列式で終局まで再計算しWIN780・LOSS237、勝敗・合法手数・状態数の不一致0。52個のLOSS葉で103義務を全被覆。半整数双対は25義務に1、54義務に1/2の重みを与え総和52、237個のLOSS候補の各被覆重みは高々1。従ってこの証明形式で葉数52が厳密最小。旧53相異なる葉との比較で個別状態数12327から12280へ減少。副次的費用最適性はHiGHS計算への依存を残す。
---

# 4個の8石LOSSに対する52葉の最小同時証明

対象の正準8石局面は次の4件。

- `00000000100001821080000020000020`
- `00000000108000821080000020000020`
- `00008000100000821080000020000020`
- `00020000000000821080000020040020`

8石偶数ORがLOSSであるには全9石合法子がLOSSでなければならない。各9石奇数ANDは10石LOSS子を一つ持てばLOSS。4根の9石義務は相異なる103件で、選択した52個の10石LOSS葉は全件を覆う。

10石候補の完全集合は1017件。各候補のWIN/LOSSを独立したC++とPythonで終局まで再計算し、WIN780・LOSS237で完全一致した。選択葉はLOSS237件からのみ取る。

葉数最小性は`dual-weights.tsv`の有理数双対で証明できる。25義務に1、54義務に1/2、その他に0を与えると重み合計は52。どの10石LOSS候補も覆う重みは1以下なので、51葉以下の証明は不可能。証明葉52件が実在するため最小値は52。検証器は全候補の合法性、全子集合の完全性、勝敗、被覆、双対制約を再計算する。

以前の27葉＋13葉＋14葉には重複1件があり、相異なる葉は53件。今回52件で1葉減少。個別終局探索状態数合計も12327から12280へ47減少した。実行時間や共有探索表の同率削減を意味しない。52葉の中で費用12280が最小という副次的主張は整数計画器の結果であり、独立した費用最適性証明はない。

925件の旧比較集合と730件重なり、WIN/LOSS矛盾0。新たな287件はその比較集合に対する増分であり、研究全体の全cacheに対する新規件数とは限らない。

これは4個の8石局面の終局証明であり、二石rootや11×11空盤の勝敗を決定しない。**標準11×11空盤はUNKNOWN**。


## 2026-10-23: 52葉の共有終局探索表を7,948状態へ削減

52葉の集合と103個の9石義務、葉数最小性は変えず、各10石LOSS葉の終局再帰の着手順と盤面共有を変更した。従来の個別12,280状態から、D4正準化・禁止2/3/4点組の出現数に基づく着手順・全葉共有表によって**7,948状態**（35.28%減）となった。同じ探索順で葉ごとに表を分離すると8,967状態であり、共有そのものの寄与は1,019状態（11.36%減）。4×4整数行列式のC++と3×3整数行列式のPythonが52個のLOSS、状態数、再利用数で一致した。固定探索順での計測であって状態数の大域最適性や空盤探索の削減率を主張しない。再現コードは research/experiments/n11-four-s8-shared-tt-20261023/README.md を参照。空盤はUNKNOWN。
