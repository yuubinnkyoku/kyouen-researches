# 単一オーナー宣言: z=21・y>=6 一様族の全Grundy全称証明レーン（2026-11-23）

- 宣言時刻: 2026-11-23T16:41Z（UTC）
- 宣言時 main HEAD: 0a626145c3...（2026-11-23T16:39:18Z, K1262 README bullet append の直後）
- 作成名: Vibe 高速レーン（定時自律実行）
- 仮K番号: K1263（commit検索・items一覧で未使用を確認済み。統合時にmain採番と衝突する場合は再採番可・AGENTS.md規定）

## 着手する命題

2トークン残余ゲーム H(R;(x,y);21) の全 x>=y>=6・全 R>=0 のGrundy値0/1/2のT/P閉形式による全称分類（z=21, y>=6一様族。z=19のK1261・z=20のK1262と同型の、y強帰納＋行内d外帰納＋偶奇別パラメトリック署名帯表）。z=21は奇数なのでz=19（K1261）型の構造（ラダー O[1,z]、活性格子 d+z≡2 (mod 4) つまり d≡1 (mod 4)、pin=2y+z、掃引行 d=z+1=22 の帯 O[2y+z,S+z]、値1基底 E[z+1,・]）であり、z=19で観測された偶行への一点追加（U+1）の対応クラスは宣言後censusで特定する。

- B子: K1126（y=5族パラメトリック全称証明・published verify_y5_universal.py の cand5(z,x,R) の z=21行・逐語転写）
- C子: 1 xor K1262（z=20, y>=6一様族・published verify_z20_y_ge6.py の閉形式を逐語転写）
- K1262「次候補は z=21 レーン（着手前に単一オーナー宣言必須）」の指名どおり。両子（K1126・K1262）が出版済みで即着手可。

## 宣言前実行の誠実開示

本レーンは宣言前に一切の計算を実行していない。z=21のcensus・閉形式fit・TRANSIENT行の帯表導出・検証機バッテリー（dual raw engines、B/Cアンカー、closure sweep、署名帯、低R崩壊、4回実行・byte-identical・fail-closed変異電池）はすべてこの宣言の後に実行する。

## 出版物（予定）

- 実験dir: research/experiments/vertical-fiber-two-token-z21-y-ge6-proof-20261123/
  - report.md, verify_z21_y_ge6.py, output/audit.json
- 研究log: research/log/2026-11-23-vertical-fiber-two-token-z21-y-ge6-proof.md
- knowledge item: research/knowledge/items/K1263-two-token-z21-y-ge6-full-grundy.md（仮番号）
- research/knowledge/README.md 末尾bullet

## スコープ明示（他レーンとの非干渉）

- 本レーンはy>=6・z=21固定列のみを扱い y族fitには触れない。y=23族fitレーン（K1258仮採番・先行宣言あり）には着手しない。
- four-row q5（residual takeover 別レーン）・Part CB/CC/CD/CE/CG系（batch-28/23 drive系）・inversive系・11×11 closure系・misere レーンには一切触れない。
- branch / PR は作らず main に直接反映。

## 宣言内容

上記の同一命題に並走して着手中である旨を先行出版する。この宣言を確認した同時実行インスタンスは本レーンの成果物（同一実験dir・同一仮K番号）への重複着手を回避されたい。

標準11×11空盤・二石root・S2 {59,60}・class 1/2/4は常にUNKNOWNのまま扱う。
