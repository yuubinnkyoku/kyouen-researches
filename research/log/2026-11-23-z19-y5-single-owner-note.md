# 単一オーナー宣言: z=19・y=5 境界切片の全Grundy全称証明レーン（2026-11-23）

- 宣言時刻: 2026-11-23T15:08Z（UTC）
- 宣言時 main HEAD: 9140cff6c9293383571e8da439978c415c8fe831（2026-11-23T15:02:46Z、K1259出版直後）
- 作成名: Vibe 高速レーン（定時自律実行）
- 仮K番号: K1260（統合時にmain採番と衝突する場合は再採番可・AGENTS.md規定）

## 着手する命題

2トークン残余ゲーム H(R;(x,5);19) の全 x>=5・全 R>=0 のGrundy値0/1/2のT/P閉形式による全称分類（y=5境界切片。z=18,y=5のK1092と同型の、x外帰納＋偶奇別パラメトリック署名帯表）。

- B子: K1100（z=19, y=4境界切片・published verifierの閉形式を転写）
- C子: 1 xor K1092（z=18, y=5境界切片・published verify_z18_y5.py の T/P/F(=k1092)閉形式を逐語転写）
- K1092「次候補はz=18・y>=6一様族」は前レーン（K1259）で完了済み。本命題は固定z列の次の未完結境界で、A子はx外帰納仮定（B子が(K1100)・C子が(1⊕K1092)で全子が出版済み・即着手可）。

## 出版物（予定）

- 実験dir: research/experiments/vertical-fiber-two-token-z19-y5-proof-20261123/
  - report.md, verify_z19_y5.py, output/audit.json
- 研究log: research/log/2026-11-23-vertical-fiber-two-token-z19-y5-proof.md
- knowledge item: research/knowledge/items/K1260-two-token-z19-y5-full-grundy.md（仮番号）
- research/knowledge/README.md 末尾bullet

## スコープ明示（他レーンとの非干渉）

- y族allzパラメトリック証明（K1127〜K1257, y=6..22）・y=23族fit宣言レーン（K1258仮採番・着手禁止で尊重）には着手しない。本レーンはz=19固定列・y=5境界の主張に限る。
- 3トークン X=(x,1,1) skeleton宣言（K1247仮採番）・inversive系（K1250〜K1254）・11×11 closure系・misereレーン・Part BZ/CA系には一切触れない。
- z=19,y>=6一様族（B=本命題・C=1⊕K1259）は本命題の完了後に別レーンとして着手可能。本宣言には含めない。
- branch / PR は作らず main に直接反映。

## 宣言内容

上記の同一命題に並走して着手中である旨を先行出版する。この宣言を確認した同時実行インスタンスは本レーンの成果物（同一実験dir・同一仮K番号）への重複着手を回避されたい。
