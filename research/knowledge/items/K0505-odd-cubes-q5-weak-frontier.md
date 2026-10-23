---
id: K0505
title: 3次元5点禁止版の7×7×7以降の奇数辺立方盤はどちらが必勝か
kind: question
status: open
topics: [variants, first-moves, search-methods]
aliases: []
relations: []
artifacts:
- path: research/experiments/cube-q5-seven-probe-20261022/README.md
  role: log
  note: 7立方の2石根・35第三手境界・増加予算probe・未検証範囲
- path: research/experiments/cube-q5-seven-probe-20261022/probe.cpp
  role: solver
  note: 343点・6ワードmask・48対称性・遅延四点幾何のbounded exact solver
- path: research/experiments/cube-q5-seven-probe-20261022/probe-7.json
  role: data
  note: "{0,5}は76189展開・400万四点cacheでUNKNOWN"
- path: research/experiments/cube-q5-seven-probe-20261022/probe-7-20m.json
  role: data
  note: "{0,5}は100万展開・18881241四点cacheでもUNKNOWN"
- path: research/experiments/cube-q5-seven-probe-20261022/coverage-7.json
  role: data
  note: 341第三手のうち306手に4石終局応手。残る35手は全てz=6
- path: research/experiments/cube-q5-seven-probe-20261022/regression.json
  role: data
  note: 7立方上の104四点配置・35672追加候補の独立幾何比較と3立方全20二石軌道
- path: research/experiments/cube-q5-seven-probe-20261022/manifest.json
  role: manifest
  note: solver・幾何境界・回帰・実行結果のSHA-256
- path: research/experiments/cube-q5-seven-frontier-20261022/README.md
  role: log
  note: 19軌道化・再開可能な確定memo・df-pn比較・独立部分証明
- path: research/experiments/cube-q5-seven-frontier-20261022/dfpn-weighted-250k.jsonl
  role: data
  note: DFS確定候補を引き継ぎ19三石軌道を各25万展開、全てUNKNOWN
- path: research/experiments/cube-q5-seven-frontier-20261022/manifest.json
  role: manifest
  note: 追加成果とprivate checkpointの所在・hash・独立検査範囲
- path: research/experiments/cube-q5-seven-incremental-20261022/README.md
  role: log
  note: 合法手の差分更新・候補点直接判定・一括checkpoint IOの検証と速度測定
- path: research/experiments/cube-q5-seven-incremental-20261022/regression-direct.json
  role: data
  note: 既知3立方のdf-pn・DFS両方式の独立証明、差分更新照合、旧checkpoint互換性
- path: research/experiments/cube-q5-seven-incremental-20261022/results-search.md
  role: log
  note: 五石根に追加1550万展開、UNKNOWN。最終27264695候補行からの再開方法
- path: research/experiments/cube-q5-seven-incremental-20261022/manifest-search.json
  role: manifest
  note: 終了した各探索結果とprivate checkpointの所在・hash・信頼範囲
- path: research/experiments/cube-q5-seven-balanced-20261023/five-results.md
  role: proof
  note: priorの底4への変更により五石Nと六石Pを閉じ、全証明書を独立Bareiss検査
- path: research/experiments/cube-q5-seven-balanced-20261023/frontier-results.md
  role: log
  note: 4石根2件はUNKNOWN、最終35412458候補行からの再開方法と保存範囲
- path: research/experiments/cube-q5-seven-balanced-20261023/manifest-frontier.json
  role: manifest
  note: 最終private checkpointのhash・header・信頼範囲と追加探索結果
- path: research/experiments/cube-q5-seven-hybrid-20261023/README.md
  role: log
  note: ディスク基礎表・追加確定候補・未確定df-pn推定値を分離した再開方式
- path: research/experiments/cube-q5-seven-hybrid-20261023/regression.json
  role: data
  note: 中断再開と連続探索の一致、基礎表20根の独立証明、tree置換、不正checkpoint拒否
scope: 共平面または共球面5点禁止・通常プレイ、奇数n≥7のn×n×n整数格子
evidence: 7立方の残り35第三手を19軌道化し、再開可能な探索と独立部分証明を作成したが根は未確定
solution:
  board: n×n×n・3次元q=5・奇数n≥7
  level: unsolved
  outcome: unknown
  classification: [root]
  coverage: 7立方{0,5}の残り35第三手を19軌道化。各25万df-pn展開でも全てUNKNOWN
  conditions: 5点共平面または共球面禁止・完全指摘・通常プレイ
  verification: [exact-search]
  certificate: 根はUNKNOWNで勝敗証明書なし。K0506の有限部分証明は別に独立検査済み
  independent_check: K0506の6石N・7石P・17石および18石終端を独立検査。標本幾何・既知3立方の回帰も確認。空盤証明ではない
  note: 5立方のK0503および全偶数辺長のK0502から奇数n≥7の勝敗は従わない
---

全偶数辺長の構成的弱解決はK0502、5×5×5の有限証明書はK0503に記録した。
次の奇数盤7×7×7以降の空盤の勝敗と後手戦略または先手戦略を求める問題は未解決。

7立方の2石根 `{0,5}`（座標(0,0,0),(0,0,5)）について、341第三手のうち306手は
共円または共線の4石終局へ応じられる。残る35手は全てz=6面上で、4手終局では
処理できない。これだけでは2石根も空盤も判定できない。

同根を6ワードmask・48対称性・遅延幾何のexact探索器で処理した。
四点cache上限400万では76,189展開でUNKNOWNとなり、上限を2,000万に上げた
別processでは1,000,000展開、確定memo1,359,510、四点cache18,881,241でも
node上限に達してUNKNOWNだった。探索中の部分確定memoは、根の勝敗証明や
独立検査済み全局面表と混同しない。

7立方の幾何は104四点配置・35,672候補で独立行列式と照合し、探索部分は
既知3立方の全20二石軌道の独立証明書で回帰確認した。これは7立方の全幾何の
網羅検査でも空盤証明でもない。根のUNKNOWNから先手・後手どちらの勝ちも
推定しない。奇数n≥9は今回探索していない。

## 19軌道化と再開可能な境界（2026-10-22追跡）

35第三手を48立方体等長変換で19三石軌道にまとめた。各10万DFS展開と、
第三手34の平面内46第四手への各2万展開ではいずれも根を閉じられなかった。
確定候補3,818,433局面をprivate checkpointとして保存し、そのsnapshotから
19軌道へ各25万の深さ重み付きdf-pn展開を追加した。最終確定候補memoは
8,568,236局面。全19軌道は依然UNKNOWNであり、確定候補の全体は独立未検査。
再開時は確定P/Nだけを再利用し、UNKNOWNは確定cacheへ入れない。

checkpointから抽出した6石N・7石Pと17石極大安全局面は、別のBareiss幾何検査器で
独立検査できた（K0506）。6石Nは三石根69の下の部分木に属するが、三石根69や
二石根・空盤を閉じる証明ではない。17石構成から最大安全石数≥17は従うが、
空盤の勝敗や最大値17は従わない。詳細な再現・失敗prior・検査の範囲は追加artifactを参照。

さらに第三手69の下の五石根 `{0,2,5,26,69}`、`{0,2,5,49,69}`、
`{0,5,26,49,69}` を同snapshotから各100万追加展開したが、3件ともUNKNOWN。
最終のprivate確定候補memoは11,568,207局面。次回再開用の同ファイルを保存したが、
この全ラベルの独立検査ではなく、三石根・二石根・空盤の未解決性を維持する。

再開探索のため、合法手の差分更新と現在の候補点だけの整数幾何判定を実装した。
既知3立方の全20二石軌道についてdf-pn・mobility DFSの各証明を独立検査し、
標本履歴で従来の全再計算との一致とcheckpointの双方向互換性を確認した。
同じprivate seedからの五石根 `{0,2,5,26,69}` の2万展開では、各方式が同じ
11,588,199候補行でUNKNOWNとなった。速度改善は空盤の勝敗を意味しない。

続いて同五石根へ500万df-pn、1000万の候補点直接判定df-pn、50万のmobility DFSを
順に加えたが、全てUNKNOWN。最終のprivate候補memoは27,264,695行で、この全体は
独立未検査。別の100万mobility DFS分岐で得た18石終端だけは独立検査し、
最大安全石数の下界を18へ更新した（K0506）。上位根の弱解決は未達である。

2026-10-23、深さpriorの底を344から4へ変更して再開した。100万展開の後、
追加307,229展開で五石根 `{0,2,5,26,69}` をNと確定。54着手後の六石局面はP。
431,195局面の全証明書を独立Bareiss検査した（K0517）。前日の同五石根UNKNOWNを
更新する結果であるが、三石根69・二石根・空盤は依然未確定。

次に4石根 `{0,2,5,69}`、`{0,5,26,69}` を各200万展開し、前者へさらに
4,890,897展開を加えたがUNKNOWNだった。最後は未確定tree100万件の上限。
最終private候補memo35,412,458行は再開用に保存したが、その全体は独立未検査。

継続のため、基礎表をディスク索引で参照し、追加P/N候補と未確定treeを単一の
Q5HYB1 checkpointへ分離保存する方式を実装した。未確定の作業量推定を確定ラベルへ
変換しない。既知3立方で再開と連続探索の展開数・証明書一致およびtree置換後の
独立証明を確認した。大きな4石根の勝敗は依然未確定である。
