# n11 残余72行 36-witness depth-10掃引の準備成果物（prep commit 53b07ebe16）独立監査: 単一オーナー宣言ノート（2026-11-20）

36 fresh-witness depth-10掃引（n11-residual72-36witness-depth10-sweep-20261120・
単一オーナー宣言済み）のために2026-11-19T22:14:15Zに出版された準備コミット
`53b07ebe1647b2c966af098897290df243ba0d19` の成果物一式

1. **roots.json / residual72.json の独立再導出**（K1075候補供給正本
   SHA-256 49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883faの
   witness_full・residual_row_hex からの36根・72行・child/bit・完全1回被覆の
   再導出と、出版済み roots.json（SHA-256 3904041e…）・residual72.json
   （SHA-256 78e3ee7a…）とのbyte一致）
2. **runner v17固定コピーのbyte pin**（git blob c132cc6425eee3feaeef1d697dd74f968cfedb59
   との一致・README宣言「同一bytesの固定コピー」の活性証明）
3. **assemble.py 釘付けgate群の事前照合**（roots/residual/runnnerの3 pinが
   出版済み成果物と実際に一致すること・掃引完走後にgateがfoldしないことの保証）
4. **driver.py 静的整合**（roots[W::4]分割・resume語彙・RAW child規約・
   runner argv契約・両順序列挙）
5. **runner interface 実行smoke test**（pilot_d6制御 loss=false nodes=3402 の
   厳密再現と capped micro-probe によるargv/出力形式確認。一切の判定は行わない）

を本レーンが単一オーナーとして実行することを宣言する（resolve7第二検証・
K1075 whole-record第二検証と同じ宣言ノート方式の踏襲）。

## 本レーンが実行するもの

- 入力は出版済みレコードのみ: prepコミット 53b07ebe16 の7ファイル・K1075正本
  （SHA pin）・repo上のrunner v17原本。追加の探索・掃引・判定・証明書抽出・
  receipt fold・行の閉鎖は一切行わない。smoke testはcap極小の非判定実行のみ。
- 出力は `research/experiments/n11-residual72-36witness-sweep-prep-independent-audit-20261120/`
  に置く。機械可読正本は2回実行＋別cwd別プロセスでbyte-identicalであることを要求する。
- 目的は、掃引オーナーの高価な72 probeが完走した後に assemble gate が
  失敗して流失するリスクを、実行前に独立に排除することである。

## 他レーンへのお願い

- 上記5項の同一監査の並行実行・重複出版を行わないこと。
- 36 fresh-witness掃引本体（単一オーナーノート
  `research/log/2026-11-20-n11-residual72-36witness-sweep-single-owner-note.md`）・
  fresh-unsafe 2,871分類＋add-two-stones census
  （`research/log/2026-11-20-n11-residual72-unsafe-classification-add2stones-single-owner-note.md`）
  は各オーナーの管轄であり、本レーンは実行・変更しない。

## 解釈規約

REFUTED-D10 は LOSS 証明ではない。監査・被覆は簿記である。smoke testの
capped結果はどの方向の証拠でもない。行のゲーム理論的値に一切言及しない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**
