---
id: K0372
title: 11×11 exact境界の独立監査とraw・cache・minimaxの信頼分離
kind: verification
status: verified
topics: [square-outcomes, verification, certificates, provenance]
aliases: []
relations:
- type: verifies
  target: K0371
  note: 撤回の中間S6・上位S4依存、追加loaderと終局ガードを監査
- type: verifies
  target: K0355
  note: 全S4境界と第三手被覆を再生成し、solver/cacheを信頼する葉を分離
- type: depends_on
  target: K0001
  note: 共円・共線4点禁止、完全指摘、通常プレイ
- type: depends_on
  target: K0002
  note: 全層で元の先手に固定した勝敗
artifacts:
- path: research/experiments/n11-independent-exact-audit-20261010/README.md
  role: source
  note: 監査範囲、信頼境界、修正、再現手順
- path: research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py
  role: verifier
  note: 独自整数幾何・D4・AND/OR・ranked証明DAG検査
- path: research/experiments/n11-independent-exact-audit-20261010/scripts/audit.py
  role: verifier
  note: 集計JSONを入力にせずtracked raw/cacheから証拠とfrontierを再構成
- path: research/experiments/n11-independent-exact-audit-20261010/output/audit.json
  role: data
  note: 現行cacheの全行照合と条件付きfrontier再現
- path: research/experiments/n11-independent-exact-audit-20261010/output/source-manifest.json
  role: manifest
  note: 3923 raw sourcesと280 cache sourcesのhash
- path: research/experiments/n11-independent-exact-audit-20261010/output/cache-only-claims.json
  role: data
  note: positive-budget replayまで復元できない2746 S5の個別cache出所
- path: research/experiments/n11-independent-exact-audit-20261010/output/raw-rooted-proof.json.gz
  role: certificate
  note: 2988 S5のranked上位証明。solver exact葉への信頼を残す
- path: research/experiments/n11-independent-exact-audit-20261010/output/third-move-certificate.json
  role: certificate
  note: 119第三手の117 LOSS witnessと2 UNKNOWN
- path: research/experiments/n11-independent-exact-audit-20261010/output/withdrawal-dependencies.json
  role: data
  note: 撤回2 S5、混入48 cache、依存6 S4の完全一覧
- path: research/experiments/n11-independent-exact-audit-20261010/output/legacy-intermediate-s6.json
  role: data
  note: 旧S7 LOSS反転による6 S6 WINの根拠撤回
- path: research/experiments/n11-independent-exact-audit-20261010/output/minimax-s6-win-escalated.json.gz
  role: certificate
  note: S6 WIN一局面のterminalまで閉じた10407-node独立minimax DAG
- path: research/experiments/n11-independent-exact-audit-20261010/output/verification.json
  role: data
  note: hash・raw行・上位DAG・全frontier・7つのminimax certificateの可搬検査
- path: research/experiments/n11-independent-exact-audit-20261010/tests/test_independent.py
  role: verifier
  note: S0..S121三値境界、小盤面全安全状態、誤極性mutant、証明書改変、loader隔離
- path: research/experiments/n11-independent-exact-audit-20261010/tests/test_cache_policy.cpp
  role: verifier
  note: C++ cache隔離・幾何・不正入力・矛盾拒否の実行回帰
scope: 保存solver verdictを前提とした上位幾何・伝播と、明示した少数terminal-leaf certificateのみ。全5734 S5の独立minimaxではない。
---

開始main `ed75f33d9ccc1557df6143a59ec0994f46f28594` の11×11証明体系を、既存solver/geometry/伝播を呼ばない別実装で検査した。S0からS121までの三値AND/ORをBoolean completionで照合し、子0件の偶数LOSS・奇数WINも確認した。1×1〜4×4の全安全状態は独立な手番側DPと一致した。循環、欠けた全子、非合法辺、誤verdict、信頼葉の無断挿入は証明書検査で拒否する。

撤回2 S5の支持をtracked rawとlocal rawで再調査し、直接exactも正しい境界導出も見つからなかった。旧4 S7 LOSS証人の不正反転による中間S6 WINは6局面。2 S5は48個のtracked historical cacheに混入し、6個のreply27 S4 classへ接続する。別のWIN支持を残す4 classと、WINからUNKNOWNへ戻る2 classを区別した。現在の31 LOSS classはこの誤ったWINに依存しない。現行知識への影響はK0355/K0371で明示する。

C++ loader、追加のPython loaderと10手動workflow内mergerの隔離漏れを塞いだ。空の子集合をUNKNOWNにするnonemptyガードも修正した。C++ cacheには盤面・安全性・D4・数値・UNKNOWN・矛盾の入力拒否を加え、exact replayの不安全・盤外入力も拒否する。コンパイル済み隔離表はregistryとの一致をテストし、registry欠落はPythonでもfail closedとする。

別途、C++ `run_cover` の119要素配列を盤面番号0..120で添字参照する範囲外アクセスと、未被覆表示のslot/盤面番号混同を発見した。修正前は同じ31 LOSS classから116/119と誤表示した。配列を全121盤面点の幅に直し、独立集計と同じ117/119・remaining `{100,108}` を実行回帰で確認する。これはS4 verdictの反転とは別のcoverage実装不具合で、修正前出力も反例として保存した。

保存cacheを前提とする全3,384 S4境界の再構成はK0355の現行frontierと一致する。これは**幾何・伝播の独立検証**であり、solver verdict自体の独立証明とは異なる。positive-budget replayおよび正しいraw-rooted導出まで復元できたS5は2,988件で、残る2,746件は保存cache一次出力への信頼を残す。raw-rootedな葉もsolver exact値を信頼する。31 LOSS classのうち、このraw-rooted部分だけで完全に閉じるのは1 class・3 secured verticesで、30 classにはcache-only葉が残る。従って117/119の再現を全体の独立minimax完了に昇格させない。

S5/S6のWIN/LOSS代表4件を2,000 unique-state上限で測定し全てUNKNOWNだった。そのうちS6 `(10448351135500075008,1040)` を30,000上限へ増額して26,577状態・約23.90秒でWINを再計算した。10,407-node DAGはterminalだけを葉とし、solver値を一切前提にせず検査した。これはこの一局面の独立証明であり、残るS5/S6へ一般化しない。両terminal極性を含む11×11の2証明書と、小盤面4空盤の証明書も保存した。

全体の独立minimax certificateには、各exact rootの決定子または完全全子、TTで省略された依存、terminalまでのranked共有DAGを収集し、独立geometry checkerで検査する必要がある。S5全件を無計画に再探索せず、共有・保存容量・生成費用を少数標本で計測する。root `{60,27}` および11×11空盤の勝敗は未確定のままである。
