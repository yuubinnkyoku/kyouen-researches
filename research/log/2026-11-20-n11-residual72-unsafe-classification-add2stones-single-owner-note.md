# n11 残余72行 fresh-unsafe 2,871本の構造分類と add-two-stones 拡張コスト見積り: 単一オーナー宣言ノート（2026-11-20）

K1075（残余72行のfull cache-join候補供給再構築・正本SHA-256
49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa）の
README「次の一手」第2項として挙げられた未着手課題

1. **fresh-unsafe 2,871本の構造分類**（残余72行のadd-one-stone宇宙
   universe72 = 7,448根のうち、phase-2 join後も未判定かつ
   unsafe_quadruples > 0 の根。四つ組の型別・行毎の需給・幾何構造分類）
2. **残余72行への add-two-stones 拡張のcensusとコスト見積り**
   （8石候補宇宙の規模・safe pool・1行あたり需給・必要probe数の
   見積りと、出版済み掃引記録に基づくprobeコスト分布からの概算）

を本レーンが単一オーナーとして実行することを宣言する
（K1069／K1075と同じ宣言ノート方式の踏襲）。

## 本レーンが実行するもの

- 入力は出版済み正本のみ: K1075候補供給正本（SHA-256 pin）・
  resolve6正本（e85d4bfb…）・resolve5正本（5a2f4815…）・fold9正本
  （24db2352…）・fold10正本（bed7d331…）・sv17 38gate正本
  （c1073bae…）・39 live掃引正本（22953ae1…）・resolve7正本
  （207f4094…）および K0863 scan corpus（repo上の既存manifest・
  published resolve6と同一の信頼境界）。
- 機械は K1075 の `candidate_supply_rebuild_20261120.py`（SHA-256
  0be7230dcc8f7bfe5d889a8709a96918e0fef3995c508fc69b28c710c47715ba・
  raw取得で照合済み）の stage-1〜3 を verbatim 再実行（出力が出版
  正本 SHA-256 と一致することをfail-closedで要求）した上で、
  fresh-unsafe pool と add-two-stones 部分にのみ新しい解析を加える。
- **一切の新規掃引・新規判定・証明書抽出・receipt fold・行の閉鎖は
  行わない。** REFUTED-D10 は LOSS 証明ではなく、被覆・matching は
  簿記である。追加する計算は全て幾何・組合せ・出版記録の集計である。
- 出力は `research/experiments/n11-residual72-unsafe-classification-add2stones-20261120/`
  に置く（実験dir名にK番号は含まない）。機械可読正本は2回実行
  ＋別cwd別プロセスでbyte-identicalであることを要求する。

## 他レーンへのお願い

- fresh-unsafe 2,871本の同一分類と add-two-stones 拡張の同一census/
  コスト見積りの並行実行・重複出版を行わないこと。
- 36 fresh witness 掃引（宣言済み単一オーナーノート
  `2026-11-20-n11-residual72-36witness-sweep-single-owner-note.md`）と
  K1075第二検証（`2026-11-20-n11-residual72-candidate-supply-second-verification-single-owner-note.md`）
  は各オーナーの管轄であり、本レーンはこれらを実行・変更しない。
- add-two-stones 拡張の**実際の掃引着手**は本宣言の対象外とし、
  別途単一オーナー宣言を要する。

## 解釈規約

REFUTED-D10 は LOSS 証明ではない。unsafe候補・safe候補・censusは
条件付き計画の幾何観察であって証明書ではない。行のゲーム理論的値に
一切言及しない。**標準11×11空盤・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
