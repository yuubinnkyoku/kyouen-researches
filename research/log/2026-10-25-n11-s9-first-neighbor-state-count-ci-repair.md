# 2026-10-25：9石終局証明の状態数誤記とCI停止を修正

作業開始時のmainは `eff818f47a81e468af44c1c7e5cca9da0a9e9295`。
AGENTS.md、research/knowledge/README.md、K0023・K0560、最新の11×11証明・統合実験・logを確認。

CI `40175740942` の「Verify n11 S9 terminal neighbor certificate with independent geometry」は
`ValueError: terminal search-state count changed` で停止していた。
`n11-s9-terminal-neighbor-20261025/verify.py` が18葉の探索状態数合計を1192と固定していたため。

保存済み `s10-win18.keys` の18葉を、3×3差分行列式と別実装の4×4 Bareiss整数行列式、
各葉で独立した辞書を使う完全終局再帰で再計算した。両実装の各葉WIN判定・合法着手数・
探索状態数はすべて一致した。

キー昇順の探索状態数：
`56,56,99,64,76,141,62,46,23,49,76,23,71,71,23,37,81,28`。
合計 **1082**。9石根は手番側LOSSであることも3×3版で再確認した。
CIの既存C++検証器は18葉WIN、探索状態数1083と表示する。
探索順の差による状態数の違いを勝敗不一致とは扱わない。

`verify.py` に葉ごとの探索状態数指紋を追加し、合計の誤記を訂正。
実験README・K0560にも訂正を記載した。探索状態数は勝敗や距離を意味せず、
18葉の独立終局判定と合法な親子関係が局所証明の根拠である。

**この記録の時点では変更後のGitHub Actions CIとknowledge生成整合性の成功は未確認。**
二石rootの新規閉鎖は0、標準11×11空盤は **UNKNOWN**。
