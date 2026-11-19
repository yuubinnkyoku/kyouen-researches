# 残余78行 39-witness掃引の深さ飽和audit（depth-saturation）

2026-11-19。K1059のdepth-10掃引が39 root全てREFUTED-D10とした追加検証として、
同じ39 root・同じ(child,bit)分解・同じrunner v17でdepth 12・14を全78 probe再実行し、
差があった6分岐のみdepth 16で再probeした。

## 疑問

REFUTED-D10はdepth-10内の完全探索に過ぎない。depth>10に先手勝ちが隠れているなら、
この39 rootは以後の照合で「済み」扱いにできない。そこで探索木の深さ飽和を
node同一性で直接測定した: ある深さでnode数が完全一致すれば、それより深い探索は
同じ終端規則で到達不能な部分しか展開していない。

## 方法（全てK1059掃引と同じpin）

- runner v17 git blob c132cc6425eee3feaeef1d697dd74f968cfedb59・cap 30M・
  両AND順序・pilot_d6制御（3,402 nodes・loss=false を各probe前に合格）・生maxbit child。
- driverはK1059出版driver.pyの--depthのみ10→12/14に（timeout 285→270s）変更した版
  （driver-d12.py・driver-d14.py として実行bytesをそのまま出版）。
- 39 root×2順序=78 probeをd12・d14で再実行（records-d12/d14-w0/w1.jsonl・worker-*.log）。
- d12とd14でnode数が異なった6分岐（root 5個、うち1個は両順序）のみさらにdepth 16で
  再probeし、d14とのnode同一性を確認（depth16-residual-branches-20261119.json）。
- 組立: build_depth_saturation_audit_20261119.py（生recordsからaudit JSONを独立生成し、
  pilot gate・78分岐完全被覆・飽和分類の検証assert込み）。

## 結果（正本: depth-saturation-audit-20261119.json、SHA-256 46afc523186cbd68225b70fcecc152951ebb8efde36bd1fc7d47f7f961ab24d5）

- d12総nodes 134,902,159（d10比 +16.4%）・d14総nodes 134,917,058。
  全78 probeで loss=false・uncapped、pilot_d6全件合格。順序矛盾なし。
- **72/78分岐はd12とd14のnode数が完全一致**。残余6分岐も**d14とd16が完全一致**
  （例: root 00000000000000003800220008100000・andclose0: d12 11,661,043 →
  d14 11,665,350 → d16 11,665,350）。
- **したがってこの39 rootのrunner v17探索木は深さ14以内に飽和する。runner v17の
  移動モデル・終端規則の下では全深さで先手勝ちが存在せず、この39 rootは残余78行の
  閉鎖witnessとして永久に使用不能。**（飽和はprobe結果ではなくnode同一性で判定。）

## 訂正: K1059初期出版の「候補供給枯渇」表現について

K1059初期出版文書（実験README.txt・研究log・item・knowledge READMEの該当bullet）
は「残余78行へのadd-one-stone・depth-10レーンのfresh候補供給はこのスコープで枯渇
（全行の被覆候補確実全滅の初波）」と記したが、**この記述は誤り**。resolve5の39本は
matchingの選択に過ぎない: 事前fresh-safe候補4,728本のうち掃引外に4,689本、706 pair辺の
うち未選択667辺、78行すべてのsingleton候補が残る
（n11-residual78-witness39-candidate-supply-scope-audit-20261120 参照）。
正しい帰結は「選択された39-root計画の全滅、かつ本auditによる飽和でこの39 rootの
永久使用不能が確定」であり、**次の一手は39 dead rootを除外したpool再照合（resolve6）**である。

## 解釈規約

- 飽和裏付きのREFUTEDも、各rootからrunner v17移動モデル内で先手勝ちが存在しない
  ことのみを意味する。行のゲーム理論的値（先手必勝/後手必勝/引き分け）には一切言及しない。
  runner移動モデル外の着手はこのauditの対象外。
- 78行は1行も閉じない。frontier 6,213行/492,021・solved S6 1,635・5親target 34/112は
  K1057 fold後のまま不変。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## ファイル

| ファイル | SHA-256 |
|---|---|
| depth-saturation-audit-20261119.json | 46afc523186cbd68225b70fcecc152951ebb8efde36bd1fc7d47f7f961ab24d5 |
| records-d12-w0.jsonl | 63790a060539c81745cff869073eb09ac3e0175d5a1afb531aa0faed37176b7e |
| records-d12-w1.jsonl | 9daa79ec90e464163fec85dd145c379f1d37366964727de0214793f3a8690822 |
| records-d14-w0.jsonl | 712c18311d8026c82ace5de2b83c88142cd7100620fbb7182aec484eed7dbeef |
| records-d14-w1.jsonl | 6a435c2d67c39f269cc520217300c89ee94ede776f92d5160c0e93707b69fb94 |
| worker-d12-w0.log | b99728464a4535dd9ca0e62b5f6d5c50a651a399136b5cdf49641c4858cc6a39 |
| worker-d12-w1.log | b2c8cf8426eee2b914be13fc5b69f7661f488c451881d15da39cec469b519d33 |
| worker-d14-w0.log | c4bd65a57887e4795269a6a01c5693206e3216bd245978609b84bbfef5ccc617 |
| worker-d14-w1.log | 26ffc633b9ccf2307c3745af4149c0a21f8c5158ae4e3a1a13ede8c3b1d58bfb |
| depth16-residual-branches-20261119.json | 5edfcf118b248daf322f8c6e96bfce4f6338f80e82b215b485a736bb8cf2b59a |
| driver-d12.py | ab00550915d2f958e6f8d7e550fe83f95c506f42687fc21ee002fc3954b9b9d8 |
| driver-d14.py | 00a49afb761ae535ebde31a9394d0e251d06f8f6488a5292780f4b7639b37deb |
| build_depth_saturation_audit_20261119.py | 3157c0c7863e04de85fbdbcb35dec222aecf4b7e52e0001dff9fd764322c0a71 |

records-*.jsonl は各depthの生probe記録（root・bit・covered rows・pilot制御・結果を1行1 probeで保持）。
worker-*.log は実行時のwall時間・返却nodesの実行ログ（実験事実そのまま）。
