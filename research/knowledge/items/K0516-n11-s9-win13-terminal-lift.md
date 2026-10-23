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


## 2026-10-23: 9石WIN 29件と8石WIN 231件への拡張

既存9個の8石WIN親から到達する9石候補291件を調査し、全合法10石子が終局WINとなる9石局面29件を独立検証した。9石ANDの全子は延べ802辺・相異なる734個の10石WIN。C++4×4とPython3×3整数行列式による終局探索で勝敗・合法手数・個別状態数が一致（合計255,458状態）。9石WIN 29件から8石WIN親231件を導出。旧1,611件の9石WIN一覧に対する差分28件、旧13,501件の8石WIN一覧に対する差分219件。旧294件の8石LOSSとの矛盾0件。旧一覧以外の全cacheに対する新規性は主張しない。

独立証明書・再現手順: research/experiments/n11-s9-win29-lift-20261023/README.md 。証明対象の29根以外の9石候補の敗北側は独立再証明していない。7石WIN・二石rootの新規閉鎖なし。11×11空盤は **UNKNOWN**。

## 2026-10-23: 734個の10石WIN葉の共有終局探索表

29個の9石WIN根の全合法10石WIN子734件を変更せず、終局探索表の共有・D4正準化・禁止組への出現度による着手順を組み合わせた。個別255,458状態から共有55,010状態へ削減（200,448状態、78.47%）。C++4×4整数行列式とPythonの独立3点円方程式で734葉全WIN、状態55,010、参照94,068、再利用39,058、再帰辺93,334が一致。共有なし255,458、共有のみ123,684、共有＋D4で103,277、着手順調整を加えて55,010状態。これらは指定した734葉の終局再計算に関する値であり、証明対象の増加や空盤勝敗を意味しない。

再現: `research/experiments/n11-s9-win29-lift-20261023/reproduce_shared734.sh`。標準11×11空盤は **UNKNOWN**。
