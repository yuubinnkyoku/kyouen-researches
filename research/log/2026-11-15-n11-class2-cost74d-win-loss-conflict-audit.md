# cost74d WIN7/LOSS7 のD4衝突監査

cost74dの15個のWIN7-D10 rootを、既存の公開証明記録・LOSS7親持ち上げ・既知LOSS候補表とD4正準形で照合した。座標変換は audit_published_candidates.py と同じ8通り、盤面は121-bit整数で扱い、浮動小数点は使っていない。

## 結果

- cost74d WIN7-D10: **15 root / 15 D4軌道**
- 既存の17 verified manifest: 277件（WIN7 77・LOSS7 200）
- 中央49のLOSS7 parent-lift: 274軌道
- category-1 known-loss候補表: 396軌道（候補分類であり、独立LOSS7証明書とは数えない）

cost74dの15軌道との交差は次のとおり。

| 照合先 | D4交差 |
|---|---:|
| 既存WIN7 77件 | 0 |
| 既存LOSS7 200件 | 0 |
| 中央49 LOSS7 parent-lift 274件 | 0 |
| category-1候補396件 | 0 |
| cost72b WIN7証明書 | 1（意図した再利用） |

唯一の交差はcost74d bit91とcost72b bit85。両者は (x,y)->(x,10-y) で同一正準形 00000000000080811202000020000000 になる。したがってbit91の証明書本体を重ねて公開せず、cost72b bit85の既存証明書を再利用する。cost72bとの和集合に対する新規D4軌道は14。

**この公開範囲でWIN/LOSS衝突は0件。** 既存17 manifest内のWIN7/LOSS7相互、LOSS7と中央49 parent-lift、LOSS7とcategory-1候補、中央49 parent-liftとcategory-1候補の交差も全て0だった。

## 再現と限界

再現スクリプトは入力21ファイルのGit blob SHAを固定し、D4正準化・件数・交差を再計算する。結果JSONに入力SHAと件数を保存した。

これは公開済みmanifestと候補表の範囲監査であり、全raw cache・非公開worker cache・リポジトリ内の全証明書を走査したものではない。S6 frontierは変更していない。category-1候補396件をLOSS7証明書396件と誤読してはならない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class2・class4は引き続き **UNKNOWN**。

成果物:
- audit_cost74d_win_loss_conflicts_20261115.mjs
- cost74d-win-loss-conflict-audit-20261115.json
