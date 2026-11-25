---
id: K0486
title: 11盤35個のS8 LOSSの385終局葉証明と246個のS7 LOSSへの伝播を独立検証
kind: verification
status: verified
topics:
- square-outcomes
- certificates
- verification
aliases: []
relations:
- type: depends_on
  target: K0371
  note: 元先手固定の偶奇AND/OR伝播
artifacts:
- path: research/experiments/n11-s8-compact385-pruned1946-20261020/selected385.txt
  role: certificate
  note: 385個のS10 LOSS葉
- path: research/experiments/n11-s8-compact385-pruned1946-20261020/verify_compact385.py
  role: verifier
  note: 全合法応手・双対下界・整数gapの独立検査
- path: research/experiments/n11-s8-to-s7-lift238-20261020/verify_and_lift.py
  role: verifier
  note: 終局葉からの35根の再証明と全7石親列挙
- path: research/experiments/bundle-integration-20261020/n11-compact-validation.txt
  role: log
  note: 今回の再現記録
- path: research/experiments/bundle-integration-20261020/n11-lift-validation.txt
  role: log
  note: 今回のterminal-only実行、旧cache比較を省略
scope: 標準11×11、q=4、通常プレイ・元先手固定視点。指定35個のS8根、終局証明および合法S7親に限定。
evidence: 2026-10-20にC++とPythonで1946終局義務を独立再計算。C++/Pythonの整数gap検査ともUNSAT。別のterminal-only検査も35根・246親でPASS。
---

385個のS10 LOSS葉から指定35個のS8 LOSSを証明し、その合法な7石親246個もLOSSと導ける。終局385葉のPython再計算は34,709状態であり、C++も同じ結果だった。さらに1,561個のS10 WINについてS11 LOSS子を独立検査し、合計1,946個の局面でWIN/LOSSが一致した。

葉被覆の双対下界383に対し、二つの連結成分の整数gapをそれぞれPython/C++の完全探索で排除して最小385を得た。この最小性は資料に定義された35根と全合法S10応手による被覆問題についてのもの。

旧2,232件との比較で新規238件という値は旧cacheの内容に条件付きであり、今回のterminal-only検査はその比較を省略した。246個のS7 LOSSの導出自体は旧cacheを使わない。元のREADME・検査器がS6候補をUNKNOWNと報告する箇所は当時のLOSS集合だけの評価であり、現在のS6 WIN訂正はK0485を参照する。

新しい二石root閉鎖はない。標準11×11空盤はUNKNOWN。385葉の最小性を空盤全体の最小証明書サイズに拡張しない。
