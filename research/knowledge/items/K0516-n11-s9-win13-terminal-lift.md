---
id: K0516
title: 11×11の9石WINを13個の終局WIN葉で証明し8石WIN親9件へ伝播
kind: verification
status: verified
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の奇数AND・偶数ORの伝播
- type: depends_on
  target: K0372
  note: terminal-only独立証明とsolver-trusted cacheの信頼境界
artifacts:
- path: research/experiments/n11-s9-win13-lift-20261023/certificate.json
  role: certificate
  note: 9石根・13個の10石WIN子・9個の8石WIN親の完全一覧
- path: research/experiments/n11-s9-win13-lift-20261023/verify.py
  role: verifier
  note: 独立整数幾何による全子・終局minimax・伝播検査
- path: research/experiments/n11-s9-win13-lift-20261023/s10-cpp.tsv
  role: data
  note: C++の独立4×4整数行列式による13子の勝敗・状態数
- path: research/experiments/n11-s9-win13-lift-20261023/README.md
  role: source
  note: 再現手順と信頼境界
scope: 標準11×11・q=4・通常プレイ・元先手固定視点。指定9石根と9個の合法8石親に限定。空盤勝敗は含まない。
evidence: 指定9石根の合法な正準10石子13件を全て列挙し、C++4×4とPython3×3整数行列式による終局minimaxで13件全てWIN、状態数合計557、不一致0。9石ANDでWIN、9個の8石親は合法9石WIN子を持つため8石ORでWIN。8件は既存13,501件の8石WIN一覧に未収録。旧294件の8石LOSS一覧との重複0。cache勝敗を信頼しない。
---

9石 `00040000400000821084000002000020` は、全13個の合法10石子が独立終局計算でWINであるためWIN。9個の正準8石親はいずれもこの9石WIN局面を合法な子に持つためWIN。8件は指定した既存13,501件の一覧にないが、全研究資産に対する新規性を主張するものではない。

新たな7石WINや二石rootの閉鎖はない。標準11×11空盤の勝敗は **UNKNOWN**。
