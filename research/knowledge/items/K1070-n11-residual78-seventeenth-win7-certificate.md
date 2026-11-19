---
id: K1070
title: "残余74行の第17 WIN7-D10証明書: root 00004000000000821082000000000100 の全60応手を証明書化し、Bareiss二系統とBigIntで三重独立検証（49,591戦略行・SHA-256 21dd2f0e…7c8・38 gate全PASS）。receipt fold前のため残余2行は未閉鎖"
kind: verification
status: verified
topics: [certificates, verification, search-methods, residual-games]
aliases:
  - seventeenth WIN7-D10 certificate for the sole WIN root in the residual78 resolve6 39-live-witness sweep
  - root 00004000000000821082000000000100, child 4000000000821082000000000000, added bit 8
  - blind extraction and triple independent verification: TS Bareiss 4x4, Python exact Bareiss, BigInt 3x3 cofactor
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性・終局規則
- type: depends_on
  target: K1069
  note: 本rootはK1069の39 live witness depth-10掃引で得た唯一のWIN7-D10 root
- type: depends_on
  target: K1066
  note: blind抽出・証明書形式・Bareiss/BigInt独立検証の先行実績と手順
- type: verifies
  target: K1069
  note: K1069がWIN7-D10とした当該7石rootの戦略木を三方式で独立検証
artifacts:
- path: research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/README.md
  role: source
  note: 第17証明書の抽出・三重検証・限界・fold待ちを含む実験正本
- path: research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/certs/win7-root-00004000000000821082000000000100-20261120.n11
  role: proof
  note: 戦略証明書（49,591データ行・1,791,541 bytes・SHA-256 21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8）
- path: research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/output/seventeenth-cert-triple-verification-20261120.json
  role: data
  note: 38 gate全件の機械可読な検証正本。証明書hash、60 subroot、3方式のunion一致、掃引との照合を固定
- path: research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/scripts/build_verify_record_seventeenth_20261120.py
  role: verifier
  note: resolve6・fold9・単一オーナー掃引・証明書・抽出summary・独立検証結果をfail-closedで再集成するbuilder
- path: research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/output/bigint-independent-verification-seventeenth-20261120.json
  role: verifier
  note: BigInt 3×3余因子展開による独立検証結果
- path: research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/output/python-bareiss-replay-seventeenth-20261120.json
  role: verifier
  note: 純Python exact整数Bareissによる全subtree再帰検証結果
- path: research/experiments/n11-residual78-seventeenth-win7-cert-extract-20261120/output/ts-subroot-stats-seventeenth-20261120.jsonl
  role: verifier
  note: TypeScript Bareiss 4×4 subroot検証の全60応手統計
- path: research/experiments/n11-residual78-39livewitness-depth10-sweep-20261120/output/witness-39live-root-depth10-sweep-20261120.json
  role: data
  note: 発見元の39 root×両順序78 probeの単一オーナー掃引正本
scope: >-
  7石D4正準root 00004000000000821082000000000100でsecond moverが手番の局面に限る。
  second moverの全60合法初手から始まる戦略木49,591行をblind抽出し、全subrootを
  三方式で独立検証した有限証明書。標準11×11空盤、一石root、二石root、
  S2、全classの勝敗には拡張しない。証明書が覆う残余S6行2本の閉鎖計上も
  receipt foldの対象であり、本項の対象外。
evidence: >-
  （1）対象root: 00004000000000821082000000000100（7石・D4正準形）、
  child 4000000000821082000000000000 と bit 8 の合成。K1069の39 live witness
  depth-10両順序掃引で唯一のWIN7-D10（両順序uncapped、1,576,372 /
  2,544,178 nodes）。発見元の単一オーナー掃引と追加実行は78/78 probeで
  nodes/loss/cappedがnode-exact一致。
  （2）抽出: repo-verbatim extractorをblind（kill table空）で実行。
  second moverの合法初手60通りを全て処理し、4,250,297 extraction nodes、
  49,591戦略行、fbt_drops=0、全move ok・uncapped。2回の抽出は
  SHA-256 21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8
  でbyte-identical、証明書サイズ1,791,541 bytes。
  （3）独立検証A: TypeScript Bareiss 4×4 subroot分解。60/60 subroot PASS、
  seen 103,152・terminal 17,157・opponent edges 90,499。消費集合と証明書行の
  差分はmissing 0 / extra 0。
  （4）独立検証B: 純Python exact整数Bareissでrootから全subtreeを再帰展開。
  60/60 PASS、visited winner states 150,963、終局石数{13,15,17}、
  union差分0/0。
  （5）独立検証C: BigInt 3×3余因子展開。60/60 PASS、winner states 66,212、
  loser states 19,783、loser reply edges 90,499、terminal 17,157、
  union差分0/0。3方式の状態流量・終局範囲・消費集合は記録上整合。
  （6）fail-closed builderはroot構築、D4正準性、7石、child/bit分解、
  証明書header・49,591行の整列一意性、抽出再実行、3検証器のunion、
  39-root掃引との分類・node数一致、pilot_d6対照等を検査し、38/38 gate PASS。
  （7）限界: fold9後の残余74行中、当該証明書の幾何学的被覆候補は
  00000000000000821082000000000001 と 00000000000000821082000000000004。
  ただし証明書単体は行を閉じない。8つのD4像から1石を除く幾何joinを
  receipt fold側で再導出し、fold10へ計上するまで両行はopenのまま。
  REFUTED-D10はLOSS証明ではない。標準11×11空盤・二石root {49,60}/{59,60}・
  S2 {59,60}・class 1/2/4はUNKNOWNのまま。
---

## 主張

7石root `00004000000000821082000000000100` でsecond moverが手番のとき、
original first moverが必勝する。second moverの全60合法初手を含む戦略木を
証明書に収録し、全subrootを三つの独立方式で検証した。終局はsecond moverが
合法手を持たない状態で、証明書に記録された終局石数は13〜17である。

## 検証境界

これは当該7石rootの有限な戦略証明であり、11×11全体の弱解決ではない。
証明書の行集合と三検証器の消費集合は完全一致したが、残余S6行の閉鎖簿記は
別工程である。単一オーナー宣言に従い、本項の作成ではfold10を実行していない。
fold10の成立前に残余74行を72行へ変更したり、当該2行をclosedと数えたりしない。
