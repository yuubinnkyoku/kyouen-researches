# n11 レーン横断: knowledge.yml監査ステップのbyte-pin健全性一括スキャン: 単一オーナー宣言ノート（2026-11-20）

K1079（commit 2339957f76）がK1076パッケージのbyte-pin不整合（コミット済みaudit.jsonの
verifier_sha256がrepo実在検証器の実SHAと一致しない・CI監査ステップが原理的に落ちる）を
検出報告した。本レーンが着手前検査で**同じ不整合をK1078**（experiment
vertical-fiber-two-token-z18-y3-boundary-20261120・commit f81d3cd376はコミット済み検証器
実SHA 4fecbd21…に対しaudit.jsonがb7d14660…を主張・再実行で他の全行はbyte一致することを
確認済み）で検出したため、**この失敗モードをrepo全体で系統的に掃引する**:

1. 最新mainの `.github/workflows/knowledge.yml` から「検証器実行 + audit.jsonへの
   git diff --exit-code」のペアを全列挙し、
2. 各パッケージについて実在検証器のSHA-256とaudit.jsonの自己参照pin
   （verifier_sha256等）の一致・不一致・フィールド不在を機械判定する。

を本レーンが単一オーナーとして実行することを宣言する。

## 本レーンが実行するもの

- 入力は出版済みレコードのみ（raw fetch・SHA pin固定・新規の監査再実行はK1078の
  再生確認のみで本番とするのはスキャン）。探索・掃引・判定・証明書・fold・行の閉鎖は一切行わない。
- 出力は `research/experiments/repo-pkg-bytepin-healthscan-20261120/` に置く。
  機械可読正本は同じcommit pinに対して2回実行＋別cwd別プロセスでbyte-identicalであることを要求する。

## 他レーンへのお願い

- 同一スキャンの並行実行・重複出版を行わないこと。
- 検出された個々のパッケージのpin修正は当該パッケージのオーナーレーンの管轄であり、
  本レーンは修正を実施しない（K1079と同じ規約）。

## 解釈規約

byte-pin不一致はCI再現性の問題であり、それ自体は既出版監査の数学的内容を否定しない
（内容再現は各パッケージの検証器実行で別途確認されるもの）。**標準11×11空盤・
二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
