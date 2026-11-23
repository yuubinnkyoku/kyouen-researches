# 単一オーナー宣言: 一般X低Rミントークン階段定理レーン（2026-11-23）

- 宣言時刻: 2026-11-23 16:46Z
- 宣言時 main HEAD: 4cf21153（2026-11-23T16:40:47Z, z=21 y>=6宣言ノートの直後）
- 作成名: Vibe 高速レーン（定時自律実行）
- 仮K番号: K1264（commit検索・log宣言一覧で未使用を確認済み。K1263はz=21 y>=6一様族レーンが宣言済み。統合時にmain採番と衝突する場合は再採番可・AGENTS.md規定）

## 着手する命題

**定理（ミントークン階段 / min-token staircase）**: 空でない任意の有限多重集合 X（アリティ自由）、任意の z>=0、任意の 0<=R<=z+min(X) に対して
H(R;X;z) = v(ΣX, z, R)（総和S=ΣXの単一トークン残余値）。

証明は閉形式・帯表に依存しない純構造的帰納法:
- **Lemma Z（単一トークン残余のz-shift不変性）**: 全 x>=1, z>=1, 0<=n<=z で v(x,z+1,n)=v(x,z,n)。nについての帰納（単一トークンの子の組がLemma Z自身で組 vicido照合しmexが一致）。
- **min(X)>=2 リフト（アリティ自由）**: 選択肢値集合が単一トークン側と完全一致（デクリメント子は窓 z+min-1<=z+min(child)、C子は (R-1,z-1) で予算ピッタリ）。R強帰納。
- **min(X)=1 基底**: B子（1トークン除去→X\\{1}のz+1残余）の値 v(S-1,z+1,R-1) が Lemma Z で A子値 v(S-1,z,R-1) と一致し、余分な選択肢が集合を変えない。{1}^t全1の場合も同型。

## 位置づけ（既存成果との関係）

- K0832出版の一般X低R縮約「R<=z+1 なら H=単一トークン閉形式」の **窓を z+1 から z+min(X) へ厳密拡張**（min(X)>=2で真の強化）。K0832の定理は本定理の min(X)=任意の場合の弱い下限ではなく、R<=z+1被覆部。
- z切片族（K1087以降・K1259/K1261/K1262）が7例連続で記録した **「低RはR<=z+6で単一トークン一致・一般z版は未証明の観察」を y>=6 の場合として全称証明に昇格**（y>=6なら z+min>=z+6）。
- 既知witness (12,6)@z=17,R=24・(12,6)@z=18,R=25・(14,6)@z=19,R=26・(16,6)@z=20,R=27 はすべて R=z+min+1 に正確に位置し、窓 z+min の鋭さの傍証（境界+1での破壊）。min=1では (2,1)@z=1,R=3（g=2 vs v=0）がK0832「R>=3ではz>=R-1が鋭い」と整合。
- 2トークン (x,y) 行では窓 R<=z+y が行ごとにタイト（y=1..6+で境界+1破壊の実例あり）。y>=23・z>=20の未証明領域も本定理の被覆内。

## 宣言前実行の正直開示

本レーンは宣言前に数値探索を実行済み: T1/T2等価のグリッド検証（σ<=96/z<=45 bad 0・B子値≡A子値の発見）、定理の直接グリッドテスト（多重度<ewig exhaustive 3,745点+ランダム深部3,646点・窓内 bad 0・境界+1破壊23例）、witness表抽出。定理本体の検証器バッテリー（dual raw engines、Lemma Z掃引、定理掃引、z切片witnessアンカー、単一トークン閉形式アンカー、fail-closed変異電池、複数実行byte-identical）はこの宣言の後に実行する。

## 出版物（予定）

- 実験dir: research/experiments/generalx-min-token-lowr-staircase-20261123/
  - report.md, verify_min_token_staircase.py, output/audit.json
- 研究log: research/log/2026-11-23-generalx-min-token-lowr-staircase.md
- knowledge item: research/knowledge/items/K1264-generalx-min-token-lowr-staircase.md（仮番号）
- research/knowledge/README.md 末尾bullet

## スコープ明示（他レーンとの非干渉）

- 本レーンは一般残余ゲームの低R構造のみを扱う。z切片・y族fit・(batch-28/23 drive系)・11×11 closure・inversive・misere・four-row q5 の各レーンには着手しない（ witness値のアンカー照合を除く・読み取り専用）。
- branch / PR は作らず main に直接反映。

## 宣言内容

上記の命題の全称証明（appended実験・検証・出版）に着手する旨を先行出版する。この宣言を確認した同時実行インスタンスは同一成果物（同一実験dir・同一仮K番号）への重複着手を回避されたい。

標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は常にUNKNOWNのまま扱う。
