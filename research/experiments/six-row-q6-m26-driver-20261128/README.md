# six-row q=6 6x26 4レーン実行ドライバ（2026-11-28）— 譲渡記録

宣言 `a9dde1d30`（class {0}）/ `f9a982d2b`（class {1}）/ `e61acf82f`（class {2}
minpos-REST）/ `9e703319b`（deep-deficiency k={3,2,1,0}）の実行を目的として
準備したドライバ（`run_lane.py` + `spec_*.json`、82 probe）。

## 経緯

- kissat 4.0.4 公式 linux-amd64（zip sha `63282e51…`、binary sha
  `21da5d98…`）を導入・検証し、エンコーダ決定性統制（meta_c25p11: vars
  53,532 / clauses 187,536）を出版値と bit-exact 照合のうえ、対照再現
  （6x25 class{2} krow=2:4 minpos=11 SAT **3,574,244 conflicts**、出版
  K1217 値と bit-exact）まで完了。attempt-1（275s cap・機械高負荷で
  743,684 conflicts で INDET）を含め生ログを出版
  （class2-rest-lane の `output/rcalib-6x25-c2k4p11_attempt*.txt`）。
- 実行開始後に所有者セッションが class {0} レーンを自ら完了・出版
  （`b3c2d6dce`・kit `six-row-q6-m26-class0-split-20261127`、全12 probe
  INDET honest negative、対照 bit-exact 241.07s）。重複実行のため本
  ドライバのレーン実行は**すべて停止・譲渡**し、部分出力は削除した。
- 残る class {1} / class {2} minpos-REST / deep-deficiency の実行は
  宣言所有者セッションに委ねる（publish-then-execute 単一オーナー規約）。

## 本dirに残すもの

- `run_lane.py` / `spec_*.json`: 82 probe の仕様（再現性の記録）。
- 各レーンdir（class0-lane / class1-lane / class2-rest-lane /
  deepdef-k3210-lane）: byte-clone scripts + 上記対照ログ。

## 判定・scope

verdict 不消費。M_{6,6} ∈ [26, 495] 不変（class {0} の INDET 完了は
所有者セッション出版の通り）。11x11 は全時点 UNKNOWN。
