---
id: K0531
title: 11×11の7個の9石WINを89個の終局WIN葉で独立検証し63個の8石WINを導出
kind: verification
status: verified
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の奇数AND・偶数OR伝播
- type: depends_on
  target: K0516
  note: 既存86個の9石WIN根との比較
- type: depends_on
  target: K0528
  note: 既存10石LOSS葉からの不足境界探索
artifacts:
- path: research/experiments/n11-s9-win7-expansion-20261024/s9-win7.keys
  role: certificate
  note: 9石WIN根7件
- path: research/experiments/n11-s9-win7-expansion-20261024/s10-win89.keys
  role: certificate
  note: 全合法10石WIN子89件
- path: research/experiments/n11-s9-win7-expansion-20261024/s8-win63.keys
  role: certificate
  note: 導出した8石WIN親63件
- path: research/experiments/n11-s9-win7-expansion-20261024/verify.py
  role: verifier
  note: 全子・親・独立終局勝敗の検証
- path: research/experiments/n11-s9-win7-expansion-20261024/frontier_audit.py
  role: verifier
  note: 427個の既存LOSS葉の逆向き構造と最小不足8件の監査
- path: research/experiments/n11-s9-win7-expansion-20261024/audit_coverage.py
  role: verifier
  note: 63親の新規性・504辺の監査
scope: 標準11×11、q=4、完全指摘、通常プレイ、元先手固定視点。指定9石7根と8石親63件のみ。
evidence: 7根の全合法10石子89件をC++4×4整数行列式とPython3×3整数行列式で終局WINと独立検証し、合法手数不一致0。別の盤面再帰C++/Pythonで状態数合計2800が一致。9石ANDの全子WINから7根WIN、8石ORの合法9石WIN子から63親WIN。旧86根由来の687親・凍結8石WIN13501件と重複0、凍結8石LOSS294件と矛盾0。7石親247件への証明辺504本を追加。新規7石閉包・二石root閉鎖0。空盤UNKNOWN。
---

# 7個の9石WINと63個の8石WINを終局から証明

証明根・全合法子・導出親は対応する実験ディレクトリに固定。9石は元先手固定のANDなので89個の10石子がすべてWINなら7根WIN、8石はORなので証明済み9石WIN子を持つ63親もWIN。

427個の既存10石LOSS葉からの逆向き被覆では、8石候補17,338件中、全子が覆われたのは既存38根のみ。最小不足8件の8石候補に9石WIN子が見つかり、その証明を近隣へ広げた。最小不足はLOSSの証拠ではない。

63親は旧86根の8石親687件と重ならず、凍結8石WIN13,501件にも含まれない。7石への証明済み504辺は増加したが、7石の新規全子閉包はない。証明は凍結cache判定に依存しない。二石rootと空盤勝敗は未解決であり、標準11×11空盤はUNKNOWN。

## 2026-10-24：一石交換近傍20根から154個の8石WINを追加

上記7根の一石交換近傍1,963件から、合法10石子の少ない順に111候補を
調査し、20個の新しい9石WIN根を選択した。選択段階の判定を証明として
信用せず、**全246合法辺・相異なる233個の10石子**をC++4×4整数行列式と
Python3×3整数行列式の独立終局再帰で検証した。全233葉WIN、
合法手数不一致0。C++の個別終局探索状態数合計4,985。
固定一覧と再現手順は
`research/experiments/n11-s9-win20-neighbor-20261024/`。

20根から8石WIN親167件を導出。既存93個の9石WIN根由来の
8石WIN750件との重複13件、凍結8石WIN13,501件との重複0件、
凍結8石LOSS294件との矛盾0件。
**指定比較集合に対して154個の8石WINを追加**した。
新規154件を一手戻した7石親600件への被覆辺増分は1,232本。
凍結cacheの勝敗は新証明に使用せず、比較にのみ用いる。
新しい7石局面の全子被覆0、二石root閉鎖0。
**標準11×11空盤はUNKNOWN**。

## 2026-10-24：8石LOSS候補の反対極性を終局で確定（7個の9石WIN、6個の9石LOSS）

既存439個の10石LOSS葉の逆向き被覆と、独立終局証明済み113個の9石WIN根から
8石LOSS候補を選別した。既知の全子被覆38根・8石WIN 904件を除外すると、
最小未被覆は13件だった。8石
`00000000041000001000501000102000` は合法9石子15件のうち
LOSS被覆2件、未被覆13件だったが、後者を終局再計算すると
**9石WIN7件・LOSS6件**。この8石はWIN子を持つため**WIN**であり、
LOSS候補として計算を続けるべきではない。

7個の9石WINは全合法10石子79辺、相異なる63個の10石WIN葉を再計算して証明。
6個の9石LOSSは5個の10石LOSS葉で証人を与えた。
計68葉のC++4×4整数行列式と独立Python3×3整数行列式で
勝敗・合法手数不一致0。C++訪問状態数合計3,152、Python3,122であり、
探索順・対称性が異なるため状態数の一致は要求しない。
7個の9石WINのうち5件は凍結9石WIN 1,611件と重複し、
比較集合に対する新規勝敗は2件。

7根から8石WIN親57件を導出し、凍結8石WIN13,501件との重複43件、
旧113根由来904件との重複0件。**14個の8石WIN**が指定比較集合に追加され、
その7石親63件に**112本の独立終局証明由来の合法辺**を追加した。
5個の10石LOSS葉は既存439葉と重複0。逆向きに9石LOSS
4,273→4,319件（+46）、8石候補17,798→17,978件（+180）、
197個の8石候補へのLOSS被覆+414辺。新たな8石LOSS全子閉包は0、
既知WIN/LOSS矛盾0。

固定入力・検証器・再現手順は
`research/experiments/n11-s8-frontier-13way-20261024/`。
新しい68葉の勝敗は旧cacheを信用せず独立終局再計算し、
旧439葉の逆向き被覆は旧証明を前提とする別の信頼境界として監査した。
7石の新規閉包、二石root閉鎖はない。**標準11×11空盤はUNKNOWN**。
