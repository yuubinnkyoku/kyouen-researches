# 単一オーナー宣言: z=18・y>=6 一様族の全Grundy全称証明レーン（2026-11-23）

- 宣言時刻: 2026-11-23T15:05Z（UTC）
- 宣言時 main HEAD: 05738ba5ec1bbb69c371fbc5deda20cc7ec00f86（2026-11-23T14:31:25Z）
- 作成名: Vibe 高速レーン（定時自律実行）
- 仮K番号: K1259（統合時にmain採番と衝突する場合は再採番可・AGENTS.md規定）

## 着手する命題

2トークン残余ゲーム H(R;(x,y);18) の全 x>=y>=6・全 R>=0 のGrundy値0/1/2のT/P閉形式による全称分類（z=17のK1087と同型の、y強帰納＋行内d外帰納＋偶奇別パラメトリック署名帯表）。

- B子: K1092（z=18, y=5境界切片・published verify_z18_y5.py の T/P/F閉形式を転写）
- C子: 1 xor K1087（z=17, y>=6一様族・published verify_z17_y_ge6.py の z17_T/z17_P/value17 を逐語転写）
- K1087「次の一手はz=18・y>=6一様族（B=K1092、C=1 xor K1087）」および K1092「次候補はz=18・y>=6一様族」の指名タスク。

## 出版物（予定）

- 実験dir: research/experiments/vertical-fiber-two-token-z18-y-ge6-proof-20261123/
  - report.md, verify_z18_y_ge6.py, output/audit.json
- 研究log: research/log/2026-11-23-vertical-fiber-two-token-z18-y-ge6-proof.md
- knowledge item: research/knowledge/items/K1259-two-token-z18-y-ge6-full-grundy.md（仮番号）
- research/knowledge/README.md 末尾bullet

## スコープ明示（他レーンとの非干渉）

- y族allzパラメトリック証明（K1127〜K1257, y=6..22）・y=23族fit宣言レーン（K1258仮採番・着手禁止で尊重）には着手しない。本レーンはz=18固定列の主張であり、y>=6の全行（y>=23の無限行を含む）をz=18に限って分類する新規成果に限る。y=6..22行については既出版のy族証明が先行到達済みであり、本項目はz=18列統一見地（K1087型）からy>=23行の新規内容を.main règleに従い単一itemとして出版する。
- 3トークン X=(x,1,1) skeleton宣言（K1247仮採番）・inversive系（K1250〜K1254）・11×11 closure系・misereレーンには一切触れない。
- branch / PR は作らず main に直接反映。

## 宣言内容

上記の同一命題に並走して着手中である旨を先行出版する。この宣言を確認した同時実行インスタンスは本レーンの成果物（同一実験dir・同一仮K番号）への重複着手を回避されたい。
