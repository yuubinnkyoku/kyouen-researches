# 高速レーン y=22 two-token 全称検証器の第二ホスト独立再現（兄弟実行・K1257/K1256 の裏付け拡張）

- 日付: 2026-11-23（毎時並走の高速レーン・単一実行）
- 対象: 単一オーナー宣言 `e1e60cd4` 配下で出版された y=22 全称機体
  （commit A `6360bb32`・K1257・機体 SHA-256 `96d9787f…`）と
  K1256 observed→proved 昇格の証拠基盤。
- 実験dir: `research/experiments/vertical-fiber-two-token-y22-universal-second-host-reproduction-20261123/`（push前に404で空き確認）

## 経緯と判断

y=22 全称は宣言オーナー単一ホストで出版され、K1257/K1256/実験READMEに
「兄弟実行による独立ビルド・第二ホストbyte再現は出版時点でまだ無く、
次回実行の最優先裏付け課題」と正直記載されていた（y=21 edition は第2実行に
よる独立再現を持っていたが、y=22 edition は出版時点で持っていなかった）。
本実行はその課題をそのまま実行した。並走確認: 最新main（HEAD `00e7c7b5`）に
y=22 再現の出版は無く（実験dir・logともに404）、K1256/K1257・y23 skeleton宣言
（`6f79c81f`・並走所有）・Part BZ/CA（長期レーン並走所有）は未接触。

## 実行（.detailは実験dir README + output/reproduction-record.txt 参照）

1. **corpus取得+pin検証**: 12ファイルとも出版pin一致（機体 `96d9787f…`
   53,422B・y21機 git blob `ca5e8284`〔53,269B〕・cand21 blob `38613e92`・
   cand22 blob `fd50358e`、git blob SHAは取得bytesから再算出して照合）。
2. **出版bytesの段階再実行**: 転写検査→preflight（12,012+9,108点 bad 0）→
   census（生成器+pin体裁: `3275cc74…` 791,080B・rows 3,920・433,160点・
   zero_points 216,626・**engine states misses 11,469,227 / hits 22,466,349
   が出版と一致**）→12チェック（5,664,680点 PASS）→フル14チェック
   （6,956,320点・型 797,559・merge 887,200/tail 191,158・C4t clip45違反280
   最初 (60,108,108)）の**全7出版出力が byte 再現**。census 再生成の生stdout
   （rows/states）も本logで採取済み。
3. **自前ビルド**: 出版y21機+出版cand corpusから、失敗閉鎖型変換表
   （全rename・全定数/文脈置換の回数assert・外れたらabort）で機体を自前構築。
   46,170B・SHA-256 `88ce3ed1…`・2回の独立再構築でbyte一致（決定論的）。
   構築の落とし穴: x<21 crop の2箇所・x<=z-22境界の2箇所・R range の
   y=22適合・出版機体が転写marker直後に空行を持たない点など、複数の回数差を
   fail-closed assert が検出し個別修正（修正後は全count一致のまま確定）。
   `ast_compare.py`（docstring除去・commentはpacked tree外）で出版機体と
   **AST同一・rc=0**。
4. **自前ビルド全段階再実行**: 転写 PASS・preflight PASS・census byte同一。
   監査は出版と**`verifier_sha256` のみ**異なる（flat-key差集合の機械検証で
   確認・`88ce3ed1` vs `96d9787f` 埋め込み由来）。**4実行 byte-identical**
   （3同一cwd+隔離tree/env -i/PYTHONHASHSEED=randomでの全pipelineゼロ再生成、
   census engine statesまで一致）。
5. **fail-closed電池**: 自作harness（battery.py・全probe新規スクラッチコピー
   で実施・各probe後に正典bytes/出版bytes/scratch出力のbaseline完全性を再検証）
   で12探針**すべて caught rc=1**、**bad数は出版電池と完全一致**
   （bad 1/1/3,920・C1d 14,869/9,108・merge 59・C4 945・C1 4,898+C2 24,024・
   C1 1,763+C2 24,451・FAIL-CLOSED 3種）。
   P04のみ初回変異が無効（census集合表記はカンマ後に空白なし→`, 43`探索不;
   余計な波括弧付加という変異になったが機体はint解析失敗でrc=1=fail-closed。
   harness側の瑕疵として正直記録し有効変異で即再probe: bad=1捕捉）。
   電池が悪用に使うbaselineは出版bytesと毎回cmp検証、正典treeは無傷。

## 意味（route statement・新規主張なし）

K1256 昇格（observed→proved）の証拠基盤が「単一ホスト・4実行+
電池12種」から「**2ホスト・出版bytes再実行+AST同一自前ビルド+2組の
決定性4実行+2組のfail-closed電池（bad数完全一致）**」に拡張された。
K1257 機体は単一出版のまま改造ゼロ。statusの変更は無し。標準11×11空盤・
二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
3トークン以上・y>=23族・固定幅・q点版は本レーンの範囲外。

## 出版（push直前HEAD再取得・fetch-back全照合）

- commit A: 実験dir正本6ファイル（README.md・build_y22_own.py・
  ast_compare.py・battery.py・output/battery-results-ALL.json・
  output/reproduction-record.txt）。push直前HEAD `00e7c7b5`・
  実験dir/logはpush前に404で空き確認。
- commit B: 本 run log + K1257 item 追記編集（単一ホスト正直記録に
  第二ホスト再現の追記・出版時点の記述は無改稿のまま追記形式）。
- commit C: knowledge README 末尾bullet 1件追記。
- 各commit後に commit-pinned raw URL fetch-back で byte/sha256照合。

## 次のレジューム（着手前に必ず最新main再取得・hourly並走注意）

y=22 第二ホスト独立再現は完結。次の最有力:
(a) **y=23族fit+全称**（seed cand21〔K1248 proved・証明済みseed外挿5連続目
候補〕・fit→全称で2単一オーナー宣言・y23 skeleton宣言 `6f79c81f` は並走所有
なので実行前に成果の有無を最新mainで確認してから着手）、
(b) 横断法則一般補題化（band下端2y+2の帰納構造・pin行数則の一般化・
型系列の階差構造・K1254 FR-XのF±X全称・K1254 order-32 arc gap の追試は
`f1d9e460` で並走が拡張済み）、
(c) C1dアンカーz切片拡張調査（現行 z0∈{8,9,10,15,16,17} の外側）。
3トークン以上・y>=23族全称・固定幅・q点版安定化長は非接触。
